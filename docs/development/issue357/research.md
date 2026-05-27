<!-- docs\development\issue357\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-27T20:33Z updated= -->
# Fix agent lifecycle: parent detection, submit_pr base, end-issue safety

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-05-27

---

## Purpose

Establish the current defect framing, verified blast radius, root-cause areas, and contract boundaries for issue #357 before design or planning.

## Scope

**In Scope:**
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

### F3 - `@imp` startup remains logically wrong for fresh branches, even though `get_work_context()` no longer crashes

`@imp` startup still mandates `get_work_context()` as the first action for every session. Current tool behavior no longer hard-fails on a fresh branch because `GetWorkContextTool.execute()` catches missing-state errors and degrades gracefully. But that only softens the failure mode; it does not make the startup sequence coherent. On a fresh branch there is no initialized workflow state yet, so a graceful empty response is still the wrong control surface for bootstrap.

**Evidence:**
- `.github/agents/imp.agent.md` startup protocol still requires `get_work_context` first
- `mcp_server/tools/discovery_tools.py` catches state-read failure and returns empty workflow/phase rather than failing
- `docs/development/issue268/research.md` explicitly defines branch start as a lifecycle-boundary exception where no machine state exists yet to query

**Consequence:**
- the live defect is now a contract mismatch between startup instructions and the lifecycle model from issue `#268`
- later phases should fix the startup contract, not treat graceful degradation as sufficient behavior

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
- later phases should prefer the existing branch issue-extraction helper over inventing a second parser
- affected regression surface includes `tests/mcp_server/integration/test_context_loaded_enforcement.py`

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

---

## Supported Contract vs Defect Dependence

| Boundary | Supported contract to preserve | Faulty behavior that may be corrected |
|---|---|---|
| branch start | bootstrap is a lifecycle-boundary exception, not a normal in-phase `get_work_context()` moment | treating fresh branches as if they already have valid phase context |
| child-branch ownership | `@co` stops at the documented hand-off boundary for non-epic branches | `@co` performing child initialization as part of the common flow |
| parent-branch truth | branch-local `parent_branch` is authoritative when present | silent fallback to repo-wide default base on non-main child branches |
| post-merge cleanup | destructive cleanup should follow authoritative merge verification | deleting branches immediately after merge acceptance without local parent verification |
| issue-number parsing | reuse existing branch-convention parser where already available | introducing duplicate branch-name parsing logic for the same convention |

---

## Approved Strategy

**Boundary / consumer scope:** internal lifecycle coordination surfaces only: prompt contracts, agent startup instructions, `submit_pr` base selection, and enforcement bootstrap behavior.

**Selected strategy:** no special migration policy required.

**Supported contract vs defect dependence:**
- preserve the lifecycle-boundary model already established in issue `#268`
- preserve `end-issue` use of `get_pr()` for merged PR metadata from issue `#354`
- preserve reflog-based parent detection when `initialize_project(...)` is called without explicit override
- do not preserve incorrect child-initialization ownership, default-to-main base selection, cleanup-before-verification ordering, or inherited-state bootstrap blocking

**Constraints for later phases:**
- do not broaden issue `#357` into a generic workflow redesign or new merge orchestration system
- do not reintroduce explicit `parent_branch` overrides into `start-issue`
- prefer the existing `GitConfig.extract_issue_number()` helper over adding new branch issue parsers
- treat prompt and agent-instruction edits as first-class deliverables, not mere documentation afterthoughts
- keep `end-issue` human-invoked and `@co`-owned; this issue does not authorize automated merge flow

---

## Open Questions

- How should design model `@imp` startup so fresh branches respect the lifecycle-boundary exception while already-initialized branches still remain `get_work_context()`-first?
- Which boundary should own the `submit_pr` fallback read of `parent_branch`: direct state read, an injected state-engine query, or another existing abstraction?
- What is the narrowest safe verification step for `end-issue` cleanup under the current tool set: exact merge-SHA reachability only, or a broader local-sync proof?
- Should the issue body for `#357` be narrowed to reflect that the explicit `parent_branch` override in `start-issue` is already gone, while the child-init ownership problem remains live?

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
| implementation duplicates branch issue-number parsing logic | Medium | cite and reuse `GitConfig.extract_issue_number()` |
| prompt fixes land without corresponding code-side enforcement changes, or vice versa | High | keep prompt, startup, tool, and enforcement surfaces in the same bug family during design/planning |
| validation ignores prompt-level behavior because prompts are not primarily pytest-covered | High | treat human-reviewed prompt contracts as part of the authoritative blast radius |

---

## Corrected Behavior For Design And Planning

Design and planning should work toward the following corrected behavior framing:

- child-branch bootstrap and child-branch hand-off follow one coherent ownership model
- `submit_pr` respects the actual branch parent before defaulting to repo-wide configuration
- post-merge branch cleanup does not run until the parent branch is locally updated and the merged content is verifiably reachable
- inherited parent state does not block initialization of a different child issue branch
- prior fixes from issues `#268`, `#345`, and `#354` are treated as binding constraints, not re-opened by accident

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

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-27 | Agent | Initial scaffolded draft |
| 1.1 | 2026-05-27 | Agent | Replaced scaffold with evidence-backed lifecycle bug research, narrowed stale sub-gap, and recorded no-bridge strategy |
