<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 503 — explicit branch registration and PR target authority

**Status:** RESEARCH DRAFT — INITIAL SOURCE INVENTORY  
**Version:** 0.1  
**Last Updated:** 2026-10-15

## Purpose

Refresh the bounded #319 deferred investigation against the initialized #503 branch and establish the refactor's structural evidence and preservation boundary.

## Scope In

Explicit parent registration; persisted branch/head identity; fail-closed PR admission before lifecycle effects; complete validated state initialization through existing mutation boundaries; direct create_pr base requirement; affected existing consumers, fixtures, embedded requests, active instructions and references.

## Scope Out

Release preparation/publication, wheel/manifest content policy, phase-owned cycles (#370), phase/cycle tool consolidation (#269), a new state framework, general transactions, remote branch-history discovery, broad test cleanup and unrelated GitHub/quality policy.

## Problem Statement

Parent authority is currently distributed across optional input, reflog inference, optional project metadata, nullable state and PR caller/config fallbacks. The existing state initializer also mutates an incomplete or previous-branch state rather than starting from a complete validated registration. These paths make lifecycle target identity harder to validate before effects.

## Goals

- Identify actual current owners, mutation/read seams and all direct consumer categories before designing changes.
- Preserve branch handover, read-only contracts, configured Ready/PR safeguards and unrelated check scopes.
- Apply the owner's clean-break direction without inference/compatibility routes or a broad test rewrite.

## Background

The owner moved this work out of #319 and Coordination opened #503 on refactor/503-branch-registration-and-pr-targets, parent main, Refactor/Research. Initial worktree contains the two newly initialized untracked workflow files; the first Research commit will track them with the document. The #319 deferred record is an input, not a completed #503 design. Prior owner decisions put create/checkout/initialize at CO and require Imp to receive an initialized branch.

## Findings

### Current responsibility and coupling

| Boundary | Current source observation | Refactor concern |
| --- | --- | --- |
| initialize_project tool | parent_branch is optional; reflog inference precedes project/state writes; actual branch is read from Git. | Explicit parent input must replace inference; actual branch remains server-observed. |
| ProjectManager | Parent is optional inside ProjectInitOptions and ProjectPlan and persisted with project metadata. | Registration identity is currently mixed with optional customization. |
| PhaseStateEngine | initialize_branch may inherit the parent from metadata; an apply callback calls with_updates on loaded/placeholder state. | Complete initialization and ordinary mutation are conflated; unspecified old fields may survive. |
| WorkflowStateMutator | Missing/key/OS errors produce a placeholder with empty workflow/phase; only the updated branch is checked before save. | Absence and read failure can be confused; the callback starts from incomplete state. |
| BranchState | parent is nullable; with_updates uses model_copy(update=...) without revalidation. | Required registration invariants could otherwise be bypassed by later copies. |
| Bootstrap | Constructs a mutator but does not inject it into PhaseStateEngine; the engine creates another instance/lock. | Existing coordination dependency is not actually shared as constructed. |
| Parent reader | Checks issue identity, not exact branch identity. | Same-issue state from another branch can supply a stale parent. |
| submit_pr | Caller head is used for PR creation; current Git branch drives preparation/status; base has input → state → default cascade. | One invocation can use different branch identities and fallback targets. |
| Lower GitHub create_pr | Manager and adapter default base to main. | Internal target selection remains implicit. |

### Preservation counterexamples and existing seams

FileStateRepository intentionally returns its single stored state independent of the requested branch; BranchValidatedStateReader provides strict matching for consumers that need it. Initialization must inspect a previous different-branch registration to support handover. Globally tightening every repository read would break that distinction.

BranchStateParentReader has exactly two production consumers: submit_pr and branch check selection. The latter already turns absent parent into branch_parent_missing. Configured/workspace/targets scopes return before parent lookup. Keep those boundaries; a general parent requirement for every check is outside scope.

IWorkflowStateMutator is the existing lock/write seam. PhaseStateEngine has five mutation callbacks: initialization, phase transition, normal cycle, forced cycle and subphase. Their inventory does not authorize a cycle redesign. The mutator is the only production caller of repository.save found in the bounded source scan; all five production with_updates calls are in the state engine. Existing Git submission separately neutralizes configured branch-local artifacts. The current lock is in-process/per-instance, not a Git-worktree, cross-process or cross-file transaction guarantee. A distinct complete-initialization operation is a candidate seam for Design, not an approved method signature.

Project metadata and state are persisted separately today. Research does not claim a cross-file transaction. Required early identity/registration refusal must be distinguished from a later I/O failure. FileStateRepository currently backs up malformed/version-invalid state before re-raising; that pre-existing diagnostic read behavior needs explicit consideration rather than silently removing backups under a broad side-effect claim.

### Refreshed consumer inventory

Read-only Python AST scan over mcp_server, tests and scripts, excluding generated assets and __pycache__; counts are calls, overlap across categories and do not equal required edits.

| Surface | Production calls | Test calls / files |
| --- | ---: | ---: |
| initialize_project | 1 | 97 / 23 |
| initialize_branch | 1 | 57 / 16 |
| ProjectInitOptions | 2 | 7 / 2 |
| BranchState construction | 1 placeholder | 44 / 10 |
| with_updates | 5, all PhaseStateEngine | 20 / 4 |
| InitializeProjectInput | Tool model | 14 / 2 |
| SubmitPRInput | Tool model | 7 / 2 |
| Lower create_pr | 2; both already supply base | 3 / 2 |
| Parent-reader calls | 2 | 4 / 1 |

BranchState's prior 43/9 inventory is now 44/10 because #319 added meaningful status-resource setup to an existing test. Reusing the old count as current would be inaccurate.

Non-AST consumers include raw head/base JSON in unit/test_server.py, embedded initialization in integration/test_target_startup.py and raw state dictionaries in repository/context/Ready tests. Existing mutator test doubles also depend on the placeholder/apply contract. Scan those directly during Design/Planning; do not rely only on call-name counts.

Active instructions include seven submit_pr(head=...) Ready examples in contracts.yaml, AGENTS tool signatures and bundled host copies, project/GitHub references and setup calls. Start-issue flows already pass CO's selected parent; they do not need a role redesign. Update existing relevant text rather than adding instruction blocks everywhere.

### Test structure and evidence boundary

Existing parent/reflog/cascade tests encode behavior that the clean break removes; they are not preservation obligations. Valuable repository, admission, atomic submission/rollback, state and check-scope tests already exist. Adapt those for the new input/invariant contract and meaningful failure-before-effects evidence. Mechanically repair fixtures and embedded payloads without adding production defaults or compatibility test shims.

The issue's phrase 'behavioral regression coverage' is read as durable behavior evidence for the intended new contract, consistent with the owner's earlier direction: no legacy-preservation campaign, content snapshots or generic test expansion. Research runs no test suite and claims no #503 implementation evidence.

## Questions

- Complete the raw/embedded-fixture and error-contract inventory beyond the confirmed single ordinary state-save path before declaring Research complete.
- Design must state the minimum identity validation and observable failure outcomes without assuming Git ancestry/ref discovery or introducing a second head field.
- Specify the preservation boundary for diagnostic backups versus forbidden lifecycle effects and for existing separate metadata/state writes; do not imply cross-file transactional guarantees.

## References

- [Initialization tool](<../../../mcp_server/tools/project_tools.py>)
- [Project manager](<../../../mcp_server/managers/project_manager.py>)
- [State engine](<../../../mcp_server/managers/phase_state_engine.py>)
- [State models/readers](<../../../mcp_server/managers/state_repository.py>)
- [Mutation seam](<../../../mcp_server/managers/workflow_state_mutator.py>)
- [Parent reader](<../../../mcp_server/managers/branch_parent_reader.py>)
- [PR tool](<../../../mcp_server/tools/pr_tools.py>)
- [Bootstrap](<../../../mcp_server/bootstrap.py>)
- [Check scope selection](<../../../mcp_server/execution/check_selection.py>)
- [State mutator interface](<../../../mcp_server/core/interfaces/workflow.py>)

## Approved Strategy

Previously explicit owner choices carried into #503: public initialization requires a supplied nonempty parent; Git supplies the actual branch stored in the existing branch field; CO initializes before Imp starts. PR targets derive from matching registration, with no caller head/base or default-base cascade; lower create_pr requires base. Clean break at affected public/internal contracts, without a compatibility bridge. Preserve existing single-statefile handover, general versus validated readers, configuration-driven Ready/admission, normal phase/cycle behavior and unrelated check scopes. Use existing state/mutator/composition seams; no new state framework or general transaction layer. Adapt valuable existing behavior tests and only the affected active instructions. This initial draft is not phase approval; current code observations and the remaining contract details below must be reviewed before Research is declared complete.

## Expected Results

A complete valid registration has one actual branch and one explicit parent. Missing, corrupt, unreadable or mismatched registration prevents PR lifecycle effects. Initialization refuses invalid identity before project/state writes and does not carry unrelated old-branch fields forward. Normal mutations retain registration validity. Branch check behavior and other scopes retain their established contracts. Error diagnosis and production admission remain intact; no release is authorized.

## Consumers

### CO/start-issue and public initialization

Provide issue/workflow/parent and initialize the checked-out worktree branch.

**Impact:** Parent becomes mandatory; update existing schemas/calls and success output.

### Project metadata, state models and mutator

Persist planning metadata and workflow registration through their current boundaries.

**Impact:** Remove optional identity/inference paths and research complete initialization plus validated copies.

### submit\_pr / GitHub manager and adapter

Prepare/push branch, create PR and record PR status.

**Impact:** Use matching registration for head/base before effects; remove lower default base.

### Branch checks and read-only status consumers

Read branch-specific context through existing narrow interfaces.

**Impact:** Preserve unrelated scopes/general readers; strengthen exact branch identity only at appropriate consumers.

### Existing tests, raw payloads, embedded scripts and instructions

Express supported behavior and construct valid inputs/state.

**Impact:** Proportionate migration; remove obsolete inference/cascade expectations without a legacy suite.

## Risks

### A global state-reader or mandatory-parent rule leaks into unrelated operations.

Keep the general repository read contract distinct from branch-validated consumers and check scope applicability.

### Required fields alone do not protect updates that use unchecked copies or placeholders.

Research the existing mutation boundary and all five callbacks; preserve normal phase/cycle behavior.

### Fixture migration dominates the patch or tests continue exercising implicit defaults.

Use refreshed counts plus raw/embedded inventory; adapt existing public behavior coverage and central helpers without a production compatibility path.

### Refactor scope expands into transactions, Git history or broader workflows.

Treat those as excluded unless a concrete in-scope invariant proves the existing seam insufficient; reopen strategy explicitly rather than growing the design.

## Related Documents

- [Issue 503](<https://github.com/MikeyVK/phase-gate-mcp/issues/503>)
- [Deferred source](<../issue319/deferred.md>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-15 | @imp researcher | Refresh deferred #319 source observations, consumer counts and approved direction for the bounded #503 Research; no production/test changes. |
