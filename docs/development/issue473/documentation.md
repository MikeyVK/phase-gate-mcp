<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=xoYbNuJbkallN_DM sf=FAN5Vr-4vcbMMjZ2 -->

# Issue 473 — Documentation Reconciliation

**Status:** Documentation — independent review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-04

## Purpose

Reconcile current user/contributor instructions with independently validated template behavior and finalize bounded follow-up triage.

## Summary

The concrete template corrections and existing consumers are validated. Documentation now makes their input/output boundaries explicit, restores authoritative instruction-source parity and transfers deferred tool work without runtime changes.

## Deliverable mapping

| Deliverable | Reconciled surface | Outcome |
| --- | --- | --- |
| DOC_CURRENT | Public scaffold reference, usage/maintenance guidance, Unreleased notes, authoritative create-issue sources and active consumers | Corrected-context, metadata, whitespace, real filter registration and publication responsibilities aligned with validated behavior. |
| DOC_TRIAGE | Current tool-practice findings and explicit deferred branch-check research | Reproduction/impact/uncertainty indexed for coordination; no unrelated repair or automatic issue476 scope expansion. |

## Changed authoritative and current surfaces

| Surface | Action / reason |
| --- | --- |
| [Scaffolding reference](../../reference/tools/scaffolding.md) | Add discover-and-migrate guidance; distinguish authored header/history from technical provenance and caller content from generated spacing. |
| [Template library usage](../../reference/TEMPLATE_LIBRARY_USAGE.md) | Link the authoritative output/migration explanation without copying the package catalog. |
| [Schema/template maintenance](../schema-template-maintenance.md) | Clarify that technical source-version records do not replace required authored full-document metadata; direct Jinja consumers register the real filters before admission/rendering. |
| [Changelog](../../../CHANGELOG.md) | Record the clean input break and corrected first-call presentation in Unreleased; do not bump a release version. |
| [Codex source](../../agents/codex/workflows/create-issue.md) and [active workflow](../../../.agents/workflows/create-issue.md) | Authoritative source first, then equal active copy: current file_name, body-only context, explicit-empty presence and provenance extraction. |
| [VS Code source](../../agents/vscode/copilot/.github/prompts/create-issue.prompt.md) and [active prompt](../../../.github/prompts/create-issue.prompt.md) | Same validated publication boundary, with full source/runtime text parity. |
| [Antigravity source](../../agents/antigravity/workflows/create-issue.md) | Correct distributed instructions; no active Antigravity workflow directory is present in this checkout. |
| [Tool findings](tool-practice-findings.md) | Replace stale current-status statements with dated closure and coordination triage; preserve historical evidence. |

## Reviewed but unchanged

| Reviewed surface | Reason for no edit |
| --- | --- |
| [Code Style](../../coding_standards/CODE_STYLE.md), [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md), [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md) | Already reconciled during Implementation and validated; preserve wording/ownership rather than introduce another policy. |
| [Root README](../../../README.md), [manual index](../../manuals/README.md), [user guide](../../manuals/user-guide.md), [reference index](../../reference/README.md) | Already route to live schemas and category references; no obsolete first-call field recipe remains in the reviewed current guidance. |
| [Scaffolding diagram](../../manuals/architectural_diagrams/09_scaffolding_subsystem.md), [configuration consumers](../../manuals/architectural_diagrams/10_config_consumers.md), [configuration/loading reference](../../reference/config-loading-architecture.md) | Generic catalog/schema/render responsibilities remain unchanged; no artifact dispatch or new runtime layer was built. |
| [Setup](../../setup/README.md), [quality reference](../../reference/tools/quality.md), [Quality Gates](../../coding_standards/QUALITY_GATES.md), [AGENTS](../../../AGENTS.md) | Existing tracked budget/cache policy and native contracts remain valid. The issue473 gate replacement is explicitly local to its Validation report, not a new default selection policy. |
| [Workspace upgrade](../../setup/workspace-upgrade.md), [release source/deployment procedure](../../reference/release-assets-procedure.md) | Owner-approved suite renewal and source deployment remain unchanged. No package build, deployment or ignored local config is claimed by this phase. |
| [Historical vision](../../reference/mcp_vision_reference.md), earlier issue460 and issue473 research/comparison artifacts | Explicit historical/context material, not current operational truth; no mass migration or retrospective rewrite. |

