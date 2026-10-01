"""Stdlib-only Ruff fix/v1 adapter for explicitly admitted existing files."""

from __future__ import annotations

import importlib.metadata
import json
import os
import re
import subprocess
import sys

_KEYS = frozenset({"operation", "targets", "args", "execution_context"})
_ABSOLUTE = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
# These native value options consume one token; unrecognized bare tokens cannot add sources.
_VALUE_OPTIONS = frozenset(
    {
        "--config",
        "--select",
        "--ignore",
        "--extend-select",
        "--extend-ignore",
        "--fixable",
        "--unfixable",
        "--extend-fixable",
        "--extend-unfixable",
        "--output-format",
        "--line-length",
        "--target-version",
        "--exclude",
        "--extend-exclude",
        "--cache-dir",
        "--extension",
        "--per-file-ignores",
        "--extend-per-file-ignores",
        "--range",
    }
)
_CONFLICTS = frozenset(
    {
        "--no-fix",
        "--diff",
        "--check",
        "--stdin-filename",
        "--stdin",
        "--output-file",
        "--help",
        "--version",
        "--show-files",
        "--show-settings",
        "--watch",
        "--add-noqa",
    }
)


def _invalid(field: str | list[str] | None, code: str) -> tuple[dict[str, object], int]:
    location = field if isinstance(field, list) else [] if field is None else [field]
    return {
        "reason": "invalid_request",
        "details": [{"location": location, "code": code}],
    }, 2


def _validate_execution_context(value: object) -> tuple[dict[str, object], int] | None:
    if not isinstance(value, dict):
        return _invalid(["execution_context"], "wrong_type")
    unknown = sorted(str(key) for key in set(value) - {"scratch_directory"})
    if unknown:
        return _invalid(["execution_context", unknown[0]], "unknown_field")
    if "scratch_directory" not in value:
        return _invalid(["execution_context", "scratch_directory"], "missing_field")
    directory = value["scratch_directory"]
    if not isinstance(directory, str):
        return _invalid(["execution_context", "scratch_directory"], "wrong_type")
    if not directory or "\x00" in directory or _ABSOLUTE.fullmatch(directory) is None:
        return _invalid(["execution_context", "scratch_directory"], "invalid_value")
    return None


def _validate(value: object) -> tuple[str, list[str], list[str]] | tuple[dict[str, object], int]:
    if not isinstance(value, dict):
        return _invalid(None, "wrong_type")
    unknown = sorted(str(key) for key in set(value) - _KEYS)
    missing = sorted(_KEYS - set(value))
    if unknown:
        return _invalid(unknown[0], "unknown_field")
    if missing:
        return _invalid(missing[0], "missing_field")
    context_issue = _validate_execution_context(value["execution_context"])
    if context_issue is not None:
        return context_issue
    if not isinstance(value["operation"], str):
        return _invalid("operation", "wrong_type")
    if value["operation"] not in {"format", "lint"}:
        return _invalid("operation", "invalid_value")
    for field in ("targets", "args"):
        if not isinstance(value[field], list) or any(
            not isinstance(item, str) for item in value[field]
        ):
            return _invalid(field, "wrong_type")
    if not value["targets"] or any(
        not path
        or "\x00" in path
        or _ABSOLUTE.fullmatch(path) is None
        or re.search(r"(?:[\\/]|(?:^|[\\/])\.{1,2})$", path) is not None
        for path in value["targets"]
    ):
        return _invalid("targets", "invalid_value")
    return value["operation"], value["targets"], value["args"]


def _safe_args(args: list[str]) -> bool:
    expecting_value = False
    for token in args:
        if "\x00" in token or token.startswith("@"):
            return False
        if expecting_value:
            if token.startswith("-"):
                return False
            expecting_value = False
            continue
        if not token.startswith("-") or token in {"-", "--"}:
            return False
        option = token.split("=", 1)[0]
        if option in _CONFLICTS:
            return False
        if token.startswith("--"):
            expecting_value = option in _VALUE_OPTIONS and "=" not in token
        elif not set(token[1:]).issubset("qvsn"):
            return False
    return not expecting_value


def _result(
    status: str,
    version: str | None,
    *,
    message: str | None = None,
    reason: str | None = None,
    evidence: str = "",
) -> tuple[dict[str, object], int]:
    decision = {"status": status}
    if message is not None:
        decision["message"] = message
    if reason is not None:
        decision["reason"] = reason
    response: dict[str, object] = {
        "decision": decision,
        "external_tools": [{"tool_id": "ruff", "version": version}],
    }
    if evidence:
        response["evidence"] = {"format": "text", "data": evidence}
    return response, {"passed": 0, "failed": 1, "unavailable": 3}[status]


def _unavailable(
    reason: str,
    message: str,
    version: str | None = None,
    evidence: str = "",
) -> tuple[dict[str, object], int]:
    return _result("unavailable", version, reason=reason, message=message, evidence=evidence)


def _run(value: object) -> tuple[dict[str, object], int]:
    admitted = _validate(value)
    if len(admitted) == 2:
        return admitted
    operation, targets, args = admitted
    # Check the complete file set before any native operation can write.
    if any(not os.path.isfile(path) or any(char in path for char in "*?[]") for path in targets):
        return _unavailable("unsupported_input", "Fix targets must be existing literal files.")
    if not _safe_args(args) or os.environ.get("RUFF_OUTPUT_FILE"):
        return _unavailable(
            "unsupported_input",
            "Native arguments or output routing conflict with the fix request.",
        )
    try:
        version = importlib.metadata.version("ruff")
    except importlib.metadata.PackageNotFoundError:
        return _unavailable(
            "dependency_unavailable", "Ruff is unavailable to the adapter interpreter."
        )
    controls = ["format"] if operation == "format" else ["check", "--fix"]
    try:
        native = subprocess.run(
            [sys.executable, "-m", "ruff", *controls, *args, "--", *targets],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return _unavailable("execution_error", f"Ruff execution failed: {exc}", version)
    stdout = native.stdout.decode("utf-8", errors="replace")
    stderr = native.stderr.decode("utf-8", errors="replace")
    evidence = stdout
    if stderr:
        evidence = f"{stdout}\nstderr:\n{stderr}" if stdout else stderr
    if native.returncode == 0:
        return _result("passed", version, evidence=evidence)
    if native.returncode == 1:
        if not evidence.strip():
            return _unavailable(
                "invalid_result",
                "Ruff returned no substantive negative-result evidence.",
                version,
            )
        return _result(
            "failed",
            version,
            message="Ruff reported a negative native fixing result (exit 1).",
            evidence=evidence,
        )
    lowered = evidence.casefold()
    if any(
        token in lowered
        for token in (
            "toml parse error",
            "configuration file",
            "config file",
            "failed to load configuration",
        )
    ):
        reason = "invalid_configuration"
    elif any(
        token in lowered for token in ("unexpected argument", "invalid value", "unknown option")
    ):
        reason = "unsupported_input"
    else:
        reason = "execution_error"
    return _unavailable(
        reason,
        f"Ruff could not complete the requested fix (native exit {native.returncode}).",
        version,
        evidence,
    )


def main() -> int:
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        result, code = _invalid(None, "invalid_value")
    else:
        result, code = _run(request)
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=False).encode("utf-8") + b"\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
