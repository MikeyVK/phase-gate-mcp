<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — scope closure and deferred work

**Status:** OWNER-DIRECTED SCOPE BOUNDARY — FOLLOW-UP DEFERRED  
**Version:** 0.2  
**Last Updated:** 2026-10-14

## Purpose

Freeze the remaining Chore boundary and preserve investigated follow-up work without implementing it on this branch.

## Scope In

Existing G004/BLE001/SLF001 maintenance, configuration_choice admission and installation acknowledgement, approved exception/diagnostic cleanup, safe-edit report recovery, and the already implemented explicit GitHubSettings injection/default removal. The owner also retains the bounded fallback/document-portability repairs listed below. Remaining work is their focused verification, review, current validation, bounded documentation and Ready hand-off.

## Scope Out

New initialization/parent/head contracts, state-mutation refactoring, PR-base fallback removal, release-manifest/build content transformations, new native-config assets and broad test-housekeeping campaigns. A new release, version bump, package build, tagging and publication are explicitly postponed.

## Summary

Owner decision on 2026-10-14: stop expanding #319. Complete the existing native-lint/configuration-choice maintenance and already implemented GitHub identity repair, then validate, document and hand off for Ready. DF-319.1, DF-319.2 and DF-319.4 are follow-up work, not missing #319 implementation. The owner's subsequent clarification retains the former DF-319.3 fallback/document-portability candidates inside #319 and explicitly postpones a new release. Baseline: b1069a55ece891b2958933c44054bc57deb62515.

## Retained implementation and evidence boundary

The GitHub identity repair at b1069a55 removes concrete owner/repository defaults and the implicit project-board number, injects GitHubSettings from the composition root and preserves lazy client construction. It stays on this branch; no rollback is requested. Independent QA approved entry for this repair, not its completed implementation. Targeted evidence recorded in the commit: 115 passed, plus focused checks and additional targeted cases. Existing PR-status enforcement can require GitHub setup before branch mutations; startup/health availability does not imply an offline mutation bypass.

The existing [Validation report](validation.md) records a full configured suite at a5cdbcaa: 2931 passed, 1 skipped and 1 xpassed, with passing branch checks. That remains historical evidence for that snapshot. It does not cover the later identity repair and must not be presented as final validation of b1069a55 or subsequent documentation commits. The current owner decision changes scope, not the truth of earlier results.

## DF-319.1 — explicit branch registration and parent-only PR submission

Observed: initialize_project accepts an optional parent and can infer it from checkout reflog; the state engine can inherit a parent from project metadata. submit_pr accepts a caller head and optional base, falling back through stored parent to the configured default. The parent reader checks issue identity but not the exact branch name.

Owner-selected direction: CO creates/checks out/initializes the branch and must supply parent_branch explicitly. Git supplies the actual checked-out branch; state.branch is the head identity, so no duplicate head field is needed. Imp starts from that initialized state. submit_pr should accept neither head nor base and should use only matching branchstate and its parent. Lower-level create_pr should require an explicit base. This direction is retained for a separate issue; it is not implemented or a completed design.

- Reopen boundaries together: InitializeProjectInput/output, ProjectInitOptions/ProjectPlan, ProjectManager.initialize_project, PhaseStateEngine.initialize_branch, BranchState, BranchStateParentReader, SubmitPRInput/SubmitPRTool and the lower GitHub manager/adapter create_pr methods.
- Remove reflog inference and the parent/base cascades; refuse absent, blank or mismatched registration before project/state or PR side effects. Preserve the existing configured Ready admission.
- Investigate the existing mutator placeholder and unchecked BranchState.with_updates copy. The proposed bounded solution is complete-state initialization through the existing locked mutator, an explicit method on its existing protocol, validated updates and injection of the already constructed mutator into PhaseStateEngine. This proposal still needs follow-up design/review; no new state framework is approved.
- Preserve different-branch handover of the single statefile and the existing repository read contract. Do not globally require every state reader to reject another branch. Corrupt/unreadable state must be distinguished from genuine absence when designing initialization.
- Shared consumers: parent reading is used by submit_pr and branch check selection. Keep existing branch-basis-unavailable behavior; targets/configured/workspace selection must not acquire a new parent requirement. Five state-mutator calls exist in PhaseStateEngine; only initialization needs the proposed distinct operation.
- Read-only AST inventory: initialize_project 97 test calls/23 files; initialize_branch 57/16; direct BranchState construction 43/9; InitializeProjectInput 14/2; SubmitPRInput 7/2. Counts overlap and are not the number of required edits. Include raw JSON requests and embedded Python strings omitted by outer AST counts. Adapt existing behavior tests/fixtures; remove obsolete inference/cascade tests without compatibility helpers.
- Instruction consumers: seven submit_pr(head=...) Ready examples in contracts.yaml, project/GitHub tool references, setup examples and active AGENTS copies. Start-issue instructions already put initialization at CO. Change existing instructions proportionately; do not rewrite historical issue documents.

