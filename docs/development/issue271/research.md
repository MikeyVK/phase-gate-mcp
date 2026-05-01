<!-- c:\temp\st3\docs\development\issue271\research.md -->
<!-- template=research version=8b7bb3ab created=2026-04-28T14:08Z updated=2026-05-01T00:00Z -->
# Issue #271 Research: phase_contracts.yaml as SSOT for workflow-phase membership

**Status:** COMPLETE  
**Version:** 3.0  
**Last Updated:** 2026-05-01

---

## Purpose

Map the concrete production and test blast radius of removing workflow-phase membership from `workflows.yaml` and making `phase_contracts.yaml` (or its successor) the authoritative runtime source for workflow membership and order.

## Scope

**In Scope:**
Production and test code paths that read workflow phase order or membership from `WorkflowConfig.phases`; configuration loader and validator behavior; initialization and transition behavior that depends on workflow-first phase lists; the rename of `phase_contracts.yaml` and `PhaseContractsConfig` if decided; YAML structural changes if decided.

**Out of Scope:**
Implementing the refactor itself; broader `workphases.yaml` cleanup beyond the overlap already covered by issue #270.

## Prerequisites

Read these first:
1. Issue #271
2. Issue #270
3. docs/development/issue231/research-state-json-absolute-ssot-impact.md

---

## Problem Statement

Workflow-phase membership and ordering are currently split across `workflows.yaml`, `phase_contracts.yaml`, and runtime helpers built around `WorkflowConfig.phases`. That duplication creates drift risk and prevents a single file from being the authoritative source for workflow membership and phase ordering. Additionally, `phase_contracts.yaml` carries responsibilities (merge policy, file contracts, workflow sequencing) that its name may no longer accurately reflect after the refactor.

## Research Goals

- Identify the production code paths that still depend directly on `WorkflowConfig.phases`
- Determine whether `PhaseContractsConfig` or `PhaseContractResolver` already expose an equivalent API for first phase, ordered membership, and transition validation
- Map the config-loader and startup-validator assumptions that must change if `workflows.yaml` stops carrying phase lists
- Identify the highest-impact test suites that currently encode `workflows.yaml` as the workflow-phase SSOT
- Identify all callers that hardcode the filename `"phase_contracts.yaml"` or import `PhaseContractsConfig` by name

---

## Background

Issue #271 was reactivated as the first follow-up after issue #231. The issue statement already identifies the architectural duplication: `workflows.yaml` declares ordered workflow phases, while `phase_contracts.yaml` re-declares the same workflow-phase membership by key presence. The immediate question for research is not whether duplication exists, but where the current runtime still assumes `WorkflowConfig.phases` is authoritative.

---

## Findings

### Current runtime SSOT

Initial inspection confirms the current runtime treats `WorkflowConfig.phases` as the authoritative ordered phase list. `WorkflowConfig.get_first_phase()` and `WorkflowConfig.validate_transition()` in `mcp_server/config/schemas/workflows.py` are direct SSOT helpers over `workflow.phases`. Project initialization copies `tuple(workflow.phases)` into `required_phases` via `ProjectManager.create_project_plan()`. `ConfigLoader._inject_terminal_phase()` appends the terminal phase to `workflow.phases` at startup, reinforcing `workflows.yaml` as the mutable phase-sequence carrier. Startup validation in `ConfigValidator` compares `phase_contracts.yaml` entries against `workflow.get_workflow(workflow_name).phases`, so phase_contracts is currently validated as a *subset* of `workflows.yaml` rather than the authority. `PhaseContractsConfig` and `PhaseContractResolver` expose cycle-based checks, commit-type resolution, and exit gates, but have no ordered workflow membership, first-phase lookup, or transition validation helpers.

`phase_contracts.yaml` uses YAML dict key order for implied phase ordering within a workflow — this is not guaranteed by the YAML spec. The existing `subphases: list[str]` fields within `PhaseContractPhase` demonstrate that explicit ordered lists are already the established pattern for similar problems.

### Production blast radius

All production files that must change:

