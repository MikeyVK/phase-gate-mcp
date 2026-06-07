<!-- docs\development\issue357\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-27T20:33Z updated=2026-05-29T00:00Z -->
# Fix agent lifecycle: parent detection, submit_pr base, end-issue safety
**Status:** DRAFT  
**Version:** 1.3  
**Last Updated:** 2026-05-29
**Last Updated:** 2026-05-28

---

## Purpose
**In Scope:**
Lifecycle coordination surfaces for `start-issue`, `end-issue`, `@imp` startup, `submit_pr` base resolution, and `context_loaded` bootstrap behavior on child branches that inherit parent state. Also in scope: the `check_merge` MCP tool — a new thin read-only tool required by the post-merge verification step in `end-issue`.

**Out of Scope:**
Production feature work outside lifecycle coordination; generic git safety redesign unrelated to the reported bug family; implementation planning, TDD cycles, or exact patch sequencing.
Lifecycle coordination surfaces for `start-issue`, `end-issue`, `@imp` startup, `submit_pr` base resolution, and `context_loaded` bootstrap behavior on child branches that inherit parent state.

**Out of Scope:**
Production feature work outside lifecycle coordination; generic git safety redesign unrelated to the reported bug family; implementation planning, TDD cycles, or exact patch sequencing.

## Prerequisites

Read these first:
1. `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`
2. `docs/coding_standards/DOCUMENTATION_STANDARD.md`
3. Issue `#357`
4. `docs/development/issue268/research.md`
5. `docs/development/issue345/validation.md`
6. `docs/development/issue354/validation.md`

---

## Problem Statement

Issue `#357` groups a family of lifecycle-coordination defects that were discovered during live epic execution. Current repo evidence shows the family is real, but not all five originally reported sub-problems are still live in the same form:

- one prompt sub-gap is already partially fixed in the current branch state
- several remaining gaps are confirmed directly in prompt, tool, and enforcement code
- one originally reported failure mode has shifted from a hard crash to an incoherent bootstrap path because `get_work_context()` now degrades gracefully when branch state is absent

The research task is therefore not only to confirm the remaining defects, but also to separate live defects from already-landed prior fixes so later phases do not redesign stale problems.

## Research Goals

- Verify which reported lifecycle gaps are still live in the repository and which are already partially resolved or stale.
- Identify the concrete production files, boundaries, and tests affected by the remaining defects.
- Clarify the supported lifecycle contract from prior repository decisions and distinguish it from accidental dependence on faulty behavior.
- Define the corrected behavior that design and planning should treat as the target outcome.

---

## Background

Issue `#268` established the lifecycle symmetry model: branch start and post-merge cleanup are lifecycle-boundary moments where normal in-phase `get_work_context()` behavior is not authoritative yet. Everything between those boundaries is in-phase work driven by branch-local state.

Issue `#345` established the explicit `end-issue` prompt contract, but its validation also records that prompt behavior is validated by human review rather than pytest. Issue `#354` later corrected `end-issue` to use `get_pr()` for `base_branch` and PR body after merge. Issue `#357` sits on top of that prior art: it is not a blank-slate lifecycle redesign, but a bug-fix issue for remaining coordination gaps and stale instructions.

---

## Observed vs Expected Behavior

| Surface | Observed now | Expected corrected behavior |
|---|---|---|
| `start-issue.prompt.md` child flow | `@co` still calls `initialize_project(...)` in the common sequence before handing off non-epic branches | child-branch initialization should not remain owned by `@co` |
| `start-issue.prompt.md` epic parent override | explicit `parent_branch` override is no longer present in the current file | keep reflog-based parent detection, do not reintroduce manual override |
| `@imp` startup on fresh branch | `get_work_context()` is still mandated first, but now returns bootstrap degradation when state is absent | startup should reflect the lifecycle-boundary exception instead of pretending an uninitialized branch is already in-phase |
| `submit_pr` base selection | falls back directly to `git_config.default_base_branch` when `params.base` is absent | should respect branch-local `parent_branch` before defaulting to repo-wide base |
| `end-issue.prompt.md` cleanup safety | merge is confirmed, `get_pr()` is read, then checkout and branch deletion proceed without `git_pull` or merge-SHA reachability verification | child branch cleanup should halt unless the merged content is verified on the parent branch |
| `check_context_loaded` bootstrap gate | gate is inactive only when `state.json` is absent | inherited parent `state.json` should not block child-branch initialization when the state belongs to a different issue |

