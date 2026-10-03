<!-- pgmcp:v1 id=research pv=1.0.0 pf=i6OWAIfugGkQJPIz sf=9PfER5JkyAoFQLRi -->

# Issue 473 — First-call Quality of Shipped Concrete Templates

**Status:** RESEARCH — prepared for independent review  
**Version:** 0.23  
**Last updated:** 2026-10-03

## Purpose and scope

Investigate evidenced first-output defects and ownership boundaries, and record human-approved formatting, lint, presentation, compatibility and verification objectives for subsequent Design. The consolidated Approved Strategy below governs; earlier findings/proposals preserve the discussion state at the time of observation.

All 19 shipped concrete packages with minimal and representative filled context, generated-versus-authored attribution and per-boundary strategy options.

Excluded from this Research execution: Template/runtime fixes, Design or Planning and full Validation. The human explicitly confirmed that #476 remains independent, with concrete semantic inspection and shared evidence from #473; its generic analyzer is outside #473. The human also directs an active current-tool practice assessment during later implementation, with reproducible findings for subsequent triage.

## Problem statement

Shipped concrete templates can produce syntactically accepted first outputs that require native formatting/lint repair or have excessive generated Markdown whitespace and mechanical labels. Schema acceptance and preflight success do not define the desired first-output objective.

## Goals

- Reproduce the first output of every shipped concrete package with minimal and representative filled context.
- Trace defects to generated structure while retaining caller-content and dependency counterevidence.
- Present separate formatting, lint, presentation, compatibility and enforcement choices for human approval.

## Background

Issue #473 follows deferred D-VAL-05 from issue #460. Branch bug/473-first-call-template-quality integrates into main; epic #72 is administrative. Prior gallery evidence is context only; fresh survey evidence below is authoritative for this Research.

## Findings

### Investigation boundary and reproducibility

The authoritative branch is `bug/473-first-call-template-quality`, initialized as a bug workflow in Research, integrating into `main`. Epic #72 is an administrative parent. This investigation does not change templates, schemas, production/test code, native configuration, or workflow enforcement. All findings below concern the current source catalog, not hypothetical future output.

The [release manifest](../../../.pgmcp/config/release_manifest.yaml) ships the complete [active suite](../../../.pgmcp/template_suite), and [catalog loading](../../../mcp_server/services/template_catalog.py) enumerates direct concrete packages while excluding shared support. All 19 admitted IDs were confirmed with live `scaffold_schema`; each current package version is 1.0.0. For each ID, an accepted required-only context and a representative filled context were rendered through public `scaffold_artifact`, yielding **38 untouched first outputs**. Exact inputs, source fingerprints, invocation controls, receipts, SHA-256 output digests, measurements, decisive native logs and selected outputs are preserved in [the survey evidence](first-output-survey.md).

Report-mode survey persistence retained native failed/unavailable facts and was deliberately confined to ignored `.pgmcp/temp/issue473-survey/`; no repair or auto-fix was performed. The persisted Research documents are separately authored analysis, not part of the 38 output measurements. One schema-rejected TypeScript preparation input was corrected before an output existed; it is recorded as a caller error and excluded from the accepted inventory.

### Observed versus expected behavior

**Observed:** all 16 Python outputs pass syntax yet fail Ruff formatting. Lint reports **15 findings: 10 I001 import-block findings, 3 E501 long lines, and 2 W293 whitespace-only lines**. Ten Python outputs have lint findings; six are lint clean. All 18 Markdown outputs pass their configured scaffold preflights, while generated blank runs range from 4 to 21 lines across these Markdown cases. The two TypeScript and two commit outputs persist with `dependency_unavailable`; their native checks are not proved by this survey.

**Possible direction for discussion:** template-generated structure should be useful on the first call under an explicit, bounded quality contract; caller content, native availability and workspace policy must remain separately accountable. Schema acceptance and syntax success must not be presented as formatting, lint, dependency-resolution, editorial or semantic certification.

| Concrete package | Output | Preflight minimal / filled | Maximum blank run minimal / filled | First-output observation |
| --- | --- | --- | ---: | --- |
| architecture | Markdown | passed / passed | 8 / 5 | Generated vertical spacing; subsection grouping is useful, but its label is mechanical. |
| commit | Text | unavailable / unavailable | 2 / 2 | Extra generated trailing lines; native commitlint unavailable. |
| design | Markdown | passed / passed | 20 / 11 | Absent optional sections retain whitespace; labels carry actual option/validation distinctions. |
| generic_doc | Markdown | passed / passed | 8 / 7 | Generated Sections/Content wrappers; supplied empty migration list emits an empty section. |
| issue | Markdown body | passed / passed | 8 / 4 | Whitespace persists around absent/filled tracking fields. |
| planning | Markdown | passed / passed | 10 / 13 | Repeated blank joins and mechanical field labels around work/deliverable records. |
| pr | Markdown body | passed / passed | 5 / 5 | Repeated generated joins; explicit empty deferred work truthfully emits its current message. |
| pytest_integration_test | Python | passed / passed | 5 / 5 | Both format fail; filled I001. |
| pytest_unit_test | Python | passed / passed | 5 / 3 | Both format fail; filled I001 and fixture/marker spacing in format diff. |
| python_adapter | Python | passed / passed | 5 / 4 | Both format fail; filled I001 and generated method/logger spacing. |
| python_class | Python | passed / passed | 2 / 2 | Both format fail only for generated trailing blank lines in these samples; lint clean. |
| python_protocol | Python | passed / passed | 3 / 3 | Both format fail; both I001 with template-required Protocol import. |
| python_pydantic_config | Python | passed / passed | 4 / 4 | Both format fail/I001; minimal W293; filled E501 (153 columns). |
| python_pydantic_dto | Python | passed / passed | 4 / 4 | Both format fail/I001; minimal W293; filled E501 (126 and 114 columns). |
| python_worker | Python | passed / passed | 5 / 4 | Both format fail; filled I001. |
| reference | Markdown | passed / passed | 5 / 6 | Whitespace and repeated Sources/Methods labels; source scopes retain real meaning. |
| research | Markdown | passed / passed | 14 / 5 | Absent optional blocks and evidence/consumer/risk joins retain blank lines. |
| typescript_dto | TypeScript | unavailable / unavailable | 2 / 2 | Generated extra joins and repeated assignments; no configured TS format/lint objective. |
| validation_report | Markdown | passed / passed | 21 / 8 | Minimal emits title plus 21 blank lines; filled metadata/evidence labels and spacing. |

The maximum blank-run column includes trailing blank lines; it is an observation, not an approved threshold. Python line lengths are evaluated against the actual [Ruff baseline](../../../pyproject.toml), including line-length 100, target Python 3.11 and its selected lint families. The first-output examples use short ordinary descriptions and normally formatted bodies. The survey targets do not receive the repository's `tests/**/*.py` ANN/ARG exclusions. No caller-body or unresolved-dependency lint finding occurred in these examples.

The minimal `python_class` is useful counterevidence: its generated import/body structure is lint clean and only its generated trailing blank lines require formatting. A minimal protocol still raises I001 using only the package's fixed `Protocol` import; caller import ordering is therefore not necessary to reproduce the import defect. Minimal Pydantic models generate a line containing four spaces when no field is supplied. Populated configuration/DTO samples produce a 153-column `ConfigDict`, a 126-column `ConfigDict`, and a 114-column `Field` call from modest values; the complete expression is authored by the template.

### Causal evidence and competing explanations

| Finding | Direct causal evidence | Ownership and countercondition |
| --- | --- | --- |
| Excess blank lines across first outputs | [Production Jinja composition](../../../mcp_server/bootstrap.py) constructs a plain `Environment(loader=DictLoader(...))`; [root](../../../.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2), [code](../../../.pgmcp/template_suite/shared/templates/bases/tier1_code.jinja2) and [document](../../../.pgmcp/template_suite/shared/templates/bases/tier1_document.jinja2) bases retain newlines around inherited blocks. Concrete loops/conditionals add further seams. Untouched native format diffs remove those exact lines. | Template-owned when no caller value contains those runs. Omitting optional values can increase empty-block spacing; filling them does not eliminate it. Caller paragraphs/fences deliberately containing blank lines remain caller-owned. |
| Import-block I001 | [Import emission](../../../.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2) inserts group comments/newlines and sorts rendered statements; surrounding [Python](../../../.pgmcp/template_suite/shared/templates/bases/tier2_python.jinja2) and package blocks add spacing. Minimal protocol and minimal Pydantic models reproduce I001 with template-required imports. | Generated grouping/spacing is causal; lexical ordering of supplied imported members is not currently a full native isort contract. This survey does not claim every import order/group combination is investigated. The class's one ordinary import is lint clean in the filled sample. |
| W293 for absent model fields | [Pydantic DTO](../../../.pgmcp/template_suite/python_pydantic_dto/template.jinja2) and [configuration](../../../.pgmcp/template_suite/python_pydantic_config/template.jinja2) indent the empty field macro result; native logs locate the whitespace-only line after `model_config`. | Template-owned; the minimal context has no field/body string capable of supplying it. Populating fields removes this specific finding. |
| Long model expressions | [Pydantic macros](../../../.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2) emit `ConfigDict` and `Field` on one physical line with all supplied structured values. Native format diffs wrap the generated expressions and E501 identifies their exact columns. | Template-owned composition of individually modest values. Arbitrarily long authored annotation/prose/literal tokens or code bodies cannot be universally cured without a different ownership contract. |
| Mechanical Markdown presentation | [Generic document](../../../.pgmcp/template_suite/generic_doc/template.jinja2) emits fixed `Sections` and `Content:`/carrier labels; [planning](../../../.pgmcp/template_suite/planning/template.jinja2), [reference](../../../.pgmcp/template_suite/reference/template.jinja2) and [validation](../../../.pgmcp/template_suite/validation_report/template.jinja2) emit fixed field labels around nested records. Generated labels and whitespace are observable independently of the supplied prose. | Excess spacing is measured. Label redundancy is an editorial judgment requiring approval; Sources/Expected Result/Outcome and other labels often distinguish real contracts or evidence and must not be removed indiscriminately. |
| Successful preflight despite defects | [Scaffold policy](../../../mcp_server/services/scaffold_operation.py) runs the package-selected profile; [checks configuration](../../../.pgmcp/config/checks.yaml) keeps syntax/Markdown preflights separate from Python review. [Markdown preflight](../../../mcp_server/bundled_adapters/markdown_preflight/check.py) checks structural/link conditions, not these blank runs or editorial redundancy. | Intended check boundary, not evidence that syntax/preflight implementation is faulty. The renderer validates context then renders; it contains no formatter phase. |

