#!/usr/bin/env python3
"""Forward MCP stdio with generation-owned readers and explicit restart outcomes."""

import contextlib
import copy
import io
import json
import math
import os
import re
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, TypeAlias

from mcp.types import InitializeResult

from mcp_server.presenters.startup_recovery_presenter import present_proxy_event

# RESTART_MARKER: Printed to stderr by server to signal restart request
# Proxy detects this marker and triggers transparent server restart
RESTART_MARKER = "__MCP_RESTART_REQUEST__"


def fix_json_surrogates(json_str: str) -> str:
    """Fix malformed Unicode surrogate pairs in JSON strings.

    VS Code sometimes sends emoji as broken surrogate pairs (e.g. \\uD83D\\uDE80
    split across encoding boundaries). This fixes those cases by:
    1. Finding surrogate pair patterns
    2. Converting to proper UTF-8
    3. Re-encoding as valid JSON escape sequences

    Args:
        json_str: Raw JSON string potentially containing malformed surrogates

    Returns:
        Fixed JSON string safe for Python json.loads()
    """
    # Pattern: \uD800-\uDBFF (high surrogate) followed by \uDC00-\uDFFF (low surrogate)
    surrogate_pattern = re.compile(
        r"\\u([dD][8-9a-bA-B][0-9a-fA-F]{2})\\u([dD][c-fC-F][0-9a-fA-F]{2})"
    )

    def replace_surrogate_pair(match: re.Match[str]) -> str:
        high = int(match.group(1), 16)
        low = int(match.group(2), 16)

        # Convert surrogate pair to Unicode codepoint
        # Formula: (high - 0xD800) * 0x400 + (low - 0xDC00) + 0x10000
        codepoint = (high - 0xD800) * 0x400 + (low - 0xDC00) + 0x10000

        # Convert to UTF-8 character
        try:
            return chr(codepoint)
        except (ValueError, OverflowError):
            # Invalid codepoint - replace with Unicode replacement character
            return "\ufffd"

    return surrogate_pattern.sub(replace_surrogate_pair, json_str)


def _setup_utf8_encoding() -> None:
    """Force UTF-8 encoding on Windows stdout/stderr.

    CRITICAL: Prevents 'charmap' codec errors when forwarding Unicode.
    Only runs in production (not during pytest imports).
    """
    if sys.platform == "win32" and "pytest" not in sys.modules:
        # Reconfigure stdin to read UTF-8 bytes correctly
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding="utf-8",
            errors="replace",
            line_buffering=True,
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer,
            encoding="utf-8",
            errors="replace",
            line_buffering=True,
        )


RpcId: TypeAlias = str | int | None
TransportState: TypeAlias = Literal["starting", "ready", "restarting", "unavailable", "stopped"]
EventPresenter: TypeAlias = Callable[[str, Mapping[str, object]], str]
ProcessFactory: TypeAlias = Callable[[dict[str, str]], subprocess.Popen[str]]


