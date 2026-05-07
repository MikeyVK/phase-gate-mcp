# Research: Align labels config, GitHub labels, and docs (Issue #302)

**Status:** FINAL
**Version:** 1.1
**Phase:** Research
**Issue:** #302
**Branch:** fix/302-align-labels-config-github-docs

---

## 1. Problem Statement

Issue #302 groups three distinct alignment failures between `.st3/config/labels.yaml` (the
authoritative SSOT), the MCP server tool code, and documentation:

| # | Sub-problem | Layer |
|---|-------------|-------|
| A | `AddLabelsTool` uses `label_exists()` (exact dict) instead of `validate_label_name()` (pattern-aware) | Code (tool) |
| B | `DetectLabelDriftTool` reports all pattern-matching GitHub labels as "drift" | Code (tool) |
| C | Docs still reference `status:*` labels that were intentionally removed in issue #149 | Docs |
| D | `labels.yaml` explicitly lists 9 `phase:*` entries that diverge from `workphases.yaml` — DRY/SSOT violation | Config + Code |

---

## 2. Background

### 2.1 labels.yaml is the SSOT

`.st3/config/labels.yaml` defines the label taxonomy in two ways:
- **Static labels**: explicit `labels:` list — 37 labels, exact name + color + description.
- **Dynamic patterns**: `label_patterns:` list — validated by regex, created on demand.
  Currently one pattern: `^parent:\d+$` (example: `parent:91`).

```yaml
label_patterns:
  - pattern: "^parent:\\d+$"
    description: "Parent issue reference for child issues"
    color: "EDEDED"
    example: "parent:91"
```

### 2.2 Two validation methods in LabelConfig

`mcp_server/config/schemas/label_config.py` exposes two methods:

| Method | Logic | Pattern-aware? |
|--------|-------|----------------|
| `label_exists(name)` | `return name in self._labels_by_name` | ❌ No |
| `validate_label_name(name)` | checks freeform_exceptions → exact dict → label_patterns regex | ✅ Yes |

`CreateLabelTool` (line ~85) correctly uses `validate_label_name()`.
`AddLabelsTool` (line ~195) incorrectly uses `label_exists()`.

### 2.3 status:* labels removed in issue #149

Issue #149 deliberately removed all `status:*` labels from `labels.yaml`. The rationale:
GitHub issue state (`open`/`closed`) combined with `phase:*` labels is sufficient.
The `status:*` labels (blocked, in-progress, needs-info, ready) remain as orphaned labels
on the live GitHub repo — but they are unused and not in the config SSOT.

The docs were never updated to reflect this decision.

---

## 3. Blast Radius

### 3.1 Sub-problem A — AddLabelsTool validation bug

**Root cause:** `AddLabelsTool.execute()` in `mcp_server/tools/label_tools.py` (line ~195):

```python
# BUG — exact dict lookup, no pattern awareness
undefined = [label for label in params.labels
             if not self._label_config.label_exists(label)]
```

**Effect:** Any dynamically-patterned label (`parent:NNN`) is rejected at validation time,
even though:
1. The label is valid per `validate_label_name()`.
2. The label may already exist on GitHub (created via `create_label`).

**Observed impact:** During the current session, `add_labels(["parent:290"])` failed for
issues #278 and #268 — requiring a manual `gh issue edit` CLI workaround.

**Files affected:**
- `mcp_server/tools/label_tools.py` — the fix (one line + error message)
- `tests/mcp_server/unit/tools/test_label_tools_integration.py` — new RED→GREEN test
- `tests/mcp_server/unit/tools/test_label_tools.py` — fixture has no `label_patterns`;
  test `test_add_labels_tool` passes `["bug", "p1"]` which are static labels — unaffected

**Tests that currently exist and their status after the fix:**
- `test_add_labels_validates_existence` (line 146): asserts `"not defined in labels.yaml"` in
  the error text — this assertion **will break** because the message changes to
  `"not valid per labels.yaml"`. Must be updated in GREEN phase.
- `test_add_labels_partial_invalid_rejects_all` (line 184): same assertion —
  **will also break** for the same reason. Must be updated in GREEN phase.
- `test_add_labels_all_valid_succeeds`: uses explicit static labels — still passes
- `test_add_labels_freeform_allowed`: uses freeform exception label — still passes

**Error message impact:** Current message is `"Labels not defined in labels.yaml: {list}"`.
After the fix the semantic shifts: a label may be "not valid per labels.yaml" rather than
"not defined" (since a pattern label is valid but not explicitly listed). The message
needs updating. The two assertions noted above must be updated from `"not defined in labels.yaml"`
to `"not valid per labels.yaml"` as part of the GREEN phase.

### 3.2 Sub-problem B — DetectLabelDriftTool blind spot

**Root cause:** `DetectLabelDriftTool.execute()` builds `github_only` with:

```python
github_only = [name for name in github_by_name if name not in yaml_by_name]
```

`yaml_by_name` only contains statically defined labels. Pattern-matching labels on GitHub
(e.g., `parent:91`, `parent:290`) will always appear as "GitHub-only drift".

