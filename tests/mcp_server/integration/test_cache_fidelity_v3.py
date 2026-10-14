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
@pytest.mark.parametrize("serialization_fails", [False, True])
async def test_error_cache_preserves_diagnosis_and_json_fallback(
    tmp_path: Path,
    serialization_fails: bool,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    cause = OSError("serialization storage unavailable")
    failure = RuntimeError("serialization failed")

    class BrokenErrorOutput(ExecutionErrorOutput):
        pass

    if serialization_fails:

        def fail_serialization(*_args: object, **_kwargs: object) -> str:
            raise failure from cause

        monkeypatch.setattr(BrokenErrorOutput, "model_dump_json", fail_serialization)

    operation = (
        BrokenErrorOutput(error_message="Failed", traceback="Original tool traceback")
        if serialization_fails
        else ExecutionErrorOutput(error_message="Failed")
    )
    text = await _read_cached_operation(tmp_path, operation)
    result = json.loads(text)
    if serialization_fails:
        assert result["success"] is False
        assert result["error_type"] == "SerializationError"
        assert result["dto_type"] == "BrokenErrorOutput"
        assert result["error_message"] == "Failed"
        assert result["traceback"] == "Original tool traceback"
        assert "serialization failed" in result["message"]
        record = caplog.records[-1]
        assert record.exc_info is not None
        assert record.exc_info[1] is failure
        assert failure.__cause__ is cause
        assert "OSError: serialization storage unavailable" in caplog.text
        assert "RuntimeError: serialization failed" in caplog.text
        return

    assert result == {
        "success": False,
        "error_type": "ExecutionError",
        "error_message": "Failed",
        "params": {},
        "error_params": {},
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
