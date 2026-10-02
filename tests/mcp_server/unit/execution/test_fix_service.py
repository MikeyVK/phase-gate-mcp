"""Ordered fixes preserve native mutation and stop before later work."""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

import pytest
from pydantic import BaseModel, ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig, FixCapability
from mcp_server.config.schemas.fixes_config import FixesConfig
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_selection import CheckSelectionError, CheckSelectionFailureReason
from mcp_server.execution.fix_service import FileFixScopePaths, FixManager, FixSelectionRequest
from mcp_server.execution.invocation_scratch import FileInvocationScratch
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    ApplyFixesOutput,
    FixRoleResponse,
    FixScopeDetails,
    FixTerminationDetails,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    ProcessCapture,
    PublicFixResult,
    RejectedFixRequestDetails,
    StreamCapture,
    TerminationProblem,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from mcp_server.execution.protocol import AdapterRequestContract, AdapterResponseContract

TRequest = TypeVar("TRequest", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)


class Catalog:
    @property
    def fixes(self) -> tuple[AdapterBinding[FixCapability], ...]:
        return tuple(self.get_fix(name, "repair") for name in ("alpha", "beta"))

    def get_fix(self, adapter_id: str, capability: str) -> AdapterBinding[FixCapability]:
        return AdapterBinding(
            AdapterPackageIdentity(adapter_id, "1.0.0", "a" * 16),
            capability,
            1,
            AdapterLaunch(Path("C:/adapter/python.exe"), (adapter_id,)),
            FixCapability.model_validate(
                {"addresses": [{"adapter_id": adapter_id, "capability": "check"}]}
            ),
        )


@dataclass(frozen=True)
class Call:
    launch: AdapterLaunch
    workspace_root: Path
    request: BaseModel
    timeout_seconds: float


class RecordingRuntime(AdapterProcessRuntime):
    def __init__(
        self,
        answers: tuple[tuple[bytes, int] | InvocationFailed | InvocationCancelled, ...],
        effect: Callable[[int], None] | None = None,
    ) -> None:
        self.answers = iter(answers)
        self.effect = effect
        self.calls: list[Call] = []

    async def invoke(
        self,
        *,
        launch: AdapterLaunch,
        workspace_root: Path,
        request: TRequest,
        request_contract: AdapterRequestContract[TRequest],
        response_contract: AdapterResponseContract[TResponse],
        timeout_seconds: float,
    ) -> InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled:
        self.calls.append(Call(launch, workspace_root, request, timeout_seconds))
        if self.effect is not None:
            self.effect(len(self.calls))
        answer = next(self.answers)
        if isinstance(answer, (InvocationFailed, InvocationCancelled)):
            return answer
        raw, code = answer
        empty = StreamCapture(observed_bytes=0, head="", tail="", truncated=False)
        capture = ProcessCapture(
            exit_code=code,
            stdout=StreamCapture(observed_bytes=len(raw), head=None, tail=None, truncated=False),
            stderr=empty,
        )
        return response_contract.complete(response_contract.decode(raw, code), capture)


def passed() -> tuple[bytes, int]:
    return json.dumps({"decision": {"status": "passed"}, "external_tools": []}).encode(), 0


def configuration() -> FixesConfig:
    return FixesConfig.model_validate(
        {
            "fixes": {
                name: {
                    "adapter_id": adapter,
                    "capability": "repair",
                    "timeout_seconds": budget,
                    "default_args": ["two words", ""],
                }
                for name, adapter, budget in (
                    ("first", "alpha", 10),
                    ("second", "beta", 20),
                    ("third", "alpha", 30),
                )
            }
        }
    )


