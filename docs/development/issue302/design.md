# Design: Align labels config, GitHub labels, and docs (Issue #302)

**Status:** FINAL
**Version:** 1.1
**Phase:** Design
**Issue:** #302
**Branch:** fix/302-align-labels-config-github-docs

---

## 1. Design Goals

1. `AddLabelsTool` must accept labels matching `label_patterns` (e.g., `parent:302`).
2. `DetectLabelDriftTool` must not report pattern-matching GitHub labels as false-positive drift.
3. All doc references to `status:*` labels must be replaced with valid labels from the current taxonomy.
4. `workphases.yaml` must be the sole SSOT for valid `phase:*` label suffixes; `labels.yaml` must not maintain a parallel list of phase names.

All changes must comply with ARCHITECTURE_PRINCIPLES.md.

---

## 2. Design Decisions

### Decision 1 — Fix AddLabelsTool (Sub-problem A)

**File:** `mcp_server/tools/label_tools.py`

**Change:** In `AddLabelsTool.execute()`, replace the `label_exists()` call with
`validate_label_name()` (which already correctly handles freeform exceptions, exact labels,
and label patterns).

Before:
```python
undefined = [label for label in params.labels
             if not self._label_config.label_exists(label)]
if undefined:
    return ToolResult.text(f"❌ Labels not defined in labels.yaml: {undefined}")
```

After:
```python
invalid = [label for label in params.labels
           if not self._label_config.validate_label_name(label)[0]]
if invalid:
    return ToolResult.text(f"❌ Labels not valid per labels.yaml: {invalid}")
```

**Architecture alignment:**
- §2 DRY+SSOT: delegates to the single authoritative validator already used by `CreateLabelTool`
- §9 YAGNI: reuses existing method, no new abstractions
- §11 DI: uses already-injected `_label_config`
- §1.1 SRP: `AddLabelsTool` responsibility unchanged — validate + add

**Variable rename:** `undefined` → `invalid` to match the updated semantics (a label can be
valid-per-pattern but not "defined" as a static entry).

### Decision 2 — Fix DetectLabelDriftTool (Sub-problem B)

**File:** `mcp_server/tools/label_tools.py`

**Change:** In `DetectLabelDriftTool.execute()`, filter the `github_only` list to exclude
labels that match a `label_pattern`.

Before:
```python
github_only = [name for name in github_by_name if name not in yaml_by_name]
```

After:
```python
github_only = [
    name for name in github_by_name
    if name not in yaml_by_name
    and not self._label_config.validate_label_name(name)[0]
]
```

**Architecture alignment:**
- §2 DRY+SSOT: uses the same `validate_label_name()` method — single validation path
- §9 YAGNI: no new method; existing method already handles all cases
- §5 CQS: `validate_label_name()` is a pure query — no side effects

**Important note:** `validate_label_name()` returns `(True, "")` for both explicit static
labels AND for pattern-matching labels. This means the filter expression is semantically
correct: "exclude from drift if the name is valid per the SSOT's taxonomy".

However, there is a known limitation: `validate_label_name()` has a fallback regex that
accepts any `category:value` where category is one of a hardcoded list including `type`,
`priority`, `status`, `phase`, `scope`, `component`, `effort`, `parent`. This means a stale
GitHub label like `effort:high` or `component:auth` would pass `validate_label_name()` and
be excluded from drift reports even if not in labels.yaml. This is a **new false-negative
class introduced by this fix** (not a pre-existing problem) — though the practical impact
today is zero because only `parent:NNN` is actively used. The full resolution of this
fallback regex behaviour is out of scope for #302.

**Note — interaction with Decision 4 (sub-problem D):** For the `phase:*` category
specifically, the fallback regex in `validate_label_name()` passes *any* `phase:X` label
through the format check. This means `phase:unicorn` would pass `validate_label_name()` in
`AddLabelsTool` and reach the `validate_phase_label()` check (Decision 4), which then
correctly rejects it. Decisions A and D together fully mitigate the fallback for `phase:*`;
the remaining false-negative classes (`effort:*`, `component:*`, `status:*`) are deferred.

