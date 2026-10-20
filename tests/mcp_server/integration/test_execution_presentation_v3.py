# tests\mcp_server\integration\test_execution_presentation_v3.py
# template=integration_test version=c2e61372 created=2026-09-13T18:55Z updated=
"""Exercise generic projection admission and shipped cache guidance.

@layer: Tests (Integration)
@dependencies: pydantic, mcp, TextPresenter, ToolFactory, CachedResponseResource
"""

import re
from enum import StrEnum
from pathlib import Path
from typing import Literal, cast
from unittest.mock import MagicMock

import pytest
from mcp.types import (
    CallToolResult,
    ReadResourceResult,
    TextContent,
    TextResourceContents,
)
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.presentation_config import PresentationConfig, ToolPresentationConfig
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.git import CycleEvidence, ICycleEvidenceReader
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.itool_response_cache import IToolResponsePublisher
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource, CacheReadGuideResource
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.deliverables import (
    CycleInput, CyclesInput, DeliverableInput, SavePlanningModel, StoredPlanningModel,
)
from mcp_server.schemas.tool_outputs import ProjectPlanOutput
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.project_tools import GetProjectPlanTool, UpdatePlanningDeliverablesTool
from tests.mcp_server.test_support import (
    connected_mcp_client, make_config_loader, make_project_manager, make_response_presenter,
)


class Status(StrEnum):
    COMPLETE = "complete"
    UNKNOWN = "None"


