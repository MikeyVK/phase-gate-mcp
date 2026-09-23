# tests/mcp_server/integration/test_target_startup.py
# template=integration_test version=c2e61372 created=2026-09-17T16:47Z updated=2026-09-17
"""Integration tests for target_startup_composition_and_launch_rehearsal.

Integration rehearsal testing target runtime composition, server process handshake,
startup lock exclusion, and configuration verification.

@layer: Tests (Integration)
@dependencies: [pytest, mcp_server.bootstrap, tests.mcp_server.fixtures.server_process]
@responsibilities:
    - Test end-to-end target_startup_composition_and_launch_rehearsal
    - Verify current normal startup remains usable with legacy tools
    - Verify target tool assembly has 6 target V3 tools and no duplicate names
    - Verify presentation alignment for target tools
    - Verify DI-06 startup lock blocks concurrent target startup
    - Verify unresolved recovery refusal halts startup without mutating disk
    - Rehearse real stdio ServerProcess handshake and tool discovery
    - Rehearse configuration hashes and [tool.pyright] deletion preservation
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
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
from tests.mcp_server.integration.test_rollout_configuration import (
    PROSPECTIVE_V3_ARTIFACTS_YAML,
    PYPROJECT_AGENT_ASSET_NEW,
    PYPROJECT_AGENT_ASSET_OLD,
    PYPROJECT_PYRIGHT_HUNK,
    build_prospective_presentation_yaml,
)
from tests.mcp_server.test_support import make_project_manager

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
    """Create isolated config and server roots with prospective V3 artifacts.yaml."""
    server_root = tmp_path / "server_root"
    server_root.mkdir(parents=True, exist_ok=True)

    config_root = tmp_path / "config_root"
    config_root.mkdir(parents=True, exist_ok=True)

    # Copy existing YAML configs from live repository
    live_config = REPO_ROOT / ".pgmcp" / "config"
    for yaml_file in live_config.glob("*.yaml"):
        shutil.copy2(yaml_file, config_root / yaml_file.name)

    # Rehearse the exact prepared V3 placement and presentation inputs.
    (config_root / "artifacts.yaml").write_text(PROSPECTIVE_V3_ARTIFACTS_YAML, encoding="utf-8")
    presentation_path = config_root / "presentation.yaml"
    presentation_path.write_text(
        build_prospective_presentation_yaml(presentation_path.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (config_root / "quality.yaml").unlink()

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


def _replace_exact_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise AssertionError("candidate_dispatch_preimage_mismatch")
    return source.replace(old, new, 1)


def _apply_host_instruction_patches(candidate: Path) -> tuple[str, ...]:
    """Apply CY069's exact six source patches to mapped candidate assets only."""
    prepared = (REPO_ROOT / "docs/development/issue460/rollout-host-input.md").read_text(
        encoding="utf-8"
    )
    sources = (
        ("3.1", "docs/agents/vscode/copilot/AGENTS.md"),
        ("3.2", "docs/agents/codex/AGENTS.md"),
        ("3.3", "docs/agents/antigravity/AGENTS.md"),
        ("3.4", "docs/agents/vscode/copilot/.github/agents/qa.agent.md"),
        ("3.5", "docs/agents/vscode/copilot/.github/agents/co.agent.md"),
        ("3.6", "docs/agents/codex/rules/research.agent.md"),
    )
    for section, relative in sources:
        section_text = prepared.split(f"### {section} ", 1)[1].split("\n### ", 1)[0]
        preimage, postimage = re.findall(r"[a-f0-9]{64}", section_text)[:2]
        diff = section_text.split("```diff\n", 1)[1].split("\n```", 1)[0]
        path = candidate / relative
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == preimage
        newline = b"\r\n" if b"\r\n" in raw else b"\n"
        hunks = re.split(r"(?=^@@ )", diff, flags=re.MULTILINE)[1:]
        for hunk in hunks:
            lines = hunk.splitlines()[1:]
            old = (
                newline.join(
                    line[1:].encode("utf-8") for line in lines if line.startswith((" ", "-"))
                )
                + newline
            )
            new = (
                newline.join(
                    line[1:].encode("utf-8") for line in lines if line.startswith((" ", "+"))
                )
                + newline
            )
            assert raw.count(old) == 1, f"host_patch_preimage_mismatch:{section}"
            raw = raw.replace(old, new, 1)
        assert hashlib.sha256(raw).hexdigest() == postimage
        path.write_bytes(raw)
    return tuple(relative for _, relative in sources)