@pytest.mark.asyncio
async def test_explicit_order_args_and_noop_continue(tmp_path: Path) -> None:
    config = configuration()
    source = tmp_path / "input with spaces.py"
    source.write_bytes(b"# native no-op\n")
    runtime = RecordingRuntime((passed(), passed()))
    output = await FixManager(config, Catalog(), runtime, FileFixScopePaths(tmp_path)).run(
        FixSelectionRequest(
            scope="targets",
            targets=[source.name, "./" + source.name],
            fixes=["second", "first"],
            args={"second": []},
        )
    )
    assert output.success and output.error_code is None
    assert output.selected_fixes == ("second", "first")
    assert [call.request.model_dump() for call in runtime.calls] == [
        {"operation": "repair", "targets": (str(source),), "args": ()},
        {"operation": "repair", "targets": (str(source),), "args": ("two words", "")},
    ]
    assert [call.timeout_seconds for call in runtime.calls] == [20, 10]
    assert [row.args_source for row in output.results] == ["caller", "configured"]
    assert all(row.status == "passed" and row.message is None for row in output.results)
    assert output.results[0].evidence is None and output.results[0].external_tools == ()
    assert source.read_bytes() == b"# native no-op\n"


def selection(source: Path) -> FixSelectionRequest:
    return FixSelectionRequest(
        scope="targets", targets=[source.name], fixes=["first", "second", "third"]
    )


@pytest.mark.asyncio
async def test_complete_selection_and_file_admission_launch_nothing(tmp_path: Path) -> None:
    source = tmp_path / "input.py"
    source.write_bytes(b"original")
    directory = tmp_path / "directory"
    directory.mkdir()
    base = selection(source).model_dump()
    for config, fields, expected in (
        (FixesConfig.model_validate({"fixes": {}}), base, "no_configured_fixes"),
        (configuration(), {**base, "fixes": ("first", "unknown")}, "selection_invalid"),
        (configuration(), {**base, "args": {"unknown": []}}, "selection_invalid"),
        (
            configuration(),
            {**base, "fixes": ("first",), "args": {"second": []}},
            "selection_invalid",
        ),
        (
            configuration(),
            {**base, "targets": (source.name, "missing.py")},
            "scope_resolution_failed",
        ),
        (
            configuration(),
            {**base, "targets": (source.name, directory.name)},
            "scope_resolution_failed",
        ),
    ):
        # Omitted optionals stay omitted; explicit null is not a valid public request.
        fields = {key: value for key, value in fields.items() if value is not None}
        runtime = RecordingRuntime(())
        output = await FixManager(config, Catalog(), runtime, FileFixScopePaths(tmp_path)).run(
            FixSelectionRequest.model_validate(fields)
        )
        assert output.success and output.error_code == expected and not runtime.calls
        assert all(row.reason == "not_started" and row.adapter is None for row in output.results)
        if isinstance(output.error_details, FixScopeDetails):
            assert output.error_details.issues[0].reason in {"missing", "not_file"}
        assert ApplyFixesOutput.model_validate_json(output.model_dump_json()) == output
    assert source.read_bytes() == b"original"


def test_closed_file_selection_rejects_implicit_scope_globs_and_coercion() -> None:
    base = {"scope": "targets", "targets": ["source.py"], "fixes": ["first"]}
    for change in (
        {"scope": "workspace"},
        {"scope": None},
        {"targets": []},
        {"fixes": []},
        {"fixes": ["first", "first"]},
        {"args": None},
        {"timeout_seconds": None},
        {"timeout_seconds": True},
        {"args": {"first": [1]}},
        {"verbose": True},
        *({"targets": [path]} for path in (".", "./", "dir/", "dir/.", "../file", "*.py", "C:/x")),
    ):
        with pytest.raises(ValidationError):
            FixSelectionRequest.model_validate({**base, **change})
    for required in ("scope", "targets", "fixes"):
        with pytest.raises(ValidationError):
            FixSelectionRequest.model_validate({k: v for k, v in base.items() if k != required})


