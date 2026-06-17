# tests/mcp_server/unit/test_presenter.py
# template=unit_test version=3d15d309 created=2026-06-12T20:48Z updated=2026-06-12T21:00Z
"""
Unit tests for mcp_server.presenters.text_presenter.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.presenters.text_presenter, unittest.mock]
@responsibilities:
    - Test TextPresenter functionality
    - Verify presentation.yaml config parsing
    - Test drift validator validate_presentation_alignment
"""

# Standard library
from typing import Any, ClassVar

# Third-party
import pytest
from pydantic import BaseModel

from mcp_server.core.exceptions import ConfigError

# Project modules
from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.schemas.error_outputs import (
    ValidationErrorOutput,
    ExecutionErrorOutput,
    CacheErrorOutput,
    EnforcementErrorOutput,
)
from mcp_server.schemas.tool_outputs import BaseToolOutput


class DummyOutput(BaseToolOutput):
    message: str = ""
    items: list[str] = []


class DummySimpleOutput(BaseToolOutput):
    message: str = ""


class DummyTool:
    name: ClassVar[str] = "dummy_tool"
    presentation_category: ClassVar[str | None] = "query"
    output_model: ClassVar[type[BaseModel]] = DummyOutput


class DummyNoOutputModelTool:
    name: ClassVar[str] = "dummy_no_model"
    presentation_category: ClassVar[str | None] = "mutation"
    output_model: ClassVar[type[BaseModel] | None] = None


