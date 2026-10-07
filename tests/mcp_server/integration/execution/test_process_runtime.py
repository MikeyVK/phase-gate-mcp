"""Real non-Python transport evidence, using a declared synthetic adapter package."""

from __future__ import annotations

import asyncio
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from shutil import which
from typing import Literal
from uuid import UUID

import pytest
from jsonschema import Draft202012Validator

from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.config.schemas.fixes_config import FixesConfig
from mcp_server.config.schemas.tests_config import TestsConfig as ExecutionTestsConfig
from mcp_server.core.interfaces.execution import AdapterLaunch, AdapterProcess, InvocationDirectory
from mcp_server.execution.check_selection import (
    CheckSelectionRequest,
    CheckSelector,
    FileScopePaths,
    ScopeResolver,
)
from mcp_server.execution.check_service import CheckService
from mcp_server.execution.configured_targets import ConfiguredTargetMatcher
from mcp_server.execution.content_input import ContentInputPreparer, FileContentScratch
from mcp_server.execution.fix_service import FileFixScopePaths, FixManager, FixSelectionRequest
from mcp_server.execution.invocation_scratch import FileInvocationScratch
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterExitCode,
    ApplyFixesOutput,
    ContentCheckResponse,
    InvalidCheckRequest,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    JsonEvidence,
    NativeEvidence,
    ProcessCapture,
    RunTestsOutput,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from mcp_server.execution.protocol import (
    STDERR_LIMIT,
    STDOUT_LIMIT,
    AdapterRequestContract,
    AdapterResponseContract,
)
from mcp_server.execution.protocol import (
    TestWireRequest as WireTestRequest,
)
from mcp_server.execution.test_service import TestRunManager as ExecutionTestManager
from mcp_server.execution.test_service import TestSelectionRequest as ExecutionTestSelection
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.execution_outputs import RunChecksOutput
from mcp_server.schemas.mutation_outputs import MutationCheck
from mcp_server.services.check_operation import CheckOperation
from mcp_server.services.scaffold_operation import project_mutation_check
from mcp_server.state.response_cache import ResponseCacheManager
from tests.mcp_server.fixtures.adapter_process import (
    EchoEvidence,
    FixtureResponse,
    InvalidRequest,
    ProcessFixture,
    ProcessRequest,
    ProcessResponse,
    create_process_fixture,
    request_contract,
    response_contract,
)
from tests.mcp_server.unit.execution.test_check_service import EmptyBranch

pytestmark = [pytest.mark.asyncio, pytest.mark.slow]


@pytest.fixture
def process_fixture(tmp_path: Path) -> ProcessFixture:
    node = which("node")
    assert node is not None, "Node is required for direct non-Python process evidence"
    return create_process_fixture(tmp_path, Path(node).resolve())


def request(fixture: ProcessFixture, mode: str, content: str = "hello\n世界") -> ProcessRequest:
    return ProcessRequest(
        operation="echo",
        target_path=str(fixture.workspace / "untouched.txt"),
        content=content,
        args=(mode,),
    )


async def invoke(
    fixture: ProcessFixture, mode: str, launch: AdapterLaunch | None = None
) -> InvocationCompleted[FixtureResponse] | InvocationFailed | InvocationCancelled:
    return await asyncio.wait_for(
        AdapterProcessRuntime(
            AsyncioProcessBackend(), FileInvocationScratch(fixture.workspace / "invocations")
        ).invoke(
            launch=launch or fixture.binding.launch,
            workspace_root=fixture.workspace,
            request=request(fixture, mode),
            request_contract=request_contract(),
            response_contract=response_contract(),
            timeout_seconds=10,
        ),
        timeout=15,
    )


