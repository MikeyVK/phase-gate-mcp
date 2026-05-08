# tests/mcp_server/unit/managers/test_c3_note_context_scaffold_chain.py
"""
C3 RED tests: NoteContext propagation through scaffold chain.

Validates that:
- ScaffoldArtifactTool.execute() passes NoteContext to ArtifactManager (no 'del context')
- ArtifactManager.scaffold_artifact() accepts note_context parameter
- TemplateScaffolder.validate() accepts note_context parameter
- BlockerNote, RecoveryNote produced in artifact_manager on validation/config errors
- SuggestionNote produced in template_scaffolder on validation errors

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.managers.artifact_manager, mcp_server.scaffolders.template_scaffolder,
               mcp_server.tools.scaffold_artifact, mcp_server.core.operation_notes]
"""

from __future__ import annotations

import inspect
from unittest.mock import AsyncMock, MagicMock

import pytest

from mcp_server.core.operation_notes import BlockerNote, NoteContext, RecoveryNote, SuggestionNote
from mcp_server.managers.artifact_manager import ArtifactManager
from mcp_server.scaffolders.template_scaffolder import TemplateScaffolder
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

    @pytest.mark.asyncio
    async def test_note_context_forwarded_to_manager(self) -> None:
        """NoteContext passed to execute() must be forwarded to manager.scaffold_artifact()."""
        manager = MagicMock()
        manager.scaffold_artifact = AsyncMock(return_value="/tmp/artifact.py")
        tool = ScaffoldArtifactTool(manager=manager)

        note_context = NoteContext()
        params = MagicMock()
        params.artifact_type = "dto"
        params.name = "MyDto"
        params.output_path = None
        params.context = {}

        await tool.execute(params, note_context)

        call_kwargs = manager.scaffold_artifact.call_args
        assert call_kwargs is not None
        # note_context must appear as a keyword argument
        assert "note_context" in call_kwargs.kwargs, (
            "execute() must pass note_context= to manager.scaffold_artifact()"
        )
        assert call_kwargs.kwargs["note_context"] is note_context, (
            "note_context forwarded to manager must be the same object"
        )


# ---------------------------------------------------------------------------
# D3.2 — ArtifactManager.scaffold_artifact() accepts note_context parameter
# ---------------------------------------------------------------------------


class TestArtifactManagerNoteContextParam:
    """D3.2: scaffold_artifact() signature includes note_context parameter."""

    def test_scaffold_artifact_accepts_note_context(self) -> None:
        """scaffold_artifact() must declare note_context in its signature."""
        sig = inspect.signature(ArtifactManager.scaffold_artifact)
        assert "note_context" in sig.parameters, (
            "ArtifactManager.scaffold_artifact() must accept note_context parameter"
        )


# ---------------------------------------------------------------------------
# D3.3 — TemplateScaffolder.validate() accepts note_context parameter
# ---------------------------------------------------------------------------


class TestTemplateScaffolderNoteContextParam:
    """D3.3: validate() signature includes note_context parameter."""

    def test_validate_accepts_note_context(self) -> None:
        """validate() must declare note_context in its signature."""
        sig = inspect.signature(TemplateScaffolder.validate)
        assert "note_context" in sig.parameters, (
            "TemplateScaffolder.validate() must accept note_context parameter"
        )


# ---------------------------------------------------------------------------
# D3.4–D3.6 — ArtifactManager produces BlockerNote / RecoveryNote
# ---------------------------------------------------------------------------


def _make_manager_with_failing_scaffolder(
    error: Exception,
) -> tuple[ArtifactManager, NoteContext]:
    """Return a manager whose scaffolder.validate() raises the given error."""
    from mcp_server.core.exceptions import ValidationError
    from mcp_server.managers.artifact_manager import ArtifactManagerDependencies
    from mcp_server.schemas import ArtifactRegistryConfig

    registry = MagicMock(spec=ArtifactRegistryConfig)
    artifact = MagicMock()
    artifact.template_path = "dto.py.jinja2"
    artifact.output_type = None
    registry.get_artifact.return_value = artifact

    scaffolder = MagicMock(spec=TemplateScaffolder)
    scaffolder.validate.side_effect = error

    deps = ArtifactManagerDependencies(
        registry=registry,
        scaffolder=scaffolder,
    )
    manager = ArtifactManager(dependencies=deps)
    note_context = NoteContext()
    return manager, note_context


