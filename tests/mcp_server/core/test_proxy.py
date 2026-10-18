"""Exercise public proxy lifecycle with controlled native SDK children."""

import io
import json
import subprocess
import sys
import threading
from collections.abc import Iterator, Mapping
from pathlib import Path
from queue import Queue
from typing import Any

import pytest

from mcp_server.core.proxy import MCPProxy

CHILD = """
import asyncio, os, sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool
async def listing(ctx, params):
    return ListToolsResult(tools=[
        Tool(name=name, input_schema={"type":"object"}) for name in ("echo","hold")
    ])
async def call(ctx, params):
    if params.name == "hold":
        print("hold_started", file=sys.stderr, flush=True)
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            print("hold_cancelled", file=sys.stderr, flush=True)
            raise
    return CallToolResult(content=[TextContent(type="text", text=str(os.getpid()))])
async def main():
    server=Server("proxy-child", on_list_tools=listing, on_call_tool=call)
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())
asyncio.run(main())
"""


class FrameSink(io.StringIO):
    """Collect whole public JSON-RPC frames written by the proxy."""

    def __init__(self) -> None:
        super().__init__()
        self.frames: Queue[dict[str, Any]] = Queue()
        self.observed: list[dict[str, Any]] = []

    def write(self, value: str) -> int:
        for line in value.splitlines():
            if line.startswith("{"):
                frame = json.loads(line)
                self.observed.append(frame)
                self.frames.put(frame)
        return len(value)

    def receive(self, identifier: int) -> dict[str, Any]:
        frame = self.frames.get(timeout=45)
        assert frame["id"] == identifier, frame
        return frame


class ProxyProbe:
    """Own real test processes and observe protocol/events through public seams."""

    def __init__(self, sink: FrameSink, monkeypatch: pytest.MonkeyPatch) -> None:
        self.sink = sink
        self.monkeypatch = monkeypatch
        self.processes: list[subprocess.Popen[str]] = []
        self.events: list[tuple[str, Mapping[str, object]]] = []
        self.condition = threading.Condition()
        self.replacement = "healthy"
        self.proxy = MCPProxy(
            process_factory=self.spawn,
            event_presenter=self.present_event,
        )

    def spawn(self, env: dict[str, str]) -> subprocess.Popen[str]:
        mode = self.replacement if self.processes else "healthy"
        if mode == "spawn_failure":
            raise OSError("replacement launch failed")
        code = "import threading; threading.Event().wait()" if mode == "silent" else CHILD
        process = subprocess.Popen(
            [sys.executable, "-u", "-c", code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            encoding="utf-8",
        )
        self.processes.append(process)
        return process

    def present_event(self, event: str, fields: Mapping[str, object]) -> str:
        with self.condition:
            self.events.append((event, dict(fields)))
            self.condition.notify_all()
        return event

    def wait_event(self, event: str, *, stderr: str | None = None) -> None:
        with self.condition:
            found = self.condition.wait_for(
                lambda: any(
                    name == event and (stderr is None or fields.get("raw_stderr") == stderr)
                    for name, fields in self.events
                ),
                timeout=45,
            )
        assert found, self.events

    def send(self, identifier: int, name: str) -> None:
        self.proxy.send_to_server(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": identifier,
                    "method": "tools/call",
                    "params": {"name": name, "arguments": {}},
                }
            )
        )

    def connect(self) -> None:
        self.monkeypatch.setattr(sys, "stdout", self.sink)
        self.proxy.start_server()
        self.proxy.send_to_server(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-11-25",
                        "capabilities": {},
                        "clientInfo": {"name": "proxy-test", "version": "1"},
                    },
                }
            )
        )
        assert "result" in self.sink.receive(1)
        self.proxy.send_to_server(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                }
            )
        )
        self.wait_event("server_ready")


