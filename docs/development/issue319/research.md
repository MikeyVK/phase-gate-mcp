<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — native policy findings and deliberate workspace quality setup

**Status:** APPROVED STRATEGY — COMPACT DESIGN FOR REVIEW  
**Version:** 0.4  
**Last Updated:** 2026-10-12

## Purpose

Bound native lint repairs and investigate deliberate workspace quality-tool setup and missing-configuration refusal before implementation.

## Scope In

Owner-authorized native Ruff activation; all 179 current diagnostics and affected consumers; consolidated #47 exception boundary assessment; actual settings of all nine bundled tools; owner-reopened distribution strategy, missing-native-config behavior and installation guidance. The issue's release target remains provisional pending the revised strategy.

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

### Native configuration inventory and proposed requirement scope — superseded file-gate proposal

The actual nine-tool inventory remains current. Its mandatory-file recommendations and proposed scope-lock bullets are historical intermediate proposals, superseded by the final configuration-choice strategy below and design.md.

All nine current adapters were rechecked against their native invocations and workspace bindings. Reading native configuration is already supported; unconditional refusal on absence is a separate policy, not an existing guarantee.

| Adapter / roles | Current actual native policy in this workspace | Native config behavior | Proposed #319 requirement scope |
| --- | --- | --- | --- |
| Ruff0.15.6: format/lint checks and fixes | pyproject.toml tool.ruff, including lint rules/ignores and shared format settings | Native Ruff discovery or explicit --config. No unconditional adapter-owned file requirement. | Require the owner-declared native policy file for both check and fix roles; this keeps formatting/lint behavior intentional. Do not prescribe one filename for every workspace. |
| Mypy1.19.1: types check | pyproject.toml tool.mypy, including overrides | Native parser reads discovered or explicit --config-file config; missing explicit file was live-refused. No unconditional file requirement. | Require an owner-declared config file to make source selection/strictness explicit. |
| Pyright1.1.408: types check | pyrightconfig.json plus --level warning --warnings in checks.yaml | Native discovery or --project; discovered file already controls include/platform/severity. Missing explicit file was live-refused. | Require an owner-declared native project config; preserve native argument/discovery semantics. |
| Pytest9.0.2: tests | pyproject.toml tool.pytest.ini_options, with Coverage7.13.5 configuration for opt-in coverage | Native pytest discovery or -c; missing explicit TOML stopped before collection with an untidy failed/traceback result. | Require the owner-declared test policy config. Do not introduce separate mandatory coverage config or enable coverage. Existing plugin pins remain prerequisites. |
| Commitlint21.2.2: content-based commit check | commitlint.config.cjs selects parser/rules | Native CLI discovers config or accepts --config. Adapter rejects empty-rules reports as invalid_configuration. Explicit missing-file refusal has source/CLI evidence, not a live producer probe. | Require an owner-declared native policy file for this content check. Do not confuse native rules with the adapter's provenance marker reader. |
| Lychee0.24.2: selection/content links | checks.yaml native --offline --cache=false --include-fragments; no authored lychee file/section here | Native config is supported; the adapter reads applicable boundary settings. CLI-only policy is already explicit and sufficient here. Missing explicitly requested config was live-refused. | No universal native-file requirement. Keep CLI-only setup valid; owner may declare a required file if this binding deliberately uses one. |
| Check-jsonschema0.38.2: YAML/JSON source shape and metaschema | Explicit --schemafile paths for YAML/JSON-source checks; --check-metaschema for metaschema check | The external schema is the native policy/input dependency, not a separate general tool config. Schema-backed bindings already point to released schema files. Metaschema uses the tool's built-in schema. | Apply any declared prerequisite to external-schema bindings only; no mandatory general config file and no external-file requirement for metaschema. Native checker interprets/validates schemas. |
| Python syntax: content syntax | ast.parse under the provisioned Python interpreter | No native config file or args are supported. | Exclude from native-file requirement; retain syntax-only preflight. |
| TypeScript syntax6.0.3: content syntax | No tsconfig in this repo. Adapter uses TypeScript API to find nearest tsconfig for logical target; absent file produces empty compiler options | Existing native config is consumed when found and parse errors are refused. Absent config is intentionally allowed; native args are unsupported. It does not provide semantic/type checking. | No universal tsconfig requirement for this syntax capability; keep native discovery and configless syntax. Owner-declared prerequisites could be opt-in later, not a new default here. |

