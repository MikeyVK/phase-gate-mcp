"""Generic bounded adapter transport and Windows managed process lifetimes."""

from __future__ import annotations

import asyncio
import ctypes
import logging
import math
import os
from collections.abc import Callable
from contextlib import suppress
from ctypes import wintypes
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ValidationError

from mcp_server.core.interfaces.execution import (
    AdapterLaunch,
    AdapterProcess,
    AdapterProcessBackend,
    AdapterProcessSetupError,
    InvocationScratchDirectories,
)
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    AdapterExitCode,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    ProcessCapture,
    TerminationProblem,
)
from mcp_server.execution.protocol import (
    READ_CHUNK_SIZE,
    AdapterExecutionContext,
    AdapterRequestContract,
    AdapterResponseContract,
    InvalidAdapterResponseError,
    StderrBuffer,
    StdoutBuffer,
)

TRequest = TypeVar("TRequest", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)
TERMINATION_TIMEOUT_SECONDS = 5
PROCESS_POLL_SECONDS = 0.01


class AsyncioAdapterProcess:
    """Own asynchronous pipes and a job covering the adapter's associated work."""

    def __init__(
        self,
        process: asyncio.subprocess.Process,
        stdin: asyncio.StreamWriter,
        stdout: asyncio.StreamReader,
        stderr: asyncio.StreamReader,
        job: WindowsJob,
    ) -> None:
        self._process = process
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        self._job = job

    @property
    def returncode(self) -> int | None:
        return self._process.returncode

    async def write_input(self, payload: bytes) -> None:
        try:
            with suppress(BrokenPipeError, ConnectionResetError):
                self._stdin.write(payload)
                await self._stdin.drain()
        finally:
            self._stdin.close()
        with suppress(BrokenPipeError, ConnectionResetError):
            await self._stdin.wait_closed()

    async def read_stdout(self, maximum: int) -> bytes:
        return await self._stdout.read(maximum)

    async def read_stderr(self, maximum: int) -> bytes:
        return await self._stderr.read(maximum)

    async def wait(self) -> int:
        # Process.wait can also wait for inherited pipes. Observe the leader separately.
        while self._process.returncode is None:
            await asyncio.sleep(PROCESS_POLL_SECONDS)
        return self._process.returncode

    async def wait_finished(self) -> None:
        await self.wait()
        while True:
            self._job.observe_members()
            if self._job.active_processes() == 0 and self._job.members_finished():
                return
            await asyncio.sleep(PROCESS_POLL_SECONDS)

    def kill(self) -> None:
        self._job.terminate()
        if self._process.returncode is None:
            with suppress(ProcessLookupError):
                self._process.kill()

    def close(self) -> None:
        self._stdin.close()
        self._job.close()


class AsyncioProcessBackend:
    """Start a direct argv suspended and assign its job before any adapter work."""

    async def start(self, launch: AdapterLaunch, workspace_root: Path) -> AdapterProcess:
        if launch.executable is None:
            raise FileNotFoundError("adapter_program_unresolved")
        if not launch.executable.is_absolute() or not workspace_root.is_absolute():
            raise ValueError("adapter_launch_requires_absolute_paths")
        job = WindowsJob()  # Unsupported platforms fail; no parent-only fallback.
        process: asyncio.subprocess.Process | None = None
        try:
            process = await asyncio.create_subprocess_exec(
                str(launch.executable),
                *launch.args,
                cwd=workspace_root,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                limit=READ_CHUNK_SIZE,
                creationflags=0x00000004,  # CREATE_SUSPENDED before Job Object assignment.
            )
            assert process.stdin is not None
            assert process.stdout is not None
            assert process.stderr is not None
            owned = AsyncioAdapterProcess(
                process, process.stdin, process.stdout, process.stderr, job
            )
            try:
                job.attach_and_resume(process.pid)
            except OSError as exc:
                raise AdapterProcessSetupError(owned, exc) from exc
            return owned
        except AdapterProcessSetupError:
            raise
        except BaseException:
            if process is not None and process.returncode is None:
                with suppress(ProcessLookupError):
                    process.kill()
            job.close()
            raise


