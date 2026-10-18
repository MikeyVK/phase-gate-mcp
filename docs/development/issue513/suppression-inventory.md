<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 513 — Checker Suppression Inventory

**Status:** Research disposition complete for independent review — repair remains future delivery  
**Version:** 0.10  
**Last Updated:** 2026-10-17

## Purpose

Keep one complete location index for substantive reassessment; an entry is not automatically a defect or an approved permanent exception.

**Final owner direction:** complete #513 as research; migrate to Python>=3.15/SDK2.3 and the tested coherent checker/dependency set first, then repair remaining suppressions on that baseline. Preserve initialized2025-11-25 operation and useful runtime guards. Correct ordinary helpers and use precise necessary test exceptions instead of blanket ANN/ARG/untyped-helper exemptions. No production/configuration/test changes occur here. The [final disposition](#final-disposition-proposal-for-owner-decision) supersedes earlier provisional recommendations. Actual source-removal/masking measurements and final source-group review are complete; delivery verification remains separate.

## Scope In

Actual native selections/ignores/overrides, true local directives and directly relevant warning policy for the active production/test surface.

## Scope Out

No automatic expansion into caches, generated assets, archive documentation, every unselected Ruff rule or intentionally inapplicable native scanning.

## Summary

The original scoped scan covered **472 production/test Python files**, with zero tokenize/AST errors, and found **278 comment lines in 76 files**. The later [actual-source analysis](#actual-source-removal-impact-2026-10-17) covers473 active files and281 comment lines/77 files by including root test infrastructure and excluding intentionally invalid fixtures. Original family counts: 201 Ruff, 59 Mypy, 13 Pyright and 9 Pylint directives; four lines belong to multiple families. String-literal fixture text was excluded using Python tokenize. Generated assets/caches were excluded; any native-excluded source fixture is explicitly tagged by the collector. The configured native policy is recorded separately.

Baseline: Python 3.13.7, MCP 1.30.0, Pydantic 2.11.7, Ruff 0.15.6, Mypy 1.19.1 and Pyright 1.1.408. The isolated SDK probe uses MCP 2.3.0/Pydantic 2.14.1, not a modified baseline environment. No final per-group disposition is claimed yet.

## Native Policy

**Evidence chronology:** the sections before Final Disposition preserve earlier measurements and provisional recommendations. Their open/proposed wording is historical; the final disposition, actual-removal results and final source-group assessment govern the current research conclusion.

| Tool/source | Observed policy and reassessment state |
| --- | --- |
| [Ruff](../../../pyproject.toml) | select=E, W, F, I, N, UP, ANN, B, C4, DTZ, T10, T20, ISC, RET, SIM, ARG, PLC. extend-select=G004, BLE001, SLF001. Global ignore is empty. tests/**/*.py ignores ANN and ARG families; other source exclusions cover cache/archive/intentional validation fixtures. Selection/exclusion is policy, not itself evidence of a defect. |
| [Mypy](../../../pyproject.toml) | Strict production scope, Pydantic plugin with init_typed/init_forbid_extra; warn_unused_ignores=true. tests.* overrides disallow_untyped_defs=false. No global disable_error_code or ignore_missing_imports=true. Original rationale for the test override is not established by this inventory. |
| [Pyright](../../../pyrightconfig.json) | strict with 27 explicitly false report flags, listed below; some may coincide with a native default. Establish each flag's effective signal before classifying it as debt or removing it. |
| Warning policy | No pytest filterwarnings, relevant source filterwarnings/simplefilter/catch_warnings or PYTHONWARNINGS override found in the searched active Python/binding surface. No new blanket filters were added. |
| Binding arguments | defaults/checks.yaml Python lint/Mypy arguments are empty; Pyright has --level warning --warnings. Root overrides acknowledge native_discovery, not new diagnostic suppressions. Tests/fixes have empty default_args. Other capability arguments are unrelated schema/offline-link policy. |
| Pylint comments | Nine historical comments remain in source/tests; current check bindings do not run Pylint. They are inventoried as non-effective commentary, not current native checker policy. |

## Explicit Pyright Flags

[pyrightconfig.json](../../../pyrightconfig.json), JSON properties with value false:

- L80: `reportArgumentType`
- L68: `reportAssertAlwaysTrue`
- L82: `reportAttributeAccessIssue`
- L64: `reportCallInDefaultInitializer`
- L81: `reportCallIssue`
- L79: `reportFunctionMemberAccess`
- L70: `reportImplicitStringConcatenation`
- L74: `reportIncompleteStub`
- L61: `reportMissingParameterType`
- L53: `reportMissingSuperCall`
- L62: `reportMissingTypeArgument`
- L31: `reportMissingTypeStubs`
- L54: `reportUninitializedInstanceVariable`
- L57: `reportUnknownArgumentType`
- L58: `reportUnknownLambdaType`
- L60: `reportUnknownMemberType`
- L56: `reportUnknownParameterType`
- L59: `reportUnknownVariableType`
- L66: `reportUnnecessaryCast`
- L67: `reportUnnecessaryComparison`
- L65: `reportUnnecessaryIsInstance`
- L46: `reportUntypedBaseClass`
- L45: `reportUntypedClassDecorator`
- L44: `reportUntypedFunctionDecorator`
- L47: `reportUntypedNamedTuple`
- L33: `reportUnusedClass`
- L34: `reportUnusedFunction`

## Ruff Groups and First Disposition Evidence

| Rule | Local occurrences | Current evidence / unfinished disposition |
| --- | ---: | --- |
| PLC0415 | 145 | Exact source comments below; otherwise original rationale is unknown. Some annotations overlap native per-test ignores or no longer apply. Per-group positive+negative proof remains open. |
| T201 | 5 | Exact source comments below; otherwise original rationale is unknown. Some annotations overlap native per-test ignores or no longer apply. Per-group positive+negative proof remains open. |
| BLE001 | 10 | Boundary/cleanup rationales exist; some are now reported unused below. Reassess suppression without deleting necessary catch/cleanup/diagnosis. |
| UP046 | 7 | Seven #507 declaration exceptions have explicit variance/library rationale and remain subject to current/candidate positive+negative comparison. |
| ANN401 | 10 | Exact source comments below; otherwise original rationale is unknown. Some annotations overlap native per-test ignores or no longer apply. Per-group positive+negative proof remains open. |
| ARG002 | 12 | Exact source comments below; otherwise original rationale is unknown. Some annotations overlap native per-test ignores or no longer apply. Per-group positive+negative proof remains open. |
| N818 | 1 | Source says domain-event name, not technical error; verify protected public naming before changing. |
| ARG001 | 5 | Exact source comments below; otherwise original rationale is unknown. Some annotations overlap native per-test ignores or no longer apply. Per-group positive+negative proof remains open. |
| SLF001 | 3 | Exact source comments below; otherwise original rationale is unknown. Some annotations overlap native per-test ignores or no longer apply. Per-group positive+negative proof remains open. |
| B017 | 5 | Broad exception assertions: one comment claims Pydantic version variance; other original rationales are unknown. Test actual exception contract rather than preserve an overbroad assertion by default. |

The diagnostic run retained native rule selection and added only RUF100; it did not disable underlying rules or per-file policy. **19 RUF100 diagnostics** and no other diagnostic code were observed. These are proposed annotation-removal candidates under the current policy, not approval to remove the underlying exception handling, type contracts or tests.

| Source | Line | Observed native diagnostic |
| --- | ---: | --- |
| [mcp_server/core/error_handling.py](../../../mcp_server/core/error_handling.py) | 136 | Unused 'noqa' directive (unused: 'BLE001') |
| [mcp_server/managers/project_manager.py](../../../mcp_server/managers/project_manager.py) | 295 | Unused 'noqa' directive (unused: 'BLE001') |
| [mcp_server/tools/discovery_tools.py](../../../mcp_server/tools/discovery_tools.py) | 84 | Unused 'noqa' directive (unused: 'ANN401') |
| [mcp_server/tools/git_tools.py](../../../mcp_server/tools/git_tools.py) | 442 | Unused 'noqa' directive (unused: 'BLE001') |
| [mcp_server/tools/git_tools.py](../../../mcp_server/tools/git_tools.py) | 446 | Unused 'noqa' directive (unused: 'BLE001') |
| [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py) | 117 | Unused 'noqa' directive (unused: 'ANN401') |
| [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py) | 223 | Unused 'noqa' directive (unused: 'ANN401') |
| [tests/mcp_server/test_support.py](../../../tests/mcp_server/test_support.py) | 566 | Unused 'noqa' directive (non-enabled: 'ANN401') |
| [tests/mcp_server/unit/adapters/test_github_adapter.py](../../../tests/mcp_server/unit/adapters/test_github_adapter.py) | 32 | Unused 'noqa' directive (non-enabled: 'ARG001') |
| [tests/mcp_server/unit/adapters/test_github_adapter.py](../../../tests/mcp_server/unit/adapters/test_github_adapter.py) | 62 | Unused 'noqa' directive (non-enabled: 'ARG001') |
| [tests/mcp_server/unit/config/test_settings.py](../../../tests/mcp_server/unit/config/test_settings.py) | 43 | Unused 'noqa' directive (non-enabled: 'ARG001') |
| [tests/mcp_server/unit/core/test_note_context_unit.py](../../../tests/mcp_server/unit/core/test_note_context_unit.py) | 24 | Unused 'noqa' directive (non-enabled: 'ANN401') |
| [tests/mcp_server/unit/managers/test_enforcement_runner.py](../../../tests/mcp_server/unit/managers/test_enforcement_runner.py) | 93 | Unused 'noqa' directive (non-enabled: 'ARG001') |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c1.py](../../../tests/mcp_server/unit/managers/test_phase_state_engine_c1.py) | 162 | Unused 'noqa' directive (non-enabled: 'ARG001') |
| [tests/mcp_server/unit/managers/test_workflow_status_resolver.py](../../../tests/mcp_server/unit/managers/test_workflow_status_resolver.py) | 104 | Unused 'noqa' directive (non-enabled: 'ARG002') |
| [tests/mcp_server/unit/resources/test_base.py](../../../tests/mcp_server/unit/resources/test_base.py) | 21 | Unused 'noqa' directive (non-enabled: 'ARG002') |
| [tests/mcp_server/unit/resources/test_resources_base.py](../../../tests/mcp_server/unit/resources/test_resources_base.py) | 17 | Unused 'noqa' directive (non-enabled: 'ARG002') |
| [tests/mcp_server/unit/server/test_validate_tool_arguments.py](../../../tests/mcp_server/unit/server/test_validate_tool_arguments.py) | 73 | Unused 'noqa' directive (non-enabled: 'ARG002') |
| [tests/mcp_server/unit/tools/test_initialize_project_tool.py](../../../tests/mcp_server/unit/tools/test_initialize_project_tool.py) | 227 | Unused 'noqa' directive (non-enabled: 'ARG002') |

## Exact Local Directive Locations

Original rationale is retained when written in the comment or explained by final #507 evidence. A bare directive's historical rationale is **unknown** until supported by source/history/behavior evidence; location alone never grants retention. The single unqualified type:ignore is tests/mcp_server/unit/resources/test_base.py:47. Final remove/smaller/retain decisions and reassessment triggers remain Research work.

