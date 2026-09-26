"""Observe managed Windows lifetimes with real Node parent/parallel-child processes."""

from __future__ import annotations

import asyncio
import ctypes
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from shutil import which

import pytest

from mcp_server.core.interfaces.execution import (
    AdapterLaunch,
    AdapterProcess,
    AdapterProcessBackend,
)
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    TerminationProblem,
)
from mcp_server.execution.process_runtime import (
    AdapterProcessRuntime,
    AsyncioProcessBackend,
    WindowsJob,
)
from mcp_server.execution.protocol import STDERR_LIMIT, STDOUT_LIMIT
from tests.mcp_server.fixtures.adapter_process import ProcessRequest, response_contract
from tests.mcp_server.fixtures.suite_roots import write_package_tree

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.slow,
    pytest.mark.skipif(sys.platform != "win32", reason="Windows lifecycle evidence"),
]

LIFECYCLE_SCRIPT = r"""
const fs = require('node:fs');
const {spawn} = require('node:child_process');
const [mode, root, label] = process.argv.slice(2);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
async function main() {
  if (mode === 'child') {
    fs.writeFileSync(root + '/' + label + '.pid', String(process.pid));
    while (!fs.existsSync(root + '/' + label + '.armed')) await sleep(5);
    await sleep(Number(process.argv[5]));
    fs.writeFileSync(root + '/' + label + '.done', 'finished');
    return;
  }
  fs.writeFileSync(root + '/parent.pid', String(process.pid));
  for await (const chunk of process.stdin) { /* Consume the request through EOF. */ }
  const duration = mode === 'normal' ? '350' : '15000';
  for (const name of ['first', 'second']) {
    const child = spawn(process.execPath, [__filename, 'child', root, name, duration],
                        {stdio: 'ignore', detached: true});
    child.unref();
  }
  while (!fs.existsSync(root + '/first.pid') || !fs.existsSync(root + '/second.pid'))
    await sleep(5);
  while (!fs.existsSync(root + '/first.armed') || !fs.existsSync(root + '/second.armed'))
    await sleep(5);
  const response = JSON.stringify({decision: {status: 'passed'}, external_tools: [],
                                  evidence: {format: 'text', data: '{}'}});
  if (mode === 'oversize') {
    process.stdout.write(' '.repeat(8 * 1024 * 1024 + 1));
    setInterval(() => {}, 1000);
  } else {
    process.stdout.write(mode === 'invalid' ? '{broken' : response);
    process.stderr.write('x'.repeat(256 * 1024 + 37));
    process.exitCode = mode === 'crash' ? 42 : 0;
  }
}
main().catch(error => {process.stderr.write(String(error)); process.exitCode = 42;});
"""


@dataclass(frozen=True)
class LifecycleCase:
    launch: AdapterLaunch
    root: Path
    request: ProcessRequest


@pytest.fixture
def lifecycle_case(tmp_path: Path) -> LifecycleCase:
    node = which("node")
    assert node is not None, "Node is required for real lifecycle evidence"
    write_package_tree(
        tmp_path, {"lifecycle.cjs": LIFECYCLE_SCRIPT.encode(), "target.txt": b"keep"}
    )
    return LifecycleCase(
        AdapterLaunch(Path(node).resolve(), (str(tmp_path / "lifecycle.cjs"),)),
        tmp_path,
        ProcessRequest(
            operation="echo", target_path=str(tmp_path / "target.txt"), content="proposal", args=()
        ),
    )


def launch_for(case: LifecycleCase, mode: str) -> AdapterLaunch:
    return AdapterLaunch(case.launch.executable, (*case.launch.args, mode, str(case.root)))


async def wait_for_children(case: LifecycleCase) -> None:
    async with asyncio.timeout(5):
        while not all((case.root / f"{name}.pid").exists() for name in ("first", "second")):
            await asyncio.sleep(0.01)


def child_pids(case: LifecycleCase) -> tuple[int, ...]:
    return tuple(int((case.root / f"{name}.pid").read_text()) for name in ("first", "second"))


def _process_api() -> ctypes.WinDLL:
    """Bind only the Windows calls needed for original-process observations."""
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.WaitForSingleObject.restype = wintypes.DWORD
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    return kernel


