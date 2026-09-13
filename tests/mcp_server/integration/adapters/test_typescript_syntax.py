"""CY023 native TypeScript syntax and adapter RED evidence."""

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
  getCompilationSettings: () => ({ allowJs: true }),
  getDefaultLibFileName: (options) => ts.getDefaultLibFilePath(options),
  useCaseSensitiveFileNames: () => ts.sys.useCaseSensitiveFileNames,
  fileExists: (file) => ts.sys.resolvePath(file) === normalizedTarget,
  readFile: (file) => ts.sys.resolvePath(file) === normalizedTarget ? source : undefined,
  readDirectory: () => [],
};
const service = ts.createLanguageService(host);
const diagnostics = service.getSyntacticDiagnostics(normalizedTarget);
const facts = diagnostics.map((diagnostic) => ({
  code: diagnostic.code,
  start: diagnostic.start ?? null,
  length: diagnostic.length ?? null,
  message: ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'),
  file: diagnostic.file?.fileName ?? null,
}));
const formatHost = {
  getCanonicalFileName: (fileName) => fileName,
  getCurrentDirectory: () => process.cwd(),
  getNewLine: () => '\n',
};
process.stdout.write(JSON.stringify({
  diagnostics: facts,
  text: ts.formatDiagnostics(diagnostics, formatHost),
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
        binding.launch,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def test_native_language_service_checks_syntax_only_and_allows_absent_target(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    runtime = _runtime(pytestconfig.rootpath)
    workspace = tmp_path / "native workspace"
    workspace.mkdir()
    node_modules = workspace / "node_modules" / "typescript"
    node_modules.parent.mkdir()
    copytree(runtime.package, node_modules)
    before = {
        path.relative_to(workspace)
        for path in workspace.rglob("*")
        if path.is_file() and "node_modules" not in path.parts
    }
    target = workspace / "missing" / "source.ts"
    valid = "import missing_package from 'missing_package';\nconst value: number = 1;\n"
    invalid = "const value: number = ;\n"
    valid_result = _native(runtime, workspace, target, valid)
    assert valid_result["diagnostics"] == []
    invalid_result = _native(runtime, workspace, target, invalid)
    diagnostics = invalid_result["diagnostics"]
    assert isinstance(diagnostics, list) and diagnostics
    assert isinstance(invalid_result["text"], str) and invalid_result["text"]
    after = {
        path.relative_to(workspace)
        for path in workspace.rglob("*")
        if path.is_file() and "node_modules" not in path.parts
    }
    assert before == after
    assert not target.exists()


def test_adapter_preserves_native_syntax_result(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    runtime = _runtime(pytestconfig.rootpath)
    workspace = tmp_path / "workspace"
    native_package = workspace / "node_modules" / "typescript"
    native_package.parent.mkdir(parents=True)
    copytree(runtime.package, native_package)
    target = workspace / "absent.ts"
    request = {"operation": "syntax", "target_path": str(target),
               "content": "const value: number = 1;\n", "args": []}
    entrypoint = pytestconfig.rootpath / "mcp_server/bundled_adapters/typescript_syntax/check.cjs"
    result = subprocess.run(
        [str(runtime.node), str(entrypoint)], input=json.dumps(request).encode(),
        cwd=workspace, capture_output=True, timeout=15,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["decision"]["status"] == "passed"
    assert not target.exists()


def invoke(
    package: TypeScriptPackage, workspace: Path, payload: dict[str, object]
) -> tuple[int, dict[str, JsonValue]]:
    result = subprocess.run(
        [str(package.launch.executable), *package.launch.args],
        cwd=workspace,
        input=json.dumps(payload).encode("utf-8"),
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
    response = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(response, dict)
    package.schema.validate(response)
    return result.returncode, response