---

## Findings

### F1 - One originally reported prompt defect is already partially fixed

The current `start-issue.prompt.md` no longer passes an explicit `parent_branch` argument to `initialize_project(...)`. That means the live defect is narrower than the issue body originally described: the bad parent override is already gone in the current prompt, so later phases should not spend effort fixing a path that no longer exists.

**Evidence:**
- `.github/prompts/start-issue.prompt.md` step 4 calls `initialize_project(issue_number=ISSUE_NUMBER, issue_title="{title}", workflow_name=WORKFLOW_TYPE)` with no `parent_branch`
- `mcp_server/tools/project_tools.py` already auto-detects `parent_branch` from reflog when the parameter is absent

**Consequence:**
- the live start-issue bug is now ownership and ordering on child branches, not explicit parent override
- research should record issue-body drift so design does not target a stale sub-problem

### F2 - `start-issue` still violates the intended `@co` -> `@imp` hand-off boundary for child branches

Although the explicit parent override is gone, the prompt still runs `initialize_project(...)` in the common sequence before the non-epic hand-off. That keeps child-branch initialization under `@co`, even though the same prompt later says `@imp` becomes the first agent to call `get_work_context()` before the first commit or further write action.

**Evidence:**
- `.github/prompts/start-issue.prompt.md` step 4 initializes the project before the workflow splits into epic vs non-epic paths
- the non-epic section then says `@co` stops and `@imp` becomes the first agent to call `get_work_context()`

**Consequence:**
- the prompt currently encodes two different ownership models in one flow
- the live defect is a lifecycle-boundary contract mismatch, not a missing tool capability
- `initialize_project` is a `BranchMutatingTool` and is not exempt from the `check_context_loaded` gate; `@imp` cannot supply the required `issue_number`, `issue_title`, and `workflow_name` inputs without the `start-issue` context that `@co` holds; therefore `@co` is the architecturally required initialization owner, not a style preference

### F3 - `@imp` startup precondition is not explicit: the `@co`-must-initialize contract is missing

`@imp` startup correctly mandates `get_work_context()` as the first action for every session. The startup design is not the bug. The bug is that neither `imp.agent.md` nor any lifecycle prompt states the precondition: the branch must already be initialized by `@co` before `@imp` starts. Without that precondition, the startup rule silently appears to tolerate uninitialized branches via graceful degradation, but graceful degradation is a silent failure, not correct behavior.

The `@co`-owns-init constraint is architecturally required: `initialize_project` is a `BranchMutatingTool` subject to the `check_context_loaded` gate, is not in the exempt list, and requires inputs (`issue_number`, `issue_title`, `workflow_name`) that `@co` holds from the `start-issue` flow and that `@imp` cannot supply reliably without user input or branch-name inference. Once `@co` has initialized and F6 is fixed, `@imp`'s unconditional `get_work_context()` at Go is architecturally valid.

**Evidence:**
- `.github/agents/imp.agent.md` startup protocol requires `get_work_context` first but states no `@co`-must-initialize precondition
- `mcp_server/tools/project_tools.py` `InitializeProjectTool` inherits `BranchMutatingTool` and is not exempt from `check_context_loaded`
- `docs/development/issue268/research.md` defines branch start as a lifecycle-boundary exception; the corollary is that `@co` owns that boundary, not `@imp`

