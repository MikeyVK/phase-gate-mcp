<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 503 — explicit branch registration and PR target authority

**Status:** RESEARCH DRAFT — OWNER CHOICES PENDING  
**Version:** 0.3  
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

The owner moved this work out of #319 and Coordination opened #503 on refactor/503-branch-registration-and-pr-targets, parent main, Refactor/Research. Initial commit defda419 tracked the newly initialized workflow files with the Research document; the source inventory was conducted on that clean, pushed baseline. The #319 deferred record is an input, not a completed #503 design. Prior owner decisions put create/checkout/initialize at CO and require Imp to receive an initialized branch.

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

Project metadata and state are persisted separately today. Research does not claim a cross-file transaction. Required early identity/registration refusal must be distinguished from a later I/O failure or a concurrent external modification.

The existing read has a concrete side effect: FileStateRepository.load catches malformed/version-invalid state and calls StateVersionValidator.backup_file, which **renames** the active file to .bak; an existing backup is overwritten. The repository test explicitly expects the original file to disappear. Source-derived sequence: the first read fails after moving the file; a later initialization sees absence and can proceed. This is a code-path finding, not a destructive live reproduction. The validator also wraps read OSError as StateCorruptedError, retaining its cause; those failures can enter this backup path.

The bounded proposal is to make branch-state reads leave the original untouched and propagate the diagnostic. Only genuine absence admits initialization; schema/I/O failures must not be caught as absence by the initialization guard or ordinary mutator. The owner requested further discussion before deciding this change. No backup change is approved. Do not change the shared backup command globally: ProjectManager invokes it explicitly in planning **command** paths, and its separate semantics are outside #503. Sources: [repository](../../../mcp_server/managers/state_repository.py):79–91, [validator](../../../mcp_server/managers/state_version_validator.py):56–101, [repository test](../../../tests/mcp_server/unit/managers/test_state_repository.py):100–118, [planning commands](../../../mcp_server/managers/project_manager.py):305–314 and 574–587.

No production consumer of state.json.bak or deliverables.json.bak was found in the bounded source search. The current command preserves invalid bytes but does not restore, repair or migrate them; the subsequent absence is not successful recovery. This differs from template-activation backups, which have their own unrelated lifecycle. Compare the viable strategies:

| Read-error strategy | Benefit | Cost / risk |
| --- | --- | --- |
| Retain automatic rename | Keeps the existing observable behavior and leaves one invalid-file backup. | A read removes the active registration; later initialization can treat it as absent. The query still mutates files and replaces prior backup evidence. |
| Copy a backup and keep the active file | Preserves the blocking file while retaining a separate diagnostic copy. | Adds write/failure policy to a read and needs backup-overwrite handling; no actual repair is provided. |
| Leave the active file untouched and raise | Preserves original evidence and repeats the same blocking condition until deliberate repair; follows CQS. | Automatic .bak creation is removed at this read boundary. Recovery must be deliberate with existing edit/Git facilities; no new repair tool is proposed. |

The third option remains the producer recommendation, pending the owner's decision. This research has not demonstrated an actual #503 data-loss incident.

### Bounded production seams

| Existing seam | Evidence | Research implication |
| --- | --- | --- |
| Initializer / manager / state engine | One production call to each initialize operation. | The registration-contract change is a small production chain; it does not justify a new orchestration layer. |
| State writes / validated copies | One ordinary repository.save caller; five with_updates callbacks in one engine. | Complete initialization and validated normal mutation can remain within the existing model, mutator and lock boundaries. |
| Composition root | One production PhaseStateEngine constructor; it omits the already constructed mutator. Other direct constructors found are four test locations, including the shared helper. | Repair the existing dependency injection. No second lock owner or new coordinator is needed. |
| State read versus parent lookup | Existing IStateReader and BranchValidatedStateReader already express read-only state and exact-branch validation. Parent-only lookup has two consumers. | Design can reuse these narrow interfaces for PR authority rather than enlarging a parent-only reader into a new lifecycle service. Preserve branch-check absence behavior. |
| GitHub create_pr | Two production callers already supply base explicitly. | Removing the lower default has local impact; authentication and unrelated adapter behavior need no change. |

The minimum identity boundary for Design is an explicit nonblank parent, the actual attached worktree branch, exact matching registration for submission and the existing configured issue-identity rule. Detached HEAD is not a usable branch registration. Do not add remote discovery, ancestry-based parent inference, a second head field or hardcoded branch-name conventions. Persisted project metadata may describe the supplied parent; it must not become a fallback authority for registration or submission. A metadata/state pair is not made transactional by these validations.

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

The secondary scan found five raw state dictionaries carrying branch, workflow_name and current_phase in four files: integration/test_ready_phase_enforcement.py:70, unit/test_server.py:104, unit/managers/test_phase_state_engine.py:1540 and unit/managers/test_state_repository.py:80/367. None supplies parent_branch. Context enforcement uses a BranchState constructor instead and is included in the table above. Raw head/base tool-request fields also occur in unit/test_server.py:158–159. Treat deliberately invalid payloads separately from valid setup.

