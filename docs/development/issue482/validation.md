<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# Issue #482 Validation

**Status:** Review requested  
**Version:** 0.2  
**Last Updated:** 2026-10-07

## Outcome and scope

Producer-observed outcome: **PASS**. Independent Validation review is requested; this report does not authorize a phase transition.

C482.1 implements the approved clean break. Implementation is `d09f4edbb33221b9580f978a0c9fd241d05a9205`, with the omitted Mypy version corrected in `052fc16d0b5f5e13b613f1760421fbfa5da4654b`. The owner's “Goed, fix en ga door” also authorized repairing the #481 baseline circular import by importing TemplateId directly from its owning schema.

Scope excludes native configuration interpretation, force-exclude, compatibility, impact-based test selection, new test modules and old-behavior regression expansion.

## Deliverable and contract mapping

| Obligation | Observable evidence and source | Outcome |
|---|---|---|
| D482.1.1: immutable policies, required references and startup cross-validation | [Policy model](../../../mcp_server/config/schemas/checks_config.py), [manifest declaration](../../../mcp_server/config/schemas/adapter_manifest.py), [validator](../../../mcp_server/config/validator.py); three admission scenarios and healthy startup | Required active references resolve, including configured bindings outside the default profile; missing/malformed/unresolved declarations fail admission. |
| D482.1.1: generic matching and dependency direction | [Injected interface](../../../mcp_server/core/interfaces/execution.py), [matcher](../../../mcp_server/execution/configured_targets.py), [bootstrap](../../../mcp_server/bootstrap.py); mixed branch-candidate behavior | Workspace-relative, anchored, case-sensitive matching preserves literal Unicode/whitespace and deterministic order. Generic code contains no tool IDs, native defaults, native-config reads or recursive discovery. |
| D482.1.2: per-check branch planning and ordinary invocation | [Selector](../../../mcp_server/execution/check_selection.py), [selection tests](../../../tests/mcp_server/unit/execution/test_check_selection.py); separate per-check subsets and comparison of equal effective requests | Branch candidates resolve once and filter per selected check. Other scopes retain ordinary requests; explicit directory and descendant targets both survive. |
| D482.1.2: neutral empty subsets and truthful public outcomes | [Executor](../../../mcp_server/execution/check_service.py), [public model](../../../mcp_server/schemas/execution_outputs.py), [projection](../../../mcp_server/services/check_operation.py), [public tests](../../../tests/mcp_server/integration/test_checks_public_v3.py) | Five outcome scenarios prove all-filtered, positive/negative mixtures, attempted refusal and stop behavior. Preselected empties have no invocation/native identity; actual refusal and later unstarted work stay incomplete. Global empty branch retains empty_selection with no rows. |
| D482.1.3: coherent consumer migration and cleanup | [Planning inventory](planning.md), [admission tests](../../../tests/mcp_server/unit/config/test_checks_config.py), branch diff | Constructor, inline manifest and carrier searches cover actual consumers. CheckSelectionPlan.calls and directory covering are removed without aliases. Coupled fixture migration adds no scenarios. |
| D482.1.3: bounded behavior evidence | Focused receipt and independent QA receipts below | Three new functions, nine new scenarios, zero new modules; 15 selected existing/new cases pass. No content, package-version or old-route snapshot tests. |
| Four affected package declarations | [Ruff](../../../mcp_server/bundled_adapters/ruff/manifest.yaml), [Mypy](../../../mcp_server/bundled_adapters/mypy/manifest.yaml), [Pyright](../../../mcp_server/bundled_adapters/pyright/manifest.yaml), [Lychee](../../../mcp_server/bundled_adapters/lychee/manifest.yaml) | Direct inspection after correction confirms all four are 2.0.0; native pins and wire contract_version=1 remain unchanged. |
| Authorized baseline import repair | [Direct TemplateId import](../../../mcp_server/core/tool_execution.py), [owning schema](../../../mcp_server/schemas/template_identity.py) | Two existing baseline cases and the full configured collection pass. No new tests for this repair. |

## Exact required evidence

| Selection | Observed result | Commit / receipt |
|---|---|---|
| `run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200)` | **2818 collected: 2816 passed, 1 skipped, 1 xpassed, 229 warnings; 331.24 seconds; exit 0.** Eight workers; effective_args=[]; pyproject defaults retained without caller filters, coverage reduction or split. | d09f4edb / aeb13588601642ec9b4aa3e3f8469357 |
| `run_checks(scope="branch", checks=["python_format","python_lint","python_types","python_pyright","markdown_links"], timeout_seconds=600)` | Original five checks passed, exit 0 each. Ruff: 24 files; Mypy/Pyright: 11 production sources. Lychee: 50 occurrences, 33 successful, 17 native offline exclusions, zero errors. | d09f4edb / 674b0dc1d7ca4a81a39173a632b813d2 |
| `run_checks(scope="configured", profile="python_review", timeout_seconds=600)` | Four checks passed, exit 0 each. Ruff format: 468 files; Mypy: 189 sources; Pyright: 189 sources with zero errors/warnings. Native configured roots retained. | d09f4edb / c14fa86af80f4d0c8e6be1963597a496 |
| Same five-check branch call after version repair and report creation | Five checks passed, exit 0 each. Ruff: 24 files; Mypy/Pyright: 11 production sources. Lychee: 68 occurrences, 51 successful, 17 native offline exclusions, zero errors. Mypy package **2.0.0 / Ji_GICw8UiKbT6Is**, native Mypy 1.19.1. | 052fc16d + Validation state/report / 6396364541ff494297239f6c2133bf6a |