def _open_process(pid: int) -> int:
    handle = _process_api().OpenProcess(0x00100000, False, pid)  # SYNCHRONIZE only.
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    return int(handle)


def _handle_is_alive(handle: int) -> bool:
    """Inspect a retained handle, never a later lookup of a reusable PID."""
    status = int(_process_api().WaitForSingleObject(handle, 0))
    assert status in (0, 258)
    return status == 258


@contextmanager
def retained_children(case: LifecycleCase) -> Iterator[tuple[int, ...]]:
    """Hold both original children while the invocation completes."""
    kernel = _process_api()
    handles: list[int] = []
    try:
        for pid in child_pids(case):
            handles.append(_open_process(pid))
        for name in ("first", "second"):
            (case.root / f"{name}.armed").touch()
        yield tuple(handles)
    finally:
        for handle in handles:
            assert kernel.CloseHandle(handle)


async def test_response_and_parent_exit_wait_for_parallel_work(
    lifecycle_case: LifecycleCase,
) -> None:
    task = asyncio.create_task(
        AdapterProcessRuntime(AsyncioProcessBackend()).invoke(
            launch=launch_for(lifecycle_case, "normal"),
            workspace_root=lifecycle_case.root,
            request=lifecycle_case.request,
            response_contract=response_contract(),
            timeout_seconds=5,
        )
    )
    await wait_for_children(lifecycle_case)
    with retained_children(lifecycle_case) as children:
        result = await task
        assert not any(_handle_is_alive(handle) for handle in children)
    assert isinstance(result, InvocationCompleted)
    assert all((lifecycle_case.root / f"{name}.done").exists() for name in ("first", "second"))
    assert result.capture.stderr.observed_bytes == STDERR_LIMIT + 37
    assert result.capture.stderr.truncated
    assert (lifecycle_case.root / "target.txt").read_text() == "keep"


@pytest.mark.parametrize(
    "mode, reason",
    [
        ("late", AdapterCallFailureReason.TIMEOUT),
        ("crash", AdapterCallFailureReason.PROCESS_FAILED),
        ("invalid", AdapterCallFailureReason.INVALID_RESPONSE),
        ("oversize", AdapterCallFailureReason.RESPONSE_TOO_LARGE),
    ],
)
async def test_failure_stops_live_children_and_keeps_primary_cause(
    lifecycle_case: LifecycleCase, mode: str, reason: AdapterCallFailureReason
) -> None:
    task = asyncio.create_task(
        AdapterProcessRuntime(AsyncioProcessBackend()).invoke(
            launch=launch_for(lifecycle_case, mode),
            workspace_root=lifecycle_case.root,
            request=lifecycle_case.request,
            response_contract=response_contract(),
            timeout_seconds=1 if mode == "late" else 5,
        )
    )
    await wait_for_children(lifecycle_case)
    with retained_children(lifecycle_case) as children:
        result = await task
        assert not any(_handle_is_alive(handle) for handle in children)
    assert isinstance(result, InvocationFailed)
    assert result.failure.reason is reason
    assert result.termination_problem is None
    assert not any(lifecycle_case.root.glob("*.done"))
    assert (lifecycle_case.root / "target.txt").read_text() == "keep"
    assert result.capture.stdout.head is not None
    if mode == "oversize":
        assert result.capture.stdout.observed_bytes >= STDOUT_LIMIT + 1
        assert len(result.capture.stdout.head.encode()) <= STDOUT_LIMIT
        assert result.capture.stdout.truncated


async def test_cancellation_is_typed_and_confirmed_before_return(
    lifecycle_case: LifecycleCase,
) -> None:
    task = asyncio.create_task(
        AdapterProcessRuntime(AsyncioProcessBackend()).invoke(
            launch=launch_for(lifecycle_case, "late"),
            workspace_root=lifecycle_case.root,
            request=lifecycle_case.request,
            response_contract=response_contract(),
            timeout_seconds=20,
        )
    )
    await wait_for_children(lifecycle_case)
    with retained_children(lifecycle_case) as children:
        task.cancel()
        result = await task
        assert not any(_handle_is_alive(handle) for handle in children)
    assert isinstance(result, InvocationCancelled)
    assert result.termination_problem is None
    assert (lifecycle_case.root / "target.txt").read_text() == "keep"