**Consequence:**
- later phases should add an explicit `@co`-must-initialize precondition to `imp.agent.md` and any relevant lifecycle prompt
- do not add a recovery path in `@imp` startup for uninitialized branches; an uninitialized branch reaching `@imp` is a process violation, not a tool robustness problem

### F4 - `submit_pr` still ignores branch-local parent state when `base` is omitted

`SubmitPRTool.execute()` still computes the target base as `params.base or self._git_manager.git_config.default_base_branch`. It does not consult branch-local `state.json.parent_branch`, so child branches rooted on an epic can still be silently retargeted to the repo-wide default base.

**Evidence:**
- `mcp_server/tools/pr_tools.py` sets `base = params.base or self._git_manager.git_config.default_base_branch`
- no branch-state lookup appears in the tool body
- issue `#357` is therefore still correct on this point

**Consequence:**
- the base-selection defect is fully live
- affected validation surface includes `tests/mcp_server/integration/test_submit_pr_atomic_flow.py`, `tests/mcp_server/integration/test_ready_phase_enforcement.py`, and server/request tests for `submit_pr`

### F5 - `end-issue` already uses `get_pr()` correctly, but cleanup remains unsafe

The current `end-issue.prompt.md` already includes the `get_pr()` step introduced by issue `#354`, and it already uses `base_branch` from the PR instead of `parent_branch` from `get_work_context()`. The remaining defect is narrower: after merge confirmation, the prompt still checks out the base branch and immediately deletes the child branch without a `git_pull` or merge-SHA reachability verification step.

**Evidence:**
- `.github/prompts/end-issue.prompt.md` step 3 reads `get_pr(pr_number=PR_NUMBER)` and records `head_branch` plus `base_branch`
- `.github/prompts/end-issue.prompt.md` step 4 checks out `base_branch`
- `.github/prompts/end-issue.prompt.md` step 5 deletes the branch with `git_delete_branch(mode="both")`
- `docs/development/issue354/validation.md` confirms the prompt was intentionally updated to source `base_branch` from `get_pr()`

**Consequence:**
- issue `#357` should not reopen the already-fixed parent-source problem from issue `#354`
- the live bug is the missing post-merge verification barrier before destructive cleanup
- prompt coverage remains primarily human-reviewed, per `docs/development/issue345/validation.md`

### F6 - The inherited `state.json` bootstrap problem remains live in enforcement

`_handle_check_context_loaded(...)` still disables the gate only when `state.json` does not exist. On child branches created from a parent branch with committed state, that predicate remains false even though the state belongs to a different issue. Nothing in the current handler checks whether the stored issue number matches the current branch.

**Evidence:**
- `mcp_server/managers/enforcement_runner.py` returns early only when `(self.server_root / "state.json").exists()` is false
- no issue-number comparison appears in the handler
- an existing parser already exists: `mcp_server/config/schemas/git_config.py::extract_issue_number()`
- existing production code already reuses that parser in `mcp_server/managers/state_reconstructor.py`

**Consequence:**
- issue `#357` is correct that the bootstrap predicate is too weak
- later phases should treat structured branch state as the primary source when it is trusted; if bootstrap mismatch logic must infer branch identity before state is trusted, reuse the existing `GitConfig.extract_issue_number()` helper rather than inventing a second parser
- affected regression surface includes `tests/mcp_server/integration/test_context_loaded_enforcement.py`
- F6 also blocks `@co`'s own `initialize_project` call when creating an epic-child branch whose inherited `state.json` comes from a parent with committed state; the fix (extending the bootstrap predicate to bypass when state belongs to a different issue) is the enabler for the `@co`-always-initializes model to function correctly on epic-child branches

### F7 - The strongest prior art already defines the supported lifecycle contract

The repo already contains the contract that later phases should preserve:

- issue `#268`: branch start and post-merge cleanup are lifecycle-boundary exceptions, not ordinary in-phase `get_work_context()` moments
- issue `#345`: `end-issue` is an explicit `@co` lifecycle surface, not an automated merge pipeline
- issue `#354`: `end-issue` must use `get_pr()` for merged PR metadata, including `base_branch` and PR body

