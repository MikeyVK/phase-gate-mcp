# tests\documentation\test_c5_agent_partitioning.py
# template=unit_test version=3d15d309 created=2026-07-08T05:15:53Z updated=
"""Unit tests for pathlib.

@layer: Tests (Unit)
@dependencies: [pathlib]
@responsibilities:
    - Test TestC5AgentPartitioning functionality
"""

# Project modules
from pathlib import Path


class TestC5AgentPartitioning:
    """Test suite for pathlib."""

    def test_vscode_agents_partitioned(self) -> None:
        """VS Code agent instructions and AGENTS.md must exist in partitioned path."""
        repo_root = Path(__file__).parent.parent.parent
        vscode_agents_dir = repo_root / "docs" / "agents" / "vscode"

        # Check global AGENTS.md
        vscode_agents_md = vscode_agents_dir / "AGENTS.md"
        root_agents_md = repo_root / "AGENTS.md"
        assert vscode_agents_md.exists()

        vscode_content = vscode_agents_md.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        root_content = root_agents_md.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        assert vscode_content == root_content

        # Check persona files
        src_personas = repo_root / ".github" / "agents"
        dest_personas = vscode_agents_dir / ".github" / "agents"
        assert dest_personas.exists()
        for f in src_personas.glob("*.agent.md"):
            dest_file = dest_personas / f.name
            assert dest_file.exists()
            dest_content = dest_file.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            src_content = f.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            assert dest_content == src_content

    def test_antigravity_agents_partitioned(self) -> None:
        """Antigravity agent instructions and AGENTS.md must exist in partitioned path."""
        repo_root = Path(__file__).parent.parent.parent
        antigravity_dir = repo_root / "docs" / "agents" / "antigravity"

        # Check global AGENTS.md
        antigravity_agents_md = antigravity_dir / "AGENTS.md"
        root_agents_md = repo_root / "AGENTS.md"
        assert antigravity_agents_md.exists()

        antigravity_content = (
            antigravity_agents_md.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        )
        root_content = root_agents_md.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        assert antigravity_content == root_content

        # Check persona rules
        src_rules = repo_root / ".agents" / "rules"
        dest_rules = antigravity_dir / "rules"
        assert dest_rules.exists()
        for f in src_rules.glob("*.agent.md"):
            dest_file = dest_rules / f.name
            assert dest_file.exists()
            dest_content = dest_file.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            src_content = f.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            assert dest_content == src_content

        # Check workflows
        src_workflows = repo_root / ".agents" / "workflows"
        dest_workflows = antigravity_dir / "workflows"
        assert dest_workflows.exists()
        for f in src_workflows.glob("*.md"):
            dest_file = dest_workflows / f.name
            assert dest_file.exists()
            dest_content = dest_file.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            src_content = f.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            assert dest_content == src_content

    def test_original_files_untouched(self) -> None:
        """Original files must remain in their locations."""
        repo_root = Path(__file__).parent.parent.parent
        assert (repo_root / "AGENTS.md").exists()
        assert (repo_root / ".github" / "agents").exists()
        assert (repo_root / ".agents" / "rules").exists()
        assert (repo_root / ".agents" / "workflows").exists()
