<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 121 — Minimal structure-preserving artifact edit review

**Status:** Draft — strategy decision pending  
**Version:** 0.1  
**Last Updated:** 2026-10-08

## Purpose

Present the least heavy architecturally clean response to the structure-preservation finding consolidated from issue483.

## Scope In

Current edit/profile/provenance boundaries, representative Markdown edits, package-owned structural requirements, existing instruction ownership, options and strategy decisions.

## Scope Out

Production safeguards, new editing APIs, Jinja/AST output-contract inference, generic undo, universal rewrite restrictions, text/newline policy changes, implementation sequencing and a new architecture.

## Problem Statement

A native-passed edit and retained template provenance do not establish that required artifact structure and information remain usable. The owner wants the lightest architecturally clean option, not a new editing architecture.

## Goals

- Separate demonstrated structural damage from valid refinement.
- Identify authoritative requirements without freezing generated text or moving package knowledge into generic server code.
- Recommend a minimal solution and make its review-versus-runtime guarantee explicit before strategy approval.

## Background

Issue121 now consolidates the deferred finding from #483. The historical revision-table repair removed two blank lines between the 0.3/0.4/0.5 rows; it is a bounded example, not a measured incident rate. The active issue explicitly permits an instruction-based conclusion and rejects treating historical introspection/API sketches as current design requirements.

## Findings

### Current responsibility boundary

| Surface | Established behavior | Consequence |
| --- | --- | --- |
| EditOperation / select_profile | Reads original content, selects explicit package ID, recognized first-line package ID or extension profile; validates the proposal and guards persistence. | Selecting a package check profile is not output-contract validation. Selection does not compare pv/pf/sf with current or historical sources. |
| Provenance / scaffold_schema | Provenance names generation inputs; schema discovery returns the current package version, fingerprint and input schema. No historical-source lookup is promised. | A retained marker is navigation evidence, not proof of preserved structure. Matching ID alone cannot establish the original rendering contract. |
| Markdown profile | Existing Lychee 0.24.2 / adapter 2.0.0 checks local links/fragments with --offline --cache=false --include-fragments. | A document with no links can correctly pass despite broken table layout or missing authored metadata. |
| Template packages / shared bases | Packages own generation; shared full-document base emits H1, authored metadata and contiguous revision history. Tracking bodies use a different base. | Requirements must be interpreted for the applicable artifact purpose; no universal H1/history rule belongs in generic edit code. |
| Existing guidance | Normal use says scaffold, read and refine. Package release review assesses generation sources and rendered behavior. The editing reference already disclaims structure preservation. | The missing instruction is a proportionate review of an edited artifact, not another package release or Jinja-admission analysis. |

### Smallest useful distinction

| Category | Concrete source-backed example | Appropriate edit treatment |
| --- | --- | --- |
| Required structure/information | Full-document authored status/version/date and revision history are required by the Documentation Standard and emitted by the shared base. | Retain their usable function, or resolve an explicit contract conflict; retaining every text token is unnecessary. |
| Optional | Research Findings is emitted only when the optional input is defined. | Omission can be valid; deleting a section is not inherently damage. |
| Conditional | PR Summary depends on supplied context; package branches and called shared blocks affect generation. The artifact does not retain its original context. | Inspect the relevant purpose/source and task requirement; do not infer permanent obligations from every generated heading or from a list of input fields. |
| Freely authored/refined | Research prose and code implementation bodies. python_class scaffolds method stubs with raise NotImplementedError. | Content changes and completing code stubs are legitimate refinement; full generated-text comparison would reject useful work. |

### Proportionate options

| Option | Benefit | Cost, limitation and architectural impact |
| --- | --- | --- |
| A — Source-aware agent edit review in existing suite instructions (recommended) | Covers structural function and deliberate deviations with contextual reasoning; uses existing operations, source access and independent workflow review. | Small documentation change, no runtime/API/config migration. Review can be missed or wrong: this is review evidence, not an automatic no-write guarantee. |
| B — Additional section/range editing operation | Can make some bounded edits easier. | Existing replace/search_window/append already support bounded edits. A tiny insertion can split a table; operation size does not prove conformance. New API/selection/encoding semantics intersect #470 without closing the observed gap. |
| C — Explicit package output contracts plus runtime validator | Could deterministically block a precisely defined subset of damage. | Requires new package contract ownership, resolution/version policy, output interpretation and validation integration. Optional/conditional/free content and unavailable historical sources create real false-positive and maintenance questions. Not the lightest justified route. |
| D — Keep only native syntax/link checks, or globally forbid rewrites | Existing checks remain useful; a ban is mechanically simple. | Link/syntax checks do not establish artifact function. A rewrite ban blocks valid work while allowing damaging small edits. Neither meets the observed need. |

