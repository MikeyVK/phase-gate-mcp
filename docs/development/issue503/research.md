<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 503 — explicit branch registration and PR target authority

**Status:** RESEARCH — STRATEGY RECORDED; CLARIFICATION IN PROGRESS  
**Version:** 0.6  
**Last Updated:** 2026-10-15

## Purpose

Refresh the bounded #319 deferred investigation against the initialized #503 branch and establish the refactor's structural evidence and preservation boundary.

## Scope In

Explicit parent registration; persisted branch/head identity; fail-closed PR admission before lifecycle effects; complete validated state initialization through existing mutation boundaries; direct create_pr base requirement; preserve original files and existing backups on failed prerequisite validation in branch-state reads and the two planning-command backup sites; affected existing consumers, fixtures, embedded requests, active instructions and references.

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

The owner approved route 3 and the targeted planning-command scope amendment after the historical recovery rationale was examined: failed prerequisite validation leaves original files and existing backups untouched and propagates the diagnostic. Only genuine absence admits initialization; schema/I/O failures must not be caught as absence by the initialization guard or ordinary mutator. The agreed scope includes the two ProjectManager command backup sites. Unrelated upgrade/activation backups remain outside #503. Sources: [repository](../../../mcp_server/managers/state_repository.py):79–91, [validator](../../../mcp_server/managers/state_version_validator.py):56–101, [repository test](../../../tests/mcp_server/unit/managers/test_state_repository.py):100–118, [planning commands](../../../mcp_server/managers/project_manager.py):305–314 and 574–587.

No production consumer automatically restoring state.json.bak or deliverables.json.bak was found. **Historical correction:** this absence is expected under the original design, which deliberately prepared a subsequent human/agent-requested reinitialization. It does not establish that the backup was accidental or an unfinished automated recovery route. Template-activation backups have a separate unrelated lifecycle.

### Original backup rationale and later preservation boundary