A possible caller-content explanation was tested rather than discarded: the generic document's supplied link points to a non-existent suite README. Offline Lychee inspects 15 links, with **14 successful and one missing target**, preserving exactly the authored target. This is a research-input defect, not an escaping/templating defect; the first output and failed receipt are retained. Likewise the keyword-excluded TypeScript name and missing current-workspace native dependencies cannot be counted as generated-source failures.

### Existing evidence, limits and confidence

The 19 existing concrete-package integration test files pass: **85 passed, one existing Pydantic schema-shadowing warning, 83.31 seconds**, via `run_tests` with selected files, `-q -n 0` and timeout 120. These durable tests already cover important context validation, preserved bodies/literals, native syntax or compilation, missing/empty optional carriers, ordering, escaping, links, class/method/model shape and explicit provenance. Their successful semantic contracts coexist with live first-output formatting defects.

The [delivered-template fixture](../../../tests/mcp_server/fixtures/delivered_templates.py) composes separate copied suite snapshots, `StrictUndefined` and `keep_trailing_newline=True`; the live production environment differs in those flags. [TypeScript tests](../../../tests/mcp_server/integration/templates/test_typescript_artifact.py) use their fixture's native dependency for strict compilation, and [commit tests](../../../tests/mcp_server/integration/templates/test_commit_artifact.py) use their own package fixture. Those passes do not prove current workspace TypeScript/commitlint availability for the survey. No broader gates or full configured suite were run in Research.

Causal confidence is high for generated blank-line seams, empty Pydantic indentation and unwound generated model expressions because raw inputs, first outputs, template lines and native diagnostics agree. It is bounded for import combinations beyond the observed cases and deliberately qualitative for editorial labels. Two samples per package establish a reproducible defect family, not every schema-valid value or every optional branch. No generic declaration-to-consumption theorem or missing-field finding is established here.

### Proportional blast radius and consumers

| Surface or consumer | Impact and existing owner |
| --- | --- |
| Shipped concrete templates and transitive shared bases/macros | Direct source of generated layout; shared changes may affect multiple artifact families. A root/shared-base change can affect all 19 packages. Package/source fingerprints must reflect changed effective sources through the existing mechanism. |
| First-time scaffold callers, agents and human editors | Receive the first output, supply raw bodies/prose/types/import choices and expect explicit context values to retain meaning. The current `scaffold_schema` contract defines shape, not universal quality. |
| Catalog/schema rendering services and scaffold/safe-edit operations | Consume prepared packages and profiles. No production change is established as necessary; they must retain explicit injected rendering, immutable selections, factual native results and persistence behavior. |
| Native tool configuration and selected preflight/review profiles | Own the workspace Ruff baseline and availability. A template-quality promise does not implicitly broaden enforcement or introduce installation/formatter dependencies. |
| Existing package tests, copied-suite fixtures, header/AST consumers | Preserve semantic contracts, escaping and provenance. Tests should gain meaningful first-output quality evidence under the approved contract; entire-output snapshots would couple callers to incidental whitespace. Fixture/live rendering differences must be acknowledged. |
| Markdown readers, fragment links and tooling | Consume heading hierarchy, record distinctions and exact authored link targets. Reducing redundant labels must preserve meaningful grouping and established headings/anchors unless a separate explicit compatibility decision authorizes a change. |
| Commit, Python, TypeScript and model consumers | May depend on literal values, defaults/factories, method bodies, optional-field behavior, constructor shape and framing. Pure presentation work cannot alter those semantics or claim arbitrary snippets are valid executions. |
| Release, installation and renewal consumers | Ship/copy the source suite; existing component fingerprint/checkpoint conflict handling remains authoritative. No upgrade/migration protocol change is required by the current evidence. |
| Documentation, agent instructions and workflow | Need an accurate first-output objective and limitations once approved; Research cannot substitute code quality for independent QA, nor turn template conformance into a new implicit global gate. Architecture contract and English artifact/Dutch chat rules remain binding. |

### Concrete Python comparison and current standards

At the user's request, [the first Python class comparison](python-class-comparison.md) now precedes a strategy decision. It preserves exact contexts, raw v2/v3 outputs, source limits, digests and native receipts. Both current public scaffolds are lint clean and syntax valid; both fail Ruff format only for two generated terminal blank lines. The old renderer output fails current formatting and ANN201 on its invented placeholder method.

The intended `C:/Users/miche/.codex/worktrees/issue460-validation-baseline` directory contains only an empty name marker. A separate legacy PGMCP checkout supplies the unmodified v2 renderer and Generic template used for provisional comparison; this is not a full issue460 public pipeline reproduction. Exact source paths and the probe-only legacy metadata marker are documented in the comparison.

The canonical #460 strategy register records removing Generic's forced architecture metadata, logger and placeholder as part of its approved portable plain-class responsibility. That recorded approval does not independently verify the original human conversation, and not every quote/layout choice was a separately approved Research decision. Familiar presentation preferences remain open for discussion.

Current [Code Style](../../coding_standards/CODE_STYLE.md) delegates formatting to native configuration and does not require those legacy defaults or triple-quoted docstrings. The observed trailing-line defect violates that formatting baseline for the samples. [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) governs this Research's evidence, presentation and phase ownership; it does not impose Python logger or quote rules. Its own version metadata is inconsistent and its four related-document definitions are broken according to offline Lychee. Architecture's template-path/schema wording is a candidate stale terminology issue. No standards or engine policy have been changed; the comparison maps each concern to its owner and evidence level.

### Design Markdown comparison: metadata and version history

The user next identified missing familiar headers and version-history tables. [The Design document comparison](design-document-comparison.md) now preserves two authorized legacy-render examples, the original minimal/filled v3 examples, and an additional public v3 scaffold with all document metadata supplied.

The original filled Design context supplied status, but not version or last_updated. The added case renders all three correctly; omission of metadata is therefore distinct from a lost rendering capability. The minimal v3 output still has a title and hidden provenance comment, but no visible status/version/date block. Current Design has no dedicated history input or generated Version History table.

Legacy Design supplies DRAFT, version 1.0, a timestamp-derived header date and an automatic Agent/Initial draft history row. Its minimal-nucleus history date is blank despite the dated header; the filled example has matching explicit dates. #460 Design records relaxing metadata requiredness and removing automatic history, authors and lifecycle defaults. The older BASE/Design references require those sections; the current Documentation Standard does not state the same universal requirement. Desired authored metadata/history framing remains a separate discussion objective, not a silent reversal of prior boundaries.

The legacy examples have maximum blank runs of one line; current Design has 20 minimal and 11 filled, including terminal whitespace. Header hard-break markup, section numbering, requirement checkboxes, empty section/table placeholders and pros/cons symbols also differ. Structural/link preflights pass, but do not certify these editorial choices. The comparison records source and evidence limits, including that the v2 minimal-nucleus render is not a full old schema-valid public call.

### Historical rationale audit, without new objectives

