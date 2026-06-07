<!-- docs\development\issue341\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-23T09:33Z updated=2026-05-23 -->
# Research: @co as end-to-end epic workflow owner

**Status:** DRAFT  
**Version:** 1.3  
**Last Updated:** 2026-05-23

---

## Purpose

Determine whether epic workflow ownership should move fully to `@co`, identify the smallest coherent blast radius for that change, and capture the approved strategy for the same-branch orchestration follow-ups in `#339` and `#340` before any design or implementation work begins.

## Scope

**In Scope:**
Epic workflow ownership, role authority, allowed tool sets, epic phase instructions, hand-over paths, prompt ownership for lifecycle entry and exit, documentation authority, explicit in-branch handling of child issues `#339` and `#340`, and any minimal runtime implications needed to make the model coherent.

**Out of Scope:**
Implementing the redesign, reopening issue #268 C1-C8 implementation code, introducing a generic phase-ownership system, redesigning non-epic workflows, or deciding detailed file-by-file implementation patches.

## Research Method

- Repo-only research. No external research was requested for this issue.
- Primary sources read: `AGENTS.md`, `.github/agents/co.agent.md`, `.github/agents/imp.agent.md`, `.github/agents/qa.agent.md`, `.phase-gate/config/contracts.yaml`, `.github/prompts/open-issue.prompt.md`, `.github/prompts/implement-cycle.prompt.md`, issue `#341`, issue `#339`, issue `#340`, `docs/development/issue268/research.md`, and direct code/test anchors in `mcp_server/tools/phase_tools.py`, `mcp_server/tools/cycle_tools.py`, `mcp_server/tools/discovery_tools.py`, `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`, `tests/mcp_server/unit/tools/test_cycle_tools.py`, and `tests/mcp_server/unit/tools/test_discovery_tools.py`.
- Current branch bootstrap for issue #341 provided one additional empirical signal: the current `open-issue.prompt.md` does not match the live tool contract because `initialize_project` now requires `issue_title`, and branch-mutating follow-up steps were blocked until `get_work_context` was called.
- No dedicated `docs/development/issue339/` or `docs/development/issue340/` research artifacts currently exist, so this document is the authoritative research surface for their in-branch handling within issue `#341`.

---

## Problem Statement

The repository already models `epic` as a distinct workflow, but the operational ownership model is still centered on `@imp`. That creates a structural mismatch in epic-specific phases, especially `coordination`, where the workflow semantics point toward `@co` while the active role, prompt, and hand-over surfaces still assume implementation-led execution.

The result is ambiguity in five places:
- who owns an epic branch from research through ready
- who may mutate epic workflow state and artifacts
- how epic work hands over to and from `@qa`
- which prompts belong to lifecycle coordination versus technical execution
- whether epic work is governed as coordination work or treated as a large implementation branch

## Current Authoritative Surfaces

| Surface | Current statement | Why it matters |
|---------|-------------------|----------------|
| `AGENTS.md` | Defines `epic` as `research, design, planning, coordination, documentation, ready` and defines `@co` as coordination authority while `@imp` has all PhaseGate MCP tools | Workflow semantics and role permissions currently point in different directions |
| `.github/agents/co.agent.md` | `@co` is coordination authority, does not edit production code or tests, and produces hand-overs for `@imp` | Current role contract still assumes `@co -> @imp` delegation instead of epic ownership |
| `.github/agents/imp.agent.md` | `@imp` remains the implementation executor and takes coordination directives from `@co` | Current execution path assumes technical execution stays with `@imp` |
| `.github/agents/qa.agent.md` | `@qa` remains an external reviewer and hands findings back into the two-chat model | Preserving QA as an independent outside role is part of the ownership decision |
| `.phase-gate/config/contracts.yaml` | Epic phases exist, but the epic workflow still uses implementation-style sub-roles and the `coordination` phase literally says `Coordinate with @co as needed.` | The epic contract itself currently treats `@co` as adjacent rather than as owner |
| `.github/prompts/open-issue.prompt.md` | Prompt is owned by `agent: imp` and bootstraps branch + initialize + commit + push | Current lifecycle-entry surface is attached to the wrong agent for the intended future model |
| `.github/prompts/implement-cycle.prompt.md` | Prompt is still built around `@imp` TDD-cycle execution and an older activation model | It does not fit a future where epic ownership never passes through `@imp` |
| `docs/development/issue268/research.md` | F_268.12 already defines `@co` as lifecycle coordinator for branch entry and exit | This is the strongest existing prior-art anchor for the redesign |