**Effect:** Drift reports contain false positives for every `parent:NNN` label on GitHub,
generating incorrect "Recommendation: Add to labels.yaml or remove from GitHub" advice.

**Files affected:**
- `mcp_server/tools/label_tools.py` — filter logic in `DetectLabelDriftTool.execute()`
- `tests/mcp_server/unit/tools/test_label_tools_integration.py` — new RED→GREEN test

**Tests that currently exist (unaffected):**
- All five `TestDetectLabelDriftTool` tests use YAML with only static labels. They remain
  valid and passing.

### 3.3 Sub-problem C — Documentation drift

**Files affected with specific locations:**

| File | Location | Stale content |
|------|----------|---------------|
| `docs/mcp_server/GITHUB_SETUP.md` | Lines 116-123 (§4.4 Status) | Lists `status:blocked`, `status:needs-info`, `status:ready-for-review` as if they are active labels |
| `docs/reference/mcp/tools/github.md` | Line 270 | `"labels": ["type:feature", "status:resolved"]` in update_issue example |
| `docs/reference/mcp/tools/github.md` | Line 292 | `"labels": ["type:feature", "status:resolved", "phase:done"]` in update_issue example |
| `docs/reference/mcp/tools/github.md` | Line 793 | `"labels": ["priority:high", "status:in-progress"]` in add_labels example |
| `docs/reference/mcp/tools/github.md` | Lines 826, 835 | `"labels": ["status:in-progress"]` in add_labels example |
| `docs/reference/mcp/tools/github.md` | Lines 1062-1067 | Completely fabricated YAML snippet showing `label_config.patterns` with `status:(backlog|in-progress|review|done)` — wrong structure AND wrong labels |

**No other docs files** are affected. The archive files (`docs/development/archive/issue149/`,
`docs/development/archive/issue51/`) contain historical references to `status:*` labels —
these are intentionally accurate historical records and must NOT be changed.

**Not in scope:** Broader inaccuracies in `GITHUB_SETUP.md` (stale Project V2 config, phase
labels list, type labels list). Fixing those is a separate concern. This issue touches only
the `status:*` alignment.

### 3.4 Sub-problem D — DRY/SSOT violation: `labels.yaml` phase:* vs `workphases.yaml`

**Root cause:** `.st3/config/labels.yaml` contains 9 explicit `phase:*` label entries that
are maintained independently of `.st3/config/workphases.yaml` — the canonical source of
workflow phase definitions used by all tooling. This creates a DRY and SSOT violation:
adding or renaming a phase in `workphases.yaml` requires a manual parallel update to
`labels.yaml`.

**Current divergences (audit result):**

| Label | In `labels.yaml` | In `workphases.yaml` | Assessment |
|-------|-------------------|----------------------|------------|
| `phase:research` | ✅ | ✅ | OK |
| `phase:planning` | ✅ | ✅ | OK |
| `phase:design` | ✅ | ✅ | OK |
| `phase:documentation` | ✅ (color `0075CA`) | ✅ | Color inconsistency — other phases use `C5DEF5` |
| `phase:implementation` | ❌ missing | ✅ | Missing GitHub label |
| `phase:validation` | ❌ missing | ✅ | Missing GitHub label |
| `phase:coordination` | ❌ missing | ✅ | Missing GitHub label |
| `phase:ready` | ❌ missing | ✅ (terminal) | Missing GitHub label |
| `phase:integration` | ✅ | ❌ removed | Stale — was a workphase in old design |
| `phase:tdd` | ✅ | ❌ (subphase alias) | Invalid issue label — not a top-level workphase |
| `phase:red` | ✅ | ❌ (subphase of implementation) | Invalid issue label — commit-level granularity only |
| `phase:green` | ✅ | ❌ (subphase of implementation) | Invalid issue label — commit-level granularity only |
| `phase:refactor` | ✅ | ❌ (subphase of implementation) | Invalid issue label — commit-level granularity only |

**Consequence:** Issues can currently be labeled `phase:red` or `phase:tdd` (misleading),
while `phase:implementation`, `phase:validation`, `phase:coordination`, and `phase:ready`
cannot be used as labels at all — even though they are valid workflow states.

**Files affected:**
- `.st3/config/labels.yaml` — remove 9 explicit `phase:*` entries, add one dynamic pattern
- `mcp_server/config/schemas/label_config.py` — new module-level function `validate_phase_label()`
- `mcp_server/tools/label_tools.py` — `AddLabelsTool` and `CreateLabelTool` gain two-step phase validation
- `tests/mcp_server/unit/tools/test_label_tools_integration.py` — 1 new TDD cycle (C_302.3)
- GitHub labels — delete 5 stale labels, create 4 missing labels (one-time operation)

**Design constraint:** `workphases.yaml` is the SSOT. Only top-level keys in
`workphases.phases` are valid `phase:*` label suffixes — subphases (e.g., `red`, `green`,
`refactor`, `contracts`, `e2e`) are **never** valid issue labels.

