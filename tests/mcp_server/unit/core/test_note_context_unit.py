# tests/mcp_server/unit/core/test_note_context_unit.py
"""
Unit tests for NoteContext and generic note entries.

@layer: Tests (Unit)
@dependencies: [mcp_server.core.operation_notes, mcp_server.tools.tool_result]
"""

# Standard library
from unittest.mock import Mock

# Project modules
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.tools.tool_result import ToolResult


def test_operation_notes_module_exists() -> None:
    """operation_notes module must exist and expose NoteContext."""
    assert NoteContext is not None


def test_note_context_produce_of_type_insertion_order() -> None:
    """produce() and of_type() preserve insertion order for matching variants."""
    context = NoteContext()
    context.produce(Note(key="allowed_branch_types", params={"types": "a"}))
    context.produce(Note(key="allowed_branch_types", params={"types": "b"}))
    context.produce(Note(key="allowed_branch_types", params={"types": "c"}))

    notes = context.of_type(Note)
    types = [note.params["types"] for note in notes]
    assert types == ["a", "b", "c"]


def test_render_empty_returns_base_unchanged() -> None:
    """render_to_response returns the original ToolResult when nothing is renderable."""
    context = NoteContext()
    base = ToolResult.text("ok")

    result = context.render_to_response(base)

    assert result is base


def test_note_context_delegation() -> None:
    """NoteContext must delegate to presenter.present_notes if presenter is passed."""
    mock_presenter = Mock()
    mock_presenter.present_notes.return_value = "Formatted markdown"

    context = NoteContext(presenter=mock_presenter, tool_name="dummy_tool")

    note = Note(key="test_key", params={"val": 1})
    context.produce(note)

    base = ToolResult.text("base content")
    result = context.render_to_response(base)

    mock_presenter.present_notes.assert_called_once_with("dummy_tool", [note])

    assert len(result.content) == 2
    assert result.content[0] == {"type": "text", "text": "base content"}
    assert result.content[1] == {"type": "text", "text": "Formatted markdown"}