### Decision 3 — Fix documentation (Sub-problem C)

#### 3a. `docs/mcp_server/GITHUB_SETUP.md`

Remove §4.4 entirely. The section is titled "Status" and contains only the three stale
`status:*` labels plus two unrelated `scope:*` labels. Replacement: a note that status
tracking uses GitHub issue state (`open`/`closed`) combined with `phase:*` labels.

The `needs:discussion` and `scope:*` entries in §4.4 are also not in `labels.yaml` and
will be removed with the section.

**Exact change (lines 115–123):**

Before:
```markdown
### 4.4 Status (`#FBCA04` - Yellow)
Automated bot triggers or blocked states.

- `status:blocked`: Cannot proceed (needs `blocked-by` comment)
- `status:needs-info`: Waiting on user input
- `status:ready-for-review`: PR open and checks passed
- `needs:discussion`: Requires team input
- `scope:architecture`: Affects system design
- `scope:component`: Affects single component
```

After:
```markdown
### 4.4 Status

Status tracking uses GitHub issue state (`open`/`closed`) combined with `phase:*` labels
(see §4.3). There are no separate `status:*` labels — this category was removed in issue #149.
```

#### 3b. `docs/reference/mcp/tools/github.md`

Replace all `status:*` label occurrences with valid alternatives from the current taxonomy.

| Location | Current | Replacement |
|----------|---------|-------------|
| Line 270 (update_issue response) | `"status:resolved"` | `"phase:documentation"` |
| Line 292 (update_issue example) | `"status:resolved", "phase:done"` | `"phase:documentation"` (dedup + fix: `phase:done` does not exist) |
| Line 793 (add_labels example) | `"priority:high", "status:in-progress"` | `"priority:high", "phase:implementation"` |
| Line 826 (add_labels example) | `"status:in-progress"` | `"phase:implementation"` |
| Line 835 (add_labels example) | `"status:in-progress"` | `"phase:implementation"` |
| Lines 1062–1067 (Configuration section YAML) | Fabricated `label_config.patterns` with `status:(backlog|in-progress|review|done)` | Replace entire snippet with accurate summary of actual labels.yaml structure |

---

### Decision 4 — Fix SSOT violation: replace explicit phase:* entries with dynamic pattern + use-time validation (Sub-problem D)

#### 4a. `.st3/config/labels.yaml` restructure

Remove the 9 explicit `phase:*` label entries. Add one dynamic `label_pattern` that covers
all current and future top-level workphases at format level.

Before (excerpt):
```yaml
  - name: "phase:research"
    color: "C5DEF5"
    description: "Research/discovery phase"
  # ... 8 more explicit entries ...
  - name: "phase:documentation"
    color: "0075CA"
    description: "Documentation phase"
```

After (new entry in `label_patterns`):
```yaml
label_patterns:
  - pattern: "^parent:\\d+$"
    description: "Parent issue reference for child issues"
    color: "EDEDED"
    example: "parent:91"
  - pattern: "^phase:[a-z][a-z0-9-]*$"
    description: "Workflow phase label — valid suffixes derived from workphases.yaml at use-time"
    color: "C5DEF5"
    example: "phase:research"
```

**Architecture alignment:**
- §2 DRY+SSOT: `workphases.yaml` becomes the single source of phase names; `labels.yaml` expresses only format, not semantics
- §9 YAGNI: one pattern replaces 9 static entries; no information is lost

#### 4b. `mcp_server/config/schemas/label_config.py` — new `validate_phase_label()` function

New module-level function (not a method on `LabelConfig` — avoids coupling two config value
objects per §7 LoD):

**F-3 fix:** The correct import path is `from mcp_server.config.schemas.workphases import WorkphasesConfig` (no top-level `mcp_server.schemas` module exists — verified via scope_encoder.py line 19).

```python
from __future__ import annotations

from mcp_server.config.schemas.workphases import WorkphasesConfig


