"""Real-process Python syntax adapter conformance, isolated from server dependencies."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_complete_content_is_parsed_without_import_or_execution(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    entrypoint = (
        pytestconfig.rootpath / "mcp_server/bundled_adapters/python_syntax/check.py"
    )
    target = tmp_path / "absent parent" / "proposed.py"
    marker = tmp_path / "executed.txt"
    content = (
        "import nonexistent_syntax_fixture_dependency\n"
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('must not execute')\n"
        "return 1\n"
    )
    result = subprocess.run(
        [sys.executable, "-I", "-S", str(entrypoint)],
        input=json.dumps({
            "operation": "syntax", "target_path": str(target), "content": content, "args": [],
        }).encode("utf-8"),
        cwd=tmp_path, capture_output=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    response = json.loads(result.stdout)
    assert response["decision"] == {"status": "passed"}
    assert not target.exists()
    assert not marker.exists()
