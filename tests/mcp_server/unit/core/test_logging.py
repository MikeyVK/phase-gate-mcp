"""Tests for structured logging.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.core.logging
"""

from __future__ import annotations

import contextlib
import io
import json
import logging
import sys
from pathlib import Path

import pytest
from pydantic import JsonValue, TypeAdapter

from mcp_server.core.logging import StructuredFormatter, get_logger, setup_logging


def _reset_mcp_server_logger() -> None:
    logger = logging.getLogger("mcp_server")
    for handler in list(logger.handlers):
        with contextlib.suppress(OSError):
            handler.close()
    logger.handlers.clear()


def _flush_mcp_server_logger() -> None:
    logger = logging.getLogger("mcp_server")
    for handler in logger.handlers:
        flush = getattr(handler, "flush", None)
        if callable(flush):
            flush()


def test_structured_formatter() -> None:
    """StructuredFormatter produces valid JSON with props."""
    formatter = StructuredFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.props = {"key": "value"}

    log_output = formatter.format(record)
    data = json.loads(log_output)

    assert data["message"] == "Test message"
    assert data["level"] == "INFO"
    assert data["key"] == "value"


def _reject_nonfinite_constant(token: str) -> None:
    raise ValueError(f"Non-finite JSON constant: {token}")


def _formatted_payload(record: logging.LogRecord) -> dict[str, JsonValue]:
    decoded: object = json.loads(
        StructuredFormatter().format(record), parse_constant=_reject_nonfinite_constant
    )
    return TypeAdapter(dict[str, JsonValue]).validate_python(decoded)


def _payload_record(extra: dict[str, object] | None = None) -> logging.LogRecord:
    return logging.Logger("test.payload").makeRecord(
        "test.payload", logging.ERROR, "", 0, "Primary %s", ("event",), None, extra=extra
    )


def _payload_issues(data: dict[str, JsonValue]) -> list[dict[str, JsonValue]]:
    diagnosis = data["logging_payload"]
    assert isinstance(diagnosis, dict)
    issues = diagnosis["issues"]
    assert isinstance(issues, list) and issues
    checked: list[dict[str, JsonValue]] = []
    for issue in issues:
        assert isinstance(issue, dict)
        assert set(issue) <= {"location", "code", "observed_type", "entry_index"}
        location = issue["location"]
        assert isinstance(location, list)
        assert all(isinstance(part, (str, int)) for part in location)
        assert isinstance(issue["code"], str) and issue["code"]
        assert isinstance(issue["observed_type"], str)
        checked.append(issue)
    return checked


def _assert_primary_metadata(data: dict[str, JsonValue], record: logging.LogRecord) -> None:
    assert data["message"] == "Primary event"
    assert data["level"] == "ERROR"
    assert data["logger"] == "test.payload"
    assert data["timestamp"] == StructuredFormatter().formatTime(record)


def test_payload_absence_and_nullable_values_remain_distinct() -> None:
    """Absent props and explicit null properties are ordinary, lossless events."""
    absent = _payload_record()
    absent_data = _formatted_payload(absent)
    _assert_primary_metadata(absent_data, absent)
    assert "logging_payload" not in absent_data

    props: dict[str, JsonValue] = {
        "nullable": None,
        "nested": {"flag": False, "count": 0, "items": []},
    }
    record = _payload_record({"props": props})
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    assert data["nullable"] is None
    assert data["nested"] == props["nested"]
    assert "logging_payload" not in data


@pytest.mark.parametrize(
    "raw",
    [None, 17, [], [["unsafe", "value"]]],
    ids=["null", "scalar", "empty-list", "update-compatible-list"],
)
def test_payload_malformed_root_keeps_primary_metadata(raw: object) -> None:
    """Raw Logger.extra bypasses the producer helper but still receives admission."""
    record = _payload_record({"props": raw})
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    assert "unsafe" not in data
    assert _payload_issues(data)
    diagnosis = data["logging_payload"]
    assert isinstance(diagnosis, dict)
    assert diagnosis["reserved_fields"] == {}


def _assert_rejected_property(value: object, expected_code: str) -> None:
    record = _payload_record({"props": {"bad": value, "safe": {"flag": False}, "nullable": None}})
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    assert data["safe"] == {"flag": False}
    assert data["nullable"] is None
    assert "bad" not in data
    issues = _payload_issues(data)
    assert any(
        isinstance(issue["location"], list)
        and issue["location"][:1] == ["bad"]
        and issue["code"] == expected_code
        for issue in issues
    )


@pytest.mark.parametrize(
    ("value", "expected_code"),
    [
        ({"nested": [object()]}, "invalid-json-value"),
        ({"nested": float("nan")}, "finite_number"),
        ({"nested": float("inf")}, "finite_number"),
        ({"nested": {7: "not a string key"}}, "string_type"),
    ],
    ids=["nested-object", "nested-nan", "nested-infinity", "nested-nonstring-key"],
)
def test_payload_invalid_property_keeps_valid_siblings(value: object, expected_code: str) -> None:
    """Reject the whole invalid property while retaining other actual JSON facts."""
    _assert_rejected_property(value, expected_code)


def test_payload_cycle_is_diagnosed_without_losing_siblings() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)
    _assert_rejected_property(cyclic, "recursion_loop")


def test_payload_nonstring_root_key_has_safe_diagnosis() -> None:
    record = _payload_record({"props": {7: object(), "safe": "kept"}})
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    assert data["safe"] == "kept"
    assert "7" not in data
    issues = _payload_issues(data)
    assert any(
        issue["location"] == []
        and issue["observed_type"] == "int"
        and issue.get("entry_index") == 0
        for issue in issues
    )


