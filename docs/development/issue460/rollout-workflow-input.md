<!-- docs\development\issue460\rollout-workflow-input.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T05:52Z updated=2026-09-17 -->
# Issue 460 Rollout Workflow Input: Nineteen Workflow Carriers and Phase Semantics

**Status:** IMPLEMENTATION EVIDENCE — REVIEW REQUESTED  
**Version:** 1.1  
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
- **Preimage SHA-256 (raw bytes, CRLF):** `9610d38bf943c687e8c200b626259b3f107b69d4e9d0a40e44f38c91f8194d10`
- **Postimage SHA-256 (UTF-8 text with LF line endings after universal-newline decoding):** `008a84d242a7fc5c3d56f211553348d5a820905874bf237dab42f90c01f2ce50`

### 5.2 Exact Patch (Unified Diff)
```diff
--- a/.pgmcp/config/contracts.yaml
+++ b/.pgmcp/config/contracts.yaml
@@ -47,11 +47,13 @@
                 "No special migration policy; preserve supported contracts" is valid when explicit.
                 Stop if scope, evidence, or strategy remains ambiguous.
 
-            [ ] Scaffold the research artifact with
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
-                Apply the relevant DOCUMENTATION_STANDARD boundaries and add concrete source links.
-                Self-check that claims are evidenced, test blast radius is explicit, and no design
-                or planning commitment leaked into Research.
+            [ ] Obtain the current Research context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Apply the relevant
+                DOCUMENTATION_STANDARD boundaries and add concrete source links. Self-check that
+                claims are evidenced, test blast radius is explicit, and no design or planning
+                commitment leaked into Research.
 
             [ ] Commit with git_add_or_commit(workflow_phase='research',
                 message='Research findings (#N)').
@@ -116,11 +118,13 @@
             [ ] Stop for a human decision if the Approved Strategy is missing, evidence makes it
                 unsound, or a major design choice cannot be resolved from approved constraints.
 
-            [ ] Scaffold the design artifact with
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
-                Record the chosen direction, rejected alternatives, production and test design,
-                validation obligations, risks, and planning consequences with source links.
-                Self-check phase and document boundaries.
+            [ ] Obtain the current Design context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Record the chosen
+                direction, rejected alternatives, production and test design, validation
+                obligations, risks, and planning consequences with source links. Self-check phase
+                and document boundaries.
 
             [ ] Commit with git_add_or_commit(workflow_phase='design',
                 message='Design for #N').
@@ -188,11 +192,13 @@
 
             [ ] Stop if Design or Approved Strategy is ambiguous, contradicted, or requires change.
 
-            [ ] Scaffold the plan with
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Apply Documentation Standard boundaries and keep document cycles identical to the
-                structured payload. Save them with save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]) after verifying IDs, ordering, and dependencies.
+            [ ] Obtain the current Planning context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Apply Documentation
+                Standard boundaries and keep document cycles identical to the structured payload.
+                Save them with save_planning_deliverables(issue_number=N, ...) after verifying IDs,
+                ordering, and dependencies.
 
             [ ] Commit with git_add_or_commit(workflow_phase='planning',
                 message='Planning for #N').
@@ -257,7 +263,7 @@
                   and commit with sub_phase='refactor' only when cleanup changed files
 
-            [ ] Use run_tests(path='<focused scope>') and
+            [ ] Use run_tests(scope='targets', targets=['tests/example_test.py']) and
-                run_quality_gates(scope='files', files=[...]) proportionally. Do not run the full
+                run_checks(scope='targets', targets=['src/example.py']) proportionally on affected files. Do not run the full
                 suite here; Validation owns the workspace-wide run.
 
             [ ] Perform a producer self-check against cycle deliverables, direct diff evidence,
@@ -313,7 +319,7 @@
                 high-risk production/test surface to observable evidence.
 
-            [ ] Run the single workspace-wide suite with run_tests(scope='full') and branch-wide
+            [ ] Run the single workspace-wide suite with run_tests(scope='workspace') and branch-wide
-                gates with run_quality_gates(scope='branch'). Reuse nothing stale; if a check
+                gates with run_checks(scope='branch'). Reuse nothing stale; if a check
                 fails, preserve exact evidence and report FAIL rather than weakening criteria.
 
             [ ] Add targeted validation only for a material gap not covered by the full checks.
@@ -324,12 +330,13 @@
             [ ] Identify residual risk, limitations, and deferred work explicitly, including
                 findings that Ready must transfer for @co triage.
 
-            [ ] Create the validation artifact if absent with
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update the existing phase artifact.
-                Record scope, exact outcomes, deliverable mapping, Design and Approved Strategy
-                alignment, demonstration/fallback, failures, caveats, and deferred work.
-                Do not claim independent QA approval.
+            [ ] Create the validation artifact if absent: obtain the context schema via
+                scaffold_schema if not already available, scaffold with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context, and refine
+                with safe_edit_file; otherwise update the existing phase artifact. A valid scaffold
+                is not phase completion. Record scope, exact outcomes, deliverable mapping, Design
+                and Approved Strategy alignment, demonstration/fallback, failures, caveats, and
+                deferred work. Do not claim independent QA approval.
 
             [ ] Commit with git_add_or_commit(workflow_phase='validation',
                 message='Validation for #N').
@@ -441,8 +448,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
@@ -517,11 +525,13 @@
                 defect is not evidenced, root cause remains materially ambiguous, issue scope
                 must change, or strategy is undecided.
 
-            [ ] Scaffold the research artifact with
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
-                Apply relevant Documentation Standard boundaries; link evidence and state
-                reproduction, root cause, blast radius, corrected behavior, risks, and strategy.
-                Keep fix design and planning out.
+            [ ] Obtain the current Research context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Apply relevant
+                Documentation Standard boundaries; link evidence and state reproduction, root
+                cause, blast radius, corrected behavior, risks, and strategy. Keep fix design and
+                planning out.
 
             [ ] Commit with git_add_or_commit(workflow_phase='research',
                 message='Research findings (#N)').
@@ -587,11 +597,13 @@
             [ ] Stop for human decision if root cause, corrected behavior, or Approved Strategy is
                 missing, contradicted, or made unsound by new evidence.
 
-            [ ] Scaffold the design artifact with
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
-                Record chosen correction, rejected alternatives, production/test design,
-                preservation obligations, validation evidence, and planning consequences.
-                Self-check phase and document boundaries.
+            [ ] Obtain the current Design context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Record chosen
+                correction, rejected alternatives, production/test design, preservation
+                obligations, validation evidence, and planning consequences. Self-check phase and
+                document boundaries.
 
             [ ] Commit with git_add_or_commit(workflow_phase='design',
                 message='Design for #N').
@@ -659,11 +671,12 @@
 
             [ ] Stop if Root Cause, Design, corrected behavior, or Approved Strategy conflicts.
 
-            [ ] Scaffold Planning with
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Keep document cycles identical to save_planning_deliverables(issue_number=N,
-                cycles={...}, deliverables=[...]); verify IDs, ordering, dependencies, regression
-                value, and cleanup ownership before saving.
+            [ ] Obtain the current Planning context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Keep document cycles
+                identical to save_planning_deliverables(issue_number=N, ...); verify IDs, ordering,
+                dependencies, regression value, and cleanup ownership before saving.
 
             [ ] Commit with git_add_or_commit(workflow_phase='planning',
                 message='Planning for #N').
@@ -730,7 +743,7 @@
                   sub_phase='refactor' only when files changed
 
-            [ ] Use run_tests(path='<focused scope>') and
+            [ ] Use run_tests(scope='targets', targets=['tests/example_test.py']) and
-                run_quality_gates(scope='files', files=[...]) proportionally. Validation owns the
+                run_checks(scope='targets', targets=['src/example.py']) proportionally on affected files. Validation owns the
                 full suite and branch-wide gates.
 
             [ ] Self-check the diff against root cause, corrected behavior, cycle deliverables,
@@ -786,7 +799,7 @@
                 preservation constraints, and high-risk production/test surfaces to evidence.
 
-            [ ] Run the single workspace-wide suite with run_tests(scope='full') and branch-wide
+            [ ] Run the single workspace-wide suite with run_tests(scope='workspace') and branch-wide
-                gates with run_quality_gates(scope='branch'). Preserve exact failures and report
+                gates with run_checks(scope='branch'). Preserve exact failures and report
                 FAIL; do not weaken criteria or reinterpret the plan.
 
             [ ] Explicitly rerun the durable regression/reproduction scope if the full suite does
@@ -796,12 +809,13 @@
 
             [ ] Identify residual risks, limitations, and deferred work for Ready/@co triage.
 
-            [ ] Create Validation if absent with
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update it. Record exact full-suite/gate/regression
-                results, root-cause and corrected-behavior proof, deliverable/design/strategy
-                mapping, demonstration/fallback, failures, caveats, and deferred work.
-                Do not claim independent QA approval.
+            [ ] Create Validation if absent: obtain the context schema via scaffold_schema if not
+                already available, scaffold with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context, and refine
+                with safe_edit_file; otherwise update it. A valid scaffold is not phase completion.
+                Record exact full-suite/gate/regression results, root-cause and corrected-behavior
+                proof, deliverable/design/strategy mapping, demonstration/fallback, failures,
+                caveats, and deferred work. Do not claim independent QA approval.
 
             [ ] Commit with git_add_or_commit(workflow_phase='validation',
                 message='Validation for #N').
@@ -911,8 +925,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
@@ -988,7 +1003,7 @@
                   files changed
 
-            [ ] Use run_tests(path='<focused scope>') and
+            [ ] Use run_tests(scope='targets', targets=['tests/example_test.py']) and
-                run_quality_gates(scope='files', files=[...]) proportionally. Validation owns the
+                run_checks(scope='targets', targets=['src/example.py']) proportionally on affected files. Validation owns the
                 full suite and branch-wide gates.
 
             [ ] Self-check failure correction, containment, rollback exposure when relevant,
@@ -1042,7 +1057,7 @@
                 slice exit criteria, and high-risk production/test surfaces to evidence.
 
-            [ ] Run the single workspace-wide suite with run_tests(scope='full') and branch-wide
+            [ ] Run the single workspace-wide suite with run_tests(scope='workspace') and branch-wide
-                gates with run_quality_gates(scope='branch'). Preserve exact failures and report
+                gates with run_checks(scope='branch'). Preserve exact failures and report
                 FAIL rather than weakening criteria. Explicitly rerun the focused hotfix regression
                 if the full suite does not expose corrected behavior.
 
@@ -1051,11 +1066,13 @@
                 reviewable fallback. Identify deferred work for Ready/@co triage; keep nonessential
                 cleanup outside the hotfix.
 
-            [ ] Create Validation if absent with
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update it. Record exact tests/gates/regression evidence,
-                correction and containment mapping, demonstration/fallback, failures, rollback
-                notes, caveats, and deferred work. Do not claim independent QA approval.
+            [ ] Create Validation if absent: obtain the context schema via scaffold_schema if not
+                already available, scaffold with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context, and refine
+                with safe_edit_file; otherwise update it. A valid scaffold is not phase completion.
+                Record exact tests/gates/regression evidence, correction and containment mapping,
+                demonstration/fallback, failures, rollback notes, caveats, and deferred work. Do
+                not claim independent QA approval.
 
             [ ] Commit with git_add_or_commit(workflow_phase='validation',
                 message='Validation for #N').
@@ -1163,8 +1180,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
@@ -1238,11 +1256,13 @@
                 boundary; preserving supported behavior without a bridge is valid when explicit.
                 Stop on scope drift, ambiguous invariants, or undecided strategy.
 
-            [ ] Scaffold Research with
-                scaffold_artifact(artifact_type='research', name='research', context={...}).
-                Apply Documentation Standard boundaries; link evidence and record current
-                structure, invariants, blast radius, seams, risks, expected outcomes, and strategy.
-                Keep target design and cycles out.
+            [ ] Obtain the current Research context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Apply Documentation
+                Standard boundaries; link evidence and record current structure, invariants, blast
+                radius, seams, risks, expected outcomes, and strategy. Keep target design and
+                cycles out.
 
             [ ] Commit with git_add_or_commit(workflow_phase='research',
                 message='Research findings (#N)').
@@ -1308,10 +1328,12 @@
             [ ] Stop for human decision if invariants or Approved Strategy are missing/unsound, or
                 the target necessarily changes supported behavior.
 
-            [ ] Scaffold Design with
-                scaffold_artifact(artifact_type='design', name='design', context={...}).
-                Record target/rejected structures, preservation mapping, production/test design,
-                transition/cleanup, validation obligations, risks, and planning consequences.
+            [ ] Obtain the current Design context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Record target/rejected
+                structures, preservation mapping, production/test design, transition/cleanup,
+                validation obligations, risks, and planning consequences.
 
             [ ] Commit with git_add_or_commit(workflow_phase='design',
                 message='Design for #N').
@@ -1378,10 +1400,12 @@
 
             [ ] Stop if target Design, invariants, or Approved Strategy conflict.
 
-            [ ] Scaffold Planning with
-                scaffold_artifact(artifact_type='planning', name='planning', context={...}).
-                Keep cycles identical to save_planning_deliverables(issue_number=N, cycles={...},
-                deliverables=[...]); verify order, IDs, preservation, cleanup, and dependencies.
+            [ ] Obtain the current Planning context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Keep cycles identical to
+                save_planning_deliverables(issue_number=N, ...); verify order, IDs, preservation,
+                cleanup, and dependencies.
 
             [ ] Commit with git_add_or_commit(workflow_phase='planning',
                 message='Planning for #N').
@@ -1444,7 +1468,7 @@
                   rerun focused tests and file gates, and commit sub_phase='refactor' when changed
 
-            [ ] Use run_tests(path='<focused scope>') and
+            [ ] Use run_tests(scope='targets', targets=['tests/example_test.py']) and
-                run_quality_gates(scope='files', files=[...]) proportionally. Validation owns the
+                run_checks(scope='targets', targets=['src/example.py']) proportionally on affected files. Validation owns the
                 full suite and branch gates.
 
             [ ] Self-check diff purity, responsibility/dependency direction, invariants, behavior,
@@ -1499,7 +1523,7 @@
                 Inspect for remnants, dependency-direction violations, and test/helper coupling.
 
-            [ ] Run the single workspace-wide suite with run_tests(scope='full') and branch-wide
+            [ ] Run the single workspace-wide suite with run_tests(scope='workspace') and branch-wide
-                gates with run_quality_gates(scope='branch'). Preserve exact failure evidence and
+                gates with run_checks(scope='branch'). Preserve exact failure evidence and
                 report FAIL rather than weakening preservation criteria.
 
             [ ] Add targeted structural/characterization checks only for material proof gaps.
@@ -1508,11 +1532,13 @@
 
             [ ] Identify residual coupling, caveats, and deferred work for Ready/@co triage.
 
-            [ ] Create Validation if absent with
-                scaffold_artifact(artifact_type='validation_report', name='validation',
-                context={...}); otherwise update it. Record exact suite/gate results, deliverable
-                and cleanup mapping, invariant/behavior/design/strategy alignment, structural
-                checks, failures, demonstration/fallback, risks, and deferred work.
+            [ ] Create Validation if absent: obtain the context schema via scaffold_schema if not
+                already available, scaffold with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context, and refine
+                with safe_edit_file; otherwise update it. A valid scaffold is not phase completion.
+                Record exact suite/gate results, deliverable and cleanup mapping,
+                invariant/behavior/design/strategy alignment, structural checks, failures,
+                demonstration/fallback, risks, and deferred work.
 
             [ ] Commit with git_add_or_commit(workflow_phase='validation',
                 message='Validation for #N').
@@ -1621,8 +1647,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
@@ -1695,12 +1722,11 @@
                 outcome, review proof, and consistency risks.
                 Do not hide implementation or redesign work in the plan.
 
-            [ ] Call scaffold_schema(artifact_type='planning'), then scaffold and complete
-                the Planning artifact with schema-complete evidence:
-                scaffold_artifact(artifact_type='planning', name='planning',
-                context={...}).
-                Verify boundary, source mapping, dependencies, review criteria,
-                and Documentation Standard compliance.
+            [ ] Obtain the current Planning context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Verify boundary, source
+                mapping, dependencies, review criteria, and Documentation Standard compliance.
 
             [ ] Commit with git_add_or_commit(workflow_phase='planning',
                 message='Planning for #N').
@@ -1819,8 +1845,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
@@ -1956,7 +1983,7 @@
                 stale terms, missed consumers, and unsupported claims.
             [ ] After final implementation changes run once:
-                - run_tests(scope='full')
+                - run_tests(scope='workspace')
-                - run_quality_gates(scope='branch', verbose=True)
+                - run_checks(scope='branch')
                 Read both cached resources. Add narrow checks only for a material gap;
                 do not duplicate fresh evidence.
             [ ] Explain failures directly. Do not accept stale/unexplained broad results
@@ -2059,8 +2086,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
@@ -2130,13 +2158,14 @@
                 Obtain and capture human Approved Strategy.
                 Stop if the epic must be narrowed, split, reframed, or lacks a decision.
 
-            [ ] Call scaffold_schema(artifact_type='research'), then
-                scaffold_artifact(artifact_type='research', name='research',
-                context={...}) with schema-complete evidence. Complete Research with
-                initiative framing, candidate workstreams, blast radius, dependencies,
-                shared proof obligations,
-                assumptions/risks, Approved Strategy, and expected Planning inputs.
-                Keep child issue creation, selected decomposition, design, and execution out.
+            [ ] Obtain the current Research context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Complete Research with
+                initiative framing, candidate workstreams, blast radius, dependencies, shared
+                proof obligations, assumptions/risks, Approved Strategy, and expected Planning
+                inputs. Keep child issue creation, selected decomposition, design, and execution
+                out.
 
             [ ] Verify evidence traceability, boundary discipline, and applicable
                 Documentation Standard compliance. Commit with
@@ -2190,12 +2219,12 @@
                 Bounded discovery, when useful, must be neutral, source-citing,
                 uncertainty-bearing, producer-verified, and non-authoritative.
 
-            [ ] Call scaffold_schema(artifact_type='planning'), then
-                scaffold_artifact(artifact_type='planning', name='planning',
-                context={...}) with schema-complete evidence. Verify complete
-                Research/strategy traceability, non-overlapping child ownership,
-                executable dependencies,
-                and no hidden Design or implementation work.
+            [ ] Obtain the current Planning context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Verify complete
+                Research/strategy traceability, non-overlapping child ownership, executable
+                dependencies, and no hidden Design or implementation work.
 
             [ ] Present the decomposition and external mutations to the human.
                 After explicit confirmation, create the child issues with create_issue
@@ -2261,13 +2290,13 @@
                 findings/uncertainty, exclusions, and stop conditions; verify output.
                 Producer-owned review cannot return a verdict or drive progression.
 
-            [ ] Call scaffold_schema(artifact_type='design'), then
-                scaffold_artifact(artifact_type='design', name='design',
-                context={...}) with schema-complete evidence. Verify
-                Research/Planning/strategy traceability, child usability,
-                architecture/test quality, coordination
-                consequences, and applicable Documentation Standard compliance.
-                Commit with git_add_or_commit(workflow_phase='design',
+            [ ] Obtain the current Design context schema via scaffold_schema if not already
+                available. Create the initial document with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine it with
+                safe_edit_file. A valid scaffold is not phase completion. Verify
+                Research/Planning/strategy traceability, child usability, architecture/test
+                quality, coordination consequences, and applicable Documentation Standard
+                compliance. Commit with git_add_or_commit(workflow_phase='design',
                 message='Design for #N').
 
             [ ] Stop with the outcome-neutral review index below.
@@ -2404,8 +2433,9 @@
                 recommended follow-up, and existing issue reference or @co triage need.
                 Record "None identified" when the search finds none.
 
-            [ ] Scaffold the PR body:
-                scaffold_artifact(artifact_type='pr', name='pr', context={...}).
+            [ ] Obtain the PR context schema via scaffold_schema if not already available.
+                Scaffold the PR body with
+                scaffold_artifact using the selected artifact_type, output basename as file_name, and schema-complete context and refine with safe_edit_file.
                 Include delivered scope, exact verification evidence, closure claims,
                 residual risks, deferred work, tracking state, and links to primary artifacts.
                 Use only supported claims; stop if scope or closure intent is ambiguous.
```

