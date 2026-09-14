"""Preserve partial fix effects and stop decisions through the real public boundary."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from jsonschema import Draft202012Validator
from mcp.types import EmbeddedResource
from pydantic import JsonValue

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.fixes_config import FixesConfig
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.execution.fix_service import FileFixScopePaths, FixManager
from mcp_server.execution.models import ApplyFixesOutput
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.fix_tools import ApplyFixesTool
from tests.mcp_server.integration.test_scaffold_public_v3 import Composition, invoke
from tests.mcp_server.unit.execution.test_fix_service import (
    Catalog,
    NativeRuntime,
    RecordingRuntime,
    catalog,
    configuration,
    failure,
    passed,
)


def compose(
    root: Path, pytestconfig: pytest.Config, manager: FixManager, config: FixesConfig
) -> Composition:
    core = ApplyFixesTool(manager=manager, config=config)
    wrapped = ToolErrorHandlerDecorator(
        InputValidationDecorator(
            EnforcementDecorator(core, MagicMock(spec=EnforcementRunner), root),
            input_contract=core.input_contract,
        )
    )
    data = ConfigLoader(pytestconfig.rootpath / ".pgmcp/config").load_presentation_config()
    presentation = data.model_dump(mode="json", by_alias=True)
    presentation["tools"] = {
        "apply_fixes": {
            "max_items": 5,
            "template_success": "{requested_scope}",
            "template_failure": "{requested_scope}: {error_code}",
            "collections": [{
                "field": "results", "heading": "Fixes",
                "item_template": "{fix_id}: {status}; args_source={args_source}",
            }],
            "enum_cases": [{
                "field": "error_code",
                "cases": {
                    "no_configured_fixes": "No fix bindings configured.",
                    "selection_invalid": "Fix selection invalid.",
                    "scope_resolution_failed": "Fix scope could not be resolved.",
                    "adapter_request_rejected": "Internal fix request rejected.",
                    "operation_interrupted": "Fix operation interrupted.",
                    "termination_unconfirmed": "Fix termination unconfirmed.",
                },
            }],
        }
    }
    presenter = TextPresenter(config_data=presentation)
    validate_presentation_alignment(
        presenter, (SupportedToolContract(name=core.name, output_model=core.output_model),)
    )
    text = MagicMock(spec=ITextPresenter, wraps=presenter)
    cache = ResponseCacheManager()
    resource = CachedResponseResource(cache)
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(root))),
        tools=[wrapped], resources=[resource], publisher=cache,
        presenter=ResponsePresenter(text, SchemaResourcePresenter()),
    )
    return Composition(server, resource, text)


async def run(composition: Composition, arguments: dict[str, JsonValue]) -> ApplyFixesOutput:
    response, cached = await invoke(composition, "apply_fixes", arguments)
    operation = composition.text.present_text.call_args.kwargs["data"]
    assert isinstance(operation, ApplyFixesOutput)
    assert cached == operation.model_dump(mode="json")
    assert response.isError is not operation.success
    assert not any(isinstance(item, EmbeddedResource) for item in response.content)
    assert "run_status" not in cached and "changed_files" not in cached
    return operation


@pytest.mark.asyncio
async def test_noop_order_and_explicit_empty_args_survive_transport(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    source = tmp_path / "input with spaces.py"
    source.write_bytes(b"unchanged")
    runtime = RecordingRuntime((passed(), passed()))
    config = configuration()
    composition = compose(
        tmp_path, pytestconfig, FixManager(config, Catalog(), runtime, FileFixScopePaths(tmp_path)),
        config,
    )
    result = await run(composition, {
        "scope": "targets", "targets": [source.name, "./" + source.name],
        "fixes": ["second", "first"], "args": {"second": []},
    })
    assert result.success and result.error_code is None
    assert result.selected_fixes == ("second", "first")
    assert [call.request.model_dump() for call in runtime.calls] == [
        {"operation": "repair", "targets": (str(source),), "args": ()},
        {"operation": "repair", "targets": (str(source),), "args": ("two words", "")},
    ]
    assert [call.timeout_seconds for call in runtime.calls] == [20, 10]
    assert all(row.status == "passed" and row.message is None for row in result.results)
    assert result.results[0].args_source == "caller" and result.results[0].effective_args == ()
    assert result.results[1].args_source == "configured"
    assert source.read_bytes() == b"unchanged"


@pytest.mark.asyncio
async def test_native_three_step_chain_reports_partial_writes_without_rollback(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    source = tmp_path / "source with spaces.py"
    original = b"import os\nvalue= 1\nunknown_name\n"
    source.write_bytes(original)
    decoy = tmp_path / "outside_selection.py"
    decoy.write_bytes(original)
    (tmp_path / "ruff.toml").write_text('[lint]\nselect = ["F"]\n', encoding="utf-8")
    formatted = subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--", str(source)],
        cwd=tmp_path, capture_output=True, timeout=15,
    )
    after_format = source.read_bytes()
    linted = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--fix", "--", str(source)],
        cwd=tmp_path, capture_output=True, timeout=15,
    )
    after_lint = source.read_bytes()
    assert formatted.returncode == 0 and linted.returncode == 1
    assert original != after_format != after_lint
    source.write_bytes(original)
    config = FixesConfig.model_validate({
        "fixes": {
            name: {
                "adapter_id": "ruff", "capability": capability,
                "timeout_seconds": 20, "default_args": [],
            }
            for name, capability in (("first", "format"), ("second", "lint"), ("third", "format"))
        }
    })
    runtime = NativeRuntime(source)
    manager = FixManager(
        config, catalog(pytestconfig.rootpath, tmp_path), runtime, FileFixScopePaths(tmp_path)
    )
    result = await run(compose(tmp_path, pytestconfig, manager, config), {
        "scope": "targets", "targets": [source.name], "fixes": ["first", "second", "third"],
    })
    assert result.success and result.error_code is None
    assert [row.status for row in result.results] == ["passed", "failed", "not_executed"]
    assert runtime.observed == [original, after_format]
    assert source.read_bytes() == after_lint and decoy.read_bytes() == original
    failed = result.results[1]
    assert failed.evidence is not None and "F821" in failed.evidence.model_dump_json()
    assert failed.external_tools and failed.external_tools[0].version
    assert failed.capture is not None and failed.capture.exit_code == 1
    assert result.results[2].reason == "not_started" and result.results[2].adapter is None


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", [
    "unavailable", "timeout", "cancelled", "unconfirmed_failure", "rejected"
])
async def test_attempted_effects_survive_faults_and_later_fixes_do_not_start(
    tmp_path: Path, pytestconfig: pytest.Config, kind: str
) -> None:
    source = tmp_path / "source.py"
    source.write_text("original", encoding="utf-8")

    def mutate(number: int) -> None:
        if kind != "rejected" or number == 1:
            source.write_text(f"native step {number}", encoding="utf-8")

    runtime = RecordingRuntime((passed(), failure(kind)), mutate)
    config = configuration()
    manager = FixManager(config, Catalog(), runtime, FileFixScopePaths(tmp_path))
    result = await run(compose(tmp_path, pytestconfig, manager, config), {
        "scope": "targets", "targets": [source.name],
        "fixes": ["first", "second", "third"], "timeout_seconds": 7,
    })
    assert result.success is (kind != "rejected")
    assert len(runtime.calls) == 2 and all(call.timeout_seconds == 7 for call in runtime.calls)
    assert source.read_text(encoding="utf-8") == (
        "native step 1" if kind == "rejected" else "native step 2"
    )
    assert result.results[0].status == "passed"
    row = result.results[1]
    assert row.adapter is not None and row.capture is not None
    assert result.results[2].reason == "not_started" and result.results[2].capture is None
    assert result.results[2].effective_args == ("two words", "")
    expected = {
        "cancelled": "operation_interrupted", "unconfirmed_failure": "termination_unconfirmed",
        "rejected": "adapter_request_rejected",
    }.get(kind)
    assert result.error_code == expected
    if kind == "rejected":
        assert row.reason == "invalid_request" and row.request_rejection is not None
    elif kind == "unavailable":
        assert row.reason == "unsupported_input" and row.evidence is not None
    else:
        assert row.evidence is None and row.external_tools is None


@pytest.mark.asyncio
@pytest.mark.parametrize("arguments", [
    {},
    {"scope": "workspace", "targets": ["file.py"], "fixes": ["first"]},
    {"scope": "targets", "targets": ["file.py"], "fixes": ["first"], "timeout_seconds": "7"},
    {"scope": "targets", "targets": ["file.py"], "fixes": ["first"], "args": {"first": None}},
])
async def test_strict_public_schema_is_reusable_after_invalid_calls(
    tmp_path: Path, pytestconfig: pytest.Config, arguments: dict[str, JsonValue]
) -> None:
    runtime = RecordingRuntime(())
    config = configuration()
    manager = FixManager(config, Catalog(), runtime, FileFixScopePaths(tmp_path))
    composition = compose(tmp_path, pytestconfig, manager, config)
    schema = composition.server.tools[0].input_schema
    Draft202012Validator.check_schema(schema)
    response, cached = await invoke(composition, "apply_fixes", arguments)
    assert response.isError and cached["error_type"] == "ValidationError"
    assert cached["input_schema"] == schema and runtime.calls == []
    resources = [item for item in response.content if isinstance(item, EmbeddedResource)]
    assert len(resources) == 1 and str(resources[0].resource.uri) == "schema://validation"
    if not arguments:
        properties = schema["properties"]
        assert isinstance(properties, dict)
        assert properties["args"] == {
            "type": "object",
            "properties": {
                name: {"type": "array", "items": {"type": "string"}}
                for name in ("first", "second", "third")
            }, "additionalProperties": False,
        }


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["directory", "unselected"])
async def test_complete_admission_precedes_any_write(
    tmp_path: Path, pytestconfig: pytest.Config, kind: str
) -> None:
    source = tmp_path / "source.py"
    source.write_bytes(b"original")
    directory = tmp_path / "directory"
    directory.mkdir()
    runtime = RecordingRuntime(())
    config = configuration()
    manager = FixManager(config, Catalog(), runtime, FileFixScopePaths(tmp_path))
    arguments: dict[str, JsonValue] = {
        "scope": "targets", "targets": [source.name], "fixes": ["first"],
    }
    expected = "selection_invalid"
    if kind == "directory":
        arguments["targets"] = [source.name, directory.name]
        expected = "scope_resolution_failed"
    else:
        arguments["args"] = {"third": []}
    result = await run(compose(tmp_path, pytestconfig, manager, config), arguments)
    assert result.success and result.error_code == expected and runtime.calls == []
    assert source.read_bytes() == b"original"
