# Research: Align labels config, GitHub labels, and docs (Issue #302)

**Status:** FINAL
**Version:** 1.0
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

---

## 5. Impacted File Summary

| File | Change type | Sub-problem |
|------|-------------|-------------|
| `mcp_server/tools/label_tools.py` | Code fix (2 locations) | A + B |
| `tests/mcp_server/unit/tools/test_label_tools_integration.py` | 2 new tests | A + B |
| `docs/mcp_server/GITHUB_SETUP.md` | Remove §4.4 status labels block | C |
| `docs/reference/mcp/tools/github.md` | Replace 7 label references + 1 YAML snippet | C |

**Total files: 4. No schema changes. No interface changes. No new classes.**

---

## 6. Validation Strategy

All changes are validated by existing + new unit tests:
- Sub-problems A and B: TDD cycle (RED → GREEN) in `test_label_tools_integration.py`
- Sub-problem C: doc-only, validated by review (no testable contract)

Quality gates: full test suite must pass (currently ~2580 tests).
