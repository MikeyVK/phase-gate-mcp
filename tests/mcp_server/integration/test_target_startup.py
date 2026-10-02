# tests/mcp_server/integration/test_target_startup.py
# template=integration_test version=c2e61372 created=2026-09-17T16:47Z updated=2026-09-17
"""Integration tests for target_startup_composition_and_launch_rehearsal.

Integration rehearsal testing target runtime composition, server process handshake,
startup lock exclusion, and configuration verification.

@layer: Tests (Integration)
@dependencies: [pytest, mcp_server.bootstrap, tests.mcp_server.fixtures.server_process]
@responsibilities:
    - Test end-to-end target_startup_composition_and_launch_rehearsal
    - Verify current normal startup uses target V3 tools
    - Verify target tool assembly has 6 target V3 tools and no duplicate names
    - Verify presentation alignment for target tools
    - Verify DI-06 startup lock blocks concurrent target startup
    - Verify unresolved recovery refusal halts startup without mutating disk
    - Rehearse real stdio ServerProcess handshake and tool discovery
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from git import Repo as GitRepo

from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.exceptions import MCPError
from mcp_server.services.template_activation import UpgradeLock
from scripts.build_package import read_manifest
from tests.mcp_server.fixtures.installed_distribution import (
    InstalledDistribution,
    build_installed_distribution,
)
from tests.mcp_server.fixtures.server_process import run_server_process
from tests.mcp_server.test_support import (
    copy_server_startup_inputs,
    make_project_manager,
)

REPO_ROOT = Path(__file__).resolve().parents[3]

TARGET_V3_TOOL_NAMES = frozenset(
    {
        "scaffold_artifact",
        "scaffold_schema",
        "safe_edit_file",
        "run_checks",
        "run_tests",
        "apply_fixes",
    }
)

LEGACY_V2_TOOL_NAMES = frozenset(
    {
        "run_quality_gates",
        "auto_fix",
    }
)


@pytest.fixture
def isolated_target_env(tmp_path: Path) -> tuple[Path, Path]:
    """Create isolated roots with the active V3 configuration."""
    server_root = tmp_path / "server_root"
    server_root.mkdir(parents=True, exist_ok=True)

    config_root = tmp_path / "config_root"
    config_root.mkdir(parents=True, exist_ok=True)

    # Copy existing YAML configs from live repository
    live_config = REPO_ROOT / ".pgmcp" / "config"
    for yaml_file in live_config.glob("*.yaml"):
        shutil.copy2(yaml_file, config_root / yaml_file.name)

    return config_root, server_root


def _build_test_settings(config_root: Path, server_root: Path) -> Settings:
    """Build settings pointing to isolated config and server roots."""
    return Settings(
        server=ServerSettings(
            workspace_root=str(server_root.parent),
            config_root=str(config_root),
            template_root=str(REPO_ROOT / ".pgmcp" / "template_suite"),
            server_root_dir=server_root.name,
        )
    )


def _installed_candidate(tmp_path: Path) -> InstalledDistribution:
    """Build and install the current V3 source with the configured launcher."""
    candidate = tmp_path / "candidate_source"
    candidate.mkdir()
    shutil.copy2(REPO_ROOT / "pyproject.toml", candidate / "pyproject.toml")
    shutil.copytree(
        REPO_ROOT / "mcp_server",
        candidate / "mcp_server",
        ignore=shutil.ignore_patterns("assets", "__pycache__", "*.pyc"),
    )
    manifest = read_manifest(REPO_ROOT / ".pgmcp/config/release_manifest.yaml")
    for mapping in manifest["assets"]:
        source = REPO_ROOT / mapping["source"]
        destination = candidate / mapping["source"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    launcher_python, _ = _active_launcher_runtime()
    distribution = build_installed_distribution(
        candidate, tmp_path / "distribution", python_executable=launcher_python
    )
    host_sources = (
        "docs/agents/vscode/copilot/AGENTS.md",
        "docs/agents/codex/AGENTS.md",
        "docs/agents/antigravity/AGENTS.md",
        "docs/agents/vscode/copilot/.github/agents/qa.agent.md",
        "docs/agents/vscode/copilot/.github/agents/co.agent.md",
        "docs/agents/codex/rules/research.agent.md",
    )
    for relative in host_sources:
        mapped = relative.removeprefix("docs/agents/")
        packaged = distribution.root / "mcp_server/assets/agents" / mapped
        assert packaged.is_file(), f"packaged_host_asset_missing:{mapped}"
        assert packaged.read_bytes() == (candidate / relative).read_bytes(), (
            f"packaged_host_asset_mismatch:{mapped}"
        )
    return distribution


def _active_launcher_runtime() -> tuple[Path, str]:
    """Read the configured Codex launcher for an actual subprocess probe."""
    launcher = tomllib.loads((REPO_ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
    configured = launcher["mcp_servers"]["phase_gate_mcp"]
    launcher_python = Path(configured["command"])
    assert launcher_python.is_absolute() and launcher_python.is_file()
    assert configured["args"] == ["-m", "mcp_server.core.proxy"]
    assert Path(configured["cwd"]).resolve() == REPO_ROOT.resolve()
    assert Path(configured["env"]["PYTHONPATH"]).resolve() == REPO_ROOT.resolve()
    assert Path(configured["env"]["PGMCP_WORKSPACE_ROOT"]).resolve() == REPO_ROOT.resolve()
    assert configured["env"]["PGMCP_SERVER_PROJECT_DIR"] == ".pgmcp"
    assert "VIRTUAL_ENV" not in configured["env"]
    assert "PATH" not in configured["env"]

    # The launcher does not override PATH; verify the subprocess sees this value.
    return launcher_python, os.environ["PATH"]


def _installed_environment(distribution: InstalledDistribution, workspace: Path) -> dict[str, str]:
    launcher_python, launcher_path = _active_launcher_runtime()
    assert launcher_python.is_file()
    env = os.environ.copy()
    env["PATH"] = launcher_path
    env.pop("VIRTUAL_ENV", None)
    env.update(
        {
            "PYTHONPATH": str(distribution.root),
            "PGMCP_WORKSPACE_ROOT": str(workspace),
            "PGMCP_SERVER_PROJECT_DIR": ".pgmcp",
            "PGMCP_BYPASS_VERSION_CHECK": "false",
            "PYTHONNOUSERSITE": "1",
            "PYTHONUTF8": "1",
        }
    )
    for key in ("PGMCP_CONFIG_ROOT", "PGMCP_TEMPLATE_ROOT", "PGMCP_CONFIG_PATH"):
        env.pop(key, None)
    return env


def _assert_candidate_launch_parity(python: Path, workspace: Path, env: dict[str, str]) -> None:
    """Observe the subprocess values that govern startup and adapter lookup."""
    probe = subprocess.run(
        [
            str(python),
            "-c",
            "import json, os, shutil, sys; "
            "print(json.dumps({'python': sys.executable, 'cwd': os.getcwd(), "
            "'path': os.environ['PATH'], 'virtual_env': os.environ.get('VIRTUAL_ENV'), "
            "'python_adapter': shutil.which('python'), 'node_adapter': shutil.which('node'), "
            "'pythonpath': os.environ.get('PYTHONPATH'), "
            "'workspace': os.environ.get('PGMCP_WORKSPACE_ROOT'), "
            "'project_dir': os.environ.get('PGMCP_SERVER_PROJECT_DIR')}))",
        ],
        cwd=workspace,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert probe.returncode == 0, probe.stdout + probe.stderr
    observed = json.loads(probe.stdout)
    _, launcher_path = _active_launcher_runtime()
    assert Path(observed["python"]).resolve() == python.resolve()
    assert Path(observed["cwd"]).resolve() == workspace.resolve()
    assert observed["path"] == launcher_path
    assert observed["virtual_env"] == env.get("VIRTUAL_ENV")
    assert observed["python_adapter"] == shutil.which("python", path=launcher_path)
    assert observed["node_adapter"] == shutil.which("node", path=launcher_path)
    assert observed["pythonpath"] == env["PYTHONPATH"]
    assert observed["workspace"] == str(workspace)
    assert observed["project_dir"] == ".pgmcp"


class TestTargetStartup:
    """Integration test suite for target_startup_composition_and_launch_rehearsal."""

    def test_target_tool_assembly_composition_and_no_duplicate_names(
        self, isolated_target_env: tuple[Path, Path]
    ) -> None:
        """Verify target assembly has the 6 target V3 tools and no duplicate names."""
        config_root, server_root = isolated_target_env
        settings = _build_test_settings(config_root, server_root)
        bootstrapper = ServerBootstrapper(settings)
        server = bootstrapper.bootstrap_target()

        tool_names = [tool.name for tool in server.tools]
        unique_names = set(tool_names)

        # No duplicate names allowed in assembly
        assert len(tool_names) == len(unique_names), "Duplicate tool names found in target assembly"

        # All 6 target V3 tools must be present
        for target_tool in TARGET_V3_TOOL_NAMES:
            assert target_tool in unique_names, f"Expected target tool {target_tool} in assembly"

        # Legacy V2 tools must NOT be present in target assembly
        for legacy_tool in LEGACY_V2_TOOL_NAMES:
            assert legacy_tool not in unique_names, (
                f"Legacy tool {legacy_tool} must not be in target assembly"
            )

        # Key unchanged tools must be present
        unchanged_expected = {
            "create_branch",
            "git_status",
            "git_diff_stat",
            "get_work_context",
            "health_check",
            "restart_server",
            "initialize_project",
            "get_project_plan",
            "create_issue",
            "get_issue",
        }
        for tool_name in unchanged_expected:
            assert tool_name in unique_names, (
                f"Expected unchanged tool {tool_name} in target assembly"
            )

    def test_target_presentation_alignment(self, isolated_target_env: tuple[Path, Path]) -> None:
        """Verify target tools validate presentation alignment cleanly."""
        config_root, server_root = isolated_target_env
        settings = _build_test_settings(config_root, server_root)
        bootstrapper = ServerBootstrapper(settings)
        server = bootstrapper.bootstrap_target()
        assert server.presenter is not None

    def test_target_startup_lock_exclusion(self, isolated_target_env: tuple[Path, Path]) -> None:
        """Verify DI-06 startup lock blocks concurrent target startup."""
        config_root, server_root = isolated_target_env
        lock_path = server_root / "template_upgrade.lock"

        settings = _build_test_settings(config_root, server_root)
        bootstrapper = ServerBootstrapper(settings)

        # Acquire lock externally
        external_lock = UpgradeLock(lock_path)
        with external_lock.hold():
            with pytest.raises(MCPError) as exc_info:
                bootstrapper.bootstrap_target()
            assert "template_upgrade_locked" in str(exc_info.value)
            assert exc_info.value.code == "ERR_CONFIG"

    def test_target_startup_unresolved_recovery_refusal(
        self, isolated_target_env: tuple[Path, Path]
    ) -> None:
        """Verify active recovery record halts startup without disk mutation."""
        config_root, server_root = isolated_target_env
        recovery_path = server_root / "template_upgrade.json"
        recovery_content = '{"prior_suite": {"present": false}, "target_suite": {"present": true}}'
        recovery_path.write_text(recovery_content, encoding="utf-8")
        before_stat = recovery_path.stat()

        settings = _build_test_settings(config_root, server_root)
        bootstrapper = ServerBootstrapper(settings)

        with pytest.raises(MCPError) as exc_info:
            bootstrapper.bootstrap_target()
        assert "template_recovery_unknown" in str(exc_info.value)
        assert exc_info.value.code == "ERR_CONFIG"

        # Verify disk was NOT mutated
        assert recovery_path.exists()
        assert recovery_path.read_text(encoding="utf-8") == recovery_content
        after_stat = recovery_path.stat()
        assert before_stat.st_mtime == after_stat.st_mtime

    def test_real_server_process_handshake_default_target(self, tmp_path: Path) -> None:
        """Verify real subprocess handshake on normal startup publishes target tools."""
        workspace = copy_server_startup_inputs(REPO_ROOT, tmp_path)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT)
        env["PGMCP_WORKSPACE_ROOT"] = str(workspace)
        env["PGMCP_SERVER_PROJECT_DIR"] = ".pgmcp"
        for key in ("PGMCP_CONFIG_ROOT", "PGMCP_TEMPLATE_ROOT", "PGMCP_CONFIG_PATH"):
            env.pop(key, None)
        with run_server_process(
            [sys.executable, "-m", "mcp_server.core.proxy"],
            cwd=workspace,
            env=env,
        ) as proc:
            info = proc.initialize(client_name="pytest-target", client_version="1.0.0")
            assert "serverInfo" in info
            assert info["serverInfo"]["name"] == "phase-gate-mcp"

            tools = proc.list_tools()
            tool_names = {t["name"] for t in tools}
            assert tool_names >= TARGET_V3_TOOL_NAMES
            assert not LEGACY_V2_TOOL_NAMES & tool_names

    def test_installed_candidate_init_migration_and_mcp_handshake(self, tmp_path: Path) -> None:
        """Rehearse one installed V3 candidate across fresh and owner-migrated roots."""
        try:
            distribution = _installed_candidate(tmp_path)
        except Exception as exc:
            pytest.fail(f"candidate_build_rehearsal_failed:{exc!r}")
        assert distribution.root.resolve().is_relative_to(tmp_path.resolve())
        assert not distribution.root.resolve().is_relative_to(REPO_ROOT.resolve())
        launcher_python, _ = _active_launcher_runtime()
        launch = [str(launcher_python), "-m", "mcp_server.core.proxy"]

        fresh = distribution.workspace
        fresh_env = _installed_environment(distribution, fresh)
        _assert_candidate_launch_parity(launcher_python, fresh, fresh_env)
        initialized = subprocess.run(
            [str(launcher_python), "-m", "mcp_server", "--init"],
            cwd=fresh,
            env=fresh_env,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
        assert initialized.returncode == 0, initialized.stdout + initialized.stderr
        assert (fresh / ".pgmcp/installation.json").is_file()
        assert not (fresh / ".pgmcp/.version").exists()
        repo = GitRepo.init(str(fresh))
        marker = fresh / "README.md"
        marker.write_text("Candidate workspace\n", encoding="utf-8")
        repo.index.add([str(marker)])
        repo.index.commit("Initialize candidate workspace")
        manager = make_project_manager(fresh)
        manager.initialize_project(53, "Candidate planning readback", "feature")
        expected_plan = {
            "cycles": {
                "total": 117,
                "cycles": [
                    {
                        "cycle_number": number,
                        "name": f"Cycle {number}: candidate readback",
                        "deliverables": [
                            {
                                "id": f"C{number}.D1",
                                "description": f"Preserve value {number}",
                                "validates": {
                                    "type": "file_exists",
                                    "file": f"src/c{number}.py",
                                },
                            }
                        ],
                        "exit_criteria": f"Cycle {number} complete",
                    }
                    for number in range(1, 118)
                ],
            }
        }
        manager.save_planning_deliverables(53, expected_plan)
        with run_server_process(launch, cwd=fresh, env=fresh_env) as proc:
            assert "serverInfo" in proc.initialize(client_name="pytest-target")
            tools = proc.list_tools()
            names = [tool["name"] for tool in tools]
            assert len(names) == len(set(names))
            assert set(names) >= TARGET_V3_TOOL_NAMES
            assert not {"run_quality_gates", "auto_fix"} & set(names)

            plan_response = proc.send_request(
                "tools/call",
                {"name": "get_project_plan", "arguments": {"issue_number": 53}},
            )
            presented = "\n".join(
                item["text"]
                for item in plan_response["result"]["content"]
                if item.get("type") == "text"
            )
            assert "Paged result; see pgmcp://docs/cache-reading" in presented
            guide = proc.send_request("resources/read", {"uri": "pgmcp://docs/cache-reading"})
            guide_text = guide["result"]["contents"][0]["text"]
            assert "next_offset" in guide_text
            assert "sha256" in guide_text
            match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", presented)
            assert match is not None
            uri = match.group()
            fragments: list[str] = []
            offset = 0
            while True:
                resource = proc.send_request(
                    "resources/read", {"uri": f"{uri}?offset={offset}&limit=6000"}
                )
                page = json.loads(resource["result"]["contents"][0]["text"])
                assert page["offset"] == offset
                fragments.append(page["text"])
                next_offset = page["next_offset"]
                if next_offset is None:
                    break
                offset = next_offset
            complete = "".join(fragments)
            assert hashlib.sha256(complete.encode("utf-8")).hexdigest() == page["sha256"]
            parsed = json.loads(complete)
            assert "planning_deliverables" in parsed, sorted(parsed)
            assert parsed["planning_deliverables"] == expected_plan

            def schema_text() -> str:
                response = proc.send_request(
                    "tools/call",
                    {"name": "scaffold_schema", "arguments": {"artifact_type": "research"}},
                )
                content = response["result"]["content"]
                return next(
                    item["resource"]["text"]
                    for item in content
                    if item.get("type") == "resource"
                    and item["resource"]["uri"].startswith("schema://")
                )

            admitted = schema_text()
            manifest = fresh / ".pgmcp/template_suite/research/manifest.yaml"
            held = manifest.with_name("manifest.yaml.held")
            manifest.rename(held)
            try:
                assert schema_text() == admitted
            finally:
                held.rename(manifest)

        legacy = tmp_path / "legacy_workspace"
        legacy.mkdir()
        legacy_root = legacy / ".pgmcp"
        legacy_root.mkdir()
        (legacy_root / "templates").mkdir()
        shutil.copytree(distribution.root / "mcp_server/assets/config", legacy_root / "config")
        (legacy_root / ".version").write_text("2.0.0\n", encoding="utf-8")
        legacy_env = _installed_environment(distribution, legacy)
        _assert_candidate_launch_parity(launcher_python, legacy, legacy_env)
        ordinary = subprocess.run(
            [str(launcher_python), "-m", "mcp_server", "--upgrade"],
            cwd=legacy,
            env=legacy_env,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
        assert ordinary.returncode == 2, ordinary.stdout + ordinary.stderr
        assert (legacy_root / "templates").is_dir()
        forced = subprocess.run(
            [
                str(launcher_python),
                "-m",
                "mcp_server",
                "--upgrade",
                "--force-template-upgrade",
            ],
            cwd=legacy,
            env=legacy_env,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
        assert forced.returncode == 0, forced.stdout + forced.stderr
        assert (legacy_root / "installation.json").is_file()
        with run_server_process(launch, cwd=legacy, env=legacy_env) as proc:
            assert "serverInfo" in proc.initialize(client_name="pytest-migrated")
            names = [tool["name"] for tool in proc.list_tools()]
            assert len(names) == len(set(names))
            assert set(names) >= TARGET_V3_TOOL_NAMES