**Consequence:**
- no broad lifecycle redesign is needed in issue `#357`
- the task is to bring prompts, startup rules, and enforcement behavior back into alignment with established repo contracts

### F8 - The affected surface includes both machine-tested code and human-reviewed prompt contracts

This bug family spans multiple validation styles:

| Surface | Current validation mode |
|---|---|
| `SubmitPRTool` | integration and unit tests |
| `check_context_loaded` enforcement | integration tests |
| `GetWorkContextTool` bootstrap/degradation behavior | unit tests |
| lifecycle prompts (`start-issue`, `end-issue`) | primarily human review and workflow artifact validation |
| agent startup instruction files | document review, not direct pytest coverage |

**Consequence:**
- design and planning must account for both code-test blast radius and prompt/document review surfaces
- success cannot be judged only by pytest; the prompt contracts themselves are part of the bug surface

### F9 - The `end-issue` cleanup gate references a non-existent `check_merge` MCP tool

The redesigned `end-issue.prompt.md` (step 6) mandates `check_merge(merge_sha=MERGE_SHA)` as the
reachability gate before branch deletion. No such tool exists in the MCP server. When `@co`
executes the `end-issue` flow, step 6 fails with "tool not found."

**Evidence:**
- `.github/prompts/end-issue.prompt.md` step 6 calls `check_merge(merge_sha=MERGE_SHA)` (committed on this branch)
- `.github/agents/co.agent.md` lists `phase-gate-mcp/check_merge` in its `tools:` allowlist
- `mcp_server/tools/git_tools.py` contains no `CheckMergeTool` class
- `mcp_server/adapters/git_adapter.py` has no `is_ancestor` method; existing `merge_base` calls compute common ancestors, not reachability from HEAD
- `mcp_server/managers/git_manager.py` has no `is_ancestor` delegation
- `mcp_server/server.py` has no `CheckMergeTool` registration in its `tools` list

**Git primitive:** `git merge-base --is-ancestor <sha> HEAD`
- Exit 0: SHA is a reachable ancestor of HEAD → reachable
- Exit 1: SHA is not reachable → not reachable (expected outcome, not an error)
- Exit ≥2: git internal error → `ExecutionError`

GitPython raises `GitCommandError` on any non-zero exit. `GitAdapter.is_ancestor` must explicitly
check `GitCommandError.status == 1` to distinguish the "not an ancestor" case from a real git error.

**Architectural fit (confirmed from codebase evidence):**
- Read-only: inherits `BaseTool`, not `BranchMutatingTool`; `enforcement_event = None`
- Constructor: `CheckMergeTool(manager: GitManager)` — no additional dependencies
- Input: `CheckMergeInput(merge_sha: str)` — single required field
- Placement: addition to `mcp_server/tools/git_tools.py` (consistent with other thin git tools; no new file needed)
- Layer additions: `GitAdapter.is_ancestor`, `GitManager.is_ancestor`, `CheckMergeTool`, `server.py` registration
- No new interface needed: `GitManager` is already the abstraction boundary for simple git tools at the tool layer

**Consequence:**
- `end-issue` step 6 is broken until this tool is shipped
- the fix is the narrowest possible addition: one read-only method per layer, no new dependencies, no enforcement events
- F9 is explicitly within the confirmed scope of issue `#357`; it is the implementation counterpart of the F5 corrected behavior

---

## Supported Contract vs Defect Dependence

| Boundary | Supported contract to preserve | Faulty behavior that may be corrected |
|---|---|---|
| branch start | bootstrap is a lifecycle-boundary exception, not a normal in-phase `get_work_context()` moment | treating fresh branches as if they already have valid phase context |
| child-branch ownership | `@co` always initializes the branch before the `@imp` handoff; `initialize_project` belongs to `@co`'s lifecycle entry sequence | prompt encoding two competing ownership models: `initialize_project` in the common flow while simultaneously stating `@imp` calls `get_work_context()` before any write action |
| parent-branch truth | branch-local `parent_branch` is authoritative when present | silent fallback to repo-wide default base on non-main child branches |
| post-merge cleanup | destructive cleanup should follow authoritative merge verification | deleting branches immediately after merge acceptance without local parent verification |
| issue-number parsing | reuse existing branch-convention parser where already available | introducing duplicate branch-name parsing logic for the same convention |

