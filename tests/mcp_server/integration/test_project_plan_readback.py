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
from git import Actor, Repo
from pydantic import AnyUrl

import mcp_server
from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.interfaces import GateViolation
from mcp_server.core.interfaces.git import CycleEvidence
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.deliverables import (
    CycleInput,
    CyclesInput,
    DeliverableInput,
    PhaseBlockInput,
    ReplaceCycle,
    SavePlanningModel,
    SetPhase,
    ValidatesModel,
)
from mcp_server.server import MCPServer
from tests.mcp_server.fixtures.suite_roots import SuiteRoots
from tests.mcp_server.test_support import make_project_manager


class _CompleteEvidence:
    """Explicitly isolate planning mutations from the checkout's real Git."""

    def read_cycle_evidence(self, issue_number: int, execution_phase: str | None) -> CycleEvidence:
        return CycleEvidence(
            status="complete",
            branch=f"feature/{issue_number}-test",
            head_sha="test-head",
            execution_phase=execution_phase,
            protected_cycle_numbers=(),
        )


def _planning_payload(cycle_count: int) -> SavePlanningModel:
    """Distinct authored values make omissions and swaps observable."""
    return SavePlanningModel(
        cycles=CyclesInput(
            cycles=[
                CycleInput(
                    cycle_name=f"Cycle {number}: preserve boundary",
                    deliverables=[
                        DeliverableInput(
                            deliverable_name="Implementation",
                            description=f"Implement bounded surface {number}",
                            validates=ValidatesModel(type="file_exists", file=f"src/c{number}.py"),
                        ),
                        DeliverableInput(
                            deliverable_name="Evidence",
                            description=f"Independent evidence for {number}",
                            validates=ValidatesModel(
                                type="contains_text",
                                file=f"evidence/c{number}.md",
                                text=f"Retained behavior {number}",
                            ),
                        ),
                    ],
                    exit_criteria=f"Cycle {number}: explicit stop/go; preserve newline.\nDone.",
                )
                for number in range(1, cycle_count + 1)
            ]
        ),
        phases={
            "design": PhaseBlockInput(
                deliverables=[
                    DeliverableInput(
                        deliverable_name="Inventory",
                        description="Contract inventory",
                        validates=ValidatesModel(
                            type="file_glob", dir="docs/design", pattern="*.md"
                        ),
                    )
                ]
            ),
            "validation": PhaseBlockInput(
                deliverables=[
                    DeliverableInput(
                        deliverable_name="Review",
                        description="No unresolved blocker",
                        validates=ValidatesModel(
                            type="absent_text", file="review.md", text="OPEN BLOCKER"
                        ),
                    )
                ]
            ),
            "documentation": PhaseBlockInput(
                deliverables=[
                    DeliverableInput(
                        deliverable_name="Schema",
                        description="Document final schema",
                        validates=ValidatesModel(
                            type="key_path", file="contract.json", path="version"
                        ),
                    )
                ]
            ),
        },
    )


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
    if not suite_source.is_dir():
        suite_source = Path(__file__).resolve().parents[3] / ".pgmcp/template_suite"
    assert suite_source.is_dir(), "v3_template_suite_source_missing"
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
    manager = make_project_manager(
        legacy_suite_roots.workspace, cycle_evidence_reader=_CompleteEvidence()
    )
    manager.initialize_project(53, "Planning readback", "feature")
    authored = _planning_payload(cycle_count)
    manager.save_planning_deliverables(53, authored)
    saved = manager.get_project_plan(53)
    assert saved is not None
    expected = saved["planning_deliverables"]
    assert expected["cycles"]["cycles"][0]["cycle_id"] == "C_1"
    assert (
        expected["cycles"]["cycles"][-1]["deliverables"][-1]["deliverable_id"]
        == f"D_{cycle_count}.2"
    )

    server = ServerBootstrapper(settings).bootstrap_target()
    old_uri = await _call_plan(server)
    first = await _read_resource(server, old_uri)
    assert first["planning_deliverables"] == expected
    assert await _read_windowed_plan(server, old_uri) == first
    assert [phase["name"] for phase in first["phases"]] == manager.get_phases("feature")

    assert authored.cycles is not None
    revised_cycle = authored.cycles.cycles[0].model_copy(
        update={"exit_criteria": "Revised stop/go proof"}
    )
    manager.update_planning_deliverables(
        53,
        [ReplaceCycle(op="replace_cycle", cycle_id="C_1", cycle=revised_cycle)],
        context=NoteContext(),
    )
    revised = manager.get_project_plan(53)
    assert revised is not None
    expected = revised["planning_deliverables"]

    restarted = ServerBootstrapper(settings).bootstrap_target()
    with pytest.raises(ValueError, match="No cached data found"):
        await _read_resource(restarted, old_uri)
    new_uri = await _call_plan(restarted)
    assert new_uri != old_uri
    second = await _read_windowed_plan(restarted, new_uri)
    assert second["planning_deliverables"] == expected
    assert second["phases"] == first["phases"]

