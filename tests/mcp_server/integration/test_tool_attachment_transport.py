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
from mcp.shared.exceptions import MCPError as ProtocolError
from mcp.types import (
    CallToolResult,
    ListToolsResult,
)
from pydantic import BaseModel, ConfigDict, model_serializer

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.core.interfaces.itool_response_cache import IToolResponsePublisher
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.core.tool_execution import (
    SchemaAttachment,
    TemplateContextSchemaIdentity,
    ToolExecution,
)
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.startup_recovery_presenter import StartupRecoveryPresenter
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
@pytest.mark.parametrize("profile_id", ["structured_inline", "structured_resource", "text_inline"])
@pytest.mark.parametrize("operation_success", [True, False], ids=["success", "operation-failure"])
@pytest.mark.parametrize("cache_available", [True, False], ids=["cached", "uncached"])
async def test_processing_failure_preserves_diagnosis_and_unknown_tool_result(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    profile_id: str,
    operation_success: bool,
    cache_available: bool,
) -> None:
    """The SDK receives the known outcome and a schema-valid compact recovery."""
    failure = RuntimeError("presentation unavailable")
    operation = Operation(success=operation_success, value=1)
    core = AttachedCore(ToolExecution(operation=operation, attachments=()))
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(core)
    presenter = make_response_presenter(profile_id=profile_id)
    publisher = MagicMock(spec=IToolResponsePublisher)
    publisher.put.return_value = (
        CachePublication(run_id="b" * 32, size_chars=123)
        if cache_available
        else CachePublication(success=False, error_code="cache_write_failed")
    )
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        presenter=presenter,
        publisher=publisher,
    )
    with (
        patch.object(presenter, "present", side_effect=failure) as normal,
        patch.object(core, "execute", wraps=core.execute) as execute,
    ):
        async with connected_mcp_client(server) as client:
            listing = await client.list_tools()
            response = await client.call_tool("attached", {})
            missing = await client.call_tool("missing", {})
    assert response.is_error is not operation_success
    schema = listing.tools[0].output_schema
    if profile_id == "text_inline":
        assert response.structured_content is None
        assert schema is None
        payload = json.loads(response.content[0].text.split("```json\n", 1)[1].split("\n```", 1)[0])
    else:
        payload = response.structured_content
        assert payload is not None
        assert schema is not None
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        if not cache_available:
            missing_marker = dict(payload)
            missing_marker.pop("processing_error")
            assert not validator.is_valid(missing_marker)
    assert payload["success"] is operation_success
    assert payload["data"] == (
        {"delivery": "resource", "uri": "pgmcp://cache/runs/" + "b" * 32, "size_chars": 123}
        if cache_available
        else None
    )
    assert payload["attachments"] == []
    assert payload["delivery_error"] is None
    assert "presentation unavailable" in payload["processing_error"]["error_message"]
    publisher.put.assert_called_once_with("attached", operation)
    execute.assert_awaited_once()
    normal.assert_called_once()
    assert any(record.exc_info and record.exc_info[1] is failure for record in caplog.records)
    assert missing.is_error
    assert missing.structured_content is None
    assert "missing" in missing.content[0].text


