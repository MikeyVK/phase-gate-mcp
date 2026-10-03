<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Design Markdown v2/v3 Comparison

**Status:** RESEARCH DISCUSSION — objectives undecided  
**Version:** 0.2  
**Last updated:** 2026-10-02

## Purpose and scope

Investigate the user's observation that minimal Markdown lacks the familiar header and filled documents lack the version-history table. This is a Research comparison of illustrative Design artifacts, not the Design phase of issue #473. No template, schema, standard or runtime policy is changed.

The user authorized continued use of the located v2 renderer within branch `bug/473-first-call-template-quality` on 2026-10-02. The [Python comparison](python-class-comparison.md) records its source-selection limits. The same unmodified renderer and shipped template graph are used here; the missing issue460 checkout is not a blocker to this authorized comparison.

The initial [38-output survey](first-output-survey.md) remains intact. Its filled contexts are representative, not exhaustive. In particular, the filled Design input supplied status but omitted document version and date. This comparison adds a real public v3 scaffold with all three metadata fields to distinguish omitted input from ignored input.

## Files and comparable inputs

| Example | File | Input and limits |
| --- | --- | --- |
| Original v3 minimal | [design.minimal.md](../../../.pgmcp/temp/issue473-survey/design.minimal.md) | Required-only live context: title, problem statement and two requirement arrays |
| Original v3 filled | [design.filled.md](../../../.pgmcp/temp/issue473-survey/design.filled.md) | Representative body plus status; no version or last_updated was supplied |
| v2 with the current minimal nucleus | [design.v2-minimal-render.md](../../../.pgmcp/temp/issue473-comparison-02/design.v2-minimal-render.md) | Legacy raw render using the same authored nucleus and explicit probe metadata; not a claimed schema-valid minimal old public MCP call |
| v2 filled comparison | [design.v2-filled-render.md](../../../.pgmcp/temp/issue473-comparison-02/design.v2-filled-render.md) | Shared authored body and all three metadata values; legacy-specific framing |
| v3 filled with all metadata | [design.v3-filled-metadata.md](../../../.pgmcp/temp/issue473-comparison-02/design.v3-filled-metadata.md) | Original filled context plus version 0.1 and last_updated 2026-10-02, through public scaffold_artifact |

The two v2 outputs came from `TemplateEngine.render("concrete/design.md.jinja2", **context)`, explicitly imported from `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/services/template_engine.py`. The concrete Design source identifies itself as template version 3.5.0. That source version is part of the legacy v2 architecture; it is not the PGMCP product version or the authored document version.

Persistence used MCP only: create a scratch Design file through the current scaffold operation, then rewrite it with the exact legacy-render bytes using safe_edit_file and explicit Design validation. The bootstrap file is not legacy output evidence. The final hashes match the raw render strings. `comparison-only` in the legacy comment is a probe marker, not a computed historic provenance hash.

The v2 filled input deliberately uses only fields consumed by its old concrete renderer. New v3 contracts, validation obligations and risk records are retained in the current examples; they were not silently tunnelled into legacy fields. The examples therefore share relevant metadata/problem/requirements/options/decision content, not identical schemas or total body capability.

## Header and history findings

“Header” has three distinct meanings here: the H1 title, hidden provenance comment, and visible document metadata. Both architectures produce a title and a source comment. The observed absence in the v3 minimal file concerns the visible Status/Version/Last Updated block.

| Feature | v2 minimal nucleus | Original v3 minimal | Original v3 filled | New v3 filled with metadata |
| --- | --- | --- | --- | --- |
| H1 title | Present | Present | Present | Present |
| Hidden source provenance | Legacy probe marker | Real id/pv/pf/sf | Real id/pv/pf/sf | Real id/pv/pf/sf |
| Status | DRAFT default | Absent | Supplied value | Supplied value |
| Document version | 1.0 default | Absent | Absent, not supplied | 0.1, supplied |
| Last Updated | Derived from probe timestamp | Absent | Absent, not supplied | 2026-10-02, supplied |
| Version History heading/table | Automatically present | Absent | Absent | Absent |
| Author/change cells | Agent / Initial draft defaults | None | None | None |

