<!-- docs/development/issue341/validation.md -->
<!-- template=generic_doc version=43c84181 created=2026-05-24 updated=2026-05-24 -->
# Validation Report — Issue #341

**Status:** PASS  
**Version:** 1.0  
**Last Updated:** 2026-05-24

---

## Purpose

Capture branch-wide validation evidence for issue #341 after implementation cycles 1-4 completed and the branch transitioned from implementation to validation.

## Scope

**In Scope:**
Epic contract alignment, lifecycle prompt realignment, transition advisory note behavior for issue #339, invalid-state recovery guidance for issue #340, affected unit and server tests, and branch-wide validation of the resulting branch state.

**Out of Scope:**
Documentation-phase close-out edits, PR submission, merge or close execution, and any redesign or implementation patching during validation.

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
| Branch-wide regression suite available | PASS | `run_tests(scope="full")` completed successfully on 2026-05-24 |
| Branch-scoped quality validation available | PASS | `run_quality_gates(scope="branch")` completed successfully on 2026-05-24 |
| Manual prompt and archive evidence available | PASS | `.github/prompts/open-issue.prompt.md` and `.github/prompts/close-issue.prompt.md` exist as active prompts, while `.github/prompts/archive/implement-cycle.prompt.md` exists only in the archive |
| Validation artifact required | PASS | No prior `docs/development/issue341/validation.md` existed on this branch |

---

## Summary

Issue #341 satisfies the current validation-phase contract. The full regression suite is green, branch quality gates are green, and the branch contents align with the four-cycle plan: contract-first epic ownership alignment, lifecycle prompt realignment, a narrow transition-advisory runtime slice, and a narrow invalid-state recovery runtime slice.

The validated branch also remains aligned with the Approved Strategy boundaries. Epic ownership is expressed through project and agent contract surfaces instead of a generic runtime ownership framework, `@co` remains on a narrow explicit allowlist, prompt ownership moved to `@co`, the stale live `implement-cycle` prompt was retired into the archive, the issue `#339` note remains limited to the four transition tools, and issue `#340` remains a non-error recovery warning instead of a new hard enforcement path.

This PASS verdict includes explicit caveats rather than hiding them: docs and prompt surfaces still rely partly on manual validation because no dedicated prompt suite exists, the worktree still contains branch-local `.phase-gate` artifacts and locally modified Cycle 1 surfaces during this validation pass, and the full suite still reports skipped, xfailed, and warning counts that remain visible but non-blocking.

---

## Branch-Wide Evidence

| Planned slice | Evidence on branch |
|---|---|
| Cycle 1 — epic contract alignment | `AGENTS.md` now treats epic phase order as SSOT-owned by `.phase-gate/config/contracts.yaml`, exposes the `@co` epic lifecycle sub-roles, and documents owned-branch epic execution plus background coordination. `.github/agents/co.agent.md` mirrors the same operating modes and narrow epic allowlist. `.phase-gate/config/contracts.yaml` uses `epic-researcher`, `epic-planner`, `epic-designer`, `epic-coordinator`, `epic-documenter`, and `epic-releaser`. `tests/mcp_server/unit/config/test_contracts_loader.py` remains in the branch-wide green suite as the contract-loading proof surface. |
| Cycle 2 — lifecycle prompt realignment | `.github/prompts/open-issue.prompt.md` is owned by `agent: co`, preserves the exact epic bootstrap order, and keeps the non-epic hand-off boundary at `get_project_plan`. `.github/prompts/close-issue.prompt.md` exists and models the epic-owned merge-verify-cleanup override while keeping `close_issue` recovery-only on that path. Directory evidence shows `.github/prompts` exposes only `open-issue` and `close-issue` as active prompt surfaces, while `.github/prompts/archive/implement-cycle.prompt.md` confirms the stale cycle prompt is archived rather than left live. |
| Cycle 3 — issue #339 transition advisory note | `mcp_server/tools/phase_tools.py` and `mcp_server/tools/cycle_tools.py` emit the same `TRANSITION_ADVISORY_NOTE` via `InfoNote` on successful phase and cycle transitions. `mcp_server/server.py` and `mcp_server/core/operation_notes.py` preserve the advisory as a secondary rendered response element while allowing targeted suppression when post-enforcement converts success into error. The affected regression surfaces remain green in the full suite: `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `test_force_phase_transition_tool.py`, `test_cycle_tools.py`, and `tests/mcp_server/unit/test_server.py`. |
| Cycle 4 — issue #340 invalid-state recovery warning | `mcp_server/tools/discovery_tools.py` distinguishes known-workflow plus invalid-phase state from the generic unknown fallback, renders an explicit recovery warning before `### 🎯 Phase Instructions`, and preserves non-error behavior. `tests/mcp_server/unit/tools/test_discovery_tools.py` remains the primary proof surface and is green in the full suite. The active `get_work_context()` response on this branch also confirms validation-phase instructions still render normally in the non-invalid path after the issue #340 changes. |

---

## Test Results

| Scope | Tool invocation | Result |
|---|---|---|
| Full regression suite | `run_tests(scope="full")` | PASS - 2809 passed, 11 skipped, 6 xfailed, 26 warnings in 61.87s |

## Quality Gate Evidence

| Scope | Tool invocation | Result |
|---|---|---|
| Branch sweep | `run_quality_gates(scope="branch")` | PASS - 6/6 active gates passed across 10 branch files in gate scope; generic Gate 4 types check skipped by configuration; Gate 4b Pyright passed; Gate 4c `mcp_server` types passed |