| File | Reason |
|---|---|
| `mcp_server/config/schemas/workflows.py` | Current holder of ordered workflow membership, `get_first_phase()`, `validate_transition()`; `WorkflowTemplate.phases` field must be removed or hollowed out |
| `mcp_server/config/schemas/phase_contracts_config.py` | The schema class itself (`PhaseContractsConfig`) must be extended or replaced; module may be renamed |
| `mcp_server/config/schemas/__init__.py` | Internal re-export layer: exports `PhaseContractsConfig` by name in `__all__` (r.27, r.83) and re-exports `WorkflowConfig` (r.51, r.95); both change |
| `mcp_server/schemas/__init__.py` | Public API layer: imports directly from `mcp_server.config.schemas.phase_contracts_config` (r.26) and exports `PhaseContractsConfig` (r.29, r.142) and `WorkflowConfig` (r.45, r.150); all downstream callers using `from mcp_server.schemas import PhaseContractsConfig` break via this file |
| `mcp_server/managers/phase_state_engine.py` | Strict phase transitions delegate directly to `WorkflowConfig.validate_transition()`; must migrate to new API |
| `mcp_server/managers/project_manager.py` | Project initialization persists `required_phases` from `workflow.phases`; must migrate |
| `mcp_server/managers/phase_contract_resolver.py` | Imports `PhaseContractsConfig` (r.14); hardcodes display path `".st3/config/phase_contracts.yaml"` (r.18) — breaks on file rename |
| `mcp_server/tools/issue_tools.py` | `create_issue` derives initial phase label from `WorkflowConfig.get_first_phase()` |
| `mcp_server/config/loader.py` | `_inject_terminal_phase()` mutates workflow phase list at startup; `load_phase_contracts_config()` hardcodes filename (r.284) |
| `mcp_server/config/validator.py` | `phase_contracts.yaml` validated against `workflows.yaml`; direction inverts after refactor |
| `mcp_server/server.py` | Calls `ConfigLoader._inject_terminal_phase()` (r.170), `load_phase_contracts_config()` (r.187), wires `PhaseContractResolver` with `phase_contracts` keyword (r.222, r.225) |
| `.st3/config/phase_contracts.yaml` | The YAML file itself; renamed if that decision is taken |

### Test blast radius

All test files that must change:

| File | Reason |
|---|---|
| `tests/mcp_server/unit/config/test_workflow_config.py` | Encodes `get_first_phase()`, `validate_transition()`, and live workflow phase order as `WorkflowConfig` behavior |
| `tests/mcp_server/unit/config/test_loader.py` | Locks in `_inject_terminal_phase` behavior via 4 direct tests (r.49, r.60, r.71, r.84) |
| `tests/mcp_server/unit/tools/test_initialize_project_tool.py` | Derives expected initial phase from `workflow.phases[0]` |
| `tests/mcp_server/unit/managers/test_project_manager.py` | Asserts workflow lengths and exact phase lists from `workflows.yaml` |
| `tests/mcp_server/fixtures/workflow_fixtures.py` | Central test helpers export phase lists from `WorkflowConfig`; used by dependent tests |
| `tests/mcp_server/test_support.py` | Hardcodes `"phase_contracts.yaml"` path (r.247, r.253, r.329); calls `load_phase_contracts_config` by string (r.254, r.330); constructs `PhaseContractsConfig` directly (r.258); widely used by integration tests |
| `tests/mcp_server/unit/config/test_phase_contracts_schema.py` | Imports and constructs `PhaseContractsConfig` directly; test class named `TestPhaseContractsConfigMergePolicy` (r.80) |
| `tests/mcp_server/unit/config/test_label_startup.py` | At least 7 fixture methods construct `PhaseContractsConfig` directly (r.115, r.175, r.199, r.233, r.276 and more) |
| `tests/mcp_server/unit/config/test_validator_c3.py` | Imports `PhaseContractsConfig` (r.31), `MergePolicy` (r.22); builds instances directly |
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | Hardcodes `"phase_contracts.yaml"` as file path 4 times (r.302, r.306, r.318, r.324); imports `BranchLocalArtifact` from `phase_contracts_config` module (r.43) |
| `tests/unit/config/test_c_loader_structural.py` | Hardcodes `"phase_contracts.yaml"` (r.242); calls `load_phase_contracts_config` by string (r.299, r.330); imports and asserts `PhaseContractsConfig` (r.32, r.330, r.349, r.443) |
| `tests/mcp_server/unit/managers/test_phase_contract_resolver.py` | Writes temp `"phase_contracts.yaml"` in fixtures (r.48, r.162, r.199); hardcodes display path assertion `"/.st3/config/phase_contracts.yaml"` (r.181) |
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | Writes temp `"phase_contracts.yaml"` in fixture (r.255) |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c1.py` | Writes temp `"phase_contracts.yaml"` (r.73); references it in docstring (r.121) |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c2.py` | Writes temp `"phase_contracts.yaml"` (r.145, r.241); references in docstring (r.7) |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py` | Writes temp `"phase_contracts.yaml"` (r.239) |
| `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` | Writes temp `"phase_contracts.yaml"` (r.36) |

### References outside mcp_server and tests

`agent.md` (r.370) references `".st3/config/phase_contracts.yaml"` as a documentation string in the enforcement configuration section. This is not a code caller but must be updated if the filename changes.

---

## Open Questions

The following questions must be resolved in the design phase before implementation begins:

- ❓ **YAML structure for phase ordering:** Should ordered workflow membership in the contracts file be expressed as (a) a `phases: list[str]` key alongside existing per-phase dict keys (mixed-keys), (b) a nested `contracts:` key containing the per-phase dict, or (c) phases as an ordered list of objects where each entry carries both the phase name and its contract? Each has different implications for Pydantic schema complexity and YAML readability.

- ❓ **File and class rename:** Should `phase_contracts.yaml` be renamed (e.g., to `contracts.yaml`) to reflect its broader scope after the refactor? If so, what is the new class name for `PhaseContractsConfig` and the new loader method name? Is this rename in scope for issue #271 or a separate issue?

- ❓ **Terminal phase handling:** Should `ready` continue to be injected by `_inject_terminal_phase()` at loader time, or should it be declared explicitly in each workflow's phase list in the contracts file? If explicit, how do we enforce that it is always present and always last?

- ❓ **Validator direction after migration:** After the refactor, does the startup validator check that phase names in the contracts file exist in the `workphases.yaml` catalog, check that workflow names exist in `workflows.yaml`, or both? Does the existing `_validate_phase_contracts` method disappear, invert, or split?

- ❓ **API placement:** Should the new ordered-membership API (`get_first_phase`, `validate_transition`, `get_phases`) live on `PhaseContractsConfig` (or its successor) directly, on a dedicated resolver class, or on a new facade? The design must avoid adding runtime responsibilities to the config value object beyond what is necessary.

- ❓ **Relationship with issue #270:** Issue #270 covers `workphases.yaml` cleanup. Does issue #271 have a dependency on #270, or can they proceed in parallel? If parallel, are there interface contracts that must be agreed before either issue starts implementation?

- ❓ **Clean break enforcement:** The project coding standards (no deprecated aliases, no `| None = None` shims, no backward-compat shims for breaking changes) imply several enforcement questions that the design must answer explicitly:
  - May `WorkflowConfig.phases` remain as a deprecated property during transition, or is it a hard remove?
  - May `PhaseContractsConfig` remain as an alias alongside the new class name, or is it a clean rename everywhere simultaneously?
  - May `phase_contracts.yaml` exist alongside `contracts.yaml` temporarily, or is the rename atomic?
  - Are there callers outside `mcp_server/` (e.g., scripts, CI, documentation strings) that reference `"phase_contracts.yaml"` as a literal string and would not be caught by a Python refactor? (Research finding: `agent.md` is one such caller.)
  - What is the removal policy for `_inject_terminal_phase`? Hard delete in the same PR, or deprecated first?

---

## Related Documentation
- **[docs/development/issue231/research-state-json-absolute-ssot-impact.md][related-1]**
- **[docs/development/issue290/research-issue293-cycle-boundary-semantics.md][related-2]**

<!-- Link definitions -->
[related-1]: docs/development/issue231/research-state-json-absolute-ssot-impact.md
[related-2]: docs/development/issue290/research-issue293-cycle-boundary-semantics.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-28 | Agent | Initial draft — blast radius mapping |
| 2.0 | 2026-05-01 | Agent | Design decisions D1–D6 added (QA: boundary violation) |
| 3.0 | 2026-05-01 | Agent | QA NOGO resolved: D1–D6 removed; open questions reformulated; test blast radius expanded to 13 files; production blast radius expanded to 11 files; clean break enforcement questions added |
| 3.1 | 2026-05-01 | Agent | QA CONDITIONAL GO resolved: `mcp_server/schemas/__init__.py` (public API layer) added to production blast radius |
