<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# Issue 472 — Public-tool audit validation

**Status:** PARTIAL — accepted verification limits  
**Version:** 1.0  
**Last Updated:** 2026-10-07

## Purpose

Durable record of the six guided public-tool demonstrations. Observations below were made on 2026-10-07; candidate code is commit 94bdbe5, with the evidence-rule change in 2ff197ae. This report makes no claim of full-suite verification.

## Issue Number

#472

## Validation Status

PARTIAL

## Scope

Approved boundary: audit the six replaced V3 routes and the get_project_plan/create_issue seams of #460; retain the approved one-line syntax diagnostic correction and one documentation rule. No compatibility layer, new tests, V2 environment repair, stricter Pyright policy, expanded typecheck selection, or output-size investigation. The human explicitly approved only this compact report, push and Ready closeout, with no further tests, evidence artifacts or repairs.

## Demonstration

| Route / invocation or reproduction | Observed result |
|---|---|
| `scaffold_schema` for `generic_doc` and `python_pydantic_dto`; `scaffold_artifact` with those types, explicit `.pgmcp/temp/issue472/block1-v3` target, `force_target=true`, `validation="enforce"`, schema-complete contexts (DTO class `Block1DemoDTO`, integer `value`, example `{"value":7}`) | Both artifacts written; native preflight passed. Omitting document `purpose` returned `context_invalid`, `written=false`; no invalid artifact created. |
| `safe_edit_file`: replace `class Block1DemoDTO(BaseModel):` with the same line without `:`, first `enforce`, then `report` | Enforce: `validation_blocked`, no write. Report: written with failed syntax result `expected ':'`. Original bytes restored. |
| Repeat that enforce edit after the one-line adapter correction in `94bdbe5` | Correct evidence: `source: class Block1DemoDTO(BaseModel)`; error unchanged; original file untouched. Existing syntax diagnostic test selected below passed. |
| `run_checks(scope="targets", targets=[temporary DTO], checks=["python_format","python_lint"])`; then `scope="branch", checks=["python_format","python_lint","markdown_links"]` | Both runs passed. Branch included code, Markdown and workflow JSON: Ruff reported one Python file; Lychee reported four successful links, zero errors. |
| `run_checks(scope="targets", targets=["tests/mcp_server/validation_fixtures/gate0_format_violation.py"], checks=["python_format"])` | Native Ruff checked one file despite its configured exclusion. File was already formatted; no intentional violation was inferred. |
| `run_checks(scope="configured", checks=["python_format"], args={"python_format":["mcp_server/bundled_adapters/python_syntax/check.py"]})` | Passed, one file checked. This bounded native-argument demonstration was not a workspace-wide default configured run. |
| `run_tests(scope="targets", tests=["python_tests"], targets=["tests/mcp_server/unit/execution/test_check_selection.py"], args={"python_tests":["-k", "<two names below>"]})` | Two existing tests passed: `test_branch_configured_targets_and_explicit_intent` and `test_configured_empty_targets_still_plan_checks_but_empty_branch_has_no_calls`. Pytest 9.0.2, native exit 0. |
| Replace the temporary DTO's class description double quotes with single quotes; `run_checks` → `apply_fixes(scope="targets", fixes=["python_format"], targets=[temporary DTO])` → same check | Check failed with the correct diff; Ruff 0.15.6 fixed one file, exit 0; separate recheck passed. Final 592 bytes equal original. Fixing did not imply an automatic post-check. |
| `get_project_plan(issue_number=472)` | Returned chore phases, Research active at observation time, and `planning_deliverables=null`. Stored-plan integration below covered populated data and fresh bootstrap. |

All focused calls used explicit budgets of 120–240 seconds; no timeout was induced. Temporary DTO path: `.pgmcp/temp/issue472/block1-v3/block1_demo_dto.py`.

## Preservation

Additional existing tests were run through `run_tests(scope="targets", tests=["python_tests"], args={"python_tests":["-k", "<listed names joined with or>"]})`:
- `tests/mcp_server/integration/adapters/test_python_syntax.py`: `test_syntax_error_keeps_complete_content_location_and_logical_filename` — passed; targeted Ruff format/lint on the changed adapter also passed.
- `tests/mcp_server/integration/test_create_issue_e2e.py`: `test_minimal_input_creates_issue_with_correct_labels`, `test_all_options_creates_issue_with_full_label_set`; `tests/mcp_server/integration/test_project_plan_readback.py`: `test_stored_planning_survives_fresh_bootstrap_cache` variants 3 and 117 — four passed, native exit 0. A fresh bootstrap invalidated the old cache URI while a new public call recovered complete persisted planning.
- `tests/mcp_server/integration/templates/test_issue.py`: `test_minimal_issue_body_has_no_h1_and_keeps_saved_header`, `test_issue_preserves_optional_values_order_and_related_reference_namespace`; `tests/mcp_server/unit/tools/test_issue_tools.py`: `test_create_issue_input_body_is_str`, `test_create_issue_input_body_rejects_dict` — four passed, native exit 0. No real GitHub publication; existing create_issue cases used controlled manager doubles. These cases do not establish byte-exact end-to-end publication fidelity.

## Containment

Documentation reviewed: the single Documentation Standard evidence rule is the only active-doc change; other agent instructions, contracts, references and historical documents need no update for these delivered changes. #485 is included through this human-approved minimal rule; Coordination should align its broader issue wording with that approved outcome. No additional repair work identified within the approved boundary.

## Caveats

- Human-approved exception to the Chore Validation contract: no new configured full-suite run, full Python branch-profile run, timeout/interruption/partial-write matrix, or extra checks will be performed for closeout. Existing evidence is reused; PARTIAL is an explicit coverage limit, not a claim that unexecuted obligations passed.
- Installed V2 is phase-gate-mcp 2.0.0 at C:/1Voudig/99_Programming/ST. Schema/scaffold and edit demonstrations ran. Original V2 check 'passes' were corrected: run_quality_gates(scope='files', files=['.pgmcp/temp/issue472/block1-v2/block1_demo_dto.py'], verbose=true) reported passed while Ruff/Pyright exited 1 with 'No module named ...'. run_tests(path='tests/backend/utils/test_id_generators.py', timeout=180, verbose=true) likewise ran zero tests because Pytest was absent. These are not successful native checks or a working performance/strictness benchmark.
- V2 strict edit recovery reproduced CRCRLF expansion; strict rewrite with LF-normalized original text recovered exact original bytes. No repair was requested.
- No additional V3 failure remains demonstrated. Remaining unexercised paths are accepted limits, not newly opened repair issues. Existing SchemaAttachment field-shadow and read_resource deprecation warnings were observed; no warning cleanup was undertaken.

## Related Documents

- [Syntax adapter](<../../../mcp_server/bundled_adapters/python_syntax/check.py>)
- [Documentation evidence rule](<../../coding_standards/DOCUMENTATION_STANDARD.md>)
- [Original issue scope](<https://github.com/MikeyVK/phase-gate-mcp/issues/472>)
- [Evidence-rule issue](<https://github.com/MikeyVK/phase-gate-mcp/issues/485>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-07 | @imp validator | Record existing observations and the human-approved minimal closeout. |