def launch_server(env: dict[str, str]) -> subprocess.Popen[str]:
    """Compose the child process used by the standalone proxy entry point."""
    return subprocess.Popen(
        [sys.executable, "-m", "mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace",
    )


@dataclass
class _Child:
    """Private mutable lifecycle owner; never exposed as a query value object."""

    number: int
    process: subprocess.Popen[str]
    is_restart: bool
    started_at: float
    pending: set[RpcId] = field(default_factory=set)
    initialize_request: dict[str, Any] | None = None
    initialize_response_seen: bool = False
    initialized: bool = False
    failed: bool = False
    restart_requested: bool = False
    handshake_done: threading.Event = field(default_factory=threading.Event)
    timer: threading.Timer | None = None
    deadline: float | None = None


def _message_id(message: dict[str, Any]) -> RpcId:
    """Narrow the JSON-RPC correlation identity at the input boundary."""
    value: object = message["id"]
    if isinstance(value, bool) or not isinstance(value, (str, int, type(None))):
        raise ValueError("invalid_jsonrpc_id")
    return value


class MCPProxy:
    """Own transparent child replacement and correlated stdio forwarding."""

    def __init__(
        self,
        *,
        process_factory: ProcessFactory = launch_server,
        event_presenter: EventPresenter = present_proxy_event,
        initialization_timeout_seconds: float = 30.0,
    ) -> None:
        if not math.isfinite(initialization_timeout_seconds) or initialization_timeout_seconds <= 0:
            raise ValueError("positive_initialization_timeout_required")
        _setup_utf8_encoding()
        self._process_factory = process_factory
        self._event_presenter = event_presenter
        self._initialization_timeout = initialization_timeout_seconds
        self._child: _Child | None = None
        self._generation = 0
        self._state: TransportState = "starting"
        self._stopped = False
        self._output_available = True
        self._protocol_version: str | int | None = None
        self._restart_started_at: float | None = None
        self.init_request: dict[str, Any] | None = None
        self.restart_count = 0
        self.proxy_pid = os.getpid()
        self.lock = threading.RLock()
        self._lifecycle_lock = threading.Lock()
        self._stdout_lock = threading.Lock()
        self._log_lock = threading.Lock()
        workspace = os.environ.get("PGMCP_WORKSPACE_ROOT") or os.getcwd()
        server_dir = os.environ.get("PGMCP_SERVER_PROJECT_DIR") or ".pgmcp"
        logs_dir = os.environ.get("PGMCP_LOGS_DIR") or "logs"
        self._logs_dir = Path(workspace) / server_dir / logs_dir

    @property
    def server_process(self) -> subprocess.Popen[str] | None:
        """Read the active process identity, including an exited active generation."""
        with self.lock:
            return self._child.process if self._child is not None else None

    @property
    def restarting(self) -> bool:
        """Read transport state without changing it."""
        with self.lock:
            return self._state == "restarting"

    def audit_log(self, message: str, level: str = "INFO", **fields: object) -> None:
        """Persist the event snapshot; do not re-read another generation's PID."""
        try:
            self._logs_dir.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": datetime.now(UTC).isoformat(),
                "level": level,
                "logger": "mcp_proxy",
                "message": message,
                "proxy_pid": self.proxy_pid,
                **fields,
            }
            with (self._logs_dir / "mcp_audit.log").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError as error:
            sys.stderr.write(
                self._event_presenter("audit_log_failed", {"error": str(error)}) + "\n"
            )
            sys.stderr.flush()

    def _event(self, event_type: str, level: str = "INFO", **fields: object) -> None:
        with self.lock:
            child = self._child
            snapshot: dict[str, object] = {
                "server_pid": child.process.pid if child is not None else None,
                "generation": child.number if child is not None else self._generation,
                "restart_count": self.restart_count,
                **fields,
            }
        message = self._event_presenter(event_type, snapshot)
        with self._log_lock:
            sys.stderr.write(message + "\n")
            sys.stderr.flush()
            self.audit_log(message, level=level, event_type=event_type, **snapshot)

    def _write_client(self, message: dict[str, Any]) -> None:
        """Serialize protocol frames without interleaved writes from worker threads."""
        with self._stdout_lock:
            if not self._output_available:
                return
            try:
                sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
                sys.stdout.flush()
            except (OSError, ValueError):
                self._output_available = False

    def _unavailable(self, identifier: RpcId, reason: str, child: _Child | None) -> None:
        fields: dict[str, object] = {
            "code": "ERR_SERVER_UNAVAILABLE",
            "state": self._state,
            "generation": child.number if child is not None else self._generation,
            "server_pid": child.process.pid if child is not None else None,
            "reason": reason,
        }
        self._write_client(
            {
                "jsonrpc": "2.0",
                "id": identifier,
                "error": {
                    "code": -32000,
                    "message": self._event_presenter("server_unavailable", fields),
                    "data": fields,
                },
            }
        )

    def _fail_pending(self, child: _Child, reason: str) -> None:
        for identifier in tuple(child.pending):
            child.pending.remove(identifier)
            self._unavailable(identifier, reason, child)

    def _cancel_deadline(self, child: _Child) -> None:
        if child.timer is not None:
            child.timer.cancel()
            child.timer = None

    def _mark_failed(self, child: _Child, reason: str, **details: object) -> None:
        """Command called under the state lock; finish identities only once."""
        if child.failed:
            return
        child.failed = True
        self._cancel_deadline(child)
        if self._child is child and not self._stopped and not child.restart_requested:
            self._state = "unavailable"
        self._fail_pending(child, reason)
        child.handshake_done.set()
        self._event(
            reason,
            level="ERROR",
            generation=child.number,
            server_pid=child.process.pid,
            **details,
        )
        if child.is_restart and not child.initialized and not child.restart_requested:
            self._event(
                "restart_failed",
                level="ERROR",
                generation=child.number,
                server_pid=child.process.pid,
                reason=reason,
                **details,
            )
        if child.process.poll() is None:
            threading.Thread(target=self._stop_process, args=(child,), daemon=True).start()

    def _write_child(self, child: _Child, message: dict[str, Any]) -> None:
        if child.process.poll() is not None or child.process.stdin is None:
            raise BrokenPipeError("child_stdin_unavailable")
        child.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        child.process.stdin.flush()

    def _begin_initialize(self, child: _Child, message: dict[str, Any]) -> None:
        child.initialize_request = copy.deepcopy(message)
        child.deadline = time.monotonic() + self._initialization_timeout
        child.timer = threading.Timer(
            self._initialization_timeout, self._initialize_timeout, args=(child,)
        )
        child.timer.daemon = True
        child.timer.start()
        self._write_child(child, message)

    def _initialize_timeout(self, child: _Child) -> None:
        with self.lock:
            if self._child is child and not child.failed and not child.initialized:
                self._mark_failed(child, "initialize_timeout")

    def _mark_ready(self, child: _Child) -> None:
        if self._stopped or self._child is not child or child.failed or child.restart_requested:
            return
        if child.process.poll() is not None:
            self._mark_failed(child, "initialize_child_exited", exit_code=child.process.poll())
            return
        child.initialized = True
        self._state = "ready"
        self._cancel_deadline(child)
        child.handshake_done.set()
        self._event(
            "server_ready",
            generation=child.number,
            server_pid=child.process.pid,
            startup_time_ms=(time.monotonic() - child.started_at) * 1000,
        )
        if child.is_restart:
            self._event(
                "restart_completed",
                generation=child.number,
                new_server_pid=child.process.pid,
                restart_duration_ms=(
                    time.monotonic() - (self._restart_started_at or child.started_at)
                )
                * 1000,
            )

    def _accept_initialize(self, child: _Child, message: dict[str, Any]) -> None:
        request = child.initialize_request
        assert request is not None
        try:
            identifier = _message_id(message)
            expected = _message_id(request)
            if (
                message.get("jsonrpc") != "2.0"
                or type(identifier) is not type(expected)
                or identifier != expected
                or "error" in message
            ):
                raise ValueError("invalid_initialize_response")
            result = InitializeResult.model_validate(message["result"])
            if child.is_restart and result.protocolVersion != self._protocol_version:
                raise ValueError("initialize_protocol_changed")
        except (KeyError, ValueError) as error:
            self._mark_failed(
                child,
                "initialize_response_failed",
                error=str(error),
                response=message,
            )
            return
        child.initialize_response_seen = True
        if child.is_restart:
            self._event(
                "initialize_replayed",
                generation=child.number,
                server_pid=child.process.pid,
                protocol_version=result.protocolVersion,
            )
            try:
                self._write_child(child, {"jsonrpc": "2.0", "method": "notifications/initialized"})
            except (OSError, ValueError) as error:
                self._mark_failed(child, "initialize_notification_failed", error=str(error))
                return
            self._mark_ready(child)
        else:
            self._protocol_version = result.protocolVersion
            child.pending.remove(identifier)
            self._write_client(message)

    def _handle_server_message(self, child: _Child, message: dict[str, Any]) -> None:
        with self.lock:
            if self._child is not child or child.failed or self._stopped:
                return
            if "method" in message:
                self._write_client(message)
                return
            if child.initialize_request is not None and not child.initialize_response_seen:
                self._accept_initialize(child, message)
                return
            try:
                identifier = _message_id(message)
            except (KeyError, ValueError):
                self._event("uncorrelated_response", generation=child.number)
                return
            if identifier in child.pending:
                child.pending.remove(identifier)
                self._write_client(message)
            else:
                self._event("uncorrelated_response", generation=child.number)

    def read_server_output(self, child: _Child) -> None:
        """Consume exactly this generation's stdout, including initialize responses."""
        stream = child.process.stdout
        assert stream is not None
        try:
            for line in stream:
                if not line.strip():
                    continue
                try:
                    message: dict[str, Any] = json.loads(line)
                    if not isinstance(message, dict):
                        raise ValueError("jsonrpc_object_required")
                except ValueError as error:
                    with self.lock:
                        if (
                            child.initialize_request is not None
                            and not child.initialize_response_seen
                        ):
                            self._mark_failed(
                                child,
                                "initialize_stdout_invalid",
                                error=str(error),
                                raw_stdout=line.rstrip("\r\n"),
                            )
                    continue
                self._handle_server_message(child, message)
        except (OSError, ValueError) as error:
            with self.lock:
                self._mark_failed(child, "stdout_read_failed", error=str(error))
        finally:
            stream.close()
            with self.lock:
                self._mark_failed(child, "stdout_closed", exit_code=child.process.poll())

    def read_server_stderr(self, child: _Child) -> None:
        """Drain this generation to EOF, even after its process has exited."""
        stream = child.process.stderr
        assert stream is not None
        try:
            for line in stream:
                raw = line.rstrip("\r\n")
                self._event(
                    "server_stderr",
                    generation=child.number,
                    server_pid=child.process.pid,
                    raw_stderr=raw,
                )
                if raw == RESTART_MARKER:
                    threading.Thread(
                        target=self.trigger_restart,
                        args=(child.number,),
                        daemon=True,
                    ).start()
        except (OSError, ValueError) as error:
            self._event(
                "stderr_read_failed",
                level="ERROR",
                generation=child.number,
                server_pid=child.process.pid,
                error=str(error),
            )
        finally:
            stream.close()

    def _watch_child(self, child: _Child) -> None:
        exit_code = child.process.wait()
        with self.lock:
            self._mark_failed(child, "child_exited", exit_code=exit_code)
        if child.process.stdin is not None:
            with contextlib.suppress(OSError, ValueError):
                child.process.stdin.close()
        # Reader threads own and close stdout/stderr only after draining them to EOF.

    def _spawn_child(self, is_restart: bool) -> None:
        with self.lock:
            if self._stopped:
                return
            self._generation += 1
            generation = self._generation
            self._state = "restarting" if is_restart else "starting"
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        started_at = time.monotonic()
        try:
            process = self._process_factory(env)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            with self.lock:
                if not self._stopped:
                    self._state = "unavailable"
            self._event(
                "server_start_failed", level="ERROR", error=str(error), generation=generation
            )
            if is_restart:
                self._event("restart_failed", level="ERROR", reason="server_start_failed")
            return
        child = _Child(generation, process, is_restart, started_at)
        with self.lock:
            stopped = self._stopped
            if not stopped:
                self._child = child
            threading.Thread(target=self.read_server_output, args=(child,), daemon=True).start()
            threading.Thread(target=self.read_server_stderr, args=(child,), daemon=True).start()
            threading.Thread(target=self._watch_child, args=(child,), daemon=True).start()
            self._event("server_spawned", generation=child.number, server_pid=process.pid)
            if is_restart and not stopped:
                if self.init_request is None:
                    self._mark_failed(child, "initialize_replay_missing")
                else:
                    try:
                        self._begin_initialize(child, self.init_request)
                    except (OSError, ValueError) as error:
                        self._mark_failed(child, "initialize_send_failed", error=str(error))
        if stopped:
            self._stop_process(child)

    def start_server(self, is_restart: bool = False) -> None:
        """Spawn without claiming readiness; replay only through serialized restart."""
        if is_restart:
            self.trigger_restart()
        else:
            with self._lifecycle_lock:
                self._spawn_child(is_restart=False)

    def _forward_client_message(self, message: dict[str, Any]) -> None:
        is_request = "method" in message and "id" in message
        identifier = _message_id(message) if is_request else None
        method = message.get("method")
        with self.lock:
            child = self._child
            can_initialize = (
                child is not None
                and self._state == "starting"
                and method == "initialize"
                and child.initialize_request is None
                and is_request
            )
            can_finish_initialize = (
                child is not None
                and self._state == "starting"
                and method == "notifications/initialized"
                and child.initialize_response_seen
            )
            if (
                child is None
                or child.failed
                or child.process.poll() is not None
                or not (self._state == "ready" or can_initialize or can_finish_initialize)
            ):
                if is_request:
                    self._unavailable(identifier, "forwarding_unavailable", child)
                else:
                    self._event("message_not_forwarded", state=self._state, method=method)
                return
            if is_request:
                if identifier in child.pending:
                    self._event("duplicate_request_id", request_id=identifier)
                    return
                child.pending.add(identifier)
            try:
                if can_initialize:
                    self.init_request = copy.deepcopy(message)
                    self._begin_initialize(child, message)
                else:
                    self._write_child(child, message)
                    if can_finish_initialize:
                        self._mark_ready(child)
            except (OSError, ValueError) as error:
                self._mark_failed(child, "stdin_write_failed", error=str(error))

    def send_to_server(self, message_line: str) -> None:
        """Validate the transport boundary and correlate every accepted request."""
        try:
            message: dict[str, Any] = json.loads(message_line)
            if not isinstance(message, dict):
                raise ValueError("jsonrpc_object_required")
        except ValueError as error:
            self._event("client_json_failed", level="WARNING", error=str(error))
            return
        try:
            json.dumps(message, ensure_ascii=False).encode("utf-8")
        except (UnicodeError, ValueError) as error:
            details = {"error": str(error)}
            self._event("message_encoding_failed", level="WARNING", **details)
            if "method" in message and "id" in message:
                self._write_client(
                    {
                        "jsonrpc": "2.0",
                        "id": message["id"],
                        "error": {
                            "code": -32602,
                            "message": self._event_presenter("message_encoding_failed", details),
                        },
                    }
                )
            return
        try:
            self._forward_client_message(message)
        except ValueError as error:
            self._event("client_id_invalid", level="WARNING", error=str(error))

    def _stop_process(self, child: _Child) -> None:
        """Terminate a child without closing pipes owned by its draining readers."""
        process = child.process
        try:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
        except (OSError, subprocess.SubprocessError) as error:
            self._event(
                "server_stop_failed",
                level="ERROR",
                generation=child.number,
                server_pid=process.pid,
                error=str(error),
            )

    def trigger_restart(self, generation: int | None = None) -> None:
        """Claim one restart per active generation, including an already exited child."""
        with self.lock:
            child = self._child
            if (
                child is None
                or self._stopped
                or child.restart_requested
                or self._state == "restarting"
                or (generation is not None and generation != child.number)
            ):
                return
            child.restart_requested = True
            self._state = "restarting"
            self.restart_count += 1
            self._restart_started_at = time.monotonic()
            self._cancel_deadline(child)
            self._fail_pending(child, "restart_interrupted")
            self._event("restart_initiated", old_server_pid=child.process.pid)
        with self._lifecycle_lock:
            self._stop_process(child)
            self._spawn_child(is_restart=True)
            with self.lock:
                replacement = self._child
            if replacement is None or replacement is child:
                return
            deadline = replacement.deadline
            if deadline is not None and not replacement.handshake_done.wait(
                timeout=max(0, deadline - time.monotonic())
            ):
                self._initialize_timeout(replacement)

    def run(self) -> None:
        """Forward client stdin until shutdown; worker threads own child streams."""
        self._event("proxy_started", proxy_pid=self.proxy_pid)
        self.start_server()
        try:
            for line in sys.stdin:
                if line.strip():
                    self.send_to_server(line)
        except KeyboardInterrupt:
            self._event("proxy_interrupted")
        except OSError as error:
            self._event("proxy_io_failed", level="ERROR", error=str(error))
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Stop the lifecycle without permitting late restart or ready events."""
        with self.lock:
            self._stopped = True
            self._state = "stopped"
            child = self._child
            if child is not None:
                self._cancel_deadline(child)
                self._fail_pending(child, "proxy_stopped")
                child.handshake_done.set()
        if child is not None:
            self._stop_process(child)
        self._event("proxy_stopped")


def main() -> None:
    """Entry point for python -m mcp_server.core.proxy."""
    MCPProxy().run()


if __name__ == "__main__":
    main()
