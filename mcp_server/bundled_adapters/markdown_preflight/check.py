"""Stdlib-only markdown_preflight check/v1 adapter."""

from __future__ import annotations

import json
import platform
import re
import sys
from pathlib import Path

_REQUEST_KEYS = frozenset({"operation", "target_path", "content", "args", "execution_context"})
_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_H1_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
_BARE_UNC_ROOT = re.compile(r"^\\\\[^\\/]+[\\/][^\\/]+$")
_SKIPPED_SCHEMES = ("http:", "https:", "mailto:", "pgmcp:")


def _external_tools() -> list[dict[str, str]]:
    return [{"tool_id": "python", "version": platform.python_version()}]


def _issue(location: list[str | int], code: str) -> dict[str, object]:
    return {"location": location, "code": code}


def _invalid(details: list[dict[str, object]]) -> dict[str, object]:
    return {"reason": "invalid_request", "details": details}


def _valid_absolute_file_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    if _ABSOLUTE_PATH.fullmatch(value) is None or _BARE_UNC_ROOT.fullmatch(value):
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
    operation = value["operation"]
    if not isinstance(operation, str):
        return _invalid([_issue(["operation"], "wrong_type")])
    if operation not in {"document", "body"}:
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

    return operation, target_path, content, tuple(args)


def _check_links(text: str, target_path: str) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    target_parent = Path(target_path).parent
    for match in _LINK_PATTERN.finditer(text):
        link_target = match.group(2)
        if link_target.startswith(_SKIPPED_SCHEMES) or link_target.startswith("#"):
            continue
        target_file = link_target.split("#")[0]
        if not target_file:
            continue
        resolved_path = (target_parent / target_file).resolve()
        if not resolved_path.exists():
            line_no = text[: match.start()].count("\n") + 1
            issues.append(
                {
                    "severity": "warning",
                    "message": f"Broken link: '{link_target}' not found at {resolved_path}",
                    "line": line_no,
                }
            )
    return issues


def _run(request: object) -> tuple[dict[str, object], int]:
    validated = _validate_request(request)
    if isinstance(validated, dict):
        return validated, 2
    operation, target_path, content, args = validated
    if args:
        return {
            "decision": {
                "status": "unavailable",
                "reason": "unsupported_input",
                "message": "Markdown preflight does not support native options.",
            },
            "external_tools": _external_tools(),
        }, 3
    issues: list[dict[str, object]] = []
    if operation == "document" and _H1_PATTERN.search(content) is None:
        issues.append(
            {
                "severity": "error",
                "message": "Missing H1 title (start line with '# ')",
                "line": None,
            }
        )
    issues.extend(_check_links(content, target_path))
    evidence = {
        "format": "json",
        "data": {"issues": issues},
    }
    errors = [issue for issue in issues if issue["severity"] == "error"]
    if errors:
        return {
            "decision": {"status": "failed", "message": str(errors[0]["message"])},
            "external_tools": _external_tools(),
            "evidence": evidence,
        }, 1
    response: dict[str, object] = {
        "decision": {"status": "passed"},
        "external_tools": _external_tools(),
    }
    if issues:
        response["evidence"] = evidence
    return response, 0


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
