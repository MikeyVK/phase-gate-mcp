# tests/mcp_server/integration/test_project_plan_readback.py
# template=integration_test version=c2e61372 created=2026-09-13T12:26Z updated=
"""Stored planning through normal bootstrap, MCP handlers and cache resources.

@layer: Tests (Integration)
"""

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

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
from pydantic import AnyUrl

import mcp_server
from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.server import MCPServer
from tests.mcp_server.fixtures.suite_roots import SuiteRoots
from tests.mcp_server.test_support import make_project_manager


def _planning_payload(cycle_count: int) -> dict[str, Any]:
    """Create distinct ordered values so omissions and swaps are observable."""
    return {
        "cycles": {
            "total": cycle_count,
            "cycles": [
                {
                    "cycle_number": number,
                    "name": f"Cycle {number}: preserve boundary",
                    "deliverables": [
                        {
                            "id": f"C{number}.D1",
                            "description": f"Implement bounded surface {number}",
                            "validates": {"type": "file_exists", "file": f"src/c{number}.py"},
                        },
                        {
                            "id": f"C{number}.D2",
                            "description": f"Independent evidence for {number}",
                            "validates": {
                                "type": "contains_text",
                                "file": f"evidence/c{number}.md",
                                "text": f"Retained behavior {number}",
                            },
                        },
                    ],
                    "exit_criteria": f"Cycle {number}: explicit stop/go; preserve newline.\nDone.",
                }
                for number in range(1, cycle_count + 1)
            ],
        },
        "design": {
            "deliverables": [
                {
                    "id": "DESIGN.1",
                    "description": "Contract inventory",
                    "validates": {"type": "file_glob", "file": "docs/design/*.md"},
                }
            ]
        },
        "validation": {
            "deliverables": [
                {
                    "id": "VALIDATE.1",
                    "description": "No unresolved blocker",
                    "validates": {
                        "type": "absent_text",
                        "file": "review.md",
                        "text": "OPEN BLOCKER",
                    },
                }
            ]
        },
        "documentation": {
            "deliverables": [
                {
                    "id": "DOC.1",
                    "description": "Document final schema",
                    "validates": {"type": "key_path", "file": "contract.json", "path": "version"},
                }
            ]
        },
    }


async def _call_plan(server: MCPServer) -> str:
    """Call the registered MCP handler and obtain its advertised resource URI."""
    response = await server.server.request_handlers[CallToolRequest](
        CallToolRequest(
            params=CallToolRequestParams(name="get_project_plan", arguments={"issue_number": 53})
        )
    )
    result = response.root
    assert isinstance(result, CallToolResult)
    assert not result.isError
    text = "\n".join(part.text for part in result.content if isinstance(part, TextContent))
    assert "Implement bounded surface" not in text
    match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", text)
    assert match is not None
    return match.group()


async def _read_resource(server: MCPServer, uri: str) -> dict[str, Any]:
    """Read through the MCP resource handler, never the persistence file."""
    response = await server.server.request_handlers[ReadResourceRequest](
        ReadResourceRequest(params=ReadResourceRequestParams(uri=AnyUrl(uri)))
    )
    result = response.root
    assert isinstance(result, ReadResourceResult)
    assert len(result.contents) == 1
    content = result.contents[0]
    assert isinstance(content, TextResourceContents)
    payload = json.loads(content.text)
    assert isinstance(payload, dict)
    return payload


async def _read_windowed_plan(server: MCPServer, uri: str) -> dict[str, Any]:
    """Reconstruct one snapshot exclusively through bounded MCP resource reads."""
    offset = 0
    fragments: list[str] = []
    checksum: str | None = None
    total: int | None = None
    while True:
        page = await _read_resource(server, f"{uri}?offset={offset}&limit=6000")
        assert page["run_id"] == uri.rsplit("/", maxsplit=1)[-1]
        assert page["offset"] == offset
        checksum = page["sha256"] if checksum is None else checksum
        total = page["total_chars"] if total is None else total
        assert page["sha256"] == checksum
        assert page["total_chars"] == total
        assert len(page["text"]) <= 6000
        fragments.append(page["text"])
        next_offset = page["next_offset"]
        if next_offset is None:
            break
        assert next_offset == offset + len(page["text"])
        offset = next_offset
    complete = "".join(fragments)
    assert len(complete) == total
    assert hashlib.sha256(complete.encode("utf-8")).hexdigest() == checksum
    payload = json.loads(complete)
    assert isinstance(payload, dict)
    return payload


@pytest.mark.asyncio
@pytest.mark.parametrize("cycle_count", [3, 117])
async def test_stored_planning_survives_fresh_bootstrap_cache(
    legacy_suite_roots: SuiteRoots, cycle_count: int
) -> None:
    """A fresh bootstrap cache regenerates full saved and updated planning."""
    suite_source = Path(mcp_server.__file__).resolve().parent / "assets/template_suite"
    shutil.copytree(suite_source, legacy_suite_roots.server / "template_suite")
    settings = Settings(
        server=ServerSettings(
            workspace_root=str(legacy_suite_roots.workspace),
            server_root_dir=legacy_suite_roots.server.name,
            config_root=str(legacy_suite_roots.config),
            template_root=str(legacy_suite_roots.server / "template_suite"),
            bypass_version_check=False,
        )
    )
    (legacy_suite_roots.server / "installation.json").write_text(
        json.dumps({"pgmcp_version": settings.server.version}), encoding="utf-8"
    )
    manager = make_project_manager(legacy_suite_roots.workspace)
    manager.initialize_project(53, "Planning readback", "feature")
    expected = _planning_payload(cycle_count)
    manager.save_planning_deliverables(53, expected)

    server = ServerBootstrapper(settings).bootstrap_target()
    old_uri = await _call_plan(server)
    first = await _read_resource(server, old_uri)
    assert first["planning_deliverables"] == expected
    assert await _read_windowed_plan(server, old_uri) == first
    assert [phase["name"] for phase in first["phases"]] == manager.get_phases("feature")

    revised_cycle = {**expected["cycles"]["cycles"][0], "exit_criteria": "Revised stop/go proof"}
    manager.update_planning_deliverables(53, {"cycles": {"cycles": [revised_cycle]}})
    expected["cycles"]["cycles"][0] = revised_cycle

    restarted = ServerBootstrapper(settings).bootstrap_target()
    with pytest.raises(ValueError, match="No cached data found"):
        await _read_resource(restarted, old_uri)
    new_uri = await _call_plan(restarted)
    assert new_uri != old_uri
    second = await _read_windowed_plan(restarted, new_uri)
    assert second["planning_deliverables"] == expected
    assert second["phases"] == first["phases"]