class Row(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    label: StrictStr
    args: tuple[StrictStr, ...] | None


class Projection(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    success: bool
    title: StrictStr
    count: StrictInt | Literal["unknown"] | None
    labels: tuple[StrictStr, ...] | None
    status: Status | None
    rows: tuple[Row, ...]
    detail: Row | str


class CollectionProjection(BaseModel):
    """Use an independent concrete shape for collection admission."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    labels: tuple[StrictStr, ...]
    rows: tuple[Row, ...]
    status: Status
    detail: Row | str


class ProjectionCore:
    name = "projection"
    description = "Return a typed projection"
    args_model = None

    def __init__(self, operation: Projection) -> None:
        self.operation = operation

    async def execute(self, params: BaseModel, context: NoteContext) -> Projection:
        del params, context
        return self.operation


@pytest.fixture
def config(pytestconfig: pytest.Config) -> PresentationConfig:
    root = pytestconfig.rootpath / ServerSettings().server_root_dir
    return ConfigLoader(config_root=root / "config").load_presentation_config()


def _presenter(config: PresentationConfig, tool: ToolPresentationConfig) -> TextPresenter:
    return TextPresenter(
        config=PresentationConfig.model_validate(
            {
                "global": config.global_settings,
                "response_profiles": config.response_profiles,
                "tools": {"projection": tool},
            }
        )
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("nullable", [False, True], ids=["values", "nulls"])
async def test_strict_nullable_rows_survive_presentation_and_cache(
    config: PresentationConfig,
    tmp_path: Path,
    nullable: bool,
) -> None:
    presenter = _presenter(
        config,
        ToolPresentationConfig.model_validate(
            {
                "template_success": "{title}: {count}; {labels}",
                "max_items": 1,
                "collections": {
                    "entry_1": {"order": 10, "field": "rows", "item_template": "{label}: {args}"}
                },
                "enum_cases": {
                    "entry_1": {
                        "order": 10,
                        "field": "status",
                        "cases": {"complete": "COMPLETE", "None": "UNKNOWN"},
                    }
                },
            }
        ),
    )
    validate_presentation_alignment(
        presenter, [SupportedToolContract(name="projection", output_model=Projection)]
    )
    operation = Projection(
        success=True,
        title="Result",
        count=None if nullable else 0,
        labels=None if nullable else ("first", "second"),
        status=None if nullable else Status.COMPLETE,
        rows=(Row(label="row-one", args=None if nullable else ("a", "b")),),
        detail="cache-only",
    )
    cache = ResponseCacheManager()
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        ProjectionCore(operation)
    )
    server = MCPServer(
        Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[CachedResponseResource(cache)],
        publisher=cache,
        presenter=make_response_presenter(config, text_presenter=presenter),
    )
    async with connected_mcp_client(server) as client:
        response = await client.call_tool("projection", {})
    assert isinstance(response, CallToolResult)
    assert not response.is_error
    text = "\n".join(item.text for item in response.content if isinstance(item, TextContent))
    assert "row-one:" in text and "cache-only" not in text
    assert "UNKNOWN" not in text
    assert ("COMPLETE" in text) is (not nullable)
    assert ("Result: -" if nullable else "Result: 0") in text
    match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", text)
    assert match is not None
    async with connected_mcp_client(server) as client:
        readback = await client.read_resource(match.group())
    assert isinstance(readback, ReadResourceResult)
    content = readback.contents[0]
    assert isinstance(content, TextResourceContents)
    assert Projection.model_validate_json(content.text) == operation


@pytest.mark.parametrize(
    ("tool_config", "diagnosis"),
    [
        [{"template_success": "{detail}"}, "structured|unsupported"],
        [{"template_success": "{"}, "Invalid template format"],
        [
            {
                "collections": {
                    "items": {"order": 10, "field": "labels", "item_template": "{label}"}
                }
            },
            "may reference only",
        ],
        [
            {"collections": {"items": {"order": 10, "field": "absent", "item_template": "{item}"}}},
            "not present",
        ],
        [
            {
                "collections": {
                    "items": {"order": 10, "field": "rows.args", "item_template": "{item}"}
                }
            },
            "direct field",
        ],
        [
            {
                "enum_cases": {
                    "state": {"order": 10, "field": "absent", "cases": {"complete": "Complete"}}
                }
            },
            "not present",
        ],
        [
            {
                "enum_cases": {
                    "state": {
                        "order": 10,
                        "field": "status.value",
                        "cases": {"complete": "Complete"},
                    }
                }
            },
            "direct field",
        ],
        [
            {
                "enum_cases": {
                    "state": {"order": 10, "field": "status", "cases": {"unexpected": "Unexpected"}}
                }
            },
            "invalid case value",
        ],
    ],
)
def test_alignment_rejects_invalid_typed_projections(
    config: PresentationConfig, tool_config: dict[str, object], diagnosis: str
) -> None:
    presenter = _presenter(config, ToolPresentationConfig.model_validate(tool_config))
    with pytest.raises(ConfigError, match=diagnosis):
        validate_presentation_alignment(
            presenter, [SupportedToolContract(name="projection", output_model=CollectionProjection)]
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("length", "cache_failure", "operation_success"),
    [
        pytest.param(8, False, True, id="published-small"),
        pytest.param(20_000, False, True, id="published-large"),
        pytest.param(8, True, True, id="unpublished-small"),
        pytest.param(20_000, True, True, id="unpublished-large"),
        pytest.param(20_000, True, False, id="unpublished-error"),
    ],
)
async def test_shipped_cache_delivery_preserves_operation(
    config: PresentationConfig,
    length: int,
    cache_failure: bool,
    operation_success: bool,
    tmp_path: Path,
) -> None:
    """Preserve operation facts while selecting truthful configured cache guidance."""
    presenter = _presenter(config, ToolPresentationConfig(template_success="{title}"))
    operation = Projection(
        success=operation_success,
        title="Brief summary",
        count=0,
        labels=None,
        status=None,
        rows=(),
        detail="diagnostic-" + "x" * length,
    )
    cache = ResponseCacheManager()
    publisher: IToolResponsePublisher = cache
    if cache_failure:
        failed_publisher = MagicMock(spec=IToolResponsePublisher)
        failed_publisher.put.return_value = CachePublication(
            success=False, error_code="write_failed"
        )
        publisher = failed_publisher
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        ProjectionCore(operation)
    )
    server = MCPServer(
        Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[CachedResponseResource(cache), CacheReadGuideResource()],
        publisher=publisher,
        presenter=make_response_presenter(config, text_presenter=presenter),
    )
    async with connected_mcp_client(server) as client:
        response = await client.call_tool("projection", {})
        assert isinstance(response, CallToolResult)
        assert response.is_error is (not operation_success)
        assert response.structured_content is not None
        assert response.structured_content["data"]["operation"] == operation.model_dump(
            mode="json", by_alias=True
        )
        text = "\n".join(item.text for item in response.content if isinstance(item, TextContent))
        assert len(text.encode("utf-8")) <= config.global_settings.max_text_response_bytes
        match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", text)
        guide_uri = CacheReadGuideResource.uri_pattern
        if cache_failure:
            assert match is None
            assert guide_uri not in text
            notices = config.global_settings.next_instruction_texts
            assert notices["cache_publication_failed"] in text
            assert response.structured_content["delivery_error"] is None
            return

        assert match is not None
        readback = await client.read_resource(match.group())
        assert isinstance(readback, ReadResourceResult)
        content = readback.contents[0]
        assert isinstance(content, TextResourceContents)
        assert Projection.model_validate_json(content.text) == operation
        paged = len(content.text) > config.global_settings.cache_read_budget_chars
        assert (guide_uri in text) is paged
        assert len(text) < 200
        if paged:
            guide = await client.read_resource(guide_uri)
            assert isinstance(guide, ReadResourceResult)
            assert isinstance(guide.contents[0], TextResourceContents)
            assert guide.contents[0].text == (
                Path(__file__).parents[3] / "mcp_server/resources/cache_reading.md"
            ).read_text(encoding="utf-8")


@pytest.mark.parametrize("names", [(), ("missing",), ("projection", "projection")])
def test_alignment_rejects_catalog_identity_drift(
    config: PresentationConfig, names: tuple[str, ...]
) -> None:
    presenter = _presenter(config, ToolPresentationConfig(template_success="{title}"))
    contracts = [SupportedToolContract(name=name, output_model=Projection) for name in names]
    with pytest.raises(ConfigError):
        validate_presentation_alignment(presenter, contracts)


@pytest.mark.parametrize("location", ["failure", "note"])
def test_alignment_rejects_unsupported_diagnostic_placeholders(
    config: PresentationConfig, location: str
) -> None:
    global_settings = config.global_settings.model_dump(mode="python")
    if location == "failure":
        global_settings["failures"]["ERR_SYSTEM"] = "{unknown_fact}"
    else:
        global_settings["notes"]["templates"]["recoveries"]["transition_conflict_recovery"] = (
            "{unknown_fact}"
        )
    policy = PresentationConfig.model_validate(
        {
            "global": global_settings,
            "response_profiles": config.response_profiles,
            "tools": {"projection": {"template_success": "{title}"}},
        }
    )
    with pytest.raises(ConfigError, match="placeholder"):
        validate_presentation_alignment(
            TextPresenter(config=policy),
            [SupportedToolContract(name="projection", output_model=Projection)],
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("presentation_channel", "data_channel", "delivery"),
    [
        ("both", "structured", "inline"),
        ("both", "structured", "resource"),
        ("text", "text", "inline"),
        ("structured", "text", "inline"),
        ("structured", "structured", "inline"),
        ("text", "structured", "resource"),
        ("both", "text", "resource"),
    ],
)
async def test_selected_profiles_preserve_guidance_and_complete_output(
    config: PresentationConfig,
    tmp_path: Path,
    presentation_channel: str,
    data_channel: str,
    delivery: str,
) -> None:
    """Real SDK consumers receive exactly the selected projections and full data."""
    import json  # noqa: PLC0415
    from uuid import uuid4  # noqa: PLC0415

    from jsonschema import Draft202012Validator  # noqa: PLC0415

    raw = config.model_dump(by_alias=True)
    marker = "required-guidance-" + uuid4().hex
    raw["global"]["next_instruction_texts"]["probe_instruction"] = marker
    raw["global"]["default_response_profile"] = "probe"
    raw["response_profiles"]["probe"] = {
        "presentation_channel": presentation_channel,
        "data_channel": data_channel,
        "data_delivery": delivery,
    }
    raw["tools"] = {
        "projection": {"template_success": "{title}", "next_instructions": ["probe_instruction"]}
    }
    policy = PresentationConfig.model_validate(raw)
    operation = Projection(
        success=True,
        title="Operation summary",
        count=0,
        labels=None,
        status=None,
        rows=(),
        detail="complete-data-" + "x" * 20_000,
    )
    cache = ResponseCacheManager()
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        ProjectionCore(operation)
    )
    server = MCPServer(
        Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[CachedResponseResource(cache)],
        publisher=cache,
        presenter=make_response_presenter(policy),
    )
    async with connected_mcp_client(server) as client:
        listing = await client.list_tools()
        response = await client.call_tool("projection", {})
        text = "\n".join(item.text for item in response.content if isinstance(item, TextContent))
        structured = response.structured_content
        has_structured = (
            presentation_channel in {"both", "structured"} or data_channel == "structured"
        )
        assert (listing.tools[0].output_schema is not None) is has_structured
        assert (structured is not None) is has_structured
        if has_structured:
            assert structured is not None
            schema = listing.tools[0].output_schema
            assert schema is not None
            Draft202012Validator(schema).validate(structured)
            assert (structured["presentation"] is not None) is (presentation_channel != "text")
            if structured["presentation"] is not None:
                assert marker in structured["presentation"]
        if presentation_channel in {"text", "both"}:
            assert marker in text
        else:
            assert marker not in text
        if data_channel == "text":
            bundle = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
            assert structured is None or structured["data"] is None
        else:
            assert structured is not None
            bundle = structured
            assert isinstance(operation.detail, str)
            assert operation.detail not in text
        selected_data = bundle["data"]
        if delivery == "inline":
            assert selected_data["operation"] == operation.model_dump(mode="json", by_alias=True)
        else:
            recovered = await client.read_resource(selected_data["uri"])
            content = recovered.contents[0]
            assert isinstance(content, TextResourceContents)
            assert Projection.model_validate_json(content.text) == operation
        assert not response.is_error


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("failure_stage", "delivery", "operation_success"),
    [
        ("cache", "inline", True),
        ("inline", "inline", True),
        ("both", "inline", False),
        ("cache", "resource", True),
    ],
)
async def test_independent_serialization_failure_retains_actual_outcome(
    config: PresentationConfig,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
    delivery: str,
    operation_success: bool,
) -> None:
    """Neither native failure can be mistaken for full data or a failed mutation."""
    from jsonschema import Draft202012Validator  # noqa: PLC0415

    operation = Projection(
        success=operation_success,
        title="Required operation facts",
        count=0,
        labels=None,
        status=None,
        rows=(),
        detail="native detail",
    )
    expected = operation.model_dump(mode="json", by_alias=True)
    calls = {"cache": 0, "inline": 0}
    original_dump = Projection.model_dump
    if failure_stage in {"cache", "both"}:

        def fail_cache(*_args: object, **_kwargs: object) -> str:
            calls["cache"] += 1
            raise RuntimeError("canonical serializer failed") from OSError("native canonical cause")

        monkeypatch.setattr(Projection, "model_dump_json", fail_cache)
    if failure_stage in {"inline", "both"}:

        def fail_inline(self: Projection, **kwargs: object) -> dict[str, object]:
            if kwargs.get("mode") == "json":
                calls["inline"] += 1
                raise RuntimeError("inline serializer failed") from OSError("native inline cause")
            return original_dump(self, **kwargs)

        monkeypatch.setattr(Projection, "model_dump", fail_inline)
    raw = config.model_dump(by_alias=True)
    raw["tools"] = {"projection": {"template_success": "{title}", "template_failure": "{title}"}}
    policy = PresentationConfig.model_validate(raw)
    profile = "structured_inline" if delivery == "inline" else "structured_resource"
    cache = ResponseCacheManager()
    wrapped = ToolFactory(MagicMock(spec=EnforcementRunner), tmp_path).create_tool(
        ProjectionCore(operation)
    )
    server = MCPServer(
        Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[wrapped],
        resources=[CachedResponseResource(cache)],
        publisher=cache,
        presenter=make_response_presenter(policy, profile_id=profile),
    )
    async with connected_mcp_client(server) as client:
        listing = await client.list_tools()
        response = await client.call_tool("projection", {})
    assert response.is_error is (not operation_success)
    body = response.structured_content
    assert body is not None and body["success"] is operation_success
    assert operation.title in body["presentation"]
    schema = listing.tools[0].output_schema
    assert schema is not None
    Draft202012Validator(schema).validate(body)
    if failure_stage == "cache" and delivery == "inline":
        assert body["data"]["operation"] == expected
        assert body["delivery_error"] is None
    else:
        assert body["data"] is None
        assert body["delivery_error"]["code"] == "operation_serialization_failed"
    if failure_stage in {"cache", "both"}:
        assert calls["cache"] == 1
        assert "pgmcp://cache/runs/" not in body["presentation"]
    if failure_stage in {"inline", "both"}:
        assert calls["inline"] == 1



@pytest.mark.asyncio
@pytest.mark.usefixtures("git_workspace")
async def test_planning_update_note_preserves_independent_readback(
    configured_workspace: Path,
) -> None:
    """A readable evidence note cannot stand in for independent stored-plan proof."""
    head_sha = "planning-evidence-head"
    evidence = MagicMock(spec=ICycleEvidenceReader)
    evidence.read_cycle_evidence.return_value = CycleEvidence(
        status="complete",
        branch="bug/530-note",
        head_sha=head_sha,
        execution_phase="implementation",
        protected_cycle_numbers=(1,),
    )
    manager = make_project_manager(configured_workspace, cycle_evidence_reader=evidence)
    manager.initialize_project(530, "Note behavior", "feature", parent_branch="main")
    original = CycleInput(
        cycle_name="Existing",
        deliverables=[DeliverableInput(deliverable_name="Keep", description="Keep description")],
        exit_criteria="Keep criteria",
    )
    manager.save_planning_deliverables(530, SavePlanningModel(cycles=CyclesInput(cycles=[original])))
    before = manager.get_project_plan(530)
    assert before is not None
    snapshot = StoredPlanningModel.model_validate(before["planning_deliverables"], strict=True)
    added = CycleInput(
        cycle_name="Appended",
        deliverables=[DeliverableInput(deliverable_name="New", description="New description")],
        exit_criteria="New criteria",
    )
    factory = ToolFactory(MagicMock(spec=EnforcementRunner), configured_workspace)
    cores = [UpdatePlanningDeliverablesTool(manager), GetProjectPlanTool(manager)]
    server = MCPServer(
        Settings(server=ServerSettings(workspace_root=str(configured_workspace))),
        tools=[factory.create_tool(cast(ICoreTool[BaseModel, BaseModel], core)) for core in cores],
        resources=[],
        presenter=make_response_presenter(
            make_config_loader(configured_workspace).load_presentation_config(),
            profile_id="structured_inline",
        ),
    )
    async with connected_mcp_client(server) as client:
        update = await client.call_tool("update_planning_deliverables", {
            "issue_number":530,
            "operations":[{"op":"append_cycle", "cycle":added.model_dump(mode="json")}],
        })
        readback = await client.call_tool("get_project_plan", {"issue_number":530})
    assert not update.is_error and not readback.is_error
    assert update.structured_content is not None
    assert update.structured_content["success"] is True
    assert readback.structured_content is not None
    plan = ProjectPlanOutput.model_validate(readback.structured_content["data"]["operation"])
    assert plan.planning_deliverables is not None and plan.planning_deliverables.cycles is not None
    stored = plan.planning_deliverables.cycles.cycles
    assert snapshot.cycles is not None
    assert stored[0] == snapshot.cycles.cycles[0]
    assert stored[1].cycle_id == "C_2"
    assert stored[1].deliverables[0].deliverable_id == "D_2.1"
    assert stored[1].deliverables[0].description == added.deliverables[0].description
    assert stored[1].exit_criteria == added.exit_criteria
    assert head_sha in update.content[0].text
