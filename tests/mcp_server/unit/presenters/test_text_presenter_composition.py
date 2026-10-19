"""Protected composition, truthful delivery and direct complete attachments."""

import json
from enum import StrEnum

from pydantic import BaseModel

from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.core.operation_notes import Note
from mcp_server.core.tool_execution import SchemaAttachment, WholeToolSchemaIdentity
from mcp_server.presenters.text_presenter import TextPresenter
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ValidationErrorOutput
from tests.mcp_server.test_support import make_config_loader, make_response_presenter


class _Status(StrEnum):
    MISSING = "missing"


class _Item(BaseModel):
    name: str
    tags: tuple[str, ...]


class _Output(BaseModel):
    success: bool = True
    name: str
    labels: tuple[str, ...]
    items: list[_Item]
    status: _Status
    payload: str


def _config(
    *, max_bytes: int = 800, template_success: str = "SCALAR {name}: {labels}"
) -> PresentationConfig:
    source = make_config_loader().load_presentation_config().model_dump(by_alias=True)
    source["global"]["max_text_response_bytes"] = max_bytes
    source["global"]["max_cache_failure_detail_bytes"] = 96
    source["global"]["formatting"]["truncation_notice"] = "[TRUNCATED]"
    source["global"]["formatting"]["cache_unavailable_truncation_notice"] = "[UNAVAILABLE]"
    source["global"]["next_instruction_texts"]["instruction"] = "INSTRUCTION {name}"
    source["global"]["notes"]["groups"]["suggestions"] = {"emoji": "N", "header": "NOTES"}
    source["tools"] = {
        "synthetic_tool": {
            "category": "query",
            "max_items": 2,
            "template_success": template_success,
            "template_failure": "ERROR {error_message}",
            "collections": {
                "items": {
                    "order": 10,
                    "field": "items",
                    "heading": "COLLECTION",
                    "item_template": "- ITEM {name}: {tags}",
                }
            },
            "enum_cases": {
                "status": {"order": 10, "field": "status", "cases": {"missing": "ENUM {name}"}}
            },
            "next_instructions": ["instruction"],
            "suggestions": {"composition_note": "NOTE {value}"},
        }
    }
    return PresentationConfig.model_validate(source)


def _output(*, payload: str = "short") -> _Output:
    return _Output(
        name="sample",
        labels=("bug", "priority", "backend"),
        items=[_Item(name="first", tags=("a", "b", "c")), _Item(name="second", tags=("d",))],
        status=_Status.MISSING,
        payload=payload,
    )


class TestTextPresenterComposition:
    def test_separates_protected_guidance_and_optional_collections(self) -> None:
        config = _config()
        data = _output()
        before = data.model_dump()
        rendered = TextPresenter(config=config).present_text(
            "synthetic_tool",
            data,
            notes=[Note(key="composition_note", params={"value": "present"})],
        )
        positions = [
            rendered.core.index(marker) for marker in ("SCALAR", "ENUM", "INSTRUCTION", "NOTES")
        ]
        assert positions == sorted(positions)
        assert "bug, priority, … 1 more" in rendered.core
        assert "COLLECTION" not in rendered.core
        assert "- ITEM first: a, b, … 1 more" in rendered.details
        assert data.model_dump() == before

    def test_oversized_required_core_survives_budget_and_keeps_cache_reference(self) -> None:
        config = _config(max_bytes=180, template_success="SCALAR {payload}")
        data = _output(payload="🚀" * 300)
        output = make_response_presenter(config).present(
            "synthetic_tool",
            data,
            cache_pub=CachePublication(run_id="b" * 32),
        )
        assert output.text is not None
        assert data.payload in output.text
        assert len(output.text.encode("utf-8")) > 180
        assert output.text.count("pgmcp://cache/runs/" + "b" * 32) == 1
        assert "[TRUNCATED]" in output.text
        assert "�" not in output.text

    def test_resource_failure_bounds_diagnostic_details_and_keeps_required_guidance(self) -> None:
        config = _config(max_bytes=100)
        presenter = make_response_presenter(config, profile_id="structured_resource")
        output = presenter.present(
            "synthetic_tool",
            _output(payload="diagnostic-value " * 200),
            notes=[Note(key="composition_note", params={"value": "required-recovery"})],
            cache_pub=CachePublication(success=False, error_code="write_failed"),
        )
        assert output.text is not None and output.structured_content is not None
        assert "INSTRUCTION sample" in output.text and "required-recovery" in output.text
        assert "pgmcp://cache/runs/" not in output.text
        assert output.structured_content["success"] is True
        assert output.structured_content["data"] is None
        assert output.structured_content["delivery_error"] == {
            "code": "cache_publication_failed",
            "details_truncated": True,
        }
        label = config.global_settings.next_instruction_texts["diagnostic_excerpt_label"]
        if label in output.text:
            assert (
                len(output.text.split(label, 1)[1].encode("utf-8")) + len(label.encode("utf-8"))
                <= 96
            )

    def test_failure_rendering_does_not_require_absent_success_collections(self) -> None:
        rendered = TextPresenter(config=_config()).present_text(
            "synthetic_tool", {"success": False, "error_message": "post hook failed"}, success=False
        )
        assert "ERROR post hook failed" in rendered.core
        assert rendered.details == ""

    def test_direct_schema_and_operation_remain_complete_outside_presentation_budget(self) -> None:
        source = _config(max_bytes=1).model_dump(by_alias=True)
        source["tools"]["synthetic_tool"] = {
            "template_success": "UNUSED",
            "template_failure": "{error_message}",
        }
        config = PresentationConfig.model_validate(source)
        schema = {
            "type": "object",
            "properties": {f"field_{index}": {"type": "string"} for index in range(100)},
        }
        frozen = freeze_json(schema)
        assert isinstance(frozen, FrozenJsonObject)
        data = ValidationErrorOutput(
            error_message="x" * 1000, validation_errors=[], input_schema=schema
        )
        output = make_response_presenter(config).present(
            "synthetic_tool",
            data,
            attachments=(
                SchemaAttachment(
                    identity=WholeToolSchemaIdentity(kind="whole_tool"), schema_document=frozen
                ),
            ),
            cache_pub=CachePublication(run_id="c" * 32),
        )
        assert output.text is not None
        assert data.error_message is not None
        assert data.error_message in output.text
        payload = output.structured_content
        assert payload is not None
        attachments = payload["attachments"]
        assert isinstance(attachments, list) and isinstance(attachments[0], dict)
        assert json.loads(str(attachments[0]["content"])) == schema
        assert data.input_schema == schema
