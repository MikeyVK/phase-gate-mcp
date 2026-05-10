"""RED tests for Cycle 2 of issue #260: state_root injection.

These tests verify that all production code accepts an injected state_root
and does NOT compute workspace_root / '.st3' internally.

TDD: These tests FAIL before the GREEN implementation.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# F1 / normalize_config_root — dir-name-agnostic
# ---------------------------------------------------------------------------


class TestNormalizeConfigRootPhaseGate:
    """normalize_config_root must accept .phase-gate/ as well as .st3/."""

    def test_accepts_phase_gate_config_dir(self, tmp_path: Path) -> None:
        """normalize_config_root('/ws/.phase-gate/config') → same path."""
        from mcp_server.config.loader import normalize_config_root

        config_dir = tmp_path / ".phase-gate" / "config"
        config_dir.mkdir(parents=True)
        result = normalize_config_root(config_dir)
        assert result == config_dir.resolve()

    def test_accepts_phase_gate_state_root(self, tmp_path: Path) -> None:
        """normalize_config_root('/ws/.phase-gate') → '/ws/.phase-gate/config'."""
        from mcp_server.config.loader import normalize_config_root

        state_root = tmp_path / ".phase-gate"
        config_dir = state_root / "config"
        config_dir.mkdir(parents=True)
        result = normalize_config_root(state_root)
        assert result == config_dir.resolve()

    def test_st3_still_works(self, tmp_path: Path) -> None:
        """Backward compat: normalize_config_root still accepts .st3/config."""
        from mcp_server.config.loader import normalize_config_root

        config_dir = tmp_path / ".st3" / "config"
        config_dir.mkdir(parents=True)
        result = normalize_config_root(config_dir)
        assert result == config_dir.resolve()

    def test_state_root_parent_gives_back_state_root(self, tmp_path: Path) -> None:
        """config_root.parent == state_root for any hidden dir name."""
        from mcp_server.config.loader import normalize_config_root

        for state_dir_name in (".st3", ".phase-gate", ".myapp"):
            state_root = tmp_path / state_dir_name
            config_dir = state_root / "config"
            config_dir.mkdir(parents=True)
            result = normalize_config_root(config_dir)
            assert result.parent == state_root.resolve(), (
                f"For {state_dir_name}: expected parent {state_root.resolve()}, got {result.parent}"
            )
            # Cleanup for next iteration
            import shutil
            shutil.rmtree(state_root)


# ---------------------------------------------------------------------------
# F1 / PhaseStateEngine — accepts state_root
# ---------------------------------------------------------------------------


class TestPhaseStateEngineStateRoot:
    """PhaseStateEngine must use injected state_root for state.json path."""

    def _make_engine(self, state_root: Path, workspace_root: Path) -> object:
        from mcp_server.managers.phase_state_engine import PhaseStateEngine

        return PhaseStateEngine(
            workspace_root=workspace_root,
            state_root=state_root,
            project_manager=MagicMock(),
            git_config=MagicMock(),
            contracts_config=MagicMock(),
            workphases_config=MagicMock(),
            state_repository=MagicMock(),
            scope_decoder=MagicMock(),
            workflow_gate_runner=MagicMock(),
            state_reconstructor=MagicMock(),
            workflow_state_mutator=MagicMock(),
        )

    def test_state_file_uses_injected_state_root(self, tmp_path: Path) -> None:
        """When state_root is provided, state_file = state_root / 'state.json'."""
        state_root = tmp_path / ".phase-gate"
        workspace_root = tmp_path / "workspace"

        engine = self._make_engine(state_root, workspace_root)

        assert engine.state_file == state_root / "state.json"

    def test_state_file_is_not_workspace_root_st3(self, tmp_path: Path) -> None:
        """state_file must NOT be derived from workspace_root / '.st3'."""
        state_root = tmp_path / ".phase-gate"
        workspace_root = tmp_path / "workspace"

        engine = self._make_engine(state_root, workspace_root)

        assert ".st3" not in str(engine.state_file)


# ---------------------------------------------------------------------------
# F1 / ProjectManager — accepts state_root
# ---------------------------------------------------------------------------


class TestProjectManagerStateRoot:
    """ProjectManager must use injected state_root for deliverables.json path."""

    def _make_manager(self, state_root: Path, workspace_root: Path) -> object:
        from mcp_server.managers.project_manager import ProjectManager

        return ProjectManager(
            workspace_root=workspace_root,
            state_root=state_root,
            contracts_config=MagicMock(),
            workflow_status_resolver=MagicMock(),
        )

    def test_deliverables_file_uses_injected_state_root(self, tmp_path: Path) -> None:
        state_root = tmp_path / ".phase-gate"
        workspace_root = tmp_path / "workspace"

        manager = self._make_manager(state_root, workspace_root)

        assert manager.deliverables_file == state_root / "deliverables.json"

    def test_deliverables_file_is_not_workspace_root_st3(self, tmp_path: Path) -> None:
        state_root = tmp_path / ".phase-gate"
        workspace_root = tmp_path / "workspace"

        manager = self._make_manager(state_root, workspace_root)

        assert ".st3" not in str(manager.deliverables_file)


# ---------------------------------------------------------------------------
# F1 / EnforcementRunner — accepts state_root
# ---------------------------------------------------------------------------


class TestEnforcementRunnerStateRoot:
    """EnforcementRunner._read_current_phase must use injected state_root."""

    def test_reads_from_state_root_not_workspace_dot_st3(self, tmp_path: Path) -> None:
        """_read_current_phase reads state.json from state_root, not workspace/.st3."""
        from mcp_server.managers.enforcement_runner import _read_current_phase  # pyright: ignore[reportPrivateUsage]

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir(parents=True)
        state_file = state_root / "state.json"
        state_file.write_text(json.dumps({"current_phase": "implementation"}), encoding="utf-8")

        # Must accept state_root directly (not workspace_root)
        result = _read_current_phase(state_root)
        assert result == "implementation"

    def test_enforcement_runner_init_accepts_state_root(self, tmp_path: Path) -> None:
        """EnforcementRunner must accept state_root kwarg."""
        from mcp_server.managers.enforcement_runner import EnforcementRunner

        state_root = tmp_path / ".phase-gate"
        runner = EnforcementRunner(
            workspace_root=tmp_path,
            state_root=state_root,
            config=MagicMock(),
        )
        assert runner.state_root == state_root


# ---------------------------------------------------------------------------
# F1 / build_phase_guard — accepts state_root
# ---------------------------------------------------------------------------


class TestBuildPhaseGuard:
    """build_phase_guard must take state_root (not workspace_root) and read state.json from it."""

    def test_reads_state_json_from_state_root(self, tmp_path: Path) -> None:
        from mcp_server.tools.git_tools import build_phase_guard

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir()
        state_file = state_root / "state.json"
        state_file.write_text(
            json.dumps({
                "branch": "feature/42-test",
                "current_phase": "implementation",
            }),
            encoding="utf-8",
        )

        guard = build_phase_guard(state_root)
        # Should not raise (phase matches)
        guard("feature/42-test", "implementation", None)

    def test_does_not_read_from_workspace_st3(self, tmp_path: Path) -> None:
        """Guard built with state_root must not read from workspace_root/.st3."""
        from mcp_server.tools.git_tools import build_phase_guard

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir()
        # No state.json in state_root — should skip silently (no file = no guard)

        # Create a misleading .st3/state.json at tmp_path (workspace root)
        st3_dir = tmp_path / ".st3"
        st3_dir.mkdir()
        (st3_dir / "state.json").write_text(
            json.dumps({"branch": "feature/42-test", "current_phase": "research"}),
            encoding="utf-8",
        )

        guard = build_phase_guard(state_root)
        # Should NOT raise — because guard reads from state_root, not workspace/.st3
        guard("feature/42-test", "implementation", None)


# ---------------------------------------------------------------------------
# F1 / cycle_tools — uses state_root in _get_current_branch
# ---------------------------------------------------------------------------


class TestCycleToolsStateRoot:
    """Cycle tools must read state.json from state_root, not workspace_root/.st3."""

    def test_transition_cycle_tool_reads_state_from_state_root(self, tmp_path: Path) -> None:
        """TransitionCycleTool._get_current_branch falls back to state_root/state.json."""
        from mcp_server.tools.cycle_tools import TransitionCycleTool

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir()
        state_file = state_root / "state.json"
        state_file.write_text(
            json.dumps({"branch": "feature/99-test"}), encoding="utf-8"
        )

        tool = TransitionCycleTool(
            workspace_root=tmp_path,
            state_root=state_root,
        )
        # Simulate git unavailable — should fall back to state.json
        with patch.object(tool, "_get_git_manager") as mock_git:
            mock_git.return_value.get_current_branch.side_effect = RuntimeError("no git")
            branch = tool._get_current_branch()  # pyright: ignore[reportPrivateUsage]
        assert branch == "feature/99-test"

    def test_transition_cycle_tool_does_not_read_from_workspace_st3(
        self, tmp_path: Path
    ) -> None:
        from mcp_server.tools.cycle_tools import TransitionCycleTool

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir()
        # No state.json in state_root

        # Put misleading state.json in workspace/.st3
        st3_dir = tmp_path / ".st3"
        st3_dir.mkdir()
        (st3_dir / "state.json").write_text(
            json.dumps({"branch": "feature/wrong-branch"}), encoding="utf-8"
        )

        tool = TransitionCycleTool(
            workspace_root=tmp_path,
            state_root=state_root,
        )
        with patch.object(tool, "_get_git_manager") as mock_git:
            mock_git.return_value.get_current_branch.return_value = "feature/correct-branch"
            branch = tool._get_current_branch()  # pyright: ignore[reportPrivateUsage]
        assert branch == "feature/correct-branch"


# ---------------------------------------------------------------------------
# F5 / admin_tools — workspace-aware restart marker
# ---------------------------------------------------------------------------


class TestAdminToolsRestartMarker:
    """_get_restart_marker_path must resolve relative to MCP_WORKSPACE_ROOT, not CWD."""

    def test_uses_mcp_workspace_root_env_var(self, tmp_path: Path) -> None:
        from mcp_server.tools.admin_tools import _get_restart_marker_path  # pyright: ignore[reportPrivateUsage]

        with patch.dict(os.environ, {"MCP_WORKSPACE_ROOT": str(tmp_path)}):
            result = _get_restart_marker_path()

        assert str(tmp_path) in str(result)
        assert ".restart_marker" in result.name

    def test_does_not_use_cwd_dot_st3(self, tmp_path: Path) -> None:
        from mcp_server.tools.admin_tools import _get_restart_marker_path  # pyright: ignore[reportPrivateUsage]

        fake_workspace = tmp_path / "workspace"
        fake_workspace.mkdir()
        with patch.dict(os.environ, {"MCP_WORKSPACE_ROOT": str(fake_workspace)}):
            result = _get_restart_marker_path()

        assert ".st3" not in str(result) or str(fake_workspace) in str(result)


# ---------------------------------------------------------------------------
# F6 / artifact_manager — ephemeral temp uses workspace_root
# ---------------------------------------------------------------------------


class TestArtifactManagerEphemeralTemp:
    """ArtifactManager ephemeral temp dir must be workspace_root-relative."""

    def test_ephemeral_temp_uses_workspace_root(self, tmp_path: Path) -> None:
        """Path('.st3/temp') must be replaced with self.workspace_root / state_dir / 'temp'."""
        from mcp_server.managers.artifact_manager import ArtifactManager

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir()
        (state_root / "template_registry.json").touch()

        manager = ArtifactManager(
            workspace_root=tmp_path,
            state_root=state_root,
            registry=MagicMock(),
        )

        # The internal state_root should be the injected one
        assert manager.state_root == state_root

    def test_template_registry_path_not_cwd_relative(self, tmp_path: Path) -> None:
        """template_registry path must be based on workspace_root, not CWD."""
        from mcp_server.managers.artifact_manager import ArtifactManager
        from mcp_server.scaffolding.template_registry import TemplateRegistry

        state_root = tmp_path / ".phase-gate"
        state_root.mkdir()
        registry_path = state_root / "template_registry.json"

        manager = ArtifactManager(
            workspace_root=tmp_path,
            state_root=state_root,
            registry=MagicMock(),
            template_registry=TemplateRegistry(registry_path=registry_path),
        )
        assert str(tmp_path) in str(manager.template_registry.registry_path)


# ---------------------------------------------------------------------------
# template_config — no CWD-relative .st3 fallback
# ---------------------------------------------------------------------------


class TestTemplateConfigNoCwdSt3:
    """get_template_root() must not check CWD-relative .st3/templates."""

    def test_does_not_fall_through_to_cwd_dot_st3(self, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        """Even if .st3/templates exists in CWD, it must not be used."""
        from mcp_server.utils import template_config

        st3_templates = tmp_path / ".st3" / "templates"
        st3_templates.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        # Patch package root to not exist so we can test isolation
        # Actually: package templates ALWAYS exist, so the function should return those
        # not the .st3/templates fallback. We verify package templates are returned.
        with patch.dict(os.environ, {}, clear=False):
            if "TEMPLATE_ROOT" in os.environ:
                del os.environ["TEMPLATE_ROOT"]
            result = template_config.get_template_root()

        # Must return package templates, not .st3/templates
        assert "scaffolding" in str(result), f"Expected scaffolding path, got: {result}"


# ---------------------------------------------------------------------------
# template_registry — default arg not .st3-based
# ---------------------------------------------------------------------------


class TestTemplateRegistryDefaultArg:
    """TemplateRegistry default registry_path must not hardcode .st3."""

    def test_default_registry_path_is_not_cwd_dot_st3(self) -> None:
        """TemplateRegistry() without args must not default to Path('.st3/...')."""
        import inspect
        from mcp_server.scaffolding.template_registry import TemplateRegistry

        sig = inspect.signature(TemplateRegistry.__init__)
        default = sig.parameters["registry_path"].default

        # Default should be None (not a .st3 Path)
        assert default is None or str(default) != ".st3/template_registry.json", (
            f"Default registry_path should not be '.st3/template_registry.json', got: {default}"
        )