def validate_phase_label(name: str, workphases: WorkphasesConfig) -> tuple[bool, str]:
    """Validate that a phase:* label's suffix is a known top-level workphase.

    Only top-level phase keys are valid issue labels. Subphases (e.g., 'red',
    'green', 'contracts', 'e2e') are commit-level granularity and must not be used.

    Args:
        name: The full label name (e.g., "phase:implementation").
        workphases: Loaded WorkphasesConfig — the SSOT for valid phase names.

    Returns:
        (True, "") if valid or not a phase:* label.
        (False, error_message) if the suffix is not a known top-level workphase.
    """
    if not name.startswith("phase:"):
        return (True, "")
    suffix = name.removeprefix("phase:")
    valid_phases = set(workphases.phases.keys())
    if suffix not in valid_phases:
        return (
            False,
            f"Label '{name}' references unknown workphase '{suffix}'. "
            f"Valid phases: {sorted(valid_phases)}",
        )
    return (True, "")
```

**Architecture alignment:**
- §1.1 SRP: `LabelConfig` remains unchanged — format validation only
- §7 LoD: free function takes both config objects as parameters — no cross-dependency between value objects
- §5 CQS: pure query function, no side effects

#### 4c. `mcp_server/tools/label_tools.py` — two-step phase validation in tools

Both `AddLabelsTool` and `CreateLabelTool` gain a **required** `workphases_config: WorkphasesConfig`
constructor parameter and call `validate_phase_label()` after `validate_label_name()` passes.

**Parameter requirement decision:** The parameter is **required** (not `Optional`).
An optional parameter with `default=None` that silently skips the phase check would make it
impossible to detect unguarded construction sites — defeating the purpose of sub-problem D.
All construction sites must be updated (see blast radius below).

**Full construction site audit — files requiring update in C_302.3 GREEN:**

| File | Tool | Sites | Lines |
|------|------|-------|-------|
| `mcp_server/server.py` | `AddLabelsTool` | 1 | L411 |
| `mcp_server/server.py` | `CreateLabelTool` | 1 | L413 |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | `AddLabelsTool` | 4 | L141, 162, 180, 202 |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | `CreateLabelTool` | 4 | L60, 76, 97, 121 |
| `tests/mcp_server/unit/tools/test_label_tools.py` | `AddLabelsTool` | 1 | L105 |
| `tests/mcp_server/unit/tools/test_label_tools.py` | `CreateLabelTool` | 1 | L74 |
| `tests/mcp_server/unit/tools/test_github_extras.py` | `AddLabelsTool` | 1 | L58 |
| `tests/mcp_server/unit/integration/test_all_tools.py` | `AddLabelsTool` | 1 | L203 (via `make_add_labels_tool`) |

**Total: 14 sites across 5 files.** A shared `workphases_config` fixture (backed by
`.st3/config/workphases.yaml`) will be added to conftest / test helper to avoid repetition.

`server.py` already loads `workphases_config` at L169
(`workphases_config = config_loader.load_workphases_config()`). The two tool instantiations
at L411/L413 need only add `workphases_config=workphases_config` as a keyword argument.

**`AddLabelsTool` change:**

After the existing `validate_label_name()` check, add:
```python
from mcp_server.config.schemas.label_config import validate_phase_label

# Step 2: semantic phase check (after format check passes)
phase_errors = [
    f"{label}: {validate_phase_label(label, self._workphases_config)[1]}"
    for label in params.labels
    if label.startswith("phase:") and not validate_phase_label(label, self._workphases_config)[0]
]
if phase_errors:
    return ToolResult.text(f"❌ Labels reference unknown workphase: {phase_errors}")
```

**`CreateLabelTool` change:**

After the existing `validate_label_name()` check, add:
```python
is_valid_phase, phase_error = validate_phase_label(params.name, self._workphases_config)
if not is_valid_phase:
    return ToolResult.text(f"❌ {phase_error}")
