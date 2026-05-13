<!-- docs\development\issue268\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-13T09:17Z updated= -->
# Issue #268 — MCP-Tool-First Orchestration: get_work_context + context_loaded Gate

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-13

---

## Purpose

Define the TDD cycle breakdown for the two-stage delivery of MCP-tool-first orchestration (issue #268). Eight cycles: one MVP cycle that validates the delivery hypothesis, seven Stage 2 cycles that build the full enforcement infrastructure.

## Scope

**In Scope:**
Stage 1 MVP: GetWorkContextTool response extension (sub_role_hint, phase_instructions). Stage 2: ContextLoadedCache + interfaces, EnforcementAction.exempt_tools, EnforcementRunner handler, PhaseStateEngine + GitCheckoutTool + GitPullTool reset writers, contracts.yaml + PhaseInstructionsSpec, GetWorkContextTool full implementation, server.py composition root wiring + integration test suite.

**Out of Scope:**
create_handover tool and SubRoleSpec YAML (OQ 6 — separate issue). Full contracts.yaml instructions authorship for all workflows/phases beyond feature/implementation. close-issue.prompt.md (separate issue). AGENTS.md @co role definition update (separate issue). initialize_project guard bug fix (separate issue — MVP validation harness).

## Prerequisites

Read these first:
1. design.md v1.1 QA-approved
2. Feature branch feature/268-mcp-tool-first-orchestration-get-work-context-create-handover active
3. Separate issue created for initialize_project guard bug (MVP validation harness)
---

## Summary

Two-stage delivery. Stage 1 MVP: extend GetWorkContextTool to return sub_role_hint and phase_instructions via two module-level lookup maps. MVP validates the hypothesis that agents follow phase_instructions without reading AGENTS.md, using the initialize_project guard bug (separate issue) as the real-work test subject. Stage 2 (gated on MVP validation): add ContextLoadedCache, IContextLoadedReader/Writer protocol pair, check_context_loaded enforcement handler, state-reset writers in PhaseStateEngine and Git tools, contracts.yaml instructions section, and full composition-root wiring in server.py.

---

## Dependencies

- C2 (interfaces + cache) must precede C4 (runner), C5 (state reset writers), C7 (full tool)
- C3 (EnforcementAction schema) must precede C4 (runner uses exempt_tools)
- C6 (contracts schema) must precede C7 (full tool reads from contracts)
- C4 + C5 + C7 must precede C8 (composition root wires all injections)

---

## TDD Cycles


### Cycle 1: MVP — GetWorkContextTool response extension

**Goal:** Extend GetWorkContextTool.execute() to append sub_role_hint and phase_instructions to the context dict using two module-level lookup maps marked # TODO(MVP). Validates core delivery hypothesis with minimal blast radius: one file, no cache, no gate.

**Tests:**
- test_get_work_context_returns_sub_role_hint_for_known_phase: sub_role_hint='implementer' when phase='implementation'
- test_get_work_context_returns_phase_instructions_for_feature_implementation: non-empty instructions string returned for (feature, implementation)
- test_get_work_context_returns_empty_string_for_unknown_workflow_phase: .get() fallback — no KeyError on uncovered (workflow, phase) combo
- test_get_work_context_returns_empty_string_when_workflow_unavailable: graceful fallback when workflow resolution raises

**Success Criteria:**
- GetWorkContextTool.execute() response contains sub_role_hint and phase_instructions keys
- phase_instructions for (feature, implementation) embeds hand-over format inline at end
- Unknown (workflow, phase) combinations return empty string, never KeyError
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


### Cycle 3: EnforcementAction schema — exempt_tools field + model_validator

**Goal:** Add exempt_tools: list[str] = [] field to EnforcementAction with a model_validator that rejects exempt_tools on action types other than those in _EXEMPT_TOOLS_ALLOWED_TYPES. Fail-Fast §4: detected at Pydantic parse time (server startup). _EXEMPT_TOOLS_ALLOWED_TYPES frozenset is the SSOT for which action types support exemption (OCP §1.2).

**Tests:**
- test_enforcement_action_exempt_tools_defaults_empty: default value is []
- test_enforcement_action_exempt_tools_accepted_on_check_context_loaded: valid parse when type=check_context_loaded
- test_enforcement_action_exempt_tools_rejected_on_check_pr_status: ValidationError when type=check_pr_status with non-empty exempt_tools
- test_enforcement_action_exempt_tools_rejected_on_check_phase_readiness: ValidationError when type=check_phase_readiness
- test_enforcement_action_extra_fields_still_rejected: extra='forbid' regression check

**Success Criteria:**
- exempt_tools field present with default []
- _EXEMPT_TOOLS_ALLOWED_TYPES frozenset is the extension point — add new types there, no if-chain change
- model_validator raises ValueError on invalid type+exempt_tools combo at parse time
- Existing enforcement.yaml parses without error (no regression)

**Dependencies:** C1 committed


### Cycle 4: EnforcementRunner — _handle_check_context_loaded handler

**Goal:** Add _context_loaded_reader constructor param to EnforcementRunner. Register _handle_check_context_loaded in _build_default_registry(). Handler implements: gate disabled when reader=None; bootstrap domain rule (state.json absent = gate inactive, no tool names in code); static exempt_tools bypass; detached-HEAD pass-through. All tests via runner.run() public API (§14).

**Tests:**
- test_enforcement_runner_blocks_when_context_not_loaded: ValidationError raised when is_context_loaded returns False
- test_enforcement_runner_passes_when_context_loaded: no error when is_context_loaded returns True
- test_enforcement_runner_gate_inactive_when_no_state_json: no error when state.json absent — bootstrap domain rule
- test_enforcement_runner_gate_disabled_when_reader_none: no error when context_loaded_reader=None injected
- test_enforcement_runner_exempt_tool_bypasses_gate: no error when tool_name in action.exempt_tools
- test_enforcement_runner_detached_head_passes: no error when _get_current_git_branch returns None

**Success Criteria:**
- IContextLoadedReader injected via constructor (DIP §1.5)
- Bootstrap exemption: no tool names in Python code — predicate is state.json existence
- Handler tested exclusively via runner.run() public API — no private method access (§14)
- check_context_loaded registered in _build_default_registry() — registry pattern, no if-chain (OCP)

**Dependencies:** C2 (IContextLoadedReader interface), C3 (EnforcementAction.exempt_tools)


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

**Goal:** Add PhaseInstructionsSpec Pydantic model to contracts_config.py with sub_role, phase_instructions, handover_template fields (all frozen, ConfigDict(frozen=True)). Add optional instructions: PhaseInstructionsSpec | None field to phase entry schema. Populate feature/implementation entry in .phase-gate/config/contracts.yaml. handover_template text is the Imp→QA format from design.md.

**Tests:**
- test_phase_instructions_spec_parses_with_all_fields: valid YAML dict parses correctly
- test_phase_instructions_spec_is_frozen: assignment raises ValidationError or AttributeError
- test_phase_instructions_spec_requires_all_three_fields: missing any field raises
- test_contracts_config_loads_instructions_field: PhaseEntry.instructions is PhaseInstructionsSpec when present
- test_contracts_config_instructions_optional: phase with no instructions field parses as None
- test_contracts_config_validator_passes_when_some_instructions_none: validator does not raise ConfigError when only feature/implementation has instructions and other phase entries have instructions=None

**Success Criteria:**
- PhaseInstructionsSpec has model_config = ConfigDict(frozen=True)
- Phase entry schema accepts instructions as optional field (None default)
- feature/implementation entry in contracts.yaml populated with sub_role, phase_instructions, handover_template
- ConfigLoader post-load validator infrastructure added; raises ConfigError only after full instructions authorship (all workflows x phases populated — deferred issue). For C6: validator code present, non-enforcing on None instructions field.

**Dependencies:** C1 committed


### Cycle 7: GetWorkContextTool full — writer injection + contracts read + handover_template

**Goal:** Replace the two TODO(MVP) lookup maps with reads from injected ContractsConfig. Add IContextLoadedWriter constructor param. Add third response field handover_template from PhaseInstructionsSpec. Flag set at end of execute(). Removes all MVP transitional debt — no _SUB_ROLE_MAP or _PHASE_INSTRUCTIONS_MAP remain.

**Tests:**
- test_get_work_context_reads_sub_role_from_contracts_config: sub_role_hint not from hardcoded dict
- test_get_work_context_reads_phase_instructions_from_contracts_config: phase_instructions not from hardcoded dict
- test_get_work_context_returns_handover_template_field: ctx['handover_template'] present and matches contracts.yaml entry
- test_get_work_context_sets_context_loaded_flag_on_success: writer.set_context_loaded called with branch and value=True
- test_get_work_context_no_writer_does_not_crash: optional writer=None is safe
- test_get_work_context_returns_empty_strings_when_instructions_none: graceful for phase with no instructions entry

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
| 1.0 |  | Agent | Initial draft |