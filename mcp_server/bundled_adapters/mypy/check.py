"""Mypy types check/v1 adapter."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

_REQUEST_KEYS = frozenset({"operation", "targets", "args", "execution_context"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")


def _issue(location: list[str | int], code: str) -> dict[str, object]:
    return {"location": location, "code": code}


def _invalid(details: list[dict[str, object]]) -> dict[str, object]:
    return {"reason": "invalid_request", "details": details}


def _valid_path(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and "\x00" not in value
        and _ABSOLUTE_PATH.fullmatch(value) is not None
    )


def _validate_execution_context(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return _invalid([_issue(["execution_context"], "wrong_type")])
    unknown = sorted(str(key) for key in set(value) - {"scratch_directory"})
    if unknown:
        return _invalid([_issue(["execution_context", unknown[0]], "unknown_field")])
    if "scratch_directory" not in value:
        return _invalid([_issue(["execution_context", "scratch_directory"], "missing_field")])
    directory = value["scratch_directory"]
    if not isinstance(directory, str):
        return _invalid([_issue(["execution_context", "scratch_directory"], "wrong_type")])
    if not directory or "\x00" in directory or _ABSOLUTE_PATH.fullmatch(directory) is None:
        return _invalid([_issue(["execution_context", "scratch_directory"], "invalid_value")])
    return None


def _validate(value: object) -> tuple[list[str], list[str]] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([_issue([], "wrong_type")])
    unknown = sorted(str(key) for key in set(value) - _REQUEST_KEYS)
    if unknown:
        return _invalid([_issue([key], "unknown_field") for key in unknown])
    missing = sorted(_REQUEST_KEYS - set(value))
    if missing:
        return _invalid([_issue([key], "missing_field") for key in missing])
    context_issue = _validate_execution_context(value["execution_context"])
    if context_issue is not None:
        return context_issue
    if not isinstance(value["operation"], str):
        return _invalid([_issue(["operation"], "wrong_type")])
    if value["operation"] != "types":
        return _invalid([_issue(["operation"], "invalid_value")])
    targets = value["targets"]
    if not isinstance(targets, list):
        return _invalid([_issue(["targets"], "wrong_type")])
    issues: list[dict[str, object]] = []
    for index, target in enumerate(targets):
        if not isinstance(target, str):
            issues.append(_issue(["targets", index], "wrong_type"))
        elif not _valid_path(target):
            issues.append(_issue(["targets", index], "invalid_value"))
    args = value["args"]
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        issues.append(_issue(["args"], "wrong_type"))
    if issues:
        return _invalid(issues)
    return [str(target) for target in targets], [str(arg) for arg in args]


def _native_version_error(version: str) -> str | None:
    """Read the package declaration before relying on the installed Mypy parser."""
    try:
        declaration = (
            Path(__file__).with_name("requirements.txt").read_text(encoding="utf-8").strip()
        )
    except (OSError, UnicodeError) as exc:
        return f"Mypy prerequisite declaration is unreadable (actual {version}): {exc}"
    requirement = re.fullmatch(r"mypy==([^\s;]+)", declaration)
    if requirement is None:
        return f"Mypy prerequisite declaration is invalid: {declaration!r} (actual {version})."
    expected = requirement.group(1)
    if version != expected:
        return f"Mypy version is unsupported: actual {version}, expected {declaration}."
    return None


def _external(version: str | None) -> list[dict[str, str | None]]:
    return [{"tool_id": "mypy", "version": version}]


def _evidence(stdout: bytes, stderr: bytes) -> dict[str, object] | None:
    out = stdout.decode("utf-8", errors="replace")
    err = stderr.decode("utf-8", errors="replace")
    if not out and not err:
        return None
    parts: list[str] = []
    if out:
        parts.append(f"stdout:\n{out}")
    if err:
        parts.append(f"stderr:\n{err}")
    return {"format": "text", "data": "\n".join(parts)}


def _unavailable(
    reason: str, message: str, version: str | None, evidence: dict[str, object] | None = None
) -> tuple[dict[str, object], int]:
    response: dict[str, object] = {
        "decision": {"status": "unavailable", "reason": reason, "message": message},
        "external_tools": _external(version),
        "coverage": None,
        "required_targets": [],
    }
    if evidence is not None:
        response["evidence"] = evidence
    return response, 3


@dataclass(frozen=True)
class _GuardResult:
    reason: str
    message: str
    stdout: str = ""
    stderr: str = ""


def _native_guard(args: list[str]) -> _GuardResult | str | None:
    """Read native options/configuration before invoking Mypy's runner."""
    if any("\x00" in arg or arg.startswith("@") for arg in args):
        return _GuardResult(
            "unsupported_input",
            "Response-file and NUL-containing arguments are outside the check contract.",
        )
    try:
        native_main = importlib.import_module("mypy.main")
        native_config = importlib.import_module("mypy.config_parser")
        native_options = importlib.import_module("mypy.options")
        native_namespace = importlib.import_module("mypy.split_namespace")
    except ImportError as exc:
        return _GuardResult("dependency_unavailable", f"Mypy parser is unavailable: {exc}")

    stdout, stderr = StringIO(), StringIO()
    parser, _, strict_assignments = native_main.define_options(stdout=stdout, stderr=stderr)
    dummy = argparse.Namespace()
    try:
        parser.parse_args(args, dummy)
    except SystemExit as exc:
        if exc.code == 0:
            return _GuardResult(
                "unsupported_input",
                "Native metadata requests do not perform type analysis.",
                stdout.getvalue(),
                stderr.getvalue(),
            )
        return _GuardResult(
            "unsupported_input",
            _message(stdout.getvalue().encode(), stderr.getvalue().encode())
            or "Mypy rejected native arguments.",
            stdout.getvalue(),
            stderr.getvalue(),
        )

    options = native_options.Options()

    def set_strict() -> None:
        for destination, setting in strict_assignments:
            setattr(options, destination, setting)

    previous = os.environ.get("MYPY_CONFIG_FILE_DIR")
    try:
        native_config.parse_config_file(options, set_strict, dummy.config_file, stdout, stderr)
    except OSError as exc:
        return _GuardResult(
            "execution_error",
            f"Mypy configuration read failed: {exc}",
            stdout.getvalue(),
            stderr.getvalue(),
        )
    finally:
        if previous is None:
            os.environ.pop("MYPY_CONFIG_FILE_DIR", None)
        else:
            os.environ["MYPY_CONFIG_FILE_DIR"] = previous
    if stderr.getvalue().strip():
        return _GuardResult(
            "invalid_configuration",
            _message(stdout.getvalue().encode(), stderr.getvalue().encode())
            or "Mypy rejected native configuration.",
            stdout.getvalue(),
            stderr.getvalue(),
        )

    special = argparse.Namespace()
    parser.parse_args(args, native_namespace.SplitNamespace(options, special, "special-opts:"))
    if special.command:
        return _GuardResult(
            "unsupported_input", "Mypy --command replaces the selected source input."
        )
    for field in (
        "shadow_file",
        "junit_xml",
        "timing_stats",
        "line_checking_stats",
        "install_types",
    ):
        if getattr(options, field):
            return _GuardResult(
                "unsupported_input",
                f"Mypy option {field} writes or replaces input outside the check contract.",
            )
    if options.report_dirs or any(
        value for field, value in vars(special).items() if field.endswith("_report")
    ):
        return _GuardResult(
            "unsupported_input", "Mypy report output is outside the check contract."
        )
    return options.config_file if isinstance(options.config_file, str) else None


