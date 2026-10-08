<!-- pgmcp:v1 id=planning pv=1.0.0 pf=CscfYyDLqj0OeHml sf=5--KpGf2wHUv2qAj -->

# Issue \#471 — Active documentation link baseline

**Status:** Planning — independent review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-08

## Purpose

Repair the demonstrated local documentation links and make the existing native link checks reproducible with the correct reading bases.

## Scope In

Six documentation files with 21 observed local link failures; active documentation inventory, instruction source/deployment bases, historical citations, and native offline evidence.

## Scope Out

Production/test/configuration/adapter changes; new tests, CI requirements or phase-contract gates; general content modernization; historical issue-document cleanup and external URL availability certification.

## Summary

The owner approved the repair proposal on 2026-10-08: “Helemaal goed repareer volgens je voorstel.” Preserve tool, adapter, public behavior and source/runtime instruction contracts. Correct current local destinations; preserve historical facts through immutable source links; remove obsolete references with no established replacement.

Research used Lychee 0.24.2 through markdown_link_review with --offline --cache=false --include-fragments. A 57-file survey found 513 successful link occurrences, 6 exclusions and 21 errors: nine ordinary path errors in four references/diagrams, three unavailable maintenance-document references and nine historical code citations in the active deferred register. These are local file failures, not fragment failures.

A 52-file instruction survey had 38 storage-base failures. Separate native checks for seven role sources, eleven workflow sources and three VS Code agent sources passed using their documented deployment bases. The remaining 31 files passed with configured arguments. Four AGENTS copies passed with the workspace-root reading base (44 occurrences, nine unique targets); all 24 Codex/VS Code source/runtime pairs were byte-equivalent. Antigravity checks use the documented deployment layout, not a certified separate installed host.

### Authoritative scope and source mapping

| Target | Authoritative input | Intended change |
|---|---|---|
| [Git fetch/pull reference](../../reference/git_fetch_pull.md) | Existing #94 archive documents | Correct two relative destinations |
| [Workflow-state diagram](../../manuals/architectural_diagrams/02_workflow_state_subsystem.md), [runtime flows](../../manuals/architectural_diagrams/06_runtime_flows.md), [dev infrastructure](../../manuals/architectural_diagrams/07_dev_infrastructure.md) | Existing neighboring diagrams, proxy reference and archived #257 gap analysis | Correct seven link definitions; preserve diagram content |
| [Maintenance examples](../MAINTENANCE_SCRIPTS.md) | [Current execution reference](../../reference/tools/quality.md), [check binding](../../../.pgmcp/config/checks.yaml), [source/deployment procedure](../../reference/release-assets-procedure.md) and [bootstrap deployment](../../setup/agentic-bootstrap.md) | Remove three unsupported references; replace the obsolete regex link-check example with a compact native baseline recipe and outcome |
| [Deferred register](../issue460/deferred-work.md) | Historical source tree at commit 79759183272e28ddbc68b9b1023168a63bd79cbb | Replace nine dead local citations with immutable GitHub source links; preserve historical claims |

The historical snapshot precedes legacy scaffolder retirement. Read-only git cat-file verified all eight unique cited paths at this commit (pytest_runner has two citations). Offline checks cannot certify HTTP reachability.

### Selected inventory

Use explicit targets, never a whole-workspace traversal. Normal group: root README.md, CHANGELOG.md and AGENTS.md; Markdown under docs/manuals, docs/reference, docs/coding_standards and docs/setup; docs/development/schema-template-maintenance.md, MAINTENANCE_SCRIPTS.md and issue460/deferred-work.md; mcp_server/resources/cache_reading.md. Exclude the explicitly HISTORICAL docs/reference/migration_v2.0.md. This is 56 current normal targets.

Include every current Markdown instruction source under docs/agents and active runtime copy under .agents and .github. Exclude .github/prompts/archive and docs/agents archive counterparts if present. Group the three source AGENTS files plus .agents/AGENTS.md by workspace-root reading base; Codex/Antigravity role sources by the deployed .agents/rules parent; their workflow sources by the deployed .agents/workflows parent; VS Code agent sources by .github/agents. All other active instruction files retain their natural base. Current groups contain 4, 7, 11, 3 and 31 files, respectively: 112 distinct active targets in total.