def failure(kind: str) -> tuple[bytes, int] | InvocationFailed | InvocationCancelled:
    if kind == "unavailable":
        return json.dumps(
            {
                "decision": {
                    "status": "unavailable",
                    "reason": "unsupported_input",
                    "message": "Native selection refused.",
                },
                "external_tools": [],
                "evidence": {"format": "text", "data": "native diagnostic"},
            }
        ).encode(), 3
    if kind == "rejected":
        return json.dumps(
            {
                "reason": "invalid_request",
                "details": [{"location": ["args"], "code": "invalid_value"}],
            }
        ).encode(), 2
    stream = StreamCapture(observed_bytes=4, head="head", tail="", truncated=False)
    capture = ProcessCapture(exit_code=None, stdout=stream, stderr=stream)
    termination = TerminationProblem.UNCONFIRMED if kind.startswith("unconfirmed") else None
    if "cancelled" in kind:
        return InvocationCancelled(
            outcome="cancelled", capture=capture, termination_problem=termination
        )
    return InvocationFailed(
        outcome="failed",
        capture=capture,
        termination_problem=termination,
        failure=AdapterCallFailure(
            reason=(
                AdapterCallFailureReason.INVALID_RESPONSE
                if kind == "invalid_response"
                else AdapterCallFailureReason.TIMEOUT
            ),
            message="No valid native response was obtained.",
        ),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kind",
    [
        "unavailable",
        "timeout",
        "invalid_response",
        "cancelled",
        "unconfirmed_failure",
        "unconfirmed_cancelled",
        "rejected",
    ],
)
async def test_first_non_success_preserves_attempted_writes_and_stops(
    tmp_path: Path,
    kind: str,
) -> None:
    source = tmp_path / "source.py"
    source.write_text("original", encoding="utf-8")

    def mutate(number: int) -> None:
        source.write_text(f"native step {number}", encoding="utf-8")

    runtime = RecordingRuntime((passed(), failure(kind)), mutate)
    output = await FixManager(configuration(), Catalog(), runtime, FileFixScopePaths(tmp_path)).run(
        selection(source)
    )
    assert len(runtime.calls) == 2 and source.read_text(encoding="utf-8") == "native step 2"
    assert output.results[0].status == "passed"
    row = output.results[1]
    assert row.adapter is not None and row.capture is not None
    assert output.results[2].reason == "not_started" and output.results[2].capture is None
    assert output.results[2].effective_args == ("two words", "")
    assert output.success == (kind != "rejected")
    expected = (
        "termination_unconfirmed"
        if kind.startswith("unconfirmed")
        else "adapter_request_rejected"
        if kind == "rejected"
        else "operation_interrupted"
        if kind == "cancelled"
        else None
    )
    assert output.error_code == expected
    if kind == "unavailable":
        assert row.reason == "unsupported_input" and row.external_tools == ()
        assert row.evidence is not None
    else:
        assert row.evidence is None and row.external_tools is None
    if kind == "rejected":
        assert row.reason == "invalid_request" and row.request_rejection is not None
        assert isinstance(output.error_details, RejectedFixRequestDetails)
        assert output.error_details.fix_id == "second"
    if kind.startswith("unconfirmed"):
        assert isinstance(output.error_details, FixTerminationDetails)
        assert output.error_details.fix_id == "second"
        assert output.error_details.interrupted == ("cancelled" in kind)
        with pytest.raises(ValidationError):
            ApplyFixesOutput.model_validate(
                {
                    **output.model_dump(),
                    "error_details": {"fix_id": "first", "interrupted": "cancelled" in kind},
                }
            )
    if expected:
        with pytest.raises(ValidationError):
            ApplyFixesOutput.model_validate(
                {
                    **output.model_dump(),
                    "success": True,
                    "error_code": None,
                    "error_details": None,
                }
            )
    assert ApplyFixesOutput.model_validate_json(output.model_dump_json()) == output