Correction to the initial inventory: integration/test_target_startup.py:363 is a normal Python initialization call, already included in the AST count, not an additional embedded Python call. The AST string scan found an initialization example in the ProjectInitOptions docstring, not another executable test script. Keep raw serialized requests and documentation examples in the migration inventory without double-counting ordinary calls. Existing mutator doubles also depend on the placeholder/apply contract.

Active instructions include seven submit_pr(head=...) Ready examples in contracts.yaml, AGENTS tool signatures and bundled host copies, project/GitHub references and setup calls. Start-issue flows already pass CO's selected parent; they do not need a role redesign. Update existing relevant text rather than adding instruction blocks everywhere.

### Test blast radius: contract versus preparation

Read-only AST classification confirms that call-site counts do not predict failing test counts. Of 97 test initialize_project calls, 74 are inside test functions and 23 inside fixtures/helpers; of 57 initialize_branch calls, 44 are inside test functions and 13 inside fixtures/helpers. Only seven project calls supply options, three branch calls supply parent_branch and nine of 44 BranchState constructors supply parent_branch. Supplying options alone does not prove that options contains a parent.

| Category | Concrete evidence | Appropriate boundary |
| --- | --- | --- |
| Necessary contract migration | Public initialization/PR DTOs, reflog/nullable-parent/cascade expectations, state validation and handover tests. | Adapt valuable tests to the new contract; remove obsolete expectations rather than retaining legacy coverage. |
| Incidental setup coupling | Outside project-manager, phase-engine and initialization-test files: 25 project calls / 13 files and 20 branch calls / 9 files. Cycle, context, transition and readback tests often register only to establish their starting condition. | Consolidate only affected uninteresting setup; keep the behavior under test visible. |
| Existing reusable construction | test_support.py:289/335 factories have 124 project-manager calls / 26 files and 92 engine calls / 21 files. They construct dependencies but do not establish a registered project/branch. | Extend existing test support only if it reduces duplicated affected preparation; at most one explicit registration preparation helper, not a new fixture framework. |
| Duplicated implementation in doubles | _TrackingMutator at test_phase_state_engine.py:528 recreates the placeholder fallback. | Do not reproduce removed production bootstrap logic in a fake. Preserve narrow spies that prove delegation. |
| Valuable narrow doubles | ChangedPlanMutator:279 and _FreshSMutator:950 deliberately supply fresh changed state to mutation callbacks. | Retain meaningful evidence for state freshness and planning checks; multiple test consumers are justified here. |
| Weak source/absence assertions | Mutator test:195 searches for Lock text; :210 searches bootstrap for WorkflowStateMutator. PR test:130 searches for an internal adapter expression. Engine test:1260 checks that a former private save method stays absent. | Within directly changed tests, replace or remove assertions according to observable behavioral value. Do not start a suite-wide campaign. |

The bootstrap string assertion currently passes its own predicate even though bootstrap does not inject its constructed mutator into the engine. It therefore cannot prove the wiring its docstring promises. This is a concrete example of coverage that follows source wording while missing the architectural behavior.

A bounded preparation helper is proposed for tests where registration is incidental, with an **explicit parent and relevant identity**, not a compatibility default. Direct initialization, invalid-state, model/repository and PR-authority tests continue to exercise their public contracts directly. Existing integration/atomic-submission/rollback and scope-bypass tests remain valuable. Example repeated preparation: test_phase_state_engine_workflow.py:58–65 and :86–93; test_cycle_tools_business_logic.py has five variants at :103/:147, :324/:375, :530/:573, :740/:772 and :904/:911.

One implementation change having multiple consumers is not itself a defect: shared contracts and independent integration evidence legitimately fan out. Avoidable coupling is when an unrelated test must restate all details of that contract or reproduce its implementation. Do not weaken production validation or enlarge production interfaces to accommodate test setup.

The issue's phrase 'behavioral regression coverage' means durable evidence for the intended new contract, consistent with the owner's direction: no legacy-preservation tests, content snapshots or generic test expansion. No new test files are presumed necessary. Sources: [shared test support](../../../tests/mcp_server/test_support.py), [mutator tests](../../../tests/mcp_server/unit/managers/test_workflow_state_mutator.py), [state-engine tests](../../../tests/mcp_server/unit/managers/test_phase_state_engine.py), [PR tests](../../../tests/mcp_server/unit/tools/test_submit_pr_tool.py).

### Remaining warning signal and relevance

The last durable full-suite evidence is #319 at production snapshot 18095d0e: run_tests(scope="configured", timeout_seconds=1200), **2934 passed, one skipped, one xpassed, 283 warning occurrences, native exit 0**, recorded in [Validation](../issue319/validation.md). There is no fresh #503 suite run. The transient receipt has expired, so exact historical category counts are unavailable; current source candidates below do not establish current frequencies or a complete warning inventory.