---

## Approved Strategy

**Boundary / consumer scope:** internal lifecycle coordination surfaces only: prompt contracts, agent startup instructions, `submit_pr` base selection, enforcement bootstrap behavior, and the `check_merge` read-only MCP tool that implements the `end-issue` reachability gate.

**Selected strategy:** no special migration policy required.

**Supported contract vs defect dependence:**
- preserve the lifecycle-boundary model already established in issue `#268`
- preserve `end-issue` use of `get_pr()` for merged PR metadata from issue `#354`
- preserve reflog-based parent detection when `initialize_project(...)` is called without explicit override
- do not preserve incorrect child-initialization ownership, default-to-main base selection, cleanup-before-verification ordering, or inherited-state bootstrap blocking

**Constraints for later phases:**
- do not broaden issue `#357` into a generic workflow redesign or new merge orchestration system
- do not reintroduce explicit `parent_branch` overrides into `start-issue`
- if bootstrap mismatch logic must infer branch identity before structured state is trusted, reuse the existing `GitConfig.extract_issue_number()` helper rather than adding a second branch parser
- treat prompt and agent-instruction edits as first-class deliverables, not mere documentation afterthoughts
- keep `end-issue` human-invoked and `@co`-owned; this issue does not authorize automated merge flow
- `@co` must always call `initialize_project` before the `@imp` handoff on all child branches; design must not add an `@imp`-side recovery path for uninitialized branches
- `submit_pr` base resolution must inject a narrow `IBranchParentReader` interface via constructor; do not inject `PhaseStateEngine` or `IStateRepository` for this read-only lookup; fall back to `default_base_branch` on state-mismatch or absent state
- `check_merge` must be a thin read-only `BaseTool`; do not inherit `BranchMutatingTool`, do not add enforcement events; `GitAdapter.is_ancestor` must distinguish exit code 1 (not reachable, return `False`) from exit ≥2 (git error, raise `ExecutionError`) via `GitCommandError.status`

---

## Open Questions

- **[Resolved]** `@imp` startup design — `@co`-owns-init model: `@imp` startup correctly calls `get_work_context()` first; the missing piece is an explicit precondition in `imp.agent.md` stating the branch must already be co-initialized; once F6 is fixed, `@imp` can rely on `get_work_context()` unconditionally at Go
- **[Resolved]** `submit_pr` fallback read of `parent_branch` — inject a narrow `IBranchParentReader` interface (ISP §1.4/§6, DIP §1.5/§11, CQS §5); do not inject `PhaseStateEngine`; back with identity validation; fall back to `default_base_branch` on state-mismatch or absent state
- **[Resolved]** narrowest safe `end-issue` verification step — checkout of parent branch, then `git_pull`, then verify the merged SHA is reachable before branch deletion
- **[Resolved]** issue body narrowing for `#357` — lightly correct scope; record that the explicit `parent_branch` override in `start-issue` is already gone (F1) so design does not target a stale sub-problem; the live defect is child-init ownership and the `@co`-must-initialize contract
- **[Resolved]** `check_merge` implementation fit — thin read-only `BaseTool`; `GitAdapter.is_ancestor` uses `merge_base("--is-ancestor", sha, "HEAD")` with `GitCommandError.status == 1` returning `False`; `GitManager.is_ancestor` delegates; `CheckMergeTool` placed in `git_tools.py`; registered in `server.py`

---

## Assumptions

- The branch naming convention `{type}/{N}-{slug}` remains authoritative for issue-number extraction on issue branches.
- Child branches may inherit committed `.phase-gate/state.json` from their parent branches in normal workflow use.
- Prompt files and agent instruction files are active coordination surfaces, not passive documentation.