## Evidence and verification boundary

Validation GO on commit 2756f8dd and its independent evidence are indexed in [Validation 0.7](validation.md#independent-validation-closure--2026-10-04): 2775 passed, 1 skipped, 1 XPASS, 229 warnings; accepted changed-file gates. No runtime/test/template source changed in Documentation, so those results are reused without another full-suite or branch-gate run.

All edited existing documents/instruction files passed safe_edit_file enforce preflight. Host-native direct text comparison proves four source/runtime pairs equal: Codex create-issue, VS Code create-issue, Codex AGENTS and VS Code/root AGENTS. No routine hashes were computed. The new report is generated with the discovered generic_doc schema and authored metadata. Changed-file offline link verification and final report inspection are recorded in the verification appendix before review.

## Deferred coordination hand-off

[Tool findings 0.4](tool-practice-findings.md#documentation-closure-and-coordination-triage--2026-10-04) owns the actionable reproduction/impact/uncertainty index. Prioritize separately scoped F6 bootstrap/proxy diagnostics and recovery. Keep F1 link parsing, F3 response bounds, F5 schema authoring and observed cross-session receipt access distinct from supported cache/restart guidance.

[Branch-check research](tool-practice-findings.md#deferred-branch-wide-check-solution--owner-disposition-2026-10-04) remains owner-deferred to a separate issue: generic semantic intent, native applicability/config reuse, meaningful file/folder distinctions, four relevant adapter packages, no-applicable handling and unresolved wire/resolver feasibility. None is implemented here.

Issue #476 remains separately scoped to generic schema/template consumption. Current manual evidence establishes the concrete corrected package outputs; it is not a generic proof of every admitted field's consumption. Coordination assigns follow-up issues; no new issue number or approval is invented.

## Bug / Documentation Hand-over

### Scope

- Reconcile current corrected-behavior guidance, distributable instructions and active copies; finalize deferred triage.
- Exclude runtime/template/test changes, new tests, broad validation repetition, package release/deployment and merge.

### Deliverables

- DOC_CURRENT and DOC_TRIAGE mapping and authoritative/derived inventory above.
- [Validation](validation.md), [Planning](planning.md), [Implementation](implementation.md), [Current tool findings](tool-practice-findings.md).
- This Documentation report and the changed documentation branch diff are the review inventory.

### Evidence

- Enforce content preflights passed on the edits; four source/runtime pairs compare equal.
- Fresh Validation and actual nineteen-family output evidence reused.
- Only invalidated documentation links and final artifact presentation are checked in this phase.

### Open Work

- Independent Documentation review and Ready phase.
- Deferred tool/adapter/issue476 hand-off as explicitly indexed above.
- The original 41 AGENTS source-location link errors in four files remain the accepted deployment-context limitation, not silently repaired or globally excluded.

### Review Request

- Review requested; no independent Documentation approval is claimed.

## Documentation verification appendix

The eleven changed documentation/instruction files passed the targeted native offline markdown_link_review with configured arguments and timeout_seconds=120 (receipt pgmcp://cache/runs/dbbccefb18ba4c0e8b321e6ae00a261b). The report's final narrow recheck covers the heading/wording refinement and this appendix. No full-suite or branch-gate repetition was performed.

All existing-file edits passed their enforce content preflight; the report scaffold passed enforce validation and was then read as authored output. Manual inspection confirmed one visible current metadata header, a populated terminal Version History and the intended tables/hand-over hierarchy. The technical first-line provenance remains separate. No schema shape or marker-only check is presented as substantive proof.

Direct text comparisons passed for Codex create-issue source/active workflow, VS Code create-issue source/active prompt, Codex AGENTS source/active copy and VS Code AGENTS source/root copy. Unchanged Validation/native/scaffold evidence remains valid because this phase changes only documentation and instruction text. Pre-commit review found no new runtime contract, adapter behavior, release/version bump, generated asset build, extra tests or hidden deferred implementation.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-04 | @imp documenter | Reconcile validated scaffold contracts, authoritative instruction sources and deferred triage with source/runtime parity and focused documentation evidence. |
