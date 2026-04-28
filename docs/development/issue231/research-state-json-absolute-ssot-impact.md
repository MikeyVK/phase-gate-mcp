<!-- c:\temp\st3\docs\development\issue231\research-state-json-absolute-ssot-impact.md -->
<!-- template=research version=custom created=2026-04-27T00:00Z updated=2026-04-28 -->
# Issue #231: Revised Impact Assessment for State.json SSOT with Persistent Subphase
**Status:** FINAL  
**Version:** 2.1  
**Last Updated:** 2026-04-28

---

## Purpose

Assess the implementation, test, and documentation impact of promoting `.st3/state.json` to the primary reporting source for workflow status while retaining `sub_phase` as a supported part of the user-facing contract.

This revision supersedes the earlier lower-impact recommendation to phase out subphases. The product decision is now explicit: red, green, and refactor remain meaningful during implementation and should be persisted rather than inferred only from commit history.

---

## Scope

**In Scope:**
- Current resolver precedence and read-side inconsistency
- Readiness of the current architecture for persistent subphase support
- Production files that must change to persist and report `current_sub_phase`
- Production files that are affected only conditionally or as supporting seams
- Test files that must change under the persistent-subphase design
- Documentation and instruction-layer implications of making `state.json` primary for reporting

**Out of Scope:**
- Implementing the redesign in this document
- Reopening broader #292 write-integrity scope beyond the already established mutation seam
- Removing subphases from commit conventions
- Broad CQRS redesign of the workflow subsystem

---

## Prerequisites

Read these first:
1. `docs/development/issue231/research.md`
2. `docs/development/issue231/design.md`
3. `docs/development/archive/issue138/design.md`
4. `docs/development/archive/issue138/research.md`
5. `docs/development/archive/issue273/research.md`
6. `mcp_server/managers/state_repository.py`
7. `mcp_server/managers/workflow_state_mutator.py`
8. `mcp_server/managers/phase_state_engine.py`
9. `mcp_server/tools/git_tools.py`
10. `mcp_server/managers/workflow_status_resolver.py`
11. `.st3/config/workphases.yaml`
12. `.st3/config/phase_contracts.yaml`

---

## Problem Statement

The platform currently has a write-side truth and a read-side truth that can diverge.

- Write-side phase and cycle transitions are persisted in `.st3/state.json`.
- Read-side workflow reporting still prefers commit-scope when commit detection is high confidence.
- `sub_phase` is currently known in commit flows and reporting, but not persisted in branch state.

During live validation on 2026-04-27, forced transitions updated `.st3/state.json` first to `current_phase="implementation"` with `current_cycle=3` and later to `current_phase="research"`, while `get_work_context()` continued to render `implementation -> c1_refactor` because `WorkflowStatusResolver` preferred commit-scope for phase and subphase.

The issue is therefore not only precedence. It is also data ownership:
- `state.json` owns phase and cycle
- commit history currently owns effective `sub_phase`
- user-facing tools merge those answers into a hybrid status view

The new product decision is to keep subphase as first-class workflow context during implementation and documentation, but to stop treating commit history as the primary reporting source.

---

## Decision Baseline for This Revision

This research revision assumes the following target direction:

1. `.st3/state.json` becomes the primary reporting source for workflow status.
2. `sub_phase` remains part of the supported user-facing contract.
3. `sub_phase` therefore needs to be persisted in workflow state.
4. Commit history may remain as fallback or diagnostics when state is absent, but it no longer overrides valid persisted state.
5. No new repository or mutex layer is introduced if the existing mutation seam is already sufficient.

---

## Current Baseline

### 1. What state owns today

`BranchState` currently persists:
- `current_phase`
- `current_cycle`
- `last_cycle`
- `cycle_history`
- branch metadata and transition audit trail

It does **not** persist any subphase field.

### 2. What commit flows own today

`GitCommitTool.execute()` receives:
- `workflow_phase`
- `sub_phase`
- `cycle_number`

That data is used to:
- validate commit scope through `ScopeEncoder`
- resolve commit type through `PhaseContractResolver`
- format the commit message through `GitManager.commit_with_scope()`

