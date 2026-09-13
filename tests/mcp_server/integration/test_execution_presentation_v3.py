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
    CallToolRequest,
    CallToolRequestParams,
    CallToolResult,
    ReadResourceRequest,
    ReadResourceRequestParams,
    ReadResourceResult,
    TextContent,
    TextResourceContents,
)
from pydantic import AnyUrl, BaseModel, ConfigDict, StrictInt, StrictStr

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.presentation_config import PresentationConfig, ToolPresentationConfig
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.presenters.response_presenter import ResponsePresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager


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
    return ConfigLoader(
        config_root=root / "config", template_root=root / "templates"
    ).load_presentation_config()


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
                "collections": [{"field": "rows", "item_template": "{label}: {args}"}],
                "enum_cases": [
                    {
                        "field": "status",
                        "cases": {
                            "complete": "COMPLETE",
                            "None": "UNKNOWN",
                        },
                    }
                ],
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
    response = await server.server.request_handlers[CallToolRequest](
        CallToolRequest(params=CallToolRequestParams(name="projection", arguments={}))
    )
    assert isinstance(response.root, CallToolResult)
    assert not response.root.isError
    text = "\n".join(item.text for item in response.root.content if isinstance(item, TextContent))
    assert "row-one:" in text and "cache-only" not in text
    assert "UNKNOWN" not in text
    assert ("COMPLETE" in text) is (not nullable)
    assert ("Result: -" if nullable else "Result: 0") in text
    match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", text)
    assert match is not None
    readback = await server.server.request_handlers[ReadResourceRequest](
        ReadResourceRequest(params=ReadResourceRequestParams(uri=AnyUrl(match.group())))
    )
    assert isinstance(readback.root, ReadResourceResult)
    content = readback.root.contents[0]
    assert isinstance(content, TextResourceContents)
    assert Projection.model_validate_json(content.text) == operation


def test_alignment_rejects_structured_union(config: PresentationConfig) -> None:
    presenter = _presenter(config, ToolPresentationConfig(template_success="{detail}"))
    with pytest.raises(ConfigError, match="structured|unsupported"):
        validate_presentation_alignment(
            presenter, [SupportedToolContract(name="projection", output_model=Projection)]
        )


@pytest.mark.parametrize("length", [8, 20_000], ids=["short", "truncated"])
def test_shipped_cache_hint_stays_complete_within_budget(
    config: PresentationConfig,
    length: int,
) -> None:
    presenter = _presenter(config, ToolPresentationConfig(template_success="{title}"))
    run_id = "c" * 32
    hint = config.global_settings.next_instruction_texts["uri_reference"].format(run_id=run_id)
    text = presenter.present_text(
        "projection",
        {"success": True, "title": "x" * length},
        cache_pub=CachePublication(run_id=run_id),
    )
    assert hint in text
    assert len(text.encode("utf-8")) <= config.global_settings.max_text_response_bytes
    assert f"pgmcp://cache/runs/{run_id}?offset=0&limit=" in hint
    for fact in ("next_offset", "null", "run_id", "sha256", "total_chars", "UTF-8", "Unicode"):
        assert fact in hint
    assert "smaller" in hint and "mutating" in hint and "read-only" in hint
