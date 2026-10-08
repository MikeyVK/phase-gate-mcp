<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 121 — Minimal structure-preserving artifact edit review

**Status:** Draft — tool-enforced strategy pending  
**Version:** 0.3  
**Last Updated:** 2026-10-08

## Purpose

Present the least heavy architecturally clean response to the structure-preservation finding consolidated from issue483.

## Scope In

Current edit/profile/provenance boundaries, all template-generated artifact formats, original Jinja source association, existing checker feasibility, package-owned preservation requirements, options and strategy decisions.

## Scope Out

Implementing safeguards before approval, new editing APIs, designing a universal Jinja/AST output-contract framework, generic undo, universal rewrite restrictions, text/newline policy changes, implementation sequencing and a new architecture.

## Problem Statement

A native-passed edit and retained template provenance do not establish that required artifact structure and information remain usable. The owner wants the lightest architecturally clean option, not a new editing architecture.

## Goals

- Separate demonstrated structural damage from valid refinement.
- Identify authoritative requirements without freezing generated text or moving package knowledge into generic server code.
- Recommend a minimal solution and make its review-versus-runtime guarantee explicit before strategy approval.

## Background

Issue121 now consolidates the deferred finding from #483. The historical revision-table repair removed two blank lines between the 0.3/0.4/0.5 rows; it is a bounded example, not a measured incident rate. The active issue permits an instruction-based conclusion, but the owner has now rejected that as sufficient and requires protection through pgmcp tooling. Historical introspection/API sketches remain unapproved design assumptions.

## Findings

### Existing tooling boundary

| Surface | Current facts | Reuse or limitation |
| --- | --- | --- |
| EditOperation / ScaffoldOperation | Construct proposed content, run a configured profile before persistence, interpret factual results, and block negative required results under enforce. | Existing no-write behavior can enforce an additional contentcheck. No new editing engine or operation mode is required for this route. |
| CheckService / adapter wire | A profile can contain multiple checks. Each receives proposed content or its owned scratch file, target_path, configured args and execution context. | A final-content contract check fits. The original snapshot is not part of this wire contract: before/after comparisons are not a free existing capability. |
| Profile selection | Explicit package ID overrides original recognized metadata, then extension fallback. Package policy chooses output_profile. | Associate the selected package with the configured structural obligation; do not let rewritten provenance choose a weaker contract. .md alone does not identify a template contract. |
| EnforcementDecorator | Pre/post actions receive tool parameters; they do not share the operation's constructed proposal and checked original snapshot. | A decorator would duplicate proposal construction/reads or need another integration boundary. Post-write checks cannot provide the requested pre-write protection. |
| TemplatePolicy / suite identity | Strict policy currently admits only output_profile and persistence. Extra private generation sources must be reachable from the admitted generation graph. policy.yaml is excluded from generation identity but included in operational component state. | Adding an arbitrary rules file is not automatically safe/admitted. A small generic policy extension carrying opaque native checkconfig is a candidate; do not smuggle output rules into the input context schema or whitelist a tool-specific filename in generic code. |

### Cross-format requirement and original Jinja source

The owner explicitly requires tooling for all template-generated content, including code, rather than a Markdown-only safeguard. The previous Markdownlint recommendation is therefore insufficient as the issue-wide solution. Existing pre-write contentcheck execution is reusable; the missing capability is a checker that distinguishes permitted development from loss of required template structure.

Jinja renders text from source, environment and caller context. Its documented Meta API exposes referenced variables/templates, not a post-generation preservation contract; dynamic references can be unresolved statically. Inspection of the installed python_class template gives a concrete counterexample to exact equality: methods are generated with raise NotImplementedError and an empty class can contain pass. Replacing these with working implementation is expected development, although the placeholder is literal template output. The TypeScript DTO also builds conditional declarations and assignments through macros, loops and filters. The original renderer alone does not declare which emitted elements must remain invariant after generation.

There are three distinct guarantees:

| Check | Required information | Limit |
| --- | --- | --- |
| Exact regenerated output comparison | Original source graph, renderer environment/custom filters, original context and reproducible generation | Rejects legitimate changes to generated placeholders and authored content. It is suitable only for intentionally immutable outputs. |
| Match some possible render of the original template | A supported inverse/render-language analysis and suitable context constraints | Does not establish required post-edit semantics. Flexible content slots admit many outputs; literal generated placeholders can still be intended to change. |
| Preserve declared artifact obligations | Explicit required/optional/conditional/editable semantics associated with the source package | Can admit development and reject structural damage, but these semantics must be supplied rather than inferred as a universal Jinja guarantee. |