The complete full-suite DTO was assembled from 68 contiguous Unicode-codepoint windows, with stable metadata and UTF-8 SHA-256 verified once: `9fe3eea6050102433647bf9c024a37852a4b91e18e2ac74fde4cd4beb2ed2b15`. The producer retains the complete DTO. Native summary:

```text
2816 passed, 1 skipped, 1 xpassed, 229 warnings in 331.24s (0:05:31)
```

Focused implementation evidence: receipt `307bc0f045dd41f8bb4d2c10fb86e598`, **15 passed, 9 warnings, 6.76 seconds, exit 0**. Applicable production Python format/lint/Pyright passed (`23cbf8ee43954f13b64e623bbe48a0f4`); test/fixture format/lint passed (`faa2def15ea64aafb2ba8492fa79c1cf`). The approved selector also matches two existing invalid-config parameter IDs; the new coverage budget remains nine scenarios.

Independent Implementation QA reran 15 selected cases (`83dddebe32ce48d8b12c4c77fdad76b8`), production gates (`250825aac6784a1fa7c93a7d334cd2f1`), test gates (`3996e4a9597a46a3a909fb64acc8dadc`) and healthy admission (`4e31b6a97c41470b948b165ac1e62b77`).

## Failure, correction and evidence reuse

The first deliverable assessment was **FAIL**, preserved in auditcommit `c8dda67ee6722e52fac38ef75eac6a7b896bd9e3`: Mypy still declared package version 1.0.0 despite the four-package 2.0.0 requirement. Independent QA confirmed P2 in turn `01a114db-03ac-7400-832f-81aa1e4494e6`. Green tests did not prove this authored version requirement.

The audited backward transition returned the work to Implementation under the owner's fix authorization, without skipping a gate. Repair `052fc16d` changes only that manifest version and workflow registration. After reload, health is healthy (PID 18500, receipt `55846ad8beaf422bbd319391e2e7033d`); targeted Mypy passed with the new identity (`2f740a1c5b8c4f08a8a9eeb1c468a1d0`, one source, exit 0).

Independent QA closed the implementation P2 and gave GO to resume Validation in turn `01a114e0-8dfe-7200-98db-5514be088d28`. Its direct diff/source review found no concrete invalidation of full-suite, behavioral or native configured results: production/tests, policies, native versions and invocation are unchanged. A second full suite was unnecessary. This was an implementation-repair review, not final Validation approval.

Original Mypy receipts remain observations of **1.0.0 / pIuqT753FXPApELy**. Their native typecheck conclusions are reused; the fresh branch and targeted receipts separately prove the current **2.0.0 / Ji_GICw8UiKbT6Is** identity. The branch check was refreshed because the new Validation report changed the Markdown inventory. No old receipt is relabeled as a new-identity invocation.

Open failures: **None observed after correction.**

## Preservation and containment

Native protocol version 1, pins, commands, guards and configured/workspace/content/test/fix meanings remain unchanged. Only branch selection checks consume the authored policies. Pytest gains no branch scope or policy field. No native-config parser, adapter intent flag, compatibility bridge or directory-covering alias remains.

Tests use existing isolated fixtures and invocation boundaries. No new modules/shared harnesses were retained. Research, Design and Planning are reviewed authoritative inputs and remain unchanged by this Validation correction.

## Caveats and deferred work

- The existing suite skips `TestProxyIntegration.test_end_to_end_restart_flow` when RUN_MANUAL_TESTS is absent; its source describes a manual full-server integration test. Native scope/defaults are retained. See [the test](../../../tests/mcp_server/core/test_proxy.py).
- `TestGitCommitToolC3.test_server_renders_exclusion_note_in_response` XPASSes under its existing `xfail(strict=False)` marker; no marker was changed. See [the test](../../../tests/mcp_server/unit/managers/test_enforcement_runner_unit.py).
- 229 native warnings include Pydantic field shadowing/collection warnings, pathlib reserved-path deprecation, deprecated MCP resource returns and synchronous tests marked asyncio. Restart-tool tests also emit SystemExit task diagnostics. These observations are not suppressed; native completion is exit 0.
- Caches are transient and connection-local. The controlled reload cleared the old producer receipts; durable observations and exact commit/identity distinctions are recorded above. The full DTO remains producer-retained.
- No new deferred implementation work or exception is introduced. Existing warning/manual-test/xfail maintenance is outside this issue; independent QA must assess the stated limitations.

## Related documents

- [Approved Research 0.15 and Strategy](research.md)
- [Approved Design 0.3](design.md)
- [Planning 0.1](planning.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-07 | @imp validator | Record full configured verification and incomplete Mypy migration as FAIL. |
| 0.2 | 2026-10-07 | @imp validator | Preserve the initial failure, record approved repair, fresh branch evidence and bounded reuse for final review. |
