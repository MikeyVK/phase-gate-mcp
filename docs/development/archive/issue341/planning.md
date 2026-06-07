<!-- docs\development\issue341\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-24T06:04Z updated=2026-05-24 -->
# Planning: @co-owned epic workflow orchestration

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-24

---

## Purpose

Translate the approved research and design into implementation-sized cycles that preserve the contract-first strategy, keep runtime changes narrow, and make validation obligations explicit before implementation begins.

## Scope

**In Scope:**
Epic workflow ownership contract surfaces, `@co` allowlist and epic sub-role alignment, lifecycle prompt realignment including new `close-issue` and `implement-cycle` archive move, runtime transition advisory for issue `#339`, runtime invalid-state recovery warning for issue `#340`, and the affected unit or integration tests plus manual prompt validation.

**Out of Scope:**
Generic runtime ownership enforcement, non-epic workflow redesign beyond the inherited issue268 baseline, production implementation outside the orchestration surfaces in design, milestone management, and exact commit-by-commit sequencing.

## Prerequisites

Read these first:
1. Approved strategy in `docs/development/issue341/research.md` remains binding.
2. Design decisions in `docs/development/issue341/design.md` remain the planning boundary.
3. Lifecycle entry and exit for non-epic flows continue to inherit the issue268 baseline unless explicitly marked epic-only.

---

## Summary

This plan keeps issue `#341` in four sequential cycles.

Cycle 1 establishes the contract and authority baseline for epic ownership so later prompt and runtime work has one stable source of truth. Cycle 2 applies that ownership model to lifecycle prompt surfaces, including the new epic-owned `close-issue` flow and retirement of the stale `implement-cycle` prompt from the live inventory. Cycle 3 delivers issue `#339` as a narrow transition-note runtime slice. Cycle 4 delivers issue `#340` as a narrow `get_work_context` invalid-state recovery slice.

This ordering preserves the Approved Strategy, keeps runtime changes narrow, and prevents planning from hiding redesign decisions inside later implementation work.

---

## Cycle Strategy

| Cycle | Focus | Why this boundary exists | Main affected surfaces | Primary proof |
|---|---|---|---|---|
| 1 | Epic contract alignment | Prompt and runtime work must not proceed against conflicting ownership rules | `AGENTS.md`, `.github/agents/*.agent.md`, `.phase-gate/config/contracts.yaml`, contract-loading tests | Contract surfaces align on the approved `@co` epic model |
| 2 | Lifecycle prompt realignment | Entry and exit prompts depend on the ownership split and allowlist boundary from Cycle 1 | `.github/prompts/open-issue.prompt.md`, new `.github/prompts/close-issue.prompt.md`, `.github/prompts/archive/`, prompt inventory | Prompt flows match design and the stale live prompt is retired |
| 3 | Issue `#339` transition advisory | Runtime note behavior is isolated from lifecycle prompt work and can be validated independently | `mcp_server/tools/phase_tools.py`, `mcp_server/tools/cycle_tools.py`, note-rendering tests | All four transition tools append the standardized success-path note |
| 4 | Issue `#340` invalid-state recovery | `get_work_context` fallback behavior is a separate runtime slice with its own tests and recovery wording | `mcp_server/tools/discovery_tools.py`, `tests/mcp_server/unit/tools/test_discovery_tools.py` | Invalid workflow-phase state becomes explicit recovery guidance without becoming a hard error |

---

## Dependencies

- Cycle 2 depends on Cycle 1 because prompt ownership, epic lifecycle wording, and the close-issue cleanup model must follow the approved contract and allowlist boundary.
- Cycle 3 depends on Cycle 1 only for ownership vocabulary alignment; the runtime `#339` slice stays otherwise independent of prompt implementation.
- Cycle 4 depends on Cycle 1 only indirectly; the runtime `#340` slice must remain narrow and must not reopen workflow policy.

---

## Cross-Cycle Obligations

### Approved Strategy Constraints

- `@co` becomes the owner of epic workflow execution from research through ready.
- The `@co` allowlist remains narrow and explicit; planning must not smuggle in extra mutation tools because the epic exit wording is richer.
- `#339` and `#340` stay separate in-branch runtime slices of issue `#341`.
- Non-epic lifecycle behavior remains inherited from issue `#268` unless the design explicitly marks an epic-only override.
- `implement-cycle.prompt.md` is retired as a live prompt surface and not reused as a compatibility bridge.

