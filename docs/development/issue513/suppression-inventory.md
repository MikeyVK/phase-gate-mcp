<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 513 — Checker Suppression Inventory

**Status:** Complete baseline and executed group controls — final dispositions open  
**Version:** 0.3  
**Last Updated:** 2026-10-17

## Purpose

Keep one complete location index for substantive reassessment; an entry is not automatically a defect or an approved permanent exception.

## Scope In

Actual native selections/ignores/overrides, true local directives and directly relevant warning policy for the active production/test surface.

## Scope Out

No automatic expansion into caches, generated assets, archive documentation, every unselected Ruff rule or intentionally inapplicable native scanning.

## Summary

Scanned **472 active production/test Python files**, with zero tokenize/AST errors. Found **278 comment lines in 76 files**: 201 Ruff, 59 Mypy, 13 Pyright and 9 Pylint directives; four lines belong to multiple families. String-literal fixture text was excluded using Python tokenize. Generated assets/caches were excluded; any native-excluded source fixture is explicitly tagged by the collector. The configured native policy is recorded separately.

Baseline: Python 3.13.7, MCP 1.30.0, Pydantic 2.11.7, Ruff 0.15.6, Mypy 1.19.1 and Pyright 1.1.408. The isolated SDK probe uses MCP 2.3.0/Pydantic 2.14.1, not a modified baseline environment. No final per-group disposition is claimed yet.

## Native Policy

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
- Fetch/pull test files: private import of test_support._input_schema (one each).
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
| execution.py:57 | misc: covariance used in synthetic replacement parameter | Retain exact exception with explicit covariance; recheck at Mypy/Python baseline change. |
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

Mypy was hosted on the native 3.13 adapter; Pyright runs in Node. The Mypy process/plugin used its host Pydantic 2.11.7; the Python-executable option selected the candidate dependency path. These are3.15 target/dependency comparisons, not proof of all language features or whole-checker execution on 3.15. The Mypy/Ruff packages separately installed/imported in the3.15 lab. No checker pin, native policy, production declaration or permanent test changed.

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