Five policy-file families therefore qualify for the proposed mandatory workspace prerequisite: Ruff, Mypy, Pyright, Pytest and Commitlint. Lychee/file-backed JSON checks are conditional cases; the two syntax adapters and built-in metaschema need no invented file.

Coverage is a subsection/dependency of the Pytest family, not a tenth adapter. Pytest's existing plugin prerequisites are pytest-cov7.0.0, pytest-xdist3.8.0 and pytest-asyncio1.3.0. Provisioning native packages/versions, PGMCP check/test/fix bindings, and native policy files are three distinct installation tasks.

Proposed scope lock, awaiting owner approval:
- Retain the activated G004/BLE001/SLF001 policy and bounded diagnostic repairs.
- Keep parsing/discovery/native option semantics with the native tool. No per-tool exporter, config builder or resolved-config engine.
- Required paths are workspace-owned declarations at the relevant operation binding, not filenames/tools hardcoded in generic execution or compulsory files baked into adapter packages.
- Any missing-file check applies before an applicable invocation, including content-only preflight and fix roles where configured. It must not treat an already-not-applicable branch row as an attempted check.
- Preserve caller native args. If unconditional presence is chosen, the prerequisite must not disappear with args overrides; presence still does not promise use of that exact file or policy correctness.
- Document deliberate setup for all nine adapters, including CLI-only and no-file cases; improve selected native-config failure presentation only where needed.
- Exclude server-startup blocking, sample distribution/export, new native configuration files for currently no-file tools, general adapter redesign, and additional coverage enforcement.
- Actual shape of the prerequisite declaration and failure contract remains an implementation/design decision after strategy approval. The issue body needs Coordination reconciliation with this proposed replacement of its earlier asset scope.

### Placement and source-ownership choices — superseded proposal

The owner reopened this route after reviewing its extraction/maintenance cost. These alternatives remain research history; separate asset references and TOML builders are not the current recommended execution strategy. See the owner-revision findings below.

| Option | Architecture / cost | Owner adoption |
| --- | --- | --- |
| References inside adapter packages | Existing package-data can include declared samples, but manifest files/fingerprints become tied to optional workspace policy. Fresh init does not copy adapter-package files. No invocation change is required. | Read from installed package; explicitly copy/merge native settings. |
| Separate optional release-assets directory (recommended) | Existing manifest file/directory copy and package-data support it. Keeps adapter identity and native discovery unchanged. Proposed name native_quality_configs is illustrative, not implemented. | Fresh init copies references under server root; owner chooses root-native placement/merge. |

Source ownership is a separate choice. Shipping the whole root pyproject is simple but includes PGMCP identity/dependencies/build settings; a hand-maintained extracted file creates drift. Moving active policy to separate canonical config files avoids extraction but alters native discovery/layout for four families. The smallest route preserving current discovery and SSOT is a narrow build-time export of only Ruff/Mypy/Pytest/Coverage sections, alongside direct copies of Pyright/Commitlint.

The build script currently copies files/directories; it cannot extract TOML sections. Python tomllib only reads TOML. No TOML writer is currently installed in the active development environment. A library-based export needs an explicit build-only serializer prerequisite, faithful nested/array-table handling and parsed source/output parity; do not introduce a runtime dependency or a hand-written general TOML parser. Output placement and this bounded build addition still need owner agreement.

### Initialization, renewal and release boundaries — packaging facts and superseded asset proposal

The current init/renewal mechanisms described here remain source facts. Proposed native-reference distribution in this section is not part of the final strategy.

Fresh --init rejects an existing server root before copying all package/assets into a new root. Native references there are inactive until owner adoption; no new root pyproject/Pyright/Commitlint file should be created implicitly. Existing --upgrade selects package/assets/template_suite only: it will NOT refresh the proposed native-reference folder. New installed distributions can still supply current references for manual adoption. Do not quietly broaden renewal or overwrite workspace files.

The updated issue targets v3.1.0 for additive optional assets and compatible repairs. Research does not change version values/build artifacts or authorize publication. Published v3.0.0 stays immutable. If maintaining the requested behavior requires a public contract change or a new general mechanism, reopen the scope/workflow decision instead of calling it mechanical.

### Consumer and verification boundary — earlier asset proposal

The final affected surfaces and evidence boundary are defined by the approved choice strategy and compact design; export/installed-reference obligations below are superseded.

