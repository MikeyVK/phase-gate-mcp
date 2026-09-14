"""Observe check operational success and complete results through real public composition."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from mcp.types import EmbeddedResource, TextContent
from mcp_server.schemas.execution_outputs import RunChecksOutput
from mcp_server.services.check_operation import CheckOperation
from mcp_server.tools.check_tools import RunChecksTool
from pydantic import JsonValue

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from tests.mcp_server.integration.test_scaffold_public_v3 import Composition, invoke
from tests.mcp_server.unit.execution.test_check_service import RecordingRuntime
from tests.mcp_server.unit.execution.test_check_service import compose as build_checks


def compose(
    root: Path,
    pytestconfig: pytest.Config,
    outcomes: tuple[str, ...],
) -> tuple[Composition, RecordingRuntime]:
    executor, selector, runtime = build_checks(root, outcomes)
    names = tuple(f"check_{index}" for index in range(len(outcomes)))
    config = ChecksConfig.model_validate(
        {
            "checks": {
                name: {
                    "adapter_id": "fixture",
                    "capability": "check",
                    "timeout_seconds": index + 3,
                    "default_args": [name],
                }
                for index, name in enumerate(names)
            },
            "profiles": {"renamed": {"checks": list(names)}},
            "profiles_by_extension": {},
            "run_checks": {"default_profile": "renamed"},
        }
    )
    core = RunChecksTool(
        operation=CheckOperation(selector=selector, executor=executor),
        config=config,
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
        "run_checks": {
            "max_items": 5,
            "template_success": "{requested_scope}: {run_status}; profile={selected_profile}",
            "template_failure": "{requested_scope}: {run_status}; error={error_code}",
            "collections": [
                {
                    "field": "results",
                    "heading": "Checks",
                    "item_template": "{check_id}: {status}; args_source={args_source}",
                }
            ],
            "enum_cases": [
                {
                    "field": "error_code",
                    "cases": {
                        "no_configured_checks": "No checks are configured.",
                        "default_profile_missing": "No default check profile is configured.",
                        "selection_invalid": "The check selection is invalid.",
                        "branch_basis_unavailable": "The branch comparison basis is unavailable.",
                        "scope_resolution_failed": "The requested check scope could not be resolved.",
                        "adapter_request_rejected": "An adapter rejected the check request.",
                        "operation_interrupted": "The operation was interrupted.",
                        "termination_unconfirmed": "Process termination was not confirmed.",
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
    return Composition(server, resource, text), runtime


async def run(
    composition: Composition,
    arguments: dict[str, JsonValue],
) -> RunChecksOutput:
    response, cached = await invoke(composition, "run_checks", arguments)
    operation = composition.text.present_text.call_args.kwargs["data"]
    assert isinstance(operation, RunChecksOutput)
    assert cached == operation.model_dump(mode="json")
    assert response.isError is not operation.success
    assert not any(isinstance(item, EmbeddedResource) for item in response.content)
    text = response.content[0]
    assert isinstance(text, TextContent)
    assert str(operation.run_status) in text.text
    return operation


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("outcomes", "status", "success", "code"),
    [
        (("failed", "unavailable"), "incomplete", True, None),
        (("failed", "passed"), "failed", True, None),
        (("failed", "invalid_request", "passed"), "incomplete", False, "adapter_request_rejected"),
        (("failed", "unconfirmed", "passed"), "incomplete", True, "termination_unconfirmed"),
    ],
)
async def test_native_findings_and_internal_failures_keep_distinct_operational_success(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    outcomes: tuple[str, ...],
    status: str,
    success: bool,
    code: str | None,
) -> None:
    marker = tmp_path / "state-evidence.json"
    marker.write_bytes(b'{"unrelated": true}')
    composition, runtime = compose(tmp_path, pytestconfig, outcomes)
    result = await run(
        composition,
        {
            "scope": "configured",
            "args": {"check_0": []},
            "timeout_seconds": 11,
        },
    )
    assert result.success is success and result.run_status == status and result.error_code == code
    assert result.selected_profile == "renamed"
    assert result.requested_targets == () and result.removed_targets == ()
    first = result.results[0]
    assert first.status == "failed" and first.evidence is not None
    assert first.args_source == "caller" and first.effective_args == ()
    assert first.capture is not None and first.capture.exit_code == 1
    assert first.adapter is not None and first.request_rejection is None
    assert first.termination_problem is None
    assert first.coverage is None and first.required_targets == ()
    if code is not None:
        assert result.results[-1].reason == "not_started"
        assert result.results[-1].capture is None and result.results[-1].adapter is None
    if code == "adapter_request_rejected":
        rejected = result.results[1]
        assert rejected.reason == "invalid_request" and rejected.request_rejection
        assert rejected.capture is not None and rejected.capture.exit_code == 2
        assert rejected.message is None and rejected.evidence is None
    assert all(timeout == 11 for _, timeout in runtime.requests)
    assert marker.read_bytes() == b'{"unrelated": true}'


@pytest.mark.asyncio
async def test_empty_branch_retains_no_invocation_and_explicit_nulls(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    composition, runtime = compose(tmp_path, pytestconfig, ("passed",))
    result = await run(composition, {"scope": "branch"})
    assert result.success and result.run_status == "empty_selection"
    assert result.results == () and runtime.requests == []
    assert result.error_code is None and result.error_details is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"scope": "auto"},
        {"scope": "configured", "timeout_seconds": "11"},
        {"scope": "configured", "args": {"check_0": None}},
    ],
)
async def test_malformed_envelope_returns_validation_schema(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    arguments: dict[str, JsonValue],
) -> None:
    composition, runtime = compose(tmp_path, pytestconfig, ("passed",))
    response, cached = await invoke(composition, "run_checks", arguments)
    assert response.isError and cached["error_type"] == "ValidationError"
    assert runtime.requests == []
    resources = [item for item in response.content if isinstance(item, EmbeddedResource)]
    assert len(resources) == 1 and str(resources[0].resource.uri) == "schema://validation"