@dataclass(frozen=True)
class WithheldStopProcess:
    """Fault injection with real streams, exits and children; only stop is denied."""

    process: AdapterProcess

    @property
    def returncode(self) -> int | None:
        return self.process.returncode

    async def write_input(self, payload: bytes) -> None:
        await self.process.write_input(payload)

    async def read_stdout(self, maximum: int) -> bytes:
        return await self.process.read_stdout(maximum)

    async def read_stderr(self, maximum: int) -> bytes:
        return await self.process.read_stderr(maximum)

    async def wait(self) -> int:
        return await self.process.wait()

    async def wait_finished(self) -> None:
        await self.process.wait_finished()

    def kill(self) -> None:
        raise PermissionError("injected OS stop refusal")

    def close(self) -> None:
        # The fixture owns final cleanup so independent evidence can inspect live work.
        pass


class WithheldStopBackend:
    def __init__(self, backend: AdapterProcessBackend) -> None:
        self.backend = backend
        self.process: AdapterProcess | None = None

    async def start(self, launch: AdapterLaunch, workspace_root: Path) -> AdapterProcess:
        self.process = await self.backend.start(launch, workspace_root)
        return WithheldStopProcess(self.process)


@pytest.mark.parametrize("cancel", [False, True], ids=["timeout", "cancellation"])
async def test_unconfirmed_stop_preserves_cause_and_shared_five_second_budget(
    lifecycle_case: LifecycleCase, cancel: bool
) -> None:
    backend = WithheldStopBackend(AsyncioProcessBackend())
    start = time.monotonic()
    task = asyncio.create_task(
        AdapterProcessRuntime(backend).invoke(
            launch=launch_for(lifecycle_case, "late"),
            workspace_root=lifecycle_case.root,
            request=lifecycle_case.request,
            response_contract=response_contract(),
            timeout_seconds=20 if cancel else 1,
        )
    )
    try:
        await wait_for_children(lifecycle_case)
        with retained_children(lifecycle_case) as children:
            if cancel:
                start = time.monotonic()
                task.cancel()
            result = await task
            elapsed = time.monotonic() - start
            assert 4.5 <= elapsed < 8.5
            if cancel:
                assert isinstance(result, InvocationCancelled)
                assert InvocationCancelled.model_validate_json(result.model_dump_json()) == result
            else:
                assert isinstance(result, InvocationFailed)
                assert result.failure.reason is AdapterCallFailureReason.TIMEOUT
                assert InvocationFailed.model_validate_json(result.model_dump_json()) == result
            assert result.termination_problem is TerminationProblem.UNCONFIRMED
            assert all(_handle_is_alive(handle) for handle in children)
        assert result.capture.exit_code == 0
        assert result.capture.stdout.head is not None
        assert result.capture.stderr.observed_bytes == STDERR_LIMIT + 37
        assert (lifecycle_case.root / "target.txt").read_text() == "keep"
    finally:
        if backend.process is not None:
            backend.process.kill()
            await asyncio.wait_for(backend.process.wait_finished(), 5)
            backend.process.close()
        if not task.done():
            task.cancel()
            await task


async def test_setup_failure_retains_created_process_and_confirms_its_stop(
    lifecycle_case: LifecycleCase, monkeypatch: pytest.MonkeyPatch
) -> None:
    observed_pids: list[int] = []
    observed_handles: list[int] = []

    def fail_assignment(_job: WindowsJob, pid: int) -> None:
        observed_pids.append(pid)
        observed_handles.append(_open_process(pid))
        raise OSError("injected job assignment failure")

    monkeypatch.setattr(WindowsJob, "attach_and_resume", fail_assignment)
    try:
        result = await AdapterProcessRuntime(AsyncioProcessBackend()).invoke(
            launch=launch_for(lifecycle_case, "normal"),
            workspace_root=lifecycle_case.root,
            request=lifecycle_case.request,
            response_contract=response_contract(),
            timeout_seconds=5,
        )
        assert isinstance(result, InvocationFailed)
        assert result.failure.reason is AdapterCallFailureReason.PROCESS_FAILED
        assert result.capture.exit_code is not None
        assert result.termination_problem is None
        assert len(observed_pids) == len(observed_handles) == 1
        assert not _handle_is_alive(observed_handles[0])
    finally:
        kernel = _process_api()
        for handle in observed_handles:
            assert kernel.CloseHandle(handle)
