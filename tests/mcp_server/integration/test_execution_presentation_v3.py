# tests\mcp_server\integration\test_execution_presentation_v3.py
# template=integration_test version=c2e61372 created=2026-09-13T18:55Z updated=
"""Exercise generic projection admission and shipped cache guidance.

@layer: Tests (Integration)
@dependencies: pydantic, mcp, TextPresenter, ToolFactory, CachedResponseResource
"""

import re
from enum import StrEnum
from pathlib import Path
from typing import Literal
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
from mcp_server.core.interfaces.itool_response_cache import IToolResponsePublisher
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource, CacheReadGuideResource
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from tests.mcp_server.test_support import connected_mcp_client


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
        presenter=ResponsePresenter(presenter, SchemaResourcePresenter()),
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
        presenter=ResponsePresenter(presenter, SchemaResourcePresenter()),
    )
    async with connected_mcp_client(server) as client:
        response = await client.call_tool("projection", {})
        assert isinstance(response, CallToolResult)
        assert response.is_error is (not operation_success)
        assert response.structured_content == operation.model_dump(mode="json", by_alias=True)
        text = "\n".join(item.text for item in response.content if isinstance(item, TextContent))
        assert len(text.encode("utf-8")) <= config.global_settings.max_text_response_bytes
        match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", text)
        guide_uri = CacheReadGuideResource.uri_pattern
        if cache_failure:
            assert match is None
            assert guide_uri not in text
            tail = config.global_settings.formatting.cache_unavailable_truncation_notice
            if length > config.global_settings.max_text_response_bytes:
                assert text.endswith(tail)
            else:
                notices = config.global_settings.next_instruction_texts
                assert notices["cache_publication_failed"] in text
                assert tail not in text
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
            "tools": {"projection": {"template_success": "{title}"}},
        }
    )
    with pytest.raises(ConfigError, match="placeholder"):
        validate_presentation_alignment(
            TextPresenter(config=policy),
            [SupportedToolContract(name="projection", output_model=Projection)],
        )
