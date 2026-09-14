"""Internal check execution, native facts and interruption boundaries."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

import pytest
from pydantic import BaseModel, ValidationError

from mcp_server.config.schemas.adapter_manifest import CheckCapability
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.core.interfaces.git import BranchChanges
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject
from mcp_server.execution.catalog import AdapterCatalog
from mcp_server.execution.check_selection import (
    CheckSelectionRequest,
    CheckSelector,
    FileScopePaths,
    ScopeResolver,
)
from mcp_server.execution.check_service import CheckService, ContentPreparationError
from mcp_server.execution.content_input import ContentInputPreparer, FileContentScratch
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    ContentCheckResponse,
    ContentRoleResponse,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    JsonEvidence,
    ProcessCapture,
    SelectionCheckResponse,
    SelectionRoleResponse,
    StreamCapture,
    TerminationProblem,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import AdapterResponseContract


class EmptyBranch:
    def get_current_branch(self) -> str:
        return "fixture"

    def get_branch_changes(self, parent: str) -> BranchChanges:
        return BranchChanges(current_paths=(), removed_paths=())

    def get_parent_branch(self, branch: str) -> str:
        return "parent"


TResponse = TypeVar("TResponse", bound=BaseModel)


class RecordingRuntime(AdapterProcessRuntime):
    """Direct typed invocation double; no process, native parser or private mocking."""

    def __init__(self, outcomes: tuple[str, ...]) -> None:
        self.outcomes = iter(outcomes)
        self.requests: list[tuple[BaseModel, float]] = []

    async def invoke(
        self,
        *,
        launch: AdapterLaunch,
        workspace_root: Path,
        request: BaseModel,
        response_contract: AdapterResponseContract[TResponse],
        timeout_seconds: float,
    ) -> InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled:
        self.requests.append((request, timeout_seconds))
        if "input_path" in type(request).model_fields:
            assert Path(str(request.input_path)).read_bytes() == b"proposed\r\n"
        kind = next(self.outcomes)
        empty = StreamCapture(observed_bytes=0, head="", tail="", truncated=False)
        if kind in {"timeout", "unconfirmed", "cancelled"}:
            capture = ProcessCapture(exit_code=None, stdout=empty, stderr=empty)
            termination = TerminationProblem.UNCONFIRMED if kind == "unconfirmed" else None
            if kind == "cancelled":
                return InvocationCancelled(
                    outcome="cancelled", capture=capture, termination_problem=termination
                )
            return InvocationFailed(
                outcome="failed",
                capture=capture,
                termination_problem=termination,
                failure=AdapterCallFailure(
                    reason=AdapterCallFailureReason.TIMEOUT, message="deadline expired"
                ),
            )
        if kind == "invalid_request":
            payload: dict[str, object] = {
                "reason": kind,
                "details": [{"location": ["operation"], "code": "invalid_value"}],
            }
            exit_code = 2
        else:
            decision: dict[str, object] = {"status": kind}
            if kind != "passed":
                decision["message"] = "Native observation"
            if kind == "unavailable":
                decision["reason"] = "dependency_unavailable"
            if kind == "not_executed":
                decision["reason"] = "not_applicable"
            payload = {
                "decision": decision,
                "external_tools": [{"tool_id": "native", "version": "1"}],
                "evidence": {
                    "format": "json",
                    "data": {"notes": [{"line": 3, "text": "native note"}]},
                },
            }
            if "targets" in type(request).model_fields:
                payload.update(coverage=None, required_targets=[])
            exit_code = {"passed": 0, "failed": 1, "unavailable": 3, "not_executed": 3}[kind]
        raw = json.dumps(payload).encode()
        accepted = StreamCapture(observed_bytes=len(raw), head=None, tail=None, truncated=False)
        capture = ProcessCapture(exit_code=exit_code, stdout=accepted, stderr=empty)
        return response_contract.complete(response_contract.decode(raw, exit_code), capture)


def compose(
    root: Path,
    outcomes: tuple[str, ...],
    *,
    file_content: bool = False,
    write_bytes: Callable[[Path, bytes], int] = Path.write_bytes,
) -> tuple[CheckService, CheckSelector, RecordingRuntime]:
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
    binding = AdapterBinding(
        AdapterPackageIdentity("fixture", "1.0.0", "1234567890abcdef"),
        "check",
        1,
        AdapterLaunch(None, ()),
        CheckCapability(inputs=("content", "selection"), requires_file=file_content),
    )
    catalog = AdapterCatalog(checks=(binding,), tests=(), fixes=())
    runtime = RecordingRuntime(outcomes)
    scratch = FileContentScratch(root / "scratch", fresh_id=lambda: "one", write_bytes=write_bytes)
    service = CheckService(config, catalog, runtime, ContentInputPreparer(scratch), root)
    selector = CheckSelector(
        config, catalog, ScopeResolver(FileScopePaths(root), EmptyBranch(), EmptyBranch())
    )
    return service, selector, runtime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("outcomes", "expected"),
    [
        (("passed", "passed"), "passed"),
        (("passed", "failed"), "failed"),
        (("failed", "unavailable", "passed"), "incomplete"),
        (("failed", "not_executed", "passed"), "incomplete"),
        (("failed", "timeout", "passed"), "incomplete"),
    ],
)
async def test_selection_reduction_preserves_every_native_fact(
    tmp_path: Path, outcomes: tuple[str, ...], expected: str
) -> None:
    service, selector, runtime = compose(tmp_path, outcomes)
    plan = selector.select(CheckSelectionRequest(scope="configured", args=(("check_0", ()),)))
    result = await service.run_selection(plan)
    assert result.run_status == expected
    assert len(runtime.requests) == len(outcomes)
    assert result.stop_reason is None
    assert result.results[0].effective_args == ()
    assert result.results[0].args_source == "caller"
    assert [budget for _, budget in runtime.requests] == list(range(3, 3 + len(outcomes)))
    assert all(request.targets == () for request, _ in runtime.requests)
    first = result.results[0].invocation
    assert isinstance(first, InvocationCompleted)
    response = first.response.root
    assert isinstance(response, SelectionRoleResponse)
    assert isinstance(response.evidence, JsonEvidence)
    assert isinstance(response.evidence.data, FrozenJsonObject)
    notes = response.evidence.data["notes"]
    assert isinstance(notes, tuple) and isinstance(notes[0], FrozenJsonObject)
    assert notes[0]["text"] == "native note"
    assert response.external_tools[0].version == "1"


@pytest.mark.asyncio
@pytest.mark.parametrize("stop", ["invalid_request", "cancelled", "unconfirmed"])
async def test_blocker_keeps_prior_facts_and_unstarted_obligations(
    tmp_path: Path, stop: str
) -> None:
    service, selector, runtime = compose(tmp_path, ("failed", stop, "passed"))
    result = await service.run_selection(selector.select(CheckSelectionRequest(scope="configured")))
    assert result.run_status == "incomplete"
    assert (
        result.stop_reason
        == {
            "invalid_request": "adapter_request_rejected",
            "cancelled": "operation_interrupted",
            "unconfirmed": "termination_unconfirmed",
        }[stop]
    )
    assert len(runtime.requests) == 2
    first = result.results[0].invocation
    assert isinstance(first, InvocationCompleted)
    assert isinstance(first.response.root, SelectionRoleResponse)
    assert first.response.root.decision.status == "failed"
    assert result.results[1].invocation is not None
    assert result.results[2].invocation is None
    assert result.results[2].not_executed == "not_started"
    assert result.results[2].effective_args == ("check_2",)


@pytest.mark.asyncio
async def test_empty_branch_does_not_turn_into_native_discovery(tmp_path: Path) -> None:
    service, selector, runtime = compose(tmp_path, ("passed",))
    result = await service.run_selection(selector.select(CheckSelectionRequest(scope="branch")))
    assert result.run_status == "empty_selection"
    assert result.results == ()
    assert runtime.requests == []


@pytest.mark.asyncio
@pytest.mark.parametrize("file_content", [False, True])
async def test_content_uses_same_bindings_and_owns_only_scratch(
    tmp_path: Path, file_content: bool
) -> None:
    service, _, runtime = compose(
        tmp_path, ("failed", "unavailable", "passed"), file_content=file_content
    )
    target = tmp_path / "logical.md"
    result = await service.run_content("renamed", target_path=str(target), content="proposed\r\n")
    assert len(result.results) == 3
    assert result.stop_reason is None
    assert all(row.cleanup_problem is None for row in result.results)
    assert [row.effective_args for row in result.results] == [
        ("check_0",),
        ("check_1",),
        ("check_2",),
    ]
    assert [request.operation for request, _ in runtime.requests] == ["check"] * 3
    assert not target.exists()
    assert not (tmp_path / "scratch" / "one").exists()


def test_wire_contracts_keep_roles_closed_and_native_json_immutable() -> None:
    good = {
        "decision": {"status": "passed"},
        "external_tools": [],
        "evidence": {"format": "json", "data": {"nested": [True, None, {"count": 3}]}},
    }
    response = ContentCheckResponse.model_validate_json(json.dumps(good))
    assert response.model_dump(mode="json") == good
    assert isinstance(response.root, ContentRoleResponse)
    assert isinstance(response.root.evidence, JsonEvidence)
    assert isinstance(response.root.evidence.data, FrozenJsonObject)
    assert response.root.evidence.data["nested"] == (True, None, FrozenJsonObject((("count", 3),)))
    for invalid in (
        {**good, "coverage": None, "required_targets": []},
        {**good, "evidence": None},
        {"decision": {"status": "failed", "message": "failure"}, "external_tools": []},
    ):
        with pytest.raises(ValidationError):
            ContentCheckResponse.model_validate_json(json.dumps(invalid))
    with pytest.raises(ValidationError):
        SelectionCheckResponse.model_validate_json(json.dumps(good))


@pytest.mark.asyncio
async def test_later_content_preparation_failure_preserves_prior_results(tmp_path: Path) -> None:
    writes = 0

    def fail_second(path: Path, data: bytes) -> int:
        nonlocal writes
        writes += 1
        if writes == 2:
            raise OSError("validation scratch unavailable")
        return path.write_bytes(data)

    service, _, runtime = compose(
        tmp_path,
        ("failed", "passed", "passed"),
        file_content=True,
        write_bytes=fail_second,
    )
    with pytest.raises(ContentPreparationError) as caught:
        await service.run_content(
            "renamed", target_path=str(tmp_path / "untouched.md"), content="proposed\r\n"
        )
    assert isinstance(caught.value.__cause__, OSError)
    assert caught.value.check_id == "check_1"
    result = caught.value.execution
    assert result.stop_reason == "content_preparation_failed"
    assert [row.check_id for row in result.results] == ["check_0", "check_1", "check_2"]
    assert len(runtime.requests) == 1
    first = result.results[0].invocation
    assert isinstance(first, InvocationCompleted)
    assert isinstance(first.response.root, ContentRoleResponse)
    assert first.response.root.decision.status == "failed"
    assert first.response.root.evidence is not None
    assert all(
        row.invocation is None and row.not_executed == "not_started" for row in result.results[1:]
    )
    assert not (tmp_path / "scratch" / "one").exists()