### Architecture Obligations

- Keep workflow and phase behavior config-driven. Do not solve epic ownership or invalid-state handling with hardcoded workflow or phase if-chains.
- Preserve SSOT: epic phase sequencing and epic instructions remain authoritative in `.phase-gate/config/contracts.yaml`.
- Keep tool-layer dependency injection intact in runtime slices. Do not instantiate new managers inside `execute()` paths.
- Treat close-issue remote branch cleanup as a required outcome to verify, not as an assumed capability of a non-existent MCP tool.

### Typing Obligations

- No global checker relaxations.
- Any new typing work in Cycles 3 and 4 must follow `TYPE_CHECKING_PLAYBOOK.md`: fix at source, narrow with runtime checks, and avoid blind casts or broad ignores.
- Contract and prompt cycles should not introduce typing debt through helper shortcuts or ad-hoc dynamic structures.

### Quality-Gate Obligations

- Every cycle must run quality gates on all changed production and test files before completion.
- Runtime cycles must validate both changed tool files and their changed tests.
- Prompt and agent surfaces require explicit manual validation because no dedicated prompt-validation suite was confirmed during design.

---

## TDD Cycles

### Cycle 1: Epic contract alignment

**Goal:** Align epic ownership at the contract layer so agent docs, project authority text, and epic workflow metadata all agree on `@co`-owned epic execution without widening the approved allowlist.

**Affected Surfaces:**
- `AGENTS.md`
- `.github/agents/co.agent.md`
- `.github/agents/imp.agent.md`
- `.github/agents/qa.agent.md`
- `.phase-gate/config/contracts.yaml`
- `tests/mcp_server/unit/config/test_contracts_loader.py`
- Any adjacent contract or config validation tests that fail because epic metadata changes

**Deliverables:**
- `C1.contract.epic-role-authority`: project and agent docs describe epic work as `@co`-owned instead of `@imp`-owned.
- `C1.contract.epic-allowlist-boundary`: the explicit `@co` allowlist matches the approved strategy and does not broaden into general implementation rights.
- `C1.contract.epic-subroles`: epic workflow instructions use coordination-scoped sub-role names consistently.
- `C1.contract.epic-phase-order-ssot`: non-SSOT surfaces stop enumerating epic phase order and defer sequence authority to `.phase-gate/config/contracts.yaml`.
- `C1.contract.co-operating-modes`: `AGENTS.md` and `.github/agents/co.agent.md` both describe owned-branch epic execution and background coordination around child work.
- `C1.contract.co-startup-and-handback-boundaries`: startup protocol, lifecycle-boundary exception wording, and hand-back boundary text align between project and agent surfaces.
- `C1.validation.contract-loader`: contract-loading tests cover the updated epic workflow entries.

**Exit Criteria:**
- Epic contract surfaces expose coordination-scoped epic sub-roles consistently.
- `@co` allowlist and role boundaries match the approved strategy without adding unapproved implementation tools.
- Non-SSOT epic phase-order enumeration is removed from project and agent surfaces that should defer to `.phase-gate/config/contracts.yaml`.
- `AGENTS.md` and `.github/agents/co.agent.md` describe the same two operating modes, startup expectations, and hand-back boundaries.
- Contract-loading and adjacent config tests pass.
- No new hardcoded epic workflow logic is introduced outside config-driven contract surfaces.
**Validation Obligations:**
- Run the narrow contract/config tests touched by the epic workflow entry changes.
- Run quality gates on changed config, Python, and test files.
- Manually verify that project-level and agent-level authority text no longer contradict each other on ownership, epic phase-order SSOT, operating modes, startup protocol, or hand-back boundaries.

**Typing and Quality Notes:**
- Typing risk is low, but changed Python helpers or tests must still pass strict checks.
- This cycle must not defer visible authority contradictions into later prompt work.

**Dependencies:** None.

### Cycle 2: Lifecycle prompt realignment

**Goal:** Realign lifecycle entry and exit prompts to the approved ownership model, add the missing `close-issue` prompt surface, and retire `implement-cycle` from the live prompt inventory.

**Affected Surfaces:**
- `.github/prompts/open-issue.prompt.md`
- new `.github/prompts/close-issue.prompt.md`
- `.github/prompts/implement-cycle.prompt.md`
- `.github/prompts/archive/`
- Any prompt inventory or reference surfaces that still point at the live `implement-cycle` prompt
- Manual validation of prompt flows because no dedicated prompt suite was confirmed

