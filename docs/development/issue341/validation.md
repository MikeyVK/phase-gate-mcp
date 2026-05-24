<!-- docs/development/issue341/validation.md -->
<!-- template=generic_doc version=43c84181 created=2026-05-24 updated=2026-05-24 -->
# Validation Report — Issue #341

**Status:** PASS  
**Version:** 1.2  
**Last Updated:** 2026-05-24

---

## Purpose

Capture the authoritative validation evidence for issue #341 after the implementation cycles completed, including the original validation pass, the later wording-only rerun, and the QA-driven commit-protocol correction that revalidated the committed branch state.

## Scope

**In Scope:**
Epic contract alignment, lifecycle prompt realignment, transition advisory note behavior for issue `#339`, invalid-state recovery guidance for issue `#340`, affected unit and server tests, branch-wide validation of the resulting branch state, and the later QA-driven revalidation after the previously uncommitted implementation files were committed.

**Out of Scope:**
Documentation-phase close-out edits beyond this validation report, PR submission, merge or close execution, and any redesign or implementation patching outside the validated branch state.

## Environment

- Branch: `feature/341-co-as-end-to-end-epic-workflow-owner`
- Workflow phase at evidence capture: `validation`
- OS: Windows
- Python environment: `.venv` at `c:/temp/st3/.venv`
- Evidence run date: 2026-05-24
- Tester: GitHub Copilot (`@imp`)

---

## Validation Inputs

| Input | Status | Evidence |
|---|---|---|
| Research, design, and planning artifacts available | PASS | `docs/development/issue341/research.md`, `design.md`, and `planning.md` were read before validation |
| Approved Strategy available and usable | PASS | `research.md` contains explicit Approved Strategy entries for epic ownership, allowlist boundary, prompt ownership, `#339`, and `#340` |
| Original branch-wide regression suite available | PASS | `run_tests(scope="full")` completed successfully on 2026-05-24 during the first validation pass |
| QA-driven revalidation on committed branch state available | PASS | After QA reported that C1 and the wording delta were not committed on HEAD, the missing implementation files were committed and the branch-wide suite and branch gates were rerun on the committed state |
| Manual prompt and archive evidence available | PASS | `.github/prompts/open-issue.prompt.md` and `.github/prompts/close-issue.prompt.md` exist as active prompts, while `.github/prompts/archive/implement-cycle.prompt.md` exists only in the archive |
| Validation artifact required | PASS | No prior `docs/development/issue341/validation.md` existed on this branch |

---

## Summary

Issue #341 now satisfies the validation-phase contract on the committed branch state. The original branch-wide validation had already shown the implementation was substantively correct, but QA correctly rejected the handover because key Cycle 1 files and the later wording-only delta were still only present in the working tree and not on HEAD.

That blocker is now resolved. The previously uncommitted implementation files were committed in three catch-up commits:

- `f977c8c5448d61c178e9956321add875baf4e95c` — C1 epic contract alignment
- `cfd4d90a64ec42ea64d4f3e6a9682f6817cb21a9` — C3 strengthened transition advisory note
- `8d049326f3489e4239784be4d399532e66e5612c` — C4 strengthened invalid-state warning wording

After those commits, the full regression suite was rerun on the committed branch state and remained green at `2809 passed, 11 skipped, 6 xfailed, 26 warnings`. The branch quality gates were also rerun and remained green, now across `11` branch files instead of the earlier `10`, which closes the exact QA concern about `tests/mcp_server/unit/config/test_contracts_loader.py` not having been included in the committed branch-gate scope.

The branch remains aligned with the Approved Strategy boundaries. Epic ownership is still expressed through project and agent contract surfaces instead of a generic runtime ownership framework, `@co` remains on a narrow explicit allowlist, prompt ownership remains with `@co`, the stale live `implement-cycle` prompt remains archived, the issue `#339` note remains limited to the four transition tools, and issue `#340` remains a non-error recovery warning instead of a new hard enforcement path.

---

## QA Rework Resolution