---

## 4. Options Considered

### Sub-problem A

| Option | Tradeoff |
|--------|----------|
| **A1 (chosen):** Replace `label_exists()` with `validate_label_name()[0]` in AddLabelsTool | Minimal change, uses existing correct method, no new abstractions |
| A2: Change `label_exists()` to also check patterns | Would change meaning of `label_exists()` (semantic shift); other callers may rely on exact-match semantics |
| A3: Add a third method `is_valid_label_name()` | Unnecessary duplication — `validate_label_name()` already exists (YAGNI) |

Option A1 wins: one-line fix using the already-correct method that `CreateLabelTool` uses.

### Sub-problem B

| Option | Tradeoff |
|--------|----------|
| **B1 (chosen):** Filter `github_only` using `validate_label_name()` | Symmetric with A1 fix; no new methods; consistent validation |
| B2: Add a separate method `is_pattern_matched(name)` | Unnecessary; `validate_label_name()` already does this |

Option B1 wins: same pattern as A1.

### Sub-problem C

| Option | Tradeoff |
|--------|----------|
| **C1 (chosen):** Remove/replace `status:*` references in both docs; replace with valid labels | Minimal targeted fix; archive docs untouched |
| C2: Full GITHUB_SETUP.md rewrite | Out of scope — other inaccuracies are cosmetic, not misleading |

Option C1 wins: targeted fix, archive preserved.

### Sub-problem D

| Option | Tradeoff |
|--------|----------|
| **D1 (chosen):** Replace 9 explicit `phase:*` entries in `labels.yaml` with one `label_pattern`; add `validate_phase_label()` free function; both `AddLabelsTool` and `CreateLabelTool` call it after `validate_label_name()` | Eliminates DRY violation; `workphases.yaml` becomes true SSOT; two-step validation keeps SRP; no new classes |
| D2: Add cross-config validation in `ConfigValidator.validate_startup()` | Only validates YAML-vs-YAML at startup — does not enforce semantics at use-time when labels are assigned |
| D3: Store workphase names directly in `labels.yaml` as the SSOT | Inverts the existing SSOT contract — `workphases.yaml` is used for commit conventions, phase transitions, and contracts; cannot be demoted |
| D4: Generate `labels.yaml` phase section from `workphases.yaml` at startup | Adds runtime mutation of config — violates immutable value object contract of `LabelConfig` |

Option D1 wins: eliminates the violation at its root, enforces semantics at the point of
label assignment, and does not couple config loading to GitHub at startup.

**`validate_phase_label()` placement rationale:**
A module-level function in `mcp_server/config/schemas/label_config.py` is the correct
location. It is cohesive with label validation logic, avoids coupling two config value
objects (§7 LoD), and keeps `LabelConfig` itself unchanged (§1.1 SRP). Both
`AddLabelsTool` and `CreateLabelTool` receive `workphases_config` via constructor injection
and call the function after `validate_label_name()` passes (two-step: form first, meaning
second).

**Why both tools need the check:** `CreateLabelTool` creates GitHub labels — not config
entries. Creating `phase:unicorn` on GitHub when `unicorn` is not a workphase is as wrong
as assigning it to an issue. The semantic check must apply everywhere a `phase:*` label is
created or assigned.

---

## 5. Impacted File Summary

| File | Change type | Sub-problem |
|------|-------------|-------------|
| `mcp_server/tools/label_tools.py` | Code fix (2 locations) | A + B |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | 2 new tests | A + B |
| `docs/mcp_server/GITHUB_SETUP.md` | Remove §4.4 status labels block | C |
| `docs/reference/mcp/tools/github.md` | Replace 7 label references + 1 YAML snippet | C |
| `.st3/config/labels.yaml` | Remove 9 explicit `phase:*` entries; add `^phase:[a-z][a-z0-9-]*$` pattern | D |
| `mcp_server/config/schemas/label_config.py` | Add `validate_phase_label()` module-level function | D |
| `mcp_server/tools/label_tools.py` | Add `workphases_config` to `AddLabelsTool` + `CreateLabelTool`; call `validate_phase_label()` | D |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | 1 new TDD cycle (C_302.3) | D |
| GitHub labels (runtime) | Delete: `phase:integration`, `phase:tdd`, `phase:red`, `phase:green`, `phase:refactor`; Create: `phase:implementation`, `phase:validation`, `phase:coordination`, `phase:ready` | D |

**Total files: 6 code/config files + 2 doc files + 1 GitHub runtime operation. No new classes. No interface changes beyond constructor extensions.**

---

## 6. Validation Strategy

All changes are validated by existing + new unit tests:
- Sub-problems A and B: TDD cycle (RED → GREEN) in `test_label_tools_integration.py`
- Sub-problem C: doc-only, validated by review (no testable contract)
- Sub-problem D: TDD cycle C_302.3 in `test_label_tools_integration.py`; labels.yaml change
  validated by existing schema tests; `validate_phase_label()` covered by dedicated unit tests

Quality gates: full test suite must pass (currently ~2580 tests).