@pytest.mark.parametrize(
    "mode, code", [("passed", 0), ("failed", 1), ("invalid_request", 2), ("unavailable", 3)]
)
async def test_domain_outcomes_are_completed_and_keep_concrete_resource_payload(
    process_fixture: ProcessFixture, pytestconfig: pytest.Config, mode: str, code: int
) -> None:
    result = await invoke(process_fixture, mode)
    assert isinstance(result, InvocationCompleted)
    assert isinstance(result.response, FixtureResponse)
    assert result.capture.exit_code == code
    assert result.capture.stdout.observed_bytes > 0
    assert result.capture.stdout.head is None
    assert result.capture.stdout.tail is None
    assert not result.capture.stdout.truncated
    assert result.capture.stderr.head == ""
    assert result.capture.stderr.tail == ""
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(result.response.model_dump(mode="json"))
    if isinstance(result.response.root, ProcessResponse):
        response = result.response.root
        assert response.decision.status == mode
        assert response.external_tools[0].version is not None
        assert response.external_tools[0].version.startswith("v")
        echo = EchoEvidence.model_validate_json(response.evidence.data)
        assert (
            echo.request.model_dump(exclude={"execution_context"})
            == request(process_fixture, mode).model_dump()
        )
        assert Path(echo.request.execution_context.scratch_directory).parent == (
            process_fixture.workspace / "invocations"
        )
        assert not Path(echo.request.execution_context.scratch_directory).exists()
        assert Path(echo.cwd) == process_fixture.workspace
        assert echo.argv == ("", "a b; literal")
        assert echo.dependency == "declared package contribution\n"
    else:
        assert isinstance(result.response.root, InvalidRequest)
    assert not (process_fixture.workspace / "untouched.txt").exists()
    assert process_fixture.binding.identity.adapter_id == "process_fixture"
    assert process_fixture.binding.identity.version == "1.2.3"
    assert len(process_fixture.binding.identity.fingerprint) == 16
    cache = ResponseCacheManager()
    publication = cache.put("process_fixture", result)
    text = await CachedResponseResource(cache).read(f"pgmcp://cache/runs/{publication.run_id}")
    assert InvocationCompleted[FixtureResponse].model_validate_json(text) == result


@pytest.mark.parametrize(
    "mode, reason, exit_code",
    [
        ("malformed", AdapterCallFailureReason.INVALID_RESPONSE, 0),
        ("logs", AdapterCallFailureReason.INVALID_RESPONSE, 0),
        ("multiple", AdapterCallFailureReason.INVALID_RESPONSE, 0),
        ("unknown_field", AdapterCallFailureReason.INVALID_RESPONSE, 0),
        ("empty", AdapterCallFailureReason.INVALID_RESPONSE, 0),
        ("mismatch", AdapterCallFailureReason.INVALID_RESPONSE, 1),
        ("crash", AdapterCallFailureReason.PROCESS_FAILED, 42),
    ],
)
async def test_protocol_rejects_unusable_responses_without_stdout_salvage(
    process_fixture: ProcessFixture, mode: str, reason: AdapterCallFailureReason, exit_code: int
) -> None:
    result = await invoke(process_fixture, mode)
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is reason
    assert result.capture.exit_code == exit_code
    assert result.capture.stdout.head is not None
    assert result.capture.stdout.tail == ""
    assert not result.capture.stdout.truncated
    assert result.termination_problem is None
    assert not any((process_fixture.workspace / "invocations").iterdir())


@pytest.mark.parametrize("mode", ["exact", "oversize"])
async def test_stdout_limit_counts_whitespace_and_first_excess_byte(
    process_fixture: ProcessFixture, mode: str
) -> None:
    result = await invoke(process_fixture, mode)
    if mode == "exact":
        assert isinstance(result, InvocationCompleted)
        assert result.capture.stdout.observed_bytes == STDOUT_LIMIT
        assert result.capture.stdout.head is None
    else:
        assert isinstance(result, InvocationFailed)
        assert result.failure.reason is AdapterCallFailureReason.RESPONSE_TOO_LARGE
        assert result.capture.stdout.observed_bytes == STDOUT_LIMIT + 1
        assert result.capture.stdout.truncated
        assert result.capture.stdout.head is not None
        assert len(result.capture.stdout.head.encode()) == STDOUT_LIMIT
        assert result.capture.stdout.tail == ""


