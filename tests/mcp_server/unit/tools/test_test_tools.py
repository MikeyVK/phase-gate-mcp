"""Unit tests for RunTestsTool thin adapter.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.test_tools, tests.mcp_server.fixtures.fake_pytest_runner]
"""

import subprocess
from collections.abc import Awaitable, Callable

import pytest

from mcp_server.config.settings import Settings
from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import (
    InfoNote,
    NoteContext,
    RecoveryNote,
    SuggestionNote,
)
from mcp_server.managers.pytest_runner import FailureDetail, PytestResult
from mcp_server.tools.test_tools import RunTestsInput, RunTestsTool
from tests.mcp_server.fixtures.fake_pytest_runner import FakePytestRunner


@pytest.fixture
def injected_settings() -> Settings:
    """Provide explicit settings injection for RunTestsTool."""
    return Settings(server={"workspace_root": "/workspace"})


def _make_pytest_result(
    *,
    exit_code: int = 0,
    summary_line: str = "1 passed in 0.10s",
    passed: int = 1,
    failed: int = 0,
    skipped: int = 0,
    errors: int = 0,
    failures: tuple[FailureDetail, ...] = (),
    coverage_pct: float | None = None,
    lf_cache_was_empty: bool = False,
    should_raise: bool = False,
    note: RecoveryNote | SuggestionNote | InfoNote | None = None,
    is_error: bool = False,
    stderr: str = "",
) -> PytestResult:
    return PytestResult(
        exit_code=exit_code,
        summary_line=summary_line,
        passed=passed,
        failed=failed,
        skipped=skipped,
        errors=errors,
        failures=failures,
        coverage_pct=coverage_pct,
        lf_cache_was_empty=lf_cache_was_empty,
        should_raise=should_raise,
        note=note,
        is_error=is_error,
        stderr=stderr,
    )


def test_c1_fake_pytest_runner_run_accepts_verbose_kwarg() -> None:
    """FakePytestRunner.run accepts verbose keyword-only argument."""
    runner = FakePytestRunner(result=_make_pytest_result())
    runner.run(["pytest"], cwd=".", timeout=30, verbose=True)


class _TimeoutPytestRunner:
    def run(self, cmd: list[str], cwd: str, timeout: int) -> PytestResult:
        del cwd
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)


class _OSErrorPytestRunner:
    def run(self, cmd: list[str], cwd: str, timeout: int) -> PytestResult:
        del cmd, cwd, timeout
        raise OSError("Boom")


async def _execute_unwrapped(
    tool: RunTestsTool,
    params: RunTestsInput,
    context: NoteContext,
) -> object:
    raw_execute: Callable[[RunTestsTool, RunTestsInput, NoteContext], Awaitable[object]]
    raw_execute = RunTestsTool.execute.__wrapped__
    return await raw_execute(tool, params, context)


@pytest.mark.asyncio
async def test_c4_run_tests_all_passed_via_injected_runner(injected_settings: Settings) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(summary_line="2 passed in 0.45s", passed=2)
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    result = await tool.execute(RunTestsInput(path="tests/unit"), context)

    assert result.content[1]["text"] == "2 passed in 0.45s"
    assert result.content[0]["json"]["summary"]["passed"] == 2
    assert len(context.of_type(RecoveryNote)) == 0


