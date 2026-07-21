# mcp_server/core/interfaces/file_writer.py
# template=interface version=f35abd82 created=2026-07-21T11:59Z updated=2026-07-21T11:59Z
"""Protocol interface for atomic file writing."""

from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IAtomicFileWriter(Protocol):
    """Protocol interface for atomic file operations across all file types."""

    def write_text(self, path: Path, content: str, *, temp_name: str = ".tmp") -> None:
        """Atomically write text content to path via temp file replacement."""
        ...

    def write_json(self, path: Path, payload: dict[str, Any], *, temp_name: str = ".tmp") -> None:
        """Atomically write JSON payload to path via temp file replacement."""
        ...
