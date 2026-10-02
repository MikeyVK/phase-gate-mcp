"""Real-process Markdown preflight adapter conformance without server dependencies."""

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
class MarkdownPackage:
    binding: AdapterBinding[CheckCapability]
    root: Path
    schema: Draft202012Validator


def resolve_program(name: str) -> Path | None:
    resolved = which(name)
    return Path(resolved) if resolved is not None else None


@pytest.fixture
def markdown_package(tmp_path: Path, pytestconfig: pytest.Config) -> MarkdownPackage:
    source = pytestconfig.rootpath / "mcp_server/bundled_adapters/markdown_preflight"
    root = tmp_path / "official packages" / "markdown_preflight"
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
    for operation in ("document", "body"):
        binding = catalog.get_check("markdown_preflight", operation)
        assert binding.capability.inputs == ("content",)
        assert binding.capability.requires_file is False
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return MarkdownPackage(
        catalog.get_check("markdown_preflight", "document"),
        root,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def invoke(
    package: MarkdownPackage,
    workspace: Path,
    payload: dict[str, object] | bytes,
    *,
    isolated: bool = True,
) -> tuple[int, dict[str, JsonValue]]:
    executable = package.binding.launch.executable
    assert executable is not None, "The manifest-declared Python interpreter must be provisioned"
    flags = ["-I", "-S"] if isolated else []
    request = (
        payload
        if isinstance(payload, bytes)
        else json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.root.parent.parent)},
                **payload,
            }
        ).encode("utf-8")
    )
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
    return {"operation": "document", "target_path": str(target), "content": content, "args": []}


def issues(response: dict[str, JsonValue]) -> list[dict[str, JsonValue]]:
    evidence = response.get("evidence")
    if evidence is None:
        return []
    assert isinstance(evidence, dict) and evidence["format"] == "json"
    data = evidence["data"]
    assert isinstance(data, dict)
    observations = data["issues"]
    assert isinstance(observations, list)
    result: list[dict[str, JsonValue]] = []
    for observation in observations:
        assert isinstance(observation, dict)
        result.append(observation)
    return result


def test_body_without_h1_keeps_missing_link_as_warning(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
) -> None:
    target = tmp_path / "proposed.md"
    payload = {**request(target, "## Body\n[missing](missing.md)\n"), "operation": "body"}
    code, response = invoke(markdown_package, tmp_path, payload)
    assert code == 0
    assert response["decision"] == {"status": "passed"}
    observations = issues(response)
    assert len(observations) == 1
    assert observations[0]["severity"] == "warning"
    assert observations[0]["line"] == 2
    assert "missing.md" in str(observations[0]["message"])
    assert not target.exists()


@pytest.mark.parametrize(
    ("content", "expected_status", "expected_exit"),
    [
        ("Preface first\n\n# Title anywhere\n[unfinished Markdown\n", "passed", 0),
        ("## Body without document title\n", "failed", 1),
    ],
)
def test_document_requires_only_the_retained_h1_observation(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
    content: str,
    expected_status: str,
    expected_exit: int,
) -> None:
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "document.md", content))
    assert code == expected_exit
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == expected_status
    observations = issues(response)
    assert len(observations) == (1 if expected_status == "failed" else 0)
    if observations:
        assert observations[0]["severity"] == "error"
        assert "H1" in str(observations[0]["message"])


def test_link_observations_use_intended_parent_and_leave_source_bytes_unchanged(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
) -> None:
    docs = tmp_path / "intended docs"
    docs.mkdir()
    target = docs / "report.md"
    neighbor = docs / "neighbor.md"
    picture = docs / "image.png"
    originals = {
        target: b"## Original on disk lacks H1\r\n",
        neighbor: b"No matching anchor here\r\n",
        picture: b"unchanged image bytes",
    }
    for path, data in originals.items():
        path.write_bytes(data)
    (tmp_path / "only-in-cwd.md").write_text("wrong parent", encoding="utf-8")
    content = (
        "# Supplied title\n"
        "[neighbor](neighbor.md#missing-anchor)\n"
        "![image](image.png)\n"
        "![missing](missing.png#fragment)\n"
        "[wrong parent](only-in-cwd.md)\n"
        "[http](http://nonexistent.invalid)\n"
        "[https](https://nonexistent.invalid)\n"
        "[mail](mailto:nobody@example.invalid)\n"
        "[resource](pgmcp://cache/example)\n"
        "[anchor](#missing-anchor)\n"
        "[reference][not-declared]\n"
    )
    code, response = invoke(markdown_package, tmp_path, request(target, content), isolated=False)
    assert code == 0
    assert response["decision"] == {"status": "passed"}
    observations = issues(response)
    assert [item["severity"] for item in observations] == ["warning", "warning"]
    assert [item["line"] for item in observations] == [4, 5]
    assert "missing.png#fragment" in str(observations[0]["message"])
    assert str(docs / "missing.png") in str(observations[0]["message"])
    assert str(docs / "only-in-cwd.md") in str(observations[1]["message"])
    assert {path: path.read_bytes() for path in originals} == originals


def test_missing_h1_and_missing_link_preserve_distinct_error_and_warning(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
) -> None:
    code, response = invoke(
        markdown_package, tmp_path, request(tmp_path / "report.md", "[missing](absent.md)\n")
    )
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert [item["severity"] for item in issues(response)] == ["error", "warning"]


@pytest.mark.parametrize(
    ("changes", "field", "reason"),
    [
        ({"operation": "unknown"}, "operation", "invalid_value"),
        ({"operation": []}, "operation", "wrong_type"),
        ({"target_path": 42}, "target_path", "wrong_type"),
    ],
)
def test_invalid_request_preserves_exact_validation_details(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
    changes: dict[str, object],
    field: str,
    reason: str,
) -> None:
    payload = {**request(tmp_path / "proposed.md", "content"), **changes}
    code, response = invoke(markdown_package, tmp_path, payload)
    assert code == 2
    assert response == {
        "reason": "invalid_request",
        "details": [{"location": [field], "code": reason}],
    }


def test_valid_but_unsupported_options_report_inability(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
) -> None:
    payload = {**request(tmp_path / "proposed.md", "invalid content"), "args": ["--strict"]}
    code, response = invoke(markdown_package, tmp_path, payload)
    assert code == 3
    decision = response["decision"]
    assert isinstance(decision, dict)
    assert decision["status"] == "unavailable"
    assert decision["reason"] == "unsupported_input"
    assert response["external_tools"]


def test_malformed_transport_and_nonobject_root_have_distinct_root_details(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
) -> None:
    for payload, reason in (
        (b'{"operation":', "invalid_value"),
        (bytes([255]), "invalid_value"),
        (b"[]", "wrong_type"),
    ):
        code, response = invoke(markdown_package, tmp_path, payload)
        assert code == 2
        assert response == {
            "reason": "invalid_request",
            "details": [{"location": [], "code": reason}],
        }


def test_stdlib_only_body_operation_works_for_empty_content(
    tmp_path: Path,
    markdown_package: MarkdownPackage,
) -> None:
    payload = {**request(tmp_path / "empty.md", ""), "operation": "body"}
    code, response = invoke(markdown_package, tmp_path, payload)
    assert code == 0
    assert response["decision"] == {"status": "passed"}
    assert issues(response) == []
    requirements = (markdown_package.root / "requirements.txt").read_text(encoding="utf-8")
    assert not [
        line
        for line in requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