def _installed_candidate(tmp_path: Path) -> InstalledDistribution:
    """Build a separate wheel from exact isolated V3 config and dispatch copies."""
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

    patched_host_sources = _apply_host_instruction_patches(candidate)

    pyproject = candidate / "pyproject.toml"
    pyproject_source = _replace_exact_once(
        pyproject.read_text(encoding="utf-8"), PYPROJECT_PYRIGHT_HUNK, ""
    )
    pyproject_source = _replace_exact_once(
        pyproject_source,
        PYPROJECT_AGENT_ASSET_OLD,
        PYPROJECT_AGENT_ASSET_NEW,
    )
    pyproject.write_bytes(pyproject_source.encode("utf-8"))
    config = candidate / ".pgmcp/config"
    (config / "artifacts.yaml").write_text(PROSPECTIVE_V3_ARTIFACTS_YAML, encoding="utf-8")
    presentation = config / "presentation.yaml"
    presentation.write_text(
        build_prospective_presentation_yaml(presentation.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (config / "quality.yaml").unlink()

    cli = candidate / "mcp_server/cli.py"
    source = cli.read_text(encoding="utf-8")
    source = _replace_exact_once(
        source,
        "    args = parser.parse_args()\n",
        """    args, unknown = parser.parse_known_args()
    if args.upgrade:
        from mcp_server.cli_renewal import main as renewal_main

        sys.exit(renewal_main(sys.argv[1:], settings=_settings))
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")
""",
    )
    source = _replace_exact_once(
        source,
        """            # Write package version file
            version_file = resolved_server_root / ".version"
            version_file.write_text(_settings.server.version + "\\n", encoding="utf-8")
""",
        """            from mcp_server.cli_renewal import build_default_operation

            operation = build_default_operation(_settings)
            operation.execute()
            outcome = operation.last_result
            if outcome is None or outcome.exit_code != 0:
                raise RuntimeError("target_initialization_failed")
""",
    )
    old_upgrade_start = source.index("    if args.upgrade:\n", source.index("    if args.init:\n"))
    old_upgrade_end = source.index(
        "\n    resolved_server_root = Path(_settings.server.resolved_server_root)\n"
        "    if not resolved_server_root.exists():",
        old_upgrade_start,
    )
    source = source[:old_upgrade_start] + source[old_upgrade_end + 1 :]
    source = _replace_exact_once(
        source,
        "        server = bootstrapper.bootstrap()\n",
        "        server = bootstrapper.bootstrap_target()\n",
    )
    cli.write_text(source, encoding="utf-8")
    distribution = build_installed_distribution(candidate, tmp_path / "distribution")
    for relative in patched_host_sources:
        mapped = relative.removeprefix("docs/agents/")
        packaged = distribution.root / "mcp_server/assets/agents" / mapped
        assert packaged.is_file(), f"packaged_host_asset_missing:{mapped}"
        assert packaged.read_bytes() == (candidate / relative).read_bytes(), (
            f"packaged_host_asset_mismatch:{mapped}"
        )
    return distribution


def _installed_environment(distribution: InstalledDistribution, workspace: Path) -> dict[str, str]:
    env = os.environ.copy()
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


class TestTargetStartup:
    """Integration test suite for target_startup_composition_and_launch_rehearsal."""

    def test_current_normal_startup_remains_usable(self) -> None:
        """Verify normal bootstrap() preserves legacy V2 assembly and tools."""
        bootstrapper = ServerBootstrapper()
        server = bootstrapper.bootstrap()

        tool_names = {tool.name for tool in server.tools}
        # Legacy V2 tools must be present in normal startup
        for legacy_tool in LEGACY_V2_TOOL_NAMES:
            assert legacy_tool in tool_names, (
                f"Expected legacy tool {legacy_tool} in normal startup"
            )

        # Target V3 replacement tools must NOT be present in normal startup
        assert "run_checks" not in tool_names
        assert "apply_fixes" not in tool_names

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
            "validate_template",
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

    def test_real_server_process_handshake_default_legacy(self) -> None:
        """Verify real subprocess handshake on normal startup publishes legacy tools."""
        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT)
        env["PGMCP_WORKSPACE_ROOT"] = str(REPO_ROOT)
        env["PGMCP_SERVER_PROJECT_DIR"] = ".pgmcp"
        with run_server_process(
            [sys.executable, "-m", "mcp_server.core.proxy"],
            cwd=REPO_ROOT,
            env=env,
        ) as proc:
            info = proc.initialize(client_name="pytest-legacy", client_version="1.0.0")
            assert "serverInfo" in info
            assert info["serverInfo"]["name"] == "phase-gate-mcp"

            tools = proc.list_tools()
            tool_names = {t["name"] for t in tools}
            assert "run_quality_gates" in tool_names
            assert "auto_fix" in tool_names
            assert "run_checks" not in tool_names
            assert "apply_fixes" not in tool_names

    def test_installed_candidate_init_migration_and_mcp_handshake(self, tmp_path: Path) -> None:
        """Rehearse one installed V3 candidate across fresh and owner-migrated roots."""
        try:
            distribution = _installed_candidate(tmp_path)
        except Exception as exc:
            pytest.fail(f"candidate_build_rehearsal_failed:{exc!r}")
        assert distribution.root.resolve().is_relative_to(tmp_path.resolve())
        assert not distribution.root.resolve().is_relative_to(REPO_ROOT.resolve())
        launch = [sys.executable, "-m", "mcp_server.core.proxy"]

        fresh = distribution.workspace
        fresh_env = _installed_environment(distribution, fresh)
        initialized = subprocess.run(
            [sys.executable, "-m", "mcp_server", "--init"],
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
            assert "validate_template" in names

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
        shutil.copytree(REPO_ROOT / ".pgmcp/templates", legacy_root / "templates")
        shutil.copytree(distribution.root / "mcp_server/assets/config", legacy_root / "config")
        (legacy_root / ".version").write_text("2.0.0\n", encoding="utf-8")
        legacy_env = _installed_environment(distribution, legacy)
        ordinary = subprocess.run(
            [sys.executable, "-m", "mcp_server", "--upgrade"],
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
                sys.executable,
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