| QA blocker | Resolution |
|---|---|
| Cycle 1 deliverables were present only in the working tree | Resolved by commit `f977c8c5448d61c178e9956321add875baf4e95c`, which captured `AGENTS.md`, `.github/agents/co.agent.md`, `.phase-gate/config/contracts.yaml`, and `tests/mcp_server/unit/config/test_contracts_loader.py` on HEAD |
| Post-validation wording delta was present only in the working tree | Resolved by commits `cfd4d90a64ec42ea64d4f3e6a9682f6817cb21a9` and `8d049326f3489e4239784be4d399532e66e5612c`, which captured the strengthened issue `#339` advisory wording and the adjusted issue `#340` invalid-state wording on HEAD |
| Branch quality gate did not include the new contract-loader test in committed scope | Resolved by rerunning `run_quality_gates(scope="branch")` after the C1 commit; the rerun passed across `11` branch files |
| Validation handover no longer reflected the committed branch truth | Resolved by this report update, which now treats the committed branch rerun as the authoritative validation evidence |

---

## Branch-Wide Evidence

| Planned slice | Evidence on branch |
|---|---|
| Cycle 1 — epic contract alignment | `AGENTS.md` treats epic phase order as SSOT-owned by `.phase-gate/config/contracts.yaml`, exposes the `@co` epic lifecycle sub-roles, and documents owned-branch epic execution plus background coordination. `.github/agents/co.agent.md` mirrors the same operating modes and narrow epic allowlist. `.phase-gate/config/contracts.yaml` uses `epic-researcher`, `epic-planner`, `epic-designer`, `epic-coordinator`, `epic-documenter`, and `epic-releaser`. `tests/mcp_server/unit/config/test_contracts_loader.py` is now committed on HEAD and was included in the rerun branch-gate scope. |
| Cycle 2 — lifecycle prompt realignment | `.github/prompts/open-issue.prompt.md` is owned by `agent: co`, preserves the exact epic bootstrap order, and keeps the non-epic hand-off boundary at `get_project_plan`. `.github/prompts/close-issue.prompt.md` exists and models the epic-owned merge-verify-cleanup override while keeping `close_issue` recovery-only on that path. `.github/prompts/archive/implement-cycle.prompt.md` confirms the stale cycle prompt is archived rather than left live. |
| Cycle 3 — issue `#339` transition advisory note | `mcp_server/tools/phase_tools.py` and `mcp_server/tools/cycle_tools.py` emit the same `TRANSITION_ADVISORY_NOTE` via `InfoNote` on successful phase and cycle transitions. `mcp_server/server.py` and `mcp_server/core/operation_notes.py` preserve the advisory as a secondary rendered response element while allowing targeted suppression when post-enforcement converts success into error. The strengthened advisory copy now reads `🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call to load the current phase context for this branch.` and is committed on HEAD. |
| Cycle 4 — issue `#340` invalid-state recovery warning | `mcp_server/tools/discovery_tools.py` distinguishes known-workflow plus invalid-phase state from the generic unknown fallback, renders an explicit recovery warning before `### 🎯 Phase Instructions`, and preserves non-error behavior. The adjusted invalid-state wording is now committed on HEAD, and the dedicated discovery-tool regression coverage remains green. |

---

## Test Results

| Scope | Tool invocation | Result |
|---|---|---|
| Original branch-wide validation | `run_tests(scope="full")` | PASS - 2809 passed, 11 skipped, 6 xfailed, 26 warnings in 61.87s |
| Wording-only changed-scope rerun | `run_tests(path="tests/mcp_server/unit/tools/test_transition_phase_tool.py tests/mcp_server/unit/tools/test_force_phase_transition_tool.py tests/mcp_server/unit/tools/test_cycle_tools.py tests/mcp_server/unit/test_server.py tests/mcp_server/unit/tools/test_discovery_tools.py")` | PASS - 91 passed, 1 xfailed, 1 warning in 15.89s |
| QA-driven committed-state revalidation | `run_tests(path="tests/mcp_server")` | PASS - 2809 passed, 11 skipped, 6 xfailed, 26 warnings in 63.12s |

## Quality Gate Evidence

