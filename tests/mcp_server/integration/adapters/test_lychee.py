"""Native Lychee/check-v1 content and literal selection conformance."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree, which

import pytest
from jsonschema import Draft202012Validator
from pydantic import JsonValue, TypeAdapter

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader

DEFAULT_ARGS = ("--offline", "--cache=false", "--include-fragments")


@dataclass(frozen=True)
class LycheeRuntime:
    executable: Path
    workspace: Path


@dataclass(frozen=True)
class LycheePackage:
    runtime: LycheeRuntime
    launch: AdapterLaunch
    schema: Draft202012Validator


@pytest.fixture
def lychee_runtime(tmp_path: Path, pytestconfig: pytest.Config) -> LycheeRuntime:
    program = which("lychee")
    executable = (
        Path(program)
        if program
        else (
            pytestconfig.rootpath
            / "temp/link-probe-20260906/bin/lychee-x86_64-pc-windows-msvc/lychee.exe"
        )
    )
    assert executable.is_file(), "Install the declared Lychee native prerequisite"
    version = subprocess.run(
        [str(executable), "--version"], capture_output=True, check=True, timeout=10
    )
    assert version.stdout.decode().strip() == "lychee 0.24.2"
    workspace = tmp_path / "workspace with spaces"
    workspace.mkdir()
    return LycheeRuntime(executable, workspace)


def package_for(runtime: LycheeRuntime, tmp_path: Path, repo_root: Path) -> LycheePackage:
    root = tmp_path / "official packages" / "lychee"
    copytree(repo_root / "mcp_server/bundled_adapters/lychee", root)
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_check("lychee", "links")
    assert set(binding.capability.inputs) == {"content", "selection"}
    assert binding.capability.requires_file is True
    schema_path = repo_root / "mcp_server/execution/contracts/check_v1.schema.json"
    return LycheePackage(
        runtime,
        binding.launch,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def invoke(
    package: LycheePackage,
    request: dict[str, object],
    *,
    native_available: bool = True,
) -> tuple[int, dict[str, JsonValue]]:
    environment = {
        **os.environ,
        "PATH": str(package.runtime.executable.parent) + os.pathsep + os.environ.get("PATH", ""),
    }
    if not native_available:
        environment["PATH"] = ""
    result = subprocess.run(
        [str(package.launch.executable), *package.launch.args],
        input=json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.runtime.workspace.parent)},
                **request,
            }
        ).encode("utf-8"),
        cwd=package.runtime.workspace,
        capture_output=True,
        timeout=30,
        env=environment,
    )
    payload: JsonValue = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(payload, dict)
    package.schema.validate(payload)
    if result.returncode != 2:
        if "targets" in request:
            assert "coverage" in payload and payload["coverage"] is None
            assert payload["required_targets"] == []
        else:
            assert "coverage" not in payload and "required_targets" not in payload
    return result.returncode, payload


@pytest.mark.parametrize("broken", [False, True])
def test_native_self_toc_and_neighbor_snapshot(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    broken: bool,
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "docs" / "guide.md"
    target.parent.mkdir()
    neighbor = target.with_name("neighbor.md")
    neighbor.write_text("# Neighbor\n\n## Existing\n", encoding="utf-8")
    scratch = tmp_path / "validation" / "fresh invocation" / target.name
    scratch.parent.mkdir(parents=True)
    content = "# Guide\n\n## Existing\n\n[TOC](#existing)\n"
    content += "[Self](guide.md#existing)\n[Neighbor](neighbor.md#existing)\n"
    if broken:
        content += "[Bad TOC](#absent)\n[Bad self](guide.md#absent)\n"
        content += "[Bad neighbor](neighbor.md#absent)\n[Missing](missing.md)\n"
    scratch.write_text(content, encoding="utf-8")
    logical_url = target.as_uri()
    remap = "^" + re.escape(logical_url) + "(#.*)?$ " + scratch.as_uri() + "$1"
    args = (*DEFAULT_ARGS, "--format", "json")
    native_result = subprocess.run(
        [str(runtime.executable), *args, "--base-url", logical_url, "--remap", remap, str(scratch)],
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert native_result.returncode == (2 if broken else 0), (
        native_result.stdout,
        native_result.stderr,
    )
    assert not target.exists()
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(
        package,
        {
            "operation": "links",
            "target_path": str(target),
            "input_path": str(scratch),
            "args": list(args),
        },
    )
    assert code == (1 if broken else 0)
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == ("failed" if broken else "passed")
    assert response["external_tools"] == [{"tool_id": "lychee", "version": "0.24.2"}]
    native_report: JsonValue = TypeAdapter(JsonValue).validate_json(native_result.stdout)
    native_evidence = response["evidence"]
    assert isinstance(native_evidence, dict) and native_evidence["format"] == "json"
    assert native_facts(native_evidence["data"]) == native_facts(native_report)
    assert not target.exists()
    assert scratch.read_text(encoding="utf-8") == content
    assert neighbor.read_text(encoding="utf-8") == "# Neighbor\n\n## Existing\n"


@pytest.mark.parametrize("directory", [False, True])
def test_native_literal_selection(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    directory: bool,
) -> None:
    runtime = lychee_runtime
    selected = runtime.workspace / "[draft].md"
    selected.write_text("# Draft\n\n[Missing](missing.md)\n", encoding="utf-8")
    (runtime.workspace / "d.md").write_text("# Other\n\n[Self](#other)\n", encoding="utf-8")
    target = runtime.workspace if directory else selected
    literal = "".join(f"[{char}]" if char in "[]*?" else char for char in str(target))
    native_result = subprocess.run(
        [str(runtime.executable), *DEFAULT_ARGS, "--format", "json", literal],
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert native_result.returncode == 2, (native_result.stdout, native_result.stderr)
    report = json.loads(native_result.stdout)
    assert report["errors"] == 1
    assert report["total"] == (2 if directory else 1)
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(
        package,
        {
            "operation": "links",
            "targets": [str(target)],
            "args": [*DEFAULT_ARGS, "--format", "json"],
        },
    )
    assert code == 1
    native_evidence = response["evidence"]
    assert isinstance(native_evidence, dict) and native_evidence["format"] == "json"
    data = native_evidence["data"]
    assert isinstance(data, dict)
    assert data["errors"] == report["errors"]
    assert data["total"] == report["total"]


@pytest.mark.parametrize(
    ("case", "native_code", "expected_code", "reason"),
    [
        ("empty", 2, 3, "unsupported_input"),
        ("invalid-input", 1, 3, "unsupported_input"),
        ("unknown-option", 2, 3, "unsupported_input"),
        ("invalid-config", 3, 3, "invalid_configuration"),
        ("native-text", 2, 1, None),
    ],
)
def test_native_options_and_inability(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    case: str,
    native_code: int,
    expected_code: int,
    reason: str | None,
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "source.md"
    target.write_text("# Source\n\n[Missing](missing.md)\n", encoding="utf-8")
    invalid_config = runtime.workspace / "invalid.toml"
    invalid_config.write_text("not valid toml = [", encoding="utf-8")
    choices = {
        "empty": (),
        "invalid-input": (target.as_uri(),),
        "unknown-option": ("--nonexistent-option",),
        "invalid-config": ("--config", str(invalid_config)),
        "native-text": ("--format", "detailed"),
    }
    args = (*DEFAULT_ARGS, *choices[case])
    targets = [] if case in {"empty", "invalid-input"} else [str(target)]
    result = subprocess.run(
        [str(runtime.executable), *args, *targets],
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == native_code, (result.stdout, result.stderr)
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(package, {"operation": "links", "targets": targets, "args": list(args)})
    assert code == expected_code
    decision = response["decision"]
    assert isinstance(decision, dict) and decision.get("reason") == reason
    if case == "native-text":
        native_evidence = response["evidence"]
        assert isinstance(native_evidence, dict) and native_evidence["format"] == "text"
        data = native_evidence["data"]
        assert isinstance(data, str) and "missing.md" in data


def native_facts(value: JsonValue) -> JsonValue:
    """Compare native reports while excluding only per-run durations and ordering."""
    if isinstance(value, dict):
        return {key: native_facts(item) for key, item in value.items() if key != "duration"}
    if isinstance(value, list):
        return sorted((native_facts(item) for item in value), key=lambda item: json.dumps(item))
    return value


def test_missing_native_and_malformed_wire(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    package = package_for(lychee_runtime, tmp_path, pytestconfig.rootpath)
    request: dict[str, object] = {"operation": "links", "targets": [], "args": list(DEFAULT_ARGS)}
    code, response = invoke(package, request, native_available=False)
    assert code == 3
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "lychee", "version": None}]
    code, response = invoke(package, {**request, "extra": True})
    assert code == 2
    assert response["reason"] == "invalid_request"
    for invalid in ({**request, "operation": "other"}, {**request, "targets": ["relative.md"]}):
        code, response = invoke(package, invalid)
        assert code == 2 and response["reason"] == "invalid_request"


def test_declared_version_precedes_native_configuration(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    package = package_for(lychee_runtime, tmp_path, pytestconfig.rootpath)
    assert package.launch.args
    declaration = Path(package.launch.args[0]).with_name("dependencies.json")
    metadata = json.loads(declaration.read_text(encoding="utf-8"))
    metadata["native_tools"][0]["version"] = "0.0.0"
    declaration.write_text(json.dumps(metadata), encoding="utf-8")
    code, response = invoke(
        package,
        {"operation": "links", "targets": [], "args": ["--config", "missing.toml"]},
    )
    assert code == 3
    result = response["decision"]
    assert isinstance(result, dict) and result["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "lychee", "version": "0.24.2"}]
    message = str(result["message"])
    assert "actual=0.24.2" in message and "expected=0.0.0" in message
    assert "evidence" not in response


def test_source_and_write_options_are_refused(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    runtime = lychee_runtime
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    target = runtime.workspace / "source.md"
    target.write_text("# Source\n", encoding="utf-8")
    output = runtime.workspace / "forbidden-output"
    before = {path: path.read_bytes() for path in runtime.workspace.rglob("*") if path.is_file()}
    for args in (
        ("--output", str(output)),
        ("-vo" + str(output),),
        ("--cache=true",),
        ("--cookie-jar", str(output)),
        ("--preprocess", "echo replaced"),
        ("--dump",),
        ("--generate", "man"),
        ("--files-from", "-"),
        ("--method", "POST"),
    ):
        code, response = invoke(
            package,
            {
                "operation": "links",
                "targets": [str(target)],
                "args": list(args),
            },
        )
        assert code == 3, args
        decision = response["decision"]
        assert isinstance(decision, dict) and decision["reason"] == "unsupported_input", args
    code, response = invoke(
        package,
        {
            "operation": "links",
            "input_path": str(target),
            "target_path": str(runtime.workspace / "absent.md"),
            "args": ["--base-url", "https://example.invalid/"],
        },
    )
    assert code == 3
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["reason"] == "unsupported_input"
    assert before == {
        path: path.read_bytes() for path in runtime.workspace.rglob("*") if path.is_file()
    }


@pytest.mark.parametrize(
    ("filename", "section"),
    [
        ("lychee.toml", ""),
        ("Cargo.toml", "[package.metadata.lychee]\n"),
        ("Cargo.toml", "[workspace.metadata.lychee]\n"),
        ("pyproject.toml", "[tool.lychee]\n"),
    ],
)
def test_native_config_sources_cannot_enable_writes(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    filename: str,
    section: str,
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "source.md"
    target.write_text("# Source\n", encoding="utf-8")
    output = runtime.workspace / "forbidden-output"
    config = runtime.workspace / filename
    config.write_text(section + "output = " + json.dumps(str(output)) + "\n", encoding="utf-8")
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    for extra in ([], ["--config", str(config)]):
        code, response = invoke(
            package,
            {
                "operation": "links",
                "targets": [str(target)],
                "args": [*DEFAULT_ARGS, *extra],
            },
        )
        assert code == 3
        decision = response["decision"]
        assert isinstance(decision, dict) and decision["reason"] == "unsupported_input"
        assert not output.exists()


def test_native_configuration_precedence_and_safe_overrides(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "source.md"
    target.write_text("# Source\n\n[Missing](missing.md)\n", encoding="utf-8")
    first = runtime.workspace / "first.toml"
    first.write_text('cache = true\nmethod = "POST"\nformat = "json"\n', encoding="utf-8")
    second = runtime.workspace / "second.toml"
    second.write_text('cache = false\nmethod = "get"\nformat = "json"\n', encoding="utf-8")
    (runtime.workspace / "lychee.toml").write_text('format = "json"\n', encoding="utf-8")
    (runtime.workspace / "Cargo.toml").write_text(
        '[package.metadata.lychee]\noutput = "forbidden-output"\n',
        encoding="utf-8",
    )
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    for extra in (
        ("-c", str(first), "--method", "GET", "-f", "detailed"),
        ("--config", str(first), "--config", str(second)),
        (),
    ):
        args = (*DEFAULT_ARGS, *extra)
        result = subprocess.run(
            [str(runtime.executable), *args, str(target)],
            cwd=runtime.workspace,
            capture_output=True,
            timeout=30,
        )
        assert result.returncode == 2, (result.stdout, result.stderr)
        code, response = invoke(
            package,
            {
                "operation": "links",
                "targets": [str(target)],
                "args": list(args),
            },
        )
        assert code == 1
        item = response["evidence"]
        assert isinstance(item, dict)
        assert item["format"] == ("text" if "-f" in extra else "json")
    assert not (runtime.workspace / ".lycheecache").exists()
    assert not (runtime.workspace / "forbidden-output").exists()


def test_pinned_native_filename_stdin_preserves_internal_spaces_and_unicode(
    lychee_runtime: LycheeRuntime,
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "reference Ω with spaces.md"
    target.write_text("# Reference\n\n[Self](#reference)\n", encoding="utf-8")
    direct = subprocess.run(
        [str(runtime.executable), *DEFAULT_ARGS, "--format", "json", "--files-from", "-"],
        input=f"# comment\n\n{target}\n".encode(),
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert direct.returncode == 0, (direct.stdout, direct.stderr)
    report = json.loads(direct.stdout)
    assert report["total"] == 1 and report["errors"] == 0


def test_caller_option_terminator_preserves_owned_filename_selector(
    lychee_runtime: LycheeRuntime, tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    runtime = lychee_runtime
    target = runtime.workspace / "selected.md"
    target.write_text("# Selected\n\n[Missing](selected-missing.md)\n", encoding="utf-8")
    args = [*DEFAULT_ARGS, "--format", "json", "--"]
    direct = subprocess.run(
        [str(runtime.executable), *args, str(target)],
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert direct.returncode == 2
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(package, {"operation": "links", "targets": [str(target)], "args": args})
    assert code == 1
    evidence = response["evidence"]
    assert isinstance(evidence, dict) and evidence["format"] == "json"
    assert native_facts(evidence["data"]) == native_facts(json.loads(direct.stdout))


def oversized_sources(runtime: LycheeRuntime) -> list[str]:
    targets: list[str] = []
    for index in range(350):
        source = runtime.workspace / (f"input_{index:04d}_Ω_" + "selection_" * 5 + ".md")
        source.write_text("# Source\n\n[Self](#source)\n", encoding="utf-8")
        targets.append(str(source))
    Path(targets[-1]).write_text("# Late\n\n[Missing](late-missing.md)\n", encoding="utf-8")
    assert len(" ".join(targets).encode("utf-16-le")) // 2 > 32_767
    return targets


def test_complete_oversized_selection_keeps_late_native_link_result(
    lychee_runtime: LycheeRuntime, tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    runtime = lychee_runtime
    targets = oversized_sources(runtime)
    outside = runtime.workspace / "outside.md"
    outside.write_text("# Outside\n\n[Decoy](outside-decoy.md)\n", encoding="utf-8")
    direct = subprocess.run(
        [str(runtime.executable), *DEFAULT_ARGS, "--format", "json", targets[0], targets[-1]],
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert direct.returncode == 2
    control = json.loads(direct.stdout)
    assert control["errors"] == 1 and control["total"] == 2
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(
        package, {"operation": "links", "targets": targets, "args": list(DEFAULT_ARGS)}
    )
    assert code == 1
    evidence = response["evidence"]
    assert isinstance(evidence, dict) and evidence["format"] == "json"
    data = evidence["data"]
    assert isinstance(data, dict)
    assert data["errors"] == 1 and data["total"] == len(targets)
    assert "late-missing.md" in json.dumps(data)
    assert "outside-decoy.md" not in json.dumps(data)


@pytest.mark.parametrize("source", ["cli", "config"])
def test_occupied_files_from_channel_preserves_native_inputs(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    source: str,
) -> None:
    runtime = lychee_runtime
    selected = runtime.workspace / "selected.md"
    selected.write_text("# Selected\n\n[Self](#selected)\n", encoding="utf-8")
    additional = runtime.workspace / "native additional.md"
    additional.write_text("# Additional\n\n[Missing](native-missing.md)\n", encoding="utf-8")
    supplied = runtime.workspace / "caller filenames.txt"
    supplied.write_text(str(additional) + "\n", encoding="utf-8")
    args = list(DEFAULT_ARGS)
    if source == "cli":
        args.extend(["--files-from", str(supplied)])
    else:
        (runtime.workspace / "lychee.toml").write_text(
            "files_from = " + json.dumps(str(supplied)) + "\n", encoding="utf-8"
        )
    direct = subprocess.run(
        [str(runtime.executable), *args, "--format", "json", str(selected)],
        cwd=runtime.workspace,
        capture_output=True,
        timeout=30,
    )
    assert direct.returncode == 2
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(
        package, {"operation": "links", "targets": [str(selected)], "args": args}
    )
    assert code == 1
    evidence = response["evidence"]
    assert isinstance(evidence, dict) and evidence["format"] == "json"
    assert native_facts(evidence["data"]) == native_facts(json.loads(direct.stdout))


@pytest.mark.parametrize("suffix", ["\n", "\ud800"])
def test_unrepresentable_stdin_filename_is_explicitly_refused(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    suffix: str,
) -> None:
    package = package_for(lychee_runtime, tmp_path, pytestconfig.rootpath)
    target = str(lychee_runtime.workspace / "source.md") + suffix
    code, response = invoke(
        package, {"operation": "links", "targets": [target], "args": list(DEFAULT_ARGS)}
    )
    assert code == 3
    result = response["decision"]
    assert isinstance(result, dict) and result["reason"] == "unsupported_input"


@pytest.mark.skipif(os.name != "nt", reason="Windows native argv launch limit")
def test_occupied_files_from_large_selection_reports_remaining_argv_limit(
    lychee_runtime: LycheeRuntime, tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    runtime = lychee_runtime
    targets = oversized_sources(runtime)
    supplied = runtime.workspace / "caller list.txt"
    supplied.write_text(targets[0] + "\n", encoding="utf-8")
    package = package_for(runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(
        package,
        {
            "operation": "links",
            "targets": targets,
            "args": [*DEFAULT_ARGS, "--files-from", str(supplied)],
        },
    )
    assert code == 3
    result = response["decision"]
    assert isinstance(result, dict) and result["reason"] == "execution_error"
    message = str(result["message"]).casefold()
    assert "files-from" in message and "occupied" in message and "argv" in message
