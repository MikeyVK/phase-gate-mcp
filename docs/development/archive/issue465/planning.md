<!-- pgmcp:v1 id=planning pv=1.0.0 pf=K72uxa-fhywx1wo8 sf=zJbLuUrs_I33kpX4 -->

# Issue 465 — bounded artifact-family implementation plan

**Status:** Planning complete — independent review pending  
**Version:** 0.1  
**Last Updated:** 2026-10-11

## Purpose

Make the approved design executable without reopening its architecture or strategy.

## Scope In

Shared YAML emission/JSON framing and reader; native adapter/configuration; four packages; focused behavior coverage, per-issue Validation and active documentation.

## Scope Out

Legacy bridges, old-format rejection tests, snapshots, automatic ADR lifecycle/synchronization, custom directory expansion and template-compliance engine.

## Prerequisites

- Research v0.6 and Design v0.1 are binding.
- Independent Design → Planning GO on 2b401d70a7d8e2d8d80b7dcf6c4a5df652a1fd42.
- Use public boundaries and tmp_path; do not touch live workflow files in tests.

## Summary

Deliver the approved #465/#484/#498 design in three dependency-ordered behavioral cycles. Independent QA reviews every phase boundary; one full suite belongs to Validation.

## Dependencies

- C_2 follows C_1; C_3 follows C_2. Source packages can then refer to admitted native profiles.
- Install the exact adapter requirements before native behavior evidence. Verify the interpreter selected by the existing runtime.
- New package/configuration/Jinja assets have no matching live scaffold family yet; author those source assets directly. Scaffold new Python/test/doc modules with the existing admitted packages, then refine through safe_edit_file.

## Risks

### Mixed branch inventory is misrouted or native configured input lacks files.

At Validation run run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','markdown_links','yaml_configuration','json_schema_shape','json_schema_metaschema'], timeout_seconds=900). The existing per-capability branch policies preselect admitted file types. Additionally run run_checks(scope='configured', profile='python_review', timeout_seconds=900) for workspace Python baseline; do not include new files-required checks in this empty configured route.

### Native dependency/parser baseline or shared-root changes invalidate wider consumers.

At Validation execute one run_tests(scope='configured', timeout_seconds=1800), retaining native arguments; do not split solely for timeout. Include actual emitted-file native checks, real consumer evidence, effective nested-field review and assembled asset inspection. Reuse earlier evidence only while its inputs remain unchanged.

## Work Units

### C\_1 — Shared rendering and provenance

**Goal:** Focused rendering/reader tests pass after observed RED; changed Python format/lint/pyright checks pass. Existing shared-tier consumers remain covered.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Deliverables

##### D\_1.1

Pure PyYAML 6.0.3 serializer with the real toyaml filter and supported data round-trip behavior.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/services/yaml_serialization.py"

##### D\_1.2

Shared artifact_frame and JSON base; bounded first-root-$comment reader using the existing record/model with adapted public tests.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/template_suite/shared/templates/bases/tier1_json_object.jinja2"

#### Exit Criteria

Focused rendering/reader tests pass after observed RED; changed Python format/lint/pyright checks pass. Existing shared-tier consumers remain covered.

#### Dependencies

#### Obligations

- RED → GREEN for durable new behavior; no artificial RED for manifest/config mechanics. Commit the narrow red/green boundaries; refactor only if actual cleanup is needed.
- Respect the approved package/generic/adapter ownership. No pgmcp application rules or hidden discovery in the adapter.
- Prefer existing tests/helpers; new organizational modules at most the four defined by Design. Tests assert behavior rather than complete artifact content.

#### Verification

##### Focused tests

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/services/test_artifact_header_reader.py','tests/mcp_server/unit/services/test_edit_construction.py','tests/mcp_server/unit/services/test_template_engine.py','tests/mcp_server/integration/templates/test_shared_python.py','tests/mcp_server/integration/templates/test_shared_documents.py'], timeout_seconds=600). Add the serializer case to test_template_engine.py.

**Expected Result:** Observed intended RED then complete focused GREEN; failures are substantive, not omitted or normalized away.

##### Changed Python quality

**Method:** Use repository diff selection to select the changed .py/.pyi files; run_checks(scope='targets', targets=that list, checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). No Markdown/Jinja/YAML/JSON targets enter Python gates.

**Expected Result:** All applicable changed-file checks pass; reuse valid evidence.

#### Stop Conditions

- Stop and request targeted correction if an approved contract is impossible or tests need architectural violations.
- Unavailable native prerequisites, missing instance operands or incomplete results never count as pass.

### C\_2 — Native source-family checks

**Goal:** Declared prerequisites installed in the actual adapter interpreter; focused adapter tests demonstrate actual pass/fail and unusable inputs after RED; targeted Python gates pass.

**Cycle Number:** 2

**Owner:** @imp implementer

#### Deliverables

##### D\_2.1

Package-local check/v1 adapter, exact dependency baseline, native diagnostics, files-only routes and read-only argument boundary.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/bundled_adapters/check_jsonschema/check.py"

