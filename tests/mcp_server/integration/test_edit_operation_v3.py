"""Observe safe-edit persistence, independent blockers and original/proposed identity."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Literal, TypeVar

import pytest
from pydantic import BaseModel, ValidationError

from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.core.interfaces.file_writer import OriginalFileSnapshot, WriteHousekeepingIssue
from mcp_server.execution.models import InvocationCancelled, InvocationCompleted, InvocationFailed
from mcp_server.execution.protocol import AdapterRequestContract, AdapterResponseContract
from mcp_server.schemas.mutation_outputs import EditOperationOutput
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.edit_construction import (
    AppendOperation,
    EditProfileSelection,
    PatternReplaceOperation,
    ReplaceOperation,
    RewriteOperation,
    construct_edit_proposal,
    select_profile,
)
from mcp_server.services.edit_construction import (
    EditOperation as EditCommand,
)
from mcp_server.services.edit_operation import EditOperation
from mcp_server.utils.atomic_file_writer import CheckedFileWriter, OriginalFileReader
from mcp_server.utils.path_resolver import FileArtifactTargetPaths
from tests.mcp_server.unit.execution.test_check_service import RecordingRuntime, compose
from tests.mcp_server.unit.services.test_artifact_target_resolver import create_directory_link


def operation(
    root: Path,
    outcomes: tuple[str, ...],
    *,
    has_profile: bool = True,
) -> tuple[EditOperation, RecordingRuntime]:
    checks, _, runtime = compose(root, outcomes)
    config = ChecksConfig.model_validate(
        {
            "configured_targets": {"fixture": {"include": ["**"], "exclude": []}},
            "checks": {
                "syntax": {
                    "adapter_id": "fixture",
                    "capability": "check",
                    "timeout_seconds": 3,
                    "default_args": [],
                }
            },
            "profiles": {"renamed": {"checks": ["syntax"]}},
            "profiles_by_extension": {".md": "renamed"} if has_profile else {},
            "run_checks": {},
        }
    )

    def select(original: str, filename: str, explicit: str | None) -> EditProfileSelection:
        return select_profile(
            original,
            filename,
            explicit_template_id=explicit,
            header_reader=ArtifactHeaderReader(),
            template_profiles={"source_notes": "renamed"},
            extension_profile_for_filename=config.match_for_filename,
        )

    return EditOperation(
        paths=FileArtifactTargetPaths(root),
        reader=OriginalFileReader(),
        writer=CheckedFileWriter(),
        select=select,
        construct=construct_edit_proposal,
        checks=checks,
    ), runtime


@pytest.mark.asyncio
@pytest.mark.parametrize("policy", ["enforce", "report"])
@pytest.mark.parametrize(
    ("outcome", "has_profile"),
    [("passed", True), ("failed", True), ("unavailable", True), ("passed", False)],
)
async def test_policy_retains_actual_text_bytes_and_validation(
    tmp_path: Path,
    policy: Literal["enforce", "report"],
    outcome: str,
    has_profile: bool,
) -> None:
    service, runtime = operation(tmp_path, (outcome,), has_profile=has_profile)
    target = tmp_path / "notes.md"
    original = b"\xef\xbb\xbfsource\r\nbody\r"
    target.write_bytes(original)
    proposed = "\ufeffsource\nbody\n"
    result = await service.execute(
        path=target.name,
        operation=RewriteOperation(content=proposed),
        validation=policy,
    )
    written = policy == "report" or (has_profile and outcome == "passed")
    assert result.written is written and result.success is written
    assert target.read_bytes() == (proposed.encode("utf-8") if written else original)
    assert result.content_changed is (False if written else None)
    assert result.validation_status == (outcome if has_profile else "not_executed")
    assert result.profile_id == ("renamed" if has_profile else None)
    assert len(runtime.requests) == int(has_profile)
    if has_profile:
        request = runtime.requests[0][0].model_dump()
        assert request["content"] == proposed and request["args"] == ("check_0",)
    else:
        assert result.selected_source == "none" and result.checks == ()
    assert EditOperationOutput.model_validate_json(result.model_dump_json()) == result
    if written:
        invalid = result.model_dump(mode="json")
        invalid["content_changed"] = None
        with pytest.raises(ValidationError):
            EditOperationOutput.model_validate_json(json.dumps(invalid))


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["bytes", "missing"])
async def test_final_guard_preserves_external_writer_and_passed_checks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change: str,
) -> None:
    service, runtime = operation(tmp_path, ("passed",))
    target = tmp_path / "notes.md"
    original = b"source\r\n"
    competing = b"source\n"
    target.write_bytes(original)
    actual = CheckedFileWriter.replace_if_unchanged

    def intervene(
        self: CheckedFileWriter, path: Path, expected_original: bytes, content: str
    ) -> tuple[WriteHousekeepingIssue, ...]:
        assert expected_original == original and content == "proposed"
        if change == "bytes":
            path.write_bytes(competing)
        else:
            path.unlink()
        return actual(self, path, expected_original, content)

    monkeypatch.setattr(CheckedFileWriter, "replace_if_unchanged", intervene)
    result = await service.execute(
        path=target.name,
        operation=RewriteOperation(content="proposed"),
        validation="report",
    )
    assert result.error_code == ("original_changed" if change == "bytes" else "original_missing")
    assert result.validation_status == "passed" and len(runtime.requests) == 1
    assert not result.written and result.content_changed is None
    if change == "bytes":
        assert target.read_bytes() == competing
    else:
        assert not target.exists()
    assert list(tmp_path.glob("*.staging")) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["missing", "directory", "root", "encoding", "permission", "edit"])
async def test_precheck_failures_do_not_invent_check_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    kind: str,
) -> None:
    service, runtime = operation(tmp_path, ("passed",))
    target = tmp_path if kind == "root" else tmp_path / "notes.md"
    command: EditCommand = RewriteOperation(content="proposed")
    if kind == "directory":
        target.mkdir()
    elif kind not in ("missing", "root"):
        target.write_bytes(b"\xff" if kind == "encoding" else b"original")
    if kind == "permission":

        def deny_read(_self: OriginalFileReader, _path: Path) -> OriginalFileSnapshot:
            raise PermissionError("controlled original read denial")

        monkeypatch.setattr(OriginalFileReader, "read_snapshot", deny_read)
    if kind == "edit":
        command = ReplaceOperation(target_content="absent", replacement="new")
    result = await service.execute(
        path="." if kind == "root" else target.name, operation=command, validation="report"
    )
    expected = {
        "missing": "original_missing",
        "directory": "target_invalid",
        "root": "target_invalid",
        "encoding": "original_unreadable",
        "permission": "original_unreadable",
        "edit": "edit_invalid",
    }
    assert result.error_code == expected[kind] and result.checks == ()
    assert result.validation_status == "not_executed" and not result.written
    assert result.content_changed is None and runtime.requests == []
    assert result.profile_id == ("renamed" if kind == "edit" else None)
    if kind in ("root", "directory"):
        assert result.error_details is not None
        assert result.error_details.model_dump()["reason"] == "not_file"


@pytest.mark.asyncio
async def test_parent_alias_cannot_edit_outside_workspace(tmp_path: Path) -> None:
    root, outside = tmp_path / "workspace", tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    target = outside / "notes.md"
    target.write_bytes(b"external")
    alias = root / "alias"
    create_directory_link(alias, outside)
    try:
        service, runtime = operation(root, ("passed",))
        result = await service.execute(
            path="alias/notes.md",
            operation=RewriteOperation(content="proposed"),
        )
        assert result.error_code == "target_invalid" and runtime.requests == []
        assert target.read_bytes() == b"external" and not result.written
    finally:
        alias.rmdir() if os.name == "nt" else alias.unlink()


@pytest.mark.asyncio
async def test_retry_rechecks_original_without_repeating_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, runtime = operation(tmp_path, ("passed",))
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    attempts = 0

    def transient(_source: Path, destination: Path) -> None:
        nonlocal attempts
        attempts += 1
        destination.write_bytes(b"competing")
        raise PermissionError("controlled transient replacement denial")

    monkeypatch.setattr("mcp_server.utils.atomic_file_writer.os.replace", transient)
    result = await service.execute(path=target.name, operation=RewriteOperation(content="proposed"))
    assert result.error_code == "original_changed" and not result.written
    assert result.validation_status == "passed"
    assert attempts == 1 and len(runtime.requests) == 1
    assert target.read_bytes() == b"competing"


@pytest.mark.asyncio
@pytest.mark.parametrize("stop", ["invalid_request", "unconfirmed", "cancelled"])
async def test_runtime_stop_retains_prior_checks_and_blocks_report(
    tmp_path: Path,
    stop: str,
) -> None:
    service, runtime = operation(tmp_path, ("failed", stop, "passed"))
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    result = await service.execute(
        path=target.name,
        operation=RewriteOperation(content="proposed"),
        validation="report",
    )
    assert (
        result.error_code
        == {
            "invalid_request": "adapter_request_rejected",
            "unconfirmed": "termination_unconfirmed",
            "cancelled": "operation_interrupted",
        }[stop]
    )
    assert result.validation_status == "failed" and result.checks[0].status == "failed"
    assert result.checks[-1].reason == "not_started"
    assert len(runtime.requests) == 2 and target.read_bytes() == b"original"
    assert not result.written and result.content_changed is None


TRequest = TypeVar("TRequest", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)


@pytest.mark.asyncio
async def test_lock_wait_is_separate_from_validation_and_is_released(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, runtime = operation(tmp_path, ("passed",))
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    entered, release = asyncio.Event(), asyncio.Event()
    actual = runtime.invoke

    async def held(
        *,
        launch: AdapterLaunch,
        workspace_root: Path,
        request: TRequest,
        request_contract: AdapterRequestContract[TRequest],
        response_contract: AdapterResponseContract[TResponse],
        timeout_seconds: float,
    ) -> InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled:
        entered.set()
        await release.wait()
        return await actual(
            launch=launch,
            workspace_root=workspace_root,
            request=request,
            request_contract=request_contract,
            response_contract=response_contract,
            timeout_seconds=timeout_seconds,
        )

    monkeypatch.setattr(runtime, "invoke", held)
    first = asyncio.create_task(
        service.execute(
            path=target.name,
            operation=RewriteOperation(content="first"),
        )
    )
    entered_wait = asyncio.create_task(entered.wait())
    try:
        done, _ = await asyncio.wait(
            (first, entered_wait), timeout=5, return_when=asyncio.FIRST_COMPLETED
        )
        if first in done:
            await first
            pytest.fail("The first edit completed before entering held validation")
        assert entered_wait in done, "The first edit did not enter held validation"
        blocked = await service.execute(
            path=target.name, operation=RewriteOperation(content="second")
        )
        assert blocked.error_code == "preparation_failed"
        assert blocked.error_details is not None
        assert blocked.error_details.model_dump()["reason"] == "lock_wait_timeout"
        assert target.read_bytes() == b"original" and blocked.checks == ()
    finally:
        release.set()
        entered_wait.cancel()
        await asyncio.gather(entered_wait, return_exceptions=True)
        completed = await asyncio.wait_for(first, timeout=5)
    assert completed.written and completed.content_changed is True
    runtime.outcomes = iter(("timeout",))
    timed_out = await service.execute(path=target.name, operation=RewriteOperation(content="third"))
    assert timed_out.error_code == "validation_blocked"
    assert timed_out.checks[0].reason is not None and target.read_bytes() == b"first"


@pytest.mark.asyncio
async def test_postcommit_result_failure_leaves_completed_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, _ = operation(tmp_path, ("passed",))
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")

    def fail_result(**fields: object) -> None:
        assert fields["written"] is True
        raise RuntimeError("controlled result failure after commit")

    monkeypatch.setattr("mcp_server.services.edit_operation.EditOperationOutput", fail_result)
    with pytest.raises(RuntimeError, match="after commit"):
        await service.execute(path=target.name, operation=RewriteOperation(content="proposed"))
    assert target.read_bytes() == b"proposed"


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["write", "write_cleanup", "missing_stage"])
async def test_partial_staging_failure_preserves_original_and_cleanup_facts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    service, _ = operation(tmp_path, ("passed",))
    target = tmp_path / "notes.md"
    target.write_bytes(b"original")
    actual_write, actual_unlink, actual_replace = os.write, Path.unlink, os.replace
    cleanup_denied = failure == "write_cleanup"

    def partial(descriptor: int, payload: bytes) -> int:
        actual_write(descriptor, payload[:3])
        raise OSError("controlled partial stage failure")

    def cleanup(path: Path, missing_ok: bool = False) -> None:
        if cleanup_denied and path.suffix == ".staging":
            raise PermissionError("controlled cleanup denial")
        actual_unlink(path, missing_ok=missing_ok)

    if failure == "missing_stage":

        def lose_stage(source: Path, destination: Path) -> None:
            source.unlink()
            actual_replace(source, destination)

        monkeypatch.setattr("mcp_server.utils.atomic_file_writer.os.replace", lose_stage)
    else:
        monkeypatch.setattr("mcp_server.utils.atomic_file_writer.os.write", partial)
    monkeypatch.setattr(Path, "unlink", cleanup)
    result = await service.execute(path=target.name, operation=RewriteOperation(content="proposed"))
    assert result.error_code == "persistence_failed" and not result.written
    assert result.content_changed is None and result.validation_status == "passed"
    assert target.read_bytes() == b"original"
    assert result.error_details is not None
    assert result.error_details.model_dump()["stage"] == (
        "replace" if failure == "missing_stage" else "write_staging"
    )
    assert bool(result.housekeeping) is cleanup_denied
    if cleanup_denied:
        issue = result.housekeeping[0]
        assert issue.purpose == "write_staging"
        assert (tmp_path / issue.path).read_bytes() == b"pro"
    else:
        assert list(tmp_path.glob("*.staging")) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("original", "command", "expected", "changed"),
    [
        (
            b"alpha\r\nbeta\r\n",
            ReplaceOperation(target_content="beta", replacement="BETA"),
            b"alpha\r\nBETA\r\n",
            True,
        ),
        (
            b"alpha\r\nbeta\r\n",
            ReplaceOperation(target_content="beta", replacement="BETA\nGAMMA"),
            b"alpha\r\nBETA\r\nGAMMA\r\n",
            True,
        ),
        (
            b"alpha\r\n",
            AppendOperation(content="beta"),
            b"alpha\r\nbeta\r\n",
            True,
        ),
        (
            b"alpha\r\nbeta\r\n",
            PatternReplaceOperation(pattern="beta", replacement="BETA"),
            b"alpha\r\nBETA\r\n",
            True,
        ),
        (
            b"a\r\nb\nc\r\n",
            ReplaceOperation(target_content="b\nc", replacement="B\nC"),
            b"a\r\nB\r\nC\r\n",
            True,
        ),
        (
            b"alpha\r\nbeta\nlast\r",
            ReplaceOperation(target_content="beta", replacement="BETA"),
            b"alpha\r\nBETA\nlast\r",
            True,
        ),
        (
            b"a\r\nb\nc\r\n",
            ReplaceOperation(target_content="b\n", replacement="b\n"),
            b"a\r\nb\nc\r\n",
            False,
        ),
        (
            b"a\r\nb\nc\r\n",
            PatternReplaceOperation(pattern="b\n", replacement="b\n", regex=False),
            b"a\r\nb\nc\r\n",
            False,
        ),
        (
            b"a\r\nb\nc\r\n",
            PatternReplaceOperation(pattern=r"b\n", replacement="b\n"),
            b"a\r\nb\nc\r\n",
            False,
        ),
        (
            b"alpha\r\nbeta\r\n",
            PatternReplaceOperation(pattern="absent", replacement="X"),
            b"alpha\r\nbeta\r\n",
            False,
        ),
        (
            b"alpha\r\nbeta\r\n",
            ReplaceOperation(target_content="beta", replacement="BETA\r\nGAMMA"),
            b"alpha\r\nBETA\r\nGAMMA\r\n",
            True,
        ),
        (
            b"alpha\r\nbeta\r\n",
            PatternReplaceOperation(pattern="\n", replacement="\r\n", regex=False),
            b"alpha\r\nbeta\r\n",
            True,
        ),
        (
            b"same\r\nsame\nsame\r\n",
            ReplaceOperation(target_content="same", replacement="X", search_window=(2, 2)),
            b"same\r\nX\nsame\r\n",
            True,
        ),
        (
            b"alpha\r\nbeta\r\n",
            PatternReplaceOperation(pattern=r"(b)(eta)", replacement=r"\2-\1"),
            b"alpha\r\neta-b\r\n",
            True,
        ),
        (
            b"alpha\r\nbeta\r\n",
            PatternReplaceOperation(pattern=r"(?=b)", replacement="X"),
            b"alpha\r\nXbeta\r\n",
            True,
        ),
        (
            b"alpha\nbeta\n",
            ReplaceOperation(target_content="beta", replacement="BETA\r\nGAMMA"),
            b"alpha\nBETA\r\nGAMMA\n",
            True,
        ),
    ],
)
async def test_targeted_edits_preserve_original_line_terminators(
    tmp_path: Path,
    original: bytes,
    command: EditCommand,
    expected: bytes,
    changed: bool,
) -> None:
    service, runtime = operation(tmp_path, ("passed",))
    target = tmp_path / "notes.md"
    target.write_bytes(original)

    result = await service.execute(path=target.name, operation=command)

    assert result.written and result.validation_status == "passed"
    assert result.content_changed is changed
    assert target.read_bytes() == expected
    assert runtime.requests[0][0].model_dump()["content"] == expected.decode("utf-8")
