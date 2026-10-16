<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 505 — Asset assembly validation

**Status:** VALIDATION — PASS, QA REVIEW REQUESTED  
**Version:** 0.2  
**Last Updated:** 2026-10-16

## Purpose

Record the fail-closed builder correction, the owner-approved test-consumer repair and actual complete Validation outcomes. Preserve the first failed attempt and its disposition.

## Scope In

C_1 builder admission, filesystem ownership and error behavior; C_2 explicit test preparation and current keyed/id/order consumers; the complete native suite and planned gates.

## Scope Out

No new production architecture, manifest/content routing, native configuration or timeout policy change, release/version bump, repository release build or deployment. C_2 changes tests only.

## Issue Number

#505

## Cycle

C_1 — bounded_assembly_safety; C_2 — current_config_test_consumers.

## Validation Status

PASS — producer evidence complete; independent Validation review requested.

## Scope

Branch bug/505-fail-closed-asset-assembly, parent main. Current tested snapshot: **8eb60cca10b87fb02afcc0064d72f47d3829ae58**. C_1 final correction: db50b1d868e6b0506bda32c07b71cc4a67b07b8d. C_2 Planning: bfab9acc17bf5b579d4a0e27b0b01f89e6fb8b48. No production or test edits followed the current full run.

## Obligations

| Deliverable | Evidence and outcome |
| --- | --- |
| C_1 / D_1.1 — fail_closed_assembly | [Builder](../../../scripts/build_package.py): all mappings admitted before effects; explicit disposable output; original exceptions/notes; no success/build after assembly failure. |
| C_1 / D_1.2 — assembly_behavior_evidence | [Existing builder tests](../../../tests/mcp_server/unit/test_build_package.py): 29 public behavior cases, including real cleanup/link proof, pass in focused and complete runs. |
| C_2 / D_2.1 — explicit_fixture_and_consumer_adoption | [Opt-in config fixture](../../../tests/mcp_server/fixtures/suite_roots.py) and the exact 26 modules in [Planning](planning.md): explicit defaults preparation and current keyed/id/order consumers. No added/removed test functions, weakened behavior assertions, skips, suppressions or hidden loader/factory writes. |
| C_2 / D_2.2 — cli_and_handshake_diagnosis | [Renewal CLI](../../../tests/mcp_server/integration/test_renewal_cli.py) reaches its intended branches after admission repair; [startup tests](../../../tests/mcp_server/integration/test_target_startup.py) pass without speculative timeout/environment/production changes. Original source-handshake timeout remains unexplained and unreproduced. |
| Validation / D_1 — assembly_validation | Complete native run passes; planned branch gates and configured production Mypy pass with the execution distinctions below. |

## Evidence

### C_1 corrected behavior and causal RED

The initial focused run produced **23 failed, 6 passed, 9 warnings**. It exposed skipped invalid mappings, cleanup before source validation, absent path/overlap/link protection, suppressed cleanup errors and diagnostic gaps. An unsafe overlap probe was stabilized by spying on the directory-copy action instead of allowing recursion; that pair then failed with DID NOT RAISE ValueError. RED commit c6b7b018; supplemental operations f54d6cea and 2f1849da.

Exact reproduction:

```text
run_tests(scope="targets", targets=["tests/mcp_server/unit/test_build_package.py"],
          tests=["python_tests"], timeout_seconds=180)
# Stabilized RED overlap pair additionally used:
args={"python_tests": ["-k", "overlap"]}
```

After correction, the same complete module passed **29 tests, 9 SchemaAttachment.schema warnings, exit 0, 9.41s** (358931d5). QA's evidence correction makes the rmtree case create child.txt and inject PermissionError through shutil.os.unlink beneath real rmtree; it asserts the original exception, notes and preserved output. No new case or production change was needed.

Exact file gates: run_checks(scope="targets", targets=["scripts/build_package.py","tests/mcp_server/unit/test_build_package.py"], checks=["python_format","python_lint","python_pyright"], timeout_seconds=600) passed (b6a3bbfc); the later test-only correction passed the same checks on the test file (dd6461c3). One intervening adapter_deadline_expired run without output was incomplete; a health check and completed passing rerun superseded it.

The resumed full native output explicitly shows all 29 builder cases PASSED, including actual rmtree failure, external staging/dotfiles and successful orchestration. No extra focused rerun was needed.

### Original required full run — FAIL retained

