"""Tests for GitAdapter - extended git operations.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.adapters.git_adapter
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from git import Actor, GitCommandError, Repo
from git.remote import PushInfo

from mcp_server.adapters.git_adapter import GitAdapter
from mcp_server.core.exceptions import ExecutionError, MCPSystemError


def _mock_root() -> Path:
    return Path(__file__).resolve().parent / "mock-worktree"


def _mock_repository() -> MagicMock:
    repository = MagicMock()
    repository.bare = False
    repository.working_tree_dir = str(_mock_root())
    repository.git_dir = str(_mock_root() / ".git")
    repository.git.rev_parse.return_value = str(_mock_root())
    return repository


class TestGitAdapterCheckout:
    """Tests for checkout functionality."""

    def test_checkout_existing_branch(self) -> None:
        """Test checkout to existing branch."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_branch = MagicMock()
            mock_branch.name = "feature/test"
            mock_repo.heads.__iter__ = lambda _self: iter([mock_branch])
            mock_repo.heads.__contains__ = lambda _self, x: x == "feature/test"
            mock_repo.heads.__getitem__ = lambda _self, _x: mock_branch
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.checkout("feature/test")

            mock_branch.checkout.assert_called_once()
            # Performance invariant: fast path must NEVER call remote
            mock_repo.remote.assert_not_called()  # Cycle 4: S1 performance requirement

    def test_checkout_nonexistent_branch_raises_error(self) -> None:
        """Test checkout to non-existent branch raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads.__contains__ = lambda _self, _x: False
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="does not exist"):
                adapter.checkout("nonexistent")

    def test_checkout_remote_only_branch(self) -> None:
        """Test checkout creates local tracking branch from remote-only ref.

        Scenario S2: Remote-tracking ref exists, no local branch.
        Expected: Create local tracking branch and checkout.

        TDD Cycle 1 - RED: This test WILL FAIL until remote fallback implemented.
        """
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()

            # Setup: No local branch exists
            mock_repo.heads.__contains__ = lambda _self, _x: False

            # Setup: Origin remote with remote-tracking ref
            mock_origin = MagicMock()
            mock_remote_ref = MagicMock()
            mock_remote_ref.name = "origin/feature/test"
            mock_origin.refs = [mock_remote_ref]
            mock_repo.remote.return_value = mock_origin

            # Setup: create_head returns mock branch with tracking methods
            mock_local_branch = MagicMock()
            mock_repo.create_head.return_value = mock_local_branch

            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            # WHEN: Checkout remote-only branch
            adapter.checkout("feature/test")

            # THEN: Local tracking branch created from remote ref
            mock_repo.create_head.assert_called_once_with("feature/test", mock_remote_ref)
            mock_local_branch.set_tracking_branch.assert_called_once_with(mock_remote_ref)
            mock_local_branch.checkout.assert_called_once()

    def test_checkout_strips_origin_prefix(self) -> None:
        """Test checkout normalizes origin/ prefix in input.

        Scenario S5: User provides 'origin/feature/test' as input.
        Expected: Prefix stripped, local branch created as 'feature/test'.

        TDD Cycle 2 - RED: This test WILL FAIL until prefix normalization added.
        """
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()

            # Setup: No local branch exists
            mock_repo.heads.__contains__ = lambda _self, _x: False

            # Setup: Origin remote with remote-tracking ref
            mock_origin = MagicMock()
            mock_remote_ref = MagicMock()
            mock_remote_ref.name = "origin/feature/test"
            mock_origin.refs = [mock_remote_ref]
            mock_repo.remote.return_value = mock_origin

            # Setup: create_head returns mock branch
            mock_local_branch = MagicMock()
            mock_repo.create_head.return_value = mock_local_branch

            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            # WHEN: Checkout WITH origin/ prefix
            adapter.checkout("origin/feature/test")

            # THEN: Prefix stripped, local branch "feature/test" created
            # NOT: create_head("origin/feature/test", ...)
            mock_repo.create_head.assert_called_once_with("feature/test", mock_remote_ref)
            mock_local_branch.set_tracking_branch.assert_called_once_with(mock_remote_ref)
            mock_local_branch.checkout.assert_called_once()

    def test_checkout_no_origin_remote(self) -> None:
        """Test checkout raises clear error when origin not configured.

        Scenario S3: No local branch, no origin remote.
        Expected: ExecutionError with "Origin remote not configured" message.

        TDD Cycle 3A - RED: This test WILL FAIL until ValueError caught explicitly.
        """
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()

            # Setup: No local branch exists
            mock_repo.heads.__contains__ = lambda _self, _x: False

            # Setup: No origin remote (ValueError when accessed)
            mock_repo.remote.side_effect = ValueError("Remote 'origin' not found")

            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            # WHEN/THEN: Checkout raises descriptive error
            with pytest.raises(ExecutionError, match="Origin remote not configured"):
                adapter.checkout("feature/test")

    def test_checkout_branch_missing_everywhere(self) -> None:
        """Test checkout error includes actionable hint.

        Scenario S4: No local branch, origin configured, no remote-tracking refs.
        Expected: ExecutionError with exhaustive search message AND git_fetch hint.

        Issue #144: RED phase - test expects hint in error message.
        """
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()

            # Setup: No local branch exists
            mock_repo.heads.__contains__ = lambda _self, _x: False

            # Setup: Origin configured, but no remote-tracking refs
            mock_origin = MagicMock()
            mock_origin.refs = []  # Empty - no branches on remote
            mock_repo.remote.return_value = mock_origin

            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            # WHEN/THEN: Error message includes exhaustive search AND hint
            with pytest.raises(
                ExecutionError,
                match=r"does not exist \(checked: local, origin\)\. Hint: Run git_fetch",
            ):
                adapter.checkout("missing")


class TestGitAdapterPush:
    """Tests for push functionality."""

    def test_push_to_origin_success(self) -> None:
        """Test push to origin remote with success flag."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_origin = MagicMock()
            mock_repo.remotes.__iter__ = lambda _self: iter([mock_origin])
            mock_repo.remotes.__contains__ = lambda _self, _x: _x == "origin"
            mock_repo.remote.return_value = mock_origin
            mock_repo.active_branch.name = "feature/test"
            mock_info = MagicMock()
            mock_info.flags = PushInfo.FAST_FORWARD
            mock_info.summary = "Fast-forward"
            mock_origin.push.return_value = [mock_info]
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.push()

            mock_origin.push.assert_called_once()

    def test_push_with_set_upstream_success(self) -> None:
        """Test push with --set-upstream flag."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_origin = MagicMock()
            mock_repo.remotes.__contains__ = lambda _self, _x: _x == "origin"
            mock_repo.remote.return_value = mock_origin
            mock_repo.active_branch.name = "feature/new"
            mock_info = MagicMock()
            mock_info.flags = PushInfo.NEW_HEAD
            mock_info.summary = "New head"
            mock_origin.push.return_value = [mock_info]
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.push(set_upstream=True)

            mock_origin.push.assert_called_once()

    def test_push_no_remote_raises_error(self) -> None:
        """Test push without origin remote raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.remotes.__iter__ = lambda _self: iter([])
            mock_repo.remote.side_effect = ValueError("Remote origin not found")
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="origin"):
                adapter.push()

    def test_push_rejected_by_remote_raises_execution_error(self) -> None:
        """Test push rejected by remote (non-fast-forward) raises ExecutionError with summary."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_origin = MagicMock()
            mock_repo.remotes.__contains__ = lambda _self, _x: _x == "origin"
            mock_repo.remote.return_value = mock_origin
            mock_repo.active_branch.name = "feature/test"
            mock_info = MagicMock()
            mock_info.flags = PushInfo.REJECTED
            mock_info.summary = "[rejected] (non-fast-forward)"
            mock_origin.push.return_value = [mock_info]
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(
                ExecutionError,
                match=r"Push rejected by remote: \[rejected\] \(non-fast-forward\)",
            ):
                adapter.push()

    @pytest.mark.parametrize(
        ("flag", "summary_text"),
        [
            (PushInfo.ERROR, "General push error"),
            (PushInfo.REMOTE_REJECTED, "[remote rejected] (pre-receive hook declined)"),
            (PushInfo.REMOTE_FAILURE, "Remote failure occurred"),
        ],
    )
    def test_push_error_flags_raise_execution_error(self, flag: int, summary_text: str) -> None:
        """Test push encountering various GitPython error flags raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_origin = MagicMock()
            mock_repo.remotes.__contains__ = lambda _self, _x: _x == "origin"
            mock_repo.remote.return_value = mock_origin
            mock_repo.active_branch.name = "feature/test"
            mock_info = MagicMock()
            mock_info.flags = flag
            mock_info.summary = summary_text
            mock_origin.push.return_value = [mock_info]
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match=r"Push rejected by remote"):
                adapter.push()

    def test_push_empty_result_list_raises_execution_error(self) -> None:
        """Test empty push result list raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_origin = MagicMock()
            mock_repo.remotes.__contains__ = lambda _self, _x: _x == "origin"
            mock_repo.remote.return_value = mock_origin
            mock_repo.active_branch.name = "feature/test"
            mock_origin.push.return_value = []
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="No push status returned by remote"):
                adapter.push()

    @pytest.mark.parametrize(
        "success_flag",
        [
            PushInfo.NEW_HEAD,
            PushInfo.NEW_TAG,
            PushInfo.FAST_FORWARD,
            PushInfo.UP_TO_DATE,
            PushInfo.FORCED_UPDATE,
        ],
    )
    def test_push_success_flags_do_not_raise(self, success_flag: int) -> None:
        """Test valid push success flags execute cleanly without raising exceptions."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_origin = MagicMock()
            mock_repo.remotes.__contains__ = lambda _self, _x: _x == "origin"
            mock_repo.remote.return_value = mock_origin
            mock_repo.active_branch.name = "feature/test"
            mock_info = MagicMock()
            mock_info.flags = success_flag
            mock_info.summary = "OK"
            mock_origin.push.return_value = [mock_info]
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.push()


