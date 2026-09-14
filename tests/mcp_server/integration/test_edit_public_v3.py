"""Observe edit operations through real admission, presentation and cached results."""

from __future__ import annotations

from pathlib import Path
from typing import Literal
from unittest.mock import MagicMock

import pytest
from jsonschema import Draft202012Validator
from mcp.types import EmbeddedResource, TextContent
from mcp_server.tools.edit_tool import SafeEditTool
from pydantic import JsonValue

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.file_writer import WriteHousekeepingIssue
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.mutation_outputs import EditOperationOutput
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.utils.atomic_file_writer import CheckedFileWriter
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.test_edit_operation_v3 import operation as build_operation
from tests.mcp_server.integration.test_scaffold_public_v3 import Composition, invoke


@pytest.fixture
def delivered(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    return load_delivered_template(
        source_suite=suite,
        source_package=suite / "issue",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite",
        template_id="source_notes",
    )


def compose(
    root: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    outcomes: tuple[str, ...] = ("passed",),
    *,
    has_profile: bool = True,
) -> Composition:
    service, _ = build_operation(root, outcomes, has_profile=has_profile)
    core = SafeEditTool(operation=service, catalog=delivered.catalog)
    wrapped = ToolErrorHandlerDecorator(
        InputValidationDecorator(
            EnforcementDecorator(core, MagicMock(spec=EnforcementRunner), root),
            input_contract=core.input_contract,
        )
    )
    data = ConfigLoader(pytestconfig.rootpath / ".pgmcp/config").load_presentation_config()
    config = data.model_dump(mode="json", by_alias=True)
    summary = (
        "{path}: written={written}; changed={content_changed}; policy={validation_policy}; "
        "validation={validation_status}; profile={profile_id}; source={selected_source}; "
        "error={error_code}"
    )
    config["tools"] = {
        "safe_edit_file": {
            "max_items": 5,
            "template_success": summary,
            "template_failure": summary,
            "enum_cases": [
                {
                    "field": "error_code",
                    "cases": {
                        "context_invalid": "The selected context was rejected.",
                        "target_invalid": "The requested target was rejected.",
                        "target_exists": "The output already exists.",
                        "render_failed": "Rendering failed.",
                        "preparation_failed": "Mutation preparation failed.",
                        "validation_blocked": "Output checks prevented persistence.",
                        "persistence_failed": "The output could not be saved.",
                        "adapter_request_rejected": "An adapter rejected the check request.",
                        "termination_unconfirmed": "Process termination was not confirmed.",
                        "operation_interrupted": "The operation was interrupted.",
                        "original_unreadable": "The original file could not be read.",
                        "original_changed": "The original file changed.",
                        "original_missing": "The original file is missing.",
                        "edit_invalid": "The requested edit could not be constructed.",
                    },
                }
            ],
            "collections": [
                {
                    "field": "checks",
                    "heading": "Checks",
                    "item_template": "{check_id}: {status}; args_source={args_source}",
                },
                {
                    "field": "housekeeping",
                    "heading": "Cleanup",
                    "item_template": "{purpose}: {path}; {message}",
                },
            ],
        }
    }
    presenter = TextPresenter(config_data=config)
    validate_presentation_alignment(
        presenter, (SupportedToolContract(name=core.name, output_model=core.output_model),)
    )
    text = MagicMock(spec=ITextPresenter, wraps=presenter)
    cache = ResponseCacheManager()
    resource = CachedResponseResource(cache)
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(root))),
        tools=[wrapped],
        resources=[resource],
        publisher=cache,
        presenter=ResponsePresenter(text, SchemaResourcePresenter()),
    )
    return Composition(server, resource, text)


