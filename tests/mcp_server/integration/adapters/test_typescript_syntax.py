"""Native TypeScript single-snapshot syntax and check/v1 conformance."""

from __future__ import annotations

import json
import os
import re
import subprocess
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


@dataclass(frozen=True)
class TypeScriptRuntime:
    node: Path
    package: Path


@dataclass(frozen=True)
class TypeScriptPackage:
    runtime: TypeScriptRuntime
    root: Path
    workspace: Path
    launch: AdapterLaunch
    schema: Draft202012Validator


def _runtime(repo_root: Path) -> TypeScriptRuntime:
    resolved_node = which("node")
    assert resolved_node is not None, "Node is required for the native baseline"
    repo_package = repo_root / "node_modules" / "typescript"
    package = repo_package
    if not (package / "package.json").is_file():
        code = which("code")
        assert code is not None, "VS Code command is required to provision the native baseline"
        code_path = Path(code)
        launcher = code_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"\.\.\\([0-9a-f]+)\\resources", launcher, re.IGNORECASE)
        assert match is not None, "VS Code launcher must identify its installed build"
        package = (
            code_path.parent.parent
            / match.group(1)
            / "resources"
            / "app"
            / "extensions"
            / "node_modules"
            / "typescript"
        )
    metadata = json.loads((package / "package.json").read_text(encoding="utf-8"))
    assert metadata["name"] == "typescript"
    assert metadata["version"] == "6.0.3"
    assert (package / "lib" / "typescript.js").is_file()
    return TypeScriptRuntime(Path(resolved_node), package)


def _native(
    runtime: TypeScriptRuntime, workspace: Path, target: Path, source: str
) -> dict[str, object]:
    script = r"""
const ts = require('typescript');
const [target, source] = JSON.parse(process.argv[1]);
const normalizedTarget = ts.sys.resolvePath(target);
const host = {
  getScriptFileNames: () => [normalizedTarget],
  getScriptVersion: () => '0',
  getScriptSnapshot: (file) => {
    if (ts.sys.resolvePath(file) !== normalizedTarget) return undefined;
    return ts.ScriptSnapshot.fromString(source);
  },
  getCurrentDirectory: () => process.cwd(),
  getCompilationSettings: () => ({}),
  getDefaultLibFileName: (options) => ts.getDefaultLibFilePath(options),
  useCaseSensitiveFileNames: () => ts.sys.useCaseSensitiveFileNames,
  fileExists: (file) => ts.sys.resolvePath(file) === normalizedTarget,
  readFile: (file) => ts.sys.resolvePath(file) === normalizedTarget ? source : undefined,
  readDirectory: () => [],
};
const service = ts.createLanguageService(host);
const diagnostics = service.getSyntacticDiagnostics(normalizedTarget);
const formatted = ts.formatDiagnostics(diagnostics, {
  getCanonicalFileName: (fileName) => fileName,
  getCurrentDirectory: () => process.cwd(),
  getNewLine: () => ts.sys.newLine,
});
const facts = diagnostics.map((diagnostic) => ({
  code: diagnostic.code,
  start: diagnostic.start ?? null,
  length: diagnostic.length ?? null,
  message: ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'),
  file: diagnostic.file?.fileName ?? null,
}));
service.dispose();
process.stdout.write(JSON.stringify({
  diagnostics: facts,
  text: formatted,
}));
"""
    result = subprocess.run(
        [str(runtime.node), "-e", script, json.dumps([str(target), source])],
        cwd=workspace,
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert isinstance(payload, dict)
    assert isinstance(payload["diagnostics"], list)
    assert isinstance(payload["text"], str)
    return payload


@pytest.fixture
def typescript_package(tmp_path: Path, pytestconfig: pytest.Config) -> TypeScriptPackage:
    runtime = _runtime(pytestconfig.rootpath)
    workspace = tmp_path / "workspace"
    package = workspace / "node_modules" / "typescript"
    package.parent.mkdir(parents=True)
    copytree(runtime.package, package)
    source = pytestconfig.rootpath / "mcp_server/bundled_adapters/typescript_syntax"
    root = tmp_path / "official packages" / "typescript_syntax"
    copytree(source, root)
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: runtime.node if name == "node" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_check("typescript_syntax", "syntax")
    assert binding.capability.inputs == ("content",)
    assert binding.capability.requires_file is False
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return TypeScriptPackage(
        runtime,
        root,
        workspace,
        binding.launch,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def invoke(
    package: TypeScriptPackage, workspace: Path, payload: dict[str, object]
) -> tuple[int, dict[str, JsonValue]]:
    result = subprocess.run(
        [str(package.launch.executable), *package.launch.args],
        cwd=workspace,
        input=json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.workspace.parent)},
                **payload,
            }
        ).encode("utf-8"),
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
    response = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(response, dict)
    package.schema.validate(response)
    return result.returncode, response


def _content_request(target: Path, content: str, args: tuple[str, ...] = ()) -> dict[str, object]:
    return {
        "operation": "syntax",
        "target_path": str(target),
        "content": content,
        "args": list(args),
    }


def _decision(response: dict[str, JsonValue]) -> dict[str, JsonValue]:
    value = response["decision"]
    assert isinstance(value, dict)
    return value