It is **not** written back to branch state.

### 3. What reporting owns today

`WorkflowStatusResolver.resolve_current()` currently:
1. loads persisted phase and cycle from state
2. parses the latest commit through `CommitPhaseDetector`
3. returns commit-derived phase and subphase when detection confidence is high
4. only falls back to state when commit-scope is missing or weak

This makes reporting hybrid rather than state-owned.

### 4. What enforcement owns today

The enforcement path already treats `.st3/state.json` as authoritative for:
- current phase checks
- current cycle checks
- forced transition audit trail

So the proposed redesign mainly affects reporting and persistence completeness, not enforcement ownership.

---

## Readiness Conclusion

**Conclusion Up Front: YES**

The current architecture is structured enough to add subphase persistence without breaking the foundation.

The required change fits the existing seams with one deliberate addition:
- add `current_sub_phase` to `BranchState`
- add one new public write seam on `PhaseStateEngine`, for example `record_sub_phase(branch, sub_phase)`
- call that seam from `GitCommitTool.execute()` after a successful commit
- teach `WorkflowStatusResolver` to prefer persisted `current_sub_phase`

No new repository, lock manager, or parallel state subsystem is required.

---

## Findings

### Finding 1 - `BranchState` is safely extensible

`BranchState` uses `frozen=True`, `extra="forbid"`, and immutable copying via `with_updates(**kwargs)`.

Adding:

```python
current_sub_phase: str | None = None
```

is backward-compatible for existing persisted files because the field can default to `None`.

Effects:
- existing `state.json` files still deserialize
- `with_updates()` already supports additive schema evolution
- `FileStateRepository.save()` already serializes whatever the model contains

**Conclusion:** the state schema is ready for this extension.

### Finding 2 - `WorkflowStateMutator` is already the correct write seam

`WorkflowStateMutator.apply(branch, mutate_fn)` already provides:
- coordinated lock acquisition
- fresh state load
- immutable state transform
- branch identity validation
- repository save

This means subphase persistence does not need:
- a new mutex
- a new repository
- a second state file
- a new mutation service

A subphase mutation can already fit the current seam:

```python
mutator.apply(branch, lambda s: s.with_updates(current_sub_phase=sub_phase))
```

**Conclusion:** the write infrastructure is already in place.

### Finding 3 - `GitCommitTool` is the correct trigger point

`sub_phase` is known at commit time, not at phase-transition time.

The current execution flow is:

```text
GitCommitTool.execute()
  -> ScopeEncoder validation
  -> commit_type resolution
  -> GitManager.commit_with_scope(..., sub_phase=params.sub_phase)
  -> adapter.commit(...)
```

This is the first point where all of the following are true together:
- the requested `sub_phase` is available
- the value has passed config validation
- the commit has actually succeeded
- the current branch is known

`GitCommitTool` already receives `state_engine=self.phase_state_engine` from `server.py`.

**Conclusion:** the correct write trigger is a post-commit call from `GitCommitTool.execute()`, not a resolver-side fallback or a direct tool-to-mutator shortcut.

### Finding 4 - `PhaseStateEngine` is the correct owner for the new seam

`PhaseStateEngine` already owns workflow lifecycle hooks such as:
- `on_enter_implementation_phase()`
- `on_exit_implementation_phase()`

It already coordinates its writes through the mutator boundary.

Adding a new public method such as:

```python
def record_sub_phase(self, branch: str, sub_phase: str | None) -> None:
    ...
```

fits the existing ownership model better than injecting `IWorkflowStateMutator` directly into `GitCommitTool`.

Why this is the better seam:
- tools stay on engine-level workflow semantics rather than raw state writes
- mutation coordination remains inside the engine and mutator collaboration
- clearing rules stay centralized with the rest of the workflow lifecycle

**Conclusion:** one new engine method is the right extension point.

### Finding 5 - Clearing semantics are already modeled

`on_exit_implementation_phase()` already clears `current_cycle` and preserves `last_cycle`.

The same pattern can clear `current_sub_phase`:

```python
updated_state = state.with_updates(
    last_cycle=current_cycle,
    current_cycle=None,
    current_sub_phase=None,
)
```

This also applies to transitions out of implementation through the normal phase lifecycle.

**Conclusion:** no new lifecycle model is needed. The clearing pattern already exists.

### Finding 6 - `WorkflowStatusResolver` changes are real but localized

After schema extension, resolver logic can read:
- `persisted_phase`
- `persisted_cycle`
- `persisted_sub_phase`

The main behavior change becomes:
- if state exists and is valid for the branch, return phase, cycle, and subphase from state
- use commit detection only when state is absent, invalid, or intentionally consulted for diagnostics

The resolver is already structurally split into:
- a state path
- a commit detection path

So the change is a precedence shift and field sourcing change, not a redesign.

A design detail still needs an explicit contract decision: whether persisted state stores the raw subphase such as `red` and lets readers derive `c1_red` from `current_cycle`, or stores the rendered token directly. Current commit-scope parsing yields values like `c1_refactor`, because commit scopes are encoded as `P_IMPLEMENTATION_SP_C1_REFACTOR` and the resolver forwards that token today.

**Conclusion:** resolver impact is moderate and localized.

### Finding 7 - Config and commit-validation layers remain authoritative for validation, not persistence

The following remain valid and useful under persistent subphase support:
- `.st3/config/workphases.yaml` as subphase whitelist per phase
- `.st3/config/phase_contracts.yaml` as commit type mapping per subphase
- `ScopeEncoder` as strict subphase validator and scope formatter
- `PhaseContractResolver.resolve_commit_type()` as commit-type lookup for a valid subphase

These layers do not need to own persistence. They remain validation and formatting sources.

**Conclusion:** persistent subphase does not require replacing the config-driven commit model.

### Finding 8 - Several earlier blast-radius gaps were specific to the phased-out-subphase option

The earlier QA critique correctly identified omitted files for the **subphase phase-out** path, especially:
- `scope_encoder.py`
- `phase_detection.py`
- `phase_contract_resolver.py`
- `.st3/config/phase_contracts.yaml`
- `tests/mcp_server/core/test_scope_encoder.py`
- `tests/mcp_server/core/test_phase_detection.py`
- `tests/mcp_server/integration/test_workflow_cycle_e2e.py`
- `tests/mcp_server/managers/test_git_manager_config.py`

Own research confirms those files were underrepresented in the previous blast-radius map.

However, under the **persistent-subphase** direction, they reclassify as follows:
- `scope_encoder.py`, `phase_contract_resolver.py`, `workphases.yaml`, and `phase_contracts.yaml` become mostly supporting or unchanged
- `phase_detection.py` and its tests remain relevant only if commit-history fallback or diagnostics remain part of the resolver contract
- `test_workflow_cycle_e2e.py` stays high impact because output sourcing changes even if subphase survives

**Conclusion:** the QA gaps were valid, but their severity depends on the chosen design direction.

### Finding 9 - The composition root is already mostly ready

`server.py` already injects `state_engine` into `GitCommitTool`.

That means the preferred design does **not** require:
- new GitCommitTool constructor dependencies
- mutator injection into tools
- new server wiring for the write trigger itself

Potential server changes are limited to whatever the `PhaseStateEngine` constructor already needs for its internal collaborators, which are already present after the #231/#292 refactor.

**Conclusion:** composition-root impact is low.

### Finding 10 - The instruction layer stays aligned if subphase remains supported

Because the product decision is now to retain and persist subphase, the current workflow instructions that use `sub_phase="red|green|refactor"` do not become invalid.

This avoids a large instruction-layer break in:
- `agent.md`
- tool documentation
- examples for TDD commit usage

**Conclusion:** retaining subphase materially reduces documentation and behavior churn compared with phasing it out.

---

## Production Impact Matrix

### Direct production changes

