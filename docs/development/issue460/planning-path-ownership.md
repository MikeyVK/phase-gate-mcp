# Issue 460 Planning — Exact Path Ownership

Status: DRAFT. Baseline: ea48558c. [Planning](planning.md) owns sequencing; [frozen catalog](template-suite-catalog.md) owns the original census; [integration §3.2](design-integration-review.md#32-exact-testhelper-dispositions) owns each test's durable claim, architecture disposition and removal prerequisite.

## Index contract

C001–C126 exclude the two governing standards; T001–T151 and A001–A079 follow the frozen catalog order. S rows enumerate 57 independently discovered dependencies. Each row has one accountable owner and all ordered write/review episodes. Empty write-set means preservation review only; a review never authorizes edits. CY identifiers are cycles. The cycle's D1 limits the permitted slice; sharing a file never permits unrelated cleanup.

New exact paths have a creation owner and every planned revisit below. Generated build/candidate/temp outputs are derived test/operational artifacts, not manually maintained source truth. Any unexpected caller or new source path requires a bounded amendment before editing. A deleted source referenced by a later review means closure evidence, never recreation. Existing tests must migrate their last imports at the first production removal, even if later residual cleanup is separately assigned.

## c source register

126 consumers.

| ID | Exact path | Primary owner | Ordered write episodes | Ordered review episodes | Bounded disposition |
|---|---|---|---|---|---|
| C001 | `docs/coding_standards/CODE_STYLE.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C002 | `docs/coding_standards/README.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C003 | `.pgmcp/config/contracts.yaml` | [CY088](planning-rollout.md#cy088) | CY072, CY088 | CY068 | Migrate only workflow execution wording/schema-discovery/carriers; CY072 owns the earlier name/allowlist activation and CY088 auto-state registration. |
| C004 | `.pgmcp/config/artifacts.yaml` | [CY072](planning-rollout.md#cy072) | CY052, CY072 | CY070 | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C005 | `.pgmcp/config/quality.yaml` | [CY072](planning-rollout.md#cy072) | CY072 | CY070, CY086 | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C006 | `pyproject.toml` | [CY072](planning-rollout.md#cy072) | CY020, CY021, CY027, CY062, CY072, CY086 | CY022, CY070 | CY020/CY021/CY027 own only their named native Ruff/Mypy/Pytest settings; CY062 owns packaging. CY022 is read-only for this file. CY070 prepares the exact [tool.pyright]-only deletion hunk from proved values; CY072 alone applies it after CY071 rehearsal. CY086 may remove only other obsolete quality wiring, never re-own the Pyright deletion. |
| C007 | `.pgmcp/config/scaffold_metadata.yaml` | [CY078](planning-rollout.md#cy078) | CY078 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C008 | `.agents/AGENTS.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. Include the general cache-window discovery procedure prepared in CY069, rehearsed in CY071 and installed only in CY072. |
| C009 | `.agents/reboot.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C010 | `.agents/rules/research.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C011 | `.agents/workflows/create-issue.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C012 | `.github/agents/co.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C013 | `.github/agents/qa.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C014 | `docs/agents/vscode/copilot/.github/agents/qa.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C015 | `docs/agents/vscode/copilot/.github/agents/co.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C016 | `.github/prompts/create-issue.prompt.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C017 | `AGENTS.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. Include the general cache-window discovery procedure prepared in CY069, rehearsed in CY071 and installed only in CY072. |
| C018 | `README.md` | [CY091](planning-rollout.md#cy091) | CY091 | None | Align install/setup/root/native prerequisite/migration guidance; no external rollout. |
| C019 | `docs/agents/antigravity/AGENTS.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. Include the general cache-window discovery procedure prepared in CY069, rehearsed in CY071 and installed only in CY072. |
| C020 | `docs/agents/antigravity/workflows/create-issue.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C021 | `docs/agents/codex/AGENTS.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. Include the general cache-window discovery procedure prepared in CY069, rehearsed in CY071 and installed only in CY072. |
| C022 | `docs/agents/codex/reboot.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C023 | `docs/agents/codex/rules/research.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C024 | `docs/agents/codex/workflows/create-issue.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C025 | `docs/agents/vscode/copilot/AGENTS.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. Include the general cache-window discovery procedure prepared in CY069, rehearsed in CY071 and installed only in CY072. |
| C026 | `docs/manuals/architectural_diagrams/01_module_decomposition.md` | [CY092](planning-rollout.md#cy092) | CY092 | None | Update only the named architecture diagram; reconcile exact owner/dependency facts. |
| C027 | `docs/manuals/architectural_diagrams/03_tool_layer.md` | [CY092](planning-rollout.md#cy092) | CY092 | None | Update only the named architecture diagram; reconcile exact owner/dependency facts. |
| C028 | `docs/manuals/architectural_diagrams/05_config_layer.md` | [CY092](planning-rollout.md#cy092) | CY092 | None | Update only the named architecture diagram; reconcile exact owner/dependency facts. |
| C029 | `docs/manuals/architectural_diagrams/08_naming_landscape.md` | [CY092](planning-rollout.md#cy092) | CY092 | None | Update only the named architecture diagram; reconcile exact owner/dependency facts. |
| C030 | `docs/manuals/architectural_diagrams/09_scaffolding_subsystem.md` | [CY092](planning-rollout.md#cy092) | CY092 | None | Update only the named architecture diagram; reconcile exact owner/dependency facts. |
| C031 | `docs/manuals/architectural_diagrams/10_config_consumers.md` | [CY092](planning-rollout.md#cy092) | CY092 | None | Update only the named architecture diagram; reconcile exact owner/dependency facts. |
| C032 | `docs/manuals/architecture.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C033 | `docs/manuals/phase-workflows.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C034 | `docs/development/schema-template-maintenance.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C035 | `docs/reference/TEMPLATE_LIBRARY_PATTERNS.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C036 | `docs/manuals/README.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C037 | `docs/reference/config-loading-architecture.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C038 | `docs/reference/MCP_TOOLS.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C039 | `docs/reference/mcp_vision_reference.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C040 | `docs/reference/migration_v2.0.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C041 | `docs/reference/presentation_architecture.md` | [CY090](planning-rollout.md#cy090) | CY010, CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. Cache/attachment architecture-reference correction lands with cache fidelity, remaining role presentation wording in CY090. |
| C042 | `docs/reference/README.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C043 | `docs/reference/TEMPLATE_LIBRARY_QUICK_REFERENCE.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C044 | `docs/reference/TEMPLATE_LIBRARY_USAGE.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C045 | `docs/reference/template_metadata_format.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C046 | `docs/reference/tools/editing.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C047 | `docs/reference/tools/discovery.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C048 | `docs/reference/tools/quality.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |
| C049 | `docs/reference/tools/github.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |
| C050 | `docs/reference/tools/project.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |
| C051 | `docs/reference/tools/README.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C052 | `docs/reference/tools/scaffolding.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C053 | `docs/reference/validation_api.md` | [CY089](planning-rollout.md#cy089) | CY089 | None | Selected DI-07 reference disposition and inbound-link migration; remove only designated obsolete authorities. |
| C054 | `docs/setup/workspace-upgrade.md` | [CY091](planning-rollout.md#cy091) | CY091 | None | Align install/setup/root/native prerequisite/migration guidance; no external rollout. |
| C055 | `mcp_server/bootstrap.py` | [CY072](planning-rollout.md#cy072) | CY009, CY071, CY072, CY074, CY077, CY078, CY079, CY081, CY082, CY083, CY086, CY087, CY088 | CY012, CY052, CY064 | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C056 | `mcp_server/cli.py` | [CY076](planning-rollout.md#cy076) | CY072, CY076 | CY067 | CLI/renewal slice, no unrelated commands; CY064 compatibility-state reader, CY072 active entry routing. |
| C057 | `mcp_server/config/loader.py` | [CY087](planning-rollout.md#cy087) | CY003, CY005, CY012, CY016, CY028, CY030, CY052, CY064, CY071, CY077, CY078, CY079, CY081, CY082, CY086, CY087 | None | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C058 | `mcp_server/config/validator.py` | [CY087](planning-rollout.md#cy087) | CY003, CY005, CY012, CY016, CY028, CY030, CY052, CY071, CY077, CY078, CY079, CY081, CY082, CY086, CY087 | None | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C059 | `mcp_server/config/schemas/scaffold_metadata_config.py` | [CY078](planning-rollout.md#cy078) | CY078 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C060 | `mcp_server/config/schemas/__init__.py` | [CY087](planning-rollout.md#cy087) | CY002, CY005, CY012, CY016, CY028, CY030, CY052, CY064, CY071, CY077, CY078, CY081, CY082, CY086, CY087 | None | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C061 | `mcp_server/config/schemas/artifact_registry_config.py` | [CY077](planning-rollout.md#cy077) | CY077 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C062 | `mcp_server/config/schemas/quality_config.py` | [CY087](planning-rollout.md#cy087) | CY087 | None | Retire generic quality/parser/old public runtime after CY072; retained check/fix facts owned by native role cycles. |
| C063 | `mcp_server/config/settings.py` | [CY072](planning-rollout.md#cy072) | CY072 | CY001, CY012, CY052, CY064, CY067, CY070, CY071 | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C064 | `mcp_server/managers/artifact_manager.py` | [CY074](planning-rollout.md#cy074) | CY074 | CY053, CY071, CY077, CY078, CY079, CY081, CY082 | Retire only in CY074 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C065 | `mcp_server/managers/qa_manager.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Retire generic quality/parser/old public runtime after CY072; retained check/fix facts owned by native role cycles. |
| C066 | `mcp_server/scaffolders/template_scaffolder.py` | [CY075](planning-rollout.md#cy075) | CY075 | CY053, CY071, CY077, CY078, CY079, CY080 | Retire only in CY075 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C067 | `mcp_server/scaffolding/template_introspector.py` | [CY079](planning-rollout.md#cy079) | CY079 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C068 | `mcp_server/scaffolding/base.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C069 | `mcp_server/scaffolding/components/doc.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C070 | `mcp_server/scaffolding/components/dto.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C071 | `mcp_server/scaffolding/components/generic.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C072 | `mcp_server/scaffolding/components/schema.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C073 | `mcp_server/scaffolding/components/service.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C074 | `mcp_server/scaffolding/components/test.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C075 | `mcp_server/scaffolding/components/tool.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C076 | `mcp_server/scaffolding/components/worker.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C077 | `mcp_server/scaffolding/renderer.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Delete only parallel scaffold stack after all imports/callers move. |
| C078 | `mcp_server/scaffolding/metadata.py` | [CY078](planning-rollout.md#cy078) | CY078 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C079 | `mcp_server/scaffolding/utils.py` | [CY082](planning-rollout.md#cy082) | CY082 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C080 | `mcp_server/scaffolding/template_registry.py` | [CY077](planning-rollout.md#cy077) | CY077 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C081 | `mcp_server/scaffolding/version_hash.py` | [CY077](planning-rollout.md#cy077) | CY077 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C082 | `mcp_server/schemas/base.py` | [CY078](planning-rollout.md#cy078) | CY078 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C083 | `mcp_server/schemas/mixins/lifecycle.py` | [CY078](planning-rollout.md#cy078) | CY078 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C084 | `mcp_server/schemas/mixins/__init__.py` | [CY078](planning-rollout.md#cy078) | CY078 | None | Remove legacy provenance/schema authority only after last caller and successor evidence. |
| C085 | `mcp_server/schemas/__init__.py` | [CY087](planning-rollout.md#cy087) | CY002, CY008, CY009, CY011, CY071, CY077, CY078, CY081, CY083, CY086, CY087 | None | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C086 | `mcp_server/schemas/tool_outputs.py` | [CY011](planning-execution.md#cy011) | CY009, CY010, CY011, CY077, CY078, CY081, CY083, CY086, CY087 | CY053, CY055, CY056, CY057, CY058, CY059, CY060, CY061, CY071 | Stage exact operation models/transport outputs per consumer; preserve unrelated result models; no generic semantic parser. |
| C087 | `mcp_server/services/template_engine.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY005, CY031, CY041, CY053, CY079, CY080 | CY071 | Retain the migrated generic injected template engine used by the catalog (CY005); keep the old caller usable before CY072. CY080 removes only parallel scaffolding components, not this engine. |
| C088 | `mcp_server/scaffolders/base_scaffolder.py` | [CY075](planning-rollout.md#cy075) | CY075 | CY080 | Retire only in CY075 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C089 | `mcp_server/scaffolders/scaffold_result.py` | [CY075](planning-rollout.md#cy075) | CY075 | CY080 | Retire only in CY075 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C090 | `mcp_server/scaffolders/__init__.py` | [CY075](planning-rollout.md#cy075) | CY075 | CY080 | Retire only in CY075 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C091 | `mcp_server/tools/template_validation_tool.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C092 | `mcp_server/validation/template_validator.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C093 | `mcp_server/services/workspace_upgrader.py` | [CY076](planning-rollout.md#cy076) | CY076 | CY063, CY064, CY065, CY066, CY067, CY071 | Keep the old active upgrade route intact until public activation; delete it only after the replacement renewal CLI/startup proofs. |
| C094 | `mcp_server/tools/issue_tools.py` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 | CY071 | Only affected scaffold/refinement/result seam; preserve issue/GitHub publication semantics and use actual wrappers. |
| C095 | `mcp_server/tools/quality_tools.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Retire generic quality/parser/old public runtime after CY072; retained check/fix facts owned by native role cycles. |
| C096 | `mcp_server/tools/safe_edit_tool.py` | [CY081](planning-rollout.md#cy081) | CY081 | CY054, CY055, CY071 | Only affected scaffold/refinement/result seam; preserve issue/GitHub publication semantics and use actual wrappers. |
| C097 | `mcp_server/tools/scaffold_artifact.py` | [CY074](planning-rollout.md#cy074) | CY074 | CY053, CY071 | Retire only in CY074 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C098 | `mcp_server/tools/scaffold_schema_tool.py` | [CY074](planning-rollout.md#cy074) | CY074 | CY056, CY071 | Retire only in CY074 after public cutover; earlier episodes inspect or prepare its replacement. Later review means absence/import-closure evidence, never writing a deleted path. |
| C099 | `mcp_server/validation/base.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C100 | `mcp_server/validation/registry.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C101 | `mcp_server/validation/python_validator.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C102 | `mcp_server/validation/markdown_validator.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C103 | `mcp_server/validation/layered_template_validator.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C104 | `mcp_server/validation/template_analyzer.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C105 | `mcp_server/validation/validation_service.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Retire legacy validation/naming stack after CY052, CY053, CY054, CY055, CY056 and relevant native proof; no broader validation-domain cleanup. |
| C106 | `.pgmcp/config/presentation.yaml` | [CY072](planning-rollout.md#cy072) | CY011, CY056, CY057, CY058, CY059, CY060, CY061, CY072, CY078, CY081, CY083, CY086 | CY070 | Activate only already-proven target wiring/config and remove legacy required reads; additional cycle-specific slices listed below. |
| C107 | `mcp_server/core/interfaces/__init__.py` | [CY088](planning-rollout.md#cy088) | CY007, CY008, CY012, CY013, CY016, CY028, CY030, CY052, CY071, CY077, CY078, CY081, CY082, CY083, CY086, CY088 | None | Narrow interface export, adjacent tool guidance and standards resource wiring; no unrelated behavior change. |
| C108 | `mcp_server/core/interfaces/ipytest_runner.py` | [CY083](planning-rollout.md#cy083) | CY083 | None | Retire after native pytest conformance CY027, internal test service CY028, public test composition CY060 and successful actual cutover CY072. Remove all runtime/type-only imports with the old route. |
| C109 | `mcp_server/core/interfaces/quality.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Retire generic quality/parser/old public runtime after CY072; retained check/fix facts owned by native role cycles. |
| C110 | `mcp_server/managers/pytest_runner.py` | [CY083](planning-rollout.md#cy083) | CY083 | None | Retire after native pytest conformance CY027, internal test service CY028, public test composition CY060 and successful actual cutover CY072. Remove all runtime/type-only imports with the old route. |
| C111 | `mcp_server/managers/quality_state_repository.py` | [CY088](planning-rollout.md#cy088) | CY088 | None | Delete auto replay state only; retain independently proven general locking/cache/PR behavior. |
| C112 | `mcp_server/state/quality_state.py` | [CY088](planning-rollout.md#cy088) | CY088 | None | Delete auto replay state only; retain independently proven general locking/cache/PR behavior. |
| C113 | `mcp_server/tools/admin_tools.py` | [CY090](planning-rollout.md#cy090) | CY090 | None | Narrow interface export, adjacent tool guidance and standards resource wiring; no unrelated behavior change. |
| C114 | `mcp_server/tools/test_tools.py` | [CY083](planning-rollout.md#cy083) | CY083 | None | Retire after native pytest conformance CY027, internal test service CY028, public test composition CY060 and successful actual cutover CY072. Remove all runtime/type-only imports with the old route. |
| C115 | `mcp_server/utils/violation_parser.py` | [CY087](planning-rollout.md#cy087) | CY087 | None | Retire generic quality/parser/old public runtime after CY072; retained check/fix facts owned by native role cycles. |
| C116 | `docs/coding_standards/QUALITY_GATES.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |
| C117 | `docs/manuals/github-setup.md` | [CY091](planning-rollout.md#cy091) | CY091 | None | Align install/setup/root/native prerequisite/migration guidance; no external rollout. |
| C118 | `docs/manuals/user-guide.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |
| C119 | `docs/reference/server-configuration.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |
| C120 | `docs/setup/dev-isolation.md` | [CY091](planning-rollout.md#cy091) | CY091 | None | Align install/setup/root/native prerequisite/migration guidance; no external rollout. |
| C121 | `.agents/rules/qa.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C122 | `docs/agents/antigravity/rules/qa.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C123 | `docs/agents/codex/rules/qa.agent.md` | [CY072](planning-rollout.md#cy072) | CY072 | CY069 | Source-first host mapping; CY072 handles executable name/allowlist activation, CY069 completes semantic/parity review; preserve unaffected reboot and role authority. |
| C124 | `mcp_server/resources/standards.py` | [CY090](planning-rollout.md#cy090) | CY059, CY090 | None | Narrow interface export, adjacent tool guidance and standards resource wiring; no unrelated behavior change. |
| C125 | `docs/reference/copilot-agent-instructions-model.md` | [CY093](planning-rollout.md#cy093) | CY093 | None | Edit affected authority/navigation only; retain reviewed-unaffected material with explicit reason. |
| C126 | `docs/reference/resources.md` | [CY090](planning-rollout.md#cy090) | CY090 | None | Execution/result/resource/presentation explanation; preserve unrelated Git/project semantics. |

## t source register

151 tests and helpers.

| ID | Exact path | Primary owner | Ordered write episodes | Ordered review episodes | Bounded disposition |
|---|---|---|---|---|---|
| T001 | `tests/mcp_server/acceptance/test_issue56_acceptance.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T002 | `tests/mcp_server/config/test_component_registry.py` | [CY005](planning-execution.md#cy005) | CY005, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T003 | `tests/mcp_server/config/test_project_structure.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052, CY082 | None | Migrate location/containment/startup slice; preserve unrelated label/workflow assertions. |
| T004 | `tests/mcp_server/fixtures/artifact_test_harness.py` | [CY105](planning-rollout.md#cy105) | CY001, CY053, CY056, CY057, CY073, CY105 | None | Stage narrow support in its first consumer cycle; retire legacy helper only at CY105 after exact caller/plugin closure. |
| T005 | `tests/mcp_server/integration/mcp_server/test_scaffold_tool_execute_e2e.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T006 | `tests/mcp_server/integration/mcp_server/test_server_tool_registration.py` | [CY072](planning-rollout.md#cy072) | CY056, CY057, CY059, CY060, CY061, CY072 | None | Migrate affected registration/bootstrap/input rows; preserve unrelated tool/enforcement/schema claims. |
| T007 | `tests/mcp_server/integration/mcp_server/validation/test_safe_edit_validation_integration.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY055, CY058 | None | Complete-content enforce/report, original-file consistency, actual no-write/write and operations; use injected public boundaries. |
| T008 | `tests/mcp_server/integration/test_artifact_e2e.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T009 | `tests/mcp_server/integration/test_concrete_templates.py` | [CY037](planning-artifacts-mutation.md#cy037) | CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY095 | None | Split mixed concrete family assertions across CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039; retain portably meaningful behavior; no forced project lifecycle. |
| T010 | `tests/mcp_server/integration/test_config_error_e2e.py` | [CY005](planning-execution.md#cy005) | CY005, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T011 | `tests/mcp_server/integration/test_document_templates.py` | [CY097](planning-rollout.md#cy097) | CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY097 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T012 | `tests/mcp_server/integration/test_exception_propagation.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T013 | `tests/mcp_server/integration/test_metadata_e2e.py` | [CY007](planning-execution.md#cy007) | CY007, CY074, CY078 | None | Close all ArtifactManager imports/builders no later than CY074; preserve the mapped header/provenance/registry-or-location public intent in the earlier successor proof. Later retirement episodes cover only independent residual claims. |
| T014 | `tests/mcp_server/integration/test_pr_status_lockdown.py` | [CY105](planning-rollout.md#cy105) | CY073, CY105 | None | Preserve unrelated PR/workflow/root/server/cycle behavior; change only affected shared fixture interface. |
| T015 | `tests/mcp_server/integration/test_provenance_e2e.py` | [CY006](planning-execution.md#cy006) | CY006, CY074, CY077 | None | Close all ArtifactManager imports/builders no later than CY074; preserve the mapped header/provenance/registry-or-location public intent in the earlier successor proof. Later retirement episodes cover only independent residual claims. |
| T016 | `tests/mcp_server/integration/test_scaffold_validation_e2e.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056 | None | Actual prepared public schema/admission/resource equality; preserve unrelated schema-override rows. |
| T017 | `tests/mcp_server/integration/test_smoke_all_types.py` | [CY062](planning-rollout.md#cy062) | CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051, CY062 | None | Real delivered family acceptance; CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 supply each family case, CY062 accounts complete installed roots without copied context registry. |
| T018 | `tests/mcp_server/integration/test_strict_input_validation_response.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056 | None | Actual prepared public schema/admission/resource equality; preserve unrelated schema-override rows. |
| T019 | `tests/mcp_server/integration/test_template_missing_e2e.py` | [CY004](planning-execution.md#cy004) | CY004, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T020 | `tests/mcp_server/integration/test_tool_error_contract_e2e.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T021 | `tests/mcp_server/integration/test_tool_error_e2e.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T022 | `tests/mcp_server/integration/test_validation_policy_e2e.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY055, CY058 | None | Complete-content enforce/report, original-file consistency, actual no-write/write and operations; use injected public boundaries. |
| T023 | `tests/mcp_server/scaffolding/test_concrete_code_templates.py` | [CY095](planning-rollout.md#cy095) | CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY095 | None | Replace/remove source-level code/test assertions after CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039 semantic proof. |
| T024 | `tests/mcp_server/scaffolding/test_concrete_test_integration.py` | [CY095](planning-rollout.md#cy095) | CY095 | None | Replace/remove source-level code/test assertions after CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039 semantic proof. |
| T025 | `tests/mcp_server/scaffolding/test_concrete_test_unit.py` | [CY095](planning-rollout.md#cy095) | CY095 | None | Replace/remove source-level code/test assertions after CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039 semantic proof. |
| T026 | `tests/mcp_server/scaffolding/test_doc_template_pattern_imports.py` | [CY100](planning-rollout.md#cy100) | CY041, CY100 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T027 | `tests/mcp_server/scaffolding/test_doc_template_rendering.py` | [CY097](planning-rollout.md#cy097) | CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY097 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T028 | `tests/mcp_server/scaffolding/test_tier1_base_document.py` | [CY104](planning-rollout.md#cy104) | CY104 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T029 | `tests/mcp_server/scaffolding/test_tier3_document_patterns.py` | [CY100](planning-rollout.md#cy100) | CY100 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T030 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_assertions.py` | [CY103](planning-rollout.md#cy103) | CY103 | None | Remove the empty assertions placeholder and metadata-only tests. Caller-owned test bodies remain proved through CY038 and CY039; do not recreate a placeholder helper. |
| T031 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_async.py` | [CY099](planning-rollout.md#cy099) | CY031, CY034, CY035, CY036, CY037, CY038, CY039, CY099 | None | Preserve explicit async signatures/caller imports through class/Protocol CY034/CY035 and public test families CY038 and CY039; no inferred async-context-manager feature. |
| T032 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_di.py` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove source-project DI/strategy_cache/capability defaults after portable adapter/worker evidence CY036/CY037; no retained operational framework. |
| T033 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_error.py` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove project exception-wrapper macros; portable adapter/worker content and absence of implicit framework dependencies are proved in CY036/CY037. |
| T034 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_lifecycle.py` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove IWorkerLifecycle/strategy_cache initialization/shutdown defaults; retain only explicit portable worker content through CY037. |
| T035 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_log_enricher.py` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove LogEnricher/event-taxonomy defaults; retain explicit opt-in logging through CY036/CY037. |
| T036 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_logging.py` | [CY099](planning-rollout.md#cy099) | CY031, CY036, CY037, CY099 | None | Prove opt-in versus omitted logging through CY036/CY037; remove fixed macro/getLogger/import assertions. |
| T037 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_mocking.py` | [CY099](planning-rollout.md#cy099) | CY031, CY038, CY039, CY099 | None | Preserve caller-declared testing imports/doubles and fixture content through CY038 and CY039; no forced all-mock import set. |
| T038 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_pydantic.py` | [CY099](planning-rollout.md#cy099) | CY031, CY032, CY033, CY099 | None | Prove supplied Pydantic fields/constraints/defaults through DTO CY032 and config CY033; retire hidden ID/converter/validator inference. |
| T039 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_pytest.py` | [CY099](planning-rollout.md#cy099) | CY031, CY038, CY039, CY099 | None | Prove caller-selected pytest imports/content through CY038 and CY039; remove unconditional pytest/Path imports and macro-name assertions. |
| T040 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_test_fixtures.py` | [CY103](planning-rollout.md#cy103) | CY038, CY039, CY103 | None | Remove the orphan fixture macro only after scope/autouse/params, including combined options, are proved through actual unit/integration packages CY038 and CY039. |
| T041 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_test_structure.py` | [CY099](planning-rollout.md#cy099) | CY031, CY038, CY039, CY099 | None | Retain caller-selected test structure through CY038 and CY039; remove AAA prose snapshots and macro counts. |
| T042 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_translator.py` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove implicit project Translator/get_param_name conventions; portable operation content is covered by CY036/CY037. |
| T043 | `tests/mcp_server/scaffolding/test_tier3_pattern_python_typed_id.py` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove automatic project typed-ID defaults/imports; explicitly supplied factories/defaults remain covered by CY032. |
| T044 | `tests/mcp_server/scaffolding/test_tracking_templates.py` | [CY050](planning-artifacts-mutation.md#cy050) | CY049, CY050, CY051 | None | Public tracking body/refs/checklists/deferred semantics; CY051 separately covers commit part of mixed tracking file. |
| T045 | `tests/mcp_server/test_design_e2e.py` | [CY096](planning-rollout.md#cy096) | CY096 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T046 | `tests/mcp_server/test_design_template.py` | [CY096](planning-rollout.md#cy096) | CY096 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T047 | `tests/mcp_server/test_scaffolder_output_path_validation.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052, CY082 | None | Migrate location/containment/startup slice; preserve unrelated label/workflow assertions. |
| T048 | `tests/mcp_server/test_support.py` | [CY105](planning-rollout.md#cy105) | CY001, CY005, CY012, CY026, CY027, CY028, CY030, CY052, CY053, CY055, CY056, CY057, CY058, CY059, CY060, CY061, CY064, CY066, CY067, CY071, CY073, CY074, CY075, CY077, CY078, CY081, CY083, CY086, CY088, CY105 | None | Stage narrow support in its first consumer cycle; retire legacy helper only at CY105 after exact caller/plugin closure. |
| T049 | `tests/mcp_server/test_template_registry.py` | [CY006](planning-execution.md#cy006) | CY006, CY077 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T050 | `tests/mcp_server/test_tier0_conditional_header.py` | [CY007](planning-execution.md#cy007) | CY007, CY078 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T051 | `tests/mcp_server/test_tier0_template.py` | [CY007](planning-execution.md#cy007) | CY007, CY078 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T052 | `tests/mcp_server/test_tier0_two_line_format.py` | [CY007](planning-execution.md#cy007) | CY007, CY078 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T053 | `tests/mcp_server/test_tier1_document.py` | [CY104](planning-rollout.md#cy104) | CY104 | None | Retire old document/macro suites only with CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 semantic successors. |
| T054 | `tests/mcp_server/test_tier1_templates.py` | [CY104](planning-rollout.md#cy104) | CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY104 | None | Remove source-extends/tier/YAML snapshots after concrete Python family CY032–CY040 and document family CY042–CY051 evidence. Do not revive deferred YAML. |
| T055 | `tests/mcp_server/test_tier2_markdown.py` | [CY100](planning-rollout.md#cy100) | CY041, CY042, CY046, CY047, CY048, CY100 | None | Preserve supplied references and omitted links through actual document packages CY042–CY051; remove direct tier fixtures. |
| T056 | `tests/mcp_server/test_tier2_templates.py` | [CY104](planning-rollout.md#cy104) | CY031, CY034, CY035, CY036, CY037, CY041, CY046, CY047, CY104 | None | Preserve typed signatures, constructors and caller content through concrete Python and document owners CY032–CY051; remove tier/V2-header/YAML snapshots. |
| T057 | `tests/mcp_server/test_validation_enforcement.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Remove obsolete validation-language/tool claims only after relevant native and mutation/public proof. |
| T058 | `tests/mcp_server/test_validation_metadata.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Remove obsolete validation-language/tool claims only after relevant native and mutation/public proof. |
| T059 | `tests/mcp_server/test_version_hash.py` | [CY006](planning-execution.md#cy006) | CY006, CY077 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T060 | `tests/mcp_server/tools/test_a4_schema_overrides.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056, CY071 | None | Actual prepared public schema/admission/resource equality; preserve unrelated schema-override rows. |
| T061 | `tests/mcp_server/unit/config/test_artifact_definition_no_version.py` | [CY002](planning-execution.md#cy002) | CY002, CY077 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T062 | `tests/mcp_server/unit/config/test_artifact_registry_config.py` | [CY002](planning-execution.md#cy002) | CY002, CY077 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T063 | `tests/mcp_server/unit/config/test_artifacts_type_field.py` | [CY002](planning-execution.md#cy002) | CY002, CY077 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T064 | `tests/mcp_server/unit/config/test_c_loader_schema_structural.py` | [CY003](planning-execution.md#cy003) | CY003, CY005, CY012, CY016, CY028, CY030, CY052, CY064, CY071, CY077, CY078, CY081, CY086 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T065 | `tests/mcp_server/unit/config/test_scaffold_metadata_config.py` | [CY007](planning-execution.md#cy007) | CY007, CY078 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T066 | `tests/mcp_server/unit/config/test_contracts_loader.py` | [CY068](planning-rollout.md#cy068) | CY068, CY088 | None | Preserve loaded workflow ordering/instructions and get_work_context behavior; use actual public loaders/explicit composition. |
| T067 | `tests/mcp_server/unit/config/test_label_startup.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052, CY071, CY081, CY082 | None | Migrate location/containment/startup slice; preserve unrelated label/workflow assertions. |
| T068 | `tests/mcp_server/unit/config/test_loader_behaviors.py` | [CY003](planning-execution.md#cy003) | CY003, CY005, CY012, CY052, CY071, CY077, CY078, CY081, CY082 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T069 | `tests/mcp_server/unit/config/test_modular_loader.py` | [CY003](planning-execution.md#cy003) | CY003, CY005, CY071, CY077, CY078 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T070 | `tests/mcp_server/unit/config/test_settings.py` | [CY064](planning-rollout.md#cy064) | CY064 | None | Preserve public env/YAML/root/settings behavior; installation-only default changes. |
| T071 | `tests/mcp_server/unit/config/test_template_path_resolution.py` | [CY005](planning-execution.md#cy005) | CY005, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T072 | `tests/mcp_server/unit/config/test_tool_presentation_rollout.py` | [CY011](planning-execution.md#cy011) | CY011, CY057, CY058, CY059, CY060, CY061 | None | Actual wrapper/cache/presenter proof; retain unrelated tools and limits; remove test-produced response oracles. |
| T073 | `tests/mcp_server/unit/config/test_validator_c3.py` | [CY003](planning-execution.md#cy003) | CY003, CY012, CY052, CY071, CY081, CY082 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T074 | `tests/mcp_server/unit/config/test_workflow_config_c6.py` | [CY105](planning-rollout.md#cy105) | CY052, CY071, CY105 | None | Preserve unrelated PR/workflow/root/server/cycle behavior; change only affected shared fixture interface. |
| T075 | `tests/mcp_server/unit/integration/test_all_tools.py` | [CY083](planning-rollout.md#cy083) | CY056, CY057, CY059, CY060, CY061, CY071, CY073, CY083 | None | Actual public registered tools and narrow importability; preserve Git/GitHub/health/state. |
| T076 | `tests/mcp_server/unit/managers/test_artifact_manager_metadata.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T077 | `tests/mcp_server/unit/managers/test_artifact_manager_registry.py` | [CY006](planning-execution.md#cy006) | CY006, CY074, CY077 | None | Close all ArtifactManager imports/builders no later than CY074; preserve the mapped header/provenance/registry-or-location public intent in the earlier successor proof. Later retirement episodes cover only independent residual claims. |
| T078 | `tests/mcp_server/unit/managers/test_artifact_manager.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T079 | `tests/mcp_server/unit/managers/test_c3_note_context_scaffold_chain.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY074 | None | Adapt or consolidate public scaffold/error/persistence claim; old redundant suite removed only once CY057/CY058 proves its replacement. |
| T080 | `tests/mcp_server/unit/managers/test_directory_resolution.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052, CY074, CY082 | None | Close all ArtifactManager imports/builders no later than CY074; preserve the mapped header/provenance/registry-or-location public intent in the earlier successor proof. Later retirement episodes cover only independent residual claims. |
| T081 | `tests/mcp_server/unit/managers/test_typescript_dto_scaffold.py` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 | None | Real TS package schema/render; explicit structured caller fields. |
| T082 | `tests/mcp_server/unit/scaffolders/test_filesystem_integration.py` | [CY005](planning-execution.md#cy005) | CY005, CY075, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T083 | `tests/mcp_server/unit/scaffolders/test_template_registry.py` | [CY005](planning-execution.md#cy005) | CY005, CY075, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T084 | `tests/mcp_server/unit/scaffolders/test_template_scaffolder_introspection.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056, CY075, CY079 | None | Actual prepared public schema/admission/resource equality; preserve unrelated schema-override rows. |
| T085 | `tests/mcp_server/unit/scaffolders/test_template_scaffolder_no_hardcoded_fallback.py` | [CY005](planning-execution.md#cy005) | CY005, CY075, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T086 | `tests/mcp_server/unit/scaffolders/test_template_scaffolder.py` | [CY005](planning-execution.md#cy005) | CY005, CY075, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T087 | `tests/mcp_server/unit/scaffolding/test_components.py` | [CY080](planning-rollout.md#cy080) | CY080 | None | Remove per-artifact Python scaffolder assertions after CY032, CY033, CY034, CY035, CY036, CY037, CY038, CY039, CY040, CY041, CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050 plus CY053/CY057/CY058. |
| T088 | `tests/mcp_server/unit/scaffolding/test_metadata_parser.py` | [CY007](planning-execution.md#cy007) | CY007, CY078 | None | Replace header/identity meanings; old registry/timestamps/private parser claims retire at CY077/CY078/CY079/CY099/CY100/CY104. |
| T089 | `tests/mcp_server/unit/scaffolding/test_template_introspector.py` | [CY004](planning-execution.md#cy004) | CY004, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T090 | `tests/mcp_server/unit/schemas/test_lifecycle.py` | [CY002](planning-execution.md#cy002) | CY002, CY078 | None | Migrate pure config/admission/closed schema claim; preserve unrelated loader/startup behavior; no-op/lifecycle legacy portions removed at CY077/CY078/CY079. |
| T091 | `tests/mcp_server/unit/server/test_bootstrap.py` | [CY072](planning-rollout.md#cy072) | CY009, CY012, CY052, CY064, CY071, CY072, CY074, CY077, CY078, CY081, CY083, CY086 | None | Migrate affected registration/bootstrap/input rows; preserve unrelated tool/enforcement/schema claims. |
| T092 | `tests/mcp_server/unit/services/test_template_engine.py` | [CY005](planning-execution.md#cy005) | CY005, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T093 | `tests/mcp_server/unit/services/test_workspace_upgrader.py` | [CY066](planning-rollout.md#cy066) | CY063, CY064, CY065, CY066, CY067, CY076 | None | Split renewal assertions across CY063, CY064, CY065; replace old copy/registry heuristics with actual tree/checkpoint/recovery evidence. |
| T094 | `tests/mcp_server/unit/templates/test_generic_doc_template.py` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 | None | Actual Generic Document schema/render and primitive/extra rejection. |
| T095 | `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` | [CY105](planning-rollout.md#cy105) | CY001, CY052, CY071, CY077, CY078, CY082, CY105 | None | Preserve unrelated PR/workflow/root/server/cycle behavior; change only affected shared fixture interface. |
| T096 | `tests/mcp_server/unit/test_cli.py` | [CY067](planning-rollout.md#cy067) | CY064, CY067, CY072, CY076 | None | CLI result/filesystem preservation; CY072 activates routing; unrelated CLI behavior retained. |
| T097 | `tests/mcp_server/unit/test_server.py` | [CY105](planning-rollout.md#cy105) | CY009, CY011, CY071, CY105 | None | Preserve unrelated PR/workflow/root/server/cycle behavior; change only affected shared fixture interface. |
| T098 | `tests/mcp_server/unit/tools/test_cycle_tools.py` | [CY105](planning-rollout.md#cy105) | CY009, CY071, CY105 | None | Preserve unrelated PR/workflow/root/server/cycle behavior; change only affected shared fixture interface. |
| T099 | `tests/mcp_server/unit/tools/test_extra_forbid.py` | [CY088](planning-rollout.md#cy088) | CY056, CY057, CY058, CY059, CY060, CY061, CY071, CY073, CY077, CY078, CY079, CY081, CY082, CY083, CY086, CY087, CY088 | None | Migrate affected registration/bootstrap/input rows; preserve unrelated tool/enforcement/schema claims. |
| T100 | `tests/mcp_server/unit/tools/test_template_validation_tool.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Remove obsolete validation-language/tool claims only after relevant native and mutation/public proof. |
| T101 | `tests/mcp_server/unit/tools/test_issue_template_h1.py` | [CY050](planning-artifacts-mutation.md#cy050) | CY049, CY050 | None | Public tracking body/refs/checklists/deferred semantics; CY051 separately covers commit part of mixed tracking file. |
| T102 | `tests/mcp_server/unit/tools/test_safe_edit_tool.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY055, CY058, CY081 | None | Complete-content enforce/report, original-file consistency, actual no-write/write and operations; use injected public boundaries. |
| T103 | `tests/mcp_server/unit/tools/test_scaffold_artifact.py` | [CY057](planning-artifacts-mutation.md#cy057) | CY057, CY074 | None | Thin scaffold tool unchanged nested context and operational failures via real wrapper/injected service. |
| T104 | `tests/mcp_server/unit/tools/test_scaffold_schema_tool.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056, CY074 | None | Actual prepared public schema/admission/resource equality; preserve unrelated schema-override rows. |
| T105 | `tests/mcp_server/unit/validation/test_template_analyzer.py` | [CY004](planning-execution.md#cy004) | CY004, CY079 | None | Migrate graph/catalog/renderer claim via explicit-root public APIs; retirement waits for CY077/CY078/CY079/CY080 as applicable. |
| T106 | `tests/mcp_server/fixtures/fake_pytest_runner.py` | [CY105](planning-rollout.md#cy105) | CY027, CY028, CY060, CY083, CY105 | None | Stage narrow support in its first consumer cycle; retire legacy helper only at CY105 after exact caller/plugin closure. |
| T107 | `tests/mcp_server/integration/test_qa.py` | [CY026](planning-execution.md#cy026) | CY017, CY026, CY059 | None | Split selection/runtime/native/public cases into their bounded earlier cycles; no generic parser or global QA harness. |
| T108 | `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | [CY088](planning-rollout.md#cy088) | CY088 | None | Retire only auto-state registration/repository/value model claims; preserve PR transaction, atomic writer and cache under existing owners. |
| T109 | `tests/mcp_server/unit/config/test_quality_config.py` | [CY016](planning-execution.md#cy016) | CY012, CY016, CY028, CY030, CY071, CY086, CY087 | None | Preserve role-config coherence and explicit scope semantics through CY016/CY017, with actual public checks CY059. Close manager imports before CY086; retire only obsolete auto/parser/state claims at their named removal episodes after CY072. |
| T110 | `tests/mcp_server/unit/core/interfaces/test_interface_imports.py` | [CY088](planning-rollout.md#cy088) | CY012, CY013, CY016, CY028, CY030, CY071, CY083, CY086, CY088 | None | Actual public registered tools and narrow importability; preserve Git/GitHub/health/state. |
| T111 | `tests/mcp_server/unit/managers/test_auto_scope_resolution.py` | [CY017](planning-execution.md#cy017) | CY017 | None | Early scope episodes must replace obsolete auto/parser expectations and close every legacy manager import through explicit scope CY017; preserve public scope selection through CY059. No old-runtime dependency is deferred beyond manager removal. |
| T112 | `tests/mcp_server/unit/managers/test_autofix_propagation.py` | [CY030](planning-execution.md#cy030) | CY029, CY030, CY061, CY085 | None | Replace generic fixability propagation with explicit binding/order/native outcome evidence. |
| T113 | `tests/mcp_server/unit/managers/test_baseline_advance.py` | [CY085](planning-rollout.md#cy085) | CY085 | CY088 | Retire only auto-state registration/repository/value model claims; preserve PR transaction, atomic writer and cache under existing owners. |
| T114 | `tests/mcp_server/unit/managers/test_c8_cleanup_grep_closure.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T115 | `tests/mcp_server/unit/managers/test_execute_gate_dispatch.py` | [CY026](planning-execution.md#cy026) | CY013, CY020, CY021, CY022, CY026, CY059, CY086 | None | Split selection/runtime/native/public cases into their bounded earlier cycles; no generic parser or global QA harness. |
| T116 | `tests/mcp_server/unit/managers/test_extract_violations_array.py` | [CY022](planning-execution.md#cy022) | CY022, CY084 | CY087 | Retained native diagnostic facts through Pyright/Ruff adapter evidence; generic field-map/offset/fixability DSL retired at CY086/CY087. |
| T117 | `tests/mcp_server/unit/managers/test_files_for_gate.py` | [CY026](planning-execution.md#cy026) | CY017, CY026, CY059, CY086 | None | Split selection/runtime/native/public cases into their bounded earlier cycles; no generic parser or global QA harness. |
| T118 | `tests/mcp_server/unit/managers/test_filter_files_removed.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T119 | `tests/mcp_server/unit/managers/test_legacy_parsers_removed.py` | [CY084](planning-rollout.md#cy084) | CY084 | CY087 | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T120 | `tests/mcp_server/unit/managers/test_parse_json_violations_nested.py` | [CY022](planning-execution.md#cy022) | CY022, CY084 | CY087 | Retained native diagnostic facts through Pyright/Ruff adapter evidence; generic field-map/offset/fixability DSL retired at CY086/CY087. |
| T121 | `tests/mcp_server/unit/managers/test_parse_json_violations_options.py` | [CY022](planning-execution.md#cy022) | CY020, CY022, CY084 | CY087 | Retained native diagnostic facts through Pyright/Ruff adapter evidence; generic field-map/offset/fixability DSL retired at CY086/CY087. |
| T122 | `tests/mcp_server/unit/managers/test_parse_json_violations.py` | [CY022](planning-execution.md#cy022) | CY020, CY022, CY084 | CY087 | Retained native diagnostic facts through Pyright/Ruff adapter evidence; generic field-map/offset/fixability DSL retired at CY086/CY087. |
| T123 | `tests/mcp_server/unit/managers/test_parse_text_violations_defaults.py` | [CY084](planning-rollout.md#cy084) | CY084 | CY087 | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T124 | `tests/mcp_server/unit/managers/test_parse_text_violations.py` | [CY021](planning-execution.md#cy021) | CY021, CY084 | CY087 | Mypy native text including unmatched notes; no generic regex/default severity promise. |
| T125 | `tests/mcp_server/unit/managers/test_pyright_severity_mapping.py` | [CY022](planning-execution.md#cy022) | CY022, CY084 | CY087 | Retained native diagnostic facts through Pyright/Ruff adapter evidence; generic field-map/offset/fixability DSL retired at CY086/CY087. |
| T126 | `tests/mcp_server/unit/managers/test_pytest_helpers_removed.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T127 | `tests/mcp_server/unit/managers/test_pytest_runner.py` | [CY027](planning-execution.md#cy027) | CY027, CY028, CY060, CY083 | None | Preserve native Pytest outcomes, collection, coverage, LF/CRLF, args and descendants behind test/v1. |
| T128 | `tests/mcp_server/unit/managers/test_qa_manager.py` | [CY026](planning-execution.md#cy026) | CY013, CY014, CY017, CY020, CY021, CY022, CY026, CY059, CY086, CY087 | None | Split selection/runtime/native/public cases into their bounded earlier cycles; no generic parser or global QA harness. |
| T129 | `tests/mcp_server/unit/managers/test_quality_state_repository.py` | [CY088](planning-rollout.md#cy088) | CY088 | None | Retire only auto-state registration/repository/value model claims; preserve PR transaction, atomic writer and cache under existing owners. |
| T130 | `tests/mcp_server/unit/managers/test_skip_reason_unified.py` | [CY086](planning-rollout.md#cy086) | CY086 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T131 | `tests/mcp_server/unit/managers/test_summary_c39.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY011, CY026, CY059, CY085 | CY086 | Truthful check/public resource projection, relative operation paths vs unmodified bounded native diagnostics; no old summary/default DTO policy. |
| T132 | `tests/mcp_server/unit/managers/test_summary_line_formatter.py` | [CY011](planning-execution.md#cy011) | CY011 | None | Actual wrapper/cache/presenter proof; retain unrelated tools and limits; remove test-produced response oracles. |
| T133 | `tests/mcp_server/unit/managers/test_violation_path_normalization.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY026, CY059, CY085 | None | Truthful check/public resource projection, relative operation paths vs unmodified bounded native diagnostics; no old summary/default DTO policy. |
| T134 | `tests/mcp_server/unit/schemas/test_structured_tool_output_migration.py` | [CY011](planning-execution.md#cy011) | CY010, CY011, CY057, CY058, CY059, CY060, CY061, CY071 | None | Actual wrapper/cache/presenter proof; retain unrelated tools and limits; remove test-produced response oracles. |
| T135 | `tests/mcp_server/unit/state/test_quality_state.py` | [CY088](planning-rollout.md#cy088) | CY088 | None | Retire only auto-state registration/repository/value model claims; preserve PR transaction, atomic writer and cache under existing owners. |
| T136 | `tests/mcp_server/unit/tools/test_autofix_tool.py` | [CY061](planning-artifacts-mutation.md#cy061) | CY010, CY011, CY029, CY030, CY061, CY086 | None | Fix public effects plus independent FIFO/resource claim owned by CY011; no cache-claim loss at old tool removal. |
| T137 | `tests/mcp_server/unit/tools/test_dev_tools.py` | [CY060](planning-artifacts-mutation.md#cy060) | CY028, CY060, CY083 | None | Framework-neutral test public response; real decorators/cache replace substituted execute wrapper. |
| T138 | `tests/mcp_server/unit/tools/test_discovery_tools.py` | [CY068](planning-rollout.md#cy068) | CY068 | None | Preserve loaded workflow ordering/instructions and get_work_context behavior; use actual public loaders/explicit composition. |
| T139 | `tests/mcp_server/unit/tools/test_quality_tools.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY059 | None | Truthful check/public resource projection, relative operation paths vs unmodified bounded native diagnostics; no old summary/default DTO policy. |
| T140 | `tests/mcp_server/unit/tools/test_test_tools.py` | [CY060](planning-artifacts-mutation.md#cy060) | CY027, CY028, CY060, CY083 | None | Framework-neutral test public response; real decorators/cache replace substituted execute wrapper. |
| T141 | `tests/mcp_server/unit/tools/test_tool_result_contract.py` | [CY011](planning-execution.md#cy011) | CY010, CY011 | None | Actual wrapper/cache/presenter proof; retain unrelated tools and limits; remove test-produced response oracles. |
| T142 | `tests/mcp_server/unit/validation/test_python_validator.py` | [CY081](planning-rollout.md#cy081) | CY018, CY026, CY053, CY055, CY081 | None | Remove obsolete validation-language/tool claims only after relevant native and mutation/public proof. |
| T143 | `tests/mcp_server/validation_fixtures/violations.py` | [CY020](planning-execution.md#cy020) | CY018, CY020, CY021, CY022, CY086 | None | Assign negative snippets to Python syntax CY018, Markdown CY019, Ruff CY020 and Mypy CY021 native proofs. Remove only exhausted misleading examples after their effects are independently established. |
| T144 | `tests/mcp_server/unit/config/test_json_violations_parsing.py` | [CY087](planning-rollout.md#cy087) | CY087 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T145 | `tests/mcp_server/unit/config/test_quality_config_scope.py` | [CY017](planning-execution.md#cy017) | CY017 | None | Early scope episodes must replace obsolete auto/parser expectations and close every legacy manager import through explicit scope CY017; preserve public scope selection through CY059. No old-runtime dependency is deferred beyond manager removal. |
| T146 | `tests/mcp_server/unit/config/test_text_violations_parsing_defaults_validator.py` | [CY087](planning-rollout.md#cy087) | CY087 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T147 | `tests/mcp_server/unit/config/test_text_violations_parsing.py` | [CY087](planning-rollout.md#cy087) | CY087 | None | Consolidate bounded absence checks with native/role/public evidence; no per-private-symbol tombstone tests. |
| T148 | `tests/mcp_server/unit/config/test_violation_dto.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY059, CY087 | None | Truthful check/public resource projection, relative operation paths vs unmodified bounded native diagnostics; no old summary/default DTO policy. |
| T149 | `tests/mcp_server/unit/managers/test_compact_payload_builder.py` | [CY011](planning-execution.md#cy011) | CY010, CY011 | None | Actual wrapper/cache/presenter proof; retain unrelated tools and limits; remove test-produced response oracles. |
| T150 | `tests/mcp_server/unit/managers/test_scope_resolution.py` | [CY017](planning-execution.md#cy017) | CY017 | None | Early scope episodes must replace obsolete auto/parser expectations and close every legacy manager import through explicit scope CY017; preserve public scope selection through CY059. No old-runtime dependency is deferred beyond manager removal. |
| T151 | `tests/mcp_server/unit/resources/test_standards.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY059, CY090 | None | Truthful check/public resource projection, relative operation paths vs unmodified bounded native diagnostics; no old summary/default DTO policy. |

## a source register

79 legacy suite sources.

| ID | Exact path | Primary owner | Ordered write episodes | Ordered review episodes | Bounded disposition |
|---|---|---|---|---|---|
| A001 | `.pgmcp/templates/concrete/adapter.py.jinja2` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A002 | `.pgmcp/templates/concrete/architecture.md.jinja2` | [CY097](planning-rollout.md#cy097) | CY097 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A003 | `.pgmcp/templates/concrete/commit.txt.jinja2` | [CY098](planning-rollout.md#cy098) | CY098 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A004 | `.pgmcp/templates/concrete/config_schema.py.jinja2` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A005 | `.pgmcp/templates/concrete/design.md.jinja2` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A006 | `.pgmcp/templates/concrete/dto.py.jinja2` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A007 | `.pgmcp/templates/concrete/dto_v2.py.jinja2` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A008 | `.pgmcp/templates/concrete/generic.md.jinja2` | [CY097](planning-rollout.md#cy097) | CY097 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A009 | `.pgmcp/templates/concrete/generic.py.jinja2` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A010 | `.pgmcp/templates/concrete/interface.py.jinja2` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A011 | `.pgmcp/templates/concrete/issue.md.jinja2` | [CY098](planning-rollout.md#cy098) | CY098 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A012 | `.pgmcp/templates/concrete/planning.md.jinja2` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A013 | `.pgmcp/templates/concrete/pr.md.jinja2` | [CY098](planning-rollout.md#cy098) | CY098 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A014 | `.pgmcp/templates/concrete/reference.md.jinja2` | [CY097](planning-rollout.md#cy097) | CY097 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A015 | `.pgmcp/templates/concrete/research.md.jinja2` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A016 | `.pgmcp/templates/concrete/resource.py.jinja2` | [CY101](planning-rollout.md#cy101) | CY101 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A017 | `.pgmcp/templates/concrete/service_command.py.jinja2` | [CY101](planning-rollout.md#cy101) | CY101 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A018 | `.pgmcp/templates/concrete/test_integration.py.jinja2` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A019 | `.pgmcp/templates/concrete/test_unit.py.jinja2` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A020 | `.pgmcp/templates/concrete/tool.py.jinja2` | [CY101](planning-rollout.md#cy101) | CY101 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A021 | `.pgmcp/templates/concrete/typescript_dto.ts.jinja2` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A022 | `.pgmcp/templates/concrete/validation_report.md.jinja2` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A023 | `.pgmcp/templates/concrete/worker.py.jinja2` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A024 | `.pgmcp/templates/config/adapter.yaml` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A025 | `.pgmcp/templates/config/architecture.yaml` | [CY097](planning-rollout.md#cy097) | CY097 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A026 | `.pgmcp/templates/config/commit.yaml` | [CY098](planning-rollout.md#cy098) | CY098 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A027 | `.pgmcp/templates/config/design.yaml` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A028 | `.pgmcp/templates/config/dto.yaml` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A029 | `.pgmcp/templates/config/generic.yaml` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A030 | `.pgmcp/templates/config/generic_doc.yaml` | [CY097](planning-rollout.md#cy097) | CY097 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A031 | `.pgmcp/templates/config/integration_test.yaml` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A032 | `.pgmcp/templates/config/interface.yaml` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A033 | `.pgmcp/templates/config/issue.yaml` | [CY098](planning-rollout.md#cy098) | CY098 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A034 | `.pgmcp/templates/config/planning.yaml` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A035 | `.pgmcp/templates/config/pr.yaml` | [CY098](planning-rollout.md#cy098) | CY098 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A036 | `.pgmcp/templates/config/reference.yaml` | [CY097](planning-rollout.md#cy097) | CY097 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A037 | `.pgmcp/templates/config/research.yaml` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A038 | `.pgmcp/templates/config/resource.yaml` | [CY101](planning-rollout.md#cy101) | CY101 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A039 | `.pgmcp/templates/config/schema.yaml` | [CY094](planning-rollout.md#cy094) | CY094 | None | Remove after CY032/CY033/CY034/CY035: Pydantic and class/Protocol public package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A040 | `.pgmcp/templates/config/service.yaml` | [CY101](planning-rollout.md#cy101) | CY101 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A041 | `.pgmcp/templates/config/tool.yaml` | [CY101](planning-rollout.md#cy101) | CY101 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A042 | `.pgmcp/templates/config/typescript_dto.yaml` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A043 | `.pgmcp/templates/config/unit_test.yaml` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A044 | `.pgmcp/templates/config/validation_report.yaml` | [CY096](planning-rollout.md#cy096) | CY096 | None | Remove after CY042, CY043, CY044, CY045, CY046, CY047, CY048, CY049, CY050, CY051: document/tracking semantic evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A045 | `.pgmcp/templates/config/worker.yaml` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A046 | `.pgmcp/templates/tier0_base_artifact.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A047 | `.pgmcp/templates/tier1_base_code.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A048 | `.pgmcp/templates/tier1_base_config.jinja2` | [CY103](planning-rollout.md#cy103) | CY103 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A049 | `.pgmcp/templates/tier1_base_document.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A050 | `.pgmcp/templates/tier1_base_tracking.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A051 | `.pgmcp/templates/tier2_base_markdown.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A052 | `.pgmcp/templates/tier2_base_python.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A053 | `.pgmcp/templates/tier2_base_typescript.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A054 | `.pgmcp/templates/tier2_base_yaml.jinja2` | [CY103](planning-rollout.md#cy103) | CY103 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A055 | `.pgmcp/templates/tier2_tracking_markdown.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A056 | `.pgmcp/templates/tier2_tracking_text.jinja2` | [CY104](planning-rollout.md#cy104) | CY104 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A057 | `.pgmcp/templates/tier3_pattern_markdown_agent_hints.jinja2` | [CY103](planning-rollout.md#cy103) | CY103 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A058 | `.pgmcp/templates/tier3_pattern_markdown_dividers.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A059 | `.pgmcp/templates/tier3_pattern_markdown_open_questions.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A060 | `.pgmcp/templates/tier3_pattern_markdown_prerequisites.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A061 | `.pgmcp/templates/tier3_pattern_markdown_purpose_scope.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A062 | `.pgmcp/templates/tier3_pattern_markdown_related_docs.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A063 | `.pgmcp/templates/tier3_pattern_markdown_status_header.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A064 | `.pgmcp/templates/tier3_pattern_markdown_version_history.jinja2` | [CY100](planning-rollout.md#cy100) | CY100 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A065 | `.pgmcp/templates/tier3_pattern_python_assertions.jinja2` | [CY103](planning-rollout.md#cy103) | CY103 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A066 | `.pgmcp/templates/tier3_pattern_python_async.jinja2` | [CY099](planning-rollout.md#cy099) | CY099 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A067 | `.pgmcp/templates/tier3_pattern_python_di.jinja2` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A068 | `.pgmcp/templates/tier3_pattern_python_error.jinja2` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A069 | `.pgmcp/templates/tier3_pattern_python_lifecycle.jinja2` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A070 | `.pgmcp/templates/tier3_pattern_python_log_enricher.jinja2` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A071 | `.pgmcp/templates/tier3_pattern_python_logging.jinja2` | [CY099](planning-rollout.md#cy099) | CY099 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A072 | `.pgmcp/templates/tier3_pattern_python_mocking.jinja2` | [CY099](planning-rollout.md#cy099) | CY099 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A073 | `.pgmcp/templates/tier3_pattern_python_pydantic.jinja2` | [CY099](planning-rollout.md#cy099) | CY099 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A074 | `.pgmcp/templates/tier3_pattern_python_pytest.jinja2` | [CY099](planning-rollout.md#cy099) | CY099 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A075 | `.pgmcp/templates/tier3_pattern_python_test_fixtures.jinja2` | [CY103](planning-rollout.md#cy103) | CY103 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A076 | `.pgmcp/templates/tier3_pattern_python_test_structure.jinja2` | [CY099](planning-rollout.md#cy099) | CY099 | None | Remove after CY031/CY041 and all dependent family cycles: portable shared graph edges migrated. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A077 | `.pgmcp/templates/tier3_pattern_python_translator.jinja2` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A078 | `.pgmcp/templates/tier3_pattern_python_typed_id.jinja2` | [CY102](planning-rollout.md#cy102) | CY102 | None | Remove after CY032/CY033/CY036/CY037/CY038/CY039 and approved exclusions: rejected Resource/Service/Tool/project/orphan/YAML sources. The original source stays recoverable at the captured pre-cycle Git checkpoint. |
| A079 | `.pgmcp/templates/tier3_pattern_typescript_dto.jinja2` | [CY095](planning-rollout.md#cy095) | CY095 | None | Remove after CY036/CY037/CY038/CY039/CY040: portable operation/test/TS package evidence. The original source stays recoverable at the captured pre-cycle Git checkpoint. |

## s source register

57 additional existing dependencies.

| ID | Exact path | Primary owner | Ordered write episodes | Ordered review episodes | Bounded disposition |
|---|---|---|---|---|---|
| S001 | `mcp_server/core/decorators/input_validation_decorator.py` | [CY009](planning-execution.md#cy009) | CY008, CY009, CY056 | None | Prepared admission and normalization; preserve unrelated ValidationErrorOutput schema. |
| S002 | `mcp_server/utils/schema_utils.py` | [CY003](planning-execution.md#cy003) | CY003, CY056 | None | Bounded static refs without dropped constraints or network resolution. |
| S003 | `mcp_server/server.py` | [CY009](planning-execution.md#cy009) | CY009, CY011, CY056, CY057, CY058, CY059, CY060, CY061 | None | Operation/attachment assembly and publication only; existing enforcement and isError retained. |
| S004 | `mcp_server/presenters/text_presenter.py` | [CY011](planning-execution.md#cy011) | CY011, CY057, CY058, CY059, CY060, CY061 | None | Generic strict/nullable admission and configured projections; no native/error-class dispatch. |
| S005 | `mcp_server/presenters/collection_text_renderer.py` | [CY011](planning-execution.md#cy011) | CY011 | None | Generic supported shape classification, order and limits. |
| S006 | `tests/mcp_server/unit/presenters/test_collection_text_renderer.py` | [CY011](planning-execution.md#cy011) | CY011 | None | Strict scalars/nullable inline cases and unchanged rejection of unsupported shapes. |
| S007 | `tests/mcp_server/unit/presenters/test_text_presenter_composition.py` | [CY011](planning-execution.md#cy011) | CY009, CY011, CY057, CY058, CY059, CY060, CY061 | None | Actual public rows and byte-budget evidence. |
| S008 | `pyrightconfig.json` | [CY022](planning-execution.md#cy022) | CY022 | CY070, CY071, CY072 | CY022 applies only the approved Python 3.11/Windows editor/native settings and retains diagnostic toggles/execution environments. CY070/CY071/CY072 review preserved values; the duplicate [tool.pyright] in C006 remains until CY072 removes it. |
| S009 | `tests/mcp_server/unit/decorators/test_pipeline_decorators.py` | [CY009](planning-execution.md#cy009) | CY008, CY009, CY056, CY057, CY058, CY059, CY060, CY061 | None | Real input/enforcement/error transport, no substitute execute. |
| S010 | `tests/mcp_server/unit/resources/test_cache_resource.py` | [CY010](planning-execution.md#cy010) | CY010, CY057, CY058, CY059, CY060, CY061 | None | URI/read/FIFO and required-null variant round trips. |
| S011 | `tests/mcp_server/unit/utils/test_schema_utils.py` | [CY003](planning-execution.md#cy003) | CY003 | None | Complete schema inlining and bounded rejection. |
| S012 | `tests/conftest.py` | [CY105](planning-rollout.md#cy105) | CY001, CY071, CY073, CY105 | None | Only affected suite/plugin registration; workflow_fixtures plugin retained. |
| S013 | `tests/mcp_server/integration/mcp_server/conftest.py` | [CY105](planning-rollout.md#cy105) | CY009, CY071, CY073, CY105 | None | Explicit public server composition; GitHub mock behavior retained. |
| S014 | `tests/mcp_server/conftest.py` | [CY105](planning-rollout.md#cy105) | None | CY105 | Read-only preservation owner: unrelated CreateBranchInput reset; edit only if exact dependency requires it. |
| S015 | `tests/mcp_server/unit/conftest.py` | [CY105](planning-rollout.md#cy105) | None | CY105 | Read-only preservation owner: unrelated scoped environment; no global cleanup. |
| S016 | `tests/mcp_server/fixtures/workflow_fixtures.py` | [CY105](planning-rollout.md#cy105) | CY052, CY071, CY073, CY105 | None | Preserve workflow semantics; adapt only explicit root/loader acquisition. |
| S017 | `.pgmcp/config/project_structure.yaml` | [CY082](planning-rollout.md#cy082) | CY082 | CY070, CY071 | CY072 stops required loading; CY081/CY082 removes after explicit field/consumer migration. |
| S018 | `mcp_server/config/schemas/project_structure_config.py` | [CY082](planning-rollout.md#cy082) | CY082 | CY071 | Remove old directory schema after live consumer switch. |
| S019 | `mcp_server/core/directory_policy_resolver.py` | [CY082](planning-rollout.md#cy082) | CY082 | None | Remove obsolete inheritance/permissive fallback and last callers. |
| S020 | `mcp_server/core/policy_engine.py` | [CY082](planning-rollout.md#cy082) | CY082 | None | Remove only dead project-structure dependency; unrelated operation policy retained. |
| S021 | `tests/mcp_server/core/test_directory_policy_resolver.py` | [CY082](planning-rollout.md#cy082) | CY052, CY082 | None | Move meaningful location cases; retire old inherited directory contract. |
| S022 | `tests/mcp_server/core/test_policy_engine.py` | [CY082](planning-rollout.md#cy082) | CY082 | None | Retain unrelated operation policy claims; retire old directory dependency cases. |
| S023 | `tests/mcp_server/core/test_policy_engine_config.py` | [CY082](planning-rollout.md#cy082) | CY082 | None | Preserve operation-policy config behavior; no collateral deletion. |
| S024 | `mcp_server/managers/enforcement_runner.py` | [CY088](planning-rollout.md#cy088) | CY088 | None | Reviewed-unaffected directory consumer; remove only quality-state registration impact if present; preserve all actual enforcement. |
| S025 | `mcp_server/core/interfaces/icore_tool.py` | [CY009](planning-execution.md#cy009) | CY008, CY009 | None | Typed transport return contract, preserve unrelated generic binding behavior. |
| S026 | `mcp_server/core/interfaces/itool.py` | [CY009](planning-execution.md#cy009) | CY008, CY009 | None | Outer typed normalized execution. |
| S027 | `mcp_server/core/decorators/enforcement_decorator.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Transport carrier; preserve pre/post skip/approval behavior. |
| S028 | `mcp_server/core/decorators/tool_error_handler_decorator.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Keep existing error DTO and empty attachments on unrelated errors. |
| S029 | `mcp_server/schemas/presentation_output.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Structured resource presentation only; no domain policy. |
| S030 | `mcp_server/resources/cache.py` | [CY010](planning-execution.md#cy010) | CY010 | None | Schema-aware complete operation serialization; attachments excluded. |
| S031 | `mcp_server/state/response_cache.py` | [CY010](planning-execution.md#cy010) | CY010, CY088 | None | FIFO/publication claim preserved; no check-result reuse authority. |
| S032 | `tests/mcp_server/unit/state/test_response_cache.py` | [CY010](planning-execution.md#cy010) | CY010, CY088 | None | Independent existing FIFO/cache evidence required before old autofix suite removal. |
| S033 | `mcp_server/utils/atomic_file_writer.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY053, CY055, CY066, CY088 | None | Only justified create/guard/activation interface changes; preserve unrelated atomic writer consumers. |
| S034 | `mcp_server/core/interfaces/file_writer.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY053, CY055, CY066 | None | Narrow actual write boundary; no fixer transaction. |
| S035 | `tests/mcp_server/unit/utils/test_atomic_file_writer.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY053, CY055, CY066, CY088 | None | Independent atomicity/locking coverage retained before quality-state test removal. |
| S036 | `mcp_server/utils/atomic_json_writer.py` | [CY064](planning-rollout.md#cy064) | CY064, CY066, CY088 | None | Checkpoint publication uses existing general primitive; no new check state. |
| S037 | `mcp_server/utils/path_resolver.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY001, CY012, CY015, CY052, CY064, CY071 | None | Central resolved root/sibling ownership; no artifact IDs/native rules. |
| S038 | `scripts/build_package.py` | [CY062](planning-rollout.md#cy062) | CY062 | None | Build template_suite and all explicit bundled package assets; no workspace adapters as build source. |
| S039 | `tests/mcp_server/unit/test_build_package.py` | [CY062](planning-rollout.md#cy062) | CY062 | None | Real source mappings/dotfiles and package output. |
| S040 | `.pgmcp/config/release_manifest.yaml` | [CY062](planning-rollout.md#cy062) | CY062 | CY069 | Explicit suite mapping and source-authoritative agent assets only. |
| S041 | `docs/reference/release-assets-procedure.md` | [CY091](planning-rollout.md#cy091) | CY062, CY091 | None | Reflect actual source mappings/installed proof; preserve owner deployment authority. |
| S042 | `mcp_server/config/schemas/presentation_config.py` | [CY011](planning-execution.md#cy011) | CY011 | None | Generic declarative admission only, no new DTO-specific registry. |
| S043 | `mcp_server/core/interfaces/itool_response_cache.py` | [CY009](planning-execution.md#cy009) | CY009, CY010 | None | Narrow publisher/read separation; cache only operation. |
| S044 | `tests/mcp_server/unit/core/interfaces/test_itool_response_cache_segregation.py` | [CY010](planning-execution.md#cy010) | CY009, CY010 | None | Preserve publisher/read segregation. |
| S045 | `mcp_server/tools/tool_result.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Only affected final response composition carrier conversion. |
| S046 | `mcp_server/utils/mcp_converters.py` | [CY009](planning-execution.md#cy009) | CY009 | None | MCP resource/text assembly retains operation isError authority. |
| S047 | `mcp_server/core/decorators/__init__.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Necessary exports for transport changes only. |
| S048 | `docs/development/issue460/deferred-work.md` | [CY103](planning-rollout.md#cy103) | CY103 | None | Only append exact removed YAML source commit/release recovery trace explicitly required by Design; no Research strategy rewrite. |
| S049 | `mcp_server/managers/workspace_version_validator.py` | [CY071](planning-rollout.md#cy071) | CY071, CY077 | CY072 | Preserve configured version compatibility while final startup consumes installation.json; legacy scalar read is restricted to explicit one-time upgrade migration, then removed from normal startup. |
| S050 | `tests/mcp_server/unit/managers/test_workspace_version_validator.py` | [CY071](planning-rollout.md#cy071) | CY071, CY077 | CY072 | Keep missing/mismatch/bypass/error semantics at public validation; separately prove normal startup uses installation.json and only upgrade may read the legacy scalar. |
| S051 | `.pgmcp/.version` | [CY072](planning-rollout.md#cy072) | CY072 | CY070 | Capture compatibility value and bytes before explicit repository-owner migration; never derive a component checkpoint from this scalar; final normal startup stops reading it. |
| S052 | `mcp_server/schemas/error_outputs.py` | [CY009](planning-execution.md#cy009) | None | CY009 | Preserve existing ValidationErrorOutput.input_schema and all unrelated whole-tool cache facts; review only. Template-selected context failures use their target operation plus attachments. |
| S053 | `mcp_server/presenters/validation_resource_presenter.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Replace DTO/dictionary-specific schema extraction with the new attachment resource presenter; remove this obsolete module only with all imports switched in the same transport cycle. |
| S054 | `tests/mcp_server/integration/test_pipeline_e2e.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Migrate resource-presenter composition; preserve real pipeline success, cache fallback and enforcement blocker behavior. |
| S055 | `tests/mcp_server/unit/test_presenter.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Replace only old DTO-schema extraction tests with attachment presentation claims; retain text bounds, cache failure, error/notes and dynamic category behavior. |
| S056 | `mcp_server/presenters/__init__.py` | [CY009](planning-execution.md#cy009) | CY009 | None | Switch/remove the obsolete ValidationResourcePresenter eager export with the generic attachment presenter, preserving unrelated exports. |
| S057 | `mcp_server/validation/__init__.py` | [CY081](planning-rollout.md#cy081) | CY081 | None | Remove obsolete eager base/registry exports in the same cycle as their modules; fresh server imports must still work. |

## Readback prerequisite supplement

R001–R008 are additional dependencies of the bounded Planning QA tooling prerequisite. They do not replace or renumber the frozen 126 C / 151 T / 79 A / 57 S rows or the 279 proposed implementation paths. R001/R006/R007 were created by the prerequisite; the other five paths already existed outside that census. Their baseline for cycle recovery is the completed prerequisite commit, never ea48558c. No implementation cycle is already completed by this repair.

C086 (output models), S030 (cache resource), S010 (cache-resource tests) and C050 (project reference) already have exact rows and retain their existing owners. Those owners must preserve complete planning readback and the bounded-window protocol. The supplement's recorded write episodes grant only the stated seam. Review-only episodes grant no edits. Each corresponding card includes these IDs, proof paths, immediate previous writers and the existing independent recovery/stop-go rules.

| ID | Exact path | Accountable owner | Ordered write episodes | Review/preservation episodes | Bounded preservation obligation |
|---|---|---|---|---|---|
| R001 | `mcp_server/core/interfaces/project_plan.py` | [CY009](planning-execution.md#cy009) | None | CY009, CY071 | Retain narrow planning read contract and structural manager binding; no project-command exposure. |
| R002 | `mcp_server/managers/project_manager.py` | [CY071](planning-rollout.md#cy071) | None | CY009, CY071, CY072, CY105 | Preserve stored query, save/update schema and command-only deliverables backup; no project lifecycle refactor. |
| R003 | `mcp_server/tools/project_tools.py` | [CY009](planning-execution.md#cy009) | CY009 | CY010, CY071, CY072 | Adapt only the shared transport seam when required; preserve complete planning output, existing commands and phase behavior. |
| R004 | `tests/mcp_server/unit/tools/test_project_tools.py` | [CY105](planning-rollout.md#cy105) | CY001, CY009, CY072, CY105 | CY010, CY071, CY073 | Migrate only explicit-root, transport and surviving helper acquisition; retain absent/invalid/full planning and unrelated command assertions. |
| R005 | `tests/mcp_server/unit/managers/test_project_manager.py` | [CY105](planning-rollout.md#cy105) | CY001, CY072, CY105 | CY071, CY073 | Migrate only explicit-root and surviving helper acquisition; retain query byte preservation and all three command-backup observations. |
| R006 | `tests/mcp_server/integration/test_project_plan_readback.py` | [CY072](planning-rollout.md#cy072) | CY001, CY009, CY010, CY072, CY105 | CY071, CY073 | CY001 isolates fixture roots; CY009 adapts only transport; CY010 preserves full-response/window fidelity. CY071 prepares and tests exact config/template/bootstrap test hunks solely in isolated candidate copies; CY072 alone applies those preimage-checked live hunks. CY105 removes only residual exhausted helper acquisition. Retain save/update, fresh-cache and full MCP readback assertions. |
| R007 | `mcp_server/schemas/cache_chunk.py` | [CY010](planning-execution.md#cy010) | None | CY009, CY010, CY071 | Preserve frozen read-window/chunk values, full-content hash, Unicode offsets and explicit EOF; no secondary planning storage. |
| R008 | `mcp_server/schemas/deliverables.py` | [CY044](planning-artifacts-mutation.md#cy044) | None | CY009, CY010, CY044, CY071 | Retain existing strict frozen planning schema and cycle order validation used by save/update/read; no new planning-schema authority. |

The supplement does not authorize general project/state management cleanup. The existing state.json backup path in FileStateRepository is outside the prerequisite's deliverables-query correction. CY071 rehearses every necessary root/bootstrap test change in isolated copies and leaves the live R004/R005/R006 bytes unchanged. CY072 alone applies their exact preimage-checked test hunks with the rehearsed public cutover, then verifies the landed result; it makes no new migration decision. CY073 closes actual legacy import dependencies before production removal; CY105 may remove only the remaining exhausted helper acquisition.

## Proposed new source register

279 exact proposed paths. Files do not yet exist unless explicitly recorded as subsequent implementation progress. Creation and revisits are separately scoped by their cards.

| Exact path | Creation owner | Ordered write episodes |
|---|---|---|
| `tests/mcp_server/fixtures/suite_roots.py` | [CY001](planning-execution.md#cy001) | CY001 |
| `tests/mcp_server/unit/fixtures/test_suite_roots.py` | [CY001](planning-execution.md#cy001) | CY001 |
| `mcp_server/config/schemas/template_suite.py` | [CY002](planning-execution.md#cy002) | CY002 |
| `mcp_server/core/interfaces/template_catalog.py` | [CY002](planning-execution.md#cy002) | CY002 |
| `tests/mcp_server/unit/config/test_template_suite.py` | [CY002](planning-execution.md#cy002) | CY002 |
| `mcp_server/services/template_contract_loader.py` | [CY003](planning-execution.md#cy003) | CY003 |
| `tests/mcp_server/unit/services/test_template_contract_loader.py` | [CY003](planning-execution.md#cy003) | CY003 |
| `mcp_server/services/template_graph.py` | [CY004](planning-execution.md#cy004) | CY004 |
| `tests/mcp_server/unit/services/test_template_graph.py` | [CY004](planning-execution.md#cy004) | CY004 |
| `mcp_server/services/template_catalog.py` | [CY005](planning-execution.md#cy005) | CY005, CY071 |
| `tests/mcp_server/unit/services/test_template_catalog.py` | [CY005](planning-execution.md#cy005) | CY005 |
| `mcp_server/services/artifact_identity.py` | [CY006](planning-execution.md#cy006) | CY006 |
| `tests/mcp_server/unit/services/test_artifact_identity.py` | [CY006](planning-execution.md#cy006) | CY006 |
| `mcp_server/core/interfaces/artifact_header_reader.py` | [CY007](planning-execution.md#cy007) | CY007 |
| `mcp_server/services/artifact_header_reader.py` | [CY007](planning-execution.md#cy007) | CY007 |
| `tests/mcp_server/unit/services/test_artifact_header_reader.py` | [CY007](planning-execution.md#cy007) | CY007 |
| `.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2` | [CY007](planning-execution.md#cy007) | CY007 |
| `mcp_server/core/interfaces/tool_input_contract.py` | [CY008](planning-execution.md#cy008) | CY008 |
| `tests/mcp_server/integration/test_prepared_tool_contract.py` | [CY008](planning-execution.md#cy008) | CY008 |
| `mcp_server/core/tool_execution.py` | [CY009](planning-execution.md#cy009) | CY009 |
| `mcp_server/presenters/schema_resource_presenter.py` | [CY009](planning-execution.md#cy009) | CY009 |
| `tests/mcp_server/integration/test_tool_attachment_transport.py` | [CY009](planning-execution.md#cy009) | CY009 |
| `tests/mcp_server/integration/test_cache_fidelity_v3.py` | [CY010](planning-execution.md#cy010) | CY010 |
| `tests/mcp_server/integration/test_execution_presentation_v3.py` | [CY011](planning-execution.md#cy011) | CY011 |
| `mcp_server/config/schemas/adapter_manifest.py` | [CY012](planning-execution.md#cy012) | CY012 |
| `mcp_server/core/interfaces/execution.py` | [CY012](planning-execution.md#cy012) | CY012, CY013, CY053 |
| `mcp_server/execution/catalog.py` | [CY012](planning-execution.md#cy012) | CY012 |
| `tests/mcp_server/unit/execution/test_catalog.py` | [CY012](planning-execution.md#cy012) | CY012 |
| `mcp_server/execution/__init__.py` | [CY012](planning-execution.md#cy012) | CY012 |
| `mcp_server/bundled_adapters/__init__.py` | [CY012](planning-execution.md#cy012) | CY012 |
| `.pgmcp/config/adapters.yaml` | [CY012](planning-execution.md#cy012) | CY012, CY072 |
| `mcp_server/execution/contracts/check_v1.schema.json` | [CY012](planning-execution.md#cy012) | CY012 |
| `mcp_server/execution/contracts/test_v1.schema.json` | [CY012](planning-execution.md#cy012) | CY012 |
| `mcp_server/execution/contracts/fix_v1.schema.json` | [CY012](planning-execution.md#cy012) | CY012 |
| `mcp_server/execution/protocol.py` | [CY013](planning-execution.md#cy013) | CY013, CY014 |
| `mcp_server/execution/process_runtime.py` | [CY013](planning-execution.md#cy013) | CY013, CY014, CY015 |
| `tests/mcp_server/fixtures/adapter_process.py` | [CY013](planning-execution.md#cy013) | CY013 |
| `tests/mcp_server/integration/execution/test_process_runtime.py` | [CY013](planning-execution.md#cy013) | CY013 |
| `mcp_server/execution/models.py` | [CY013](planning-execution.md#cy013) | CY013, CY026, CY028, CY030 |
| `tests/mcp_server/integration/execution/test_process_stopping.py` | [CY014](planning-execution.md#cy014) | CY014 |
| `mcp_server/execution/content_input.py` | [CY015](planning-execution.md#cy015) | CY015, CY053 |
| `tests/mcp_server/integration/execution/test_content_input.py` | [CY015](planning-execution.md#cy015) | CY015, CY053 |
| `mcp_server/config/schemas/checks_config.py` | [CY016](planning-execution.md#cy016) | CY016, CY054 |
| `tests/mcp_server/unit/config/test_checks_config.py` | [CY016](planning-execution.md#cy016) | CY016 |
| `mcp_server/execution/check_selection.py` | [CY017](planning-execution.md#cy017) | CY017 |
| `tests/mcp_server/unit/execution/test_check_selection.py` | [CY017](planning-execution.md#cy017) | CY017 |
| `mcp_server/bundled_adapters/python_syntax/manifest.yaml` | [CY018](planning-execution.md#cy018) | CY018 |
| `mcp_server/bundled_adapters/python_syntax/check.py` | [CY018](planning-execution.md#cy018) | CY018 |
| `mcp_server/bundled_adapters/python_syntax/requirements.txt` | [CY018](planning-execution.md#cy018) | CY018 |
| `tests/mcp_server/integration/adapters/test_python_syntax.py` | [CY018](planning-execution.md#cy018) | CY018 |
| `mcp_server/bundled_adapters/markdown_preflight/manifest.yaml` | [CY019](planning-execution.md#cy019) | CY019 |
| `mcp_server/bundled_adapters/markdown_preflight/check.py` | [CY019](planning-execution.md#cy019) | CY019 |
| `mcp_server/bundled_adapters/markdown_preflight/requirements.txt` | [CY019](planning-execution.md#cy019) | CY019 |
| `tests/mcp_server/integration/adapters/test_markdown_preflight.py` | [CY019](planning-execution.md#cy019) | CY019 |
| `mcp_server/bundled_adapters/ruff/manifest.yaml` | [CY020](planning-execution.md#cy020) | CY020, CY029 |
| `mcp_server/bundled_adapters/ruff/check.py` | [CY020](planning-execution.md#cy020) | CY020 |
| `mcp_server/bundled_adapters/ruff/requirements.txt` | [CY020](planning-execution.md#cy020) | CY020, CY029 |
| `tests/mcp_server/integration/adapters/test_ruff_checks.py` | [CY020](planning-execution.md#cy020) | CY020 |
| `mcp_server/bundled_adapters/mypy/manifest.yaml` | [CY021](planning-execution.md#cy021) | CY021 |
| `mcp_server/bundled_adapters/mypy/check.py` | [CY021](planning-execution.md#cy021) | CY021 |
| `mcp_server/bundled_adapters/mypy/requirements.txt` | [CY021](planning-execution.md#cy021) | CY021 |
| `tests/mcp_server/integration/adapters/test_mypy.py` | [CY021](planning-execution.md#cy021) | CY021 |
| `mcp_server/bundled_adapters/pyright/manifest.yaml` | [CY022](planning-execution.md#cy022) | CY022 |
| `mcp_server/bundled_adapters/pyright/check.cjs` | [CY022](planning-execution.md#cy022) | CY022 |
| `mcp_server/bundled_adapters/pyright/package.json` | [CY022](planning-execution.md#cy022) | CY022 |
| `tests/mcp_server/integration/adapters/test_pyright.py` | [CY022](planning-execution.md#cy022) | CY022 |
| `mcp_server/bundled_adapters/typescript_syntax/manifest.yaml` | [CY023](planning-execution.md#cy023) | CY023 |
| `mcp_server/bundled_adapters/typescript_syntax/check.cjs` | [CY023](planning-execution.md#cy023) | CY023 |
| `mcp_server/bundled_adapters/typescript_syntax/package.json` | [CY023](planning-execution.md#cy023) | CY023 |
| `tests/mcp_server/integration/adapters/test_typescript_syntax.py` | [CY023](planning-execution.md#cy023) | CY023 |
| `mcp_server/bundled_adapters/commitlint/manifest.yaml` | [CY024](planning-execution.md#cy024) | CY024 |
| `mcp_server/bundled_adapters/commitlint/check.py` | [CY024](planning-execution.md#cy024) | CY024 |
| `mcp_server/bundled_adapters/commitlint/package.json` | [CY024](planning-execution.md#cy024) | CY024 |
| `mcp_server/bundled_adapters/commitlint/requirements.txt` | [CY024](planning-execution.md#cy024) | CY024 |
| `tests/mcp_server/integration/adapters/test_commitlint.py` | [CY024](planning-execution.md#cy024) | CY024 |
| `commitlint.config.cjs` | [CY024](planning-execution.md#cy024) | CY024 |
| `mcp_server/bundled_adapters/lychee/manifest.yaml` | [CY025](planning-execution.md#cy025) | CY025 |
| `mcp_server/bundled_adapters/lychee/check.py` | [CY025](planning-execution.md#cy025) | CY025 |
| `mcp_server/bundled_adapters/lychee/dependencies.json` | [CY025](planning-execution.md#cy025) | CY025 |
| `tests/mcp_server/integration/adapters/test_lychee.py` | [CY025](planning-execution.md#cy025) | CY025 |
| `mcp_server/execution/check_service.py` | [CY026](planning-execution.md#cy026) | CY026 |
| `tests/mcp_server/unit/execution/test_check_service.py` | [CY026](planning-execution.md#cy026) | CY026, CY053 |
| `tests/mcp_server/integration/execution/test_check_profiles.py` | [CY026](planning-execution.md#cy026) | CY026 |
| `.pgmcp/config/checks.yaml` | [CY026](planning-execution.md#cy026) | CY026, CY072 |
| `mcp_server/bundled_adapters/pytest/manifest.yaml` | [CY027](planning-execution.md#cy027) | CY027 |
| `mcp_server/bundled_adapters/pytest/test.py` | [CY027](planning-execution.md#cy027) | CY027 |
| `mcp_server/bundled_adapters/pytest/requirements.txt` | [CY027](planning-execution.md#cy027) | CY027 |
| `tests/mcp_server/fixtures/test_role_double.py` | [CY027](planning-execution.md#cy027) | CY027 |
| `tests/mcp_server/integration/adapters/test_pytest.py` | [CY027](planning-execution.md#cy027) | CY027 |
| `mcp_server/config/schemas/tests_config.py` | [CY028](planning-execution.md#cy028) | CY028 |
| `mcp_server/execution/test_service.py` | [CY028](planning-execution.md#cy028) | CY028 |
| `tests/mcp_server/unit/execution/test_test_service.py` | [CY028](planning-execution.md#cy028) | CY028 |
| `.pgmcp/config/tests.yaml` | [CY028](planning-execution.md#cy028) | CY028, CY072 |
| `mcp_server/bundled_adapters/ruff/fix.py` | [CY029](planning-execution.md#cy029) | CY029 |
| `tests/mcp_server/integration/adapters/test_ruff_fixes.py` | [CY029](planning-execution.md#cy029) | CY029 |
| `mcp_server/config/schemas/fixes_config.py` | [CY030](planning-execution.md#cy030) | CY030 |
| `mcp_server/execution/fix_service.py` | [CY030](planning-execution.md#cy030) | CY030 |
| `tests/mcp_server/unit/execution/test_fix_service.py` | [CY030](planning-execution.md#cy030) | CY030 |
| `.pgmcp/config/fixes.yaml` | [CY030](planning-execution.md#cy030) | CY030, CY072 |
| `tests/mcp_server/integration/templates/test_shared_python.py` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/definitions/python.schema.json` | [CY031](planning-artifacts-mutation.md#cy031) | CY031, CY033, CY035, CY037, CY039 |
| `.pgmcp/template_suite/shared/templates/bases/tier1_code.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/bases/tier2_python.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/bases/tier2_typescript.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/patterns/python/signatures.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/patterns/python/logging.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/shared/templates/patterns/testing/pytest.jinja2` | [CY031](planning-artifacts-mutation.md#cy031) | CY031 |
| `.pgmcp/template_suite/python_pydantic_dto/manifest.yaml` | [CY032](planning-artifacts-mutation.md#cy032) | CY032 |
| `.pgmcp/template_suite/python_pydantic_dto/.version` | [CY032](planning-artifacts-mutation.md#cy032) | CY032 |
| `.pgmcp/template_suite/python_pydantic_dto/policy.yaml` | [CY032](planning-artifacts-mutation.md#cy032) | CY032 |
| `.pgmcp/template_suite/python_pydantic_dto/context.schema.json` | [CY032](planning-artifacts-mutation.md#cy032) | CY032, CY033 |
| `.pgmcp/template_suite/python_pydantic_dto/template.jinja2` | [CY032](planning-artifacts-mutation.md#cy032) | CY032 |
| `tests/mcp_server/integration/templates/test_python_pydantic_dto.py` | [CY032](planning-artifacts-mutation.md#cy032) | CY032, CY034 |
| `.pgmcp/template_suite/python_pydantic_config/manifest.yaml` | [CY033](planning-artifacts-mutation.md#cy033) | CY033 |
| `.pgmcp/template_suite/python_pydantic_config/.version` | [CY033](planning-artifacts-mutation.md#cy033) | CY033 |
| `.pgmcp/template_suite/python_pydantic_config/policy.yaml` | [CY033](planning-artifacts-mutation.md#cy033) | CY033 |
| `.pgmcp/template_suite/python_pydantic_config/context.schema.json` | [CY033](planning-artifacts-mutation.md#cy033) | CY033 |
| `.pgmcp/template_suite/python_pydantic_config/template.jinja2` | [CY033](planning-artifacts-mutation.md#cy033) | CY033 |
| `tests/mcp_server/integration/templates/test_python_pydantic_config.py` | [CY033](planning-artifacts-mutation.md#cy033) | CY033, CY034 |
| `.pgmcp/template_suite/python_class/manifest.yaml` | [CY034](planning-artifacts-mutation.md#cy034) | CY034 |
| `.pgmcp/template_suite/python_class/.version` | [CY034](planning-artifacts-mutation.md#cy034) | CY034 |
| `.pgmcp/template_suite/python_class/policy.yaml` | [CY034](planning-artifacts-mutation.md#cy034) | CY034 |
| `.pgmcp/template_suite/python_class/context.schema.json` | [CY034](planning-artifacts-mutation.md#cy034) | CY034, CY035 |
| `.pgmcp/template_suite/python_class/template.jinja2` | [CY034](planning-artifacts-mutation.md#cy034) | CY034 |
| `tests/mcp_server/integration/templates/test_python_class.py` | [CY034](planning-artifacts-mutation.md#cy034) | CY034 |
| `tests/mcp_server/fixtures/delivered_templates.py` | [CY034](planning-artifacts-mutation.md#cy034) | CY034 |
| `.pgmcp/template_suite/python_protocol/manifest.yaml` | [CY035](planning-artifacts-mutation.md#cy035) | CY035 |
| `.pgmcp/template_suite/python_protocol/.version` | [CY035](planning-artifacts-mutation.md#cy035) | CY035 |
| `.pgmcp/template_suite/python_protocol/policy.yaml` | [CY035](planning-artifacts-mutation.md#cy035) | CY035 |
| `.pgmcp/template_suite/python_protocol/context.schema.json` | [CY035](planning-artifacts-mutation.md#cy035) | CY035 |
| `.pgmcp/template_suite/python_protocol/template.jinja2` | [CY035](planning-artifacts-mutation.md#cy035) | CY035 |
| `tests/mcp_server/integration/templates/test_python_protocol.py` | [CY035](planning-artifacts-mutation.md#cy035) | CY035 |
| `.pgmcp/template_suite/python_adapter/manifest.yaml` | [CY036](planning-artifacts-mutation.md#cy036) | CY036 |
| `.pgmcp/template_suite/python_adapter/.version` | [CY036](planning-artifacts-mutation.md#cy036) | CY036 |
| `.pgmcp/template_suite/python_adapter/policy.yaml` | [CY036](planning-artifacts-mutation.md#cy036) | CY036 |
| `.pgmcp/template_suite/python_adapter/context.schema.json` | [CY036](planning-artifacts-mutation.md#cy036) | CY036, CY037 |
| `.pgmcp/template_suite/python_adapter/template.jinja2` | [CY036](planning-artifacts-mutation.md#cy036) | CY036 |
| `tests/mcp_server/integration/templates/test_python_adapter.py` | [CY036](planning-artifacts-mutation.md#cy036) | CY036 |
| `.pgmcp/template_suite/python_worker/manifest.yaml` | [CY037](planning-artifacts-mutation.md#cy037) | CY037 |
| `.pgmcp/template_suite/python_worker/.version` | [CY037](planning-artifacts-mutation.md#cy037) | CY037 |
| `.pgmcp/template_suite/python_worker/policy.yaml` | [CY037](planning-artifacts-mutation.md#cy037) | CY037 |
| `.pgmcp/template_suite/python_worker/context.schema.json` | [CY037](planning-artifacts-mutation.md#cy037) | CY037 |
| `.pgmcp/template_suite/python_worker/template.jinja2` | [CY037](planning-artifacts-mutation.md#cy037) | CY037 |
| `tests/mcp_server/integration/templates/test_python_worker.py` | [CY037](planning-artifacts-mutation.md#cy037) | CY037 |
| `.pgmcp/template_suite/pytest_unit_test/manifest.yaml` | [CY038](planning-artifacts-mutation.md#cy038) | CY038 |
| `.pgmcp/template_suite/pytest_unit_test/.version` | [CY038](planning-artifacts-mutation.md#cy038) | CY038 |
| `.pgmcp/template_suite/pytest_unit_test/policy.yaml` | [CY038](planning-artifacts-mutation.md#cy038) | CY038 |
| `.pgmcp/template_suite/pytest_unit_test/context.schema.json` | [CY038](planning-artifacts-mutation.md#cy038) | CY038, CY039 |
| `.pgmcp/template_suite/pytest_unit_test/template.jinja2` | [CY038](planning-artifacts-mutation.md#cy038) | CY038 |
| `tests/mcp_server/integration/templates/test_pytest_unit_test.py` | [CY038](planning-artifacts-mutation.md#cy038) | CY038 |
| `.pgmcp/template_suite/pytest_integration_test/manifest.yaml` | [CY039](planning-artifacts-mutation.md#cy039) | CY039 |
| `.pgmcp/template_suite/pytest_integration_test/.version` | [CY039](planning-artifacts-mutation.md#cy039) | CY039 |
| `.pgmcp/template_suite/pytest_integration_test/policy.yaml` | [CY039](planning-artifacts-mutation.md#cy039) | CY039 |
| `.pgmcp/template_suite/pytest_integration_test/context.schema.json` | [CY039](planning-artifacts-mutation.md#cy039) | CY039 |
| `.pgmcp/template_suite/pytest_integration_test/template.jinja2` | [CY039](planning-artifacts-mutation.md#cy039) | CY039 |
| `tests/mcp_server/integration/templates/test_pytest_integration_test.py` | [CY039](planning-artifacts-mutation.md#cy039) | CY039 |
| `tests/mcp_server/integration/templates/test_typescript_artifact.py` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 |
| `.pgmcp/template_suite/typescript_dto/manifest.yaml` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 |
| `.pgmcp/template_suite/typescript_dto/.version` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 |
| `.pgmcp/template_suite/typescript_dto/policy.yaml` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 |
| `.pgmcp/template_suite/typescript_dto/context.schema.json` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 |
| `.pgmcp/template_suite/typescript_dto/template.jinja2` | [CY040](planning-artifacts-mutation.md#cy040) | CY040 |
| `tests/mcp_server/integration/templates/test_shared_documents.py` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/bases/tier1_document.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/bases/tier1_tracking.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/bases/tier2_markdown_tracking.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/bases/tier2_text_tracking.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/patterns/markdown/links.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/templates/patterns/markdown/sections.jinja2` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/definitions/link.schema.json` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/definitions/issue-reference.schema.json` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `.pgmcp/template_suite/shared/definitions/checklist-item.schema.json` | [CY041](planning-artifacts-mutation.md#cy041) | CY041 |
| `tests/mcp_server/integration/templates/test_research_artifact.py` | [CY042](planning-artifacts-mutation.md#cy042) | CY042, CY047 |
| `.pgmcp/template_suite/research/manifest.yaml` | [CY042](planning-artifacts-mutation.md#cy042) | CY042 |
| `.pgmcp/template_suite/research/.version` | [CY042](planning-artifacts-mutation.md#cy042) | CY042 |
| `.pgmcp/template_suite/research/policy.yaml` | [CY042](planning-artifacts-mutation.md#cy042) | CY042 |
| `.pgmcp/template_suite/research/context.schema.json` | [CY042](planning-artifacts-mutation.md#cy042) | CY042, CY043, CY045 |
| `.pgmcp/template_suite/shared/definitions/evidence.schema.json` | [CY045](planning-artifacts-mutation.md#cy045) | CY045 |
| `.pgmcp/template_suite/shared/definitions/risk.schema.json` | [CY043](planning-artifacts-mutation.md#cy043) | CY043 |
| `.pgmcp/template_suite/research/template.jinja2` | [CY042](planning-artifacts-mutation.md#cy042) | CY042 |
| `tests/mcp_server/integration/templates/test_design_artifact.py` | [CY043](planning-artifacts-mutation.md#cy043) | CY043, CY047 |
| `.pgmcp/template_suite/design/manifest.yaml` | [CY043](planning-artifacts-mutation.md#cy043) | CY043 |
| `.pgmcp/template_suite/design/.version` | [CY043](planning-artifacts-mutation.md#cy043) | CY043 |
| `.pgmcp/template_suite/design/policy.yaml` | [CY043](planning-artifacts-mutation.md#cy043) | CY043 |
| `.pgmcp/template_suite/design/context.schema.json` | [CY043](planning-artifacts-mutation.md#cy043) | CY043, CY044, CY046, CY048 |
| `.pgmcp/template_suite/shared/definitions/section.schema.json` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/shared/definitions/decision.schema.json` | [CY046](planning-artifacts-mutation.md#cy046) | CY046 |
| `.pgmcp/template_suite/shared/definitions/evidence-requirement.schema.json` | [CY044](planning-artifacts-mutation.md#cy044) | CY044 |
| `.pgmcp/template_suite/design/template.jinja2` | [CY043](planning-artifacts-mutation.md#cy043) | CY043 |
| `tests/mcp_server/integration/templates/test_planning_artifact.py` | [CY044](planning-artifacts-mutation.md#cy044) | CY044, CY047 |
| `.pgmcp/template_suite/planning/manifest.yaml` | [CY044](planning-artifacts-mutation.md#cy044) | CY044 |
| `.pgmcp/template_suite/planning/.version` | [CY044](planning-artifacts-mutation.md#cy044) | CY044 |
| `.pgmcp/template_suite/planning/policy.yaml` | [CY044](planning-artifacts-mutation.md#cy044) | CY044 |
| `.pgmcp/template_suite/planning/context.schema.json` | [CY044](planning-artifacts-mutation.md#cy044) | CY044 |
| `.pgmcp/template_suite/planning/template.jinja2` | [CY044](planning-artifacts-mutation.md#cy044) | CY044 |
| `tests/mcp_server/integration/templates/test_validation_artifact.py` | [CY045](planning-artifacts-mutation.md#cy045) | CY045, CY047 |
| `.pgmcp/template_suite/validation_report/manifest.yaml` | [CY045](planning-artifacts-mutation.md#cy045) | CY045 |
| `.pgmcp/template_suite/validation_report/.version` | [CY045](planning-artifacts-mutation.md#cy045) | CY045 |
| `.pgmcp/template_suite/validation_report/policy.yaml` | [CY045](planning-artifacts-mutation.md#cy045) | CY045 |
| `.pgmcp/template_suite/validation_report/context.schema.json` | [CY045](planning-artifacts-mutation.md#cy045) | CY045, CY050 |
| `.pgmcp/template_suite/shared/definitions/deferred-item.schema.json` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `.pgmcp/template_suite/validation_report/template.jinja2` | [CY045](planning-artifacts-mutation.md#cy045) | CY045 |
| `.pgmcp/template_suite/architecture/manifest.yaml` | [CY046](planning-artifacts-mutation.md#cy046) | CY046 |
| `.pgmcp/template_suite/architecture/.version` | [CY046](planning-artifacts-mutation.md#cy046) | CY046 |
| `.pgmcp/template_suite/architecture/policy.yaml` | [CY046](planning-artifacts-mutation.md#cy046) | CY046 |
| `.pgmcp/template_suite/architecture/context.schema.json` | [CY046](planning-artifacts-mutation.md#cy046) | CY046 |
| `.pgmcp/template_suite/architecture/template.jinja2` | [CY046](planning-artifacts-mutation.md#cy046) | CY046 |
| `tests/mcp_server/integration/templates/test_architecture.py` | [CY046](planning-artifacts-mutation.md#cy046) | CY046, CY047 |
| `.pgmcp/template_suite/reference/manifest.yaml` | [CY047](planning-artifacts-mutation.md#cy047) | CY047 |
| `.pgmcp/template_suite/reference/.version` | [CY047](planning-artifacts-mutation.md#cy047) | CY047 |
| `.pgmcp/template_suite/reference/policy.yaml` | [CY047](planning-artifacts-mutation.md#cy047) | CY047 |
| `.pgmcp/template_suite/reference/context.schema.json` | [CY047](planning-artifacts-mutation.md#cy047) | CY047 |
| `.pgmcp/template_suite/reference/template.jinja2` | [CY047](planning-artifacts-mutation.md#cy047) | CY047 |
| `tests/mcp_server/integration/templates/test_reference.py` | [CY047](planning-artifacts-mutation.md#cy047) | CY047 |
| `tests/mcp_server/integration/templates/test_generic_document.py` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/generic_doc/manifest.yaml` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/generic_doc/.version` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/generic_doc/policy.yaml` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/generic_doc/context.schema.json` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/generic_doc/template.jinja2` | [CY048](planning-artifacts-mutation.md#cy048) | CY048 |
| `.pgmcp/template_suite/issue/manifest.yaml` | [CY049](planning-artifacts-mutation.md#cy049) | CY049 |
| `.pgmcp/template_suite/issue/.version` | [CY049](planning-artifacts-mutation.md#cy049) | CY049 |
| `.pgmcp/template_suite/issue/policy.yaml` | [CY049](planning-artifacts-mutation.md#cy049) | CY049 |
| `.pgmcp/template_suite/issue/context.schema.json` | [CY049](planning-artifacts-mutation.md#cy049) | CY049 |
| `.pgmcp/template_suite/issue/template.jinja2` | [CY049](planning-artifacts-mutation.md#cy049) | CY049 |
| `tests/mcp_server/integration/templates/test_issue.py` | [CY049](planning-artifacts-mutation.md#cy049) | CY049 |
| `.pgmcp/template_suite/pr/manifest.yaml` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `.pgmcp/template_suite/pr/.version` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `.pgmcp/template_suite/pr/policy.yaml` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `.pgmcp/template_suite/pr/context.schema.json` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `.pgmcp/template_suite/pr/template.jinja2` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `tests/mcp_server/integration/templates/test_pr.py` | [CY050](planning-artifacts-mutation.md#cy050) | CY050 |
| `tests/mcp_server/integration/templates/test_commit_artifact.py` | [CY051](planning-artifacts-mutation.md#cy051) | CY051 |
| `.pgmcp/template_suite/commit/manifest.yaml` | [CY051](planning-artifacts-mutation.md#cy051) | CY051 |
| `.pgmcp/template_suite/commit/.version` | [CY051](planning-artifacts-mutation.md#cy051) | CY051 |
| `.pgmcp/template_suite/commit/policy.yaml` | [CY051](planning-artifacts-mutation.md#cy051) | CY051 |
| `.pgmcp/template_suite/commit/context.schema.json` | [CY051](planning-artifacts-mutation.md#cy051) | CY051 |
| `.pgmcp/template_suite/commit/template.jinja2` | [CY051](planning-artifacts-mutation.md#cy051) | CY051 |
| `mcp_server/config/schemas/artifact_locations.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052 |
| `mcp_server/services/artifact_target_resolver.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052, CY053 |
| `tests/mcp_server/unit/services/test_artifact_target_resolver.py` | [CY052](planning-artifacts-mutation.md#cy052) | CY052 |
| `mcp_server/services/scaffold_operation.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY055 |
| `tests/mcp_server/integration/test_scaffold_operation_v3.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053 |
| `mcp_server/schemas/mutation_outputs.py` | [CY053](planning-artifacts-mutation.md#cy053) | CY053, CY055, CY057, CY058 |
| `mcp_server/services/edit_construction.py` | [CY054](planning-artifacts-mutation.md#cy054) | CY054 |
| `tests/mcp_server/unit/services/test_edit_construction.py` | [CY054](planning-artifacts-mutation.md#cy054) | CY054 |
| `mcp_server/services/edit_operation.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY055 |
| `tests/mcp_server/integration/test_edit_operation_v3.py` | [CY055](planning-artifacts-mutation.md#cy055) | CY055 |
| `tests/mcp_server/integration/test_schema_public_v3.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056 |
| `mcp_server/tools/template_schema_tool.py` | [CY056](planning-artifacts-mutation.md#cy056) | CY056 |
| `mcp_server/tools/scaffold_tool.py` | [CY057](planning-artifacts-mutation.md#cy057) | CY057 |
| `tests/mcp_server/integration/test_scaffold_public_v3.py` | [CY057](planning-artifacts-mutation.md#cy057) | CY057 |
| `mcp_server/tools/edit_tool.py` | [CY058](planning-artifacts-mutation.md#cy058) | CY058 |
| `tests/mcp_server/integration/test_edit_public_v3.py` | [CY058](planning-artifacts-mutation.md#cy058) | CY058 |
| `mcp_server/tools/check_tools.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY059 |
| `tests/mcp_server/integration/test_checks_public_v3.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY059 |
| `mcp_server/schemas/execution_outputs.py` | [CY059](planning-artifacts-mutation.md#cy059) | CY059, CY060, CY061 |
| `mcp_server/tools/run_tests_tool.py` | [CY060](planning-artifacts-mutation.md#cy060) | CY060 |
| `tests/mcp_server/integration/test_tests_public_v3.py` | [CY060](planning-artifacts-mutation.md#cy060) | CY060 |
| `mcp_server/tools/fix_tools.py` | [CY061](planning-artifacts-mutation.md#cy061) | CY061 |
| `tests/mcp_server/integration/test_fixes_public_v3.py` | [CY061](planning-artifacts-mutation.md#cy061) | CY061 |
| `tests/mcp_server/fixtures/installed_distribution.py` | [CY062](planning-rollout.md#cy062) | CY062 |
| `tests/mcp_server/integration/test_installed_distribution_v3.py` | [CY062](planning-rollout.md#cy062) | CY062 |
| `mcp_server/services/template_components.py` | [CY063](planning-rollout.md#cy063) | CY063 |
| `tests/mcp_server/unit/services/test_template_components.py` | [CY063](planning-rollout.md#cy063) | CY063 |
| `mcp_server/services/template_renewal.py` | [CY063](planning-rollout.md#cy063) | CY063, CY064, CY065, CY066, CY067 |
| `mcp_server/config/schemas/installation.py` | [CY064](planning-rollout.md#cy064) | CY064 |
| `mcp_server/services/installation_state.py` | [CY064](planning-rollout.md#cy064) | CY064, CY071 |
| `tests/mcp_server/unit/services/test_installation_state.py` | [CY064](planning-rollout.md#cy064) | CY064 |
| `mcp_server/services/template_proposal.py` | [CY065](planning-rollout.md#cy065) | CY065 |
| `tests/mcp_server/integration/test_template_proposal.py` | [CY065](planning-rollout.md#cy065) | CY065 |
| `mcp_server/services/template_activation.py` | [CY066](planning-rollout.md#cy066) | CY066 |
| `tests/mcp_server/integration/test_template_activation.py` | [CY066](planning-rollout.md#cy066) | CY066 |
| `mcp_server/presenters/renewal_presenter.py` | [CY067](planning-rollout.md#cy067) | CY067 |
| `tests/mcp_server/integration/test_renewal_cli.py` | [CY067](planning-rollout.md#cy067) | CY067 |
| `mcp_server/cli_renewal.py` | [CY067](planning-rollout.md#cy067) | CY067, CY071 |
| `docs/development/issue460/rollout-workflow-input.md` | [CY068](planning-rollout.md#cy068) | CY068 |
| `docs/development/issue460/rollout-host-input.md` | [CY069](planning-rollout.md#cy069) | CY069 |
| `docs/development/issue460/rollout-config-input.md` | [CY070](planning-rollout.md#cy070) | CY070 |
| `tests/mcp_server/integration/test_rollout_configuration.py` | [CY070](planning-rollout.md#cy070) | CY070 |
| `tests/mcp_server/fixtures/server_process.py` | [CY071](planning-rollout.md#cy071) | CY071 |
| `tests/mcp_server/integration/test_target_startup.py` | [CY071](planning-rollout.md#cy071) | CY071 |
| `docs/development/issue460/rollout-rehearsal.md` | [CY071](planning-rollout.md#cy071) | CY071 |
| `tests/mcp_server/integration/test_v3_cutover.py` | [CY072](planning-rollout.md#cy072) | CY072 |