async def test_stderr_drains_during_large_stdin_and_preserves_bounded_unicode_fragments(
    process_fixture: ProcessFixture,
) -> None:
    launch = replace(
        process_fixture.binding.launch, args=(*process_fixture.binding.launch.args, "--duplex")
    )
    supplied = request(process_fixture, "passed", "雪\n" * 400_000)
    result = await asyncio.wait_for(
        AdapterProcessRuntime(
            AsyncioProcessBackend(),
            FileInvocationScratch(process_fixture.workspace / "invocations"),
        ).invoke(
            launch=launch,
            workspace_root=process_fixture.workspace,
            request=supplied,
            request_contract=request_contract(),
            response_contract=response_contract(),
            timeout_seconds=10,
        ),
        timeout=15,
    )
    assert isinstance(result, InvocationCompleted)
    assert isinstance(result.response.root, ProcessResponse)
    echo = EchoEvidence.model_validate_json(result.response.root.evidence.data)
    assert echo.request.model_dump(exclude={"execution_context"}) == supplied.model_dump()
    stderr = result.capture.stderr
    assert stderr.observed_bytes == STDERR_LIMIT + 31
    assert stderr.truncated
    assert stderr.head is not None and stderr.head.startswith("HEAD\n")
    assert stderr.head.endswith("\ufffd")
    assert stderr.tail is not None and stderr.tail.endswith("TAIL✓")
    assert len(stderr.tail.encode()) == STDERR_LIMIT // 2


@pytest.mark.parametrize("missing", [None, "missing executable"])
async def test_launch_failure_has_no_started_process_capture(
    process_fixture: ProcessFixture, missing: str | None
) -> None:
    executable = None if missing is None else process_fixture.workspace / missing
    result = await invoke(process_fixture, "passed", AdapterLaunch(executable, ()))
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is AdapterCallFailureReason.LAUNCH_FAILED
    assert result.capture.exit_code is None
    for stream in (result.capture.stdout, result.capture.stderr):
        assert stream.observed_bytes == 0
        assert stream.head == stream.tail == ""
        assert not stream.truncated
    assert result.termination_problem is None
    assert not any((process_fixture.workspace / "invocations").iterdir())


async def test_directory_description_is_pure_frozen_and_create_is_exclusive(
    process_fixture: ProcessFixture,
) -> None:
    root = process_fixture.workspace / "described-only"
    provider = FileInvocationScratch(root)
    allocation = provider.describe(UUID(int=1))
    assert not root.exists()
    assert allocation.directory.parent == root
    with pytest.raises(FrozenInstanceError):
        allocation.directory = root  # type: ignore[misc]
    assert provider.create(allocation) is None
    sentinel = allocation.directory / "existing.txt"
    sentinel.write_bytes(b"owned by original creator")
    with pytest.raises(FileExistsError):
        provider.create(allocation)
    assert sentinel.read_bytes() == b"owned by original creator"
    assert provider.remove(allocation) is None
    assert not allocation.directory.exists()


class ObservedBackend:
    """Observe whether preparation failures reached process launch."""

    def __init__(self) -> None:
        self.starts = 0

    async def start(self, launch: AdapterLaunch, workspace_root: Path) -> AdapterProcess:
        self.starts += 1
        raise AssertionError("preparation failure must not launch a process")


async def test_collision_preserves_existing_directory_without_launch(
    process_fixture: ProcessFixture,
) -> None:
    provider = FileInvocationScratch(process_fixture.workspace / "invocations")
    identifier = UUID(int=2)
    allocation = provider.describe(identifier)
    provider.create(allocation)
    sentinel = allocation.directory / "existing.txt"
    sentinel.write_bytes(b"keep")
    backend = ObservedBackend()
    result = await AdapterProcessRuntime(
        backend, provider, invocation_id=lambda: identifier
    ).invoke(
        launch=process_fixture.binding.launch,
        workspace_root=process_fixture.workspace,
        request=request(process_fixture, "passed"),
        request_contract=request_contract(),
        response_contract=response_contract(),
        timeout_seconds=5,
    )
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is AdapterCallFailureReason.LAUNCH_FAILED
    assert allocation.directory.name in result.failure.message
    assert result.capture.exit_code is None
    assert result.capture.stdout.observed_bytes == result.capture.stderr.observed_bytes == 0
    assert sentinel.read_bytes() == b"keep"
    assert backend.starts == 0
    provider.remove(allocation)


