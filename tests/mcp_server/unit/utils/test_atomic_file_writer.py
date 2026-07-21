# tests/mcp_server/unit/utils/test_atomic_file_writer.py
# template=unit_test version=1.0.0 created=2026-07-21T11:58Z updated=2026-07-21T11:58Z
"""Unit tests for AtomicFileWriter utility."""

import json
from pathlib import Path
from unittest.mock import patch

from mcp_server.core.interfaces.file_writer import IAtomicFileWriter
from mcp_server.utils.atomic_file_writer import AtomicFileWriter


class TestAtomicFileWriter:
    """Test suite verifying AtomicFileWriter execution and retry mechanics."""

    def test_atomic_file_writer_implements_protocol(self) -> None:
        """Verify AtomicFileWriter cleanly implements IAtomicFileWriter."""
        writer = AtomicFileWriter()
        assert isinstance(writer, IAtomicFileWriter)

    def test_write_text_success(self, tmp_path: Path) -> None:
        """Verify write_text atomically creates parent directory and writes content."""
        writer = AtomicFileWriter()
        target_file = tmp_path / "nested" / "dir" / "test.txt"
        writer.write_text(target_file, "Hello, Atomic World!")

        assert target_file.exists()
        assert target_file.read_text(encoding="utf-8") == "Hello, Atomic World!"

    def test_write_json_success(self, tmp_path: Path) -> None:
        """Verify write_json atomically writes formatted JSON payload."""
        writer = AtomicFileWriter()
        target_file = tmp_path / "data.json"
        payload = {"status": "ok", "count": 42}
        writer.write_json(target_file, payload)

        assert target_file.exists()
        data = json.loads(target_file.read_text(encoding="utf-8"))
        assert data == payload

    def test_windows_permission_retry_logic(self, tmp_path: Path) -> None:
        """Verify os.replace retries on transient PermissionError before succeeding."""
        writer = AtomicFileWriter()
        target_file = tmp_path / "retry.txt"

        attempts = 0

        def mock_replace(src: Path, dst: Path) -> None:
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise PermissionError("Access is denied")
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

        with patch("os.replace", side_effect=mock_replace):
            writer.write_text(target_file, "Retry test")

        assert attempts == 3
        assert target_file.read_text(encoding="utf-8") == "Retry test"
