# pgmcp:v1 id=python_adapter pv=1.0.0 pf=avBY4V-97IK6mPQy sf=2JPaeqdf6mSOUgvn

"""Native check-jsonschema content and literal selection check/v1 adapter."""

from __future__ import annotations

import importlib
import importlib.metadata
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_CONTENT_KEYS = frozenset({"operation", "target_path", "input_path", "args", "execution_context"})
_SELECTION_KEYS = frozenset({"operation", "targets", "args", "execution_context"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
# Token arities of the pinned native CLI; schema and option semantics remain native.
_VALUE_OPTIONS = frozenset(
    {
        "schemafile",
        "base-uri",
        "builtin-schema",
        "cache-filename",
        "disable-formats",
        "format-regex",
        "regex-variant",
        "default-filetype",
        "force-filetype",
        "traceback-mode",
        "data-transform",
        "validator-class",
        "output-format",
        "color",
    }
)
_SHORT_OPTIONS = {"h": "help", "o": "output-format", "v": "verbose", "q": "quiet"}


@dataclass(frozen=True)
class _Request:
    content: bool
    files: tuple[str, ...]
    args: tuple[str, ...]


@dataclass(frozen=True)
class _Options:
    entries: tuple[tuple[str, str | bool], ...]
    files: tuple[str, ...]


@dataclass(frozen=True)
class _Prerequisites:
    module: str
    external_tools: tuple[dict[str, str | None], ...]
    error: str | None = None


def _issue(location: list[str | int], code: str) -> dict[str, object]:
    return {"location": location, "code": code}


def _invalid(location: list[str | int], code: str) -> dict[str, object]:
    return {"reason": "invalid_request", "details": [_issue(location, code)]}


def _absolute(value: object, *, file: bool = False) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    if _ABSOLUTE_PATH.fullmatch(value) is None:
        return False
    return not (
        file
        and (
            value.endswith(("/", "\\"))
            or value.replace("\\", "/").split("/")[-1] in {".", ".."}
            or re.fullmatch(r"\\\\[^\\/]+[\\/][^\\/]+", value) is not None
        )
    )


def _validate(value: object) -> _Request | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([], "wrong_type")
    content = "input_path" in value or "target_path" in value
    expected = _CONTENT_KEYS if content else _SELECTION_KEYS
    unknown = sorted(str(key) for key in set(value) - expected)
    missing = sorted(expected - set(value))
    if unknown:
        return _invalid([unknown[0]], "unknown_field")
    if missing:
        return _invalid([missing[0]], "missing_field")
    operation = value["operation"]
    if not isinstance(operation, str):
        return _invalid(["operation"], "wrong_type")
    if operation not in {"yaml_configuration", "json_schema"}:
        return _invalid(["operation"], "invalid_value")
    context = value["execution_context"]
    if not isinstance(context, dict):
        return _invalid(["execution_context"], "wrong_type")
    if set(context) != {"scratch_directory"}:
        unknown = sorted(str(key) for key in set(context) - {"scratch_directory"})
        field, code = (
            (unknown[0], "unknown_field") if unknown else ("scratch_directory", "missing_field")
        )
        return _invalid(["execution_context", field], code)
    if not isinstance(context["scratch_directory"], str):
        return _invalid(["execution_context", "scratch_directory"], "wrong_type")
    if not _absolute(context["scratch_directory"]):
        return _invalid(["execution_context", "scratch_directory"], "invalid_value")
    args = value["args"]
    if not isinstance(args, list) or any(not isinstance(arg, str) for arg in args):
        return _invalid(["args"], "wrong_type")
    if content:
        for field in ("target_path", "input_path"):
            if not isinstance(value[field], str):
                return _invalid([field], "wrong_type")
            if not _absolute(value[field], file=True):
                return _invalid([field], "invalid_value")
        files = (str(value["input_path"]),)
    else:
        targets = value["targets"]
        if not isinstance(targets, list):
            return _invalid(["targets"], "wrong_type")
        for index, target in enumerate(targets):
            if not isinstance(target, str):
                return _invalid(["targets", index], "wrong_type")
            if not _absolute(target):
                return _invalid(["targets", index], "invalid_value")
        files = tuple(str(target) for target in targets)
    return _Request(content, files, tuple(str(arg) for arg in args))


def _prerequisites() -> _Prerequisites:
    """Read authoritative exact pins and verify imports in this interpreter."""
    external: list[dict[str, str | None]] = []
    module = ""
    try:
        root = Path(__file__).parent
        descriptor = json.loads((root / "dependencies.json").read_text(encoding="utf-8"))
        native_tools = descriptor["native_tools"]
        if not isinstance(native_tools, list) or len(native_tools) != 1:
            raise ValueError("Invalid native dependency descriptor.")
        native = native_tools[0]
        module = native["module"]
        filename = native["requirements_file"]
        if not isinstance(module, str) or not re.fullmatch(r"[a-zA-Z_][\w.]*", module):
            raise ValueError("Invalid native module declaration.")
        if not isinstance(filename, str) or Path(filename).name != filename:
            raise ValueError("Invalid local requirements filename.")
        declarations = (root / filename).read_text(encoding="utf-8").splitlines()
        if not declarations:
            raise ValueError("Native requirements are empty.")
        problems: list[str] = []
        for declaration in declarations:
            match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s;]+)", declaration)
            if match is None:
                raise ValueError(f"Invalid exact requirement: {declaration!r}")
            name, expected = match.groups()
            try:
                actual = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError as exc:
                external.append({"tool_id": name, "version": None})
                problems.append(str(exc))
                continue
            external.append({"tool_id": name, "version": actual})
            if actual != expected:
                problems.append(f"{name}: actual {actual}, expected {expected}")
            try:
                importlib.import_module(name.replace("-", "_"))
            except ImportError as exc:
                problems.append(str(exc))
        importlib.import_module(module)
        return _Prerequisites(module, tuple(external), "; ".join(problems) or None)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, ImportError) as exc:
        return _Prerequisites(module, tuple(external), str(exc))