```

**Architecture alignment:**
- §11 DI: `workphases_config` injected at construction time — no runtime config loading
- §2 DRY: single `validate_phase_label()` call site per tool — no duplicated logic
- §1.1 SRP: tool responsibility unchanged — validate then act

#### 4d. GitHub label cleanup (one-time runtime operation)

Performed as part of the implementation cycle using existing `create_label` / `delete_label`
MCP tools. Not a code change — a data migration.

| Operation | Labels |
|-----------|--------|
| Delete (stale/invalid) | `phase:integration`, `phase:tdd`, `phase:red`, `phase:green`, `phase:refactor` |
| Create (missing) | `phase:implementation`, `phase:validation`, `phase:coordination`, `phase:ready` |

All created labels use color `C5DEF5` (uniform for all `phase:*` labels).

---

## 3. TDD Cycle Plan

### Cycle C_302.1 — AddLabelsTool accepts dynamic pattern labels (Sub-problem A)

**Phase RED:**
Add to `tests/mcp_server/unit/tools/test_label_tools_integration.py`,
class `TestAddLabelsToolValidation`:

```python
@pytest.mark.asyncio
async def test_add_labels_accepts_dynamic_pattern_label(self, tmp_path: Path) -> None:
    """AddLabelsTool accepts labels matching label_patterns (e.g. parent:NNN)."""
    yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^parent:\\\\d+$"
    description: "Parent issue reference"
    color: "EDEDED"
    example: "parent:91"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
    label_config = _load_label_config(tmp_path, yaml_content)
    mock_manager = Mock()
    tool = AddLabelsTool(manager=mock_manager, label_config=label_config)
    params = AddLabelsInput(issue_number=1, labels=["parent:302"])

    result = await tool.execute(params, NoteContext())

    assert "Added labels" in result.content[0]["text"]
    mock_manager.add_labels.assert_called_once_with(1, ["parent:302"])
```

This test FAILS (RED) because the current code uses `label_exists()` which returns False
for `parent:302`.

**Phase GREEN:** Apply Decision 1 fix. Also update the two existing assertions in
`tests/mcp_server/unit/tools/test_label_tools_integration.py`:
- Line 146 (`test_add_labels_validates_existence`): `"not defined in labels.yaml"` → `"not valid per labels.yaml"`
- Line 184 (`test_add_labels_partial_invalid_rejects_all`): same update

**Phase REFACTOR:** None required (change is minimal).

---

### Cycle C_302.2 — DetectLabelDriftTool ignores pattern-matching labels (Sub-problem B)

**Phase RED:**
Add to `tests/mcp_server/unit/tools/test_label_tools_integration.py`,
class `TestDetectLabelDriftTool`:

```python
@pytest.mark.asyncio
async def test_drift_detection_pattern_labels_not_reported_as_drift(
    self, tmp_path: Path
) -> None:
    """DetectLabelDriftTool does not report pattern-matching GitHub labels as drift."""
    yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^parent:\\\\d+$"
    description: "Parent issue reference"
    color: "EDEDED"
    example: "parent:91"
labels:
  - name: "type:feature"
    color: "1D76DB"
    description: "Test"