**Deliverables:**
- `C2.prompt.open-issue-co-ownership`: `open-issue` is owned by `@co` and reflects the approved epic versus non-epic split.
- `C2.prompt.epic-open-issue-bootstrap`: the epic-owned `open-issue` path uses the exact bootstrap order `get_issue -> create_branch -> git_checkout -> initialize_project(issue_number, issue_title, workflow_name) -> get_work_context -> get_project_plan -> first commit -> git_push`.
- `C2.prompt.open-issue-stop-go`: the epic-owned path stops before the first commit or push if `get_work_context` cannot load startup context cleanly or if `get_project_plan` returns a missing or inconsistent workflow or phase contract.
- `C2.prompt.non-epic-hand-off-boundary`: the inherited non-epic path keeps `@co` at lifecycle entry through `get_project_plan` and hands the first `get_work_context` plus first write boundary to `@imp`.
- `C2.prompt.output-contract`: prompt output reports branch, workflow, first phase, whether the flow stopped at `@co` hand-off or completed full owned-branch bootstrap, push result when applicable, and blockers.
- `C2.prompt.close-issue-epic-exit`: `close-issue` models the epic-owned merge-verify-cleanup override and keeps `close_issue` as explicit recovery only on that path.
- `C2.prompt.implement-cycle-archived`: `implement-cycle` is moved into `.github/prompts/archive/` and is no longer a live prompt surface.
- `C2.validation.prompt-manual`: manual validation confirms prompt ownership, sequencing, stop-go behavior, output contract, and archive state are internally consistent.

**Exit Criteria:**
- `open-issue` is owned by `@co` and reflects the approved epic versus non-epic split.
- The epic-owned bootstrap order matches the approved sequence exactly.
- The epic-owned path stops before the first write when `get_work_context` or `get_project_plan` fails its approved verification role.
- The inherited non-epic hand-off boundary still matches issue268: `@co` owns lifecycle entry through `get_project_plan`, and `@imp` is the first agent to call `get_work_context` before further writes.
- Prompt output reports branch, workflow, first phase, hand-off versus full-bootstrap status, push result when applicable, and blockers.
- `close-issue` models the epic-owned merge-verify-cleanup override without making `close_issue` normative on that path.
- `implement-cycle` is moved out of the live prompt inventory.
**Validation Obligations:**
- Manually validate the prompt frontmatter, exact execution ordering, stop-go rules, and output contract against the design.
- Manually confirm the archive move leaves no active prompt surface at `.github/prompts/implement-cycle.prompt.md`.
- Cross-check the inherited non-epic wording against issue268 before treating prompt changes as complete.
- Run quality gates on any changed text, config, or test surfaces that are in gate scope.

**Typing and Quality Notes:**
- This cycle is prompt-heavy rather than code-heavy, but it still must not introduce stale tool signatures or stale ownership wording.
- Remote branch cleanup remains an outcome to verify, not a silently assumed tool call.

**Dependencies:** Cycle 1.

### Cycle 3: Transition advisory note

**Goal:** Deliver issue `#339` as a narrow runtime slice that appends the standardized post-transition `get_work_context` note on successful phase and cycle transitions.

**Affected Surfaces:**
- `mcp_server/tools/phase_tools.py`
- `mcp_server/tools/cycle_tools.py`
- `mcp_server/core/operation_notes.py` only if a minimal supporting import or helper change is truly required
- `tests/mcp_server/unit/tools/test_transition_phase_tool.py`
- `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`
- `tests/mcp_server/unit/tools/test_cycle_tools.py`
- `tests/mcp_server/unit/test_server.py` or adjacent note-rendering or integration coverage as needed

**Deliverables:**
- `C3.runtime.transition-info-note`: all four transition tools emit the standardized success-path note after transition success.
- `C3.tests.transition-note-unit`: unit tests cover the note emission for phase and cycle transitions.
- `C3.validation.note-rendering`: server-visible rendering remains a secondary response element and does not mutate the primary success contract.

**Exit Criteria:**
- `transition_phase`, `force_phase_transition`, `transition_cycle`, and `force_cycle_transition` emit the same standardized advisory note after success.
- Primary success text remains intact and note rendering stays a secondary response element.
- All changed unit or integration tests pass.
- Quality gates and typing checks pass on changed production and test files.

