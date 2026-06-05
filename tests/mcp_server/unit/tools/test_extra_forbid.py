from typing import Any

import pytest
from pydantic import ValidationError

from mcp_server.tools.admin_tools import RestartServerInput
from mcp_server.tools.cycle_tools import ForceCycleTransitionInput, TransitionCycleInput
from mcp_server.tools.discovery_tools import GetWorkContextInput, SearchDocumentationInput
from mcp_server.tools.git_analysis_tools import GitDiffInput, GitListBranchesInput
from mcp_server.tools.git_fetch_tool import GitFetchInput
from mcp_server.tools.git_pull_tool import GitPullInput
from mcp_server.tools.git_tools import (
    GetParentBranchInput,
    GitCheckoutInput,
    GitDeleteBranchInput,
    GitMergeInput,
    GitPushInput,
    GitRestoreInput,
    GitStashInput,
    GitStatusInput,
)
from mcp_server.tools.health_tools import HealthCheckInput
from mcp_server.tools.issue_tools import (
    CloseIssueInput,
    GetIssueInput,
    ListIssuesInput,
    UpdateIssueInput,
)
from mcp_server.tools.label_tools import (
    AddLabelsInput,
    CreateLabelInput,
    DeleteLabelInput,
    DetectLabelDriftInput,
    ListLabelsInput,
    RemoveLabelsInput,
)
from mcp_server.tools.milestone_tools import (
    CloseMilestoneInput,
    CreateMilestoneInput,
    ListMilestonesInput,
)
from mcp_server.tools.phase_tools import ForcePhaseTransitionInput, TransitionPhaseInput
from mcp_server.tools.pr_tools import ListPRsInput, MergePRInput, SubmitPRInput
from mcp_server.tools.project_tools import (
    GetProjectPlanInput,
    SavePlanningDeliverablesInput,
    UpdatePlanningDeliverablesInput,
)
from mcp_server.tools.quality_tools import RunQualityGatesInput
from mcp_server.tools.safe_edit_tool import LineEdit, SafeEditInput
from mcp_server.tools.scaffold_artifact import ScaffoldArtifactInput
from mcp_server.tools.template_validation_tool import TemplateValidationInput
from mcp_server.tools.test_tools import RunTestsInput


class TestExtraForbidOnAllInputModels:
    """Parametrized test: all input models reject extra fields."""

    @pytest.mark.parametrize(
        "model_class,valid_kwargs",
        [
            # admin
            (RestartServerInput, {}),
            # cycle
            (TransitionCycleInput, {"to_cycle": 2}),
            (
                ForceCycleTransitionInput,
                {"to_cycle": 2, "skip_reason": "r", "human_approval": "ok"},
            ),
            # discovery
            (SearchDocumentationInput, {"query": "test"}),
            (GetWorkContextInput, {}),
            # git_analysis
            (GitListBranchesInput, {}),
            (GitDiffInput, {"target_branch": "main"}),
            # git_fetch
            (GitFetchInput, {}),
            # git_pull
            (GitPullInput, {}),
            # git_tools
            (GitStatusInput, {}),
            (GitRestoreInput, {"files": ["file.py"]}),
            (GitCheckoutInput, {"branch": "main"}),
            (GitPushInput, {}),
            (GitMergeInput, {"branch": "feature/1-x"}),
            (GitDeleteBranchInput, {"branch": "feature/1-x"}),
            (GitStashInput, {"action": "list"}),
            (GetParentBranchInput, {}),
            # health
            (HealthCheckInput, {}),
            # issue
            (GetIssueInput, {"issue_number": 1}),
            (ListIssuesInput, {}),
            (UpdateIssueInput, {"issue_number": 1}),
            (CloseIssueInput, {"issue_number": 1}),
            # label
            (ListLabelsInput, {}),
            (CreateLabelInput, {"name": "type:bug", "color": "ff0000"}),
            (DeleteLabelInput, {"name": "bug"}),
            (RemoveLabelsInput, {"issue_number": 1, "labels": ["bug"]}),
            (AddLabelsInput, {"issue_number": 1, "labels": ["bug"]}),
            (DetectLabelDriftInput, {}),
            # milestone
            (ListMilestonesInput, {}),
            (CreateMilestoneInput, {"title": "v1.0"}),
            (CloseMilestoneInput, {"milestone_number": 1}),
            # phase
            (TransitionPhaseInput, {"branch": "feature/1-x", "to_phase": "implementation"}),
            (
                ForcePhaseTransitionInput,
                {
                    "branch": "feature/1-x",
                    "to_phase": "implementation",
                    "skip_reason": "r",
                    "human_approval": "ok",
                },
            ),
            # pr
            (ListPRsInput, {}),
            (MergePRInput, {"pr_number": 1}),
            (SubmitPRInput, {"head": "feature/1-x", "title": "PR", "body": "desc"}),
            # project
            (GetProjectPlanInput, {"issue_number": 1}),
            (
                SavePlanningDeliverablesInput,
                {
                    "issue_number": 1,
                    "planning_deliverables": {"tdd_cycles": {"total": 1}, "cycles": []},
                },
            ),
            (UpdatePlanningDeliverablesInput, {"issue_number": 1, "planning_deliverables": {}}),
            # quality
            (RunQualityGatesInput, {}),
            # scaffold
            (ScaffoldArtifactInput, {"artifact_type": "migration", "name": "test"}),
            # template_validation
            (TemplateValidationInput, {"path": "/tmp/f.py", "template_type": "tool"}),
            # test_tools
            (RunTestsInput, {"path": "tests/"}),
        ],
    )
    def test_extra_field_raises_validation_error(
        self, model_class: type[Any], valid_kwargs: dict[str, Any]
    ) -> None:
        """Extra field raises ValidationError with extra="forbid"."""

        # Valid input should work
        model_class(**valid_kwargs)

        # Extra field must raise
        with pytest.raises(ValidationError) as exc_info:
            model_class(**valid_kwargs, extra_field="should_fail")

        assert (
            "extra_field" in str(exc_info.value).lower() or "extra" in str(exc_info.value).lower()
        )

    def test_safe_edit_nested_extra_forbid(self) -> None:
        """Extra field inside LineEdit / InsertLine also raises."""

        SafeEditInput(
            path="/test.py",
            line_edits=[LineEdit(start_line=1, end_line=1, new_content="x = 1\n")],
        )

        with pytest.raises(ValidationError):
            SafeEditInput(
                path="/test.py",
                line_edits=[
                    {
                        "start_line": 1,
                        "end_line": 1,
                        "new_content": "x = 1\n",
                        "extra_in_nested": "fail",
                    }
                ],
            )

        with pytest.raises(ValidationError):
            SafeEditInput(
                path="/test.py",
                insert_lines=[{"at_line": 1, "content": "x = 1\n", "extra_in_insert": "fail"}],
            )