##### D\_2.2

YAML/JSON capabilities, three checks, two native schemas/profiles and branch filters; existing default profile remains.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/config/check_schemas/json_schema_source.schema.json"

#### Exit Criteria

Declared prerequisites installed in the actual adapter interpreter; focused adapter tests demonstrate actual pass/fail and unusable inputs after RED; targeted Python gates pass.

#### Dependencies

- C_1

#### Obligations

- RED → GREEN for durable new behavior; no artificial RED for manifest/config mechanics. Commit the narrow red/green boundaries; refactor only if actual cleanup is needed.
- Respect the approved package/generic/adapter ownership. No pgmcp application rules or hidden discovery in the adapter.
- Prefer existing tests/helpers; new organizational modules at most the four defined by Design. Tests assert behavior rather than complete artifact content.

#### Verification

##### Focused tests

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/integration/adapters/test_check_jsonschema.py'], timeout_seconds=600); actual native prerequisites must be available.

**Expected Result:** Observed intended RED then complete focused GREEN; failures are substantive, not omitted or normalized away.

##### Changed Python quality

**Method:** Use repository diff selection to select the changed .py/.pyi files; run_checks(scope='targets', targets=that list, checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). No Markdown/Jinja/YAML/JSON targets enter Python gates.

**Expected Result:** All applicable changed-file checks pass; reuse valid evidence.

#### Stop Conditions

- Stop and request targeted correction if an approved contract is impossible or tests need architectural violations.
- Unavailable native prerequisites, missing instance operands or incomplete results never count as pass.

### C\_3 — Four delivered artifact packages

**Goal:** Focused new-family/mutation and shared-tier tests pass after meaningful RED; native checks and linked-pair proof pass; no blocked promised behavior or architecture violation; changed Python gates pass.

**Cycle Number:** 3

**Owner:** @imp implementer

#### Deliverables

##### D\_3.1

Complete named packages, configured authoring roots and emitted minimal/populated examples, parsed semantics, actual consumer and suite-only extension evidence.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/template_suite/json_schema/template.jinja2"

##### D\_3.2

Markdown-tier packages, effective nested consumption, draft carriers, actual link pair and co-located source/license attribution.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/template_suite/sad/template.jinja2"

**Integration correction:** The exact component license and attribution are retained in non-rendered comments in this owning generation source; cold suite admission rejects auxiliary `.txt` files. No cycle, deliverable scope or exit criterion changes.

##### D\_3.3

Public scaffold/edit native evidence for enforce/report, original identity/suffix routing and isolated proposed content, with no live workflow-file writes.

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_data_artifact_mutations.py"

#### Exit Criteria

Focused new-family/mutation and shared-tier tests pass after meaningful RED; native checks and linked-pair proof pass; no blocked promised behavior or architecture violation; changed Python gates pass.

#### Dependencies

- C_2

#### Obligations

- RED → GREEN for durable new behavior; no artificial RED for manifest/config mechanics. Commit the narrow red/green boundaries; refactor only if actual cleanup is needed.
- Respect the approved package/generic/adapter ownership. No pgmcp application rules or hidden discovery in the adapter.
- Prefer existing tests/helpers; new organizational modules at most the four defined by Design. Tests assert behavior rather than complete artifact content.

#### Verification

##### Focused tests

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/integration/templates/test_data_artifacts.py','tests/mcp_server/integration/templates/test_architecture_records.py','tests/mcp_server/integration/test_data_artifact_mutations.py','tests/mcp_server/integration/templates/test_shared_documents.py','tests/mcp_server/integration/templates/test_shared_python.py'], timeout_seconds=900); real native checker and Lychee executions are required.

**Expected Result:** Observed intended RED then complete focused GREEN; failures are substantive, not omitted or normalized away.

##### Changed Python quality

**Method:** Use repository diff selection to select the changed .py/.pyi files; run_checks(scope='targets', targets=that list, checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). No Markdown/Jinja/YAML/JSON targets enter Python gates.

**Expected Result:** All applicable changed-file checks pass; reuse valid evidence.

#### Stop Conditions

- Stop and request targeted correction if an approved contract is impossible or tests need architectural violations.
- Unavailable native prerequisites, missing instance operands or incomplete results never count as pass.

## Phase Deliverables

### Validation

#### D\_1

Compact durable report with separate #465/#484/#498 outcomes, full configured suite, correctly selected branch/configured gates, runtime demonstration and release review.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue465/validation.md"

### Documentation

#### D\_1

Targeted updates to current template provenance, scaffolding and adapter/native prerequisite references; no instruction rollout.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/template_metadata_format.md"

## Related Documents

- [Approved Design](<design.md>)
- [Approved Research](<research.md>)
- [Template maintenance procedure](<../../schema-template-maintenance.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-11 | @imp planner | Plan three coherent behavioral cycles, structured plan references and proportional phase-owned evidence. |
