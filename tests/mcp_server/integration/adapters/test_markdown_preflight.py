"""Real-process Markdown preflight preservation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_body_without_h1_keeps_missing_link_as_warning(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    entrypoint = pytestconfig.rootpath / "mcp_server/bundled_adapters/markdown_preflight/check.py"
    target = tmp_path / "proposed.md"
    result = subprocess.run(
        [sys.executable, "-I", "-S", str(entrypoint)],
        input=json.dumps({
            "operation": "body", "target_path": str(target),
            "content": "## Body\n[missing](missing.md)\n", "args": [],
        }).encode("utf-8"),
        cwd=tmp_path, capture_output=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    response = json.loads(result.stdout)
    assert response["decision"] == {"status": "passed"}
    issues = response["evidence"]["data"]["issues"]
    assert len(issues) == 1
    assert issues[0]["severity"] == "warning"
    assert not target.exists()