The public live Design schema admits optional status, version and last_updated. [The shared Markdown base](../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2) renders each only when defined. The metadata-complete scaffold proves they are consumed. There is no dedicated history/versions/revisions field in the current resolved Design schema, and neither its concrete renderer nor shared document footer emits a version-history table.

The legacy [status-header pattern source](../../../../st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_status_header.jinja2) supplies defaults through the concrete Design call. The old history pattern is invoked unconditionally with one version/date pair. It produces an initial boilerplate row, not an accumulated revision log or inferred Git history.

A legacy inconsistency is reproduced: with last_updated omitted, the visible header derives 2026-10-02 from timestamp, but the history row has an empty Date cell. Concrete Design passes an empty string to the history macro; its default filter does not replace that empty string. The filled v2 example, which supplies last_updated, has matching dates.

Source-level header presentation also changed. V2 adds two trailing spaces after its first two metadata lines; v3 uses plain line feeds. Standard Markdown may render the latter as a single metadata paragraph rather than three explicit hard-break lines. No rendered UI screenshot is claimed here; desired visible header layout should be discussed and checked separately from presence of field text.

The package version `pv=1.0.0` in a v3 provenance comment is not the document version. The new sample legitimately contains both package pv 1.0.0 and document Version 0.1; neither substitutes for document history.

## Other visible Design differences

| Surface | v2 | v3 | Significance |
| --- | --- | --- | --- |
| Main structure | Numbered Context & Requirements / Design Options / Chosen Design | Semantic standalone headings, numbered individual alternatives | Presentation changed; no missing problem or requirement content in these inputs |
| Requirements | Unchecked checkboxes inserted by template | Bullets | Removes invented completion state for plain requirements |
| Constraints and related documentation when absent | None placeholders and section framing | Omitted | Explicit presence behavior changed |
| Empty option/decision/key-decision areas | Headings, blank decision/rationale and an empty decision table remain | Omitted when corresponding fields are absent | v3 permits a truthful initial nucleus before final choices exist |
| Pros/cons | Automatic check/cross symbols | Ordinary bullets | Editorial presentation difference |
| Maximum consecutive blank lines | 1 in both v2 examples | 20 minimal, 11 in both filled examples | Reproduced generated spacing issue, including terminal blank runs |
| Terminal newline | Neither captured v2 output ends with a newline | Current samples retain extra terminal blank lines | v2 is more compact here but is not a complete formatting reference |

Compact legacy output does not by itself make its defaults or phase claims correct. Conversely, keeping metadata caller-authored does not prevent offering a consistent visible document frame.

## Traceability to #460 and current standards

[Design document/tracking artifacts](../issue460/design-document-tracking-artifacts.md) records these relevant contracts:

| Source | Recorded direction | What this comparison establishes |
| --- | --- | --- |
| D-ART-DOC-06, line 67 | No invented status, evidence, checklist state, authors or version history | Explains removal of automatic defaults; does not prove every layout choice was separately approved |
| §7.1, lines 108–130 | Preserve optional caller-authored status/version/date; omit absent content; relax previous unconditional requiredness | Current metadata consumption and omission match this contract |
| §9, line 367 | Auto Agent/Initial draft history, timestamps/path headers and agent hints: approved removal/header replacement; no second history mechanism | Automatic history removal is explicitly recorded, rather than an accidental lost rendering branch |
| Introduction, lines 28–31 | Do not drop an existing capability merely because a concise table omitted it | A requested authored-history capability must be examined on its own merits |
| Legacy concrete history call | Basic single-row macro receives version/date; fixed Agent/Initial draft | This evidence does not show a previously exposed caller-authored multi-revision list in Design |