| Source | Exact comment locations and authored rationale |
| --- | --- |
| [mcp_server/adapters/git_adapter.py](../../../mcp_server/adapters/git_adapter.py) | L175: # type: ignore[assignment] |
| [mcp_server/adapters/github_adapter.py](../../../mcp_server/adapters/github_adapter.py) | L24: # pylint: disable=no-member<br>L34: # pylint: disable=no-member<br>L36: # pylint: disable=no-member |
| [mcp_server/cli.py](../../../mcp_server/cli.py) | L68: # noqa: PLC0415<br>L74: # pylint: disable=no-member<br>L75: # noqa: T201<br>L81: # noqa: T201<br>L98: # noqa: PLC0415<br>L110: # noqa: T201<br>L115: # noqa: BLE001 -- Terminal CLI boundary preserves exception diagnostics.<br>L122: # noqa: T201<br>L129: # noqa: PLC0415 |
| [mcp_server/cli_renewal.py](../../../mcp_server/cli_renewal.py) | L235: # noqa: BLE001 -- Terminal CLI boundary preserves exception diagnostics.<br>L258: # noqa: BLE001 -- Terminal CLI composition boundary preserves diagnostics. |
| [mcp_server/config/schemas/adapter_manifest.py](../../../mcp_server/config/schemas/adapter_manifest.py) | L146: # noqa: UP046 -- Pydantic 2.11 cannot resolve validator TypeVars after migration; reassess in #513. |
| [mcp_server/config/schemas/label_config.py](../../../mcp_server/config/schemas/label_config.py) | L81: # noqa: ANN401 |
| [mcp_server/config/settings.py](../../../mcp_server/config/settings.py) | L65: # type: ignore[prop-decorator] |
| [mcp_server/config/validator.py](../../../mcp_server/config/validator.py) | L138: # noqa: ARG002 |
| [mcp_server/core/decorators/input_validation_decorator.py](../../../mcp_server/core/decorators/input_validation_decorator.py) | L115: # type: ignore[arg-type] |
| [mcp_server/core/decorators/tool_error_handler_decorator.py](../../../mcp_server/core/decorators/tool_error_handler_decorator.py) | L37: # noqa: UP046 -- Preserve invariant wrapper contract; reassess in #513. |
| [mcp_server/core/error_handling.py](../../../mcp_server/core/error_handling.py) | L39: # noqa: PLC0415 -- Avoid eager core/schema imports.<br>L69: # noqa: ANN401<br>L136: # noqa: BLE001 |
| [mcp_server/core/exceptions.py](../../../mcp_server/core/exceptions.py) | L58: # noqa: ANN401  # Core layer; TemplateSchema would violate layer deps |
| [mcp_server/core/interfaces/execution.py](../../../mcp_server/core/interfaces/execution.py) | L49: # noqa: UP046 -- Preserve explicit covariance; reassess in #513.<br>L57: # type: ignore[misc] |
| [mcp_server/core/interfaces/gate.py](../../../mcp_server/core/interfaces/gate.py) | L25: # noqa: N818 - domain event name, not a technical error type |
| [mcp_server/core/interfaces/icore_tool.py](../../../mcp_server/core/interfaces/icore_tool.py) | L25: # type: ignore[misc]  # pyright: ignore[reportInvalidTypeVarUse]  # noqa: UP046 -- Preserve invariant protocol parameters; reassess in #513. |
| [mcp_server/core/interfaces/tool_input_contract.py](../../../mcp_server/core/interfaces/tool_input_contract.py) | L36: # noqa: UP046 -- Preserve explicit covariance; reassess in #513. |
| [mcp_server/core/tool_execution.py](../../../mcp_server/core/tool_execution.py) | L53: # noqa: UP046 -- Preserve explicit covariance; reassess in #513. |
| [mcp_server/execution/content_input.py](../../../mcp_server/execution/content_input.py) | L176: # noqa: BLE001 -- Preserve the primary failure or cancellation during cleanup.<br>L185: # noqa: BLE001 -- Preserve the primary failure or cancellation during cleanup.<br>L248: # noqa: BLE001 -- Preserve the primary failure or cancellation during cleanup. |
| [mcp_server/execution/protocol.py](../../../mcp_server/execution/protocol.py) | L59: # noqa: UP046 -- Preserve invariant request admission; reassess in #513. |
| [mcp_server/managers/github_manager.py](../../../mcp_server/managers/github_manager.py) | L140: # pylint: disable=too-many-arguments,too-many-positional-arguments<br>L155: # pylint: disable=too-many-arguments,too-many-positional-arguments<br>L216: # pylint: disable=too-many-arguments,too-many-positional-arguments |
| [mcp_server/managers/project_manager.py](../../../mcp_server/managers/project_manager.py) | L295: # noqa: BLE001 -- Enrich post-write failure without discarding its cause. |
| [mcp_server/resources/github.py](../../../mcp_server/resources/github.py) | L18: # noqa: ARG002 |
| [mcp_server/resources/standards.py](../../../mcp_server/resources/standards.py) | L26: # noqa: ARG002 |
| [mcp_server/resources/status.py](../../../mcp_server/resources/status.py) | L21: # noqa: ARG002 |
| [mcp_server/server.py](../../../mcp_server/server.py) | L1: # pyright: reportMissingImports=false<br>L84: # type: ignore[no-untyped-call, untyped-decorator]<br>L96: # type: ignore[no-untyped-call, untyped-decorator]<br>L108: # type: ignore[no-untyped-call, untyped-decorator]<br>L125: # type: ignore[untyped-decorator]<br>L266: # noqa: PLC0415<br>L270: # noqa: PLC0415<br>L271: # noqa: PLC0415 |
| [mcp_server/services/template_engine.py](../../../mcp_server/services/template_engine.py) | L46: # noqa: ANN401 |
| [mcp_server/state/response_cache.py](../../../mcp_server/state/response_cache.py) | L41: # noqa: ARG002 |
| [mcp_server/tools/admin_tools.py](../../../mcp_server/tools/admin_tools.py) | L32: # noqa: ANN401<br>L223: # noqa: T201 - proxy protocol marker |
| [mcp_server/tools/discovery_tools.py](../../../mcp_server/tools/discovery_tools.py) | L3: # pyright: reportIncompatibleMethodOverride=false<br>L84: # noqa: ANN401, ARG002 |
| [mcp_server/tools/git_tools.py](../../../mcp_server/tools/git_tools.py) | L442: # noqa: BLE001 -- Restore state before propagating to the wrapper.<br>L446: # noqa: BLE001 -- Preserve the original commit error. |
| [mcp_server/tools/phase_tools.py](../../../mcp_server/tools/phase_tools.py) | L138: # noqa: PLC0415 |
| [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py) | L117: # noqa: ANN401, ARG002<br>L223: # noqa: ANN401 |
| [tests/mcp_server/integration/execution/test_process_runtime.py](../../../tests/mcp_server/integration/execution/test_process_runtime.py) | L266: # type: ignore[misc] |
| [tests/mcp_server/integration/test_ready_phase_enforcement.py](../../../tests/mcp_server/integration/test_ready_phase_enforcement.py) | L129: # type: ignore[arg-type]<br>L146: # type: ignore[arg-type] |
| [tests/mcp_server/managers/test_phase_state_engine_async.py](../../../tests/mcp_server/managers/test_phase_state_engine_async.py) | L2: # pyright: reportPrivateUsage=false<br>L37: # noqa: PLC0415<br>L39: # noqa: PLC0415<br>L92: # noqa: PLC0415<br>L94: # noqa: PLC0415 |
| [tests/mcp_server/test_support.py](../../../tests/mcp_server/test_support.py) | L73: # noqa: PLC0415<br>L75: # noqa: PLC0415<br>L302: # noqa: PLC0415<br>L349: # noqa: PLC0415<br>L361: # type: ignore[arg-type]<br>L363: # type: ignore[arg-type]<br>L461: # noqa: PLC0415<br>L462: # noqa: PLC0415<br>L540: # noqa: PLC0415<br>L541: # noqa: PLC0415<br>L542: # noqa: PLC0415<br>L545: # noqa: PLC0415<br>L546: # noqa: PLC0415<br>L547: # noqa: PLC0415<br>L566: # noqa: ANN401 |
| [tests/mcp_server/unit/adapters/test_github_adapter.py](../../../tests/mcp_server/unit/adapters/test_github_adapter.py) | L32: # noqa: ARG001 -- Fixture patches the external client.<br>L62: # noqa: ARG001 |
| [tests/mcp_server/unit/config/test_contracts_config.py](../../../tests/mcp_server/unit/config/test_contracts_config.py) | L18: # type: ignore[arg-type]<br>L88: # type: ignore[misc] |
| [tests/mcp_server/unit/config/test_presentation_config.py](../../../tests/mcp_server/unit/config/test_presentation_config.py) | L142: # type: ignore[misc] |
| [tests/mcp_server/unit/config/test_settings.py](../../../tests/mcp_server/unit/config/test_settings.py) | L43: # noqa: ARG001 |
| [tests/mcp_server/unit/config/test_workflow_config.py](../../../tests/mcp_server/unit/config/test_workflow_config.py) | L21: # type: ignore[import-untyped]<br>L123: # type: ignore[arg-type]<br>L132: # type: ignore[call-arg] |
| [tests/mcp_server/unit/config/test_workflow_config_c6.py](../../../tests/mcp_server/unit/config/test_workflow_config_c6.py) | L123: # type: ignore[call-arg]<br>L183: # type: ignore[arg-type]<br>L192: # type: ignore[arg-type] |
| [tests/mcp_server/unit/core/test_note_context_unit.py](../../../tests/mcp_server/unit/core/test_note_context_unit.py) | L24: # noqa: ANN401<br>L103: # noqa: PLC0415 |
| [tests/mcp_server/unit/core/test_tool_error_handler_c4.py](../../../tests/mcp_server/unit/core/test_tool_error_handler_c4.py) | L133: # type: ignore[call-arg]<br>L136: # type: ignore[call-arg]<br>L139: # type: ignore[call-arg]<br>L142: # type: ignore[call-arg] |
| [tests/mcp_server/unit/dtos/test_upgrade_log.py](../../../tests/mcp_server/unit/dtos/test_upgrade_log.py) | L28: # type: ignore[misc]<br>L42: # type: ignore[call-arg]<br>L56: # type: ignore[arg-type] |
| [tests/mcp_server/unit/managers/test_consumers_c4.py](../../../tests/mcp_server/unit/managers/test_consumers_c4.py) | L93: # noqa: PLC0415<br>L205: # noqa: PLC0415<br>L206: # noqa: PLC0415<br>L207: # noqa: PLC0415<br>L230: # noqa: SLF001  # pyright: ignore[reportPrivateUsage] |
| [tests/mcp_server/unit/managers/test_enforcement_runner.py](../../../tests/mcp_server/unit/managers/test_enforcement_runner.py) | L93: # noqa: ARG001 |
| [tests/mcp_server/unit/managers/test_git_manager.py](../../../tests/mcp_server/unit/managers/test_git_manager.py) | L7: # pyright: reportCallIssue=false, reportAttributeAccessIssue=false, reportPrivateUsage=false<br>L279: # type: ignore[call-arg] |
| [tests/mcp_server/unit/managers/test_note_migration.py](../../../tests/mcp_server/unit/managers/test_note_migration.py) | L14: # noqa: PLC0415 |
| [tests/mcp_server/unit/managers/test_phase_contract_resolver_c3.py](../../../tests/mcp_server/unit/managers/test_phase_contract_resolver_c3.py) | L111: # noqa: SLF001 |
| [tests/mcp_server/unit/managers/test_phase_state_engine_c1.py](../../../tests/mcp_server/unit/managers/test_phase_state_engine_c1.py) | L162: # noqa: ARG001 |
| [tests/mcp_server/unit/managers/test_project_manager.py](../../../tests/mcp_server/unit/managers/test_project_manager.py) | L905: # pyright: ignore[reportPrivateUsage]  # noqa: SLF001 — inject test double: no public setter<br>L943: # type: ignore[operator]<br>L1036: # noqa: PLC0415<br>L1037: # noqa: PLC0415 |
| [tests/mcp_server/unit/managers/test_workflow_status_resolver.py](../../../tests/mcp_server/unit/managers/test_workflow_status_resolver.py) | L66: # type: ignore[misc]<br>L70: # type: ignore[call-arg]<br>L104: # noqa: ARG002<br>L242: # type: ignore[arg-type]<br>L251: # type: ignore[arg-type]<br>L261: # type: ignore[arg-type]<br>L270: # type: ignore[arg-type] |
| [tests/mcp_server/unit/resources/test_base.py](../../../tests/mcp_server/unit/resources/test_base.py) | L7: # pyright: reportCallIssue=false, reportAttributeAccessIssue=false<br>L21: # noqa: ARG002<br>L46: # pylint: disable=abstract-class-instantiated<br>L47: # type: ignore |
| [tests/mcp_server/unit/resources/test_resources_base.py](../../../tests/mcp_server/unit/resources/test_resources_base.py) | L17: # noqa: ARG002 |
| [tests/mcp_server/unit/schemas/test_presentation_output.py](../../../tests/mcp_server/unit/schemas/test_presentation_output.py) | L46: # type: ignore[misc]<br>L54: # type: ignore[call-arg]<br>L79: # type: ignore[misc]<br>L84: # type: ignore[call-arg] |
| [tests/mcp_server/unit/schemas/test_structured_tool_output_migration.py](../../../tests/mcp_server/unit/schemas/test_structured_tool_output_migration.py) | L72: # type: ignore[attr-defined] |
| [tests/mcp_server/unit/server/test_bootstrap.py](../../../tests/mcp_server/unit/server/test_bootstrap.py) | L130: # type: ignore[misc]<br>L292: # type: ignore[call-arg] |
| [tests/mcp_server/unit/server/test_validate_tool_arguments.py](../../../tests/mcp_server/unit/server/test_validate_tool_arguments.py) | L28: # noqa: PLC0415<br>L73: # noqa: ARG002 |
| [tests/mcp_server/unit/test_cli.py](../../../tests/mcp_server/unit/test_cli.py) | L95: # noqa: PLC0415<br>L205: # noqa: PLC0415<br>L207: # noqa: PLC0415<br>L239: # noqa: PLC0415<br>L241: # noqa: PLC0415<br>L328: # noqa: PLC0415 |
| [tests/mcp_server/unit/test_server.py](../../../tests/mcp_server/unit/test_server.py) | L1: # pyright: reportMissingImports=false<br>L75: # noqa: PLC0415<br>L718: # noqa: PLC0415<br>L720: # noqa: PLC0415<br>L721: # noqa: PLC0415<br>L724: # noqa: PLC0415<br>L725: # noqa: PLC0415<br>L830: # noqa: PLC0415<br>L831: # noqa: PLC0415<br>L832: # noqa: PLC0415<br>L833: # noqa: PLC0415<br>L836: # noqa: PLC0415<br>L837: # noqa: PLC0415<br>L838: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_c7_tool_conflict_handling.py](../../../tests/mcp_server/unit/tools/test_c7_tool_conflict_handling.py) | L58: # type: ignore[method-assign]<br>L59: # type: ignore[method-assign]<br>L60: # type: ignore[method-assign]<br>L61: # type: ignore[method-assign]<br>L224: # noqa: PLC0415<br>L240: # noqa: PLC0415<br>L292: # noqa: PLC0415<br>L312: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_create_issue_input.py](../../../tests/mcp_server/unit/tools/test_create_issue_input.py) | L1: # pyright: reportCallIssue=false, reportAttributeAccessIssue=false<br>L92: # type: ignore[arg-type]<br>L96: # type: ignore[arg-type] |
| [tests/mcp_server/unit/tools/test_create_issue_schema.py](../../../tests/mcp_server/unit/tools/test_create_issue_schema.py) | L39: # type: ignore[type-arg]<br>L42: # type: ignore[type-arg]<br>L48: # type: ignore[type-arg]<br>L55: # type: ignore[type-arg]<br>L62: # type: ignore[type-arg]<br>L69: # type: ignore[type-arg] |
| [tests/mcp_server/unit/tools/test_cycle_tools.py](../../../tests/mcp_server/unit/tools/test_cycle_tools.py) | L1: # pyright: reportMissingImports=false<br>L78: # noqa: PLC0415<br>L576: # noqa: PLC0415<br>L632: # noqa: PLC0415<br>L681: # noqa: PLC0415<br>L730: # noqa: PLC0415<br>L741: # noqa: PLC0415<br>L743: # noqa: PLC0415<br>L757: # noqa: PLC0415<br>L759: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py](../../../tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py) | L484: # noqa: PLC0415<br>L499: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_discovery_tools.py](../../../tests/mcp_server/unit/tools/test_discovery_tools.py) | L107: # noqa: PLC0415<br>L119: # noqa: PLC0415<br>L135: # noqa: PLC0415<br>L151: # noqa: PLC0415<br>L178: # noqa: PLC0415<br>L195: # noqa: PLC0415<br>L224: # noqa: PLC0415<br>L269: # noqa: PLC0415<br>L315: # noqa: PLC0415<br>L330: # noqa: PLC0415<br>L345: # noqa: PLC0415<br>L361: # noqa: PLC0415<br>L376: # noqa: PLC0415<br>L457: # noqa: PLC0415<br>L471: # noqa: PLC0415<br>L485: # noqa: PLC0415<br>L498: # noqa: PLC0415<br>L513: # noqa: PLC0415<br>L527: # noqa: PLC0415<br>L539: # noqa: PLC0415<br>L551: # noqa: PLC0415<br>L563: # noqa: PLC0415<br>L576: # noqa: PLC0415<br>L588: # noqa: PLC0415<br>L599: # noqa: PLC0415<br>L694: # noqa: PLC0415<br>L707: # noqa: PLC0415<br>L722: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_git_checkout_state_sync.py](../../../tests/mcp_server/unit/tools/test_git_checkout_state_sync.py) | L45: # noqa: PLC0415<br>L66: # noqa: PLC0415<br>L94: # noqa: PLC0415<br>L119: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_git_fetch_tool_behavior.py](../../../tests/mcp_server/unit/tools/test_git_fetch_tool_behavior.py) | L1: # pyright: reportPrivateUsage=false<br>L54: # noqa: PLC0415<br>L73: # noqa: PLC0415<br>L93: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_git_pull_tool_behavior.py](../../../tests/mcp_server/unit/tools/test_git_pull_tool_behavior.py) | L1: # pyright: reportPrivateUsage=false<br>L62: # noqa: PLC0415<br>L93: # noqa: PLC0415<br>L115: # noqa: PLC0415<br>L134: # noqa: PLC0415<br>L165: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_git_tools.py](../../../tests/mcp_server/unit/tools/test_git_tools.py) | L80: # noqa: B017 — Pydantic validation error; exact type varies by version<br>L87: # noqa: B017<br>L94: # noqa: B017<br>L98: # noqa: B017<br>L211: # noqa: PLC0415<br>L252: # noqa: PLC0415<br>L283: # noqa: PLC0415<br>L317: # noqa: PLC0415<br>L349: # noqa: PLC0415<br>L382: # noqa: PLC0415<br>L424: # noqa: PLC0415<br>L470: # noqa: PLC0415<br>L590: # noqa: PLC0415<br>L651: # noqa: PLC0415<br>L679: # noqa: PLC0415<br>L708: # noqa: PLC0415<br>L1612: # noqa: PLC0415<br>L1613: # noqa: PLC0415<br>L1642: # noqa: PLC0415<br>L1643: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_health_tools.py](../../../tests/mcp_server/unit/tools/test_health_tools.py) | L37: # noqa: PLC0415<br>L38: # noqa: PLC0415<br>L39: # noqa: PLC0415<br>L54: # noqa: PLC0415<br>L55: # noqa: PLC0415<br>L56: # noqa: PLC0415<br>L78: # noqa: PLC0415<br>L79: # noqa: PLC0415<br>L80: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_initialize_project_tool.py](../../../tests/mcp_server/unit/tools/test_initialize_project_tool.py) | L227: # noqa: ARG002<br>L322: # noqa: PLC0415 |
| [tests/mcp_server/unit/tools/test_issue_tools.py](../../../tests/mcp_server/unit/tools/test_issue_tools.py) | L237: # noqa: B017<br>L243: # type: ignore[arg-type] |
| [tests/mcp_server/unit/tools/test_label_tools_integration.py](../../../tests/mcp_server/unit/tools/test_label_tools_integration.py) | L37: # pylint: disable=too-few-public-methods |
| [tests/mcp_server/unit/tools/test_project_tools.py](../../../tests/mcp_server/unit/tools/test_project_tools.py) | L123: # noqa: PLC0415<br>L170: # noqa: PLC0415<br>L189: # noqa: PLC0415<br>L216: # noqa: PLC0415<br>L608: # noqa: PLC0415<br>L610: # noqa: PLC0415<br>L638: # noqa: PLC0415<br>L640: # noqa: PLC0415<br>L669: # noqa: PLC0415<br>L671: # noqa: PLC0415<br>L702: # noqa: PLC0415<br>L704: # noqa: PLC0415 |

