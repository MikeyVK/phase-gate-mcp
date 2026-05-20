# tests/mcp_server/unit/managers/test_enforcement_runner_c4.py
"""Unit tests for C4 EnforcementRunner: check_context_loaded handler.

Tests exercise the public runner.run() API exclusively; no private-method access.

@layer: Tests (Unit)
@dependencies: [pathlib, pytest, unittest.mock, mcp_server.managers.enforcement_runner,
                mcp_server.core.interfaces]
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server.core.exceptions import ConfigError, ValidationError
from mcp_server.core.interfaces import IContextLoadedReader
from mcp_server.core.operation_notes import NoteContext, SuggestionNote
from mcp_server.managers.enforcement_runner import (
    EnforcementAction,
    EnforcementConfig,
    EnforcementContext,
    EnforcementRule,
    EnforcementRunner,
)


def _make_runner_c4(
    tmp_path: Path,
    config: EnforcementConfig,
    context_loaded_reader: IContextLoadedReader | None = None,
) -> EnforcementRunner:
    return EnforcementRunner(
        workspace_root=tmp_path,
        config=config,
        server_root=tmp_path / ".phase-gate",
        context_loaded_reader=context_loaded_reader,
    )


def _make_ctx(
    tmp_path: Path,
    tool_name: str = "some_tool",
    current_branch: str = "feature/42-test",
) -> EnforcementContext:
    return EnforcementContext(
        workspace_root=tmp_path,
        tool_name=tool_name,
        params={"current_branch": current_branch},
    )


def _make_note_context() -> NoteContext:
    return NoteContext()


def _make_check_context_loaded_config(
    tool: str = "some_tool",
    exempt_tools: list[str] | None = None,
) -> EnforcementConfig:
    return EnforcementConfig(
        enforcement=[
            EnforcementRule(
                event_source="tool",
                tool=tool,
                timing="pre",
                actions=[
                    EnforcementAction(
                        type="check_context_loaded",
                        exempt_tools=exempt_tools or [],
                    )
                ],
            )
        ]
    )


class TestCheckContextLoadedHandler:
    """check_context_loaded action via runner.run() public API."""

    def test_raises_config_error_when_reader_not_configured(
        self, tmp_path: Path
    ) -> None:
        """Missing context_loaded_reader must raise ConfigError at execution time."""
        config = _make_check_context_loaded_config()
        runner = _make_runner_c4(tmp_path, config, context_loaded_reader=None)

        with pytest.raises(ConfigError):
            runner.run(
                event="some_tool",
                timing="pre",
                enforcement_ctx=_make_ctx(tmp_path),
                note_context=_make_note_context(),
            )

    def test_passes_when_context_is_loaded(self, tmp_path: Path) -> None:
        """No exception when reader reports context already loaded for branch."""
        reader = MagicMock(spec=IContextLoadedReader)
        reader.is_context_loaded.return_value = True
        config = _make_check_context_loaded_config()
        runner = _make_runner_c4(tmp_path, config, context_loaded_reader=reader)

        runner.run(
            event="some_tool",
            timing="pre",
            enforcement_ctx=_make_ctx(tmp_path),
            note_context=_make_note_context(),
        )

        reader.is_context_loaded.assert_called_once_with("feature/42-test")

    def test_raises_validation_error_when_context_not_loaded(
        self, tmp_path: Path
    ) -> None:
        """ValidationError raised when reader reports context not yet loaded."""
        reader = MagicMock(spec=IContextLoadedReader)
        reader.is_context_loaded.return_value = False
        config = _make_check_context_loaded_config()
        runner = _make_runner_c4(tmp_path, config, context_loaded_reader=reader)

        with pytest.raises(ValidationError):
            runner.run(
                event="some_tool",
                timing="pre",
                enforcement_ctx=_make_ctx(tmp_path),
                note_context=_make_note_context(),
            )

    def test_produces_suggestion_note_on_block(self, tmp_path: Path) -> None:
        """SuggestionNote present in note_context when ValidationError is raised."""
        reader = MagicMock(spec=IContextLoadedReader)
        reader.is_context_loaded.return_value = False
        config = _make_check_context_loaded_config()
        runner = _make_runner_c4(tmp_path, config, context_loaded_reader=reader)
        note_context = _make_note_context()

        with pytest.raises(ValidationError):
            runner.run(
                event="some_tool",
                timing="pre",
                enforcement_ctx=_make_ctx(tmp_path),
                note_context=note_context,
            )

        notes = note_context.collect()
        assert any(isinstance(n, SuggestionNote) for n in notes)

    def test_exempt_tool_bypasses_when_not_loaded(self, tmp_path: Path) -> None:
        """Tool listed in exempt_tools passes even when context is not loaded."""
        reader = MagicMock(spec=IContextLoadedReader)
        reader.is_context_loaded.return_value = False
        config = _make_check_context_loaded_config(
            tool="some_tool", exempt_tools=["some_tool"]
        )
        runner = _make_runner_c4(tmp_path, config, context_loaded_reader=reader)

        # Must not raise
        runner.run(
            event="some_tool",
            timing="pre",
            enforcement_ctx=_make_ctx(tmp_path, tool_name="some_tool"),
            note_context=_make_note_context(),
        )

    def test_exempt_tool_bypasses_when_reader_none(self, tmp_path: Path) -> None:
        """Tool in exempt_tools bypasses even when no reader is configured."""
        config = _make_check_context_loaded_config(
            tool="some_tool", exempt_tools=["some_tool"]
        )
        runner = _make_runner_c4(tmp_path, config, context_loaded_reader=None)

        # Must not raise ConfigError — exempt_tools checked before reader access
        runner.run(
            event="some_tool",
            timing="pre",
            enforcement_ctx=_make_ctx(tmp_path, tool_name="some_tool"),
            note_context=_make_note_context(),
        )