class ChangingPaths(FileFixScopePaths):
    escaped = False
    unreadable = False

    def resolve(self, relative: str):
        if self.escaped:
            raise CheckSelectionError(CheckSelectionFailureReason.INVALID_TARGETS, relative)
        return super().resolve(relative)

    def is_file(self, path: Path) -> bool:
        if self.unreadable:
            raise PermissionError("test file inspection failed")
        return super().is_file(path)


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["missing", "escape", "unreadable"])
async def test_target_readmission_keeps_prior_effects_and_remaining_obligations(
    tmp_path: Path,
    change: str,
) -> None:
    source = tmp_path / "source.py"
    source.write_text("original", encoding="utf-8")
    paths = ChangingPaths(tmp_path)

    def alter(_number: int) -> None:
        if change == "missing":
            source.unlink()
        else:
            source.write_text("first fix", encoding="utf-8")
            paths.escaped = change == "escape"
            paths.unreadable = change == "unreadable"

    runtime = RecordingRuntime((passed(),), alter)
    output = await FixManager(configuration(), Catalog(), runtime, paths).run(selection(source))
    assert output.success and output.error_code == "scope_resolution_failed"
    assert isinstance(output.error_details, FixScopeDetails)
    assert output.error_details.issues[0].target == source.name
    assert output.error_details.issues[0].reason == (
        "missing" if change == "missing" else "unresolvable"
    )
    assert [row.reason for row in output.results] == [None, "not_started", "not_started"]
    assert len(runtime.calls) == 1
    assert not source.exists() if change == "missing" else source.read_text() == "first fix"


class CancelBeforeCallPaths(FileFixScopePaths):
    def __init__(self, root: Path, cancel_at: int) -> None:
        super().__init__(root)
        self.cancel_at = cancel_at
        self.inspections = 0

    def is_file(self, path: Path) -> bool:
        self.inspections += 1
        if self.inspections == self.cancel_at:
            task = asyncio.current_task()
            assert task is not None
            task.cancel()
        return super().is_file(path)


@pytest.mark.asyncio
@pytest.mark.parametrize("admission", [1, 2])
async def test_cancellation_before_call_has_no_fabricated_attempt(
    tmp_path: Path,
    admission: int,
) -> None:
    source = tmp_path / "source.py"
    source.write_text("original", encoding="utf-8")
    runtime = RecordingRuntime((passed(),))
    task = asyncio.current_task()
    assert task is not None
    try:
        output = await FixManager(
            configuration(), Catalog(), runtime, CancelBeforeCallPaths(tmp_path, admission)
        ).run(selection(source))
    finally:
        task.uncancel()
    assert output.success and output.error_code == "operation_interrupted"
    assert len(runtime.calls) == admission - 1
    assert all(row.status == "passed" for row in output.results[: admission - 1])
    assert all(
        row.reason == "not_started" and row.capture is None
        for row in output.results[admission - 1 :]
    )


class NativeRuntime(AdapterProcessRuntime):
    def __init__(self, source: Path) -> None:
        super().__init__(
            AsyncioProcessBackend(), FileInvocationScratch(source.parent / "invocations")
        )
        self.source = source
        self.observed: list[bytes] = []

    async def invoke(
        self,
        *,
        launch: AdapterLaunch,
        workspace_root: Path,
        request: TRequest,
        request_contract: AdapterRequestContract[TRequest],
        response_contract: AdapterResponseContract[TResponse],
        timeout_seconds: float,
    ) -> InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled:
        self.observed.append(self.source.read_bytes())
        return await super().invoke(
            launch=launch,
            workspace_root=workspace_root,
            request=request,
            request_contract=request_contract,
            response_contract=response_contract,
            timeout_seconds=timeout_seconds,
        )