### Recommended boundary, pending owner approval

Option A is sufficient only if the owner accepts an agentic review obligation rather than a deterministic tool rejection. The proposed obligation is to identify the affected artifact and applicable requirements, make the requested edit, inspect the affected resulting structure, and record material preservation/deviation/uncertainty in the existing work evidence. Prefer bounded edits for bounded changes; keep rewrites available. No separate approval or QA round is proposed for each edit; use the existing workflow review boundary. Review affected sections and their joins, tables, metadata and roles according to blast radius rather than rereading the entire suite for every prose correction.

Use current matching package sources when available. A version/fingerprint mismatch, an absent/invalid/old marker, an unknown package or a manually authored artifact does not authorize inventing a package association or silently applying the latest output shape. Use accessible source-bound history and explicit task/document requirements; limit the claim or ask the owner when a material structural decision cannot be justified. Existing tool profile fallback remains factual and unchanged. Preserve provenance as generation provenance; an edit must not stamp current provenance to imply regeneration.

The smallest current instruction surface is the existing normal-refinement route in TEMPLATE_LIBRARY_USAGE.md, with one navigation reference from the Documentation Standard's existing drafting workflow for governed documents. Both are already distributed by release_manifest.yaml. The package maintenance guide remains the authority for generation/release review. No new instruction file, phase-contract layer, mirrored checklist in all agent roles, manifest field, package rule language or server branch is justified. The host instruction model requires source-first edits and parity if a host consumer ever needs an additional navigation pointer; editing only the root AGENTS.md would violate that ownership.

### Blast radius and verification limits

Recommended production, config, adapters, schemas, renderer, provenance and public edit contracts: unchanged. Existing edit-construction/public-operation tests cover actual matching, original-profile selection, write facts and check enforcement; they are not artifact-conformance tests. No test code or full-suite run was added in Research. For an instruction-only outcome, evaluate changed guidance using representative before/after review examples and affected link checks, not wording asserts, full-text snapshots, an obsolete-behavior regression matrix or an exhaustive package matrix. Human/LLM review performed here establishes judgments on these examples; no measured reduction in agent errors is claimed. The evidence below directly exercises Markdown, not a guarantee for every code package.

Related boundaries: #483 supplies the gap and native-link route; #476 supplies generation/release review; #470 owns text/newline/source-span/race semantics; #491 owns structured planning-data mutation. None must be redesigned for option A.

## Questions

- Does the owner accept option A's source-aware edit-review obligation, with existing runtime contracts preserved and no deterministic structural write block?
- If a deterministic rejection of structural damage is required instead, the requirements and option C boundary must be reopened explicitly before Design.

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

## Approved Strategy

Pending owner decision. The latest human instruction establishes the constraint: investigate the least heavy architecturally clean option and do not develop a new architecture. It does not yet approve option A or its guarantee boundary.

| Boundary | Proposed strategy for option A | Approval state |
| --- | --- | --- |
| Public edits, validation policies and profile selection | Preserve supported contracts; no special migration policy or compatibility path needed. | Pending |
| Package generation, provenance and installed versions | Preserve existing ownership/identity; no backfill, latest-version coercion or historical registry. | Pending |
| Authoring/review instructions | Add one shared normal-use edit-review obligation and minimal navigation; preserve optional/free content and intentional justified changes. | Pending |
| Validation/test promise | Evidence-backed structural review plus unchanged native checks; no automatic structural write-block guarantee or new runtime regression suite. | Pending |

## Expected Results

Proposed acceptance for option A: review identifies the split revision table as structural damage, missing authored metadata as a required-information loss, and optional Findings removal/prose refinement as potentially valid. Intentional changes are justified against the task and applicable requirements. The reviewed source/scope and conclusion are recoverable from existing work evidence. A native pass is never relabeled as structure conformance; uncertain package association is disclosed. These are proposed review outcomes, not implemented tool postconditions.

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
