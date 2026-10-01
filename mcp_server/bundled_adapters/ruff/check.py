"""Stdlib-only Ruff format/lint check/v1 adapter."""

from __future__ import annotations

import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

_REQUEST_KEYS = frozenset({"operation", "targets", "args", "execution_context"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
_CONFLICTING_FLAGS = (
    "--fix",
    "--fix-only",
    "--stdin",
    "--stdin-filename",
    "--output-file",
    "-o",
    "--add-noqa",
    "--help",
    "--version",
    "--show-files",
    "--show-settings",
    "--watch",
    "--diff",
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


def _validate_request(value: object) -> tuple[str, list[str], list[str], str] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([_issue([], "wrong_type")])
    keys = set(value)
    unknown = sorted(str(key) for key in keys - _REQUEST_KEYS)
    if unknown:
        return _invalid([_issue([key], "unknown_field") for key in unknown])
    missing = sorted(_REQUEST_KEYS - keys)
    if missing:
        return _invalid([_issue([key], "missing_field") for key in missing])
    context_issue = _validate_execution_context(value["execution_context"])
    if context_issue is not None:
        return context_issue
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
    return (
        operation,
        [str(target) for target in targets],
        list(args),
        value["execution_context"]["scratch_directory"],
    )


def native_version_error(version: str) -> str | None:
    """Compare the observed native version with this package's exact requirement."""
    try:
        declaration = (
            Path(__file__).with_name("requirements.txt").read_text(encoding="utf-8").strip()
        )
    except (OSError, UnicodeError) as exc:
        return f"Ruff prerequisite declaration is unreadable (actual {version}): {exc}"
    requirement = re.fullmatch(r"ruff==([^\s;]+)", declaration)
    if requirement is None:
        return f"Ruff prerequisite declaration is invalid: {declaration!r} (actual {version})."
    expected = requirement.group(1)
    if version != expected:
        return f"Ruff version is unsupported: actual {version}, expected {declaration}."
    return None


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
    _, message = native_failure(message_source)
    if message is not None:
        return message
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


def native_arguments_supported(arguments: list[str]) -> bool:
    """Admit representable UTF-8 tokens without native line separators."""
    if any("\r" in argument or "\n" in argument for argument in arguments):
        return False
    try:
        "\n".join(arguments).encode("utf-8")
    except UnicodeError:
        return False
    return True


def write_native_arguments(path: Path, arguments: list[str]) -> None:
    """Write one admitted native vector exclusively in the supplied invocation directory."""
    payload = ("\n".join(arguments) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(payload)


def native_failure(output: str) -> tuple[str, str | None]:
    """Interpret Ruff's substantive error and causal lines independently of debug chatter."""
    lines = [
        line.strip()
        for line in output.splitlines()
        if line.strip()
        and re.match(
            r"^\[\d{4}-\d{2}-\d{2}\]\[\d{2}:\d{2}:\d{2}\]\[[^\]]+\]\[(?:DEBUG|TRACE|INFO)\]",
            line,
        )
        is None
        and line.strip() not in {"stdout:", "stderr:"}
    ]
    # Only the terminal native cause is evidence of access failure, not an intermediate path.
    causes = [line for line in lines if line.startswith("Cause: ")]
    terminal = causes[-1:] if causes else [line for line in lines if line.startswith("error:")]
    access = next(
        (line for line in terminal if re.search(r"\(os error \d+\)$", line) is not None),
        None,
    )
    if access is not None:
        return "execution_error", access
    lowered = "\n".join(lines).casefold()
    message = next(
        (line for line in lines if line.casefold().startswith(("ruff failed", "error:"))),
        lines[0] if lines else None,
    )
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
        return "unsupported_input", message
    if any(
        marker in lowered
        for marker in (
            "toml parse error",
            "failed to parse configuration",
            "invalid configuration",
            "failed to load configuration",
            "unknown field",
            "invalid type",
        )
    ):
        return "invalid_configuration", message
    return "execution_error", message


def _conflicting_argument(arg: str) -> bool:
    if "\x00" in arg or arg.startswith("@"):
        return True
    if arg in _CONFLICTING_FLAGS:
        return True
    if arg.startswith("--fix=") or arg.startswith("--fix-only="):
        return True
    if arg.startswith("--stdin-filename=") or arg.startswith("--output-file="):
        return True
    if arg.startswith("-") and not arg.startswith("--") and any(char in arg[1:] for char in "ohV"):
        return True
    return arg.startswith("--add-noqa=")


def _run(request: object) -> tuple[dict[str, object], int]:
    validated = _validate_request(request)
    if isinstance(validated, dict):
        return validated, 2
    operation, targets, args, scratch_directory = validated
    try:
        version = importlib.metadata.version("ruff")
    except importlib.metadata.PackageNotFoundError:
        return _unavailable(
            "dependency_unavailable",
            "Ruff distribution is unavailable to the adapter interpreter.",
            None,
        )

    version_error = native_version_error(version)
    if version_error is not None:
        return _unavailable("dependency_unavailable", version_error, version)

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

    controls = ["--check", "--diff"] if operation == "format" else ["--no-fix", "--no-fix-only"]
    arguments = [*controls, *args, *targets]
    if not native_arguments_supported(arguments):
        return _unavailable(
            "unsupported_input",
            "Ruff argument-file tokens must be UTF-8 without CR or LF.",
            version,
        )
    arguments_path = Path(scratch_directory) / f"ruff-arguments-{uuid4().hex}.txt"
    native_operation = "format" if operation == "format" else "check"
    try:
        write_native_arguments(arguments_path, arguments)
        completed = subprocess.run(
            [sys.executable, "-m", "ruff", native_operation, "@" + str(arguments_path)],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return _unavailable("execution_error", f"Ruff preparation or launch failed: {exc}", version)

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
    reason, failure_message = native_failure(output)
    return _unavailable(
        reason,
        failure_message or f"Ruff returned native exit status {completed.returncode}.",
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
