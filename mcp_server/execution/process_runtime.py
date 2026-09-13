"""One-shot adapter transport, independent of native language and result semantics.

This staged transport is not wired into consumers. Managed process deadlines,
cancellation and descendant lifetime are added by the next process-lifecycle cycle.
"""

from __future__ import annotations

import asyncio
from contextlib import suppress
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from mcp_server.core.interfaces.execution import (
    AdapterLaunch,
    AdapterProcess,
    AdapterProcessBackend,
)
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    AdapterExitCode,
    InvocationCompleted,
    InvocationFailed,
    ProcessCapture,
)
from mcp_server.execution.protocol import (
    READ_CHUNK_SIZE,
    AdapterResponseContract,
    InvalidAdapterResponseError,
    StderrBuffer,
    StdoutBuffer,
)

TResponse = TypeVar("TResponse", bound=BaseModel)


class AsyncioAdapterProcess:
    """Expose independent pipe operations on an already started asyncio process."""

    def __init__(
        self,
        process: asyncio.subprocess.Process,
        stdin: asyncio.StreamWriter,
        stdout: asyncio.StreamReader,
        stderr: asyncio.StreamReader,
    ) -> None:
        self._process = process
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr

    async def write_input(self, payload: bytes) -> None:
        """Send the full request once and close stdin, including on early exit."""
        try:
            self._stdin.write(payload)
            await self._stdin.drain()
        except (BrokenPipeError, ConnectionResetError):
            # The observed exit/output still determines protocol completion.
            pass
        finally:
            self._stdin.close()
        with suppress(BrokenPipeError, ConnectionResetError):
            await self._stdin.wait_closed()

    async def read_stdout(self, maximum: int) -> bytes:
        return await self._stdout.read(maximum)

    async def read_stderr(self, maximum: int) -> bytes:
        return await self._stderr.read(maximum)

    async def wait(self) -> int:
        return await self._process.wait()

    def kill(self) -> None:
        """Request immediate termination; final process facts come from wait."""
        if self._process.returncode is None:
            with suppress(ProcessLookupError):
                self._process.kill()


class AsyncioProcessBackend:
    """Start an explicit argv directly, with no shell or interpreter fallback."""

    async def start(self, launch: AdapterLaunch, workspace_root: Path) -> AdapterProcess:
        if launch.executable is None:
            raise FileNotFoundError("adapter_program_unresolved")
        if not launch.executable.is_absolute() or not workspace_root.is_absolute():
            raise ValueError("adapter_launch_requires_absolute_paths")
        process = await asyncio.create_subprocess_exec(
            str(launch.executable),
            *launch.args,
            cwd=workspace_root,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=READ_CHUNK_SIZE,
        )
        assert process.stdin is not None
        assert process.stdout is not None
        assert process.stderr is not None
        return AsyncioAdapterProcess(process, process.stdin, process.stdout, process.stderr)


class AdapterProcessRuntime:
    """Transport one constructed request through an injected process backend."""

    def __init__(self, backend: AdapterProcessBackend) -> None:
        self._backend = backend

    async def invoke(
        self,
        *,
        launch: AdapterLaunch,
        workspace_root: Path,
        request: BaseModel,
        response_contract: AdapterResponseContract[TResponse],
    ) -> InvocationCompleted[TResponse] | InvocationFailed:
        # Requests are already typed; serialization must not replay admission.
        payload = request.model_dump_json().encode("utf-8")
        stdout = StdoutBuffer()
        stderr = StderrBuffer()
        try:
            process = await self._backend.start(launch, workspace_root)
        except OSError as exc:
            return _failure(
                AdapterCallFailureReason.LAUNCH_FAILED,
                str(exc),
                ProcessCapture(exit_code=None, stdout=stdout.capture(), stderr=stderr.capture()),
            )
        try:
            exit_code = await _exchange(process, payload, stdout, stderr)
        except BaseException:
            # Cleanup never relabels a server defect as adapter unavailability.
            process.kill()
            await process.wait()
            raise
        rejected_capture = ProcessCapture(
            exit_code=exit_code, stdout=stdout.capture(), stderr=stderr.capture()
        )
        if stdout.oversized:
            return _failure(
                AdapterCallFailureReason.RESPONSE_TOO_LARGE,
                "adapter_stdout_limit_exceeded",
                rejected_capture,
            )
        if exit_code not in tuple(int(code) for code in AdapterExitCode):
            return _failure(
                AdapterCallFailureReason.PROCESS_FAILED,
                f"adapter_exit_code:{exit_code}",
                rejected_capture,
            )
        accepted_capture = ProcessCapture(
            exit_code=exit_code, stdout=stdout.capture(accepted=True), stderr=stderr.capture()
        )
        try:
            return response_contract.decode(stdout.data, exit_code, accepted_capture)
        except (ValidationError, InvalidAdapterResponseError) as exc:
            return _failure(
                AdapterCallFailureReason.INVALID_RESPONSE,
                str(exc),
                rejected_capture,
            )


async def _exchange(
    process: AdapterProcess,
    payload: bytes,
    stdout: StdoutBuffer,
    stderr: StderrBuffer,
) -> int:
    async def drain_stdout() -> None:
        while chunk := await process.read_stdout(READ_CHUNK_SIZE):
            already_oversized = stdout.oversized
            stdout.feed(chunk)
            if stdout.oversized and not already_oversized:
                process.kill()

    async def drain_stderr() -> None:
        while chunk := await process.read_stderr(READ_CHUNK_SIZE):
            stderr.feed(chunk)

    async with asyncio.TaskGroup() as group:
        group.create_task(process.write_input(payload))
        group.create_task(drain_stdout())
        group.create_task(drain_stderr())
        completion = group.create_task(process.wait())
    return completion.result()


def _failure(
    reason: AdapterCallFailureReason, message: str, capture: ProcessCapture
) -> InvocationFailed:
    return InvocationFailed(
        outcome="failed",
        failure=AdapterCallFailure(reason=reason, message=message),
        capture=capture,
        termination_problem=None,
    )
