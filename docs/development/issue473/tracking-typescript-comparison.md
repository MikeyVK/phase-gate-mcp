<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Tracking and TypeScript Comparison

**Status:** RESEARCH DISCUSSION — final batch; remaining criteria open  
**Version:** 0.3  
**Last Updated:** 2026-10-03

## Purpose and scope

Complete the remaining concrete comparisons: TypeScript DTO, Issue, PR and Commit. The earlier [Python Class](python-class-comparison.md), [Python family](python-family-comparison.md), [Design](design-document-comparison.md) and [document family](document-family-comparison.md) evidence now covers the other fifteen shipped packages. All nineteen have a concrete v2/v3 comparison index, subject to the recorded renderer/source limits.

This batch records observed output, #460 rationale, standards boundaries and independent whitespace examples. It does not approve new editorial requirements, change production packages, expand #476 or close Research. The approved [clean break](research.md#approved-strategy-clean-break-no-legacy-compatibility--2026-10-02) remains binding. The full-document metadata/revision-table objective applies to seven document families; it does not automatically apply to these three tracking artifacts or TypeScript.

## Renderer and evidence method

The human-authorized old renderer is `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\services\template_engine.py`, SHA-256 `ea6024a1612795b07161b50a6416ad40259757229c7a3885ed891f085d0eb382`. Calls used its unmodified TemplateEngine.render and original Jinja settings: trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True. Exploratory Python -B wrote JSON to stdout only.

Issue/PR/Commit use the original root `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/`. That root has no TypeScript DTO. TypeScript uses the separately found installed root `C:/1Voudig/99_Programming/ST/.pgmcp/templates/` with the same authorized renderer. That installed source is not claimed to be an identical issue460 historical snapshot.

Each baseline uses the original survey's minimal or filled context. Eight fresh public v3 scaffolds match the original eight files byte-for-byte by SHA-256. Eight corresponding legacy outputs and an additional old colon-type probe were persisted exactly through scaffold_artifact plus safe_edit_file with report validation and explicit selected identity. Bootstrap output is not legacy evidence. No raw comparison file was repaired, autoformatted, imported or executed in the initial batch. The later authorized native follow-up rechecks these unchanged raw files and executes the existing contract-test fixtures, as distinguished below.

Minimal-nucleus legacy contexts translate the modern required input and add explicit comparison metadata; they are not claimed to satisfy an old public schema or to replay the old caller-enrichment pipeline. The comparison-only header hash is probe metadata, not a historical package identity. Old source hashes and exact contexts appear below.

| Translation | Explicit limits |
| --- | --- |
| TypeScript class_name → name; description → module_title; fields → old field strings; imports → project group; implements → joined native text | Old root has no field-description carrier. Old optional field names include ?; the old string parser/assignment exposes its own limitation. Old @layer/responsibilities defaults were not supplied as modern semantics. |
| Issue reproduction_steps → numbered steps_to_reproduce; structured related docs → target strings | Old macro has no equivalent label slot in this source. Added H1 title is an explicit old-renderer requirement, absent from the current body schema. Old reference macro emits a use without a definition in this raw render; no later pipeline repair is claimed. |
| PR checklist → description/checked records; closes → closes_issues | This old root has no deferred_work renderer; that current-only content is explicitly excluded from the old context. Added title supplies the old H1. |
| Commit subject → message; positive refs → explicit # strings | Header/body/footer/breaking fields remain comparable. Translation supplies old punctuation rather than assuming the old root formats native issue IDs. |

## Concrete baseline files

| Family | v2 minimal nucleus | v2 filled | v3 minimal | v3 filled |
| --- | --- | --- | --- | --- |
| typescript_dto | [Old minimal](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-minimal-render.ts) | [Old filled](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts) | [Current minimal](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-minimal.ts) | [Current filled](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-filled.ts) |
| issue | [Old minimal](../../../.pgmcp/temp/issue473-comparison-05/issue.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-05/issue.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-comparison-05/issue.v3-minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-comparison-05/issue.v3-filled.md) |
| pr | [Old minimal](../../../.pgmcp/temp/issue473-comparison-05/pr.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-05/pr.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-comparison-05/pr.v3-minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-comparison-05/pr.v3-filled.md) |
| commit | [Old minimal](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-minimal-render.txt) | [Old filled](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-filled-render.txt) | [Current minimal](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-minimal.txt) | [Current filled](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-filled.txt) |

## Family-specific findings and #460 rationale

| Family | Preserved or improved current capability | Recorded intentional change | Remaining presentation question |
| --- | --- | --- | --- |
| TypeScript DTO | Exported class, object-style constructor, ordered native imports/types/implements, explicit readonly/optional properties and conditional optional assignment; field descriptions now render. | Structured properties replace colon splitting; remove Unknown/layer/dependencies/responsibilities specialization and hidden name derivation. | Empty constructor has extra blank spacing; filled constructor has a blank before every assignment; module/class descriptions coincide when module_description is omitted. |
| Issue | Problem, Summary, Expected/Actual, Context, ordered numbered steps and labeled reference links. | Body-only: remove H1 title and labels/milestone/assignees from the body schema. Remove fabricated Problem placeholder. | Excessive optional/section joins and EOF spacing; visible heading wording/order differs. |
| PR | Summary, Changes, Testing, caller checklist states, breaking prose, reference links and closes IDs. | Body-only; remove invented testing/checklist defaults; require explicit none/populated deferred_work. Coordination owns triage/issue linkage. | Deferred grouping is meaningful; spacing around its headings/references/Closes is excessive. |
| Commit | Explicit conventional type/scope/subject, breaking marker/footer, multiline authored body/footer, native # refs, case preserved. | subject replaces message; positive issue IDs and framing validation replace presentation-shaped aliases. No phase-derived prefix, automatic casing or wrapping. | Generated EOF surplus; explicitly empty refs/footer remain distinguishable from omitted input. |

### TypeScript DTO

