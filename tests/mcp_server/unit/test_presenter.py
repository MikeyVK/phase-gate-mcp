# tests/mcp_server/unit/test_presenter.py
# template=unit_test version=3d15d309 created=2026-06-12T20:48Z updated=2026-08-19T19:05Z
"""Unit tests for presenter subcomponents: TextPresenter, SchemaResourcePresenter.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.presenters, unittest.mock]
@responsibilities:
    - Test TextPresenter (ITextPresenter) markdown rendering and note grouping
    - Test SchemaResourcePresenter (IResourcePresenter) schema resource generation
    - Test ResponsePresenter (IPresenter) composite coordination
    - Test drift validator validate_presentation_alignment
"""

# Standard library
import json
from typing import Any, ClassVar
from unittest.mock import patch

# Third-party
import pytest
from jsonschema import Draft202012Validator
from pydantic import BaseModel

# Project modules
from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.core.operation_notes import Note, NoteEntry
from mcp_server.core.tool_execution import SchemaAttachment, WholeToolSchemaIdentity
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import (
    SchemaResourcePresenter,
)
from mcp_server.presenters.text_budget_limiter import TextBudgetLimiter
from mcp_server.presenters.text_presenter import (
    TextPresenter,
    validate_presentation_alignment,
)
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ExecutionErrorOutput
from mcp_server.schemas.presentation_output import (
    InlineOperation,
    PresentedOutput,
    PublicToolResponse,
    RenderedPresentation,
)
from mcp_server.schemas.tool_outputs import BaseToolOutput
from tests.mcp_server.test_support import make_config_loader, make_response_presenter


class DummyOutput(BaseToolOutput):
    result: str = ""
    items: list[str] = []


class DummySimpleOutput(BaseToolOutput):
    result: str = ""


class DummyTool:
    name: ClassVar[str] = "dummy_tool"
    output_model: ClassVar[type[BaseModel]] = DummyOutput


class DummyNoOutputModelTool:
    name: ClassVar[str] = "dummy_no_model"
    output_model: ClassVar[type[BaseModel] | None] = None


class TestSchemaResourcePresenter:
    """Resources depend only on explicit immutable attachments."""

    def test_present_resources_whole_tool_schema(self) -> None:
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        frozen = freeze_json(schema)
        assert isinstance(frozen, FrozenJsonObject)
        attachment = SchemaAttachment(
            identity=WholeToolSchemaIdentity(kind="whole_tool"), schema_document=frozen
        )
        resources = SchemaResourcePresenter().present_resources((attachment,))
        assert len(resources) == 1
        assert resources[0].uri == "schema://validation"
        assert resources[0].mime_type == "application/json"
        assert json.loads(resources[0].content) == schema

    def test_present_resources_empty(self) -> None:
        assert SchemaResourcePresenter().present_resources(()) == ()


class TestResponsePresenter:
    """Test suite for ResponsePresenter composite."""

    def test_present_combines_text_and_resources(self) -> None:
        """Verify ResponsePresenter coordinates text and resource delegates."""

        class MockTextPres:
            def present_text(
                self,
                tool_name: str,
                data: BaseModel | dict[str, Any],
                notes: list[NoteEntry] | None = None,
                cache_pub: CachePublication | None = None,
                success: bool | None = None,
            ) -> RenderedPresentation:
                del tool_name, data, notes, cache_pub, success
                return RenderedPresentation(core="Rendered Markdown", details="")

            def present_notes(self, tool_name: str, notes: list[NoteEntry]) -> str | None:
                del tool_name, notes
                return None

        presenter = make_response_presenter(text_presenter=MockTextPres())
        schema = freeze_json({"type": "object"})
        assert isinstance(schema, FrozenJsonObject)
        attachment = SchemaAttachment(
            identity=WholeToolSchemaIdentity(kind="whole_tool"), schema_document=schema
        )
        output = presenter.present(
            tool_name="dummy_tool", data=DummyOutput(result="test"), attachments=(attachment,)
        )

        assert isinstance(output, PresentedOutput)
        assert output.text is not None and output.text.startswith("Rendered Markdown")
        assert output.structured_content is not None
        envelope = PublicToolResponse.model_validate_json(json.dumps(output.structured_content))
        assert envelope.presentation == output.text
        assert isinstance(envelope.data, InlineOperation)
        assert envelope.data.operation["result"] == "test"
        assert len(envelope.attachments) == 1
        assert envelope.attachments[0].uri == "schema://validation"
        assert output.resources[0].content == json.dumps({"type": "object"})


