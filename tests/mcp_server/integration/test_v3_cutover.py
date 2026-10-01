# tests/mcp_server/integration/test_v3_cutover.py
# template=integration_test version=c2e61372 created=2026-09-23T18:46Z updated=
"""Integration proof for the landed public V3 entrypoint and tool catalog."""

from __future__ import annotations

import os
import subprocess
import tomllib
from pathlib import Path
from typing import TypedDict, cast

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


class LauncherConfig(TypedDict):
    command: str
    args: list[str]
    cwd: str
    env: dict[str, str]


def _launcher() -> tuple[Path, LauncherConfig]:
    launcher = tomllib.loads((REPO_ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
    configured = cast(LauncherConfig, launcher["mcp_servers"]["phase_gate_mcp"])
    python = Path(configured["command"]).resolve()
    assert python.is_file()
    assert configured["args"] == ["-m", "mcp_server.core.proxy"]
    assert Path(configured["cwd"]).resolve() == REPO_ROOT
    assert Path(configured["env"]["PYTHONPATH"]).resolve() == REPO_ROOT
    assert Path(configured["env"]["PGMCP_WORKSPACE_ROOT"]).resolve() == REPO_ROOT
    return python, configured


def _launch_environment(
    python: Path,
    configured: LauncherConfig,
    *,
    workspace: Path,
    package_root: Path,
) -> dict[str, str]:
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
            "PGMCP_WORKSPACE_ROOT": str(workspace),
            "PYTHONPATH": str(package_root),
            "PGMCP_BYPASS_VERSION_CHECK": "false",
            "PYTHONNOUSERSITE": "1",
            "PYTHONUTF8": "1",
        }
    )
    for key in ("PGMCP_CONFIG_ROOT", "PGMCP_TEMPLATE_ROOT", "PGMCP_CONFIG_PATH"):
        env.pop(key, None)
    return env


def _assert_v3_catalog(
    python: Path, configured: LauncherConfig, workspace: Path, env: dict[str, str]
) -> None:
    with run_server_process(
        [str(python), *configured["args"]], cwd=workspace, env=env, timeout=30
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
    """Verify the activated workspace and a fresh installed distribution."""

    def test_configured_stdio_entrypoint_discovers_v3_tools(self, tmp_path: Path) -> None:
        assert (REPO_ROOT / ".pgmcp/installation.json").is_file()
        assert not (REPO_ROOT / ".pgmcp/config/quality.yaml").exists()
        python, configured = _launcher()
        workspace = copy_server_startup_inputs(REPO_ROOT, tmp_path)
        env = _launch_environment(python, configured, workspace=workspace, package_root=REPO_ROOT)
        _assert_v3_catalog(python, configured, workspace, env)

    def test_fresh_installed_init_and_startup(self, tmp_path: Path) -> None:
        python, configured = _launcher()
        distribution_path = tmp_path / "distribution"
        build = subprocess.run(
            [
                str(python),
                "-c",
                "from pathlib import Path; from tests.mcp_server.fixtures.installed_distribution "
                "import build_installed_distribution; import sys; "
                "build_installed_distribution(Path(sys.argv[1]), Path(sys.argv[2]))",
                str(REPO_ROOT),
                str(distribution_path),
            ],
            cwd=REPO_ROOT,
            env=_launch_environment(
                python, configured, workspace=REPO_ROOT, package_root=REPO_ROOT
            ),
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
        assert build.returncode == 0, build.stdout + build.stderr
        workspace = distribution_path / "workspace"
        package_root = distribution_path / "installed"
        env = _launch_environment(
            python,
            configured,
            workspace=workspace,
            package_root=package_root,
        )
        initialized = subprocess.run(
            [str(python), "-m", "mcp_server", "--init"],
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
        _assert_v3_catalog(python, configured, workspace, env)