def _native_error(text: str) -> str | None:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                diagnostic = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(diagnostic, dict) and diagnostic.get("severity") == "error":
                message = diagnostic.get("message")
                if isinstance(message, str) and message.strip():
                    return message
        elif ": error:" in line or line.startswith("error:"):
            return line
    return None


def _message(stdout: bytes, stderr: bytes) -> str | None:
    combined = (stdout + b"\n" + stderr).decode("utf-8", errors="replace")
    error = _native_error(combined)
    if error is not None:
        return error
    return next((line.strip() for line in combined.splitlines() if line.strip()), None)


def _configuration_diagnostic(text: str, config_file: str) -> bool:
    expected = os.path.normcase(os.path.abspath(config_file))
    for line in text.splitlines():
        line = line.strip()
        filename: str | None = None
        if line.startswith("{"):
            try:
                diagnostic = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(diagnostic, dict) and diagnostic.get("severity") == "error":
                native_file = diagnostic.get("file")
                if isinstance(native_file, str):
                    filename = native_file
        elif ": error:" in line:
            location = line.split(": error:", 1)[0]
            for _ in range(2):
                prefix, separator, position = location.rpartition(":")
                if not separator or not position.isdigit():
                    break
                location = prefix
                filename = location
        if filename is not None and os.path.normcase(os.path.abspath(filename)) == expected:
            return True
    return False