The user asked to trace intent rather than turn observations into new objectives. [The rationale and decision-authority audit](design-document-comparison.md#rationale-and-decision-authority-audit--2026-10-02) now cites the archived Design 460 conversation. On 2026-09-11 the human explicitly defined optional-field presence behavior, required preservation of correct behavior, delegated detailed W07/W08 Design, and later supplied independent QA GO for those contracts.

Metadata optionality and automatic history removal therefore precede implementation as agent-authored choices under human delegation. No separate per-field human preference was found. The rationale against invented lifecycle facts does not itself prove that metadata must be optional or that a caller-authored table must be absent. Research catalog rows 172–173 retain/adapt the portable header/history patterns; header capability survives, while the version-table responsibility has no clearly reconciled current Design facility. This is an unresolved preservation explanation, not a new QA verdict or a finding of unauthorized conduct. Generated blank runs remain implementation quality evidence rather than approved presentation intent.

No new objective or Approved Strategy follows from this historical audit.

### Human-approved document-framing objective — 2026-10-02

The user explicitly agreed to the proposed mandatory metadata header and version-history table, then asked whether tiered Jinja composition can keep the implementation DRY. This approval is limited to the full-document framing objective; it does not approve every B1–B5 candidate or select the exact implementation.

For architecture, research, design, planning, validation_report, reference and generic_doc, even a minimal scaffold must visibly present caller-authored status, document version and last-updated date, plus a version-history table with at least one explicitly supplied revision (version, date, author and change description). Header version/date and the current revision must agree. Package provenance remains separate; neither document status nor the table grants workflow authority. Issue, PR and commit retain their own presentation contracts.

This deliberately tightens the admitted context boundary: existing calls without the required document facts/revision content cannot satisfy the new objective. The no-legacy clean-break strategy below now governs this context change. Exact context shape, requiredness composition and the affected-consumer inventory remain to be defined within that strategy. The earlier B4 context-preservation candidate cannot apply unchanged to these seven document contexts.

DRY and the generic engine boundary remain binding. Current evidence shows all seven concrete roots already inherit one shared Markdown document base; shared JSON Schema definitions also already exist. Design should assess reuse of these established seams and a single authoritative source for current revision facts, rather than copy rendering/validation policy or introduce artifact-specific generic Python. This records a feasible direction and architectural constraint, not an approved patch or macro/schema layout.


### Structured document-family follow-up — 2026-10-02

The user agreed to use one concrete comparison as a baseline, then review similar concrete templates faster. [The document-family comparison](document-family-comparison.md) now uses Design for common framing and compares the other six full-document families separately. Twelve authorized legacy raw renders (minimal-nucleus and filled) are stored next to the twelve untouched current survey outputs. Exact translated inputs, graph/file hashes and fully read persistence receipts are preserved; all twelve final legacy files match the raw renderer SHA-256 and pass Markdown structural preflight.

The original authorized source contains no Validation Report template. That family explicitly uses a separately found installed legacy template root with the same renderer; no identical historical snapshot or full old MCP-call claim is made. Explicit probe metadata augments the current minimal body nucleus, so the old render inputs are not advertised as schema-valid old minimal public calls.

Architecture preserves content and repairs constraint rendering but changes subsection numbering and decisions-table presentation. Generic Doc preserves custom-section capacity but introduces a Sections wrapper and Content/Bullets/Checklist labels. Those editorial choices lack a separate rationale in the inspected #460 contract and remain discussion points. Planning's workflow-neutral Work Units and Reference's source/test/language changes are explicitly recorded in #460. Research preserves content and repairs reference-list shadowing; Validation Report extends explicit evidence carriers and removes invented defaults.

Shared metadata/history findings are recorded once against the approved framing objective. Generated whitespace remains separately evidenced: current family samples have maximum blank runs of 5–21; the old examples also have defects (1–5), so legacy output is not a normative quality baseline. Empty-container rendering when an optional field is explicitly supplied empty follows the earlier human-approved presence rule and must be distinguished from accidental whitespace. No new family-specific objective, template/schema/standards change or phase progression follows from this comparison.

### Human-approved Architecture and Generic Doc presentation objectives — 2026-10-02

After the concrete presentation comparison, the user explicitly answered “Ja” to recording the proposed choices as objectives. This is a bounded outcome approval for these two families, additional to the earlier shared document-framing approval.

| Family / boundary | Approved objective | Preservation and limit |
| --- | --- | --- |
| Architecture concept grouping | Keep Concepts as a meaningful parent distinct from Constraints, Decisions and Sources. | Preserve concept order and the association of descriptions, diagrams and subsections. |
| Architecture subsection navigation | Restore visible hierarchical subsection numbering, such as 1.1 under concept 1. | Numbering expresses authored sequence; it does not create operational identity or reorder content. |
| Architecture redundant carrier labels | Omit generated Diagram and Subsections labels where the diagram and heading hierarchy already communicate their role. | Preserve the diagram and every supplied subsection; this does not approve removing meaningful source, evidence or alternatives labels elsewhere. |
| Architecture decisions | Prefer a comparison table for concise decision/rationale/alternative records. | Fully preserve long or structured authored explanations in a readable representation; no requirement to force arbitrary prose into table cells, truncate it or invent alternatives. |
| Architecture constraints | Retain separate explicit constraint rendering. | Preserve the v3 repair; do not return to the old decisions-dependent omission. |
| Generic Doc custom sections | Present each caller-supplied section directly as a document section, rather than beneath a generated Sections wrapper. | Preserve supplied heading, prose, bullets, checklists and their order. |
| Generic Doc redundant carrier labels | Do not automatically add Content, Bullets or Checklist labels where the native text/list/checklist shape communicates the role. | Preserve checked state and caller-authored text. Meaningful headings/labels remain; this is not a blanket label-removal objective. |

The [family comparison](document-family-comparison.md#human-approved-presentation-objectives--2026-10-02) records the same decision next to the untouched evidence. These outcomes do not approve every B3 presentation candidate or the remaining B1–B5 choices. In particular, numerical whitespace limits, runtime formatting/enforcement, other families' editorial choices and a universal final-output guarantee remain undecided.

Changing generated heading text/numbering can change Markdown anchors and invalidate the earlier B4 candidate of preserving every heading/anchor; heading level alone need not change the fragment. The human has now approved the clean-break strategy below for presentation and metadata/revision contexts. Affected-consumer discovery determines concrete migration work within that decision.

DRY and the generic engine boundary still apply. Shared framing and reusable presentation patterns should have shared owners, while family-specific meaning governs document grouping. Exact Jinja composition, table handling for complex prose, schemas, test design and implementation sequence are not selected here.


### Approved Strategy: clean break, no legacy compatibility — 2026-10-02

After the practical compatibility explanation, the user explicitly stated: “Ja, ik wil geen compat legacy.” This approves a clean break for the boundaries changed by the agreed issue #473 outcomes.

| Affected boundary | Approved strategy | Consumer consequences |
| --- | --- | --- |
| Generated document presentation and headings | New scaffolds use the agreed presentation. Do not preserve the previous output through legacy modes, duplicate heading aliases, redirects or a parallel template suite. | Identify and update demonstrably affected repository links, expectations and consumers to the new output. Accept changed generated heading fragments; no byte-for-byte legacy output commitment. |
| Full-document metadata and revision context | Require the explicitly supplied document facts and revision content agreed for the seven full-document families. Do not accept the old incomplete context through a legacy schema, adapter or fabricated defaults. | Existing active callers and fixtures must supply the new facts; incomplete calls follow ordinary context-validation failure. Exact field shape and schema composition belong to Design. |
| Existing authored files | Keep existing documents as ordinary files; do not mass-rewrite them to imitate newly scaffolded output. | Update concrete affected references where needed. Old document content/provenance does not require a compatibility renderer. |

Heading text and generated numbering can change Markdown anchors; a change of heading level alone does not necessarily change the fragment. Consumer discovery determines the edits required, not whether a legacy bridge should be added. No such bridge is authorized.

The accepted cost is targeted migration of known callers, fixtures, tests and references. An unknown external consumer can encounter changed headings or a rejected incomplete context and must adopt the new contract. Retaining dual behavior would add schema/template/test branches and ongoing maintenance; the user explicitly rejected that trade-off.

This strategy applies to changes within the approved #473 scope, not arbitrary unrelated API or distribution redesign. The located v2 renderer remains authorized as Research comparison evidence; it is not a production compatibility path. The source suite's existing identity, provenance, fingerprint and distribution mechanisms retain their current owners.

The context/anchor compatibility decision is now settled. Exact implementation remains Design work; broader first-output quality and enforcement objectives remain separate discussion choices. Research still requires those remaining affected-boundary decisions and independent review before it can close.


### Remaining Python-family batch — 2026-10-02

The user requested the next template batch. [The Python-family comparison](python-family-comparison.md) uses Python Class as the established reference and covers Protocol, Pydantic Config, Pydantic DTO, Adapter, Worker and both pytest families. Sixteen authorized legacy raw renders are now stored: fourteen minimal/filled counterparts plus two additional hidden dto_v2 examples. Protocol and Adapter use their real counterparts from the separately found installed legacy suite because the original source root lacks them.

All sixteen legacy stored hashes match their raw renderer strings. Thirteen final public Python syntax checks passed; three old DTO outputs failed and are preserved unchanged in report mode. These are renderer comparisons, not schema-valid old public pipeline claims. The rich filled factory uses a modern dotted callable outside the old typed-ID import assumption; rich/hidden minimal roots also render a dedented pass before model_config. Both rich and hidden old DTO baselines matter because the old manager could select dto_v2 in its enabled typed pipeline.

All fourteen current files match their original survey hashes. The original quality receipt had expired from the live cache, so a fresh narrow run_checks over these fourteen files was executed and its complete DTO read: `pgmcp://cache/runs/6bc2219eed2d401d901859251173301f`. Ruff 0.15.6 confirms fourteen formatter differences and fifteen lint findings (ten I001, two W293 and three E501). Ordinary supplied records are joined into overlong ConfigDict/Field expressions; imports and blank joins account for the remaining generated defects. No file was fixed and no generated-source runtime or full Validation test was run.

The substantive removals are recorded #460 choices: no fabricated Protocol execute/Adapter adapt, opt-in portable logging, pure distinct DTO/config contracts, no source-project worker lifecycle/typed-ID factory imports and no inferred pytest mocks/classes/fixtures/async or passing placeholders. Constructor, method and test/fixture bodies remain explicit portable capabilities. The old DTO Fields docstring summary and Worker __all__ export list have no individually located rationale; they remain bounded presentation/export questions, not proven loss of an affected real consumer or automatic restoration objectives.

The batch itself did not approve an objective. The subsequent human reply on 2026-10-03 approved the proposed bounded Python native quality objective with the independent whitespace qualification recorded below. The existing no-legacy strategy remains binding. The final TypeScript DTO and Issue/PR/Commit comparisons below complete the nineteen-family inventory; document metadata/history objectives do not apply automatically to those tracking/code families.


### Human-approved Python quality and independent whitespace objective — 2026-10-03

The human agreed to the proposed Python first-output format/lint objective, while explicitly qualifying that Ruff conformance may not establish tidy whitespace. The human requested targeted examples for Python and the document batch and kept whitespace an important independent concern.

- B1 is approved as a bounded objective: generated structure in minimal, representative and meaningful boundary cases should satisfy the configured native Ruff format/lint baseline when caller fragments themselves satisfy it. Syntax success or lint success alone is not a presentation claim.
- Python and full-document Markdown whitespace must be assessed independently against concrete examples: omitted/empty/filled joins, declaration/section transitions, whitespace-only lines and EOF. No additional numerical blank-line limit has been approved yet.
- Preserve the distinction between generated structure and authored content. This approval does not permit indiscriminate whole-output formatting, rewriting caller prose/code/fences, new blanket context restrictions or runtime enforcement changes.

[Eight untouched whitespace probes](whitespace-comparison.md) now provide those examples. All structural preflights passed; Ruff would format all four Python files. Generated import/empty-block findings are separate from an authored adapter-body lint finding. The native formatter would also collapse an authored two-blank-line body separator. All four Markdown examples pass structural preflight while containing excessive generated joins. These observations support an explicit generated-structure boundary; they do not select a normalization algorithm.

Candidate criteria remain for discussion: syntax-aware Python spacing under the configured baseline, one empty separator for generated Markdown blocks, no generated indentation-only lines and one terminal newline without additional generated blank lines. Authored internal whitespace and meaningful Markdown hard-break spaces are preserved. Exact criteria and exceptions, shared tier implementation and runtime policy are not implied by this qualified approval.

### Final tracking and TypeScript batch — 2026-10-03

[The final family comparison](tracking-typescript-comparison.md) covers TypeScript DTO and Issue/PR/Commit. All nineteen shipped families now have minimal/filled v2/v3 comparison indexes, subject to the recorded source and renderer limits. The final batch adds eight exact legacy baselines, one old colon-type probe, eight fresh current baselines and five current boundary probes. Nine legacy files match raw renders; the eight current baselines match original survey bytes exactly.

The original old source root supplies Issue/PR/Commit; the separately found installed root supplies TypeScript because the original root has no TypeScript package. The same authorized unmodified renderer is used. Modern required-nucleus translations and explicit old comparison metadata are evidence contexts, not asserted old public schema/pipeline equivalents.

Recorded #460 choices explain body-only Issue/PR envelopes, no document metadata/history for tracking, explicit deferred-none/populated declarations, removal of invented Testing/checklist defaults, native Commit framing and structured TypeScript properties/optional presence. TypeScript's duplicate minimal description has an explicit rationale in Code/Test Design §7.1: class description also supplies module documentation when module_description is omitted.

Old outputs are not a layout standard. Old minimal PR joins its test placeholder and Checklist heading on one line; old filled PR/Commit omit the terminal newline. Old TypeScript turns optional names into question-mark assignments and truncates a function/object type on colons. Current output preserves full native type text and emits a guarded optional assignment. Native checks were initially unavailable; the authorized tooling follow-up below now confirms current syntax and the two old syntax defects.

Independent blank measurements show current Issue minimal has eight extra EOF blank lines, PR minimal five, Commit minimal/filled two and TypeScript minimal/filled one. PR filled has five generated blank lines before Closes; TypeScript filled inserts generated blanks between assignments. Additional Issue/PR/Commit examples preserve authored three-blank separators, code-fence spacing and a Markdown hard break exactly. Empty carriers remain a separate presence-contract choice.

Initial native artifact evidence: six current Issue/PR body preflights and four legacy body rewrites passed. Four current TypeScript, three current Commit, three legacy TypeScript and two legacy Commit preflights were unavailable because the workspace cannot resolve typescript or @commitlint/cli. Three preliminary run_checks requests were rejected at public selection before execution and are not native evidence. No installs, fixes, broad gates or new tests were performed in that initial batch.

The adjacent [.agents/workflows/create-issue.md](../../../.agents/workflows/create-issue.md) still uses obsolete name/title/labels scaffolding inputs and instructs full saved-content publication. Record this active consumer mismatch against live inputs and #460 surface ownership; no instruction repair, publication route or automatic #476 expansion is selected here.

This batch adds evidence and recommendations, not human approval for tracking/TypeScript numerical layout, description deduplication or heading changes. Research remains open for consolidated boundary decisions and independent review.

### Authorized native tooling follow-up — 2026-10-03

The human authorized installing the missing prerequisites for an honest substantive analysis. [The native tooling follow-up](native-tooling-follow-up.md) records project-pinned TypeScript 6.0.3, commitlint 21.2.2 and conventionalcommits parser 10.4.0 installed locally, with existing Pyright restored and retained at 1.1.408 after npm pruning. No root dependency manifest or lockfile was created and no template, adapter, schema or gate configuration was changed.

All twelve raw TypeScript/Commit comparison files remain byte-for-byte unchanged. Four current TypeScript and three current Commit preflights pass. Old minimal TypeScript passes; old filled and colon-type TypeScript fail with native syntax diagnostics at the generated defects. Both complete saved old Commit files fail because the comparison provenance line reaches commitlint; separate views excluding only that first line both pass. This isolates message content from the legacy storage envelope without adding compatibility behavior.

The eight existing TypeScript/Commit native contract tests pass, with one existing Pydantic warning. Their strict/executable TypeScript fixture evidence is distinct from raw syntax preflight and caller-owned support dependencies. The original availability receipts remain historical; the current native dependency gap is resolved. Native success does not settle generated spacing/EOF, select new format/lint tooling, impose universal guarantees or approve runtime enforcement. Remaining Research decisions below are unchanged.

### Human-directed sequential decision discussion — 2026-10-03

The human instructed the researcher to discuss and record the remaining points systematically, then request independent QA only after those decisions are complete. This changes the discussion sequence and review timing; it does not approve any numerical criterion or unresolved strategy proposal.

| Order | Boundary to decide | Current status |
| --- | --- | --- |
| 1 | Generated whitespace and EOF across Python, full documents, tracking and TypeScript | Approved below; text-block boundary treatment resolved in point 2. |
| 2 | Caller-owned code/prose/value preservation versus structural transformations | Approved below: trim blank boundary lines of inserted text blocks; preserve internal content and data values. |
| 3 | Remaining family-specific presentation and export choices | TypeScript constructor spacing and separate class/module documentation approved; Python explicit documentation and retained one-main-class scope approved below; DTO retains field descriptions in Field definitions without an automatic repeated summary; Worker does not generate an automatic __all__. These remaining presentation/export choices are approved below. |
| 4 | First-output verification and runtime preflight/enforcement | Approved: actual scaffolding and manual agent inspection during implementation, without additional automated content/regression tests; apply changed input contracts/render behavior while retaining existing preflights and adding no runtime quality gates. |
| 5 | Standards reconciliation and affected callers, fixtures, links and instructions | Approved: reconcile directly relevant standards and demonstrably affected active consumers with agreed contracts; retain existing authored files and exclude unrelated cleanup. |

For each point, record the human decision, affected boundary, behavioral outcome, preservation constraints and clean-break consumer implications. Keep proposed criteria visibly separate from approved decisions. Macro/schema shape, algorithms and implementation sequencing remain Design/Planning work.

After all affected-boundary decisions are recorded, consolidate Approved Strategy and Expected Results and prepare the outcome-neutral independent Research review request. No independent QA request or phase transition is made during this discussion.

### Human-approved generated whitespace and EOF objectives — 2026-10-03

The human explicitly agreed to all four proposed criteria in the sequential discussion ("Ja mee eens"). These are behavioral objectives for generated structure; they do not select a formatter algorithm, global Jinja flags, schema shape or runtime enforcement.

| Boundary | Approved objective | Preservation and limit |
| --- | --- | --- |
| Generated Python spacing | Follow the configured Ruff formatter's syntax-aware layout, including suitable top-level, method, decorator and docstring spacing. | This specifies generated structure; it does not authorize rewriting arbitrary supplied bodies or guarantee all caller fragments are format/lint clean. |
| Generated Markdown spacing | Use one empty separator between independent generated blocks such as headings, paragraphs, lists, tables and fences; add no unnecessary empty lines within a list/table. | Applies to full documents and Issue/PR bodies. Authored prose/fence spacing and meaningful hard-break spaces remain outside this approval. |
| Absent and explicitly empty generated parts | Omitted parts leave no blank-line residue; no generated source line consists only of spaces/tabs. | Explicitly empty containers retain their defined meaning; correct surrounding spacing without silently dropping them. |
| Generated EOF | End every template family with one terminal newline and no additional template-generated blank lines. | Includes Commit and TypeScript. Point 2 below resolves inserted text-block boundary lines; meaningful content/data whitespace remains preserved. |

TypeScript/Commit receive the EOF criterion, not a new complete formatter style. The subsequent point 3 decision below additionally approves TypeScript constructor spacing; other presentation choices remain open. Python native quality remains subject to the already agreed caller-fragment baseline.

All nineteen concrete families can be affected through shared composition. The approved clean break continues to govern changed generated output/contexts and targeted consumer migration. Existing evidence files remain unchanged. The subsequent point 2 decision below resolves that conflict: inserted text blocks lose only blank boundary lines, preserve meaningful/internal content, and let the renderer own separators and EOF.

Earlier numerical criteria marked pending describe the discussion state before this decision. The approved table above supersedes those proposals for these generated boundaries; B2 is settled by the subsequent decision below; remaining B3 presentation and B5 enforcement remain open. Independent QA remains deferred until all sequential decisions are complete.

### Human-approved caller-content ownership and boundary normalization — 2026-10-03

The human explicitly agreed ("Ja") to the clarified boundary: normalize blank lines at the edges of inserted text blocks, preserve internal whitespace and data values, and let the renderer add surrounding separators. The clarification supersedes the earlier blanket suggestion to preserve all supplied edge whitespace.

| Input / rendering boundary | Approved behavior | Limit |
| --- | --- | --- |
| Inserted code or document text blocks | Remove leading/trailing source lines that are empty or consist only of spaces/tabs before composition. | This is block-boundary normalization, not general stripping of every context string. No extra caller instructions or new padding-specific errors are needed. |
| Internal code/prose/fence content | Preserve internal blank lines, comments, paragraph/fence structure and meaningful spaces on substantive lines, including Markdown hard breaks. | Do not remove lines that belong to a supplied fence or string literal as though they were outside-block padding. No automatic body refactor, wrapping or lint repair. |
| Structural insertion and generated syntax | Supply required structural indentation, safe encoding and generated separators; readable layout of composed expressions remains renderer-owned. | Preserve code meaning, native type/expression choices, structured values, ordered records and explicit states under the declared package contract. |
| Data values and literals | Preserve exact meaningful values, including a default such as "  value  ". | No recursive context-wide trim or general .strip() policy; distinguish data from inserted source/document blocks. |
| Whitespace-only supplied block | Treat its renderable text as empty for composition. | Preserve the declared absent-versus-supplied-empty container behavior; do not bypass existing input validation. |
| Surrounding section spacing and artifact EOF | The renderer supplies separators and the single terminal newline according to point 1. | Supplied blank boundary lines do not accumulate with generated joins. Meaningful terminal content, fence/literal lines and hard-break spaces remain content. |

This is one shared rendering contract under DRY and the generic engine boundary. Design determines reusable tiered composition and the means of distinguishing inserted text from literal/data content; no recursive engine mutation, artifact-specific Python dispatch, algorithm or exact schema change is selected in Research.

The approved clean break covers this explicit change in output fidelity at text-block boundaries; it does not introduce an opt-in legacy preservation path. Existing raw research outputs remain untouched. Targeted evidence must distinguish padded versus unpadded blocks, preserved internal blanks/indentation/comments/fences/hard breaks, whitespace-only carriers and untouched literal/data values. The baseline Python quality condition still applies to caller fragments; normalization does not promise to repair their defects.

Independent QA remains deferred until presentation, verification/enforcement and standards/consumer decisions are recorded.

### Human-approved TypeScript constructor spacing — 2026-10-03

The human explicitly agreed ("Ja") to the four proposed constructor-spacing outcomes. This is a bounded generated-presentation decision for typescript_dto, additional to approved EOF and text-block ownership. No TypeScript-wide formatter policy or implementation technique is selected.

| Generated constructor surface | Approved outcome | Preservation |
| --- | --- | --- |
| Consecutive ordinary assignments | Emit directly on consecutive lines, without an empty line before every assignment. | Preserve assignment order and values. |
| Logically separate block | One empty separator between ordinary assignments and a separate block such as the optional-property presence check. | Preserve the guard and strict optional-presence semantics. |
| Constructor braces | No empty source lines immediately after the opening brace or before the closing brace. | Preserve the constructor signature and statements. |
| Omitted/empty fields | Retain the object-style constructor with no blank content lines. | Do not substitute an interface or omit the constructor. |

The source views in [the final comparison](tracking-typescript-comparison.md) remain unchanged observations of current behavior. Future first-output evidence must show the approved spacing for populated and omitted/empty fields while retaining the native syntax and existing strict optional contracts. The next presentation discussion concerns description reuse; no deduplication objective is approved by this constructor decision.

Independent QA remains deferred until all remaining sequential boundary decisions are complete.

### Human-approved explicit TypeScript documentation contract — 2026-10-03

In response to the module/class duplication proposal, the human selected a more explicit public name: description becomes class_description, distinct from module_description. This naming direction applies to typescript_dto in the current discussion; it does not silently rename other packages.

The current schema requires description and admits optional module_description. Renaming the class field alone does not change those responsibilities or select a new requiredness policy. The target class_description owns class documentation, while module_description owns module documentation. The existing clean-break strategy governs the rename: no description alias or dual legacy schema; affected callers, fixtures, tests and references must migrate.

After selecting the explicit name, the human explicitly agreed ("ja") to removing the automatic #460 class-to-module fallback.

| Target field / presence | Approved rendering |
| --- | --- |
| Required class_description | Class documentation only; replaces description under the clean break. |
| Optional module_description omitted | No separate module-description block. |
| module_description supplied | Render its own module documentation under the declared supplied-empty/content rules; no cross-fill from class_description. |
| Both descriptions explicitly supplied with identical text | Preserve both blocks; no text-equality deduplication. |

This deliberately replaces the #460 fallback for typescript_dto. Required class documentation remains; module description remains optional. Targeted evidence must cover omitted, explicitly empty and supplied module descriptions, distinct descriptions and explicitly identical descriptions while retaining encoding, boundary normalization and provenance. No analogous Python change follows automatically.

No source/schema or example input has been edited. Exact schema composition and implementation remain Design work. Independent QA stays deferred until the remaining decisions are recorded.

### Python documentation cardinality question — 2026-10-03

The human expressed agreement in principle with explicit Python module/class descriptions, then asked whether one scaffold can have multiplicity. This is not recorded as complete approval of Python requiredness or multi-class composition. Clarify the unit of documentation and the intended #473 scope before closing this presentation boundary.

Fresh live scaffold_schema queries for all six class-generating Python packages were fully read from cached DTOs using contiguous windows, consistent metadata, codepoint-length verification and UTF-8 SHA-256 verification. Each schema has one required class_name/description pair, optional module_description, additionalProperties=false and no admitted root collection of classes. Concrete templates each generate one main class; their method/field collections are separate cardinalities.

| Package | Required root content | Live cached schema |
| --- | --- | --- |
| python_class | class_name, description | `pgmcp://cache/runs/1d349237f8c347b5ae4a17c112886a5f` |
| python_protocol | class_name, description | `pgmcp://cache/runs/ce087213fd2c453ba3719681641a1576` |
| python_pydantic_config | class_name, description, frozen | `pgmcp://cache/runs/8ac2066b5be54fdd80b9f05746a9b8ae` |
| python_pydantic_dto | class_name, description | `pgmcp://cache/runs/6996b46c7a19467c92f22ca3fe64123c` |
| python_adapter | class_name, description | `pgmcp://cache/runs/a3fdf4c737914358972b07b22f4c4e78` |
| python_worker | class_name, description, operation | `pgmcp://cache/runs/bb095f9d5f864477bfaffcc1b1d2e9f8` |

Primary renderer evidence is in the six concrete roots, represented by [Python Class](../../../.pgmcp/template_suite/python_class/template.jinja2), [Protocol](../../../.pgmcp/template_suite/python_protocol/template.jinja2), [Config](../../../.pgmcp/template_suite/python_pydantic_config/template.jinja2), [DTO](../../../.pgmcp/template_suite/python_pydantic_dto/template.jinja2), [Adapter](../../../.pgmcp/template_suite/python_adapter/template.jinja2) and [Worker](../../../.pgmcp/template_suite/python_worker/template.jinja2). One main-class contract does not imply that a Python file can never contain multiple classes; caller-owned source and later editing are distinct from an admitted structured multi-class scaffold.

The documentation responsibility is per module/file for module_description and per generated class for class_description, with method documentation at its own member scope. A flat single-class context is the current carrier, not a universal architecture rule. Adding structured multiple-main-class composition would change context/cardinality, shared module/import composition, family-specific settings, consumers and regression coverage; it is not implicitly approved by naming or whitespace decisions. Exact container/schema shape remains Design work.

Open choice: retain current one-main-class package cardinality in #473 while making documentation roles explicit, or explicitly expand the approved scope to structured multi-class generation and investigate the additional boundary costs. No proposal is implemented or independently reviewed in this discussion.

### Human-approved Python documentation and starting-point scope — 2026-10-03

The human agreed in principle with the proposed explicit Python documentation contract, raised the possible multiplicity of one scaffold, then approved drawing the boundary at the current one-main-class scope. The stated reason is that scaffolds must provide valid starting points for further editing, not complete end products. Taken together, these replies approve the documentation proposal within that bounded cardinality; they do not authorize structured multi-class composition.

For python_class, python_protocol, python_pydantic_config, python_pydantic_dto, python_adapter and python_worker, one scaffold continues to generate one main class in one module/file. Required class_description replaces description; module_description becomes required and documents the module's own purpose. The renderer does not substitute either description for the other. Explicitly supplied identical descriptions remain legitimate caller content; no text-equality deduplication is introduced. This agrees with CODE_STYLE's module/class documentation responsibilities without claiming that the existing standard itself prescribes these exact schema fields or universal requiredness. The two pytest packages remain outside this class-description decision.

Descriptions attach to their semantic owner: module/file, generated class and, where admitted, individual members. A file may acquire additional classes through caller-owned code or subsequent editing; the present contract does not turn that possibility into an admitted collection of generated main classes. Multiple-main-class composition, shared imports and family-specific per-class configuration would require a separate investigation and decision. No composite schema or rendering algorithm is selected here.

The clean break applies to these changed input names and requiredness: known callers and fixtures migrate explicitly, with no legacy description alias, compatibility mode or fabricated module description. Ordinary context validation enforces the selected required fields; no arbitrary application logic, completeness, successful execution or whole-output architecture certification follows from this decision. The previously approved preservation and block-boundary rules still apply.

The starting-point boundary does not waive approved first-output objectives: template-generated structure, supplied documentation, presentation and whitespace must meet the agreed criteria. It limits the deliverable's completeness, not the care taken with what the templates actually generate. Design will determine the shared schema/template composition and concrete migration inventory. Independent QA remains deferred until all remaining Research decisions have been discussed and recorded.

### Human-approved DTO field-documentation presentation — 2026-10-03

The human approved retaining the current presentation without an automatically repeated Fields summary in the Pydantic DTO class docstring. The class description explains the DTO's purpose and collective contract; supplied field descriptions remain attached to their individual Field definitions. The caller may include cross-field relationships or other additional explanation in class_description. This decision removes no admitted field description or model contract and introduces no content deduplication algorithm.

The legacy rich DTO root repeated the field descriptions in its class docstring; the inspected #460 material did not establish a separate rationale for that presentation change. The current decision explicitly resolves that historical uncertainty. CODE_STYLE does not require an additional automatically generated Fields summary. The hidden legacy DTO root's fabricated descriptions and other old model differences are not restored by this presentation choice.

This is a shipped DTO-template presentation decision within the approved starting-point scope. It does not require the engine to analyze or suppress a caller-authored Fields section in class_description, and the existing caller-content preservation rules continue to apply. No new context shape, runtime formatting step or field documentation mechanism is selected here.

### Human-approved Worker export presentation — 2026-10-03

The human approved leaving the shipped Worker template without an automatically generated __all__ list. The old Worker root declared only its generated class in that list; the current root does not. No separate historical rationale for this exact removal, governing standard requiring the list, or concrete consumer relying on the old wildcard-export behavior was established in the bounded Research.

The decision is explicit: #473 does not restore the old Worker export list. A named import of the generated class remains available. The observed wildcard-import difference is accepted: without __all__, Python's usual public-name selection applies and can include imported names. An export list is not access control, and its absence does not prevent the module owner from declaring a deliberate public export surface during subsequent editing.

This fits the approved valid-starting-point boundary. No export-list context field, class-only public API commitment, mandatory wildcard-import support or blanket export policy for other packages is introduced. Caller-authored export declarations remain subject to the ordinary ownership/preservation boundary. The clean-break decision does not introduce a legacy export mode or bridge. Runtime/enforcement and bounded standards/consumer reconciliation remain separate pending choices.

### Human-directed verification by actual scaffolding and agent inspection — 2026-10-03

The human rejected the producer's proposal and formulation of additional automated content/regression tests as the evidence mechanism for first-output quality. The explicit instruction is to actually scaffold during implementation and have the agent inspect the resulting artifacts manually. This instruction takes precedence over the earlier proposed regression obligations and package-level automation recommendation; the approved quality and presentation objectives themselves remain in force.

For this issue's first-output content, formatting and presentation assessment, use scaffold_artifact through the real pgmcp route and inspect the generated files themselves. Cover all shipped concrete families with minimal and representative filled contexts, plus targeted examples for the already identified whitespace, omission, explicit-empty and caller-boundary questions where needed. Review the first output before subsequent repair: content preservation, documentation ownership, metadata/history, headings/grouping, imports and composed structure, separators, indentation, meaningful internal whitespace and terminal newline. Record the actual contexts, artifact locations, observed findings and correction/re-scaffold outcomes as review evidence. Exact execution sequence remains Planning work.

Do not introduce additional automated content assertions, golden-output snapshots or a permanent content/presentation regression suite to substitute for that inspection. Native tools may supply factual format/lint/syntax evidence through the existing MCP quality tools where relevant; such evidence supports the agent's inspection rather than certifying content or replacing the requested review. This direction does not authorize deleting existing tests or bypassing the active workflow's existing gates. Changes to existing callers/fixtures required by the approved clean break remain a separate migration boundary.

This decision selects the implementation verification method. It does not approve expanding runtime preflights, mandatory formatting/lint dependencies, startup gates or generic schema/template consumption enforcement. Those runtime changes remain unapproved; #476 remains separate. Independent QA is still deferred until the remaining Research decisions are settled.

### Human-approved runtime validation boundary — 2026-10-03

The human approved applying the changed input contracts and agreed render behavior while retaining the existing configured preflights, without additional runtime quality gates. This settles the runtime decision separately from the already selected manual implementation verification method.

Ordinary context validation applies to the approved new required metadata/revision facts and module/class description fields according to their package contracts. The renderer applies the agreed generated whitespace and blank-boundary normalization behavior. Retaining existing preflights does not preserve the old incomplete context or old field names: those boundaries follow the approved clean break.

No extra mandatory Ruff, content or presentation check is added to each scaffold invocation by #473. No new runtime formatter, startup quality gate, automatic dependency installation or generic schema/template consumption enforcement is authorized. Existing report/enforce semantics and configured preflight responsibilities remain with their current owners. Actual scaffolding and manual agent inspection during implementation provide the selected first-output assessment; existing native tools may support it.

This boundary avoids additional per-call dependency, latency and rejection behavior, including broad checks of caller-authored fragments, while preserving the already approved generation objectives. If Design later finds that those objectives cannot be achieved within this boundary, reopen the affected human decision explicitly. Standards and active-consumer reconciliation, plus the human's announced execution addition, remain to be discussed before independent QA is requested.

### Human-approved standards and active-consumer reconciliation — 2026-10-03

The human explicitly approved including directly relevant standards and demonstrably affected active consumers in #473, aligned with the selected contracts. Templates/engine behavior and governing instructions must not enforce competing accounts of the same responsibility. This resolves the bounded reconciliation/migration scope; it does not authorize a general documentation rewrite or restoration of familiar legacy defaults.

Record the agreed document metadata/history responsibilities in DOCUMENTATION_STANDARD and module/class documentation responsibilities in CODE_STYLE, preserving the approved package-specific distinctions. Standards own intent and responsibility; package schemas and templates own their concrete input/render contracts. The differing Python and TypeScript module-description requiredness is an approved package distinction, not a reason to silently homogenize them. Formatting remains grounded in configured native tooling rather than a second conflicting style policy.

Correct demonstrably stale or contradictory guidance directly tied to these surfaces. The bounded Research identified obsolete scaffold context/publication guidance in .agents/workflows/create-issue.md, four related-document link defects and inconsistent version information in the inspected DOCUMENTATION_STANDARD, and candidate stale architecture template-path/schema terminology. Confirm each uncertain mismatch against its current owner before changing it. An instruction correction must preserve existing external-body/envelope ownership and cannot invent a new publication route.

Migrate known active callers, examples and existing fixtures to the approved names, required context and presentation contracts. Adapt existing tests only where their inputs/expectations must follow an approved change; this does not authorize the rejected additional automated content/regression suite. Identify concrete affected heading/link consumers and repair those references. Exact inventory and sequencing belong to Design/Planning; the clean-break strategy rules out legacy aliases, old-schema bridges and dual render modes.

Existing authored documents remain ordinary files and are not mass-converted to the new scaffold format. Unrelated standards improvements, speculative consumers and generic schema/template consumption analysis stay outside #473. Actual scaffolding and manual agent inspection remain the selected implementation verification method, with existing workflow gates and preflights retaining their agreed scope.

All five sequential discussion boundaries now have recorded human decisions. The human announced an additional execution instruction that has not yet been supplied; capture it before final consolidation and independent Research QA. This section records scope approval, not implementation completion, producer GO or review authorization.

### Reopened #476 inclusion decision and trade-offs — 2026-10-03

The human requested a clear, recorded #473 decision on why #476 should or should not be included. This explicitly reopens the original scope separation for discussion; it does not approve merging the issues. Fresh get_issue DTOs for #473, #476 and #460 were fully read: pgmcp://cache/runs/0720de81e95e45518c56a8219dc19632, pgmcp://cache/runs/156579fd2b284958abddd5419eb8f9ae and pgmcp://cache/runs/2e716d57025d4e379b982b508daf1b52. Their descriptions distinguish D-VAL-05 concrete first-output quality from D-VAL-08 generic consumption-analysis research.

The benefit of combining the work is shared discovery across the same package schemas, templates, macros and optional fields. A declared value with no meaningful effect could be missed by examples aimed only at whitespace; reviewing semantic influence can expose incomplete first outputs and reduce repeated onboarding to the same graph. Changed required descriptions and metadata make concrete value preservation relevant to #473.

The cost is a distinct unanswered research problem. #476 must define semantic consumption (direct output, structure, conditions, iteration and justified downstream effects), distinguish absent from uncertain use, investigate aliases/macros/arrays/composed schemas/dynamic access and evaluate false positives. It must separately compare authoring diagnostics, package conformance and startup rejection; its current issue text does not select any of those or require a runtime gate. Ordinary schema validation and a few successful renders cannot establish that generic property. Neither the fresh issue descriptions nor the #473 survey demonstrate a currently shipped ignored-field defect.

| Option | Benefit | Cost / risk and relationship to approved #473 decisions |
| --- | --- | --- |
| Integrate the full #476 research/deliverable into #473 | One investigation can share graph discovery and study first-output correctness alongside generic completeness. | Broadens Research and downstream acceptance to semantic-analysis feasibility and policy before #473 can finish; may require a different strategy than the approved manual inspection and unchanged runtime gates. No analysis/enforcement mechanism is yet approved. |
| Keep #476 independent, with an explicit evidence interface — recommended | Complete the evidenced #473 corrections while supplying actual contexts, expected effects and ignored-value findings to #476. Shared observations remain usable without coupling issue completion. | Generic completeness remains unproven in #473. Coordination must preserve links/evidence so later #476 work does not repeat discovery or overlook concrete findings. |

Recommended proposed boundary: #473 manually checks the admitted values and semantic effects in its actual minimal/representative/targeted scaffolds, including changed metadata/description contracts. A reproduced package-local ignored value relevant to the agreed first-output contract may be corrected within that contract; a broader generic consumption-analysis mechanism, uncertainty/false-positive study or new enforcement policy stays in #476. Trace and document any larger boundary change rather than absorbing it silently.

Decision status: HUMAN-APPROVED on 2026-10-03. The human explicitly selected the second option: keep #476 independent with concrete semantic inspection and shared evidence from #473. The accepted limitation is that #473 does not certify every possible schema path or conditional branch. Do not close or absorb #476 through #473. This decision supersedes the pending discussion state above; the trade-offs remain its rationale.

### Human-directed current-tool practice assessment during implementation — 2026-10-03

The human instructed the implementer to actively assess the correctness and usability of tools changed by #460 while executing #473. The deliverable is concrete documentation of currently existing problems, with reproduction steps, for later triage and coordination. It is not a numeric comparison or exact score against the pre-#460 system, and a current defect is not automatically attributed to #460 as a proven regression.

Use the changed-route inventory in [D-VAL-04](../issue460/deferred-work.md#deferred-work-notice-issue-460-affected-public-route-behavior) as an evidence-backed starting point: scaffold_schema, scaffold_artifact, safe_edit_file, run_checks, run_tests and apply_fixes, plus get_project_plan at its changed readback/transport seam and create_issue at its changed authored-body seam where an admitted bounded assessment is available. Inventory other derived tools when a concrete #460 change or shared execution/content-validation consumer is traced; record that connection rather than declaring all public tools audited because they share a wrapper.

Actively exercise the real pgmcp public routes as part of relevant implementation work and bounded practical probes. Assess admitted input and discoverability, real target selection, defaults/native-argument behavior, diagnostic and failure classification, check/test/fix results, actual file effects, compact presentation, complete cached DTO/readback, actionable errors and recovery/friction. Use normal successful operations and useful negative/problem cases when they inform actual correctness or usability. Read complete cached DTOs; compare claims with native evidence and actual effects, not merely success flags. Use narrow existing test selections where needed to observe run_tests; no new automated content/regression suite follows from this instruction.

Preserve pristine scaffold first-output evidence before edits/fixes. Perform exploratory file mutations on explicit isolated temporary artifacts; relevant production edits remain governed by #473's implementation scope. External issue publication is not required by this documentation task; the create_issue authored-body seam may be assessed using existing controlled evidence without generating a live issue merely as a probe. Unexercised or unavailable routes remain explicit coverage limitations.

Maintain a durable current-tool findings log alongside implementation evidence. For each demonstrated problem or usability friction, record: finding ID; affected route/adapter/shared consumer; current branch/commit and relevant server/native versions; prerequisites and exact admitted call/arguments or minimal context; reproducible steps and necessary input artifacts; expected behavior and its source; actual compact/structured/native result and observed file effect; persisted evidence in addition to transient cache URIs; reproducibility and impact; known cause versus uncertainty; workaround if observed; and links to any existing deferred finding/follow-up for deduplication. Distinguish a demonstrated contract defect, usability friction and an environmental prerequisite problem. A passing observation documents bounded coverage, not exhaustive certification.

Keep corrections within the approved #473 contract; record unrelated check/test/fix or derived-tool repairs for later triage rather than silently expanding implementation. Cross-reference relevant existing D-VAL-01/04/06/07 notices where appropriate. An actual blocker to executing #473 must be surfaced explicitly for disposition. The human's instruction authorizes this active practice assessment and findings deliverable; further issue creation, prioritization and coordinated repair remain subsequent work.

### Possible objectives and strategy questions for discussion

**Discussion state: reopened on 2026-10-02.** The user considers B1–B5 possible objectives, not established guarantees, and requests concrete v2/v3 comparisons plus a standards/issue-460 audit before deciding any strategy. The prior approval question is superseded. The following are discussion candidates, not a complete Approved Strategy. The explicitly approved framing, Architecture/Generic Doc outcomes and no-legacy clean-break strategy above take precedence where they overlap these earlier candidates; B4 records the selected clean-break strategy; B1 now has the qualified human approval above. The independent whitespace objective now includes the four approved generated-spacing/EOF criteria above. The approved block-boundary normalization decision settles caller-owned blank suffixes; remaining presentation/enforcement decisions remain open. Each boundary has independent compatibility, cost/risk and consumer consequences. No fix structure, global whitespace flags, formatting algorithm or implementation sequence is selected in Research.

| Boundary | Recommended strategy | Alternative and trade-off | Compatibility, cost and risk |
| --- | --- | --- | --- |
| B1 — Python first-output quality | APPROVED BOUNDED OBJECTIVE, with independent whitespace assessment: establish a shipped-package conformance objective: the minimal/representative and meaningful boundary cases produce Ruff-format-clean and Ruff-lint-clean template-generated structure under the configured native baseline when caller fragments themselves satisfy that baseline. Explicitly cover generated imports, absent/filled optional blocks and long composed expressions. | Keep syntax-only possible objectives: low change cost, manual cleanup remains. Promise every schema-valid complete output is clean: much higher cost, cannot be honest without restricting or transforming raw caller fragments, arbitrary identifiers and dependencies. | Existing context shape/API and source semantics remain; generated whitespace/expression layout may change. Moderate package/test maintenance. Quality does not mean dependency resolution, successful execution or Mypy/Pyright certification. |
| B2 — Authored-content ownership | APPROVED: trim empty/space-tab-only boundary lines of inserted code/document blocks; preserve internal code/prose/fence content, meaningful spaces, literal/data values and declared ordered records/states. Renderer owns structural indentation, safe encoding, generated joins and EOF. | Whole-output formatting or context-wide trimming was not selected; it can change caller internals and data values and would reopen this decision. | Clean break for changed block-boundary output; no legacy mode. No extra padding-specific errors/instructions, no general .strip(), no body refactor/lint repair and no implicit widening of input validation. |
| B3 — Markdown, tracking text and TypeScript presentation | APPROVED generated spacing/EOF slice: one empty separator between independent generated Markdown blocks, no omitted-block residue or generated whitespace-only lines, and one terminal newline without additional generated blank lines. Python spacing follows the configured syntax-aware formatter. Preserve authored whitespace inside prose/fences/bodies. Remove purely mechanical carrier labels only where adjacent structure already communicates their role; retain real evidence/source/contract distinctions. Apply intentional generated spacing and trailing-newline cleanup to commit/TypeScript, without inventing absent format/lint tooling commitments. | Whitespace-only correction has lower editorial risk but leaves redundant field narration. A global text formatter or broad heading redesign has higher risk to raw Markdown/code fences, links, provenance and anchors. | Approved Architecture/Generic Doc heading changes follow the clean-break strategy; explicit absent/empty semantics remain. Other editorial choices still need representative multi-carrier cases. The approved framing objective replaces the former title-only minimal document input without inventing validation success. |
| B4 — Public compatibility, source identity and distribution | APPROVED CLEAN BREAK for changed #473 presentation/heading and required document-context boundaries: new contracts only, no legacy mode/schema/aliases/bridge. Existing authored files remain; update demonstrably affected active consumers and references. | A dual old/new output or context path was considered and explicitly rejected by the human because it adds maintenance and preserves legacy behavior. | Caller/fixture/link migration cost is accepted. Exact new field shape belongs to Design. Package identity, provenance, fingerprint and distribution retain their existing owners; no unrelated protocol redesign follows from this approval. |
| B5 — Verification/enforcement and #476 boundary | HUMAN-DIRECTED VERIFICATION: actually scaffold and manually inspect first outputs during implementation; record concrete artifacts and findings. No additional automated content/regression tests. Native evidence can support inspection through existing tools. APPROVED RUNTIME BOUNDARY: apply the changed input contracts and render behavior with existing configured preflights and no additional runtime quality gates. Generic schema/template consumption analysis remains in #476. | Mandatory new runtime/startup format, presentation or consumption gates would add dependency, availability, performance and rejection impact; no such expansion is approved. | Existing tests/gates remain governed by the active workflow. No new content/snapshot suite, automatic dependency installation, global formatter or blanket consumption validator follows from this decision. |

The recommendation is bounded enough to preserve portable caller-owned fragments while making generated output useful without subsequent repair. The objectives and their scope must first be discussed against concrete comparisons and governing standards. A later strategy decision must identify each affected boundary explicitly. If Design discovers a required schema/anchor change, a whole-output formatter requirement, or a stronger universal objective, it must reopen that boundary instead of expanding this approval implicitly.

### Corrected-behavior and manual verification boundary

The human-directed implementation evidence is actual first-output scaffolding followed by manual agent inspection, as recorded above. Inspect the real shipped-package path and retain the untouched first output as evidence before repair. Review the relevant semantic and presentation cases: required/optional imports, ordinary import mixtures, omitted and explicitly empty carriers, methods/constructors/fixtures and their spacing, modest multi-option model fields/examples that require wrapping, and minimal/filled documents with useful grouping. The review must identify generated defects separately from caller-authored content and inspect preservation of input values, body semantics, encoding, link targets and first-line provenance. These are inspection dimensions, not a mandate for new automated assertions or regression tests.

A generated seam blank-line bound is not a global ban on consecutive blank lines in caller code/prose/fences. A lint-clean claim must state its native configuration and context assumptions; arbitrary unused imports, invalid naming, long raw expressions, absent dependencies and authored check states remain outside the template objective. The authorized native tooling follow-up resolves TypeScript/Commit workspace availability and re-executes the eight existing native contract tests successfully. Raw TypeScript syntax, provisioned strict fixture behavior and Commit message validity remain distinct evidence domains; none establishes an agreed presentation or whitespace objective.

### #476 interface and excluded work

[Issue #476](https://github.com/MikeyVK/phase-gate-mcp/issues/476) owns generic schema-to-template consumption analysis, including structural versus conditional influence, AST/macros/aliases/dynamic paths, uncertainty and policy. The current [TemplateInputValidator](../../../mcp_server/services/template_catalog.py) explicitly checks declaration linkage rather than proving all value-dependent behavior. #473 can supply package-specific first-output examples and any future concrete ignored-value reproduction as evidence, but may not assume that every declared property influences output, build a generic reverse-consumption analyzer, or enforce startup rejection.

No concrete missing-field symptom is established by this survey. Metadata/sample evidence strings are caller-authored; no produced example status certifies actual Research/Validation progress. No production/template fix, Design, Planning, broad Validation, epic lifecycle change or #476 implementation is part of this Research pass.


## Approved Strategy

**Human-approved boundaries, consolidated on 2026-10-03; independent Research review pending.** The explicit decisions below supersede earlier discussion candidates and pending labels in this document and the dated comparison reports. Observed outputs, native receipts and historical #460 reasoning remain evidence, not current approval or universal guarantees. All sequential choices and the two execution additions have been discussed and recorded.

| Boundary | Approved outcome / strategy | Limits and affected consumers |
| --- | --- | --- |
| Useful starting point | Shipped concrete scaffolds provide valid, carefully generated starting points for further editing. Retain one main class per call in the six class-generating Python families. | No complete application/end-product promise, structured multi-main-class composition, dependency resolution, execution success or universal typing/architecture certification. |
| Python generated quality | Minimal/representative and meaningful boundary examples must have native format/lint-clean template-generated structure under the configured Ruff baseline when caller fragments themselves satisfy it. Inspect imports, omitted/filled joins, indentation and composed expressions. | Preserve arbitrary caller bodies and data; no refactoring of supplied code or whole-output cleanliness claim for arbitrary fragments. |
| Generated whitespace / EOF | Python spacing follows the configured syntax-aware baseline. Independent generated Markdown blocks have one empty separator, including Issue/PR; omitted blocks leave no residue and no generated indentation-only blank lines remain. Every family has one terminal newline without generated surplus EOF blank lines. | Preserve caller-owned internal code/prose/fence spacing and meaningful spaces. A separator rule does not prohibit legitimate internal blank lines. No new TypeScript formatter/linter baseline is selected. |
| Text-block boundary ownership | Remove empty/space-tab-only boundary lines from inserted text blocks; renderer owns structural indentation, encoding, separators and EOF. | Preserve internal text, meaningful spaces and literal/data values. No recursive general trimming, padding-specific errors/instructions or changed absent/explicit-empty validation semantics. Exact generic mechanism belongs to Design. |
| Seven full-document families | architecture, research, design, planning, validation_report, reference and generic_doc require visible explicit status, document version and last-updated date, plus at least one caller-supplied revision with version/date/author/change; header/current revision agree. | No fabricated lifecycle facts, dates, authors or history. Provenance remains separate. Use established tiered template/schema composition to satisfy DRY; generic engine remains artifact-agnostic. Issue/PR/Commit retain their distinct contracts. |
| Architecture / Generic Doc presentation | Retain Concepts and separate Constraints; show hierarchical subsection numbering; remove mechanical Diagram/Subsections labels; concise decisions use a comparison table while long explanations remain readable. Generic custom sections appear directly, without Sections/Content/Bullets/Checklist wrappers. | Preserve supplied order, grouping, diagram/subsection association, constraints, long text, list/check state and meaningful headings. Heading/anchor changes follow the clean break. |
| Python documentation | For python_class, python_protocol, python_pydantic_config, python_pydantic_dto, python_adapter and python_worker, required class_description replaces description and module_description becomes required at its own file scope; no fallback between them. | Explicit identical descriptions are allowed; no text-equality deduplication. The two pytest families are outside this naming/requiredness decision. Member documentation retains its own scope. |
| TypeScript documentation / constructor | Required class_description replaces description; optional module_description renders only its supplied content, without fallback or deduplication. Ordinary constructor assignments are consecutive; one separator precedes a distinct optional block; no inner brace-edge blank lines; retain the empty-field constructor. | Preserve supplied types, values, readonly/optional semantics and explicit absent/empty presence behavior. No automatic legacy alias or extra class composition. |
| DTO / Worker presentation | Keep field descriptions in Field definitions without an automatic repeated Fields summary in the DTO docstring. Worker does not generate automatic __all__. | Caller may supply additional class explanation or later declare exports. Named imports remain available; the legacy wildcard-import difference is accepted. |
| Compatibility / migration | Clean break for changed #473 input names/requiredness, output headings and presentation. Update known active callers, examples, existing fixtures/tests and concrete affected references. | No legacy alias/schema/mode/bridge or parallel output suite. Unknown external consumers must adopt the new contracts. Existing authored documents remain; no mass conversion. Source identity, provenance and distribution retain current owners. |
| Implementation verification | Actually scaffold through pgmcp and manually inspect untouched first outputs; retain contexts, artifacts, findings and re-scaffold outcomes. Native MCP checks may supply supporting factual evidence. | No additional automated content/regression tests or snapshot suite. Existing tests and workflow gates retain their functions; adaptation for approved contract migration is allowed. |
| Runtime boundary | Apply agreed new input contracts and renderer behavior with existing context validation, configured preflights and report/enforce responsibilities. | No additional per-call Ruff/content/presentation gate, new runtime formatter, startup quality gate or automatic dependency installation. |
| Standards / active consumers | Align directly relevant CODE_STYLE/DOCUMENTATION_STANDARD guidance and demonstrably stale affected instructions/examples/links with the agreed contracts. Confirm uncertain terminology mismatches before editing. | Correct the relevant link/version/instruction defects; keep package-specific distinctions. No unrelated standards rewrite, speculative consumer migration or restoration of legacy defaults. |
| #476 interface | Keep #476 independent. #473 manually inspects actual admitted values and effects and passes reproducible ignored-value findings/context evidence to #476. | Generic consumption analysis, exhaustive path/branch claims, uncertainty/false-positive research and new analysis/enforcement policy remain in #476. A demonstrated relevant package-local defect can be corrected within #473's approved contract; larger boundary changes require explicit disposition. |
| Current-tool practice assessment | Actively assess correctness/usability of #460-changed check/test/fix/scaffold/edit routes and traced derived consumers during implementation. Maintain durable reproducible findings for later triage/coordination. | No exact pre-#460 score, retrospective regression claim without evidence, new automated content suite or silent repair of unrelated tool defects. Record bounded coverage, environmental limitations and links to existing follow-ups; surface actual #473 blockers. |

## Expected results

Design can define the correction within these approved outcomes and architecture constraints, using the 19-family survey, v2/v3 comparisons, targeted whitespace examples and factual native evidence. It must define shared composition and the precise affected-consumer inventory without turning Research into an implementation plan.

Implementation must produce the agreed first-output improvements and demonstrate them through actual scaffolding and manual inspection. It must also document current tool problems/friction with exact reproduction steps, expected/actual behavior, durable evidence, impact and known uncertainty for subsequent triage. Existing native tools and workflow verification support these observations at their configured scope.

Research approval does not certify the proposed implementation, prove generic consumption completeness or close #476. A later incompatible discovery must reopen the affected human decision explicitly. No implementation or Design work has been performed in this Research phase.

## Open research questions

- No unresolved human strategy choice remains in the discussed #473 boundaries. Independent Research QA is requested against this consolidated set.
- Downstream Design must confirm uncertain stale terminology, the concrete consumer migration inventory and shared schema/template composition.
- Planning must make the manual scaffold inspection and practical tool-assessment deliverables explicit, with bounded cases and reproducible findings; no new automated content/regression suite.
- Known limitations: authorized legacy renders are not full old MCP-pipeline parity; raw TypeScript syntax does not certify caller dependencies; cached resources are transient; current generic consumption completeness remains unproven and owned by #476.
- Implementation, full Validation and unrelated tool repairs remain downstream or separately triaged work.

### Bug / Research Hand-over

#### Scope

- Investigated all 19 shipped concrete packages with minimal and representative filled context, attributing generated defects separately from caller content.
- Compared authorized legacy/current renders and inspected #460 decisions and governing standards.
- Recorded explicit human choices for output quality, documentation, presentation, clean break, manual verification, runtime gates, standards/consumer reconciliation, independent #476 work and active current-tool practice assessment.
- Excluded production/template/schema/test modifications, Design/Planning, full Validation and generic #476 analyzer implementation.

#### Deliverables

- [Research and consolidated Approved Strategy](research.md#approved-strategy)
- [First-output survey](first-output-survey.md)
- [Python Class baseline comparison](python-class-comparison.md)
- [Design document comparison and rationale audit](design-document-comparison.md)
- [Document-family comparison](document-family-comparison.md)
- [Python-family comparison](python-family-comparison.md)
- [Independent whitespace examples](whitespace-comparison.md)
- [Tracking/TypeScript comparison](tracking-typescript-comparison.md)
- [Native tooling follow-up](native-tooling-follow-up.md)

#### Evidence

- 38 untouched current first outputs: 16 Python syntax preflights passed, all 16 needed Ruff formatting, 15 lint findings; 18 Markdown preflights passed while generated blank runs reached 4–21.
- Authorized v2/v3 examples preserve original bytes/hashes and stated old-renderer/pipeline limitations. Targeted whitespace examples distinguish generated joins from authored internal spacing.
- After authorized native installation, 12 raw TypeScript/Commit rechecks produced 8 passing and 4 failing results; old TypeScript syntax defects and old Commit comparison-envelope failures are separately explained.
- Existing template integration evidence: 85 passed with one existing warning; the narrow eight TypeScript/Commit tests also passed with one existing warning. These results do not certify presentation and introduce no new content/regression tests.
- Complete native DTOs and decisive logs are persisted in the source reports. Research Markdown checks/commit identity are supplied with the external review request.
- Human-approved strategy is consolidated above; producer evidence is not a QA verdict.

#### Open Work

- Independent Research review.
- Downstream Design/Planning work and the implementation inspection/tool-findings deliverables described above.
- Generic schema/template consumption analysis remains #476; unrelated demonstrated tool defects go to subsequent triage/coordination.

#### Review Request

- Review requested.

## Research review verification — 2026-10-03

The narrow nine-document markdown_link_review completed with run_status=passed using Lychee 0.24.2 and configured arguments --offline, --cache=false and --include-fragments. Complete DTO pgmcp://cache/runs/d538bd5c2b1646109b973be679cec3b5 was read. Durable result: 307 occurrences, 184 unique links, 300 successful, 7 excluded and zero errors. Exclusions were four GitHub issue links and three pgmcp cache references; this offline check does not certify external reachability. This section was added after that run and contains no new Markdown links.

An initial combined request for markdown_document and markdown_links was rejected before native execution because markdown_document is content-only and unsupported for selection: error_code=selection_invalid, reason=selection_unsupported, check_id=markdown_document, results=[]. Complete DTO pgmcp://cache/runs/f7c8d4b1c2f2486ba16308e86e501ca3 was read. That rejected selection supplies no native pass/fail evidence. The validated Research safe-edit itself passed its selected markdown_document preflight; the standalone link-review result above is separate evidence.

Pre-commit reality check: the deliverable is the factual survey/comparison evidence and explicit strategy boundaries for Design, not repaired scaffold quality or implementation certification. No production, template, schema or test files changed; no additional content/regression tests were introduced. Original first outputs and documented old-renderer limitations remain the evidence baseline. The active workflow remains Research with independent review pending.

## References

- [First-output survey evidence](first-output-survey.md)
- [Python class v2/v3 comparison and standards assessment](python-class-comparison.md)
- [Independent Python and Markdown whitespace examples](whitespace-comparison.md)
- [Final Issue/PR/Commit and TypeScript comparison](tracking-typescript-comparison.md)
- [Authorized native tooling installation and fresh evidence](native-tooling-follow-up.md)
- [Code Style Guide](../../coding_standards/CODE_STYLE.md)
- [Documentation Standard](../../../docs/coding_standards/DOCUMENTATION_STANDARD.md)
- [Architecture Principles](../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Issue #473](https://github.com/MikeyVK/phase-gate-mcp/issues/473)


## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.3 | 2026-10-02 | @imp researcher | Record human-approved Architecture and Generic Doc presentation objectives; identify unresolved context and anchor migration boundaries. |
| 0.4 | 2026-10-02 | @imp researcher | Record the human-approved clean break without legacy compatibility for changed presentation and document-context boundaries. |
| 0.5 | 2026-10-02 | @imp researcher | Index the remaining Python-family comparisons, sixteen raw legacy renders and fresh fourteen-file native quality evidence. |
| 0.6 | 2026-10-03 | @imp researcher | Record qualified Python native quality approval and independent Python/Markdown whitespace assessment, with eight untouched examples; numerical criteria remain open. |
| 0.7 | 2026-10-03 | @imp researcher | Complete all nineteen concrete family comparisons; record tracking/TypeScript rationale, independent whitespace, native availability and the bounded active-consumer mismatch. |
| 0.8 | 2026-10-03 | @imp researcher | Resolve authorized TypeScript/Commit prerequisites, preserve raw hashes, confirm old syntax versus Commit framing causes and record eight passing native contract tests. |
| 0.9 | 2026-10-03 | @imp researcher | Record human-directed sequential boundary decisions and defer independent QA until those decisions are complete. |
| 0.10 | 2026-10-03 | @imp researcher | Record four human-approved generated-spacing/EOF objectives; advance sequential discussion to caller-content ownership and retain pending boundaries. |
| 0.11 | 2026-10-03 | @imp researcher | Record approved text-block boundary trimming and caller/data preservation; advance discussion to remaining presentation choices. |
| 0.12 | 2026-10-03 | @imp researcher | Record approved TypeScript constructor assignment/block/brace spacing and retained empty-field constructor; continue presentation discussion. |
| 0.13 | 2026-10-03 | @imp researcher | Record human-selected TypeScript class_description naming under clean break; keep module fallback behavior explicit and pending. |
| 0.14 | 2026-10-03 | @imp researcher | Record approved TypeScript class/module documentation separation without fallback, preserve explicitly supplied duplicate/empty content and continue with Python documentation. |
| 0.15 | 2026-10-03 | @imp researcher | Verify six live one-main-class contracts and record human-raised module/class cardinality question; Python requiredness and scope remain pending. |
| 0.16 | 2026-10-03 | @imp researcher | Record approved one-main-class starting-point scope and explicit required Python module/class descriptions; retain separate multi-class scope and remaining presentation decisions. |
| 0.17 | 2026-10-03 | @imp researcher | Record approved DTO field descriptions without an automatically repeated Fields docstring summary; continue with the Worker export choice. |
| 0.18 | 2026-10-03 | @imp researcher | Record approved Worker presentation without an automatic __all__, accepting the bounded wildcard-import difference; continue with verification/enforcement. |
| 0.19 | 2026-10-03 | @imp researcher | Replace proposed additional automated content/regression testing with human-directed actual scaffolding and manual agent inspection during implementation; keep runtime changes unapproved. |
| 0.20 | 2026-10-03 | @imp researcher | Record approved changed input contracts/render behavior with retained preflights and no additional runtime quality gates; continue standards/consumer discussion and reserve execution addition. |
| 0.21 | 2026-10-03 | @imp researcher | Record approved bounded standards and active-consumer reconciliation; mark sequential boundaries decided and await announced execution addition before consolidation/QA. |
| 0.22 | 2026-10-03 | @imp researcher | Reopen explicit #476 inclusion decision with evidenced trade-offs; record human-directed active current-tool practice assessment and reproducible findings for later triage. |
| 0.23 | 2026-10-03 | @imp researcher | Record explicit human approval to keep #476 independent with shared evidence; consolidate all Approved Strategy boundaries, execution additions and outcome-neutral Research hand-over for independent review. |
