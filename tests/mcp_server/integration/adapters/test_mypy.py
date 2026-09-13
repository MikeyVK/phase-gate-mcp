"""Native Mypy/check-v1 conformance in isolated workspaces."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from shutil import copytree

import pytest

NATIVE_CONFIG = '[tool.mypy]\npython_version = "3.11"\nstrict = true\n'


def test_native_mypy_negative_and_note_baseline(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(NATIVE_CONFIG, encoding="utf-8")
    source = tmp_path / "sample.py"
    source.write_text('value: int = "bad"\nreveal_type(value)\n', encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "mypy", str(source)],
        cwd=tmp_path, capture_output=True, timeout=30,
    )
    assert result.returncode == 1
    assert b"Incompatible types" in result.stdout
    assert b"Revealed type" in result.stdout
    assert b"note:" in result.stdout


def test_adapter_preserves_native_negative_evidence(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    package = tmp_path / "packages" / "mypy"
    copytree(pytestconfig.rootpath / "mcp_server/bundled_adapters/mypy", package)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "pyproject.toml").write_text(NATIVE_CONFIG, encoding="utf-8")
    source = workspace / "sample.py"
    before = b'value: int = "bad"\nreveal_type(value)\n'
    source.write_bytes(before)
    native = subprocess.run(
        [sys.executable, "-m", "mypy", str(source)],
        cwd=workspace, capture_output=True, timeout=30,
    )
    result = subprocess.run(
        [sys.executable, str(package / "check.py")],
        input=json.dumps({"operation": "types", "targets": [str(source)], "args": []}).encode(),
        cwd=workspace, capture_output=True, timeout=30,
    )
    assert result.returncode == native.returncode == 1
    response = json.loads(result.stdout)
    assert response["decision"]["status"] == "failed"
    assert native.stdout.decode() in response["evidence"]["data"]
    assert source.read_bytes() == before