The primary [Research decision register](../issue460/research.md#approved-strategy-and-decision-status) owns binding boundary decisions. The lines above are recorded Design direction and preservation policy; original human approval messages for these specific changes have not been independently retrieved. They must not be substituted with the user's present approval of the renderer source.

The older `docs/reference/templates/BASE_TEMPLATE.md` in that legacy checkout labels both the status/version/date header and Version History as required. Its Design reference inherits that framing. These old references explain the user's expectation; the current repository no longer contains those files at that path.

The current [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) requires traceable evidence, readable presentation, distinct facts/questions/decisions and phase ownership. It does not expressly mandate a status/version/date block or version-history table for every scaffold. It does itself have such a header and history, which is evidence of a familiar convention, not a universal requirement inferred from one example.

[Code Style](../../coding_standards/CODE_STYLE.md) is principally Python guidance and does not define the Design document footer. Provenance source-header replacement is separate from visible authored document metadata and revision history.

The desired policy remains open: restoring a useful document frame, making metadata an expected caller input for governed documents, and supporting explicit truthful revision entries are different options from deriving workflow status, author, date or history automatically. Research should not silently reverse the #460 boundary to achieve a familiar layout.

## Verification and limitations

All three newly persisted samples passed the configured Design Markdown preflight. Offline native link review passed over all five comparison files; this is structural/link evidence, not editorial certification or workflow approval. The two original v3 SHA-256 digests still match the survey inventory.

| Evidence | Cached run |
| --- | --- |
| Current complete Design schema | `00113803dddf44d981a4d4e35fc3f85b` |
| Exact v2 minimal-render persistence | `d5c4b0f41ad943cbb59b82d6ef1748e0` |
| Exact v2 filled-render persistence | `4bea7fa02b914d45ab2811849e579af6` |
| Current public metadata-complete Design scaffold | `998c7f1e085d45e5b6c442f4f6847e2a` |
| Native link check on the five examples | `3332ec17056444a38e1cd6affe453421` |

Complete structured receipts were read from cache with full pagination and length/hash verification.

| File | SHA-256 | Max blank run |
| --- | --- | ---: |
| design.minimal.md | `b66139975fa1547744aa97c1c99eab211b5889373bd969b379f92fc1db56d31c` | 20 |
| design.filled.md | `c2be4a7f91273d80019127f1c17a3a8cfa3eaee8220ec0a26ea47bc0ce6321ef` | 11 |
| design.v2-filled-render.md | `97f498469ee3052da76b58ddf1ad9adfc242da6ce4fb75e6f53afe273a52aa72` | 1 |
| design.v2-minimal-render.md | `2294dad6afca3a5d06999dacd9ab75678cacce6472d5a3901b5e0a2a3c78337c` | 1 |
| design.v3-filled-metadata.md | `50e85b76129b4a2a45aab9ae8d0bfc5cc666f413657475b0142713ce9bba85a0` | 11 |

Legacy source SHA-256:

- `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\services\template_engine.py`: `ea6024a1612795b07161b50a6416ad40259757229c7a3885ed891f085d0eb382`
- `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates\concrete\design.md.jinja2`: `104814d8b2b50c7807d02f9962cac24921b2ea523584fc57b82584b451feb1cb`
- `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates\tier3_pattern_markdown_status_header.jinja2`: `6ac4c14522b29c8f7166f4f241d46f1a12cb491e64e041b8c9f5e5de6c358680`
- `C:\temp\st3.worktrees\agents-bugfixget-project-plan-phase-8383c97a\mcp_server\scaffolding\templates\tier3_pattern_markdown_version_history.jinja2`: `82756769cd78a4ae6bd74330ef0c4c687b1d5d882b2657d229d60f5c2046305b`

## Rationale and decision-authority audit — 2026-10-02

The user asked for historical explanation, not new objectives. This audit distinguishes an explicit human rule, a delegated Design choice, implementation conformance, and an unresolved preservation rationale. No new strategy or goal is approved.

### Primary conversation evidence

The archived Codex chat **Design 460**, thread `01a041df-de97-79f3-9e83-32c30c56edb2`, was read through the relevant turns using the app's read_thread API. The dates below are UTC. Human statements are summarized in English; they are separate from agent explanations.

| Time and turn | Primary human evidence | Scope of the evidence |
| --- | --- | --- |
| 2026-09-11 07:25:03; `01a08f5b-09fe-7502-87ed-7ece51f2cb44` | For an optional template field: render supplied content, render an explicit empty container when admitted and supplied empty, omit completely when absent; avoid interventions obscuring that rule | Explicit human presence rule. It does not decide which individual document fields must be optional |
| 2026-09-11 10:09:32; `01a08ff1-a26f-74a0-8e70-65fae9e0919a` | Research identifies defects; correct existing behavior must remain. The user challenged incomplete proposals and invisible optionality | Explicit preservation and completeness requirement |
| 2026-09-11 10:18:06; `01a08ff9-7932-7750-be52-e2df13a8b2c1` | The user did not want to design every template/schema detail and asked where Design ends and Implementation begins | Context for delegating detailed Design; not approval of a specific header/history removal |
| 2026-09-11 10:26:39; `01a09001-4ade-7e82-9d02-423e9c458e43` | The user instructed the designer to work out W07/W08 from the proposal, with research/existing implementation leading and external independent QA checking completeness; no per-field human review | Explicit human delegation of detailed Design under preservation constraints |
| 2026-09-11 11:06:11; `01a09025-7cb8-73b2-9171-aed941869041` | The user supplied independent QA: no P0–P3 findings, GO for the two concrete template-contract designs at commit 8b19e0e6 | Evidence that this delegated Design was reviewed. No runtime tests were performed; not proof of a separate human preference for every rendering detail |

The agent response at 10:18 distinguished Design-owned public behavior/requiredness/removals from Implementation-owned exact schemas/macros. It expressly denied a free pass for Implementation to invent behavior. This supports identifying metadata optionality and automatic-history removal as Design choices rather than later implementation improvisation.

### Recorded rationale and its limits

[Design §7.1](../issue460/design-document-tracking-artifacts.md) deliberately makes document status/version/date optional authored content and relaxes old unconditional requiredness. Its stated reason is to avoid forcing invented lifecycle facts into an initial scaffold. D-ART-DOC-06 and §9 deliberately remove automatic Agent/Initial draft history and inferred dates/status/authors. The current schema and templates follow those written choices.

The rationale for avoiding manufactured workflow facts is coherent: scaffolding cannot confer approval; the render timestamp is not inherently a document's latest substantive revision; a fixed Agent/Initial draft row is not an actual accumulated change record. These are different concerns from consistently displaying metadata supplied by the caller.

The recorded rationale does **not logically require** omitting metadata from minimal documents. A package can require explicit metadata, or a governing phase can require it before completion, while the renderer remains ignorant of workflow authority. That was a possible policy alternative; the evidence retrieved does not show a focused comparison explaining why optionality was preferable to those alternatives.

Likewise, rejecting automatic history does **not inherently reject** rendering a caller-authored table. A passive renderer of explicit version/date/author/change records need not become a history engine. No separate human instruction rejecting all authored history-table support was found in the relevant conversation turns. This is a limit of the retrieved evidence, not proof that no such instruction ever existed.

### Preservation discrepancy requiring explanation

The [Research catalog](../issue460/template-suite-catalog.md), lines 172–173, marks both the Markdown status-header and version-history patterns **Retain and adapt — human-approved 2026-08-23**, with portable shared responsibility retained and contract/metadata adaptation required.

There is an important asymmetry:

- Header capability survives as optional supplied status/version/date. That is identifiable adaptation, with optionality chosen in delegated Design.
- The automatic history row is explicitly removed by Design. The current Design schema offers no dedicated revision record and the shared document footer offers no version-history macro/container.
- The old concrete Design path itself did not expose a public multi-revision list; it invoked the basic one-row macro. Therefore this audit does not invent a lost, previously admitted Design history input.
- The shared legacy pattern did provide table rendering. The path from retaining that portable responsibility to offering no dedicated current full-document history facility is not clearly reconciled in the catalog or Design rationale.

“Retain and adapt” does not promise identical source files, byte output or synthetic defaults. It also does not, by itself, explain removing the table responsibility altogether. This is an unresolved preservation explanation, not an independently adjudicated QA defect or proof of unauthorized behavior.

Document-version history must also stay separate from #460's rejection of provenance registries, package-history discovery and lifecycle engines. Those infrastructure exclusions cannot automatically be used as the rationale for excluding caller-owned Markdown revision content.

### Bounded attribution

| Observed behavior | Attribution supported by evidence | What is not established |
| --- | --- | --- |
| Omit an absent field already declared optional | Explicit human general rule plus template conformance | The general rule does not authorize making every particular field optional |
| Make document metadata optional instead of mandatory | Explicit choice in delegated, independently reviewed Design | Separate human per-field preference or a complete trade-off analysis |
| Remove automatic DRAFT/version/date/Agent history filling | Recorded Design choice, consistent with caller-content ownership; implemented accordingly | A direct specific human instruction covering each default |
| No dedicated table for explicitly authored revision entries | Present in the delivered contract; automatic-history removal recorded | Clear reconciliation with the Research pattern-retention row or a specific human rejection of authored table support |
| Excess generated blank lines | Observed implementation/source-composition consequence; later deferred first-output quality issue | A deliberate approved editorial preference for those blank runs |
| Header hard-break markup, section numbering, empty import/section headings | Source-visible presentation choices | Separate human approval of every incidental layout change |

For the two concerns investigated here, the central policies existed in Design before implementation. They were agent-authored choices under explicit human delegation, with independent review. That is materially different from a late implementer silently inventing the behavior, and also different from a direct human decision on each item.

No defensible percentage of all nineteen template changes can be computed from this bounded audit. The evidence does establish where rationale is explicit and where preservation reasoning is incomplete. The current user discussion does not change any contract or convert these concerns into objectives.


## Discussion questions

- Should governed full documents consistently carry explicit document status, version and date, even when the generic scaffold permits a smaller nucleus?
- Should the visible metadata frame keep the familiar three-line presentation?
- Is a version-history table useful for every full document, or only when explicit revision content is available?
- If explicit history is desired, should the package admit caller-authored version/date/author/change records rather than generate Agent/Initial draft? The old concrete Design evidence here shows only an automatic basic row.
- Which numbered section/divider/table conventions materially aid comparison and review?
- How should the agreed document expectations be expressed consistently in schemas, templates, phase instructions and documentation without creating competing truths?

These are possible objectives, not Approved Strategy. No generic schema/template-consumption analyzer or #476 implementation is introduced.

## Exact legacy render contexts

### v2 with the current minimal nucleus

This raw-render input is not advertised as a valid old public Design payload; the old context schema additionally required choices that the current first-draft nucleus omits.

```json
{
  "artifact_type": "design",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T00:00:00Z",
  "format": "markdown",
  "output_path": "",
  "title": "Event Path Design",
  "problem_statement": "The consumer can acknowledge an event before its journal append is durable.",
  "requirements_functional": [
    "Acknowledge only after durable append."
  ],
  "requirements_nonfunctional": [
    "Preserve per-partition order."
  ]
}
```

### v2 filled comparison

```json
{
  "artifact_type": "design",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T00:00:00Z",
  "format": "markdown",
  "output_path": "",
  "title": "Event Path Design",
  "status": "DRAFT — review pending",
  "problem_statement": "The consumer can acknowledge an event before its journal append is durable.",
  "requirements_functional": [
    "Acknowledge only after durable append."
  ],
  "requirements_nonfunctional": [
    "Preserve per-partition order."
  ],
  "options": [
    {
      "name": "Append then acknowledge",
      "description": "Commit to the journal before replying.",
      "pros": [
        "Crash recovery has a durable source."
      ],
      "cons": [
        "Adds append latency."
      ]
    }
  ],
  "decision": "Append before acknowledgement.",
  "rationale": "The durability requirement determines the ordering.",
  "version": "0.1",
  "last_updated": "2026-10-02"
}
```

### v3 metadata-complete public input

```json
{
  "title": "Event Path Design",
  "status": "DRAFT — review pending",
  "problem_statement": "The consumer can acknowledge an event before its journal append is durable.",
  "requirements_functional": [
    "Acknowledge only after durable append."
  ],
  "requirements_nonfunctional": [
    "Preserve per-partition order."
  ],
  "options": [
    {
      "name": "Append then acknowledge",
      "description": "Commit to the journal before replying.",
      "pros": [
        "Crash recovery has a durable source."
      ],
      "cons": [
        "Adds append latency."
      ]
    }
  ],
  "decision": "Append before acknowledgement.",
  "rationale": "The durability requirement determines the ordering.",
  "contracts": [
    {
      "heading": "Append result",
      "content": "Returns an explicit durable position."
    }
  ],
  "validation": [
    {
      "obligation": "A failed append is not acknowledged",
      "method": "Inject journal failure",
      "expected_result": "The call fails and no acknowledgement is sent.",
      "references": [
        {
          "label": "Journal contract",
          "target": "../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"
        }
      ]
    }
  ],
  "risks": [
    {
      "description": "Append latency increases.",
      "mitigation": "Measure the journal path.",
      "consequence": "Higher tail latency."
    }
  ],
  "version": "0.1",
  "last_updated": "2026-10-02"
}
```

## Untouched output snapshots

The original v3 snapshots and contexts are already preserved in the first-output survey. New snapshots below preserve legacy output and the added v3 case because the actual example files live in scratch space.

### v2 minimal nucleus — exact renderer output

```markdown
<!-- template=design version=comparison-only -->
# Event Path Design

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-10-02

---

## 1. Context & Requirements

### 1.1. Problem Statement

The consumer can acknowledge an event before its journal append is durable.

### 1.2. Requirements

**Functional:**
- [ ] Acknowledge only after durable append.

**Non-Functional:**
- [ ] Preserve per-partition order.

### 1.3. Constraints

None
---

## 2. Design Options
---

## 3. Chosen Design

**Decision:** 

**Rationale:** 

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |
```

### v2 filled — exact renderer output

```markdown
<!-- template=design version=comparison-only -->
# Event Path Design

**Status:** DRAFT — review pending  
**Version:** 0.1  
**Last Updated:** 2026-10-02

---

## 1. Context & Requirements

### 1.1. Problem Statement

The consumer can acknowledge an event before its journal append is durable.

### 1.2. Requirements

**Functional:**
- [ ] Acknowledge only after durable append.

**Non-Functional:**
- [ ] Preserve per-partition order.

### 1.3. Constraints

None
---

## 2. Design Options

### 2.1. Option A: Append then acknowledge

Commit to the journal before replying.

**Pros:**
- ✅ Crash recovery has a durable source.

**Cons:**
- ❌ Adds append latency.
---

## 3. Chosen Design

**Decision:** Append before acknowledgement.

**Rationale:** The durability requirement determines the ordering.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-10-02 | Agent | Initial draft |
```

### v3 filled with all metadata — exact public scaffold output

```markdown
<!-- pgmcp:v1 id=design pv=1.0.0 pf=WCiT2npbapCBexKy sf=9PfER5JkyAoFQLRi -->

# Event Path Design

**Status:** DRAFT — review pending
**Version:** 0.1
**Last Updated:** 2026-10-02




## Problem Statement

The consumer can acknowledge an event before its journal append is durable.

## Functional Requirements

- Acknowledge only after durable append.

## Nonfunctional Requirements

- Preserve per-partition order.



## Options


### 1. Append then acknowledge

Commit to the journal before replying.


**Pros:**

- Crash recovery has a durable source.



**Cons:**

- Adds append latency.





## Decision

Append before acknowledgement.



## Rationale

The durability requirement determines the ordering.







## Contracts


### Append result


Returns an explicit durable position.











## Validation


### A failed append is not acknowledged

**Method:** Inject journal failure

**Expected Result:** The call fails and no acknowledgement is sent.


**References:**

- [Journal contract](<../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md>)





## Risks


### Append latency increases.

Measure the journal path.


**Consequence:** Higher tail latency.








```
