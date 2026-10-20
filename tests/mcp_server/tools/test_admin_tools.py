"""Tests for administrative tools (server restart functionality).

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.tools.admin_tools
"""

import asyncio
import json
import logging
import os
import time
from collections.abc import Coroutine
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import JsonValue, TypeAdapter
from pytest import MonkeyPatch

from mcp_server.core.logging import StructuredFormatter
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.admin_tools import (
    RestartServerInput,
    RestartServerTool,
    verify_server_restarted,
)


@pytest.mark.asyncio
async def test_restart_returns_before_exit_and_records_marker_and_audit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Own the delayed task and observe the response, marker, audit and exit protocol."""
    tasks: list[asyncio.Task[None]] = []
    exit_calls: list[int] = []
    create_task = asyncio.create_task

    def schedule(coroutine: Coroutine[object, object, None]) -> asyncio.Task[None]:
        task = create_task(coroutine)
        tasks.append(task)
        return task

    monkeypatch.setattr("mcp_server.tools.admin_tools.asyncio.create_task", schedule)
    monkeypatch.setattr("mcp_server.tools.admin_tools.sys.exit", exit_calls.append)
    tool = RestartServerTool(server_root=tmp_path)
    reason = "Test restart execution"

    with caplog.at_level(logging.INFO, logger="mcp_server.tools.admin"):
        try:
            result = await tool.execute(RestartServerInput(reason=reason), NoteContext())
            assert result.success
            assert result.reason == reason
            assert result.pid == os.getpid()
            assert len(tasks) == 1
            assert not exit_calls
            marker = TypeAdapter(dict[str, JsonValue]).validate_json(
                (tmp_path / ".restart_marker").read_text(encoding="utf-8")
            )
            assert marker == {
                "timestamp": result.timestamp,
                "pid": result.pid,
                "reason": reason,
                "iso_time": result.iso_time,
            }
            assert isinstance(marker["timestamp"], float)
            assert marker["timestamp"] > 0
            marker_iso_time = marker["iso_time"]
            assert isinstance(marker_iso_time, str)
            assert datetime.fromisoformat(marker_iso_time).tzinfo is not None
        finally:
            await asyncio.gather(*tasks)

    assert exit_calls == [42]
    assert capsys.readouterr().err.splitlines() == ["__MCP_RESTART_REQUEST__"]
    records = [record for record in caplog.records if record.name == "mcp_server.tools.admin"]
    formatter = StructuredFormatter()
    payloads = [
        TypeAdapter(dict[str, JsonValue]).validate_json(formatter.format(record))
        for record in records
    ]
    assert [payload["event_type"] for payload in payloads] == [
        "server_restart_requested",
        "restart_marker_written",
        "server_exiting_for_restart",
    ]
    for record, payload in zip(records, payloads, strict=True):
        props = TypeAdapter(dict[str, JsonValue]).validate_python(record.__dict__["props"])
        event_timestamp = payload["event_timestamp"]
        assert isinstance(event_timestamp, str)
        assert datetime.fromisoformat(event_timestamp).tzinfo is not None
        assert event_timestamp == props["event_timestamp"]
        assert payload["timestamp"] == formatter.formatTime(record)
        assert payload["reason"] == reason
        assert payload["pid"] == result.pid
        assert "logging_payload" not in payload
    assert payloads[1]["marker_content"] == marker
    assert payloads[1]["marker_path"] == str(tmp_path / ".restart_marker")
    assert payloads[2]["exit_code"] == 42


def test_verify_server_restarted_with_valid_marker(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """RED: Test verify_server_restarted with valid marker.

    Verifies:
    - Returns restarted=True when marker timestamp > since_timestamp
    - Returns restart details (timestamp, PID, reason)
    - Returns current vs previous PID
    """
    marker_path = tmp_path / ".restart_marker"

    past_time = time.time() - 10
    marker_data = {
        "timestamp": past_time + 5,
        "pid": 99999,
        "reason": "Test restart verification",
        "iso_time": datetime.now(UTC).isoformat(),
    }
    marker_path.write_text(json.dumps(marker_data), encoding="utf-8")

    with caplog.at_level(logging.INFO, logger="mcp_server.tools.admin"):
        result = verify_server_restarted(since_timestamp=past_time, server_root=tmp_path)

    assert result["restarted"] is True
    assert result["previous_pid"] == 99999
    assert result["reason"] == "Test restart verification"
    assert result["restart_timestamp"] == past_time + 5
    assert "current_pid" in result
    assert "time_since_restart" in result
    records = [record for record in caplog.records if record.name == "mcp_server.tools.admin"]
    assert len(records) == 1
    payload = TypeAdapter(dict[str, JsonValue]).validate_json(
        StructuredFormatter().format(records[0])
    )
    assert payload["message"] == "Server restart verification"
    assert payload["result"] == result
    assert payload["since_timestamp"] == past_time
    assert "logging_payload" not in payload


def test_verify_server_restarted_no_marker(
    tmp_path: Path,
) -> None:
    """RED: Test verify_server_restarted with missing marker.

    Verifies:
    - Returns restarted=False when marker doesn't exist
    - Returns error message
    """
    result = verify_server_restarted(since_timestamp=time.time(), server_root=tmp_path)

    assert result["restarted"] is False
    assert "error" in result
    assert "not found" in result["error"].lower()


def test_verify_server_restarted_old_marker(
    tmp_path: Path,
) -> None:
    """RED: Test verify_server_restarted with outdated marker.

    Verifies:
    - Returns restarted=False when marker timestamp < since_timestamp
    """
    marker_path = tmp_path / ".restart_marker"

    old_time = time.time() - 100
    marker_data = {
        "timestamp": old_time,
        "pid": 99999,
        "reason": "Old restart",
        "iso_time": datetime.now(UTC).isoformat(),
    }
    marker_path.write_text(json.dumps(marker_data), encoding="utf-8")

    recent_time = time.time() - 10
    result = verify_server_restarted(since_timestamp=recent_time, server_root=tmp_path)

    assert result["restarted"] is False
