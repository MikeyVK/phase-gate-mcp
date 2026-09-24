<!-- template=reference -->
# Scaffolding and Schema Discovery

The public scaffolding surface consists of `scaffold_schema` and `scaffold_artifact`. Their schemas are defined by [`template_schema_tool.py`](../../../mcp_server/tools/template_schema_tool.py) and [`scaffold_tool.py`](../../../mcp_server/tools/scaffold_tool.py); exact package data comes from the resolved catalog. Do not use a static tool or template-type inventory as authority.

## Discover a package context schema

Call `scaffold_schema` with `artifact_type`, the admitted package identity. The tool returns the package's resolved context schema and provenance (package version and fingerprint); the nested schema is also attached as a schema resource. This is the authoritative source for required and optional context fields.

```json
{"artifact_type": "design"}
```

Inspect that schema and construct a context that satisfies it. Schema validity proves input shape, not that the artifact is complete or correct.

## Generate an artifact

`scaffold_artifact` accepts:

| Field | Meaning |
|---|---|
| `artifact_type` | Admitted template-package identity. |
| `file_name` | Required output basename, including extension. |
| `context` | Caller-provided JSON object validated against that package's context schema. |
| `target_path` | Optional workspace-relative target directory, normally selected from configured artifact locations. |
| `force_target` | Defaults to false; true requires `target_path` and opts out of configured locations while remaining within the workspace. |
| `validation` | `enforce` by default or `report`; selects whether failed required checks block persistence. |

Example:

```json
{
  "artifact_type": "design",
  "file_name": "oauth-design.md",
  "context": {
    "title": "OAuth integration",
    "status": "DRAFT",
    "version": "1.0",
    "last_updated": "2026-09-24",
    "problem_statement": "Describe the problem.",
    "requirements_functional": ["Support the agreed authentication flow."],
    "requirements_nonfunctional": ["Keep credentials outside source control."],
    "decision": "Use the selected provider.",
    "rationale": "Document the decision basis.",
    "options": [],
    "key_decisions": []
  }
}
```

This example follows the current design package's required context fields; optional fields may be added only when the resolved schema admits them. Other artifact types have different schemas. Discover them instead of copying this example as a universal shape.

## Validation, persistence, and provenance

The result reports the selected template identity, package version/fingerprint, output path when written, check observations, validation status, and persistence/failure facts. `enforce` prevents persistence when required checks fail; `report` retains check outcomes while permitting persistence according to the operation contract. Native check availability and execution are reported as observed facts, not converted into an assumed pass.

Every newly scaffolded artifact carries the compact `pgmcp:v1` provenance record on its first physical line. The record is not an alternate schema or package registry. Package manifests, context schema and policy own their respective facts; artifact-location config selects default destinations. Use [editing.md](editing.md) for changes to an existing file.

## Related references

- [Tools reference index](README.md)
- [Configuration and template loading](../config-loading-architecture.md)
- [Checks, tests, and fixes](quality.md)
- [Presentation architecture](../presentation_architecture.md)
