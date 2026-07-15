# tests/mcp_server/unit/managers/test_c3_note_context_scaffold_chain.py
"""
C3 RED tests: NoteContext propagation through scaffold chain.

Validates that:
- ScaffoldArtifactTool.execute() passes NoteContext to ArtifactManager (no 'del context')
- ArtifactManager.scaffold_artifact() accepts note_context parameter
- TemplateScaffolder.validate() accepts note_context parameter
- Note objects produced in artifact_manager on validation/config errors
- Suggestion Note produced in template_scaffolder on validation errors

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.managers.artifact_manager,
               mcp_server.scaffolders.template_scaffolder,
               mcp_server.tools.scaffold_artifact, mcp_server.core.operation_notes]
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

import mcp_server.scaffolders.template_scaffolder as ts_scaffolder_mod
from mcp_server.core.exceptions import ValidationError
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.managers.artifact_manager import ArtifactManager, ArtifactManagerDependencies
from mcp_server.scaffolders.template_scaffolder import TemplateScaffolder
from mcp_server.scaffolding.template_introspector import TemplateSchema
from mcp_server.schemas import ArtifactRegistryConfig
from mcp_server.tools.scaffold_artifact import ScaffoldArtifactTool

# ---------------------------------------------------------------------------
# D3.1 — ScaffoldArtifactTool.execute() must NOT discard NoteContext
# ---------------------------------------------------------------------------


class TestScaffoldArtifactToolNoteContext:
    """D3.1: execute() passes NoteContext to manager instead of discarding it."""

    def test_execute_does_not_del_context(self) -> None:
        """Source code of execute() must not contain 'del context'."""
        src = inspect.getsource(ScaffoldArtifactTool.execute)
        assert "del context" not in src, (
            "ScaffoldArtifactTool.execute() must not discard NoteContext via 'del context'"
        )


# ---------------------------------------------------------------------------
# D3.2 — ArtifactManager.scaffold_artifact() accepts note_context
# ---------------------------------------------------------------------------


class TestArtifactManagerSignature:
    """D3.2: scaffold_artifact accepts note_context as optional keyword argument."""

    def test_scaffold_artifact_accepts_note_context(self) -> None:
        """scaffold_artifact signature must include note_context parameter."""
        sig = inspect.signature(ArtifactManager.scaffold_artifact)
        assert "note_context" in sig.parameters, (
            "ArtifactManager.scaffold_artifact must accept note_context parameter"
        )
        param = sig.parameters["note_context"]
        assert param.default is inspect.Parameter.empty or param.default is None, (
            "note_context parameter should be optional"
        )


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


# Helper fixtures/methods for error path tests
def _make_manager_with_failing_scaffolder(
    exc_to_raise: Exception,
) -> tuple[ArtifactManager, NoteContext]:
    """Configure ArtifactManager with mock scaffolder that raises exc_to_raise on scaffold()."""

    registry = MagicMock(spec=ArtifactRegistryConfig)
    mock_art = MagicMock()
    from mcp_server.config.schemas.artifact_registry_config import SchemaFieldDef  # noqa: PLC0415
    mock_art.context_schema = {
        "name": SchemaFieldDef(
            type="string", title="Name", description="DTO Name", required=True
        ),
    }
    registry.get_artifact.return_value = mock_art

    scaffolder = MagicMock(spec=TemplateScaffolder)
    scaffolder.scaffold.side_effect = exc_to_raise

    dependencies = ArtifactManagerDependencies(
        registry=registry,
        scaffolder=scaffolder,
    )

    manager = ArtifactManager(dependencies=dependencies, server_root=Path("."))
    note_context = NoteContext()

    return manager, note_context


class TestArtifactManagerProducesNotes:
    """D3.4–D3.6: ArtifactManager produces Note on error paths."""

    @pytest.fixture(autouse=True)
    def _force_v1_pipeline(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Disable v2 Pydantic pipeline so scaffolder.scaffold() is reached directly."""
        monkeypatch.setenv("PYDANTIC_SCAFFOLDING_ENABLED", "false")

    @pytest.mark.asyncio
    async def test_produces_blocker_note_on_validation_error(self) -> None:
        """On ValidationError from scaffolder.validate(), a Note must be produced."""

        error = ValidationError("Missing required field: name")
        manager, note_context = _make_manager_with_failing_scaffolder(error)

        with pytest.raises(ValidationError):
            await manager.scaffold_artifact(
                "dto",
                output_path="/tmp/out.py",
                name="MyDto",
                note_context=note_context,
            )

        blocker_notes = [
            n for n in note_context.of_type(Note) if n.key == "scaffold_validation_failed"
        ]
        assert len(blocker_notes) >= 1, (
            "ArtifactManager must produce scaffold_validation_failed Note on ValidationError"
        )

    @pytest.mark.asyncio
    async def test_blocker_note_message_contains_context(self) -> None:
        """Note error_details must contain diagnostic context."""

        error = ValidationError("Missing required field: name")
        manager, note_context = _make_manager_with_failing_scaffolder(error)

        with pytest.raises(ValidationError):
            await manager.scaffold_artifact(
                "dto",
                output_path="/tmp/out.py",
                name="MyDto",
                note_context=note_context,
            )

        notes = [n for n in note_context.of_type(Note) if n.key == "scaffold_validation_failed"]
        assert notes, "Expected scaffold_validation_failed Note"
        assert notes[0].params.get("error_details"), (
            "Note.params['error_details'] must be non-empty"
        )

    @pytest.mark.asyncio
    async def test_produces_recovery_note_on_validation_error(self) -> None:
        """On ValidationError, a scaffold_fields_recovery Note must be produced."""

        error = ValidationError("Missing required field: name")
        manager, note_context = _make_manager_with_failing_scaffolder(error)

        with pytest.raises(ValidationError):
            await manager.scaffold_artifact(
                "dto",
                output_path="/tmp/out.py",
                name="MyDto",
                note_context=note_context,
            )

        recovery_notes = [
            n for n in note_context.of_type(Note) if n.key == "scaffold_fields_recovery"
        ]
        assert len(recovery_notes) >= 1, (
            "ArtifactManager must produce scaffold_fields_recovery Note on ValidationError"
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
