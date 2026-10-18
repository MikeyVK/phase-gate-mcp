# tests/mcp_server/integration/test_v3_cutover.py
# template=integration_test version=c2e61372 created=2026-09-23T18:46Z updated=
"""Integration proof for the public source and installed V3 entrypoints."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from tests.mcp_server.fixtures.installed_distribution import build_installed_distribution
from tests.mcp_server.fixtures.server_process import run_server_process
from tests.mcp_server.test_support import copy_server_startup_inputs

REPO_ROOT = Path(__file__).resolve().parents[3]
V3_TOOLS = {
    "scaffold_artifact",
    "scaffold_schema",
    "safe_edit_file",
    "run_checks",
    "run_tests",
    "apply_fixes",
}


def _launch_environment(*, workspace: Path, package_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "PGMCP_WORKSPACE_ROOT": str(workspace),
            "PGMCP_SERVER_PROJECT_DIR": ".pgmcp",
            "PYTHONPATH": str(package_root),
            "PGMCP_BYPASS_VERSION_CHECK": "false",
            "PYTHONNOUSERSITE": "1",
            "PYTHONUTF8": "1",
        }
    )
    for key in ("PGMCP_CONFIG_ROOT", "PGMCP_TEMPLATE_ROOT", "PGMCP_CONFIG_PATH"):
        env.pop(key, None)
    return env


def _assert_v3_catalog(workspace: Path, env: dict[str, str]) -> None:
    with run_server_process(
        [sys.executable, "-m", "mcp_server.core.proxy"],
        cwd=workspace,
        env=env,
        timeout=45,
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


class TestV3Cutover:
    """Verify source startup and a freshly built installed distribution."""

    def test_source_stdio_entrypoint_discovers_v3_tools(self, tmp_path: Path) -> None:
        assert (REPO_ROOT / ".pgmcp/installation.json").is_file()
        assert not (REPO_ROOT / ".pgmcp/config/quality.yaml").exists()
        workspace = copy_server_startup_inputs(REPO_ROOT, tmp_path)
        env = _launch_environment(workspace=workspace, package_root=REPO_ROOT)
        _assert_v3_catalog(workspace, env)

    def test_fresh_installed_init_and_startup(self, tmp_path: Path) -> None:
        distribution = build_installed_distribution(REPO_ROOT, tmp_path / "distribution")
        workspace = distribution.workspace
        env = _launch_environment(workspace=workspace, package_root=distribution.root)
        initialized = subprocess.run(
            [sys.executable, "-m", "mcp_server", "--init"],
            cwd=workspace,
            env=env,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
        assert initialized.returncode == 0, initialized.stdout + initialized.stderr
        assert (workspace / ".pgmcp/installation.json").is_file()
        assert not (workspace / ".pgmcp/.version").exists()
        assert not (workspace / ".pgmcp/config/quality.yaml").exists()
        _assert_v3_catalog(workspace, env)
