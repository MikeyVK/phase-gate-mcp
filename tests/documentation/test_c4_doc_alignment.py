"""
C4 documentation alignment tests for issue #345.
Verifies that reference docs, agent files, and contracts.yaml
reflect the new git_delete_branch mode enum and branch-local state wording.

@layer: Tests (Documentation)
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]


# ---------------------------------------------------------------------------
# D4.1: git.md mode param documented
# ---------------------------------------------------------------------------


def test_git_md_delete_branch_mode_param_present() -> None:
    """git.md documents mode parameter for git_delete_branch with three values."""
    content = (REPO_ROOT / "docs" / "reference" / "mcp" / "tools" / "git.md").read_text(
        encoding="utf-8"
    )
    # Verify mode param exists in the git_delete_branch section
    delete_section_start = content.index("### git_delete_branch")
    delete_section_end = content.index("\n### ", delete_section_start + 1)
    delete_section = content[delete_section_start:delete_section_end]
    assert "| `mode` |" in delete_section
    assert "local" in delete_section
    assert "remote" in delete_section
    assert "both" in delete_section


def test_git_md_delete_branch_migration_note_present() -> None:
    """git.md includes a migration note for the mode default change."""
    content = (REPO_ROOT / "docs" / "reference" / "mcp" / "tools" / "git.md").read_text(
        encoding="utf-8"
    )
    delete_section_start = content.index("### git_delete_branch")
    delete_section_end = content.index("\n### ", delete_section_start + 1)
    delete_section = content[delete_section_start:delete_section_end]
    # Must have migration or breaking-change note
    lower = delete_section.lower()
    assert "migration" in lower or "breaking" in lower


# ---------------------------------------------------------------------------
# D4.2: MCP_TOOLS.md mode param documented
# ---------------------------------------------------------------------------


def test_mcp_tools_md_delete_branch_mode_param_present() -> None:
    """MCP_TOOLS.md documents mode parameter for git_delete_branch."""
    content = (REPO_ROOT / "docs" / "reference" / "mcp" / "MCP_TOOLS.md").read_text(
        encoding="utf-8"
    )
    # Find git_delete_branch reference and check mode appears near it
    idx = content.index("git_delete_branch")
    # mode should appear in the document somewhere after the first mention
    assert "mode" in content[idx : idx + 2000]


# ---------------------------------------------------------------------------
# D4.3: project.md state.json wording fixed
# ---------------------------------------------------------------------------


def test_project_md_state_json_not_runtime_not_committed() -> None:
    """project.md no longer describes state.json as 'runtime, not committed'."""
    content = (REPO_ROOT / "docs" / "reference" / "mcp" / "tools" / "project.md").read_text(
        encoding="utf-8"
    )
    assert "(runtime, not committed)" not in content


def test_project_md_state_json_branch_local_wording() -> None:
    """project.md describes state.json as branch-local and committed."""
    content = (REPO_ROOT / "docs" / "reference" / "mcp" / "tools" / "project.md").read_text(
        encoding="utf-8"
    )
    # state.json line must now say branch-local, not runtime/not-committed
    # find the state.json line specifically
    lines = content.splitlines()
    state_json_lines = [ln for ln in lines if "state.json" in ln and "phase-gate" in ln]
    assert state_json_lines, "state.json reference line not found"
    state_line = state_json_lines[0]
    assert "branch-local" in state_line


# ---------------------------------------------------------------------------
# D4.4: imp.agent.md branch-local state wording
# ---------------------------------------------------------------------------


def test_imp_agent_md_branch_local_wording() -> None:
    """imp.agent.md contains branch-local state artifact wording."""
    content = (REPO_ROOT / ".github" / "agents" / "imp.agent.md").read_text(encoding="utf-8")
    assert "branch-local" in content


# ---------------------------------------------------------------------------
# D4.5: co.agent.md branch-local state wording
# ---------------------------------------------------------------------------


def test_co_agent_md_branch_local_wording() -> None:
    """co.agent.md contains branch-local state artifact wording."""
    content = (REPO_ROOT / ".github" / "agents" / "co.agent.md").read_text(encoding="utf-8")
    assert "branch-local" in content


# ---------------------------------------------------------------------------
# D4.6: contracts.yaml first-push discipline
# ---------------------------------------------------------------------------


def test_contracts_yaml_feature_first_push_present() -> None:
    """contracts.yaml feature workflow: git_push(set_upstream=True) at first commit."""
    content = (REPO_ROOT / ".phase-gate" / "config" / "contracts.yaml").read_text(encoding="utf-8")
    # find 'feature:' workflow section — must contain set_upstream
    feature_idx = content.index("\n  feature:\n")
    bug_idx = content.index("\n  bug:\n")
    feature_section = content[feature_idx:bug_idx]
    assert "set_upstream=True" in feature_section


def test_contracts_yaml_bug_first_push_present() -> None:
    """contracts.yaml bug workflow: git_push(set_upstream=True) at first commit."""
    content = (REPO_ROOT / ".phase-gate" / "config" / "contracts.yaml").read_text(encoding="utf-8")
    bug_idx = content.index("\n  bug:\n")
    refactor_idx = content.index("\n  refactor:\n")
    bug_section = content[bug_idx:refactor_idx]
    assert "set_upstream=True" in bug_section
