# tests/mcp_server/unit/utils/test_atomic_file_writer.py
# template=unit_test version=1.0.0 created=2026-07-21T11:58Z updated=2026-07-21T11:58Z
"""Unit tests for AtomicFileWriter utility."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from mcp_server.core.interfaces.file_writer import (
    FileReplacementError,
    OriginalReadError,
    OriginalTargetMissingError,
    OriginalTargetNotFileError,
)
from mcp_server.utils.atomic_file_writer import (
    AtomicFileWriter,
    CheckedFileWriter,
    OriginalFileReader,
)


class TestAtomicFileWriter:
    """Test suite verifying AtomicFileWriter execution and retry mechanics."""

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


@pytest.mark.parametrize("operation", ["read", "replace"])
@pytest.mark.parametrize("failure_point", ["stat", "read"])
@pytest.mark.parametrize("denied", [False, True], ids=["io_error", "permission_denied"])
def test_original_io_failure_keeps_bytes_and_diagnosis(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
    failure_point: str,
    denied: bool,
) -> None:
    target = tmp_path / "artifact.txt"
    target.write_bytes(b"original\r\n")
    failure = PermissionError("access denied") if denied else OSError("read unavailable")
    stat = Path.lstat
    read = Path.read_bytes

    def stat_with_failure(path: Path) -> os.stat_result:
        if path == target and failure_point == "stat":
            raise failure
        return stat(path)

    def read_with_failure(path: Path) -> bytes:
        if path == target and failure_point == "read":
            raise failure
        return read(path)

    monkeypatch.setattr(Path, "lstat", stat_with_failure)
    monkeypatch.setattr(Path, "read_bytes", read_with_failure)
    with pytest.raises(OriginalReadError) as captured:
        if operation == "read":
            OriginalFileReader().read_snapshot(target)
        else:
            CheckedFileWriter().replace_if_unchanged(target, b"original\r\n", "replacement")
    assert captured.value.reason == ("permission_denied" if denied else "io_error")
    cause: BaseException | None = captured.value
    causes = []
    while cause is not None:
        causes.append(cause)
        cause = cause.__cause__
    assert failure in causes
    assert read(target) == b"original\r\n"
    assert not tuple(tmp_path.glob("*.staging"))


def test_short_staging_write_preserves_original_and_removes_owned_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "artifact.txt"
    target.write_bytes(b"original")
    monkeypatch.setattr(os, "write", lambda _descriptor, _payload: 0)
    with pytest.raises(FileReplacementError) as captured:
        CheckedFileWriter().replace_if_unchanged(target, b"original", "replacement")
    assert captured.value.reason == "io_error"
    assert isinstance(captured.value.__cause__, OSError)
    assert target.read_bytes() == b"original"
    assert not tuple(tmp_path.glob("*.staging"))


@pytest.mark.parametrize("operation", ["read", "replace"])
@pytest.mark.parametrize(
    ("failure_type", "diagnosis"),
    [
        (FileNotFoundError, OriginalTargetMissingError),
        (IsADirectoryError, OriginalTargetNotFileError),
    ],
)
def test_read_race_exposes_the_correct_failure_without_overwriting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
    failure_type: type[OSError],
    diagnosis: type[Exception],
) -> None:
    target = tmp_path / "artifact.txt"
    target.write_bytes(b"original")
    read = Path.read_bytes
    failure = failure_type("changed after metadata inspection")

    def read_with_failure(path: Path) -> bytes:
        if path == target:
            raise failure
        return read(path)

    monkeypatch.setattr(Path, "read_bytes", read_with_failure)
    with pytest.raises(diagnosis) as captured:
        if operation == "read":
            OriginalFileReader().read_snapshot(target)
        else:
            CheckedFileWriter().replace_if_unchanged(target, b"original", "replacement")
    cause: BaseException | None = captured.value
    while cause is not None and cause is not failure:
        cause = cause.__cause__
    assert cause is failure
    assert read(target) == b"original"
    assert not tuple(tmp_path.glob("*.staging"))


@pytest.mark.parametrize("failure_type", [PermissionError, OSError])
def test_replacement_failure_preserves_original_and_removes_staging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure_type: type[OSError]
) -> None:
    target = tmp_path / "artifact.txt"
    target.write_bytes(b"original")
    failure = failure_type("replacement unavailable")

    def replace_with_failure(_source: Path, _target: Path) -> None:
        raise failure

    monkeypatch.setattr(os, "replace", replace_with_failure)
    with pytest.raises(FileReplacementError) as captured:
        CheckedFileWriter().replace_if_unchanged(target, b"original", "replacement")
    assert captured.value.__cause__ is failure
    assert target.read_bytes() == b"original"
    assert not tuple(tmp_path.glob("*.staging"))