class TestGitAdapterMerge:
    """Tests for merge functionality."""

    def test_merge_branch(self) -> None:
        """Test merge branch into current."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads.__contains__ = lambda _self, _x: _x == "feature/test"
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.merge("feature/test")

            mock_repo.git.merge.assert_called_once_with("feature/test")

    def test_merge_nonexistent_branch_raises_error(self) -> None:
        """Test merge non-existent branch raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads.__contains__ = lambda _self, _x: False
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="does not exist"):
                adapter.merge("nonexistent")


class TestGitAdapterDeleteBranch:
    """Tests for branch deletion."""

    def test_delete_branch(self) -> None:
        """Test delete a branch."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads.__contains__ = lambda _self, _x: _x == "feature/test"
            mock_repo.active_branch.name = "main"
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.delete_local_branch("feature/test")

            mock_repo.delete_head.assert_called_once_with("feature/test", force=False)

    def test_delete_current_branch_raises_error(self) -> None:
        """Test cannot delete current branch."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.active_branch.name = "feature/test"
            mock_repo.heads.__contains__ = lambda _self, _x: _x == "feature/test"
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="current branch"):
                adapter.delete_local_branch("feature/test")

    def test_delete_nonexistent_branch_raises_error(self) -> None:
        """Test delete non-existent branch raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads.__contains__ = lambda _self, _x: False
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            with pytest.raises(ExecutionError, match="does not exist"):
                adapter.delete_local_branch("nonexistent")


class TestGitAdapterDeleteRemoteBranch:
    """Tests for remote branch deletion."""

    def test_delete_remote_branch_deleted(self) -> None:
        """Test successful remote branch deletion returns 'deleted'."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_remote = MagicMock()
            mock_ref = MagicMock()
            mock_ref.name = "origin/feature/old"
            mock_remote.refs = [mock_ref]
            mock_repo.remote.return_value = mock_remote
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            result = adapter.delete_remote_branch("feature/old")

            assert result == "deleted"
            mock_repo.git.push.assert_called_once_with("origin", "--delete", "feature/old")

    def test_delete_remote_branch_absent_returns_absent(self) -> None:
        """Test absent remote branch returns 'absent', not an error."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_remote = MagicMock()
            mock_remote.refs = []
            mock_repo.remote.return_value = mock_remote
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            result = adapter.delete_remote_branch("feature/old")

            assert result == "absent"
            mock_repo.git.push.assert_not_called()

    def test_delete_remote_branch_no_origin_raises_error(self) -> None:
        """Test missing origin remote raises ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.remote.side_effect = ValueError("Remote 'origin' not found")
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            with pytest.raises(ExecutionError, match="not configured"):
                adapter.delete_remote_branch("feature/old")


