<!-- docs/development/issue268/design.md -->
<!-- template=design version=5827e841 created=2026-05-13T08:34Z updated=2026-05-13 -->
# MCP-Tool-First Orchestration: get_work_context Extension + context_loaded Gate

**Status:** UPDATED
**Version:** 1.3
**Last Updated:** 2026-05-19

---

## 1. Context & Requirements

### 1.1. Problem Statement

Agents have no reliable mechanism to receive phase-specific work instructions. Hook injection
paths are dead (issue #263). The only reliable injection path is MCP tool-call responses.
`get_work_context` must be extended to deliver phase instructions, and a `context_loaded`
enforcement gate must block write-tools until an agent has acknowledged its context.

### 1.2. Requirements

**Functional:**
- [ ] `get_work_context` returns `sub_role_hint`, `phase_instructions`, `workflow_name`, `issue_number`, and `parent_branch` (sourced from `BranchState`)
- [ ] MVP: `phase_instructions` embeds hand-over format inline for roles that produce hand-overs
- [ ] Stage 2: `get_work_context` additionally returns `handover_template` as a separate field read from `contracts.yaml`
- [ ] Response omits noise fields: no `tdd_cycle_info` block, `active_issue`, `recent_commits`, or `recently_closed` in output (F_268.13)
- [ ] `current_cycle` rendered as compact position indicator only — no name, no total (format: `cycle N`)
- [ ] `phase_source`/`phase_confidence` conditional: rendered only when confidence ≠ `high` or source ≠ `state_json`
- [ ] `phase_instructions` promoted to dominant first block (after orientation header)
- [ ] `linked_issue_number` → `issue_number`; sourced from `BranchState.issue_number` (eliminates branch-name regex)
- [ ] `GetWorkContextInput.include_closed_recent` parameter removed (breaking — no external consumers)
- [ ] `context_loaded` flag resets on phase entry, cycle entry, `git_checkout`, non-noop `git_pull`
- [ ] All `branch_mutating` tools are blocked when `context_loaded` is `false`
- [ ] `force_phase_transition` and `force_cycle_transition` are exempt via `exempt_tools` in `enforcement.yaml`
- [ ] Gate is inactive for all tools when no `state.json` exists (bootstrap — no phase to acknowledge)
- [ ] `get_work_context` sets `context_loaded = true` as a command side-effect
- [ ] `EnforcementAction` schema gains `exempt_tools: list[str] = []` with startup validation
- [ ] `EnforcementAction` schema gains `enabled: bool = True` — explicit gate on/off switch (explicit over implicit)

**Non-Functional:**
- [ ] `context_loaded` is session-scope in-memory only — no `state.json` persistence
- [ ] `EnforcementRunner` receives `IContextLoadedReader` (read-only — ISP §1.4)
- [ ] `GetWorkContextTool` receives `IContextLoadedWriter` (write-only — ISP §1.4)
- [ ] `PhaseStateEngine` receives `IContextLoadedWriter` (write-only — ISP §1.4)
- [ ] `GitCheckoutTool` and `GitPullTool` receive `IContextLoadedWriter` (write-only — ISP §1.4)
- [ ] All new dependencies injected via constructor (DIP §1.5)
- [ ] `ContextLoadedCache` instantiated once at `server.py` composition root (DIP §11)
- [ ] `exempt_tools` validated at Pydantic parse time, not at call time (Fail-Fast §4)

### 1.3. Constraints

- CQS: `get_work_context.execute()` is a command-with-result at the tool layer. This is
  an accepted exception at the tool boundary (see research OQ 1 — closed). The flag
  write is a side-effect of context delivery, not a separate domain command.
- MVP hardcoded fields violate Config-First §3 intentionally. This is an acknowledged
  transitional design: the MVP validates the delivery mechanism before committing to
  full `contracts.yaml` authorship. The code must carry an explicit `# TODO(MVP)` comment
  marking the hardcoded section for replacement.

---

## 2. Design Options

### Option A — MVP only (hardcoded fields, no gate)

Extend `GetWorkContextTool.execute()` to append `sub_role_hint` and `phase_instructions`
to the context dict using module-level lookup maps. No new files. No cache. No enforcement
gate. Full implementation deferred until MVP validates the hypothesis.

**Pros:** minimal blast radius; validates hypothesis before full investment.
**Cons:** `context_loaded` gate does not exist; agents cannot be mechanically blocked.

### Option B — Full implementation (cache + gate + config)

Implement all components in one pass: `ContextLoadedCache`, interfaces, enforcement handler,
`enforcement.yaml` rule, `contracts.yaml` instructions section for all workflow+phases.

**Pros:** complete feature; mechanically enforced behavior.
**Cons:** substantial implementation risk with unproven delivery mechanism; repeats #263.

### Option C — Two-stage delivery (chosen)

MVP first (Option A), then full implementation (Option B) gated on MVP validation result.
The MVP uses the `initialize_project` guard bug (issue separate, see F_268.10/F_268.11) as
the real-work validation harness.

---

## 3. Chosen Design — Option C (Two-Stage)

**Decision:** Two-stage delivery: MVP first (hardcoded fields, no cache/gate), full
implementation gated on MVP validation. MVP validates the core hypothesis that agents follow
`phase_instructions` without reading AGENTS.md.

**Rationale:** Full implementation is substantial risk. Previous orchestration work (#263)
invested similar effort and produced no behavioral change. MVP reduces blast radius to one
tool change, validates the delivery mechanism using real work, and defers the enforcement
gate until the mechanism is proven.

### 3.1. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| `context_loaded` storage | In-memory `ContextLoadedCache` | No external ground truth; `false` on cold start is semantically correct |
| Flag keyed by | Branch name (`str`) | Consistent with `PRStatusCache` per-branch model |
| `exempt_tools` scope | Action-level in `enforcement.yaml` | Chirurgical: applies only to `check_context_loaded`, not to `check_pr_status` |
| Bootstrap exemption | Gate inactive when `state.json` absent — domain rule, no tool names in code | If no state exists there is no phase to acknowledge; rule covers all tools in bootstrap state, including `initialize_project` |
| ISP split | `IContextLoadedReader` + `IContextLoadedWriter` (separate) | Writer injected into tools that set the flag; reader injected into enforcement only |
| `EnforcementAction.exempt_tools` validation | `model_validator` with `_EXEMPT_TOOLS_ALLOWED_TYPES` constant | Fail-Fast §4: detected at startup, not at call time |
| MVP content storage | Module-level dicts in `discovery_tools.py` with `# TODO(MVP)` | Explicit transitional; replaced by `contracts.yaml` on full implementation |
| `handover_template` MVP | Embedded in `phase_instructions` text for hand-over-producing roles | No separate field until Stage 2; avoids universal template that is wrong for non-implementer roles |
| `handover_template` Stage 2 | Separate `handover_template` field, per-phase from `contracts.yaml` | Role-specific; part of `PhaseInstructionsSpec` alongside `sub_role` and `phase_instructions` |
| `issue_number` sourcing | From `BranchState.issue_number` (not branch-name regex) | State is authoritative; regex is fragile and contradicts `BranchState` as SSOT |
| `parent_branch` in response | Inline from `BranchState.parent_branch` | Same data source as `get_parent_branch` tool; eliminates redundant call in ready phase; zero cost |
| Cycle indicator format | `cycle N` only — no `/M` total | Total cycle count is planning content owned by `get_project_plan`; non-overlap boundary (F_268.13) |
| `include_closed_recent` removal | Remove from `GetWorkContextInput` (breaking) | Dead parameter after field removal; no external consumers; clean break preferred |

---

## 4. Component Design

### 4.1. Stage 1 — MVP: GetWorkContextTool response extension

**File:** `mcp_server/tools/discovery_tools.py`

Two module-level lookup maps (transitional — marked `# TODO(MVP)`):

```python
# TODO(MVP): Replace with contracts.yaml instructions section on full implementation.
_SUB_ROLE_MAP: dict[str, str] = {
    "research": "researcher",
    "design": "designer",
    "planning": "planner",
    "implementation": "implementer",
    "validation": "validator",
    "documentation": "documenter",
    "ready": "documenter",
}

# TODO(MVP): Replace with contracts.yaml instructions section on full implementation.
# Keyed by (workflow_name, phase_name). phase_instructions embeds the hand-over format
# inline for roles that produce hand-overs (implementer, documenter). This avoids a
# universal handover_template field that would be incorrect for non-hand-over roles.
#
# TODO(Stage 2): Populate remaining (workflow, phase) pairs via contracts.yaml.
# Current production scope: all 7 bug phases + ("feature", "implementation").
# Additional workflows (refactor, docs, hotfix, feature non-implementation phases)
# are populated as contracts.yaml is implemented.
_PHASE_INSTRUCTIONS_MAP: dict[tuple[str, str], str] = { ... }  # see note below
```

> **C1 MAP CONTENT NOTE — F1 correction:**
> The `_PHASE_INSTRUCTIONS_MAP` in `discovery_tools.py` already contains **8 production entries**:
> all 7 bug phases (`research`, `design`, `planning`, `implementation`, `validation`,
> `documentation`, `ready`), each with a full TODO checklist and embedded hand-over format,
> plus `("feature", "implementation")` with the same structure.
>
> **C1 does not modify these entries.** The map content is retained as-is.
> Only the `execute()` function (how the map is looked up and how `BranchState` fields are
> sourced) changes in C1. An implementer must not replace the existing 8-entry map with a
> shorter or truncated version — doing so is a regression.

```python
# F_268.13 / MVP: orientation sourced from BranchState; lookup maps replaced by
# contracts.yaml on full implementation.  # TODO(MVP)
branch = self._git_manager.get_current_branch()
try:
    state = await anyio.to_thread.run_sync(self._state_engine.get_state, branch)
    workflow = state.workflow_name or "" if state is not None else ""
    phase = state.current_phase or "" if state is not None else ""
except Exception:  # noqa: BLE001 — bootstrap: branch not yet initialized
    # Graceful degradation: return orientation header with branch name only.
    # All map lookups produce "" → _format_context() shows "No instructions defined".
    workflow, phase = "", ""
    state = None

# Orientation fields — all from BranchState (already in memory, zero cost).
ctx["workflow_name"] = workflow
if state is not None:
    ctx["issue_number"] = state.issue_number        # renamed from linked_issue_number
    ctx["parent_branch"] = state.parent_branch or ""
    if state.current_cycle is not None:
        ctx["current_cycle"] = state.current_cycle  # position indicator only; no deliverables

# Noise fields intentionally omitted from ctx:
#   tdd_cycle_info, active_issue, recent_commits, recently_closed — not added per F_268.13.

# phase_source/phase_confidence: strip when confidence is "high" (healthy default).
if ctx.get("phase_confidence") == "high":
    ctx.pop("phase_source", None)
    ctx.pop("phase_confidence", None)

ctx["sub_role_hint"] = _SUB_ROLE_MAP.get(phase, "")
ctx["phase_instructions"] = _PHASE_INSTRUCTIONS_MAP.get((workflow, phase), "")
```

**`_format_context()` output structure (rewrite required):**

The existing `_format_context()` function must be rewritten to produce the following
structure. `phase_instructions` is the dominant first block — it is never buried at the
end.

```
Branch: `<branch>` | Workflow: <workflow> | Issue: #<issue_number>
Phase: <emoji> <phase>[ → <sub_phase>][ (cycle <N>)] | Role: <sub_role_hint>
[Parent: <parent_branch>]                              ← only if non-empty
[⚠️ Phase detection: source=<s>, confidence=<c>]      ← only if confidence ≠ high

---

### 🎯 Phase Instructions

<phase_instructions>
[(No instructions defined for workflow: X, phase: Y)]  ← if map returns ""
```

The ctx keys that drove the old renderer are either renamed (`linked_issue_number` →
`issue_number`) or removed entirely (`active_issue`, `tdd_cycle_info`, `recent_commits`,
`recently_closed`). The rewritten `_format_context()` must not reference removed keys.

**No constructor changes for MVP.** No `IContextLoadedWriter` injection yet.

**Architecture compliance:**
- DIP §1.5: no new instantiation in `execute()` — lookups are module-level constants; `BranchState` already fetched
- Config-First §3: intentionally violated — `# TODO(MVP)` marks the debt; instructions are per-phase text, not a shared SSOT claim
- CQS §5: no flag write in MVP; the side-effect is Stage 2
- C7 (`TODO(C7)`): closed — `workflow_name` rendered directly from `BranchState`; no `WorkflowStatusDTO` extension needed

---

### 4.2. Stage 2 — Full: IContextLoadedReader and IContextLoadedWriter interfaces

**File:** `mcp_server/core/interfaces/__init__.py`

Add alongside existing `IPRStatusReader` / `IPRStatusWriter`:

```python
@runtime_checkable
class IContextLoadedReader(Protocol):
    """Read the context-loaded flag for a branch."""

    def is_context_loaded(self, branch: str) -> bool:
        raise NotImplementedError


@runtime_checkable
class IContextLoadedWriter(Protocol):
    """Write the context-loaded flag for a branch."""

    def set_context_loaded(self, branch: str, *, value: bool) -> None:
        raise NotImplementedError
```

**Architecture compliance:**
- ISP §1.4: reader and writer are separate protocols — no consumer receives both unless justified
- Law of Demeter §7: tool layer interacts only with `IContextLoadedWriter`, not with cache internals

---

### 4.3. Stage 2 — Full: ContextLoadedCache

**File:** `mcp_server/state/context_loaded_cache.py` (new)

```python
"""In-memory context-loaded flag cache. Session-scope, no persistence.

@layer: Backend (State)
@dependencies: [mcp_server.core.interfaces]
@responsibilities:
    - Store context_loaded flag per branch for the current MCP session
    - Default false on cold start (no external ground truth exists)
"""

from __future__ import annotations

from mcp_server.core.interfaces import IContextLoadedReader, IContextLoadedWriter


class ContextLoadedCache(IContextLoadedReader, IContextLoadedWriter):
    """Session-scope in-memory flag store for context-loaded state per branch.

    Lifecycle:
    - cold start / phase entry / cycle entry / git_checkout → false (default)
    - non-noop git_pull → false (new commits received, context stale)
    - get_work_context (success) → true
    """

    def __init__(self) -> None:
        self._cache: dict[str, bool] = {}

    def is_context_loaded(self, branch: str) -> bool:
        """Return flag for branch; defaults to False on first access."""
        return self._cache.get(branch, False)

    def set_context_loaded(self, branch: str, *, value: bool) -> None:
        """Set flag for branch."""
        self._cache[branch] = value
```

**Architecture compliance:**
- SRP §1.1: only stores/returns the boolean flag; no business logic
- No import-time side effects §12: pure in-memory object; no file reads in `__init__`
- No `ClassVar` singleton — instantiated at `server.py` composition root (§12, §11)

---

### 4.4. Stage 2 — Full: EnforcementAction schema change

**File:** `mcp_server/config/schemas/enforcement_config.py`

Add to `EnforcementAction`:

```python
# Allowlist of action types that support the exempt_tools field.
# Update this constant when a new action type needs exemption support.
_EXEMPT_TOOLS_ALLOWED_TYPES: frozenset[str] = frozenset({"check_context_loaded"})


class EnforcementAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    policy: str | None = None
    rules: dict[str, list[str]] = Field(default_factory=dict)
    path: str | None = None
    message: str | None = None
    enabled: bool = True                                      # new field
    exempt_tools: list[str] = Field(default_factory=list)    # new field

    @model_validator(mode="after")
    def validate_required_fields(self) -> EnforcementAction:
        if self.type == "check_branch_policy" and not self.rules:
            raise ValueError("check_branch_policy requires non-empty rules")
        if self.type == "delete_file" and not self.path:
            raise ValueError("delete_file requires path")
        if self.exempt_tools and self.type not in _EXEMPT_TOOLS_ALLOWED_TYPES:
            raise ValueError(
                f"exempt_tools is not supported for action type '{self.type}'. "
                f"Supported types: {sorted(_EXEMPT_TOOLS_ALLOWED_TYPES)}"
            )
        return self
```

**Architecture compliance:**
- Fail-Fast §4: `model_validator` rejects invalid `exempt_tools` at parse time (server startup)
- OCP §1.2: `_EXEMPT_TOOLS_ALLOWED_TYPES` is the extension point — add new types there, no if-chain change
- Config-First §3: the allowed-types constant is the SSOT for which action types support exemption

---

### 4.5. Stage 2 — Full: EnforcementRunner extension

**File:** `mcp_server/managers/enforcement_runner.py`

**Constructor change:**
```python
def __init__(
    self,
    workspace_root: Path,
    config: EnforcementConfig,
    registry: EnforcementRegistry | dict[str, ActionHandler] | None = None,
    default_base_branch: str = "main",
    pr_status_reader: IPRStatusReader | None = None,
    context_loaded_reader: IContextLoadedReader | None = None,  # new
    server_root: Path | None = None,
) -> None:
    ...
    self._context_loaded_reader = context_loaded_reader  # new
```

**Registry registration in `_build_default_registry()`:**
```python
registry.register("check_context_loaded", self._handle_check_context_loaded)
```

**New handler:**
```python
def _handle_check_context_loaded(
    self,
    action: EnforcementAction,
    context: EnforcementContext,
    workspace_root: Path,
    note_context: NoteContext,
    """Block write-tools until get_work_context has been called this session.

    Gate is explicitly disabled when action.enabled=False (explicit over implicit:
    disabling requires a deliberate YAML config decision, never an absent dependency).
    Raises ConfigError when action.enabled=True but reader is not injected — this is a
    composition-root wiring error that must fail loudly at call time.
    Gate is inactive when state.json does not exist — bootstrap state; no phase
    exists to acknowledge. This is a domain rule covering all tools, not a
    tool-name exemption.
    Exempt tools listed in action.exempt_tools bypass the gate regardless.
    """
    del workspace_root  # unused; runner has self.server_root
    if not action.enabled:
        return  # gate explicitly disabled via YAML

    if self._context_loaded_reader is None:
        raise ConfigError(
            "check_context_loaded action requires context_loaded_reader; "
            "wire ContextLoadedCache in EnforcementRunner.__init__",
            file_path=_ENFORCEMENT_DISPLAY_PATH,
        )

    # Domain rule: no state.json means bootstrap — gate is semantically inactive.
    # This covers initialize_project and any other tool called before state exists.
    if not (self.server_root / "state.json").exists():
        return

    # Exempt tools bypass the gate entirely (e.g. force_phase_transition).
    if context.tool_name in action.exempt_tools:
        return

    branch = _get_current_git_branch(self.workspace_root)
    if branch is None:
        return  # detached HEAD or git error — gate cannot determine branch

    if not self._context_loaded_reader.is_context_loaded(branch):
        raise ValidationError(
            "Context not loaded. Call 'get_work_context' before using write tools.",
        )
```

**Bootstrap domain rule — no Config-First §3 violation:** the `state.json` existence
check is a domain predicate ("is there a workflow state to acknowledge?"), not a tool-name
check. It applies uniformly to all tools — no tool name appears in Python code. The
`exempt_tools` YAML list handles static per-tool exemptions; the bootstrap check handles
the dynamic state-conditional case.

**`KNOWN_TOOL_CATEGORIES` update:** no change needed — `check_context_loaded` matches on
`tool_category: branch_mutating`, which is already in the frozenset. The category is not
a new category; the action type is new.

**Architecture compliance:**
- DIP §1.5: `IContextLoadedReader` injected via constructor; no direct `ContextLoadedCache` import
- ISP §1.4: `EnforcementRunner` receives read-only `IContextLoadedReader` — cannot write the flag
- SRP §1.1: handler is one method with one responsibility (block or pass)
- OCP §1.2: new handler registered via registry, no modification to `run()` or existing handlers
- Config-First §3: no tool names hardcoded in Python; bootstrap check is a domain predicate
- Fail-Fast §4: `_validate_registered_actions()` already validates action types at startup

---

### 4.6. Stage 2 — Full: GetWorkContextTool constructor change (flag writer)

**File:** `mcp_server/tools/discovery_tools.py`

Add to `GetWorkContextTool.__init__`:
```python
context_loaded_writer: IContextLoadedWriter | None = None,  # new
```
Store as `self._context_loaded_writer`.

At the end of `execute()`, after building `ctx` and before `return`:
```python
# Set context_loaded flag — command side-effect of context delivery.
if self._context_loaded_writer is not None:
    branch = self._git_manager.get_current_branch()
    if branch:
        self._context_loaded_writer.set_context_loaded(branch, value=True)
```

Stage 2 also replaces the two `# TODO(MVP)` lookup maps with reads from the injected
`ContractsConfig`. The response gains a third field `handover_template` read from
`contracts.yaml` (see §4.10).

**Architecture compliance:**
- ISP §1.4: tool receives `IContextLoadedWriter` (write-only); cannot read the flag
- CQS §5: the flag write is documented as an accepted command-with-result at the tool boundary
- DIP §1.5: injected via constructor, not instantiated in `execute()`

---

### 4.7. Stage 2 — Full: PhaseStateEngine reset injection

**File:** `mcp_server/managers/phase_state_engine.py`

Add constructor parameter:
```python
context_loaded_writer: IContextLoadedWriter | None = None,  # new
```
Store as `self._context_loaded_writer`.

Add private reset helper:
```python
def _reset_context_loaded(self, branch: str) -> None:
    """Signal the context_loaded cache that phase/cycle context is stale."""
    if self._context_loaded_writer is not None:
        self._context_loaded_writer.set_context_loaded(branch, value=False)
```

Call `self._reset_context_loaded(branch)` in:
- `transition()` — after `_apply_state()` on phase write
- `force_transition()` — after `_apply_state()` on forced phase write
- `enter_cycle()` — after `_apply_state()` on cycle entry
- `force_enter_cycle()` — after `_apply_state()` on forced cycle entry

**Not in `initialize_branch()`:** the bootstrap domain rule in the gate handler covers
the pre-state case. Calling reset on init would set `false` on a branch with no state,
which is harmless but unnecessary.

**Architecture compliance:**
- SRP §1.1: `PhaseStateEngine` signals state-write events; it does not own the cache
- ISP §1.4: `PhaseStateEngine` receives `IContextLoadedWriter` (write-only)
- DIP §1.5: writer injected via constructor

---

### 4.8. Stage 2 — Full: GitCheckoutTool and GitPullTool

**File:** `mcp_server/tools/git_tools.py` (GitCheckoutTool)

Add `context_loaded_writer: IContextLoadedWriter | None = None` to `__init__`.
After successful checkout: `self._context_loaded_writer.set_context_loaded(new_branch, value=False)`.

**File:** `mcp_server/tools/git_pull_tool.py` (GitPullTool)

Add `context_loaded_writer: IContextLoadedWriter | None = None` to `__init__`.
After a non-noop pull (commits received): `self._context_loaded_writer.set_context_loaded(branch, value=False)`.
On noop pull ("Already up to date"): no reset.

**Architecture compliance:**
- DIP §1.5: injected via constructor
- ISP §1.4: write-only interface; tools cannot read current flag state

---

### 4.9. Stage 2 — Full: enforcement.yaml new rule

```yaml
  - event_source: tool
    tool_category: branch_mutating
    timing: pre
    actions:
      - type: check_context_loaded
        exempt_tools:
          - force_phase_transition
          - force_cycle_transition
```

This rule fires for all `branch_mutating` tools on `pre` event. The handler applies the
bootstrap domain rule first (inactive pre-state), then `action.exempt_tools` for static
per-tool exemptions.

**Why `branch_mutating` and not a new category:** force tools are `BranchMutatingTool`
subclasses by design — they mutate state and must be blocked by `check_pr_status`. Adding
a separate `context_gated` category would require subclassing from two ABCs or losing the
PR-status blocking on force tools. Using `exempt_tools` on the existing `branch_mutating`
category is the correct chirurgical mechanism.

**Architecture compliance:**
- Config-First §3: exemptions live in config; bootstrap is a domain predicate, not a tool-name entry
- OCP §1.2: adding a new exempt tool is a config change, not a code change
- Fail-Fast §4: `EnforcementAction` model_validator rejects unknown types at startup

---

### 4.10. Stage 2 — Full: contracts.yaml instructions section

Each workflow+phase entry gains a sibling `instructions` section alongside `exit_requires`:

```yaml
workflows:
  feature:
    phases:
      - name: implementation
        cycle_based: true
        subphases: [red, green, refactor]
        commit_type_map:
          red: test
          green: feat
          refactor: refactor
        exit_requires: [...]
        instructions:
          sub_role: implementer
          phase_instructions: |
            1. Call get_project_plan to read TDD cycle deliverables.
            2. Follow RED→GREEN→REFACTOR strictly.
            ...
          handover_template: |
            ### Scope
            - what cycle or task was executed
            - what was intentionally kept out of scope

            ### Files
            - changed files grouped by role

            ### Deliverables
            - which authoritative deliverables are now satisfied

            ### Stop-Go Proof
            - exact tests run
            - exact gate commands or MCP checks run
            - exact outcome
```

**`PhaseInstructionsSpec` Pydantic model** (new, in `mcp_server/config/schemas/contracts_config.py`):

```python
class PhaseInstructionsSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    sub_role: str
    phase_instructions: str
    handover_template: str | None = None
```

**Phase entry gains required field:**
```python
instructions: PhaseInstructionsSpec
```

**Instructions are required for every phase entry (explicit over implicit):** a phase
defined in `contracts.yaml` without an `instructions` block is an incomplete definition.
The Pydantic schema enforces this at parse time (Fail-Fast §4): startup fails immediately
if any phase entry is missing `instructions`. No separate post-load validator is needed —
Pydantic's own required-field enforcement is the SSOT. `contracts.yaml` must be fully
authored for all workflows × phases before the schema change can be activated.

**`handover_template` is role-specific by construction:** each phase entry defines its
own `handover_template` text. An `@imp implementer` entry has the Imp→QA format; an
`@imp researcher` entry has the Co→Imp format. No universal template — no SSOT drift
between AGENTS.md and the tool response.

---

## 5. Sequence Diagrams

### 5.1. MVP: agent startup with phase_instructions delivery

```
@imp session start (validation harness — bug/330 branch in research phase)
  → get_work_context()
    → GetWorkContextTool.execute()
      → get_state(branch) → state: workflow_name="bug", current_phase="research",
                                    issue_number=330, parent_branch="main"
      → lookup _SUB_ROLE_MAP["research"] → "researcher"
      → lookup _PHASE_INSTRUCTIONS_MAP[("bug","research")]
          → instructions string: read bug report, inspect files, write research.md, handover
      → ctx built: workflow_name, issue_number, parent_branch, sub_role_hint, phase_instructions
      → return ToolResult with orientation header + 🎯 Phase Instructions block
  → agent reads phase_instructions as dominant first block
  → agent follows prescribed tool order (hypothesis validation)
  → agent produces hand-over using format embedded in phase_instructions
```

### 5.2. Stage 2: context_loaded gate enforcement

```
@imp session start (cold)
  → get_work_context()
    → execute() sets context_loaded_writer.set_context_loaded(branch, value=True)
    → returns context with sub_role_hint, phase_instructions, handover_template
  → git_add_or_commit()
    → EnforcementRunner.run("git_add_or_commit", "pre", ...)
      → rule matches: tool_category=branch_mutating, timing=pre, action=check_context_loaded
      → _handle_check_context_loaded():
          state.json exists → continue
          "git_add_or_commit" not in exempt_tools → continue
          context_loaded_reader.is_context_loaded(branch) → True → pass
    → commit proceeds normally

@imp session start (cold) WITHOUT get_work_context first
  → git_add_or_commit()
    → EnforcementRunner.run(...)
      → _handle_check_context_loaded():
          state.json exists → continue
          not in exempt_tools → continue
          is_context_loaded(branch) → False → raise ValidationError
    → tool blocked with error message

initialize_project on fresh branch (no state.json yet)
  → EnforcementRunner.run("initialize_project", "pre", ...)
    → _handle_check_context_loaded():
        state.json does NOT exist → return (gate inactive)
    → initialize_project proceeds normally
```

### 5.3. Stage 2: force tool exempt path

```
→ force_phase_transition()
  → EnforcementRunner.run("force_phase_transition", "pre", ...)
    → rule matches: tool_category=branch_mutating, action=check_context_loaded
    → _handle_check_context_loaded():
        state.json exists → continue
        "force_phase_transition" in action.exempt_tools → True → return (pass)
    → force transition proceeds

→ PhaseStateEngine.force_transition() writes new state
  → _reset_context_loaded(branch) → set_context_loaded(branch, value=False)
→ next write-tool call is blocked until get_work_context called again
```

---

## 6. Blast Radius Summary

| File | Change | Stage |
|------|--------|-------|
| `mcp_server/tools/discovery_tools.py` | C1: full `execute()` restructuring — `BranchState`-first sourcing with graceful bootstrap fallback, noise field removal (`active_issue`, `recent_commits`, `tdd_cycle_info`, `recently_closed`), conditional `phase_source`/`phase_confidence` stripping; `_format_context()` complete rewrite (orientation header + dominant `### 🎯 Phase Instructions` block); `GetWorkContextInput.include_closed_recent` parameter removed (breaking); 3 new orientation fields (`workflow_name`, `issue_number`, `parent_branch`) | MVP |
| `mcp_server/core/interfaces/__init__.py` | Add `IContextLoadedReader`, `IContextLoadedWriter` | Stage 2 |
| `mcp_server/state/context_loaded_cache.py` | New file: in-memory flag cache | Stage 2 |
| `mcp_server/config/schemas/enforcement_config.py` | Add `exempt_tools` field + model_validator | Stage 2 |
| `mcp_server/managers/enforcement_runner.py` | Add `context_loaded_reader` param + handler + registration | Stage 2 |
| `mcp_server/tools/discovery_tools.py` | Add `context_loaded_writer` param + flag write + `handover_template` from config | Stage 2 |
| `mcp_server/managers/phase_state_engine.py` | Add `context_loaded_writer` param + `_reset_context_loaded()` | Stage 2 |
| `mcp_server/tools/git_tools.py` | Add `context_loaded_writer` + reset on checkout | Stage 2 |
| `mcp_server/tools/git_pull_tool.py` | Add `context_loaded_writer` + conditional reset | Stage 2 |
| `.phase-gate/config/enforcement.yaml` | Add `check_context_loaded` rule | Stage 2 |
| `.phase-gate/config/contracts.yaml` | Add `instructions` section (sub_role, phase_instructions, handover_template) per workflow+phase | Stage 2 |
| `mcp_server/config/schemas/contracts_config.py` | Add `PhaseInstructionsSpec` + `instructions` field per phase entry | Stage 2 |
| `mcp_server/server.py` | Instantiate `ContextLoadedCache`; inject into tools + managers | Stage 2 |

**Test blast radius:**

| File | Change | Stage |
|------|--------|-------|
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | Extend `TestGetWorkContextTool`: orientation fields present (`workflow_name`, `issue_number`, `parent_branch`); noise fields absent (`active_issue`, `recent_commits`, `tdd_cycle_info`); `phase_instructions` as dominant first block in output; `include_closed_recent` parameter removed; bootstrap/no-state graceful degradation (no crash, empty instructions); empty-string fallback for uncovered `(workflow, phase)` — no `KeyError`; Stage 2: writer side-effect | MVP + Stage 2 |
| `tests/mcp_server/unit/state/test_context_loaded_cache.py` | New file: default false, set/reset, branch independence | Stage 2 |
| `tests/mcp_server/integration/test_pr_status_lockdown.py` | Verify force tools STILL inherit `BranchMutatingTool` | Stage 2 |
| `tests/mcp_server/unit/tools/test_git_tools.py` | Add checkout reset test | Stage 2 |
| `tests/mcp_server/unit/tools/test_git_pull_tool.py` | Add noop/non-noop pull reset tests | Stage 2 |
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | Add reset signal tests on phase/cycle entry | Stage 2 |
| `tests/mcp_server/integration/test_context_loaded_enforcement.py` | New integration test: gate blocks/unblocks; bootstrap domain rule (no state.json → all tools pass) | Stage 2 |

---

## 7. Open Design Questions

All research open questions are resolved (see research.md). No design-phase questions remain.

The following items are explicitly deferred and must not be pulled into implementation scope:

| Item | Status |
|------|--------|
| `create_handover` tool + SubRoleSpec YAML | Deferred — separate issue (OQ 6) |
| Full `contracts.yaml` `instructions` authorship (all workflows × phases) | Deferred — Stage 2, after MVP validation |
| `close-issue.prompt.md` creation | Deferred — separate issue |
| `AGENTS.md` `@co` role definition update | Deferred — separate issue or documentation phase |
| `initialize_project` guard bug | Separate issue — MVP validation harness (F_268.10/F_268.11) |

---

## Related Documentation

- [research.md](research.md) — Findings F_268.1–F_268.13, all open questions resolved
- [ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- Issue #268 — MCP-tool-first orchestration
- Issue #263 — hook injection research (context for why MVP-first approach)
- `mcp_server/tools/base.py` — `BranchMutatingTool` pattern
- `mcp_server/state/pr_status_cache.py` — structural model for `ContextLoadedCache`
- `mcp_server/core/interfaces/__init__.py` — `IPRStatusReader`/`IPRStatusWriter` structural model
- `mcp_server/managers/enforcement_runner.py` — `_handle_check_pr_status` structural model
- `.phase-gate/config/enforcement.yaml` — existing gate registrations