Canonical id/pv/pf/sf metadata is generation provenance. It does not store the original context or provide an archived source registry. Selecting the current installed package by ID does not prove that its graph is the original graph. Source mismatch or unavailability must remain visible; a current-contract policy and historical-source conformance are separate choices.

### Existing tool investigation

This is a documentation/source feasibility assessment, not a native execution witness. No drop-in checker for the complete installed Jinja suite and permitted post-generation edits has been established. That is a bounded research finding, not proof that no such tool exists anywhere.

| Tool / API | Verified purpose | Fit for the requested check |
| --- | --- | --- |
| Jinja Meta API | Inspect variables and referenced templates in the source AST. | No documented output-conformance or editable-region semantics. Reusing this alone would reopen the earlier introspection problem. |
| jinja2schema | Infer expected input-context types and a JSON Schema for input. | Validates a different boundary; does not validate edited emitted artifacts. |
| TTP | Extract structured data from text using authored parsing templates and matching expressions. | Cross-format text parsing is possible, but its templates are a separate matching language. Existing Jinja inheritance/macros/filters are not directly a TTP validation contract. Extraction success alone is not full-content acceptance. |
| jinja-reverse | Build derived templates by extracting block contents from samples. Source uses regex for simple block syntax and treats surrounding text literally. | Does not execute the installed Jinja graph or return a complete conformance verdict. No-match samples can still produce an extends-only output; loops/expressions/filters and edited code semantics are not covered. |
| Copier | Regenerate versioned Jinja projects from stored answers and merge template updates with user changes. | Useful for update management, not a pre-write structural acceptance check. Requires source/answer lifecycle absent from current provenance. |
| Markdownlint custom rules | Apply owned predicates to parsed Markdown. | Possible format-specific implementation component only. Neither all-artifact coverage nor direct original-Jinja validation. |

Genji was also checked: it extends Jinja rendering with LLM generation calls and format escaping, rather than checking an independently edited artifact against its source. It is not a solution to this acceptance boundary.

### Proportionate direction, still pending

Keep generic edit/scaffold orchestration responsible for constructing, validating and conditionally persisting content. Keep adapter code responsible for invocation/result translation. Template-specific preservation meaning belongs with the template package; substantive checking belongs in a checker/native extension.

A bounded source-associated contentcheck with explicit preservation requirements remains a feasible direction to investigate across formats. Existing parsers can help assess particular artifact structures, but a thin adapter cannot manufacture a complete Jinja conformance guarantee. A shared text check can verify declared anchors/regions, while semantic code/document constraints may require format-aware inspection. This distinction must be resolved before selecting a tool or proposing a rule language. Neither a universal output-contract framework nor a new generator is approved.

If automatic interpretation of the original Jinja source is essential, a source-aware LLM checker is another research option. It would offer contextual judgments rather than deterministic structural proof and adds model invocation, repeatability and operational availability questions. No such implementation has been selected or demonstrated here.

### Existing enforcement boundary

Under enforce, a selected required contentcheck failure prevents persistence. Existing report permits failed checks to be written while retaining failure facts; making structural failure block report is a separate owner decision. Missing association, unavailable source/config and unavailable execution cannot be presented as successful template conformance.

The current check transport contains proposed content/its scratch file, target_path, configured args and execution context. It does not carry original text, historical source graph or original render context. Fixed source/config references can potentially be supplied through existing configured args; automatic source-bound resolution needs an explicit ownership and identity decision. Preserve factual guarantees rather than claiming all required inputs already exist.

### Blast radius and evidence

No implementation strategy is approved. The existing pre-write executor offers a small integration boundary, but cross-format checker selection, preservation semantics and source association remain open. Any package metadata extension must stay generic/opaque to server orchestration; no package names, language predicates or native-specific rule schemas belong in generic Python.

Behavioral evidence should distinguish permitted edits from structural damage and verify actual persistence/results. Reuse meaningful existing consumer/enforcement tests and add only missing coverage for the selected behavior; no full-text snapshots, wording inventories or retired checker regressions. The Markdown probes below establish a real gap but cannot establish cross-format coverage or candidate-checker success.

#483's link checker replacement, #476's package release review, #470's text/newline/span/race work and #491's planning-data contracts remain separate.

## Questions