class DeniedInvocationRemoval:
    """Refuse removal while keeping genuine directory allocation behavior."""

    def __init__(self, provider: FileInvocationScratch) -> None:
        self.provider = provider

    def describe(self, invocation_id: UUID) -> InvocationDirectory:
        return self.provider.describe(invocation_id)

    def create(self, directory: InvocationDirectory) -> None:
        self.provider.create(directory)

    def remove(self, directory: InvocationDirectory) -> None:
        raise PermissionError(f"fixture denied invocation removal: {directory.directory}")


async def test_owned_cleanup_failure_keeps_completion_capture_and_reports_operational_failure(
    process_fixture: ProcessFixture,
) -> None:
    provider = FileInvocationScratch(process_fixture.workspace / "invocations")
    identifier = UUID(int=3)
    allocation = provider.describe(identifier)
    result = await AdapterProcessRuntime(
        AsyncioProcessBackend(), DeniedInvocationRemoval(provider), invocation_id=lambda: identifier
    ).invoke(
        launch=process_fixture.binding.launch,
        workspace_root=process_fixture.workspace,
        request=request(process_fixture, "passed"),
        request_contract=request_contract(),
        response_contract=response_contract(),
        timeout_seconds=5,
    )
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is AdapterCallFailureReason.PROCESS_FAILED
    assert str(allocation.directory) in result.failure.message
    assert "fixture denied invocation removal" in result.failure.message
    assert result.capture.exit_code == 0
    assert result.capture.stdout.observed_bytes > 0
    assert result.termination_problem is None
    assert allocation.directory.is_dir()
    provider.remove(allocation)


async def test_encoding_failure_cleans_owned_directory_without_launch(
    process_fixture: ProcessFixture,
) -> None:
    provider = FileInvocationScratch(process_fixture.workspace / "invocations")
    backend = ObservedBackend()
    result = await AdapterProcessRuntime(backend, provider).invoke(
        launch=process_fixture.binding.launch,
        workspace_root=process_fixture.workspace,
        request=request(process_fixture, "passed"),
        request_contract=AdapterRequestContract(WireTestRequest),
        response_contract=response_contract(),
        timeout_seconds=5,
    )
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is AdapterCallFailureReason.LAUNCH_FAILED
    assert result.capture.exit_code is None
    assert result.capture.stdout.observed_bytes == result.capture.stderr.observed_bytes == 0
    assert result.termination_problem is None
    assert backend.starts == 0
    assert not any((process_fixture.workspace / "invocations").iterdir())


async def test_cleanup_failure_preserves_completed_request_rejection(
    process_fixture: ProcessFixture,
) -> None:
    provider = FileInvocationScratch(process_fixture.workspace / "invocations")
    identifier = UUID(int=4)
    allocation = provider.describe(identifier)
    contract = AdapterResponseContract(
        ContentCheckResponse,
        InvocationCompleted[ContentCheckResponse],
        lambda _response: AdapterExitCode.INVALID_REQUEST,
    )
    result = await AdapterProcessRuntime(
        AsyncioProcessBackend(), DeniedInvocationRemoval(provider), invocation_id=lambda: identifier
    ).invoke(
        launch=process_fixture.binding.launch,
        workspace_root=process_fixture.workspace,
        request=request(process_fixture, "invalid_request"),
        request_contract=request_contract(),
        response_contract=contract,
        timeout_seconds=5,
    )
    assert isinstance(result, InvocationCompleted)
    assert isinstance(result.response.root, InvalidCheckRequest)
    assert result.response.root.reason == "invalid_request"
    assert result.capture.exit_code == 2
    assert result.capture.stdout.observed_bytes > 0
    assert result.cleanup_failure is not None
    assert result.cleanup_failure.reason is AdapterCallFailureReason.PROCESS_FAILED
    assert str(allocation.directory) in result.cleanup_failure.message
    assert allocation.directory.is_dir()
    provider.remove(allocation)


class StartedBackend:
    """Expose a launch observation before cancelling a real managed invocation."""

    def __init__(self) -> None:
        self.backend = AsyncioProcessBackend()
        self.started = asyncio.Event()

    async def start(self, launch: AdapterLaunch, workspace_root: Path) -> AdapterProcess:
        process = await self.backend.start(launch, workspace_root)
        self.started.set()
        return process