At C_1 snapshot db50b1d8, the exact required call below completed with **71 failed, 2,794 passed, 1 skipped, 1 xpassed, 253 warnings, 80 errors**, 2,947 items, **450.91s**, native exit **1**. It did not time out. The 29 builder cases and installed-candidate build/install/handshake case passed. Operation85543f55296a4b9aa42746fcb2d40982; original durable report commit f20966e67e98bb70023f74e797081d94f1db4ce4.

```text
run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200)
```

The 151 diagnostic blocks initially grouped as follows. These were observed symptoms, not a reproduced main-baseline comparison; absence of a builder stack did not establish every failure as pre-existing.

| Original family | Count | C_2 disposition |
| --- | ---: | --- |
| Missing defaults/contracts.yaml | 107 | Delivered-contract cases explicitly request configured_workspace; complete synthetic bases remain explicit. |
| Old label list shape | 14 | Keyed label/pattern objects; explicit order where required; legitimate label names retained. |
| Old milestone list shape | 1 | Empty collection uses milestones={}. |
| Missing defaults/checks.yaml | 14 | Lifecycle preparations supply complete checks/adapters bases. |
| Missing defaults/github.yaml | 2 | Isolated in-process startup fixture copies the complete config tree. |
| Missing defaults/adapters.yaml or artifacts.yaml | 2 | Selected-root fixtures author required defaults and reach their intended invalid-value/duplicate diagnostics. |
| Other id/mapping consumers | 3 | Issue-type mock keys provide IDs; phase inspection uses mapping values or explicitly renames its keyed phase. |
| Renewal CLI return-code assertions | 7 | In-process CLI admission stopped at missing defaults/checks.yaml. Repair lets the distinct behaviors execute; later invalid-profile fixture corrected as below. |
| Source-startup handshake timeout | 1 | Unchanged targeted diagnostic, later startup module and complete suite pass. Original cause remains unproven. |

No required gate was waived. The owner approved this bounded C_2 repair and explicitly approved the audited force return to Planning. The transition skipped zero gates. Independent C_2 Implementation review on 8eb60cca found no blockers; the first Validation failure was not reinterpreted as a pass.

### C_2 focused repair evidence