---

## Regression Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| design accidentally re-fixes already-closed `get_pr` parent-source behavior from issue `#354` | Medium | keep the research explicit that `end-issue` already uses `get_pr()` for `base_branch` |
| design treats graceful `get_work_context()` degradation as sufficient bootstrap behavior | Medium | anchor startup reasoning to issue `#268` lifecycle-boundary model |
| implementation duplicates bootstrap branch issue-number parsing logic | Medium | keep trusted structured state as primary; if bootstrap inference is still needed, cite and reuse `GitConfig.extract_issue_number()` |
| prompt fixes land without corresponding code-side enforcement changes, or vice versa | High | keep prompt, startup, tool, and enforcement surfaces in the same bug family during design/planning |
| validation ignores prompt-level behavior because prompts are not primarily pytest-covered | High | treat human-reviewed prompt contracts as part of the authoritative blast radius |
| F6 fix must not accidentally remove the bootstrap bypass for branches with truly no state; the extended predicate must check `absent OR mismatch`, not replace `absent` with `mismatch` | Medium | ensure the predicate is extended, not replaced; existing bypass for stateless branches must remain |
| `@co`-owns-init assumption breaks silently if `start-issue` is bypassed or a branch is created outside that prompt | Medium | treat `start-issue` as the single authoritative branch-entry point; document that `@imp` starting on an uninitialized branch is a process violation |
| `check_merge` `GitAdapter.is_ancestor` conflates exit code 1 (not ancestor) with real git errors | Medium | check `GitCommandError.status == 1` explicitly; test both the reachable and not-reachable paths in unit tests |

---

## Corrected Behavior For Design And Planning

Design and planning should work toward the following corrected behavior framing:

- `@co` owns all `initialize_project` calls; `@imp` always starts on a pre-initialized branch and can rely unconditionally on `get_work_context()` at session start once F6 is fixed
- `submit_pr` resolves the target base via a narrow `IBranchParentReader` interface before defaulting to repo-wide configuration; the tool does not query the full state engine for this read-only lookup
- post-merge branch cleanup does not run until the parent branch is locally updated and the merged content is verifiably reachable
- inherited parent state does not block initialization of a different child issue branch
- `check_merge` tool is present in the MCP server, registered in `server.py`, and callable by `@co` in the `end-issue` flow
- prior fixes from issues `#268`, `#345`, and `#354` are treated as binding constraints, not re-opened by accident

## Operating Modes For Agent Use

Current repo evidence supports two practical operating variants for agents, but this is an operating-model distinction rather than a schema-level mode switch. `contracts.yaml` still requires `instructions`, so the difference is created by enforcement and prompt pressure, not by removing the field.

### Variant A - Orchestrated workflow mode

Use this mode when the branch should actively steer the agent through workflow state.

**Setup actions:**
1. Keep `check_context_loaded` enabled in `.phase-gate/config/enforcement.yaml` for `branch_mutating` tools.
2. Keep `.github/agents/*.agent.md` and lifecycle prompts explicit that `get_work_context()` is the required first in-phase read.
3. Keep phase `instructions` present and directive enough to drive session behavior.
4. Preserve lifecycle-boundary exceptions from issue `#268`; do not force fresh-branch bootstrap through fake in-phase context.

**Usage pattern:**
1. Initialize the branch or transition through the correct lifecycle boundary.
2. Call `get_work_context()` at session start for in-phase work.
3. Follow the returned `sub_role_hint`, `phase_instructions`, and hand-over contract before branch-mutating actions.
4. Rely on enforcement to block writes until context is loaded.

### Variant B - Gated non-enforced workflow mode

Use this mode when the repo should retain workflow guardrails without forcing agent orchestration.