@pytest.mark.parametrize("boundary", ["cycle", "phase"])
@pytest.mark.parametrize("forced", [False, True])
def test_saved_file_glob_reaches_bootstrap_gates_and_refreshes_after_update(
    legacy_suite_roots: SuiteRoots, boundary: str, forced: bool
) -> None:
    """Saved and revised rules govern real normal/forced transitions without a restart."""
    workspace = legacy_suite_roots.workspace
    repo = Repo.init(workspace)
    actor = Actor("Gate Test", "gate@example.com")
    root = repo.index.commit("chore: isolated gate workspace", author=actor, committer=actor)
    branch = "feature/229-gate"
    repo.create_head(branch, root).checkout()
    settings = Settings(
        server=ServerSettings(
            workspace_root=str(workspace),
            server_root_dir=legacy_suite_roots.server.name,
            config_root=str(legacy_suite_roots.config),
            template_root=str(legacy_suite_roots.templates),
        )
    )
    bootstrapper = ServerBootstrapper(settings)
    graph = bootstrapper._build_manager_graph(bootstrapper._build_config_layer())
    manager = graph.project_manager
    engine = graph.phase_state_engine
    reader = DeliverableInput(
        deliverable_name="Reader source",
        description="Reader source exists",
        validates=ValidatesModel(type="file_glob", dir="src", pattern="**/reader.py"),
    )
    first_cycle = CycleInput(
        cycle_name="Reader", deliverables=[reader], exit_criteria="Reader source present"
    )
    manager.initialize_project(229, "Saved gate glob", "feature")
    manager.save_planning_deliverables(
        229,
        SavePlanningModel(
            cycles=CyclesInput(
                cycles=[
                    first_cycle,
                    first_cycle.model_copy(update={"cycle_name": "Follow-up"}),
                ]
            ),
            phases={"validation": PhaseBlockInput(deliverables=[reader])},
        ),
    )
    docs = workspace / "docs" / "development" / "issue229"
    docs.mkdir(parents=True)
    (docs / "validation.md").write_text("# Validation\n", encoding="utf-8")
    engine.initialize_branch(
        branch, 229, initial_phase="implementation" if boundary == "cycle" else "validation"
    )
    initial = engine.get_state(branch)
    graph.state_repository.save(initial.with_updates(current_cycle=1, last_cycle=0))
    initial = engine.get_state(branch)
    check_id = "D_1.1" if boundary == "cycle" else "D_1"

    def advance() -> dict[str, Any]:
        if boundary == "cycle":
            return engine.transition_cycle(branch, to_cycle=2)
        return engine.transition(branch, to_phase="documentation")

    with pytest.raises(GateViolation) as rejected:
        advance()
    assert check_id in rejected.value.report.blocking
    assert engine.get_state(branch) == initial

    nested = workspace / "src" / "nested"
    nested.mkdir(parents=True)
    (nested / "reader.py").write_text("# original reader\n", encoding="utf-8")
    revised = reader.model_copy(
        update={"validates": ValidatesModel(type="file_glob", dir="src", pattern="**/revised.py")}
    )
    operation = (
        ReplaceCycle(
            op="replace_cycle",
            cycle_id="C_1",
            cycle=first_cycle.model_copy(update={"deliverables": [revised]}),
        )
        if boundary == "cycle"
        else SetPhase(
            op="set_phase", phase="validation", block=PhaseBlockInput(deliverables=[revised])
        )
    )
    manager.update_planning_deliverables(229, [operation], context=NoteContext())
    with pytest.raises(GateViolation) as refreshed:
        advance()
    assert check_id in refreshed.value.report.blocking
    assert engine.get_state(branch) == initial

    if forced:
        if boundary == "cycle":
            result = engine.force_cycle_transition(
                branch, to_cycle=2, skip_reason="Inspect current rule", human_approval_message="Owner approved"
            )
        else:
            result = engine.force_transition(
                branch, to_phase="documentation", skip_reason="Inspect current rule", human_approval_message="Owner approved"
            )
        assert check_id in result["skipped_gates"]
    else:
        (nested / "revised.py").write_text("# revised reader\n", encoding="utf-8")
        result = advance()
    assert result["success"] is True
    advanced = engine.get_state(branch)
    if boundary == "cycle":
        assert advanced.current_cycle == 2
    else:
        assert advanced.current_phase == "documentation"
