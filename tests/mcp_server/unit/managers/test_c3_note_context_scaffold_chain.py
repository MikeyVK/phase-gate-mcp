# tests/mcp_server/unit/managers/test_c3_note_context_scaffold_chain.py
"""Legacy renderer NoteContext behavior retained until renderer retirement.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.scaffolders.template_scaffolder,
               mcp_server.core.operation_notes]
"""

from __future__ import annotations

import inspect
from typing import Any
from unittest.mock import MagicMock

import pytest

import mcp_server.scaffolders.template_scaffolder as ts_scaffolder_mod
from mcp_server.core.exceptions import ValidationError
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.scaffolders.template_scaffolder import TemplateScaffolder
from mcp_server.scaffolding.template_introspector import TemplateSchema
from mcp_server.schemas import ArtifactRegistryConfig

# ---------------------------------------------------------------------------
# D3.3 — TemplateScaffolder.validate() accepts note_context
# ---------------------------------------------------------------------------


class TestTemplateScaffolderSignature:
    """D3.3: validate accepts note_context as optional keyword argument."""

    def test_validate_accepts_note_context(self) -> None:
        """validate signature must include note_context parameter."""
        sig = inspect.signature(TemplateScaffolder.validate)
        assert "note_context" in sig.parameters, (
            "TemplateScaffolder.validate must accept note_context parameter"
        )


# ---------------------------------------------------------------------------
# D3.7 — TemplateScaffolder.validate() produces Suggestion Note
# ---------------------------------------------------------------------------


def _make_scaffolder_with_missing_field() -> tuple[TemplateScaffolder, NoteContext, Any, Any]:
    """Return a TemplateScaffolder configured to raise ValidationError for missing field."""

    registry = MagicMock(spec=ArtifactRegistryConfig)
    artifact = MagicMock()
    artifact.template_path = "dto.py.jinja2"
    registry.get_artifact.return_value = artifact

    renderer = MagicMock()
    loader = MagicMock()
    loader.searchpath = ["/tmp/templates"]
    renderer.env = MagicMock()
    renderer.env.loader = loader

    scaffolder = TemplateScaffolder(registry=registry, renderer=renderer)

    # Patch introspect_template_with_inheritance to require 'name'

    mock_schema = MagicMock(spec=TemplateSchema)
    mock_schema.required = ["name", "description"]

    original = ts_scaffolder_mod.introspect_template_with_inheritance
    ts_scaffolder_mod.introspect_template_with_inheritance = lambda *_a, **_k: mock_schema

    note_context = NoteContext()
    return scaffolder, note_context, original, ts_scaffolder_mod


class TestTemplateScaffolderProducesSuggestionNote:
    """D3.7: validate() produces Note on missing-field ValidationError."""

    def test_produces_suggestion_note_on_missing_fields(self) -> None:
        """When required fields are missing, validate() must produce a Note."""

        scaffolder, note_context, original_fn, ts_mod = _make_scaffolder_with_missing_field()

        try:
            with pytest.raises(ValidationError):
                scaffolder.validate("dto", note_context=note_context)
        finally:
            ts_mod.introspect_template_with_inheritance = original_fn

        suggestion_notes = [
            n for n in note_context.of_type(Note) if n.key == "scaffold_missing_fields_suggestion"
        ]
        assert len(suggestion_notes) >= 1, (
            "TemplateScaffolder.validate() must produce scaffold_missing_fields_suggestion Note "
            "when required fields are missing"
        )

    def test_suggestion_note_message_is_actionable(self) -> None:
        """Note missing_fields must be non-empty."""

        scaffolder, note_context, original_fn, ts_mod = _make_scaffolder_with_missing_field()

        try:
            with pytest.raises(ValidationError):
                scaffolder.validate("dto", note_context=note_context)
        finally:
            ts_mod.introspect_template_with_inheritance = original_fn

        notes = [
            n for n in note_context.of_type(Note) if n.key == "scaffold_missing_fields_suggestion"
        ]
        assert notes, "Expected scaffold_missing_fields_suggestion Note"
        assert notes[0].params.get("missing_fields"), "Note params missing_fields must be non-empty"
