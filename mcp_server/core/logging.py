"""Structured logging for the MCP server."""

import json
import logging
import sys
from collections.abc import Mapping
from functools import cached_property
from pathlib import Path
from typing import TextIO, TypedDict, TypeGuard

from pydantic import ConfigDict, JsonValue, TypeAdapter, ValidationError


class LoggingExtra(TypedDict):
    """Static producer contract; the formatter still admits each actual payload."""

    props: Mapping[str, JsonValue]


def logging_extra(props: Mapping[str, JsonValue]) -> LoggingExtra:
    """Carry known producer data through the standard logging extra argument."""
    return {"props": props}


def _is_payload_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    """Describe the actual container without claiming valid keys or JSON values."""
    return isinstance(value, Mapping)


class StructuredFormatter(logging.Formatter):
    """JSON formatter preserving the primary event when extra data is malformed."""

    @cached_property
    def _json_value(self) -> TypeAdapter[JsonValue]:
        return TypeAdapter(JsonValue, config=ConfigDict(strict=True, allow_inf_nan=False))

    def format(self, record: logging.LogRecord) -> str:
        """Keep valid properties and diagnose unsafe data without echoing it."""
        log_data: dict[str, JsonValue] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        issues: list[JsonValue] = []
        reserved_fields: dict[str, JsonValue] = {}
        reserved = {"timestamp", "level", "logger", "message", "exception", "logging_payload"}
        if "props" in record.__dict__:
            raw: object = record.__dict__["props"]
            if not _is_payload_mapping(raw):
                issues.append(
                    {"location": [], "code": "mapping_type", "observed_type": type(raw).__name__}
                )
            else:
                for index, (key, value) in enumerate(raw.items()):
                    if not isinstance(key, str):
                        issues.append(
                            {
                                "location": [],
                                "code": "string_type",
                                "observed_type": type(key).__name__,
                                "entry_index": index,
                            }
                        )
                        continue
                    try:
                        admitted = self._json_value.validate_python(value)
                    except ValidationError as error:
                        for detail in error.errors(
                            include_input=False, include_context=False, include_url=False
                        ):
                            location: list[JsonValue] = [key, *detail["loc"]]
                            issues.append(
                                {
                                    "location": location,
                                    "code": detail["type"],
                                    "observed_type": type(value).__name__,
                                }
                            )
                        continue
                    if key in reserved:
                        reserved_fields[key] = admitted
                        issues.append(
                            {
                                "location": [key],
                                "code": "reserved_field",
                                "observed_type": type(value).__name__,
                            }
                        )
                    else:
                        log_data[key] = admitted
        if issues:
            log_data["logging_payload"] = {
                "issues": issues,
                "reserved_fields": reserved_fields,
            }
        return json.dumps(log_data)


class _OwnedStreamHandler(logging.StreamHandler[TextIO]):
    """Mark the console handler installed by this logging facility."""


class _OwnedFileHandler(logging.FileHandler):
    """Mark the audit handler installed by this logging facility."""


def setup_logging(log_level: str = "INFO", audit_log: str | None = None) -> None:
    """Configure logging.

    Args:
        log_level: Log level string (DEBUG, INFO, WARNING, ERROR). Defaults to "INFO".
        audit_log: Path to audit log file. When None, no file handler is added.
    """
    logger = logging.getLogger("mcp_server")
    logger.setLevel(log_level)

    # Reconfiguration replaces only handlers installed by this facility. Keep
    # handlers supplied by the host or test harness attached to the logger.
    for existing_handler in tuple(logger.handlers):
        if isinstance(existing_handler, (_OwnedStreamHandler, _OwnedFileHandler)):
            logger.removeHandler(existing_handler)
            existing_handler.close()

    # Console handler
    handler = _OwnedStreamHandler(sys.stderr)
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)

    # Audit log file handler if configured
    if audit_log:
        log_path = Path(audit_log)
        try:
            # Ensure the parent directory exists (common failure on fresh checkouts)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = _OwnedFileHandler(str(log_path))
            file_handler.setFormatter(StructuredFormatter())
            logger.addHandler(file_handler)
        except OSError as exc:
            # Fallback if file cannot be opened; still keep stderr logging.
            logger.warning(
                "Failed to configure audit log file: %s",
                exc,
                exc_info=True,
                extra=logging_extra({"audit_log": str(log_path)}),
            )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(f"mcp_server.{name}")
