"""E2E tests for SearchDocumentationTool with production docs.

@layer: Tests (Integration)
@dependencies: pytest, mcp_server.config.settings, mcp_server.tools.discovery_tools
"""

from pathlib import Path

import pytest

from mcp_server.config.settings import Settings
from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.tool_outputs import SearchDocumentationOutput
from mcp_server.tools.discovery_tools import SearchDocumentationInput, SearchDocumentationTool


class TestSearchDocumentationE2E:
    """End-to-end tests for SearchDocumentationTool using real filesystem."""

    @pytest.fixture
    def sample_docs_dir(self, tmp_path: Path) -> Path:
        """Create sample documentation structure for testing."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        arch_dir = docs_dir / "architecture"
        arch_dir.mkdir()
        (arch_dir / "system.md").write_text(
            "# System Architecture\n\nPython-based microservices architecture using DTOs."
        )

        dev_dir = docs_dir / "development"
        dev_dir.mkdir()
        (dev_dir / "python_guide.md").write_text(
            "# Python Development Guide\n\nBest practices for Python development with DTOs."
        )

        coding_dir = docs_dir / "coding_standards"
        coding_dir.mkdir()
        (coding_dir / "style.md").write_text("# Code Style\n\nFollow PEP 8 style guidelines.")

        ref_dir = docs_dir / "reference"
        ref_dir.mkdir()
        (ref_dir / "api.md").write_text("# API Reference\n\nJavaScript API documentation.")

        return docs_dir

    @pytest.mark.asyncio
    async def test_tool_execute_with_real_docs(self, sample_docs_dir: Path) -> None:
        """Test tool.execute() with real filesystem docs (no mocks)."""
        tool = SearchDocumentationTool(
            settings=Settings(server={"workspace_root": str(sample_docs_dir.parent)})
        )
        result = await tool.execute(SearchDocumentationInput(query="Python"), NoteContext())

        assert isinstance(result, SearchDocumentationOutput)
        assert result.success is True
        assert result.query == "Python"
        assert result.results_count == 2
        assert any("python" in r.title.lower() for r in result.results)

    @pytest.mark.asyncio
    async def test_tool_execute_with_scope_filter(self, sample_docs_dir: Path) -> None:
        """Test tool.execute() with scope filter."""
        tool = SearchDocumentationTool(
            settings=Settings(server={"workspace_root": str(sample_docs_dir.parent)})
        )
        result = await tool.execute(
            SearchDocumentationInput(query="style", scope="coding_standards"), NoteContext()
        )

        assert result.success is True
        assert result.results_count == 1
        assert result.results[0].path.endswith("style.md")

    @pytest.mark.asyncio
    async def test_tool_execute_no_results(self, sample_docs_dir: Path) -> None:
        """Test tool.execute() when no results found."""
        tool = SearchDocumentationTool(
            settings=Settings(server={"workspace_root": str(sample_docs_dir.parent)})
        )
        result = await tool.execute(SearchDocumentationInput(query="xyznonexistent"), NoteContext())

        assert result.success is True
        assert result.results_count == 0
        assert len(result.results) == 0

    @pytest.mark.asyncio
    async def test_tool_execute_relevance_ranking(self, sample_docs_dir: Path) -> None:
        """Test that results are ranked by relevance."""
        tool = SearchDocumentationTool(
            settings=Settings(server={"workspace_root": str(sample_docs_dir.parent)})
        )
        result = await tool.execute(SearchDocumentationInput(query="Python"), NoteContext())

        assert result.success is True
        assert result.results_count > 0
        assert "Python Development Guide" in result.results[0].title

    @pytest.mark.asyncio
    async def test_tool_handles_missing_docs_dir(self, tmp_path: Path) -> None:
        tool = SearchDocumentationTool(settings=Settings(server={"workspace_root": str(tmp_path)}))
        with pytest.raises(ExecutionError, match="Documentation directory not found"):
            await tool.execute(SearchDocumentationInput(query="Python"), NoteContext())
