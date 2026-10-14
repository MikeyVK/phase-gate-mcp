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

## Text and line endings

Every completed proposal uses LF (`\n`) line endings for the entire file, including `rewrite` and operations with no matches. CRLF and lone CR in the source or inserted text are normalized to LF before validation and writing. A successful edit can therefore normalize untouched lines as well.

Literal matching operands (`target_content`, `anchor`, and `pattern` when `regex=false`) are normalized to LF too. Regex patterns and replacement syntax keep Python's native meaning: matching runs against the LF source, and expanded output is normalized to LF. Use `\n` when matching line endings; a regex escape for CRLF does not match that normalized source.

Normalization does not change Unicode characters, BOM, other whitespace or final-newline policy. Append retains its existing separator behavior. This is the safe-edit write policy; Git and editor settings can independently affect line endings outside a tool call.

## Validation and result

The operation selects check obligations using an explicit `template_id` when supplied, otherwise available artifact-header metadata or the file extension. `enforce` prevents a write when required checks fail; `report` returns the check facts without enforcing that rejection policy. These are validation policies, not legacy strict/interactive/verify-only modes or a general quality-gate invocation.

With a valid startup configuration, `report` also permits guarded edits when unresolved
`configuration_choice` prevents the selected content-check batch from starting. This
supports initial edits to workspace configuration. A completed write reports
`success=true`, `written=true` and `validation_status=not_executed`; check rows retain
`configuration_choice_required` or `not_started`, with no native invocation or scratch
allocation. Presentation explicitly reports absent validation. This does not acknowledge
any binding or certify content. Original-file and persistence failures retain their
own error and the unexecuted check facts. `enforce`, scaffold and standalone quality
operations still refuse unresolved setup. Invalid requests, interruption and unconfirmed
termination remain blockers under either edit policy.

The result records the attempted operation, write/content-change facts, selected validation profile and check results, plus structured failure details where applicable.

| Field | Meaning |
|---|---|
| `written=true` | The guarded file replacement completed, including a byte-identical proposal. |
| `content_changed=true` | The final UTF-8 proposal bytes differ from the original bytes read at the start of this call, and replacement completed. |
| `content_changed=false` | Replacement completed with the same bytes as the original. |
| `content_changed=null` | No replacement completed; this does not establish that the proposed text was identical. |

A no-match operation can still report `content_changed=true` when CRLF/CR source bytes become LF. Byte-identical proposals still run validation and the write path. Checks receive the exact final text sent to the writer; the writer retains its guard against a concurrent change to the original bytes.

Read the cached complete result when you need full diagnostics or the generated diff; use the bounded presented response for routine outcomes. Check configuration defines applicable adapter checks and native execution evidence.

For the delivered Markdown policies and the `.md` extension route, the existing Lychee adapter checks local links and heading fragments against the proposed edit before writing, using the edited file's intended path as the resolution base. Self-links resolve against the proposed content. See [Markdown validation](scaffolding.md#markdown-validation) for native availability, offline scope and the template package's structural responsibility. A successful link check does not establish that a full rewrite preserves the template's H1 or document structure.

## Related references

- [Scaffolding and schema discovery](scaffolding.md)
- [Checks, tests, and fixes](quality.md)
- [Presentation architecture](../presentation_architecture.md)
- [Architecture principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