---

## Findings

### F_341.1 - The workflow model already treats epic work as a separate governance track

`AGENTS.md` defines `epic` as its own workflow with phases `research, design, planning, coordination, documentation, ready`. That is not a technical-delivery shape like `feature`; it is already a governance and decomposition shape. The repository therefore already models epic work as a special case that should not be treated as ordinary implementation.

### F_341.2 - The role model still routes epic work through `@imp`

The same `AGENTS.md` role table still gives `@co` a narrow coordination brief while `@imp` holds all PhaseGate MCP tools, file edits, commits, and phase transitions. `.github/agents/co.agent.md` reinforces that split by telling `@co` to produce actionable hand-overs for `@imp` rather than to own the branch. The current role model therefore contradicts the epic workflow semantics instead of supporting them.

### F_341.3 - The epic contract itself exposes the mismatch

The epic section of `.phase-gate/config/contracts.yaml` already contains dedicated research, planning, design, coordination, documentation, and ready scripts. However, those scripts still use implementation-style sub-roles, and the `coordination` phase says `Coordinate with @co as needed.` That wording only makes sense if `@co` is outside the epic execution path. It is direct evidence that epic semantics and role ownership are not yet aligned.

### F_341.4 - Lifecycle prompt ownership is attached to the wrong agent

`.github/prompts/open-issue.prompt.md` is currently bound to `agent: imp`, even though opening a lifecycle boundary is already conceptually a coordination action. `docs/development/issue268/research.md` F_268.12 explicitly states that lifecycle-boundary writes belong to `@co`, including `create_branch`, `git_checkout`, `initialize_project`, and merge/close actions at lifecycle exit. The current prompt ownership therefore conflicts with the repository's own prior-art research.

### F_341.5 - The lifecycle prompt surfaces are also stale against the live tool contract

The current `open-issue.prompt.md` is not only attached to the wrong agent; it also lags behind the actual tool contract. The current bootstrap path required `initialize_project(issue_number, issue_title, workflow_name)` and required `get_work_context` before follow-up branch-mutating operations would succeed. The prompt still omits `issue_title`, still hardcodes an outdated `git_add_or_commit` message shape, and does not include the `get_work_context` checkpoint. This makes prompt ownership and prompt correctness coupled problems, not separate cleanup tasks.

### F_341.6 - `close-issue.prompt.md` is missing entirely

No `close-issue.prompt.md` file currently exists in `.github/prompts/`. That leaves lifecycle entry modeled by a prompt while lifecycle exit remains implicit. The missing prompt is especially important if epic ownership moves to `@co`, because lifecycle entry and exit should then be symmetric coordination surfaces.

### F_341.7 - `implement-cycle.prompt.md` no longer fits the intended model

`.github/prompts/implement-cycle.prompt.md` is built around `@imp`-owned TDD-cycle execution, older tool-activation assumptions, and direct cycle-level implementation control. That is still coherent for technical child issues, but not for epic ownership. If `@co` becomes full owner of the epic workflow, the prompt should not remain presented as a general path for epic execution.

### F_341.8 - Issue #341 remains a feature while `#339` and `#340` become explicit in-branch research scope