## Reproduction and Evidence Limits

The temporary collector uses tokenize COMMENT tokens and ast imports over mcp_server/ and tests/mcp_server/, excluding assets/__pycache__/node_modules. It records each path/line/comment and source parse errors, native TOML/JSON policy and actual package versions. Invocation:

`run_tests(scope='targets',targets=['.pgmcp/temp/issue513/test_issue513_research.py'],tests=['python_tests'],args={'python_tests':['-n','0','-s','--tb=short']},timeout_seconds=180)` — 3 passed in 9.41 seconds, native exit 0; SDK shape/interop cases are separate from collection. Supplemental 535b0461c7b44d10ab929a30f7b53151; result size 56194 characters inspected, then fully read for structured inventory. The initial collector-only regex was provisional; token inventory supersedes it.

`run_checks(scope='targets',targets=the 56 source files with actual Ruff directives indexed above,checks=['python_lint'],args={'python_lint':['--extend-select','RUF100','--output-format','json']},timeout_seconds=180)` — native exit 1, exactly 19 RUF100 messages (supplemental 44e745d0213c4739b5ad69c4dc4f6e1e, 19867 characters read for all diagnostic locations). This was an intentional research diagnostic run, not a failed required gate or broad fixing operation.

Neither invocation changed production, test, native configuration or checker pins. Per-rule masked-signal controls and candidate-version dispositions are not complete.


## Executed Diagnostic Controls and Provisional Dispositions

Initial controls below use Python 3.13.7 with Ruff 0.15.6, Mypy 1.19.1 and Pyright 1.1.408; the later Python 3.15 section states its distinct process/target/dependency context. Source copies and fixtures live only below `.pgmcp/temp/issue513/`; no production/test/configuration remediation has been applied. Native check exit 1 is expected for deliberately bad controls and is not a Validation verdict.

### Ruff: all ten local rule groups

For each rule, one negative source omits the suppression and must report that rule; the paired positive source must produce no diagnostic under the same selected set. The 20-file call selected exactly `PLC0415,T201,BLE001,UP046,ANN401,ARG001,ARG002,N818,SLF001,B017` and JSON output. Outcome: exactly ten diagnostics, one expected code per negative, zero diagnostics in positives. Supplemental receipt `41056ea5837f4bc9b072cb2d704446f4`.

This establishes diagnostic sensitivity, not semantic equivalence of a generic-class rewrite. Current per-test ANN/ARG policy still masks some inline exceptions; the earlier RUF100 result identifies those redundant annotations.

| Rule/group | Evidence-backed provisional treatment | Reassessment condition |
| --- | --- | --- |
| 19 RUF100 entries above | Remove the redundant annotation or redundant code within a multi-code annotation; retain necessary catches, parameters and behavior. | Re-run native selection/RUF100 after the bounded annotation change. |
| PLC0415 | Retain only where import timing prevents an evidenced cycle/eager dependency or is part of test setup. Unexplained local imports need source/consumer review; the generic control alone does not justify all 145. | Relevant import/composition boundary change; demonstrate ordinary import and selected startup/test behavior before moving it. |
| T201 | Retain at actual CLI output and the explicit proxy restart marker; these are intentional outputs. | CLI/presentation or restart signaling contract changes. |
| BLE001 | Remove the RUF100-redundant annotations; retain narrowly justified terminal/cleanup boundaries that preserve diagnosis or an existing primary failure. | Error-wrapper/presenter or cleanup behavior changes; test original error/cancellation preservation. |
| UP046 | Retain explicit covariance/invariance choices while contracts remain binding; retain AdapterRole library workaround, reproduced below on both Pydantic versions. No automatic migration from the simple syntax control. | Re-run bound, widening/narrowing and runtime negative controls for every affected declaration with a changed Python/Pydantic/checker baseline. |
| ANN401 | Remove RUF100-redundant entries. Retain genuine dynamic/decorator/foreign-schema boundaries only with the existing architectural reason; narrower stable types remain preferred. | Boundary representation becomes typed, or a local source review establishes that Any is unnecessary. |
| ARG001/ARG002 | Remove redundant per-test annotations. Preserve required interface/fixture names; distinguish these from a genuinely unused internal argument such as ConfigValidator.workflow. | Interface/caller review demonstrates safe argument removal or signature change; do not rename a keyword contract merely for lint. |
| N818 | Keep existing exception identity during SDK assessment. GateViolation is actually a ValueError subclass; its comment calling it a non-error domain event is inaccurate and is not sufficient rationale by itself. | Explicit public exception naming policy/consumer review, rather than an incidental SDK change. |
| SLF001 | The test-double injection with no setter has a local reason. The _assemble_labels assertion tests private implementation and should move to observable CreateIssueTool behavior. | A bounded test change can prove the same public behavior without the private call; inspect fetch/pull helper imports separately. |
| B017 | Narrow all five broad assertions to Pydantic ValidationError; unchanged model declarations reject all five invalid cases with that type under both 2.11.7 and 2.14.1. | Recheck the positive and invalid model inputs after changing the actual model/library contract. No message-text assertions needed. |
| Nine Pylint comments | Remove non-effective historical directives if cleanup is approved; current bindings do not run Pylint. | Introducing a Pylint binding would require an explicit new policy, not preservation of dormant comments. |

### Pyright: all 27 false flags

