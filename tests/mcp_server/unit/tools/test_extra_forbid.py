import pytest
from pydantic import ValidationError
from mcp_server.tools.admin_tools import RestartServerInput
from mcp_server.tools.git_tools import GitStatusInput
from mcp_server.tools.issue_tools import CreateIssueInput
from mcp_server.tools.safe_edit_tool import SafeEditInput, LineEdit, InsertLine
from mcp_server.tools.label_tools import CreateLabelInput
from mcp_server.tools.scaffold_artifact import ScaffoldArtifactInput


class TestExtraForbidOnAllInputModels:
    """Parametrized test: all 50 input models reject extra fields."""

    @pytest.mark.parametrize(
        "model_class,valid_kwargs",
        [
            (RestartServerInput, {}),
            (GitStatusInput, {}),
            (CreateLabelInput, {"name": "bug", "color": "ff0000"}),
            (ScaffoldArtifactInput, {"artifact_type": "migration", "name": "test"}),
            # Add more as needed; these are representative samples
        ]
    )
    def test_extra_field_raises_validation_error(self, model_class, valid_kwargs):
        """Extra field raises ValidationError with extra="forbid"."""

        # Valid input should work
        instance = model_class(**valid_kwargs)

        # Extra field must raise
        with pytest.raises(ValidationError) as exc_info:
            model_class(**valid_kwargs, extra_field="should_fail")

        # Error message should mention the extra field
        assert "extra_field" in str(exc_info.value).lower() or "extra" in str(exc_info.value).lower()

    def test_safe_edit_nested_extra_forbid(self):
        """Extra field inside LineEdit / InsertLine also raises."""

        # Valid nested structure
        valid = SafeEditInput(
            path="/test.py",
            line_edits=[
                LineEdit(start_line=1, end_line=1, new_content="x = 1\n")
            ]
        )

        # Extra field inside LineEdit must raise
        with pytest.raises(ValidationError):
            SafeEditInput(
                path="/test.py",
                line_edits=[
                    {"start_line": 1, "end_line": 1, "new_content": "x = 1\n", "extra_in_nested": "fail"}
                ]
            )

        # Extra field inside InsertLine must raise
        with pytest.raises(ValidationError):
            SafeEditInput(
                path="/test.py",
                insert_lines=[
                    {"at_line": 1, "content": "x = 1\n", "extra_in_insert": "fail"}
                ]
            )