class TestArtifactManagerProducesNotes:
    """D3.4–D3.6: ArtifactManager produces BlockerNote / RecoveryNote on error paths."""

    @pytest.mark.asyncio
    async def test_produces_blocker_note_on_validation_error(self) -> None:
        """On ValidationError from scaffolder.validate(), a BlockerNote must be produced."""
        from mcp_server.core.exceptions import ValidationError

        error = ValidationError("Missing required field: name")
        manager, note_context = _make_manager_with_failing_scaffolder(error)

        with pytest.raises(ValidationError):
            await manager.scaffold_artifact(
                "dto",
                output_path="/tmp/out.py",
                name="MyDto",
                note_context=note_context,
            )

        blocker_notes = note_context.of_type(BlockerNote)
        assert len(blocker_notes) >= 1, (
            "ArtifactManager must produce at least one BlockerNote on ValidationError"
        )

    @pytest.mark.asyncio
    async def test_blocker_note_message_contains_context(self) -> None:
        """BlockerNote message must contain diagnostic context."""
        from mcp_server.core.exceptions import ValidationError

        error = ValidationError("Missing required field: name")
        manager, note_context = _make_manager_with_failing_scaffolder(error)

        with pytest.raises(ValidationError):
            await manager.scaffold_artifact(
                "dto",
                output_path="/tmp/out.py",
                name="MyDto",
                note_context=note_context,
            )

        notes = note_context.of_type(BlockerNote)
        assert notes, "Expected BlockerNote"
        assert notes[0].message, "BlockerNote.message must be non-empty"

    @pytest.mark.asyncio
    async def test_produces_recovery_note_on_validation_error(self) -> None:
        """On ValidationError, a RecoveryNote with actionable hint must be produced."""
        from mcp_server.core.exceptions import ValidationError

        error = ValidationError("Missing required field: name")
        manager, note_context = _make_manager_with_failing_scaffolder(error)

        with pytest.raises(ValidationError):
            await manager.scaffold_artifact(
                "dto",
                output_path="/tmp/out.py",
                name="MyDto",
                note_context=note_context,
            )

        recovery_notes = note_context.of_type(RecoveryNote)
        assert len(recovery_notes) >= 1, (
            "ArtifactManager must produce at least one RecoveryNote on ValidationError"
        )


# ---------------------------------------------------------------------------
# D3.7 — TemplateScaffolder.validate() produces SuggestionNote
# ---------------------------------------------------------------------------


def _make_scaffolder_with_missing_field() -> tuple[TemplateScaffolder, NoteContext]:
    """Return a TemplateScaffolder configured to raise ValidationError for missing field."""
    from mcp_server.schemas import ArtifactRegistryConfig

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
    from mcp_server.validation.template_analyzer import Schema

    mock_schema = MagicMock(spec=Schema)
    mock_schema.required = ["name", "description"]

    import mcp_server.scaffolders.template_scaffolder as ts_mod

    original = ts_mod.introspect_template_with_inheritance
    ts_mod.introspect_template_with_inheritance = lambda *a, **k: mock_schema

    note_context = NoteContext()
    return scaffolder, note_context, original, ts_mod  # type: ignore[return-value]


class TestTemplateScaffolderProducesSuggestionNote:
    """D3.7: validate() produces SuggestionNote on missing-field ValidationError."""

    def test_produces_suggestion_note_on_missing_fields(self) -> None:
        """When required fields are missing, validate() must produce a SuggestionNote."""
        from mcp_server.core.exceptions import ValidationError

        scaffolder, note_context, original_fn, ts_mod = _make_scaffolder_with_missing_field()

        try:
            with pytest.raises(ValidationError):
                scaffolder.validate("dto", note_context=note_context)
        finally:
            ts_mod.introspect_template_with_inheritance = original_fn

        suggestion_notes = note_context.of_type(SuggestionNote)
        assert len(suggestion_notes) >= 1, (
            "TemplateScaffolder.validate() must produce at least one SuggestionNote "
            "when required fields are missing"
        )

    def test_suggestion_note_message_is_actionable(self) -> None:
        """SuggestionNote message must be non-empty and actionable."""
        from mcp_server.core.exceptions import ValidationError

        scaffolder, note_context, original_fn, ts_mod = _make_scaffolder_with_missing_field()

        try:
            with pytest.raises(ValidationError):
                scaffolder.validate("dto", note_context=note_context)
        finally:
            ts_mod.introspect_template_with_inheritance = original_fn

        notes = note_context.of_type(SuggestionNote)
        assert notes, "Expected SuggestionNote"
        assert notes[0].message, "SuggestionNote.message must be non-empty"