| File | Why it changes | Impact |
|------|----------------|--------|
| `mcp_server/managers/state_repository.py` | Add `current_sub_phase: str | None = None` to `BranchState` | High |
| `mcp_server/managers/phase_state_engine.py` | Add `record_sub_phase()` and clear `current_sub_phase` on implementation exit and related transitions | High |
| `mcp_server/tools/git_tools.py` | `GitCommitTool.execute()` should call the new engine seam after successful commit | High |
| `mcp_server/managers/workflow_status_resolver.py` | Read `current_sub_phase` from state and make state primary for reporting | Medium |

### Likely unchanged or low direct impact

| File | Why |
|------|-----|
| `mcp_server/managers/workflow_state_mutator.py` | Existing atomic mutation seam already sufficient; no new concept required |
| `mcp_server/server.py` | `GitCommitTool` already receives `state_engine`; likely no new wiring needed |
| `mcp_server/tools/discovery_tools.py` | Consumer can likely remain unchanged if resolver contract stays stable |
| `mcp_server/managers/project_manager.py` | Consumer can likely remain unchanged if resolver still returns `sub_phase` |
| `mcp_server/managers/enforcement_runner.py` | Already state-first for enforcement |
| `mcp_server/managers/qa_manager.py` | Not part of subphase lifecycle |

### Conditional or fallback-related production impact

| File | Why it may change | Impact |
|------|-------------------|--------|
| `mcp_server/core/phase_detection.py` | Only if commit-history fallback or diagnostics remain part of reporting semantics | Low to Medium |
| `mcp_server/core/commit_phase_detector.py` | Only if resolver still consults commit history when state is absent | Low to Medium |
| `mcp_server/core/scope_encoder.py` | Validation stays useful; logic changes only if commit-scope format itself changes | Low |
| `mcp_server/managers/phase_contract_resolver.py` | Commit-type mapping stays valid; direct changes only if subphase semantics broaden or narrow | Low |
| `.st3/config/workphases.yaml` | Current subphase whitelist remains correct; only changes if the supported set is revised | Low |
| `.st3/config/phase_contracts.yaml` | Current `commit_type_map` remains correct; only changes if commit policy changes | Low |

---

## Test Impact Matrix

### Directly impacted tests

| Test file | Why it changes | Impact |
|-----------|----------------|--------|
| `tests/mcp_server/unit/managers/test_workflow_status_resolver.py` | Resolver precedence changes from commit-first to state-first with persisted subphase | High |
| `tests/mcp_server/unit/tools/test_git_tools.py` | `GitCommitTool` will gain post-commit state synchronization behavior | High |
| `tests/mcp_server/integration/test_workflow_cycle_e2e.py` | End-to-end workflow context should now source subphase from persisted state rather than commit history | High |
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | Many assertions depend on resolver-derived phase source and subphase output | Medium to High |
| `tests/mcp_server/unit/managers/test_project_manager.py` | `phase_source` and `phase:sub_phase` formatting assertions depend on resolver semantics | Medium |
| `tests/mcp_server/unit/tools/test_project_tools.py` | Resolver-injection tests may need updated `phase_source` expectations | Low to Medium |

### New tests likely required

| Test area | Why new coverage is needed |
|-----------|---------------------------|
| `PhaseStateEngine.record_sub_phase()` | New public seam needs direct unit coverage |
| implementation-exit clearing | Verify `current_sub_phase` clears together with implementation lifecycle exit |
| post-commit persistence | Verify subphase is recorded only after successful commit |
| persisted-state fallback | Verify resolver uses state-owned subphase when state exists |
| missing-state behavior | Verify behavior when `state.json` is absent and commit fallback is enabled or disabled |

### Supporting tests with low or conditional impact

| Test file | Why |
|-----------|-----|
| `tests/mcp_server/core/test_scope_encoder.py` | High impact only for subphase phase-out; low impact for persistence path because validation rules still stand |
| `tests/mcp_server/core/test_phase_detection.py` | Changes only if commit-history fallback or diagnostics contract changes |
| `tests/mcp_server/managers/test_git_manager_config.py` | Commit message formatting with subphase remains valid under persistence path |
| `tests/mcp_server/unit/managers/test_git_manager.py` | Mostly unchanged unless commit formatting contract changes |
| `tests/mcp_server/unit/managers/test_git_manager_skip_paths.py` | Mostly unchanged unless commit formatting contract changes |
| `tests/mcp_server/unit/managers/test_git_manager_no_file_open.py` | Mostly unchanged unless commit formatting contract changes |

