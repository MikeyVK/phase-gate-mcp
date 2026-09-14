"""Verify schema admission and transport without pinning template wording."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from jsonschema import Draft202012Validator
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    CallToolResult,
    EmbeddedResource,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    TextResourceContents,
)
from pydantic import BaseModel, JsonValue

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ValidationErrorOutput
from mcp_server.server import MCPServer
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.project_tools import GetProjectPlanInput
from mcp_server.tools.template_schema_tool import ScaffoldSchemaOutput, ScaffoldSchemaTool
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template


@pytest.fixture
def delivered(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    return load_delivered_template(
        source_suite=suite,
        source_package=suite / "issue",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite",
        template_id="issue",
    )


@dataclass(frozen=True)
class Composition:
    server: MCPServer
    core: ScaffoldSchemaTool
    cache: ResponseCacheManager
    resource: CachedResponseResource
    runner: MagicMock
    text: MagicMock


def compose(root: Path, delivered: DeliveredTemplate) -> Composition:
    identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
    core = ScaffoldSchemaTool(catalog=delivered.catalog, identities=(identity,))
    runner = MagicMock(spec=EnforcementRunner)
    enforcement = EnforcementDecorator(core, runner, root)
    wrapped = ToolErrorHandlerDecorator(
        InputValidationDecorator(enforcement, input_contract=core.input_contract)
    )
    cache = ResponseCacheManager(max_size=1)
    resource = CachedResponseResource(cache)
    text = MagicMock(
        spec=ITextPresenter,
        wraps=TextPresenter(
            config_data={
                "global": {
                    "formatting": {
                        "inline_sequence_omission_template": " ({omitted_count} omitted)",
                        "collection_omission_template": "{omitted_count} omitted",
                        "truncation_notice": "Truncated",
                        "cache_unavailable_truncation_notice": "Truncated without cache",
                    },
                    "next_instruction_texts": {
                        "uri_reference": "pgmcp://cache/runs/{run_id}",
                    },
                },
                "tools": {
                    "scaffold_schema": {
                        "template_success": (
                            "{template_id}: {purpose} ({package_version}, {package_fingerprint})"
                        ),
                    }
                },
            }
        ),
    )
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(root))),
        tools=[wrapped],
        resources=[resource],
        publisher=cache,
        presenter=ResponsePresenter(text, SchemaResourcePresenter()),
    )
    return Composition(server, core, cache, resource, runner, text)


async def listed_schema(composition: Composition) -> dict[str, JsonValue]:
    response = await composition.server.server.request_handlers[ListToolsRequest](
        ListToolsRequest()
    )
    assert isinstance(response.root, ListToolsResult)
    assert len(response.root.tools) == 1
    return response.root.tools[0].inputSchema


async def invoke(
    composition: Composition,
    arguments: dict[str, JsonValue],
) -> tuple[CallToolResult, EmbeddedResource, str]:
    response = await composition.server.server.request_handlers[CallToolRequest](
        CallToolRequest(params=CallToolRequestParams(name="scaffold_schema", arguments=arguments))
    )
    assert isinstance(response.root, CallToolResult)
    assert len(response.root.content) == 2
    resource = response.root.content[1]
    assert isinstance(resource, EmbeddedResource)
    publication = composition.text.present_text.call_args.kwargs["cache_pub"]
    assert isinstance(publication, CachePublication)
    assert publication.run_id is not None
    return response.root, resource, publication.run_id


def resource_schema(resource: EmbeddedResource) -> object:
    assert isinstance(resource.resource, TextResourceContents)
    return json.loads(resource.resource.text)


@pytest.mark.asyncio
async def test_registered_schema_query_transfers_the_complete_catalog_view(
    tmp_path: Path,
    delivered: DeliveredTemplate,
) -> None:
    composition = compose(tmp_path, delivered)
    exposed = await listed_schema(composition)
    raw: dict[str, JsonValue] = {"artifact_type": "issue"}
    assert Draft202012Validator(exposed).is_valid(raw)
    assert (
        exposed
        == composition.core.input_schema
        == thaw_json(composition.core.input_contract.schema)
    )
    response, embedded, run_id = await invoke(composition, raw)
    assert response.isError is False
    assert embedded.resource.mimeType == "application/schema+json"
    assert str(embedded.resource.uri) == "schema://template/issue/context"
    selected = delivered.catalog.get("issue")
    assert resource_schema(embedded) == thaw_json(selected.schema)
    cached = json.loads(await composition.resource.read(f"pgmcp://cache/runs/{run_id}"))
    assert cached["schema_data"] == resource_schema(embedded)
    assert cached["purpose"] == selected.manifest.purpose
    assert cached["template_id"] == selected.manifest.template_id
    assert cached["package_version"] == selected.version
    identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
    assert cached["package_fingerprint"] == identity.pf
    Draft202012Validator(ScaffoldSchemaOutput.model_json_schema()).validate(cached)
    summary = response.content[0]
    assert isinstance(summary, TextContent)
    assert selected.manifest.purpose in summary.text
    assert f"pgmcp://cache/runs/{run_id}" in summary.text
    assert "attachments" not in cached
    assert "sf" not in cached
    operation = composition.cache.get(run_id, ScaffoldSchemaOutput)
    assert operation is not None
    assert operation.schema_data is selected.schema
    direct = await composition.core.execute(
        composition.core.input_contract.validate(raw), NoteContext()
    )
    assert direct.attachments[0].schema is operation.schema_data
    assert [call.kwargs["timing"] for call in composition.runner.run.call_args_list] == [
        "pre",
        "post",
    ]
    # Returned mutable views cannot change subsequent delayed exposure.
    exposed.clear()
    assert await listed_schema(composition) == composition.core.input_schema


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raw",
    [
        {"artifact_type": "retired-package"},
        {"artifact_type": 42},
        {"artifact_type": "issue", "context": {}},
    ],
    ids=["unknown-selection", "strict-type", "unknown-field"],
)
async def test_invalid_envelope_uses_the_exposed_whole_tool_schema(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    raw: dict[str, JsonValue],
) -> None:
    composition = compose(tmp_path, delivered)
    exposed = await listed_schema(composition)
    assert not Draft202012Validator(exposed).is_valid(raw)
    response, embedded, run_id = await invoke(composition, raw)
    assert response.isError is True
    assert str(embedded.resource.uri) == "schema://validation"
    assert resource_schema(embedded) == exposed
    composition.runner.run.assert_not_called()
    operation = composition.cache.get(run_id, ValidationErrorOutput)
    assert operation is not None
    assert operation.params == raw


@pytest.mark.asyncio
async def test_new_composition_changes_current_schema_without_mutating_old_snapshot(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
) -> None:
    first = compose(tmp_path, delivered)
    authored = tmp_path / "suite/opaque package location/context.schema.json"
    changed = json.loads(authored.read_text(encoding="utf-8"))
    changed["maxProperties"] = 99
    authored.write_text(json.dumps(changed), encoding="utf-8")
    restarted = load_delivered_template(
        source_suite=tmp_path / "suite",
        source_package=authored.parent,
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "restarted suite",
        template_id="issue",
    )
    second = compose(tmp_path, restarted)
    raw: dict[str, JsonValue] = {"artifact_type": "issue"}
    _, old_resource, old_run = await invoke(first, raw)
    _, current_resource, _ = await invoke(second, raw)
    assert old_resource.resource.uri == current_resource.resource.uri
    assert resource_schema(old_resource) == thaw_json(delivered.catalog.get("issue").schema)
    assert resource_schema(current_resource) == thaw_json(restarted.catalog.get("issue").schema)
    assert resource_schema(old_resource) != resource_schema(current_resource)
    assert second.cache.get(old_run, BaseModel) is None
    await invoke(first, raw)  # bounded cache evicts the first run
    assert first.cache.get(old_run, BaseModel) is None
    assert resource_schema(old_resource) == thaw_json(delivered.catalog.get("issue").schema)


@pytest.mark.asyncio
async def test_registered_legacy_input_keeps_its_exposed_type_boundary(tmp_path: Path) -> None:
    raw = {"issue_number": "460"}
    assert GetProjectPlanInput.model_validate(raw).issue_number == 460
    core = MagicMock(spec=ICoreTool)
    core.name = "get_project_plan"
    core.description = "Read an existing project plan"
    core.args_model = GetProjectPlanInput
    core.execute = AsyncMock()
    wrapped = ToolErrorHandlerDecorator(InputValidationDecorator(core))
    direct = await wrapped.execute(raw, NoteContext())
    assert isinstance(direct.operation, ValidationErrorOutput)
    core.execute.assert_not_called()
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[],
    )
    response = await server.server.request_handlers[CallToolRequest](
        CallToolRequest(params=CallToolRequestParams(name=core.name, arguments=raw))
    )
    assert isinstance(response.root, CallToolResult)
    assert response.root.isError is True
    core.execute.assert_not_called()
