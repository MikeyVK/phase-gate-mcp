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
    "document_metadata": {
      "status": "DRAFT",
      "revisions": [{
        "version": "1.0",
        "date": "2026-09-24",
        "author": "Design author",
        "change": "Initial design."
      }]
    },
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

## Context migration and output responsibilities

Full-document packages require authored document_metadata with explicit status and a nonempty revision list, including minimal contexts. The visible header and final Version History table use those supplied facts; the technical first-line provenance remains a separate generation-source record. Issue, PR and Commit bodies retain their own publication contracts. See the [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md#scaffolded-document-metadata-and-whitespace).

Templates own generated separators and one terminal LF. Selected prose/code fragments lose only blank edge lines; meaningful interiors, literal values and admitted explicit empty content remain caller-owned. Module and class descriptions describe different scopes; use the discovered package fields instead of copying a removed alias or using one description as a fallback. The [Code Style Guide](../../coding_standards/CODE_STYLE.md#scaffold-output-responsibilities) defines the corresponding output responsibilities.

When a package input contract changes, rediscover its schema and migrate affected callers explicitly. The issue473 changed-context transition intentionally provides no legacy aliases. Native preflight acceptance is evidence for its configured checks; it does not certify arbitrary dependencies, semantic completeness or caller-authored code quality. Read the actual generated file before treating it as a finished deliverable.

## Python structured identifier contract

The delivered Python and Pytest packages admit ASCII-only structured Python identifiers: declaration, method, function, fixture, parameter and model-field names; imported symbols and aliases; module segments; and dotted fixture decorator or model-field `default_factory` names. These fields require a complete valid identifier spelling and retain their keyword, reserved-name and package-specific discovery restrictions. Relative-import prefixes and the separate star-import form keep their existing grammar. Inspect the selected resolved schema for the exact field contract.

Unicode remains supported in prose and docstrings, literal/default/example values, logging text, markers and caller-authored raw bodies or type expressions. Paths and document link targets retain their existing contracts; this identifier restriction does not introduce another language's naming policy. Raw code and type expressions still need native syntax checks, and syntax acceptance does not establish dependency availability or runtime correctness.

This input transition is an ASCII-only clean break. Rediscover affected schemas and explicitly choose ASCII names for caller contexts that supplied non-ASCII structured identifiers. The server provides no compatibility profile, Unicode fallback, normalization, transliteration or automatic rewrite. Refresh the server's immutable catalog through the supported restart operation after changing the installed suite; distinguish a stale connection's generation from the current suite sources.

## Related references

- [Tools reference index](README.md)
- [Configuration and template loading](../config-loading-architecture.md)
- [Checks, tests, and fixes](quality.md)
- [Presentation architecture](../presentation_architecture.md)
