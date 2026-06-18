import pytest
from unittest.mock import MagicMock
from pathlib import Path

from mcp_server.config.schemas import GitConfig
from mcp_server.core.operation_notes import NoteContext, Note
from mcp_server.managers.git_manager import GitManager
from mcp_server.core.exceptions import PreflightError


@pytest.fixture
def git_config() -> GitConfig:
    from mcp_server.config.loader import ConfigLoader  # noqa: PLC0415

    return ConfigLoader(Path(".phase-gate/config")).load_git_config()


def test_git_manager_produces_generic_note_when_dirty(git_config: GitConfig) -> None:
    """RED test: GitManager.create_branch must produce a generic Note instead of BlockerNote.

    when dirty.
    """
    mock_adapter = MagicMock()
    mock_adapter.is_clean.return_value = False
    manager = GitManager(git_config=git_config, adapter=mock_adapter)
    context = NoteContext()

    with pytest.raises(PreflightError):
        manager.create_branch("my-branch", "feature", "HEAD", context)

    # Generic Note key and params assertion
    notes = context.entries
    assert len(notes) == 1
    assert isinstance(notes[0], Note)
    assert notes[0].key == "blocker_message"
    assert notes[0].params == {"message": "Commit or stash changes before creating a new branch"}
