# tests\mcp_server\unit\core\interfaces\test_presenter_interfaces.py
# template=unit_test version=8825c0bb created=2026-08-19T19:00Z updated=2026-08-19T19:05Z
"""
Unit tests for mcp_server.core.interfaces.ipresenter.

Unit tests for ITextPresenter, IResourcePresenter, and IPresenter protocols.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.core.interfaces.ipresenter]
@responsibilities:
    - Test ITextPresenter runtime_checkable protocol compliance
    - Test IResourcePresenter runtime_checkable protocol compliance
    - Test IPresenter runtime_checkable protocol compliance
"""

from typing import Any

from pydantic import BaseModel, JsonValue

from mcp_server.core.interfaces.ipresenter import IPresenter, IResourcePresenter, ITextPresenter
from mcp_server.core.operation_notes import NoteEntry
from mcp_server.core.tool_execution import SchemaAttachment
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.presentation_output import (
    PresentationResource,
    PresentedOutput,
    RenderedPresentation,
)


class MockTextPresenter:
    """Valid implementation of ITextPresenter."""

    def present_text(
        self,
        tool_name: str,
        data: BaseModel | dict[str, Any],
        notes: list[NoteEntry] | None = None,
        cache_pub: CachePublication | None = None,
        success: bool | None = None,
    ) -> RenderedPresentation:
        del tool_name, data, notes, cache_pub, success
        return RenderedPresentation(core="text", details="")

    def present_notes(
        self,
        tool_name: str,
        notes: list[NoteEntry],
    ) -> str | None:
        del tool_name, notes
        return "notes"


class MockResourcePresenter:
    """Valid implementation of IResourcePresenter."""

    def present_resources(
        self,
        attachments: tuple[SchemaAttachment, ...],
    ) -> tuple[PresentationResource, ...]:
        del attachments
        return (PresentationResource(uri="schema://validation", content="{}"),)


class MockPresenter:
    """Valid implementation of IPresenter."""

    def present(
        self,
        tool_name: str,
        data: BaseModel | dict[str, Any],
        notes: list[NoteEntry] | None = None,
        cache_pub: CachePublication | None = None,
        success: bool | None = None,
        *,
        attachments: tuple[SchemaAttachment, ...] = (),
    ) -> PresentedOutput:
        del tool_name, data, notes, cache_pub, success, attachments
        return PresentedOutput(text="ok", structured_content=None)

    def recover(
        self,
        *,
        operation_success: bool,
        error_message: str,
        traceback: str | None,
        cache_run_id: str | None,
        cache_size_chars: int | None,
    ) -> PresentedOutput:
        del operation_success, traceback, cache_run_id, cache_size_chars
        return PresentedOutput(text=error_message, structured_content=None)

    def output_schema(self) -> dict[str, JsonValue] | None:
        return None


class IncompletePresenter:
    """Invalid presenter missing required methods."""

    pass


class TestPresenterInterfaces:
    """Test suite for presenter interface protocols."""

    def test_text_presenter_protocol(self) -> None:
        """Verify isinstance check on ITextPresenter."""
        mock = MockTextPresenter()
        assert isinstance(mock, ITextPresenter)
        assert not isinstance(IncompletePresenter(), ITextPresenter)

    def test_resource_presenter_protocol(self) -> None:
        """Verify isinstance check on IResourcePresenter."""
        mock = MockResourcePresenter()
        assert isinstance(mock, IResourcePresenter)
        assert not isinstance(IncompletePresenter(), IResourcePresenter)

    def test_presenter_protocol(self) -> None:
        """Verify isinstance check on IPresenter."""
        mock = MockPresenter()
        assert isinstance(mock, IPresenter)
        assert not isinstance(IncompletePresenter(), IPresenter)
