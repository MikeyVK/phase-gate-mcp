"""Preserve test selection and native facts through actual public wrappers and cache."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from jsonschema import Draft202012Validator
from mcp.types import EmbeddedResource
from pydantic import JsonValue

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.tests_config import TestsConfig as Config
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.execution.check_selection import FileScopePaths
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    InvocationCancelled,
    InvocationFailed,
    ProcessCapture,
    RunTestsOutput,
    StreamCapture,
    TerminationProblem,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.test_service import TestRunManager as RunManager
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.run_tests_tool import RunTestsTool
from tests.mcp_server.fixtures.test_role_double import RecordingTestRuntime
from tests.mcp_server.integration.test_scaffold_public_v3 import Composition, invoke
from tests.mcp_server.unit.execution.test_test_service import (
    Catalog,
    InterruptedRuntime,
    configuration,
    passed,
)


def compose(
    root: Path,
    pytestconfig: pytest.Config,
    runtime: AdapterProcessRuntime,
    config: Config | None = None,
) -> Composition:
    admitted = configuration() if config is None else config
    core = RunTestsTool(
        manager=RunManager(admitted, Catalog(), runtime, FileScopePaths(root)),
        config=admitted,
    )
    wrapped = ToolErrorHandlerDecorator(
        InputValidationDecorator(
            EnforcementDecorator(core, MagicMock(spec=EnforcementRunner), root),
            input_contract=core.input_contract,
        )
    )
    data = ConfigLoader(pytestconfig.rootpath / ".pgmcp/config").load_presentation_config()
    presentation = data.model_dump(mode="json", by_alias=True)
    presentation["tools"] = {
        "run_tests": {
            "max_items": 5,
            "template_success": "{requested_scope}",
            "template_failure": "{requested_scope}: {error_code}",
            "collections": [
                {
                    "field": "results",
                    "heading": "Tests",
                    "item_template": "{test_id}: {status}; args_source={args_source}",
                }
            ],
            "enum_cases": [
                {
                    "field": "error_code",
                    "cases": {
                        "no_configured_tests": "No test bindings configured.",
                        "no_active_tests": "No active test bindings.",
                        "selection_invalid": "Test selection invalid.",
                        "scope_resolution_failed": "Test scope could not be resolved.",
                        "adapter_request_rejected": "Internal test request rejected.",
                        "operation_interrupted": "Test operation interrupted.",
                        "termination_unconfirmed": "Test termination unconfirmed.",
                    },
                }
            ],
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
        tools=[wrapped],
        resources=[resource],
        publisher=cache,
        presenter=ResponsePresenter(text, SchemaResourcePresenter()),
    )
    return Composition(server, resource, text)


async def run(composition: Composition, arguments: dict[str, JsonValue]) -> RunTestsOutput:
    response, cached = await invoke(composition, "run_tests", arguments)
    operation = composition.text.present_text.call_args.kwargs["data"]
    assert isinstance(operation, RunTestsOutput)
    assert cached == operation.model_dump(mode="json")
    assert response.isError is not operation.success
    assert not any(isinstance(item, EmbeddedResource) for item in response.content)
    assert "run_status" not in cached
    return operation


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["configured", "workspace", "targets"])
async def test_scopes_defaults_and_explicit_inactive_selection_survive_transport(
    tmp_path: Path, pytestconfig: pytest.Config, scope: str
) -> None:
    target = tmp_path / "selected.py"
    target.write_bytes(b"original source")
    runtime = RecordingTestRuntime((passed(), passed()))
    composition = compose(tmp_path, pytestconfig, runtime)
    arguments: dict[str, JsonValue] = {"scope": scope, "args": {"second": []}}
    expected_ids = ("first", "second")
    expected_budgets = [10, 20]
    if scope != "configured":
        arguments.update(tests=["manual", "second"], timeout_seconds=7)
        expected_ids, expected_budgets = ("manual", "second"), [7, 7]
    if scope == "targets":
        arguments["targets"] = ["selected.py"]
    result = await run(composition, arguments)
    assert result.success and result.error_code is None
    assert result.selected_tests == expected_ids
    assert [row.test_id for row in result.results] == list(expected_ids)
    expected_targets = (
        () if scope == "configured" else (str(tmp_path) if scope == "workspace" else str(target),)
    )
    assert all(call.request.model_dump()["targets"] == expected_targets for call in runtime.calls)
    assert [call.timeout_seconds for call in runtime.calls] == expected_budgets
    assert [(row.args_source, row.effective_args) for row in result.results] == [
        ("configured", ("--label", "two words", "")),
        ("caller", ()),
    ]
    assert result.results[0].message == "Native collection succeeded."
    assert result.results[0].external_tools == () and result.results[0].evidence is None
    assert target.read_bytes() == b"original source"


@pytest.mark.asyncio
async def test_native_negative_and_unavailable_are_successful_operations(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    native = [
        {"decision": {"status": "passed", "message": "No tests found."}, "external_tools": []},
        {
            "decision": {"status": "failed", "message": "Native assertions failed."},
            "external_tools": [{"tool_id": "native", "version": "1.2"}],
            "evidence": {"format": "text", "data": "original failure\r\nline two"},
        },
        {
            "decision": {
                "status": "unavailable",
                "reason": "unsupported_input",
                "message": "Native usage rejected.",
            },
            "external_tools": [],
        },
    ]
    runtime = RecordingTestRuntime(
        tuple((json.dumps(row).encode(), code) for row, code in zip(native, (0, 1, 3), strict=True))
    )
    result = await run(
        compose(tmp_path, pytestconfig, runtime),
        {
            "scope": "configured",
            "tests": ["first", "second", "manual"],
            "args": {"first": ["--collect-only", "two words", ""]},
        },
    )
    assert result.success and result.error_code is None
    assert [row.status for row in result.results] == ["passed", "failed", "unavailable"]
    assert result.results[0].message == "No tests found."
    assert result.results[0].effective_args == ("--collect-only", "two words", "")
    assert result.results[1].evidence is not None
    assert result.results[1].evidence.model_dump(mode="json") == native[1]["evidence"]
    assert result.results[2].reason == "unsupported_input"
    assert all(row.capture is not None and row.adapter is not None for row in result.results)
    assert len(runtime.calls) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["rejected", "interrupted", "unconfirmed"])
async def test_partial_results_and_unstarted_obligations_survive_transport(
    tmp_path: Path, pytestconfig: pytest.Config, kind: str
) -> None:
    runtime: AdapterProcessRuntime
    if kind == "rejected":
        rejection = {
            "reason": "invalid_request",
            "details": [{"location": ["args"], "code": "wrong_type"}],
        }
        runtime = RecordingTestRuntime((passed(), (json.dumps(rejection).encode(), 2)))
        code = "adapter_request_rejected"
    else:
        stream = StreamCapture(observed_bytes=4, head="head", tail="", truncated=False)
        capture = ProcessCapture(exit_code=None, stdout=stream, stderr=stream)
        fault = (
            InvocationCancelled(outcome="cancelled", capture=capture, termination_problem=None)
            if kind == "interrupted"
            else InvocationFailed(
                outcome="failed",
                capture=capture,
                termination_problem=TerminationProblem.UNCONFIRMED,
                failure=AdapterCallFailure(
                    reason=AdapterCallFailureReason.TIMEOUT, message="Budget expired."
                ),
            )
        )
        runtime = InterruptedRuntime(fault)
        code = "operation_interrupted" if kind == "interrupted" else "termination_unconfirmed"
    result = await run(
        compose(tmp_path, pytestconfig, runtime),
        {
            "scope": "configured",
            "tests": ["first", "second", "manual"],
        },
    )
    assert result.success is (kind != "rejected") and result.error_code == code
    assert result.results[0].status == "passed"
    assert result.results[1].capture is not None and result.results[1].adapter is not None
    assert result.results[1].evidence is None and result.results[1].external_tools is None
    assert result.results[2].reason == "not_started"
    assert result.results[2].capture is None and result.results[2].adapter is None
    assert result.results[2].effective_args == ("--label", "two words", "")
    if isinstance(runtime, RecordingTestRuntime):
        assert len(runtime.calls) == 2
        assert result.results[1].request_rejection is not None
    else:
        assert isinstance(runtime, InterruptedRuntime) and runtime.calls == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"scope": "configured", "timeout_seconds": "11"},
        {"scope": "configured", "args": {"manual": None}},
        {"scope": "configured", "coverage": True},
    ],
)
async def test_schema_exposure_and_strict_admission_share_one_contract(
    tmp_path: Path, pytestconfig: pytest.Config, arguments: dict[str, JsonValue]
) -> None:
    runtime = RecordingTestRuntime(())
    composition = compose(tmp_path, pytestconfig, runtime)
    schema = composition.server.tools[0].input_schema
    Draft202012Validator.check_schema(schema)
    response, cached = await invoke(composition, "run_tests", arguments)
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
                for name in ("first", "second", "manual")
            },
            "additionalProperties": False,
        }


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["empty", "unselected", "missing"])
async def test_early_refusals_never_launch_and_keep_required_nulls(
    tmp_path: Path, pytestconfig: pytest.Config, kind: str
) -> None:
    runtime = RecordingTestRuntime(())
    config = Config(tests=()) if kind == "empty" else configuration()
    composition = compose(tmp_path, pytestconfig, runtime, config)
    Draft202012Validator.check_schema(composition.server.tools[0].input_schema)
    arguments: dict[str, JsonValue] = {"scope": "configured"}
    expected = "no_configured_tests"
    if kind == "unselected":
        arguments.update(tests=["first"], args={"manual": []})
        expected = "selection_invalid"
    elif kind == "missing":
        arguments.update(scope="targets", targets=["missing.py"])
        expected = "scope_resolution_failed"
    result = await run(composition, arguments)
    assert result.success and result.error_code == expected and runtime.calls == []
    if kind == "missing":
        assert all(row.reason == "not_started" and row.capture is None for row in result.results)
    elif kind == "empty":
        assert result.results == () and result.error_details is None
