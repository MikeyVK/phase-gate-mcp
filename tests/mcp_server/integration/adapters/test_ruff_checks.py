"""Real native Ruff and check/v1 comparison on isolated workspace files."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_lint_preserves_native_rejection_and_never_fixes_source(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    target = tmp_path / "unused import.py"
    before = b"import os\n"
    target.write_bytes(before)
    (tmp_path / "pyproject.toml").write_text(
        '[tool.ruff]\nline-length = 100\ntarget-version = "py311"\n'
        '[tool.ruff.lint]\nselect = ["F"]\n',
        encoding="utf-8",
    )
    native = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--no-fix", "--output-format=json", str(target)],
        cwd=tmp_path, capture_output=True, timeout=15,
    )
    assert native.returncode == 1, native.stderr.decode("utf-8", errors="replace")
    assert target.read_bytes() == before
    entrypoint = pytestconfig.rootpath / "mcp_server/bundled_adapters/ruff/check.py"
    adapter = subprocess.run(
        [sys.executable, str(entrypoint)],
        input=json.dumps({
            "operation": "lint", "targets": [str(target)], "args": ["--output-format=json"],
        }).encode("utf-8"),
        cwd=tmp_path, capture_output=True, timeout=15,
    )
    assert adapter.returncode == native.returncode, adapter.stderr.decode("utf-8", errors="replace")
    response = json.loads(adapter.stdout)
    assert response["decision"]["status"] == "failed"
    assert "F401" in json.dumps(response["evidence"])
    assert target.read_bytes() == before


def test_native_ruff_version_and_read_only_controls_override_fix_configuration(
    tmp_path: Path,
) -> None:
    version = subprocess.run(
        [sys.executable, "-m", "ruff", "--version"],
        cwd=tmp_path, capture_output=True, check=True, timeout=15,
    )
    assert version.stdout.decode("utf-8").strip() == "ruff 0.15.6"
    target = tmp_path / "unused.py"
    before = b"import os\n"
    target.write_bytes(before)
    (tmp_path / "pyproject.toml").write_text(
        '[tool.ruff]\nfix = true\nfix-only = true\n'
        '[tool.ruff.lint]\nselect = ["F"]\n',
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--no-fix", "--no-fix-only", str(target)],
        cwd=tmp_path, capture_output=True, timeout=15,
    )
    assert result.returncode == 1, result.stderr.decode("utf-8", errors="replace")
    assert b"F401" in result.stdout
    assert target.read_bytes() == before
