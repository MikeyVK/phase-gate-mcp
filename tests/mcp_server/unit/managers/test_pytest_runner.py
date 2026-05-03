# tests/mcp_server/unit/managers/test_pytest_runner.py
"""Unit tests for PytestRunner — parser, exit-code classification, LF-cache detection.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.managers.pytest_runner]
"""

from __future__ import annotations

import subprocess

import pytest

import mcp_server.managers.pytest_runner as pytest_runner_module
from mcp_server.core.operation_notes import SuggestionNote
from mcp_server.managers.pytest_runner import FailureDetail, PytestResult, PytestRunner

# ---------------------------------------------------------------------------
# Stdout fixtures
# ---------------------------------------------------------------------------

_PASSED_STDOUT = """\
============================= test session starts ==============================
collected 3 items

tests/test_foo.py::test_a PASSED
tests/test_foo.py::test_b PASSED
tests/test_foo.py::test_c PASSED

============================== 3 passed in 0.12s ==============================
"""

_FAILED_STDOUT = """\
============================= test session starts ==============================
collected 2 items

tests/test_foo.py::test_ok PASSED
tests/test_foo.py::test_bad FAILED

================================= FAILURES =================================
________________________________ test_bad __________________________________

    def test_bad():
>       assert 1 == 2
E       AssertionError: assert 1 == 2

tests/test_foo.py:10: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_foo.py::test_bad - AssertionError: assert 1 == 2
========================= 1 failed, 1 passed in 0.23s =========================
"""

_SKIPPED_STDOUT = """\
============================= test session starts ==============================
collected 2 items

tests/test_foo.py::test_a PASSED
tests/test_foo.py::test_skip SKIPPED (reason)

========================= 1 passed, 1 skipped in 0.10s =========================
"""

_ERRORS_STDOUT = """\
============================= test session starts ==============================
collected 0 items / 1 error

==================================== ERRORS ====================================
__________________ ERROR collecting tests/test_bad_import.py ___________________
ImportError: cannot import name 'missing'
========================= 1 error in 0.05s =========================
"""

_COVERAGE_STDOUT = """\
============================= test session starts ==============================
collected 1 items

tests/test_foo.py::test_a PASSED

---------- coverage: platform linux, python 3.12 ----------
Name                                   Stmts   Miss Branch BrPart  Cover
TOTAL                                    250     10     40      4    96%

============================== 1 passed in 0.45s ==============================
"""

_LF_EMPTY_STDOUT = """\
============================= test session starts ==============================
run-last-failure: no previously failed tests, not deselecting.
collected 3 items

tests/test_foo.py::test_a PASSED

============================== 1 passed in 0.12s ==============================
"""

_EMPTY_STDOUT = ""

_NO_TESTS_STDOUT = """\
============================= test session starts ==============================
collected 0 items

============================ no tests ran in 0.01s ============================
"""


# ---------------------------------------------------------------------------
# Helper — exercise public PytestRunner.run() with a controlled subprocess seam
# ---------------------------------------------------------------------------


