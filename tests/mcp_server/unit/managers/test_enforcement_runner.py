# tests/mcp_server/unit/managers/test_enforcement_runner.py
# template=unit_test version=3d15d309 created=2026-03-13T10:02Z updated=
"""Unit tests for enforcement runner configuration and dispatch.

@layer: Tests (Unit)
@dependencies: [pathlib, pytest, unittest.mock, mcp_server.managers.enforcement_runner]
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from mcp_server.core.exceptions import ValidationError
from mcp_server.core.interfaces import IStateReader
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.enforcement_runner import (
    EnforcementAction,
    EnforcementConfig,
    EnforcementContext,
    EnforcementRule,
    EnforcementRunner,
)


def _make_runner(
    tmp_path: Path,
    config: EnforcementConfig,
    registry: dict[str, object] | None = None,
) -> EnforcementRunner:
    return EnforcementRunner(
        workspace_root=tmp_path,
        config=config,
        git_config=MagicMock(),
        registry=registry,
        server_root=tmp_path,
        state_reader=MagicMock(spec=IStateReader),
    )


class TestEnforcementRunner:
    """Test suite for enforcement loading and dispatch."""

    def test_run_dispatches_registered_handler_for_matching_tool_event(
        self, tmp_path: Path
    ) -> None:
        """Matching tool rules must dispatch their registered handlers."""
        config = EnforcementConfig(
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool="create_branch",
                    timing="pre",
                    actions=[
                        EnforcementAction(
                            type="check_branch_policy",
                            rules={"feature": ["main", "epic/*"]},
                        )
                    ],
                )
            ]
        )
        calls: list[tuple[str, str]] = []

        def fake_handler(
            action: EnforcementAction,
            context: EnforcementContext,
            workspace_root: Path,
            note_context: NoteContext,  # noqa: ARG001
        ) -> None:
            calls.append((action.type, context.tool_name))
            assert workspace_root == tmp_path

        runner = _make_runner(
            tmp_path,
            config,
            registry={"check_branch_policy": fake_handler},
        )

        runner.run(
            event="create_branch",
            timing="pre",
            enforcement_ctx=EnforcementContext(
                workspace_root=tmp_path,
                tool_name="create_branch",
                params=SimpleNamespace(branch_type="feature", base_branch="main"),
            ),
            note_context=NoteContext(),
        )

        assert calls == [("check_branch_policy", "create_branch")]

    def test_check_branch_policy_rejects_invalid_base_branch(self, tmp_path: Path) -> None:
        """Branch policy must block disallowed base branches."""
        config = EnforcementConfig(
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool="create_branch",
                    timing="pre",
                    actions=[
                        EnforcementAction(
                            type="check_branch_policy",
                            rules={"feature": ["main", "epic/*"]},
                        )
                    ],
                )
            ]
        )
        runner = _make_runner(tmp_path, config)

        with pytest.raises(ValidationError, match="cannot be created from base"):
            runner.run(
                event="create_branch",
                timing="pre",
                enforcement_ctx=EnforcementContext(
                    workspace_root=tmp_path,
                    tool_name="create_branch",
                    params=SimpleNamespace(
                        branch_type="feature",
                        base_branch="release/1.0",
                    ),
                ),
                note_context=NoteContext(),
            )

    def test_runner_resolves_category_dynamically(self, tmp_path: Path) -> None:
        """Runner must resolve tool category dynamically when tool_category is omitted."""
        config = EnforcementConfig(
            categories={"custom_category": ["create_branch"]},
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool_category="custom_category",
                    timing="pre",
                    actions=[EnforcementAction(type="check_pr_status")],
                )
            ],
        )
        calls = []

        def fake_handler(
            action: EnforcementAction,
            context: EnforcementContext,
            workspace_root: Path,
            note_context: NoteContext,
        ) -> None:
            calls.append(action.type)

        runner = _make_runner(tmp_path, config, registry={"check_pr_status": fake_handler})

        runner.run(
            event="create_branch",
            timing="pre",
            enforcement_ctx=EnforcementContext(
                workspace_root=tmp_path,
                tool_name="create_branch",
                params=SimpleNamespace(),
            ),
            note_context=NoteContext(),
            tool_category=None,  # Omitted: must resolve dynamically
        )
        assert calls == ["check_pr_status"]
