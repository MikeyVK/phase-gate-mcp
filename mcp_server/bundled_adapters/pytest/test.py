"""Native Pytest test/v1 adapter; native options and results retain their meanings."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

_KEYS = frozenset({"operation", "targets", "args"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")


class _MetadataGuard:
    """Reject native metadata modes after Pytest has parsed all option sources."""

    def pytest_cmdline_main(self, config: pytest.Config) -> int | None:
        if config.option.help or config.option.version:
            sys.stderr.write("ERROR: Native metadata requests do not perform testing.\n")
            return 4
        return None


def _invalid(location: list[str | int], code: str) -> dict[str, object]:
    return {"reason": "invalid_request", "details": [{"location": location, "code": code}]}


def _validate(value: object) -> tuple[tuple[str, ...], tuple[str, ...]] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([], "wrong_type")
    unknown = sorted(str(key) for key in set(value) - _KEYS)
    missing = sorted(_KEYS - set(value))
    if unknown:
        return _invalid([unknown[0]], "unknown_field")
    if missing:
        return _invalid([missing[0]], "missing_field")
    if not isinstance(value["operation"], str):
        return _invalid(["operation"], "wrong_type")
    if value["operation"] != "tests":
        return _invalid(["operation"], "invalid_value")
    for field in ("targets", "args"):
        if not isinstance(value[field], list):
            return _invalid([field], "wrong_type")
        for index, item in enumerate(value[field]):
            if not isinstance(item, str):
                return _invalid([field, index], "wrong_type")
            if field == "targets" and (
                not item or "\x00" in item or _ABSOLUTE_PATH.fullmatch(item) is None
            ):
                return _invalid([field, index], "invalid_value")
    return tuple(value["targets"]), tuple(value["args"])


def _response(
    status: str,
    message: str,
    version: str | None,
    *,
    reason: str | None = None,
    evidence: str = "",
) -> tuple[dict[str, object], int]:
    decision = {"status": status, "message": message}
    if reason is not None:
        decision["reason"] = reason
    result: dict[str, object] = {
        "decision": decision,
        "external_tools": [{"tool_id": "pytest", "version": version}],
    }
    if evidence:
        result["evidence"] = {"format": "text", "data": evidence}
    return result, {"passed": 0, "failed": 1, "unavailable": 3}[status]


def _unavailable(
    reason: str,
    message: str,
    version: str | None = None,
    evidence: str = "",
) -> tuple[dict[str, object], int]:
    return _response("unavailable", message, version, reason=reason, evidence=evidence)


def _streams(result: subprocess.CompletedProcess[bytes]) -> tuple[str, str, str]:
    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")
    evidence = stdout
    if stderr:
        evidence = f"{stdout}\nstderr:\n{stderr}" if stdout else stderr
    return stdout, stderr, evidence


def _usage_reason(stderr: str) -> str:
    # Native 9.0.2 reports parse/config-loader failures with their actual source filename.
    if re.search(r"(?m)^ERROR: .+\.(?:toml|ini|cfg):", stderr) or stderr.startswith(
        "ImportError while loading conftest"
    ):
        return "invalid_configuration"
    if "ERROR: Missing required plugins:" in stderr:
        return "dependency_unavailable"
    return "unsupported_input"


def _run(value: object) -> tuple[dict[str, object], int]:
    validated = _validate(value)
    if isinstance(validated, dict):
        return validated, 2
    targets, args = validated
    if any("\x00" in item for item in args):
        return _unavailable("unsupported_input", "Native arguments may not contain NUL.")
    if any(item in {"-h", "--help", "-V", "--version"} for item in args):
        return _unavailable("unsupported_input", "Native metadata requests do not perform testing.")
    if any("::" in target for target in targets):
        return _unavailable(
            "unsupported_input", "Pytest cannot represent this literal filesystem target."
        )
    if importlib.util.find_spec("pytest") is None:
        return _unavailable(
            "dependency_unavailable", "Pytest is unavailable to the adapter interpreter."
        )
    try:
        version_run = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return _unavailable("dependency_unavailable", f"Pytest version lookup failed: {exc}")
    version_stdout, _, version_evidence = _streams(version_run)
    match = re.fullmatch(r"pytest ([^\r\n]+)\s*", version_stdout)
    if version_run.returncode != 0 or match is None:
        return _unavailable(
            "dependency_unavailable",
            "Pytest did not report a usable version.",
            evidence=version_evidence,
        )
    version = match[1]
    try:
        result = subprocess.run(
            [sys.executable, __file__, "--native", *targets, *args],
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return _unavailable("execution_error", f"Pytest execution failed: {exc}", version)
    _, stderr, evidence = _streams(result)
    if result.returncode == 0:
        return _response(
            "passed",
            "Pytest completed the requested native operation (exit 0).",
            version,
            evidence=evidence,
        )
    if result.returncode == 5:
        return _response(
            "passed", "Pytest found no tests (native exit 5).", version, evidence=evidence
        )
    if result.returncode == 1:
        if not evidence.strip():
            return _unavailable(
                "invalid_result", "Pytest returned no negative-result evidence.", version
            )
        return _response(
            "failed",
            "Pytest reported a negative native result (exit 1).",
            version,
            evidence=evidence,
        )
    if result.returncode == 4:
        return _unavailable(
            _usage_reason(stderr), "Pytest rejected the native request (exit 4).", version, evidence
        )
    return _unavailable(
        "execution_error",
        f"Pytest could not complete the native request (exit {result.returncode}).",
        version,
        evidence,
    )


def main() -> int:
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        response, exit_code = _invalid([], "invalid_value"), 2
    else:
        response, exit_code = _run(request)
    sys.stdout.buffer.write(json.dumps(response, ensure_ascii=False).encode("utf-8") + b"\n")
    return exit_code


if __name__ == "__main__":
    if sys.argv[1:2] == ["--native"]:
        # Preserve python -m pytest workspace imports in a fresh native interpreter.
        sys.path[0] = os.getcwd()
        import pytest

        pytest.hookimpl(tryfirst=True)(_MetadataGuard.pytest_cmdline_main)
        raise SystemExit(pytest.main(sys.argv[2:], plugins=[_MetadataGuard()]))
    raise SystemExit(main())
