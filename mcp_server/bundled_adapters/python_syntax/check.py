"""Stdlib-only python_syntax check/v1 adapter."""

from __future__ import annotations

import ast
import json
import platform
import re
import sys

_REQUEST_KEYS = frozenset({"operation", "target_path", "content", "args", "execution_context"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
_BARE_UNC_ROOT = re.compile(r"^\\\\[^\\/]+[\\/][^\\/]+$")


def _external_tools() -> list[dict[str, str]]:
    return [{"tool_id": "python", "version": platform.python_version()}]


def _invalid(details: list[dict[str, object]]) -> dict[str, object]:
    return {"reason": "invalid_request", "details": details}


def _issue(location: list[str | int], code: str) -> dict[str, object]:
    return {"location": location, "code": code}


def _valid_absolute_file_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    if _ABSOLUTE_PATH.fullmatch(value) is None:
        return False
    if _BARE_UNC_ROOT.fullmatch(value) is not None:
        return False
    if value.endswith(("/", "\\")):
        return False
    components = [part for part in re.split(r"[\\/]", value) if part]
    return not components or components[-1] not in {".", ".."}


def _validate_request(value: object) -> tuple[str, str, str, tuple[str, ...]] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([_issue([], "wrong_type")])
    keys = set(value)
    unknown = sorted(str(key) for key in keys - _REQUEST_KEYS)
    if unknown:
        return _invalid([_issue([key], "unknown_field") for key in unknown])
    missing = sorted(_REQUEST_KEYS - keys)
    if missing:
        return _invalid([_issue([key], "missing_field") for key in missing])
    context = value["execution_context"]
    if not isinstance(context, dict):
        return _invalid([_issue(["execution_context"], "wrong_type")])
    unknown_context = sorted(str(key) for key in set(context) - {"scratch_directory"})
    if unknown_context:
        return _invalid(
            [_issue(["execution_context", key], "unknown_field") for key in unknown_context]
        )
    if "scratch_directory" not in context:
        return _invalid([_issue(["execution_context", "scratch_directory"], "missing_field")])
    scratch = context["scratch_directory"]
    if not isinstance(scratch, str):
        return _invalid([_issue(["execution_context", "scratch_directory"], "wrong_type")])
    if not scratch or "\x00" in scratch or _ABSOLUTE_PATH.fullmatch(scratch) is None:
        return _invalid([_issue(["execution_context", "scratch_directory"], "invalid_value")])
    if not isinstance(value["operation"], str):
        return _invalid([_issue(["operation"], "wrong_type")])
    if value["operation"] != "syntax":
        return _invalid([_issue(["operation"], "invalid_value")])
    target_path = value["target_path"]
    if not isinstance(target_path, str):
        return _invalid([_issue(["target_path"], "wrong_type")])
    if not _valid_absolute_file_path(target_path):
        return _invalid([_issue(["target_path"], "invalid_value")])
    content = value["content"]
    if not isinstance(content, str):
        return _invalid([_issue(["content"], "wrong_type")])
    args = value["args"]
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        return _invalid([_issue(["args"], "wrong_type")])

    return "syntax", target_path, content, tuple(args)


def _run(request: object) -> tuple[dict[str, object], int]:
    validated = _validate_request(request)
    if isinstance(validated, dict):
        return validated, 2
    _, target_path, content, args = validated
    if args:
        return {
            "decision": {
                "status": "unavailable",
                "reason": "unsupported_input",
                "message": "Python syntax checking does not support native options.",
            },
            "external_tools": _external_tools(),
        }, 3
    try:
        ast.parse(content, filename=target_path)
    except SyntaxError as exc:
        source_line = (exc.text or "").rstrip("\r\n")
        evidence = (
            f"filename: {target_path}\n"
            f"line {exc.lineno or 0}, column {exc.offset or 0}\n"
            f"source: {source_line}\n"
            f"message: {exc.msg}"
        )
        return {
            "decision": {"status": "failed", "message": exc.msg},
            "external_tools": _external_tools(),
            "evidence": {"format": "text", "data": evidence},
        }, 1
    return {
        "decision": {"status": "passed"},
        "external_tools": _external_tools(),
    }, 0


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
