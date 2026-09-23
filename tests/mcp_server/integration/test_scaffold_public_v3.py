"""Observe scaffold facts and recovery schemas through the real public composition."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from unittest.mock import MagicMock

import pytest
from jsonschema import Draft202012Validator
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    CallToolResult,
    EmbeddedResource,
    TextContent,
    TextResourceContents,
)
from pydantic import BaseModel, JsonValue

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.decorators.enforcement_decorator import EnforcementDecorator
from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.ipresenter import ITextPresenter
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.mutation_outputs import ScaffoldOperationOutput
from mcp_server.server import MCPServer
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.scaffold_tool import ScaffoldArtifactTool
from mcp_server.tools.template_schema_tool import ScaffoldSchemaTool
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.test_scaffold_operation_v3 import operation as build_operation


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
    cache_resource: CachedResponseResource
    text: MagicMock


def compose(
    root: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    outcome: str,
) -> Composition:
    service, _ = build_operation(root, delivered, (outcome,))
    identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
    cores = (
        ScaffoldArtifactTool(operation=service, catalog=delivered.catalog),
        ScaffoldSchemaTool(catalog=delivered.catalog, identities=(identity,)),
    )
    runner = MagicMock(spec=EnforcementRunner)
    wrapped = [
        ToolErrorHandlerDecorator(
            InputValidationDecorator(
                EnforcementDecorator(core, runner, root),
                input_contract=core.input_contract,
            )
        )
        for core in cores
    ]
    config = ConfigLoader(pytestconfig.rootpath / ".pgmcp/config").load_presentation_config()
    data = config.model_dump(mode="json", by_alias=True)
    data["tools"] = {
        "scaffold_artifact": {
            "max_items": 5,
            "template_success": (
                "{output_path}: written={written}; policy={validation_policy}; "
                "validation={validation_status}; profile={profile_id}"
            ),
            "template_failure": (
                "{output_path}: written={written}; policy={validation_policy}; "
                "validation={validation_status}; profile={profile_id}; error={error_code}"
            ),
            "collections": [
                {
                    "field": "checks",
                    "heading": "Checks",
                    "item_template": "{check_id}: {status}; args_source={args_source}",
                }
            ],
            "enum_cases": [
                {
                    "field": "error_code",
                    "cases": {
                        "context_invalid": "The selected context was rejected.",
                        "target_invalid": "The requested target was rejected.",
                        "target_exists": "The output already exists.",
                        "render_failed": "Rendering failed.",
                        "preparation_failed": "Mutation preparation failed.",
                        "validation_blocked": "Output checks prevented persistence.",
                        "persistence_failed": "The output could not be saved.",
                        "adapter_request_rejected": "An adapter rejected the check request.",
                        "termination_unconfirmed": "Process termination was not confirmed.",
                        "operation_interrupted": "The operation was interrupted.",
                        "original_unreadable": "The original file could not be read.",
                        "original_changed": "The original file changed.",
                        "original_missing": "The original file is missing.",
                        "edit_invalid": "The requested edit could not be constructed.",
                    },
                }
            ],
        },
        "scaffold_schema": {
            "template_success": "{template_id}: {purpose}",
        },
    }
    text_presenter = TextPresenter(config_data=data)
    validate_presentation_alignment(
        text_presenter,
        tuple(
            SupportedToolContract(name=core.name, output_model=core.output_model) for core in cores
        ),
    )
    text = MagicMock(spec=ITextPresenter, wraps=text_presenter)
    cache = ResponseCacheManager()
    resource = CachedResponseResource(cache)
    server = MCPServer(
        settings=Settings(server=ServerSettings(workspace_root=str(root))),
        tools=wrapped,
        resources=[resource],
        publisher=cache,
        presenter=ResponsePresenter(text, SchemaResourcePresenter()),
    )
    return Composition(server, resource, text)


async def invoke(
    composition: Composition,
    name: str,
    arguments: dict[str, JsonValue],
) -> tuple[CallToolResult, dict[str, JsonValue]]:
    response = await composition.server.server.request_handlers[CallToolRequest](
        CallToolRequest(params=CallToolRequestParams(name=name, arguments=arguments))
    )
    assert isinstance(response.root, CallToolResult)
    call = composition.text.present_text.call_args
    publication = call.kwargs["cache_pub"]
    operation = call.kwargs["data"]
    assert isinstance(publication, CachePublication)
    assert publication.run_id is not None
    assert isinstance(operation, BaseModel)
    cached = json.loads(
        await composition.cache_resource.read(f"pgmcp://cache/runs/{publication.run_id}")
    )
    if isinstance(operation, ScaffoldOperationOutput):
        assert cached == operation.model_dump(mode="json")
    summary = response.root.content[0]
    assert isinstance(summary, TextContent)
    assert f"pgmcp://cache/runs/{publication.run_id}" in summary.text
    return response.root, cached


def schema_resource(response: CallToolResult) -> EmbeddedResource:
    resources = [item for item in response.content if isinstance(item, EmbeddedResource)]
    assert len(resources) == 1
    return resources[0]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("outcome", "policy", "written", "status"),
    [
        ("passed", "enforce", True, "passed"),
        ("failed", "enforce", False, "failed"),
        ("failed", "report", True, "failed"),
    ],
)
async def test_public_scaffold_preserves_validation_and_actual_persistence(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    outcome: str,
    policy: Literal["enforce", "report"],
    written: bool,
    status: str,
) -> None:
    composition = compose(tmp_path, pytestconfig, delivered, outcome)
    response, result = await invoke(
        composition,
        "scaffold_artifact",
        {
            "artifact_type": "issue",
            "file_name": "Exact name.v2.md",
            "target_path": "outputs",
            "force_target": True,
            "context": {"problem": "Caller value", "context": ""},
            "validation": policy,
        },
    )
    assert response.isError is not written
    assert result["success"] is result["written"] is written
    assert result["validation_status"] == status
    assert result["validation_policy"] == policy
    summary = response.content[0]
    assert isinstance(summary, TextContent)
    assert policy in summary.text and status in summary.text
    profile = result["profile_id"]
    assert isinstance(profile, str) and profile in summary.text
    assert result["output_path"] == "outputs/Exact name.v2.md"
    assert (tmp_path / "outputs/Exact name.v2.md").is_file() is written
    assert result["error_code"] == (None if written else "validation_blocked")
    assert result["error_details"] is None
    checks = result["checks"]
    assert isinstance(checks, list) and len(checks) == 1
    row = checks[0]
    assert isinstance(row, dict)
    assert row["status"] == status
    assert row["termination_problem"] is None
    assert row["request_rejection"] is None
    invocation = row["invocation"]
    assert isinstance(invocation, dict)
    capture = invocation["capture"]
    assert isinstance(capture, dict) and "exit_code" in capture
    assert len(response.content) == 1
    assert "schema_data" not in result and "attachments" not in result


@pytest.mark.asyncio
async def test_context_rejection_attaches_the_same_schema_as_discovery(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
) -> None:
    composition = compose(tmp_path, pytestconfig, delivered, "passed")
    rejected, result = await invoke(
        composition,
        "scaffold_artifact",
        {
            "artifact_type": "issue",
            "file_name": "rejected.md",
            "context": {},
        },
    )
    assert rejected.isError is True
    assert result["written"] is False
    assert result["error_code"] == "context_invalid"
    assert result["checks"] == []
    assert not (tmp_path / "outputs/rejected.md").exists()
    details = result["error_details"]
    assert isinstance(details, dict) and details["issues"]
    assert "schema_data" not in result and "attachments" not in result
    queried, _ = await invoke(composition, "scaffold_schema", {"artifact_type": "issue"})
    rejection_schema = schema_resource(rejected).resource
    query_schema = schema_resource(queried).resource
    assert rejection_schema.uri == query_schema.uri
    assert str(rejection_schema.uri) == "schema://template/issue/context"
    assert isinstance(rejection_schema, TextResourceContents)
    assert isinstance(query_schema, TextResourceContents)
    assert json.loads(rejection_schema.text) == json.loads(query_schema.text)
    assert json.loads(query_schema.text) == thaw_json(delivered.catalog.get("issue").schema)


@pytest.mark.asyncio
async def test_creation_fault_retains_passed_checks_and_exact_error_details(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    composition = compose(tmp_path, pytestconfig, delivered, "passed")

    def reject_create(source: object, target: object) -> None:
        del source, target
        raise PermissionError("Creation denied")

    monkeypatch.setattr("mcp_server.utils.atomic_file_writer.os.link", reject_create)
    response, result = await invoke(
        composition,
        "scaffold_artifact",
        {
            "artifact_type": "issue",
            "file_name": "denied.md",
            "context": {"problem": "Caller value", "context": ""},
        },
    )
    assert response.isError is True
    assert result["written"] is False
    assert result["validation_status"] == "passed"
    assert result["error_code"] == "persistence_failed"
    details = result["error_details"]
    assert isinstance(details, dict)
    assert details["stage"] == "create"
    assert details["reason"] == "permission_denied"
    assert details["path"] == result["output_path"]
    assert not (tmp_path / "outputs/denied.md").exists()
    assert len(response.content) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "override",
    [
        {"file_name": "1:invalid.md"},
        {"target_path": "/outside"},
        {"force_target": True},
        {"artifact_type": "unknown"},
    ],
    ids=["basename", "relative-target", "force-needs-target", "unknown-selection"],
)
async def test_malformed_scaffold_input_stops_at_the_public_envelope(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    delivered: DeliveredTemplate,
    override: dict[str, JsonValue],
) -> None:
    composition = compose(tmp_path, pytestconfig, delivered, "passed")
    raw: dict[str, JsonValue] = {
        "artifact_type": "issue",
        "file_name": "rejected.md",
        "context": {"problem": "Caller value", "context": ""},
    }
    raw.update(override)
    schema = composition.server.tools[0].input_schema
    assert not Draft202012Validator(schema).is_valid(raw)
    response, result = await invoke(composition, "scaffold_artifact", raw)
    assert response.isError is True
    assert result["error_type"] == "ValidationError"
    assert result["params"] == raw
    assert result["input_schema"] == schema
    assert str(schema_resource(response).resource.uri) == "schema://validation"
    assert not (tmp_path / "outputs").exists()