| Scope | Tool invocation | Result |
|---|---|---|
| Original branch-wide validation | `run_quality_gates(scope="branch")` | PASS - 6/6 active gates passed across 10 branch files in gate scope; generic Gate 4 types check skipped by configuration; Gate 4b Pyright passed; Gate 4c `mcp_server` types passed |
| Wording-only changed-scope rerun | `run_quality_gates(scope="files")` on `mcp_server/tools/phase_tools.py`, `mcp_server/tools/discovery_tools.py`, `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`, `tests/mcp_server/unit/tools/test_cycle_tools.py`, and `tests/mcp_server/unit/tools/test_discovery_tools.py` | PASS - 6/6 active gates passed across 6 files; generic Gate 4 types check skipped; Gate 4b Pyright passed; Gate 4c `mcp_server` types passed |
| QA-driven committed-state revalidation | `run_quality_gates(scope="branch")` | PASS - 6/6 active gates passed across 11 branch files in gate scope; generic Gate 4 types check skipped by configuration; Gate 4b Pyright passed; Gate 4c `mcp_server` types passed |

---

## Planning, Design, And Strategy Alignment

### Planning alignment

The branch contents match the four-cycle decomposition in `planning.md`:

- Cycle 1 evidence is visible in the updated project and agent contract surfaces plus the epic contract entry and loader-test coverage.
- Cycle 2 evidence is visible in prompt ownership, the explicit epic versus non-epic split, and the archive-only presence of `implement-cycle.prompt.md`.
- Cycle 3 evidence is visible in the four transition tools, note rendering, and the transition-related tool and server tests.
- Cycle 4 evidence is visible in `GetWorkContextTool`, its warning placement, and the dedicated discovery-tool regression coverage.
- The QA-driven rework changed commit protocol and wording evidence placement, not planning scope.

### Design and Approved Strategy alignment

| Strategy or design constraint | Validation result | Evidence |
|---|---|---|
| Epic ownership remains contract-first rather than a generic runtime framework | PASS | The branch changes center on `AGENTS.md`, `.github/agents/co.agent.md`, `.phase-gate/config/contracts.yaml`, prompt surfaces, and the two narrow runtime slices; no generic ownership engine or policy layer was introduced |
| `@co` allowlist remains narrow and explicit | PASS | `.github/agents/co.agent.md` lists the approved epic-execution tools and does not add `run_tests`, `transition_cycle`, or broader production-code authority |
| Epic phase vocabulary becomes coordination-scoped | PASS | `AGENTS.md`, `.github/agents/co.agent.md`, and `.phase-gate/config/contracts.yaml` all use the `epic-*` lifecycle sub-roles |
| Lifecycle prompts move to `@co` and stale `implement-cycle` is retired | PASS | `open-issue.prompt.md` and `close-issue.prompt.md` are `agent: co`; `implement-cycle.prompt.md` exists only in `.github/prompts/archive/` |
| Issue `#339` stays limited to the four transition tools and renders the note after primary success text | PASS | The strengthened `TRANSITION_ADVISORY_NOTE` still lives only on the four transition tools; `server.py` and `operation_notes.py` preserve secondary rendering behavior |
| Issue `#340` stays a non-error recovery warning and does not widen into enforcement redesign | PASS | `discovery_tools.py` keeps the invalid-state path non-error and local to `get_work_context`, while the changed wording does not alter the underlying recovery contract |

### Architecture alignment

The branch remains materially aligned with `ARCHITECTURE_PRINCIPLES.md`:

- Epic ownership and phase-order SSOT remain config-driven instead of being hardcoded into new Python if-chains.
- The runtime slices preserve dependency-injected tool structure rather than instantiating new managers inside `execute()` paths.
- The issue `#339` change reuses the existing note bus and server rendering path instead of inventing a second note framework.
- The issue `#340` change keeps invalid-state interpretation local to `GetWorkContextTool` and does not add a new hard-fail enforcement layer.

---

## Live Demonstration Proposal And Fallback

### Safe live demonstration status

No true safe live demonstration exists as a default procedure on the active validation branch for the two runtime behavior changes that matter most:

- The issue `#339` note is only observable by performing a successful phase or cycle transition, which mutates workflow state.
- The issue `#340` warning is only observable by placing the branch in a known workflow plus invalid-phase state, which is intentionally an invalid branch condition.

Running either proof directly on the active validation branch would mutate the workflow state being validated and would therefore be unsafe as a default validation-phase demonstration.

### Closest observable fallback evidence

The closest safe fallback evidence is:

1. Review the prompt and contract surfaces directly:
   `AGENTS.md`, `.github/agents/co.agent.md`, `.github/prompts/open-issue.prompt.md`, `.github/prompts/close-issue.prompt.md`, and `.phase-gate/config/contracts.yaml`.
2. Review the runtime proof surfaces directly:
   `mcp_server/tools/phase_tools.py`, `mcp_server/tools/cycle_tools.py`, `mcp_server/server.py`, `mcp_server/core/operation_notes.py`, and `mcp_server/tools/discovery_tools.py`.
3. Review the regression proof surfaces and the green validation checks:
   `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`, `tests/mcp_server/unit/tools/test_cycle_tools.py`, `tests/mcp_server/unit/test_server.py`, and `tests/mcp_server/unit/tools/test_discovery_tools.py` together with the green branch-wide and committed-state reruns.

During the wording-only rerun, the updated issue `#339` advisory note and the updated issue `#340` invalid-state warning were both re-observed live after the necessary state changes and server reload. That live proof is real evidence, but it still depends on workflow-state mutation and therefore remains fallback evidence rather than a default demo path.

---

## Residual Risks And Caveats

- The original and committed-state full-suite reruns are green, but they still report 11 skipped tests, 6 xfailed tests, and 26 warnings. These remain visible but non-blocking.
- `run_quality_gates(scope="branch")` skips the generic Gate 4 types check, although both Pyright and the `mcp_server` types gate passed.
- Prompt and documentation surfaces still rely partly on manual validation because no dedicated prompt-validation suite was confirmed during research, design, or validation.
- The worktree is still not fully clean during this validation session, but the remaining uncommitted items are now limited to branch-local `.phase-gate` artifacts and this validation report update. The earlier QA blockers about uncommitted C1 and wording-delta implementation files are resolved.
- `.phase-gate/state.json` and `.phase-gate/deliverables.json` remain branch-local artifacts and must never reach `main`.

---

## Related Documentation
- **[docs/development/issue341/research.md][related-1]**
- **[docs/development/issue341/design.md][related-2]**
- **[docs/development/issue341/planning.md][related-3]**
- **[AGENTS.md][related-4]**
- **[.github/agents/co.agent.md][related-5]**
- **[.phase-gate/config/contracts.yaml][related-6]**
- **[.github/prompts/open-issue.prompt.md][related-7]**
- **[.github/prompts/close-issue.prompt.md][related-8]**
- **[mcp_server/tools/discovery_tools.py][related-9]**
- **[mcp_server/tools/phase_tools.py][related-10]**
- **[mcp_server/tools/cycle_tools.py][related-11]**

<!-- Link definitions -->

[related-1]: docs/development/issue341/research.md
[related-2]: docs/development/issue341/design.md
[related-3]: docs/development/issue341/planning.md
[related-4]: AGENTS.md
[related-5]: .github/agents/co.agent.md
[related-6]: .phase-gate/config/contracts.yaml
[related-7]: .github/prompts/open-issue.prompt.md
[related-8]: .github/prompts/close-issue.prompt.md
[related-9]: mcp_server/tools/discovery_tools.py
[related-10]: mcp_server/tools/phase_tools.py
[related-11]: mcp_server/tools/cycle_tools.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.2 | 2026-05-24 | Agent | Resolved QA NOGO by recording the committed C1/C3/C4 catch-up commits and the green revalidation on the committed branch state |
| 1.1 | 2026-05-24 | Agent | Added a follow-up light validation rerun for the post-validation wording changes on the issue `#339` advisory note and the issue `#340` invalid-state warning |
| 1.0 | 2026-05-24 | Agent | Initial validation report with branch-wide test, gate, prompt, contract, and runtime evidence for issue #341 |