@pytest.fixture
def probe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[ProxyProbe]:
    monkeypatch.setenv("PGMCP_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.setenv("PGMCP_SERVER_PROJECT_DIR", ".pgmcp")
    sink = FrameSink()
    instance = ProxyProbe(sink, monkeypatch)
    try:
        yield instance
    finally:
        instance.proxy.cleanup()
        for process in instance.processes:
            process.wait(timeout=10)
        assert all(process.poll() is not None for process in instance.processes)


def test_restart_replays_initialize_and_finishes_inflight_once(probe: ProxyProbe) -> None:
    probe.connect()
    probe.send(2, "echo")
    before = probe.sink.receive(2)
    probe.send(3, "hold")
    probe.wait_event("server_stderr", stderr="hold_started")
    probe.proxy.trigger_restart()
    interrupted = probe.sink.receive(3)
    assert interrupted["error"]["data"]["reason"] == "restart_interrupted"
    probe.wait_event("restart_completed")
    probe.send(4, "echo")
    after = probe.sink.receive(4)
    assert before["result"]["content"][0]["text"] != after["result"]["content"][0]["text"]
    assert sum(frame["id"] == 1 for frame in probe.sink.observed) == 1
    assert sum(frame["id"] == 3 for frame in probe.sink.observed) == 1


@pytest.mark.parametrize("replacement", ["spawn_failure", "silent"])
def test_failed_replacement_rejects_calls_and_cleans_children(
    probe: ProxyProbe, replacement: str
) -> None:
    probe.connect()
    probe.replacement = replacement
    probe.proxy.trigger_restart()
    probe.wait_event("restart_failed")
    if replacement == "silent":
        probe.wait_event("initialize_timeout")
    probe.send(2, "echo")
    rejected = probe.sink.receive(2)
    assert rejected["error"]["data"]["code"] == "ERR_SERVER_UNAVAILABLE"
    assert rejected["error"]["data"]["state"] == "unavailable"


def test_cancellation_is_forwarded_and_cleanup_finishes_pending(probe: ProxyProbe) -> None:
    probe.connect()
    probe.send(2, "hold")
    probe.wait_event("server_stderr", stderr="hold_started")
    probe.proxy.send_to_server(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "notifications/cancelled",
                "params": {"requestId": 2, "reason": "test cancellation"},
            }
        )
    )
    probe.wait_event("server_stderr", stderr="hold_cancelled")
    probe.proxy.cleanup()
    cancelled = probe.sink.receive(2)
    assert "error" in cancelled
    assert sum(frame["id"] == 2 for frame in probe.sink.observed) == 1


def test_malformed_frames_do_not_prevent_following_valid_request(probe: ProxyProbe) -> None:
    probe.connect()
    for line in ("not json", "[]"):
        probe.proxy.send_to_server(line)
    for identifier in (True, [], 1.5):
        probe.proxy.send_to_server(
            json.dumps({"jsonrpc": "2.0", "id": identifier, "method": "tools/list"})
        )
    probe.wait_event("client_json_failed")
    probe.wait_event("client_id_invalid")
    probe.proxy.send_to_server(
        json.dumps(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "\ud800"}}
        )
    )
    rejected = probe.sink.receive(2)
    assert rejected["error"]["code"] == -32602
    probe.send(3, "echo")
    assert "result" in probe.sink.receive(3)


@pytest.mark.parametrize("ending", ["eof", "interrupt", "io_error"])
def test_stdin_termination_closes_the_live_child(probe: ProxyProbe, ending: str) -> None:
    def messages() -> Iterator[str]:
        yield "\n"
        yield json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "stdin-test", "version": "1"},
                },
            }
        )
        assert "result" in probe.sink.receive(1)
        yield json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})
        yield json.dumps(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "echo"}}
        )
        assert "result" in probe.sink.receive(2)
        if ending == "interrupt":
            raise KeyboardInterrupt
        if ending == "io_error":
            raise OSError("client input closed")

    probe.monkeypatch.setattr(sys, "stdout", probe.sink)
    probe.monkeypatch.setattr(sys, "stdin", messages())
    probe.proxy.run()
    probe.wait_event("proxy_stopped")
    if ending != "eof":
        probe.wait_event("proxy_interrupted" if ending == "interrupt" else "proxy_io_failed")
    process = probe.proxy.server_process
    assert process is not None and process.poll() is not None
    assert not probe.proxy.restarting
