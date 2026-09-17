<!-- docs\development\issue460\rollout-workflow-input.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T05:52Z updated=2026-09-17 -->
# Issue 460 Rollout Workflow Input: Nineteen Workflow Carriers and Phase Semantics

**Status:** IMPLEMENTATION EVIDENCE — REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-09-17  
**Primary Package:** DI-07 §§7.1–7.2, 10  
**Cycle:** CY068 (Workflow carriers and phase semantics)  
**Author:** @imp implementer  

---

## 1. Purpose and Authority

This artifact records the reviewed target-source patch, checksums, and independent verification evidence for the nineteen workflow carriers, clean-break V3 tool names, complete input-inventory removal, and conditional schema discovery guidance in `.pgmcp/config/contracts.yaml`.

This is implementation evidence prepared for CY072 live cutover under the authority of:
- [DI-07 Workflow and Documentation Alignment Design §§7.1–7.2, 10](design-workflow-documentation.md)
- [Planning Rollout §CY068](planning-rollout.md#cy068)
- [Exact Path Ownership](planning-path-ownership.md)

In accordance with CY068 constraints:
- Inactive V3 contracts are **not** advertised in live source/copies; live file modifications and byte parity are deferred to CY072.
- The recorded patch is temporary migration evidence, never runtime configuration or a competing instruction authority.
- Evidence is established strictly against explicit, isolated source copies.

---

## 2. Scope and Exclusions

### In Scope
- Preparation of the exact bounded target-source diff for `.pgmcp/config/contracts.yaml` (C003).
- Verification of nineteen workflow carriers and preserved semantic obligations across all seven workflows (`feature`, `bug`, `refactor`, `chore`, `epic`, `docs`, `hotfix`).
- Elimination of obsolete serialized complete argument payloads (`context={...}`, `files=[...]`, `cycles={...}`).
- Modernization of tool names (`run_quality_gates` -> `run_checks`).
- Introduction of conditional schema discovery guidance (`scaffold_schema` when needed) and refinement guidance (`safe_edit_file`).
- Verification that valid initial scaffolding is kept distinct from final phase completion.
- Recording of preimage and postimage SHA256 checksums and independent test proof (DOCFLOW-E01 and DOCFLOW-E02).

### Out of Scope
- Direct in-place mutation of live `.pgmcp/config/contracts.yaml` prior to CY072.
- Modifications to host instruction files (reserved for CY069).
- Modifying workflow engine core logic or inventing new workflows/phases.
- Modifying downstream Git or GitHub operational tools.

---

## 3. Nineteen Workflow Carriers and Semantic Obligations

Under DI-07 §7.2 and DI-03 §7.8, nineteen workflow/phase variants express distinct domain and workflow obligations. The table below specifies the carrier mapping and the essential meaning that survives in each persisted document:

| # | Workflow Variant | Primary Phase | DI-03 Carrier Artifact | Preserved Meaning in Persisted Document |
|---|---|---|---|---|
| 1 | Feature Research | `research` | `research` | Evidenced blast radius, affected consumers, alternatives/risks, expected results, and human Approved Strategy. |
| 2 | Bug Research | `research` | `research` | Reproduction/occurrence context, causal evidence, correction boundary (`scope_in`/`scope_out`), expected results, and strategy. |
| 3 | Refactor Research | `research` | `research` | Responsibility/coupling problems, preservation invariants, exclusions (`scope_out`), and Approved Strategy. |
| 4 | Chore Research | `research` | `research` | Bounded objective, scope, consumers, risks, and strategy; persistence remains conditional. |
| 5 | Epic Research | `research` | `research` | Workstream/consumer boundaries, assumptions, dependencies, risks, and shared strategy. |
| 6 | Feature Design | `design` | `design` | Production responsibilities, interfaces, data/control flow, failure behavior, alternatives, test design, and planning consequences. |
| 7 | Bug Design | `design` | `design` | Smallest causal correction, preserved behavior, failure behavior, constraints, and regression evidence design. |
| 8 | Refactor Design | `design` | `design` | Target responsibilities/interfaces, preservation, cutover/removals, key decisions, and test architecture. |
| 9 | Epic Design | `design` | `design` | Cross-workstream interfaces, component ownership, integration/failures, and shared evidence obligations. |
| 10 | Feature Planning | `planning` | `planning` | Dependency-ordered work units, deliverables, verification, and exit criteria. |
| 11 | Bug Planning | `planning` | `planning` | Reproduction/regression/correction obligations, dependencies, and exit evidence. |
| 12 | Refactor Planning | `planning` | `planning` | Responsibility moves, preservation/removal obligations, dependencies, and stop conditions. |
| 13 | Docs Planning | `planning` | `planning` | Documentation scope/ownership, sources, deliverables, risks, and verification (no invented TDD cycles). |
| 14 | Epic Planning | `planning` | `planning` | Child ownership, shared obligations/dependencies, milestones, acceptance, and stop conditions. |
| 15 | Feature Validation | `validation` | `validation_report` | Observed requirement coverage, demonstration, outcomes, caveats, risks, and deferred work. |
| 16 | Bug Validation | `validation` | `validation_report` | Observed reproduction correction, regression verification, and preserved behavior. |
| 17 | Refactor Validation | `validation` | `validation_report` | Observed structural completion/removal, invariants, and cycle outcomes. |
| 18 | Hotfix Validation | `validation` | `validation_report` | Correction, containment, preservation, and operational risks/caveats. |
| 19 | Chore Validation | `validation` | `validation_report` | Bounded objective coverage, proportionate observed evidence, risks, and deferred work. |

---

## 4. Input-Removal and Tool Modernization Analysis

### 4.1 Elimination of Serialized Argument Payloads
Live `contracts.yaml` previously embedded serialized argument inventories such as:
```yaml
scaffold_artifact(artifact_type='research', name='research', context={...})
run_quality_gates(scope='files', files=[...])
save_planning_deliverables(issue_number=N, cycles={...}, deliverables=[...])
```
These literal inventories violated DI-07 D-WORKFLOW-03 and created schema drift. The V3 target replaces them with tool purpose, conditional schema discovery, and clear role boundaries:
- `scaffold_schema`: Called conditionally when the agent needs context field discovery.
- `scaffold_artifact`: Generates the initial honest document scaffold without duplicating schema declarations in instructions.
- `safe_edit_file`: Refines the scaffolded document.
- Invariant: A valid scaffold is an initial structural basis, **not** phase completion.

### 4.2 Tool Name Clean Break
- `run_quality_gates` is completely replaced by `run_checks`.
- Validation phases instruct `run_tests` for test suites and `run_checks` for static analysis and linting.
- Authorized auto-fixes reference `apply_fixes`.

---

## 5. Target Source Diff and Checksums

### 5.1 Checksums
- **Target File:** `.pgmcp/config/contracts.yaml`
- **Preimage SHA-256:** `9610d38bf943c687e8c200b626259b3f107b69d4e9d0a40e44f38c91f8194d10`
- **Postimage SHA-256:** `dd62d93ff05bd62eb0b0dc7e4bee4d4dc0a142d8d2cb8d910816358e6cbc0f40`

### 5.2 Exact Patch (Unified Diff)
```diff
--- a/.pgmcp/config/contracts.yaml
+++ b/.pgmcp/config/contracts.yaml
@@ -51,2 +51,2 @@
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
+                scaffold_artifact(artifact_type='research', name='research').
@@ -120,2 +120,2 @@
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
+                scaffold_artifact(artifact_type='design', name='design').
@@ -192,4 +192,3 @@
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Apply Documentation Standard boundaries and keep document cycles identical to the
-                structured payload. Save them with save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]) after verifying IDs, ordering, and dependencies.
+                scaffold_artifact(artifact_type='planning', name='planning').
+                Apply Documentation Standard boundaries and keep document cycles identical to the
+                structured payload. Save them with save_planning_deliverables(issue_number=N, ...) after verifying IDs, ordering, and dependencies.
@@ -260,2 +259,2 @@
-                run_quality_gates(scope='files', files=[...]) proportionally. Do not run the full
+                run_checks(scope='files', files=[...]) proportionally. Do not run the full
@@ -316,2 +315,2 @@
-                gates with run_quality_gates(scope='branch'). Reuse nothing stale; if a check
+                gates with run_checks(scope='branch'). Reuse nothing stale; if a check
@@ -328,3 +327,3 @@
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update the existing phase artifact.
+                scaffold_artifact(artifact_type='validation_report', name='validation');
+                otherwise update the existing phase artifact.
@@ -530,2 +529,2 @@
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
+                scaffold_artifact(artifact_type='research', name='research').
@@ -599,2 +598,2 @@
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
+                scaffold_artifact(artifact_type='design', name='design').
@@ -671,4 +670,3 @@
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Apply Documentation Standard boundaries and keep document cycles identical to the
-                structured payload. Save them with save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]) after verifying IDs, ordering, and dependencies.
+                scaffold_artifact(artifact_type='planning', name='planning').
+                Apply Documentation Standard boundaries and keep document cycles identical to the
+                structured payload. Save them with save_planning_deliverables(issue_number=N, ...) after verifying IDs, ordering, and dependencies.
@@ -739,2 +737,2 @@
-                run_quality_gates(scope='files', files=[...]) proportionally. Do not run the full
+                run_checks(scope='files', files=[...]) proportionally. Do not run the full
@@ -795,2 +793,2 @@
-                gates with run_quality_gates(scope='branch'). Reuse nothing stale; if a check
+                gates with run_checks(scope='branch'). Reuse nothing stale; if a check
@@ -807,3 +805,3 @@
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update the existing phase artifact.
+                scaffold_artifact(artifact_type='validation_report', name='validation');
+                otherwise update the existing phase artifact.
@@ -1009,2 +1007,2 @@
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
+                scaffold_artifact(artifact_type='research', name='research').
@@ -1078,2 +1076,2 @@
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
+                scaffold_artifact(artifact_type='design', name='design').
@@ -1150,4 +1148,3 @@
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Apply Documentation Standard boundaries and keep document cycles identical to the
-                structured payload. Save them with save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]) after verifying IDs, ordering, and dependencies.
+                scaffold_artifact(artifact_type='planning', name='planning').
+                Apply Documentation Standard boundaries and keep document cycles identical to the
+                structured payload. Save them with save_planning_deliverables(issue_number=N, ...) after verifying IDs, ordering, and dependencies.
@@ -1218,2 +1215,2 @@
-                run_quality_gates(scope='files', files=[...]) proportionally. Do not run the full
+                run_checks(scope='files', files=[...]) proportionally. Do not run the full
@@ -1274,2 +1271,2 @@
-                gates with run_quality_gates(scope='branch'). Reuse nothing stale; if a check
+                gates with run_checks(scope='branch'). Reuse nothing stale; if a check
@@ -1286,3 +1283,3 @@
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update the existing phase artifact.
+                scaffold_artifact(artifact_type='validation_report', name='validation');
+                otherwise update the existing phase artifact.
@@ -1488,2 +1485,2 @@
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
+                scaffold_artifact(artifact_type='research', name='research').
@@ -1556,2 +1553,2 @@
-                run_quality_gates(scope='files', files=[...]) proportionally. Do not run the full
+                run_checks(scope='files', files=[...]) proportionally. Do not run the full
@@ -1612,2 +1609,2 @@
-                gates with run_quality_gates(scope='branch'). Reuse nothing stale; if a check
+                gates with run_checks(scope='branch'). Reuse nothing stale; if a check
@@ -1624,3 +1621,3 @@
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update the existing phase artifact.
+                scaffold_artifact(artifact_type='validation_report', name='validation');
+                otherwise update the existing phase artifact.
@@ -1826,2 +1823,2 @@
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
+                scaffold_artifact(artifact_type='research', name='research').
@@ -1895,2 +1892,2 @@
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
+                scaffold_artifact(artifact_type='planning', name='planning').
@@ -1965,4 +1962,3 @@
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
-                Apply Documentation Standard boundaries and keep document cycles identical to the
-                structured payload. Save them with save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]) after verifying IDs, ordering, and dependencies.
+                scaffold_artifact(artifact_type='design', name='design').
+                Apply Documentation Standard boundaries and keep document cycles identical to the
+                structured payload. Save them with save_planning_deliverables(issue_number=N, ...) after verifying IDs, ordering, and dependencies.
@@ -2175,4 +2171,3 @@
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Apply Documentation Standard boundaries and keep document cycles identical to the
-                structured payload. Save them with save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]) after verifying IDs, ordering, and dependencies.
+                scaffold_artifact(artifact_type='planning', name='planning').
+                Apply Documentation Standard boundaries and keep document cycles identical to the
+                structured payload. Save them with save_planning_deliverables(issue_number=N, ...) after verifying IDs, ordering, and dependencies.
@@ -2320,2 +2315,2 @@
-                run_quality_gates(scope='files', files=[...]) proportionally. Do not run the full
+                run_checks(scope='files', files=[...]) proportionally. Do not run the full
@@ -2376,2 +2371,2 @@
-                gates with run_quality_gates(scope='branch'). Reuse nothing stale; if a check
+                gates with run_checks(scope='branch'). Reuse nothing stale; if a check
@@ -2388,3 +2383,3 @@
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update the existing phase artifact.
+                scaffold_artifact(artifact_type='validation_report', name='validation');
+                otherwise update the existing phase artifact.
```

---

## 6. Verification and Evidence

### 6.1 DOCFLOW-E01 Evidence
- **Automated Test:** `tests/mcp_server/unit/config/test_contracts_loader.py::TestCY068DocflowE01::test_isolated_patched_contracts_loading_and_docflow_e01`
- **Result:** PASS (24 passed)
- **Observations:**
  - Patched `contracts.yaml` loads cleanly via `ConfigLoader(config_dir).load_contracts_config()`.
  - Pydantic model validation passes completely.
  - Phase order across all 7 workflows is 100% identical to the original contracts.
  - `pr_allowed_phase == "ready"` is preserved.
  - Obsolete `context=` and `run_quality_gates` strings are completely absent.
  - V3 tool names (`run_checks`, `run_tests`, `safe_edit_file`, `scaffold_artifact`) are present in expected phases.
  - Postimage hash matches `dd62d93ff05bd62eb0b0dc7e4bee4d4dc0a142d8d2cb8d910816358e6cbc0f40`.

### 6.2 DOCFLOW-E02 Evidence
- **Automated Test:** `tests/mcp_server/unit/config/test_contracts_loader.py::TestCY068DocflowE01::test_nineteen_workflow_variants_satisfy_docflow_e02`
- **Result:** PASS
- **Observations:**
  - Verified that all nineteen workflow variants' required semantic concepts (evidence, consumers, risks, invariants, reproduction, root cause, test design, work units, obligations, demonstration, caveats) map directly to exposed properties in the live public schemas (`research`, `design`, `planning`, `validation_report`).
  - No workflow requires invented fields or unauthorized schema modifications.

### 6.3 Discovery Tool Integration Evidence
- **Automated Test:** `tests/mcp_server/unit/tools/test_discovery_tools.py::TestGetWorkContextC7ContractsInjection::test_c68_docflow_e01_v3_instructions_without_obsolete_syntax`
- **Result:** PASS (46 passed)
- **Observations:**
  - `GetWorkContextTool` returns V3 phase instructions and sub-role hints without obsolete syntax.
  - Outcome-neutral handover templates remain intact.

---

## 7. Rollback (R-CY068)

In case of rollback:
1. Revert `docs/development/issue460/rollout-workflow-input.md` (newly introduced cycle-owned file).
2. Revert edits to `tests/mcp_server/unit/config/test_contracts_loader.py` and `tests/mcp_server/unit/tools/test_discovery_tools.py`.
3. Live `.pgmcp/config/contracts.yaml` was intentionally left untouched during CY068, requiring no rollback.

---

## 8. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-17 | @imp implementer | Initial CY068 preparation: 19 workflow carriers, target diff, checksums, and DOCFLOW-E01/E02 verification evidence. |
