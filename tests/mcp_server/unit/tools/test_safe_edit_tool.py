# tests/unit/tools/test_safe_edit_tool.py
"""
Unit tests for SafeEditTool.

Tests safe file editing with validation according to TDD principles.
Covers multi-mode editing (content/line_edits/insert_lines/search_replace),
mutex protection, validation modes, and edge cases.

@layer: Tests (Unit)
@dependencies: [pytest, pydantic, asyncio, tempfile, pathlib, unittest.mock,
                mcp_server.tools.safe_edit_tool]
@responsibilities:
    - Test all edit modes (content, line_edits, insert_lines, search/replace)
    - Verify validation modes (strict/interactive/verify_only)
    - Test mutex protection prevents concurrent edit race conditions
    - Cover edge cases (missing args, pattern not found, validation failures)
"""

# Standard library
import asyncio
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

# Third-party
import pytest
from pydantic import ValidationError

# Project modules
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.safe_edit_tool import SafeEditInput, SafeEditTool


class TestSafeEditTool:
    """Test suite for SafeEditTool."""

    @pytest.fixture
    def tool(self) -> SafeEditTool:
        """Fixture for SafeEditTool."""
        return SafeEditTool()

    @pytest.mark.asyncio
    async def test_missing_arguments(self) -> None:
        """Test execution with missing arguments."""
        # Missing content/edit mode raises ValidationError
        with pytest.raises(ValidationError):
            SafeEditInput(path="test.py")

        # Missing path raises ValidationError
        with pytest.raises(ValidationError):
            SafeEditInput(content="code")

    @pytest.mark.asyncio
    async def test_execute_strict_pass(self, tool: SafeEditTool) -> None:
        """Test strict mode with passing validation."""
        path = "test.py"
        content = "valid code"

        async def mock_validate(*_: object, **__: object) -> tuple[bool, str]:
            return True, ""

        with (
            patch.object(tool.validation_service, "validate", side_effect=mock_validate),
            patch("pathlib.Path.write_text") as mock_write,
            patch("pathlib.Path.parent") as mock_parent,
        ):
            mock_parent.mkdir = MagicMock()

            result = await tool.execute(
                SafeEditInput(path=path, content=content, mode="strict"), NoteContext()
            )

            assert "File saved successfully" in result.content[0]["text"]
            mock_write.assert_called_once_with(content, encoding="utf-8")

    @pytest.mark.asyncio
    async def test_execute_strict_fail(self, tool: SafeEditTool) -> None:
        """Test strict mode with failing validation."""
        path = "test.py"
        content = "invalid code"

        async def mock_validate(*_: object, **__: object) -> tuple[bool, str]:
            return False, "\n\n**Validation Issues:**\n❌ Error\n"

        with (
            patch.object(tool.validation_service, "validate", side_effect=mock_validate),
            patch("pathlib.Path.write_text") as mock_write,
        ):
            result = await tool.execute(
                SafeEditInput(path=path, content=content, mode="strict"), NoteContext()
            )

            text = result.content[0]["text"]
            assert "Edit rejected" in text
            assert "Error" in text
            mock_write.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_interactive_fail(self, tool: SafeEditTool) -> None:
        """Test interactive mode allows saving even with validation failure."""
        path = "test.py"
        content = "invalid code"

        async def mock_validate(*_: object, **__: object) -> tuple[bool, str]:
            return False, "\n\n**Validation Issues:**\n❌ Error\n"

        with (
            patch.object(tool.validation_service, "validate", side_effect=mock_validate),
            patch("pathlib.Path.write_text") as mock_write,
        ):
            result = await tool.execute(
                SafeEditInput(path=path, content=content, mode="interactive"), NoteContext()
            )

            text = result.content[0]["text"]
            assert "File saved successfully" in text
            assert "Saved with validation warnings" in text
            mock_write.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_verify_only(self, tool: SafeEditTool) -> None:
        """Test verify_only mode does not write to file."""
        path = "test.py"
        content = "code"

        async def mock_validate(*_: object, **__: object) -> tuple[bool, str]:
            return True, ""

        with (
            patch.object(tool.validation_service, "validate", side_effect=mock_validate),
            patch("pathlib.Path.write_text") as mock_write,
        ):
            result = await tool.execute(
                SafeEditInput(path=path, content=content, mode="verify_only"), NoteContext()
            )

            text = result.content[0]["text"]
            assert "Validation Passed" in text
            mock_write.assert_not_called()

    @pytest.mark.asyncio
    async def test_fallback_validator_logic(self, tool: SafeEditTool) -> None:
        """Test implicit addition of base TemplateValidator for python files."""
        path = "script.py"
        content = "code"

        async def mock_validate(*_: object, **__: object) -> tuple[bool, str]:
            return True, ""

        with patch.object(tool.validation_service, "validate", side_effect=mock_validate):
            await tool.execute(SafeEditInput(path=path, content=content), NoteContext())
            tool.validation_service.validate.assert_called_once()

    @pytest.mark.asyncio
    async def test_rejects_legacy_show_diff_argument(self, tool: SafeEditTool) -> None:
        """Contract test: SafeEditInput must reject the removed show_diff argument."""

        del tool  # Contract is enforced at input-model boundary

        with pytest.raises(ValidationError) as exc_info:
            SafeEditInput.model_validate(
                {
                    "path": "test.py",
                    "content": "new code",
                    "mode": "strict",
                    "show_diff": True,
                }
            )

        assert "show_diff" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_no_duplicate_real_validation(self, tool: SafeEditTool) -> None:
        """Test with REAL validation (no duplicate validation issues in response)."""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("valid = True\n")
            temp_path = f.name

        try:
            result = await tool.execute(
                SafeEditInput(
                    path=temp_path,
                    content="invalid syntax here @@@ not python",
                    mode="strict",
                ),
                NoteContext(),
            )

            text = result.content[0]["text"]
            issues_count = text.count("**Validation Issues:**")
            assert issues_count == 1, f"Expected 1 issues block, found {issues_count}\n{text}"
            assert "invalid syntax" in text.lower() or "syntax" in text.lower()

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_pattern_not_found_shows_context(self, tool: SafeEditTool) -> None:
        """Test that 'Pattern not found' error shows file context (Issue #125 - Priority 2)."""

        content = "# Header\nline 1\nline 2\nline 3\nline 4\nline 5\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = await tool.execute(
                SafeEditInput(
                    path=temp_path,
                    search="this pattern does not exist",
                    replace="new text",
                    mode="strict",
                ),
                NoteContext(),
            )

            assert result.is_error, "Expected error result"
            text = result.content[0]["text"]
            assert "not found" in text.lower(), f"Expected 'not found' in error\n{text}"
            assert "# Header" in text or "line 1" in text, (
                f"Expected file context in error message\n{text}"
            )

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_concurrent_edits_blocked(self, tool: SafeEditTool, tmp_path: Path) -> None:
        """Test that concurrent edits on same file are blocked (mutex protection)."""

        test_file = tmp_path / "concurrent_test.py"
        test_file.write_text("line 1\nline 2\nline 3\n")

        edit_results: list[dict] = []

        async def edit_task(task_id: int) -> None:
            try:
                result = await tool.execute(
                    SafeEditInput(
                        path=str(test_file),
                        line_edits=[
                            {
                                "start_line": 1,
                                "end_line": 1,
                                "new_content": f"task {task_id} line 1\n",
                            }
                        ],
                        mode="interactive",
                    ),
                    NoteContext(),
                )
                edit_results.append({"task": task_id, "success": True, "result": result})
            except (TimeoutError, ValueError, OSError) as e:
                edit_results.append({"task": task_id, "success": False, "error": str(e)})

        await asyncio.gather(edit_task(1), edit_task(2), edit_task(3))

        assert len(edit_results) == 3, f"Expected 3 results, got {len(edit_results)}"
        assert all(r["success"] for r in edit_results), (
            f"Expected all edits to succeed with mutex, "
            f"but got failures: {[r for r in edit_results if not r['success']]}"
        )

        # Verify sequential execution via final file state — the last task wins on line 1.
        final_content = test_file.read_text()
        assert final_content.startswith("task 3 line 1\n"), (
            "Expected the last sequential edit to win and persist in the file.\n"
            f"Final file content: {final_content}"
        )
