"""Exercise the real TypeScript DTO package with native syntax and strict compilation."""

from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue, TypeAdapter

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.adapters.test_typescript_syntax import (
    TypeScriptPackage,
    invoke,
    typescript_package,
)

__all__ = ["typescript_package"]


@pytest.fixture
def delivered_dto(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source,
        source_package=source / "typescript_dto",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="typescript_dto",
    )
    selected = delivered.catalog.get("typescript_dto")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "typescript_syntax",
    )
    return delivered


def native_artifact(
    package: TypeScriptPackage,
    source: str,
    *,
    support: str = "",
    consumer: str = "",
    exercise: str = "",
) -> dict[str, JsonValue]:
    """Compile actual source with strict optional rules, then inspect native AST and behavior."""
    target = package.workspace / "caller location.ts"
    target.write_text(source, encoding="utf-8")
    (package.workspace / "support.ts").write_text(support, encoding="utf-8")
    (package.workspace / "consumer.ts").write_text(consumer, encoding="utf-8")
    script = r"""
const ts = require("typescript");
const path = require("node:path");
const [target, exercise] = JSON.parse(process.argv[1]);
const options = {
  target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS,
  strict: true, exactOptionalPropertyTypes: true, useDefineForClassFields: true,
  noEmitOnError: true, types: [],
};
const program = ts.createProgram([target, "support.ts", "consumer.ts"], options);
const diagnostics = ts.getPreEmitDiagnostics(program).map(d => ({
  code: d.code, message: ts.flattenDiagnosticMessageText(d.messageText, "\n"),
}));
const root = program.getSourceFile(target);
const classes = root.statements.filter(ts.isClassDeclaration);
const facts = classes.map(cls => ({
  name: cls.name.text,
  exported: !!cls.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword),
  implements: (cls.heritageClauses ?? []).flatMap(h => h.types.map(t => t.getText(root))),
  fields: cls.members.filter(ts.isPropertyDeclaration).map(p => ({
    name: p.name.getText(root), type: p.type.getText(root), optional: !!p.questionToken,
    readonly: !!p.modifiers?.some(m => m.kind === ts.SyntaxKind.ReadonlyKeyword),
  })),
  constructors: cls.members.filter(ts.isConstructorDeclaration).map(c => c.parameters.map(p => ({
    name: p.name.getText(root), type: p.type.getText(root),
  }))),
}));
const imports = root.statements.filter(ts.isImportDeclaration).map(i => i.getText(root));
if (diagnostics.length === 0) {
  const result = program.emit();
  if (result.emitSkipped) throw new Error("Native emit unexpectedly skipped");
  const artifact = require(target.replace(/\.ts$/, ".js"));
  new Function("artifact", "assert", exercise)(artifact, require("node:assert/strict"));
}
process.stdout.write(JSON.stringify({diagnostics, classes: facts, imports, version: ts.version}));
"""
    result = subprocess.run(
        [str(package.runtime.node), "-e", script, json.dumps([str(target), exercise])],
        cwd=package.workspace,
        capture_output=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    response = TypeAdapter(JsonValue).validate_json(result.stdout)
    assert isinstance(response, dict)
    assert response["version"] == "6.0.3"
    assert response["diagnostics"] == []
    return response


def test_omitted_and_empty_fields_keep_exported_class_and_object_constructor(
    delivered_dto: DeliveredTemplate, typescript_package: TypeScriptPackage
) -> None:
    context: dict[str, JsonValue] = {"class_name": "$Empty", "description": "An explicit DTO."}
    output = delivered_dto.renderer.render("typescript_dto", context, delivered_dto.provenance)
    assert output == delivered_dto.renderer.render(
        "typescript_dto", {**context, "fields": []}, delivered_dto.provenance
    )
    facts = native_artifact(
        typescript_package,
        output,
        exercise="assert.deepEqual(Object.keys(new artifact.$Empty({})), []);",
    )
    assert facts["classes"] == [{
        "name": "$Empty", "exported": True, "implements": [], "fields": [],
        "constructors": [[{"name": "data", "type": "{}"}]],
    }]
    assert facts["imports"] == []
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "typescript_dto"


def test_explicit_fields_preserve_native_types_and_strict_optional_behavior(
    delivered_dto: DeliveredTemplate, typescript_package: TypeScriptPackage
) -> None:
    context: dict[str, JsonValue] = {
        "class_name": "RésuméDTO",
        "description": "Explicit class */ text\nNext line 😀",
        "module_description": "Separate module documentation.",
        "imports": [
            'import type { Contract } from "./support";',
            'import type { Payload } from "./support";',
        ],
        "implements": ["Contract"],
        "fields": [
            {"name": "id", "type": "number", "readonly": True, "optional": False,
             "description": "Identifier */ remains documentation"},
            {"name": "payload", "type": "Payload", "readonly": False, "optional": False},
            {"name": "mapper", "type": "(value: { count: number }) => { ok: boolean }",
             "readonly": False, "optional": False},
            {"name": "enabled", "type": "boolean", "readonly": False, "optional": False},
            {"name": "note", "type": "string | null", "readonly": True, "optional": True},
        ],
    }
    before = deepcopy(context)
    output = delivered_dto.renderer.render("typescript_dto", context, delivered_dto.provenance)
    assert context == before
    assert "Separate module documentation." in output
    assert "Explicit class *\\/ text\n" in output
    assert "Identifier *\\/ remains documentation" in output
    support = (
        "export interface Contract { readonly id: number; }\n"
        "export type Payload = { count: number; nested: { label: string } };\n"
    )
    consumer = r"""
import { RésuméDTO } from "./caller location";
const value = new RésuméDTO({
  id: 0, payload: { count: 0, nested: { label: "" } },
  mapper: (input) => ({ ok: input.count === 0 }), enabled: false,
});
value.enabled = true;
// @ts-expect-error Readonly output property must reject assignment.
value.id = 2;
// @ts-expect-error Exact optional properties exclude explicit undefined.
new RésuméDTO({ ...value, note: undefined });
// @ts-expect-error Required typed constructor properties remain required.
new RésuméDTO({});
"""
    exercise = r"""
const data = {
  id: 0, payload: { count: 0, nested: { label: "" } },
  mapper: input => ({ ok: input.count === 0 }), enabled: false,
};
const absent = new artifact.RésuméDTO(data);
assert.equal(absent.id, 0);
assert.equal(absent.enabled, false);
assert.equal(absent.payload, data.payload);
assert.deepEqual(absent.mapper({count: 0}), {ok: true});
assert.equal(Object.hasOwn(absent, "note"), false);
assert.equal("note" in absent, false);
const present = new artifact.RésuméDTO({...data, note: null});
assert.equal(Object.hasOwn(present, "note"), true);
assert.equal(present.note, null);
absent.enabled = true;
assert.equal(absent.enabled, true);
assert.equal(data.enabled, false);
"""
    facts = native_artifact(
        typescript_package, output, support=support, consumer=consumer, exercise=exercise
    )
    assert facts["imports"] == context["imports"]
    classes = facts["classes"]
    assert isinstance(classes, list) and len(classes) == 1
    cls = classes[0]
    assert isinstance(cls, dict)
    assert cls["name"] == "RésuméDTO" and cls["exported"] is True
    assert cls["implements"] == ["Contract"]
    assert cls["fields"] == [
        {"name": "id", "type": "number", "readonly": True, "optional": False},
        {"name": "payload", "type": "Payload", "readonly": False, "optional": False},
        {"name": "mapper", "type": "(value: { count: number }) => { ok: boolean }",
         "readonly": False, "optional": False},
        {"name": "enabled", "type": "boolean", "readonly": False, "optional": False},
        {"name": "note", "type": "string | null", "readonly": True, "optional": True},
    ]


def test_schema_rejects_legacy_fields_unknown_properties_and_invalid_symbols(
    delivered_dto: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"class_name": "Example", "description": "Explicit DTO"}
    field: dict[str, JsonValue] = {
        "name": "value", "type": "{ count: number }", "readonly": False, "optional": False,
    }
    invalid: list[dict[str, JsonValue]] = [
        {"class_name": "Example"}, {**base, "description": ""},
        {**base, "class_name": "class"}, {**base, "class_name": "Invalid-Name"},
        {**base, "class_name": "Example\n"}, {**base, "name": "Alias"},
        {**base, "fields": None}, {**base, "fields": ["readonly value: number"]},
        {**base, "implements": "Contract"}, {**base, "imports": [" "]},
        {**base, "fields": [{**field, "name": "value?"}]},
        {**base, "fields": [{**field, "name": "constructor"}]},
        {**base, "fields": [{**field, "name": "__proto__", "optional": True}]},
        {**base, "fields": [{**field, "type": ""}]},
        {**base, "fields": [{**field, "readonly": "false"}]},
        {**base, "fields": [{**field, "optional": None}]},
        {**base, "fields": [{**field, "default": 0}]},
        {**base, "fields": [{"name": "value", "type": "number"}]},
        {**base, "layer": "Domain"},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            delivered_dto.renderer.render("typescript_dto", context, delivered_dto.provenance)


def test_native_syntax_check_reports_invalid_caller_type_without_writing(
    delivered_dto: DeliveredTemplate, typescript_package: TypeScriptPackage
) -> None:
    context: dict[str, JsonValue] = {
        "class_name": "Broken", "description": "Caller owns annotation syntax",
        "fields": [{"name": "value", "type": "{ count: }", "readonly": False, "optional": False}],
    }
    output = delivered_dto.renderer.render("typescript_dto", context, delivered_dto.provenance)
    target = typescript_package.workspace / "not persisted.ts"
    code, response = invoke(
        typescript_package, typescript_package.workspace,
        {"operation": "syntax", "target_path": str(target), "content": output, "args": []},
    )
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not target.exists()
