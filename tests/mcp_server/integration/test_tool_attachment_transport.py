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
from unittest.mock import MagicMock

import anyio
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    CallToolResult,
    EmbeddedResource,
    ListToolsRequest,
    ListToolsResult,
    TextResourceContents,
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
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ToolErrorOutput
from mcp_server.server import MCPServer


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
                schema=schema,
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

    def present_text(**kwargs: object) -> str:
        publisher.put.assert_called_once_with("attached", operation)
        assert kwargs["data"] is operation
        assert kwargs["cache_pub"] is publication
        assert "attachments" not in kwargs
        return "Operation result"

    text.present_text.side_effect = present_text
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        publisher=publisher,
        presenter=ResponsePresenter(text, SchemaResourcePresenter()),
    )
    response = await server.server.request_handlers[CallToolRequest](
        CallToolRequest(params=CallToolRequestParams(name="attached", arguments={}))
    )
    assert isinstance(response.root, CallToolResult)
    assert response.root.isError is error
    assert len(response.root.content) == 2
    resource = response.root.content[1]
    assert isinstance(resource, EmbeddedResource)
    assert str(resource.resource.uri) == "schema://template/order%2Fbook/context"
    assert resource.resource.mimeType == "application/schema+json"
    assert isinstance(resource.resource, TextResourceContents)
    assert json.loads(resource.resource.text) == {
        "type": "object",
        "properties": {"value": {"type": "integer"}},
    }


@pytest.mark.asyncio
async def test_listing_exposes_operation_schema_only(tmp_path: Path) -> None:
    execution: ToolExecution[BaseModel] = ToolExecution(
        operation=Operation(success=True, value=1), attachments=()
    )
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        AttachedCore(execution)
    )
    wrapped.output_model = ToolExecution[Operation]
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
    )
    listing = await server.server.request_handlers[ListToolsRequest](ListToolsRequest())
    assert isinstance(listing.root, ListToolsResult)
    assert listing.root.tools[0].outputSchema == Operation.model_json_schema()


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
            assert initialized.serverInfo.name
            listing = await client.list_tools()
            names = {tool.name for tool in listing.tools}
            assert {"health_check", "scaffold_artifact", "get_project_plan"} <= names