class TestTextPresenter:
    """Test suite for text_presenter."""

    @pytest.fixture
    def mock_yaml_config(self) -> dict[str, Any]:
        return {
            "global": {
                "emojis": {
                    "success": "✅",
                    "failure": "❌",
                    "warning": "⚠️",
                    "query": "📋",
                    "bootstrap": "🚀",
                },
                "default_failure_template": "Failed: {error_message}",
                "next_instruction_texts": {
                    "test_advisory": "🚀 TEST ADVISORY WARNING",
                    "uri_reference": (
                        "*(Full details available in the structured JSON payload. "
                        "View resource: pgmcp://cache/runs/{run_id})*"
                    ),
                },
            },
            "tools": {
                "dummy_tool": {
                    "template_success": "Success: {message}",
                    "template_failure": "Error: {error_message}",
                    "next_instructions": ["test_advisory"],
                },
                "dummy_no_model": {"template_success": "No model success message"},
            },
        }

    def test_present_success(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test presenting success output with custom template and emoji prefix."""
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = DummyOutput(success=True, message="Operation completed")

        text = presenter.present(
            tool_name="dummy_tool", success=True, presentation_category="query", data=dto
        )

        # 'query' category maps to '📋' Success maps to '📋' + template + \n\n + next_instructions
        assert text == "📋 Success: Operation completed\n\n🚀 TEST ADVISORY WARNING"

    def test_present_failure_custom(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test presenting failure output with custom template."""
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = DummyOutput(success=False, error_message="Something failed")

        text = presenter.present(
            tool_name="dummy_tool", success=False, presentation_category="query", data=dto
        )

        assert text == "❌ Error: Something failed\n\n🚀 TEST ADVISORY WARNING"

    def test_present_failure_fallback(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test presenting failure output falling back to default template."""
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = DummySimpleOutput(success=False, error_message="Fallback failure")

        text = presenter.present(
            tool_name="dummy_no_model", success=False, presentation_category="mutation", data=dto
        )

        assert text == "❌ Failed: Fallback failure"

    def test_multiple_next_instructions(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test that multiple next instructions are formatted on new lines with blank lines."""
        config = dict(mock_yaml_config)
        config["tools"]["dummy_tool"]["next_instructions"] = ["test_advisory", "uri_reference"]
        presenter = TextPresenter(config_data=config)

        class MockDTO(BaseModel):
            success: bool = True
            message: str = "Op"
            run_id: str = "abc-123"

        dto = MockDTO()
        text = presenter.present(
            tool_name="dummy_tool", success=True, presentation_category="query", data=dto
        )

        expected_text = (
            "📋 Success: Op\n\n"
            "🚀 TEST ADVISORY WARNING\n\n"
            "*(Full details available in the structured JSON payload. View resource: pgmcp://cache/runs/abc-123)*"
        )
        assert text == expected_text

    def test_drift_validator_success(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test that drift validator passes when DTO and template fields align."""
        presenter = TextPresenter(config_data=mock_yaml_config)
        tools = [DummyTool, DummyNoOutputModelTool]

        # Should not raise any exception
        validate_presentation_alignment(presenter, tools)

    def test_drift_validator_drift_detected(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test that drift validator raises ConfigError when template references missing field."""
        corrupt_config = dict(mock_yaml_config)
        corrupt_config["tools"]["dummy_tool"]["template_success"] = "Success: {non_existent_field}"

        presenter = TextPresenter(config_data=corrupt_config)
        tools = [DummyTool]

        with pytest.raises(ConfigError) as exc_info:
            validate_presentation_alignment(presenter, tools)

        assert "non_existent_field" in str(exc_info.value)

    def test_drift_validator_next_instruction_drift_detected(
        self, mock_yaml_config: dict[str, Any]
    ) -> None:
        """Test that drift validator raises ConfigError when next instruction references
        missing field.
        """
        corrupt_config = dict(mock_yaml_config)
        corrupt_config["tools"]["dummy_tool"]["next_instructions"] = ["uri_reference"]
        # Note: DummyTool's output_model is DummyOutput, which has message and
        # items, but lacks run_id! So uri_reference (which uses {run_id}) should fail validation.

        presenter = TextPresenter(config_data=corrupt_config)
        tools = [DummyTool]

        with pytest.raises(ConfigError) as exc_info:
            validate_presentation_alignment(presenter, tools)

        assert "run_id" in str(exc_info.value)

    def test_presentation_config_schema_extended(self) -> None:
        """Test that PresentationConfig schema correctly parses extended configuration fields."""
        extended_data = {
            "global": {
                "emojis": {
                    "success": "✅",
                    "failure": "❌",
                    "warning": "⚠️",
                    "query": "📋",
                    "bootstrap": "🚀",
                },
                "default_failure_template": "Failed: {error_message}",
                "formatting": {"none_value": "-"},
                "notes": {
                    "groups": {
                        "exclusions": {"emoji": "🩹", "header": "Exclusions"},
                        "suggestions": {"emoji": "💡", "header": "Suggestions"},
                    },
                    "templates": {"exclusions": {"default": "Excluded: {file}"}},
                },
                "failures": {"dirty_workdir": "Dirty: {branch}"},
            },
            "tools": {
                "dummy_tool": {
                    "template_success": "Success",
                    "exclusions": {"dirty": "Excluded {file}"},
                }
            },
        }
        config = PresentationConfig.model_validate(extended_data)
        assert config.global_settings.formatting.none_value == "-"
        assert config.global_settings.notes.groups["exclusions"].emoji == "🩹"
        assert config.global_settings.failures["dirty_workdir"] == "Dirty: {branch}"
        assert config.tools["dummy_tool"].exclusions["dirty"] == "Excluded {file}"

    def test_error_dto_compilation_and_enforcement(self) -> None:
        """Test that error DTO subclasses compile and enforce frozen and forbid-extra rules."""
        # Test ValidationErrorOutput
        val_err = ValidationErrorOutput(
            message="Validation failed",
            params={"param1": "val1"},
            validation_errors=[{"loc": ["field"], "msg": "invalid"}],
            input_schema={"type": "object"},
        )
        assert val_err.success is False
        assert val_err.error_type == "ValidationError"
        assert val_err.params == {"param1": "val1"}

        # Verify frozen
        with pytest.raises(Exception):
            val_err.message = "new message"  # type: ignore

        # Verify extra forbid
        with pytest.raises(Exception):
            ValidationErrorOutput(
                message="Err",
                params={},
                validation_errors=[],
                input_schema={},
                invalid_extra_field="fail",  # type: ignore
            )

        # Test EnforcementErrorOutput
        enf_err = EnforcementErrorOutput(
            message="Enforcement blocked", params={"rule": "no-push"}, error_code="RULE_VIOLATION"
        )
        assert enf_err.success is False
        assert enf_err.error_type == "EnforcementError"
        assert enf_err.error_code == "RULE_VIOLATION"

        # Verify ExecutionErrorOutput compile
        exec_err = ExecutionErrorOutput(message="Fail", params={})
        assert exec_err.error_type == "ExecutionError"

        # Verify CacheErrorOutput compile
        cache_err = CacheErrorOutput(message="Disk full", params={})
        assert cache_err.error_type == "CacheError"
