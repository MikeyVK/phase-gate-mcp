"""Global error handling infrastructure for MCP tools.

Provides @tool_error_handler decorator that catches exceptions and converts them
to ToolResult.error() responses with preserved MCPError contract.

Note: this handler intentionally catches only expected/known exception types.
Unexpected exceptions still propagate (so we don't blanket-catch everything).
"""

from __future__ import annotations

import functools
import json
import logging
import traceback
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from mcp_server.core.exceptions import (
    ConfigError,
    ExecutionError,
    MCPError,
    MCPSystemError,
    PreflightError,
    ValidationError,
)
from mcp_server.tools.tool_result import ToolResult

if TYPE_CHECKING:
    from mcp_server.schemas.error_outputs import ConfigErrorOutput, ExecutionErrorOutput

logger = logging.getLogger(__name__)


def capture_exception(
    error: BaseException, *, params: dict[str, Any] | None = None
) -> ConfigErrorOutput | ExecutionErrorOutput:
    """Capture original diagnostic facts without presentation or exception dispatch."""
    from mcp_server.schemas.error_outputs import (  # noqa: PLC0415 -- Avoid eager core/schema imports.
        ConfigErrorOutput,
        ExecutionErrorOutput,
    )

    trace = "".join(traceback.format_exception(error))
    error_code = error.code if isinstance(error, MCPError) else None
    error_params = error.params if isinstance(error, MCPError) else {}
    if isinstance(error, ConfigError):
        return ConfigErrorOutput(
            error_message=error.message,
            file_path=error.file_path,
            traceback=trace,
            error_code=error_code,
            error_params=error_params,
            params=params or {},
        )
    return ExecutionErrorOutput(
        error_message=f"{type(error).__name__}: {error}",
        traceback=trace,
        error_code=error_code,
        error_params=error_params,
        params=params or {},
    )


def tool_error_handler[T](func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """Catch expected tool exceptions and return structured errors."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:  # noqa: ANN401
        try:
            result: T = await func(*args, **kwargs)
        except (
            ValidationError,
            PreflightError,
            ExecutionError,
            MCPSystemError,
            ConfigError,
            MCPError,
            ValueError,
            FileNotFoundError,
        ) as exc:
            message = ""
            error_code: str | None = None
            file_path: str | None = None

            # Preserve MCPError contract
            if isinstance(exc, MCPError):
                message = exc.message
                error_code = exc.code
                # Only ConfigError has file_path attribute
                if isinstance(exc, ConfigError):
                    file_path = exc.file_path

                if isinstance(exc, (ValidationError, PreflightError)):
                    logger.warning("[VALIDATION ERROR] %s: %s", func.__name__, message)
                elif isinstance(exc, ExecutionError):
                    logger.error("[EXECUTION ERROR] %s: %s", func.__name__, message)
                else:
                    logger.exception("[MCP ERROR] %s: %s", func.__name__, message)
            elif isinstance(exc, ValueError):
                message = f"Invalid input: {exc}"
                logger.warning("[USER ERROR] %s: %s", func.__name__, message)
            else:
                # FileNotFoundError
                message = f"Configuration error: {exc}"
                logger.error("[CONFIG ERROR] %s: %s", func.__name__, message)

            # Special handling for ValidationError with schema
            if isinstance(exc, ValidationError) and hasattr(exc, "schema") and exc.schema:
                schema_dict = exc.schema if isinstance(exc.schema, dict) else exc.schema.to_dict()
                schema_text = json.dumps(schema_dict, indent=2)
                # Two text items: error message + schema JSON
                # (inline, readable by agents without extra tool call)
                content: list[dict[str, Any]] = [
                    {"type": "text", "text": message},
                    {"type": "text", "text": schema_text},
                ]
                result = cast(
                    T,
                    ToolResult(
                        content=content,
                        is_error=True,
                        error_code=error_code,
                        file_path=file_path,
                    ),
                )
            else:
                result = cast(
                    T,
                    ToolResult.error(
                        message=message,
                        error_code=error_code,
                        file_path=file_path,
                    ),
                )
        except Exception as exc:  # noqa: BLE001
            message = f"Unexpected error: {type(exc).__name__}: {exc}"
            logger.exception("[BUG] %s: %s", func.__name__, message)
            result = cast(T, ToolResult.error(message))

        return result

    return cast(Callable[..., Awaitable[T]], wrapper)