def _classify_exit(code: int, text: str, config_file: str | None) -> str:
    lowered = text.casefold()
    if any(marker in lowered for marker in ("internal error", "traceback (most recent call last)")):
        return "execution_error"
    if "cannot find config file" in lowered or (
        config_file is not None and _configuration_diagnostic(text, config_file)
    ):
        return "invalid_configuration"
    if any(marker in lowered for marker in ("usage:", "unrecognized arguments", "invalid choice")):
        return "unsupported_input"
    if code == 2:
        if any(line.strip().startswith(("error:", "mypy: error:")) for line in text.splitlines()):
            return "unsupported_input"
        if _native_error(text) is not None:
            return "failed"
    return "execution_error"


def _run(value: object) -> tuple[dict[str, object], int]:
    validated = _validate(value)
    if isinstance(validated, dict):
        return validated, 2
    targets, args = validated
    try:
        version = importlib.metadata.version("mypy")
    except importlib.metadata.PackageNotFoundError:
        return _unavailable(
            "dependency_unavailable",
            "Mypy distribution is unavailable to the adapter interpreter.",
            None,
        )
    version_error = _native_version_error(version)
    if version_error is not None:
        return _unavailable("dependency_unavailable", version_error, version)
    guard = _native_guard(args)
    if isinstance(guard, _GuardResult):
        return _unavailable(
            guard.reason,
            guard.message,
            version,
            _evidence(guard.stdout.encode(), guard.stderr.encode()),
        )
    command = [sys.executable, "-m", "mypy", *args, *targets]
    try:
        completed = subprocess.run(
            command, stdin=subprocess.DEVNULL, capture_output=True, check=False
        )
    except OSError as exc:
        return _unavailable("execution_error", f"Mypy launch failed: {exc}", version)
    evidence = _evidence(completed.stdout, completed.stderr)
    message = _message(completed.stdout, completed.stderr)
    external = _external(version)
    if completed.returncode == 0:
        response: dict[str, object] = {
            "decision": {"status": "passed"},
            "external_tools": external,
            "coverage": None,
            "required_targets": [],
        }
        if evidence is not None:
            response["evidence"] = evidence
        return response, 0
    if completed.returncode == 1:
        if message is None:
            return _unavailable(
                "invalid_result",
                "Mypy returned a failed status without substantive diagnostics.",
                version,
                evidence,
            )
        return {
            "decision": {"status": "failed", "message": message},
            "external_tools": external,
            "evidence": evidence or {"format": "text", "data": message},
            "coverage": None,
            "required_targets": [],
        }, 1
    text = str(evidence.get("data", "")) if evidence is not None else ""
    reason = _classify_exit(completed.returncode, text, guard)
    if reason == "failed" and message is not None:
        return {
            "decision": {"status": "failed", "message": message},
            "external_tools": external,
            "evidence": evidence or {"format": "text", "data": message},
            "coverage": None,
            "required_targets": [],
        }, 1
    return _unavailable(
        reason,
        message or f"Mypy returned native exit status {completed.returncode}.",
        version,
        evidence,
    )


def main() -> int:
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        response, exit_code = _invalid([_issue([], "invalid_value")]), 2
    else:
        response, exit_code = _run(request)
    sys.stdout.buffer.write(
        json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