Affected consumers: native lint/editor/branch checks; existing tests/helpers; packaging script/manifest and build prerequisites; installed asset inventory; fresh-init copy; optional owner adoption; setup/release notes and existing version parity assertions. Unaffected: execution DTOs, generic selection algorithm, adapter entrypoints/protocols, tool catalog, phase/state/planning policies, quality preflight selection, template contracts and normal template-only renewal.

During repair, adapt the narrow existing tests proving each public behavior and run relevant Python gates per file type. Reuse packaging/CLI/init fixtures for faithful section export and installed optional-file preservation; prove exact wheel/sdist/installed references using actual artifacts. Keep full configured verification in Validation. No Research full suite was run, no production/test repair is implemented yet, and 179 remains the intentionally failing baseline.

### Final owner-approved direction: configuration choice, not effective source

The owner accepts a meaningful choice declaration in checks.yaml/tests.yaml/fixes.yaml and asks for its design within a bounded issue. This supersedes both optional native-config distribution/export and the proposed universal missing-file prerequisite. Record a declared configuration choice, not a claimed resolved native configuration source.

The choice belongs to the owner-authored operation binding. No adapter-package manifest mutation, copied sample files, native-config serializer or startup prerequisite survey is in scope. Existing native args, parsing and discovery remain unchanged. An unselected choice blocks an applicable execution; a selected choice documents intent without proving a particular file was loaded or its policy is correct. Caller argument replacement remains supported and reported by the existing args_source facts.

A nullable/unset state is intentional setup state, not successful execution or legacy fallback. The server must remain available for setup and health/recovery; refusal occurs on relevant use. Syntax/no-config cases receive an explicit not-applicable choice instead of invented files. Package-config routing is not added where packages do not actually provide it.

### Bounded Chore assessment

The active Chore implementation contract permits one coherent code/config/test/docs maintenance change. Retain the existing phase sequence; no new workflow phase or initialize_project recovery is required. A compact design artifact can define the maintenance contract before the normal Research → Implementation review without creating separate Design/Planning phases.

Scope cap: one binding choice contract across the three existing YAML models and the existing selection/content-check/test/fix admission routes; one shared factual refusal vocabulary in existing result envelopes; configured presentation and one setup-guide boundary. Fresh --init resets the three newly copied pgmcp binding declarations to unresolved ownership without changing native settings or the unchanged asset compiler; existing workspace configuration and template-only renewal are untouched. Setup refusal is a not-executed outcome and blocks both content policies; report still permits its existing executed failed/unavailable results. Commit-artifact preflight is covered through its existing scaffold profile, not a new direct Git admission dependency. Adapter wires/entrypoints, source resolution, native argv semantics, template/phase/state engines and asset compiler remain unchanged. Combined with the already bounded native-lint/test cleanup, this remains a coherent quality-setup maintenance issue.

If design/QA finds a need for a resolved-config engine, native selector rewriting, package-config activation, startup survey, or generalized policy/rollout framework, stop and reconsider workflow/scope with Coordination. Chore is not permission to skip design, targeted behavior evidence or phase-owned full Validation.

### Owner revision: deliberate setup and missing native configuration — historical intermediate direction

On 2026-10-12 the owner questioned distributing project-derived examples and maintaining tool/version-specific export builders. The requested research direction is deliberate workspace setup, clear installation guidance, and quality calls that refuse absent required native configuration; server-startup refusal is a deeper alternative to assess, not an approved implementation. Do not build the earlier asset exporter while this decision is reopened.

The current setup/bootstrap guides mention native prerequisite provisioning but do not provide a complete explicit task for native quality policy: source/test roots, Python version/platform, rule/severity choices, discovery/exclusions, CLI-versus-file policy and an actual initial check. Expand the existing installation guide at that boundary rather than scattering rules across agent files/contracts. Document per-tool differences and existing owner-config precedence; no one-size root-file copy should be presented as completed setup.

### Live missing-config probes through existing tools

Verified the three named .pgmcp/temp/issue319-missing-native.{toml,json,cjs} paths were absent; no probe file was created or any real config moved. Independent calls used scope='targets', checks=[one binding], and preserved relevant severity/offline flags. Code target was mcp_server/managers/state_version_validator.py; Markdown target was this research document. Each timeout was90 seconds.

