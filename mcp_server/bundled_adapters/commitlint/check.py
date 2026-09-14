"""Commitlint message/check-v1 adapter with native parsing and provenance reading."""

from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys
from shutil import which
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_server.core.interfaces.artifact_header_reader import IArtifactHeaderReader

_REQUEST_KEYS = frozenset({"operation", "target_path", "content", "args"})
_ABSOLUTE_PATH = re.compile(r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$")
_BARE_UNC_ROOT = re.compile(r"^\\\\[^\\/]+[\\/][^\\/]+$")

# The installed parser owns tokenization. These native CLI types/aliases only guard
# input substitution and early-return modes; they never load --options files.
_NATIVE_GUARD = r"""
const {createRequire} = require("node:module");
const path = require("node:path");
const {pathToFileURL} = require("node:url");
(async () => {
  let version = null;
  try {
    const workspaceRequire = createRequire(path.join(process.cwd(), "package.json"));
    const packagePath = workspaceRequire.resolve("@commitlint/cli/package.json");
    const cliRequire = createRequire(packagePath);
    const pkg = cliRequire(packagePath);
    version = pkg.version;
    const yargsRequire = createRequire(cliRequire.resolve("yargs"));
    const {default: parse} = await import(pathToFileURL(yargsRequire.resolve("yargs-parser")));
    const result = parse.detailed(JSON.parse(process.argv[1]), {
      boolean: ["color", "default-config", "from-last-tag", "last", "quiet",
                "verbose", "legacy-output", "strict", "version", "help"],
      string: ["config", "print-config", "cwd", "edit", "env", "help-url",
               "from", "git-log-args", "format", "parser-preset", "to", "options"],
      array: ["extends"],
      alias: {color: "c", config: "g", cwd: "d", edit: "e", env: "E",
              extends: "x", "help-url": "H", from: "f", last: "l",
              format: "o", "parser-preset": "p", quiet: "q", to: "t",
              verbose: "V", strict: "s", version: "v", help: "h"},
    });
    const forbidden = ["edit", "env", "from", "to", "from-last-tag", "git-log-args",
                       "last", "options", "help", "version", "print-config"];
    const blocked = forbidden.find(key =>
      Object.hasOwn(result.argv, key) || Object.hasOwn(result.argv,
        key.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())));
    if (result.error || blocked) {
      process.stdout.write(JSON.stringify({
        version, reason: "unsupported_input",
        message: result.error?.message ??
          ("Option --" + blocked + " bypasses supplied-message checking."),
      }));
      return;
    }
    process.stdout.write(JSON.stringify({
      version, cli: path.resolve(path.dirname(packagePath), pkg.bin.commitlint),
    }));
  } catch (error) {
    process.stdout.write(JSON.stringify({
      version, reason: "dependency_unavailable", message: String(error),
    }));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
"""


def _invalid(location: list[str | int], code: str) -> dict[str, object]:
    return {"reason": "invalid_request", "details": [{"location": location, "code": code}]}


def _validate(value: object) -> tuple[str, list[str]] | dict[str, object]:
    if not isinstance(value, dict):
        return _invalid([], "wrong_type")
    for key in sorted(set(value) - _REQUEST_KEYS):
        return _invalid([str(key)], "unknown_field")
    for key in sorted(_REQUEST_KEYS - set(value)):
        return _invalid([key], "missing_field")
    for key in ("operation", "target_path", "content"):
        if not isinstance(value[key], str):
            return _invalid([key], "wrong_type")
    if value["operation"] != "message":
        return _invalid(["operation"], "invalid_value")
    path = value["target_path"]
    if (
        not path
        or "\x00" in path
        or _ABSOLUTE_PATH.fullmatch(path) is None
        or _BARE_UNC_ROOT.fullmatch(path) is not None
        or path.endswith(("/", "\\"))
        or re.split(r"[\\/]", path)[-1] in {".", ".."}
    ):
        return _invalid(["target_path"], "invalid_value")
    args = value["args"]
    if not isinstance(args, list) or any(not isinstance(arg, str) for arg in args):
        return _invalid(["args"], "wrong_type")
    return value["content"], list(args)


def _unavailable(
    reason: str,
    message: str,
    version: str | None = None,
    evidence: dict[str, object] | None = None,
) -> tuple[dict[str, object], int]:
    response: dict[str, object] = {
        "decision": {"status": "unavailable", "reason": reason, "message": message},
        "external_tools": [{"tool_id": "commitlint", "version": version}],
    }
    if evidence is not None:
        response["evidence"] = evidence
    return response, 3


def _message_view(content: str, reader: IArtifactHeaderReader) -> tuple[str, bool]:
    recognized = reader.read(content).provenance is not None
    return (content.partition("\n")[2], True) if recognized else (content, False)


def _evidence(
    content: str, stripped: bool, result: subprocess.CompletedProcess[bytes]
) -> dict[str, object]:
    view = "first valid provenance line removed" if stripped else "original supplied content"
    return {
        "format": "text",
        "data": (
            f"checked message view ({view}):\n{content}\n"
            f"native exit code: {result.returncode}\n"
            f"stdout:\n{result.stdout.decode('utf-8', errors='replace')}\n"
            f"stderr:\n{result.stderr.decode('utf-8', errors='replace')}"
        ),
    }


def _empty_rules(stdout: bytes) -> bool:
    text = stdout.decode("utf-8", errors="replace")
    try:
        report = json.loads(text)
    except json.JSONDecodeError:
        # Default native formatter: inspect the final diagnostic before its summary,
        # never the echoed input or a caller-supplied help URL.
        plain = re.sub(r"\x1b\[[0-9;]*m", "", text)
        diagnostics, separator, summary = plain.rpartition("\n\n✖   found ")
        return (
            bool(separator)
            and summary.startswith("1 problems, 0 warnings")
            and diagnostics.endswith(" [empty-rules]")
        )
    if not isinstance(report, dict) or not isinstance(report.get("results"), list):
        return False
    return any(
        isinstance(result, dict)
        and isinstance(result.get("errors"), list)
        and any(
            isinstance(error, dict) and error.get("name") == "empty-rules"
            for error in result["errors"]
        )
        for result in report["results"]
    )


def _failure_reason(result: subprocess.CompletedProcess[bytes]) -> str | None:
    if result.returncode == 9 or _empty_rules(result.stdout):
        return "invalid_configuration"
    # Native usage and load failures go to stderr; stdout also contains user input.
    lowered = result.stderr.decode("utf-8", errors="replace").casefold()
    if any(
        marker in lowered
        for marker in (
            "unknown argument",
            "invalid values:",
            "not enough arguments",
            "[input] is required",
            "the specified --cwd",
        )
    ):
        return "unsupported_input"
    if any(
        marker in lowered
        for marker in (
            "cannot find module",
            "cannot find package",
            "err_module_not_found",
        )
    ):
        return "dependency_unavailable"
    if result.stderr.strip():
        if any(
            marker in lowered
            for marker in (
                "config",
                "syntaxerror",
                "enoent",
                "invalid rule",
                "rangeerror",
            )
        ):
            return "invalid_configuration"
        return "execution_error"
    if result.returncode not in {1, 2, 3}:
        return "execution_error"
    if not result.stdout.strip():
        return "invalid_result"
    return None


def _run(
    content: str, args: list[str], reader: IArtifactHeaderReader
) -> tuple[dict[str, object], int]:
    node = which("node")
    if node is None:
        return _unavailable("dependency_unavailable", "Node executable is unavailable.")
    if any("\x00" in arg for arg in args):
        return _unavailable("unsupported_input", "Native arguments may not contain NUL.")
    environment = {**os.environ, "JITI_FS_CACHE": "0"}
    try:
        guard = subprocess.run(
            [node, "-e", _NATIVE_GUARD, json.dumps(args)],
            capture_output=True,
            check=False,
            env=environment,
        )
    except OSError as exc:
        return _unavailable("execution_error", str(exc))
    try:
        info = json.loads(guard.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _unavailable("invalid_result", "Native prerequisite probe returned invalid data.")
    if not isinstance(info, dict) or guard.returncode:
        return _unavailable("execution_error", "Native prerequisite probe could not complete.")
    version = info.get("version")
    if not isinstance(version, str):
        version = None
    if "reason" in info:
        return _unavailable(str(info["reason"]), str(info["message"]), version)
    cli = info.get("cli")
    if not isinstance(cli, str):
        return _unavailable("invalid_result", "Native CLI entrypoint is unavailable.", version)
    message, stripped = _message_view(content, reader)
    try:
        result = subprocess.run(
            [node, cli, *args],
            input=message.encode("utf-8"),
            capture_output=True,
            check=False,
            env=environment,
        )
    except (OSError, UnicodeEncodeError) as exc:
        return _unavailable("execution_error", str(exc), version)
    evidence = _evidence(message, stripped, result)
    if result.returncode:
        reason = _failure_reason(result) if message.strip() else "unsupported_input"
        if reason is not None:
            return _unavailable(
                reason, "Commitlint could not provide a message-check result.", version, evidence
            )
        return {
            "decision": {"status": "failed", "message": "Commitlint rejected the checked message."},
            "external_tools": [{"tool_id": "commitlint", "version": version}],
            "evidence": evidence,
        }, 1
    return {
        "decision": {"status": "passed"},
        "external_tools": [{"tool_id": "commitlint", "version": version}],
        "evidence": evidence,
    }, 0


def main() -> int:
    """Compose the installed pure reader and run exactly one supplied request."""
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        response, code = _invalid([], "invalid_value"), 2
    else:
        validated = _validate(request)
        if isinstance(validated, dict):
            response, code = validated, 2
        else:
            try:
                module = importlib.import_module("mcp_server.services.artifact_header_reader")
            except ImportError as exc:
                response, code = _unavailable("dependency_unavailable", str(exc))
            else:
                response, code = _run(*validated, module.ArtifactHeaderReader())
    payload = json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(payload + b"\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