## DF-319.2 — distribution content policy in the release manifest

Observed: the existing manifest copies .pgmcp/config as a directory; scripts/build_package.py copies registered assets without a content policy. Fresh CLI --init already clears configuration_choice in the copied check/test/fix bindings; packaged source bindings can still contain this repository's acknowledgements. This is the retained implemented contract, not an assertion that the wheel is workspace-neutral.

Deferred investigation: distinguish whole-file distribution sources from content transformations and decide which project-specific values should be absent in a standalone distribution. An explicitly configured copy/YAML-field-reset rule and individually registered config files were proposals only. No manifest schema, transformation grammar, alternative distribution source, new builder or packaging-content choice is approved by #319. Native tool config examples/exporters remain excluded. Follow-up must assess actual wheel/sdist/init/upgrade consumers and preserve owner-managed existing configuration.

## Retained #319 work — remaining fallback and document portability

Owner clarification, 2026-10-14: include these investigated repairs in #319. Use the existing state/configuration boundaries, remove proven unused paths, adapt existing behavior tests and correct active portable documentation. Do not redesign PR submission or package content.

- StatusResource now reads the stored phase through existing injected read-only interfaces and the existing branch-validated reader. Missing/mismatched state propagates rather than selecting a phase by branch name.
- ConfigLoader's write-only template_root parameter/environment fallback, the unused production resolve_config_root helper and bootstrap _build_config_layer are removed. Existing constructor consumers are mechanically migrated. Settings now owns the template_suite default used by startup/renewal; deliberate legacy-suite migration remains intact.
- Bundled Codex reboot instructions now identify PGMCP and use get_work_context. Active setup/manual examples use owner-provided GitHub identity rather than personal defaults; machine-local source links and obsolete remote-autodetection claims are corrected. Product source/release/license provenance remains. Owner-managed local harness copies are not automatically overwritten.
- Complete these bounded repairs in Implementation with focused evidence, then include them in final Validation. No release packaging changes are authorized.

## DF-319.4 — existing test-harness warning housekeeping

Retain the earlier Validation report's disclosed manual skip, non-strict xpass, deprecations, stale asyncio marks and mocked restart-task diagnostics for separate triage. A passing native run does not mean warning-free execution. Do not add a generic warning cleanup or regression-test campaign to #319.

## Bounded remaining closeout

- Commit the deferred-work record and the single Research boundary reference. Review the complete branch diff against the retained scope. Resolve only genuine blockers in that scope; reopen decisions for unrelated work.
- Request independent Implementation → Validation entry review from Beoordeel designplan, scoped to the completed identity repair, retained fallback/document repairs, consumer wiring and this scope cap. Do not ask QA to execute the full Validation phase as an entry review.
- After entry GO, transition and read the fresh phase instructions. Run the required complete configured suite and current branch quality gates once for the final implementation; reuse focused evidence where valid. Update validation.md with exact invocations/outcomes and caveats.
- After independent Validation GO, reconcile only active references affected by configuration_choice, report-mode recovery and GitHub setup. Add compact Unreleased/upgrade guidance, including the acknowledgement requirement and removed identity defaults. Existing setup guidance already documents fresh-init reset; do not invent manifest-neutralized wheel behavior.
- The owner explicitly postpones the new release. Keep published v3.0.0 immutable; do not bump versions, build release packages, tag or publish as part of this closeout. Unreleased notes may describe merged behavior without promising a version/date. Coordination tracks a later release decision separately.
- Complete independent Documentation/Ready reviews as required by the active contract, commit/push final artifacts, and hand the bounded issue/PR and deferred index to Coordination for administrative follow-up and owner-approved merge. Do not create follow-up issues or publish releases merely by writing this document.

## Follow-up ownership and reopen criteria

Coordination owns issue creation, priority and scheduling for these follow-ups; no new issue numbers or delivery dates are assigned here. Reopen a candidate only with its own explicit scope, affected-consumer review, proportionate behavior evidence and required owner/QA decisions. The selected clean-break direction does not authorize an unreviewed implementation or compatibility bridge.

## Related Documents

- [Issue 319](<https://github.com/MikeyVK/phase-gate-mcp/issues/319>)
- [Research and approved strategy](<research.md>)
- [Compact design](<design.md>)
- [Current validation snapshot](<validation.md>)
- [Existing release manifest](<../../../.pgmcp/config/release_manifest.yaml>)
- [Asset build procedure](<../../../scripts/build_package.py>)
- [Workspace setup guidance](<../../setup/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-14 | @imp implementer | Record owner-directed Chore cap, investigated deferred candidates, retained implementation and bounded closeout obligations. |
| 0.2 | 2026-10-14 | @imp implementer | Retain bounded fallback/document-portability repairs in #319 and explicitly postpone the new release; leave parent/head, package-content and harness-housekeeping follow-ups deferred. |