@pytest.mark.asyncio
async def test_c4_run_tests_failed_result_contains_failures(injected_settings: Settings) -> None:
    failure = FailureDetail(
        test_id="tests/unit/test_foo.py::test_bar",
        location="tests/unit/test_foo.py",
        short_reason="AssertionError: nope",
        traceback="tests/unit/test_foo.py:5: AssertionError",
    )
    runner = FakePytestRunner(
        result=_make_pytest_result(
            exit_code=1,
            summary_line="1 failed, 2 passed in 0.20s",
            passed=2,
            failed=1,
            failures=(failure,),
        )
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

    assert result.content[0]["json"]["summary"]["failed"] == 1
    assert len(result.content[0]["json"]["failures"]) == 1
    assert result.content[0]["json"]["failures"][0]["test_id"] == failure.test_id


@pytest.mark.asyncio
async def test_c4_run_tests_interrupted_raises_execution_error(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(
            exit_code=2,
            summary_line="pytest interrupted (exit 2)",
            is_error=True,
            note=RecoveryNote("Pytest was interrupted; check for hung tests or external SIGINT."),
        )
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    result = await tool.execute(RunTestsInput(path="tests/unit"), context)

    assert result.is_error is True
    assert len(context.of_type(RecoveryNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_internal_error_raises_execution_error(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(
            exit_code=3,
            summary_line="pytest internal error (exit 3)",
            is_error=True,
            note=RecoveryNote(
                "Pytest reported an internal error; inspect stderr and pytest plugins."
            ),
        )
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    result = await tool.execute(RunTestsInput(path="tests/unit"), context)

    assert result.is_error is True
    assert len(context.of_type(RecoveryNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_usage_error_raises_execution_error(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(
            exit_code=4,
            summary_line="pytest usage error (exit 4)",
            is_error=True,
            note=RecoveryNote(
                "Pytest could not start. Verify the path exists and the CLI options are valid."
            ),
        )
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    result = await tool.execute(RunTestsInput(path="tests/unit"), context)

    assert result.is_error is True
    assert len(context.of_type(RecoveryNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_no_tests_collected_returns_suggestion_note(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(
            exit_code=5,
            summary_line="no tests collected",
            passed=0,
            failed=0,
            note=SuggestionNote("No tests matched the filter. Check markers and path."),
        )
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    result = await tool.execute(RunTestsInput(path="tests/unit"), context)

    assert result.content[1]["text"] == "no tests collected"
    assert len(context.of_type(SuggestionNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_unknown_exit_code_raises_execution_error(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(
            exit_code=99,
            summary_line="pytest exited with unexpected code",
            should_raise=True,
            note=RecoveryNote("Pytest exited with unexpected code 99; inspect stderr."),
        )
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    with pytest.raises(ExecutionError, match="pytest exited with returncode 99"):
        await _execute_unwrapped(tool, RunTestsInput(path="tests/unit"), context)

    assert len(context.of_type(RecoveryNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_lf_empty_emits_info_note_when_requested(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(result=_make_pytest_result(lf_cache_was_empty=True))
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    await tool.execute(RunTestsInput(path="tests/unit", last_failed_only=True), context)

    assert len(context.of_type(InfoNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_lf_cache_populated_emits_no_info_note(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(result=_make_pytest_result(lf_cache_was_empty=False))
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    await tool.execute(RunTestsInput(path="tests/unit", last_failed_only=True), context)

    assert len(context.of_type(InfoNote)) == 0


@pytest.mark.asyncio
async def test_c4_run_tests_lf_flag_ignored_when_not_requested(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(result=_make_pytest_result(lf_cache_was_empty=True))
    tool = RunTestsTool(runner=runner, settings=injected_settings)
    context = NoteContext()

    await tool.execute(RunTestsInput(path="tests/unit", last_failed_only=False), context)

    assert len(context.of_type(InfoNote)) == 0


@pytest.mark.asyncio
async def test_c4_run_tests_coverage_true_roundtrips_json(injected_settings: Settings) -> None:
    runner = FakePytestRunner(result=_make_pytest_result(coverage_pct=92.5))
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    result = await tool.execute(RunTestsInput(path="tests/unit", coverage=True), NoteContext())

    assert result.content[0]["json"]["coverage_pct"] == pytest.approx(92.5)


@pytest.mark.asyncio
async def test_c4_run_tests_coverage_false_roundtrips_none(injected_settings: Settings) -> None:
    runner = FakePytestRunner(result=_make_pytest_result(coverage_pct=None))
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    result = await tool.execute(RunTestsInput(path="tests/unit", coverage=False), NoteContext())

    assert result.content[0]["json"]["coverage_pct"] is None


@pytest.mark.asyncio
async def test_c4_run_tests_text_and_json_summary_stay_in_sync(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(
        result=_make_pytest_result(summary_line="3 passed in 0.30s", passed=3)
    )
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

    assert result.content[1]["text"] == result.content[0]["json"]["summary_line"]


@pytest.mark.asyncio
async def test_c4_run_tests_timeout_raises_execution_error(
    injected_settings: Settings,
) -> None:
    tool = RunTestsTool(runner=_TimeoutPytestRunner(), settings=injected_settings)
    context = NoteContext()

    with pytest.raises(ExecutionError, match="Tests timed out after 12s"):
        await _execute_unwrapped(tool, RunTestsInput(path="tests/unit", timeout=12), context)

    assert len(context.of_type(RecoveryNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_oserror_raises_execution_error(
    injected_settings: Settings,
) -> None:
    tool = RunTestsTool(runner=_OSErrorPytestRunner(), settings=injected_settings)
    context = NoteContext()

    with pytest.raises(ExecutionError, match="Failed to run tests: Boom"):
        await _execute_unwrapped(tool, RunTestsInput(path="tests/unit"), context)

    assert len(context.of_type(RecoveryNote)) == 1


@pytest.mark.asyncio
async def test_c4_run_tests_build_cmd_adds_coverage_packages(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(result=_make_pytest_result())
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    await tool.execute(RunTestsInput(path="tests/unit", coverage=True), NoteContext())

    assert runner.captured_cmd is not None
    assert "--cov=backend" in runner.captured_cmd
    assert "--cov=mcp_server" in runner.captured_cmd
    assert "--cov-branch" in runner.captured_cmd


@pytest.mark.asyncio
async def test_c4_run_tests_build_cmd_adds_fail_under_threshold(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(result=_make_pytest_result())
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    await tool.execute(RunTestsInput(path="tests/unit", coverage=True), NoteContext())

    assert runner.captured_cmd is not None
    assert "--cov-fail-under=90" in runner.captured_cmd


@pytest.mark.asyncio
async def test_c4_run_tests_build_cmd_omits_coverage_flags_when_disabled(
    injected_settings: Settings,
) -> None:
    runner = FakePytestRunner(result=_make_pytest_result())
    tool = RunTestsTool(runner=runner, settings=injected_settings)

    await tool.execute(RunTestsInput(path="tests/unit", coverage=False), NoteContext())

    assert runner.captured_cmd is not None
    assert not any(part.startswith("--cov") for part in runner.captured_cmd)


# ---------------------------------------------------------------------------
# C3 — _to_tool_result() routing split on result.is_error
# ---------------------------------------------------------------------------


class TestC3ToToolResultRouting:
    """C3: _to_tool_result() routes on result.is_error; exit 2/3/4 → ToolResult(is_error=True)."""

    @pytest.mark.asyncio
    async def test_c3_to_tool_result_exit1_is_error_false(
        self, injected_settings: Settings
    ) -> None:
        """Exit 1 (tests failed) → ToolResult(is_error=False)."""
        failure = FailureDetail(
            test_id="tests/unit/test_foo.py::test_bad",
            location="tests/unit/test_foo.py",
            short_reason="AssertionError: nope",
            traceback="",
        )
        runner = FakePytestRunner(
            result=_make_pytest_result(
                exit_code=1,
                summary_line="1 failed in 0.10s",
                failed=1,
                failures=(failure,),
                is_error=False,
            )
        )
        tool = RunTestsTool(runner=runner, settings=injected_settings)

        result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

        assert result.is_error is False

    @pytest.mark.asyncio
    async def test_c3_to_tool_result_exit1_content1_includes_failure_lines(
        self, injected_settings: Settings
    ) -> None:
        """Exit 1 + failure → content[0] text contains FAILED ... — ... line."""
        failure = FailureDetail(
            test_id="tests/unit/test_foo.py::test_bad",
            location="tests/unit/test_foo.py",
            short_reason="AssertionError: nope",
            traceback="",
        )
        runner = FakePytestRunner(
            result=_make_pytest_result(
                exit_code=1,
                summary_line="1 failed in 0.10s",
                failed=1,
                failures=(failure,),
                is_error=False,
            )
        )
        tool = RunTestsTool(runner=runner, settings=injected_settings)

        result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

        assert "FAILED tests/unit/test_foo.py::test_bad" in result.content[1]["text"]
        assert "AssertionError: nope" in result.content[1]["text"]

    @pytest.mark.asyncio
    async def test_c3_to_tool_result_exit2_returns_tool_result_is_error_true(
        self, injected_settings: Settings
    ) -> None:
        """Exit 2 (is_error=True) → ToolResult(is_error=True), not ExecutionError."""
        runner = FakePytestRunner(
            result=_make_pytest_result(
                exit_code=2,
                summary_line="pytest interrupted (exit 2)",
                is_error=True,
                note=RecoveryNote(
                    "Pytest was interrupted; check for hung tests or external SIGINT."
                ),
            )
        )
        tool = RunTestsTool(runner=runner, settings=injected_settings)

        result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

        assert result.is_error is True

    @pytest.mark.asyncio
    async def test_c3_to_tool_result_exit2_text_includes_summary_line(
        self, injected_settings: Settings
    ) -> None:
        """Exit 2 + non-empty stderr → content[0] text starts with summary_line."""
        runner = FakePytestRunner(
            result=_make_pytest_result(
                exit_code=2,
                summary_line="pytest interrupted (exit 2)",
                is_error=True,
                stderr="INTERNALERROR> some traceback\nmore lines",
            )
        )
        tool = RunTestsTool(runner=runner, settings=injected_settings)

        result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

        assert result.content[1]["text"].startswith("pytest interrupted (exit 2)")
        assert "INTERNALERROR" in result.content[1]["text"]

    @pytest.mark.asyncio
    async def test_c3_to_tool_result_payload_includes_stderr_tail(
        self, injected_settings: Settings
    ) -> None:
        """content[0] JSON payload always contains 'stderr' key."""
        runner = FakePytestRunner(
            result=_make_pytest_result(
                exit_code=0,
                summary_line="1 passed in 0.10s",
                stderr="",
            )
        )
        tool = RunTestsTool(runner=runner, settings=injected_settings)

        result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

        assert "stderr" in result.content[0]["json"]

    @pytest.mark.asyncio
    async def test_c3_to_tool_result_exit0_no_failures_text_is_summary_line(
        self, injected_settings: Settings
    ) -> None:
        """Exit 0, no failures → content[1] text == summary_line exactly."""
        runner = FakePytestRunner(
            result=_make_pytest_result(
                exit_code=0,
                summary_line="3 passed in 0.30s",
                passed=3,
                is_error=False,
            )
        )
        tool = RunTestsTool(runner=runner, settings=injected_settings)

        result = await tool.execute(RunTestsInput(path="tests/unit"), NoteContext())

        assert result.content[1]["text"] == "3 passed in 0.30s"
