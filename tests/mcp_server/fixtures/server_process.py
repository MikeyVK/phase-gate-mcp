# template=generic version=f35abd82 created=2026-09-17T16:47Z updated=
"""Reliable JSON-RPC stdio fixture for MCP server subprocesses.

@layer: Tests (Fixtures)
@dependencies: [subprocess, json]
@responsibilities:
    - Spawn an explicitly configured subprocess
    - Drain JSON-RPC stdout and diagnostic stderr concurrently
    - Perform MCP handshake and tool discovery
    - Ensure bounded process termination
"""

from __future__ import annotations

import json
import queue
import subprocess
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import Any, TextIO


class ServerProcess:
    """Run an explicitly configured MCP subprocess over line-delimited JSON-RPC."""

    def __init__(
        self,
        command: list[str],
        *,
        cwd: Path,
        env: dict[str, str],
        timeout: float = 30.0,
    ) -> None:
        if not command:
            raise ValueError("command must contain at least one executable")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.command = list(command)
        self.cwd = Path(cwd)
        self.env = dict(env)
        self.timeout = timeout
        self._process: subprocess.Popen[str] | None = None
        self._next_id = 1
        self._stdout_queue: queue.Queue[str | None] = queue.Queue()
        self._stderr_lines: list[str] = []
        self._stderr_lock = threading.Lock()
        self._reader_threads: list[threading.Thread] = []

    @property
    def process(self) -> subprocess.Popen[str]:
        if self._process is None:
            raise RuntimeError("ServerProcess is not running")
        return self._process

    def start(self) -> ServerProcess:
        """Start the configured subprocess and its stdout/stderr drainers."""
        if self._process is not None:
            raise RuntimeError("ServerProcess is already running")

        self._stdout_queue = queue.Queue()
        self._stderr_lines = []
        self._reader_threads = []
        self._process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.cwd,
            env=self.env,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        assert self._process.stdout is not None
        assert self._process.stderr is not None
        self._start_reader(self._process.stdout, self._stdout_queue)
        self._start_reader(self._process.stderr, None)
        return self

    def _start_reader(
        self,
        stream: TextIO,
        output_queue: queue.Queue[str | None] | None,
    ) -> None:
        def drain() -> None:
            try:
                for line in stream:
                    if output_queue is not None:
                        output_queue.put(line)
                    else:
                        with self._stderr_lock:
                            self._stderr_lines.append(line)
            finally:
                if output_queue is not None:
                    output_queue.put(None)

        reader = threading.Thread(target=drain, name="server-process-reader", daemon=True)
        reader.start()
        self._reader_threads.append(reader)

    def _stderr_text(self) -> str:
        with self._stderr_lock:
            return "".join(self._stderr_lines)

    def _write(self, payload: dict[str, Any]) -> None:
        proc = self.process
        if proc.stdin is None:
            raise RuntimeError("stdin is not connected")
        try:
            proc.stdin.write(json.dumps(payload) + "\n")
            proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise RuntimeError(
                f"Failed to send JSON-RPC message; subprocess exited with code {proc.poll()}. "
                f"stderr: {self._stderr_text()}"
            ) from exc

    def send_notification(self, method: str, params: dict[str, Any] | None = None) -> None:
        """Send a JSON-RPC notification without waiting for a response."""
        self._write({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def send_request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        req_id: int | None = None,
    ) -> dict[str, Any]:
        """Send a JSON-RPC request and await its matching response."""
        current_id = self._next_id if req_id is None else req_id
        self._next_id = current_id + 1
        self._write(
            {
                "jsonrpc": "2.0",
                "id": current_id,
                "method": method,
                "params": params or {},
            }
        )

        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(
                    f"Timeout waiting for response to {method} (id={current_id}). "
                    f"stderr: {self._stderr_text()}"
                )
            try:
                response_line = self._stdout_queue.get(timeout=remaining)
            except queue.Empty as exc:
                raise TimeoutError(
                    f"Timeout waiting for response to {method} (id={current_id}). "
                    f"stderr: {self._stderr_text()}"
                ) from exc

            if response_line is None:
                proc = self.process
                raise RuntimeError(
                    f"Subprocess terminated unexpectedly with code {proc.poll()}. "
                    f"stderr: {self._stderr_text()}"
                )

            stripped = response_line.strip()
            if not stripped:
                continue
            try:
                response = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Received invalid JSON-RPC output while waiting for {method}: "
                    f"{stripped!r}; stderr: {self._stderr_text()}"
                ) from exc
            if not isinstance(response, dict):
                raise RuntimeError(f"Received non-object JSON-RPC response: {response!r}")
            if "error" in response:
                raise RuntimeError(
                    f"JSON-RPC request {method} (id={current_id}) failed: {response['error']!r}"
                )
            if response.get("id") != current_id:
                continue
            return response

    def initialize(
        self,
        client_name: str = "test-client",
        client_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """Perform the standard MCP initialize handshake."""
        response = self.send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": client_name, "version": client_version},
            },
        )
        self.send_notification("notifications/initialized")
        result = response.get("result", {})
        if not isinstance(result, dict):
            raise RuntimeError(f"Invalid initialize result: {result!r}")
        return result

    def list_tools(self) -> list[dict[str, Any]]:
        """Query tools/list and return the published tools."""
        response = self.send_request("tools/list", {})
        result = response.get("result", {})
        if not isinstance(result, dict) or not isinstance(result.get("tools"), list):
            raise RuntimeError(f"Invalid tools/list result: {result!r}")
        return result["tools"]

    def list_resources(self) -> list[dict[str, Any]]:
        """Query resources/list and return the published resources."""
        response = self.send_request("resources/list", {})
        result = response.get("result", {})
        if not isinstance(result, dict) or not isinstance(result.get("resources"), list):
            raise RuntimeError(f"Invalid resources/list result: {result!r}")
        return result["resources"]

    def close(self) -> tuple[int, str]:
        """Close the process within the configured timeout and return code/stderr."""
        proc = self._process
        if proc is None:
            return 0, ""

        deadline = time.monotonic() + self.timeout
        if proc.stdin is not None:
            with suppress(OSError):
                proc.stdin.close()

        try:
            self._wait_until(proc, deadline)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                self._wait_until(proc, deadline)
            except subprocess.TimeoutExpired:
                proc.kill()
                with suppress(subprocess.TimeoutExpired):
                    proc.wait(timeout=0.1)

        for reader in self._reader_threads:
            remaining = max(0.0, deadline - time.monotonic())
            reader.join(timeout=remaining)
        self._process = None
        self._reader_threads = []
        return proc.returncode if proc.returncode is not None else -1, self._stderr_text()

    @staticmethod
    def _wait_until(proc: subprocess.Popen[str], deadline: float) -> None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise subprocess.TimeoutExpired(proc.args, 0)
        proc.wait(timeout=remaining)

    def __enter__(self) -> ServerProcess:
        return self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


@contextmanager
def run_server_process(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: float = 30.0,
) -> Iterator[ServerProcess]:
    """Convenience context manager for an explicitly configured ServerProcess."""
    server = ServerProcess(command, cwd=cwd, env=env, timeout=timeout)
    with server:
        yield server
