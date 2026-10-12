<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — native policy findings and optional quality configuration assets

**Status:** RESEARCH — OWNER DECISION PENDING  
**Version:** 0.1  
**Last Updated:** 2026-10-12

## Purpose

Bound the native lint repairs and identify the smallest clean optional asset-distribution route before implementation.

## Scope In

Owner-authorized native Ruff activation; all 179 current diagnostics and affected consumers; consolidated #47 exception boundary assessment; actual settings of all nine bundled tools; optional asset/source ownership and v3.1.0 release preparation.

## Scope Out

Pylint reintegration, fixture-name conformity without defects, general exception/architecture rewrites, new adapters/native-config resolver, implicit owner-config takeover, legacy bridges or new regression campaign, publication during Research.

## Problem Statement

The historical analyzer scan is stale. Enabling three native rules exposes existing code/test boundary choices; missing released native project settings must be supplied without drift or silent activation.

## Goals

- Classify the actual stricter native diagnostics against current source and architecture, not old warning counts.
- Inventory each existing tool's native settings and distinguish files, CLI policy and no-file cases.
- Compare optional distribution placement/source-ownership routes with proportionate consumer and verification impact.

## Background

The owner asks first for substantive Research on the initialized #319 branch. Native policy activation is explicitly authorized now; production/test repairs, asset placement and TOML export are not implemented by this Research. The issue body additionally consolidates bounded #47 exception assessment.

## Findings

### Actual native policy and baseline

On parent snapshot `8a7a81bef4932cde3c47589d072b49d9a6b302cc`, the owner explicitly authorized activating `extend-select = ["G004", "BLE001", "SLF001"]` in the existing native Ruff section. No exclusions, ignores, adapter code or tool defaults were changed. TOML has no selected safe-edit preflight profile: the enforce attempt wrote nothing; the explicit report-policy edit wrote the requested line, then stdlib tomllib parsed it and actual Ruff execution consumed it.

`run_checks(scope="configured", checks=["python_lint"], args={"python_lint":["--output-format","json"]}, timeout_seconds=180)` reads the new native policy without passing rule selectors. Ruff 0.15.6 reports exit 1: G004 2, BLE001 43, SLF001 134, total 179. Diagnostic code/file/line identities equal the earlier temporary extend-select probe. A separate normal `run_checks(scope="configured", checks=["python_lint"], timeout_seconds=180)` also fails with configured defaults. Neither check fixes sources or runs tests.

| Scope | G004 | BLE001 | SLF001 | Total |
| --- | ---: | ---: | ---: | ---: |
| Active server | 2 | 36 | 1 | 39 |
| Tests | 0 | 6 | 133 | 139 |
| Old server archive | 0 | 1 | 0 | 1 |
| Total | 2 | 43 | 134 | 179 |

Native selection, existing rules and ANN/ARG test exceptions remain intact. Python write preflight remains syntax-only. W0621 fixture shadowing has no identified Ruff counterpart and is not a required repair. All nine tools retain their existing contracts/pins. The old twelve phase_state_engine logging findings are absent.

### G004: two direct logging repairs

[mcp_server/managers/state_version_validator.py](../../../mcp_server/managers/state_version_validator.py) lines 91/95 build f-strings inside warning/error calls. Lazy logging arguments can preserve message values and backup behavior with no public API change. This is a mechanical correction; no new test campaign is needed.

### BLE001: complete bounded handler inventory

These are assessment findings, not 43 proven bugs or a reduction quota. The current #319 body consolidates #47's relevant exception audit here and supersedes its percentage targets and general architecture campaign. Necessary command/error/protocol/cleanup catches must remain; rethrows and logged exc_info are already accepted by Ruff. Preserve public failure DTOs and primary exception/cancellation semantics. Adding a log solely to evade lint is not a justified fix; neither are blanket per-file ignores.