async def test_cleanup_failure_preserves_confirmed_cancellation(
    process_fixture: ProcessFixture,
) -> None:
    provider = FileInvocationScratch(process_fixture.workspace / "invocations")
    identifier = UUID(int=5)
    allocation = provider.describe(identifier)
    backend = StartedBackend()
    task = asyncio.create_task(
        AdapterProcessRuntime(
            backend, DeniedInvocationRemoval(provider), invocation_id=lambda: identifier
        ).invoke(
            launch=process_fixture.binding.launch,
            workspace_root=process_fixture.workspace,
            request=request(process_fixture, "passed"),
            request_contract=request_contract(),
            response_contract=response_contract(),
            timeout_seconds=5,
        )
    )
    try:
        await asyncio.wait_for(backend.started.wait(), 5)
        task.cancel()
        result = await asyncio.wait_for(task, 10)
        assert isinstance(result, InvocationCancelled)
        assert result.capture.exit_code is not None
        assert result.termination_problem is None
        assert result.cleanup_failure is not None
        assert result.cleanup_failure.reason is AdapterCallFailureReason.PROCESS_FAILED
        assert str(allocation.directory) in result.cleanup_failure.message
        assert allocation.directory.is_dir()
    finally:
        if not task.done():
            task.cancel()
            await asyncio.wait_for(task, 10)
        if allocation.directory.exists():
            provider.remove(allocation)


async def test_expired_preparation_deadline_never_starts_backend(
    process_fixture: ProcessFixture,
) -> None:
    provider = FileInvocationScratch(process_fixture.workspace / "invocations")
    backend = ObservedBackend()
    result = await AdapterProcessRuntime(backend, provider).invoke(
        launch=process_fixture.binding.launch,
        workspace_root=process_fixture.workspace,
        request=request(process_fixture, "passed"),
        request_contract=request_contract(),
        response_contract=response_contract(),
        timeout_seconds=1e-9,
    )
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is AdapterCallFailureReason.TIMEOUT
    assert result.capture.exit_code is None
    assert result.capture.stdout.observed_bytes == result.capture.stderr.observed_bytes == 0
    assert result.termination_problem is None
    assert backend.starts == 0
    assert not any((process_fixture.workspace / "invocations").iterdir())


PublicRole = Literal["check", "test", "fix"]
PublicOutput = RunChecksOutput | RunTestsOutput | ApplyFixesOutput


def cleanup_denied_runtime(
    fixture: ProcessFixture, backend: AsyncioProcessBackend | StartedBackend
) -> AdapterProcessRuntime:
    return AdapterProcessRuntime(
        backend,
        DeniedInvocationRemoval(FileInvocationScratch(fixture.workspace / "invocations")),
    )


def real_check_service(
    fixture: ProcessFixture, runtime: AdapterProcessRuntime, mode: str
) -> tuple[CheckService, CheckOperation]:
    declaration = {
        "adapter_id": "process_fixture",
        "capability": "echo",
        "timeout_seconds": 5,
        "default_args": [mode],
    }
    config = ChecksConfig.model_validate(
        {
            "configured_targets": {"fixture": {"include": ["**"], "exclude": []}},
            "checks": {"first": declaration, "second": {**declaration, "default_args": ["passed"]}},
            "profiles": {"fixture": {"checks": ["first", "second"]}},
            "profiles_by_extension": {},
            "run_checks": {"default_profile": "fixture"},
        }
    )
    service = CheckService(
        config,
        fixture.catalog,
        runtime,
        ContentInputPreparer(
            FileContentScratch(fixture.workspace / "content", fresh_id=lambda: "one")
        ),
        fixture.workspace,
    )
    selector = CheckSelector(
        config,
        fixture.catalog,
        ScopeResolver(FileScopePaths(fixture.workspace), EmptyBranch(), EmptyBranch()),
        ConfiguredTargetMatcher(fixture.workspace),
    )
    return service, CheckOperation(selector=selector, executor=service)


