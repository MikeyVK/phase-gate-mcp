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
    ReadResourceResult,
    TextResourceContents,
)
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.exceptions import ConfigError
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.schemas.error_outputs import ConfigErrorOutput, ExecutionErrorOutput
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from tests.mcp_server.test_support import connected_mcp_client, make_response_presenter


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
@pytest.mark.parametrize("failure_kind", ["none", "execution", "config"])
async def test_error_cache_preserves_diagnosis_and_publication_facts(
    tmp_path: Path,
    failure_kind: str,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    cause = OSError("serialization storage unavailable")
    failure = (
        ConfigError("serialization configuration failed", file_path="operation.yaml")
        if failure_kind == "config"
        else RuntimeError("serialization failed")
    )

    class BrokenErrorOutput(ExecutionErrorOutput):
        pass

    serialization_calls = 0
    if failure_kind != "none":

        def fail_serialization(*_args: object, **_kwargs: object) -> str:
            nonlocal serialization_calls
            serialization_calls += 1
            raise failure from cause

        monkeypatch.setattr(BrokenErrorOutput, "model_dump_json", fail_serialization)

    operation = (
        BrokenErrorOutput(error_message="Failed", traceback="Original tool traceback")
        if failure_kind != "none"
        else ExecutionErrorOutput(error_message="Failed")
    )
    if failure_kind != "none":
        cache = ResponseCacheManager(max_size=2)
        original = ExecutionErrorOutput(error_message="Earlier operation")
        earlier = cache.put("earlier", original)
        assert earlier.run_id is not None

        publication = cache.put("example", operation)

        assert not publication.success
        assert publication.run_id is None
        assert publication.size_chars is None
        assert publication.error_code == "serialization_failed"
        assert serialization_calls == 1
        diagnosis = publication.diagnostic
        assert diagnosis is not None
        if failure_kind == "config":
            assert isinstance(diagnosis, ConfigErrorOutput)
            assert diagnosis.file_path == "operation.yaml"
            assert diagnosis.error_code == "ERR_CONFIG"
        else:
            assert isinstance(diagnosis, ExecutionErrorOutput)
            assert diagnosis.error_code is None
        assert diagnosis.traceback is not None
        assert "OSError: serialization storage unavailable" in diagnosis.traceback
        assert type(failure).__name__ in diagnosis.traceback
        assert str(failure) in diagnosis.traceback
        assert diagnosis.error_message is not None
        assert str(failure) in diagnosis.error_message
        assert operation.error_message == "Failed"
        assert operation.traceback == "Original tool traceback"

        record = caplog.records[-1]
        assert record.exc_info is not None
        assert record.exc_info[1] is failure
        assert failure.__cause__ is cause
        assert "OSError: serialization storage unavailable" in caplog.text
        assert str(failure) in caplog.text

        # A failed publication consumes no capacity and evicts no existing entry.
        following = cache.put("following", ExecutionErrorOutput(error_message="Following"))
        assert following.run_id is not None
        assert cache.get(earlier.run_id, ExecutionErrorOutput) is original
        assert cache.exists(following.run_id)
        return

    text = await _read_cached_operation(tmp_path, operation)
    result = json.loads(text)
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
        presenter=make_response_presenter(),
    )
    async with connected_mcp_client(server) as client:
        response = await client.read_resource(f"pgmcp://cache/runs/{publication.run_id}")
    assert isinstance(response, ReadResourceResult)
    assert len(response.contents) == 1
    content = response.contents[0]
    assert isinstance(content, TextResourceContents)
    return content.text
