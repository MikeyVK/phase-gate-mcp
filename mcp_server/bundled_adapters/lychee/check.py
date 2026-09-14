"""Native Lychee links check/v1 adapter."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

_REQUEST_CONTENT_KEYS = frozenset({"operation", "target_path", "input_path", "args"})
_REQUEST_SELECTION_KEYS = frozenset({"operation", "targets", "args"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
_BARE_UNC_ROOT = re.compile(r"^\\\\[^\\/]+[\\/][^\\/]+$")
# Token arities from the supported native CLI; all option semantics stay native.
_VALUE_OPTIONS = frozenset(
    {
        "accept",
        "archive",
        "base",
        "base_url",
        "basic_auth",
        "config",
        "cache_exclude_status",
        "cookie_jar",
        "default_extension",
        "exclude",
        "exclude_file",
        "exclude_path",
        "extensions",
        "format",
        "fallback_extensions",
        "files_from",
        "generate",
        "github_token",
        "header",
        "host_concurrency",
        "host_request_interval",
        "include",
        "index_files",
        "max_redirects",
        "max_cache_age",
        "max_concurrency",
        "max_retries",
        "min_tls",
        "mode",
        "output",
        "preprocess",
        "retry_wait_time",
        "remap",
        "root_dir",
        "scheme",
        "timeout",
        "threads",
        "user_agent",
        "method",
    }
)
_SHORT_OPTIONS = {
    "a": "accept",
    "b": "base_url",
    "c": "config",
    "E": "exclude_all_private",
    "f": "format",
    "h": "help",
    "H": "header",
    "i": "insecure",
    "m": "max_redirects",
    "n": "no_progress",
    "o": "output",
    "p": "preprocess",
    "q": "quiet",
    "r": "retry_wait_time",
    "s": "scheme",
    "t": "timeout",
    "T": "threads",
    "u": "user_agent",
    "v": "verbose",
    "V": "version",
    "X": "method",
}
_BOUNDARY_FIELDS = frozenset(
    {
        "cache",
        "output",
        "cookie_jar",
        "preprocess",
        "dump",
        "dump_inputs",
        "generate",
        "method",
        "files_from",
        "base",
        "base_url",
        "remap",
        "format",
        "mode",
    }
)


@dataclass(frozen=True)
class _Options:
    entries: tuple[tuple[str, str | bool], ...]
    inputs: tuple[str, ...]


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
    parts = [part for part in re.split(r"[\\/]", value) if part]
    return bool(parts) and parts[-1] not in {".", ".."}


def _validate_args(args: object) -> tuple[str, ...] | dict[str, object]:
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        return _invalid([_issue(["args"], "wrong_type")])
    return tuple(args)


def _validate_request(
    value: object,
) -> tuple[str, tuple[str, ...], tuple[str, ...]] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([_issue([], "wrong_type")])
    content = "input_path" in value or "target_path" in value
    expected = _REQUEST_CONTENT_KEYS if content else _REQUEST_SELECTION_KEYS
    unknown = sorted(str(key) for key in set(value) - expected)
    missing = sorted(expected - set(value))
    if unknown:
        return _invalid([_issue([key], "unknown_field") for key in unknown])
    if missing:
        return _invalid([_issue([key], "missing_field") for key in missing])
    if not isinstance(value["operation"], str):
        return _invalid([_issue(["operation"], "wrong_type")])
    if value["operation"] != "links":
        return _invalid([_issue(["operation"], "invalid_value")])
    args = _validate_args(value["args"])
    if isinstance(args, dict):
        return args
    if content:
        for field in ("target_path", "input_path"):
            if not isinstance(value[field], str):
                return _invalid([_issue([field], "wrong_type")])
            if not _valid_absolute_file_path(value[field]):
                return _invalid([_issue([field], "invalid_value")])
        return "content", (value["target_path"], value["input_path"]), args
    if not isinstance(value["targets"], list):
        return _invalid([_issue(["targets"], "wrong_type")])
    for index, item in enumerate(value["targets"]):
        if not isinstance(item, str):
            return _invalid([_issue(["targets", index], "wrong_type")])
        if not item or "\x00" in item or _ABSOLUTE_PATH.fullmatch(item) is None:
            return _invalid([_issue(["targets", index], "invalid_value")])
    return "selection", tuple(value["targets"]), args


def _option_parts(args: tuple[str, ...]) -> _Options:
    """Read native token boundaries without interpreting its rule configuration."""
    entries: list[tuple[str, str | bool]] = []
    inputs: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        index += 1
        if token == "--":
            inputs.extend(args[index:])
            break
        if not token.startswith("-") or token == "-":
            inputs.append(token)
            continue
        if token.startswith("--"):
            name, separator, long_value = token[2:].partition("=")
            pending = [(name.replace("-", "_"), long_value if separator else None)]
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
            if name in {"cache", "dump", "dump_inputs"} and isinstance(value, str):
                value = {"true": True, "false": False}.get(value, value)
            entries.append((name, value))
    return _Options(tuple(entries), tuple(inputs))


def _section(data: dict[str, object], keys: tuple[str, ...]) -> dict[str, object] | None:
    value: object = data
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value if isinstance(value, dict) else None


def _config_projection(path: Path) -> dict[str, object] | None:
    """Read only native fields affecting this role; native Lychee validates settings."""
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    if path.name == "Cargo.toml":
        selected = _section(data, ("package", "metadata", "lychee"))
        if selected is None:
            selected = _section(data, ("workspace", "metadata", "lychee"))
    elif path.name == "pyproject.toml":
        selected = _section(data, ("tool", "lychee"))
    else:
        selected = data
    if selected is None:
        return None
    return {key: value for key, value in selected.items() if key in _BOUNDARY_FIELDS}


def _effective_settings(options: _Options) -> dict[str, object]:
    paths = [value for key, value in options.entries if key == "config"]
    settings: dict[str, object] = {}
    if paths:
        for path in paths:
            if not isinstance(path, str):
                raise ValueError("The native --config option requires a filename.")
            projected = _config_projection(Path(path))
            if projected is not None:
                # Native optional fields replace; remaps chain with later files first.
                remaps, previous = projected.get("remap"), settings.get("remap", [])
                if isinstance(remaps, list) and isinstance(previous, list):
                    projected["remap"] = remaps + previous
                settings.update(projected)
    else:
        # Native 0.24.2 selects the first recognized file/section in workspace cwd.
        for name in ("lychee.toml", "Cargo.toml", "pyproject.toml"):
            default_path = Path(name)
            if default_path.exists():
                projected = _config_projection(default_path)
                if projected is not None:
                    settings.update(projected)
                    break
    for key, value in options.entries:
        if key in _BOUNDARY_FIELDS:
            if key == "remap":
                previous = settings.get(key, [])
                settings[key] = [value, *previous] if isinstance(previous, list) else [value]
            else:
                settings[key] = value
    return settings


def _guard(options: _Options, settings: dict[str, object], content: bool) -> str | None:
    if any(name in {"help", "version"} for name, _ in options.entries):
        return "Native help/version does not perform link checking."
    if "-" in options.inputs or (content and options.inputs):
        return "The native arguments replace or extend the supplied content input."
    if any(
        settings.get(field) is not None
        for field in (
            "output",
            "cookie_jar",
            "preprocess",
            "generate",
        )
    ):
        return "The effective native configuration writes output or bypasses link checking."
    if any(settings.get(field) is True for field in ("cache", "dump", "dump_inputs")):
        return "Native caching or dump mode is outside the check contract."
    method = settings.get("method", "get")
    if not isinstance(method, str) or method.casefold() not in {"get", "head"}:
        return "Only native GET/HEAD requests belong to this check."
    if settings.get("files_from") == "-" or (content and settings.get("files_from") is not None):
        return "The effective files-from option replaces the supplied input."
    if content and any(settings.get(field) for field in ("base", "base_url", "remap")):
        return "The proposed-content check owns its logical base and exact self remap."
    return None


def _logical_url(path: str) -> str:
    return Path(path).as_uri()


def _remap(logical: str, physical: str) -> str:
    return f"^{re.escape(logical)}(#.*)?$ {_logical_url(physical)}$1"


def _response(
    decision: dict[str, object], version: str | None, evidence: dict[str, object] | None = None
) -> dict[str, object]:
    response: dict[str, object] = {
        "decision": decision,
        "external_tools": [{"tool_id": "lychee", "version": version}],
    }
    if evidence is not None:
        response["evidence"] = evidence
    return response


def _unavailable(
    reason: str, message: str, version: str | None = None, evidence: dict[str, object] | None = None
) -> tuple[dict[str, object], int]:
    return _response(
        {"status": "unavailable", "reason": reason, "message": message}, version, evidence
    ), 3


def _native_evidence(stdout: str, stderr: str, json_mode: bool) -> dict[str, object] | None:
    if json_mode and not stderr.strip():
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError:
            parsed = None
        if parsed is not None:
            return {"format": "json", "data": parsed}
    data = stdout
    if stderr:
        data = f"{data}\nstderr:\n{stderr}" if data else stderr
    return {"format": "text", "data": data} if data else None


def _run(request: object) -> tuple[dict[str, object], int]:
    validated = _validate_request(request)
    if isinstance(validated, dict):
        return validated, 2
    operation, payload, args = validated
    response, exit_code = _execute(operation, payload, args)
    if operation == "selection":
        response.update(coverage=None, required_targets=[])
    return response, exit_code


def _execute(
    operation: str, payload: tuple[str, ...], args: tuple[str, ...]
) -> tuple[dict[str, object], int]:
    if any("\x00" in arg for arg in args):
        return _unavailable("unsupported_input", "Native arguments may not contain NUL.")
    executable = shutil.which("lychee")
    if executable is None or Path(executable).suffix.lower() in {".cmd", ".bat", ".ps1"}:
        return _unavailable("dependency_unavailable", "Lychee executable is unavailable.")
    try:
        version_result = subprocess.run([executable, "--version"], capture_output=True, check=False)
    except OSError as exc:
        return _unavailable("dependency_unavailable", f"Lychee version lookup failed: {exc}")
    version_text = version_result.stdout.decode("utf-8", errors="replace").strip()
    version = version_text.removeprefix("lychee ").strip() or None
    if version_result.returncode != 0 or version is None:
        return _unavailable("dependency_unavailable", "Lychee did not report a usable version.")
    options = _option_parts(args)
    try:
        settings = _effective_settings(options)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        return _unavailable(
            "invalid_configuration", f"Cannot inspect native configuration: {exc}", version
        )
    except ValueError as exc:
        return _unavailable("unsupported_input", str(exc), version)
    guard = _guard(options, settings, operation == "content")
    if guard is not None:
        return _unavailable("unsupported_input", guard, version)
    command = [executable]
    if "format" not in settings and "mode" not in settings:
        command.extend(["--format", "json"])
        settings["format"] = "json"
    if operation == "content":
        target_path, input_path = payload
        try:
            logical = _logical_url(target_path)
            command.extend(["--base-url", logical, "--remap", _remap(logical, input_path)])
        except ValueError as exc:
            return _unavailable("unsupported_input", str(exc), version)
        targets: tuple[str, ...] = (input_path,)
    else:
        targets = payload
    command.extend(args)
    command.extend(_escape_selection_targets(targets))
    try:
        completed = subprocess.run(command, capture_output=True, check=False)
    except OSError as exc:
        return _unavailable("execution_error", f"Lychee execution failed: {exc}", version)
    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    evidence = _native_evidence(stdout, stderr, settings.get("format") == "json")
    if completed.returncode == 0:
        return _response({"status": "passed"}, version, evidence), 0
    if completed.returncode == 3:
        return _unavailable(
            "invalid_configuration",
            "Lychee rejected its effective configuration.",
            version,
            evidence,
        )
    if completed.returncode == 2:
        if stderr.lstrip().startswith("error:") and "\nUsage:" in stderr:
            return _unavailable(
                "unsupported_input", "Lychee rejected the native request.", version, evidence
            )
        if not stdout.strip():
            return _unavailable(
                "invalid_result", "Lychee returned no substantive link report.", version, evidence
            )
        return _response(
            {"status": "failed", "message": "Lychee reported broken links."}, version, evidence
        ), 1
    bad_input = stderr.startswith(
        ("Error: Cannot parse inputs", "Error: URL is missing a hostname")
    )
    reason = "unsupported_input" if bad_input else "execution_error"
    return _unavailable(reason, "Lychee could not perform link checking.", version, evidence)


def _escape_selection_targets(targets: tuple[str, ...]) -> tuple[str, ...]:
    escaped: list[str] = []
    replacements = {"[": "[[]", "]": "[]]", "*": "[*]", "?": "[?]"}
    for target in targets:
        target = "".join(replacements.get(char, char) for char in target)
        escaped.append(target)
    return tuple(escaped)


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
