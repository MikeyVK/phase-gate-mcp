# Design: Align labels config, GitHub labels, and docs (Issue #302)

**Status:** FINAL
**Version:** 1.0
**Phase:** Design
**Issue:** #302
**Branch:** fix/302-align-labels-config-github-docs

---

## 1. Design Goals

1. `AddLabelsTool` must accept labels matching `label_patterns` (e.g., `parent:302`).
2. `DetectLabelDriftTool` must not report pattern-matching GitHub labels as false-positive drift.
3. All doc references to `status:*` labels must be replaced with valid labels from the current taxonomy.

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
| Line 270 (update_issue response) | `"status:resolved"` | `"phase:done"` |
| Line 292 (update_issue example) | `"status:resolved", "phase:done"` | `"phase:done"` (dedup) |
| Line 793 (add_labels example) | `"priority:high", "status:in-progress"` | `"priority:high", "phase:tdd"` |
| Line 826 (add_labels example) | `"status:in-progress"` | `"phase:tdd"` |
| Line 835 (add_labels example) | `"status:in-progress"` | `"phase:tdd"` |
| Lines 1062–1067 (Configuration section YAML) | Fabricated `label_config.patterns` with `status:(backlog|in-progress|review|done)` | Replace entire snippet with accurate summary of actual labels.yaml structure |

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

## 4. Files Changed Summary

| File | Change | Lines |
|------|--------|-------|
| `mcp_server/tools/label_tools.py` | Decision 1: `label_exists()` → `validate_label_name()[0]`, rename var, update message | ~2 lines |
| `mcp_server/tools/label_tools.py` | Decision 2: filter `github_only` with `validate_label_name()` | ~3 lines |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | 2 new test methods (C_302.1 RED + C_302.2 RED) | ~40 lines |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | Update 2 existing assertions: lines 146 + 184 (message change) | 2 lines |
| `docs/mcp_server/GITHUB_SETUP.md` | Replace §4.4 (9 lines → 3 lines) | §4.4 |
| `docs/reference/mcp/tools/github.md` | Replace 6 label refs + 1 YAML snippet | 7 locations |

---

## 5. Out of Scope

The following are explicitly deferred:
- Broader inaccuracies in `GITHUB_SETUP.md` (Project V2 config, phase labels list, type labels list)
- Removing orphaned `status:*` labels from the live GitHub repo (user decision required)
- The fallback regex in `validate_label_name()` that accepts `category:value` patterns beyond the explicit `label_patterns` list — this introduces new false-negatives in drift detection for categories like `effort:*` and `component:*`. Deferred as a separate label_config correctness issue.

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Existing tests break after AddLabelsTool fix | Low | Low | All existing tests use static labels; analysis confirms no breakage |
| `validate_label_name()` fallback causes drift false-negatives for stale status:* labels | Medium | Low | Pre-existing behavior; not introduced by this fix; separate concern |
| Doc changes introduce incorrect examples | Low | Low | All replacement labels verified against labels.yaml |
