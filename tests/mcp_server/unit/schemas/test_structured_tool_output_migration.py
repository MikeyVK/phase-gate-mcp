# tests/mcp_server/unit/schemas/test_structured_tool_output_migration.py
# template=unit_test version=8825c0bb created=2026-08-22T00:00Z updated=2026-08-22
"""Approved structured DTO clean-break contract tests.

@layer: Tests (Unit)
@dependencies: [pydantic, tool_outputs]
@responsibilities:
    - Verify structured workflow state and numeric pytest duration
    - Verify obsolete presentation fields have no compatibility aliases
"""

import pytest

from mcp_server.schemas.tool_outputs import (
    AutoFixOutput,
    GetWorkContextOutput,
    LabelOperationOutput,
    PhaseTransitionOutput,
    RunTestsOutput,
    ScaffoldArtifactOutput,
    WorkflowStateStatus,
)


class TestStructuredToolOutputMigration:
    """Clean-break DTO contracts."""

    @pytest.mark.parametrize(
        "status",
        list(WorkflowStateStatus),
    )
    def test_work_context_exposes_structured_workflow_state(
        self,
        status: WorkflowStateStatus,
    ) -> None:
        output = GetWorkContextOutput(
            current_branch="feature/456-example",
            workflow_name="feature",
            phase="research",
            phase_source="state.json",
            phase_confidence="high",
            sub_role_hint="researcher",
            phase_instructions="inspect",
            workflow_state_status=status,
            valid_phases=("research", "design"),
        )

        assert output.workflow_state_status is status
        assert output.valid_phases == ("research", "design")

    def test_run_tests_uses_numeric_optional_duration(self) -> None:
        output = RunTestsOutput(
            exit_code=0,
            passed_count=3,
            failed_count=0,
            skipped_count=0,
            errors_count=0,
            duration_seconds=0.42,
        )

        assert output.duration_seconds == 0.42
        assert "summary_line" not in type(output).model_fields

    @pytest.mark.parametrize(
        ("model", "removed_fields"),
        [
            (AutoFixOutput, {"formatted_modified_files"}),
            (GetWorkContextOutput, {"invalid_phase_warning"}),
            (LabelOperationOutput, {"formatted_labels"}),
            (
                PhaseTransitionOutput,
                {"skipped_gates_warning", "passing_gates_info"},
            ),
            (
                ScaffoldArtifactOutput,
                {
                    "formatted_files_created",
                    "schema_info",
                },
            ),
        ],
    )
    def test_obsolete_presentation_fields_are_absent(
        self,
        model: type[object],
        removed_fields: set[str],
    ) -> None:
        assert removed_fields.isdisjoint(model.model_fields)  # type: ignore[attr-defined]