def _options(args: tuple[str, ...]) -> _Options:
    entries: list[tuple[str, str | bool]] = []
    files: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        index += 1
        if token == "--":
            files.extend(args[index:])
            break
        if not token.startswith("-") or token == "-":
            files.append(token)
            continue
        if token.startswith("--"):
            name, separator, attached = token[2:].partition("=")
            pending = [(name, attached if separator else None)]
        else:
            pending = []
            for position, alias in enumerate(token[1:], start=1):
                name = _SHORT_OPTIONS.get(alias, alias)
                rest = token[position + 1 :]
                if name in _VALUE_OPTIONS or rest.startswith("="):
                    pending.append((name, rest.removeprefix("=") if rest else None))
                    break
                pending.append((name, None))
        for name, attached in pending:
            value: str | bool = True
            if attached is not None:
                value = attached
            elif name in _VALUE_OPTIONS and index < len(args):
                value = args[index]
                index += 1
            entries.append((name, value))
    return _Options(tuple(entries), tuple(files))


def _guard(request: _Request, options: _Options) -> str | None:
    if any("\x00" in arg for arg in request.args):
        return "Native arguments contain a NUL character."
    if any(name in {"help", "version", "validator-class"} for name, _ in options.entries):
        return "Native metadata or validator-class mode is outside the read-only check boundary."
    if "-" in options.files or any(
        name == "schemafile" and value == "-" for name, value in options.entries
    ):
        return "Native stdin input replaces the selected source."
    if request.content:
        if options.files:
            return "Native positional inputs extend the proposed source."
        if any(name in {"data-transform", "fill-defaults"} for name, _ in options.entries):
            return "Native transforms alter the proposed data before validation."
    if any(Path(path).is_dir() for path in (*request.files, *options.files)):
        return "Native check-jsonschema requires literal instance files, not directories."
    return None


