<!-- docs\development\issue268\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-13T09:17Z updated= -->
# Issue #268 — MCP-Tool-First Orchestration: get_work_context + context_loaded Gate

**Status:** UPDATED  
**Version:** 1.2  
**Last Updated:** 2026-05-23

---

## Purpose

Define the TDD cycle breakdown for the two-stage delivery of MCP-tool-first orchestration (issue #268). Nine cycles total: one MVP cycle that validates the delivery hypothesis, seven Stage 2 cycles that build the full enforcement infrastructure, and one small follow-up cycle for TODO-discipline reinforcement in the live work-context path.

## Scope

**In Scope:**
Stage 1 MVP: GetWorkContextTool response extension (sub_role_hint, phase_instructions). Stage 2: ContextLoadedCache + interfaces, EnforcementAction.exempt_tools, EnforcementRunner handler, PhaseStateEngine + GitCheckoutTool + GitPullTool reset writers, contracts.yaml + PhaseInstructionsSpec, GetWorkContextTool full implementation, server.py composition root wiring + integration test suite. Follow-up cycle C9: strengthen TODO-discipline reinforcement in the `get_work_context` header while preserving the existing output contract and leaving the static `imp.agent.md` wording update to the documentation phase.

**Out of Scope:**
create_handover tool and SubRoleSpec YAML (OQ 6 — separate issue). Full contracts.yaml instructions authorship for all workflows/phases beyond feature/implementation. close-issue.prompt.md (separate issue). AGENTS.md @co role definition update (separate issue). initialize_project guard bug fix (separate issue — MVP validation harness). TODO-discipline changes to `.github/agents/imp.agent.md` during implementation; that wording lands in documentation phase for this follow-up.
## Prerequisites

Read these first:
1. design.md v1.3 QA-approved (after F1/F2/F3 corrections)
2. Feature branch feature/268-mcp-tool-first-orchestration-get-work-context-create-handover active
3. Issue #330 active as MVP validation harness (bug workflow, head filter fix)
---

## Summary

Two-stage delivery. Stage 1 MVP (C1): restructure `GetWorkContextTool` — source orientation fields (`workflow_name`, `issue_number`, `parent_branch`) from `BranchState`, remove noise fields, rewrite `_format_context()` with `phase_instructions` as dominant first block, remove `include_closed_recent` parameter, add graceful bootstrap fallback. Map content (`_PHASE_INSTRUCTIONS_MAP` with 8 production entries) is unchanged. MVP validates the hypothesis that agents follow `phase_instructions` without reading AGENTS.md, using issue #330 (bug/head-filter fix) as the validation harness. Stage 2 (gated on MVP validation): add `ContextLoadedCache`, `IContextLoadedReader`/`Writer` protocol pair, `check_context_loaded` enforcement handler, state-reset writers in `PhaseStateEngine` and Git tools, `contracts.yaml` instructions section, and full composition-root wiring in `server.py`. Follow-up cycle C9 adds a small live reminder in the `get_work_context` header so TODO-list discipline is reinforced before the phase-specific script, while preserving the current first-H3 contract.

---

## Dependencies

- C2 (interfaces + cache) must precede C4 (runner), C5 (state reset writers), C7 (full tool)
- C3 (EnforcementAction schema) must precede C4 (runner uses exempt_tools)
- C6 (contracts schema) must precede C7 (full tool reads from contracts)
- C4 + C5 + C7 must precede C8 (composition root wires all injections)

---

## TDD Cycles


### Cycle 1: MVP — GetWorkContextTool response extension + F_268.13 restructuring

**Goal:** Restructure `GetWorkContextTool.execute()` to source orientation fields from
`BranchState` (replacing `WorkflowStatusResolver`); remove noise fields; rewrite
`_format_context()` to produce the orientation header + dominant `### 🎯 Phase Instructions`
block; remove the `include_closed_recent` parameter. Map content (`_PHASE_INSTRUCTIONS_MAP`
with all 8 production entries) is retained unchanged — only the lookup path and output
renderer change. Validates core delivery hypothesis: agents follow phase-specific
`phase_instructions` without reading AGENTS.md.

**Tests:**
- `test_get_work_context_returns_sub_role_hint_for_known_phase`: `sub_role_hint='implementer'` when `phase='implementation'`
- `test_get_work_context_returns_phase_instructions_for_feature_implementation`: non-empty instructions string returned for `("feature", "implementation")`
- `test_get_work_context_returns_empty_string_for_unknown_workflow_phase`: `.get()` fallback — no `KeyError` on uncovered `(workflow, phase)` combo
- `test_get_work_context_returns_workflow_name_from_branch_state`: `workflow_name` in response matches `BranchState.workflow_name`
- `test_get_work_context_returns_issue_number_from_branch_state`: `issue_number` in response matches `BranchState.issue_number`
- `test_get_work_context_returns_parent_branch_from_branch_state`: `parent_branch` in response matches `BranchState.parent_branch`
- `test_get_work_context_omits_noise_fields`: response text does not contain `active_issue`, `recent_commits`, or `tdd_cycle_info`
- `test_get_work_context_phase_instructions_is_dominant_first_block`: `### 🎯 Phase Instructions` appears before other content in `_format_context()` output
- `test_get_work_context_graceful_degradation_when_state_unavailable`: no exception raised when `get_state()` returns `None` or raises; empty `phase_instructions` in output
- `test_get_work_context_input_has_no_include_closed_recent`: `GetWorkContextInput` does not accept `include_closed_recent` parameter

**Success Criteria:**
- `GetWorkContextTool.execute()` response contains `sub_role_hint`, `phase_instructions`, `workflow_name`, `issue_number`, and `parent_branch`
- `phase_instructions` for `("feature", "implementation")` is non-empty and embeds hand-over format inline
- `_format_context()` renders `### 🎯 Phase Instructions` as the dominant first block (after orientation header)
- Noise fields (`active_issue`, `recent_commits`, `tdd_cycle_info`, `recently_closed`) absent from output
- Bootstrap degradation: no crash when `BranchState` unavailable; returns orientation header with branch name only
- `include_closed_recent` parameter removed — `GetWorkContextInput()` raises `TypeError` if passed
- Unknown `(workflow, phase)` combinations return empty string, never `KeyError`
- No new constructor parameters — zero DIP surface change for MVP



### Cycle 2: Interfaces + ContextLoadedCache

**Goal:** Define IContextLoadedReader and IContextLoadedWriter Protocol classes (ISP split) and implement ContextLoadedCache as the session-scope in-memory flag store. Foundational cycle: all Stage 2 cycles depend on these interfaces. Cache defaults to False on cold start; no file reads in __init__.

**Tests:**
- test_context_loaded_cache_defaults_false: is_context_loaded returns False for unknown branch
- test_context_loaded_cache_set_true: set_context_loaded(branch, value=True) makes is_context_loaded return True
- test_context_loaded_cache_reset: set_context_loaded(branch, value=False) after True returns False
- test_context_loaded_cache_per_branch_isolation: flag for branch A does not affect branch B
- test_icontextloaded_reader_protocol_conformance: isinstance(cache, IContextLoadedReader) is True
- test_icontextloaded_writer_protocol_conformance: isinstance(cache, IContextLoadedWriter) is True

**Success Criteria:**
- IContextLoadedReader and IContextLoadedWriter are @runtime_checkable Protocol classes in core/interfaces/__init__.py
- ContextLoadedCache implements both protocols and passes isinstance checks
- No import-time side effects — pure in-memory class, no ClassVar singleton

**Dependencies:** C1 committed


### Cycle 3: EnforcementAction schema — exempt_tools field + enabled flag + model_validator

**Goal:** Add `exempt_tools: list[str] = []` and `enabled: bool = True` fields to `EnforcementAction`. A model_validator rejects `exempt_tools` on action types other than those in `_EXEMPT_TOOLS_ALLOWED_TYPES`. `enabled` is a generic gate on/off switch (explicit over implicit: disabling requires a deliberate YAML config decision). Fail-Fast §4: detected at Pydantic parse time (server startup). `_EXEMPT_TOOLS_ALLOWED_TYPES` frozenset is the SSOT for which action types support exemption (OCP §1.2).

**Tests:**
- test_enforcement_action_exempt_tools_defaults_empty: default value is []
- test_enforcement_action_enabled_defaults_true: enabled field defaults to True
- test_enforcement_action_enabled_false_parses: enabled=False parses without error
- test_enforcement_action_exempt_tools_accepted_on_check_context_loaded: valid parse when type=check_context_loaded
- test_enforcement_action_exempt_tools_rejected_on_check_pr_status: ValidationError when type=check_pr_status with non-empty exempt_tools
- test_enforcement_action_exempt_tools_rejected_on_check_phase_readiness: ValidationError when type=check_phase_readiness
- test_enforcement_action_extra_fields_still_rejected: extra='forbid' regression check

**Success Criteria:**
- exempt_tools field present with default []
- enabled field present with default True
- _EXEMPT_TOOLS_ALLOWED_TYPES frozenset is the extension point — add new types there, no if-chain change
- model_validator raises ValueError on invalid type+exempt_tools combo at parse time
- Existing enforcement.yaml parses without error (no regression)

**Dependencies:** C1 committed


### Cycle 4: EnforcementRunner — _handle_check_context_loaded handler

**Goal:** Add `_context_loaded_reader` constructor param to `EnforcementRunner`. Register `_handle_check_context_loaded` in `_build_default_registry()`. Handler implements: gate disabled when `action.enabled=False` (explicit YAML decision — not by absent dependency); raises `ConfigError` when `action.enabled=True` but reader is `None` (composition-root wiring error — fail loudly); bootstrap domain rule (`state.json` absent = gate inactive, no tool names in code); static `exempt_tools` bypass; detached-HEAD pass-through. All tests via `runner.run()` public API (§14).

**Tests:**
- test_enforcement_runner_blocks_when_context_not_loaded: ValidationError raised when is_context_loaded returns False
- test_enforcement_runner_passes_when_context_loaded: no error when is_context_loaded returns True
- test_enforcement_runner_gate_inactive_when_no_state_json: no error when state.json absent — bootstrap domain rule
- test_enforcement_runner_gate_disabled_when_enabled_false: no error when action.enabled=False, regardless of reader
- test_enforcement_runner_raises_config_error_when_gate_enabled_but_reader_missing: ConfigError when action.enabled=True and context_loaded_reader=None
- test_enforcement_runner_exempt_tool_bypasses_gate: no error when tool_name in action.exempt_tools
- test_enforcement_runner_detached_head_passes: no error when _get_current_git_branch returns None

**Success Criteria:**
- IContextLoadedReader injected via constructor (DIP §1.5)
- Gate disabled via action.enabled=False — never via absent reader (explicit over implicit)
- reader=None with enabled=True is a wiring error: ConfigError raised immediately
- Bootstrap exemption: no tool names in Python code — predicate is state.json existence
- Handler tested exclusively via runner.run() public API — no private method access (§14)
- check_context_loaded registered in _build_default_registry() — registry pattern, no if-chain (OCP)

**Dependencies:** C2 (IContextLoadedReader interface), C3 (EnforcementAction.exempt_tools + enabled)


### Cycle 5: State reset writers — PhaseStateEngine, GitCheckoutTool, GitPullTool

**Goal:** Inject IContextLoadedWriter into PhaseStateEngine, GitCheckoutTool, and GitPullTool. PhaseStateEngine adds _reset_context_loaded() helper; calls it in transition(), force_transition(), enter_cycle(), force_enter_cycle(). GitCheckoutTool resets on successful checkout. GitPullTool resets conditionally (non-noop pull only). Grouped because all share the same write-only injection pattern and reset semantics.

**Tests:**
- test_phase_state_engine_resets_flag_on_transition: writer.set_context_loaded called after _apply_state via public transition()
- test_phase_state_engine_resets_flag_on_force_transition: same for force path
- test_phase_state_engine_resets_flag_on_enter_cycle: same for cycle entry
- test_phase_state_engine_no_reset_when_writer_none: no AttributeError when writer=None
- test_git_checkout_resets_context_loaded_on_success: writer called with new branch name and value=False
- test_git_checkout_no_reset_when_writer_none: graceful when not injected
- test_git_pull_resets_on_commits_received: writer called when pull result is non-noop
- test_git_pull_no_reset_on_already_up_to_date: writer NOT called on noop pull
- test_git_pull_no_reset_when_writer_none: graceful when not injected

**Success Criteria:**
- IContextLoadedWriter injected via constructor in all three classes (DIP)
- _reset_context_loaded() is private — tested only via public transition() API (§14)
- GitPullTool distinguishes noop vs non-noop before calling writer
- No regression on existing PhaseStateEngine, GitCheckoutTool, GitPullTool tests

**Dependencies:** C2 (IContextLoadedWriter interface)


### Cycle 6: contracts.yaml instructions section + PhaseInstructionsSpec schema

**Goal:** Add `PhaseInstructionsSpec` Pydantic model to `contracts_config.py` with `sub_role`, `phase_instructions`, `handover_template` fields (frozen, `ConfigDict(frozen=True)`). Add **required** `instructions: PhaseInstructionsSpec` field to phase entry schema (no `None`, no default — explicit over implicit: every defined phase must have instructions). Fully author `.phase-gate/config/contracts.yaml` with `instructions` blocks for all defined workflows × phases. `handover_template` is optional (`str | None = None`) — phases that do not need a handover template may omit the field.

**Tests:**
- test_phase_instructions_spec_parses_with_all_fields: valid YAML dict parses correctly
- test_phase_instructions_spec_is_frozen: assignment raises ValidationError or AttributeError
- test_phase_instructions_spec_requires_all_three_fields: missing any field raises ValidationError
- test_contracts_config_loads_instructions_field: PhaseEntry.instructions is PhaseInstructionsSpec when present
- test_contracts_config_phase_entry_without_instructions_raises: WorkflowPhaseEntry without instructions raises ValidationError at parse time

**Success Criteria:**
- PhaseInstructionsSpec has model_config = ConfigDict(frozen=True)
- Phase entry schema enforces instructions as required field at Pydantic parse time (Fail-Fast §4)
- No post-load validator needed — Pydantic required-field enforcement is the SSOT
- contracts.yaml contains instructions for every phase in every defined workflow
- instructions blocks absent from contracts.yaml cause startup failure

**Dependencies:** C1 committed


### Cycle 7: GetWorkContextTool full — writer injection + contracts read + handover_template

**Goal:** Replace the two TODO(MVP) lookup maps with reads from injected ContractsConfig. Add IContextLoadedWriter constructor param. Add third response field handover_template from PhaseInstructionsSpec. Flag set at end of execute(). Removes all MVP transitional debt — no _SUB_ROLE_MAP or _PHASE_INSTRUCTIONS_MAP remain.

**Tests:**
- test_get_work_context_reads_sub_role_from_contracts_config: sub_role_hint not from hardcoded dict
- test_get_work_context_reads_phase_instructions_from_contracts_config: phase_instructions not from hardcoded dict
- test_get_work_context_returns_handover_template_field: ctx['handover_template'] present and matches contracts.yaml entry
- test_get_work_context_sets_context_loaded_flag_on_success: writer.set_context_loaded called with branch and value=True
- test_get_work_context_no_writer_does_not_crash: optional writer=None is safe

**Success Criteria:**
- _SUB_ROLE_MAP and _PHASE_INSTRUCTIONS_MAP removed — no # TODO(MVP) remaining
- ContractsConfig injected via constructor — not read from file in execute() (DIP)
- Flag write is a side-effect at end of execute(); does not affect return value shape
- ctx keys: sub_role_hint, phase_instructions, handover_template all present

**Dependencies:** C2 (IContextLoadedWriter), C6 (PhaseInstructionsSpec + contracts.yaml)


### Cycle 8: server.py composition root + integration test suite

**Goal:** Instantiate ContextLoadedCache once at server.py composition root; wire into EnforcementRunner (reader), GetWorkContextTool (writer), PhaseStateEngine (writer), GitCheckoutTool (writer), GitPullTool (writer). Activate enforcement.yaml check_context_loaded rule with force tool exemptions. Integration tests validate full gate round-trip without real filesystem side effects.

**Tests:**
- test_gate_blocks_write_tool_without_get_work_context: branch_mutating tool raises before get_work_context
- test_gate_unblocks_after_get_work_context: same tool succeeds after get_work_context called
- test_force_phase_transition_exempt_from_gate: force tool succeeds even when flag is False
- test_force_cycle_transition_exempt_from_gate: same for cycle force tool
- test_bootstrap_domain_rule_no_state_json: branch_mutating tool succeeds when no state.json present
- test_phase_transition_resets_gate: flag becomes False after transition_phase call
- test_checkout_resets_gate: flag becomes False after git_checkout call

**Success Criteria:**
- ContextLoadedCache instantiated once — no double-instantiation in server.py (DIP §11)
- enforcement.yaml check_context_loaded rule active with force_phase_transition + force_cycle_transition in exempt_tools
- Integration tests are hermetic: all writes via tmp_path, no real GitHub API calls
- Full test suite green with no regressions
- Note: mandatory ConfigLoader enforcement (all phases must have instructions) is out of scope for C8 — deferred until full contracts.yaml authorship is complete.

**Dependencies:** C4 (handler registered), C5 (reset writers injected), C7 (full GetWorkContextTool)

---

### Cycle 9: TODO-discipline reinforcement in live work context

**Goal:** Add a small, always-visible TODO-discipline reminder to the `get_work_context` orientation/header layer without changing the fieldless input shape, without adding a new H3 block before `### 🎯 Phase Instructions`, and without moving the static `imp.agent.md` wording update into the implementation phase. This cycle keeps production scope to the live work-context path and its tests; the companion `imp.agent.md` wording change is intentionally deferred to documentation phase.

**Tests:**
- `test_get_work_context_phase_instructions_is_dominant_first_block`: remains green — `### 🎯 Phase Instructions` stays the first H3 block
- `test_get_work_context_renders_todo_discipline_reminder_in_header`: output includes a fixed TODO-discipline reminder in the non-H3 orientation/header layer
- `test_get_work_context_returns_phase_instructions_for_feature_implementation`: remains green — the phase script still renders under the phase-instructions block
- `test_get_work_context_graceful_degradation_when_state_unavailable`: remains green — the reminder does not break bootstrap degradation

**Success Criteria:**
- `mcp_server/tools/discovery_tools.py` adds a stable TODO-discipline reminder above the phase-instructions block without introducing a new H3 section
- `.github/agents/imp.agent.md` is not modified in implementation phase; that wording update remains documentation work by explicit scope decision
- `tests/mcp_server/unit/tools/test_discovery_tools.py` covers the reminder and preserves the current first-H3 contract
- Focused discovery-tool tests are green, and file-scoped quality checks pass for changed Python files
- No typing suppressions, global config changes, or unrelated contract rewrites are introduced

**Dependencies:** C7 committed; F_268.14 research finding and Approved Strategy recorded

---

## Risks & Mitigation

- **Risk:** MVP validation fails — agents do not follow phase_instructions from get_work_context response
  - **Mitigation:** Stage 2 (gate enforcement) is held until MVP is validated. If hypothesis fails, Stage 2 scope changes before implementation begins.
- **Risk:** server.py composition root wiring (C8) has high blast radius — injection errors silent at startup
  - **Mitigation:** C8 integration tests validate full round-trip. EnforcementRunner startup validation catches unregistered action types at parse time.
- **Risk:** GitPullTool noop detection brittle — relies on parsing pull output string
  - **Mitigation:** Test both noop and non-noop pull outcomes explicitly in C5. If string parsing unreliable, use return code or structured result.

## Related Documentation
- **[docs/development/issue268/research.md][related-1]**
- **[docs/development/issue268/design.md][related-2]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-3]**
- **[mcp_server/tools/discovery_tools.py][related-4]**
- **[mcp_server/managers/enforcement_runner.py][related-5]**
- **[mcp_server/state/pr_status_cache.py][related-6]**
- **[.phase-gate/config/enforcement.yaml][related-7]**
- **[.phase-gate/config/contracts.yaml][related-8]**

<!-- Link definitions -->

[related-1]: docs/development/issue268/research.md
[related-2]: docs/development/issue268/design.md
[related-3]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-4]: mcp_server/tools/discovery_tools.py
[related-5]: mcp_server/managers/enforcement_runner.py
[related-6]: mcp_server/state/pr_status_cache.py
[related-7]: .phase-gate/config/enforcement.yaml
[related-8]: .phase-gate/config/contracts.yaml

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.2 | 2026-05-23 | Agent | Add follow-up Cycle 9 for TODO-discipline reinforcement and defer imp.agent.md wording to documentation phase |
| 1.1 | 2026-05-19 | Agent | Update plan to the finalized eight-cycle two-stage delivery |
| 1.0 |  | Agent | Initial draft |
