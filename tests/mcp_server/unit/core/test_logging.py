"""Tests for structured logging.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.core.logging
"""

from __future__ import annotations

import contextlib
import io
import json
import logging
from pathlib import Path

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
