# tests/mcp_server/unit/config/test_loader_behaviors.py
# template=unit_test version=manual created=2026-03-26T00:00Z updated=
"""Focused behavioral tests for ConfigLoader helper branches.

@layer: Tests (Unit)
@dependencies: [pathlib, pytest, mcp_server.config.loader, mcp_server.config.schemas]
"""

from pathlib import Path

import pytest

from mcp_server.config.loader import (
    ConfigLoader,
    normalize_config_root,
    resolve_config_root,
)
from mcp_server.config.schemas import WorkflowConfig
from mcp_server.core.exceptions import ConfigError
from tests.mcp_server.test_support import get_default_server_root


def _write_yaml(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _minimal_workflow_config() -> WorkflowConfig:
    return WorkflowConfig(
        version="1.0.0",
        workflows={
            "feature": {
                "name": "feature",
                "default_execution_mode": "interactive",
                "description": "Feature workflow",
            }
        },
    )


def test_normalize_config_root_handles_workspace_and_phase_gate_paths(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    config_root = workspace_root / get_default_server_root() / "config"

    # C3: normalize_config_root is a simple resolver — it always returns Path(...).resolve().
    # Any path is accepted without disk probes or heuristics.
    assert normalize_config_root(workspace_root) == workspace_root.resolve()
    assert (
        normalize_config_root(workspace_root / get_default_server_root())
        == (workspace_root / get_default_server_root()).resolve()
    )
    assert normalize_config_root(config_root) == config_root.resolve()


def test_resolve_config_root_uses_preferred_workspace_root(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    config_root = workspace_root / get_default_server_root() / "config"
    _write_yaml(config_root / "git.yaml", "branch_types: []\n")

    # Since C3 strips _probe_candidates,resolve_config_root will not look in .pgmcp/config/
    # and should raise FileNotFoundError.
    with pytest.raises(FileNotFoundError, match="Could not locate canonical phase-gate config"):
        resolve_config_root(
            preferred_root=workspace_root,
            required_files=("git.yaml",),
        )


def test_resolve_config_root_returns_explicit_root_when_required_files_exist(
    tmp_path: Path,
) -> None:
    config_root = tmp_path / get_default_server_root() / "config"
    _write_yaml(config_root / "workflows.yaml", "version: '1.0.0'\nworkflows: {}\n")

    assert (
        resolve_config_root(
            explicit_root=config_root,
            required_files=("workflows.yaml",),
        )
        == config_root.resolve()
    )


def test_resolve_config_root_raises_for_missing_required_file_in_explicit_root(
    tmp_path: Path,
) -> None:
    config_root = tmp_path / get_default_server_root() / "config"
    config_root.mkdir(parents=True)

    with pytest.raises(FileNotFoundError, match="missing required files"):
        resolve_config_root(
            explicit_root=config_root,
            required_files=("workflows.yaml",),
        )


def test_resolve_config_root_raises_for_nonexistent_explicit_root(tmp_path: Path) -> None:
    missing_root = tmp_path / get_default_server_root() / "config"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        resolve_config_root(explicit_root=missing_root)


def test_real_enforcement_config_declares_chore_branch_policy() -> None:
    """New chore branches use the standard non-hotfix base policy."""
    config_root = Path(__file__).resolve().parents[4] / get_default_server_root() / "config"
    config = ConfigLoader(config_root).load_enforcement_config()
    create_branch_rule = next(rule for rule in config.enforcement if rule.tool == "create_branch")
    branch_policy = next(
        action for action in create_branch_rule.actions if action.type == "check_branch_policy"
    )

    assert branch_policy.rules["chore"] == ["main", "epic/*"]
    assert "fix" not in branch_policy.rules


def test_load_enforcement_config_allows_missing_file(tmp_path: Path) -> None:
    loader = ConfigLoader(tmp_path / get_default_server_root() / "config")

    assert loader.load_enforcement_config().enforcement == []


def test_load_operation_policies_uses_workflow_loader_fallback(tmp_path: Path) -> None:
    config_root = tmp_path / get_default_server_root() / "config"
    _write_yaml(
        config_root / "workflows.yaml",
        """
version: "1.0.0"
workflows:
  feature:
    name: "feature"
    default_execution_mode: "interactive"
    description: "Feature workflow"
""".strip()
        + "\n",
    )
    policies_path = _write_yaml(
        config_root / "policies.yaml",
        """
version: "1.0.0"
operations:
  commit:
    description: "Commit changes"
    allowed_phases: ["planning"]
    blocked_patterns: []
    allowed_extensions: []
    require_tdd_prefix: false
    allowed_prefixes: []
""".strip()
        + "\n",
    )

    config = ConfigLoader(config_root).load_operation_policies_config(
        config_path=policies_path,
    )

    assert config.get_operation_policy("commit").allowed_phases == ["planning"]


def test_load_operation_policies_requires_operations_key(tmp_path: Path) -> None:
    config_root = tmp_path / get_default_server_root() / "config"
    policies_path = _write_yaml(config_root / "policies.yaml", "version: '1.0.0'\n")
    loader = ConfigLoader(config_root)

    with pytest.raises(ConfigError, match="Missing 'operations' key"):
        loader.load_operation_policies_config(config_path=policies_path)