class TestGitAdapterStash:
    """Tests for git stash functionality."""

    def test_stash_changes(self) -> None:
        """Test stash current changes."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.stash()

            mock_repo.git.stash.assert_called_once_with("push")

    def test_stash_changes_include_untracked(self) -> None:
        """Test stash current changes including untracked files (-u)."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.stash(include_untracked=True)

            mock_repo.git.stash.assert_called_once_with("push", "-u")

    def test_stash_with_message(self) -> None:
        """Test stash with custom message."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.stash(message="WIP: feature work")

            mock_repo.git.stash.assert_called_once_with("push", "-m", "WIP: feature work")

    def test_stash_with_message_include_untracked(self) -> None:
        """Test stash with message including untracked files (-u)."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.stash(message="WIP: feature work", include_untracked=True)

            mock_repo.git.stash.assert_called_once_with("push", "-u", "-m", "WIP: feature work")

    def test_stash_pop(self) -> None:
        """Test pop the latest stash."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.stash_pop()

            mock_repo.git.stash.assert_called_once_with("pop")

    def test_stash_list(self) -> None:
        """Test list all stashes."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.git.stash.return_value = (
                "stash@{0}: WIP on main: abc1234 commit msg\n"
                "stash@{1}: On feature: def5678 another msg"
            )
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            result = adapter.stash_list()

            mock_repo.git.stash.assert_called_once_with("list")
            assert len(result) == 2
            assert "stash@{0}" in result[0]

    def test_stash_list_empty(self) -> None:
        """Test list stashes when none exist."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.git.stash.return_value = ""
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            result = adapter.stash_list()

            assert result == []

    def test_stash_error_handling(self) -> None:
        """Test stash error is wrapped in ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.git.stash.side_effect = Exception("Git error")
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="stash"):
                adapter.stash()

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="does not exist"):
                adapter.delete_local_branch("nonexistent")