async def edit(
    composition: Composition,
    command: dict[str, JsonValue],
    *,
    policy: str = "enforce",
    template_id: str | None = None,
) -> EditOperationOutput:
    arguments: dict[str, JsonValue] = {
        "path": "notes.md",
        "operation": command,
        "validation": policy,
    }
    if template_id is not None:
        arguments["template_id"] = template_id
    response, cached = await invoke(composition, "safe_edit_file", arguments)
    operation = composition.text.present_text.call_args.kwargs["data"]
    assert isinstance(operation, EditOperationOutput)
    assert cached == operation.model_dump(mode="json")
    assert response.isError is not operation.success
    assert not any(isinstance(item, EmbeddedResource) for item in response.content)
    summary = response.content[0]
    assert isinstance(summary, TextContent)
    assert f"written={operation.written}" in summary.text
    assert f"validation={operation.validation_status}" in summary.text
    assert operation.validation_policy in summary.text
    return operation


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("command", "expected", "outcome", "policy", "changed"),
    [
        (
            {
                "op": "replace",
                "target_content": "alpha",
                "replacement": "new",
                "search_window": [1, 1],
            },
            "new\nbeta\n",
            "passed",
            "enforce",
            True,
        ),
        (
            {"op": "append", "content": "tail"},
            "alpha\nbeta\ntail\n",
            "passed",
            "enforce",
            True,
        ),
        (
            {"op": "rewrite", "content": "alpha\nbeta\n"},
            "alpha\nbeta\n",
            "passed",
            "enforce",
            False,
        ),
        (
            {"op": "pattern_replace", "pattern": "beta", "replacement": "changed"},
            "alpha\nchanged\n",
            "failed",
            "report",
            True,
        ),
    ],
    ids=["replace-window", "append", "rewrite-no-change", "pattern-report"],
)
async def test_public_operations_preserve_binding_and_actual_write_facts(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    command: dict[str, JsonValue],
    expected: str,
    outcome: str,
    policy: Literal["enforce", "report"],
    changed: bool,
) -> None:
    target = tmp_path / "notes.md"
    target.write_bytes(b"alpha\nbeta\n")
    composition = compose(tmp_path, pytestconfig, delivered, (outcome,))
    result = await edit(composition, command, policy=policy, template_id="source_notes")
    assert result.success and result.written and result.content_changed is changed
    assert target.read_bytes() == expected.encode("utf-8")
    assert result.selected_source == "input" and result.selection_reason is None
    assert result.error_code is None and result.error_details is None
    assert result.validation_status == outcome and result.profile_id == "renamed"
    assert result.checks[0].invocation is not None
    assert result.checks[0].request_rejection is None
    assert result.checks[0].termination_problem is None


@pytest.mark.asyncio
@pytest.mark.parametrize("has_profile", [True, False], ids=["failed-check", "no-profile"])
async def test_default_enforce_preserves_original_and_selection(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    has_profile: bool,
) -> None:
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    composition = compose(
        tmp_path,
        pytestconfig,
        delivered,
        ("failed",),
        has_profile=has_profile,
    )
    response, cached = await invoke(
        composition,
        "safe_edit_file",
        {"path": target.name, "operation": {"op": "rewrite", "content": "proposed"}},
    )
    result = composition.text.present_text.call_args.kwargs["data"]
    assert isinstance(result, EditOperationOutput) and cached == result.model_dump(mode="json")
    assert response.isError and result.error_code == "validation_blocked"
    assert result.validation_policy == "enforce" and result.error_details is None
    assert result.content_changed is None and target.read_bytes() == b"original"
    assert result.selected_source == ("extension" if has_profile else "none")
    assert result.validation_status == ("failed" if has_profile else "not_executed")


@pytest.mark.asyncio
async def test_construction_feedback_survives_the_cache(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
) -> None:
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    result = await edit(
        compose(tmp_path, pytestconfig, delivered),
        {"op": "replace", "target_content": "absent", "replacement": "new"},
        policy="report",
    )
    assert result.error_code == "edit_invalid" and result.error_details is not None
    details = result.error_details.model_dump(mode="json")
    assert details["reason"] == "missing_match"
    assert details["context"] == [{"line_number": 1, "text": "original"}]
    assert result.checks == () and result.content_changed is None and not result.written
    assert target.read_bytes() == b"original"


@pytest.mark.asyncio
async def test_concurrent_original_change_retains_passed_checks(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    actual = CheckedFileWriter.replace_if_unchanged

    def intervene(
        self: CheckedFileWriter,
        path: Path,
        expected_original: bytes,
        content: str,
    ) -> tuple[WriteHousekeepingIssue, ...]:
        path.write_bytes(b"competing")
        return actual(self, path, expected_original, content)

    monkeypatch.setattr(CheckedFileWriter, "replace_if_unchanged", intervene)
    result = await edit(
        compose(tmp_path, pytestconfig, delivered),
        {"op": "rewrite", "content": "proposed"},
    )
    assert result.error_code == "original_changed" and result.validation_status == "passed"
    assert not result.written and result.content_changed is None
    assert target.read_bytes() == b"competing"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extra",
    [
        {"mode": "verify_only"},
        {"template_id": "unknown"},
        {"path": "/outside"},
        {
            "operation": {
                "op": "replace",
                "target_content": "a",
                "replacement": "b",
                "search_window": ["1", 1],
            }
        },
    ],
    ids=["legacy-mode", "unknown-template", "absolute-path", "strict-window"],
)
async def test_target_input_rejects_legacy_and_unadmitted_values(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    extra: dict[str, JsonValue],
) -> None:
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    arguments: dict[str, JsonValue] = {
        "path": target.name,
        "operation": {"op": "rewrite", "content": "proposed"},
        **extra,
    }
    response, cached = await invoke(
        compose(tmp_path, pytestconfig, delivered),
        "safe_edit_file",
        arguments,
    )
    assert response.isError and cached["error_type"] == "ValidationError"
    assert target.read_bytes() == b"original"
    resources = [item for item in response.content if isinstance(item, EmbeddedResource)]
    assert len(resources) == 1 and str(resources[0].resource.uri) == "schema://validation"
    schema = cached["input_schema"]
    assert isinstance(schema, dict) and not Draft202012Validator(schema).is_valid(arguments)
