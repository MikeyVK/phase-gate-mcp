<!-- template=reference -->
# File Editing

[`safe_edit_file`](../../../mcp_server/tools/edit_tool.py) applies one operation to an existing workspace-relative path. Its strict public input model rejects extra fields. New artifacts belong to [`scaffold_artifact`](scaffolding.md).

## Public input

The envelope is:

| Field | Contract |
|---|---|
| `path` | Non-empty workspace-relative path; absolute paths and paths with a drive prefix are rejected. |
| `operation` | One discriminated operation described below. |
| `template_id` | Optional admitted template identity used when selecting validation obligations. |
| `validation` | `enforce` (default) or `report`. |

The exact admitted template IDs and JSON schema are prepared from the resolved catalog. The live schema in `SafeEditInput` and the public tool contract are authoritative.

## Operations

- `replace`: `target_content`, `replacement`, and optional two-integer `search_window` (1-based inclusive line bounds).
- `append`: `content`, optional exact `anchor`, and `position` (`before` or `after`, default `after`). Without an anchor, content is appended.
- `rewrite`: replace the existing file's complete content with `content`.
- `pattern_replace`: replace matches for `pattern` with `replacement`; `regex` defaults to true and may be false for literal replacement.

Example:

```json
{
  "path": "docs/example.md",
  "operation": {
    "op": "replace",
    "target_content": "old wording",
    "replacement": "updated wording"
  },
  "validation": "report"
}
```

## Validation and result

The operation selects check obligations using an explicit `template_id` when supplied, otherwise available artifact-header metadata or the file extension. `enforce` prevents a write when required checks fail; `report` returns the check facts without enforcing that rejection policy. These are validation policies, not legacy strict/interactive/verify-only modes or a general quality-gate invocation.

The result records the attempted operation, write/content-change facts, selected validation profile and check results, plus structured failure details where applicable. Read the cached complete result when you need full diagnostics or the generated diff; use the bounded presented response for routine outcomes. Check configuration defines applicable adapter checks and native execution evidence.

For the delivered Markdown policies and the `.md` extension route, the existing Lychee adapter checks local links and heading fragments against the proposed edit before writing, using the edited file's intended path as the resolution base. Self-links resolve against the proposed content. See [Markdown validation](scaffolding.md#markdown-validation) for native availability, offline scope and the template package's structural responsibility. A successful link check does not establish that a full rewrite preserves the template's H1 or document structure.

## Related references

- [Scaffolding and schema discovery](scaffolding.md)
- [Checks, tests, and fixes](quality.md)
- [Presentation architecture](../presentation_architecture.md)
- [Architecture principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