def _response(
    request: _Request,
    decision: dict[str, object],
    external: tuple[dict[str, str | None], ...],
    evidence: dict[str, object] | None = None,
) -> dict[str, object]:
    response: dict[str, object] = {"decision": decision, "external_tools": list(external)}
    if not request.content:
        response.update(coverage=None, required_targets=[])
    if evidence is not None:
        response["evidence"] = evidence
    return response


def _unavailable(
    request: _Request,
    prerequisites: _Prerequisites,
    reason: str,
    message: str,
    evidence: dict[str, object] | None = None,
) -> tuple[dict[str, object], int]:
    return _response(
        request,
        {"status": "unavailable", "reason": reason, "message": message},
        prerequisites.external_tools,
        evidence,
    ), 3


def _evidence(stdout: str, stderr: str) -> dict[str, object] | None:
    if not stderr.strip():
        try:
            return {"format": "json", "data": json.loads(stdout)}
        except json.JSONDecodeError:
            pass
    text = stdout + ("\nstderr:\n" + stderr if stdout and stderr else stderr)
    return {"format": "text", "data": text} if text else None


@dataclass(frozen=True)
class _NativeReport:
    message: str | None


def _complete_report(stdout: str, native_code: int) -> _NativeReport | None:
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    if not isinstance(report, dict):
        return None
    errors, parse_errors = report.get("errors", []), report.get("parse_errors", [])
    if not isinstance(errors, list) or not isinstance(parse_errors, list):
        return None
    if native_code == 0 and report.get("status") == "ok" and not errors and not parse_errors:
        return _NativeReport(None)
    if native_code != 1 or report.get("status") != "fail" or not (errors or parse_errors):
        return None
    messages: list[str] = []
    for item in [*errors, *parse_errors]:
        if not isinstance(item, dict):
            return None
        message = item.get("message")
        if not isinstance(message, str) or not message.strip():
            return None
        messages.append(message)
    return _NativeReport("\n".join(messages))


def _execute(request: _Request) -> tuple[dict[str, object], int]:
    prerequisites = _prerequisites()
    if prerequisites.error:
        return _unavailable(request, prerequisites, "dependency_unavailable", prerequisites.error)
    options = _options(request.args)
    guard = _guard(request, options)
    if guard:
        return _unavailable(request, prerequisites, "unsupported_input", guard)
    try:
        completed = subprocess.run(
            [sys.executable, "-m", prerequisites.module, *request.args, *request.files],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
        )
    except (OSError, ValueError) as exc:
        return _unavailable(request, prerequisites, "execution_error", str(exc))
    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    evidence = _evidence(stdout, stderr)
    report = _complete_report(stdout, completed.returncode)
    if report is not None:
        if completed.returncode == 0:
            return _response(
                request, {"status": "passed"}, prerequisites.external_tools, evidence
            ), 0
        return _response(
            request,
            {"status": "failed", "message": report.message},
            prerequisites.external_tools,
            evidence,
        ), 1
    if completed.returncode == 2 and "Usage:" in stderr:
        reason = "unsupported_input"
    elif completed.returncode == 1 and stderr.strip():
        reason = "invalid_configuration"
    elif completed.returncode in {0, 1}:
        reason = "invalid_result"
    else:
        reason = "execution_error"
    return _unavailable(
        request,
        prerequisites,
        reason,
        stderr.strip()
        or stdout.strip()
        or f"Native exit status {completed.returncode} without a complete validation report.",
        evidence,
    )


def main() -> int:
    try:
        request: object = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        response, code = _invalid([], "invalid_value"), 2
    else:
        validated = _validate(request)
        if isinstance(validated, dict):
            response, code = validated, 2
        else:
            response, code = _execute(validated)
    sys.stdout.buffer.write(
        json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