class TestGitAdapterCommit:
    """Tests for git commit functionality."""

    def test_commit_stages_all_when_files_none(self) -> None:
        """Test commit stages all changes when files is omitted."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_commit = MagicMock()
            mock_commit.hexsha = "abc1234"
            mock_repo.index.commit.return_value = mock_commit
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            result = adapter.commit("msg")

            assert result == "abc1234"
            mock_repo.git.add.assert_called_once_with(".")
            mock_repo.index.commit.assert_called_once_with("msg")

    def test_commit_stages_only_given_files(self) -> None:
        """Test commit stages only provided files."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_commit = MagicMock()
            mock_commit.hexsha = "abc1234"
            mock_repo.index.commit.return_value = mock_commit
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            result = adapter.commit("msg", files=["a.py", "docs/readme.md"])

            assert result == "abc1234"
            mock_repo.git.add.assert_called_once_with("a.py", "docs/readme.md")
            mock_repo.index.commit.assert_called_once_with("msg")


class TestGitAdapterRestore:
    """Tests for git restore functionality."""

    def test_restore_calls_git_restore_for_files(self) -> None:
        """Test restore delegates to `git restore` with correct args."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.restore(files=["a.py", "b.py"], source="HEAD")

            mock_repo.git.restore.assert_called_once_with(
                "--source=HEAD",
                "--staged",
                "--worktree",
                "--",
                "a.py",
                "b.py",
            )

    def test_restore_wraps_errors_in_execution_error(self) -> None:
        """Test restore errors are wrapped in ExecutionError."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.git.restore.side_effect = Exception("Git error")
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            with pytest.raises(ExecutionError, match="restore"):
                adapter.restore(files=["a.py"], source="HEAD")


