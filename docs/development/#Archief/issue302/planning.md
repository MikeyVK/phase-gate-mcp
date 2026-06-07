<!-- docs\development\issue302\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-07T08:25Z updated= -->
# Planning: Align labels config, GitHub labels, and docs (Issue #302)

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-07

---

## Purpose

Define cycle order, size rationale, per-cycle deliverables, and JSON gatekeepers for cycle
transfer. Each deliverable is a verifiable artefact that the next cycle (or the validation
phase) can use as a gate — if a deliverable is missing or failing, the cycle may not advance.

## Scope

**In Scope:**
Three TDD cycles: C_302.1 (sub-A), C_302.2 (sub-B), C_302.3 (sub-D). Documentation phase
for sub-C.

**Out of Scope:**
Startup GitHub-alignment validation (deferred). Fallback regex false-negatives for
effort/component labels (deferred). Broader GITHUB_SETUP.md inaccuracies.

## Prerequisites

Read these first:
1. research.md v1.1 approved (QA GO)
2. design.md v1.1 approved (QA GO)
3. workphases.yaml loaded and accessible for fixture
4. All label tool test files identified (blast radius audit complete — 14 construction sites
   across 5 files)

---

## Summary

Four sub-problems (A–D) resolved in three TDD cycles. C_302.1 fixes AddLabelsTool
validation, C_302.2 fixes DetectLabelDriftTool drift detection, C_302.3 introduces
`validate_phase_label()` and restructures `labels.yaml`. Documentation fixes (sub-problem C)
land in a separate non-TDD documentation phase, because sub-problem C has no code
dependencies and does not affect runtime behaviour validation (see design.md §2 Decision 3).

---

## Cycle Order Rationale

The cycle sequence is strictly ordered for three reasons:

**1. Dependency graph — each cycle builds on the previous**

`validate_label_name()` is the shared validator that both tools delegate to. C_302.1 proves
it works correctly for pattern-matching labels. Only after that is confirmed does C_302.2
safely reuse it in drift detection. C_302.3 then layers a *semantic* check on top of the
*format* check already validated in C_302.1. Reversing the order would mean implementing
a semantic check before confirming the format check works — increasing the chance of
composite failures that are hard to isolate.

**2. Risk escalation — smallest blast radius first**

C_302.1 changes a single method call in one tool and touches 1 new + 2 updated tests.
C_302.2 changes one filter expression in one tool and adds 1 new test.
C_302.3 changes 3 source files, 4 test files, 1 config file, and performs a runtime GitHub
operation. Ordering from smallest to largest blast radius means that if a cycle fails, the
root cause is local to that cycle — not entangled with unrelated changes.

**3. Atomicity per sub-problem**

Design decisions A and B are independent of D; D depends on both A and B being stable.
Sub-problem C (doc fixes) has no code dependencies and is deferred to the documentation
phase to keep implementation cycles focused on behaviour changes.

---

## Cycle Size Rationale

| Cycle | Source lines changed | New tests | Updated tests | Rationale |
|-------|---------------------|-----------|---------------|-----------|
| C_302.1 | ~5 | 1 | 2 | Minimal — one method swap + message change |
| C_302.2 | ~4 | 1 | 0 | Minimal — one filter expression |
| C_302.3 | ~40 source + 14 DI sites + config | 7 | 8 | Large by necessity: new function + DI + config restructure are a single atomic change — splitting would leave the system in an inconsistent state (required param not yet required) |

C_302.3 cannot be split further: adding `validate_phase_label()` without updating the tool
constructors would break existing tests; updating constructors without updating the 14 call
sites in tests would immediately fail CI. The three actions (new function + DI param + call
site updates) form an atomic unit.

---

## TDD Cycles

### Cycle C_302.1 — AddLabelsTool accepts dynamic pattern labels

**Goal:** Replace `label_exists()` with `validate_label_name()` in `AddLabelsTool.execute()`
so that labels matching `label_patterns` (e.g. `parent:302`) are accepted.

**File:** `mcp_server/tools/label_tools.py`

**Tests:**
- `test_add_labels_accepts_dynamic_pattern_label` — **new** — asserts `parent:302` is
  accepted when a matching `label_patterns` entry exists
- `test_add_labels_validates_existence` (existing) — message updated: `"not defined in
  labels.yaml"` → `"not valid per labels.yaml"`
- `test_add_labels_partial_invalid_rejects_all` (existing) — same message update

**Success Criteria:**
- `AddLabelsTool` uses `validate_label_name()` as sole validator
- Pattern-matching labels (e.g. `parent:302`) are accepted
- Error message reflects new semantics (`not valid per labels.yaml`)
- All existing `AddLabelsTool` tests pass

**Dependencies:** none (first cycle)

---

### Cycle C_302.2 — DetectLabelDriftTool ignores pattern-matching labels

**Goal:** Filter `github_only` list to exclude labels that pass `validate_label_name()`,
so pattern-matching GitHub labels (e.g. `parent:302`) are not reported as drift.

**File:** `mcp_server/tools/label_tools.py`

**Tests:**
- `test_drift_detection_pattern_labels_not_reported_as_drift` — **new** — asserts
  `parent:302` does not appear in drift report when matching `label_patterns` entry exists

**Success Criteria:**
- `github_only` filtered by `validate_label_name()`
- Pattern-matching GitHub labels excluded from drift result
- All existing `DetectLabelDriftTool` tests pass

