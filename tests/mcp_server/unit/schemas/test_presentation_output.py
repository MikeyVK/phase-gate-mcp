# tests\mcp_server\unit\schemas\test_presentation_output.py
# template=unit_test version=8825c0bb created=2026-08-19T19:00Z updated=2026-08-19T19:05Z
"""
Unit tests for mcp_server.schemas.presentation_output.

Unit tests for PresentationResource and PresentedOutput frozen DTO models.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.schemas.presentation_output]
@responsibilities:
    - Test PresentationResource model creation, defaults, immutability, and extra fields forbidden
    - Test PresentedOutput model creation, defaults, immutability, and extra fields forbidden
"""

import json

import pytest
from pydantic import ValidationError

from mcp_server.schemas.presentation_output import (
    InlineOperation,
    PresentationResource,
    PresentedOutput,
    PublicToolResponse,
    ResourceOperation,
)


class TestPresentationResource:
    """Test suite for PresentationResource DTO."""

    def test_create_resource_defaults(self) -> None:
        """Verify PresentationResource creation with default mime_type."""
        resource = PresentationResource(uri="schema://validation", content='{"type": "object"}')
        assert resource.uri == "schema://validation"
        assert resource.mime_type == "application/json"
        assert resource.content == '{"type": "object"}'

    def test_create_resource_custom_mime_type(self) -> None:
        """Verify PresentationResource creation with custom mime_type."""
        resource = PresentationResource(
            uri="text://info",
            mime_type="text/plain",
            content="Hello",
        )
        assert resource.uri == "text://info"
        assert resource.mime_type == "text/plain"
        assert resource.content == "Hello"

    def test_resource_is_frozen(self) -> None:
        """Verify PresentationResource is immutable."""
        resource = PresentationResource(uri="schema://validation", content="{}")
        with pytest.raises(ValidationError):
            resource.uri = "schema://other"  # type: ignore[misc]

    def test_resource_forbids_extra_fields(self) -> None:
        """Verify PresentationResource forbids extra fields."""
        with pytest.raises(ValidationError):
            PresentationResource(
                uri="schema://validation",
                content="{}",
                unknown_field="invalid",  # type: ignore[call-arg]
            )


class TestPresentedOutput:
    """Test suite for PresentedOutput DTO."""

    def test_output_is_frozen(self) -> None:
        """Verify PresentedOutput is immutable."""
        output = PresentedOutput(text="Test", structured_content=None)
        with pytest.raises(ValidationError):
            output.text = "New text"  # type: ignore[misc]

    def test_output_forbids_extra_fields(self) -> None:
        """Verify PresentedOutput forbids extra fields."""
        with pytest.raises(ValidationError):
            PresentedOutput.model_validate(
                {"text": "Test", "structured_content": None, "extra_prop": "invalid"}
            )


@pytest.mark.parametrize("delivery", ["inline", "resource"])
def test_public_envelope_preserves_data_and_direct_attachments(delivery: str) -> None:
    """The public carrier keeps operation facts distinct from direct schema data."""
    operation = {"success": False, "values": {"zero": 0, "empty": [], "null": None}}
    resource = PresentationResource(uri="schema://validation", content='{"type":"object"}')
    data = (
        InlineOperation(delivery="inline", operation=operation)
        if delivery == "inline"
        else ResourceOperation(
            delivery="resource", uri="pgmcp://cache/runs/" + "a" * 32, size_chars=42
        )
    )
    response = PublicToolResponse(
        success=False,
        presentation="Required instruction",
        data=data,
        attachments=(resource,),
        delivery_error=None,
    )
    payload = json.loads(response.model_dump_json())
    assert payload["success"] is False
    assert payload["presentation"] == response.presentation
    assert payload["attachments"] == [resource.model_dump()]
    if delivery == "inline":
        assert payload["data"]["operation"] == operation
    else:
        assert isinstance(data, ResourceOperation)
        assert payload["data"]["uri"] == data.uri
        assert "operation" not in payload["data"]