The current issue is correctly labeled and initialized as a `feature` workflow. It is a bounded repository change that researches and then implements a workflow-model redesign; it is not itself the epic it discusses. The user has explicitly chosen to carry child issues `#339` and `#340` inside this same issue branch and inside this research artifact. Research therefore treats them as in-branch orchestration slices of `#341`, not merely as traceability references or later follow-up work.

### F_341.9 - The strongest reusable prior art already exists in issue #268

`docs/development/issue268/research.md` F_268.12 already defines the structural rule that lifecycle-boundary writes belong to `@co`, `@imp` scope closes at `submit_pr`, and `@qa` remains write-free. That prior art is reusable because epic ownership is the same kind of governance-boundary question: it decides who owns branch lifecycle and approval flow, not how implementation code is written.

### F_341.10 - Issue `#339` exposes a concrete transition-feedback gap in current tool responses

`mcp_server/tools/phase_tools.py` and `mcp_server/tools/cycle_tools.py` return plain success text on successful transition paths. They already use the note bus for `RecoveryNote` on conflict handling, and `mcp_server/core/operation_notes.py` already provides `SuggestionNote`, but the success paths emit no proactive note directing the agent to call `get_work_context` next. Existing tests such as `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`, and `tests/mcp_server/unit/tools/test_cycle_tools.py` validate current success formatting and post-enforcement behavior, but no test currently requires the proactive next-step guidance described in issue `#339`.

### F_341.11 - Issue `#340` exposes a concrete invalid-state warning gap in `get_work_context`

`mcp_server/tools/discovery_tools.py` loads workflow and phase from branch state, then suppresses `ValueError` and `KeyError` when workflow-phase instruction lookup fails. The tool degrades to an empty instruction payload and renders the generic `(No instructions defined for workflow..., phase...)` fallback instead of surfacing an invalid workflow/phase mismatch with recovery guidance. The current tests in `tests/mcp_server/unit/tools/test_discovery_tools.py` explicitly assert this fallback behavior for unknown workflow-phase combinations. That means issue `#340` is anchored in an existing code-and-test contract, not only in GitHub issue text.

### F_341.12 - Child-issue traceability is currently branch-level only, not artifact-level

No `docs/development/issue339/` or `docs/development/issue340/` research artifacts currently exist. Given the user's decision to carry both issues on this branch, issue `#341` research becomes the authoritative place to absorb their repo evidence unless later phases deliberately create separate child artifacts for implementation history. This is a documentation-boundary choice, not just a GitHub-linking detail.

---

## Likely Blast Radius

### Production and contract surfaces

- `AGENTS.md`
- `.github/agents/co.agent.md`
- `.github/agents/imp.agent.md`
- `.github/agents/qa.agent.md`
- `.phase-gate/config/contracts.yaml`
- `.github/prompts/open-issue.prompt.md`
- new `.github/prompts/close-issue.prompt.md`
- `.github/prompts/implement-cycle.prompt.md`
- `mcp_server/tools/phase_tools.py`
- `mcp_server/tools/cycle_tools.py`
- `mcp_server/tools/discovery_tools.py`
- `mcp_server/core/operation_notes.py` as existing note-bus prior art if advisory next-step output is added without changing the primary tool result contract
- possibly `.phase-gate/config/workflows.yaml` or related reference docs if ownership or workflow descriptions must be clarified

### Existing patterns and prior art to reuse

- `docs/development/issue268/research.md` F_268.12 lifecycle-coordinator model
- the current epic workflow structure already present in `.phase-gate/config/contracts.yaml`
- the current two-chat / three-agent model wording in `AGENTS.md` and `.github/agents/*.agent.md`
- the typed note bus in `mcp_server/core/operation_notes.py`, especially `SuggestionNote` and `RecoveryNote`, as the existing pattern for follow-up guidance without overloading the primary message body

### Likely affected tests, helpers, and fixtures