**Dependencies:** C_302.1 complete — `validate_label_name()` already confirmed as correct
validator

---

### Cycle C_302.3 — validate_phase_label() + labels.yaml restructure + DI

**Goal:** Introduce `validate_phase_label()` free function, add required `workphases_config`
DI parameter to `AddLabelsTool` and `CreateLabelTool`, remove 9 explicit `phase:*` entries
from `labels.yaml`, update all 14 construction sites, and perform GitHub label cleanup.

**Files changed:**
- `mcp_server/config/schemas/label_config.py` — new function (~20 lines)
- `mcp_server/tools/label_tools.py` — two tools gain `workphases_config` param + check
  (~15 lines)
- `.st3/config/labels.yaml` — 9 entries removed, 1 pattern added (~30 line delta)
- `mcp_server/server.py` — L411/L413: `workphases_config=workphases_config` added (2 lines)
- `tests/mcp_server/unit/tools/test_label_tools_integration.py` — 7 new tests + 8 DI sites
- `tests/mcp_server/unit/tools/test_label_tools.py` — 2 DI sites (L74, L105)
- `tests/mcp_server/unit/tools/test_github_extras.py` — 1 DI site (L58)
- `tests/mcp_server/unit/integration/test_all_tools.py` — 1 DI site (L203)

**Tests (new):**
- `test_non_phase_label_is_always_valid`
- `test_known_phase_is_valid`
- `test_unknown_phase_is_invalid`
- `test_subphase_is_invalid` (`phase:red` rejected)
- `test_stale_integration_phase_is_invalid` (`phase:integration` rejected)
- `test_add_labels_rejects_unknown_phase`
- `test_add_labels_accepts_known_phase`

**Success Criteria:**
- `validate_phase_label()` exists in `label_config.py`
- `AddLabelsTool` and `CreateLabelTool` accept `workphases_config` as **required** parameter
- `labels.yaml` has no explicit `phase:*` entries; uses `^phase:[a-z][a-z0-9-]*$` pattern
- All 14 existing construction sites updated with `workphases_config` fixture
- `server.py` L411/L413 updated
- GitHub label cleanup executed (5 deleted, 4 created via MCP tool calls)
- Quality gates pass: ruff + mypy on `label_config.py` + `label_tools.py`

**Dependencies:**
- C_302.1 complete — `validate_label_name()` semantics confirmed
- C_302.2 complete — drift tool stable before adding phase check layer

---

## Per-Cycle JSON Deliverables (Gatekeepers)

Each cycle produces a set of verifiable deliverables. These are persisted in
`deliverables.json` and function as **gatekeepers**: the next cycle (or phase transition)
must confirm all deliverables of the prior cycle are present and valid before proceeding.

### C_302.1 Deliverables

| id | type | description | validates |
|----|------|-------------|-----------|
| `c302_1_new_test_exists` | `test_exists` | New test `test_add_labels_accepts_dynamic_pattern_label` present in test file | file + test name |
| `c302_1_method_replaced` | `code_pattern` | `validate_label_name` appears in `AddLabelsTool.execute()` | file + regex |
| `c302_1_old_method_absent` | `code_pattern` | `label_exists` no longer called in `AddLabelsTool.execute()` | file + absence regex |
| `c302_1_tests_pass` | `test_run` | All `TestAddLabelsToolValidation` tests pass | pytest marker |

### C_302.2 Deliverables

| id | type | description | validates |
|----|------|-------------|-----------|
| `c302_2_new_test_exists` | `test_exists` | `test_drift_detection_pattern_labels_not_reported_as_drift` present | file + test name |
| `c302_2_filter_applied` | `code_pattern` | `validate_label_name` used in `github_only` list comprehension | file + regex |
| `c302_2_tests_pass` | `test_run` | All `TestDetectLabelDriftTool` tests pass | pytest marker |

### C_302.3 Deliverables

| id | type | description | validates |
|----|------|-------------|-----------|
| `c302_3_function_exists` | `code_pattern` | `def validate_phase_label` present in `label_config.py` | file + regex |
| `c302_3_param_required` | `code_pattern` | `workphases_config: WorkphasesConfig` present in both tool `__init__` signatures | file + regex |
| `c302_3_labels_yaml_clean` | `config_check` | No `phase:` entries under `labels:` key in `labels.yaml` | file + yaml path |
| `c302_3_pattern_added` | `config_check` | `^phase:[a-z][a-z0-9-]*$` pattern present in `labels.yaml` | file + string |
| `c302_3_server_updated` | `code_pattern` | `workphases_config=workphases_config` present at L411 and L413 in `server.py` | file + regex |
| `c302_3_construction_sites_updated` | `code_pattern` | All 14 instantiation sites updated with `workphases_config` param (4 source lines in server.py + label_tools.py, 10 test sites across 4 files) | files + regex |
| `c302_3_new_tests_pass` | `test_run` | All `TestValidatePhaseLabelFunction` + `TestAddLabelsToolPhaseValidation` tests pass | pytest marker |
| `c302_3_quality_gates` | `quality_gate` | ruff + mypy pass on `label_config.py` + `label_tools.py` | tool call result |
| `c302_3_github_cleanup` | `runtime_op` | 5 stale labels deleted, 4 missing labels created on GitHub | manual confirmation |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-07 | Agent | Initial draft |
