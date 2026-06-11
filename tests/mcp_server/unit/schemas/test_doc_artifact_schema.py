# tests/mcp_server/unit/schemas/test_doc_artifact_schema.py
# SCAFFOLD: test:manual | 2026-02-18T00:00:00Z
"""Schema and pipeline tests for document artifact types.

Covers: research, planning, design, architecture, reference, generic_doc, validation_report

2 tests per artifact type:
  1. context_validates_minimal  - schema instantiates with required fields
  2. rejects_invalid_context    - empty context raises ValidationError

@layer: Tests (Unit)
@dependencies: pytest, pydantic, asyncio, mcp_server document artifact schemas
"""

import asyncio  # noqa: I001
import os
from pathlib import Path
from unittest.mock import Mock

import pytest

from mcp_server.core.exceptions import ValidationError
from mcp_server.managers.artifact_manager import ArtifactManager
from tests.mcp_server.test_support import make_artifact_manager


# ---------------------------------------------------------------------------
# Shared helpers (identical pattern to test_code_artifact_v2_parity.py)
# ---------------------------------------------------------------------------


def _make_manager(tmp_path: Path) -> ArtifactManager:
    return make_artifact_manager(tmp_path)


def _run_v2(manager: ArtifactManager, artifact_type: str, context: dict) -> str:
    """Run V2 pipeline (PYDANTIC_SCAFFOLDING_ENABLED=true), return rendered content."""
    output_captured: list[str] = []

    async def mock_validate(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202, ARG001
        return (True, "")

    manager.validation_service.validate = mock_validate
    manager.fs_adapter.write_file = Mock(
        side_effect=lambda p, c: output_captured.append(c)  # noqa: ARG005
    )

    os.environ["PYDANTIC_SCAFFOLDING_ENABLED"] = "true"
    try:
        asyncio.run(
            manager.scaffold_artifact(
                artifact_type, output_path="test_scaffold_output.py", **context
            )
        )
    finally:
        os.environ.pop("PYDANTIC_SCAFFOLDING_ENABLED", None)

    assert len(output_captured) == 1, f"V2 pipeline produced no output for {artifact_type}"
    return output_captured[0]


def _assert_has_metadata_header(output: str, label: str) -> None:
    """Assert output has a SCAFFOLD or template= metadata header."""
    has_scaffold = "# SCAFFOLD:" in output[:300]
    has_template = "# template=" in output[:300]
    assert has_scaffold or has_template, (
        f"{label} output missing metadata header (SCAFFOLD or template=)"
    )


# ---------------------------------------------------------------------------
# Research
# ---------------------------------------------------------------------------


class TestResearchSchema:
    """Schema and pipeline tests for research document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Research: Template Introspection",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "problem_statement": "Investigate template introspection limitations",
        "goals": ["Understand block override impact", "Map required vs optional fields"],
    }

    def test_research_context_validates_minimal(self) -> None:
        """ResearchContext schema accepts minimal required fields."""
        from mcp_server.schemas import ResearchContext  # noqa: PLC0415

        ctx = ResearchContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_research_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Research pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "research", {})


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------


class TestPlanningSchema:
    """Schema and pipeline tests for planning document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Planning: Doc Schemas",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "summary": "Implement Pydantic context schemas for doc artifact types",
        "cycles": [
            {"cycle": 6, "phase": "RED", "description": "failing tests"},
            {"cycle": 6, "phase": "GREEN", "description": "context schemas"},
        ],
    }

    def test_planning_context_validates_minimal(self) -> None:
        """PlanningContext schema accepts minimal required fields."""
        from mcp_server.schemas import PlanningContext  # noqa: PLC0415

        ctx = PlanningContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_planning_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Planning pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "planning", {})


# ---------------------------------------------------------------------------
# Design
# ---------------------------------------------------------------------------


class TestDesignSchema:
    """Schema and pipeline tests for design document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Design: Document Context Schemas",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "problem_statement": "No Pydantic schemas exist for document artifact types",
        "requirements_functional": [
            "Schema validates required fields",
            "RenderContext adds lifecycle",
        ],
        "requirements_nonfunctional": ["Consistent with existing BaseContext pattern"],
        "decision": "Implement XxxContext + XxxRenderContext for each doc type",
        "rationale": "Uniform pipeline coverage for all concrete templates",
    }

    def test_design_context_validates_minimal(self) -> None:
        """DesignContext schema accepts minimal required fields."""
        from mcp_server.schemas import DesignContext  # noqa: PLC0415

        ctx = DesignContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_design_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Design pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "design", {})


# ---------------------------------------------------------------------------
# Architecture
# ---------------------------------------------------------------------------


class TestArchitectureSchema:
    """Schema and pipeline tests for architecture document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Architecture: Schema Infrastructure",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "concepts": [
            "BaseContext: user-facing artifact fields",
            "BaseRenderContext: lifecycle-enriched for template rendering",
        ],
    }

    def test_architecture_context_validates_minimal(self) -> None:
        """ArchitectureContext schema accepts minimal required fields."""
        from mcp_server.schemas import ArchitectureContext  # noqa: PLC0415

        ctx = ArchitectureContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_architecture_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Architecture pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "architecture", {})


# ---------------------------------------------------------------------------
# Reference
# ---------------------------------------------------------------------------


class TestReferenceSchema:
    """Schema and pipeline tests for reference document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Reference: ResearchContext",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "source_file": "mcp_server/schemas/contexts/research.py",
        "test_file": "tests/mcp_server/unit/schemas/test_doc_artifact_schema.py",
        "api_reference": [
            {"name": "ResearchContext", "description": "Context schema for research artifacts"},
        ],
    }

    def test_reference_context_validates_minimal(self) -> None:
        """ReferenceContext schema accepts minimal required fields."""
        from mcp_server.schemas import ReferenceContext  # noqa: PLC0415

        ctx = ReferenceContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_reference_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Reference pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "reference", {})


# ---------------------------------------------------------------------------
# Validation Report
# ---------------------------------------------------------------------------


class TestValidationReportSchema:
    """Schema and pipeline tests for validation_report document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Cycle Validation",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "issue_number": 286,
        "cycle": "C_286.4",
        "validation_status": "PASS",
        "scope": "Minimal behavior smoke",
    }

    def test_validation_report_context_validates_minimal(self) -> None:
        """ValidationReportContext schema accepts minimal required fields."""
        from mcp_server.schemas import ValidationReportContext  # noqa: PLC0415

        ctx = ValidationReportContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_validation_report_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """Validation report pipeline rejects empty context with ValidationError."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "validation_report", {})


# ---------------------------------------------------------------------------
# Generic Doc
# ---------------------------------------------------------------------------


class TestGenericDocSchema:
    """Schema and pipeline tests for generic_doc document artifact."""

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ArtifactManager:
        return _make_manager(tmp_path)

    _MINIMAL = {
        "title": "Migration Guide",
        "status": "DRAFT",
        "version": "1.0",
        "last_updated": "2026-02-18",
        "purpose": "Guide users through the migration.",
        "summary": "Summarizes the operational changes for the new workflow.",
    }

    def test_generic_doc_context_validates_minimal(self) -> None:
        """GenericDocContext schema accepts minimal required fields."""
        from mcp_server.schemas import GenericDocContext  # noqa: PLC0415

        ctx = GenericDocContext(**self._MINIMAL)
        assert ctx.title == self._MINIMAL["title"]

    def test_generic_doc_rejects_invalid_context(self, manager: ArtifactManager) -> None:
        """generic_doc pipeline rejects an empty context."""
        with pytest.raises(ValidationError):
            _run_v2(manager, "generic_doc", {})