---

## Documentation and Instruction Impact

### Documents that should be revised

| Document | Why |
|----------|-----|
| `docs/development/issue231/research.md` | Needs cross-reference to the new persistent-subphase direction |
| `docs/development/issue231/design.md` | Must explicitly model `current_sub_phase` as persisted state and define the new write seam |
| `docs/development/archive/issue138/design.md` | Historical dual-source rationale remains useful, but current design direction now intentionally departs from it |
| `docs/development/archive/issue138/research.md` | Same as above; should be treated as historical context rather than target behavior |
| `docs/reference/mcp/tools/git.md` | Commit examples remain valid, but documentation should clarify that subphase is now also persisted |
| `docs/reference/mcp/MCP_TOOLS.md` | Same clarification for `git_add_or_commit` |

### Instruction-layer impact

Unlike the earlier subphase phase-out direction, the current choice preserves the existing agent and operator language around:
- red
- green
- refactor

That means `agent.md` and related workflow instructions are not invalidated by the redesign. They only need alignment with the new state ownership model.

---

## Risks and Regressions

### 1. State freshness becomes more important

Once reporting reads persisted subphase from state, a failed or skipped post-commit update becomes visible immediately in user-facing tools.

### 2. Partial implementation risk

If resolver precedence changes before `GitCommitTool` persists subphase, the platform will regress to missing subphase in user-facing status.

### 3. Lifecycle consistency risk

If `current_sub_phase` is persisted but not cleared on implementation exit, state can retain stale subphase across later phases.

### 4. Overreach risk

If `GitCommitTool` writes directly through the mutator instead of going through `PhaseStateEngine`, workflow-state ownership will leak into tool code and weaken the current architecture.

### 5. Fallback ambiguity

If commit-history fallback remains, the platform must define whether commit-derived subphase is:
- diagnostic only
- temporary reporting fallback when state is absent
- or a hard error if state and commit history disagree

---

## Implementation Options

### Option A - Persistent subphase with state-primary reporting (recommended)

- Add `current_sub_phase` to `BranchState`
- Persist it through `PhaseStateEngine.record_sub_phase()`
- Call that seam from `GitCommitTool.execute()` after a successful commit
- Make resolver prefer state for phase, cycle, and subphase
- Use commit history only when state is absent or explicitly consulted for diagnostics

**Pros:**
- Preserves red, green, refactor as meaningful workflow context
- Aligns reporting with persisted state and forced transitions
- Uses existing write seam and existing injection graph
- Avoids tearing up current instruction and commit conventions

**Cons:**
- Requires a new public engine method
- Makes state synchronization after commit part of the workflow contract

**Assessment:** best fit for the new product decision with low architectural risk.

### Option B - Persistent subphase plus strict state-only reporting

Same as Option A, but with no commit-history fallback at all.

**Pros:**
- Cleanest SSOT story
- Simplest resolver semantics once state is guaranteed to exist

**Cons:**
- Missing or invalid `state.json` becomes immediately user-visible
- Removes a potentially useful recovery path during degraded scenarios

**Assessment:** viable, but should be chosen explicitly rather than as an accidental side effect.

### Option C - Keep hybrid resolver and only add subphase persistence

Persist subphase, but still let commit-scope override state when detection is high confidence.

**Pros:**
- Smaller behavioral shift
- Retains historical observability as primary reporting source

**Cons:**
- Does not solve the actual inconsistency observed in live validation
- Leaves reporting non-SSOT even after new state fields are added

**Assessment:** not recommended if the goal is coherent state-owned reporting.

---

## Recommendation

Issue #231 should stop at documentation. The deeper analysis in this cycle changed the implementation boundary.

### Final disposition for #231