class TestTextPresenter:
    """Test suite for text_presenter."""

    @pytest.fixture
    def mock_yaml_config(self) -> dict[str, Any]:
        overrides = {
            "global": {
                "emojis": {
                    "success": "✅",
                    "failure": "❌",
                    "warning": "⚠️",
                    "query": "📋",
                    "bootstrap": "🚀",
                },
                "default_failure_template": "Failed: {error_message}",
                "formatting": {
                    "none_value": "-",
                    "inline_sequence_separator": ", ",
                    "inline_sequence_omission_template": "… {omitted_count} more",
                    "collection_omission_template": "- … {omitted_count} more {field}",
                    "truncation_notice": "Output truncated.",
                    "cache_unavailable_truncation_notice": "Output unavailable.",
                },
                "next_instruction_texts": {
                    "test_advisory": "🚀 TEST ADVISORY WARNING",
                    "cache_publication_failed": "CACHE FAILURE MARKER",
                    "uri_reference": (
                        "*(Full details available in the structured JSON payload. "
                        "View resource: pgmcp://cache/runs/{run_id})*"
                    ),
                },
                "notes": {
                    "groups": {
                        "suggestions": {"header": "Suggestions", "emoji": "💡"},
                        "recoveries": {"header": "Recovery", "emoji": "🔧"},
                    },
                    "templates": {
                        "suggestions": {"try_this": "Try {action}"},
                    },
                },
            },
            "tools": {
                "dummy_tool": {
                    "template_success": "Success: {result}",
                    "template_failure": "Error: {error_message}",
                    "next_instructions": ["test_advisory"],
                },
                "dummy_no_model": {"template_success": "No model success message"},
            },
        }

        config = make_config_loader().load_presentation_config().model_dump(by_alias=True)
        instructions = config["global"]["next_instruction_texts"] | overrides["global"].pop(
            "next_instruction_texts"
        )
        config["global"].update(overrides["global"])
        config["global"]["next_instruction_texts"] = instructions
        config["tools"] = overrides["tools"]
        return config

    def test_present_text_success(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test presenting success output with custom template and emoji prefix."""
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = DummyOutput(success=True, result="Operation completed")

        text = presenter.present_text(tool_name="dummy_tool", success=True, data=dto)

        assert text.core == "📋 Success: Operation completed\n\n🚀 TEST ADVISORY WARNING"

    @pytest.mark.parametrize("request_params", [{}, {"value": 3}])
    def test_present_text_failure(
        self, mock_yaml_config: dict[str, Any], request_params: dict[str, Any]
    ) -> None:
        """Configured failures project domain facts before conflicting request values."""
        mock_yaml_config["global"]["failures"] = {
            "domain_failure": "Failed: {error_message}; value={value}"
        }
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = ExecutionErrorOutput(
            error_message="Operation failed",
            error_code="domain_failure",
            error_params={"value": "domain fact"},
            params=request_params,
        )

        text = presenter.present_text(tool_name="dummy_tool", success=False, data=dto)

        assert text.core == "❌ Failed: Operation failed; value=domain fact"

    @pytest.mark.parametrize("tool_name", ["dummy_no_model", "dummy_tool"])
    def test_present_text_default_failure_template(
        self, mock_yaml_config: dict[str, Any], tool_name: str
    ) -> None:
        """Test presenting failure using default failure template when no specific one exists."""
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = ExecutionErrorOutput(error_message="Something crashed")

        text = presenter.present_text(tool_name=tool_name, success=False, data=dto)

        assert text.core == "❌ Failed: Something crashed"

    def test_present_text_no_output_model(self, mock_yaml_config: dict[str, Any]) -> None:
        """Test presenting tool with no output model."""
        presenter = TextPresenter(config_data=mock_yaml_config)

        text = presenter.present_text(tool_name="dummy_no_model", success=True, data={})

        assert text.core == "📋 No model success message"

    @pytest.mark.parametrize(
        ("template", "parse_error"),
        [
            ("Try {action}", None),
            ("Try {action", None),
            ("Try {action}", RuntimeError("parser failure")),
        ],
    )
    def test_present_notes_handles_format_syntax(
        self,
        mock_yaml_config: dict[str, Any],
        template: str,
        parse_error: Exception | None,
    ) -> None:
        """Note syntax errors remain visible; unexpected parser faults propagate."""
        mock_yaml_config["global"]["notes"]["templates"]["suggestions"]["try_this"] = template
        presenter = TextPresenter(config_data=mock_yaml_config)
        notes = [Note(key="try_this", params={"action": "re-running the test"})]

        if parse_error is not None:
            with (
                patch(
                    "mcp_server.presenters.text_presenter.SafeNoneFormatter.parse",
                    side_effect=parse_error,
                ),
                pytest.raises(type(parse_error)) as raised,
            ):
                presenter.present_notes("dummy_tool", notes)
            assert raised.value is parse_error
            return

        text = presenter.present_notes("dummy_tool", notes)
        assert text is not None
        assert "💡 Suggestions" in text
        if template == "Try {action":
            assert "Format error:" in text
        else:
            assert "Try re-running the test" in text

    @pytest.mark.parametrize(
        ("location", "values", "expected"),
        [
            ("global", ["first", "second", "third"], "first | second | MORE(1)"),
            ("local", ("first", "second", "third"), "first | second | MORE(1)"),
            ("global", [], "EMPTY"),
        ],
    )
    def test_present_notes_uses_configured_sequence_policy(
        self,
        mock_yaml_config: dict[str, Any],
        location: str,
        values: list[str] | tuple[str, ...],
        expected: str,
    ) -> None:
        """Declared policy controls values without mutating note facts."""
        mock_yaml_config["global"]["formatting"].update(
            none_value="EMPTY",
            inline_sequence_separator=" | ",
            inline_sequence_omission_template="MORE({omitted_count})",
        )
        mock_yaml_config["tools"]["dummy_tool"]["max_items"] = 2
        mock_yaml_config["global"]["notes"]["templates"]["suggestions"]["sequence_probe"] = (
            "GLOBAL {values}"
        )
        if location == "local":
            mock_yaml_config["tools"]["dummy_tool"]["suggestions"] = {
                "sequence_probe": "LOCAL {values}"
            }
        before = list(values)
        note = Note(key="sequence_probe", params={"values": values})
        presenter = TextPresenter(config_data=mock_yaml_config)
        output = presenter.present_notes("dummy_tool", [note])
        assert output is not None
        assert f"{location.upper()} {expected}" in output
        if location == "local":
            assert "GLOBAL" not in output
        assert list(values) == before
        assert note.params["values"] is values

    @pytest.mark.parametrize("invalid", ["missing_limit", "nested_value"])
    def test_present_notes_preserves_real_failure_diagnostics(
        self,
        mock_yaml_config: dict[str, Any],
        caplog: pytest.LogCaptureFixture,
        invalid: str,
    ) -> None:
        """No invented limit or hidden failure replaces the operation or other notes."""
        mock_yaml_config["tools"]["dummy_tool"]["max_items"] = (
            None if invalid == "missing_limit" else 2
        )
        mock_yaml_config["global"]["notes"]["templates"]["suggestions"]["sequence_probe"] = (
            "VALUES {values}"
        )
        values = ["first"] if invalid == "missing_limit" else [{"nested": "value"}]
        operation = DummyOutput(result="ACTUAL_OUTCOME")
        presenter = TextPresenter(config_data=mock_yaml_config)
        rendered = presenter.present_text(
            "dummy_tool",
            operation,
            notes=[
                Note(key="sequence_probe", params={"values": values}),
                Note(key="try_this", params={"action": "SURVIVING_NOTE"}),
            ],
        )
        assert operation.success
        assert "ACTUAL_OUTCOME" in rendered.core
        assert "SURVIVING_NOTE" in rendered.core
        causes = []
        for record in caplog.records:
            if record.exc_info is not None:
                causes.append(record.exc_info[1])
        assert len(causes) == 1
        assert isinstance(causes[0], ConfigError)
        assert str(causes[0]) in rendered.core

    def test_drift_validator_generic_notes_invalid_placeholder(
        self, mock_yaml_config: dict[str, Any]
    ) -> None:
        """Test that validator raises ConfigError when placeholders in
        generic note templates do not align with expected fields.
        """
        mock_yaml_config["global"]["notes"]["templates"]["suggestions"] = {
            "allowed_branch_types": "Allowed: {invalid_field}"
        }
        presenter = TextPresenter(config_data=mock_yaml_config)
        with pytest.raises(ConfigError) as exc_info:
            validate_presentation_alignment(presenter, [])
        assert "placeholder" in str(exc_info.value).lower()

    @pytest.mark.parametrize("format_stage", ["main", "instruction", "note"])
    def test_present_text_formatting_fault_preserves_diagnosis(
        self,
        mock_yaml_config: dict[str, Any],
        caplog: pytest.LogCaptureFixture,
        format_stage: str,
    ) -> None:
        """Formatting faults remain visible with their full logged native diagnosis."""
        notes: list[Note] = []
        if format_stage == "main":
            mock_yaml_config["tools"]["dummy_tool"]["template_success"] = "Success: {result"
        elif format_stage == "instruction":
            mock_yaml_config["global"]["next_instruction_texts"]["test_advisory"] = "Try {action"
        else:
            mock_yaml_config["global"]["notes"]["templates"]["suggestions"]["try_this"] = (
                "Try {action"
            )
            notes = [Note(key="try_this", params={"action": "retry"})]
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = DummyOutput(success=True, result="Formatting outcome")
        text = presenter.present_text(
            tool_name="dummy_tool",
            data=dto,
            notes=notes,
        )
        assert "Format error" in text.core
        records = [
            record
            for record in caplog.records
            if record.name == "mcp_server.presenters.text_presenter"
        ]
        assert len(records) == 1
        assert records[0].exc_info is not None
        assert records[0].exc_info[0] is ValueError
        assert records[0].exc_info[2] is not None

    def test_present_text_dynamic_category_emoji(self, mock_yaml_config: dict[str, Any]) -> None:
        """Verify that custom categories and emojis configured in YAML are resolved dynamically."""
        mock_yaml_config["global"]["emojis"]["custom_cat"] = "🦄"
        mock_yaml_config["tools"]["dummy_tool"]["category"] = "custom_cat"
        presenter = TextPresenter(config_data=mock_yaml_config)
        dto = DummyOutput(success=True, result="Dynamic emoji test")
        text = presenter.present_text(
            tool_name="dummy_tool",
            data=dto,
            notes=[],
        )
        assert "🦄 Success: Dynamic emoji test" in text.core


@pytest.mark.parametrize("mode", ["structured", "resource"])
@pytest.mark.parametrize("cached", [False, True])
def test_compact_recovery_routes_known_facts_without_normal_rendering(
    mode: str,
    cached: bool,
) -> None:
    """Recovery uses known facts and only an existing operation reference."""
    config_data = make_config_loader().load_presentation_config().model_dump(by_alias=True)
    config_data["global"]["response_mode"] = mode
    instructions = config_data["global"]["next_instruction_texts"]
    instructions.update(
        response_processing_failed="KNOWN-OUTCOME={success}",
        recovery_cache_unavailable="NO-EXISTING-REFERENCE",
        uri_reference="EXISTING-REFERENCE={run_id}",
    )
    config_data["global"]["formatting"].update(
        truncation_notice="DETAILS SHORTENED; RESULT AVAILABLE",
        cache_unavailable_truncation_notice="DETAILS SHORTENED; NO CACHED RESULT",
    )
    presenter = make_response_presenter(PresentationConfig.model_validate(config_data))
    run_id = "b" * 32 if cached else None
    with (
        patch.object(TextPresenter, "present_text", side_effect=AssertionError("normal rendering")),
        patch.object(
            SchemaResourcePresenter,
            "present_resources",
            side_effect=AssertionError("attachment conversion"),
        ),
        patch.object(ResponsePresenter, "present", side_effect=AssertionError("normal projection")),
    ):
        output = presenter.recover(
            operation_success=False,
            error_message="native processing failure",
            traceback="traceback diagnostic section\n\n" * 1000,
            cache_run_id=run_id,
            cache_size_chars=1_500_000 if cached else None,
        )
    assert output.text is not None
    assert "KNOWN-OUTCOME=False" in output.text
    assert "native processing failure" in output.text
    assert len(output.text.encode("utf-8")) <= config_data["global"]["max_text_response_bytes"]
    assert (f"EXISTING-REFERENCE={run_id}" if cached else "NO-EXISTING-REFERENCE") in output.text
    formatting = config_data["global"]["formatting"]
    expected_notice = formatting[
        "truncation_notice" if cached else "cache_unavailable_truncation_notice"
    ]
    wrong_notice = formatting[
        "cache_unavailable_truncation_notice" if cached else "truncation_notice"
    ]
    assert expected_notice in output.text
    assert wrong_notice not in output.text
    assert output.resources == ()
    if mode == "resource":
        assert output.structured_content is None
        assert presenter.output_schema() is None
    else:
        assert output.structured_content is not None
        envelope = PublicToolResponse.model_validate_json(json.dumps(output.structured_content))
        assert envelope.success is False
        assert envelope.attachments == ()
        assert envelope.delivery_error is None
        assert envelope.processing_error is not None
        assert envelope.processing_error.error_message is not None
        assert envelope.processing_error.error_message.startswith("native processing failure")
        assert envelope.processing_error.params == {"diagnostic_details_truncated": True}
        assert envelope.data is not None if cached else envelope.data is None
        if cached:
            assert envelope.data is not None
            assert envelope.data.model_dump() == {
                "delivery": "resource",
                "uri": f"pgmcp://cache/runs/{run_id}",
                "size_chars": 1_500_000,
            }
        schema = presenter.output_schema()
        assert schema is not None
        Draft202012Validator(schema).validate(output.structured_content)


@pytest.mark.parametrize("long_message", [False, True])
def test_recovery_bounds_unicode_before_encoding_and_shares_diagnostic_allowance(
    long_message: bool,
) -> None:
    """No full oversized diagnostic string is encoded, copied into output or replayed."""

    class OversizedDiagnostic(str):
        def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
            del encoding, errors
            raise AssertionError("Full diagnostic was encoded before bounding")

    allowance = 29
    config_data = make_config_loader().load_presentation_config().model_dump(by_alias=True)
    config_data["global"]["max_cache_failure_detail_bytes"] = allowance
    config_data["global"]["next_instruction_texts"]["processing_diagnostic_truncated"] = (
        "BOUNDED-DIAGNOSTIC"
    )
    presenter = make_response_presenter(PresentationConfig.model_validate(config_data))
    oversized = OversizedDiagnostic("🙂漢" * 100_000)
    message = oversized if long_message else "short"
    with patch.object(TextBudgetLimiter, "excerpt", wraps=TextBudgetLimiter.excerpt) as excerpts:
        output = presenter.recover(
            operation_success=True,
            error_message=message,
            traceback=oversized,
            cache_run_id=None,
            cache_size_chars=None,
        )

    assert all(len(call.args[0]) <= allowance for call in excerpts.call_args_list)
    assert excerpts.call_count == 2
    assert output.structured_content is not None
    envelope = PublicToolResponse.model_validate_json(json.dumps(output.structured_content))
    assert envelope.success is True
    diagnosis = envelope.processing_error
    assert diagnosis is not None
    byte_count = len((diagnosis.error_message or "").encode("utf-8")) + len(
        (diagnosis.traceback or "").encode("utf-8")
    )
    assert byte_count <= allowance
    assert diagnosis.params == {"diagnostic_details_truncated": True}
    assert envelope.presentation is not None
    assert "BOUNDED-DIAGNOSTIC" in envelope.presentation
    assert len(json.dumps(output.structured_content)) < 2_000
    schema = presenter.output_schema()
    assert schema is not None
    Draft202012Validator(schema).validate(output.structured_content)
