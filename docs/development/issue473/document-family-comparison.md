<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Full-document Family Comparison

**Status:** RESEARCH DISCUSSION — selected presentation objectives approved  
**Version:** 0.4  
**Last Updated:** 2026-10-03

## Purpose and method

The user agreed to establish one concrete comparison before moving faster through similar concrete templates. [Python Class](python-class-comparison.md) established the code comparison; [Design](design-document-comparison.md) established the full-document comparison. This follow-up covers the six other full-document packages, using Design as the shared framing reference. It compares first output, preserved meaning, recorded #460 intent and presentation choices. It does not select fixes or expand the approved objectives automatically.

Shared behavior is assessed once; a family is reopened in detail when its own output or contract differs materially. Findings are classified as preserved capability, recorded intentional change, repair, presentation question or evidence limit. “Recorded” means supported by #460 Research/Design, not an individually verified human instruction for every field or layout.

The human-approved mandatory caller-authored metadata and revision-table objective is recorded in [Research](research.md#human-approved-document-framing-objective--2026-10-02). It applies to all seven full-document families. The human has subsequently approved the no-legacy clean-break strategy; exact context shape remains Design work. This comparison adds no blanket approval for the remaining possible objectives. After discussing Architecture and Generic Doc, the human approved the bounded presentation outcomes recorded below.

## Sources and evidence limits

The authorized legacy renderer is `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/services/template_engine.py`; its SHA-256 is `ea6024a1612795b07161b50a6416ad40259757229c7a3885ed891f085d0eb382`. It is explicitly imported without alteration and called through `TemplateEngine(template_root=selected_root).render(template, **legacy_context)`. Its Jinja environment uses trim_blocks=True, lstrip_blocks=True and keep_trailing_newline=True. Exploratory execution used Python with -B, wrote only JSON to stdout and did not edit the source trees.

Architecture, Generic Doc, Planning, Reference and Research use the original authorized root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/`. Registered legacy generic_doc maps to `concrete/generic.md.jinja2`.

That root has no Validation Report concrete template. Validation Report therefore uses the separately identified installed legacy root `C:/1Voudig/99_Programming/ST/.pgmcp/templates/` with the same authorized renderer. This source difference is explicit; the result is not proof of an identical historical issue460 snapshot or full public v2 MCP pipeline. The intended issue460-validation-baseline directory still contains only a name marker.

Each family has a minimal-nucleus and filled legacy render, compared with its two untouched public v3 outputs from [the original survey](first-output-survey.md). “Minimal-nucleus” means the current required body translated into old renderer fields, with explicit comparison metadata. It is not a claim that the input satisfies every old public schema requirement. The old Generic Doc configuration, for example, has primitive/structured field inconsistencies that a direct renderer call does not validate.

All legacy contexts explicitly supply status, document version, date, timestamp, artifact_type and comparison-only version_hash. Existing filled metadata is retained. Added metadata is authored probe content, not an inferred workflow state. New v3-only carriers are not passed silently as unused legacy fields.

The legacy raw strings were persisted through MCP: scaffold a current generic_doc evidence container, then safe_edit_file with the exact render and explicit Markdown validation in report mode. All twelve final files match the raw strings by SHA-256. All twelve rewrites passed Markdown structural preflight. Bootstrap templates are not evidence of old output. Neither structural preflight nor matching bytes certifies editorial quality or link resolution.

## Concrete artifacts

| Family | v2 minimal nucleus | v2 filled | Original v3 minimal | Original v3 filled |
| --- | --- | --- | --- | --- |
| architecture | [Old minimal](../../../.pgmcp/temp/issue473-comparison-03/architecture.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-03/architecture.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-survey/architecture.minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-survey/architecture.filled.md) |
| generic_doc | [Old minimal](../../../.pgmcp/temp/issue473-comparison-03/generic_doc.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-03/generic_doc.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-survey/generic_doc.minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-survey/generic_doc.filled.md) |
| planning | [Old minimal](../../../.pgmcp/temp/issue473-comparison-03/planning.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-03/planning.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-survey/planning.minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-survey/planning.filled.md) |
| reference | [Old minimal](../../../.pgmcp/temp/issue473-comparison-03/reference.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-03/reference.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-survey/reference.minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-survey/reference.filled.md) |
| research | [Old minimal](../../../.pgmcp/temp/issue473-comparison-03/research.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-03/research.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-survey/research.minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-survey/research.filled.md) |
| validation_report | [Old minimal](../../../.pgmcp/temp/issue473-comparison-03/validation_report.v2-minimal-render.md) | [Old filled](../../../.pgmcp/temp/issue473-comparison-03/validation_report.v2-filled-render.md) | [Current minimal](../../../.pgmcp/temp/issue473-survey/validation_report.minimal.md) | [Current filled](../../../.pgmcp/temp/issue473-survey/validation_report.filled.md) |

## Shared findings, assessed once

All seven current roots inherit [the shared Markdown document base](../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2). That establishes a common framing seam, not automatic correctness.

- Visible status/version/date are conditional on caller presence. Original filled Architecture and Generic Doc supply all three; Reference supplies only status; Research, Planning and Validation Report supply none. Missing text is not evidence that a supplied value was ignored.
- None of these current first outputs has a dedicated version-history table. Every old example has an automatic initial history row. The old row invents Agent/Initial draft; the newly approved objective requires explicit authored revision facts instead. Its rationale and historical approval audit remain in the Design comparison.
- Current templates emit large runs of blank lines around optional blocks. The old sources also have smaller whitespace defects and sometimes empty sections. Old output is a comparison reference, not a normative formatting standard.
- Old workflow hints in comments do not survive as output instructions. #460 explicitly removed template-owned workflow guidance. Required workflow evidence and approval still belong to the active phase contract.
- Minimal scaffolding and a completed phase document have different content obligations. A required empty API list or a title-only validation context must not fabricate completion evidence.

Maximum consecutive blank or whitespace-only lines, measured on the exact persisted text:

| Family | v2 minimal | v2 filled | v3 minimal | v3 filled |
| --- | --- | --- | --- | --- |
| architecture | 2 | 2 | 8 | 5 |
| generic_doc | 5 | 2 | 8 | 7 |
| planning | 2 | 2 | 10 | 13 |
| reference | 2 | 2 | 5 | 6 |
| research | 1 | 2 | 14 | 5 |
| validation_report | 2 | 2 | 21 | 8 |

The complete file hashes below preserve the comparison without repairing either output. The later human reply on 2026-10-03 selected independent whitespace assessment as an objective beyond the approved framing; numerical spacing criteria remain open.

## Family-specific comparison

### Architecture

Concept names/descriptions, their Mermaid diagrams and subsections, and decisions with rationale/alternatives remain available. V2 numbers a concept as H2 and a subsection as 1.1; v3 adds a Concepts parent, makes concepts H3, adds Diagram and Subsections labels, and removes the visible subsection number. The old decisions table becomes individual decision headings with alternatives as bullets. The filled artifacts demonstrate these presentation changes.

V3 separately renders the supplied constraint “Never acknowledge before durable append.” V2's Constraints & Decisions section renders decisions only and does not emit that constraint; this is a recorded repair, not lost capability. V3 also has explicit source links absent from this old renderer.

#460 [Design §7.4 and §9](../issue460/design-document-tracking-artifacts.md) requires preserved concept ordering, diagram/subsection relationships and decision content, plus explicit constraint rendering. It does not separately justify the exact new labels, removal of subsection numbering or table-to-heading choice. These are presentation discussion points; no extra semantic content loss was established by the sample.

Primary current sources: [template](../../../.pgmcp/template_suite/architecture/template.jinja2), [schema](../../../.pgmcp/template_suite/architecture/context.schema.json).

### Research

Problem statement, goals, background, findings and questions remain. Research Goals becomes Goals; Open Questions becomes Questions. New evidence/consumers/risks/assumptions carriers appear in the filled v3 output; approved_strategy and expected_results are available but absent from that illustrative input.

The old template chooses references when nonempty, otherwise related_docs; the current template and shared footer can render both independently. This is a recorded repair in #460 Design §7.3 and §9. The current filled sample supplies references only, so that sample alone does not prove the combined-list path. Source inspection supplies the narrower capability evidence.

No additional lost semantic capacity was established here. The survey's authored sentence referring to “six Markdown templates” is a sample string and not a fresh factual claim about the seven-family inventory. Preserving a caller string does not certify its truth.

Primary current sources: [template](../../../.pgmcp/template_suite/research/template.jinja2), [schema](../../../.pgmcp/template_suite/research/context.schema.json).

### Planning

V2 has TDD Cycles with an automatic Cycle 1 label, goal, tests, success criteria and optional dependencies. V3 uses Work Units with explicit identity, goal, deliverables, exit criteria and optional verification/dependencies. Overall risks and milestones remain available. The richer filled current output also displays owner, validation specifications, risks, stop conditions and phase deliverables.

This is recorded intentional contract evolution: cycles → work_units, tests → verification, success_criteria → exit_criteria; no universal TDD heading, inferred operational cycle identity, scalar/list dual read or automatic scheduling. #460 Design §7.5 and §9 explicitly preserve the operational meaning and separate narrative fields from operational payloads.

The old example translates only common meaning: each verification method becomes a tests item and exit_criteria becomes success_criteria. Deliverable records, ownership, verification obligations/results, work-unit risks, stop conditions and phase deliverables have no corresponding render slot in that old example; their absence is not a v3 regression. No extra family-specific lost capacity was established.

Primary current sources: [template](../../../.pgmcp/template_suite/planning/template.jinja2), [schema](../../../.pgmcp/template_suite/planning/context.schema.json).

### Reference

Component grouping, signatures, parameter/return descriptions and usage examples remain; current records add method descriptions, errors and component/method source links. Source_file becomes a required nonempty sources list. A formerly mandatory single test_file becomes optional repeatable test_evidence. Test_count is removed. Each usage example explicitly names its language, replacing the old hardcoded Python fence. These are recorded choices in #460 Design §7.4 and §9.

The old renderer emits [source] and [tests] reference-style links without defining either identifier in these raw outputs. Current source/test/API links are complete. This supports the recorded link repair; passing structural preflight on the old output does not contradict the unresolved references.

The minimal current API Reference heading is empty because the required list explicitly allows an empty first scaffold. That is recorded §7.3 behavior, not disappeared API capacity. Whether a completed reference document should require test evidence is a possible separate content discussion, not a newly approved objective.

Primary current sources: [template](../../../.pgmcp/template_suite/reference/template.jinja2), [schema](../../../.pgmcp/template_suite/reference/context.schema.json), [link pattern](../../../.pgmcp/template_suite/shared/templates/patterns/markdown/links.jinja2).

### Generic Doc

Purpose/summary, change list, migration steps, validation checklist, FAQ and custom section capacities remain. Custom_sections is renamed sections in the documented clean break; checklist records now preserve explicitly supplied checked state, whereas this old renderer always emits unchecked string items.

A clear presentation change appears in the filled examples: v2 directly emits an H2 Evidence section containing its prose; v3 wraps it in H2 Sections, makes Evidence H3 and adds Content:. The current template also adds Bullets: and Checklist: when those carriers are supplied. #460 Design §9 requires retention of those capacities but gives no separate rationale for the mechanical wrapper/labels. Their necessity remains a discussion point.

The empty migration_steps list is omitted by v2 and produces an empty Migration Steps heading in v3. This follows the explicitly approved #460 absent-versus-supplied-empty rule. It must not be treated as the same class of accidental blank-line defect. The v2 minimal example itself contains five consecutive blank lines, so its output is not a spotless layout baseline.

The filled related_docs target points to a nonexistent template-suite README in both translated and current examples. That target is caller-authored and remains the original survey's input error, not a generated link-target defect.

Primary current sources: [template](../../../.pgmcp/template_suite/generic_doc/template.jinja2), [schema](../../../.pgmcp/template_suite/generic_doc/context.schema.json).

### Validation Report

The alternate old source presents issue/cycle/outcome in the metadata, a Scope body and an Outcome body. With the minimal nucleus it invents “Validation scope to be documented.” and “Validation outcome pending.” The filled version displays the supplied PARTIAL status.

V3 preserves caller-supplied issue/cycle/outcome/scope and adds obligations, evidence and separate demonstration/preservation/containment/failures/caveats/risks/deferred-work carriers. The filled sample demonstrates obligations and evidence; the explicitly supplied empty failures array produces a heading, while omitted carriers stay absent. Status and observation text remain illustrative producer content, not an independent QA verdict.

Removal of invented scope, explicit producer evidence indexing and no automatic status-to-workflow authority are recorded in #460 Design §7.3, §9 and DOC-E07. The current minimal title-only document has a measured 21-line blank run. This shows the general spacing problem; the already approved required framing objective will additionally change its admitted minimal input.

No family-specific lost capacity was established against this alternate installed source. Historical source parity is weaker here than for the other five templates.

Primary current sources: [template](../../../.pgmcp/template_suite/validation_report/template.jinja2), [schema](../../../.pgmcp/template_suite/validation_report/context.schema.json).

## Standards and remaining discussion

[Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) governs readable evidence, phase ownership and distinction between facts, questions and decisions. It does not independently establish the same universal mandatory history/header rule as old BASE_TEMPLATE references. The chosen mandatory framing objective is now explicit human input. [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md) governs DRY and the generic rendering boundary; shared document policy should have one owner. [Code Style](../../coding_standards/CODE_STYLE.md) remains relevant to code/fenced examples but does not choose an Architecture decisions table or a Generic Doc wrapper.

The existing standards inconsistencies and broken links remain separately evidenced in the Design/Python comparisons and Research. Neither standards nor templates were changed in this pass.

The largest distinct presentation discussion points were Architecture's navigation/decision display and Generic Doc's wrapper/carrier labels; the human subsequently approved the bounded outcomes below. Planning and Reference mostly demonstrate explicit contract evolution; Research and Validation Report demonstrate preservation/extension and removal of misleading defaults. Lack of per-layout rationale is not proof of unauthorized behavior. No producer or delegated source reviewer issued independent QA GO.

This evidence does not exhaust every optional/schema combination. In particular, combined Research link lists, Architecture with multiple concepts/subsections, non-Python Reference examples and all three Generic Doc section carriers need targeted cases if their behavior becomes a selected objective. Existing source/test contracts provide capacity evidence without pretending these rendered samples exercise those cases.

The next comparison can reuse the common findings and reopen only material family differences. The remaining affected-boundary strategy decisions must still be approved before Research closes.

## Human-qualified whitespace decision — 2026-10-03

The human explicitly included the document batch in the independent whitespace assessment. [Eight targeted untouched probes](whitespace-comparison.md) distinguish generated joins, omitted/empty carriers, EOF and caller-owned internal spacing. All four Markdown preflights passed despite generated blank runs, while authored prose, code-fence spacing and a two-space hard break remained exact.

[Research](research.md#human-approved-python-quality-and-independent-whitespace-objective--2026-10-03) records the authoritative approval boundary. Numerical generated-join limits, exact EOF criteria and runtime enforcement remain discussion choices. Existing comparison evidence stays unchanged; no caller-content normalization or production fix follows from this decision.

## Human-approved presentation objectives — 2026-10-02

The user explicitly answered “Ja” to the proposal following the concrete Architecture/Generic Doc comparison. The approval concerns desired presentation, not approval of implementation or the complete Research strategy.

| Family | Approved outcome |
| --- | --- |
| Architecture | Keep the meaningful Concepts grouping and separate constraint rendering; restore hierarchical subsection numbering; omit redundant Diagram/Subsections labels; prefer a table for concise decisions while fully preserving readable long or structured rationale/alternatives. |
| Generic Doc | Render supplied sections directly at document-section level; omit the generated Sections wrapper and Content/Bullets/Checklist carrier labels; retain all supplied content, order and checked state. |

Meaningful distinctions such as sources, evidence and alternatives are preserved. This is no blanket removal of headings/labels, no requirement to force arbitrary prose into tables and no authorization to transform or truncate authored content.

The user subsequently stated “Ja, ik wil geen compat legacy.” [Research records the approved clean break](research.md#approved-strategy-clean-break-no-legacy-compatibility--2026-10-02): new presentation and required document contexts only, no legacy output mode, parallel schema, aliases or fabricated defaults. Existing documents remain ordinary files; demonstrably affected active callers, fixtures and references migrate to the new contract. Heading text/numbering can change fragments; heading level alone need not. Shared pattern ownership remains DRY; exact macro/schema layout, handling of complex table content and implementation sequence belong to Design. The raw examples and hashes below remain unchanged evidence of the old and current behavior.


## Exact legacy inputs and reproducibility

The original v3 minimal/filled contexts and native receipts remain in the survey. This section supplies every translated legacy context. Links become old scalar targets; checklist records become old item text; section and cycle names are explicitly translated. New-only carriers are excluded as described above. Added metadata is probe content.

### architecture — minimal

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/architecture.md.jinja2`.

```json
{
  "title": "Execution Architecture",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "architecture",
  "version_hash": "comparison-only",
  "concepts": [
    {
      "name": "Event stream",
      "description": "Events move from intake to persistence."
    }
  ],
  "decisions": []
}
```

### architecture — filled

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/architecture.md.jinja2`.

```json
{
  "title": "Execution Architecture",
  "status": "DRAFT — review pending",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "architecture",
  "version_hash": "comparison-only",
  "purpose": "Describe the order-preserving event path.",
  "related_docs": [
    "../../../docs/coding_standards/DOCUMENTATION_STANDARD.md"
  ],
  "concepts": [
    {
      "name": "Event stream",
      "description": "Events move from intake to persistence.",
      "diagram": "flowchart LR\n  Intake --> Journal\n  Journal --> Store",
      "subsections": [
        {
          "name": "Ordering",
          "description": "Each partition preserves append order."
        }
      ]
    }
  ],
  "decisions": [
    {
      "decision": "Use a durable journal",
      "rationale": "Recovery needs an authoritative append order.",
      "alternatives": "In-memory queue"
    }
  ]
}
```

### generic_doc — minimal

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/generic.md.jinja2`.

```json
{
  "title": "Template Output Review",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "generic_doc",
  "version_hash": "comparison-only",
  "purpose": "Record first-call output observations.",
  "summary": "Review representative generated artifacts for formatting and presentation."
}
```

### generic_doc — filled

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/generic.md.jinja2`.

```json
{
  "title": "Template Output Review",
  "status": "Research",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "generic_doc",
  "version_hash": "comparison-only",
  "purpose": "Record observations from representative first-call rendering.",
  "scope_in": "Six shipped concrete template packages.",
  "scope_out": "Template implementation choices.",
  "prerequisites": [
    "Use contexts valid against each package schema."
  ],
  "summary": "Generated formatting and Markdown presentation are assessed separately from caller-owned values.",
  "key_changes": [
    "Compare minimal and populated output.",
    "Record defects by ownership boundary."
  ],
  "migration_steps": [],
  "related_docs": [
    "../../../.pgmcp/template_suite/README.md"
  ],
  "validation_checklist": [
    "Check output using representative contexts."
  ],
  "faq": [
    {
      "question": "Does a valid context guarantee polished output?",
      "answer": "That guarantee remains a research decision."
    }
  ],
  "custom_sections": [
    {
      "heading": "Evidence",
      "content": "Compare generated structure with the supplied values."
    }
  ]
}
```

### planning — minimal

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/planning.md.jinja2`.

```json
{
  "title": "Event Path Plan",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "planning",
  "version_hash": "comparison-only",
  "summary": "Make acknowledgement follow a durable append.",
  "tdd_cycles": [
    {
      "name": "Append ordering",
      "goal": "Enforce durable append before acknowledgement.",
      "tests": [],
      "success_criteria": "Failure injection proves no early acknowledgement."
    }
  ]
}
```

### planning — filled

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/planning.md.jinja2`.

```json
{
  "title": "Event Path Plan",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "planning",
  "version_hash": "comparison-only",
  "summary": "Make acknowledgement follow a durable append.",
  "dependencies": [
    "Approved interface contract"
  ],
  "tdd_cycles": [
    {
      "name": "Append ordering",
      "goal": "Enforce durable append before acknowledgement.",
      "tests": [
        "Run focused failure-path test"
      ],
      "success_criteria": "Failure injection proves no early acknowledgement."
    }
  ]
}
```

### reference — minimal

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/reference.md.jinja2`.

```json
{
  "title": "Event API",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "reference",
  "version_hash": "comparison-only",
  "source_file": "../../../README.md",
  "test_file": "",
  "api_reference": []
}
```

### reference — filled

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/reference.md.jinja2`.

```json
{
  "title": "Event API",
  "status": "DRAFT — review pending",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "reference",
  "version_hash": "comparison-only",
  "source_file": "../../../README.md",
  "test_file": "../../../tests/mcp_server/integration/templates/test_reference.py",
  "api_reference": [
    {
      "name": "EventReader",
      "description": "Reads events in partition order.",
      "methods": [
        {
          "signature": "read(partition: str)",
          "params": "partition identifier",
          "returns": "Event | None"
        }
      ]
    }
  ],
  "usage_examples": [
    {
      "description": "Python reader use",
      "code": "event = reader.read(partition)"
    }
  ]
}
```

### research — minimal

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/research.md.jinja2`.

```json
{
  "title": "First-call template quality research",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "research",
  "version_hash": "comparison-only",
  "goals": [
    "Locate generated presentation defects."
  ],
  "problem_statement": "Some shipped templates produce first outputs with formatting defects."
}
```

### research — filled

Source root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/research.md.jinja2`.

```json
{
  "title": "First-call template quality research",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "research",
  "version_hash": "comparison-only",
  "background": "Issue 473 reports excess Markdown spacing and mechanical labels.",
  "findings": "The six Markdown templates extend the same document base and section/link macros.",
  "questions": [
    "Which boundaries need an explicit compatibility decision?"
  ],
  "goals": [
    "Locate generated presentation defects.",
    "Separate template text from caller-authored strings."
  ],
  "problem_statement": "Some shipped templates produce first outputs with formatting defects.",
  "risks": [
    {
      "description": "A template defect can be misattributed to a user string.",
      "mitigation": "Use marker strings and compare the raw template path.",
      "consequence": "A fix could alter valid authored content."
    }
  ],
  "references": [
    "../../../docs/coding_standards/DOCUMENTATION_STANDARD.md"
  ]
}
```

### validation_report — minimal

Source root: `C:/1Voudig/99_Programming/ST/.pgmcp/templates`; template: `concrete/validation_report.md.jinja2`.

```json
{
  "title": "Event path validation",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "validation_report",
  "version_hash": "comparison-only"
}
```

### validation_report — filled

Source root: `C:/1Voudig/99_Programming/ST/.pgmcp/templates`; template: `concrete/validation_report.md.jinja2`.

```json
{
  "title": "Event path validation",
  "status": "DRAFT — comparison sample",
  "version": "1.0",
  "last_updated": "2026-10-02",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "markdown",
  "output_path": "",
  "artifact_type": "validation_report",
  "version_hash": "comparison-only",
  "issue_number": 473,
  "cycle": "C1",
  "validation_status": "PARTIAL",
  "scope": "Durable append ordering."
}
```

## Source identities

The source manifest hashes the authorized roots' Jinja files so the selected graphs can be identified independently of their mutable locations. It does not assert that the alternate installed root belongs to the same historical checkout.

```json
[
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/architecture.md.jinja2",
    "sha256": "601fe538e07bdb88b014ef9fa5f39dbc8c3e6ce0ec187eb9209e3529071247af"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/commit.txt.jinja2",
    "sha256": "4ab0569f7a8b45d96005f4af57cd1eac8bd32d26026dddfd33cc5fedbb4cb75c"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/config_schema.py.jinja2",
    "sha256": "d6b8025522cd44824c4d373f1eed6b1cc9c1f8dab94de620af93de3948f9b911"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/design.md.jinja2",
    "sha256": "104814d8b2b50c7807d02f9962cac24921b2ea523584fc57b82584b451feb1cb"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/dto.py.jinja2",
    "sha256": "8745373f84582dbe1cde01faf109f563b3115e73b8b334120d15f821c2f2b5f8"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/dto_v2.py.jinja2",
    "sha256": "07d3e0f6f88b6e0eb77162116dc0259e3dc1a9876a356de4bd91e57d366db1c1"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/generic.md.jinja2",
    "sha256": "d6c24c160fb934716de46c824c49f9cb59973e96f00c1f037757262f71c8bd8b"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/generic.py.jinja2",
    "sha256": "88438500e84ddd1c0b10eb9f2174508997a97fabed64f09ce3143feeb10666b4"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/issue.md.jinja2",
    "sha256": "08dba71a7c14ba945883cc30201ea8ed35b4f471616830a1eee5f7e2d825a6b6"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/planning.md.jinja2",
    "sha256": "48ffa3ade270188142bb91cc89f8ef168c8268efeebbba252cf1899c6581a2d3"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/pr.md.jinja2",
    "sha256": "0ee118f763fa9998580b221d856e28ba9e82e69e2b37272e86e573fc6bab4f59"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/reference.md.jinja2",
    "sha256": "2ba7c61facfa0808db563892e7eb8e9130d56fd2021c745d016a1e86c1287467"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/research.md.jinja2",
    "sha256": "41731bba06409d7e2316338aef4f905e11255c9f10233cb336f6252b9139e4a6"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/service_command.py.jinja2",
    "sha256": "0c4f6735c37f2b169002bac1612cd4818b5e32ece1a611359320d7e0dbf3ed5f"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/test_integration.py.jinja2",
    "sha256": "e6d4c37b8cc5361a39d891da70bc100627aff6c6561c942e2810a43d08bc3f47"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/test_unit.py.jinja2",
    "sha256": "bea94ac07eabc0eb4be49effad832dc567b3947bb51616e4f3953fd7eb7b0adb"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/tool.py.jinja2",
    "sha256": "518d0fea58cc865a8eb90d4b0c596ab699f41f28debc46d7b71d41a7d1c17116"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/worker.py.jinja2",
    "sha256": "9a25c23fd71ec931a85cec6eb563925c8db6d1a0d23ada24c724d92b72cde1d0"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier0_base_artifact.jinja2",
    "sha256": "07c1ebf7df1accfe88cdfcd28fbaa07d4182c099411e344b68fd2c43d0576875"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_code.jinja2",
    "sha256": "b7cc8a03c49c613241947e0825eea96f3e7b8ccbcaae849888c5c36d054d1187"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_config.jinja2",
    "sha256": "b624150db5499f7c37cc8f60e82ab1d9ab45685b5f3fe89f9306eb0db8c8bc21"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_document.jinja2",
    "sha256": "53638c9c61478a747b969a4e2444de01e276f569fc4a20cbdd7f790a27da3ce1"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_tracking.jinja2",
    "sha256": "92b133451d44b1e9ae469dff9a585f43136df06bead19be552c7f1243b7b7d7f"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_base_markdown.jinja2",
    "sha256": "1b659bbbb5cae1dab79d8b1d941c5d6a4dfb7d9f1fcde9a254e852893b6f2e71"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_base_python.jinja2",
    "sha256": "29361d5d8df6c5d6b8a8fe26640e38e508e8fe8dec44e57b87fd0653329d12f7"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_base_yaml.jinja2",
    "sha256": "5cd78e1f28c5985fbbb007cc8c54fb47ab7d0d99353d0155f5a04906811cf87f"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_tracking_markdown.jinja2",
    "sha256": "b52303ca7db85aaba2f674ea849f578220b8b20eaa33a3f9240f614a48874785"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_tracking_text.jinja2",
    "sha256": "68ecef4a411e2b1916dbc9a30a3424feae9a8a9b7c9497f39490f5e96b13203b"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_agent_hints.jinja2",
    "sha256": "129a5a31c94133b1f0adf0322361cfa1a84a1fd4a22e6b157f87ecc2e3c6aa97"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_dividers.jinja2",
    "sha256": "bc1bd14e2e56fc38316ba64cee66a7fb70bca85102c6e8efcce315759492bfd9"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_open_questions.jinja2",
    "sha256": "bc69c4a5413f345fb999b277cd980c0c31b14c350911970c4cde09dd6243c3ab"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_prerequisites.jinja2",
    "sha256": "c6ee64d0153a1745bda512d6a615859346c1aeabea3c02b6ca5b54b570f1883c"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_purpose_scope.jinja2",
    "sha256": "69d1b5b3c87e611bf2cf049f50619a8b24518fea7e0b5cbc1b158e266f211f31"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_related_docs.jinja2",
    "sha256": "013f89bb7a3347ae7a157e0203e2356d0073c7ec44ad978b3f776c5ec8fa8af0"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_status_header.jinja2",
    "sha256": "6ac4c14522b29c8f7166f4f241d46f1a12cb491e64e041b8c9f5e5de6c358680"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_markdown_version_history.jinja2",
    "sha256": "82756769cd78a4ae6bd74330ef0c4c687b1d5d882b2657d229d60f5c2046305b"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_assertions.jinja2",
    "sha256": "895e2b84e95be995d2684f92e766198a82321cb9d52bb924150da4f482ed70bb"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_async.jinja2",
    "sha256": "bc35f50608a26f2d747a98ea6408d4597c3a3a3fc5b9f79c1163120da3266be1"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_di.jinja2",
    "sha256": "709e7790699a67992ae440a373c65ce9865706473c2841ea95d12934401fbc14"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_error.jinja2",
    "sha256": "71dd907b38e11d5e6b465e438e304b4b361c4f70a999953fe7aed1b85a9604a7"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_lifecycle.jinja2",
    "sha256": "1db45bc3f319aefa3bb77bc49afd1934fcf69735d623ff169cabdcd42f30a981"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_log_enricher.jinja2",
    "sha256": "c9c8af8135d67fb035603386c53f2bebc936443ca4be4ffedcbaa5132ba543f1"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_logging.jinja2",
    "sha256": "efd77d62436d84a17f4cf8bb6d7c0bfe3d95fa64f12767fa162d165df8ff7c0e"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_mocking.jinja2",
    "sha256": "f9a099f78864bb5742f0e014ad7631d5a1f2686d9844e84b70365f02a04da534"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_pydantic.jinja2",
    "sha256": "8845488b0b1f57d6df0ed648466deec21a4a70380b6eeba78da664574661b205"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_pytest.jinja2",
    "sha256": "802f940d4aa0a48245a0bc27880589bb63532306b4432f14d2d55a04774dbd5d"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_test_fixtures.jinja2",
    "sha256": "10f8274ccdaccb335fd8c56a5bc7a494aed27ff87a23ec623bd9b61ac453abab"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_test_structure.jinja2",
    "sha256": "4e2f99d909e752678433cdd8f8d1ee41662edd7c2303a9d4f2b9aef15748c52a"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_translator.jinja2",
    "sha256": "d240e058ae16545c3e0d2cfa246b9f9b16856cc2121d9cf8ca3a628f8327e722"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_typed_id.jinja2",
    "sha256": "af9e67f6238f3acf0e01bcaf523f854248d947f555432bf70ec9c9ec31571299"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/adapter.py.jinja2",
    "sha256": "d3f53a6c0fc875ab96942657406840b8e1bcf76aec73407fc68a7ab9b38c559e"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/architecture.md.jinja2",
    "sha256": "97f9cdd7d59ee1a2aa60da82907809b4c98f13e29134bac6823cb8aeba1409e5"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/commit.txt.jinja2",
    "sha256": "4ab0569f7a8b45d96005f4af57cd1eac8bd32d26026dddfd33cc5fedbb4cb75c"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/config_schema.py.jinja2",
    "sha256": "d6b8025522cd44824c4d373f1eed6b1cc9c1f8dab94de620af93de3948f9b911"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/design.md.jinja2",
    "sha256": "2c1e229a9422b94d15bf3679657edadc4a75d5087dae2959e2ad778b2740c65e"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/dto.py.jinja2",
    "sha256": "8745373f84582dbe1cde01faf109f563b3115e73b8b334120d15f821c2f2b5f8"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/dto_v2.py.jinja2",
    "sha256": "07d3e0f6f88b6e0eb77162116dc0259e3dc1a9876a356de4bd91e57d366db1c1"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/generic.md.jinja2",
    "sha256": "7f161b975224c92ed66e3d2876ca3e49359e745898cb3a44356d22252fd39277"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/generic.py.jinja2",
    "sha256": "88438500e84ddd1c0b10eb9f2174508997a97fabed64f09ce3143feeb10666b4"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/interface.py.jinja2",
    "sha256": "93d1c6401ec9297dc370152d71ec2680d1c205c30c4027416ec1b07e317a0620"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/issue.md.jinja2",
    "sha256": "a34c27b776b1f38d1318ae2e1eb58e91816fe1224add9fb3f46c2a25f7208aa8"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/planning.md.jinja2",
    "sha256": "26036aa6d6c4c5a4748e8dcac58b1874c07123d4b54f6758a0491da90b349b84"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/pr.md.jinja2",
    "sha256": "150112534aa9351bcd2b119781035bf186ce4ed236d930fb008e57488303941d"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/reference.md.jinja2",
    "sha256": "c5f4545f11691fa39b77f1d5890f70a8da67a21ce66dd13d77de22b221ff3d99"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/research.md.jinja2",
    "sha256": "792302751c3da8a976e526373a731989a2e36bc06cf76e3860018dfc10beb6d1"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/resource.py.jinja2",
    "sha256": "d4856795fe7686f335eec71f4c21c0ba36913241e762fcd0993593bf8fff81a4"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/service_command.py.jinja2",
    "sha256": "0c4f6735c37f2b169002bac1612cd4818b5e32ece1a611359320d7e0dbf3ed5f"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/test_integration.py.jinja2",
    "sha256": "8450645418945fcfa04a87ae805a088986de99f25e255b38c5dd6ff544c1c06f"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/test_unit.py.jinja2",
    "sha256": "43fd5a7105d6c66956b68f7f59ecaf7d1956f1fba9e926ea9e42fd56fac10bdd"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/tool.py.jinja2",
    "sha256": "518d0fea58cc865a8eb90d4b0c596ab699f41f28debc46d7b71d41a7d1c17116"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/typescript_dto.ts.jinja2",
    "sha256": "d6305f5e22681286ab72d5a44137f4cc5491496b4a4f9cd63468d091b7a2cde9"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/validation_report.md.jinja2",
    "sha256": "2fd309a9fc0dc513b287bc10acc28d383b26e95df95df392ec4f65e11d775041"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/worker.py.jinja2",
    "sha256": "9a25c23fd71ec931a85cec6eb563925c8db6d1a0d23ada24c724d92b72cde1d0"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier0_base_artifact.jinja2",
    "sha256": "8b531031e82c7315ce95deebe1e88e12e46aaffb86a5707bafba5869443d4b18"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_code.jinja2",
    "sha256": "b7cc8a03c49c613241947e0825eea96f3e7b8ccbcaae849888c5c36d054d1187"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_config.jinja2",
    "sha256": "b624150db5499f7c37cc8f60e82ab1d9ab45685b5f3fe89f9306eb0db8c8bc21"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_document.jinja2",
    "sha256": "c8005bc960f83bc1f0a5b132b83e80afb6ff9a09ef26b0bef664ef50f69c6042"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_tracking.jinja2",
    "sha256": "92b133451d44b1e9ae469dff9a585f43136df06bead19be552c7f1243b7b7d7f"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_markdown.jinja2",
    "sha256": "1b659bbbb5cae1dab79d8b1d941c5d6a4dfb7d9f1fcde9a254e852893b6f2e71"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_python.jinja2",
    "sha256": "29361d5d8df6c5d6b8a8fe26640e38e508e8fe8dec44e57b87fd0653329d12f7"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_typescript.jinja2",
    "sha256": "cd7afe9f3e57d832cad092eff62caf54ee32f9dd447630dbef2d3130c7498bfb"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_yaml.jinja2",
    "sha256": "5cd78e1f28c5985fbbb007cc8c54fb47ab7d0d99353d0155f5a04906811cf87f"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_tracking_markdown.jinja2",
    "sha256": "b52303ca7db85aaba2f674ea849f578220b8b20eaa33a3f9240f614a48874785"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_tracking_text.jinja2",
    "sha256": "68ecef4a411e2b1916dbc9a30a3424feae9a8a9b7c9497f39490f5e96b13203b"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_agent_hints.jinja2",
    "sha256": "129a5a31c94133b1f0adf0322361cfa1a84a1fd4a22e6b157f87ecc2e3c6aa97"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_dividers.jinja2",
    "sha256": "bc1bd14e2e56fc38316ba64cee66a7fb70bca85102c6e8efcce315759492bfd9"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_open_questions.jinja2",
    "sha256": "bc69c4a5413f345fb999b277cd980c0c31b14c350911970c4cde09dd6243c3ab"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_prerequisites.jinja2",
    "sha256": "c6ee64d0153a1745bda512d6a615859346c1aeabea3c02b6ca5b54b570f1883c"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_purpose_scope.jinja2",
    "sha256": "69d1b5b3c87e611bf2cf049f50619a8b24518fea7e0b5cbc1b158e266f211f31"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_related_docs.jinja2",
    "sha256": "013f89bb7a3347ae7a157e0203e2356d0073c7ec44ad978b3f776c5ec8fa8af0"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_status_header.jinja2",
    "sha256": "e6e9ada2eb4c44feeb0973e2b61cffb2470a65eb416500c50141dab556e98dca"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_markdown_version_history.jinja2",
    "sha256": "4d1b6b7a82723d5cf0b6ca96df21783f81cdf7885c71c76e8b2be40cf2a929d3"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_assertions.jinja2",
    "sha256": "895e2b84e95be995d2684f92e766198a82321cb9d52bb924150da4f482ed70bb"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_async.jinja2",
    "sha256": "bc35f50608a26f2d747a98ea6408d4597c3a3a3fc5b9f79c1163120da3266be1"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_di.jinja2",
    "sha256": "709e7790699a67992ae440a373c65ce9865706473c2841ea95d12934401fbc14"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_error.jinja2",
    "sha256": "71dd907b38e11d5e6b465e438e304b4b361c4f70a999953fe7aed1b85a9604a7"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_lifecycle.jinja2",
    "sha256": "1db45bc3f319aefa3bb77bc49afd1934fcf69735d623ff169cabdcd42f30a981"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_log_enricher.jinja2",
    "sha256": "c9c8af8135d67fb035603386c53f2bebc936443ca4be4ffedcbaa5132ba543f1"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_logging.jinja2",
    "sha256": "efd77d62436d84a17f4cf8bb6d7c0bfe3d95fa64f12767fa162d165df8ff7c0e"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_mocking.jinja2",
    "sha256": "f9a099f78864bb5742f0e014ad7631d5a1f2686d9844e84b70365f02a04da534"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_pydantic.jinja2",
    "sha256": "8845488b0b1f57d6df0ed648466deec21a4a70380b6eeba78da664574661b205"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_pytest.jinja2",
    "sha256": "802f940d4aa0a48245a0bc27880589bb63532306b4432f14d2d55a04774dbd5d"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_test_fixtures.jinja2",
    "sha256": "10f8274ccdaccb335fd8c56a5bc7a494aed27ff87a23ec623bd9b61ac453abab"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_test_structure.jinja2",
    "sha256": "4e2f99d909e752678433cdd8f8d1ee41662edd7c2303a9d4f2b9aef15748c52a"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_translator.jinja2",
    "sha256": "d240e058ae16545c3e0d2cfa246b9f9b16856cc2121d9cf8ca3a628f8327e722"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_typed_id.jinja2",
    "sha256": "af9e67f6238f3acf0e01bcaf523f854248d947f555432bf70ec9c9ec31571299"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_typescript_dto.jinja2",
    "sha256": "30cbcd5f4c62ab4b0b48fcf65eaf2d1f57a13eae822b2256ca7ba72da0418383"
  }
]
```

## File identities and native persistence receipts

All twelve legacy raw-render hashes match their stored artifacts; current output hashes are measured without edits. Blank runs count consecutive lines containing only whitespace.

```json
[
  {
    "family": "architecture",
    "kind": "minimal",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/architecture.v2-minimal-render.md",
    "sha256": "1ddda9dbf8b75eeca662271fb069e919c7356fb9479363dfac8fd598bb0be701",
    "chars": 417,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "architecture",
    "kind": "minimal",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/architecture.minimal.md",
    "sha256": "c397da5adc15400389c3ac17a0f6b20d84370dc7049ff198f6c8da85c1d44ecd",
    "chars": 199,
    "max_blank_run": 8,
    "terminal_newline": true
  },
  {
    "family": "architecture",
    "kind": "filled",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/architecture.v2-filled-render.md",
    "sha256": "fa18b90f83729f524dca8598d8188e321cfd1a7e21f53afdba1f930d4278559b",
    "chars": 997,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "architecture",
    "kind": "filled",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/architecture.filled.md",
    "sha256": "df46ccf8012f4397d669f57e9dfc08aaa56a80451b61fd417676b3a6e794437f",
    "chars": 876,
    "max_blank_run": 5,
    "terminal_newline": true
  },
  {
    "family": "generic_doc",
    "kind": "minimal",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/generic_doc.v2-minimal-render.md",
    "sha256": "62641025e894c48f2ee241adda17b614a6deb2cc23cf8ecd2f65636a3bb78eb2",
    "chars": 498,
    "max_blank_run": 5,
    "terminal_newline": false
  },
  {
    "family": "generic_doc",
    "kind": "minimal",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/generic_doc.minimal.md",
    "sha256": "a30b90120872743b8a60b76a87de7732153680f89ffd9fb53ef7e0e996733e95",
    "chars": 260,
    "max_blank_run": 8,
    "terminal_newline": true
  },
  {
    "family": "generic_doc",
    "kind": "filled",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/generic_doc.v2-filled-render.md",
    "sha256": "6d288df12a76ab3b326699948daa39633842c43e33b5d440d7317209c1d0f33c",
    "chars": 1239,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "generic_doc",
    "kind": "filled",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/generic_doc.filled.md",
    "sha256": "bd9b9de85f092047e2e2e4f0e50de8e7545e092713a413c52d601475007c538e",
    "chars": 1038,
    "max_blank_run": 7,
    "terminal_newline": true
  },
  {
    "family": "planning",
    "kind": "minimal",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/planning.v2-minimal-render.md",
    "sha256": "b6ade7aa97e0b7c6333582bbf1fe1fb1e4cf9546a2ac80fc2109458203663a19",
    "chars": 594,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "planning",
    "kind": "minimal",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/planning.minimal.md",
    "sha256": "427f3b9f8a1ceba3e62f51835fa50c8365558ee1da9b99cfab4e4e58d557a949",
    "chars": 406,
    "max_blank_run": 10,
    "terminal_newline": true
  },
  {
    "family": "planning",
    "kind": "filled",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/planning.v2-filled-render.md",
    "sha256": "ddd3273342cbfaf43db6546687982ac6976b6904efdba04242a864ff7eee2284",
    "chars": 679,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "planning",
    "kind": "filled",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/planning.filled.md",
    "sha256": "52d2d2f9a91471ecfab92d4867cbdfa50a713d33810fc1f422627368772b2c12",
    "chars": 1145,
    "max_blank_run": 13,
    "terminal_newline": true
  },
  {
    "family": "reference",
    "kind": "minimal",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/reference.v2-minimal-render.md",
    "sha256": "9c98e5db60352f71991e85bd9b153707abe358cf45a338155d599f746477f189",
    "chars": 423,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "reference",
    "kind": "minimal",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/reference.minimal.md",
    "sha256": "4d9b3a6db0c3374540a743b6ad732083752e736fb1e2d1056c1bbfd184d8f956",
    "chars": 187,
    "max_blank_run": 5,
    "terminal_newline": true
  },
  {
    "family": "reference",
    "kind": "filled",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/reference.v2-filled-render.md",
    "sha256": "ba5c374e260cea3e364077e341af95083bef29a12baee0883d217ff6384b310d",
    "chars": 739,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "reference",
    "kind": "filled",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/reference.filled.md",
    "sha256": "7af78ebb8bb07aef52b3ccac7f7920dbc4fc7d8f78c1927972cf4f8a947f63cd",
    "chars": 904,
    "max_blank_run": 6,
    "terminal_newline": true
  },
  {
    "family": "research",
    "kind": "minimal",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/research.v2-minimal-render.md",
    "sha256": "2fb21d09d16bc99aa52a0b0ed75e39b45249ec6a31c349164cf6027caea7afbc",
    "chars": 514,
    "max_blank_run": 1,
    "terminal_newline": false
  },
  {
    "family": "research",
    "kind": "minimal",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/research.minimal.md",
    "sha256": "09d949ef324097e3613fd7bc9ad2b63a52c18ef5638b355a83c7235eeeff6e3e",
    "chars": 282,
    "max_blank_run": 14,
    "terminal_newline": true
  },
  {
    "family": "research",
    "kind": "filled",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/research.v2-filled-render.md",
    "sha256": "0fce896ba87cb9e31c392ba16190c2ccadf7688cfe505cbebb2876fdf30c38fc",
    "chars": 1009,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "research",
    "kind": "filled",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/research.filled.md",
    "sha256": "e368ee845068e4525fa1bccdb27a6c6451a967b49d9591cdd78960252a0d0d6c",
    "chars": 1565,
    "max_blank_run": 5,
    "terminal_newline": true
  },
  {
    "family": "validation_report",
    "kind": "minimal",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/validation_report.v2-minimal-render.md",
    "sha256": "9b7da9954a42cb22251105eb5a047a9bb4982aac0ca748d0c1cc3e8a0c6afd13",
    "chars": 447,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "validation_report",
    "kind": "minimal",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/validation_report.minimal.md",
    "sha256": "0b6e98ddd6e637c961134cf29fd2b6ed4d483dff9200c917455e87c3ad84e029",
    "chars": 134,
    "max_blank_run": 21,
    "terminal_newline": true
  },
  {
    "family": "validation_report",
    "kind": "filled",
    "version": "v2",
    "path": ".pgmcp/temp/issue473-comparison-03/validation_report.v2-filled-render.md",
    "sha256": "7a4e8f3b29ab7e014dc7b92e827f9ce31e362192a1fe48110c57dd6d0823fb6c",
    "chars": 517,
    "max_blank_run": 2,
    "terminal_newline": false
  },
  {
    "family": "validation_report",
    "kind": "filled",
    "version": "v3",
    "path": ".pgmcp/temp/issue473-survey/validation_report.filled.md",
    "sha256": "64b0ae6b95fcdf3f0dba5066cf08a34051751525cbc1303b59cea7a60fecd9f0",
    "chars": 940,
    "max_blank_run": 8,
    "terminal_newline": true
  }
]
```

Each rewrite ran explicit Markdown structural validation; all passed. Cached structured DTOs were fully read. The first evidence-container scaffold receipt is `pgmcp://cache/runs/022d8addb2f7433abdc01191f9d9da33`; the remaining scaffold/rewrite receipts are indexed below. The generic_doc bootstrap ID selects a current validation profile and does not misrepresent the source of the final legacy output.