- Do not continue with direct persistent-subphase or state-SSOT implementation on this branch.
- Treat the current research as a boundary clarification exercise, not as authorization to harden runtime semantics inside #231.
- Close out #231 in documentation phase with explicit follow-up sequencing.

### Why implementation stops here

- The MCP server does not yet have one clean runtime contract for workflow orchestration.
- `workflows.yaml` owns runtime phase order.
- `phase_contracts.yaml` owns runtime phase behavior such as cycle semantics and exit contracts.
- `workphases.yaml` is still consulted in runtime paths for phase metadata and subphase validation, which means the configuration boundary is not yet clean enough to make `state.json` authoritative without first resolving contract ownership.
- Because of that split, pushing persistent subphase semantics directly into state in #231 would risk encoding unstable contract assumptions.

### Follow-up issue set

1. Reuse existing issue #271 as follow-up 1: runtime contract closure.
   Rationale: it already captures the overlap around workflow-phase ownership and `phase_contracts.yaml` as runtime authority.
2. Use issue #298 as follow-up 2: make `state.json` authoritative after runtime contract closure.
   Rationale: this preserves the sequencing discovered in #231 instead of forcing state-SSOT work ahead of contract cleanup.

### Sequencing rule

Issue #298 must not start as an implementation effort until issue #271 has closed the contract-side ambiguity or has produced an equivalent resolved orchestration contract.

## Open Questions

These questions are now handed off to follow-up issues #271 and #298 rather than being resolved inside #231.

- Should persisted state store raw implementation subphase values such as `red`, `green`, and `refactor`, or store the rendered token style currently surfaced by commit detection, such as `c1_red` and `c1_refactor`?
- Should `current_sub_phase` be supported only for implementation, or for all phases that currently define subphases in `workphases.yaml`?
- Should `PhaseStateEngine.record_sub_phase()` accept any validated subphase, or should it explicitly constrain persistent subphase support to implementation first?
- On implementation entry, should `current_sub_phase` remain `None` until the first successful commit, or should the engine initialize it proactively?
- If commit history remains as fallback, should a mismatch between persisted subphase and latest commit become a warning, a diagnostic note, or an error?
- Should the commit guard eventually validate persisted subphase too, or remain phase-and-cycle only?

---

## Related Documentation

- `docs/development/issue231/research.md`
- `docs/development/issue231/design.md`
- `docs/development/archive/issue138/research.md`
- `docs/development/archive/issue138/design.md`
- `docs/development/archive/issue273/research.md`
- `mcp_server/managers/state_repository.py`
- `mcp_server/managers/workflow_state_mutator.py`
- `mcp_server/managers/phase_state_engine.py`
- `mcp_server/tools/git_tools.py`
- `mcp_server/managers/workflow_status_resolver.py`
- `.st3/config/workphases.yaml`
- `.st3/config/phase_contracts.yaml`
- `tests/mcp_server/unit/managers/test_workflow_status_resolver.py`
- `tests/mcp_server/unit/tools/test_git_tools.py`
- `tests/mcp_server/unit/tools/test_discovery_tools.py`
- `tests/mcp_server/unit/managers/test_project_manager.py`
- `tests/mcp_server/unit/tools/test_project_tools.py`
- `tests/mcp_server/core/test_scope_encoder.py`
- `tests/mcp_server/core/test_phase_detection.py`
- `tests/mcp_server/integration/test_workflow_cycle_e2e.py`
- `tests/mcp_server/managers/test_git_manager_config.py`

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-27 | Agent | Initial impact assessment for promoting `.st3/state.json` to absolute SSOT |
| 1.1 | 2026-04-27 | Agent | Added the temporary subphase phase-out direction and expanded findings around runtime state vs commit metadata |
| 2.0 | 2026-04-28 | Agent | Reworked the research around the new product decision to keep subphases, added readiness analysis for persistent subphase, corrected the blast-radius matrix, and reclassified previously omitted config and test surfaces |
| 2.1 | 2026-04-28 | Agent | Reclassified #231 as documentation-only close-out, recorded overlap with existing issue #271, and captured new follow-up issue #298 for post-contract state.json SSOT work |