---

## 6. Verification and Evidence

### 6.1 DOCFLOW-E01 Evidence
- **Automated Test:** `tests/mcp_server/unit/config/test_contracts_loader.py::TestCY068DocflowE01::test_isolated_patched_contracts_loading_and_docflow_e01`
- **Result:** PASS
- **Observations:**
  - Patched `contracts.yaml` loads cleanly via `ConfigLoader(config_dir).load_contracts_config()`.
  - Pydantic model validation passes completely.
  - Phase order across all 7 workflows is 100% identical to the original contracts.
  - `pr_allowed_phase == "ready"` is preserved.
  - Obsolete `context=` and `run_quality_gates` strings are completely absent.
  - V3 tool names (`run_checks`, `run_tests`, `safe_edit_file`, `scaffold_artifact`) are present in expected phases.
  - Postimage hash matches `008a84d242a7fc5c3d56f211553348d5a820905874bf237dab42f90c01f2ce50`.

### 6.2 DOCFLOW-E02 Evidence
- **Automated Test:** `tests/mcp_server/unit/config/test_contracts_loader.py::TestCY068DocflowE01::test_nineteen_workflow_variants_satisfy_docflow_e02`
- **Result:** PASS
- **Observations:**
  - Verified that all four underlying document carrier templates (`research`, `design`, `planning`, `validation_report`) render cleanly without Jinja errors when supplied with representative semantic payloads covering the 19 workflow variants.
  - Scaffolded outputs contain valid Markdown section structure and represent the essential meaning without invented fields.

