# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=4obIYmqMTT5tMpqf sf=2JPaeqdf6mSOUgvn

"""Native check-jsonschema/check-v1 conformance in isolated packages."""

from __future__ import annotations

import importlib.metadata
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree

import pytest
from jsonschema import Draft202012Validator
from pydantic import JsonValue, TypeAdapter

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader


@dataclass(frozen=True)
class CheckerPackage:
    launch: AdapterLaunch
    root: Path
    workspace: Path
    response_schema: Draft202012Validator


@pytest.fixture
def checker_package(tmp_path: Path, pytestconfig: pytest.Config) -> CheckerPackage:
    root = tmp_path / "official packages" / "check_jsonschema"
    copytree(pytestconfig.rootpath / "mcp_server/bundled_adapters/check_jsonschema", root)
    workspace = tmp_path / "workspace with spaces"
    workspace.mkdir()
    copytree(
        pytestconfig.rootpath / ".pgmcp/config/check_schemas",
        workspace / ".pgmcp/config/check_schemas",
    )
    loader = ConfigLoader(tmp_path / "config")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    yaml_binding = catalog.get_check("check_jsonschema", "yaml_configuration")
    schema_binding = catalog.get_check("check_jsonschema", "json_schema")
    for binding in (yaml_binding, schema_binding):
        assert set(binding.capability.inputs) == {"content", "selection"}
        assert binding.capability.requires_file is True
    assert yaml_binding.capability.configured_targets == "yaml_sources"
    assert schema_binding.capability.configured_targets == "json_schema_sources"
    contract = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return CheckerPackage(
        yaml_binding.launch,
        root,
        workspace,
        Draft202012Validator(json.loads(contract.read_text(encoding="utf-8"))),
    )


def invoke(
    package: CheckerPackage,
    request: dict[str, object],
    *,
    python_args: tuple[str, ...] = (),
    raw: bytes | None = None,
) -> tuple[int, dict[str, JsonValue]]:
    payload = (
        raw
        if raw is not None
        else json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.workspace.parent)},
                **request,
            }
        ).encode("utf-8")
    )
    result = subprocess.run(
        [str(package.launch.executable), *python_args, *package.launch.args],
        input=payload,
        cwd=package.workspace,
        capture_output=True,
        timeout=40,
    )
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
    response: JsonValue = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(response, dict)
    package.response_schema.validate(response)
    if result.returncode != 2:
        if "targets" in request:
            assert response["coverage"] is None
            assert response["required_targets"] == []
        else:
            assert "coverage" not in response and "required_targets" not in response
    return result.returncode, response


def decision(response: dict[str, JsonValue]) -> dict[str, JsonValue]:
    result = response["decision"]
    assert isinstance(result, dict)
    return result


def native_args(mode: str) -> list[str]:
    if mode == "metaschema":
        return ["--check-metaschema", "--force-filetype", "json", "--output-format", "JSON"]
    filename = "yaml_configuration" if mode == "yaml" else "json_schema_source"
    return [
        "--schemafile",
        f".pgmcp/config/check_schemas/{filename}.schema.json",
        "--force-filetype",
        "yaml" if mode == "yaml" else "json",
        "--output-format",
        "JSON",
    ]


def selection(
    targets: tuple[Path, ...], args: list[str], operation: str = "json_schema"
) -> dict[str, object]:
    return {"operation": operation, "targets": [str(path) for path in targets], "args": args}


@pytest.mark.parametrize(
    ("mode", "source", "expected"),
    [
        ("yaml", "enabled: true\ncount: 2\n", 0),
        ("yaml", "- sequence\n", 1),
        ("shape", '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}', 0),
        ("shape", '{"type":"object"}', 1),
        (
            "metaschema",
            '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}',
            0,
        ),
        ("metaschema", '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":7}', 1),
        ("metaschema", '{"type":', 1),
    ],
    ids=[
        "yaml-pass",
        "yaml-root-fail",
        "shape-pass",
        "shape-fail",
        "meta-pass",
        "meta-fail",
        "parse-fail",
    ],
)
def test_source_family_native_results(
    checker_package: CheckerPackage,
    mode: str,
    source: str,
    expected: int,
) -> None:
    package = checker_package
    target = package.workspace / (
        "[source] sample.yaml" if mode == "yaml" else "[source] sample.schema.json"
    )
    target.write_text(source, encoding="utf-8")
    args = native_args(mode)
    direct = subprocess.run(
        [sys.executable, "-m", "check_jsonschema", *args, str(target)],
        cwd=package.workspace,
        capture_output=True,
        timeout=30,
    )
    assert direct.returncode == expected, (direct.stdout, direct.stderr)
    code, response = invoke(
        package,
        selection((target,), args, "yaml_configuration" if mode == "yaml" else "json_schema"),
    )
    assert code == expected
    assert decision(response)["status"] == ("passed" if expected == 0 else "failed")
    evidence = response["evidence"]
    assert isinstance(evidence, dict) and evidence["format"] == "json"
    assert evidence["data"] == TypeAdapter(JsonValue).validate_json(direct.stdout)
    if expected:
        assert decision(response)["message"]
    tools = response["external_tools"]
    assert isinstance(tools, list)
    actual = {}
    for tool in tools:
        assert isinstance(tool, dict) and isinstance(tool["tool_id"], str)
        actual[tool["tool_id"]] = tool["version"]
    for distribution in ("check-jsonschema", "orjson", "ruamel.yaml", "jsonschema"):
        assert actual[distribution] == importlib.metadata.version(distribution)
    assert target.read_text(encoding="utf-8") == source