def _run(
    monkeypatch: pytest.MonkeyPatch,
    stdout: str,
    returncode: int,
    *,
    stderr: str = "",
) -> PytestResult:
    """Helper to exercise PytestRunner.run() through a controlled subprocess seam."""
    completed: subprocess.CompletedProcess[str] = subprocess.CompletedProcess(
        args=["pytest"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )

    def fake_run(
        cmd: list[str],
        *,
        capture_output: bool,
        check: bool,
        creationflags: int,
        cwd: str,
        env: dict[str, str],
        stdin: int,
        text: bool,
        timeout: int,
    ) -> subprocess.CompletedProcess[str]:
        assert cmd == ["pytest"]
        assert capture_output is True
        assert check is False
        assert creationflags >= 0
        assert cwd == "."
        assert env["PYTHONUNBUFFERED"] == "1"
        assert stdin == subprocess.DEVNULL
        assert text is True
        assert timeout == 30
        return completed

    monkeypatch.setattr(pytest_runner_module.subprocess, "run", fake_run)
    return PytestRunner().run(["pytest"], cwd=".", timeout=30)


# ---------------------------------------------------------------------------
# Test cases (8 scenarios per design.md §3.10)
# ---------------------------------------------------------------------------


class TestPytestRunnerRun:
    """Runner unit tests — exercise the public run() surface only."""

    def test_all_passed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 1: all-passed stdout → passed=N, failed=0, summary_line non-empty."""
        result = _run(monkeypatch, _PASSED_STDOUT, returncode=0)

        assert result.passed == 3
        assert result.failed == 0
        assert result.errors == 0
        assert result.failures == ()
        assert result.summary_line != ""
        assert result.exit_code == 0
        assert result.should_raise is False
        assert result.note is None

    def test_failing_tests(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 2: failing tests stdout → failures tuple populated with FailureDetail."""
        result = _run(monkeypatch, _FAILED_STDOUT, returncode=1)

        assert result.failed == 1
        assert result.passed == 1
        assert len(result.failures) == 1
        failure = result.failures[0]
        assert isinstance(failure, FailureDetail)
        assert "test_bad" in failure.test_id
        assert result.should_raise is False
        assert result.note is None

    def test_skipped_tests(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 3: skipped tests stdout → skipped=N."""
        result = _run(monkeypatch, _SKIPPED_STDOUT, returncode=0)

        assert result.skipped == 1
        assert result.passed == 1
        assert result.failed == 0

    def test_errors_during_collection(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 4: errors-during-collection stdout → errors=N."""
        result = _run(monkeypatch, _ERRORS_STDOUT, returncode=2)

        assert result.errors >= 1

    def test_coverage_pct_parsed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 5: coverage report line present → coverage_pct parsed as float."""
        result = _run(monkeypatch, _COVERAGE_STDOUT, returncode=0)

        assert result.coverage_pct is not None
        assert isinstance(result.coverage_pct, float)
        assert result.coverage_pct == pytest.approx(96.0)

    def test_lf_cache_was_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 6: LF empty fallback message in stdout → lf_cache_was_empty=True."""
        result = _run(monkeypatch, _LF_EMPTY_STDOUT, returncode=0)

        assert result.lf_cache_was_empty is True

    def test_empty_stdout_summary_line_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 7: empty/unparseable stdout → summary_line falls back to policy; never empty."""
        result = _run(monkeypatch, _EMPTY_STDOUT, returncode=2)

        assert result.summary_line != ""
        assert result.should_raise is False
        assert result.is_error is True

    def test_exit_code_5_no_tests_collected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario 8: exit code 5 path → summary_line == 'no tests collected'."""
        result = _run(monkeypatch, _NO_TESTS_STDOUT, returncode=5)

        assert result.summary_line == "no tests collected"
        assert result.should_raise is False
        assert isinstance(result.note, SuggestionNote)


# ---------------------------------------------------------------------------
# C1 — ExitCodePolicy + PytestResult contract
# ---------------------------------------------------------------------------


class TestC1ExitCodePolicyAndPytestResultContract:
    """C1: three-value Literal in ExitCodePolicy + PytestResult.is_error + PytestResult.stderr."""

    def test_c1_parse_output_exit2_sets_is_error_true(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exit 2 (INTERRUPTED) → result.is_error=True, result.should_raise=False."""
        result = _run(monkeypatch, _EMPTY_STDOUT, returncode=2)

        assert result.is_error is True
        assert result.should_raise is False

    def test_c1_parse_output_exit3_sets_is_error_true(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exit 3 (INTERNAL_ERROR) → result.is_error=True."""
        result = _run(monkeypatch, _EMPTY_STDOUT, returncode=3)

        assert result.is_error is True
        assert result.should_raise is False

    def test_c1_parse_output_exit4_sets_is_error_true(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exit 4 (USAGE_ERROR) → result.is_error=True."""
        result = _run(monkeypatch, _EMPTY_STDOUT, returncode=4)

        assert result.is_error is True
        assert result.should_raise is False

    def test_c1_parse_output_exit0_sets_is_error_false(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exit 0 (ALL_PASSED) → result.is_error=False."""
        result = _run(monkeypatch, _PASSED_STDOUT, returncode=0)

        assert result.is_error is False
        assert result.should_raise is False

    def test_c1_parse_output_exit99_should_raise_unchanged(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exit 99 (unknown) → result.should_raise=True, result.is_error=False — RNF-5 gate."""
        result = _run(monkeypatch, _EMPTY_STDOUT, returncode=99)

        assert result.should_raise is True
        assert result.is_error is False

    def test_c1_pytest_result_default_stderr_is_empty_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """PytestResult constructed without explicit stderr kwarg → result.stderr == ''."""
        result = _run(monkeypatch, _PASSED_STDOUT, returncode=0)

        assert result.stderr == ""


# ---------------------------------------------------------------------------
# C2 — stderr pipeline: run() → _parse_output() → PytestResult.stderr
# ---------------------------------------------------------------------------


class TestC2StderrPipeline:
    """C2: execution.stderr is wired through run() → _parse_output() → PytestResult.stderr."""

    def test_c2_run_passes_stderr_to_result(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Non-empty stderr from subprocess → result.stderr carries the value."""
        result = _run(monkeypatch, _PASSED_STDOUT, returncode=0, stderr="some error text")

        assert result.stderr == "some error text"

    def test_c2_run_empty_stderr_gives_empty_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Empty stderr from subprocess → result.stderr == ''."""
        result = _run(monkeypatch, _PASSED_STDOUT, returncode=0, stderr="")

        assert result.stderr == ""

    def test_c2_stderr_multiline_preserved_in_result(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Multi-line stderr → result.stderr contains all lines joined by newlines."""
        multiline = "line one\nline two\nline three"
        result = _run(monkeypatch, _EMPTY_STDOUT, returncode=2, stderr=multiline)

        assert result.stderr == multiline
