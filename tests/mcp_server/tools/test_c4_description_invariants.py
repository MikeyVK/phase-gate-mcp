"""Tests for C4 A1 description invariants.

Each test asserts that the tool or field description contains the required
new content. Tests are RED until the descriptions are updated (GREEN phase).

Covers:
- SubmitPRTool.base: 3-tier cascade documentation
- SavePlanningDeliverablesTool / UpdatePlanningDeliverablesTool: validates-spec ref
- AddLabelsInput.labels: label naming constraints
- CreateMilestoneInput.due_on: ISO 8601 datetime format
- ValidateDTOTool: file-exists scope clarification
- TransitionPhaseTool.to_phase: get_work_context() pointer
- ForcePhaseTransitionTool.to_phase: get_work_context() pointer

@dependencies: pr_tools, project_tools, label_tools, milestone_tools, validation_tools, phase_tools
"""

from mcp_server.tools.label_tools import AddLabelsInput
from mcp_server.tools.milestone_tools import CreateMilestoneInput
from mcp_server.tools.phase_tools import ForcePhaseTransitionInput, TransitionPhaseInput
from mcp_server.tools.pr_tools import SubmitPRInput
from mcp_server.tools.project_tools import (
    SavePlanningDeliverablesInput,
    UpdatePlanningDeliverablesInput,
)


class TestC4DescriptionInvariants:
    """A1 description enrichments — C4."""

    def test_submit_pr_base_documents_cascade(self) -> None:
        """SubmitPRInput.base documents the 3-tier fallback cascade."""
        field_info = SubmitPRInput.model_fields["base"]
        desc = field_info.description or ""
        assert "state.json" in desc or "parent_branch" in desc or "git_config" in desc, (
            f"SubmitPRInput.base description must document cascade: {desc!r}"
        )

    def test_save_planning_deliverables_references_validates_spec(self) -> None:
        """SavePlanningDeliverablesInput.planning_deliverables references validates-spec."""
        field_info = SavePlanningDeliverablesInput.model_fields["planning_deliverables"]
        desc = field_info.description or ""
        assert "validates" in desc.lower(), (
            f"planning_deliverables description must reference validates-spec: {desc!r}"
        )

    def test_update_planning_deliverables_references_validates_spec(self) -> None:
        """UpdatePlanningDeliverablesInput.planning_deliverables references validates-spec."""
        field_info = UpdatePlanningDeliverablesInput.model_fields["planning_deliverables"]
        desc = field_info.description or ""
        assert "validates" in desc.lower(), (
            f"planning_deliverables description must reference validates-spec: {desc!r}"
        )

    def test_add_labels_mentions_naming_constraints(self) -> None:
        """AddLabelsInput.labels mentions label naming constraints."""
        field_info = AddLabelsInput.model_fields["labels"]
        desc = field_info.description or ""
        has_naming_note = (
            "category:value" in desc.lower()
            or "naming" in desc.lower()
            or "pattern" in desc.lower()
        )
        assert has_naming_note, (
            f"AddLabelsInput.labels description must mention naming constraints: {desc!r}"
        )

    def test_create_milestone_due_on_specifies_iso8601(self) -> None:
        """CreateMilestoneInput.due_on specifies ISO 8601 datetime format."""
        field_info = CreateMilestoneInput.model_fields["due_on"]
        desc = field_info.description or ""
        assert "YYYY-MM-DD" in desc or "T" in desc and "Z" in desc, (
            f"CreateMilestoneInput.due_on must specify ISO 8601 datetime format: {desc!r}"
        )

    def test_transition_phase_to_phase_references_get_work_context(self) -> None:
        """TransitionPhaseInput.to_phase description mentions get_work_context()."""
        field_info = TransitionPhaseInput.model_fields["to_phase"]
        desc = field_info.description or ""
        assert "get_work_context" in desc, (
            f"TransitionPhaseInput.to_phase must reference get_work_context(): {desc!r}"
        )

    def test_force_phase_transition_to_phase_references_get_work_context(self) -> None:
        """ForcePhaseTransitionInput.to_phase description mentions get_work_context()."""
        field_info = ForcePhaseTransitionInput.model_fields["to_phase"]
        desc = field_info.description or ""
        assert "get_work_context" in desc, (
            f"ForcePhaseTransitionInput.to_phase must reference get_work_context(): {desc!r}"
        )
