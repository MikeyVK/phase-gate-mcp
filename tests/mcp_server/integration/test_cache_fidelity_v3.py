# tests\mcp_server\integration\test_cache_fidelity_v3.py
# template=integration_test version=c2e61372 created=2026-09-13T18:41Z updated=
"""Preserve required null and selected variants through real MCP resource reads.

@layer: Tests (Integration)
@dependencies: pydantic, mcp, CachedResponseResource, ResponseCacheManager
"""

import json
from pathlib import Path
from typing import Annotated, Literal

import pytest
from mcp.types import (
    ReadResourceRequest,
    ReadResourceRequestParams,
    ReadResourceResult,
    TextResourceContents,
)
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, JsonValue

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.error_outputs import ExecutionErrorOutput
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager


class Capture(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    stdout: str | None
    stderr: str | None
    debug: str | None = None


class Completed(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    kind: Literal["completed"]
    captures: tuple[Capture, ...]


class Unavailable(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    kind: Literal["unavailable"]
    capture: Capture | None


class OperationSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    success: bool
    outcome: Annotated[Completed | Unavailable, Field(discriminator="kind")]
    error_details: Capture | None
    values: dict[str, JsonValue]
    explicit_null: str | None = None
    absent: str | None = None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "outcome, expected",
    [
        (
            Completed(kind="completed", captures=(Capture(stdout=None, stderr=""),)),
            {"kind": "completed", "captures": [{"stdout": None, "stderr": ""}]},
        ),
        (
            Unavailable(kind="unavailable", capture=None),
            {"kind": "unavailable", "capture": None},
        ),
    ],
    ids=["nested-capture", "unavailable-variant"],
)
async def test_operation_roundtrip_retains_required_null_and_presence(
    tmp_path: Path,
    outcome: Completed | Unavailable,
    expected: dict[str, JsonValue],
) -> None:
    operation = OperationSnapshot(
        success=False,
        outcome=outcome,
        error_details=None,
        values={"null": None, "false": False, "zero": 0, "empty": []},
        explicit_null=None,
    )
    text = await _read_cached_operation(tmp_path, operation)
    assert json.loads(text) == {
        "success": False,
        "outcome": expected,
        "error_details": None,
        "values": {"null": None, "false": False, "zero": 0, "empty": []},
        "explicit_null": None,
    }
    assert OperationSnapshot.model_validate_json(text) == operation


@pytest.mark.asyncio
async def test_legacy_error_cache_keeps_defaults_and_omits_absent_null(tmp_path: Path) -> None:
    text = await _read_cached_operation(tmp_path, ExecutionErrorOutput(error_message="Failed"))
    assert json.loads(text) == {
        "success": False,
        "error_type": "ExecutionError",
        "error_message": "Failed",
        "params": {},
    }


async def _read_cached_operation(tmp_path: Path, operation: BaseModel) -> str:
    cache = ResponseCacheManager()
    publication = cache.put("example", operation)
    assert publication.run_id is not None
    server = MCPServer(
        Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[],
        resources=[CachedResponseResource(cache)],
    )
    response = await server.server.request_handlers[ReadResourceRequest](
        ReadResourceRequest(
            params=ReadResourceRequestParams(uri=AnyUrl(f"pgmcp://cache/runs/{publication.run_id}"))
        )
    )
    assert isinstance(response.root, ReadResourceResult)
    assert len(response.root.contents) == 1
    content = response.root.contents[0]
    assert isinstance(content, TextResourceContents)
    return content.text