class _CallFailedError(Exception):
    def __init__(self, failure: AdapterCallFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure


@dataclass
class _Invocation:
    """Per-call ownership of pending I/O and bounded observed process facts."""

    process: AdapterProcess | None = None
    finished: bool = False
    stop_unconfirmed: bool = False
    stdout: StdoutBuffer = field(default_factory=StdoutBuffer)
    stderr: StderrBuffer = field(default_factory=StderrBuffer)
    io_tasks: list[asyncio.Task[None]] = field(default_factory=list)
    stop_requested: asyncio.Event = field(default_factory=asyncio.Event)
    stream_failure: AdapterCallFailure | None = None
    stop_deadline: float | None = None

    def capture(self, *, accepted: bool = False) -> ProcessCapture:
        return ProcessCapture(
            exit_code=None if self.process is None else self.process.returncode,
            stdout=self.stdout.capture(accepted=accepted),
            stderr=self.stderr.capture(),
        )

    async def drain_stdout(self, process: AdapterProcess) -> None:
        while chunk := await process.read_stdout(READ_CHUNK_SIZE):
            self.stdout.feed(chunk)
            if self.stdout.oversized and self.stream_failure is None:
                self.stream_failure = AdapterCallFailure(
                    reason=AdapterCallFailureReason.RESPONSE_TOO_LARGE,
                    message="adapter_stdout_limit_exceeded",
                )
                self.stop_requested.set()

    async def drain_stderr(self, process: AdapterProcess) -> None:
        while chunk := await process.read_stderr(READ_CHUNK_SIZE):
            self.stderr.feed(chunk)


class AdapterProcessRuntime:
    """Apply one execution deadline and a separate shared bounded stop budget."""

    def __init__(
        self,
        backend: AdapterProcessBackend,
        scratch: InvocationScratchDirectories,
        *,
        invocation_id: Callable[[], UUID] = uuid4,
    ) -> None:
        self._backend = backend
        self._scratch = scratch
        self._invocation_id = invocation_id

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
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("adapter_execution_budget_must_be_positive")
        deadline = asyncio.get_running_loop().time() + timeout_seconds
        invocation = _Invocation()
        try:
            directory = self._scratch.describe(self._invocation_id())
            self._scratch.create(directory)
        except (OSError, ValueError) as exc:
            return InvocationFailed(
                outcome="failed",
                failure=AdapterCallFailure(
                    reason=AdapterCallFailureReason.LAUNCH_FAILED,
                    message=str(exc) or type(exc).__name__,
                ),
                capture=invocation.capture(),
                termination_problem=None,
            )
        try:
            try:
                context = AdapterExecutionContext(scratch_directory=str(directory.directory))
                payload = request_contract.encode(request, context)
            except ValueError as exc:
                result: InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled = (
                    InvocationFailed(
                        outcome="failed",
                        failure=AdapterCallFailure(
                            reason=AdapterCallFailureReason.LAUNCH_FAILED,
                            message=str(exc) or type(exc).__name__,
                        ),
                        capture=invocation.capture(),
                        termination_problem=None,
                    )
                )
            else:
                result = await self._invoke_owned(
                    invocation, launch, workspace_root, payload, response_contract, deadline
                )
        except BaseException as exc:
            if not invocation.stop_unconfirmed and (
                invocation.process is None or invocation.finished
            ):
                try:
                    self._scratch.remove(directory)
                except (OSError, ValueError) as cleanup_error:
                    exc.add_note(f"invocation_cleanup_failed: {cleanup_error}")
            raise
        if not invocation.stop_unconfirmed and (invocation.process is None or invocation.finished):
            try:
                self._scratch.remove(directory)
            except (OSError, ValueError) as exc:
                cleanup_failure = AdapterCallFailure(
                    reason=AdapterCallFailureReason.PROCESS_FAILED,
                    message=f"invocation_cleanup_failed: {directory.directory}: {exc}",
                )
                if (
                    isinstance(result, InvocationCancelled)
                    or result.capture.exit_code == AdapterExitCode.INVALID_REQUEST
                ):
                    logging.getLogger(__name__).error(
                        "invocation_cleanup_failed",
                        extra={"directory": str(directory.directory), "cause": str(exc)},
                    )
                    return result.model_copy(update={"cleanup_failure": cleanup_failure})
                return InvocationFailed(
                    outcome="failed",
                    failure=cleanup_failure,
                    capture=result.capture,
                    termination_problem=None,
                )
        return result

    async def _invoke_owned(
        self,
        invocation: _Invocation,
        launch: AdapterLaunch,
        workspace_root: Path,
        payload: bytes,
        response_contract: AdapterResponseContract[TResponse],
        deadline: float,
    ) -> InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled:
        if asyncio.get_running_loop().time() >= deadline:
            return InvocationFailed(
                outcome="failed",
                failure=AdapterCallFailure(
                    reason=AdapterCallFailureReason.TIMEOUT, message="adapter_deadline_expired"
                ),
                capture=invocation.capture(),
                termination_problem=None,
            )
        operation = asyncio.create_task(
            self._execute(invocation, launch, workspace_root, payload, response_contract)
        )
        stream_stop = asyncio.create_task(invocation.stop_requested.wait())
        cancelled = False
        failure: AdapterCallFailure | None = None
        try:
            try:
                async with asyncio.timeout_at(deadline):
                    await asyncio.wait(
                        (operation, stream_stop), return_when=asyncio.FIRST_COMPLETED
                    )
                    if asyncio.get_running_loop().time() >= deadline:
                        raise TimeoutError
                    if invocation.stream_failure is not None:
                        failure = invocation.stream_failure
                    else:
                        return operation.result()
            except TimeoutError:
                failure = AdapterCallFailure(
                    reason=AdapterCallFailureReason.TIMEOUT, message="adapter_deadline_expired"
                )
            except asyncio.CancelledError:
                cancelled = True
            except _CallFailedError as exc:
                failure = exc.failure
            except BaseException:
                await _stop_protected(invocation, operation)
                raise
            termination = await _stop_protected(invocation, operation)
            if cancelled:
                return InvocationCancelled(
                    outcome="cancelled",
                    capture=invocation.capture(),
                    termination_problem=termination,
                )
            assert failure is not None
            return InvocationFailed(
                outcome="failed",
                failure=failure,
                capture=invocation.capture(),
                termination_problem=termination,
            )
        finally:
            await _shielded(
                asyncio.create_task(
                    _finish_tasks([operation, stream_stop, *invocation.io_tasks], invocation)
                )
            )
            if invocation.process is not None:
                with suppress(OSError):
                    invocation.process.close()

    async def _execute(
        self,
        invocation: _Invocation,
        launch: AdapterLaunch,
        workspace_root: Path,
        payload: bytes,
        response_contract: AdapterResponseContract[TResponse],
    ) -> InvocationCompleted[TResponse]:
        try:
            process = await self._backend.start(launch, workspace_root)
        except AdapterProcessSetupError as exc:
            invocation.process = exc.process
            invocation.io_tasks.extend(
                (
                    asyncio.create_task(invocation.drain_stdout(exc.process)),
                    asyncio.create_task(invocation.drain_stderr(exc.process)),
                )
            )
            raise _CallFailedError(
                AdapterCallFailure(
                    reason=AdapterCallFailureReason.PROCESS_FAILED,
                    message=str(exc) or type(exc).__name__,
                )
            ) from exc
        except OSError as exc:
            raise _CallFailedError(
                AdapterCallFailure(
                    reason=AdapterCallFailureReason.LAUNCH_FAILED,
                    message=str(exc) or type(exc).__name__,
                )
            ) from exc
        invocation.process = process
        input_task = asyncio.create_task(process.write_input(payload))
        stdout_task = asyncio.create_task(invocation.drain_stdout(process))
        stderr_task = asyncio.create_task(invocation.drain_stderr(process))
        invocation.io_tasks.extend((input_task, stdout_task, stderr_task))
        exit_code = await process.wait()
        if invocation.stream_failure is not None:
            raise _CallFailedError(invocation.stream_failure)
        if exit_code not in tuple(AdapterExitCode):
            raise _CallFailedError(
                AdapterCallFailure(
                    reason=AdapterCallFailureReason.PROCESS_FAILED,
                    message=f"adapter_exit_code:{exit_code}",
                )
            )
        await stdout_task
        if invocation.stream_failure is not None:
            raise _CallFailedError(invocation.stream_failure)
        try:
            response = response_contract.decode(invocation.stdout.data, exit_code)
        except (ValidationError, InvalidAdapterResponseError) as exc:
            raise _CallFailedError(
                AdapterCallFailure(
                    reason=AdapterCallFailureReason.INVALID_RESPONSE, message=str(exc)
                )
            ) from exc
        try:
            await process.wait_finished()
            invocation.finished = True
        except OSError as exc:
            raise _CallFailedError(
                AdapterCallFailure(
                    reason=AdapterCallFailureReason.PROCESS_FAILED,
                    message=str(exc) or type(exc).__name__,
                )
            ) from exc
        await asyncio.gather(input_task, stderr_task)
        return response_contract.complete(response, invocation.capture(accepted=True))


async def _stop_protected(
    invocation: _Invocation, operation: asyncio.Task[InvocationCompleted[TResponse]]
) -> TerminationProblem | None:
    """Keep cancellation and all task cleanup inside one monotone stop deadline."""
    if invocation.stop_deadline is None:
        invocation.stop_deadline = asyncio.get_running_loop().time() + TERMINATION_TIMEOUT_SECONDS
    return await _shielded(asyncio.create_task(_stop(invocation, operation)))


TCleanup = TypeVar("TCleanup")


async def _shielded(task: asyncio.Task[TCleanup]) -> TCleanup:
    while True:
        try:
            return await asyncio.shield(task)
        except asyncio.CancelledError:
            if task.cancelled():
                raise


async def _finish_tasks(tasks: list[asyncio.Task[object]], invocation: _Invocation) -> None:
    for task in tasks:
        task.cancel()
    loop = asyncio.get_running_loop()
    deadline = invocation.stop_deadline
    if deadline is None:
        deadline = loop.time() + TERMINATION_TIMEOUT_SECONDS
    _, pending = await asyncio.wait(tasks, timeout=max(0.0, deadline - loop.time()))
    for task in tasks:
        if task in pending:
            # Cancellation was requested; observe eventual exception disposal without waiting.
            task.add_done_callback(_observe_task)
        else:
            _observe_task(task)


def _observe_task(task: asyncio.Future[object]) -> None:
    with suppress(asyncio.CancelledError):
        task.exception()


async def _stop(
    invocation: _Invocation, operation: asyncio.Task[InvocationCompleted[TResponse]]
) -> TerminationProblem | None:
    assert invocation.stop_deadline is not None
    try:
        async with asyncio.timeout_at(invocation.stop_deadline):
            while invocation.process is None and not operation.done():
                await asyncio.sleep(PROCESS_POLL_SECONDS)
            if invocation.process is None:
                return None
            with suppress(OSError):
                invocation.process.kill()
            await invocation.process.wait_finished()
            invocation.finished = True
            await asyncio.gather(*invocation.io_tasks, return_exceptions=True)
            return None
    except (TimeoutError, OSError):
        invocation.stop_unconfirmed = True
        return TerminationProblem.UNCONFIRMED


class _JobObjectBasicLimitInformation(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class _IoCounters(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _JobObjectExtendedLimitInformation(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JobObjectBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class _JobObjectBasicAccountingInformation(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_longlong),
        ("TotalKernelTime", ctypes.c_longlong),
        ("ThisPeriodTotalUserTime", ctypes.c_longlong),
        ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    ]


class _ThreadEntry32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ThreadID", wintypes.DWORD),
        ("th32OwnerProcessID", wintypes.DWORD),
        ("tpBasePri", ctypes.c_long),
        ("tpDeltaPri", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
    ]


class WindowsJob:
    """Own one Windows Job Object and its assigned suspended process tree."""

    _KILL_ON_JOB_CLOSE = 0x00002000
    _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
    _JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION = 1
    _JOB_OBJECT_BASIC_PROCESS_ID_LIST = 3
    _PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    _SYNCHRONIZE = 0x00100000
    _ERROR_INVALID_PARAMETER = 87
    _ERROR_MORE_DATA = 234
    _PROCESS_TERMINATE = 0x0001
    _PROCESS_SET_QUOTA = 0x0100
    _THREAD_SUSPEND_RESUME = 0x0002
    _TH32CS_SNAPTHREAD = 0x00000004
    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    def __init__(self) -> None:
        if os.name != "nt":
            raise OSError("WindowsJob requires Windows")
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._member_handles: dict[int, wintypes.HANDLE] = {}
        self._observation_failed = False
        self._stop_total_before: int | None = None
        self._configure_api()
        self._handle = self._kernel32.CreateJobObjectW(None, None)
        if not self._handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            limits = _JobObjectExtendedLimitInformation()
            limits.BasicLimitInformation.LimitFlags = self._KILL_ON_JOB_CLOSE
            self._set_information(
                self._JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
                limits,
            )
        except BaseException:
            self.close()
            raise

    def _configure_api(self) -> None:
        kernel32 = self._kernel32
        kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
        kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        kernel32.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            wintypes.INT,
            wintypes.LPVOID,
            wintypes.DWORD,
        ]
        kernel32.SetInformationJobObject.restype = wintypes.BOOL
        kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
        kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        kernel32.TerminateJobObject.restype = wintypes.BOOL
        kernel32.QueryInformationJobObject.argtypes = [
            wintypes.HANDLE,
            wintypes.INT,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        kernel32.QueryInformationJobObject.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL
        kernel32.IsProcessInJob.argtypes = [
            wintypes.HANDLE,
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.BOOL),
        ]
        kernel32.IsProcessInJob.restype = wintypes.BOOL
        kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel32.WaitForSingleObject.restype = wintypes.DWORD
        kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        kernel32.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
        kernel32.Thread32First.restype = wintypes.BOOL
        kernel32.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
        kernel32.Thread32Next.restype = wintypes.BOOL
        kernel32.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel32.OpenThread.restype = wintypes.HANDLE
        kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
        kernel32.ResumeThread.restype = wintypes.DWORD

    def _set_information(self, info_class: int, info: ctypes.Structure) -> None:
        if not self._kernel32.SetInformationJobObject(
            self._handle,
            info_class,
            ctypes.byref(info),
            ctypes.sizeof(info),
        ):
            raise ctypes.WinError(ctypes.get_last_error())

    def _close_handle(self, handle: wintypes.HANDLE) -> None:
        if handle and not self._kernel32.CloseHandle(handle):
            raise ctypes.WinError(ctypes.get_last_error())

    def attach_and_resume(self, pid: int) -> None:
        """Assign a suspended process to this job before resuming its threads."""
        process = self._kernel32.OpenProcess(
            self._PROCESS_SET_QUOTA
            | self._PROCESS_TERMINATE
            | self._PROCESS_QUERY_LIMITED_INFORMATION
            | self._SYNCHRONIZE,
            False,
            pid,
        )
        if not process:
            raise ctypes.WinError(ctypes.get_last_error())
        retained = False
        try:
            if not self._kernel32.AssignProcessToJobObject(self._handle, process):
                raise ctypes.WinError(ctypes.get_last_error())
            self._member_handles[pid] = process
            retained = True
            try:
                self._resume_threads(pid)
            except BaseException:
                self.terminate()
                raise
        finally:
            if not retained:
                self._close_handle(process)

    def _resume_threads(self, pid: int) -> None:
        snapshot = self._kernel32.CreateToolhelp32Snapshot(self._TH32CS_SNAPTHREAD, 0)
        if not snapshot or snapshot == self._INVALID_HANDLE_VALUE:
            raise ctypes.WinError(ctypes.get_last_error())
        resumed = 0
        try:
            entry = _ThreadEntry32()
            entry.dwSize = ctypes.sizeof(_ThreadEntry32)
            if not self._kernel32.Thread32First(snapshot, ctypes.byref(entry)):
                raise ctypes.WinError(ctypes.get_last_error())
            while True:
                if entry.th32OwnerProcessID == pid:
                    thread = self._kernel32.OpenThread(
                        self._THREAD_SUSPEND_RESUME,
                        False,
                        entry.th32ThreadID,
                    )
                    if not thread:
                        raise ctypes.WinError(ctypes.get_last_error())
                    try:
                        if self._kernel32.ResumeThread(thread) == 0xFFFFFFFF:
                            raise ctypes.WinError(ctypes.get_last_error())
                        resumed += 1
                    finally:
                        self._close_handle(thread)
                if not self._kernel32.Thread32Next(snapshot, ctypes.byref(entry)):
                    error = ctypes.get_last_error()
                    if error != 18:  # ERROR_NO_MORE_FILES
                        raise ctypes.WinError(error)
                    break
        finally:
            self._close_handle(snapshot)
        if resumed == 0:
            raise OSError("suspended_process_thread_not_found")

    def _member_pids(self) -> tuple[int, ...]:
        """Read the complete current Job member list, including nested jobs."""
        capacity = 8
        while capacity <= 65536:
            buffer = ctypes.create_string_buffer(8 + capacity * ctypes.sizeof(ctypes.c_size_t))
            returned = wintypes.DWORD()
            if not self._kernel32.QueryInformationJobObject(
                self._handle,
                self._JOB_OBJECT_BASIC_PROCESS_ID_LIST,
                buffer,
                ctypes.sizeof(buffer),
                ctypes.byref(returned),
            ):
                error = ctypes.get_last_error()
                if error == self._ERROR_MORE_DATA:
                    capacity *= 2
                    continue
                raise ctypes.WinError(error)
            assigned = wintypes.DWORD.from_buffer(buffer, 0).value
            listed = wintypes.DWORD.from_buffer(buffer, 4).value
            if listed < assigned:
                capacity = max(capacity * 2, assigned)
                continue
            if listed > capacity:
                raise OSError("job_member_list_invalid")
            ids = (ctypes.c_size_t * listed).from_buffer(buffer, 8)
            return tuple(int(pid) for pid in ids)
        raise OSError("job_member_list_too_large")

    def observe_members(self) -> None:
        """Retain handles to original Job members before their PIDs can be reused."""
        try:
            for pid in self._member_pids():
                if pid in self._member_handles:
                    continue
                handle = self._kernel32.OpenProcess(
                    self._SYNCHRONIZE | self._PROCESS_QUERY_LIMITED_INFORMATION,
                    False,
                    pid,
                )
                if not handle:
                    error = ctypes.get_last_error()
                    if error == self._ERROR_INVALID_PARAMETER:
                        continue  # Member exited between the Job query and OpenProcess.
                    raise ctypes.WinError(error)
                retained = False
                try:
                    membership = wintypes.BOOL()
                    if not self._kernel32.IsProcessInJob(
                        handle, self._handle, ctypes.byref(membership)
                    ):
                        raise ctypes.WinError(ctypes.get_last_error())
                    if membership.value:
                        self._member_handles[pid] = handle
                        retained = True
                finally:
                    if not retained:
                        self._close_handle(handle)
        except OSError:
            self._observation_failed = True
            raise

    def members_finished(self) -> bool:
        """Confirm every assigned process was observed and its handle is signaled."""
        if self._observation_failed:
            raise OSError("job_member_observation_failed")
        if (
            self._stop_total_before is not None
            and self.total_processes() != self._stop_total_before
        ):
            self._observation_failed = True
            raise OSError("job_member_started_during_stop")
        for handle in self._member_handles.values():
            status = int(self._kernel32.WaitForSingleObject(handle, 0))
            if status == 258:  # WAIT_TIMEOUT
                return False
            if status != 0:  # WAIT_OBJECT_0
                raise ctypes.WinError(ctypes.get_last_error())
        return True

    def _accounting(self) -> _JobObjectBasicAccountingInformation:
        info = _JobObjectBasicAccountingInformation()
        returned = wintypes.DWORD()
        if not self._kernel32.QueryInformationJobObject(
            self._handle,
            self._JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION,
            ctypes.byref(info),
            ctypes.sizeof(info),
            ctypes.byref(returned),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        return info

    def active_processes(self) -> int:
        """Return the number of currently active processes in this job."""
        return int(self._accounting().ActiveProcesses)

    def total_processes(self) -> int:
        """Return the cumulative number of processes ever assigned to this job."""
        return int(self._accounting().TotalProcesses)

    def terminate(self) -> None:
        """Detect members born between the snapshot and Job termination."""
        try:
            total_before: int | None = self.total_processes()
        except OSError:
            total_before = None
            self._observation_failed = True
        self._stop_total_before = total_before
        try:
            self.observe_members()
        finally:
            if not self._kernel32.TerminateJobObject(self._handle, 1):
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                total_after = self.total_processes()
            except OSError:
                self._observation_failed = True
            else:
                if total_before is None or total_after != total_before:
                    self._observation_failed = True

    def close(self) -> None:
        """Close retained process handles and the owned kill-on-close Job handle."""
        error: OSError | None = None
        for member in self._member_handles.values():
            try:
                self._close_handle(member)
            except OSError as exc:
                error = error or exc
        self._member_handles.clear()
        handle = self._handle
        if handle:
            try:
                self._close_handle(handle)
            except OSError as exc:
                error = error or exc
            self._handle = None
        if error is not None:
            raise error
