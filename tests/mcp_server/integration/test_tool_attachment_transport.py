# tests\mcp_server\integration\test_tool_attachment_transport.py
# template=integration_test version=c2e61372 created=2026-09-13T18:20Z updated=
"""Exercise attachment ownership at the real execution and MCP boundaries.

@layer: Tests (Integration)
@dependencies: pytest, mcp_server.core, mcp_server.server
"""

import json
import shutil
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import anyio
import pytest
from jsonschema import Draft202012Validator
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import (
    CallToolResult,
    ListToolsResult,
)
from pydantic import BaseModel, ConfigDict

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.core.interfaces.itool_response_cache import IToolResponsePublisher
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import (
    SchemaAttachment,
    TemplateContextSchemaIdentity,
    ToolExecution,
)
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ToolErrorOutput
from mcp_server.schemas.presentation_output import RenderedPresentation
from mcp_server.server import MCPServer
from tests.mcp_server.test_support import connected_mcp_client, make_response_presenter


class Operation(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    success: bool
    value: int


class AttachedCore:
    """Return a supplied execution so preservation can be checked by identity."""

    name = "attached"
    description = "Return operation and independently owned schema"
    args_model = None

    def __init__(self, execution: ToolExecution[BaseModel]) -> None:
        self.execution = execution

    async def execute(self, params: BaseModel, context: NoteContext) -> ToolExecution[BaseModel]:
        del params, context
        return self.execution


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [False, True], ids=["success", "domain-error"])
async def test_carrier_survives_wrappers_and_keeps_schema_out_of_cache_and_text(
    tmp_path: Path, error: bool
) -> None:
    schema = freeze_json({"type": "object", "properties": {"value": {"type": "integer"}}})
    assert isinstance(schema, FrozenJsonObject)
    operation = (
        ToolErrorOutput(error_message="Rejected", error_type="DomainError")
        if error
        else Operation(success=True, value=0)
    )
    execution: ToolExecution[BaseModel] = ToolExecution(
        operation=operation,
        attachments=(
            SchemaAttachment(
                identity=TemplateContextSchemaIdentity(
                    kind="template_context", template_id="order/book"
                ),
                schema_document=schema,
            ),
        ),
    )
    runner = MagicMock(spec=EnforcementRunner)
    wrapped = ToolFactory(runner, tmp_path).create_tool(AttachedCore(execution))
    assert await wrapped.execute({}, NoteContext()) is execution
    assert [call.kwargs["timing"] for call in runner.run.call_args_list] == (
        ["pre"] if error else ["pre", "post"]
    )

    publisher = MagicMock(spec=IToolResponsePublisher)
    publication = CachePublication(run_id="a" * 32)
    publisher.put.return_value = publication
    text = MagicMock(spec=ITextPresenter)

    def present_text(**kwargs: object) -> RenderedPresentation:
        publisher.put.assert_called_once_with("attached", operation)
        assert kwargs["data"] is operation
        assert kwargs["cache_pub"] is publication
        assert "attachments" not in kwargs
        return RenderedPresentation(core="Operation result", details="")

    text.present_text.side_effect = present_text
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        publisher=publisher,
        presenter=make_response_presenter(text_presenter=text),
    )
    async with connected_mcp_client(server) as client:
        response = await client.call_tool("attached", {})
    assert isinstance(response, CallToolResult)
    assert response.is_error is error
    payload = response.structured_content
    assert payload is not None
    assert payload["data"] == {
        "delivery": "inline",
        "operation": operation.model_dump(mode="json", by_alias=True),
    }
    assert len(response.content) == 1
    attachment = payload["attachments"][0]
    assert attachment["uri"] == "schema://template/order%2Fbook/context"
    assert attachment["mime_type"] == "application/schema+json"
    assert json.loads(attachment["content"]) == {
        "type": "object",
        "properties": {"value": {"type": "integer"}},
    }


@pytest.mark.asyncio
async def test_listing_exposes_selected_public_response_schema(tmp_path: Path) -> None:
    execution: ToolExecution[BaseModel] = ToolExecution(
        operation=Operation(success=True, value=1), attachments=()
    )
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        AttachedCore(execution)
    )
    wrapped.output_model = ToolExecution[Operation]
    presenter = make_response_presenter()
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        presenter=presenter,
    )
    async with connected_mcp_client(server) as client:
        listing = await client.list_tools()
    assert isinstance(listing, ListToolsResult)
    assert listing.tools[0].output_schema == presenter.output_schema()


@pytest.mark.asyncio
async def test_v3_stdio_startup_and_handshake(tmp_path: Path, pytestconfig: pytest.Config) -> None:
    """Use the real MCP SDK to verify isolated V3 startup and tool listing."""
    server_directory = ServerSettings().server_root_dir
    source = pytestconfig.rootpath / server_directory
    target = tmp_path / server_directory
    config_root = target / "config"
    template_root = target / "template_suite"
    shutil.copytree(source / "config", config_root)
    shutil.copytree(source / "template_suite", template_root)
    shutil.copyfile(source / ".version", target / ".version")
    (target / "installation.json").write_text(
        json.dumps({"pgmcp_version": Settings().server.version}), encoding="utf-8"
    )
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server"],
        cwd=pytestconfig.rootpath,
        env={
            "PGMCP_WORKSPACE_ROOT": str(tmp_path),
            "PGMCP_CONFIG_ROOT": str(config_root),
            "PGMCP_TEMPLATE_ROOT": str(template_root),
        },
    )
    with anyio.fail_after(30):
        async with stdio_client(parameters) as (read, write), ClientSession(read, write) as client:
            initialized = await client.initialize()
            assert initialized.server_info.name
            listing = await client.list_tools()
            names = {tool.name for tool in listing.tools}
            assert {"health_check", "scaffold_artifact", "get_project_plan"} <= names


@pytest.mark.asyncio
async def test_processing_failure_preserves_diagnosis_and_unknown_tool_result(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A later processing fault cannot replace a known successful operation."""
    failure = RuntimeError("presentation unavailable")
    operation = Operation(success=True, value=1)
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        AttachedCore(ToolExecution(operation=operation, attachments=()))
    )
    presenter = make_response_presenter()
    publisher = MagicMock(spec=IToolResponsePublisher)
    publisher.put.return_value = CachePublication(run_id="b" * 32, size_chars=123)
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        presenter=presenter,
        publisher=publisher,
    )
    with patch.object(presenter, "present", side_effect=failure) as normal:
        async with connected_mcp_client(server) as client:
            listing = await client.list_tools()
            response = await client.call_tool("attached", {})
            missing = await client.call_tool("missing", {})
    assert not response.is_error
    payload = response.structured_content
    assert payload is not None
    assert payload["success"] is True
    assert payload["data"] == {
        "delivery": "resource",
        "uri": "pgmcp://cache/runs/" + "b" * 32,
        "size_chars": 123,
    }
    assert payload["attachments"] == []
    assert "presentation unavailable" in payload["processing_error"]["error_message"]
    schema = listing.tools[0].output_schema
    assert schema is not None
    Draft202012Validator(schema).validate(payload)
    publisher.put.assert_called_once_with("attached", operation)
    normal.assert_called_once()
    assert any(record.exc_info and record.exc_info[1] is failure for record in caplog.records)
    assert missing.is_error
    assert missing.structured_content is None
    assert "missing" in missing.content[0].text
