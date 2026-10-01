"""Stdlib-only Ruff format/lint check/v1 adapter."""

from __future__ import annotations

import importlib.metadata
import json
import os
import re
import subprocess
import sys

_REQUEST_KEYS = frozenset({"operation", "targets", "args"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
_CONFLICTING_FLAGS = (
    "--fix",
    "--fix-only",
    "--stdin",
    "--stdin-filename",
    "--output-file",
    "-o",
    "--add-noqa",
    "-",
)


def _issue(location: list[str | int], code: str) -> dict[str, object]:
    return {"location": location, "code": code}


def _invalid(details: list[dict[str, object]]) -> dict[str, object]:
    return {"reason": "invalid_request", "details": details}


def _valid_absolute_path(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and "\x00" not in value
        and _ABSOLUTE_PATH.fullmatch(value) is not None
    )


def _validate_request(value: object) -> tuple[str, list[str], list[str]] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([_issue([], "wrong_type")])
    keys = set(value)
    unknown = sorted(str(key) for key in keys - _REQUEST_KEYS)
    if unknown:
        return _invalid([_issue([key], "unknown_field") for key in unknown])
    missing = sorted(_REQUEST_KEYS - keys)
    if missing:
        return _invalid([_issue([key], "missing_field") for key in missing])
    operation = value["operation"]
    if not isinstance(operation, str):
        return _invalid([_issue(["operation"], "wrong_type")])
    if operation not in {"format", "lint"}:
        return _invalid([_issue(["operation"], "invalid_value")])
    targets = value["targets"]
    if not isinstance(targets, list):
        return _invalid([_issue(["targets"], "wrong_type")])
    target_issues: list[dict[str, object]] = []
    for index, target in enumerate(targets):
        if not isinstance(target, str):
            target_issues.append(_issue(["targets", index], "wrong_type"))
        elif not _valid_absolute_path(target):
            target_issues.append(_issue(["targets", index], "invalid_value"))
    if target_issues:
        return _invalid(target_issues)
    args = value["args"]
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        return _invalid([_issue(["args"], "wrong_type")])
    return operation, [str(target) for target in targets], list(args)


def _external_tools(version: str | None) -> list[dict[str, str | None]]:
    return [{"tool_id": "ruff", "version": version}]


def _evidence(stdout: bytes, stderr: bytes) -> dict[str, object] | None:
    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    if not stdout_text and not stderr_text:
        return None
    parts: list[str] = []
    if stdout_text:
        parts.append(f"stdout:\n{stdout_text}")
    if stderr_text:
        parts.append(f"stderr:\n{stderr_text}")
    return {"format": "text", "data": "\n".join(parts)}


def _diagnostic_from_json(value: object) -> str | None:
    if isinstance(value, dict):
        message = value.get("message")
        if isinstance(message, str) and message.strip():
            parts: list[str] = []
            code = value.get("code")
            if isinstance(code, str) and code.strip():
                parts.append(code.strip())
            filename = value.get("filename")
            if isinstance(filename, str) and filename.strip():
                parts.append(filename.strip())
            location = value.get("location")
            if isinstance(location, dict):
                row = location.get("row")
                column = location.get("column")
                if isinstance(row, int) or isinstance(column, int):
                    parts.append(
                        f"line {row if isinstance(row, int) else 0}, "
                        f"column {column if isinstance(column, int) else 0}"
                    )
            parts.append(message.strip())
            return ": ".join(parts)
        for item in value.values():
            diagnostic = _diagnostic_from_json(item)
            if diagnostic is not None:
                return diagnostic
    elif isinstance(value, list):
        for item in value:
            diagnostic = _diagnostic_from_json(item)
            if diagnostic is not None:
                return diagnostic
    return None


def _message(stdout: bytes, stderr: bytes, operation: str) -> str | None:
    try:
        parsed = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    diagnostic = _diagnostic_from_json(parsed)
    if diagnostic is not None:
        return diagnostic

    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    combined = stdout_text + "\n" + stderr_text
    structured = stdout_text.lstrip().startswith(("{", "[", "<", "--- "))
    message_source = stderr_text if structured else combined
    meaningful = [line.strip() for line in message_source.splitlines() if line.strip()]
    if meaningful:
        return meaningful[0]
    if combined.strip():
        if operation == "format":
            return "Ruff format requires formatting changes."
        return "Ruff lint reported violations."
    return None


def _unavailable(
    reason: str,
    message: str,
    version: str | None,
    evidence: dict[str, object] | None = None,
) -> tuple[dict[str, object], int]:
    response: dict[str, object] = {
        "decision": {"status": "unavailable", "reason": reason, "message": message},
        "external_tools": _external_tools(version),
        "coverage": None,
        "required_targets": [],
    }
    if evidence is not None:
        response["evidence"] = evidence
    return response, 3


def _classify_native_failure(output: str) -> str:
    lowered = output.casefold()
    if any(
        marker in lowered
        for marker in (
            "toml parse error",
            "failed to parse",
            "configuration",
            "config file",
        )
    ):
        return "invalid_configuration"
    if any(
        marker in lowered
        for marker in (
            "unknown option",
            "unrecognized option",
            "unexpected argument",
            "invalid value",
            "no such option",
        )
    ):
        return "unsupported_input"
    return "execution_error"


def _conflicting_argument(arg: str) -> bool:
    if "\x00" in arg or arg.startswith("@"):
        return True
    if arg in _CONFLICTING_FLAGS:
        return True
    if arg.startswith("--fix=") or arg.startswith("--fix-only="):
        return True
    if arg.startswith("--stdin-filename=") or arg.startswith("--output-file="):
        return True
    if arg.startswith("-") and not arg.startswith("--") and "o" in arg[1:]:
        return True
    return arg.startswith("--add-noqa=")


def _run(request: object) -> tuple[dict[str, object], int]:
    validated = _validate_request(request)
    if isinstance(validated, dict):
        return validated, 2
    operation, targets, args = validated
    try:
        version = importlib.metadata.version("ruff")
    except importlib.metadata.PackageNotFoundError:
        return _unavailable(
            "dependency_unavailable",
            "Ruff distribution is unavailable to the adapter interpreter.",
            None,
        )

    for arg in args:
        if _conflicting_argument(arg):
            return _unavailable(
                "unsupported_input",
                f"Ruff argument conflicts with the check contract: {arg!r}",
                version,
            )
    output_file = os.environ.get("RUFF_OUTPUT_FILE")
    if output_file:
        return _unavailable(
            "unsupported_input",
            "RUFF_OUTPUT_FILE is set; file output is outside the check contract.",
            version,
        )

    command = [sys.executable, "-m", "ruff"]
    if operation == "format":
        command.extend(["format", "--check", "--diff"])
    else:
        command.extend(["check", "--no-fix", "--no-fix-only"])
    command.extend(args)
    command.extend(targets)
    try:
        completed = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return _unavailable("execution_error", f"Ruff launch failed: {exc}", version)

    evidence = _evidence(completed.stdout, completed.stderr)
    external_tools = _external_tools(version)
    message = _message(completed.stdout, completed.stderr, operation)
    if completed.returncode == 0:
        response: dict[str, object] = {
            "decision": {"status": "passed"},
            "external_tools": external_tools,
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
                "Ruff returned a failed status without substantive diagnostics.",
                version,
                evidence,
            )
        return {
            "decision": {"status": "failed", "message": message},
            "external_tools": external_tools,
            "evidence": evidence or {"format": "text", "data": message},
            "coverage": None,
            "required_targets": [],
        }, 1

    output = ""
    if evidence is not None and isinstance(evidence["data"], str):
        output = evidence["data"]
    reason = _classify_native_failure(output)
    return _unavailable(
        reason,
        message or f"Ruff returned native exit status {completed.returncode}.",
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
    payload = json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(payload + b"\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