The [pinned 1.1.408 strict-default source](https://raw.githubusercontent.com/microsoft/pyright/1.1.408/packages/pyright-internal/src/common/configOptions.ts) distinguishes four default-none policies from 23 actual strict-signal suppressions.

Each pair below enables only its named report flag in the file. Fixtures contain no type-ignore comments. Final evidence combines the unchanged successful pairs in `30ab8aaa4cd64f2fa276f7fe67329ee3` with the six-file refinement `bcced1723e10472e89fae0c4a87f27c6` for unknown members and function/class decorators. All 27 negative pairs report the intended rule; all 27 positive sources have no diagnostic. Unknown-lambda negative emits two messages of its own rule.

| Flag | Pinned strict default | Final paired control |
| --- | --- | --- |
| `reportArgumentType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportCallIssue` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportAttributeAccessIssue` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportFunctionMemberAccess` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportMissingParameterType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportMissingTypeArgument` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnknownParameterType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnknownArgumentType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnknownLambdaType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnknownVariableType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnknownMemberType` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnnecessaryCast` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnnecessaryIsInstance` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnnecessaryComparison` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportAssertAlwaysTrue` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnusedFunction` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUnusedClass` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUntypedFunctionDecorator` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUntypedClassDecorator` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUntypedBaseClass` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportUntypedNamedTuple` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportMissingSuperCall` | none — explicit setting matches strict default | negative reports this rule; positive reports no diagnostic |
| `reportUninitializedInstanceVariable` | none — explicit setting matches strict default | negative reports this rule; positive reports no diagnostic |
| `reportCallInDefaultInitializer` | none — explicit setting matches strict default | negative reports this rule; positive reports no diagnostic |
| `reportImplicitStringConcatenation` | none — explicit setting matches strict default | negative reports this rule; positive reports no diagnostic |
| `reportMissingTypeStubs` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |
| `reportIncompleteStub` | error — current false suppresses strict signal | negative reports this rule; positive reports no diagnostic |

Initial exploratory fixtures included an unsupported per-file enableTypeIgnoreComments setting; it was removed. Three initially insufficient negative examples were strengthened to actually introduce Unknown members/decorators. These preliminary runs are not the final positive/negative proof.

For argument, call and attribute checks, three equivalent bad sources with **no local enabling** pass under native project policy (receipt `1162c9af3293419497935dc98bde0ced`). With SDK 2.3 selected through `--pythonpath`, old accesses to Server.list_tools, Server.request_handlers, InitializeResult.protocolVersion and Tool.inputSchema also remain silent under native policy. Enabling the relevant diagnoses yields four reportAttributeAccessIssue errors; a correct SDK 2 source passes in the same call (receipt `2d438f387881425ababe2d33c929fc4d`).

Proposal: restore basic call/argument/attribute signals as part of an explicitly scoped policy decision, or replace a genuinely necessary exception at the narrow source boundary. Do not enable all 23 flags by quota. Keep the four default-none policies as explicit choices unless the owner changes them. Other signal groups (unknown typing, decorators, unnecessary expressions, untyped stubs and unused private definitions) need their own cost/benefit disposition; these controls prove the signal, not workspace-wide cleanliness.

### All local Pyright sites: source-copy check

Thirteen exact source copies had their Pyright directives and potentially masking Mypy ignores removed; root native policy remained unchanged. Receipt `0be4a12f0a5345dea321e7b18711179a`: 13 files, seven diagnostics:

- ICoreTool: two reportInvalidTypeVarUse messages; input expects contravariance and output covariance. Owner-approved invariance must not be changed silently.
- Fetch/pull test files: private import of the respective production git_fetch_tool/git_pull_tool._input_schema helper (one each).
- test_consumers_c4: private _assemble_labels call.
- test_project_manager: private resolver injection, already carrying its no-public-setter rationale.
- test_base: deliberately constructing abstract BaseResource; a justified exact exception can replace the bare Mypy ignore and broad module switches.

The remaining local directives produce no corresponding signal in this controlled current context, including server.py missing imports and discovery_tools.py method overrides. Global false flags can make a local false redundant; zero diagnostics is not proof that global and local policy may both be removed without a fresh run. Proposed treatment: remove obsolete module switches, narrow intentional negative/injection exceptions to their exact line, and repair private implementation assertions through public behavior.

### Mypy production directives: exact source-copy check

Six exact source copies removed all nine Mypy directive lines. Native plugin/strict policy stayed in place; `--follow-imports silent --no-incremental --show-error-codes` kept reported scope bounded. Receipt `48096919da7947429981fe0d79337642`: 13 errors across six files.

| Source | Exposed codes / meaning | Proposed treatment / trigger |
| --- | --- | --- |
| settings.py:65 | prop-decorator on computed_field/property | Retain exact library/checker exception until their supported property typing resolves it. |
| icore_tool.py:25 | Two misc variance expectations | Preserve approved invariance; reopen an intentional contract decision before removing the exception. |
| execution.py:57 | misc: covariance used in synthetic replacement parameter under the baseline | Retain only for the old baseline; the aligned Mypy 2.4/Python 3.15 reassessment below proves this exception redundant while covariance remains intact. |
| git_adapter.py:175 | assignment: Commit-inferred local later receives str | Candidate for a local explicit union annotation, preserving accepted values and runtime behavior. |
| input_validation_decorator.py:115 | arg-type: None supplied to BaseModel-bound core protocol | Genuine declared-contract mismatch with the supported no-argument path; discuss alignment instead of treating it as an SDK workaround. |
| server.py:84/96/108/125 | Seven no-untyped-call/untyped-decorator messages | Retain for SDK 1 baseline; remove along with the actual decorator API migration after typed SDK 2 handlers prove the contract. |

### Mypy tests and override

The 20 original files containing 50 Mypy directives were targeted unchanged with the native strict/plugin policy and bounded import reporting. Receipt `e555ce080dc94fdfa9e33ae5ff23af85`: **132 static errors in nine files**, not runtime test failures or a configured workspace Validation result. 117 are arg-type; other counts: unused-ignore 4, func-returns-value 2, attr-defined 3, misc 2, var-annotated 2, no-any-return 1, assignment 1. Current configured Mypy gate remains production-scoped. Extending its test scope requires an explicit policy decision; this Research does not turn all resulting diagnostics into implementation scope.

Four currently redundant Mypy directives are demonstrated:

- tests/mcp_server/unit/config/test_workflow_config_c6.py:183 and :192 (arg-type).
- tests/mcp_server/unit/managers/test_project_manager.py:943 (operator).
- tests/mcp_server/unit/config/test_workflow_config.py:21 (import-untyped).

All 50 source contexts were read and assigned to the following disjoint groups. This classification is not a claim that the as-yet unexecuted removed-suppression controls pass under candidate runtimes.

| Group | Sites | Source purpose / provisional treatment |
| --- | ---: | --- |
| Proven unused | 4 | Exact four locations above; remove annotation after a focused recheck. |
| Frozen mutation negatives | 8 | Deliberately assign to frozen dataclass/Pydantic fields while expecting a runtime rejection. Retain exact misc exceptions; reassess when immutability/type enforcement changes. |
| Invalid constructor/function call negatives | 12 | Deliberately omit required inputs or supply rejected extra keywords. Retain exact call-arg exceptions for current behavioral value; do not add historical-compatibility cases. |
| Invalid typed input negatives | 9 | Invalid literals, dictionary/None issue body; expect ValidationError. Retain exact arg-type exceptions where the runtime rejection is the behavior being tested. |
| Setup/helper type gaps | 5 | Two ready-enforcement sites use class-level descriptors where string events are expected; two test_support arguments are object-typed at stronger injected interfaces; one contracts helper expands object kwargs into a typed constructor. Align preparation with actual instance values or appropriately typed existing factories; do not call these library workarounds. |
| Mock method replacement | 4 | One conflict-engine helper replaces four methods with MagicMock. Prefer existing injection/fakes if they preserve the same conflict behavior; otherwise retain exact method-assign exceptions at that test-double boundary until it changes. |
| Bare generic dictionaries | 6 | One schema fixture and five consumers annotate plain dict. Replace with the actual typed JSON/schema mapping; then remove type-arg ignores. |
| Under-specified model parameter | 1 | model:type[object] followed by model_fields access. Narrow the test parameter to the actual BaseModel subclass contract rather than ignore attr-defined. |
| Abstract construction negative | 1 | BaseResource must reject direct construction. Replace bare ignore with the exact Mypy abstract-construction code and a justified Pyright line exception. |
| **Total** | **50** | Exact file/line membership follows the complete index and the enclosing source operations above. |

The five setup/helper gaps and under-specified model parameter are existing test typing mismatches. The native check does not by itself establish that production behavior is wrong or authorize extending the configured Mypy gate to every test. Per-group removed-suppression controls, candidate-version comparisons and final owner dispositions remain open.

Six tiny package controls exercise the **actual tests.*** override (receipt `dc44c0aecb794bf3a514b33800aeb8c2`). An untyped function is reported in application.untyped but accepted in tests.untyped. Wrong typed assignment is reported in both packages; typed positives pass. The override relaxes missing definition annotations, not all test errors. Proposed retain-as-test-policy pending an explicit wider Mypy-test-gate decision; reassess if that gate is adopted.

### AdapterRole candidate-library control

The actual unchanged declaration builds, validates, serializes and generates schema under Pydantic **2.11.7 and 2.14.1**. Both reject wrong capability model, invalid contract version, missing target, extra field and mutation of the frozen instance. A fully converted PEP695 declaration, with the obsolete global CapabilityT removed, fails in both libraries with **PydanticUserError: class not fully defined; define CapabilityT and rebuild**. Receipt `ebdc0b4fe6674fd4bab42df9faef6745`: 1 passed in 1.76s.

An initial variant accidentally retained the global TypeVar and was not a complete migration. Its apparent success is superseded by the corrected control. No rebuild workaround/compatibility layer was added. Retain the local UP046 workaround; a future supported Pydantic/checker baseline must pass this full-declaration control, not a bare generic example.

The five B017 model cases use source-extracted unchanged CreateBranchInput/CreateIssueInput declarations: missing base, missing issue, issue 0, issue -5, dictionary body. Both libraries raise ValidationError, while valid branch/issue inputs construct. Receipt `690bc161489049999aa1022dc6a291b3` includes this successful case.

### Reproduction inputs and commands

The temporary generator prepares only ignored fixtures. Run them via the existing `run_tests` tool, then direct checks via `run_checks`; no native checker subprocesses were hidden inside a test. Exact final pair sources are retained below so the evidence does not depend on the local temporary files or cache lifetime.

- Ruff targets: each `<rule>_{negative,positive}.py` under `.pgmcp/temp/issue513/diagnostic-controls/ruff/`; `checks=["python_lint"]`, `args={"python_lint":["--select","PLC0415,T201,BLE001,UP046,ANN401,ARG001,ARG002,N818,SLF001,B017","--output-format","json"]}`, `scope="targets"`, timeout 120.
- Pyright targets: each `<rule>_{negative,positive}.py` (reportIncompleteStub uses .pyi) under the sibling pyright directory. Prefix each source with `# pyright: <rule>=true`. `checks=["python_pyright"]`, `args={"python_pyright":["--outputjson"]}`, `scope="targets"`, timeout 120. No ignore directives are present.
- SDK 2 masking trio: use the four old accesses listed above in a function with Server/InitializeResult/Tool parameters, once under native policy and once with reportAttributeAccessIssue/reportCallIssue/reportArgumentType=true; positive uses Server.create_initialization_options and InitializeResult.protocol_version. Add `--pythonpath <isolated SDK 2 interpreter>`.
- Original Mypy test targets are exactly the 20 source files with Mypy comments in the complete index. Source-copy maps are the six production files and thirteen Pyright-bearing files in the same index; remove only relevant comment directives from copies, not source. Type-check with the exact options stated above.
- Mypy policy fixture packages application and tests each have __init__.py and three files: typed identity function; untyped identity function; `value: int = "wrong"`. Use native `python_types` with `--follow-imports silent --show-error-codes`.

<details>
<summary>Exact final Ruff and Pyright control sources</summary>

```json
{
  "ruff": {
    "PLC0415": {
      "negative": "def example():\n    import sys\n    return sys.version\n",
      "positive": "import sys\n\ndef example():\n    return sys.version\n"
    },
    "T201": {
      "negative": "def example():\n    print(\"sample\")\n",
      "positive": "import logging\n\ndef example():\n    logging.info(\"sample\")\n"
    },
    "BLE001": {
      "negative": "def example():\n    try:\n        return int(\"invalid\")\n    except Exception:\n        return 0\n",
      "positive": "def example():\n    try:\n        return int(\"invalid\")\n    except ValueError:\n        return 0\n"
    },
    "UP046": {
      "negative": "from typing import Generic, TypeVar\nT = TypeVar(\"T\")\nclass Box(Generic[T]):\n    value: T\n",
      "positive": "class Box[T]:\n    value: T\n"
    },
    "ANN401": {
      "negative": "from typing import Any\ndef example(value: Any) -> object:\n    return value\n",
      "positive": "def example(value: object) -> object:\n    return value\n"
    },
    "ARG001": {
      "negative": "def example(value: object) -> None:\n    return None\n",
      "positive": "def example(value: object) -> object:\n    return value\n"
    },
    "ARG002": {
      "negative": "class Example:\n    def method(self, value: object) -> None:\n        return None\n",
      "positive": "class Example:\n    def method(self, value: object) -> object:\n        return value\n"
    },
    "N818": {
      "negative": "class DomainProblem(Exception):\n    pass\n",
      "positive": "class DomainProblemError(Exception):\n    pass\n"
    },
    "SLF001": {
      "negative": "class Example:\n    _value = 1\n\ndef read(value: Example) -> int:\n    return value._value\n",
      "positive": "class Example:\n    value = 1\n\ndef read(value: Example) -> int:\n    return value.value\n"
    },
    "B017": {
      "negative": "import pytest\ndef example():\n    with pytest.raises(Exception):\n        int(\"invalid\")\n",
      "positive": "import pytest\ndef example():\n    with pytest.raises(ValueError):\n        int(\"invalid\")\n"
    }
  },
  "pyright": {
    "reportArgumentType": {
      "negative": "def accept(value: int) -> None:\n    pass\naccept(\"wrong\")\n",
      "positive": "def accept(value: int) -> None:\n    pass\naccept(1)\n"
    },
    "reportCallIssue": {
      "negative": "def accept(value: int) -> None:\n    pass\naccept()\n",
      "positive": "def accept(value: int) -> None:\n    pass\naccept(1)\n"
    },
    "reportAttributeAccessIssue": {
      "negative": "class Example:\n    value = 1\nitem = Example()\nitem.missing\n",
      "positive": "class Example:\n    value = 1\nitem = Example()\nitem.value\n"
    },
    "reportFunctionMemberAccess": {
      "negative": "def example() -> None:\n    pass\nexample.missing\n",
      "positive": "def example() -> None:\n    pass\nexample.__name__\n"
    },
    "reportMissingParameterType": {
      "negative": "def example(value) -> None:\n    pass\n",
      "positive": "def example(value: int) -> None:\n    pass\n"
    },
    "reportMissingTypeArgument": {
      "negative": "def example(value: list) -> None:\n    pass\n",
      "positive": "def example(value: list[int]) -> None:\n    pass\n"
    },
    "reportUnknownParameterType": {
      "negative": "def example(value) -> None:\n    pass\n",
      "positive": "def example(value: int) -> None:\n    pass\n"
    },
    "reportUnknownArgumentType": {
      "negative": "def accept(value: int) -> None:\n    pass\ndef example(value) -> None:\n    accept(value)\n",
      "positive": "def accept(value: int) -> None:\n    pass\ndef example(value: int) -> None:\n    accept(value)\n"
    },
    "reportUnknownLambdaType": {
      "negative": "example = lambda value: value\n",
      "positive": "from collections.abc import Callable\nexample: Callable[[int], int] = lambda value: value\n"
    },
    "reportUnknownVariableType": {
      "negative": "items = []\nresult = items[0]\n",
      "positive": "items: list[int] = [1]\nresult = items[0]\n"
    },
    "reportUnknownMemberType": {
      "negative": "def example(value) -> None:\n    value.missing()\n",
      "positive": "class Example:\n    def method(self) -> None:\n        pass\ndef example(value: Example) -> None:\n    value.method()\n"
    },
    "reportUnnecessaryCast": {
      "negative": "from typing import cast\ndef example(value: int) -> int:\n    return cast(int, value)\n",
      "positive": "from typing import cast\ndef example(value: object) -> int:\n    return cast(int, value)\n"
    },
    "reportUnnecessaryIsInstance": {
      "negative": "def example(value: int) -> bool:\n    return isinstance(value, int)\n",
      "positive": "def example(value: object) -> bool:\n    return isinstance(value, int)\n"
    },
    "reportUnnecessaryComparison": {
      "negative": "def example(value: int, other: str) -> bool:\n    return value == other\n",
      "positive": "def example(value: int, other: int) -> bool:\n    return value == other\n"
    },
    "reportAssertAlwaysTrue": {
      "negative": "assert (False, \"message\")\n",
      "positive": "def example(value: bool) -> None:\n    assert value\n"
    },
    "reportUnusedFunction": {
      "negative": "def _unused() -> None:\n    pass\n",
      "positive": "def _used() -> None:\n    pass\n_used()\n"
    },
    "reportUnusedClass": {
      "negative": "class _Unused:\n    pass\n",
      "positive": "class _Used:\n    pass\nexample = _Used()\n"
    },
    "reportUntypedFunctionDecorator": {
      "negative": "def example(decorator):\n    @decorator\n    def decorated() -> None:\n        pass\n    return decorated\n",
      "positive": "from collections.abc import Callable\ndef decorate(value: Callable[[], None]) -> Callable[[], None]:\n    return value\n@decorate\ndef example() -> None:\n    pass\n"
    },
    "reportUntypedClassDecorator": {
      "negative": "def example(decorator):\n    @decorator\n    class Decorated:\n        pass\n    return Decorated\n",
      "positive": "def decorate[T](value: type[T]) -> type[T]:\n    return value\n@decorate\nclass Example:\n    pass\n"
    },
    "reportUntypedBaseClass": {
      "negative": "def example(base):\n    class Example(base):\n        pass\n    return Example\n",
      "positive": "class Base:\n    pass\nclass Example(Base):\n    pass\n"
    },
    "reportUntypedNamedTuple": {
      "negative": "from collections import namedtuple\nExample = namedtuple(\"Example\", [\"value\"])\n",
      "positive": "from typing import NamedTuple\nclass Example(NamedTuple):\n    value: int\n"
    },
    "reportMissingSuperCall": {
      "negative": "class Base:\n    def __init__(self) -> None:\n        super().__init__()\n        self.value = 1\nclass Example(Base):\n    def __init__(self) -> None:\n        pass\n",
      "positive": "class Base:\n    def __init__(self) -> None:\n        super().__init__()\n        self.value = 1\nclass Example(Base):\n    def __init__(self) -> None:\n        super().__init__()\n"
    },
    "reportUninitializedInstanceVariable": {
      "negative": "class Example:\n    value: int\n",
      "positive": "class Example:\n    value: int\n    def __init__(self) -> None:\n        self.value = 1\n"
    },
    "reportCallInDefaultInitializer": {
      "negative": "def example(value: int = int(\"1\")) -> int:\n    return value\n",
      "positive": "def example(value: int = 1) -> int:\n    return value\n"
    },
    "reportImplicitStringConcatenation": {
      "negative": "values = [\"one\" \"two\"]\n",
      "positive": "values = [\"one\", \"two\"]\n"
    },
    "reportMissingTypeStubs": {
      "negative": "import gitdb\nexample = gitdb.__name__\n",
      "positive": "import math\nexample = math.pi\n"
    },
    "reportIncompleteStub": {
      "negative": "from typing import Any\ndef __getattr__(name: str) -> Any: ...\n",
      "positive": "value: int\n"
    }
  }
}
```

</details>

These are provisional research recommendations. Python 3.15 boundary execution is recorded below; complete per-site test/type dispositions and the owner-approved boundary strategy are still required before Research completion.

## Python 3.15 reassessment: executed boundaries

The owner approved the newest stable runtime experiment. Standard CPython 3.15.0/GIL and separate MCP 1.30/2.3 environments use Pydantic 2.14.1 below the ignored research root. The direct package set required PyYAML 6.0.3's explicit pure-Python installation variant on this Windows host; normal installation lacked a wheel and then failed without C++ Build Tools. See [Research](research.md#python-315-isolated-installation-and-actual-execution) for exact versions, commands, outcomes and scope limits.

| Suppression/contract | Additional executed evidence | Provisional disposition |
| --- | --- | --- |
| AdapterRole UP046 | Actual retained source and all five invalid/immutable controls pass under both3.15 dependency sets. Complete PEP695 conversion still fails PydanticUserError under 2.14.1. | Retain until the full source declaration, validators, schema and invalid controls pass with a supported library/checker combination. A Python upgrade alone does not remove it. |
| ToolExecution / AdapterBinding UP046 | Current Mypy 1.19.1/Pyright 1.1.408, target3.15, candidate Python/dependency path: both widening functions below accepted; both narrowing functions rejected; no masking diagnostic disable affects reportReturnType. | Retain explicit covariance as owner required. No broad generic-class conversion is justified by the higher runtime. |
| Five B017 model-validation cases | Valid branch/issue inputs construct; missing base, missing issue,0/-5 issue number and dictionary body all raise ValidationError on 3.15/Pydantic 2.14.1. | Narrow to ValidationError when remediation is approved; no reason to retain Exception merely for the candidate version. |
| SDK 1 server decorator Mypy ignores | Actual unchanged application starts healthy on 3.15/SDK 1.30; unchanged SDK 2 path fails on removed list_resources decorator. | SDK API migration owns removal of those suppressions. Raising Python does not provide the SDK 2 handler migration. |
| Ruff current version | target py315 accepts paired PLC0415 controls but emits explicit under-development warning. | Do not equate flag acceptance with fully supported 3.15 checking; do not hide it with preview. Checker upgrade is a separate decision. |
| Other native/local directives | No complete candidate runtime/source-site recheck in this increment. | Earlier evidence remains bounded to its stated context. Do not claim the whole inventory is resolved by these probes. |

Exact covariance controls use the **actual unchanged production classes**, with no local suppressions:

```python
from pydantic import BaseModel
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.core.interfaces.execution import AdapterBinding

class Result(BaseModel):
    value: int

# Positive source
def widen_execution(value: ToolExecution[Result]) -> ToolExecution[BaseModel]:
    return value

def widen_binding(value: AdapterBinding[Result]) -> AdapterBinding[BaseModel]:
    return value

# Separate negative source
def narrow_execution(value: ToolExecution[BaseModel]) -> ToolExecution[Result]:
    return value

def narrow_binding(value: AdapterBinding[BaseModel]) -> AdapterBinding[Result]:
    return value
```

Both files live temporarily under `.pgmcp/temp/issue513/diagnostic-controls/python315_variance/`. Use run_checks scope=targets with both files, checks=[python_types] and args `--python-version 3.15 --python-executable <repo>/.pgmcp/temp/issue513/sdk23-py315/Scripts/python.exe`, timeout 90: exactly two return-value errors in negative.py, zero in positive.py (supplement 00b4a05a079c42889dded64cfd8078a1). Repeat checks=[python_pyright], args `--pythonversion 3.15 --pythonpath <same interpreter> --outputjson`: exactly two reportReturnType errors in negative.py, zero in positive.py (supplement e93dcc7ceda54244ae22bc86ad7ce618).

Mypy was hosted on the native 3.13 adapter; Pyright runs in Node. The Mypy process/plugin used its host Pydantic 2.11.7; the Python-executable option selected the candidate dependency path. These are3.15 target/dependency comparisons, not proof of all language features or whole-checker execution on 3.15. The Mypy/Ruff packages separately installed/imported in the 3.15 lab. No checker pin, native policy, production declaration or permanent test changed.

## Current aligned baseline: candidate dispositions

The owner redirected Research to a coherent current Python 3.15 set. Exact dependencies, installation constraints, core-tool/adapter invocation and selected existing-test outcomes are in [Research](research.md#current-direction-align-dependencies-and-checkers-to-python-315). This supersedes using current old pins as the deciding evidence against alignment.

| Item | Aligned observed evidence | Updated proposed disposition |
| --- | --- | --- |
| AdapterBinding type:ignore[misc], execution.py:57 | Mypy 2.4 actually running on Python 3.15/Pydantic 2.14.1 reports no error in the exact source copy with the ignore removed. Targeting the real unchanged production file reports exactly unused-ignore. Existing covariance positives pass and narrowing negatives remain errors. | **Remove for the aligned baseline**; preserve explicit TypeVar covariance and the frozen dataclass. No PEP695 class conversion is required. Keep old-baseline evidence distinct. |
| ToolExecution / AdapterBinding covariance | Actual class imports in both Mypy 2.4 and Pyright 1.1.414 controls: zero positive diagnostics, two expected narrowing errors in each checker. | Retain the actual covariance contract. A newer checker removes a workaround; it does not authorize a weaker generic declaration. |
| Ruff 0.15.6's Python 3.15 target warning | Same selected PLC0415 positive/negative under Ruff 0.17.1 reports the intended diagnostic without the old instability warning or preview. | Select the aligned supported checker rather than make the old warning an argument against Python 3.15. Complete per-rule policy remains separately reviewed. |
| AdapterRole UP046 | Latest stable Pydantic is still 2.14.1. Full actual-declaration PEP695 conversion still fails class-not-fully-defined; retained behavior/schema/invalid controls pass. | Retain this specific library workaround; reassess when the actual full declaration works on a newer supported Pydantic. |
| Mypy source-copy diagnostics | With current YAML/jsonschema stubs installed, five remaining messages across four of the five non-server copies: ICoreTool variance expectations twice, property decorator limitation, Commit/string local assignment and None/BaseModel input mismatch. | Preserve intentional protocol contracts pending explicit decisions; distinguish library limitation from the two existing source declaration gaps. Do not hide or attribute all five to a version incompatibility. |
| New Mypy unused-section note | Narrow controls emit a note that tests.* override was unused in that particular invocation. | Informational consequence of the selected scope, not evidence that the test override is obsolete or a reason to disable warn_unused_configs. |
| Other directives and native flags | No blanket current-checker/source-site reassessment in this increment. | Previous provisional dispositions retain their stated context and outstanding work; no mass cleanup approval. |

Reproduction uses manifest-inventory copies of Mypy/Ruff/Pyright/Pytest with only exact prerequisite versions updated. Existing core RunChecksTool and AdapterProcessRuntime run on Python 3.15, resolving adapter Python explicitly to that interpreter. Pyright uses an isolated workspace containing the correct native Node dependency; its diagnostic policy is copied and source imports are explicitly directed to the repository. Do not bypass package-version guards or install into active node_modules.

- Mypy covariance and Ruff controls: research driver selection `python315_aligned_checks`; native arguments and control definitions match the earlier 3.15 section; supplemental 8cacb6cdc6324b47b0bc12c098dd12ae.
- Pyright final controls and Mypy five source copies: `aligned_refined_pyright`,180s; supplementalb2d29ed3436e4b0cba2eaa9a2b7a98bb. Mypy source copies use --follow-imports=silent and current types-PyYAML/types-jsonschema.
- Actual retained declaration: `aligned_retained_binding`,120s; target mcp_server/core/interfaces/execution.py, Mypy args --python-version 3.15 --python-executable <aligned interpreter> --follow-imports=silent. Exactly one unused-ignore, native exit1; supplemental 8e8ea93bdb604f0a918b5fde30ef0360.
- Existing behavior tests are **92 passed in3.11s** on actual Python 3.15/Pytest9.1.1 through the unchanged RunTestsTool/TestRunManager with candidate adapter prerequisite declarations. This is related runtime/dependency evidence, not a whole suppression-inventory verdict. Exact three-file scope is in Research.

No production annotation, native checker policy or permanent test was changed. The current aligned baseline makes at least the one local Mypy exception demonstrably removable; complete inventory disposition and owner-approved delivery strategy are still open.

## Final Disposition Proposal for Owner Decision

The owner approved the migration-before-repair sequence, target/protocol boundaries and ordinary-helper/precise-test-exception policy. This table supplies a remove, narrow or retain-with-trigger direction per equivalent group; it is not implementation evidence or QA approval. Earlier provisional recommendations are historical. Source controls, exact local index and actual-removal measurements remain the evidence.

| Group | Final research disposition | Delivery / reassessment condition |
| --- | --- | --- |
| Ruff unused directives | Remove7 policy-independent production comments. Reassess the other12 with removal of global test ANN/ARG exclusions: they become effective then. Never remove all19 blindly. | Evaluate final native policy and source together. |
| Mypy unused directives/codes | Remove4 unused whole-test ignores and the aligned AdapterBinding misc workaround, preserving covariance. SDK migration owns the3 now-unused no-untyped-call codes alongside its handler changes. | Check actual target plugin/library/source and remaining untyped-decorator codes. |
| Nine inactive Pylint comments | Remove dormant directives: no active binding consumes them. | A new Pylint binding is a separate policy. |
| B017 five assertions | Replace broad Exception with the observed Pydantic ValidationError; preserve rejection behavior without exact message assertions. | Admission model/library changes. |
| BLE001 | Retain precise terminal/cleanup/presentation error boundaries where original tracebacks/failure/cancellation survive. Remove only demonstrated redundant comments. | Wrapper/presenter/rollback/cancellation contract changes; focused existing failure-path tests. |
| T201 | Retain exact CLI outward output and proxy restart marker exceptions. | CLI presentation/restart-signaling contract changes. |
| ANN401 | Type stable known data at existing Jinja/Pydantic/audit/foreign-schema boundaries. Retain Any only where actually required, with local rationale; include the audit producer in logging repair. | Boundary schema/type authority changes; no host dependency for independent adapters. |
| ARG and Ruff test-wide ANN/ARG policy | Remove broad test exemptions in the bounded repair. Type ordinary helpers and remove unused private parameters, including ConfigValidator._validate_phase_contracts.workflow. Keep required fixture/interface parameters through exact exceptions; preserve public keyword contracts. | Actual affected test/gate under target versions; no unrelated suite rewrite. |
| Mypy tests.* override | Replace the untyped-definition relaxation with correct annotations on3 helpers: test_interface_imports.py:29, test_pipeline_decorators.py:279 and test_cli.py:99. | Keep the production-scoped configured gate; a full Mypy test gate requires a separate scope decision. |
| UP046 / variance ignores | Retain explicit covariance/intentional protocol variance and the demonstrated full AdapterRole Pydantic limitation. No generic syntax quota. | Full declaration/bounds/variance/runtime/schema controls succeed on newer supported versions, or an explicit contract decision changes. |
| Settings prop-decorator | Retain the exact computed_field/property limitation still observed with Mypy2.4. | Supported checker/plugin removes the actual source diagnosis. |
| GitAdapter assignment | Use the already-resolved HEAD hash (hexsha), preserving its snapshot. This supersedes the annotation-only suggestion; do not use a later-resolved literal HEAD. | Actual native branch behavior and typing verified in repair. |
| None-to-core | Remove with the approved model-only input contract;49 production tools already return models. Adapt direct None tests/doubles without compatibility code. | Focused admission/exposure/decorator tests on the target. |
| Literal error attributes | Preserve the narrow reason/stage type on stored attributes, matching constructor and response contracts. | Domain error/response contract changes; no cast/global disable. |
| 29 invalid/mutation test sites | Retain precise necessary codes for deliberate invalid/frozen/required-input behavior; remove unused whole ignores. | Rejection/immutability contract or test route changes. |
| 4 mock replacements / abstract negative / private assertions | Prefer existing injection/fakes and public behavior. Narrow necessary abstract/private-injection exceptions. Replace _assemble_labels/private _input_schema assertions through existing public tools. | Affected injection/interface/test changes; no new framework or legacy test. |
| Ordinary setup/bare dict/underspecified models | Repair actual helper annotations and model setup in the indexed groups, without treating them as library workarounds. | Named helpers enter repair; no requirement to fix all pre-existing test-typing diagnoses. |
| Local Pyright switches | Remove redundant module switches, narrow necessary invalid/abstract/injection exceptions and account for global masking. | Candidate checker with final global and local policy together. |
| PLC0415 | Apply the final import assessment below: preserve proven route/invocation-time behavior and otherwise prefer ordinary imports. Unknown original rationale is not proof of necessity. | Affected module/helper changes require startup/patch/fixture evidence; no mass unrelated restyling. |
| N818 GateViolation | Retain the established workflow-domain ValueError identity; correct its misleading comment. No incidental rename or alias. | Explicit gate exception contract change. |
| Pyright argument/call/attribute/decorator signals | Restore signals through migration and the bounded repair. SDK diagnoses belong to migration; Literal/input/logging/dynamic output have existing repair boundaries. | Actual migrated application/source consumers; no SDK-specific logic in managers/tools/presenters. |
| Pyright Unknown groups | Replace global blind spots using the ten boundary directions below. Existing runtime admission stays authoritative; independently establish any behavioral gap. | Boundary-specific source types and valid/invalid evidence, with exact necessary external-library exceptions. |
| Unnecessary isinstance/comparison | Preserve useful runtime guards, including immutable JSON and nullable PyGithub properties. Correct boundary types or retain exact evidence-backed exceptions when a small sound repair is unavailable. | Library annotations/runtime admission change; do not delete guards to quiet the checker. |
| Unknown lambda / unused function | Type the3 lambda diagnoses at test_git_manager.py:575. Remove _track_branch_local_artifacts at test_server.py:134: repository search finds only its definition. | Preserve existing behavior; no source-absence test. |
| 12 strict false flags with0 diagnoses | Remove false settings during repair; no immediate repair cost observed in the201-file survey. | Actual configured gate on migrated source; no guarantee for arbitrary future targets. |
| 4 native-default-none rules | Do not add missing-super/uninitialized-instance/default-initializer/implicit-string-concatenation policy. Deleting false settings leaves them off; extra195 measured findings are outside scope. | Separate explicit owner policy decision. |
| Version-only findings | Address actual candidate Ruff ISC004/UP037 and contextmanager Generator annotation findings with delivery. AnyIO's old export diagnosis needs no speculative call rewrite. | Chosen dependency/checker snapshot and actual source verification. |

No zero-suppression target, unchecked cast, lost runtime guard or broad unrelated test rewrite follows from this disposition. Installation, application and final quality evidence belong to later delivery.

## Actual Source-Removal Impact (2026-10-17)

This section supersedes generic-control-only or blanket retain/defer recommendations above. It measures suppression removal on real source copies; it does not authorize remediation or prove that every exposed diagnostic is a runtime bug.

**Scope and isolation:** 473 Python files: 191 production and 282 tests, including the root tests/conftest.py. Caches, generated assets and validation_fixtures remain excluded. The broader test scope adds exactly three PLC0415 comments at tests/conftest.py:20,21,23: **281 directive-bearing comments in 77 files**, rather than the earlier 278/76 inventory. No additional format/isort disable directives or directly relevant warning filters were found in the active source/config search. Pylint is not an active check binding; its nine historical directives do not suppress Ruff/Mypy/Pyright.

Three snapshots preserve package layout and line numbers: retained, no-local (comment directives removed with tokenize), no-all (also remove Ruff test ANN/ARG ignores and the Mypy tests.* untyped-definition override). AST equality against original source was verified for every file in every view. No production, test, dependency declaration or native workspace config was edited.

**Verified reference:** active tool interpreter Python 3.13.7, MCP 1.30.0, Pydantic 2.11.7, Mypy 1.19.1, Ruff 0.15.6, Node Pyright 1.1.408. Candidate: Python 3.15.0, MCP 2.3.0, Pydantic 2.14.1, Mypy 2.4.0, Ruff 0.17.1, Node Pyright 1.1.414, with the earlier recorded aligned dependencies/stubs. A stale repository .venv (MCP 1.26/Pydantic 2.12.5) was detected; its Mypy/Pyright measurements are superseded by the confirmed active-interpreter rerun. Relative native configuration must run from the snapshot root: preliminary Ruff measurements from the wrong CWD/config location are also superseded.

| Check / exact source scope | Reference: retained / no-local / no-all | Candidate: retained / no-local / no-all | Attribution |
| --- | --- | --- | --- |
| Ruff native selection; all 473 files | 7 / 195 / 293 | 28 / 216 / 314 | Removing local directives adds188 messages; subsequently removing test ANN/ARG exemptions adds98, identically on both stacks. Retained-view messages are separate pre-existing/version findings. |
| Mypy strict/plugin policy; explicit 473-file research targets | 1071 / 1138 / 1141 | 618 / 677 / 680 | Local removal adds71/removes4 unused-ignore messages on the reference; adds67/removes8 on the candidate. Removing the test override adds exactly3 on either. |
| Pyright; 191 production + all10 locally suppressed test files | 0 / 7 / 1294 | 1 / 8 / 869 | no-all deletes27 false settings and restores native strict defaults. Local removal adds7 on either stack; global removal then adds1287/861. |

All final captures above were complete, with no output truncation. Native diagnostic runs normally return exit1; the outer research-probe completion is not a passing quality gate. The expanded Mypy targets intentionally include tests outside the configured production gate. Of reference retained1071, all1071 are in tests; candidate retained618 includes600 test diagnostics and18 production diagnostics. These totals are not newly introduced errors, runtime test failures or a blanket repair requirement.

### Global rule impact and disposition options

| Pyright false setting(s) | Reference / candidate after actual removal | Interpretation / proposed decision |
| --- | --- | --- |
| reportArgumentType |249 /248 (production16 /15) | Real boundary mismatches coexist with test preparation/invalid-input cases. Recommend restoring this basic signal in bounded follow-up delivery; classify/fix affected boundaries rather than retain a global blind spot. |
| reportAttributeAccessIssue |416 /28 (production23 /15) | New dependency/checker types greatly change test diagnosis. Candidate still exposes removed SDK handlers and protocolVersion attributes; also dynamic LogRecord/BaseModel attributes. Source fixes or narrow dynamic boundaries need separate classification. |
| reportCallIssue |3 /11 (production0 /8) | Eight candidate production messages expose old SDK constructor spellings/missing new typed parameters. Earlier converter runtime probes accepted wire aliases, so constructor typing errors are not all independently proven runtime failures. |
| reportUnknownMemberType |153 /157 | Predominantly partially typed containers and dynamic boundaries; production114 /82. Restore only with a bounded source-typing plan, not blind casts. |
| reportUnknownArgumentType |203 /159 | Production190 /146, often values narrowed to dict[Unknown,Unknown] during JSON request validation. These counts are not proof that validation is missing. |
| reportUnknownVariableType |224 /223 | Production214 /190; correlated with the same dynamic maps. Assess once per shared boundary, not as separate runtime defects. |
| reportUnknownLambdaType |3 /3 | Three messages at test_git_manager.py:575. A typed test replacement is a concrete cleanup candidate. |
| reportUnnecessaryIsInstance / reportUnnecessaryComparison |23+4 /23+4 | Statically redundant checks can still reject invalid runtime input. E.g. ChecksConfig.match_for_filename validates str at checks_config.py:210. Do not delete runtime guards merely to satisfy this policy; decide boundary typing versus scoped exceptions. |
| reportUnusedFunction |9 /1 | Most reference messages disappear with the candidate's types. Remaining _track_branch_local_artifacts at test_server.py:134 is a test helper. No automatic dead-code conclusion without caller/registration review. |
| reportUntypedFunctionDecorator |0 /4 | Four unchanged SDK1 decorator sites on Server become invalid under SDK2. Handle with SDK migration, not a retained global suppression. |
| reportMissingTypeStubs, reportUnusedClass, reportUntypedClassDecorator, reportUntypedBaseClass, reportUntypedNamedTuple, reportUnknownParameterType, reportMissingParameterType, reportMissingTypeArgument, reportUnnecessaryCast, reportAssertAlwaysTrue, reportIncompleteStub, reportFunctionMemberAccess |0 /0 each | No source diagnostics on the measured201-file scope. Removing these false flags has no measured immediate repair cost; retain the paired negative controls as sensitivity evidence, not a promise for arbitrary future targets. |
| reportMissingSuperCall, reportUninitializedInstanceVariable, reportCallInDefaultInitializer, reportImplicitStringConcatenation |0 /0 after deletion | Native strict defaults leave these four off. Explicitly opting into all27 rules was separately measured: +125,+0,+3,+67 on either stack. That extra195 is a new policy, not the effect of removing false flags. |

Ruff's global test exemption removes **26 annotation diagnostics** and **72 unused-argument diagnostics**. The98 consist of ANN40112, ANN0017, ANN2013, ANN2022, ANN0021, ANN0031, ARG00254, ARG00116 and ARG0052. Fixtures, protocol doubles and ordinary helpers must be distinguished before choosing the future test policy.

Mypy's only test override hides three definitions: test_interface_imports.py:29, test_pipeline_decorators.py:279 and test_cli.py:99. The last is a monkeypatched copytree helper with *args/**kwargs. Adding correct test-helper annotations is the small proposed alternative to retaining the test-wide relaxation; no production contract change is implied.

### Local rules, overlaps and version findings

| Group | Actual source finding | Disposition / remaining policy |
| --- | --- | --- |
| PLC0415 |148 messages, including the3 newly indexed root-conftest imports. Eight are production imports; the others test imports. | Removal exposes placement diagnostics, not an import-cycle proof. Assess delayed CLI/recovery/error-capture composition separately from ordinary helper imports. Hoisting must preserve startup/fixture timing; it has not been executed for all sites. |
| T201 / BLE001 / UP046 / N818 / SLF001 / B017 |5 /6 /7 /1 /3 /5 after local removal on both stacks. | Existing source-specific explanations and prior behavior controls remain relevant. Preserve diagnostic/cleanup boundaries and approved variance; narrow five broad ValidationError assertions; remove private behavior assertions where public behavior proves it. No automatic API/naming rewrite. |
| ANN401 / ARG002 local |6 /7 messages with global test policy retained. | Core/dynamic schema typing and mandatory resource/interface parameters differ from an unused private helper argument. Earlier blanket per-file recommendations are not final decisions. |
| Ruff redundancy depends on global policy |Current policy reports19 unused directives. Candidate global ANN/ARG exemption removed with local comments retained: only7 RUF100 messages remain, all production sites in the earlier table. | Twelve formerly unused test comments now suppress diagnostics. Decide final global policy before deleting these12. The7 policy-independent candidates are error_handling.py:136; project_manager.py:295; discovery_tools.py:84; git_tools.py:442,446; project_tools.py:117,223. |
| Mypy local test annotations |Removal exposes frozen-object mutation, required-constructor, invalid typed-input, monkeypatch, bare dict, abstract-construction and setup issues. The exact59-comment index above remains authoritative. | Preserve deliberate invalid-input signal with precise necessary exceptions; improve ordinary preparation types. 71/67 added messages are not71/67 broken tests. |
| Mypy version-sensitive redundancy |Four whole test ignores unused on both stacks; candidate additionally makes AdapterBinding's whole ignore and3 server no-untyped-call codes unused. Those server comments still suppress untyped-decorator. | Remove/narrow only the exact redundant code. SDK handler rewrite owns the server sites. Preserve covariance. |
| Retained-view version findings |Candidate adds10 ISC004 and11 UP037 over the7 reference Ruff findings; Pyright adds reportDeprecated at template_activation.py:257 for @contextmanager -> Iterator rather than Generator. | Separate migration findings, not suppression-removal effects. Candidate SDK API typing differences likewise belong to later SDK delivery. |

Seven reference Ruff messages were already present on this expanded selection: UP043 at integration/mcp_server/conftest.py:20, integration/test_pipeline_e2e.py:85, unit/tools/test_label_tools.py:45; UP040 at unit/config/test_tool_presentation_rollout.py:39,40; I001 at integration/test_target_startup.py:20 and unit/test_build_package.py:4. These are not caused by the suppression experiment.

### Reproduction and receipts

Use code-only copies below .pgmcp/temp/issue513/aligned-node/removal-impact/{retained,no-local,no-all}; copy mcp_server/**/*.py and tests/**/*.py excluding __pycache__, assets, node_modules and validation_fixtures. Remove only true comment directives with tokenize, preserve line numbers and verify AST equality. Copy pyproject.toml to each view and set mypy_path to that view. For no-all remove only the native tests ANN/ARG ignore and tests.* disallow_untyped_defs=false override. Keep native exclusions, plugin options and selected rules.

Use the actual RunChecksTool -> CheckOperation/CheckService -> unchanged adapters/runtime, scope="targets", timeout_seconds=180, with paths relative to each execution workspace. Candidate adapter copies change exact prerequisite declarations only; retain guard enforcement.

- Ruff:473 targets, execution CWD equal to the source view; checks=["python_lint"], args=["--config","<view>/pyproject.toml","--target-version","py313|py315","--output-format","json"].
- Mypy:473 targets; checks=["python_types"], args=["--config-file","<view>/pyproject.toml","--python-version","3.13|3.15","--python-executable","<verified interpreter>","--follow-imports=silent","--cache-dir","<isolated cache>"]. Include every copied package initializer.
- Pyright:201 targets defined above; checks=["python_pyright"], args=["--project","<view>/pyright-<stack>.json","--pythonpath","<verified interpreter>","--outputjson"]. Set pythonVersion/extraPaths to the selected snapshot and interpreter. Delete all27 false report settings for the actual-removal run; setting all27 to error is a separate opt-in comparison.
- Overlap control: candidate Ruff, retained source comments, no-all native config, same473 targets/CWD, add --extend-select RUF100. Observed120 total:113 native findings plus7 RUF100, with complete capture.

Supplemental receipts: final Ruff/CWD and candidate Pyright strict removal dd19a1f1e7304cafb8ffbff7ff545ede; candidate Mypy173cc445e6644756bf283e43205e1b3d; active-interpreter confirmation7db0fd729caf48a5bac15f0ee926e3bf; confirmed reference Mypy/Pyright384c5943bc07447fa7bdfb918609e9b1; global/local Ruff overlap2f545444c0c04a86b78a2693e430e7d1. The facts/invocations above are durable evidence; cached DTOs and ignored lab files are supplemental only.

**Final disposition:** the owner-approved strategy and final group table govern later delivery. This measurement supplies removal impact; it does not execute global enablement or production changes. Migration precedes the remaining suppression repair.

## Structured Logging Robustness Follow-up (2026-10-17)

**Owner direction:** preserving current behavior through getattr alone is insufficient. Investigate malformed inputs and robust future repair; no production implementation in #513. The separate Literal-attribute fix direction is approved in [Research](research.md#approved-strategy).

Source inventory:23 logging calls with extra in9 production files;22 use props, including3 restart calls fed by _create_audit_props. One cleanup-failure call at [process_runtime.py:282](../../../mcp_server/execution/process_runtime.py#L282) supplies directory/cause directly. [StructuredFormatter](../../../mcp_server/core/logging.py) merges only props and therefore does not include those two direct fields in its JSON output. Existing [logging tests](../../../tests/mcp_server/unit/core/test_logging.py) cover valid props, names, audit setup and handler ownership, not these malformed/collision cases.

| Actual unchanged-formatter input | Python3.13.7 /3.15.0 observation |
| --- | --- |
| No props | Base JSON event produced. |
| props={"key":"value","nullable":None} | Valid object, including JSON null. A null field value differs from props itself being None. |
| props=None | TypeError before formatting completes. |
| props="invalid" | ValueError during dict.update. |
| props=[["key","value"]] | Accepted as iterable pairs, despite not being a mapping. |
| props={513:"value"} | Accepted; json.dumps silently turns the key into "513". |
| props={"path":Path("probe")} | TypeError during JSON serialization. |
| props={"message":"replacement","level":"ERROR"} | Replaces the original message and INFO severity in the output. |
| extra={"directory":"probe-dir","cause":"probe-error"} without props | Both supplied fields absent from structured output. |

A separate control shows stdlib Logger.makeRecord rejects extra={"message":...} with KeyError, but nesting it inside props bypasses that protection and our flat merge overwrites the message. This is a boundary-consistency problem, not a new-version fix.

Source review also identifies an existing collision: [admin_tools.py:47](../../../mcp_server/tools/admin_tools.py#L47) intentionally includes timestamp in _create_audit_props, which replaces the formatter timestamp on3 restart events. The property is present in live source; no claim is made that it is an accidental defect. Future metadata-ownership policy must reconcile it explicitly.

### Static coverage and proposed boundary

Exact paired sources under the ignored lab controls/logging directory:

- direct.py: get_logger returns stdlib logging.Logger; logger.info receives one valid extra, extra={"props":None}, and extra={"props":{"path":object()}}.
- typed.py: a research-only StructuredExtra TypedDict has props:Mapping[str,JsonValue]; structured_extra(props:Mapping[str,JsonValue]) returns it. Call with a valid mapping including a nullable field, then None, then an object-valued mapping.
- Both files explicitly enable reportArgumentType, reportCallIssue and reportAttributeAccessIssue. No suppressions. This prototype demonstrates typing; its passthrough body is not proposed as sufficient runtime validation.

Native Pyright1.1.408 and1.1.414 each report **exactly2 reportArgumentType diagnostics**, both typed.py:15,16; direct.py has zero. Merely removing global disables therefore does not protect the generic stdlib extra payload. The candidate requires the same explicit local contract as the reference.

Future repair should establish a typed producer contract and runtime admission using the existing logging boundary, migrate the identified callers consistently, preserve primary event/exception facts, and adapt the existing behavior tests. A typed builder is a minimal candidate, not final architecture: it helps routed calls but cannot itself prevent raw Logger.extra bypasses. A plain getattr replacement or blanket Any/default=str conversion does not meet the owner's robustness goal.

**Owner-approved future failure policy:** retain the original base event/message/severity and traceback, and explicitly expose malformed logging data through a payload diagnosis. Silent discard and replacement of the original error are unacceptable. Metadata ownership remains open: tightening reserved output fields affects the existing restart timestamp producer. The owner has not approved that timestamp change.

### Durable reproduction and outcomes

Use logging.Logger.makeRecord with message="original", severity INFO and the exact extra inputs in the table, then the real StructuredFormatter.format and json.loads. Keep each logger unregistered and attach no active handlers/files. Run identical scripts using the verified active Python3.13.7 and isolated aligned3.15.0 interpreters. Capture exception type separately from successful JSON fields; the mutation/drop observations are the asserted behavior, not a passing new implementation.

Runtime invocation: run_tests(scope="targets", targets=[".pgmcp/temp/issue513/test_issue513_research.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s","--tb=short","-k","logging_props_runtime_and_prepare"]}, timeout_seconds=90). **1 passed,50 deselected,2.28s**, covering9 cases on each interpreter. Supplemental fae5a83408b448c9a2ffb57b5830290e.

Static reference: run_checks(scope="targets", targets=[".pgmcp/temp/issue513/aligned-node/controls/logging/direct.py",".pgmcp/temp/issue513/aligned-node/controls/logging/typed.py"], checks=["python_pyright"], args={"python_pyright":["--outputjson"]}, timeout_seconds=60). **2 expected diagnostics, native exit1,2 files analyzed,0 warnings**; complete capture. Supplemental a5cc864ef1314a89b31e7b6168caa81b.

Candidate: same2 sources through the existing RunChecksTool/CheckOperation/runtime and aligned Pyright adapter, args --pythonversion3.15 --pythonpath<aligned interpreter> --outputjson; outer run_tests with -k candidate_logging_static_contracts_and_reserved, timeout120. The stdlib reserved-message control and candidate measurement complete; **2 expected native diagnostics,0 warnings**, complete capture. Supplemental094c9c69facc47889b12902e72f863b2. Production, permanent tests and active native config remain unchanged.


## Remaining Pyright Production Findings (2026-10-17)

This increment preserves production/configuration/permanent tests. It tests source variants, real public boundary behavior and installed dependency contracts. Proposed fixes below are not owner approvals; the approved logging failure policy is recorded above and in Research.

### Small source-typing variants

Seven temporary files under aligned-node/controls/remaining: retained/fixed bootstrap.py, content_input.py and git_base.py, plus anyio_api.py. Each explicitly enables reportArgumentType, reportCallIssue and reportAttributeAccessIssue; other native settings remain intact.

| Variant | Source and exact change | Reference / candidate diagnostics |
| --- | --- | --- |
| Generic bindings | Extract the actual _resolve_generic_output_models function body with its real imports. At original bootstrap.py:279 add child_bindings:dict[object,object] to the existing dict(zip(...)) assignment. | Retained1 /1; fixed0 /0. The diagnosis concerns child_bindings, not the initial visit(tool_type,{}) call. |
| Pydantic schema callback | Copy actual content_input.py; change _closed_alternatives(schema:dict[str,object]) to dict[str,JsonValue] and import the existing Pydantic JSON type. | Retained2 /2 at the union callbacks; fixed0 /0. |
| Git HEAD input | Focused function with real Repo annotation and repo.create_head(name,repo.head.commit), versus the same call using repo.head.commit.hexsha. | Retained1 /1; fixed0 /0. |
| AnyIO worker | import anyio; await anyio.to_thread.run_sync(lambda:513). | Old stack1 reportAttributeAccessIssue referring to type[BrokenWorkerInterpreter]; aligned stack0. |

Total: reference5 expected diagnoses, candidate4; all fixed sources0,0 warnings. These native failed results deliberately contain retained negative controls. They are not a passing production gate or proof of a completed Git behavior change.

Preliminary full bootstrap copies introduced an additional nominal-class mismatch because their locally defined SupportedToolContract differed from the imported original class. Those copy-artifact messages are excluded. The corrected comparison extracts the actual affected function body; no production suppressions are added.

The GitPython3.2.1 [public create_head contract](https://gitpython.readthedocs.io/en/stable/reference.html#git.repo.base.Repo.create_head) declares SymbolicReference|str. Installed git/refs/symbolic.py _create resolves str(reference); Commit stringification represents its hash. Prefer the already-resolved hexsha over passing the literal HEAD, which would defer resolution. No branch/ref mutation was executed for this research comparison; future verification must preserve the concrete selected base and failure behavior.

The installed AnyIO4.12.1 __init__ does not explicitly export to_thread and defines __getattr__ returning type[BrokenWorkerInterpreter] for an unrelated deprecated alias. AnyIO4.15.1 explicitly re-exports to_thread. Runtime call returns513 under both versions. This bounds the observed difference to the measured coherent stacks; no claim is made that changing the checker alone fixes the old library exports.

### Behavior checks protect runtime contracts

On Python3.13.7/current dependencies and3.15.0/aligned dependencies:

- FrozenJsonObject((("key","value"),)) admits the immutable value. List entries reject with TypeError; an integer key rejects with ValueError. These are real guard behaviors despite annotations describing valid inputs.
- resolve_json_schema expands #/$defs/Tuple/prefixItems/0; the resulting schema accepts {"first":"valid"} and rejects {"first":513}. Index9 rejects with unresolved_schema_pointer. Call only the public resolver, not its private pointer helper.
- Both retained and fixed content_input modules admit valid ScaffoldContentRequest data, reject a request supplying overlapping text/file fields, and emit oneOf rather than anyOf. This preserves the meaningful behavior of the callback annotation correction.
- anyio.run(anyio.to_thread.run_sync,lambda:513) succeeds on both installed library versions.

Invocation: run_tests(scope="targets",targets=[".pgmcp/temp/issue513/test_issue513_research.py"],tests=["python_tests"],args={"python_tests":["-n","0","-s","--tb=short","-k","prepare_remaining_pyright_sources"]},timeout_seconds=90). Final supplemental43bf9b8f53854f5f856b43ae4ccd902e.

Native reference: run_checks scope=targets, the exact7 files above, checks=[python_pyright], args=["--outputjson"], timeout90. Expected5 errors; supplemental e15a93140ddb4ee09883f9b637d0276f. Candidate: same7 relative paths through unchanged RunChecksTool/adapters/runtime and candidate prerequisites, args --pythonversion3.15 --pythonpath<aligned interpreter> --outputjson; outer -k remaining_candidate_pyright_source_variants,timeout120. Expected4; supplemental90e08994315d48d7ad0741f2de855c10. Complete captures.

### Library nullability versus an unnecessary-comparison recommendation

The public Github.create_from_raw_data(Issue,{"milestone":None,"body":None,"closed_at":None}) constructs complete objects without HTTP. Block Requester.requestJsonAndCheck to ensure no lazy request. In both PyGithub2.8.1/Python3.13.7 and2.10.0/Python3.15.0, all3 properties return None. Their declared return annotations remain Milestone,str,datetime.

A minimal public Issue consumer guarded by if issue.milestone is not None produces exactly1 reportUnnecessaryComparison under Pyright1.1.408 and1.1.414 when that rule is enabled. Removing this guard solely because of the diagnosis would allow an actual None value to reach .number. Preserve the production guards in github_manager.py:175,185,192; assess the additional PR-reference guard separately. Prefer a sound nullable description at the existing library boundary, or a precise documented exception if a small correct typing repair is unavailable. No new generic Github abstraction or blanket global suppression follows from this finding.

Runtime invocation: same research driver/tool, -k nullable_pygithub_properties,timeout90;1passed,54deselected,3.39s. Supplemental4354d24fc07d4e19b53b1f2daeeb381a. Native reference: one controls/remaining/nullable_github.py target, reportUnnecessaryComparison=true, checks=[python_pyright],args=[--outputjson],timeout60;1 expected error,03a2b0756a7842b894ac85182c7e0070. Candidate same source through aligned core-tool composer, outer -k nullable_pygithub_candidate_checker,timeout120;1expected error,f5e3bb0f0158475481d4dc3349a22f6e. No network or production mutation.

### Unknown-type population and adapter isolation

The already measured candidate removal DTO contains418 production Unknown* messages at296 distinct file/line positions: reportUnknownMemberType82, reportUnknownArgumentType146, reportUnknownVariableType190. Of these202 are in eight bundled adapter source files. Multiple diagnoses can describe the same dynamic container; this is not418 independent missing validations.

A focused existing public Ruff protocol behavior test, test_request_rejections_preserve_root_and_index_details, was executed unchanged. It covers malformed JSON, a list root, a non-string operation and an integer target; each returns protocol exit2 and invalid_request with the exact root/field/index. Invocation run_tests(scope="targets",targets=["tests/mcp_server/integration/adapters/test_ruff_checks.py"],tests=["python_tests"],args={"python_tests":["-n","0","--tb=short","-k","request_rejections_preserve_root_and_index_details"]},timeout_seconds=90). Passed; supplementalc471d19db221449db7483645fc880cb0.

Future typing must reflect existing validations and address any independently demonstrated validation gaps. Independent adapters remain stdlib-only and self-contained: importing host Pydantic/pgmcp models or adding knowledge to generic execution code merely to quiet diagnostics crosses the wrong boundary. Broad casts to a presumed valid mapping are not an acceptable replacement for validation. The final classification below accounts for the entire production Unknown population; this representative runtime test does not prove every boundary is complete.


### Final Unknown boundary classification

Read-only source review grouped all418 candidate production Unknown messages at296 positions in53 files. Counts are a disjoint partition of the complete candidate actual-removal capture; field-factory positions are classified before module-based groups. Multiple diagnostic kinds can describe one position. No new checker/test execution was needed.

| Existing boundary / messages / positions | Source observation | Repair direction and constraint |
| --- | --- | --- |
| Independent adapter JSON —202 /138 | All8 bundled files explicitly check request/root/field/item types. Some also parse native reports/prerequisites/options; e.g. [Ruff](../../../mcp_server/bundled_adapters/ruff/check.py#L66), [check-jsonschema](../../../mcp_server/bundled_adapters/check_jsonschema/check.py#L84), [Lychee](../../../mcp_server/bundled_adapters/lychee/check.py#L153). | Describe decoded values as object and narrow at existing boundaries. Preserve field/index diagnoses and version guards. Keep adapters stdlib-only/self-contained; no host models, generic tool-specific knowledge or assumed missing validation. |
| Config/model input —72 /44 | [composition](../../../mcp_server/config/composition.py#L55), [loader root](../../../mcp_server/config/loader.py#L277), schema before-validators and check/fix/test input normalizers handle raw containers before final Pydantic validation. | Type raw members honestly without asserting the final model early. Preserve deletion/list/order/admission semantics. No extra generic validation layer or changed runtime consumer API just for diagnostics. |
| Presentation/cache —53 /40 | [TextPresenter](../../../mcp_server/presenters/text_presenter.py#L210) reads dynamic fields; [collection rendering](../../../mcp_server/presenters/collection_text_renderer.py#L214) validates list/model/mapping items; [cache serialization](../../../mcp_server/utils/cache_serialization.py#L18) traverses DTOs and preserves diagnostic facts after failure. | Use existing DTO/config types and runtime narrowing at dynamic reads. Preserve null distinctions, template selection, item diagnoses and primary error/traceback. getattr alone is insufficient before using a field as a key/collection; establish any runtime gap separately, without silent coercion. |
| Stored JSON/context —31 /20 | [phase resolver](../../../mcp_server/managers/phase_contract_resolver.py#L166) selects plan blocks before CheckSpec validation; [project reads](../../../mcp_server/managers/project_manager.py#L531), state-version reads, gate paths and enforcement parameters expose decoded dictionaries. | Narrow/validate at existing file/plan boundaries and carry typed values through read-only interfaces. Preserve query purity and corrupt/version diagnoses; no empty-success fallback or new state framework. |
| Local collection inference —18 /17 | GitAdapter branch args, catalog inventory lists, artifact/template closure sets and Git/issue/project result lists start from partially inferred empty containers. | Specify existing element types at construction. Preserve values/order/consumers; no new DTO or runtime validation merely to supply an annotation. |
| Typed field factories —18 /18 | Complete field annotations exist but bare list/dict/set factories expose partially unknown constructor signatures across contracts, dataclasses and output models. | Use the smallest checker-supported precise factory typing. Preserve fresh-per-instance mutable defaults and public default/constructor semantics; no shared objects or blanket ignore. |
| SDK/server —12 /10 | Removed SDK1 decorators, proxy attributes and server exposure drive this group. ITool does not declare the dynamic output_model used by the server. | Migrate SDK API first. Resolve metadata typing at the existing bootstrap/tool contract owner; no duplicated schemas or SDK knowledge in tools/managers. Verify actual handler/list/resource/error behavior. |
| Core/schema/decorators —9 /7 | Generic ToolExecution wrappers, optional core admission, foreign jsonschema errors and dynamic schema error attributes feed partly inferred values. | Preserve variance/typed transport; apply model-only input. Type foreign errors at existing validator boundaries and select the declared dict/schema representation explicitly. No unchecked casts or replacement decorator pipeline. |
| Logging —2 /1 | [formatter](../../../mcp_server/core/logging.py#L23) consumes dynamic LogRecord.props. Malformed values/collisions have paired runtime evidence above. | Execute approved typed-producer/runtime-payload repair with explicit malformed-data diagnosis and preserved primary event/traceback. Metadata ownership is a scoped design question. |
| External YAML typing —1 /1 | [YamlDumper](../../../mcp_server/services/yaml_serialization.py#L21) delegates to SafeDumper.represent_scalar, whose native/stub signature is partially unknown. | Correct/contain that external signature at the existing emission boundary; a precise justified exception is a last resort. Preserve native escaping/chomping; do not reimplement YAML or stringify invalid objects. |

Reproduction: use the committed candidate no-all invocation above, parse generalDiagnostics, select rule prefixes reportUnknown and production paths, and map original one-based lines to their enclosing AST function/class. Classify default_factory source lines first; remaining paths group by bundled adapters, config/input normalizers, presenters/cache, stored plan/state/context, server/proxy, core/schema/decorators, logging, YAML emission and remaining local collections. Counts total418 messages and296 positions. The ignored raw capture is supplemental; source boundaries/counts/constraints and examples above are durable. The full file inventory is reproducible from source using that native invocation.

### Final import placement assessment

The actual removal survey has148 PLC0415 signals:8 production and140 test imports. Earlier145/137 totals omitted3 root-conftest imports and are historical.

| Source group | Source-backed observation | Later repair and verification |
| --- | --- | --- |
| cli.py:68,98 — renewal routing | Selects renewal CLI/operation only after --upgrade or --init routing. No eager cli_renewal route was found in the statically inspected internal import graph. | Retain precise route-specific delay with this rationale; reassess if the CLI/composition boundary changes. No performance claim. |
| cli.py:129 — server | bootstrap.py already imports server at module scope: cli -> bootstrap -> server. Local placement does not isolate server loading. | Move ordinary import/remove directive, with normal/degraded CLI verification. No new lazy-bootstrap refactor. |
| server.py:266,270,271 — recovery | Imports output models/health/restart classes; construction stays inside recovery. No static dependency path back to server was found, and no concrete cycle necessity was established. | Prefer hoisting declarations while keeping construction/config admission in recovery. Verify startup/degraded behavior before delivery; static graph is not proof of absent import side effects. |
| core/error_handling.py:39 | Comment requests avoiding eager schemas; inspected imports find no path from schemas.error_outputs back to error_handling. Stronger necessity is unproven. | Prefer ordinary import, verified by focused import/capture/CLI error behavior. Any demonstrated dependency constraint must get an exact local rationale. |
| tools/phase_tools.py:138 | schema_utils is a pure resolver; no static path back to phase_tools was found. | Move import while keeping schema construction on demand; verify public input_schema/phase enum behavior. |
| tests/conftest.py:20,21,23 | os/Path are ordinary dependencies. Settings construction happens inside pytest_sessionstart. | Move imports, preserve construction/env setup inside hook, verify collection/session behavior. |
| test_support.py:75 — Settings lookup | get_default_server_root imports Settings on invocation; the module separately holds RealSettings. Tests patch mcp_server.config.settings.Settings, so hoisting that class binding can change what a helper invoked inside the patch sees. | Preserve invocation-time attribute lookup or an existing injected seam. Do not substitute eagerly bound RealSettings or move a class binding across patch boundaries blindly. Mock at:73 has no equivalent timing need. |
| Other test imports | The AST index is mostly ordinary input/output models, mocks and helper factories; original rationale is unknown unless recorded. The aligned AnyIO explicitly exports the submodule previously loaded in tests. | Default to ordinary imports when repairing the file; preserve actual patch/fixture lookup semantics with focused existing tests. Only demonstrated timing needs justify local exceptions. No unrelated suite-wide restyling or source-content tests. |

The source graph followed module-executed absolute internal imports and package initializers, excluding function bodies and TYPE_CHECKING branches. It found no paths for the proposed cycle explanations above; it does not certify relative/dynamic/external imports or execute hoisting. Any later import edit needs targeted behavior evidence. A read-only repository search for _track_branch_local_artifacts finds only its test_server.py:134 definition, with no string registration/reference; removal is a local dead-helper direction.

## Related Documents

- [Final #507 findings](<../issue507/research.md>)
- [Research scope](<https://github.com/MikeyVK/phase-gate-mcp/issues/513>)
- [Typing resolution contract](<../../coding_standards/TYPE_CHECKING_PLAYBOOK.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-17 | @imp researcher | Record token-aware exact locations, native policy and observed unused exceptions without approving removals or retained policy. |
| 0.2 | 2026-10-17 | @imp researcher | Add all-rule paired controls, masking proof, source-copy checks, native test-policy comparison, candidate Pydantic evidence and provisional dispositions. |
| 0.3 | 2026-10-17 | @imp researcher | Record actual 3.15/Pydantic 2.14 controls, retained covariance signal, unchanged AdapterRole limitation and checker-support evidence without broadening remediation. |
| 0.4 | 2026-10-17 | @imp researcher | Reassess against current aligned 3.15/checker set; prove redundant AdapterBinding ignore with preserved variance and distinguish remaining source/library diagnoses. |
| 0.5 | 2026-10-17 | @imp researcher | Consolidate proposed dispositions for every indexed group with scope/trigger, repeat all candidate group controls, and correct private-helper ownership. |
| 0.6 | 2026-10-17 | @imp researcher | Correct research scope/status: global and local actual-source removal impact remains in #513; diagnostic controls and retained-annotation surveys do not complete it. |
| 0.7 | 2026-10-17 | @imp researcher | Measure all active local/global source-removal surfaces on verified reference and aligned stacks; add root-conftest omissions, policy overlap, native-default distinctions, source examples and explicit limits. |
| 0.8 | 2026-10-17 | @imp researcher | Record actual logging malformed-input/collision behavior,23-call impact inventory and paired checker limitations; leave invalid-payload/metadata policies open. |
| 0.9 | 2026-10-17 | @imp researcher | Record approved logging failure policy and next Pyright source/library controls; prove nullable-library and immutable-guard cases without removing runtime checks. |
| 0.10 | 2026-10-17 | @imp researcher | Consolidate approved migration/test policy and final dispositions; classify all418 production Unknown diagnostics and complete source-based import/reference review with delivery evidence limits. |