[Issue #438](https://github.com/MikeyVK/phase-gate-mcp/issues/438), July 2026, introduced independent dynamic-state schema versions rather than coupling data validity to every package version. Its [approved Research strategy](../archive/issue438/research.md), items 2–4, deliberately removed silent Git-history reconstruction and chose defensive backup/reset instead of maintaining data migrations: quarantine the invalid file, return a structured error, then let the agent/user explicitly reinitialize. Only transient quality-state cache was allowed an automatic empty reset.

The [Design](../archive/issue438/design.md), requirements DFV.2/DFV.3 and sections 3.1, 4.2 and 6.1, explicitly required the rename during repository load. Keeping the invalid bytes and clearing the canonical path served that restart-from-clean-state policy. A single filename.bak, overwriting its predecessor, was deliberately preferred over timestamped history to avoid disk clutter; this final Design superseded the Research's timestamp example. The implementation patch [6e3f1479](https://github.com/MikeyVK/phase-gate-mcp/commit/6e3f14798c6f347d747e8999bdfdd8a88db96c30) adds the present repository catch/backup/reraise and its test. The preceding Design commits 6525cbcc and 39d3e477 respectively record CQS refinement and the explicit clean-break strategy.

The original CQS argument split the validator into a query and a backup command, while explicitly allowing repositories to orchestrate both inside load. The current architecture's pure-reader rule applies to the whole read operation. This is a tension in the historical orchestration contract, not evidence that the rename was an implementation accident.

A later [#460 Planning prerequisite](../archive/issue460/planning.md), P2 preservation table, already required deliverables queries to preserve the invalid source and any existing backup, while retaining backups in all three planning commands. It **explicitly excluded** the existing state.json read/backup path. The [path-ownership supplement](../archive/issue460/planning-path-ownership.md), readback prerequisite, repeats that limit. Thus the remaining state behavior was knowingly left outside that earlier correction. Current manager tests distinguish pure reads from command backups.

For #503, both retaining and removing the read-time backup can reject invalid registration before PR neutralization, commit, push or PR creation. Removing it is therefore an explicit **recovery-policy change**, not a prerequisite automatically implied by safe PR target selection. Route 3 preserves invalid bytes in the original location and postpones any quarantine/reset to a deliberate recovery action; it gives up the old automatic preparation for reinitialization. Preserve the diagnosis and the no-automatic-migration/no-Git-reconstruction strategy whichever route the owner chooses.

Compare the viable strategies:

| Read-error strategy | Benefit | Cost / risk |
| --- | --- | --- |
| Retain automatic rename | Preserves #438's explicit quarantine/error/subsequent-reinitialization policy and one invalid-file backup. | A read removes the active registration; later initialization can treat it as absent. The query still mutates files and replaces prior backup evidence. |
| Copy a backup and keep the active file | Preserves the blocking file while retaining a separate diagnostic copy. | Adds write/failure policy to a read and needs backup-overwrite handling; no actual repair is provided. |
| Leave the active file untouched and raise | Preserves original evidence and repeats the same blocking condition until deliberate repair; follows CQS. | Automatic .bak creation is removed at this read boundary. Recovery must be deliberate with existing edit/Git facilities; no new repair tool is proposed. |

The owner has selected the third option together with the targeted command amendment below. This changes the historical recovery contract; it is not simply removal of an unintended side effect. Implementation has not begun, and this research has not demonstrated an actual #503 data-loss incident.

### Comparable planning-command backup boundary

Owner decision: include the targeted planning-command correction alongside route 3. The scope is the failed prerequisite-validation behavior at the existing boundaries, not a general recovery or planning redesign.

The #460 deliverables query correction preserves deliverables.json on invalid-source reads. However, get_project_plan also enriches its result with the current phase: it reads the plan, calls WorkflowStatusResolver.resolve_current, and that resolver uses its injected state reader (the composed branch-validated repository reader). A malformed/version-invalid state.json can therefore be moved to state.json.bak during a planning query while deliverables.json is untouched. The first query propagates the state diagnosis; a later query can return the plan without phase fields because state is now absent. Route 3 fixes this same repository read for all consumers. No separate query repair or new dependency is required.

The remaining **command** paths are _save_project_plan (initialize_project) and _planning_project (shared by save/update planning). Both catch PlanningVersionMismatchError/StateCorruptedError, rename the complete deliverables file to .bak and then raise. Save/update reach this before their candidate-plan validation, and update before Git cycle-evidence protection. This is not the post-persist/readback failure case, which separately reports persisted=True.

| Comparison | State repository read | Planning commands |
| --- | --- | --- |
| Requested operation | Read existing registration. | Initialize project metadata or save/update a specific plan. |
| Backup trigger | JSON/version validation failure. | JSON/version validation failure while loading the existing file. |
| Failure effect | Active state file moved; previous backup can be replaced. | Entire multi-project deliverables file moved; previous backup can be replaced, although the requested plan change is refused. |
| Subsequent call | Initialization can observe absent state. | Save/update report planning_project_missing; manager initialization can start a new project dictionary if its separate branch-state admission permits it. |
| Architectural concern | A query mutates files. | A command is permitted to write, but a failed precondition implicitly performs a whole-file quarantine outside the requested plan mutation. |

The planning command is not the same CQS violation merely because it writes: commands intentionally have effects. The narrower concern is whether the ordinary mutation contract should also authorize quarantine/reset on an unreadable or version-invalid source. The old #438 policy expressly allowed it; #460 preserved it. The approved common policy preserves the original and any existing backup when prerequisite validation fails, leaving quarantine/reinitialization to deliberate recovery. It would retain successful persistence and truthful post-write diagnostics.

Approved bounded scope amendment: apply that policy at the two existing planning catch sites alongside route 3, adapt the already-existing six command-backup cases to prove source/backup preservation, and remove the shared backup command only if the resulting production consumer inventory is empty. The three known production backup callers are this pair and FileStateRepository.load. No new recovery tool, flag, transaction or broad planning redesign is proposed. Existing template activation/upgrade backups are not implicated.

Sources: [planning commands](../../../mcp_server/managers/project_manager.py):237–314 and 573–587; [query/readback](../../../mcp_server/managers/project_manager.py):292–304 and 503–563; [query-versus-command behavior tests](../../../tests/mcp_server/unit/managers/test_project_manager.py):943–1003. Findings are source-derived; no corrupt-file live probe or test run was performed.

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

The owner approved route 3 and the targeted planning-command scope expansion, and requested an explanation of the planning query's phase-enrichment path before further progression. That path is documented above and shares the same repository correction. No additional policy choice has been identified from this clarification. Research has not transitioned to Design; no implementation behavior is claimed.

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

Previously explicit owner choices carried into #503: public initialization requires a supplied nonempty parent; Git supplies the actual branch stored in the existing branch field; CO initializes before Imp starts. PR targets derive from matching registration, with no caller head/base or default-base cascade; lower create_pr requires base. Clean break at affected public/internal contracts, without a compatibility bridge. Preserve existing single-statefile handover, general versus validated readers, configuration-driven Ready/admission, normal phase/cycle behavior and unrelated check scopes. Use existing state/mutator/composition seams; no new state framework or general transaction layer. Adapt valuable existing behavior tests and only the affected active instructions. Additional owner decision, 2026-10-15: consolidate only affected incidental test preparation through existing fixtures/factories and at most one helper with explicit parent/context; retain direct registration-contract tests, replace/remove weak source assertions within directly changed tests, and restrict the context module's asyncio marker if that file changes. No suite-wide cleanup or production fallback is authorized. Additional owner decision, 2026-10-15: adopt route 3 for branch-state reads and extend the same failed-prerequisite-validation preservation policy to the two existing planning-command backup sites. Preserve originals, existing backups, structured diagnosis, successful writes and truthful persisted readback failures; no automatic migration/reconstruction or new recovery architecture. Remove the backup helper only if no production consumers remain. The owner requested phase-enrichment clarification before further progression; this document is not QA approval or a phase transition.

## Expected Results

A complete valid registration has one actual branch and one explicit parent. Missing, corrupt, unreadable or mismatched registration prevents PR lifecycle effects. Initialization refuses invalid identity before project/state writes and does not carry unrelated old-branch fields forward. Normal mutations retain registration validity. Branch check behavior and other scopes retain their established contracts. Failed prerequisite validation retains the source and existing backup bytes for both affected file boundaries; subsequent reads do not silently convert invalid source into absence. Successful writes and persisted=True readback diagnostics remain intact. Error diagnosis and production admission remain intact; no release is authorized.

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
| 0.4 | 2026-10-15 | @imp researcher | Recover the explicit #438 quarantine/reset rationale and implementation evidence; record #460's deliberate query/command preservation boundary and qualify route 3 as a recovery-policy choice. |
| 0.5 | 2026-10-15 | @imp researcher | Compare retained planning-command quarantine with pure-read policy; distinguish failed-precondition effects from successful writes and propose a bounded, unapproved scope amendment. |
| 0.6 | 2026-10-15 | @imp researcher | Capture owner approval for route 3 and the targeted planning-command correction; explain the existing plan-query phase-enrichment path without adding a third repair. |





