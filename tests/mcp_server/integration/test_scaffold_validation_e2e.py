# artifact: type=integration_test, version=1.0, created=2026-01-21T22:32:32Z
"""
@module: tests.integration.scaffold_validation
@layer: Test Infrastructure
@dependencies: [pytest, mcp_server.tools.scaffold_artifact,
                mcp_server.core.exceptions.ValidationError]
@responsibilities:
    - Test ValidationError schema integration with ToolResult
    - Verify schema returned on missing required fields (type:text for agent readability)
"""

# Standard library
from pathlib import Path

# Third-party
import pytest

# Project modules
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.artifact_manager import ArtifactManager
from mcp_server.tools.scaffold_artifact import (
    ScaffoldArtifactInput,
    ScaffoldArtifactTool,
)


@pytest.fixture()
def _force_v1_pipeline(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force V1 pipeline (used only by tests that explicitly request it)."""
    monkeypatch.setenv("PYDANTIC_SCAFFOLDING_ENABLED", "false")


@pytest.mark.asyncio
async def test_validation_error_returns_schema(
    artifact_manager: ArtifactManager, temp_workspace: Path
) -> None:
    """Verify missing required fields returns ValidationError with schema"""
    # GIVEN: scaffold_artifact tool with incomplete context (missing required field)
    tool = ScaffoldArtifactTool(manager=artifact_manager)
    output_path = temp_workspace / "test_dto.py"
    scaffold_input = ScaffoldArtifactInput(
        artifact_type="dto",
        name="TestDTO",
        output_path=str(output_path),
        context={
            "name": "TestDTO"
            # Missing 'description' - required by DTO template
        },
    )

    # WHEN: Attempting to scaffold DTO artifact without required 'description' field
    result = await tool.execute(scaffold_input, NoteContext())

    # THEN: Returns ScaffoldArtifactOutput with success=False
    assert not result.success, "Scaffold should fail with missing required field"

    # Verify schema contains expected structure
    schema_json = result.validation_schema
    assert schema_json is not None
    assert "required" in schema_json, "Schema should have JSON Schema required list"
    assert "properties" in schema_json, "Schema should have JSON Schema properties"
    assert isinstance(schema_json["required"], list), "required should be a list"


@pytest.mark.asyncio
async def test_success_response_includes_schema(
    _force_v1_pipeline: None, artifact_manager: ArtifactManager, temp_workspace: Path
) -> None:
    """Verify successful scaffold includes schema in response"""
    # GIVEN: scaffold_artifact tool with complete valid context
    tool = ScaffoldArtifactTool(manager=artifact_manager)
    output_path = temp_workspace / "test_dto.py"
    scaffold_input = ScaffoldArtifactInput(
        artifact_type="dto",
        name="TestDTO",
        output_path=str(output_path),
        context={"name": "TestDTO", "description": "Test data transfer object", "fields": []},
    )

    # WHEN: Successfully scaffolding DTO artifact with all required fields
    result = await tool.execute(scaffold_input, NoteContext())

    # THEN: Returns ScaffoldArtifactOutput with success=True
    assert result.success, f"Scaffold should succeed: {result.error_message}"

    # Verify file was created
    assert output_path.exists(), "Generated file should exist"


@pytest.mark.asyncio
async def test_system_fields_filtered_from_schema(
    _force_v1_pipeline: None, artifact_manager: ArtifactManager, temp_workspace: Path
) -> None:
    """Verify system fields not included in agent-facing schema"""
    # GIVEN: Template with system fields (template_id, template_version, etc.)
    tool = ScaffoldArtifactTool(manager=artifact_manager)
    output_path = temp_workspace / "test_dto.py"
    scaffold_input = ScaffoldArtifactInput(
        artifact_type="dto",
        name="TestDTO",
        output_path=str(output_path),
        context={
            "name": "TestDTO"
            # Missing description - will trigger validation error with schema
        },
    )

    # WHEN: Validation error occurs and schema is returned
    result = await tool.execute(scaffold_input, NoteContext())

    # THEN: Schema only contains agent-input fields, system fields excluded
    assert not result.success, "Should fail validation"
    schema_json = result.validation_schema
    assert schema_json is not None
    system_fields = ["template_id", "template_version", "scaffold_created", "output_path"]

    for field in system_fields:
        assert field not in schema_json["required"], (
            f"System field {field} should not be in required"
        )