class TestGitAdapterCreateBranch:
    """Tests for create_branch functionality (Issue #64 - TDD RED phase)."""

    def test_create_branch_requires_explicit_base(self) -> None:
        """RED: Should fail when base parameter missing (no default allowed)."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            # Should require base parameter (no default)
            with pytest.raises(TypeError, match="base"):
                adapter.create_branch("test-branch")  # Missing base parameter

    def test_create_branch_with_head(self) -> None:
        """RED: Should create from current HEAD when base='HEAD'."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_head = MagicMock()
            mock_commit = MagicMock()
            mock_commit.hexsha = "abc123f"
            mock_head.commit = mock_commit
            mock_repo.head = mock_head
            mock_repo.heads = []
            mock_new_branch = MagicMock()
            mock_repo.create_head.return_value = mock_new_branch
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.create_branch("test-branch", base="HEAD")

            # Should resolve HEAD to commit and create from it
            mock_repo.create_head.assert_called_once_with("test-branch", mock_commit)
            mock_new_branch.checkout.assert_not_called()

    def test_create_branch_with_branch_name(self) -> None:
        """RED: Should create from specified branch name."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads = []
            mock_new_branch = MagicMock()
            mock_repo.create_head.return_value = mock_new_branch
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.create_branch("test-branch", base="main")

            # Should pass branch name directly to create_head
            mock_repo.create_head.assert_called_once_with("test-branch", "main")
            mock_new_branch.checkout.assert_not_called()

    def test_create_branch_with_commit_hash(self) -> None:
        """RED: Should create from specific commit hash."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.heads = []
            mock_new_branch = MagicMock()
            mock_repo.create_head.return_value = mock_new_branch
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.create_branch("test-branch", base="abc123f")

            # Should pass commit hash directly
            mock_repo.create_head.assert_called_once_with("test-branch", "abc123f")
            mock_new_branch.checkout.assert_not_called()

    def test_create_branch_already_exists_raises_error(self) -> None:
        """RED: Should fail when branch already exists."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_branch = MagicMock()
            mock_branch.name = "existing-branch"
            # Use MagicMock list-like behavior instead of setting __contains__
            mock_repo.heads = MagicMock()
            mock_repo.heads.__iter__ = lambda _self: iter([mock_branch])
            mock_repo.heads.__contains__ = lambda _self, _x: _x == "existing-branch"
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="already exists"):
                adapter.create_branch("existing-branch", base="main")

    def test_create_branch_logs_operation(self) -> None:
        """GREEN: Should log branch creation with all relevant details."""
        with (
            patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class,
            patch("mcp_server.core.logging.get_logger") as mock_logger,
        ):
            mock_repo = _mock_repository()
            mock_repo.heads = []
            mock_new_branch = MagicMock()
            mock_repo.create_head.return_value = mock_new_branch
            mock_repo_class.return_value = mock_repo

            mock_log = MagicMock()
            mock_logger.return_value = mock_log

            adapter = GitAdapter(str(_mock_root()))
            adapter.create_branch("test-branch", base="main")

            # Should log the operation
            assert mock_log.debug.called or mock_log.info.called


class TestGitAdapterHardResetAndForcePush:
    """Tests for hard_reset and force_push_with_lease (Issue #295 — Cycle 1 RED).

    Both methods are raw git primitives required by GitManager.prepare_submission
    and GitManager.rollback_push.
    """

    def test_hard_reset_calls_git_reset_hard_with_ref(self) -> None:
        """hard_reset('HEAD') must call repo.git.reset('--hard', 'HEAD')."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.hard_reset("HEAD")

            mock_repo.git.reset.assert_called_once_with("--hard", "HEAD")

    def test_hard_reset_calls_git_reset_hard_with_parent(self) -> None:
        """hard_reset('HEAD~1') must call repo.git.reset('--hard', 'HEAD~1')."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.hard_reset("HEAD~1")

            mock_repo.git.reset.assert_called_once_with("--hard", "HEAD~1")

    def test_hard_reset_raises_execution_error_on_failure(self) -> None:
        """hard_reset raises ExecutionError when git reset fails."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.git.reset.side_effect = Exception("git error: ref not found")
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="Failed to hard reset"):
                adapter.hard_reset("HEAD~1")

    def test_force_push_with_lease_calls_git_push(self) -> None:
        """force_push_with_lease must call repo.git.push with --force-with-lease."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.active_branch.name = "bug/295-test"
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))
            adapter.force_push_with_lease()

            mock_repo.git.push.assert_called_once_with("origin", "--force-with-lease")

    def test_force_push_with_lease_raises_execution_error_on_failure(self) -> None:
        """force_push_with_lease raises ExecutionError when git push fails."""
        with patch("mcp_server.adapters.git_adapter.Repo") as mock_repo_class:
            mock_repo = _mock_repository()
            mock_repo.active_branch.name = "bug/295-test"
            mock_repo.git.push.side_effect = Exception("rejected: stale info")
            mock_repo_class.return_value = mock_repo

            adapter = GitAdapter(str(_mock_root()))

            with pytest.raises(ExecutionError, match="Failed to force push"):
                adapter.force_push_with_lease()


@pytest.mark.slow
def test_local_remote_roundtrip_preserves_commits_and_stashed_content(tmp_path: Path) -> None:
    root = tmp_path / "work"
    repository = Repo.init(root, initial_branch="main")
    remote = Repo.init(tmp_path / "remote.git", bare=True)
    with repository.config_writer() as configuration:
        configuration.set_value("user", "name", "Adapter scenario")
        configuration.set_value("user", "email", "adapter@example.invalid")
    repository.create_remote("origin", str(remote.working_dir or remote.git_dir))
    adapter = GitAdapter(str(root))
    target = root / "artifact.txt"
    target.write_text("initial\n", encoding="utf-8")
    try:
        initial = adapter.commit("Initial artifact")
        assert adapter.is_clean()
        assert adapter.get_status()["branch"] == "main"
        assert not adapter.has_upstream()
        adapter.push(set_upstream=True)
        assert adapter.has_upstream()
        assert "origin" in adapter.fetch(prune=True)
        assert adapter.pull()
        assert any("origin/main" in branch for branch in adapter.list_branches(remote=True))

        adapter.create_branch("feature/roundtrip", base="main")
        adapter.checkout("feature/roundtrip")
        target.write_text("committed change\n", encoding="utf-8")
        changed = adapter.commit("Change artifact")
        assert adapter.has_net_diff_for_path("artifact.txt", "main")
        assert "artifact.txt" in adapter.get_diff_stat("main")
        assert adapter.is_ancestor(initial)
        assert adapter.get_recent_commits()[0] == "Change artifact"

        target.write_text("pending change\n", encoding="utf-8")
        untracked = root / "new.txt"
        untracked.write_text("untracked content\n", encoding="utf-8")
        adapter.stash(message="pending artifact", include_untracked=True)
        assert target.read_text(encoding="utf-8") == "committed change\n"
        assert not untracked.exists() and adapter.stash_list()
        adapter.stash_pop()
        assert target.read_text(encoding="utf-8") == "pending change\n"
        assert untracked.read_text(encoding="utf-8") == "untracked content\n"
        adapter.restore(["artifact.txt"])
        untracked.unlink()

        adapter.checkout("main")
        adapter.merge("feature/roundtrip")
        assert adapter.is_ancestor(changed)
        adapter.delete_local_branch("feature/roundtrip")
        assert all(
            "feature/roundtrip" not in branch for branch in adapter.list_branches(verbose=True)
        )
        assert target.read_text(encoding="utf-8") == "committed change\n"
        repository.git.checkout(initial)
        assert adapter.get_current_branch() == "HEAD"
        assert not adapter.has_upstream()
    finally:
        adapter.repo.close()
        repository.close()
        remote.close()


@pytest.mark.parametrize(
    ("operation", "backend_path", "parameters"),
    [
        ("fetch", "remote", ()),
        ("pull", "remote", ()),
        ("has_upstream", "active_branch.tracking_branch", ()),
        ("list_branches", "git.branch", ()),
        ("get_diff_stat", "git.diff", ("main",)),
        ("has_net_diff_for_path", "git.merge_base", ("artifact.txt", "main")),
        ("has_net_diff_for_path", "git.diff", ("artifact.txt", "main")),
    ],
)
def test_native_command_failures_preserve_the_cause(
    operation: str, backend_path: str, parameters: tuple[str, ...]
) -> None:
    failure = GitCommandError("git operation", 128, stderr="native failure sentinel")
    repository = _mock_repository()
    command = repository
    for segment in backend_path.split("."):
        command = getattr(command, segment)
    command.side_effect = failure
    with patch("mcp_server.adapters.git_adapter.Repo", return_value=repository):
        adapter = GitAdapter(str(_mock_root()))
        with pytest.raises(ExecutionError) as captured:
            getattr(adapter, operation)(*parameters)
    assert captured.value.__cause__ is failure


@pytest.mark.parametrize("status", [1, 128])
def test_ancestry_distinguishes_a_negative_answer_from_native_failure(status: int) -> None:
    failure = GitCommandError("git merge-base", status, stderr="ancestry diagnostic")
    repository = _mock_repository()
    repository.git.merge_base.side_effect = failure
    with patch("mcp_server.adapters.git_adapter.Repo", return_value=repository):
        adapter = GitAdapter(str(_mock_root()))
        if status == 1:
            assert adapter.is_ancestor("candidate") is False
        else:
            with pytest.raises(ExecutionError) as captured:
                adapter.is_ancestor("candidate")
            assert captured.value.__cause__ is failure


@pytest.mark.parametrize("missing", [False, True])
def test_unusable_repository_retains_the_native_diagnostic(tmp_path: Path, missing: bool) -> None:
    root = tmp_path / "repository"
    if not missing:
        root.mkdir()
    adapter = GitAdapter(str(root))
    with pytest.raises(ExecutionError) as captured:
        adapter.get_current_branch()
    access_error = captured.value.__cause__
    assert isinstance(access_error, MCPSystemError)
    assert access_error.__cause__ is not None


def _initialized_repository(root: Path, branch: str = "main") -> Repo:
    repository = Repo.init(root, initial_branch=branch)
    actor = Actor("Workspace scenario", "workspace@example.invalid")
    marker = root / "artifact.txt"
    marker.write_text("baseline\n", encoding="utf-8")
    repository.index.add(["artifact.txt"])
    repository.index.commit("Baseline", author=actor, committer=actor)
    return repository


def _repository_snapshot(repository: Repo) -> tuple[str, bytes, bytes, tuple[str, ...]]:
    return (
        repository.head.commit.hexsha,
        (Path(repository.git_dir) / "index").read_bytes(),
        (Path(repository.working_dir) / "artifact.txt").read_bytes(),
        tuple(head.name for head in repository.heads),
    )


def test_selected_worktree_commit_ignores_launch_and_later_native_redirect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = _initialized_repository(tmp_path / "selected", "selected")
    foreign = _initialized_repository(tmp_path / "foreign", "foreign")
    adapter = GitAdapter(str(tmp_path / "selected"))
    before = _repository_snapshot(foreign)
    try:
        monkeypatch.chdir(tmp_path / "foreign")
        assert adapter.get_status()["branch"] == "selected"
        with selected.config_writer() as configuration:
            configuration.set_value("core", "worktree", str(tmp_path / "foreign"))
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GIT_AUTHOR_NAME", "Explicit native author")
        monkeypatch.setenv("GIT_AUTHOR_EMAIL", "native@example.invalid")
        monkeypatch.setenv("GIT_COMMITTER_NAME", "Explicit native author")
        monkeypatch.setenv("GIT_COMMITTER_EMAIL", "native@example.invalid")
        (tmp_path / "selected" / "artifact.txt").write_text("selected change\n", encoding="utf-8")
        committed = adapter.commit("Selected change", files=["artifact.txt"])
        assert selected.head.commit.hexsha == committed
        assert selected.head.commit.author.name == "Explicit native author"
        assert selected.head.commit.tree[
            "artifact.txt"
        ].data_stream.read().decode().splitlines() == ["selected change"]
        assert _repository_snapshot(foreign) == before
    finally:
        adapter.repo.close()
        selected.close()
        foreign.close()


@pytest.mark.parametrize(
    "selector",
    [
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_COMMON_DIR",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_NAMESPACE",
        "GIT_SHALLOW_FILE",
        "GIT_GRAFT_FILE",
    ],
)
def test_native_selector_refuses_first_and_cached_writes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, selector: str
) -> None:
    repository = _initialized_repository(tmp_path / "selected")
    before = _repository_snapshot(repository)
    adapter = GitAdapter(str(tmp_path / "selected"))
    cached = adapter.repo
    try:
        with monkeypatch.context() as context:
            context.setenv(selector, "")
            for candidate in (adapter, GitAdapter(str(tmp_path / "selected"))):
                with pytest.raises(ExecutionError) as captured:
                    candidate.commit("Must not write", files=["artifact.txt"])
                error = captured.value.__cause__
                assert isinstance(error, MCPSystemError)
                assert "native_context_override" in str(error) and selector in str(error)
        assert _repository_snapshot(repository) == before
    finally:
        cached.close()
        repository.close()


@pytest.mark.parametrize("kind", ["subdirectory", "container", "bare", "administrative"])
def test_non_worktree_roots_never_search_for_another_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    repository = _initialized_repository(tmp_path / "foreign")
    before = _repository_snapshot(repository)
    bare = None
    if kind == "subdirectory":
        root = tmp_path / "foreign" / "child"
        root.mkdir()
    elif kind == "container":
        root = tmp_path
        other = _initialized_repository(tmp_path / "other")
        other.close()
    elif kind == "bare":
        root = tmp_path / "bare.git"
        bare = Repo.init(root, bare=True)
    else:
        root = Path(repository.git_dir)
    try:
        monkeypatch.chdir(tmp_path / "foreign")
        with pytest.raises(ExecutionError) as captured:
            GitAdapter(str(root)).commit("Must not write", files=["artifact.txt"])
        assert isinstance(captured.value.__cause__, MCPSystemError)
        assert _repository_snapshot(repository) == before
    finally:
        repository.close()
        if bare is not None:
            bare.close()


def test_nested_and_linked_worktrees_keep_their_own_identity(tmp_path: Path) -> None:
    outer = _initialized_repository(tmp_path / "outer", "outer")
    nested = _initialized_repository(tmp_path / "outer" / "nested", "nested")
    linked_root = tmp_path / "linked"
    outer.git.worktree("add", str(linked_root), "-b", "linked")
    adapters = [
        GitAdapter(str(tmp_path / "outer")),
        GitAdapter(str(tmp_path / "outer" / "nested")),
        GitAdapter(str(linked_root)),
    ]
    try:
        assert [adapter.get_current_branch() for adapter in adapters] == [
            "outer",
            "nested",
            "linked",
        ]
        adapters[2].create_branch("linked-only", "HEAD")
        assert "linked-only" in outer.heads and "linked-only" not in nested.heads
    finally:
        for adapter in adapters:
            adapter.repo.close()
        nested.close()
        outer.close()


def test_initial_native_worktree_redirect_is_refused(tmp_path: Path) -> None:
    selected = _initialized_repository(tmp_path / "selected")
    foreign = _initialized_repository(tmp_path / "foreign")
    before = _repository_snapshot(foreign)
    adapter = GitAdapter(str(tmp_path / "selected"))
    with selected.config_writer() as configuration:
        configuration.set_value("core", "worktree", str(tmp_path / "foreign"))
    try:
        with pytest.raises(ExecutionError) as captured:
            adapter.commit("Must not write", files=["artifact.txt"])
        assert isinstance(captured.value.__cause__, MCPSystemError)
        assert "native_worktree_mismatch" in str(captured.value.__cause__)
        assert _repository_snapshot(foreign) == before
        with selected.config_writer() as configuration:
            configuration.set_value("core", "worktree", str(tmp_path / "selected"))
        assert adapter.get_current_branch() == "main"
        adapter.repo.close()
    finally:
        selected.close()
        foreign.close()