async def public_role_run(
    fixture: ProcessFixture, runtime: AdapterProcessRuntime, role: PublicRole, mode: str
) -> PublicOutput:
    source = fixture.workspace / "selected.txt"
    source.write_bytes(b"original source\n")
    if role == "check":
        _, operation = real_check_service(fixture, runtime, mode)
        return await operation.execute(
            CheckSelectionRequest(
                scope="targets",
                targets=(source.name,),
                checks=("first", "second"),
            )
        )
    if role == "test":
        config = ExecutionTestsConfig.model_validate(
            {
                "tests": {
                    name: {
                        "adapter_id": "process_fixture",
                        "capability": "suite",
                        "timeout_seconds": 5,
                        "default_args": [mode if name == "first" else "passed"],
                        "active": True,
                    }
                    for name in ("first", "second")
                }
            }
        )
        return await ExecutionTestManager(
            config,
            fixture.catalog,
            runtime,
            FileScopePaths(fixture.workspace),
        ).run(ExecutionTestSelection(scope="targets", targets=(source.name,)))
    fixes = FixesConfig.model_validate(
        {
            "fixes": {
                name: {
                    "adapter_id": "process_fixture",
                    "capability": "repair",
                    "timeout_seconds": 5,
                    "default_args": [mode if name == "first" else "passed"],
                }
                for name in ("first", "second")
            }
        }
    )
    return await FixManager(
        fixes,
        fixture.catalog,
        runtime,
        FileFixScopePaths(fixture.workspace),
    ).run(
        FixSelectionRequest(
            scope="targets",
            targets=(source.name,),
            fixes=("first", "second"),
        )
    )


def assert_retained_response(
    evidence: NativeEvidence | None,
    message: str | None,
    capture: ProcessCapture | None,
    original_status: str,
) -> None:
    assert isinstance(evidence, JsonEvidence), (
        "accepted native response must survive cleanup failure"
    )
    original = json.loads(evidence.model_dump_json())["data"]
    assert original["decision"]["status"] == original_status
    assert original["external_tools"][0]["tool_id"] == "node"
    assert original["external_tools"][0]["version"].startswith("v")
    echo = json.loads(original["evidence"]["data"])
    if original_status == "failed":
        assert original["decision"]["message"] == "fixture rejected content"
        assert len(echo["dependency"]) > 300000
        assert echo["dependency"].endswith(":late diagnostic sentinel")
    else:
        assert echo["request"]["args"] == ["write_selected"]
    assert capture is not None
    assert capture.exit_code == (1 if original_status == "failed" else 0)
    assert capture.stdout.head is None and capture.stdout.tail is None
    assert message is not None
    assert "preceding_outcome=completed" in message
    assert f"adapter_exit_code={capture.exit_code}" in message
    assert "fixture denied invocation removal" in message
    assert echo["request"]["execution_context"]["scratch_directory"] in message


@pytest.mark.parametrize("role", ["check", "test", "fix"])
async def test_public_cleanup_failure_retains_accepted_native_response_and_fix_effect(
    process_fixture: ProcessFixture,
    role: PublicRole,
) -> None:
    mode = "write_selected" if role == "fix" else "failed_detail"
    output = await public_role_run(
        process_fixture,
        cleanup_denied_runtime(process_fixture, AsyncioProcessBackend()),
        role,
        mode,
    )
    restored = type(output).model_validate_json(output.model_dump_json())
    assert restored == output
    row = restored.results[0]
    assert row.status == "unavailable" and row.reason == "process_failed"
    if role == "fix":
        assert (
            process_fixture.workspace / "selected.txt"
        ).read_bytes() == b"fixture applied repair\n"
        assert restored.results[1].reason == "not_started"
    assert_retained_response(
        row.evidence,
        row.message,
        row.capture,
        "passed" if role == "fix" else "failed",
    )
    original = json.loads(row.evidence.model_dump_json())["data"] if row.evidence else {}
    if role == "check":
        assert original["coverage"] is None and original["required_targets"] == []


