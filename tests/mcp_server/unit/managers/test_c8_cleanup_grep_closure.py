# tests/mcp_server/unit/managers/test_c8_cleanup_grep_closure.py
"""C8 grep-closure structural tests.

Verifies that legacy fallback paths (state.json direct writes) and constructor
fallback compatibility layers have been removed from the slice touched by this branch.
"""
# Standard library
from pathlib import Path

# Third-party
import pytest

# Constants
_MANAGERS = Path("mcp_server/managers")
_QA_MANAGER = _MANAGERS / "qa_manager.py"
_SERVER = Path("mcp_server/server.py")


class TestQAManagerLegacyPathRemovalC8:
    """C8: Legacy state.json fallback paths must be absent from qa_manager.py."""

    def test_no_legacy_path_comment_in_qa_manager(self) -> None:
        """The '# Legacy path:' comment must not appear in qa_manager.py."""
        src = _QA_MANAGER.read_text(encoding="utf-8")
        assert "# Legacy path:" not in src, (
            "qa_manager.py still contains legacy state.json fallback path(s). "
            "Remove the else-branches that write directly to state.json."
        )

    def test_no_load_state_json_calls_in_qa_manager(self) -> None:
        """_load_state_json must not be called from baseline/accumulate/auto-scope methods."""
        src = _QA_MANAGER.read_text(encoding="utf-8")
        # _save_state_json and _load_state_json are internal helpers kept for backward
        # compat, but the state-mutation methods must no longer call them.
        # Count non-definition lines that call these helpers:
        calls = [
            ln for ln in src.splitlines()
            if ("_load_state_json(" in ln or "_save_state_json(" in ln)
            and not ln.strip().startswith("def ")
            and not ln.strip().startswith("#")
        ]
        assert calls == [], (
            f"qa_manager.py still calls _load_state_json/_save_state_json "
            f"outside helper definitions: {calls}"
        )


class TestServerQAManagerWiringC8:
    """C8: server.py must wire FileQualityStateRepository into QAManager."""

    def test_server_imports_file_quality_state_repository(self) -> None:
        """server.py must import FileQualityStateRepository."""
        src = _SERVER.read_text(encoding="utf-8")
        assert "FileQualityStateRepository" in src, (
            "server.py does not import FileQualityStateRepository. "
            "Add the import and wire it into QAManager."
        )

    def test_server_passes_quality_state_repository_to_qa_manager(self) -> None:
        """server.py must pass quality_state_repository= when constructing QAManager."""
        src = _SERVER.read_text(encoding="utf-8")
        assert "quality_state_repository=" in src, (
            "server.py does not pass quality_state_repository= to QAManager. "
            "Wire FileQualityStateRepository into the QAManager constructor call."
        )