"""
    label_config = _load_label_config(tmp_path, yaml_content)
    mock_manager = Mock()
    mock_manager.list_labels = Mock(
        return_value=[
            _MockLabel(name="type:feature", color="1D76DB", description="Test"),
            _MockLabel(name="parent:302", color="EDEDED", description=""),
        ]
    )

    tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
    params = DetectLabelDriftInput()

    result = await tool.execute(params, NoteContext())

    result_text = result.content[0]["text"]
    assert "no drift detected" in result_text.lower()
```

This test FAILS (RED) because `parent:302` is listed in `github_only` and drift is reported.

**Phase GREEN:** Apply Decision 2 fix.

**Phase REFACTOR:** None required.

---

### Cycle C_302.3 — validate_phase_label() + labels.yaml restructure (Sub-problem D)

**Phase RED:**
Add to `tests/mcp_server/unit/tools/test_label_tools_integration.py`:

```python
# ─── validate_phase_label() unit tests ────────────────────────────────────────

class TestValidatePhaseLabelFunction:
    """Unit tests for the validate_phase_label() free function."""

    def test_non_phase_label_is_always_valid(self, workphases_config: WorkphasesConfig) -> None:
        from mcp_server.config.schemas.label_config import validate_phase_label
        is_valid, _ = validate_phase_label("type:feature", workphases_config)
        assert is_valid

    def test_known_phase_is_valid(self, workphases_config: WorkphasesConfig) -> None:
        from mcp_server.config.schemas.label_config import validate_phase_label
        is_valid, msg = validate_phase_label("phase:implementation", workphases_config)
        assert is_valid
        assert msg == ""

    def test_unknown_phase_is_invalid(self, workphases_config: WorkphasesConfig) -> None:
        from mcp_server.config.schemas.label_config import validate_phase_label
        is_valid, msg = validate_phase_label("phase:unicorn", workphases_config)
        assert not is_valid
        assert "unicorn" in msg
        assert "Valid phases" in msg

    def test_subphase_is_invalid(self, workphases_config: WorkphasesConfig) -> None:
        """Subphases like 'red', 'green', 'refactor' are not valid issue labels."""
        from mcp_server.config.schemas.label_config import validate_phase_label
        is_valid, msg = validate_phase_label("phase:red", workphases_config)
        assert not is_valid
        assert "red" in msg

    def test_stale_integration_phase_is_invalid(self, workphases_config: WorkphasesConfig) -> None:
        from mcp_server.config.schemas.label_config import validate_phase_label
        is_valid, msg = validate_phase_label("phase:integration", workphases_config)
        assert not is_valid


# ─── AddLabelsTool phase:* semantic check ─────────────────────────────────────

class TestAddLabelsToolPhaseValidation:
    """AddLabelsTool rejects phase:* labels for unknown workphases."""

    @pytest.mark.asyncio
    async def test_add_labels_rejects_unknown_phase(
        self, tmp_path: Path, workphases_config: WorkphasesConfig
    ) -> None:
        """AddLabelsTool rejects phase labels not in workphases.yaml."""
        yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^phase:[a-z][a-z0-9-]*$"
    description: "Workflow phase label"
    color: "C5DEF5"
    example: "phase:research"
labels: []
"""
        label_config = _load_label_config(tmp_path, yaml_content)
        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager, label_config=label_config, workphases_config=workphases_config
        )
        params = AddLabelsInput(issue_number=1, labels=["phase:unicorn"])

        result = await tool.execute(params, NoteContext())

        assert "unknown workphase" in result.content[0]["text"]
        mock_manager.add_labels.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_labels_accepts_known_phase(
        self, tmp_path: Path, workphases_config: WorkphasesConfig
    ) -> None:
        """AddLabelsTool accepts phase:implementation as a valid phase label."""
        yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^phase:[a-z][a-z0-9-]*$"
    description: "Workflow phase label"
    color: "C5DEF5"
    example: "phase:research"
