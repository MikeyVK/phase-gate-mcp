# c:\temp\pgmcp\mcp_server\core\interfaces\itool_response_cache.py
# template=interface version=3fb28c28 created=2026-06-19T22:20Z updated=
"""itool_response_cache module.

CQRS cache interfaces.

@layer: Backend (Contracts)
"""

# Standard library
from typing import Protocol, Type, TypeVar, runtime_checkable

# Third-party
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@runtime_checkable
class IToolResponsePublisher(Protocol):
    """Write-only interface for publishing tool execution results to the cache."""

    def put(self, tool_name: str, output: BaseModel) -> str | None:
        """Publish the output DTO to the cache and return a unique run_id.

        If a cache write fails, the implementation must trap the exception,
        log a warning/error, and return None. It must never crash the tool
        execution pipeline.
        """
        ...


@runtime_checkable
class IToolResponseReader(Protocol):
    """Read-only interface for retrieving cached tool execution results."""

    def get(self, run_id: str, response_model: Type[T]) -> T | None:
        """Retrieve and deserialize a cached DTO using the expected type-safe model."""
        ...

    def exists(self, run_id: str) -> bool:
        """Check if a cached result exists for the run_id."""
        ...
