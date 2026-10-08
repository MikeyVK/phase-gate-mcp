<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 121 — Minimal structure-preserving artifact edit review

**Status:** Draft — tool-enforced strategy pending  
**Version:** 0.2  
**Last Updated:** 2026-10-08

## Purpose

Present the least heavy architecturally clean response to the structure-preservation finding consolidated from issue483.

## Scope In

Current edit/profile/provenance boundaries, representative Markdown edits, package-owned structural requirements, existing instruction ownership, options and strategy decisions.

## Scope Out

Implementing safeguards before approval, new editing APIs, Jinja/AST output-contract inference, generic undo, universal rewrite restrictions, text/newline policy changes, implementation sequencing and a new architecture.

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

### Smallest useful contract

Begin with the demonstrated Markdown artifact concern. A selected package declares only the structural requirements that must survive a content edit: material required sections/roles, authored document metadata where applicable, and a valid revision-table block where applicable. Optional sections and free prose remain unconstrained unless a package explicitly needs a conditional requirement. A broken history row parsed as a paragraph outside the table must fail a history-block requirement; merely requiring any table or running a blank-lines-around-tables style rule is insufficient.

This is output conformance against an explicit current contract, not reconstruction of the original Jinja context or proof of semantic completeness. Generation implements the package contract; independent package review must check the template, declared requirements and representative outputs together. Code stubs and tracking bodies have different purposes; do not apply a full-document rule indiscriminately or promise every code package is covered.

### Proportionate options after owner clarification

| Option | Benefit | Cost / limitation |
| --- | --- | --- |
| Instruction-only review | Contextual semantic review remains useful. | Owner explicitly rejected this as the sufficient solution. It cannot supply a tool write block. |
| Forbid rewrites or add section/range APIs | Restricts or simplifies certain edits. | Does not prevent small structural damage and impedes legitimate changes. Existing bounded operations already exist. |
| Compare original/proposed structure in a new mode/check | Can preserve an existing structural baseline without a declared full output contract. | Needs both immutable snapshots, which current check transport lacks. Baseline can already be invalid; intentional optional/structural changes need a separate policy. Broad structure freezing is not justified. |
| Small package-owned output contract check in existing profile (recommended) | Reuses contentcheck execution, factual diagnostics and enforce/report persistence. Rules live outside generic edit code. | New adapter/native rule support, bounded contract configuration and potentially a small policy/admission extension. Several pgmcp-specific predicates remain our responsibility; no off-the-shelf complete template-conformance guarantee has been established. |
| General output-contract/introspection framework | Broader potential coverage. | New dialect/resolution/version/interpretation machinery and much larger proof burden. Excluded from the owner's least-heavy direction. |

### Native checker candidate, not a selected implementation

Official markdownlint documentation supports configurable custom rules over parsed tokens and diagnostics with locations. markdownlint-cli2 documents stdin input, explicit config/configPointer, custom rule modules, formatters and noInlineConfig. This is a credible host for a small shared native rule implementation with package-authored parameters: parsing/lint execution belongs to the existing tool, our predicates describe the limited artifact contract, and the pgmcp adapter only translates invocation/results. Plain default markdownlint does not establish those requirements. MD058 checks blank lines around a table, not completeness of a revision-history section.

A package-specific binding/profile can supply the applicable native config using existing configured arguments; this avoids reading original files again in an adapter or selecting rules from proposed provenance. One optional opaque native-checkconfig section in existing package policy is a storage candidate, not an approved field/interface. Existing policy storage already has operational component identity; its generation provenance is a different identity. A separate operational asset declaration is another candidate but costs more admission work. Do not claim either is already implemented.

No native structure checker is installed/proven here. Node/npm are discoverable; markdownlint-cli2 was not found. Observed upstream main metadata declares CLI2 0.23.3 with Node >=22 and markdownlint 0.41.1, but this is not a chosen release pin. Before Research closes for a concrete tool selection, resolve the pin/runtime/distribution, rule-config storage/admission, config discovery/override/inline suppression, structured diagnostic transport and a small actual native behavioral witness. A direct library runner is an alternative if the CLI's configuration hierarchy cannot be constrained cleanly; compare its maintenance cost rather than inventing a bypass.