labels: []
"""
        label_config = _load_label_config(tmp_path, yaml_content)
        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager, label_config=label_config, workphases_config=workphases_config
        )
        params = AddLabelsInput(issue_number=1, labels=["phase:implementation"])

        result = await tool.execute(params, NoteContext())

        assert "Added labels" in result.content[0]["text"]
```

These tests FAIL (RED) because `validate_phase_label()` does not exist yet, and
`AddLabelsTool`/`CreateLabelTool` do not accept `workphases_config`.

**Phase GREEN:**
1. Add `validate_phase_label()` to `mcp_server/config/schemas/label_config.py` (Decision 4b)
2. Add `workphases_config: WorkphasesConfig` (required) to `AddLabelsTool.__init__` and `CreateLabelTool.__init__`; add two-step phase check (Decision 4c)
3. Update `.st3/config/labels.yaml`: remove 9 explicit `phase:*` entries, add pattern (Decision 4a)
4. Add `workphases_config=workphases_config` to `AddLabelsTool` + `CreateLabelTool` in `mcp_server/server.py` L411/L413
5. Add `workphases_config` to all 12 existing test construction sites across `test_label_tools_integration.py` (L60, 76, 97, 121, 141, 162, 180, 202), `test_label_tools.py` (L74, 105), `test_github_extras.py` (L58), `test_all_tools.py` (L203 via `make_add_labels_tool`) — add a shared `workphases_config` fixture backed by `.st3/config/workphases.yaml`
6. GitHub label cleanup via `delete_label` / `create_label` MCP calls (Decision 4d)

**Phase REFACTOR:** Run `run_quality_gates(scope="files", files=["mcp_server/config/schemas/label_config.py", "mcp_server/tools/label_tools.py"])`.

---

## 4. Files Changed Summary

| File | Change | Lines |
|------|--------|-------|
| `mcp_server/tools/label_tools.py` | Decision 1: `label_exists()` → `validate_label_name()[0]`, rename var, update message | ~2 lines |
| `mcp_server/tools/label_tools.py` | Decision 2: filter `github_only` with `validate_label_name()` | ~3 lines |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | 2 new test methods (C_302.1 RED + C_302.2 RED) | ~40 lines |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | Update 2 existing assertions: lines 146 + 184 (message change) | 2 lines |
| `docs/mcp_server/GITHUB_SETUP.md` | Replace §4.4 (9 lines → 3 lines) | §4.4 |
| `docs/reference/mcp/tools/github.md` | Replace 6 label refs + 1 YAML snippet | 7 locations |
| `.st3/config/labels.yaml` | Remove 9 explicit `phase:*` entries; add `^phase:[a-z][a-z0-9-]*$` pattern | ~30 lines |
| `mcp_server/config/schemas/label_config.py` | Add `validate_phase_label()` module-level function | ~20 lines |
| `mcp_server/tools/label_tools.py` | Add `workphases_config` constructor param + phase check to `AddLabelsTool` + `CreateLabelTool` | ~15 lines |
| `mcp_server/server.py` | Add `workphases_config=workphases_config` to `AddLabelsTool` + `CreateLabelTool` at L411/L413 | 2 lines |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | C_302.3 RED: 7 new test methods across 2 new classes | ~80 lines |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | C_302.3 GREEN: add `workphases_config` to 8 existing sites (L60, 76, 97, 121, 141, 162, 180, 202) | 8 lines |
| `tests/mcp_server/unit/tools/test_label_tools.py` | C_302.3 GREEN: add `workphases_config` to `AddLabelsTool` (L105) + `CreateLabelTool` (L74) | 2 lines |
| `tests/mcp_server/unit/tools/test_github_extras.py` | C_302.3 GREEN: add `workphases_config` to `AddLabelsTool` (L58) | 1 line |
| `tests/mcp_server/unit/integration/test_all_tools.py` | C_302.3 GREEN: add `workphases_config` to `make_add_labels_tool` (L203) | 1 line |
| GitHub labels (runtime) | Delete 5 stale labels; create 4 missing labels | N/A — MCP tool calls |

---

## 5. Out of Scope

The following are explicitly deferred:
- Broader inaccuracies in `GITHUB_SETUP.md` (Project V2 config, phase labels list, type labels list)
- Removing orphaned `status:*` labels from the live GitHub repo (user decision required — no code change needed)
- The fallback regex in `validate_label_name()` that accepts `category:value` patterns beyond the explicit `label_patterns` list — this introduces false-negatives in drift detection for categories like `effort:*` and `component:*`. Deferred as a separate label_config correctness issue.
- Startup cross-config validation of GitHub labels vs. `workphases.yaml` (no existing implementation to build on; use-time validation per Decision 4 is sufficient)

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Existing tests break after AddLabelsTool fix | Low | Low | All existing tests use static labels; analysis confirms no breakage |
| `validate_label_name()` fallback causes drift false-negatives for stale status:* labels | Medium | Low | Pre-existing behavior; not introduced by this fix; separate concern |
| Doc changes introduce incorrect examples | Low | Low | All replacement labels verified against labels.yaml |
| `workphases_config` DI breaks existing tool construction sites | Medium | Medium | Must audit all construction sites in `server.py` / test fixtures; add `workphases_config` to constructor calls |
| Removing `phase:*` from labels.yaml breaks `LabelConfig._build_caches()` | Low | Low | Pattern replaces exact entries — `validate_label_name()` still passes for valid phase labels via layer 3 |
| GitHub label cleanup deletes a label in active use on open issues | Low | Medium | Audit GitHub for open issues with the 5 stale labels before deletion; relabel as needed |