[Code/Test Design §7.8](../issue460/design-code-test-artifacts.md#78-typescript-dto) explicitly preserves the object constructor even for omitted or empty fields, ordered native type text, imports/implements and strict optional presence. The fresh fields=[] output is byte-identical to the omitted-fields baseline. Changing an empty DTO into an interface or dropping its constructor would contradict this recorded contract.

The old filled output contains `this.note? = data.note?;`. Current emits `public declare note?: string | null;` and assigns only inside `if ("note" in data)`. This reproduces the old parser/optionality limitation in raw text and shows the documented replacement. Native TypeScript was initially unavailable. The authorized follow-up now confirms this old filled render fails with TS1109 while the current filled render passes syntax. Strict fixture results remain distinct from semantic certification of the raw sample's caller-owned dependencies.

A targeted native-type input further demonstrates the split problem:

| Type placement | v2 raw text | v3 raw text |
| --- | --- | --- |
| Property | `public readonly resolve: (input;` | `public readonly resolve: (input: { key: string }) => string;` |
| Constructor member | `resolve: (input;` | `resolve: (input: { key: string }) => string;` |

See [old colon-type output](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts) and [current colon-type output](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-colon-type.ts). The old macro splits the full declaration on every colon and takes index one. Current emits the caller type string without that parsing. This is recorded #460 repair, not a new #473 DSL or #476 analyzer.

[Code/Test Design §7.1](../issue460/design-code-test-artifacts.md#71-family-inventory-and-required-nucleus) explicitly says description supplies module documentation when module_description is absent. Thus the duplicate minimal documentation has a traceable rationale: two documentation roles reuse one supplied value. Whether to suppress visually redundant output is a possible presentation choice, not a discovered silent omission or an approved deduplication objective. With supplied module_description the filled sample has distinct module/class documentation.

The original sample's Currency import and PriceRecordContract reference depend on caller-owned support modules/contracts. This batch does not treat missing support as a template defect. Current [native contract tests](../../../tests/mcp_server/integration/templates/test_typescript_artifact.py) exercise strict optional semantics, readonly behavior, native object/function types and comment escaping with provisioned fixture dependencies. Their code was inspected in the initial batch. The authorized follow-up re-executes these four tests together with the four existing Commit tests: all eight pass. Their provisioned strict/executable evidence remains distinct from raw syntax preflight and a TypeScript format/lint objective.

### Issue

[Document/Tracking Design §7.6](../issue460/design-document-tracking-artifacts.md#76-tracking-contracts) and §9 explicitly separate the external envelope from the body. The old renderer really emits an H1 title; its removal is intentional. Some catalog wording calls a downstream title unused, but that is not an accurate description of this raw concrete renderer's H1 behavior.

Current moves summary into a named section, changes Steps to Reproduce to Reproduction Steps and renders Context before the step list. Structured steps preserve order/numbering. The exact heading spelling/order is visible contract presentation; a separate per-layout human preference was not found. None of these sample values is lost.

Old Related Documentation uses the supplied target as visible label and leaves related-1 undefined in this raw output. Current Related Documents preserves explicit label/target and emits a matching definition. This is an improvement in the observed renderer surface; the whole old public pipeline is outside the reproduction.

The current absence of status/version/date/history follows body-only ownership. The accepted full-document metadata objective does not require duplicating issue title/labels/milestone/assignees in this body.

### PR

The old minimal root generates test-placeholder prose and four standard unchecked tasks; it also joins the test placeholder directly to `## Checklist`. Current minimal contains only the authored changes and explicit deferred-none rendering. The removed guesses are documented in [#460 §7.6](../issue460/design-document-tracking-artifacts.md#76-tracking-contracts).

Current `deferred_work: []` produces No deferred work identified. That is the rendering of a required caller declaration, not a runtime inference that all work is complete. Populated descriptions/rationales/references remain grouped; they are possible follow-up facts, not instructions to create issues. Checklist completion, Testing prose and Breaking Changes “None.” in the filled sample are caller-authored claims, not measured QA outcomes.

Changing the old warning-icon heading, Closes line and related-document heading presentation has no separately found per-word rationale. These are visible editorial choices; their existence does not by itself establish a first-output defect. Retain meaningful deferred rationale/reference grouping while discussing whitespace.

### Commit

Current renders all supplied subject/body/breaking/refs/footer values without wrapping or changing case. Compared with old filled output, the generated separators between body, breaking description, refs and footer are more consistent; the two extra EOF blank lines remain a distinct defect candidate.

[Tracking Design §7.6](../issue460/design-document-tracking-artifacts.md#76-tracking-contracts) deliberately distinguishes saved provenance from downstream Git/GitHub content. The saved first line is not a conventional commit subject. [commitlint _message_view](../../../mcp_server/bundled_adapters/commitlint/check.py) removes a recognized first provenance line for checking; it is a check view, not a publication route. This batch makes no claim that passing the complete saved file directly to Git is valid.

Marker-only breaking_change=true is intentional. The boundary probe preserves it and renders `Refs: ` for explicitly empty refs. Empty refs/footer/body behavior is a presence-contract issue to keep separate from surplus whitespace; do not silently drop explicit containers while applying a spacing correction.

## Human-approved TypeScript constructor spacing — 2026-10-03

In the sequential decision discussion, the human explicitly agreed to these generated constructor outcomes:

| Surface | Approved outcome |
| --- | --- |
| Ordinary assignments | Consecutive lines, without an empty line before each assignment. |
| Separate logical block | One empty separator before a distinct block such as an optional-property presence check. |
| Constructor braces | No empty source line immediately after the opening brace or before the closing brace. |
| Omitted/empty fields | Preserve the object-style constructor, without blank content lines. |

Preserve assignment order, types, signature and strict optional-presence semantics. This does not select a full TypeScript formatter style, description deduplication or runtime enforcement. The approved generated EOF and inserted-text boundary criteria in [Research](research.md) also apply; raw examples, hashes and native DTOs below remain unchanged historical observations. The complete sequential decisions and pending boundaries are owned by Research. Independent QA is requested only after the remaining decisions are complete.

## Independent whitespace evidence

Counts are from the actual persisted source, excluding the split sentinel after a final newline. Maximum blank run includes EOF and authored blanks; baseline supplied bodies contain no long authored run. Trailing blank lines mean source lines after the final nonblank line; one terminal newline alone contributes zero trailing blank lines. The original measurements preceded numerical approval. The subsequent [generated whitespace and caller-boundary decisions](whitespace-comparison.md) now establish the approved generated joins/EOF and text-block boundary treatment; the observations below remain unchanged.

| Family | v2 max blank run, minimal / filled | v3 max blank run, minimal / filled | v3 extra EOF blank lines, minimal / filled |
| --- | --- | --- | --- |
| typescript_dto | 2 / 1 | 2 / 2 | 1 / 1 |
| issue | 1 / 1 | 8 / 4 | 8 / 1 |
| pr | 1 / 1 | 5 / 5 | 5 / 4 |
| commit | 1 / 1 | 2 / 2 | 2 / 2 |

The old PR/Commit filled examples have no terminal newline. Old Issue sometimes has no blank between a heading and its prose, or between prose and the next heading. Smaller old blank-run counts are therefore not automatic evidence of good layout. No normative “restore v2 whitespace” rule follows.

Five additional current probes cover omitted-versus-empty TypeScript fields, a type containing colons, and authored-plus-empty tracking context. Issue/PR/Commit preserve each marked raw string exactly, including three authored internal blank lines. Issue preserves the authored two-space hard break; PR preserves two blank lines inside its text fence. Template-generated runs remain around those values.

```json
[
  {
    "family": "issue",
    "field": "problem",
    "preserved_exact": true
  },
  {
    "family": "pr",
    "field": "changes",
    "preserved_exact": true
  },
  {
    "family": "commit",
    "field": "body",
    "preserved_exact": true
  }
]
```

No indentation-only line was found in these twenty-two files. The current TypeScript filled constructor has one generated empty line before each required assignment and one extra empty line before its constructor; this is an aesthetic/layout concern that a max-run-only assertion would miss. Source views below locate those transitions. Python Ruff rules are not a substitute for an agreed TypeScript layout baseline.

## Initial native evidence and honest limits

Three attempted run_checks requests selecting typescript_syntax, commit_message or markdown_body were rejected at public selection with error_code=selection_invalid / selection_unsupported before native execution. The complete cache DTOs were read. Those rejected requests are not test results or dependency evidence. Actual native preflight evidence below comes from public scaffold_artifact/safe_edit_file with each selected package's own configured output profile.

| Actual first-output/persistence surface | Factual result |
| --- | --- |
| Eight current baseline scaffolds | All written in report mode; four Issue/PR markdown_body checks passed; two TypeScript and two Commit checks unavailable. |
| Five current boundary scaffolds | All written; Issue/PR body checks passed; two TypeScript and one Commit checks unavailable. |
| Nine exact legacy rewrites | All written; four Issue/PR body checks passed; three TypeScript and two Commit checks unavailable. |
| TypeScript workspace cause | dependency_unavailable: cannot resolve typescript from C:/temp/pgmcp/package.json. |
| Commit workspace cause | dependency_unavailable: cannot resolve @commitlint/cli/package.json from that workspace. |
| Byte preservation | Nine stored legacy outputs equal raw renderer strings; eight fresh current baseline outputs equal the original survey outputs. |
| Gates | No new tests, broad gates, installs, runtime checks or source repairs were performed. Markdown preflight does not certify editorial layout or link resolution. |

The table above and its complete DTO appendix retain the initial, pre-installation environment. Source inspection in that batch was not native compilation evidence. Report-mode persistence preserves evidence; it is not acceptance.

## Authorized native follow-up — 2026-10-03

[The native tooling follow-up](native-tooling-follow-up.md) records installation of the project-pinned TypeScript compiler, commitlint CLI and conventionalcommits parser, with existing Pyright restored and retained. All twelve raw TypeScript/Commit files retain their original SHA-256 hashes after rechecking through their configured content preflights.

| Fresh surface | Result | Causal interpretation |
| --- | --- | --- |
| Four current TypeScript outputs | All passed | Current native syntax is valid, including empty fields and full colon-bearing type text. |
| Old minimal TypeScript | Passed | No syntax defect in this example. |
| Old filled and colon-type TypeScript | Both failed | Native diagnostics confirm the generated question-mark assignment and colon-truncated type defects. |
| Three current Commit outputs | All passed | Configured native message contract is satisfied. |
| Two complete saved old Commit outputs | Both failed | The old comparison provenance header is included in the checked message. |
| Two separately derived old Commit message views | Both passed | Excluding only that first header line isolates valid message content; the raw files remain unchanged. |
| Existing TypeScript and Commit contract tests | 8 passed, 1 existing Pydantic warning | Strict/executable TypeScript fixture contracts and Commit framing/schema contracts are freshly exercised. |

No dependency-unavailable result remains in these fresh checks. Full fresh native DTOs, hashes and derived-view details are retained in the linked follow-up; the old DTO appendix below remains historical and unchanged. The derived message views introduce no legacy compatibility path.

Raw TypeScript preflight checks syntax, while strict fixture tests provision their own dependencies. Neither proves arbitrary external support modules nor an agreed whitespace objective. No TypeScript format/lint tool, universal conventional-commit type policy or new runtime gate is added by this Research comparison.

## Standards and consumer boundaries

| Governing source / consumer | Finding | #473 boundary |
| --- | --- | --- |
| [CODE_STYLE.md](../../coding_standards/CODE_STYLE.md) | Practical Python guidance delegates Python whitespace/imports/line length to configured native tools. It contains no universal TypeScript formatter or tracking metadata/history rule. | Preserve consistent ownership; do not claim Ruff certification for TypeScript or invent cross-language limits. |
| [DOCUMENTATION_STANDARD.md](../../coding_standards/DOCUMENTATION_STANDARD.md) | Concise evidence-backed presentation and clear fact/decision distinctions support readable Issue/PR bodies. No exact blank-run policy or mandatory metadata rule for tracking is stated. | Agree generated joins separately; preserve authored prose, evidence and states. |
| [#460 code/tracking contracts](../issue460/design-code-test-artifacts.md) | Structured native types, optional presence and body-only envelopes are recorded contracts, not layout accidents. | No restoration of old parsing, workflow defaults, tracking H1/envelope metadata or fabricated history. |
| [.agents/workflows/create-issue.md](../../../.agents/workflows/create-issue.md) | Its scaffold example still uses name and forbidden title/labels context; it also says to send the complete saved content as the external body. That does not match current live inputs and the recorded surface distinction. | Record as an existing active instruction/schema/publication-boundary mismatch; no automatic repair or new publication route in this batch. |
| [Existing Issue tests](../../../tests/mcp_server/integration/templates/test_issue.py), [PR tests](../../../tests/mcp_server/integration/templates/test_pr.py), [Commit tests](../../../tests/mcp_server/integration/templates/test_commit_artifact.py) | Tests express no H1, provenance, ordered steps, explicit states, absent/empty presence and multiline message behavior. They do not prove tidy whitespace. | Durable semantic counterevidence informs later spacing regression cases; no workflow-only tests added. |
| [#476](https://github.com/MikeyVK/phase-gate-mcp/issues/476) | Generic schema/template-consumption analysis remains separate. The workflow example is an adjacent active-consumer mismatch, not proof of an ignored admitted field. | Reference findings without taking over generic analysis/enforcement or assuming #476 owns every stale instruction. |

No current rendered field-value loss was demonstrated by this final batch. The tracked presentation concerns are generated spacing/EOF and visible redundancy/heading choices; recorded structural repairs and explicit presence semantics are not defects merely because they differ from old output.

## Recommendations for discussion

- Extend the generated Markdown-join assessment to Issue/PR; retain body-only external ownership and the explicit none/populated deferred declaration.
- Include Commit and TypeScript generated EOF/layout cases in the agreed whitespace contract, with authored message/import/type/documentation text preserved.
- Keep TypeScript minimal documentation reuse traceable to #460; select any suppression of repeated description explicitly, rather than call it an unexplained agent invention.
- Preserve structured native property types, constructor behavior, strict optional presence and meaningful deferred/reference grouping.
- Keep native syntax, strict fixture behavior, Commit message framing and presentation evidence distinct. The authorized prerequisites resolve the initial availability gap; a format/lint or stronger runtime-preflight commitment still requires its own scope/tooling decision.
- Resolve the adjacent create-issue instruction mismatch through an explicitly assigned follow-up or approved affected-consumer slice, not an automatic #476 expansion.

These are recommendations, not new human approvals. All nineteen package comparisons are now available; Research still needs consolidated affected-boundary decisions and independent QA before closure.

## Appendix — exact contexts and numbered source views

`<blank>` and `<two trailing spaces>` are annotation markers only, not edits to source.

### typescript_dto baseline inputs

```json
{
  "minimal": {
    "class_name": "PriceSnapshot",
    "description": "A price snapshot."
  },
  "filled": {
    "class_name": "PriceSnapshot",
    "description": "A price snapshot.",
    "module_description": "A normalized market price.",
    "imports": [
      "import type { Currency } from './money';"
    ],
    "implements": [
      "PriceRecordContract"
    ],
    "fields": [
      {
        "name": "instrument",
        "type": "string",
        "readonly": true,
        "optional": false,
        "description": "Instrument identifier."
      },
      {
        "name": "currency",
        "type": "Currency",
        "readonly": true,
        "optional": false
      },
      {
        "name": "mid",
        "type": "number",
        "readonly": false,
        "optional": false
      },
      {
        "name": "note",
        "type": "string | null",
        "readonly": false,
        "optional": true
      }
    ]
  }
}
```

### issue baseline inputs

```json
{
  "minimal": {
    "problem": "A valid issue body renders without caller-supplied publication metadata."
  },
  "filled": {
    "problem": "The generated Markdown contains extra blank lines.",
    "summary": "The defect appears with valid issue content.",
    "expected": "Headings and paragraphs have consistent spacing.",
    "actual": "The rendered body has excessive vertical whitespace.",
    "context": "Exercise the shipped issue template with valid content.",
    "reproduction_steps": [
      "Render the issue package with this context.",
      "Inspect whitespace between sections."
    ],
    "related_docs": [
      {
        "label": "Template contract",
        "target": "../../../.pgmcp/template_suite/issue/context.schema.json"
      }
    ]
  }
}
```

### pr baseline inputs

```json
{
  "minimal": {
    "changes": "Describe the change.",
    "deferred_work": []
  },
  "filled": {
    "summary": "First-call template output is easier to review.",
    "changes": "Render each shipped concrete package with minimal and populated valid contexts.",
    "testing": "Inspect both generated forms for Python formatting and Markdown presentation.",
    "checklist": [
      {
        "text": "Confirm supplied values are preserved.",
        "checked": true
      },
      {
        "text": "Review rendered whitespace.",
        "checked": false
      }
    ],
    "breaking_changes": "None.",
    "deferred_work": [
      {
        "description": "Review markdown layout",
        "rationale": "The generated body should be readable in a pull request.",
        "references": [
          {
            "label": "PR template schema",
            "target": "../../../.pgmcp/template_suite/pr/context.schema.json"
          }
        ]
      }
    ],
    "closes": [
      473
    ]
  }
}
```

### commit baseline inputs

```json
{
  "minimal": {
    "type": "fix",
    "subject": "Keep caller intent"
  },
  "filled": {
    "type": "feat",
    "scope": "templates",
    "subject": "Preserve authored commit framing",
    "body": "Keep the supplied message text intact.\n\nRetain paragraph boundaries.",
    "breaking_change": true,
    "breaking_description": "Consumers must supply explicit commit fields.",
    "refs": [
      473,
      460
    ],
    "footer": "Reviewed-by: Template Maintainers"
  }
}
```

### typescript_dto old minimal context

Source root: `C:\1Voudig\99_Programming\ST\.pgmcp\templates`; template: `concrete/typescript_dto.ts.jinja2`.

```json
{
  "artifact_type": "typescript_dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "typescript",
  "output_path": "",
  "title": "PriceSnapshot",
  "name": "PriceSnapshot",
  "module_title": "A price snapshot.",
  "fields": []
}
```

### typescript_dto old filled context

Source root: `C:\1Voudig\99_Programming\ST\.pgmcp\templates`; template: `concrete/typescript_dto.ts.jinja2`.

```json
{
  "artifact_type": "typescript_dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "typescript",
  "output_path": "",
  "title": "PriceSnapshot",
  "name": "PriceSnapshot",
  "module_title": "A price snapshot.",
  "module_description": "A normalized market price.",
  "fields": [
    "readonly instrument: string",
    "readonly currency: Currency",
    "mid: number",
    "note?: string | null"
  ],
  "imports": {
    "project": [
      "import type { Currency } from './money';"
    ]
  },
  "implements": "PriceRecordContract"
}
```

### issue old minimal context

Source root: `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates`; template: `concrete/issue.md.jinja2`.

```json
{
  "artifact_type": "issue",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "title": "Issue body comparison",
  "problem": "A valid issue body renders without caller-supplied publication metadata."
}
```

### issue old filled context

Source root: `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates`; template: `concrete/issue.md.jinja2`.

```json
{
  "artifact_type": "issue",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "title": "Issue body comparison",
  "problem": "The generated Markdown contains extra blank lines.",
  "summary": "The defect appears with valid issue content.",
  "expected": "Headings and paragraphs have consistent spacing.",
  "actual": "The rendered body has excessive vertical whitespace.",
  "context": "Exercise the shipped issue template with valid content.",
  "steps_to_reproduce": "1. Render the issue package with this context.\n2. Inspect whitespace between sections.",
  "related_docs": [
    "../../../.pgmcp/template_suite/issue/context.schema.json"
  ]
}
```

### pr old minimal context

Source root: `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates`; template: `concrete/pr.md.jinja2`.

```json
{
  "artifact_type": "pr",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "title": "Pr body comparison",
  "changes": "Describe the change."
}
```

### pr old filled context

Source root: `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates`; template: `concrete/pr.md.jinja2`.

```json
{
  "artifact_type": "pr",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "title": "Pr body comparison",
  "summary": "First-call template output is easier to review.",
  "changes": "Render each shipped concrete package with minimal and populated valid contexts.",
  "testing": "Inspect both generated forms for Python formatting and Markdown presentation.",
  "breaking_changes": "None.",
  "checklist_items": [
    {
      "description": "Confirm supplied values are preserved.",
      "checked": true
    },
    {
      "description": "Review rendered whitespace.",
      "checked": false
    }
  ],
  "closes_issues": [
    473
  ]
}
```

### commit old minimal context

Source root: `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates`; template: `concrete/commit.txt.jinja2`.

```json
{
  "artifact_type": "commit",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "text",
  "output_path": "",
  "title": "Commit body comparison",
  "type": "fix",
  "message": "Keep caller intent"
}
```

### commit old filled context

Source root: `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates`; template: `concrete/commit.txt.jinja2`.

```json
{
  "artifact_type": "commit",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "text",
  "output_path": "",
  "title": "Commit body comparison",
  "type": "feat",
  "scope": "templates",
  "body": "Keep the supplied message text intact.\n\nRetain paragraph boundaries.",
  "breaking_change": true,
  "breaking_description": "Consumers must supply explicit commit fields.",
  "footer": "Reviewed-by: Template Maintainers",
  "message": "Preserve authored commit framing",
  "refs": [
    "#473",
    "#460"
  ]
}
```

### typescript_dto old colon-type context

Source root: `C:\1Voudig\99_Programming\ST\.pgmcp\templates`; template: `concrete/typescript_dto.ts.jinja2`.

```json
{
  "artifact_type": "typescript_dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-03T12:00:00Z",
  "format": "typescript",
  "output_path": "",
  "title": "ArtifactMapper",
  "name": "ArtifactMapper",
  "module_title": "Map a workspace key.",
  "fields": [
    "readonly resolve: (input: { key: string }) => string"
  ]
}
```

### Additional current boundary inputs

```json
[
  {
    "family": "typescript_dto",
    "case": "empty-fields",
    "extension": "ts",
    "context": {
      "class_name": "PriceSnapshot",
      "description": "A price snapshot.",
      "fields": []
    }
  },
  {
    "family": "typescript_dto",
    "case": "colon-type",
    "extension": "ts",
    "context": {
      "class_name": "ArtifactMapper",
      "description": "Map a workspace key.",
      "fields": [
        {
          "name": "resolve",
          "type": "(input: { key: string }) => string",
          "readonly": true,
          "optional": false,
          "description": "Resolve the supplied key."
        }
      ]
    }
  },
  {
    "family": "issue",
    "case": "authored-empty",
    "extension": "md",
    "context": {
      "problem": "AUTHORED_START\n\n\n\nAUTHORED_END  \nHard break remains authored.",
      "reproduction_steps": [],
      "related_docs": []
    }
  },
  {
    "family": "pr",
    "case": "authored-empty",
    "extension": "md",
    "context": {
      "changes": "AUTHORED_START\n\n\n\nAUTHORED_END\n\n```text\nfirst\n\n\nsecond\n```",
      "deferred_work": [],
      "testing": "",
      "checklist": []
    }
  },
  {
    "family": "commit",
    "case": "authored-empty",
    "extension": "txt",
    "context": {
      "type": "fix",
      "subject": "Preserve body spacing",
      "body": "AUTHORED_START\n\n\n\nAUTHORED_END",
      "footer": "",
      "refs": [],
      "breaking_change": true
    }
  }
]
```

### commit.v2-filled-render.txt

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-filled-render.txt); SHA-256: `d9cbfbd265d6bdd50268ba898d28d7e0b18a8358b6db26f752a395d7872bacfb`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/ccb6dc3b28774fb882c8eab3fcfbab07`.

```text
  1 | # template=commit version=comparison-only
  2 | <blank>
  3 | feat(templates)!: Preserve authored commit framing
  4 | <blank>
  5 | Keep the supplied message text intact.
  6 | <blank>
  7 | Retain paragraph boundaries.
  8 | BREAKING CHANGE: Consumers must supply explicit commit fields.
  9 | Refs: #473, #460
 10 | Reviewed-by: Template Maintainers
```

### commit.v2-minimal-render.txt

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/commit.v2-minimal-render.txt); SHA-256: `d83b271a968fd7903a73a683bd302e980fdeac35a7bddf4a285d7ff15cc1415a`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/24ebf508811d4ebdaae31bc4987ed792`.

```text
  1 | # template=commit version=comparison-only
  2 | <blank>
  3 | fix: Keep caller intent
```

### commit.v3-authored-empty.txt

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-authored-empty.txt); SHA-256: `446e142b23fcc311ee332907d90f9744c327f0cacfada6a3bc1c57c7229e7c51`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/4ee439c3c90b4fef94a6fb3f78482d4f`.

```text
  1 | # pgmcp:v1 id=commit pv=1.0.0 pf=_Yga89XCROsHUBlO sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | fix!: Preserve body spacing
  4 | <blank>
  5 | AUTHORED_START
  6 | <blank>
  7 | <blank>
  8 | <blank>
  9 | AUTHORED_END
 10 | <blank>
 11 | Refs: 
 12 | <blank>
 13 | <blank>
 14 | <blank>
 15 | <blank>
```

### commit.v3-filled.txt

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-filled.txt); SHA-256: `68a77cd959414766cee1d942491afdb1a890601e233b41bb0f296b26bb6b7ccc`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/7bfca9a310134039819e6c87cf5cb17d`.

```text
  1 | # pgmcp:v1 id=commit pv=1.0.0 pf=_Yga89XCROsHUBlO sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | feat(templates)!: Preserve authored commit framing
  4 | <blank>
  5 | Keep the supplied message text intact.
  6 | <blank>
  7 | Retain paragraph boundaries.
  8 | <blank>
  9 | BREAKING CHANGE: Consumers must supply explicit commit fields.
 10 | <blank>
 11 | Refs: #473, #460
 12 | <blank>
 13 | Reviewed-by: Template Maintainers
 14 | <blank>
 15 | <blank>
```

### commit.v3-minimal.txt

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/commit.v3-minimal.txt); SHA-256: `55f1761d484042c7176109d0214e6756c49fae050d5755e841d3926069988910`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/ef8c41a0e9e54e3bb9e214e141506486`.

```text
  1 | # pgmcp:v1 id=commit pv=1.0.0 pf=_Yga89XCROsHUBlO sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | fix: Keep caller intent
  4 | <blank>
  5 | <blank>
```

### issue.v2-filled-render.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/issue.v2-filled-render.md); SHA-256: `bb861c6b2fcdacb4e8a43cf96363855d23a0cdc1c9ed8a87a98c6b6a4a5bb4f9`; native preflight: passed; receipt: `pgmcp://cache/runs/4bc7866e93ec44bab1f64fb824258044`.

```text
  1 | <!-- template=issue version=comparison-only -->
  2 | # Issue body comparison
  3 | <blank>
  4 | The defect appears with valid issue content.
  5 | ## Problem
  6 | The generated Markdown contains extra blank lines.
  7 | <blank>
  8 | ## Expected Behavior
  9 | <blank>
 10 | Headings and paragraphs have consistent spacing.
 11 | ## Actual Behavior
 12 | <blank>
 13 | The rendered body has excessive vertical whitespace.
 14 | ## Steps to Reproduce
 15 | <blank>
 16 | 1. Render the issue package with this context.
 17 | 2. Inspect whitespace between sections.
 18 | ## Context
 19 | <blank>
 20 | Exercise the shipped issue template with valid content.
 21 | ## Related Documentation
 22 | - **[../../../.pgmcp/template_suite/issue/context.schema.json][related-1]**
```

### issue.v2-minimal-render.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/issue.v2-minimal-render.md); SHA-256: `3359657b5e9a6e5465e958d1005e48d21c0dc5d6fc553a68c55d32a90ed90c41`; native preflight: passed; receipt: `pgmcp://cache/runs/f82a1dae60964eda8b817a9f4c9e98a8`.

```text
  1 | <!-- template=issue version=comparison-only -->
  2 | # Issue body comparison
  3 | <blank>
  4 | ## Problem
  5 | A valid issue body renders without caller-supplied publication metadata.
```

### issue.v3-authored-empty.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/issue.v3-authored-empty.md); SHA-256: `2f7b6ffb1d3a694a3817b4b4d6661bc3d64521c0cb43ba1de06c4b24e3e46dec`; native preflight: passed; receipt: `pgmcp://cache/runs/90414bc024c1402bb2f8cd28f93d8263`.

```text
  1 | <!-- pgmcp:v1 id=issue pv=1.0.0 pf=O3lr-JfD_5Kv7Cfx sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | <blank>
  4 | ## Problem
  5 | <blank>
  6 | AUTHORED_START
  7 | <blank>
  8 | <blank>
  9 | <blank>
 10 | AUTHORED_END<two trailing spaces>
 11 | Hard break remains authored.
 12 | <blank>
 13 | <blank>
 14 | <blank>
 15 | <blank>
 16 | <blank>
 17 | <blank>
 18 | ## Reproduction Steps
 19 | <blank>
 20 | <blank>
 21 | <blank>
 22 | <blank>
 23 | <blank>
 24 | ## Related Documents
 25 | <blank>
 26 | <blank>
 27 | <blank>
```

### issue.v3-filled.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/issue.v3-filled.md); SHA-256: `f4c1a6256a90fd318145a38c227c25bdf9ca49906675b1e960f15b2dd89817b0`; native preflight: passed; receipt: `pgmcp://cache/runs/97b33022bdc04445ba10050aae14a91b`.

```text
  1 | <!-- pgmcp:v1 id=issue pv=1.0.0 pf=O3lr-JfD_5Kv7Cfx sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | <blank>
  4 | ## Problem
  5 | <blank>
  6 | The generated Markdown contains extra blank lines.
  7 | <blank>
  8 | <blank>
  9 | ## Summary
 10 | <blank>
 11 | The defect appears with valid issue content.
 12 | <blank>
 13 | <blank>
 14 | <blank>
 15 | ## Expected Behavior
 16 | <blank>
 17 | Headings and paragraphs have consistent spacing.
 18 | <blank>
 19 | <blank>
 20 | <blank>
 21 | ## Actual Behavior
 22 | <blank>
 23 | The rendered body has excessive vertical whitespace.
 24 | <blank>
 25 | <blank>
 26 | <blank>
 27 | ## Context
 28 | <blank>
 29 | Exercise the shipped issue template with valid content.
 30 | <blank>
 31 | <blank>
 32 | <blank>
 33 | ## Reproduction Steps
 34 | <blank>
 35 | 1. Render the issue package with this context.
 36 | 2. Inspect whitespace between sections.
 37 | <blank>
 38 | <blank>
 39 | <blank>
 40 | <blank>
 41 | ## Related Documents
 42 | <blank>
 43 | - [Template contract][related-1]
 44 | <blank>
 45 | [related-1]: <../../../.pgmcp/template_suite/issue/context.schema.json>
 46 | <blank>
```

### issue.v3-minimal.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/issue.v3-minimal.md); SHA-256: `984e6c0edeed40b3a9cef85c3716641c6c9c45c8fef4927dc7af4bbda9540c9f`; native preflight: passed; receipt: `pgmcp://cache/runs/ce6acf98d1df4ad6b6a9ea741c8cac7a`.

```text
  1 | <!-- pgmcp:v1 id=issue pv=1.0.0 pf=O3lr-JfD_5Kv7Cfx sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | <blank>
  4 | ## Problem
  5 | <blank>
  6 | A valid issue body renders without caller-supplied publication metadata.
  7 | <blank>
  8 | <blank>
  9 | <blank>
 10 | <blank>
 11 | <blank>
 12 | <blank>
 13 | <blank>
 14 | <blank>
```

### pr.v2-filled-render.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/pr.v2-filled-render.md); SHA-256: `4e7fc81546944ba6fe7e9e69bc0ef5a2016f079a984ffe95c8b871f59f89ff2f`; native preflight: passed; receipt: `pgmcp://cache/runs/0fa4c50b1e2640899510bec71b5e8220`.

```text
  1 | <!-- template=pr version=comparison-only -->
  2 | # Pr body comparison
  3 | <blank>
  4 | First-call template output is easier to review.
  5 | ## Changes
  6 | Render each shipped concrete package with minimal and populated valid contexts.
  7 | <blank>
  8 | ## Testing
  9 | Inspect both generated forms for Python formatting and Markdown presentation.
 10 | ## Checklist
 11 | <blank>
 12 | - [x] Confirm supplied values are preserved.
 13 | - [ ] Review rendered whitespace.
 14 | <blank>
 15 | ## ⚠️ Breaking Changes
 16 | <blank>
 17 | None.
 18 | ---
 19 | <blank>
 20 | Closes: #473
```

### pr.v2-minimal-render.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/pr.v2-minimal-render.md); SHA-256: `ff293dcc3c9eed3330f0af7dc47755e9265760efc2bff0a5622a2d5cc798e3dd`; native preflight: passed; receipt: `pgmcp://cache/runs/0ff9a91338d6458d875a1fdf72cbd875`.

```text
  1 | <!-- template=pr version=comparison-only -->
  2 | # Pr body comparison
  3 | <blank>
  4 | ## Changes
  5 | Describe the change.
  6 | <blank>
  7 | ## Testing
  8 | [Describe how this was tested]## Checklist
  9 | <blank>
 10 | - [ ] Code follows project standards
 11 | - [ ] Tests added/updated
 12 | - [ ] Documentation updated
 13 | - [ ] Quality gates passing
```

### pr.v3-authored-empty.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/pr.v3-authored-empty.md); SHA-256: `eeedb3f12b18f28d76d5b5739e9aa95d07f542a0b095b0fd3a1508aaf07e4522`; native preflight: passed; receipt: `pgmcp://cache/runs/a0b35f9769064b5f83951cb58254479c`.

```text
  1 | <!-- pgmcp:v1 id=pr pv=1.0.0 pf=XKvE7Nls1VlJQIPF sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | <blank>
  4 | <blank>
  5 | ## Changes
  6 | <blank>
  7 | AUTHORED_START
  8 | <blank>
  9 | <blank>
 10 | <blank>
 11 | AUTHORED_END
 12 | <blank>
 13 | ```text
 14 | first
 15 | <blank>
 16 | <blank>
 17 | second
 18 | ```
 19 | <blank>
 20 | <blank>
 21 | ## Testing
 22 | <blank>
 23 | <blank>
 24 | <blank>
 25 | <blank>
 26 | <blank>
 27 | ## Checklist
 28 | <blank>
 29 | <blank>
 30 | <blank>
 31 | <blank>
 32 | <blank>
 33 | ## Deferred Work
 34 | <blank>
 35 | <blank>
 36 | No deferred work identified.
 37 | <blank>
 38 | <blank>
 39 | <blank>
 40 | <blank>
 41 | <blank>
```

### pr.v3-filled.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/pr.v3-filled.md); SHA-256: `3f72b5819a96af436fdfe0cb673c2e78dbae5fe7dcecc84ef0651f199ae10fb3`; native preflight: passed; receipt: `pgmcp://cache/runs/af6cf4972f794fffb7dd122fa9b0d3ca`.

```text
  1 | <!-- pgmcp:v1 id=pr pv=1.0.0 pf=XKvE7Nls1VlJQIPF sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | <blank>
  4 | <blank>
  5 | ## Summary
  6 | <blank>
  7 | First-call template output is easier to review.
  8 | <blank>
  9 | <blank>
 10 | ## Changes
 11 | <blank>
 12 | Render each shipped concrete package with minimal and populated valid contexts.
 13 | <blank>
 14 | <blank>
 15 | ## Testing
 16 | <blank>
 17 | Inspect both generated forms for Python formatting and Markdown presentation.
 18 | <blank>
 19 | <blank>
 20 | <blank>
 21 | ## Checklist
 22 | <blank>
 23 | - [x] Confirm supplied values are preserved.
 24 | - [ ] Review rendered whitespace.
 25 | <blank>
 26 | <blank>
 27 | <blank>
 28 | ## Breaking Changes
 29 | <blank>
 30 | None.
 31 | <blank>
 32 | <blank>
 33 | ## Deferred Work
 34 | <blank>
 35 | <blank>
 36 | <blank>
 37 | ### Review markdown layout
 38 | <blank>
 39 | The generated body should be readable in a pull request.
 40 | <blank>
 41 | <blank>
 42 | **References:**
 43 | <blank>
 44 | - [PR template schema](<../../../.pgmcp/template_suite/pr/context.schema.json>)
 45 | <blank>
 46 | <blank>
 47 | <blank>
 48 | <blank>
 49 | <blank>
 50 | ## Closes
 51 | <blank>
 52 | #473
 53 | <blank>
 54 | <blank>
 55 | <blank>
 56 | <blank>
```

### pr.v3-minimal.md

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/pr.v3-minimal.md); SHA-256: `a9a8d000fd397e472088b3fed0a7d2221e6d1ab96fa82f99145c622176f654f3`; native preflight: passed; receipt: `pgmcp://cache/runs/2f92edeec4994177b98a894150ffa6bd`.

```text
  1 | <!-- pgmcp:v1 id=pr pv=1.0.0 pf=XKvE7Nls1VlJQIPF sf=9PfER5JkyAoFQLRi -->
  2 | <blank>
  3 | <blank>
  4 | <blank>
  5 | ## Changes
  6 | <blank>
  7 | Describe the change.
  8 | <blank>
  9 | <blank>
 10 | <blank>
 11 | <blank>
 12 | ## Deferred Work
 13 | <blank>
 14 | <blank>
 15 | No deferred work identified.
 16 | <blank>
 17 | <blank>
 18 | <blank>
 19 | <blank>
 20 | <blank>
```

### typescript_dto.v2-colon-type-render.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts); SHA-256: `b9f23918a8985b4e1a12fb0b94f1082ab9dab5c13166bbdc45ebca929a70fd7d`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/fee023cd30b94fc2bccccd85e9362373`.

```text
  1 | // template=typescript_dto version=comparison-only
  2 | /**
  3 | * Map a workspace key..
  4 |  *
  5 |  * @layer Unknown * @responsibilities *   - [To be defined] */
  6 | <blank>
  7 | <blank>
  8 | export class ArtifactMapper {
  9 |   public readonly resolve: (input;
 10 |   constructor(data: {
 11 |     resolve: (input;
 12 |   }) {
 13 |     this.resolve = data.resolve;
 14 |   }
 15 | }
```

### typescript_dto.v2-filled-render.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts); SHA-256: `78223c27b7af07aaf91955be3ff2ccb437beba695b23d7aa90fa0260b09a9771`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/7a61e481839048e6afa6b172fdcef34d`.

```text
  1 | // template=typescript_dto version=comparison-only
  2 | /**
  3 | * A price snapshot..
  4 |  *
  5 |  * A normalized market price.
  6 |  *
  7 |  * @layer Unknown * @responsibilities *   - [To be defined] */
  8 | <blank>
  9 | import type { Currency } from './money';
 10 | export class PriceSnapshot implements PriceRecordContract {
 11 |   public readonly instrument: string;
 12 |   public readonly currency: Currency;
 13 |   public mid: number;
 14 |   public note?: string | null;
 15 |   constructor(data: {
 16 |     instrument: string;
 17 |     currency: Currency;
 18 |     mid: number;
 19 |     note?: string | null;
 20 |   }) {
 21 |     this.instrument = data.instrument;
 22 |     this.currency = data.currency;
 23 |     this.mid = data.mid;
 24 |     this.note? = data.note?;
 25 |   }
 26 | }
```

### typescript_dto.v2-minimal-render.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v2-minimal-render.ts); SHA-256: `a373b0a9b2418ec0e64612abf20acc6d249808f775a483f5f627440c1b102022`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/ec1253b06cb54d1a80eb5a2f2a96e1a0`.

```text
  1 | // template=typescript_dto version=comparison-only
  2 | /**
  3 | * A price snapshot..
  4 |  *
  5 |  * @layer Unknown * @responsibilities *   - [To be defined] */
  6 | <blank>
  7 | <blank>
  8 | export class PriceSnapshot {
  9 |   constructor(data: {
 10 |   }) {
 11 |   }
 12 | }
```

### typescript_dto.v3-colon-type.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-colon-type.ts); SHA-256: `a8d691c220e7e60cebe040a03a309ad118bbf1f63624abb653eedde5ba1c393e`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/75de2268b28a4ba088c7362e76578b67`.

```text
  1 | // pgmcp:v1 id=typescript_dto pv=1.0.0 pf=nrJatmiH7RAfWNzm sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | /**
  4 |  * Map a workspace key.
  5 |  */
  6 | <blank>
  7 | <blank>
  8 | /**
  9 |  * Map a workspace key.
 10 |  */
 11 | export class ArtifactMapper {
 12 | <blank>
 13 |   /**
 14 |    * Resolve the supplied key.
 15 |    */
 16 |   public readonly resolve: (input: { key: string }) => string;
 17 | <blank>
 18 | <blank>
 19 |   constructor(data: {
 20 |     resolve: (input: { key: string }) => string;
 21 |   }) {
 22 | <blank>
 23 |     this.resolve = data.resolve;
 24 |   }
 25 | }
 26 | <blank>
```

### typescript_dto.v3-empty-fields.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-empty-fields.ts); SHA-256: `1b6c2b3c9242615d061acace7777a122c2a406a36b089f9854523df65d170721`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/9c39048a3f5f41408aed349f1b3d7520`.

```text
  1 | // pgmcp:v1 id=typescript_dto pv=1.0.0 pf=nrJatmiH7RAfWNzm sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | /**
  4 |  * A price snapshot.
  5 |  */
  6 | <blank>
  7 | <blank>
  8 | /**
  9 |  * A price snapshot.
 10 |  */
 11 | export class PriceSnapshot {
 12 | <blank>
 13 | <blank>
 14 |   constructor(data: {}) {
 15 |   }
 16 | }
 17 | <blank>
```

### typescript_dto.v3-filled.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-filled.ts); SHA-256: `09e3d178fa9e001a601d461a8f497507a0ff8e0fcdc0c0ecc717be03be6db8e6`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/04be3a606e474116bad0ddeb3ca94c42`.

```text
  1 | // pgmcp:v1 id=typescript_dto pv=1.0.0 pf=nrJatmiH7RAfWNzm sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | /**
  4 |  * A normalized market price.
  5 |  */
  6 | <blank>
  7 | import type { Currency } from './money';
  8 | <blank>
  9 | <blank>
 10 | /**
 11 |  * A price snapshot.
 12 |  */
 13 | export class PriceSnapshot implements PriceRecordContract {
 14 | <blank>
 15 |   /**
 16 |    * Instrument identifier.
 17 |    */
 18 |   public readonly instrument: string;
 19 | <blank>
 20 |   public readonly currency: Currency;
 21 | <blank>
 22 |   public mid: number;
 23 | <blank>
 24 |   public declare note?: string | null;
 25 | <blank>
 26 | <blank>
 27 |   constructor(data: {
 28 |     instrument: string;
 29 |     currency: Currency;
 30 |     mid: number;
 31 |     note?: string | null;
 32 |   }) {
 33 | <blank>
 34 |     this.instrument = data.instrument;
 35 | <blank>
 36 |     this.currency = data.currency;
 37 | <blank>
 38 |     this.mid = data.mid;
 39 | <blank>
 40 |     if ("note" in data) {
 41 |       this.note = data.note;
 42 |     }
 43 |   }
 44 | }
 45 | <blank>
```

### typescript_dto.v3-minimal.ts

[Raw file](../../../.pgmcp/temp/issue473-comparison-05/typescript_dto.v3-minimal.ts); SHA-256: `1b6c2b3c9242615d061acace7777a122c2a406a36b089f9854523df65d170721`; initial native preflight: unavailable; receipt: `pgmcp://cache/runs/8cd33d672a944eada0987b816f7b3b03`.

```text
  1 | // pgmcp:v1 id=typescript_dto pv=1.0.0 pf=nrJatmiH7RAfWNzm sf=9PfER5JkyAoFQLRi
  2 | <blank>
  3 | /**
  4 |  * A price snapshot.
  5 |  */
  6 | <blank>
  7 | <blank>
  8 | /**
  9 |  * A price snapshot.
 10 |  */
 11 | export class PriceSnapshot {
 12 | <blank>
 13 | <blank>
 14 |   constructor(data: {}) {
 15 |   }
 16 | }
 17 | <blank>
```

## Appendix — source hashes

| Root | Template / shared source | SHA-256 |
| --- | --- | --- |
| legacy original | `concrete/commit.txt.jinja2` | `4ab0569f7a8b45d96005f4af57cd1eac8bd32d26026dddfd33cc5fedbb4cb75c` |
| legacy original | `concrete/issue.md.jinja2` | `08dba71a7c14ba945883cc30201ea8ed35b4f471616830a1eee5f7e2d825a6b6` |
| legacy original | `concrete/pr.md.jinja2` | `0ee118f763fa9998580b221d856e28ba9e82e69e2b37272e86e573fc6bab4f59` |
| legacy original | `tier1_base_tracking.jinja2` | `92b133451d44b1e9ae469dff9a585f43136df06bead19be552c7f1243b7b7d7f` |
| legacy original | `tier2_tracking_markdown.jinja2` | `b52303ca7db85aaba2f674ea849f578220b8b20eaa33a3f9240f614a48874785` |
| legacy original | `tier2_tracking_text.jinja2` | `68ecef4a411e2b1916dbc9a30a3424feae9a8a9b7c9497f39490f5e96b13203b` |
| legacy original | `tier0_base_artifact.jinja2` | `07c1ebf7df1accfe88cdfcd28fbaa07d4182c099411e344b68fd2c43d0576875` |
| legacy installed | `concrete/typescript_dto.ts.jinja2` | `d6305f5e22681286ab72d5a44137f4cc5491496b4a4f9cd63468d091b7a2cde9` |
| legacy installed | `tier3_pattern_typescript_dto.jinja2` | `30cbcd5f4c62ab4b0b48fcf65eaf2d1f57a13eae822b2256ca7ba72da0418383` |
| legacy installed | `tier2_base_typescript.jinja2` | `cd7afe9f3e57d832cad092eff62caf54ee32f9dd447630dbef2d3130c7498bfb` |
| legacy installed | `tier1_base_code.jinja2` | `b7cc8a03c49c613241947e0825eea96f3e7b8ccbcaae849888c5c36d054d1187` |
| legacy installed | `tier0_base_artifact.jinja2` | `8b531031e82c7315ce95deebe1e88e12e46aaffb86a5707bafba5869443d4b18` |
| current suite | `typescript_dto/template.jinja2` | `6fbafd43dc5e5968d33add647bc8ad7b51ade3b7ec162610a523ee21ba2a1d6a` |
| current suite | `commit/template.jinja2` | `ac07b453dcaae679934935dde0bae6684a8347d4028a2a60691974dc0f937360` |
| current suite | `issue/template.jinja2` | `8f71331d0aa88655c46f7804736d460f99d302960195ec0529279307382d89fa` |
| current suite | `pr/template.jinja2` | `5144a53dea5fe26e846f27d4ae120a5f8f55bf647d0f7d574fa4162bcde63916` |
| current suite | `shared/templates/bases/tier2_typescript.jinja2` | `e3f858a71e9f83700a82adabc26545964c85dba3942d52a17ff6f69021b46bef` |
| current suite | `shared/templates/bases/tier2_text_tracking.jinja2` | `9b2a33bae3076e79b44adfb67cd4683cabd9e4145519787727a0882089245b32` |
| current suite | `shared/templates/bases/tier2_markdown_tracking.jinja2` | `ce8ab1f6dda4b3424ea083550fc71012fa286f11f8d2d964e15aa2f47e232787` |
| current suite | `shared/templates/bases/tier1_tracking.jinja2` | `b6571160b411bc04b9a795e54e1fcd4101c335ef100c94db77c434587886f23f` |
| current suite | `shared/templates/patterns/markdown/sections.jinja2` | `e91910e2bcc46d00fdfc1f837c4ab033fb80a1f28f8d864fa8204a44f753dadf` |
| current suite | `shared/templates/patterns/markdown/links.jinja2` | `b19464ba140fd575c85579bf1500bb614f8ddc28ceea44a2e66195b4569f02a5` |
## Appendix — historical pre-installation native persistence DTOs

These complete receipts retain the initial environment. Fresh native checks after authorized installation are recorded in [the follow-up](native-tooling-follow-up.md).

The original cached DTOs were fully read; bootstrap DTOs are excluded from the final-output evidence list.

```json
[
  {
    "file": "typescript_dto.v3-minimal.ts",
    "kind": "current",
    "uri": "pgmcp://cache/runs/8cd33d672a944eada0987b816f7b3b03",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-minimal.ts",
      "template_id": "typescript_dto",
      "package_version": "1.0.0",
      "package_fingerprint": "nrJatmiH7RAfWNzm"
    }
  },
  {
    "file": "typescript_dto.v3-filled.ts",
    "kind": "current",
    "uri": "pgmcp://cache/runs/04be3a606e474116bad0ddeb3ca94c42",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-filled.ts",
      "template_id": "typescript_dto",
      "package_version": "1.0.0",
      "package_fingerprint": "nrJatmiH7RAfWNzm"
    }
  },
  {
    "file": "issue.v3-minimal.md",
    "kind": "current",
    "uri": "pgmcp://cache/runs/ce6acf98d1df4ad6b6a9ea741c8cac7a",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/issue.v3-minimal.md",
      "template_id": "issue",
      "package_version": "1.0.0",
      "package_fingerprint": "O3lr-JfD_5Kv7Cfx"
    }
  },
  {
    "file": "issue.v3-filled.md",
    "kind": "current",
    "uri": "pgmcp://cache/runs/97b33022bdc04445ba10050aae14a91b",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/issue.v3-filled.md",
      "template_id": "issue",
      "package_version": "1.0.0",
      "package_fingerprint": "O3lr-JfD_5Kv7Cfx"
    }
  },
  {
    "file": "pr.v3-minimal.md",
    "kind": "current",
    "uri": "pgmcp://cache/runs/2f92edeec4994177b98a894150ffa6bd",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/pr.v3-minimal.md",
      "template_id": "pr",
      "package_version": "1.0.0",
      "package_fingerprint": "XKvE7Nls1VlJQIPF"
    }
  },
  {
    "file": "pr.v3-filled.md",
    "kind": "current",
    "uri": "pgmcp://cache/runs/af6cf4972f794fffb7dd122fa9b0d3ca",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": {
            "format": "json",
            "data": {
              "issues": [
                {
                  "severity": "warning",
                  "message": "Broken link: '<../../../.pgmcp/template_suite/pr/context.schema.json>' not found at C:\\temp\\pgmcp\\.pgmcp\\temp\\.pgmcp\\template_suite\\pr\\context.schema.json>",
                  "line": 44
                }
              ]
            }
          },
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 350,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/pr.v3-filled.md",
      "template_id": "pr",
      "package_version": "1.0.0",
      "package_fingerprint": "XKvE7Nls1VlJQIPF"
    }
  },
  {
    "file": "commit.v3-minimal.txt",
    "kind": "current",
    "uri": "pgmcp://cache/runs/ef8c41a0e9e54e3bb9e214e141506486",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "commit_preflight",
      "checks": [
        {
          "check_id": "commit_message",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "Error: Cannot find module '@commitlint/cli/package.json'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "commitlint",
              "version": "1.0.0",
              "fingerprint": "vC85itWZeYn0YZQo",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 249,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 225,
                "head": "C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n  warnings.warn(\r\n",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "commitlint",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/commit.v3-minimal.txt",
      "template_id": "commit",
      "package_version": "1.0.0",
      "package_fingerprint": "_Yga89XCROsHUBlO"
    }
  },
  {
    "file": "commit.v3-filled.txt",
    "kind": "current",
    "uri": "pgmcp://cache/runs/7bfca9a310134039819e6c87cf5cb17d",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "commit_preflight",
      "checks": [
        {
          "check_id": "commit_message",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "Error: Cannot find module '@commitlint/cli/package.json'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "commitlint",
              "version": "1.0.0",
              "fingerprint": "vC85itWZeYn0YZQo",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 249,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 225,
                "head": "C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n  warnings.warn(\r\n",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "commitlint",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/commit.v3-filled.txt",
      "template_id": "commit",
      "package_version": "1.0.0",
      "package_fingerprint": "_Yga89XCROsHUBlO"
    }
  },
  {
    "file": "typescript_dto.v2-minimal-render.ts",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/ec1253b06cb54d1a80eb5a2f2a96e1a0",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-minimal-render.ts",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "typescript_dto",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "typescript_dto.v2-filled-render.ts",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/7a61e481839048e6afa6b172fdcef34d",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-filled-render.ts",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "typescript_dto",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "issue.v2-minimal-render.md",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/f82a1dae60964eda8b817a9f4c9e98a8",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/issue.v2-minimal-render.md",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "issue",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "issue.v2-filled-render.md",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/4bc7866e93ec44bab1f64fb824258044",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/issue.v2-filled-render.md",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "issue",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "pr.v2-minimal-render.md",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/0ff9a91338d6458d875a1fdf72cbd875",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/pr.v2-minimal-render.md",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "pr",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "pr.v2-filled-render.md",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/0fa4c50b1e2640899510bec71b5e8220",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/pr.v2-filled-render.md",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "pr",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "commit.v2-minimal-render.txt",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/24ebf508811d4ebdaae31bc4987ed792",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "commit_preflight",
      "checks": [
        {
          "check_id": "commit_message",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "Error: Cannot find module '@commitlint/cli/package.json'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "commitlint",
              "version": "1.0.0",
              "fingerprint": "vC85itWZeYn0YZQo",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 249,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 225,
                "head": "C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n  warnings.warn(\r\n",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "commitlint",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/commit.v2-minimal-render.txt",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "commit",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "commit.v2-filled-render.txt",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/ccb6dc3b28774fb882c8eab3fcfbab07",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "commit_preflight",
      "checks": [
        {
          "check_id": "commit_message",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "Error: Cannot find module '@commitlint/cli/package.json'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "commitlint",
              "version": "1.0.0",
              "fingerprint": "vC85itWZeYn0YZQo",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 249,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 225,
                "head": "C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n  warnings.warn(\r\n",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "commitlint",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/commit.v2-filled-render.txt",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "commit",
      "extension": null,
      "selection_reason": null
    }
  },
  {
    "file": "typescript_dto.v3-empty-fields.ts",
    "kind": "boundary",
    "uri": "pgmcp://cache/runs/9c39048a3f5f41408aed349f1b3d7520",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-empty-fields.ts",
      "template_id": "typescript_dto",
      "package_version": "1.0.0",
      "package_fingerprint": "nrJatmiH7RAfWNzm"
    }
  },
  {
    "file": "typescript_dto.v3-colon-type.ts",
    "kind": "boundary",
    "uri": "pgmcp://cache/runs/75de2268b28a4ba088c7362e76578b67",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v3-colon-type.ts",
      "template_id": "typescript_dto",
      "package_version": "1.0.0",
      "package_fingerprint": "nrJatmiH7RAfWNzm"
    }
  },
  {
    "file": "issue.v3-authored-empty.md",
    "kind": "boundary",
    "uri": "pgmcp://cache/runs/90414bc024c1402bb2f8cd28f93d8263",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/issue.v3-authored-empty.md",
      "template_id": "issue",
      "package_version": "1.0.0",
      "package_fingerprint": "O3lr-JfD_5Kv7Cfx"
    }
  },
  {
    "file": "pr.v3-authored-empty.md",
    "kind": "boundary",
    "uri": "pgmcp://cache/runs/a0b35f9769064b5f83951cb58254479c",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "passed",
      "profile_id": "markdown_body",
      "checks": [
        {
          "check_id": "markdown_body",
          "status": "passed",
          "reason": null,
          "message": null,
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "markdown_preflight",
              "version": "1.0.0",
              "fingerprint": "v0NjYjqP55u7eH7r",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 0,
              "stdout": {
                "observed_bytes": 92,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "python",
                "version": "3.13.7"
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/pr.v3-authored-empty.md",
      "template_id": "pr",
      "package_version": "1.0.0",
      "package_fingerprint": "XKvE7Nls1VlJQIPF"
    }
  },
  {
    "file": "commit.v3-authored-empty.txt",
    "kind": "boundary",
    "uri": "pgmcp://cache/runs/4ee439c3c90b4fef94a6fb3f78482d4f",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "commit_preflight",
      "checks": [
        {
          "check_id": "commit_message",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "Error: Cannot find module '@commitlint/cli/package.json'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "commitlint",
              "version": "1.0.0",
              "fingerprint": "vC85itWZeYn0YZQo",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 249,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 225,
                "head": "C:\\Users\\miche\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pydantic\\_internal\\_fields.py:198: UserWarning: Field name \"schema\" in \"SchemaAttachment\" shadows an attribute in parent \"BaseModel\"\r\n  warnings.warn(\r\n",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "commitlint",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "output_path": ".pgmcp/temp/issue473-comparison-05/commit.v3-authored-empty.txt",
      "template_id": "commit",
      "package_version": "1.0.0",
      "package_fingerprint": "_Yga89XCROsHUBlO"
    }
  },
  {
    "file": "typescript_dto.v2-colon-type-render.ts",
    "kind": "legacy",
    "uri": "pgmcp://cache/runs/fee023cd30b94fc2bccccd85e9362373",
    "result": {
      "success": true,
      "written": true,
      "validation_policy": "report",
      "validation_status": "unavailable",
      "profile_id": "typescript_preflight",
      "checks": [
        {
          "check_id": "typescript_syntax",
          "status": "unavailable",
          "reason": "dependency_unavailable",
          "message": "TypeScript is unavailable from the workspace: Cannot find module 'typescript'\nRequire stack:\n- C:\\temp\\pgmcp\\package.json",
          "evidence": null,
          "request_rejection": null,
          "invocation": {
            "adapter": {
              "adapter_id": "typescript_syntax",
              "version": "1.0.0",
              "fingerprint": "vO-8nOBLkGGYzBfJ",
              "contract_version": 1
            },
            "capture": {
              "exit_code": 3,
              "stdout": {
                "observed_bytes": 270,
                "head": null,
                "tail": null,
                "truncated": false
              },
              "stderr": {
                "observed_bytes": 0,
                "head": "",
                "tail": "",
                "truncated": false
              }
            },
            "external_tools": [
              {
                "tool_id": "typescript",
                "version": null
              }
            ]
          },
          "termination_problem": null,
          "housekeeping": [],
          "args_source": "configured",
          "effective_args": []
        }
      ],
      "error_code": null,
      "error_details": null,
      "housekeeping": [],
      "path": ".pgmcp/temp/issue473-comparison-05/typescript_dto.v2-colon-type-render.ts",
      "content_changed": true,
      "selected_source": "input",
      "template_id": "typescript_dto",
      "extension": null,
      "selection_reason": null
    }
  }
]
```

## Appendix — public selection rejections

These are recorded unsuccessful requests, not native executions.

```json
[
  {
    "surface": "typescript",
    "uri": "pgmcp://cache/runs/423557e570fe43ce8c4f0213cdddb6fe",
    "dto": {
      "success": true,
      "run_status": null,
      "requested_scope": "targets",
      "requested_targets": [
        ".pgmcp/temp/issue473-survey/typescript_dto.filled.ts",
        ".pgmcp/temp/issue473-survey/typescript_dto.minimal.ts"
      ],
      "selected_profile": null,
      "removed_targets": [],
      "results": [],
      "error_code": "selection_invalid",
      "error_details": {
        "issues": [
          {
            "reason": "selection_unsupported",
            "check_id": "typescript_syntax"
          }
        ]
      }
    }
  },
  {
    "surface": "commit",
    "uri": "pgmcp://cache/runs/518e8edec0b945898ab6d5d401ae34dc",
    "dto": {
      "success": true,
      "run_status": null,
      "requested_scope": "targets",
      "requested_targets": [
        ".pgmcp/temp/issue473-survey/commit.filled.txt",
        ".pgmcp/temp/issue473-survey/commit.minimal.txt"
      ],
      "selected_profile": null,
      "removed_targets": [],
      "results": [],
      "error_code": "selection_invalid",
      "error_details": {
        "issues": [
          {
            "reason": "selection_unsupported",
            "check_id": "commit_message"
          }
        ]
      }
    }
  },
  {
    "surface": "tracking_markdown",
    "uri": "pgmcp://cache/runs/6ba16cf87b7c43279d19d0ac59d695a0",
    "dto": {
      "success": true,
      "run_status": null,
      "requested_scope": "targets",
      "requested_targets": [
        ".pgmcp/temp/issue473-survey/issue.filled.md",
        ".pgmcp/temp/issue473-survey/issue.minimal.md",
        ".pgmcp/temp/issue473-survey/pr.filled.md",
        ".pgmcp/temp/issue473-survey/pr.minimal.md"
      ],
      "selected_profile": null,
      "removed_targets": [],
      "results": [],
      "error_code": "selection_invalid",
      "error_details": {
        "issues": [
          {
            "reason": "selection_unsupported",
            "check_id": "markdown_body"
          }
        ]
      }
    }
  }
]
```

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp researcher | Compare the last four shipped families, nine exact legacy renders, thirteen current outputs, independent whitespace and explicit native/consumer limits. |
| 0.2 | 2026-10-03 | @imp researcher | Preserve initial receipts as historical; link installed native prerequisites, unchanged raw checks, isolated old Commit message views and eight passing contract tests. |
| 0.3 | 2026-10-03 | @imp researcher | Record approved TypeScript constructor spacing and link the approved generated-whitespace/caller-boundary criteria; retain raw evidence. |