**Setup actions:**
1. Disable the `check_context_loaded` action, for example by setting `enabled: false`, while retaining other policy gates such as `check_branch_policy`, `check_pr_status`, and `check_phase_readiness` as desired.
2. Keep `instructions` present in `contracts.yaml`, because schema requires them, but make them compact, informational, and non-prescriptive rather than imperative session scripts.
3. Rewrite `.github/agents/*.agent.md` and lifecycle prompts so `get_work_context()` is optional or situational, not a hard first step.
4. Treat `get_work_context()` as an operator aid for context lookup, not as a mandatory bootstrap barrier.

**Usage pattern:**
1. Work may start from the local task anchor without first calling `get_work_context()`.
2. Agents call `get_work_context()` only when workflow state, phase guidance, or hand-over context is actually needed.
3. Branch-mutating tools remain governed by the remaining enforcement rules, but not by context-loaded bootstrap gating.
4. This mode is practically orchestration-agnostic for agents, but it is not an instructions-free product mode because schema still requires phase instructions to exist.

**Boundary note:**
Treat this distinction in later phases as an operating method and configuration posture, not as proof that the current repo already has a first-class `without_orchestration` config switch.

## Related Documentation
- **[.github/prompts/start-issue.prompt.md][related-1]**
- **[.github/prompts/end-issue.prompt.md][related-2]**
- **[.github/agents/imp.agent.md][related-3]**
- **[mcp_server/tools/discovery_tools.py][related-4]**
- **[mcp_server/tools/pr_tools.py][related-5]**
- **[mcp_server/managers/enforcement_runner.py][related-6]**
- **[mcp_server/config/schemas/git_config.py][related-7]**
- **[docs/development/issue268/research.md][related-8]**
- **[docs/development/issue345/validation.md][related-9]**
- **[docs/development/issue354/validation.md][related-10]**
- **[tests/mcp_server/integration/test_submit_pr_atomic_flow.py][related-11]**
- **[tests/mcp_server/integration/test_ready_phase_enforcement.py][related-12]**
- **[tests/mcp_server/integration/test_context_loaded_enforcement.py][related-13]**
- **[tests/mcp_server/unit/tools/test_discovery_tools.py][related-14]**
- **[mcp_server/tools/git_tools.py][related-15]**
- **[mcp_server/adapters/git_adapter.py][related-16]**
- **[mcp_server/managers/git_manager.py][related-17]**

<!-- Link definitions -->

[related-1]: .github/prompts/start-issue.prompt.md
[related-2]: .github/prompts/end-issue.prompt.md
[related-3]: .github/agents/imp.agent.md
[related-4]: mcp_server/tools/discovery_tools.py
[related-5]: mcp_server/tools/pr_tools.py
[related-6]: mcp_server/managers/enforcement_runner.py
[related-7]: mcp_server/config/schemas/git_config.py
[related-8]: docs/development/issue268/research.md
[related-9]: docs/development/issue345/validation.md
[related-10]: docs/development/issue354/validation.md
[related-11]: tests/mcp_server/integration/test_submit_pr_atomic_flow.py
[related-12]: tests/mcp_server/integration/test_ready_phase_enforcement.py
[related-13]: tests/mcp_server/integration/test_context_loaded_enforcement.py
[related-14]: tests/mcp_server/unit/tools/test_discovery_tools.py
[related-15]: mcp_server/tools/git_tools.py
[related-16]: mcp_server/adapters/git_adapter.py
[related-17]: mcp_server/managers/git_manager.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-27 | Agent | Initial scaffolded draft |
| 1.1 | 2026-05-27 | Agent | Replaced scaffold with evidence-backed lifecycle bug research, narrowed stale sub-gap, and recorded no-bridge strategy |
| 1.2 | 2026-05-28 | Agent | Added explicit operating-mode guidance for orchestrated versus gated non-enforced workflow use |
| 1.3 | 2026-05-28 | Agent | Updated F2/F3 to reflect @co-owns-init model; expanded F6 to include @co initialization blocker; resolved all open questions; added constraints and corrected behavior for @co-init and IBranchParentReader |