@pytest.mark.parametrize("broken", [False, True])
def test_content_checks_proposal_and_preserves_original(
    checker_package: CheckerPackage, broken: bool
) -> None:
    package = checker_package
    original = package.workspace / "settings.yaml"
    original.write_text("original: value\n", encoding="utf-8")
    proposed = package.workspace.parent / "proposal.yaml"
    source = "- not a mapping\n" if broken else "replacement: 3\n"
    proposed.write_text(source, encoding="utf-8")
    code, response = invoke(
        package,
        {
            "operation": "yaml_configuration",
            "target_path": str(original),
            "input_path": str(proposed),
            "args": native_args("yaml"),
        },
    )
    assert code == (1 if broken else 0)
    assert decision(response)["status"] == ("failed" if broken else "passed")
    assert original.read_text(encoding="utf-8") == "original: value\n"
    assert proposed.read_text(encoding="utf-8") == source


def test_configured_explicit_file_operands(checker_package: CheckerPackage) -> None:
    package = checker_package
    target = package.workspace / "draft.schema.json"
    target.write_text(
        '{"$schema":"https://json-schema.org/draft/2020-12/schema"}', encoding="utf-8"
    )
    code, response = invoke(package, selection((), [*native_args("shape"), str(target)]))
    assert code == 0 and decision(response)["status"] == "passed"


@pytest.mark.parametrize(
    "case",
    [
        "empty",
        "directory",
        "help",
        "version",
        "validator",
        "stdin",
        "extra-file",
        "transform",
        "defaults",
    ],
)
def test_unsupported_selection_and_content_modes(
    checker_package: CheckerPackage, case: str
) -> None:
    package = checker_package
    target = package.workspace / "draft.yaml"
    target.write_text("key: value\n", encoding="utf-8")
    args = native_args("yaml")
    request = selection((target,), args, "yaml_configuration")
    if case == "empty":
        request = selection((), args, "yaml_configuration")
    elif case == "directory":
        request = selection((package.workspace,), args, "yaml_configuration")
    elif case in ("help", "version"):
        request["args"] = [*args, f"--{case}"]
    elif case == "validator":
        request["args"] = [*args, "--validator-class", "pathlib:Path"]
    elif case == "stdin":
        request["args"] = [*args, "-"]
    else:
        additions = {
            "extra-file": [str(target)],
            "transform": ["--data-transform=gitlab-ci"],
            "defaults": ["--fill-defaults"],
        }
        request = {
            "operation": "yaml_configuration",
            "target_path": str(target),
            "input_path": str(target),
            "args": [*args, *additions[case]],
        }
    code, response = invoke(package, request)
    assert code == 3
    assert decision(response)["status"] == "unavailable"
    assert decision(response)["reason"] == "unsupported_input"
    assert target.read_text(encoding="utf-8") == "key: value\n"


@pytest.mark.parametrize("failure", ["missing", "schema", "reference"])
def test_native_schema_loading_errors_are_unavailable(
    checker_package: CheckerPackage, failure: str
) -> None:
    package = checker_package
    target = package.workspace / "source.yaml"
    target.write_text("key: value\n", encoding="utf-8")
    schema = package.workspace / "broken.schema.json"
    if failure != "missing":
        schema.write_text(
            '{"type":7}' if failure == "schema" else '{"$ref":"missing.schema.json"}',
            encoding="utf-8",
        )
    code, response = invoke(
        package,
        selection(
            (target,),
            [
                "--schemafile",
                str(schema),
                "--force-filetype",
                "yaml",
                "--output-format",
                "JSON",
            ],
            "yaml_configuration",
        ),
    )
    assert code == 3
    assert decision(response)["status"] == "unavailable"
    assert decision(response)["reason"] in {"invalid_configuration", "execution_error"}
    assert response["evidence"]


@pytest.mark.parametrize("failure", ["missing", "mismatch"])
def test_dependency_admission_uses_package_requirements(
    checker_package: CheckerPackage, failure: str
) -> None:
    package = checker_package
    python_args: tuple[str, ...] = ()
    if failure == "missing":
        python_args = ("-S",)
    else:
        requirements = package.root / "requirements.txt"
        declarations = requirements.read_text(encoding="utf-8").splitlines()
        declarations[0] = declarations[0].split("==")[0] + "==0.0.0"
        requirements.write_text("\n".join(declarations) + "\n", encoding="utf-8")
    code, response = invoke(package, selection((), native_args("shape")), python_args=python_args)
    assert code == 3
    assert decision(response)["reason"] == "dependency_unavailable"


@pytest.mark.parametrize("case", ["unknown", "operation", "relative", "malformed"])
def test_malformed_wire_is_separate_from_native_usage(
    checker_package: CheckerPackage, case: str
) -> None:
    package = checker_package
    request = selection((), native_args("shape"))
    raw = None
    if case == "unknown":
        request["unknown"] = True
    elif case == "operation":
        request["operation"] = "unsupported"
    elif case == "relative":
        request["targets"] = ["relative.schema.json"]
    else:
        raw = b"{"
    code, response = invoke(package, request, raw=raw)
    assert code == 2 and response["reason"] == "invalid_request"
    assert response["details"]