### Enforced behavior and scope

Under enforce, a selected structural obligation returning failed leaves the original untouched (or a scaffold target absent). Diagnostics must identify the violated requirement and relevant location. Unavailable checker/config cannot be fabricated as passed. Optional-section removal and free prose changes should pass when the contract admits them; a full rewrite may pass when it preserves conformance.

Existing report explicitly permits negative check results to be written, retaining failure facts and independent operational stop conditions. Reusing this route is not an unbypassable guard. If the owner requires structural damage to block even report, that is a separate mutation-policy strategy decision; do not silently tighten report or add a hidden mode. Missing/unknown/manual association stays factual; do not claim a package check ran based solely on .md extension. Older markers select current installed obligations under the current selector, not a historical schema: changed acceptance needs explicit strategy approval, without compatibility emulation or provenance restamping.

### Blast radius and evidence

The recommended boundary is a new contentcheck adapter/native rule and narrow package checkconfig/policy/profile work, preserving generic edit/scaffold orchestration and existing adapter wire DTOs. A small generic metadata/admission change may be needed; no template names, Markdown predicates or native-specific rule schema should enter generic Python. Scope and test size must follow the actual chosen contract, not an exhaustive package matrix.

Existing check/mutation tests retain enforce/report/unavailable behavior. Reuse them and add/adapt only missing native contract and public consumer cases: broken history and required metadata fail/no-write, optional/free refinement and conforming rewrite pass, and rule applicability/config identity where materially changed. No full-text snapshots, prose/heading inventories asserted as repository content, or regressions against retired #483 behavior. The probes below establish the current gap, not execution success of the proposed checker.

Reviewed existing standards, template generation/shared bases, identity/distribution, active references and agent instruction model remain binding. #483's checker replacement, #476's release review, #470's newline/span/race work and #491's planning-data contracts remain separate; the new check must respect those boundaries.

## Questions

- Is the preferred boundary a limited package-owned structurecheck through the existing enforce/report route, or must protection also block report writes?
- Which artifact requirements form the initial contract: shared full-document metadata/history plus material package-required sections, with tracking/code/manual files covered only when a matching contract is selected?
- Resolve native pin/runtime, native-config isolation, packagepolicy storage/admission and a small live feasibility witness before claiming a concrete implementation route is ready for Design.

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

## Approved Strategy

Pending owner decision. The owner now explicitly requires a tooling solution (enforcement, mode or check) and rejects instruction-only review as sufficient. The least-heavy/no-new-architecture constraint remains binding.

| Boundary | Recommended candidate strategy | Approval state |
| --- | --- | --- |
| Public edit/scaffold and validation policies | Preserve existing contentcheck/no-write machinery and wire DTOs. Preserve report unless the owner separately requires a stronger guard. | Pending |
| Native checker and adapter ownership | Use an existing Markdown parser/lint engine with small owned contract rules; adapter translates only. Choose and pin the concrete native implementation after the feasibility questions are resolved. | Pending |
| Package structure requirements/config | Declare a limited current output contract with the package; use the existing profile selection. A small generic policy/native-checkconfig extension may be required. No input-schema repurposing or tool-specific generic code. | Pending |
| Installed/older/manual artifacts | Current selected contract is not historical conformance. No guessed association, automatic metadata migration, provenance restamping or compatibility emulation. Changed enforce acceptance and uncovered artifacts must be explicit. | Pending |
| Behavioral proof | Small native contract/consumer coverage, existing meaningful tests reused; no universal Jinja contract, wording matrix or restored old checker regressions. | Pending |

## Expected Results

Proposed acceptance for the bounded check: malformed required history and missing required metadata are reported as failed and block persistence under enforce; optional/free refinements and a conforming rewrite are allowed. Rule association comes from the selected obligation/config, not newly written provenance. Evidence identifies source/config scope and native outcome; unavailable execution is explicit. report keeps its current behavior unless a stronger policy is explicitly approved. These are candidate outcomes, not implemented tool postconditions.

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