```json
[
  {
    "path": ".pgmcp/temp/issue473-comparison-03/architecture.v2-minimal-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/286ddeb29184458dba5e1c993e920806",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/architecture.v2-filled-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/4c0184ce0d594e7087694c49b9b4da77",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/architecture.v2-filled-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/956243796486429a9db47ad254e5a4b7",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/generic_doc.v2-minimal-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/df6f83fa1c7f4df5be20448bd66363ce",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/generic_doc.v2-minimal-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/59baaa19b4364008a1273dfded3dee57",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/generic_doc.v2-filled-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/93a6ef1758c64c55beb34ec99e6a3ce1",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/generic_doc.v2-filled-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/159e2ba41beb47078b4eaaa4cbb035b6",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/planning.v2-minimal-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/c5e09cb4afc4425f8c5a92349b05890a",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/planning.v2-minimal-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/da0c39bf7a99434a8b313f0649611469",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/planning.v2-filled-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/3a05920889b84a8381d569f49ce85fac",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/planning.v2-filled-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/86ffd955ef124e21b4d1417531c39434",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/reference.v2-minimal-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/03ffeeadb3174b559d4c1cf045e7e201",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/reference.v2-minimal-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/c266157f2b5c4dbe8d98c65ef0b14d08",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/reference.v2-filled-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/6a1aa07ebf9a428796562faaa4ffa8e3",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/reference.v2-filled-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/2f19dad5e0b443c3b5c85fe4147e2563",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/research.v2-minimal-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/8bde2dd9b04e46b5b29b27f5af501f62",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/research.v2-minimal-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/95720c5b85b84492b2f51e5da435dd0c",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/research.v2-filled-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/9775b657dcde4413ab9bc93c0e37a14f",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/research.v2-filled-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/c8ee402c64ed43e2bd88ce6692465043",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/validation_report.v2-minimal-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/a5cd666d8fa54a4b929deaebfe633e60",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/validation_report.v2-minimal-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/a794473b8d0b4aef937ad7cd722453d4",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/validation_report.v2-filled-render.md",
    "action": "scaffold",
    "uri": "pgmcp://cache/runs/d2470d3e3f00421f8349f423c56fa2aa",
    "status": "passed"
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-03/validation_report.v2-filled-render.md",
    "action": "rewrite",
    "uri": "pgmcp://cache/runs/477766b989234b8dba79223cbdbf9e27",
    "status": "passed"
  }
]
```

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-02 | @imp researcher | Record the six remaining document-family comparisons and twelve authorized legacy renders. |
| 0.2 | 2026-10-02 | @imp researcher | Record human-approved Architecture and Generic Doc presentation outcomes without changing raw comparison evidence. |
| 0.3 | 2026-10-02 | @imp researcher | Link the approved no-legacy clean-break strategy; retain raw comparison evidence. |
| 0.4 | 2026-10-03 | @imp researcher | Record qualified native quality and independent whitespace assessment; index eight targeted raw examples without selecting numerical limits. |