### 6.3 Discovery Tool Integration Evidence
- **Automated Test:** `tests/mcp_server/unit/tools/test_discovery_tools.py::TestGetWorkContextC7ContractsInjection::test_c68_docflow_e01_v3_instructions_without_obsolete_syntax`
- **Result:** PASS
- **Observations:**
  - `GetWorkContextTool` executes against the verified patched contracts configuration.
  - Returns V3 phase instructions and sub-role hints without obsolete syntax.
  - Outcome-neutral handover templates remain intact.

---

## 7. Rollback (R-CY068)

In case of rollback:
- **Pre-cycle Git Commit SHA:** `a365a63ac8c482770fe2bd76542efea3b9a4afb7`
1. Revert `docs/development/issue460/rollout-workflow-input.md` (newly introduced cycle-owned file).
2. Revert edits to `tests/mcp_server/unit/config/test_contracts_loader.py` and `tests/mcp_server/unit/tools/test_discovery_tools.py`.
3. Live `.pgmcp/config/contracts.yaml` was intentionally left untouched during CY068, requiring no rollback.

---

## 8. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-17 | @imp implementer | Initial CY068 preparation: 19 workflow carriers, target diff, checksums, and DOCFLOW-E01/E02 verification evidence. |
| 1.1 | 2026-09-17 | @imp implementer | Aligned exact patch and postimage checksum across all 7 workflows, added pre-cycle commit SHA, and verified forward patch application against hashes. |