def test_metadata_reserved_values_cannot_replace_primary_event() -> None:
    conflicting: dict[str, JsonValue] = {
        "timestamp": "producer time",
        "level": "DEBUG",
        "logger": "invented.logger",
        "message": "replacement event",
        "exception": "invented traceback",
        "logging_payload": {"supplied": True},
    }
    record = _payload_record({"props": {**conflicting, "safe": "kept"}})
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    assert "exception" not in data
    assert data["safe"] == "kept"
    diagnosis = data["logging_payload"]
    assert isinstance(diagnosis, dict)
    assert diagnosis["reserved_fields"] == conflicting
    issues = _payload_issues(data)
    for key in conflicting:
        assert any(
            issue["location"] == [key] and issue["code"] == "reserved_field" for issue in issues
        )


def test_metadata_invalid_collision_is_diagnosed_without_echoing_value() -> None:
    record = _payload_record({"props": {"message": object(), "safe": "kept"}})
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    assert data["safe"] == "kept"
    diagnosis = data["logging_payload"]
    assert isinstance(diagnosis, dict)
    assert diagnosis["reserved_fields"] == {}
    assert any(
        issue["location"] == ["message"] and issue["code"] == "invalid-json-value"
        for issue in _payload_issues(data)
    )


def test_metadata_real_traceback_survives_malformed_payload() -> None:
    try:
        raise ValueError("primary-cause")
    except ValueError:
        record = logging.Logger("test.payload").makeRecord(
            "test.payload",
            logging.ERROR,
            "",
            0,
            "Primary %s",
            ("event",),
            sys.exc_info(),
            extra={"props": {"bad": object(), "exception": "invented trace", "safe": "kept"}},
        )
    data = _formatted_payload(record)
    _assert_primary_metadata(data, record)
    exception = data["exception"]
    assert isinstance(exception, str)
    assert "Traceback (most recent call last)" in exception
    assert "ValueError: primary-cause" in exception
    assert exception != "invented trace"
    assert data["safe"] == "kept"
    assert "bad" not in data
    issues = _payload_issues(data)
    assert any(issue["location"] == ["bad"] for issue in issues)
    diagnosis = data["logging_payload"]
    assert isinstance(diagnosis, dict)
    assert diagnosis["reserved_fields"] == {"exception": "invented trace"}


def test_get_logger() -> None:
    """get_logger returns logger with correct name prefix."""
    logger = get_logger("test")
    assert logger.name == "mcp_server.test"


def test_setup_logging_writes_audit_log(tmp_path: Path) -> None:
    """setup_logging writes audit log file when parent exists."""
    _reset_mcp_server_logger()

    log_file = tmp_path / "audit.log"

    setup_logging(log_level="INFO", audit_log=str(log_file))

    logger = get_logger("test")
    logger.info("Test audit")
    _flush_mcp_server_logger()

    assert log_file.exists()
    assert "Test audit" in log_file.read_text(encoding="utf-8")


def test_setup_logging_creates_parent_dir(tmp_path: Path) -> None:
    """setup_logging creates missing parent directories for audit log."""
    _reset_mcp_server_logger()

    log_file = tmp_path / "nested" / "audit.log"
    assert not log_file.parent.exists()

    setup_logging(log_level="INFO", audit_log=str(log_file))

    logger = get_logger("test")
    logger.info("Test nested audit")
    _flush_mcp_server_logger()

    assert log_file.exists()
    assert "Test nested audit" in log_file.read_text(encoding="utf-8")


def test_reconfigure_logging_closes_owned_handlers_and_keeps_foreign_handler(
    tmp_path: Path,
) -> None:
    """A new audit destination must not retain old files or duplicate output."""
    _reset_mcp_server_logger()
    root_logger = logging.getLogger("mcp_server")
    foreign_output = io.StringIO()
    foreign_handler = logging.StreamHandler(foreign_output)
    root_logger.addHandler(foreign_handler)
    first_path = tmp_path / "first.jsonl"
    second_path = tmp_path / "second.jsonl"
    audit_logger = get_logger("server_lifecycle")

    try:
        setup_logging(log_level="INFO", audit_log=str(first_path))
        first_handler = next(
            handler for handler in root_logger.handlers if isinstance(handler, logging.FileHandler)
        )
        audit_logger.info("first event")

        setup_logging(log_level="INFO", audit_log=str(first_path))
        audit_logger.info("same destination event")
        assert first_path.read_text(encoding="utf-8").count("same destination event") == 1
        assert first_handler not in root_logger.handlers
        assert first_handler.stream is None

        setup_logging(log_level="INFO", audit_log=str(second_path))
        audit_logger.info("second event")
        assert "second event" not in first_path.read_text(encoding="utf-8")
        assert second_path.read_text(encoding="utf-8").count("second event") == 1

        second_handler = next(
            handler for handler in root_logger.handlers if isinstance(handler, logging.FileHandler)
        )
        setup_logging(log_level="INFO", audit_log=None)
        audit_logger.info("audit disabled event")
        assert "audit disabled event" not in first_path.read_text(encoding="utf-8")
        assert "audit disabled event" not in second_path.read_text(encoding="utf-8")
        assert second_handler not in root_logger.handlers
        assert second_handler.stream is None
        assert foreign_handler in root_logger.handlers
        assert "audit disabled event" in foreign_output.getvalue()
    finally:
        _reset_mcp_server_logger()
        foreign_output.close()