**Validation Obligations:**
- Write the failing tests first for the new note behavior where feasible.
- Prove the note is appended after the success message rather than merged into it.
- Keep the scope limited to the four transition tools only.

**Typing and Quality Notes:**
- Do not broaden `SuggestionNote` or invent a generic note framework in this cycle.
- Prefer the smallest possible change in tool response assembly and explicit test coverage for ordering.

**Dependencies:** Cycle 1.

### Cycle 4: Invalid-state recovery warning

**Goal:** Deliver issue `#340` as a narrow `get_work_context` behavior slice that distinguishes invalid workflow-phase state from the generic unknown-contract fallback while preserving non-error behavior.

**Affected Surfaces:**
- `mcp_server/tools/discovery_tools.py`
- `tests/mcp_server/unit/tools/test_discovery_tools.py`
- Any adjacent formatting or server tests needed to prove warning placement before the phase-instructions block

**Deliverables:**
- `C4.runtime.invalid-phase-warning`: `get_work_context` renders the explicit invalid-state warning for known workflow plus invalid phase.
- `C4.tests.discovery-warning`: discovery-tool tests distinguish invalid-state warning from generic unknown fallback.
- `C4.validation.warning-rendering`: rendered output preserves the non-error response and places the warning before the phase-instructions block.

**Exit Criteria:**
- `get_work_context` renders the explicit invalid-state warning with workflow, invalid phase, valid phases, and recovery action.
- Unknown or missing state cases still degrade gracefully without becoming hard errors.
- Warning placement is validated before the phase-instructions block.
- Quality gates and typing checks pass on changed production and test files.

**Validation Obligations:**
- Drive the change with discovery-tool tests that separate invalid-state from generic fallback.
- Keep `force_phase_transition` permissiveness unchanged.
- Avoid widening this cycle into a generic enforcement redesign or a broader workflow-policy rewrite.

**Typing and Quality Notes:**
- Keep any new conditional logic local and explicit; do not hide state interpretation in vague fallbacks.
- Prefer existing typed state and contract objects over dynamic dict reshaping.

**Dependencies:** Cycle 1.

---

## Risks & Mitigation

| Risk | Why it matters | Mitigation |
|---|---|---|
| Allowlist drift | Could silently turn `@co` into a second implementation agent | Keep Cycle 1 explicit about approved tools only and treat richer epic close-issue behavior as an outcome that implementation must realize without unapproved tool expansion |
| Prompt drift from inherited non-epic baseline | Could quietly rewrite issue268 behavior while claiming to preserve it | Make Cycle 2 validate every non-epic prompt step against the issue268 lifecycle baseline |
| Runtime scope creep | `#339` and `#340` could widen into a generic note-policy or invalid-state framework | Keep Cycles 3 and 4 isolated and reject abstractions not required by the design |
| Remote cleanup assumption | Planning could assume a remote-delete tool that does not exist in the current MCP surface | Treat remote branch absence as an outcome to verify and surface explicit follow-up when automatic cleanup does not happen |

---

## Open Questions

No design-blocking questions remain.

Implementation may still choose:
- the safest rollout order inside Cycle 1 between project authority text, agent wrappers, and epic contract entries
- whether Cycle 2 needs any additional reference-doc touch-ups once the prompt files are changed
- the narrowest automated coverage that proves warning placement in Cycle 4 if existing tests do not already reach that formatting layer

---

## Related Documentation
- **[docs/development/issue341/research.md][related-1]**
- **[docs/development/issue341/design.md][related-2]**
- **[docs/development/issue268/research.md][related-3]**
- **[AGENTS.md][related-4]**
- **[.github/agents/co.agent.md][related-5]**
- **[.phase-gate/config/contracts.yaml][related-6]**

<!-- Link definitions -->

[related-1]: docs/development/issue341/research.md
[related-2]: docs/development/issue341/design.md
[related-3]: docs/development/issue268/research.md
[related-4]: AGENTS.md
[related-5]: .github/agents/co.agent.md
[related-6]: .phase-gate/config/contracts.yaml

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-24 | Agent | Initial planning draft with four sequential cycles covering epic contract alignment, lifecycle prompt realignment, and the narrow runtime slices for issues #339 and #340 |