Likely impacted automated surfaces span both contract-level epic ownership work and the child-issue behavior gaps:
- `tests/mcp_server/unit/config/test_contracts_loader.py` for epic workflow round-tripping
- `tests/mcp_server/unit/managers/test_project_manager.py` and `tests/mcp_server/unit/tools/test_project_tools.py` for parent-branch and workflow-plan assumptions
- `tests/mcp_server/unit/managers/test_git_manager.py` and `tests/mcp_server/unit/integration/test_git.py` for epic branch creation assumptions
- `tests/mcp_server/unit/tools/test_transition_phase_tool.py`, `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`, and `tests/mcp_server/unit/tools/test_cycle_tools.py` for post-transition response behavior in issue `#339`
- `tests/mcp_server/unit/tools/test_discovery_tools.py` for invalid workflow-phase fallback and recovery messaging in issue `#340`
- `tests/mcp_server/integration/test_context_loaded_enforcement.py`, `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py`, and `tests/mcp_server/unit/test_server.py` if note rendering or guidance placement changes at response-composition level
- issue-type and label tests around `epic`, such as `tests/mcp_server/unit/config/test_issue_config.py` and `tests/mcp_server/unit/tools/test_create_issue_label_assembly.py`

No dedicated prompt test suite was found during this research pass. No dedicated `docs/development/issue339/` or `docs/development/issue340/` artifacts exist yet either. That means prompt ownership, child-issue documentation traceability, and some orchestration guidance changes may still rely on manual validation unless new tests are added later.

---

## Architectural Constraints

- Do not introduce a generic phase-ownership framework. The user explicitly rejected that expansion, and the current problem is narrowly about epic workflow ownership.
- Preserve `@qa` as an outside reviewer with no write access. The approved model depends on QA staying independent.
- Prefer a workflow-level ownership rule over hidden per-phase if-chains or hardcoded role switches.
- Keep research in-bounds: this document may choose the strategy boundary, but it must not turn into the detailed design or implementation plan.
- Treat prompts, agent instructions, and epic phase contracts as one interacting system. Fixing only one layer would preserve ambiguity instead of removing it.
- Treat issues `#339` and `#340` as same-branch behavior slices, not as permission to widen scope into a generic note-policy or generic invalid-state framework unless later design proves that broader abstraction is the smallest coherent implementation.

---

## Approved Strategy

### Boundary: epic workflow ownership
- **Selected strategy:** clean break
- **Decision:** `@co` becomes the full owner of the `epic` workflow from research through ready. `@imp` does not execute epic phases directly.
- **Rationale:** epic work is governance, decomposition, and coordination work. Routing it through `@imp` keeps the current semantic mismatch alive.
- **Constraints for later phases:** design and planning must align role definitions, hand-over paths, and phase contracts around `@co` ownership rather than adding exceptions inside `@imp`.

### Boundary: exact tool allowlist for epic ownership
- **Selected strategy:** narrow explicit allowlist
- **Decision:** keep the current `@co` read and issue-admin set, and add only the tools required to execute epic phases and lifecycle ownership end-to-end: `create_branch`, `git_checkout`, `initialize_project`, `transition_phase`, `force_phase_transition`, `scaffold_artifact`, `safe_edit_file`, `git_add_or_commit`, `git_push`, `run_quality_gates`, `submit_pr`, and `merge_pr`. `close_issue` remains part of lifecycle exit. `@co` does not gain `transition_cycle`, `force_cycle_transition`, `run_tests`, DTO or template validators, or general production-code implementation authority.
- **Rationale:** the current epic documentation and ready contracts already require authoring artifacts, editing docs, moving phases, committing, gating, and submitting PRs. Granting less would leave `@co` unable to perform the workflow it is supposed to own.
- **Constraints for later phases:** `@co` file edits remain limited to epic docs, prompts, contracts, coordination artifacts, and other non-production-code surfaces. Production code and tests remain outside `@co` authority.

