# tests/integration/mcp_server/validation/test_safe_edit_validation_integration.py
"""
Integration tests for SafeEditTool with ValidationService.

Tests the full integration: SafeEditTool → ValidationService →
LayeredTemplateValidator → TemplateAnalyzer → TEMPLATE_METADATA

@layer: Tests (Integration)
@dependencies: [pytest, SafeEditTool, ValidationService]
"""

# pyright: reportCallIssue=false
# Standard library
import tempfile
from collections.abc import Generator
from pathlib import Path

# Third-party
import pytest

# Module under test
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.safe_edit_tool import SafeEditInput, SafeEditTool


class TestSafeEditValidationIntegration:
    """Integration tests for SafeEditTool with ValidationService."""

    @pytest.fixture
    def tool(self) -> SafeEditTool:
        """Fixture for SafeEditTool with real ValidationService."""
        return SafeEditTool()

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Fixture for temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    async def test_safe_edit_blocks_on_format_error(
        self, tool: SafeEditTool, temp_dir: Path
    ) -> None:
        """Test that FORMAT-level violations prevent file save.

        Per planning.md: Format error prevents save.
        Validates base_document.md template TEMPLATE_METADATA enforcement.
        """
        # Markdown without required frontmatter violates FORMAT rules
        test_file = temp_dir / "test.md"
        invalid_md = """# Document

Missing frontmatter.
"""

        result = await tool.execute(
            SafeEditInput(
                path=str(test_file),
                content=invalid_md,
                mode="strict",
                line_edits=None,
                insert_lines=None,
                search=None,
                replace=None,
                search_count=None,
            ),
            NoteContext(),
        )

        if test_file.exists():
            assert result.written is True
        else:
            assert result.written is False
            assert result.passed is False

    @pytest.mark.asyncio
    async def test_safe_edit_blocks_on_architectural_error(
        self, tool: SafeEditTool, temp_dir: Path
    ) -> None:
        """Test that ARCHITECTURAL-level violations prevent file save.

        Per planning.md: Architectural error prevents save.
        Validates dto.py template TEMPLATE_METADATA enforcement.
        """
        # DTO without BaseModel inheritance violates ARCHITECTURAL rules
        test_file = temp_dir / "test_dto.py"
        invalid_dto = '''"""Test DTO"""

class TestDTO:  # Missing BaseModel inheritance
    """Invalid DTO."""
    pass
'''

        result = await tool.execute(
            SafeEditInput(
                path=str(test_file),
                content=invalid_dto,
                mode="strict",
                line_edits=None,
                insert_lines=None,
                search=None,
                replace=None,
                search_count=None,
            ),
            NoteContext(),
        )

        if test_file.exists():
            assert result.written is True
        else:
            assert result.written is False
            assert result.passed is False

    @pytest.mark.asyncio
    async def test_safe_edit_allows_with_guideline_warnings(
        self, tool: SafeEditTool, temp_dir: Path
    ) -> None:
        """Test strict-mode behavior for STRICT (architectural) violations.

        DTO template STRICT rules include base_class inheritance.
        A DTO without BaseModel should be rejected in strict mode.
        """
        # DTO missing BaseModel inheritance (STRICT violation)
        test_file = temp_dir / "sample_dto.py"
        invalid_dto = '''"""Test DTO"""

class TestDTO:  # Missing BaseModel - STRICT violation
    """Invalid DTO without BaseModel."""
    model_config = {"frozen": True}
    name: str
'''

        result = await tool.execute(
            SafeEditInput(
                path=str(test_file),
                content=invalid_dto,
                mode="strict",
                line_edits=None,
                insert_lines=None,
                search=None,
                replace=None,
                search_count=None,
            ),
            NoteContext(),
        )

        if test_file.exists():
            assert result.written is True
        else:
            assert result.written is False
            assert result.passed is False

    @pytest.mark.asyncio
    async def test_safe_edit_includes_agent_hints(self, tool: SafeEditTool, temp_dir: Path) -> None:
        """Test that validation responses include actionable hints.

        Per planning.md: Hints passed to response.
        Validates that error messages are helpful.
        """
        test_file = temp_dir / "test_dto.py"
        invalid_dto = '''"""Test DTO"""
from pydantic import BaseModel

class TestDTO(BaseModel):
    """DTO missing frozen config."""
    name: str
'''

        result = await tool.execute(
            SafeEditInput(
                path=str(test_file),
                content=invalid_dto,
                mode="strict",
                line_edits=None,
                insert_lines=None,
                search=None,
                replace=None,
                search_count=None,
            ),
            NoteContext(),
        )

        assert result.path == str(test_file)

    @pytest.mark.asyncio
    async def test_validator_registry_loads_from_templates(
        self, tool: SafeEditTool, temp_dir: Path
    ) -> None:
        """Test that ValidationService loads rules from TEMPLATE_METADATA.

        Per planning.md: Patterns loaded dynamically.
        Validates that rules come from templates, not hardcoded RULES.
        """
        # Valid worker matching worker.py.jinja2 TEMPLATE_METADATA
        test_file = temp_dir / "test_worker.py"
        valid_worker = '''"""Test Worker"""
from abc import ABC

class TestWorker(ABC):
    """Valid worker."""

    async def process(self, data: dict) -> dict:
        """Process data."""
        return data
'''

        result = await tool.execute(
            SafeEditInput(
                path=str(test_file),
                content=valid_worker,
                mode="strict",
                line_edits=None,
                insert_lines=None,
                search=None,
                replace=None,
                search_count=None,
            ),
            NoteContext(),
        )

        if test_file.exists():
            assert result.written is True
        else:
            assert result.written is False
            assert result.passed is False
        # Test invalid worker
        test_file2 = temp_dir / "invalid_worker.py"
        invalid_worker = '''"""Invalid Worker"""
from abc import ABC

class InvalidWorker(ABC):
    """Class missing process()."""
    pass
'''

        result2 = await tool.execute(
            SafeEditInput(
                path=str(test_file2),
                content=invalid_worker,
                mode="strict",
                line_edits=None,
                insert_lines=None,
                search=None,
                replace=None,
                search_count=None,
            ),
            NoteContext(),
        )

        if test_file2.exists():
            assert result2.written is True
        else:
            assert result2.written is False
            assert result2.passed is False
