<!-- docs\development\issue271\design.md -->
<!-- template=design version=5827e841 created=2026-05-01T20:00Z updated=2026-05-02T00:00Z -->
# contracts.yaml as SSOT for workflow-phase membership

**Status:** DRAFT  
**Version:** 2.1  
**Last Updated:** 2026-05-02

---

## Purpose

Define the target schema, YAML structure, API surface, and migration strategy for making `contracts.yaml` the single runtime authority for workflow-phase membership and ordering.

## Scope

**In Scope:**
Schema redesign (`WorkflowPhaseEntry`, `ContractsConfig`); YAML restructure of `.st3/config/contracts.yaml`; rename of `PhaseContractsConfig` → `ContractsConfig` and loader method; removal of `WorkflowTemplate.phases` and `_inject_terminal_phase`; migration of all 12 production files and 17 test files in the blast radius; validator inversion; `PhaseConfigContext.phase_contracts` field-type rename.

**Out of Scope:**
`workphases.yaml` cleanup (issue #270); changes to phase behavior contracts beyond what is required by the structural refactor; changes to `enforcement.yaml` or `merge_policy` semantics.

## Prerequisites

Read these first:
1. `docs/development/issue271/research.md` — blast radius mapping (v3.1)
2. Issue #270 — `workphases.yaml` cleanup (parallel, no block identified)

---

## 1. Context & Requirements

### 1.1. Problem Statement

Workflow-phase membership and ordering are split across `workflows.yaml` (`WorkflowTemplate.phases`) and `phase_contracts.yaml` (implied by YAML key presence). `phase_contracts.yaml` cannot be the runtime SSOT for workflow execution because it has no ordered phase list, no first-phase API, and no transition-validation API. The current runtime depends entirely on `WorkflowConfig.phases`, with `ConfigLoader._inject_terminal_phase()` appending the terminal phase at startup, making the full phase sequence invisible in any single config file.

Additionally, `phase_contracts.yaml` already carries `merge_policy` (branch-local file contracts) plus per-phase behavior contracts. Its name no longer reflects its scope after the refactor, and the existing `dict[str, PhaseContractPhase]` YAML structure relies on YAML key-insertion order, which is not guaranteed by the YAML spec.

### 1.2. Requirements

**Functional:**
- [ ] A single config file must be the authoritative source for which phases a workflow contains and in what order
- [ ] The terminal phase (`ready`) must be explicitly declared per workflow in that file, not injected at runtime
- [ ] `ContractsConfig` must expose `get_first_phase(workflow_name)`, `validate_transition(wf, current, target)`, and `get_phases(workflow_name)` with the same semantics as the current `WorkflowConfig` equivalents
- [ ] `workflows.yaml` and `workphases.yaml` must become pure metadata catalogs with no runtime ordering responsibility
- [ ] A `model_validator` must enforce that every workflow's last phase matches `merge_policy.pr_allowed_phase`
- [ ] A startup validator must cross-check that every phase name in `contracts.yaml` exists in the `workphases.yaml` catalog, and every workflow name exists in `workflows.yaml`

**Non-Functional:**
- [ ] Clean break: no deprecated aliases, no backward-compat shims for `WorkflowConfig.phases` or `PhaseContractsConfig`
- [ ] The rename `phase_contracts.yaml` → `contracts.yaml` and `PhaseContractsConfig` → `ContractsConfig` is atomic (single PR)
- [ ] YAML must remain human-readable; phase ordering must be explicit and unambiguous without relying on YAML key-insertion order
- [ ] All 12 production files and 17 test files in the blast radius must be updated in the same PR

### 1.3. Constraints

- No backward-compat shims: all callers migrate in the same PR
- `ready` must appear explicitly as the last phase in every workflow's phase list in `contracts.yaml`
- YAML key order must not be relied upon for phase ordering anywhere in the codebase after this refactor
- The `PhaseConfigContext.phase_contracts: PhaseContractsConfig` field-type rename is part of this refactor

---

## 2. Design Options

Three structural options were evaluated for representing ordered workflow membership in `contracts.yaml`.

### 2.1 — Mixed-keys (phases: list + dict entries at same level)

```yaml
workflows:
  feature:
    phases: [research, implementation, ready]
    research:
      exit_requires: [...]
    implementation:
      cycle_based: true
      subphases: [red, green, refactor]
```

`phases` is `list[str]` and all other keys are `PhaseContractPhase`. A `model_validator(mode="before")` separates them.

**Trade-offs:**

| | |
|---|---|
| ✅ YAML is flat and familiar | ❌ Pydantic requires magic `model_validator` to split metadata keys from phase-contract keys |
| ✅ Minimal nesting | ❌ Adding any new workflow-level metadata field (e.g. `default_execution_mode`) breaks the heuristic silently |
| | ❌ Phase names appear twice: in `phases:` list AND as dict keys — DRY violation within a single block |
| | ❌ `extra="forbid"` cannot be used safely |

### 2.2 — Nested contracts key

```yaml
workflows:
  feature:
    phases: [research, implementation, ready]
    contracts:
      research:
        exit_requires: [...]
      implementation:
        cycle_based: true
```

`phases` and `contracts` are sibling keys on a `WorkflowContractEntry` model.

**Trade-offs:**

| | |
|---|---|
| ✅ Unambiguous Pydantic schema; no parsing magic | ❌ Phase names still appear twice (in `phases:` list and as `contracts` dict keys) |
| ✅ Extensible without schema breakage | ❌ One extra nesting level compared to current YAML |
| ✅ `extra="forbid"` works | ❌ DRY violation remains: a phase entry in `contracts` with no matching entry in `phases` is valid until a validator catches it |

### 2.3 — Phases as ordered list of objects (chosen)

```yaml
workflows:
  feature:
    phases:
      - name: research
        exit_requires: [...]
      - name: implementation
        cycle_based: true
        subphases: [red, green, refactor]
        commit_type_map: {red: test, green: feat, refactor: refactor}
      - name: ready
```

Each entry is a `WorkflowPhaseEntry` (`PhaseContractPhase` + `name: str`). The list is the ordering; the name is the identity.

**Trade-offs:**

| | |
|---|---|
| ✅ Phase name appears exactly once per workflow — no DRY violation | ❌ Slightly more verbose YAML than option 2.1 |
| ✅ Ordering is unambiguous from list position | |
| ✅ No mixed-key parsing; standard Pydantic `list[WorkflowPhaseEntry]` | |
| ✅ Extensible: new `WorkflowPhaseEntry` fields don't conflict with phase names | |
| ✅ `extra="forbid"` works on both `WorkflowPhaseEntry` and `ContractsConfig` | |

---

## 3. Chosen Design

**Decision:** Option 2.3 — phases as an ordered list of objects. Rename `phase_contracts.yaml` → `contracts.yaml` and `PhaseContractsConfig` → `ContractsConfig`. Remove `WorkflowTemplate.phases` from `workflows.yaml`. Remove `_inject_terminal_phase` from the loader. Add `get_first_phase()`, `validate_transition()`, and `get_phases()` to `ContractsConfig`.

**Rationale:** Option 2.3 is the only option that eliminates the DRY violation entirely (phase names in exactly one place per workflow), requires no Pydantic parsing magic, is safe to use with `extra="forbid"`, and is extensible without schema breakage. Options 2.1 and 2.2 both retain the phase-name duplication problem in different forms.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **D1 — Three-file model:** `workphases.yaml` and `workflows.yaml` become pure catalogs; `contracts.yaml` is the runtime SSOT | Separates static catalog concerns from runtime execution contracts; each file has a single clear purpose |
| **D2 — Rename `phase_contracts.yaml` → `contracts.yaml`** | File already carries `merge_policy` (branch-local file contracts) + workflow sequencing; the name `contracts` reflects all responsibilities accurately |
| **D3 — `WorkflowPhaseEntry = PhaseContractPhase + name: str`** | Minimal schema extension; reuses existing validation logic; avoids parallel class hierarchies |
| **D4 — `ContractsConfig.workflows: dict[str, WorkflowEntry]` where `WorkflowEntry.phases: list[WorkflowPhaseEntry]`** | Outer dict keyed by workflow name (stable, unordered); inner list is the ordered phase sequence |
| **D5 — Explicit `ready` in every workflow's phase list; `_inject_terminal_phase` removed** | Terminal phase visible in YAML without reading source code; DRY justified: the *knowledge* lives once in `merge_policy.pr_allowed_phase`, the presence in each list is *data* enforced by `model_validator` |
| **D6 — `model_validator` on `ContractsConfig` enforces last-phase = `merge_policy.pr_allowed_phase`** | Parse-time enforcement; no runtime surprise; single rule written once |
| **D7 — Validator inversion: startup validator checks phase names against `workphases.yaml` catalog, not the reverse** | `contracts.yaml` is authoritative; catalogs are validated *against* it, not the other way around |
| **D8 — Runtime API on `ContractsConfig` directly, no separate interface** | Consistent with existing `WorkflowConfig` pattern; `PhaseStateEngine` and other consumers get equivalent API on the new type; no interface introduced because no alternative implementation exists or is planned |
| **D9 — `PhaseConfigContext.phase_contracts: PhaseContractsConfig` → `contracts: ContractsConfig`** | Field rename follows the class rename; frozen dataclass updated atomically in the same PR |
| **D10 — Module rename: `phase_contracts_config.py` → `contracts_config.py`** | Atomic with the class rename; callers importing from the module path (e.g. `from mcp_server.config.schemas.phase_contracts_config import BranchLocalArtifact`) must update their import path; `BranchLocalArtifact`, `MergePolicy`, `CheckSpec`, and `PhaseContractPhase` remain in the renamed module |
| **D11 — `frozen=True` not applied to `ContractsConfig`, `WorkflowEntry`, `WorkflowPhaseEntry`** | Pydantic v2 does not support `frozen=True` on a model that inherits from a non-frozen model (`WorkflowPhaseEntry` inherits from `PhaseContractPhase` which is not frozen). Applying `frozen` only on the leaf would silently break the inheritance chain. Deviation from §5 CQS is accepted here; the config object is constructed once at startup and injected read-only by convention. `extra="forbid"` is applied on all three models to provide the next-best parse-time safety |
| **D12 — `WorkflowConfig` post-refactor API surface** | `WorkflowTemplate.phases` field removed; `get_first_phase()` and `validate_transition()` removed. `has_workflow(name)` and `get_workflow(name) -> WorkflowTemplate` remain — these serve the catalog role (metadata lookup by name). `get_workflow()` returns a `WorkflowTemplate` with only `name`, `description`, and `default_execution_mode` after `phases` is removed |

### 3.2. Schema Specification

**`WorkflowPhaseEntry`** (extends `PhaseContractPhase`):

```python
class WorkflowPhaseEntry(PhaseContractPhase):
    """Single phase entry in a workflow's ordered phase list."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Phase name; must exist in workphases.yaml catalog")
    # Inherits from PhaseContractPhase:
    #   subphases: list[str]
    #   commit_type_map: dict[str, str]
    #   cycle_based: bool
    #   exit_requires: list[CheckSpec]
    #   cycle_exit_requires: dict[int, list[CheckSpec]]
    # Inherits model_validator: cycle_based requires non-empty commit_type_map
```

**`WorkflowEntry`**:

```python
class WorkflowEntry(BaseModel):
    """Single workflow definition in contracts.yaml."""

    model_config = ConfigDict(extra="forbid")

    phases: list[WorkflowPhaseEntry] = Field(..., min_length=1)

    def get_phase_names(self) -> list[str]:
        return [p.name for p in self.phases]

    def get_phase(self, name: str) -> WorkflowPhaseEntry:
        for p in self.phases:
            if p.name == name:
                return p
        raise ValueError(f"Phase '{name}' not in workflow")
```

**`ContractsConfig`** (replaces `PhaseContractsConfig`):

```python
class ContractsConfig(BaseModel):
    """Typed root object for contracts.yaml."""

    model_config = ConfigDict(extra="forbid")

    merge_policy: MergePolicy
    workflows: dict[str, WorkflowEntry] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_terminal_phase(self) -> ContractsConfig:
        terminal = self.merge_policy.pr_allowed_phase
        for name, workflow in self.workflows.items():
            last = workflow.phases[-1].name
            if last != terminal:
                raise ValueError(
                    f"Workflow '{name}': last phase must be '{terminal}' "
                    f"(merge_policy.pr_allowed_phase), got '{last}'"
                )
        return self

    def get_pr_allowed_phase(self) -> str:
        return self.merge_policy.pr_allowed_phase

    def get_first_phase(self, workflow_name: str) -> str:
        """Return the name of the first phase in the workflow.
        Raises ValueError if workflow_name is unknown."""
        return self._get_workflow(workflow_name).phases[0].name

    def get_phases(self, workflow_name: str) -> list[str]:
        """Return ordered list of phase names for the workflow.
        Raises ValueError if workflow_name is unknown."""
        return self._get_workflow(workflow_name).get_phase_names()

    def validate_transition(
        self,
        workflow_name: str,
        current_phase: str,
        target_phase: str,
    ) -> bool:
        """Validate sequential phase transition. Same error contract as WorkflowConfig.
        Raises ValueError with descriptive message on invalid transition."""
        workflow = self._get_workflow(workflow_name)
        names = workflow.get_phase_names()
        if current_phase not in names:
            raise ValueError(
                f"Current phase '{current_phase}' not in workflow '{workflow_name}'\n"
                f"Valid phases: {names}"
            )
        if target_phase not in names:
            raise ValueError(
                f"Target phase '{target_phase}' not in workflow '{workflow_name}'\n"
                f"Valid phases: {names}"
            )
        current_idx = names.index(current_phase)
        target_idx = names.index(target_phase)
        if target_idx != current_idx + 1:
            next_phase = names[current_idx + 1] if current_idx + 1 < len(names) else None
            raise ValueError(
                f"Invalid transition: {current_phase} → {target_phase}\n"
                f"Expected next phase: {next_phase}\n"
                f"Workflow: {names}\n"
                "Hint: Use force_phase_transition tool for non-sequential transitions"
            )
        return True

    def _get_workflow(self, workflow_name: str) -> WorkflowEntry:
        if workflow_name not in self.workflows:
            available = ", ".join(sorted(self.workflows.keys()))
            raise ValueError(
                f"Unknown workflow: '{workflow_name}'\n"
                f"Available workflows: {available}"
            )
        return self.workflows[workflow_name]
```

### 3.3. YAML Structure

Minimal example of `contracts.yaml` after the refactor (single workflow, trimmed):

```yaml
merge_policy:
  pr_allowed_phase: ready
  branch_local_artifacts:
    - path: .st3/state.json
      reason: "MCP workflow state — branch-local, must never reach main"

workflows:
  feature:
    phases:
      - name: research
        exit_requires:
          - id: research-doc
            type: file_glob
            required: true
            dir: docs/development
            pattern: issue*/research*.md
      - name: implementation
        cycle_based: true
        subphases: [red, green, refactor]
        commit_type_map:
          red: test
          green: feat
          refactor: refactor
        exit_requires:
          - id: implementation-test-suite
            type: file_glob
            required: true
            dir: docs/development
            pattern: issue*/*test_suite*.md
      - name: ready

  hotfix:
    phases:
      - name: implementation
        cycle_based: true
        subphases: [red, green, refactor]
        commit_type_map:
          red: test
          green: feat
          refactor: refactor
      - name: ready
```

### 3.4. API Method Error Contracts

| Method | Return | Error |
|---|---|---|
| `get_first_phase(workflow_name)` | `str` — name of first phase | `ValueError` with available workflows list if `workflow_name` unknown |
| `get_phases(workflow_name)` | `list[str]` — ordered phase names | `ValueError` with available workflows list if `workflow_name` unknown |
| `validate_transition(wf, current, target)` | `bool` (always `True` on success) | `ValueError` with descriptive message matching current `WorkflowConfig` error format, for unknown workflow, unknown phase, or non-sequential transition |


| Step | Files | Rationale |
|---|---|---|
| 1 — New schema | `mcp_server/config/schemas/phase_contracts_config.py` → `contracts_config.py` (D10) + `WorkflowPhaseEntry`, `WorkflowEntry`, `ContractsConfig` | Foundation; all consumers depend on this |
| 2 — Internal re-export | `mcp_server/config/schemas/__init__.py` | Updates symbol names for downstream |
| 3 — Public API re-export | `mcp_server/schemas/__init__.py` | Updates public-facing symbol names |
| 4 — Loader | `mcp_server/config/loader.py` | Remove `_inject_terminal_phase`; rename `load_phase_contracts_config` → `load_contracts_config`; update filename to `contracts.yaml` |
| 5 — Resolver | `mcp_server/managers/phase_contract_resolver.py` | Update `_PHASE_CONTRACTS_DISPLAY_PATH`; rename `PhaseConfigContext.phase_contracts` → `contracts` with type `ContractsConfig` |
| 6 — Runtime consumers | `phase_state_engine.py`, `project_manager.py`, `issue_tools.py` | Migrate from `WorkflowConfig` API to `ContractsConfig` API (see §3.7 for new signatures) |
| 7 — Validator | `mcp_server/config/validator.py` | Invert direction: check phase names against `workphases.yaml` catalog |
| 8 — Composition root | `mcp_server/server.py` | Remove `_inject_terminal_phase` call; update `load_phase_contracts_config` → `load_contracts_config` |
| 9 — YAML file | `.st3/config/phase_contracts.yaml` → `.st3/config/contracts.yaml` | Rename + restructure content to list-of-objects |
| 10 — Remove `phases` from `workflows.yaml` | `mcp_server/config/schemas/workflows.py`, `.st3/config/workflows.yaml` | Remove `WorkflowTemplate.phases` field; update YAML |
| 11 — Tests | All 17 test files in blast radius | Update after all production code is green |
| 12 — External references | `agent.md` r.370 | Update documentation string |

### 3.7. Consumer Constructor Signatures

The following constructors change as part of step 6. The parameter type changes from `WorkflowConfig` to `ContractsConfig`; the parameter name changes accordingly. No other parameters change.

**`PhaseStateEngine.__init__` (current → new):**

```python
# Current
def __init__(
    self,
    workspace_root: Path | str,
    project_manager: ProjectManager,
    git_config: GitConfig,
    workflow_config: WorkflowConfig,       # ← removed
    workphases_config: WorkphasesConfig,
    state_repository: IStateRepository,
    scope_decoder: ScopeDecoder,
    workflow_gate_runner: IWorkflowGateRunner,
    state_reconstructor: IStateReconstructor,
    workflow_state_mutator: IWorkflowStateMutator,
) -> None: ...

# New
def __init__(
    self,
    workspace_root: Path | str,
    project_manager: ProjectManager,
    git_config: GitConfig,
    contracts_config: ContractsConfig,     # ← replaces workflow_config
    workphases_config: WorkphasesConfig,
    state_repository: IStateRepository,
    scope_decoder: ScopeDecoder,
    workflow_gate_runner: IWorkflowGateRunner,
    state_reconstructor: IStateReconstructor,
    workflow_state_mutator: IWorkflowStateMutator,
) -> None: ...
```

**`ProjectManager.__init__` (current → new):**

```python
# Current
def __init__(
    self,
    workspace_root: Path | str,
    workflow_config: WorkflowConfig,       # ← removed
    git_manager: GitManager | None = None,
    workphases_config: WorkphasesConfig | None = None,
    *,
    workflow_status_resolver: WorkflowStatusResolver,
) -> None: ...

# New
def __init__(
    self,
    workspace_root: Path | str,
    contracts_config: ContractsConfig,     # ← replaces workflow_config
    git_manager: GitManager | None = None,
    workphases_config: WorkphasesConfig | None = None,
    *,
    workflow_status_resolver: WorkflowStatusResolver,
) -> None: ...
```

**`CreateIssueTool.__init__` (current → new):**

```python
# Current
def __init__(
    self,
    manager: GitHubManager,
    issue_config: IssueConfig,
    milestone_config: MilestoneConfig,
    workflow_config: WorkflowConfig,       # ← removed
) -> None: ...

# New
def __init__(
    self,
    manager: GitHubManager,
    issue_config: IssueConfig,
    milestone_config: MilestoneConfig,
    contracts_config: ContractsConfig,     # ← replaces workflow_config
) -> None: ...
```


### 3.6. Blast Radius (synchronized with research v3.1)

**Production (12 files):**

| File | Change |
|---|---|
| `mcp_server/config/schemas/phase_contracts_config.py` → `contracts_config.py` | Add `WorkflowPhaseEntry`, `WorkflowEntry`, `ContractsConfig`; keep `PhaseContractPhase`, `MergePolicy`, `BranchLocalArtifact`, `CheckSpec` unchanged; module renamed (D10) |
| `mcp_server/config/schemas/__init__.py` | Replace `PhaseContractsConfig` with `ContractsConfig` in imports and `__all__` |
| `mcp_server/schemas/__init__.py` | Replace `PhaseContractsConfig` with `ContractsConfig` in imports and `__all__` |
| `mcp_server/config/schemas/workflows.py` | Remove `WorkflowTemplate.phases` field; remove `get_first_phase()`, `validate_transition()` from `WorkflowConfig` |
| `mcp_server/config/loader.py` | Remove `_inject_terminal_phase`; rename `load_phase_contracts_config` → `load_contracts_config`; update filename to `contracts.yaml` |
| `mcp_server/config/validator.py` | Invert validation direction |
| `mcp_server/managers/phase_contract_resolver.py` | Update `_PHASE_CONTRACTS_DISPLAY_PATH`; rename `PhaseConfigContext.phase_contracts` → `contracts` with type `ContractsConfig` |
| `mcp_server/managers/phase_state_engine.py` | Migrate `WorkflowConfig.validate_transition()` → `ContractsConfig.validate_transition()` |
| `mcp_server/managers/project_manager.py` | Migrate `workflow.phases` → `ContractsConfig.get_phases()` |
| `mcp_server/tools/issue_tools.py` | Migrate `WorkflowConfig.get_first_phase()` → `ContractsConfig.get_first_phase()` |
| `mcp_server/server.py` | Remove `_inject_terminal_phase` call; rename loader method call |
| `.st3/config/phase_contracts.yaml` | Rename to `contracts.yaml`; restructure to list-of-objects |

**Tests (17 files):**

| File | Change |
|---|---|
| `tests/mcp_server/unit/config/test_workflow_config.py` | Rewrite: `get_first_phase()`, `validate_transition()`, phase-order tests move to `ContractsConfig` |
| `tests/mcp_server/unit/config/test_loader.py` | Remove 4 `_inject_terminal_phase` tests; add `load_contracts_config` tests |
| `tests/mcp_server/unit/tools/test_initialize_project_tool.py` | Update first-phase derivation |
| `tests/mcp_server/unit/managers/test_project_manager.py` | Update phase list assertions |
| `tests/mcp_server/fixtures/workflow_fixtures.py` | Update fixtures to use `ContractsConfig` |
| `tests/mcp_server/test_support.py` | Update path constant, loader method call, `PhaseContractsConfig` → `ContractsConfig` |
| `tests/mcp_server/unit/config/test_phase_contracts_schema.py` | Rename test class; update imports and constructions |
| `tests/mcp_server/unit/config/test_label_startup.py` | Update 7+ fixture methods |
| `tests/mcp_server/unit/config/test_validator_c3.py` | Update imports and instances |
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | Update 4 hardcoded path references; update import |
| `tests/unit/config/test_c_loader_structural.py` | Update filename, loader method, class name references |
| `tests/mcp_server/unit/managers/test_phase_contract_resolver.py` | Update fixture filenames and display path assertion |
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | Update fixture filename |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c1.py` | Update fixture filename and docstring |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c2.py` | Update fixture filename and docstrings |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py` | Update fixture filename |
| `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` | Update fixture filename |

---

## 4. Open Questions

None — all open questions from research v3.1 are resolved by decisions D1–D9 above.

---

## Related Documentation
- **[docs/development/issue271/research.md][related-0]**
- **[docs/development/issue231/research-state-json-absolute-ssot-impact.md][related-1]**
- **[docs/reference/mcp/mcp_vision_reference.md][related-2]**

<!-- Link definitions -->
[related-0]: docs/development/issue271/research.md
[related-1]: docs/development/issue231/research-state-json-absolute-ssot-impact.md
[related-2]: docs/reference/mcp/mcp_vision_reference.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-01 | Agent | Initial scaffold — sections 2 and 3.1 empty (QA: NOGO) |
| 2.0 | 2026-05-02 | Agent | QA NOGO resolved: Section 2 filled with 3 options + trade-offs; Section 3.1 key decisions table (D1–D9); schema specs for `WorkflowPhaseEntry`, `WorkflowEntry`, `ContractsConfig`; YAML example; API error contracts; migration order; blast radius synced to research v3.1 (17 test files); architectural stance on API-on-VO; `PhaseConfigContext` field-rename in scope |
| 2.1 | 2026-05-02 | Agent | QA CONDITIONAL GO resolved: D10 (module rename `contracts_config.py`); D11 (`frozen=True` deviation documented); D12 (`WorkflowConfig` post-refactor API); §3.7 consumer constructor signatures; §3.5 migration table updated with D10 reference; §3.6 blast radius updated; `WorkflowEntry` `extra="forbid"` confirmed present |