| Warning group / current source | Relation to #503 | Proposed treatment |
| --- | --- | --- |
| AnyIO cancellable=True in project_tools.py:209 | The deprecated argument is inside the parent-reflog helper being removed. | Disappears with the approved clean break; no separate API migration or test. |
| Module-wide asyncio mark in test_context_loaded_enforcement.py:59 | Marks seven synchronous and two asynchronous tests; this file already needs registration-fixture migration. | If the file is changed, restrict marking to its two async tests. Small adjacent test-metadata repair, approved by the owner with the bounded test-coupling work. |
| Resource-return deprecation, server.py:95–100 returning str | Shared MCP resource boundary; repeated callers can multiply occurrences. | Separate maintenance; do not change the resource protocol under branch-registration work. |
| Pydantic SchemaAttachment.schema shadowing, core/tool_execution.py:40–46 | Existing comment records an intentionally chosen field name. | Do not rename this independent public contract opportunistically. |
| Pytest collection-name collisions | Current candidates include imported TestsConfig in unit/resources/test_standards.py:7 and TestCapability in integration/adapters/test_pytest.py:21. | Separate test housekeeping; no complete per-class warning count is claimed. |
| Pathlib is_reserved deprecation, utils/path_resolver.py:135 | Path validation, unrelated to registered branch authority. | Separate maintenance. |
| PyGithub token-constructor deprecation, adapters/github_adapter.py:34 | Same adapter file as the explicit-base change, but different authentication responsibility. | Separate maintenance; shared filename is insufficient scope justification. |
| Unawaited restart-test coroutine and mocked SystemExit(42) diagnostics | admin_tools delayed_exit/create_task and tests/mcp_server/tools/test_admin_tools.py; already disclosed in #319. | Separate async-harness maintenance, not a new branch-registration failure. |

The manual proxy skip (core/test_proxy.py:199, RUN_MANUAL_TESTS) and non-strict XPASS are **outcomes, not warnings**. The XPASS marker in unit/managers/test_enforcement_runner_unit.py:49 still cites missing GitCommitTool neutralization, while the body tests NoteContext rendering. That reason/body mismatch deserves separate correction; it is not evidence that #503 admission is broken. The existing [deferred index](../issue319/deferred.md) retains general warning housekeeping.

### Evidence limits

Research used source reads, rg searches and read-only Python AST scans over mcp_server, tests and scripts, excluding generated assets and __pycache__. The baseline was defda4198dd6a275c6953af194383af6a61a719d. Scans classified call symbols, enclosing test/helper functions and supplied keyword names; a secondary scan identified raw dictionaries, example strings and direct engine constructors. These are source inventories, not execution/coverage measurements.

Bounded delegated research supplied findings for test coupling and warning relevance; the producer checked the decisive source paths. No delegated findings are QA approval. No production/test/config files, test suites or live registration/state were mutated for these probes.

## Questions

One strategy choice remains before Research can close: how branch-state reads handle invalid files. The owner requested discussion of the existing automatic rename and recovery consequences before deciding. The source facts and three bounded alternatives are recorded above; no change to backup behavior is authorized.

The owner approved the limited reduction of test coupling, including affected incidental preparation, directly affected weak source assertions and the adjacent asyncio marker. That decision is now part of Approved Strategy.

Other operational details belong to Design within the already approved boundaries: concrete input/model signatures, exact identity checks, existing diagnostic projection and validation order. They do not require a new state framework, transaction layer or compatibility decision.

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

Previously explicit owner choices carried into #503: public initialization requires a supplied nonempty parent; Git supplies the actual branch stored in the existing branch field; CO initializes before Imp starts. PR targets derive from matching registration, with no caller head/base or default-base cascade; lower create_pr requires base. Clean break at affected public/internal contracts, without a compatibility bridge. Preserve existing single-statefile handover, general versus validated readers, configuration-driven Ready/admission, normal phase/cycle behavior and unrelated check scopes. Use existing state/mutator/composition seams; no new state framework or general transaction layer. Adapt valuable existing behavior tests and only the affected active instructions. Additional owner decision, 2026-10-15: consolidate only affected incidental test preparation through existing fixtures/factories and at most one helper with explicit parent/context; retain direct registration-contract tests, replace/remove weak source assertions within directly changed tests, and restrict the context module's asyncio marker if that file changes. No suite-wide cleanup or production fallback is authorized. The branch-state backup strategy remains pending discussion. Research remains open and no transition to Design is authorized by this document.

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
| 0.2 | 2026-10-15 | @imp researcher | Identify branch-state read/rename effects, bound production seams, classify necessary versus incidental test coupling and historical warning relevance; record two pending owner choices. |
| 0.3 | 2026-10-15 | @imp researcher | Capture owner approval for bounded test decoupling and document existing backup/recovery behavior and alternatives for the remaining owner discussion. |