@pytest.mark.asyncio
async def test_processing_recovery_does_not_replay_large_poisoned_inputs(tmp_path: Path) -> None:
    """Increasing original inputs cannot grow or break the compact result."""
    attempts: list[int] = []

    class PoisonedOperation(BaseModel):
        model_config = ConfigDict(frozen=True)
        success: bool = True
        body: str

        @model_serializer
        def serialize(self) -> dict[str, object]:
            attempts.append(len(self.body))
            raise RuntimeError("operation serialization unavailable")

    response_sizes = []
    for size in (100, 1_000_000):
        operation = PoisonedOperation(body="PAYLOAD" * size)
        schema = freeze_json({"description": "ATTACHMENT" * size})
        assert isinstance(schema, FrozenJsonObject)
        execution = ToolExecution(
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
        core = AttachedCore(execution)

        async def execute(
            params: BaseModel,
            context: NoteContext,
            *,
            body: str = operation.body,
            result: ToolExecution[BaseModel] = execution,
        ) -> ToolExecution[BaseModel]:
            del params
            context.produce(Note(key="large", params={"body": body}))
            return result

        text = MagicMock(spec=ITextPresenter)

        def convert_for_text(**kwargs: object) -> RenderedPresentation:
            data = kwargs["data"]
            assert isinstance(data, BaseModel)
            data.model_dump(mode="json")
            raise AssertionError("Poisoned conversion unexpectedly succeeded")

        text.present_text.side_effect = convert_for_text
        presenter = make_response_presenter(text_presenter=text)
        with patch.object(core, "execute", side_effect=execute) as call:
            wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(core)
            server = MCPServer(
                settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
                tools=[wrapped],
                resources=[],
                presenter=presenter,
            )
            async with connected_mcp_client(server) as client:
                response = await client.call_tool("attached", {})
        assert not response.is_error
        payload = response.structured_content
        assert payload is not None
        assert payload["data"] is None
        assert payload["attachments"] == []
        assert "serialization unavailable" in payload["processing_error"]["error_message"]
        assert "PAYLOAD" not in json.dumps(payload)
        assert "ATTACHMENT" not in json.dumps(payload)
        response_sizes.append(len(response.model_dump_json()))
        call.assert_awaited_once()
        text.present_text.assert_called_once()
    assert attempts == [700, 7_000_000]
    assert max(response_sizes) - min(response_sizes) < 100
    assert max(response_sizes) < 20_000


@pytest.mark.asyncio
async def test_secondary_recovery_failure_is_terminal_and_logged(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """The existing SDK boundary terminates a failed single recovery attempt."""
    primary = RuntimeError("primary presentation failed")
    secondary = RuntimeError("compact recovery failed")
    core = AttachedCore(ToolExecution(operation=Operation(success=True, value=1), attachments=()))
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(core)
    presenter = make_response_presenter()
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        presenter=presenter,
    )
    with (
        patch.object(presenter, "present", side_effect=primary) as normal,
        patch.object(presenter, "recover", side_effect=secondary) as recovery,
        patch.object(core, "execute", wraps=core.execute) as execute,
    ):
        async with connected_mcp_client(server) as client:
            with pytest.raises(ProtocolError, match="compact recovery failed"):
                await client.call_tool("attached", {})
    normal.assert_called_once()
    recovery.assert_called_once()
    execute.assert_awaited_once()
    errors = [record for record in caplog.records if record.exc_info]
    assert any(record.exc_info and record.exc_info[1] is primary for record in errors)
    assert any(record.exc_info and record.exc_info[1] is secondary for record in errors)
    assert any(getattr(record, "props", {}).get("operation_success") is True for record in errors)


@pytest.mark.asyncio
@pytest.mark.parametrize("operation_success", [True, False])
async def test_startup_presenter_processing_recovery_uses_fixed_compact_channels(
    tmp_path: Path, operation_success: bool
) -> None:
    """Rejected configuration does not prevent compact post-operation diagnosis."""
    core = AttachedCore(
        ToolExecution(operation=Operation(success=operation_success, value=1), attachments=())
    )
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(core)
    presenter = StartupRecoveryPresenter(SchemaResourcePresenter())
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
        presenter=presenter,
    )
    with patch.object(presenter, "present", side_effect=RuntimeError("startup presentation")):
        async with connected_mcp_client(server) as client:
            listing = await client.list_tools()
            response = await client.call_tool("attached", {})
    assert response.is_error is not operation_success
    payload = response.structured_content
    assert payload is not None
    assert payload["success"] is operation_success
    assert payload["data"] is None
    assert payload["attachments"] == []
    assert payload["processing_error"]["error_message"]
    assert response.content[0].text == payload["presentation"]
    schema = listing.tools[0].output_schema
    assert schema is not None
    Draft202012Validator(schema).validate(payload)
