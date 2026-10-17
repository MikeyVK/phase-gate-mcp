<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 513 — Checker Suppression Inventory

**Status:** Complete baseline inventory — dispositions in progress  
**Version:** 0.1  
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

## Related Documents

- [Final #507 findings](<../issue507/research.md>)
- [Research scope](<https://github.com/MikeyVK/phase-gate-mcp/issues/513>)
- [Typing resolution contract](<../../coding_standards/TYPE_CHECKING_PLAYBOOK.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-17 | @imp researcher | Record token-aware exact locations, native policy and observed unused exceptions without approving removals or retained policy. |