@pytest.mark.parametrize(
    ("filename", "content", "existing", "status"),
    [
        (
            "source.ts",
            "import { missing } from 'missing-package';\nconst value: number = 'semantic error';\n",
            True,
            "passed",
        ),
        ("component.tsx", 'const view = <MissingWidget title="hello" />;\n', False, "passed"),
        (
            "negative.ts",
            "import { missing } from 'missing-package';\nconst value: number = ;\n",
            False,
            "failed",
        ),
    ],
    ids=["semantic-errors-ignored", "tsx", "syntax-error"],
)
def test_native_snapshot_results_and_no_writes(
    typescript_package: TypeScriptPackage,
    filename: str,
    content: str,
    existing: bool,
    status: str,
) -> None:
    package = typescript_package
    target = package.workspace / filename
    stale = b"const stale = ;\n"
    if existing:
        target.write_bytes(stale)
    before = {path.relative_to(package.workspace) for path in package.workspace.rglob("*")}
    direct = _native(package.runtime, package.workspace, target, content)
    code, response = invoke(package, package.workspace, _content_request(target, content))
    assert code == (0 if status == "passed" else 1)
    assert _decision(response)["status"] == status
    assert response["external_tools"] == [{"tool_id": "typescript", "version": "6.0.3"}]
    diagnostics = direct["diagnostics"]
    assert isinstance(diagnostics, list)
    if status == "passed":
        assert diagnostics == []
    else:
        assert diagnostics
        first = diagnostics[0]
        assert isinstance(first, dict)
        assert isinstance(first["code"], int) and isinstance(first["start"], int)
        assert isinstance(first["length"], int)
        assert Path(str(first["file"])) == target
        assert _decision(response)["message"] == first["message"]
        assert response["evidence"] == {"format": "text", "data": direct["text"]}
    assert before == {path.relative_to(package.workspace) for path in package.workspace.rglob("*")}
    if existing:
        assert target.read_bytes() == stale
    else:
        assert not target.exists()
    dependency = json.loads((package.root / "package.json").read_text())
    assert dependency["dependencies"] == {"typescript": "6.0.3"}


@pytest.mark.parametrize(
    ("configuration", "status"),
    [
        ("{}", "passed"),
        ('{"files": []}', "passed"),
        ("{", "unavailable"),
        ('{"compilerOptions":{"target":"invalid-target"}}', "unavailable"),
        ('{"extends":"./missing-base.json"}', "unavailable"),
    ],
    ids=["no-project-inputs", "empty-files", "invalid-json", "invalid-option", "missing-extends"],
)
def test_native_configuration_and_snapshot_selection(
    typescript_package: TypeScriptPackage,
    configuration: str,
    status: str,
) -> None:
    package = typescript_package
    config = package.workspace / "tsconfig.json"
    config.write_text(configuration, encoding="utf-8")
    target = package.workspace / "not-created" / "source.ts"
    code, response = invoke(
        package, package.workspace, _content_request(target, "const value = 1;\n")
    )
    assert code == (0 if status == "passed" else 3)
    assert _decision(response)["status"] == status
    if status == "unavailable":
        assert _decision(response)["reason"] == "invalid_configuration"
        assert _decision(response)["message"]
        assert response["evidence"]
    assert config.read_text(encoding="utf-8") == configuration
    assert not target.exists()


def test_native_extends_is_read_and_validated(typescript_package: TypeScriptPackage) -> None:
    package = typescript_package
    base = package.workspace / "base.json"
    config = package.workspace / "tsconfig.json"
    config.write_text('{"extends":"./base.json","files":[]}', encoding="utf-8")
    target = package.workspace / "absent.ts"
    request = _content_request(target, "const value: number = 'semantic';\n")
    base.write_text('{"compilerOptions":{"target":"invalid-target"}}', encoding="utf-8")
    code, rejected = invoke(package, package.workspace, request)
    assert code == 3 and _decision(rejected)["reason"] == "invalid_configuration"
    base.write_text('{"compilerOptions":{"strict":true}}', encoding="utf-8")
    code, accepted = invoke(package, package.workspace, request)
    assert code == 0 and _decision(accepted)["status"] == "passed"
    assert not target.exists()


def test_dependency_absence_is_distinct_from_missing_node(
    typescript_package: TypeScriptPackage,
    tmp_path: Path,
) -> None:
    package = typescript_package
    empty = tmp_path / "empty lookup and workspace"
    empty.mkdir()
    assert which("node", path=str(empty)) is None
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")

    def resolve_missing(name: str) -> Path | None:
        result = which(name, path=str(empty))
        return Path(result) if result is not None else None

    catalog = AdapterCatalogLoader(
        package.root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=resolve_missing,
        windows=os.name == "nt",
    ).load()
    assert catalog.get_check("typescript_syntax", "syntax").launch.executable is None
    # An adapter-adjacent dependency must not satisfy workspace provisioning.
    copytree(package.runtime.package, package.root / "node_modules" / "typescript")
    target = empty / "absent.ts"
    code, response = invoke(package, empty, _content_request(target, "const value = 1;\n"))
    assert code == 3 and _decision(response)["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "typescript", "version": None}]
    assert not target.exists()


def test_unsupported_arguments(typescript_package: TypeScriptPackage) -> None:
    package = typescript_package
    target = package.workspace / "absent.ts"
    code, response = invoke(
        package,
        package.workspace,
        _content_request(target, "const value = 1;\n", ("--strict",)),
    )
    assert code == 3 and _decision(response)["reason"] == "unsupported_input"
    assert not target.exists()


def test_protocol_rejects_invalid_target(typescript_package: TypeScriptPackage) -> None:
    package = typescript_package
    code, response = invoke(
        package,
        package.workspace,
        _content_request(Path("relative.ts"), "const value = 1;\n"),
    )
    assert code == 2
    assert response == {
        "reason": "invalid_request",
        "details": [
            {"location": ["target_path"], "code": "invalid_value"},
        ],
    }