### Boundary: epic sub-role vocabulary
- **Selected strategy:** coordination-scoped sub-roles
- **Decision:** epic workflow `sub_role` hints become explicit `@co`-scoped names: `epic-researcher`, `epic-planner`, `epic-designer`, `epic-coordinator`, `epic-documenter`, and `epic-releaser`.
- **Rationale:** the current generic names, especially `researcher` and `implementer`, blur the distinction between `@co` epic ownership and `@imp` technical execution.
- **Constraints for later phases:** do not reuse `implementer` or other `@imp`-flavored labels inside epic phase instructions. Hand-overs and agent docs must use the same vocabulary consistently.

### Boundary: hand-over model
- **Selected strategy:** preserve three-role separation, redesign the contract
- **Decision:** `.github/agents/co.agent.md`, epic workflow phase instructions, and the QA role form a cooperating three-part contract. `@qa` remains an outside reviewer, not an owner of epic execution.
- **Rationale:** the role split remains useful, but the current `@co -> @imp -> @qa` assumption is wrong for epic work.
- **Constraints for later phases:** the revised hand-over paths must be explicit per epic phase and must keep QA outside the ownership chain.

### Boundary: issue and child-slice scope model
- **Selected strategy:** preserve current issue type, absorb child behavior scope in-branch
- **Decision:** issue `#341` remains a `feature` workflow. Child issues `#339` and `#340` are explicitly in scope on this same branch and inside this research artifact; they are not treated as optional later references.
- **Rationale:** the work is a bounded repository change about orchestration ownership, and the concrete behavior gaps from `#339` and `#340` sit on the same transition-feedback and `get_work_context` surfaces already under redesign.
- **Constraints for later phases:** planning must represent `#339` and `#340` as explicit in-branch sub-slices or deliverables of `#341`, not as external dependencies. If separate GitHub issue hygiene is needed later, that is coordination follow-through, not scope deferral.

### Boundary: lifecycle prompt ownership
- **Selected strategy:** clean break
- **Decision:** `open-issue.prompt.md` and the future `close-issue.prompt.md` become `@co`-owned lifecycle surfaces, and tool permissions must align with that ownership.
- **Rationale:** lifecycle entry and exit belong to the coordination boundary, not to technical execution.
- **Constraints for later phases:** prompt ownership, allowed tool rights, and lifecycle flow wording must be updated together. Do not move only one of them.

### Boundary: runtime ownership enforcement
- **Selected strategy:** contract-layer only
- **Decision:** issue `#341` does not introduce a generic runtime agent-ownership enforcement system. The authoritative control surface is the combination of agent docs, prompt ownership, tool allowlists, and epic phase instructions. Runtime changes in this issue stay limited to the targeted guidance improvements from `#339` and `#340`.
- **Rationale:** the user already rejected a generic ownership framework, and the repository now has narrower, sufficient contract surfaces to express epic ownership.
- **Constraints for later phases:** if later evidence suggests a hard runtime gate is still necessary, raise a new issue instead of widening `#341` by stealth.

### Boundary: `implement-cycle.prompt.md` fate
- **Selected strategy:** retire and replace if needed
- **Decision:** `implement-cycle.prompt.md` is retired as an active authoritative prompt. It is not kept as the future epic or child-issue execution surface. If a child-issue helper prompt is still needed later, it must be a new `@imp` prompt designed from current phase instructions rather than a minimal edit of the stale file.
- **Rationale:** the current prompt bakes in obsolete activation steps, stale context-loading assumptions, and a branch-wide execution posture that no longer fits the current three-agent model.
- **Constraints for later phases:** do not keep the existing file half-alive as a compatibility bridge.

### Boundary: issue `#339` transition advisory contract
- **Selected strategy:** narrow proactive guidance on successful transitions
- **Decision:** `transition_phase`, `force_phase_transition`, `transition_cycle`, and `force_cycle_transition` append the same `InfoNote` after successful execution: `Call get_work_context to load the current phase context for this branch before proceeding.` Scope does not extend this note to `git_checkout` or `git_pull` in issue `#341`.
- **Rationale:** this matches the issue statement, keeps the slice narrow, and uses the existing note type whose semantics fit a success-path nudge better than `SuggestionNote`.
- **Constraints for later phases:** the note text must be identical across all four transition tools, emitted regardless of enforcement state, and rendered after the primary success message.