---

## Planning, Design, And Strategy Alignment

### Planning alignment

The branch contents match the four-cycle decomposition in `planning.md`:

- Cycle 1 evidence is visible in the updated project and agent contract surfaces plus the epic contract entry and loader-test coverage.
- Cycle 2 evidence is visible in prompt ownership, the explicit epic versus non-epic split, and the archive-only presence of `implement-cycle.prompt.md`.
- Cycle 3 evidence is visible in the four transition tools, note rendering, and the transition-related tool and server tests.
- Cycle 4 evidence is visible in `GetWorkContextTool`, its warning placement, and the dedicated discovery-tool regression coverage.

No planning contradiction was found during this validation pass.

### Design and Approved Strategy alignment

| Strategy or design constraint | Validation result | Evidence |
|---|---|---|
| Epic ownership remains contract-first rather than a generic runtime framework | PASS | The branch changes center on `AGENTS.md`, `.github/agents/co.agent.md`, `.phase-gate/config/contracts.yaml`, prompt surfaces, and the two narrow runtime slices; no generic ownership engine or policy layer was introduced |
| `@co` allowlist remains narrow and explicit | PASS | `.github/agents/co.agent.md` lists the approved epic-execution tools and does not add `run_tests`, `transition_cycle`, or broader production-code authority |
| Epic phase vocabulary becomes coordination-scoped | PASS | `AGENTS.md`, `.github/agents/co.agent.md`, and `.phase-gate/config/contracts.yaml` all use the `epic-*` lifecycle sub-roles |
| Lifecycle prompts move to `@co` and stale `implement-cycle` is retired | PASS | `open-issue.prompt.md` and `close-issue.prompt.md` are `agent: co`; `implement-cycle.prompt.md` exists only in `.github/prompts/archive/` |
| Issue #339 stays limited to the four transition tools and renders the note after primary success text | PASS | `TRANSITION_ADVISORY_NOTE` lives on the four transition tools; `server.py` and `operation_notes.py` preserve secondary rendering behavior |
| Issue #340 stays a non-error recovery warning and does not widen into enforcement redesign | PASS | `discovery_tools.py` adds warning text and invalid-phase differentiation while keeping graceful fallback behavior for other cases |

### Architecture alignment

The branch remains materially aligned with `ARCHITECTURE_PRINCIPLES.md`:

- Epic ownership and phase-order SSOT remain config-driven instead of being hardcoded into new Python if-chains.
- The runtime slices preserve dependency-injected tool structure rather than instantiating new managers inside `execute()` paths.
- The issue #339 change reuses the existing note bus and server rendering path instead of inventing a second note framework.
- The issue #340 change keeps invalid-state interpretation local to `GetWorkContextTool` and does not add a new hard-fail enforcement layer.

---

## Live Demonstration Proposal And Fallback

### Safe live demonstration status

No true safe live demonstration exists on the current branch state for the two runtime behavior changes that matter most:

- The issue #339 note is only observable by performing a successful phase or cycle transition, which mutates workflow state.
- The issue #340 warning is only observable by placing the branch in a known workflow plus invalid-phase state, which is intentionally an invalid branch condition.

Running either proof directly on the active validation branch would mutate the workflow state being validated and would therefore be unsafe as a default validation-phase demonstration.

### Closest observable fallback evidence

The closest safe fallback evidence is:

1. Review the prompt and contract surfaces directly:
   `AGENTS.md`, `.github/agents/co.agent.md`, `.github/prompts/open-issue.prompt.md`, `.github/prompts/close-issue.prompt.md`, and `.phase-gate/config/contracts.yaml`.
2. Review the runtime proof surfaces directly:
   `mcp_server/tools/phase_tools.py`, `mcp_server/tools/cycle_tools.py`, `mcp_server/server.py`, `mcp_server/core/operation_notes.py`, and `mcp_server/tools/discovery_tools.py`.
3. Review the regression proof surfaces and the green branch-wide checks:
   `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`, `tests/mcp_server/unit/tools/test_cycle_tools.py`, `tests/mcp_server/unit/test_server.py`, and `tests/mcp_server/unit/tools/test_discovery_tools.py` together with the green `run_tests(scope="full")` and `run_quality_gates(scope="branch")` results.

If a true live demo is later desired, the safest route is a disposable copy branch created solely for demonstration, not the active validation branch.

---

## Residual Risks And Caveats

- The full suite is green, but it still reports 11 skipped tests, 6 xfailed tests, and 26 warnings. These remain visible but non-blocking in this validation pass.
- `run_quality_gates(scope="branch")` skips the generic Gate 4 types check, although both Pyright and the `mcp_server` types gate passed.
- Prompt and documentation surfaces still rely partly on manual validation because no dedicated prompt-validation suite was confirmed during research, design, or validation.
- The worktree is not clean during this validation pass. `AGENTS.md`, `.github/agents/co.agent.md`, `.phase-gate/config/contracts.yaml`, and `tests/mcp_server/unit/config/test_contracts_loader.py` remain locally modified Cycle 1 surfaces, while `.phase-gate/state.json` and `.phase-gate/deliverables.json` remain intentional branch-local artifacts that must never reach `main`.
- Branch diff evidence spans more files than the branch quality-gate scope, so docs and prompt correctness still depends on the explicit manual validation described above.

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
| 1.0 | 2026-05-24 | Agent | Initial validation report with branch-wide test, gate, prompt, contract, and runtime evidence for issue #341 |
