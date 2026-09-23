# tests/mcp_server/integration/test_v3_cutover.py
# template=integration_test version=c2e61372 created=2026-09-23T18:46Z updated=
"""Integration proof for the landed public V3 entrypoint and tool catalog."""

from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path

from tests.mcp_server.fixtures.server_process import run_server_process

REPO_ROOT = Path(__file__).resolve().parents[3]
V3_TOOLS = {
    "scaffold_artifact",
    "scaffold_schema",
    "safe_edit_file",
    "run_checks",
    "run_tests",
    "apply_fixes",
}


class TestV3Cutover:
    """Verify the activated workspace through composition and the real launcher."""

    def test_configured_stdio_entrypoint_discovers_v3_tools(self) -> None:
        assert (REPO_ROOT / ".pgmcp/installation.json").is_file()
        assert not (REPO_ROOT / ".pgmcp/config/quality.yaml").exists()
        launcher = tomllib.loads((REPO_ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
        configured = launcher["mcp_servers"]["phase_gate_mcp"]
        python = Path(configured["command"]).resolve()
        assert python == Path(sys.executable).resolve()
        assert configured["args"] == ["-m", "mcp_server.core.proxy"]
        assert Path(configured["cwd"]).resolve() == REPO_ROOT

        env = os.environ.copy()
        prefix = f"{python.parent}{os.pathsep}"
        if (
            env.get("VIRTUAL_ENV") == str(python.parent.parent)
            and env.get("PATH", "")[: len(prefix)].casefold() == prefix.casefold()
        ):
            env["PATH"] = env["PATH"][len(prefix) :]
            env.pop("VIRTUAL_ENV")
        env.update(configured["env"])
        env.update(
            {
                "PGMCP_BYPASS_VERSION_CHECK": "false",
                "PYTHONNOUSERSITE": "1",
                "PYTHONUTF8": "1",
            }
        )
        for key in ("PGMCP_CONFIG_ROOT", "PGMCP_TEMPLATE_ROOT", "PGMCP_CONFIG_PATH"):
            env.pop(key, None)

        with run_server_process(
            [str(python), *configured["args"]], cwd=REPO_ROOT, env=env, timeout=30
        ) as process:
            info = process.initialize(client_name="pytest-v3-cutover")
            assert info["serverInfo"]["name"] == "phase-gate-mcp"
            names = [tool["name"] for tool in process.list_tools()]
            assert len(names) == len(set(names))
            assert set(names) >= V3_TOOLS
            assert not {"run_quality_gates", "auto_fix"} & set(names)
            response = process.send_request(
                "tools/call",
                {"name": "scaffold_schema", "arguments": {"artifact_type": "research"}},
            )
            assert "result" in response
            assert any(
                item.get("type") == "resource" and item["resource"]["uri"].startswith("schema://")
                for item in response["result"]["content"]
            )
