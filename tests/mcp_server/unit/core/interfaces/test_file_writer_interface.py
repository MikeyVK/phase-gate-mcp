# tests/mcp_server/unit/core/interfaces/test_file_writer_interface.py
# template=unit_test version=1.0.0 created=2026-07-21T11:58Z updated=2026-07-21T11:58Z
"""Unit tests for IAtomicFileWriter protocol interface."""

from pathlib import Path
from typing import Any

from mcp_server.core.interfaces.file_writer import IAtomicFileWriter


class DummyFileWriter:
    """Dummy class implementing IAtomicFileWriter methods for runtime check testing."""

    def write_text(self, path: Path, content: str, *, temp_name: str = ".tmp") -> None:
        pass

    def write_json(self, path: Path, payload: dict[str, Any], *, temp_name: str = ".tmp") -> None:
        pass


class TestIAtomicFileWriterProtocol:
    """Test suite verifying IAtomicFileWriter protocol contract."""

    def test_iatomic_file_writer_runtime_checkable(self) -> None:
        """Verify @runtime_checkable allows isinstance checks against valid implementation."""
        dummy = DummyFileWriter()
        assert isinstance(dummy, IAtomicFileWriter)

    def test_invalid_class_fails_runtime_check(self) -> None:
        """Verify object missing protocol methods fails isinstance check."""
        assert not isinstance("not_a_writer", IAtomicFileWriter)
