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

    def test_advance_baseline_has_no_save_state_json_call(self) -> None:
        """_advance_baseline_on_all_pass must not call _save_state_json (legacy write path)."""
        src = _QA_MANAGER.read_text(encoding="utf-8")
        # Extract only the _advance_baseline_on_all_pass method body
        method_start = src.find("def _advance_baseline_on_all_pass(")
        next_def = src.find("\n    def ", method_start + 1)
        method_body = src[method_start:next_def]
        assert "_save_state_json(" not in method_body, (
            "_advance_baseline_on_all_pass still calls _save_state_json. "
            "Remove the legacy state.json write path."
        )

    def test_accumulate_failed_has_no_save_state_json_call(self) -> None:
        """_accumulate_failed_files_on_failure must not call _save_state_json."""
        src = _QA_MANAGER.read_text(encoding="utf-8")
        method_start = src.find("def _accumulate_failed_files_on_failure(")
        next_def = src.find("\n    def ", method_start + 1)
        method_body = src[method_start:next_def]
        assert "_save_state_json(" not in method_body, (
            "_accumulate_failed_files_on_failure still calls _save_state_json. "
            "Remove the legacy state.json write path."
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