Each test call used scope="targets", tests=["python_tests"], timeout_seconds=300 with no caller args. Exact target lists are the groups below, all within the [Planning inventory](planning.md#c_2--current_config_test_consumers).

| Selection | Observed result |
| --- | --- |
| 13 state/workflow modules: phase_state_engine plus its c3/c4/parent/persistence/workflow modules, state_repository; c7 conflicts, force/initialize/transition/cycle tools; issue39 cross-machine | 163 passed, 9 warnings, 19.27s, exit 0 (542f4c45567a4788b9342d812992cc1a). |
| 9 other modules: label_tools, label_tools_integration, github_extras, create_issue_e2e, a4_schema_overrides, planning_artifact, project_manager, catalog, artifact_target_resolver | 134 passed, 2 failed, 48 warnings, 15.02s, exit 1 (7eb283e94b7a486faf6da2cabc1697f9). Two later phase-pattern fixtures still used lists; corrected to keyed/order. |
| 4 lifecycle/startup modules: renewal_cli, template_activation, template_proposal, target_startup | 35 passed, 1 failed, 9 warnings, 135.12s, exit 1 (f09c678796204051a81a666117e0daaf). Remaining failure appended duplicate output_profile YAML keys instead of constructing one unknown profile. |
| Final rerun of precisely unit/tools/test_label_tools_integration.py and integration/test_renewal_cli.py | 28 passed, 9 warnings, 15.22s, exit 0 (39b5623d66b745b79f4d6a7f0514b2de). Both final fixture corrections verified; fresh unaffected passes reused. |

All target basenames above resolve to the exact repository-relative paths in Planning. No module outside that inventory was repaired. Seven distinct CLI scenarios retain their original assertions: fresh install, checkpointless baseline, external checkpoint/force refusal, verified backup force, conflict reconciliation, completed recovery and first legacy migration. The invalid-profile fixture now sets its existing output_profile key to missing_profile, preserving the actionable diagnosis/traceback assertions.

Final changed-file gate: run_checks(scope="targets", targets=["tests/mcp_server/fixtures/suite_roots.py", <all 26 Planning module paths>], checks=["python_format","python_lint","python_pyright"], timeout_seconds=600). All passed, exit 0; Ruff reports27formatted files, Pyright27files with zero errors/warnings (a062aa19ba824201ae99095c7215264b). Formatting was applied before these gates.

The separate unchanged handshake diagnostic used scope="targets", targets=["tests/mcp_server/integration/test_target_startup.py"], tests=["python_tests"], args={"python_tests":["-k","test_real_server_process_handshake_default_target","--tb=long"]}, timeout_seconds=180. Its delegated summary reported passed/configured tool execution with caller args; native counts/timing were unavailable. This limited diagnostic is superseded for acceptance by the completed module/full suite, not expanded into an invented causal explanation.

### Resumed complete native suite — PASS

The exact same configured invocation as the failed attempt completed at 8eb60cca with:

- **2,945 passed, 1 skipped, 1 xpassed, 253 warnings**; zero failures/errors.
- **2,947 items**, Python3.13.7, pytest9.0.2, native pyproject.toml, eight xdist workers.
- **437.09s (7m17s), exit 0**; no rejection, deadline or termination problem.
- No caller args or scope/coverage reduction; native coverage remains opt-in.
- Operation49dd6e1140cd4084971cceec831c2c63 is supplemental navigation; the invocation, snapshot and observed native outcome here are the durable evidence.

### Resumed branch and production gates

Exact invocations:

```text
run_checks(scope="branch",
  checks=["python_format","python_lint","python_pyright","python_types",
          "markdown_links","yaml_configuration","json_schema_shape","json_schema_metaschema"],
  timeout_seconds=600)
run_checks(scope="configured", checks=["python_types"], timeout_seconds=600)
```

Branch run6cc786814a774191968d4113f7857cf3 passed: format29files, lint and Markdown links40successful/zero errors, all native exit0. python_pyright, python_types, yaml_configuration, json_schema_shape and json_schema_metaschema were **not_executed / not_applicable** under their configured branch selectors; they are not claimed as executed. Explicit focused Pyright covers the changed Python files.

Configured Mypy1.19.1 passed: **no issues in193production source files**, exit0 (12f9464fd25743d28acd5a99131080a0). Initial Validation had also passed these gates (2cf22363 and ab870828); the resumed results now replace those for acceptance.

## Demonstration

Run the existing builder module with the focused call above. Invalid records/missing sources preserve stale output and never call build; traversal/absolute/overlap/link/hardlink cases preserve outside sentinels; actual cleanup denial escapes with original diagnosis; valid separate staging retains hidden files; successful scratch orchestration copies bytes and removes stale output before one substituted build call. It does not touch repository assets.

## Preservation

Public helper signatures and manifest mapping shape remain unchanged. Valid separate staging and dotfiles work. Test maintenance preserves behavioral assertions and explicit negative configurations. The native suite includes a hermetic temporary wheel build/install through the [installed-distribution fixture](../../../tests/mcp_server/fixtures/installed_distribution.py); no repository release artifact, tag, upload or external rollout was created.

## Containment

Only explicitly supplied generated output is disposable. Admission rejects escaping/overlapping/indirect paths, Windows reparse points and multiply linked output files. Required IO failure aborts; disposable partial output may remain. Static checks do not promise protection against a hostile concurrent filesystem change.

## Failures

No current failing required gate. The original full-run FAIL is retained above with its owner-approved repair and successful rerun. The source-handshake timeout did not recur and remains causally unexplained.

## Caveats

The full run still reports one skip, one xpass and253warnings; no new skips/suppressions were introduced. Observed warning families include SchemaAttachment.schema shadowing, TestCapability/TestsConfig collection, deprecated PurePath.is_reserved, deprecated resource-return types and one unawaited RestartServerTool delayed_exit coroutine. Their policy/cleanup is outside this bounded issue. A passing run does not explain the original intermittent handshake timeout. No #504 gate waiver is inherited.

## Deferred Work

No additional implementation required for the approved #505 correction. Preserve the exact stderr and investigate the startup stage if the source-handshake timeout recurs. Existing warning/skip/xpass policy is retained for Coordination triage, without creating new scope here.

## Related Documents

- [Approved Research](research.md)
- [Design](design.md)
- [Planning](planning.md)
- [Native test settings](../../../pyproject.toml)
- [Current check selection](../../../.pgmcp/config/checks.yaml)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp validator | Record focused correction evidence and the required full-suite blocker with bounded diagnosis. |
| 0.2 | 2026-10-16 | @imp validator | Retain the original FAIL; record owner-approved C_2 repair, focused diagnostics and complete passing native suite/gates without waiver. |
