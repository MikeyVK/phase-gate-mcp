# tests/documentation/test_c5_agent_partitioning.py
# template=unit_test version=3d15d309 created=2026-07-08T05:15:53Z updated=
"""Unit tests for agent instructions partitioning.

@layer: Tests (Unit)
@dependencies: [pathlib]
"""

# Project modules
from pathlib import Path


def _read_normalized(path: Path) -> str:
    """Read file content and normalize line endings."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()


class TestC5AgentPartitioning:
    """Test suite for agent instructions partitioning."""

    def test_copilot_agents_partitioned(self) -> None:
        """Copilot agent instructions, prompts, and AGENTS.md must exist in partitioned path."""
        repo_root = Path(__file__).parent.parent.parent
        copilot_agents_dir = repo_root / "docs" / "agents" / "copilot"

        # Check global AGENTS.md
        copilot_agents_md = copilot_agents_dir / "AGENTS.md"
        root_agents_md = repo_root / "AGENTS.md"
        assert copilot_agents_md.exists()

        assert _read_normalized(copilot_agents_md) == _read_normalized(root_agents_md)

        # Check persona files
        src_personas = repo_root / ".github" / "agents"
        dest_personas = copilot_agents_dir / ".github" / "agents"
        assert dest_personas.exists()
        for f in src_personas.glob("*.agent.md"):
            dest_file = dest_personas / f.name
            assert dest_file.exists()
            assert _read_normalized(dest_file) == _read_normalized(f)

        # Check prompts
        src_prompts = repo_root / ".github" / "prompts"
        dest_prompts = copilot_agents_dir / ".github" / "prompts"
        assert dest_prompts.exists()
        for f in src_prompts.glob("*.prompt.md"):
            dest_file = dest_prompts / f.name
            assert dest_file.exists()
            assert _read_normalized(dest_file) == _read_normalized(f)

    def test_antigravity_agents_partitioned(self) -> None:
        """Antigravity agent instructions and AGENTS.md must exist in partitioned path."""
        repo_root = Path(__file__).parent.parent.parent
        antigravity_dir = repo_root / "docs" / "agents" / "antigravity"

        # Check global AGENTS.md
        antigravity_agents_md = antigravity_dir / "AGENTS.md"
        root_agents_md = repo_root / "AGENTS.md"
        assert antigravity_agents_md.exists()

        assert _read_normalized(antigravity_agents_md) == _read_normalized(root_agents_md)

        # Check persona rules
        src_rules = repo_root / ".agents" / "rules"
        dest_rules = antigravity_dir / "rules"
        assert dest_rules.exists()
        for f in src_rules.glob("*.agent.md"):
            dest_file = dest_rules / f.name
            assert dest_file.exists()
            assert _read_normalized(dest_file) == _read_normalized(f)

        # Check workflows
        src_workflows = repo_root / ".agents" / "workflows"
        dest_workflows = antigravity_dir / "workflows"
        assert dest_workflows.exists()
        for f in src_workflows.glob("*.md"):
            dest_file = dest_workflows / f.name
            assert dest_file.exists()
            assert _read_normalized(dest_file) == _read_normalized(f)

    def test_original_files_untouched(self) -> None:
        """Original files must remain in their locations."""
        repo_root = Path(__file__).parent.parent.parent
        assert (repo_root / "AGENTS.md").exists()
        assert (repo_root / ".github" / "agents").exists()
        assert (repo_root / ".agents" / "rules").exists()
        assert (repo_root / ".agents" / "workflows").exists()