### Boundary: issue `#340` invalid workflow-phase recovery contract
- **Selected strategy:** explicit recovery-oriented warning without hard failure
- **Decision:** when `state.current_phase` is not part of the active workflow, `get_work_context` remains a non-error response but renders an explicit invalid-state warning before the phase-instructions block. That warning names the workflow, the invalid phase, the valid phases list, and the concrete recovery action: use `force_phase_transition` to a valid phase, then call `get_work_context` again.
- **Rationale:** the current generic `No instructions defined` fallback hides the real inconsistency and the real recovery path.
- **Constraints for later phases:** preserve graceful response behavior, but distinguish invalid branch state from genuinely missing state or generic unknown-contract fallback cases. `force_phase_transition` permissiveness stays unchanged in this issue.

---

## Remaining Open Questions

No design-blocking open questions remain.

Implementation may still choose:
- the final user-facing copy for the standardized `#339` and `#340` messages
- the exact file-by-file rollout order across agent docs, prompts, contracts, code, and tests

## Expected Results For Later Phases

Later phases should produce:
- one coherent epic ownership model centered on `@co`
- an explicit `@co` epic allowlist that is narrow but sufficient for research, planning, design, documentation, ready, and lifecycle exit
- epic phase instructions and agent docs that use coordination-scoped sub-roles consistently
- lifecycle prompts owned by `@co` and consistent with current tool contracts
- retirement of `implement-cycle.prompt.md` as a current authoritative surface
- transition success responses that proactively nudge `get_work_context` after phase and cycle transitions in issue `#339`
- `get_work_context` invalid workflow-phase recovery messaging instead of silent empty instructions in issue `#340`
- `#339` and `#340` operationalized as explicit in-branch sub-slices of issue `#341`

## Related Documentation
- **[AGENTS.md][related-1]**
- **[.github/agents/co.agent.md][related-2]**
- **[.github/agents/imp.agent.md][related-3]**
- **[.github/agents/qa.agent.md][related-4]**
- **[.phase-gate/config/contracts.yaml][related-5]**
- **[.phase-gate/config/workflows.yaml][related-6]**
- **[docs/development/issue268/research.md][related-7]**
- **[docs/architecture/VSCODE_AGENT_ORCHESTRATION.md][related-8]**
- **[.github/prompts/open-issue.prompt.md][related-9]**
- **[.github/prompts/implement-cycle.prompt.md][related-10]**

<!-- Link definitions -->

[related-1]: AGENTS.md
[related-2]: .github/agents/co.agent.md
[related-3]: .github/agents/imp.agent.md
[related-4]: .github/agents/qa.agent.md
[related-5]: .phase-gate/config/contracts.yaml
[related-6]: .phase-gate/config/workflows.yaml
[related-7]: docs/development/issue268/research.md
[related-8]: docs/architecture/VSCODE_AGENT_ORCHESTRATION.md
[related-9]: .github/prompts/open-issue.prompt.md
[related-10]: .github/prompts/implement-cycle.prompt.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-05-23 | Agent | Resolve the design-blocking research questions by fixing the epic tool allowlist, epic sub-role vocabulary, `implement-cycle.prompt.md` retirement path, and the exact behavior contracts for issues `#339` and `#340` |
| 1.2 | 2026-05-23 | Agent | Restart research from step 1, absorb issues `#339` and `#340` as same-branch research scope, and add direct code/test evidence for transition guidance and invalid-phase warning gaps |
| 1.1 | 2026-05-23 | Agent | Expand pre-research nucleus into evidence-backed research, capture Approved Strategy, add prompt ownership findings, and record child-issue traceability boundaries |
| 1.0 | 2026-05-23 | Agent | Initial draft |
