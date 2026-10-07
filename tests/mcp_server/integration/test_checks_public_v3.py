"""Observe check operational success and complete results through real public composition."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from mcp.types import EmbeddedResource, TextContent
from pydantic import JsonValue, ValidationError

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.git import BranchChanges, IBranchChangeReader
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.execution.check_selection import CheckSelector
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.execution_outputs import RunChecksOutput, SelectionCheckResult
from mcp_server.server import MCPServer
from mcp_server.services.check_operation import CheckOperation
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.check_tools import RunChecksTool
from tests.mcp_server.integration.test_scaffold_public_v3 import Composition, invoke
from tests.mcp_server.unit.execution.test_check_selection import configured_checks
from tests.mcp_server.unit.execution.test_check_selection import selector as build_selector
from tests.mcp_server.unit.execution.test_check_service import EmptyBranch, RecordingRuntime
from tests.mcp_server.unit.execution.test_check_service import compose as build_checks


def compose(
    root: Path,
    pytestconfig: pytest.Config,
    outcomes: tuple[str, ...],
    *,
    config_override: ChecksConfig | None = None,
    selector_override: CheckSelector | None = None,
    branch: IBranchChangeReader | None = None,
    filtered_checks: frozenset[str] = frozenset(),
) -> tuple[Composition, RecordingRuntime]:
    executor, selector, runtime = build_checks(
        root, outcomes, branch=branch, filtered_checks=filtered_checks
    )
    names = tuple(f"check_{index}" for index in range(len(outcomes)))
    config = ChecksConfig.model_validate(
        {
            "configured_targets": {
                "fixture": {"include": ["**"], "exclude": []},
                "filtered": {"include": ["**/*.never"], "exclude": []},
            },
            "checks": {
                name: {
                    "adapter_id": "fixture",
                    "capability": "filtered" if name in filtered_checks else "check",
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
    if config_override is not None:
        config = config_override
    if selector_override is not None:
        selector = selector_override
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
                    "item_template": (
                        "{check_id}: {status}; reason={reason}; args_source={args_source}"
                    ),
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
                        "scope_resolution_failed": "The requested scope could not be resolved.",
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
    if operation.run_status is not None:
        assert operation.run_status in text.text
    return operation


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("outcomes", "status", "success", "code"),
    [
        (("failed", "unavailable"), "incomplete", True, None),
        (("failed", "not_executed", "passed"), "incomplete", True, None),
        (("failed", "passed"), "failed", True, None),
        (("failed", "invalid_request", "passed"), "incomplete", False, "adapter_request_rejected"),
        (("failed", "unconfirmed", "passed"), "incomplete", True, "termination_unconfirmed"),
        (("failed", "cancelled", "passed"), "incomplete", True, "operation_interrupted"),
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
    marker = tmp_path / ".pgmcp" / "quality_state.json"
    marker.parent.mkdir(exist_ok=True)
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

    if outcomes == ("failed", "passed"):
        for evidence in ({"format": "text", "data": "   "}, {"format": "json", "data": None}):
            invalid_row = first.model_dump(mode="json")
            invalid_row["evidence"] = evidence
            with pytest.raises(ValidationError):
                SelectionCheckResult.model_validate_json(json.dumps(invalid_row))
        for invalid_code in ("no_configured_checks", "operation_interrupted"):
            invalid_result = result.model_dump(mode="json")
            invalid_result["error_code"] = invalid_code
            with pytest.raises(ValidationError):
                RunChecksOutput.model_validate_json(json.dumps(invalid_result))


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
    if not arguments:
        schema = cached["input_schema"]
        assert isinstance(schema, dict)
        properties = schema["properties"]
        assert isinstance(properties, dict)
        assert properties["args"] == {
            "type": "object",
            "properties": {"check_0": {"type": "array", "items": {"type": "string"}}},
            "additionalProperties": False,
        }
    assert runtime.requests == []
    resources = [item for item in response.content if isinstance(item, EmbeddedResource)]
    assert len(resources) == 1 and str(resources[0].resource.uri) == "schema://validation"


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["no-checks", "no-default", "selection", "parent", "scope"])
async def test_early_operation_refusals_retain_exact_details_without_invocation(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    kind: str,
) -> None:
    config = configured_checks(default_profile=None if kind == "no-default" else "default")
    if kind == "no-checks":
        config = ChecksConfig(
            configured_targets=(), checks=(), profiles=(), profiles_by_extension=(), run_checks={}
        )
    arguments: dict[str, JsonValue] = {"scope": "configured"}
    if kind == "selection":
        arguments.update(checks=["first"], args={"second": []})
    elif kind == "parent":
        arguments["scope"] = "branch"
    elif kind == "scope":
        arguments.update(scope="targets", targets=["missing.md"])
    selector = build_selector(
        tmp_path,
        config=config,
        parent=None if kind == "parent" else "upstream",
    )
    composition, runtime = compose(
        tmp_path,
        pytestconfig,
        ("passed",),
        config_override=config,
        selector_override=selector,
    )
    result = await run(composition, arguments)
    assert result.success and result.run_status is None and runtime.requests == []
    assert result.results == ()
    assert (
        result.error_code
        == {
            "no-checks": "no_configured_checks",
            "no-default": "default_profile_missing",
            "selection": "selection_invalid",
            "parent": "branch_basis_unavailable",
            "scope": "scope_resolution_failed",
        }[kind]
    )
    details = result.error_details.model_dump(mode="json") if result.error_details else None
    if kind in {"no-checks", "no-default"}:
        assert details is None
    elif kind == "selection":
        assert details == {"issues": [{"reason": "unselected_args", "check_id": "second"}]}
    elif kind == "parent":
        assert details is not None and details["reason"] == "parent_unavailable"
    else:
        assert details is not None and details["issues"][0]["target"] == "missing.md"
        assert details["issues"][0]["reason"] == "missing"
    invalid = result.model_dump(mode="json")
    invalid["error_details"] = {"unexpected": True}
    with pytest.raises(ValidationError):
        RunChecksOutput.model_validate_json(json.dumps(invalid))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("outcomes", "filtered", "expected", "reasons", "calls"),
    [
        (("passed",), frozenset({"check_0"}), "not_applicable", ("not_applicable",), 0),
        (("passed", "passed"), frozenset({"check_1"}), "passed", (None, "not_applicable"), 1),
        (("failed", "passed"), frozenset({"check_1"}), "failed", (None, "not_applicable"), 1),
        (
            ("not_executed", "passed"),
            frozenset({"check_1"}),
            "incomplete",
            ("not_applicable", "not_applicable"),
            1,
        ),
        (
            ("invalid_request", "passed", "passed"),
            frozenset({"check_1"}),
            "incomplete",
            ("invalid_request", "not_applicable", "not_started"),
            1,
        ),
    ],
)
async def test_branch_no_applicable_outcomes(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    outcomes: tuple[str, ...],
    filtered: frozenset[str],
    expected: str,
    reasons: tuple[str | None, ...],
    calls: int,
) -> None:
    (tmp_path / "source.py").write_text("candidate", encoding="utf-8")

    class ChangedBranch(EmptyBranch):
        def get_branch_changes(self, parent: str) -> BranchChanges:
            return BranchChanges(current_paths=("source.py",), removed_paths=())

    composition, runtime = compose(
        tmp_path,
        pytestconfig,
        outcomes,
        branch=ChangedBranch(),
        filtered_checks=filtered,
    )
    result = await run(
        composition,
        {
            "scope": "branch",
            "args": {"check_0": []},
            "timeout_seconds": 11,
        },
    )
    assert result.run_status == expected
    assert result.success is (outcomes[0] != "invalid_request")
    assert tuple(row.reason for row in result.results) == reasons
    assert len(runtime.requests) == calls
    assert result.results[0].args_source == "caller" and result.results[0].effective_args == ()
    for row in result.results:
        if row.check_id in filtered:
            assert row.status == "not_executed" and row.reason == "not_applicable"
            assert row.adapter is None and row.capture is None and row.external_tools is None
            assert row.message is None and row.evidence is None and row.coverage is None
            assert row.termination_problem is None and row.request_rejection is None
            assert row.required_targets == ()
    if calls:
        assert runtime.requests[0][0].targets == (str(tmp_path / "source.py"),)
        assert runtime.requests[0][1] == 11
        assert result.results[0].adapter is not None and result.results[0].capture is not None
