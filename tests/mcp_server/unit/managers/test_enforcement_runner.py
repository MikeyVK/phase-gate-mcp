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

from mcp_server.core.exceptions import ConfigError, ValidationError
from mcp_server.core.interfaces import IStateReader
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.enforcement_runner import (
    EnforcementAction,
    EnforcementConfig,
    EnforcementContext,
    EnforcementRule,
    EnforcementRunner,
)


def _write_enforcement_file(tmp_path: Path, content: str) -> None:
    config_dir = tmp_path / ".phase-gate" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "enforcement.yaml").write_text(content, encoding="utf-8")


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
    """Test suite for Cycle 5 enforcement loading and dispatch."""

    def test_constructor_raises_config_error_for_unknown_action_type(self, tmp_path: Path) -> None:
        """Unknown action types must fail fast at startup."""
        config = EnforcementConfig(
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool="create_branch",
                    timing="pre",
                    actions=[EnforcementAction(type="unknown_action")],
                )
            ]
        )

        with pytest.raises(ConfigError, match="unknown_action"):
            _make_runner(tmp_path, config)

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

    def test_enforcement_runner_handles_tool_guards_only(self, tmp_path: Path) -> None:
        """Guard-only enforcement should not require state-commit collaborators."""
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
        runner = EnforcementRunner(
            workspace_root=tmp_path,
            config=config,
            git_config=MagicMock(),
            server_root=tmp_path,
            state_reader=MagicMock(spec=IStateReader),
        )

        runner.run(
            event="create_branch",
            timing="pre",
            enforcement_ctx=EnforcementContext(
                workspace_root=tmp_path,
                tool_name="create_branch",
                params=SimpleNamespace(
                    branch_type="feature",
                    base_branch="main",
                ),
            ),
            note_context=NoteContext(),
        )


class TestEnforcementSchemaValidation:
    """Direct schema validation coverage for enforcement config models."""

    def test_branch_policy_action_requires_rules(self) -> None:
        """check_branch_policy actions must declare at least one rule."""
        with pytest.raises(ValueError, match="requires non-empty rules"):
            EnforcementAction(type="check_branch_policy")

    def test_legacy_commit_state_files_action_is_rejected_by_runner(
        self,
        tmp_path: Path,
    ) -> None:
        """Legacy commit_state_files actions should fail fast at startup."""
        config = EnforcementConfig(
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool="transition_phase",
                    timing="post",
                    actions=[EnforcementAction(type="commit_state_files")],
                )
            ]
        )

        with pytest.raises(ConfigError, match="commit_state_files"):
            _make_runner(tmp_path, config)

    def test_delete_file_action_requires_path(self) -> None:
        """delete_file actions must declare a single target path."""
        with pytest.raises(ValueError, match="requires path"):
            EnforcementAction(type="delete_file")

    def test_tool_event_source_requires_tool_name(self) -> None:
        """Tool-triggered rules must include the tool name."""
        with pytest.raises(ValueError, match="requires tool"):
            EnforcementRule(event_source="tool", timing="pre")

    def test_phase_event_source_requires_phase_name(self) -> None:
        """Phase-triggered rules must include the phase name."""
        with pytest.raises(ValueError, match="requires phase"):
            EnforcementRule(event_source="phase", timing="post")

    def test_dynamic_categories_config_parsing(self) -> None:
        """EnforcementConfig must accept dynamic categories mapping."""
        config = EnforcementConfig(
            categories={"custom_category": ["create_branch", "git_checkout"]},
            enforcement=[]
        )
        assert config.categories == {"custom_category": ["create_branch", "git_checkout"]}

    def test_runner_validates_against_dynamic_categories(self, tmp_path: Path) -> None:
        """Runner must reject rules with tool categories not present in config.categories."""
        config = EnforcementConfig(
            categories={"valid_cat": ["some_tool"]},
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool_category="invalid_cat",
                    timing="pre",
                    actions=[EnforcementAction(type="check_pr_status")]
                )
            ]
        )
        with pytest.raises(ConfigError, match="Unknown tool_category value"):
            _make_runner(tmp_path, config)

    def test_runner_resolves_category_dynamically(self, tmp_path: Path) -> None:
        """Runner must resolve tool category dynamically when tool_category is omitted."""
        config = EnforcementConfig(
            categories={"custom_category": ["create_branch"]},
            enforcement=[
                EnforcementRule(
                    event_source="tool",
                    tool_category="custom_category",
                    timing="pre",
                    actions=[EnforcementAction(type="check_pr_status")]
                )
            ]
        )
        calls = []
        def fake_handler(
            action: EnforcementAction,
            context: EnforcementContext,
            workspace_root: Path,
            note_context: NoteContext,
        ) -> None:
            calls.append(action.type)

        runner = _make_runner(
            tmp_path,
            config,
            registry={"check_pr_status": fake_handler}
        )

        runner.run(
            event="create_branch",
            timing="pre",
            enforcement_ctx=EnforcementContext(
                workspace_root=tmp_path,
                tool_name="create_branch",
                params=SimpleNamespace(),
            ),
            note_context=NoteContext(),
            tool_category=None  # Omitted: must resolve dynamically
        )
        assert calls == ["check_pr_status"]

    def test_exempt_tools_allowed_on_any_action_type(self) -> None:
        """exempt_tools must be allowed on actions other than check_context_loaded."""
        action = EnforcementAction(
            type="check_pr_status",
            exempt_tools=["some_tool"]
        )
        assert action.exempt_tools == ["some_tool"]