| Tool | Native argument supplied | Observed public outcome |
| --- | --- | --- |
| Ruff0.15.6 | --config .pgmcp/temp/issue319-missing-native.toml | Check unavailable / unsupported_input; native invalid-value diagnostic names the missing --config argument. No passed check. |
| Mypy1.19.1 | --config-file .pgmcp/temp/issue319-missing-native.toml | Check unavailable / invalid_configuration; Cannot find config file. |
| Pyright1.1.408 | --project .pgmcp/temp/issue319-missing-native.json, --level warning --warnings | Check unavailable / invalid_configuration; native config-read message names cwd rather than the requested path. This is not proof of a precise missing-path presentation. |
| Lychee0.24.2 | --config .pgmcp/temp/issue319-missing-native.toml, --offline --cache=false --include-fragments | Check unavailable / invalid_configuration; file-not-found from existing native-config inspection. |
| Pytest9.0.2 | run_tests(scope='targets', targets=['tests/mcp_server/unit/test_cli.py'], tests=['python_tests'], args={'python_tests':['-c','.pgmcp/temp/issue319-missing-native.toml','--collect-only','-q']}, timeout_seconds=90) | Test result failed; native child exit1 and FileNotFoundError traceback. It stopped in config loading before test collection; no test assertions ran. This is refusal, but not a tidy typed configuration-unavailable result. |

The four check operations have success=true with run_status=incomplete and an unavailable row: successful orchestration must not be mistaken for a passed native check. The adapter process captures exit3; native dependency identities are explicit. Pytest's observed response is materially different and should be kept visible. Commitlint --config support is source/official-CLI evidence only, not live-probed here because its public check is content-only. Syntax tools and CLI-only/schema-driven tools still need their own applicability decision; a native-file requirement cannot honestly apply to every tool.

### Configuration policy versus unconditional enforcement — historical alternatives

The final choice gate above supersedes a universal file-presence gate. This comparison explains the trade-off that led to the owner decision; neither missing-file prerequisite nor startup blocking is the selected implementation.

Existing check_selection.py:371 and test_service.py:290 replace a binding's default_args when the caller supplies args. Therefore explicit native file flags in default_args are a useful configured-call policy but are bypassable by ordinary argument replacement. They are not an unconditional file-prerequisite contract. Requires_file in adapter manifests describes content-input scratch requirements, not workspace setup; do not repurpose it.

| Route | What it guarantees | Cost / limitation |
| --- | --- | --- |
| Installation task plus explicit native flags in configured defaults | Calls using those defaults refuse missing named configs through current native tools. Owner-selected policy and paths stay visible. | Mostly docs/config, but explicit caller args can omit the flags. File presence alone does not certify complete tool sections or correct selection. |
| Declarative workspace file prerequisites checked before relevant invocation | Can refuse missing owner-declared files even when native args are overridden, without parsing native configuration or hardcoding tool names. | This does not exist today: needs a bounded configuration/execution contract and consistent check/test/fix/content handling. Confirm scope/workflow before designing it. Existence still does not prove that native args consumed the file or that its policy is suitable. |
| Refuse server startup on native setup omissions | Strong early admission boundary for declared startup prerequisites. | Can prevent health/recovery and unrelated tools from helping finish setup; heavier than call-time refusal. No startup change is recommended or implemented by this research. |

Recommended next decision: keep native policy repairs and make quality-tool setup a concrete owner/agent installation task. Do not ship project-config builders. Decide whether configured defaults plus explicit native arguments are sufficient, or missing-file refusal must hold for every relevant call despite args overrides. If the latter is required, treat it as a small explicit call-time requirement feature with its own approved boundary; do not pretend it is already enforced by configuration. Native tools remain responsible for parsing/policy; PGMCP must not infer resolved config or audit all tool-version defaults.


## Questions

No remaining owner-level placement/enforcement choice for the selected bounded strategy. Compact design and independent QA must verify the concrete binding/refusal semantics before Implementation. Coordination must replace the issue body's obsolete sample-asset acceptance criteria.

## Approved Strategy

Owner-approved final strategy: preserve and repair the activated native lint policy; add a truthful, owner-authored configuration-choice declaration to checks/tests/fixes bindings; refuse relevant use while the choice is unresolved; document deliberate workspace setup. Preserve native argument replacement/discovery and report actual argument origin rather than claiming effective config sources. Syntax and other no-file cases remain legitimate. Public tool inputs and adapter protocols/entrypoints remain intact; any new choice-refusal fact uses the existing result envelopes and configured presentation. Missing/empty choice represents unresolved setup and must not silently continue old execution. Existing owners must acknowledge the chosen policy; do not add a compatibility bridge. No sample/config assets, exporter, native-file existence mandate, package configuration router, startup refusal or broad architecture rewrite. Issue remains Chore only under the scope cap above. The issue's v3.1.0 preparation target is retained provisionally; final release assessment must describe the new acknowledgement requirement and confirm the resulting public contract impact.