def catalog(root: Path, config_root: Path):
    loader = ConfigLoader(config_root, root / ".pgmcp/templates")
    return AdapterCatalogLoader(
        root / "mcp_server/bundled_adapters",
        config_root / "adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()


@pytest.mark.asyncio
async def test_native_three_step_chain_preserves_format_and_partial_lint_writes(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    source = tmp_path / "source with spaces.py"
    original = b"import os\nvalue= 1\nunknown_name\n"
    source.write_bytes(original)
    decoy = tmp_path / "outside_selection.py"
    decoy.write_bytes(original)
    (tmp_path / "ruff.toml").write_text('[lint]\nselect = ["F"]\n', encoding="utf-8")
    # Independent native oracle observes both byte transitions before invoking the manager.
    formatted = subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--", str(source)],
        cwd=tmp_path,
        capture_output=True,
        timeout=15,
    )
    after_format = source.read_bytes()
    linted = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--fix", "--", str(source)],
        cwd=tmp_path,
        capture_output=True,
        timeout=15,
    )
    after_lint = source.read_bytes()
    native_version = (
        subprocess.run(
            [sys.executable, "-m", "ruff", "--version"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
            timeout=15,
        )
        .stdout.decode()
        .strip()
        .removeprefix("ruff ")
    )
    assert native_version
    assert formatted.returncode == 0 and linted.returncode == 1
    assert original != after_format != after_lint
    assert b"import os" not in after_lint and b"unknown_name" in after_lint
    source.write_bytes(original)
    config = FixesConfig.model_validate(
        {
            "fixes": {
                name: {
                    "adapter_id": "ruff",
                    "capability": operation,
                    "timeout_seconds": 20,
                    "default_args": [],
                }
                for name, operation in (
                    ("first", "format"),
                    ("second", "lint"),
                    ("third", "format"),
                )
            }
        }
    )
    runtime = NativeRuntime(source)
    output = await FixManager(
        config, catalog(pytestconfig.rootpath, tmp_path), runtime, FileFixScopePaths(tmp_path)
    ).run(selection(source))
    assert output.success and output.error_code is None
    assert [row.status for row in output.results] == ["passed", "failed", "not_executed"]
    assert runtime.observed == [original, after_format]
    assert source.read_bytes() == after_lint and decoy.read_bytes() == original
    assert output.results[2].adapter is None and output.results[2].reason == "not_started"
    failed = output.results[1]
    assert failed.evidence is not None
    assert failed.external_tools is not None and len(failed.external_tools) == 1
    assert failed.external_tools[0].tool_id == "ruff"
    assert failed.external_tools[0].version == native_version
    assert "F821" in failed.evidence.model_dump_json()
    assert failed.capture is not None and failed.capture.exit_code == 1
    assert ApplyFixesOutput.model_validate_json(output.model_dump_json()) == output
    assert "changed_files" not in output.model_dump() and "run_status" not in output.model_dump()
    for change in (
        {"evidence": None},
        {"message": None},
        {"capture": None},
        {"reason": "not_started"},
    ):
        with pytest.raises(ValidationError):
            PublicFixResult.model_validate({**failed.model_dump(), **change})
    with pytest.raises(ValidationError):
        FixRoleResponse.model_validate_json(
            '{"decision":{"status":"passed","message":"changed"},"external_tools":[]}'
        )


def test_required_fix_config_and_catalog_admission_without_execution(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    loader = ConfigLoader(tmp_path, pytestconfig.rootpath / ".pgmcp/templates")
    config_file = tmp_path / "fixes.yaml"
    authored = (pytestconfig.rootpath / ".pgmcp/config/fixes.yaml").read_text(encoding="utf-8")
    with pytest.raises(ConfigError):
        loader.load_fixes_config()
    config_file.write_text(authored, encoding="utf-8")
    config = loader.load_fixes_config()
    assert tuple(name for name, _ in config.fixes) == ("python_format", "python_lint")
    resolved = catalog(pytestconfig.rootpath, tmp_path)
    ConfigValidator().validate_fixes_config(config, resolved)
    for _, binding in config.fixes:
        assert binding.default_args == ()
        capability = resolved.get_fix(binding.adapter_id, binding.capability).capability
        assert capability.addresses[0].capability == binding.capability
    for replacement in (
        authored.replace("timeout_seconds: 60", "timeout_seconds: true"),
        authored.replace("default_args: []", "default_args: [true]"),
        authored.replace("    capability: format", "    capability: format\n    active: true"),
        authored.replace("    capability: format", "    capability: format\n    capability: lint"),
    ):
        config_file.write_text(replacement, encoding="utf-8")
        with pytest.raises(ConfigError):
            loader.load_fixes_config()
    for adapter, capability in (("unknown", "lint"), ("python", "syntax"), ("ruff", "unknown")):
        changed = config.model_dump()
        changed["fixes"]["python_format"].update(adapter_id=adapter, capability=capability)
        with pytest.raises(ConfigError):
            ConfigValidator().validate_fixes_config(FixesConfig.model_validate(changed), resolved)
