"""Real-process Python syntax adapter conformance without server dependencies."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree, which

import pytest
from jsonschema import Draft202012Validator
from pydantic import JsonValue, TypeAdapter

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig, CheckCapability
from mcp_server.core.interfaces.execution import AdapterBinding
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader


@dataclass(frozen=True)
class SyntaxPackage:
    binding: AdapterBinding[CheckCapability]
    root: Path
    schema: Draft202012Validator


def resolve_program(name: str) -> Path | None:
    resolved = which(name)
    return Path(resolved) if resolved is not None else None


@pytest.fixture
def syntax_package(tmp_path: Path, pytestconfig: pytest.Config) -> SyntaxPackage:
    source = pytestconfig.rootpath / "mcp_server/bundled_adapters/python_syntax"
    root = tmp_path / "official packages" / "python_syntax"
    copytree(source, root)
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=resolve_program,
        windows=os.name == "nt",
    ).load()
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return SyntaxPackage(
        catalog.get_check("python_syntax", "syntax"),
        root,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def invoke(
    package: SyntaxPackage,
    workspace: Path,
    payload: dict[str, object] | bytes,
    *,
    isolated: bool = True,
) -> tuple[int, dict[str, JsonValue]]:
    executable = package.binding.launch.executable
    assert executable is not None, "The manifest-declared Python interpreter must be provisioned"
    flags = ["-I", "-S"] if isolated else []
    request = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    result = subprocess.run(
        [str(executable), *flags, *package.binding.launch.args],
        input=request,
        cwd=workspace,
        capture_output=True,
        timeout=10,
    )
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
    response = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(response, dict)
    package.schema.validate(response)
    return result.returncode, response


def request(target: Path, content: str) -> dict[str, object]:
    return {"operation": "syntax", "target_path": str(target), "content": content, "args": []}


def test_complete_content_is_parsed_without_import_or_execution(
    tmp_path: Path,
    syntax_package: SyntaxPackage,
) -> None:
    target = tmp_path / "absent parent" / "proposed.py"
    marker = tmp_path / "executed.txt"
    content = (
        "import nonexistent_syntax_fixture_dependency\n"
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('must not execute')\n"
        "return 1\n"
    )
    code, response = invoke(syntax_package, tmp_path, request(target, content), isolated=False)
    assert code == 0
    assert response["decision"] == {"status": "passed"}
    assert not target.exists()
    assert not marker.exists()


def test_stdlib_only_package_reports_the_actual_adapter_interpreter(
    tmp_path: Path,
    syntax_package: SyntaxPackage,
) -> None:
    executable = syntax_package.binding.launch.executable
    assert executable is not None
    runtime = (
        subprocess.run(
            [
                str(executable),
                "-I",
                "-S",
                "-c",
                "import platform; print(platform.python_version())",
            ],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            timeout=10,
        )
        .stdout.decode("utf-8")
        .strip()
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "empty.py", ""))
    assert code == 0
    assert response["external_tools"] == [{"tool_id": "python", "version": runtime}]
    assert syntax_package.binding.capability.inputs == ("content",)
    assert syntax_package.binding.capability.requires_file is False
    requirements = (syntax_package.root / "requirements.txt").read_text(encoding="utf-8")
    assert not [
        line
        for line in requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def test_syntax_error_keeps_complete_content_location_and_logical_filename(
    tmp_path: Path,
    syntax_package: SyntaxPackage,
) -> None:
    target = tmp_path / "does not exist" / "café.py"
    content = "label = 'café'\r\ndef broken(:\r\n    pass\r\n"
    code, response = invoke(syntax_package, tmp_path, request(target, content))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict)
    assert decision["status"] == "failed"
    assert isinstance(decision["message"], str) and decision["message"].strip()
    evidence = response["evidence"]
    assert isinstance(evidence, dict) and evidence["format"] == "text"
    data = evidence["data"]
    assert isinstance(data, str)
    assert str(target) in data
    assert "line 2" in data
    assert "def broken(" in data
    assert response["external_tools"]
    assert not target.exists()


@pytest.mark.parametrize(
    "changed_fields",
    [
        {"args": ["--ignore-errors"]},
        {"operation": "unknown"},
        {"content": 42},
        {"targets": []},
    ],
)
def test_invalid_or_unsupported_request_is_not_a_passing_check(
    tmp_path: Path,
    syntax_package: SyntaxPackage,
    changed_fields: dict[str, object],
) -> None:
    payload = {**request(tmp_path / "proposed.py", "x = 1\n"), **changed_fields}
    code, response = invoke(syntax_package, tmp_path, payload)
    assert code == 2
    assert response["reason"] == "invalid_request"
    assert response["details"]
    assert "decision" not in response


def test_malformed_transport_receives_closed_invalid_request_response(
    tmp_path: Path,
    syntax_package: SyntaxPackage,
) -> None:
    code, response = invoke(syntax_package, tmp_path, b'{"operation":')
    assert code == 2
    assert response["reason"] == "invalid_request"