- Can a small explicit preservation contract satisfy the requirement, or must the checker interpret original Jinja source directly? What constitutes permitted development for code and documents?
- Should checks enforce a selected current package contract or require availability of the exact generation source? How should missing/mismatching source be handled?
- Does report retain its existing semantics or must structural failure also block report writes?
- After these semantics are chosen, establish a pinned native implementation and a small cross-format feasibility witness before recommending Design.

## References

- [Editing execution and persistence](<../../../mcp_server/services/edit_operation.py>)
- [Original-source profile selection](<../../../mcp_server/services/edit_construction.py>)
- [Provenance recognition](<../../../mcp_server/services/artifact_header_reader.py>)
- [Package identity and limitations](<../../reference/template_metadata_format.md>)
- [Normal template use](<../../reference/TEMPLATE_LIBRARY_USAGE.md>)
- [Package review procedure](<../schema-template-maintenance.md#develop-and-release-a-package>)
- [Documentation requirements](<../../coding_standards/DOCUMENTATION_STANDARD.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Research template](<../../../.pgmcp/template_suite/research/template.jinja2>)
- [Shared document structure](<../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2>)
- [Existing original/profile behavior tests](<../../../tests/mcp_server/unit/services/test_edit_construction.py>)
- [Existing public edit behavior tests](<../../../tests/mcp_server/integration/test_edit_public_v3.py>)
- [Current validation bindings](<../../../.pgmcp/config/checks.yaml>)
- [Authoritative instruction model](<../../reference/copilot-agent-instructions-model.md>)

- [Existing contentcheck executor](<../../../mcp_server/execution/check_service.py>)
- [Existing proposed-content wire](<../../../mcp_server/execution/content_input.py>)
- [Tool-level enforcement boundary](<../../../mcp_server/core/decorators/enforcement_decorator.py>)
- [Strict current package policy](<../../../mcp_server/config/schemas/template_suite.py>)
- [Generation-source admission and closure](<../../../mcp_server/services/artifact_identity.py>)
- [Operational package component identity](<../../../mcp_server/services/template_components.py>)
- [Markdownlint custom rule contract](<https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md>)
- [Markdownlint CLI2 configuration and input](<https://github.com/DavidAnson/markdownlint-cli2>)
- [Built-in Markdownlint rules](<https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>)
- [Observed CLI2 main metadata, not a selected release](<https://raw.githubusercontent.com/DavidAnson/markdownlint-cli2/main/package.json>)
- [Jinja Meta API and renderer context](<https://jinja.palletsprojects.com/en/stable/api/#the-meta-api>)
- [jinja2schema input-context purpose](<https://jinja2schema.readthedocs.io/en/latest/>)
- [TTP matching-template language](<https://ttp.readthedocs.io/en/latest/Writing%20templates/>)
- [jinja-reverse extraction implementation](<https://github.com/gabihodoroaga/jinja-reverse/blob/master/reverse.py>)
- [Copier update and stored-answer lifecycle](<https://copier.readthedocs.io/en/stable/updating/>)
- [Genji generation and escaping](<https://pypi.org/project/genji/>)
- [Python class scaffold and intentional stubs](<../../../.pgmcp/template_suite/python_class/template.jinja2>)
- [TypeScript DTO scaffold and conditional structure](<../../../.pgmcp/template_suite/typescript_dto/template.jinja2>)

## Approved Strategy

Pending owner decision. The owner requires a tooling solution covering all template-generated artifact formats and rejects instruction-only review or Markdown-only coverage as sufficient. The least-heavy/no-new-architecture constraint remains binding.

| Boundary | Candidate to assess | Approval state |
| --- | --- | --- |
| Public edit/scaffold and validation policies | Reuse existing contentcheck/no-write machinery; stronger report protection requires an explicit decision. | Pending |
| Native checker and adapter ownership | Check all applicable artifact formats in the substantive tool; keep invocation/results in a thin adapter. No complete off-the-shelf original-Jinja checker has been verified. | Pending |
| Package preservation semantics | Explicit source-associated requirements versus contextual interpretation of original Jinja; do not silently infer permanent structure from generated literals. | Pending |
| Source identity and older/manual artifacts | Decide current-contract versus exact original-source acceptance and unavailable/mismatching source behavior. No guessed association, automatic restamping or compatibility emulation. | Pending |
| Behavioral proof | Small cross-format permitted/damaged edit and persistence coverage; reuse useful tests, avoid full-text/wording matrices. | Pending |

## Expected Results

A selected checker must permit intended code/document development and identify loss of required structure across the applicable template-generated formats. Exact regeneration, source compatibility and preservation of declared obligations must not be conflated. Evidence must identify the actual source/contract association, check scope and native outcome. Enforcement/report semantics and missing-source behavior remain pending; no new tool postconditions are implemented here.

## Evidence

### Historical table damage was a small edit-level defect

Commit ab189a83fb1511c02f73c93a442d4d1f257345c5 removed exactly two blank lines between existing revision rows. The facts remained present while table continuity was lost. Current #483 Research is corrected; no historical document was edited here.

- [Exact revision-table correction](<https://github.com/MikeyVK/phase-gate-mcp/commit/ab189a83fb1511c02f73c93a442d4d1f257345c5>)

**Invocation:** Read-only git show --format= --unified=3 ab189a83fb1511c02f73c93a442d4d1f257345c5 -- docs/development/issue483/research.md

**Observed Result:** Two deleted blank lines, no revision fact changes.

### Current enforce validation admits damaged and valid structural variants alike

Scaffold one disposable research artifact; retain its original text BASE. Each of the three public edits uses operation={op:'rewrite',content:<BASE with the stated change>}, validation='enforce', no explicit template_id. A: insert one blank line immediately before '| 0.2 |' in Version History. B: remove the visible Status/Version/Last Updated block, retaining first-line provenance. C: remove the optional Findings heading/prose and replace the Problem Statement with 'Link acceptance and reviewed artifact conformance are distinct claims.', retaining valid metadata/history. Reconstruct every variant from BASE rather than carrying damage into later cases. The final on-disk file is C.

- [Editing execution and persistence](<../../../mcp_server/services/edit_operation.py>)
- [Original-source profile selection](<../../../mcp_server/services/edit_construction.py>)
- [Research template](<../../../.pgmcp/template_suite/research/template.jinja2>)
- [Shared document structure](<../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2>)
- [Current validation bindings](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** scaffold_artifact(artifact_type="research", file_name="edit-proof.md", target_path=".pgmcp/temp/issue121-research", force_target=true, validation="enforce", context={"title":"Issue 121 structural edit probe","problem_statement":"Native link acceptance does not establish artifact conformance.","goals":["Compare structural damage with intentional valid refinement."],"findings":"Optional findings prose can be removed when not needed.","document_metadata":{"status":"Research probe","revisions":[{"version":"0.1","date":"2026-10-08","author":"@imp researcher","change":"Initial disposable probe."},{"version":"0.2","date":"2026-10-08","author":"@imp researcher","change":"Second row for the table boundary probe."}]}}); safe_edit_file(path=".pgmcp/temp/issue121-research/edit-proof.md", operation={"op":"rewrite","content":<variant>}, validation="enforce")

**Observed Result:** All three: success=true, written=true, content_changed=true, validation_status=passed, selected_source=metadata, template_id=research, profile_id=markdown_link_review. Lychee 0.24.2 / adapter 2.0.0 returned native exit 0, zero links and zero errors, configured args --offline --cache=false --include-fragments. Correct link acceptance is not structural approval. Supplemental receipts A a946a9b38c2d4228b03be91ad3aa11de, B 2389d554caaa40f7a4ef20cb37849132, C 2d15d206f2f443c2b25b2453a673ed86. Probes are ignored temporary artifacts, not new test code.

## Risks

### Review wording is mistaken for runtime enforcement

State the accepted guarantee boundary explicitly; do not promise a no-write result from unchanged tools.

**Consequence:** False assurance when an agent omits or misjudges a review.

### Latest or guessed template shape becomes an implicit migration

Use source-bound identity and explicit requirements; disclose mismatches/missing source and resolve material uncertainty.

**Consequence:** Valid manual/older artifacts may be incorrectly rewritten.

### Instruction duplication or frozen content expands the work

Keep one shared procedure, reference it minimally, and distinguish required, optional, conditional and freely authored content.

**Consequence:** Maintenance ballast and false positives against valid refinement.

## Related Documents

- [Issue #121](<https://github.com/MikeyVK/phase-gate-mcp/issues/121>)
- [#483 deferred finding](<../issue483/research.md#deferred-finding--preserve-template-structure-during-artifact-edits>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp researcher | Establish current edit boundaries, reproduce structural gaps and compare minimal source-aware review with runtime alternatives. |
| 0.2 | 2026-10-08 | @imp researcher | Replace the rejected instruction-only recommendation with a bounded contentcheck candidate; expose native-rule, policy/admission and enforce/report decisions. |
| 0.3 | 2026-10-08 | @imp researcher | Require all generated artifact formats; assess existing Jinja-related tools and distinguish exact rendering, source matching and permitted-edit obligations. |