@pytest.mark.parametrize("mode", ["failed_detail", "invalid_request", "cancel"])
async def test_content_cleanup_failure_preserves_response_or_stop_in_serialized_projection(
    process_fixture: ProcessFixture,
    mode: str,
) -> None:
    backend = StartedBackend() if mode == "cancel" else AsyncioProcessBackend()
    service, _ = real_check_service(
        process_fixture,
        cleanup_denied_runtime(process_fixture, backend),
        "passed" if mode == "cancel" else mode,
    )
    task = asyncio.create_task(
        service.run_content(
            "fixture",
            target_path=str(process_fixture.workspace / "proposed.txt"),
            content="proposed content",
        )
    )
    if isinstance(backend, StartedBackend):
        await asyncio.wait_for(backend.started.wait(), 5)
        task.cancel()
    execution = await asyncio.wait_for(task, 10)
    projected = project_mutation_check(execution.results[0], process_fixture.workspace)
    restored = MutationCheck.model_validate_json(projected.model_dump_json())
    assert restored == projected
    assert restored.invocation is not None
    if mode == "failed_detail":
        assert restored.status == "unavailable" and restored.reason == "process_failed"
        assert_retained_response(
            restored.evidence,
            restored.message,
            restored.invocation.capture,
            "failed",
        )
    else:
        assert restored.status == "not_executed"
        assert restored.evidence is None
        assert restored.message is not None
        assert "fixture denied invocation removal" in restored.message
        directories = tuple((process_fixture.workspace / "invocations").iterdir())
        assert any(str(directory) in restored.message for directory in directories)
        if mode == "cancel":
            assert restored.reason == "interrupted"
            assert execution.stop_reason == "operation_interrupted"
            assert restored.request_rejection is None
        else:
            assert restored.reason == "invalid_request"
            assert execution.stop_reason == "adapter_request_rejected"
            assert restored.request_rejection is not None
            assert restored.request_rejection[0].location == ("operation",)
            assert restored.request_rejection[0].code == "invalid_value"
    assert not (process_fixture.workspace / "proposed.txt").exists()


@pytest.mark.parametrize("role", ["check", "test", "fix"])
@pytest.mark.parametrize("mode", ["invalid_request", "cancel"])
async def test_public_cleanup_failure_keeps_stop_reason_details_and_exposes_cleanup(
    process_fixture: ProcessFixture,
    role: PublicRole,
    mode: str,
) -> None:
    backend = StartedBackend() if mode == "cancel" else AsyncioProcessBackend()
    runtime = cleanup_denied_runtime(process_fixture, backend)
    task = asyncio.create_task(
        public_role_run(
            process_fixture,
            runtime,
            role,
            "passed" if mode == "cancel" else mode,
        )
    )
    if isinstance(backend, StartedBackend):
        await asyncio.wait_for(backend.started.wait(), 5)
        task.cancel()
    output = await asyncio.wait_for(task, 10)
    restored = type(output).model_validate_json(output.model_dump_json())
    assert restored == output
    row = restored.results[0]
    assert row.status == "not_executed"
    assert restored.results[1].reason == "not_started"
    assert row.capture is not None and row.capture.exit_code is not None
    if mode == "cancel":
        assert restored.error_code == "operation_interrupted" and restored.success
        assert row.reason == "interrupted"
        assert row.request_rejection is None
        assert restored.error_details is None
    else:
        assert restored.error_code == "adapter_request_rejected" and not restored.success
        assert row.reason == "invalid_request"
        assert row.request_rejection is not None
        assert row.request_rejection[0].location == ("operation",)
        assert row.request_rejection[0].code == "invalid_value"
        assert restored.error_details is not None
        id_field = {"check": "check_id", "test": "test_id", "fix": "fix_id"}[role]
        assert restored.error_details.model_dump() == {id_field: "first"}
    assert row.message is not None, "cleanup failure must reach the serialized public result"
    assert "fixture denied invocation removal" in row.message
    directories = tuple((process_fixture.workspace / "invocations").iterdir())
    assert any(str(directory) in row.message for directory in directories)


async def test_public_cleanup_failure_preserves_primary_process_failure(
    process_fixture: ProcessFixture,
) -> None:
    output = await public_role_run(
        process_fixture,
        cleanup_denied_runtime(process_fixture, AsyncioProcessBackend()),
        "test",
        "crash",
    )
    restored = RunTestsOutput.model_validate_json(output.model_dump_json())
    assert restored == output
    row = restored.results[0]
    assert row.status == "unavailable" and row.reason == "process_failed"
    assert row.capture is not None and row.capture.exit_code == 42
    assert row.capture.stdout.head == "{broken"
    assert row.evidence is None
    assert row.message is not None and "adapter_exit_code:42" in row.message
    assert "fixture denied invocation removal" in row.message
    directories = tuple((process_fixture.workspace / "invocations").iterdir())
    assert any(str(directory) in row.message for directory in directories)