Historical issue artifacts and docs/development/archive are excluded as input documents, but remain valid destinations. The active deferred register is explicitly included. Implementation-adjacent legacy notes are not part of the maintained documentation inventory. No host instruction family is blanket-excluded. Check the new Planning artifact separately.

### Review boundaries

The documentation standard's phase boundaries, source-first ownership, concise presentation and durable invocation/outcome evidence apply. No runtime tests or broad Python gates are needed for this docs-only change. Preserve native arguments and dependencies. The existing .md mutation profile from #483 remains unchanged. Source/deployment context is a selection-check concern; this plan does not change safe_edit content-check behavior.

## Work Units

### DOC471 — Repair and establish the selected baseline

**Goal:** Make the approved active local-link inventory pass with truthful, reproducible evidence.

**Owner:** @imp documenter

#### Deliverables

##### DOC471.1

Correct the nine ordinary path errors and three obsolete maintenance references in the five current reference/diagram/maintenance files.

##### DOC471.2

Pin all nine historical code citations in the deferred register to the verified immutable source snapshot, without replacing historical semantics with V3 implementations.

##### DOC471.3

Document the 112-target inventory and native reading-base groups in the existing maintenance guide, with exact selection recipe, native arguments, outcomes, exclusions and offline limits.

#### Exit Criteria

All selected groups complete with native exit 0, zero local errors/timeouts and no capture truncation; the reviewed inventory is reproducible and accounts for all 112 distinct active targets. Historical links match the verified source tree. Source/runtime parity remains intact. Independent Documentation review is requested on committed results.

#### Dependencies

- Approved owner repair scope; Lychee 0.24.2 already installed; existing links capability and markdown_link_review profile.

#### Obligations

- Resolve and verify source destinations first, then edit the four ordinary documents, maintenance guide and historical register using safe_edit_file.
- Apply all related link replacements in a single proposed edit per failing document so native enforce checks can assess the complete corrected artifact.
- Keep native arguments --offline --cache=false --include-fragments in every selection; add --base-url only to the declared instruction-source groups.
- Record complete per-group invocation/outcome evidence and explicit exclusions in the maintenance guide; do not use a run ID as the durable proof.
- Reuse Research checks on unchanged instruction groups; re-run only changed/previously failing normal targets plus the final normal inventory. Independently verify source/runtime byte parity.
- Commit the Documentation repair and push; request independent QA from Beoordeel designplan.

#### Verification

##### Current and historical link repairs

**Method:** Review every edited destination against the existing file tree or git cat-file on 79759183272e28ddbc68b9b1023168a63bd79cbb; use run_checks(scope='targets', targets=<56 normal files>, profile='markdown_link_review', timeout_seconds=120).

**Expected Result:** Nine ordinary destinations resolve; three unsupported references are removed; all historical paths exist at the pinned commit. Native local checks pass. Excluded external URLs are reported separately.

##### Complete active instruction coverage

**Method:** Reuse unchanged successful groups: 31 natural-base files; four root-base AGENTS copies; seven role sources; eleven workflow sources; three VS Code agent sources. Exact groups and base construction must be documented.

**Expected Result:** All 56 instruction files are covered without blanket exclusions; source/runtime byte comparison confirms the unchanged 24 Codex/VS Code pairs.

##### Planning and final documentation evidence

**Method:** Targeted native Markdown check of planning.md; review actual branch diff and inventory against the approved docs-only scope.

**Expected Result:** Planning links pass; source/target mappings, dependencies and review criteria are explicit; no production, test, configuration or instruction edits.

#### Stop Conditions

- A source replacement would alter historical meaning or invent current behavior.
- A native failure requires production/adapter/configuration changes.
- An active instruction is missing, differs from its source, or has unresolved deployment ownership.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp planner | Capture approved narrow repair, verified source snapshot, reading-base groups and proportional checks. |
