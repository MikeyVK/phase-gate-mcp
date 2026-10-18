<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 517 — Python 3.15 and MCP SDK 2.3 Migration Research

**Status:** Research complete for independent review; inherited strategy, no new owner policy requested  
**Version:** 0.2  
**Last Updated:** 2026-10-18

## Purpose

Bound the delivery refactor using the already approved #513 strategy, current source responsibilities and actual acceptance gaps.

## Scope In

Runtime/package/checker prerequisites; SDK integration at server, converter and proxy boundaries; directly affected tests/helpers; installation and real application/proxy verification. Inherit the controlled Python>=3.15/MCP2.3 target and coherent tested dependency snapshot from #513.

## Scope Out

No implementation in Research. No SDK1/Python3.13 production bridge, initialization-free2026 lifecycle, unrelated suppression repair (#518), new abstraction framework, release/publication or automatic upgrade of the active server environment. No legacy-dependency environments, SDK1 interoperability test matrix, legacy API preservation tests or new tests whose only purpose is to assert dependency version numbers.

## Prerequisites

- Read the final Research Outcome and Approved Strategy of #513; historical provisional proposals are not new decisions.
- Apply ARCHITECTURE_PRINCIPLES.md, DOCUMENTATION_STANDARD.md and TYPE_CHECKING_PLAYBOOK.md at the affected boundaries.

## Problem Statement

Research #513 establishes a feasible, approved Python>=3.15/MCP SDK2.3 direction, but the application still registers SDK1 decorators and returns SDK1 handler shapes. Metadata/checker/adapter prerequisites select the previous stack. The delivery must replace those integration contracts together and prove the installed pgmcp application, not merely import packages or replay a minimal SDK server.

## Goals

- Preserve application behavior, typed transport/covariance, wire aliases, resource identity and initialized protocol operation while changing the SDK API.
- Identify the smallest existing production seams, direct consumers and shared test coupling; do not spread SDK adaptation through business layers.
- Make package/native prerequisite selection coherent and verified without bypassing version guards or changing the active environment automatically.
- Assign concrete installation/application/proxy evidence to delivery and keep unrelated suppression remediation in dependent #518.

## Background

Issue #513 is merged through PR #516 (main commit4a302d773a9bad2760a53429b12b678b89049c94). Its final research and inventory are inherited inputs, not work to repeat. Coordination initialized refactor/517-migrate-python315-mcp-sdk23 with explicit parent main; the branch is in Research. Initial untracked state.json/deliverables.json are expected lifecycle artifacts. #518 is blocked on this migration's completion and acceptance.

## Findings

### Existing responsibilities and coupling

| Boundary | Current responsibility and observed coupling | Refactor scope / invariant |
| --- | --- | --- |
| [Package metadata](../../../pyproject.toml), [runtime requirements](../../../requirements.txt), [dev requirements](../../../requirements-dev.txt) | Python>=3.13; mcp>=1.30.0,<2; pydantic-settings2.13.1; other direct/dev requirements use broad lower bounds. Requirement files are additional installation consumers. | Align declared/provisioned runtime and checker dependencies to the controlled #513 snapshot. Do not mistake pip resolving an arbitrary newer package for target verification; avoid a new build/lock framework. Exact packaging form is Design work. |
| Native checker config | pyproject Mypy/Ruff target3.13/py313 and [Pyright](../../../pyrightconfig.json) pythonVersion3.13. Existing suppression policy remains. | Change language/prerequisite baseline, not unrelated diagnostic policy. Only migration-obsolete exceptions may be removed here. |
| [Bundled adapter prerequisites](../../../mcp_server/bundled_adapters) | Mypy1.19.1, Ruff0.15.6, Pyright1.1.408; Pytest's5 exact pins select the former set. check_jsonschema also pins jsonschema4.25.1, while the approved candidate has4.26.0. | Include all affected exact requirements in dependency consistency, not only the4 adapter copies used in #513. Preserve native guards. Pin alignment is part of this issue; proof of compatibility remains delivery work. No automatic upgrade of unrelated Node/commitlint/Lychee/TypeScript tools. |
| [Catalog/bootstrap](../../../mcp_server/bootstrap.py#L462) | AdapterLaunch stores the resolved executable; bootstrap resolves program names using shutil.which. Installed Python metadata and an adapter process's actual Python can differ through PATH. | Prove actual executable/package identity during acceptance. Existing explicit resolver seams suffice for isolated evidence; do not introduce interpreter selection architecture or silently alter the host launcher. |
| [Server](../../../mcp_server/server.py#L58) | Owns SDK Server,4 nested decorator handlers, resource/tool enumeration, normalized pipeline dispatch, cache publication/presentation and stdio serving. | Replace SDK registration/result/context contracts here. Managers, core tools and presenters retain their application contracts. Preserve input admission/output schema, cache/attachments and cancellation propagation. |
| [Converters](../../../mcp_server/utils/mcp_converters.py#L28) | Converts application text/JSON/image/resource content to SDK content/result models with current Python keyword spellings. | Adapt SDK Python constructors/attributes without changing wire names, content text, attachment URI/MIME, isError semantics or adding a generic conversion framework. |
| [Proxy](../../../mcp_server/core/proxy.py#L339) | Owns child generations, pending IDs, initialize capture/replay, protocol consistency and cleanup. Only direct SDK model is InitializeResult;3 protocolVersion accesses remain. Child launch uses the proxy's sys.executable. | Replace the SDK attribute at this owner. Preserve initialized2025-11-25 behavior and existing supervision; no initialization-free lifecycle/proxy redesign. |
| [Resource read](../../../mcp_server/server.py#L96) | SDK1 ReadResourceContents returns text/plain; resource listing uses each resource's declared mime_type. Existing startup test explicitly asserts delivered text/plain. Embedded schema attachments separately use application/schema+json. | Preserve actual observable values in this migration, including URI/content and these distinct MIME paths. Do not silently turn the differing listing/read MIME behavior into an incidental fix. |
| [Build procedure](../../../scripts/build_package.py) | Builds manifest-defined package assets and invokes the package builder; version comes from installed distribution metadata. | Use existing build/asset ownership to prove an actual installed wheel. No release_manifest redesign, package publication/version-policy change or editable-checkout-only acceptance. |
| [Setup reference](../../setup/README.md), [developer isolation](../../setup/dev-isolation.md) | Active docs explicitly state3.13/SDK1 and distinguish installed package, source workspace and neutral CWD. | Update invalidated baseline/install examples in Documentation. Preserve workspace/credential/launcher ownership. No new phase contracts/agent instructions/templates are needed for SDK method spelling. |

### Source and test impact

A fresh AST/source scan confirms exactly3 active production files import mcp directly: server.py, core/proxy.py and utils/mcp_converters.py. Seventeen test files import SDK types directly. Twelve access request_handlers at38 source positions. These are the same structural boundaries reported in #513, now checked against the issue baseline.

| Registry-coupled existing test file | References |
| --- | --- |
| integration/test_cache_fidelity_v3.py |157 |
| integration/test_execution_presentation_v3.py |145,157,211 |
| integration/test_pipeline_e2e.py |152,215,267 |
| integration/test_project_plan_readback.py |134,151,327,346 |
| integration/test_scaffold_public_v3.py |161 |
| integration/test_schema_public_v3.py |115,127,273 |
| integration/test_tool_attachment_transport.py |120,151 |
| unit/test_server.py |271,338,398,462,518,595,648,783 |
| unit/decorators/test_pipeline_decorators.py |355,370 |
| unit/server/test_validate_tool_arguments.py |119,141,179,210,233 |
| unit/tools/test_cycle_tools.py |236,299,418,484 |
| integration/mcp_server/test_server_startup.py |38,54 |

Paths in this table are relative to tests/mcp_server. Other direct SDK consumers are integration/test_checks_public_v3.py, test_edit_public_v3.py, test_fixes_public_v3.py, test_tests_public_v3.py and unit/server/test_tool_result_conversion.py. Inspect them for constructor/attribute changes even without registry access.

The existing [shared helpers](../../../tests/mcp_server/test_support.py#L459) make_test_server, make_dispatch_dependencies and make_dispatch_server are the bounded test composition seam. Preserve valuable admission, enforcement, cache, attachment, schema and project readback scenarios. Replace access to removed SDK internals through a supported SDK/application boundary; never recreate request_handlers in pgmcp or a test compatibility facade. Do not rewrite unrelated fixtures or test content.

### Preserved behavior and acceptance gaps

| Surface | Existing evidence | Delivery evidence still needed |
| --- | --- | --- |
| SDK API/versions/variance | #513 isolated SDK2.3/Python3.15 environment, paired type/runtime controls and92 unchanged existing tests. Candidate package metadata remains present on disk; no new installation was made here. | Actual migrated source under selected dependencies; required native-configured gates in their owning phase. This is not a demand to repeat the old version matrix. |
| Application startup/listing | [stdio startup test](../../../tests/mcp_server/integration/test_tool_attachment_transport.py#L157) launches actual source and lists tools; other tests exercise resource/tool dispatch through the removed registry. | Installed pgmcp in a clean environment, neutral CWD and explicit isolated workspace: initialize/list tools/list resources/call/read/errors, schema/attachments/cache fidelity and diagnostic/degraded startup. Separate process/package identity from an editable/source import. |
| Protocol/harness | #513 actual proxy/minimal candidate child, SDK1 client/SDK2 server and initialized negotiation/restart probes. | Real migrated pgmcp/proxy using the selected SDK2 stack and the preserved initialized protocol route. The owner excludes a legacy SDK/dependency compatibility matrix and separate SDK1-client test environments; the older #513 probes remain historical research evidence, not required delivery tests. |
| Proxy lifecycle | [Current6 proxy tests](../../../tests/mcp_server/core/test_proxy.py) mainly inspect/assign attributes or assert constants; they do not exercise replacement, cancellation/deadline or child cleanup. | Adapt/replace low-value cases with compact public behavior coverage in the existing surface: restart success, failed replacement, in-flight outcome, cancellation/deadline and cleanup. Use real controlled child processes where the behavior requires them, with bounded cleanup. No permanent duplicate research-probe suite. |
| Native prerequisite consistency | #513's4 upgraded adapter lab copies proved selected check/test paths, not installation of every configured bundled tool. | Reconcile the check_jsonschema jsonschema pin and relevant other exact prerequisites; verify actual selected executables and complete pip consistency. If an external pin cannot support the target, report the exact conflict instead of disabling guards or upgrading unrelated tooling. |
| Installed package | #513 proved the dependency set and supported PyYAML pure-Python route, not a migrated pgmcp wheel. | Build using the existing asset procedure; install the real artifact, pip check and probe the installed server/proxy. Set PYYAML_FORCE_LIBYAML=0 only in the intended isolated install process as needed; no C-loader application rewrite or performance claim. |

### Candidate seams and alternatives

Native SDK2 constructor handlers and typed result models provide the existing integration seam; the installed candidate source exposes on_list_tools/on_call_tool/on_list_resources/on_read_resource and a stream-based Server.run that natively serves initialized sessions. Their exact contracts belong in Design, not new production layers in Research.

| Alternative | Cost / consumer effect | Strategy |
| --- | --- | --- |
| Clean replacement at existing integration owners |3 direct production SDK modules plus baseline declarations/prerequisites and direct tests. Existing domain contracts can stay stable. | Inherited and approved; verify application behavior rather than emulate removed internals. |
| SDK1 bridge or fake handler registry |Carries2 APIs, obscures actual SDK acceptance and preserves the test coupling being removed. | Excluded by owner. |
| Upgrade plus initialization-free proxy rewrite |Changes supervision/session semantics in addition to dependencies; introduces independent acceptance questions. | Separate scope, not #517. |
| Simultaneous broad suppression repair |Confounds dependency changes with unrelated input/logging/type policy and inflates consumers. | #518 after completion/acceptance of #517. |

### Installation and active-environment boundary

The inherited strategy permits isolated development/acceptance and explicitly excludes automatic active-environment upgrades. Read metadata/source in the existing #513 lab as evidence inputs; do not make that mutable ignored environment the only reproducible deployment record. Delivery needs a clean installed artifact and recorded exact versions. Native Python resolves through PATH, while the proxy child follows sys.executable, so both must be checked.

Changing/repointing the active host runtime and restarting its client is an explicit owner action/approval later. It is not authorized by starting #517, and is not necessary to close this source Research. Design/Planning must identify the safe activation boundary before it is needed for workflow-owned configured verification. No credential files or host launcher configuration were changed or printed here.

### Explicit owner clarification: clean break and tests

The owner confirmed a clean break on2026-10-18 and rejected legacy tests or additional tests whose purpose is to guard dependency versions. Preserve meaningful application/protocol behavior through the selected new SDK; do not preserve old SDK Python APIs or package combinations. Adapt valuable existing tests, remove obsolete ones and add only focused behavior coverage for an actual acceptance gap.

Exact dependency/prerequisite declarations and existing runtime version guards remain part of the approved operational contract. Recording the installed environment and running pip consistency checks are installation acceptance evidence, not a new permanent version-assertion suite. This decision does not authorize disabling guards or unrelated removal of existing guard-behavior tests. #518 retains the remaining suppression-repair scope.

## Approved Strategy

Inherited from the owner-approved #513 outcome and published #517 scope, with the owner's explicit test-scope clarification on2026-10-18. That clarification supersedes the earlier old/new dependency-client verification wording: only the selected target stack is a delivery test target.

| Boundary | Approved strategy |
| --- | --- |
| Python/SDK/dependencies |Python>=3.15, SDK2.3 and the coherent investigated snapshot; align package/checker/exact adapter prerequisites together. Material target drift or contradiction reopens the owner decision. No floating-latest acceptance or guard bypass. |
| SDK ownership |Clean replacement in server/converter/proxy integration; preserve tool/domain/presenter/resource interfaces and wire behavior. No SDK1 production bridge or new architecture. |
| Initialized protocol |Preserve2025-11-25 with native SDK2 support and prove that behavior on the selected stack. Initialization-free2026/proxy simplification and maintained SDK1-client/dependency compatibility tests are excluded. |
| Installation |Supported Windows pure-Python PyYAML route; actual clean pgmcp package install and pip consistency. No release/deployment or automatic active environment replacement. |
| Type contracts |Keep explicit covariance, intentional variance and useful runtime guards. Remove only demonstrably migration-obsolete exceptions such as AdapterBinding misc and applicable SDK handler codes. All remaining repair belongs to #518. |
| Consumers/tests |Adapt valuable direct/shared consumers to behavior on the chosen new stack. Remove or replace obsolete SDK1 API tests instead of preserving them through facades. No legacy test paths, old dependency environments, compatibility matrix, new dependency-version-only assertions or suite-wide rewrite. Add focused tests only for meaningful behavior/acceptance gaps; reuse fresh evidence and run required full suite/gates in the owning phase. |
| Workflow/config/docs |Normal refactor phases with independent QA. Preserve enforcement and effective workspace config. Update only baseline/prerequisite/setup docs invalidated by the delivered migration; historical #513 remains evidence. |
| Activation |Keep current server/client operational during isolated research. Actual active-runtime installation/host switch requires an explicit later owner decision before execution. No hidden automatic restart/launcher edit. |

## Expected Results

Research supplies a bounded structural and preservation basis for Design, not a migrated application. Delivery succeeds only when the actual installed pgmcp artifact, initialized protocol operations and proxy failure/lifecycle behavior work under the controlled target with required quality/full-suite evidence. Direct tests are adapted proportionally and unrelated suppression work remains in #518. There is no new owner policy request from current source findings; exact handler/test/packaging and activation arrangements are Design/Planning questions within these boundaries.

## Evidence

### Inherited decision and executed compatibility evidence

#513 final Research Outcome/Approved Strategy and coherent version matrix are authoritative. Its92 candidate tests and isolated protocol/type probes are reused research inputs, not #517 acceptance.

- [Final #513 research](<../issue513/research.md>)
- [Suppression dispositions](<../issue513/suppression-inventory.md>)

### Current source consumer inventory

Read-only AST traversal of active mcp_server and tests/mcp_server Python, excluding assets/cache/invalid fixtures, found3 production SDK import owners,17 direct test consumers and38 request_handlers references across12 files. Tables above preserve the exact relative files/lines. Source inspection also established the jsonschema pin conflict and proxy coverage gap.

- [Server owner](<../../../mcp_server/server.py>)
- [Shared test helpers](<../../../tests/mcp_server/test_support.py>)
- [Proxy tests](<../../../tests/mcp_server/core/test_proxy.py>)
- [Native JSON/YAML prerequisite](<../../../mcp_server/bundled_adapters/check_jsonschema/requirements.txt>)

**Invocation:** Host-native repository search plus Python AST/read-only analysis of imports whose module is exactly mcp or starts mcp.; request_handlers source references; selected package/prerequisite/helper/SDK source reads.

**Observed Result:** No production, runtime, dependency or native-configuration change and no new runtime/test matrix. scaffold_artifact(artifact_type="research", file_name="research.md", target_path="docs/development/issue517", context=<authored Research context>) returned validation=passed for the configured markdown_links check; this is document validation, not migration acceptance.

## Risks

### Same interpreter does not prove matching native adapter prerequisites

Check resolved PATH programs, process Python and actual package metadata; align exact declared pins including JSON/YAML tooling and run actual gates. Retain existing version guards.

**Consequence:** A healthy bootstrap can coexist with a native prerequisite rejection.

### Registry-coupled tests can tempt a compatibility facade

Use supported SDK/application behavior through existing composition/transport seams. Preserve the scenario and remove coupling rather than recreate removed SDK data structures.

**Consequence:** A recreated registry would hide incomplete migration and preserve maintenance cost.

### Installed wheel acceptance can accidentally import source

Use neutral CWD, explicit isolated workspace and record executable/package module identity for both server and proxy. Follow existing asset build ownership.

**Consequence:** Passing source tests would not establish installability or deployed package behavior.

### Research proxy controls can be mistaken for actual migrated lifecycle proof

Keep #513 evidence labeled and require actual application success/failure/cancellation/cleanup evidence under #517. Replace shallow proxy tests proportionally.

**Consequence:** Restart or shutdown faults can escape a successful startup/listing test.

## Related Documents

- [Issue #517](<https://github.com/MikeyVK/phase-gate-mcp/issues/517>)
- [Blocked suppression follow-up #518](<https://github.com/MikeyVK/phase-gate-mcp/issues/518>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Developer isolation](<../../setup/dev-isolation.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp researcher | Map current SDK/dependency/test boundaries against inherited #513 decisions and identify delivery acceptance gaps without repeating compatibility research. |
| 0.2 | 2026-10-18 | @imp researcher | Record explicit clean-break/target-only behavior-test policy; remove old/new dependency-client matrix as a delivery requirement while preserving native guards and installation acceptance. |