| Source | Lines | Research disposition |
| --- | --- | --- |
| [mcp_server/#Archief/supervisor_old.py](../../../mcp_server/%23Archief/supervisor_old.py) | 132 | Archive selection: propose exclude in native discovery and branch preselection; retain explicit targeting semantics. Do not repair old code. |
| [mcp_server/cli.py](../../../mcp_server/cli.py) | 109 | Final initialization/CLI failure boundary: preserve exit 1 and error reporting; retain cause/trace diagnostics rather than changing the public command outcome. |
| [mcp_server/config/schemas/label_config.py](../../../mcp_server/config/schemas/label_config.py) | 120, 146 | External label-list/per-label operation boundaries. Preserve error collection and partial progress; no general relocation of sync orchestration in this issue. |
| [mcp_server/config/settings.py](../../../mcp_server/config/settings.py) | 33, 48 | Two silent metadata/YAML fallbacks. Narrow expected lookup/read/parse failures; unexpected programming errors must not be silently mistaken for unavailable version metadata. |
| [mcp_server/core/policy_engine.py](../../../mcp_server/core/policy_engine.py) | 154 | Fail-closed policy evaluation. Preserve deny on evaluation failure and its decision facts; do not make a lint repair turn this into allow or uncontrolled propagation. |
| [mcp_server/execution/content_input.py](../../../mcp_server/execution/content_input.py) | 172, 178, 238 | Three nested cleanup catches attach rollback diagnostics to the original failure. Preserve cancellation/primary exception and notes; narrow local justified exceptions only, not BaseException handling globally. |
| [mcp_server/managers/enforcement_runner.py](../../../mcp_server/managers/enforcement_runner.py) | 350, 410 | Unknown phase becomes a blocking mismatch; context-load read failure currently falls through. Preserve admission safety; distinguish known missing-state cases from unexpected failures and make diagnostics explicit. |
| [mcp_server/presenters/text_presenter.py](../../../mcp_server/presenters/text_presenter.py) | 248, 324, 428, 438 | Four formatting/placeholder boundaries. Preserve safe presentation and original tool-result availability; parser errors are expected, but generic swallowed errors need a deliberate local policy. |
| [mcp_server/state/response_cache.py](../../../mcp_server/state/response_cache.py) | 54 | Publication must report write_failed without losing the underlying tool outcome. Preserve that boundary; scope diagnostic treatment locally. |
| [mcp_server/tools/git_analysis_tools.py](../../../mcp_server/tools/git_analysis_tools.py) | 101, 165 | Two tool-specific failure DTO boundaries. Preserve response shapes and error messages; no error DTO redesign. |
| [mcp_server/tools/git_tools.py](../../../mcp_server/tools/git_tools.py) | 175, 251, 414, 438, 480, 484, 554, 623, 772, 775, 846, 929, 1007, 1074 | 14 catches mix tool failure DTOs, phase rollback and secondary branch lookup. Preserve each existing outcome and primary failure; make trace/cause meaningful where a catch intentionally remains broad. |
| [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py) | 294, 567, 617 | Initialization and two planning mutation failure boundaries; preserve persisted/primary failure facts. No planning/state/history behavior redesign. |
| [mcp_server/utils/cache_serialization.py](../../../mcp_server/utils/cache_serialization.py) | 49 | Serialization failure fallback must remain JSON and preserve material failure facts; no cache/presenter refactor. |
| [tests/mcp_server/integration/test_model1_branch_tip_neutralization.py](../../../tests/mcp_server/integration/test_model1_branch_tip_neutralization.py) | 130, 141 | Two Git-query helper catches can use the actual Git command failure type rather than suppressing arbitrary defects. |
| [tests/mcp_server/integration/test_target_startup.py](../../../tests/mcp_server/integration/test_target_startup.py) | 338 | Catch merely converts any build exception to pytest.fail. Prefer allowing the original failure to retain its traceback unless a demonstrated diagnostic need justifies conversion. |
| [tests/mcp_server/test_support.py](../../../tests/mcp_server/test_support.py) | 77 | Broad Settings/config fallback in shared helper. Identify the expected setup error; do not hide arbitrary helper defects. |
| [tests/mcp_server/unit/test_server.py](../../../tests/mcp_server/unit/test_server.py) | 74, 84 | Two schema-version fixture normalizations swallow every error. Keep isolated fixture scope; remove obsolete normalization or narrow genuine IO/JSON errors. This observation is not proof of any past live-workspace incident. |

Only two existing active-server `noqa: BLE001` sites were found: ConfigLoader.__init__ line 136 (implicit template-root fallback when Settings fails), and core/error_handling.py line 102 (logged terminal error translation). Inspect their local necessity/rationale with the affected boundaries; do not turn this into a server-wide suppression cleanup or resurrection of old ToolResult architecture.

### SLF001: exact access-shape inventory and bounded remedies

AST inspection of all 134 reported attribute accesses yields 40 calls, 27 writes and 67 reads; one read is production, the other 133 accesses are tests. A read often prepares a nested mock dependency; it is not necessarily a private-state assertion.

| Source | Calls | Writes | Reads |
| --- | ---: | ---: | ---: |
| [mcp_server/core/decorators/tool_error_handler_decorator.py](../../../mcp_server/core/decorators/tool_error_handler_decorator.py) | 0 | 0 | 1 |
| [tests/mcp_server/config/test_git_config.py](../../../tests/mcp_server/config/test_git_config.py) | 0 | 1 | 1 |
| [tests/mcp_server/conftest.py](../../../tests/mcp_server/conftest.py) | 0 | 1 | 0 |
| [tests/mcp_server/unit/config/test_label_config.py](../../../tests/mcp_server/unit/config/test_label_config.py) | 2 | 0 | 5 |
| [tests/mcp_server/unit/config/test_validator_c3.py](../../../tests/mcp_server/unit/config/test_validator_c3.py) | 2 | 0 | 0 |
| [tests/mcp_server/unit/core/test_tool_factory.py](../../../tests/mcp_server/unit/core/test_tool_factory.py) | 0 | 0 | 5 |
| [tests/mcp_server/unit/test_c260_c2_state_root_injection.py](../../../tests/mcp_server/unit/test_c260_c2_state_root_injection.py) | 7 | 0 | 0 |
| [tests/mcp_server/unit/test_server.py](../../../tests/mcp_server/unit/test_server.py) | 2 | 0 | 0 |
| [tests/mcp_server/unit/tools/test_create_issue_label_assembly.py](../../../tests/mcp_server/unit/tools/test_create_issue_label_assembly.py) | 25 | 0 | 0 |
| [tests/mcp_server/unit/tools/test_cycle_tools.py](../../../tests/mcp_server/unit/tools/test_cycle_tools.py) | 2 | 0 | 0 |
| [tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py](../../../tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py) | 0 | 0 | 7 |
| [tests/mcp_server/unit/tools/test_discovery_tools.py](../../../tests/mcp_server/unit/tools/test_discovery_tools.py) | 0 | 20 | 48 |
| [tests/mcp_server/unit/tools/test_git_checkout_state_sync.py](../../../tests/mcp_server/unit/tools/test_git_checkout_state_sync.py) | 0 | 4 | 0 |
| [tests/mcp_server/unit/tools/test_issue_tools.py](../../../tests/mcp_server/unit/tools/test_issue_tools.py) | 0 | 1 | 0 |

- Discovery accounts for 68 accesses: 20 private dependency assignments and 48 nested dependency/settings reads. Constructor parameters and public execute already exist; retain mock references outside the tool and inject them at construction. Several tests patch GitManager despite explicit injected instances. Remove ineffective patching while retaining their observable contract.
- Label assembly accounts for 25 direct private calls. Adapt the existing cases to CreateIssueTool.execute and inspect the manager call's labels; consolidate repetition where it keeps distinct behaviors. Do not make _assemble_labels public just to satisfy lint.
- ConfigValidator's two private calls duplicate a public validate_startup failure case already present in the same file. Retain useful public positive/negative behavior rather than private helper coverage.
- Tests reaching bootstrap, restart paths and branch helpers should exercise public startup/execute outcomes with injected/mocked side effects. Do not trigger a real restart or create a public accessor solely for tests.
- Tests assert internal label/config caches and decorator wiring. Prefer public validation/dispatch/enforcement outcomes. Apply a local justified exception only when test-infrastructure access has no constructor/factory alternative, as Architecture Principles §14 permits.
- The autouse conftest fixture resets CreateBranchInput._git_config, but that field no longer exists in the active input model. This is orphaned test maintenance, not a real config-singleton dependency.
- The sole production diagnostic is ToolErrorHandlerDecorator._tool unwrapping inner._inner_tool. Repository consumer search finds only seven getattr(...,"_tool",...) uses in the registration integration test; no active production consumer. The public tool name/schema suffice for registration assertions. Removing this test-driven escape property and adapting those assertions is smaller than adding a general wrapper interface. The seven reflection consumers do not themselves trigger SLF001; the inventory therefore includes them explicitly.

### Native configuration inventory: all bundled quality tools

| Tool / admitted version | Actual source | Distribution implications |
| --- | --- | --- |
| Ruff 0.15.6 | pyproject.toml tool.ruff, including new lint rules | Export nested native values and test exceptions; py311, length 100 and exclusions are workspace policy. |
| Mypy 1.19.1 | pyproject.toml tool.mypy, including overrides array | Strict production mcp_server selection and tests.* override are repository-specific; preserve shape. |
| Pyright 1.1.408 | pyrightconfig.json; checks.yaml native --level warning --warnings | Preserve explicit severities/exceptions; Windows, mcp_server/backend/tests roots require owner adjustment. |
| Pytest 9.0.2 | pyproject.toml tool.pytest.ini_options | Test roots, markers, asyncio strict and -n auto depend on the workspace and installed plugins. |
| Coverage 7.13.5 / pytest-cov 7.0.0 | pyproject.toml tool.coverage | Part of the Pytest package family; source=mcp_server, branch=true, threshold 90. Coverage stays opt-in, not newly enforced. |
| Commitlint 21.2.2 / parser 10.4.0 | commitlint.config.cjs | Simple parser preset, defaultIgnores=false and two required-field rules; no pgmcp import. Package prerequisites remain separately declared. |
| Lychee 0.24.2 | checks.yaml native --offline --cache=false --include-fragments | No authored native file exists; these defaults already ship. Do not invent one for symmetry. |
| Check-jsonschema 0.38.2 | checks.yaml native args plus existing check_schemas | Already shipped; schema paths are root-relative. YAML shape, JSON-source shape and metaschema are distinct bindings. |
| Python syntax / provisioned interpreter | ast.parse, no native file | No configuration asset to export; grammar follows admitted interpreter. |
| TypeScript syntax 6.0.3 | Native API discovers nearest target tsconfig; no authored tsconfig exists here | Retain owner config discovery; document no supplied baseline rather than manufacture one. |

There are nine adapters; Coverage is listed separately as an existing dependency/config subsection of Pytest, not a tenth adapter. pytest-xdist 3.8.0 and pytest-asyncio 1.3.0 are pinned prerequisites. PGMCP checks/tests/fixes configs, schema files and adapter dependency manifests already ship; they are distinct from missing native project-config reference files.

### Placement and source-ownership choices

| Option | Architecture / cost | Owner adoption |
| --- | --- | --- |
| References inside adapter packages | Existing package-data can include declared samples, but manifest files/fingerprints become tied to optional workspace policy. Fresh init does not copy adapter-package files. No invocation change is required. | Read from installed package; explicitly copy/merge native settings. |
| Separate optional release-assets directory (recommended) | Existing manifest file/directory copy and package-data support it. Keeps adapter identity and native discovery unchanged. Proposed name native_quality_configs is illustrative, not implemented. | Fresh init copies references under server root; owner chooses root-native placement/merge. |

Source ownership is a separate choice. Shipping the whole root pyproject is simple but includes PGMCP identity/dependencies/build settings; a hand-maintained extracted file creates drift. Moving active policy to separate canonical config files avoids extraction but alters native discovery/layout for four families. The smallest route preserving current discovery and SSOT is a narrow build-time export of only Ruff/Mypy/Pytest/Coverage sections, alongside direct copies of Pyright/Commitlint.

The build script currently copies files/directories; it cannot extract TOML sections. Python tomllib only reads TOML. No TOML writer is currently installed in the active development environment. A library-based export needs an explicit build-only serializer prerequisite, faithful nested/array-table handling and parsed source/output parity; do not introduce a runtime dependency or a hand-written general TOML parser. Output placement and this bounded build addition still need owner agreement.

### Initialization, renewal and release boundaries

Fresh --init rejects an existing server root before copying all package/assets into a new root. Native references there are inactive until owner adoption; no new root pyproject/Pyright/Commitlint file should be created implicitly. Existing --upgrade selects package/assets/template_suite only: it will NOT refresh the proposed native-reference folder. New installed distributions can still supply current references for manual adoption. Do not quietly broaden renewal or overwrite workspace files.

The updated issue targets v3.1.0 for additive optional assets and compatible repairs. Research does not change version values/build artifacts or authorize publication. Published v3.0.0 stays immutable. If maintaining the requested behavior requires a public contract change or a new general mechanism, reopen the scope/workflow decision instead of calling it mechanical.

### Consumer and verification boundary

Affected consumers: native lint/editor/branch checks; existing tests/helpers; packaging script/manifest and build prerequisites; installed asset inventory; fresh-init copy; optional owner adoption; setup/release notes and existing version parity assertions. Unaffected: execution DTOs, generic selection algorithm, adapter entrypoints/protocols, tool catalog, phase/state/planning policies, quality preflight selection, template contracts and normal template-only renewal.

During repair, adapt the narrow existing tests proving each public behavior and run relevant Python gates per file type. Reuse packaging/CLI/init fixtures for faithful section export and installed optional-file preservation; prove exact wheel/sdist/installed references using actual artifacts. Keep full configured verification in Validation. No Research full suite was run, no production/test repair is implemented yet, and 179 remains the intentionally failing baseline.

### Recommended strategy awaiting remaining owner decision

Retain the activated native rules; narrow real silent-fallback defects, preserve necessary failure/cleanup contracts, prefer public behavior and constructor injection, remove proven orphan test setup/escape access, and use only locally justified exceptions. For distribution, prefer separate optional assets and a bounded build-time TOML section export. The latter two choices are proposals, not owner-approved placement/extraction design.

## Questions

- Approve separate optional release assets plus a narrow build-time export of only the four native TOML tool sections, with an explicit build-only writer dependency? Alternative placements/source strategies are compared above.
- Confirm the proposed local treatment of necessary boundary/cleanup catches and exclusion of old server archive in both native discovery and branch preselection; explicit target access remains available.

## References

- [Ruff configuration](<https://docs.astral.sh/ruff/configuration/>)
- [BLE001 semantics](<https://docs.astral.sh/ruff/rules/blind-except/>)
- [Mypy 1.19.1 config reference](<https://github.com/python/mypy/blob/v1.19.1/docs/source/config_file.rst>)
- [Python tomllib](<https://docs.python.org/3.13/library/tomllib.html>)
- [TOML writer option](<https://github.com/hukkin/tomli-w>)

## Approved Strategy

Approved by the owner: activate G004/BLE001/SLF001; assess and repair meaningful active problems; ship existing native settings as optional owner-controlled reference assets in a new release. Existing architecture requires public-behavior tests and preserved command/error/cleanup semantics. Updated issue targets v3.1.0. No compatibility bridges, Pylint reintegration or unbounded test expansion. Pending human decision: adapter-package versus separate-assets placement, and whole-project reference versus faithful build-time TOML export/canonical config relocation. Research must not close or enter Implementation until that remaining strategy is settled.

## Expected Results

Agreed stricter lint policy passes after justified bounded repairs and exclusions; existing public tool/error/cancellation outcomes remain correct. All actual native-file cases have SSOT-derived packaged references, all CLI/no-file cases are explained, and fresh installation exposes optional references without touching root-native configs. Native args/discovery and template renewal retain their current contracts.

## Evidence

### The stricter policy is stored and actually consumed.

The stored native rule extension is consumed without rule-selector arguments; stricter diagnostics are current and intentionally unresolved during Research.

- [Native policy](<../../../pyproject.toml>)
- [Branch policies and bindings](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** safe_edit_file(pyproject.toml, report) adds only extend-select; tomllib parse; run_checks(scope='configured', checks=['python_lint'], args={'python_lint':['--output-format','json']}, timeout_seconds=180). A normal configured call with no args also fails.

**Observed Result:** Ruff 0.15.6/native exit 1:179 diagnostics, G004 2/BLE001 43/SLF001 134. Complete JSON assembled contiguously and identity checked; locations equal the earlier temporary probe. No fixes/tests executed.

## Risks

### Removing a broad catch or adding private test APIs can alter established contracts while making lint green.

Classify each inventory row; adapt meaningful existing public behavior evidence; preserve primary exceptions/failure DTOs and allow only justified local exceptions.

### Optional native samples drift or are silently adopted.

One authoritative source, faithful derived outputs, inactive placement and explicit owner adoption; no runtime config injection or root overwrite.

## Related Documents

- [Issue319](<https://github.com/MikeyVK/phase-gate-mcp/issues/319>)
- [Architecture Principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Adapter contract](<../../reference/execution-adapters.md>)
- [Release assets procedure](<../../reference/release-assets-procedure.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-12 | @imp researcher | Activate authorized native policy, classify current diagnostics and compare bounded optional configuration distribution strategies. |