Owner-approved lint repair, 2026-10-12: runtime server identity uses installed `phase-gate-mcp` metadata exclusively, including editable development installs. Remove repository-manifest/default-version fallbacks and the special treatment of version 1.0.0; missing or defective metadata remains an error. This decision concerns server identity, separately from the quality bindings' unchanged fail-on-use setup policy. Refresh editable installation metadata when the package version changes. Adapt existing public version behavior tests and remove the obsolete fallback/content-parity test; no compatibility route is retained.

Owner-approved phase-readiness repair, 2026-10-12: retain the phase-policy rejection for FileNotFoundError and StateNotFoundError only. Propagate every other state-reader failure unchanged through existing error boundaries, so corrupted/unreadable state is not presented as a phase mismatch. No phase-policy or presentation mechanism change; adapt the existing public enforcement behavior test.

Owner-approved context-loaded repair, 2026-10-12: retain missing-state bootstrap and issue-mismatch bypasses, but remove the catch that suppresses other state-read/issue-extraction failures before consulting the context-loaded flag. Those failures propagate unchanged even when the flag is true. The context cache, reset lifecycle, configured exemptions and presentation remain unchanged. Repair invalid existing state fixtures and adapt one existing public gate test.

Owner-approved note-parser repair, 2026-10-12: catch only ValueError while extracting note-format placeholders. Invalid format syntax remains visible through the existing formatting-error output; unexpected parser errors propagate. Do not change format-error presentation or the separate formatting error boundaries. Adapt the existing public note-rendering test, with no new test file.

Owner-approved test-helper repair, 2026-10-12: remove the broad Settings failure fallback in get_default_server_root. Real configuration errors propagate to test setup instead of selecting .pgmcp silently; retain the separate explicit Mock provisions. Adapt the existing root-resolution test to default/custom settings and invalid YAML, without a new test file.

Owner-approved Git test-helper repair, 2026-10-12: remove the merge-base failure-to-False conversion in _has_net_diff. Git failures retain their native diagnosis; the two existing positive assertions remain unchanged. Run the existing affected integration test, without adding helper/regression tests.

Owner-approved unused-helper cleanup, 2026-10-12: delete _path_in_head_tree after repository search confirms no production/test callers. Do not add behavior or tests for unused code. This completes the eight fallback/classification items; protective exception boundaries and archive selection remain separate owner decisions.

## Expected Results

The selected strict lint policy passes after bounded justified repairs. Existing command/error/cleanup/cancellation behavior remains correct. Valid binding choices permit existing native calls with unchanged argument selection; unresolved choices produce a factual configured diagnostic before applicable adapter execution or fix mutation. Startup remains usable for setup/recovery. No implicit source/policy guarantee is claimed. Setup instructions explain all nine tools and demonstrate a deliberate initial scoped verification. No expanded asset builder/distribution scope.

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

### A declaration could falsely claim effective native configuration.

Use choice/intent vocabulary; preserve args_source facts. No resolved-source claim, native file interpretation or mandatory sample activation. Inspect all invocation routes for the same unresolved-choice guard.

## Related Documents

- [Issue319](<https://github.com/MikeyVK/phase-gate-mcp/issues/319>)
- [Architecture Principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Adapter contract](<../../reference/execution-adapters.md>)
- [Release assets procedure](<../../reference/release-assets-procedure.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-12 | @imp researcher | Activate authorized native policy, classify current diagnostics and compare bounded optional configuration distribution strategies. |
| 0.2 | 2026-10-12 | @imp researcher | Reopen native asset/export proposal; document live missing-config refusals, default-argument override boundary and focused workspace setup alternatives. |
| 0.3 | 2026-10-12 | @imp researcher | Classify all nine adapters into native-file, conditional/CLI and no-file cases; propose exact invocation requirement and installation scope. |
| 0.4 | 2026-10-12 | @imp researcher | Capture owner-approved truthful choice gate and cap Chore scope; supersede assets, file-prerequisite and startup-blocking proposals. |

