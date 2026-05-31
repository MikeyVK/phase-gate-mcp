"""Tests for C1 A4 schema overrides: CreateBranchTool and GitCommitTool.input_schema.

Verifies that input_schema enums and patterns reflect git_config values (not hardcoded).

Conventions tested:
- #7: branch_type.enum adapts to git.yaml branch_types
- #8: name.pattern adapts to git.yaml branch_name_pattern
- A4: commit_type.enum adapts to git.yaml commit_types

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.tools.git_tools
"""

from unittest.mock import MagicMock

from mcp_server.tools.git_tools import CreateBranchTool, GitCommitTool


def _make_manager(
    branch_types: list[str] | None = None,
    commit_types: list[str] | None = None,
    branch_name_pattern: str = "^[a-z][a-z0-9/-]*$",
) -> MagicMock:
    """Build a mock GitManager with the given config values."""
    manager = MagicMock()
    git_config = MagicMock()
    git_config.branch_types = branch_types or ["feature", "bug", "docs"]
    git_config.commit_types = commit_types or ["feat", "fix", "docs", "chore"]
    git_config.branch_name_pattern = branch_name_pattern
    manager.git_config = git_config
    return manager


class TestCreateBranchToolSchema:
    """A4 schema override: CreateBranchTool.input_schema reflects git_config values."""

    def test_branch_type_enum_matches_config(self) -> None:
        """input_schema.properties.branch_type.enum == git_config.branch_types."""
        custom_types = ["epic", "hotfix"]
        manager = _make_manager(branch_types=custom_types)
        tool = CreateBranchTool(manager=manager)

        schema = tool.input_schema
        assert "enum" in schema["properties"]["branch_type"]
        assert schema["properties"]["branch_type"]["enum"] == custom_types

    def test_branch_type_enum_excludes_types_not_in_config(self) -> None:
        """branch_type.enum does not contain types outside git_config.branch_types."""
        custom_types = ["epic", "hotfix"]
        manager = _make_manager(branch_types=custom_types)
        tool = CreateBranchTool(manager=manager)

        enum_values = tool.input_schema["properties"]["branch_type"]["enum"]
        assert "feature" not in enum_values

    def test_name_pattern_matches_config(self) -> None:
        """input_schema.properties.name.pattern == git_config.branch_name_pattern."""
        pattern = "^[a-z][a-z0-9/-]*$"
        manager = _make_manager(branch_name_pattern=pattern)
        tool = CreateBranchTool(manager=manager)

        schema = tool.input_schema
        assert "pattern" in schema["properties"]["name"]
        assert schema["properties"]["name"]["pattern"] == pattern


class TestGitCommitToolSchema:
    """A4 schema override: GitCommitTool.input_schema reflects git_config values."""

    def test_commit_type_enum_matches_config(self) -> None:
        """input_schema.properties.commit_type.enum == git_config.commit_types."""
        custom_types = ["feat", "fix", "hotfix"]
        manager = _make_manager(commit_types=custom_types)
        tool = GitCommitTool(manager=manager)

        schema = tool.input_schema
        assert "enum" in schema["properties"]["commit_type"]
        assert schema["properties"]["commit_type"]["enum"] == custom_types

    def test_commit_type_enum_excludes_invalid_types(self) -> None:
        """commit_type.enum does not contain unknown types."""
        manager = _make_manager(commit_types=["feat", "fix"])
        tool = GitCommitTool(manager=manager)

        enum_values = tool.input_schema["properties"]["commit_type"]["enum"]
        assert "invalid_type" not in enum_values
