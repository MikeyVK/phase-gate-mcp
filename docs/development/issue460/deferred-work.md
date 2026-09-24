<!-- docs/development/issue460/deferred-work.md -->
<!-- template=generic_doc version=43c84181 created=2026-08-24 updated=2026-08-24 -->
# Issue 460 Deferred Work

**Status:** APPROVED — F-20 EXECUTION ADAPTER SCOPE IS NOT DEFERRED  
**Version:** 1.15  
**Last Updated:** 2026-09-07  
**Originating Issue:** 460

## Purpose

Preserve all work explicitly deferred from issue 460 in one durable, non-authoritative follow-up notice. This document keeps deferred evidence and ownership visible without enlarging the primary Research artifact or authorizing implementation.

## Status and Authority

The five original deferrals below remain closed issue-460 Research decisions. Their inventories and any ordering recommendations are inputs to future Research, not future Design or implementation authorization. `APPROVED` confirms their exclusion and ownership; it does not authorize the deferred work or reject its possible future value. The 2026-08-31 component-level renewal deferral was explicitly superseded by the human-directed F-10/S-10 amendment on 2026-09-03 and is no longer deferred work.

The 2026-09-04 F-20 language-agnostic adapter extension suite is also explicitly retained inside issue 460. Check, test, and fix extensibility cannot be deferred without producing incompatible language-specific product paths. This does not authorize unlimited future roles: a new tool or language within the three approved contracts is extension work; a genuinely new product role still requires its own evidenced consumer and contract decision.

The Generic Python class responsibility is approved in [Research](research.md) as a bounded body-free plain-class skeleton. That artifact-local boundary does not decide method-content policy for specialized Python templates.

| Deferred boundary | Issue-460 consequence | Future owner |
|---|---|---|
| S1mpleTrader-local specialization | Remove consumer-specific behavior from the portable PGMCP suite; perform no cross-repository edits | A later S1mpleTrader repository-local issue |
| Complete YAML artifact subset | Remove two incomplete unreachable seeds now; do not restore them piecemeal | A future PGMCP issue |
| Portable Python artifact coverage | Add no new Python artifact types in issue 460 | A future PGMCP issue with fresh consumer validation |
| Purpose-aware runtime artifact discovery | Add no new MCP tool or overloaded introspection mode in issue 460; use the approved 50-template design threshold below to trigger the separate follow-up | A future PGMCP feature issue |
| Command/query service artifact family | Remove broad Service and hidden subtype routing; add no replacement in issue 460 | A future PGMCP issue after concrete consumer validation |
| Agent-facing startup health and recovery | Retain configuration-based input contracts and on-use dependency failures; add no startup adapter probes, health-check changes, health-first policy, or health-driven tool blockade | A separate future PGMCP issue; Design-stage exclusion dated 2026-09-05, retained-scope correction 2026-09-07 |
| Removal of safe-edit `verify_only` | **No longer deferred** — human scope expansion brings retirement into issue 460 together with validation-policy alignment | DI-04; narrow Research amendment dated 2026-09-07, independent QA requested |

## Deferred Work Notice: Safe-Edit Verify-Only Removal

**Status: SUPERSEDED.** The initial deferral on 2026-09-07 was withdrawn later in the
same workshop by explicit human scope expansion. The owner rejected retaining a
temporary policy boundary only for functionality already nominated for removal.

The [narrow Research amendment](research.md#narrow-safe-edit-policy-amendment--2026-09-07)
now owns validation=enforce/report alignment, retirement of mode/verify_only and rejection
of aliases or replacement dry-run APIs. DI-04 owns this work in issue 460. Independent
QA is requested on the delta. No separate removal issue is required by this notice.

The mode already exists in [SafeEditInput and execution](../../../mcp_server/tools/safe_edit_tool.py):
it validates proposed content without writing the target. The
[unit test](../../../tests/mcp_server/unit/tools/test_safe_edit_tool.py) checks that no
writer call occurs, and the [public reference](../../reference/tools/editing.md) exposes
the mode. Repository inspection found implementation, tests and documentation, but no
concrete non-test invocation in the inspected source/configuration/instruction roots.
This is not telemetry and does not establish that external agents never use it.

The earlier preserve/no-further-design instructions are historical and no longer bind
the changed policy boundary. Removal is explicit loss of proposed-edit preview, not
an inference that the mode was unused. All unrelated deferrals and frozen scope remain.

## Deferred Work Notice: Server and Subprocess Security Isolation

**Decision:** explicitly deferred by the human owner during Design on 2026-09-06.  
**Future owner:** a separate PGMCP security issue, not yet created.  
**Suggested issue title:** Define and enforce security isolation for the PGMCP server and tool subprocesses.

### Limited Current Evidence

The user wants a security boundary for the complete server and its tools. This brief
source inspection is not a security audit or an assessment of actual host/container
permissions. No credentials or environment values were inspected and no escape attempt
was performed. Virtual environments, cwd selection and temporary directories are not
OS security boundaries; admitted code is not necessarily technically confined.

| Source | Observed behavior | Consequence / uncertainty |
|---|---|---|
| [ServerProxy](../../../mcp_server/core/proxy.py), `_spawn_server_in_context` | Ordinary subprocess.Popen; startup copies the environment | The inspected launcher establishes no OS filesystem/network sandbox; an external deployment could still impose one |
| [QAManager](../../../mcp_server/managers/qa_manager.py), gate subprocess invocation | subprocess.run with timeout, output capture and cwd, no restricted environment argument at this call | Lifecycle controls are not access restrictions; host permissions and inherited environment require review |
| [PytestRunner](../../../mcp_server/managers/pytest_runner.py), `_execute` | Copies os.environ and adjusts virtual-environment/PATH settings | Dependency isolation is not security isolation; actual credential exposure was not investigated |
| [FilesystemAdapter](../../../mcp_server/adapters/filesystem.py), `resolve_path` | Resolves paths, then compares string startswith against the root | Only protects calls routed through this adapter; lexical prefixes do not prove path-component containment, including sibling names sharing a prefix. Prioritize focused correctness evidence; no public exploit path was exercised |

Absolute paths identify locations, not permissions. Relative paths cannot prevent a
process from constructing other paths. Actual access depends on host permissions and
enforced policies, not the representation sent to an adapter.

### Future Issue Scope and Evidence

- Define the threat model for server, admitted adapters, external tools, workspace/test
  code and executable plugins/configuration; distinguish trusted-but-buggy integrations
  from untrusted execution without promising support for the latter.
- Inventory required filesystem, child-process, environment/credential and network
  access, including Git/GitHub, installed toolchains and authorized workspace mutations.
- Evaluate whole-server isolation separately from per-role subprocess restrictions:
  a workspace writable by the server does not make a check process read-only.
- Select supported-platform enforcement/deployment and native-path mappings, with
  explicit portability, cost and unavailable-enforcement behavior. No sandbox or
  container technology is selected by this notice.
- Review component-aware containment, symlink/junction behavior and environment
  inheritance. Route immediate correctness defects separately if warranted.
- Prove both allowed workflows and denied reads/writes/network access, including
  descendants and check-versus-fix authority. Document limits; no silent weakening.

### Issue-460 Boundary and Interim Promise

No sandbox implementation, security manifest DSL, container packaging, credential
broker, platform matrix or security monitoring is added to issue 460. Frozen Research
and the approved consumer catalog remain unchanged. This future work does not block
continuing Design under the human-approved deferral.

Issue 460 retains application-level package trust/admission, path validation, bounded
mutation, role responsibilities and controlled temporary-file ownership. Read-only
checks are an integration contract, not a claim of OS-enforced confinement. No safe
execution of untrusted adapters is promised. Public workspace-relative presentation
remains separate from internal paths and enforcement. Exact adapter input fields
remain Design work; this notice does not approve an absolute-host-path-only protocol.
Residual validation-file maintenance stays manual; no temp monitoring or sweeping.

## Deferred Work Notice: Agent-Facing Startup Health and Recovery

**Decision:** explicitly deferred by the human owner during Design on 2026-09-05.  
**Future owner:** a separate PGMCP issue, not yet created.  
**Suggested issue title:** Agent-facing startup health, diagnostics, and recovery guidance.

The preferred future presentation route for startup availability problems is
`health_check`, not diagnostic prose embedded in tool input schemas. This direction
does not authorize health implementation inside issue 460. The work has its own
consumer, policy, presentation, and failure-recovery boundaries and must not enlarge
the already expanded adapter refactor. The future issue is **not a prerequisite for
issue-460 completion or public V3 cutover**.

**Retained-scope correction (2026-09-07):** the human owner removed startup adapter
dependency preflight and availability-based schema filtering. The health deferral
remains; it must not implicitly retain that superseded execution obligation. A future
issue must establish its own diagnostic evidence sources rather than assume that
issue 460 produces adapter-readiness facts or an availability report.

### Retained in Issue 460

- A coherent startup-bound contract view based on validated declarations and references,
  without invoking adapters or native tools to check dependency availability.
- Complete input contracts for check/test/fix consumers, exposing valid configured
  selections, with matching invocation validation and consistent lazy exposure.
- Full profile obligations: no silent removal of missing checks or weaker fallback.
- Explicit consumer-specific defaults and no-configured-choice behavior. These
  remain Design work in issue 460, not an excuse for a general health-based blockade.
- Existing scaffold `report` semantics and ordinary per-call invalid-input or
  runtime `unavailable` outcomes, including absent dependencies on first use or later
  dependency loss; inability to start the adapter remains a generic invocation failure.
- Existing operation-result presentation, structured evidence, and cache/attachment
  responsibilities under issues 456/459. Deferring startup diagnostics does not
  suppress relevant operation failures.

Input schemas describe inputs, constraints, defaults, and valid configured choices only.
They do not explain omitted dependencies or carry startup diagnoses. Moving that
diagnosis into dynamic tool descriptions is not an alternative within issue 460.

### Excluded from Issue 460

- Changes to `health_check` logic, output contracts, or presentation to report
  startup availability, health aggregation, or a new degraded status.
- New health-driven tool filtering/blockades, a health-only mode, or an obligation
  to call `health_check` before other calls are admitted.
- Health-first instructions in `AGENTS.md` or changed `restart_server` guidance.
- New agent-facing startup reports, diagnostic log/resource exposure, or recovery
  recommendations. No startup diagnostic store or speculative health DTO is required.

Existing health/admin behavior and the existing emergency server fallback are
preserved; this exclusion introduces no new policy for them. Frozen Research and
the approved 126/151 consumer/test catalog remain unchanged.

### Follow-Up Research and Evidence

The future issue must establish its evidence sources, the exact healthy/degraded/unhealthy meanings,
agent-visible summary and detail route, recovery guidance, and whether any tool
blocking is justified. It must assess startup instructions and restart verification
together, and prove behavior with lazy discovery and direct tool calls. Diagnostic
availability when normal configuration, presentation, or cache initialization fails
needs its own evidence; do not promise a report URI before it exists.

Read the existing [health tool](../../../mcp_server/tools/health_tools.py),
[server fallback](../../../mcp_server/server.py),
[admin tools](../../../mcp_server/tools/admin_tools.py), and
[agent protocol](../../../AGENTS.md) as current behavior, not as permission to modify
them. The issue-460 [adapter Design](design-execution-adapters.md#77-configuration-based-exposure-and-on-use-availability)
owns the retained configuration/on-use-availability boundary. This notice is follow-up
input, not approval of a future health schema or implementation plan.

---

## S1mpleTrader-Local Template Specialization

Portable PGMCP code templates must remove unconditional logging, translator, Backend-layer, and other S1mpleTrader-specific boilerplate. Those details are not valueless: they are precisely what can make a workspace-owned suite substantially more productive than the portable baseline.

The later S1mpleTrader repository-local migration issue must therefore treat the six preserved patterns and the adapter/service boilerplate as one deliberate specialization set. It must assess and, where still valid, recompose project logging, LogEnricher, Translator, lifecycle, dependency, error, and typed-ID conventions on top of the new PGMCP extension contract. In particular, removing unconditional logging/translation behavior from the package adapter is not a decision to discard it from S1mpleTrader. The distinction is ownership: generic behavior in PGMCP, project conventions in S1mpleTrader.

Issue 460 records this preservation obligation but does not design or implement the S1mpleTrader-local successor suite.

## Complete YAML Artifact Package Subset

The unreachable `tier1_base_config.jinja2` and `tier2_base_yaml.jinja2` files are incomplete seeds, not supported behavior. They have no public artifact registration, concrete renderer, complete schema, output-profile contract, or behavioral consumer. Issue 460 removes them from the official suite instead of carrying an unreachable partial tier.

A future PGMCP Research phase should evaluate a complete YAML configuration artifact subset instead of restoring the two files verbatim. The following are inherited constraints and Design hypotheses to evaluate, not selected Design or Planning:

- a public YAML/config artifact registration and complete portable context contract;
- tier-one config, tier-two YAML, and concrete renderer responsibilities;
- bounded acyclic structured entries and sections rather than an unrestricted recursive YAML DSL;
- strict-by-default YAML output-profile validation;
- startup discovery, complete graph identity, and `scaffold_schema` exposure without artifact-specific Python registration;
- minimal and property-complete rendering whose parsed YAML data proves semantic behavior without full-text snapshots;
- a temporary complete active-root fixture that proves a new artifact can be added through suite files alone;
- packaging, documentation, and extension-boundary evidence.

The current files remain recoverable through Git history and this durable specification; keeping dead package files is not required to preserve the idea.

**Issue-460 Git recovery trace (Research F-14/F-14A/F-14B, deferred YAML disposition):** Both files were incomplete, unregistered seeds removed in CY103. Recover their final source from pre-removal commit `4ba22137757400d975d7ab8178c508f58999fb67`; removal commit: `d6602c5e92b8bbe235d9f453747a0ec8e6b62a4d`.

| Exact historical source path | Pre-removal Windows working-tree SHA-256 (CRLF bytes) |
|---|---|
| `.pgmcp/templates/tier1_base_config.jinja2` | `B624150DB5499F7C37CC8F60E82AB1D9AB45685B5F3FE89F9306EB0DB8C8BC21` |
| `.pgmcp/templates/tier2_base_yaml.jinja2` | `5CD78E1F28C5985FBBB007CC8C54FB47AB7D0D99353D0155F5A04906811CF87F` |

**Deferred Strategy (human-approved 2026-08-23):** remove both incomplete files in issue 460. Hand the complete YAML artifact package subset to coordination as the explicitly recommended first follow-up PGMCP issue on its own branch.

---

## Purpose-Aware Runtime Artifact Discovery

Current scaffold tool schemas enumerate the artifact IDs resolved from the active registry, while `scaffold_schema` exposes one selected artifact's context contract. Neither surface currently lists each available ID together with its purpose before selection. This is a real usability gap, but issue 460 does not need a new runtime discovery capability to correct schema-template rendering contracts.

Issue-460 Research classified F-18 as a feature request and compared three future directions:

| Future option | Benefit | Cost, risk, and consumer impact |
|---|---|---|
| New harness-agnostic discovery tool | Clear list-first workflow and a focused ID-to-purpose response | Adds a public MCP capability, input/output DTOs, cache/presentation behavior, tests, documentation, and another tool for clients to discover |
| Extend an existing introspection surface | Reuses an existing capability and avoids a new tool name | Overloads an artifact-specific contract query with catalog behavior and changes its input/output semantics |
| Improve existing/static discovery without runtime expansion | Lowest runtime and migration cost | Retains dependence on instructions or documentation and does not fully eliminate catalog drift risk |

F-16 remains in issue 460 because it preserves an existing suite-owned purpose description through selected-artifact introspection. It does not by itself create pre-selection catalog discovery.

**Deferred Strategy (human-approved 2026-08-24):** introduce no new discovery tool or overloaded introspection mode in issue 460. A future feature issue must revalidate the consumer need and compare all three options; the previously proposed single MCP tool is retained only as a non-binding hypothesis.

### Design Escalation Threshold — 50 Template IDs

**Human-approved Design guardrail (2026-09-07):** use 50 distinct loaded concrete
template IDs as the pragmatic threshold for enum-only discovery. This is a product
design decision, not a measured model limit, protocol limit, or maximum suite size.
Shared support files and repetitions of the same catalog in several tool schemas do
not count as additional templates.

| Situation | Design consequence |
|---|---|
| Up to and including 50 loaded template IDs | Retain complete catalog-derived enums as the simple ID-discovery route; this is not a blanket client-compatibility guarantee |
| Concrete need for more than 50 loaded template IDs | Take up the separate F-18 discovery issue before treating the large-catalog agent experience as complete |
| Earlier evidence of schema-size, exposure or selection problems | Bring the follow-up forward; ID length, repeated schema content and host/model behavior also matter |

No runtime cap, counter-driven warning, configuration field, startup rejection, enum
truncation or automatic switch of schema/tool behavior is introduced. Template 51 and
later must never disappear from a still-enum-based contract. A 300-template workspace
does not become invalid because of this guardrail. Dependency absence does not reduce
the catalog count or its exposed choices. Issue 460 retains its existing boundary;
the threshold is not an unconditional new V3-cutover gate or authorization to implement
discovery in this issue.

The inspected [MCP tool specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
and [JSON Schema enum definition](https://json-schema.org/draft/2020-12/json-schema-validation#section-6.1.2)
give no fixed enum-count maximum; the inspected MCP tool definition also gives no
fixed schema-byte ceiling. This does not establish a universal client/provider limit
or prove usable model selection at any particular count. Lazy tool exposure does not
shrink the enum when the containing tool schema is eventually exposed.

The preferred follow-up direction must address discovery and invocation together:
bounded search/browsing results with manifest-owned purpose descriptions, compact
template-ID inputs without a full-catalog enum, and exact server-side membership
validation against the same loaded catalog. Merely adding a discovery tool beside
unchanged full enums would retain their size cost. Exact tool names, query/pagination
contracts, transitions, supported-client evidence and presentation remain decisions
for the separate issue; no new catalog or duplicate template registration is implied.

---

## Portable Python Template-Suite Coverage

### Source Context

Issue 460 found that eleven current public artifact IDs resolve exclusively to Python templates: `adapter`, `dto`, `generic`, `integration_test`, `interface`, `resource`, `schema`, `service`, `tool`, `unit_test`, and `worker`. The approved F-17 strategy will give language- or technology-specific contracts explicit identities. The approved Generic responsibility remains a bounded body-free plain-class skeleton and may not absorb the deferred artifact responsibilities.

Registration demonstrates that a responsibility is represented; it does not imply that the current schema and renderer are already coherent. The [issue-460 Research](research.md) and [template-suite catalog](template-suite-catalog.md) remain authoritative for the active semantic audit and individual dispositions.

### Current Registered Python Coverage

| Responsibility family | Current artifact types | Coverage represented by the registration |
|---|---|---|
| Plain class | `generic` | One deliberately selected, bounded Python class skeleton |
| Runtime-validated data | `dto`, `schema` | Pydantic DTO and configuration/schema models |
| Behavioral contract | `interface` | A Python `typing.Protocol` contract |
| Named component roles | `adapter`, `service`, `worker` | Package-selected architectural component responsibilities |
| MCP integration | `tool`, `resource` | Python implementations of MCP concepts |
| Tests | `unit_test`, `integration_test` | Pytest-oriented test modules |

The suite is therefore comparatively strong in Pydantic, MCP, pytest, and named class-oriented architecture roles. It offers few first-class choices for ordinary Python constructs outside those areas.

### Evidence-Backed Candidate Gaps

The gaps are not merely hypothetical language features. Current PGMCP production or test code already contains:

- top-level procedural functions in [cli.py](../../../mcp_server/cli.py), [error_handling.py](../../../mcp_server/core/error_handling.py), and [version_hash.py](../../../mcp_server/scaffolding/version_hash.py);
- standard-library dataclasses in [bootstrap.py](../../../mcp_server/bootstrap.py) and [scaffold_result.py](../../../mcp_server/scaffolders/scaffold_result.py);
- `Enum`, `StrEnum`, and `IntEnum` types in [tool_outputs.py](../../../mcp_server/schemas/tool_outputs.py), [artifact_registry_config.py](../../../mcp_server/config/schemas/artifact_registry_config.py), and [pytest_runner.py](../../../mcp_server/managers/pytest_runner.py);
- exception hierarchies in [exceptions.py](../../../mcp_server/core/exceptions.py);
- abstract base classes in [base_scaffolder.py](../../../mcp_server/scaffolders/base_scaffolder.py) and [resources/base.py](../../../mcp_server/resources/base.py);
- `TypedDict` shapes in [phase_detection.py](../../../mcp_server/core/phase_detection.py);
- package initializers throughout the source tree;
- reusable pytest fixtures and helpers under [tests/mcp_server/fixtures](../../../tests/mcp_server/fixtures).

Their presence does not automatically justify a public artifact type. It does demonstrate that the retained plain-class template cannot represent the workspace's ordinary Python vocabulary without becoming an unbounded catch-all.

| Candidate responsibility | Distinct semantic value | Preliminary disposition |
|---|---|---|
| Procedural Python module | A file-level identity with a module docstring, structured imports, and zero or more structured top-level sync/async function signatures; functions are module members rather than separate persistence targets | Strong first-wave candidate; research whether one bounded module contract is preferable to a separate single-function artifact |
| Standard-library dataclass | A value/state carrier with dataclass-specific choices such as frozen and slots, without importing Pydantic validation or serialization semantics | Strong first-wave candidate; keep its purpose distinct from DTO and config schema |
| Enum | A closed named value set with explicit member names, values, documentation, and a deliberate `Enum`, `StrEnum`, or `IntEnum` form | Strong first-wave candidate; Python-version support and value constraints need an explicit profile |
| Exception | A documented exception type or coherent hierarchy with explicit bases and intentionally minimal initial state | Strong first-wave candidate; do not make arbitrary error payload conventions portable by default |
| Abstract base class | Runtime inheritance and abstract-method enforcement, which differ materially from structural `Protocol` typing | Conditional candidate; require a consumer that needs runtime inheritance rather than expanding the interface artifact |
| Static structural data contract | `TypedDict`, `NamedTuple`, `TypeAlias`, or `NewType` express shapes or identities without Pydantic runtime behavior | Conditional candidate; first determine whether these form one coherent responsibility or several small contracts |
| Package initializer | A package docstring and deliberate public re-exports in `__init__.py` | Conditional candidate; output-path and directory ownership may place this partly in workspace skeleton templating |
| Reusable test-support module | Shared fixtures and test helpers outside one unit or integration test file | Conditional candidate; hypothesis: if retained, use an explicit structured test contract rather than reviving the removed orphan fixture macro |
| Other Python protocols | Decorators, context managers, iterators, generators, descriptors, mixins, and similar forms can have distinct mechanics | Inventory-only; normal editing or the bounded class/module artifacts are preferable until repeated consumer evidence demonstrates a stable separate contract |

This list is deliberately open to additional evidence. It is neither a complete taxonomy of Python nor a promise that every row becomes a public artifact.

### Preliminary Follow-Up Priorities

A future PGMCP issue should research portable Python language-artifact coverage as a suite-extension problem, not restore a universal source generator.

#### First Evaluation Wave

1. Procedural Python module.
2. Standard-library dataclass.
3. Enum.
4. Exception.

These candidates are common, semantically distinct, portable, and already represented in current repository code.

#### Evidence-Gated Second Wave

- Abstract base class.
- Static structural data contracts.
- Package initializer.
- Reusable test-support module.
- Additional constructs discovered through supported consumer workspaces.

The future Research phase may split, merge, reprioritize, or reject candidates when concrete consumer evidence warrants it. The wave ordering is a starting hypothesis, not an implementation plan.

### Constraints Inherited from Issue 460

For every artifact responsibility selected by future Research, the following inherited constraints and hypotheses require validation; they are not a preselected Design:

- one discoverable, language-qualified ID must have one concise purpose and one finite context contract;
- every rendered symbol name must be explicit artifact context, while the exact file name and target remain separate operation controls; no value is derived across that boundary;
- artifact descriptions and valid Python docstrings apply at the relevant module, class, member, or field boundaries;
- declarations and signatures are structured; each specialized artifact's future Research must decide independently whether any caller-supplied implementation content belongs to its finite contract;
- an empty skeleton is supported only where the empty form has legitimate scaffolding value;
- minimal and property-complete render cases prove the public contract;
- an applicable Python output-validation capability provides objective evidence where available;
- one registered renderer and one complete suite-graph/package identity own the artifact;
- optional capabilities that materially widen the contract require consumer evidence;
- first-time-right means syntactically valid and structurally coherent scaffolding that is expected to be edited, not an application-complete implementation.

Inherited issue-460 constraint: the follow-up should reject a generic Python AST, conditional mega-schema, hidden renderer routing, or fallback substitution unless new evidence explicitly reopens that boundary.

### Ownership Boundary

Architecture patterns such as repository, factory, builder, command, query, handler, controller, event consumer, or strategy are conceivable Python templates. Framework artifacts such as ORM models, API routers, CLI commands, task-queue jobs, and migrations are also conceivable. They are not automatically portable language artifacts.

Those responsibilities remain workspace or framework specializations unless multiple supported consumers demonstrate a stable package-suite purpose. A construct being implementable in Python is insufficient evidence that the portable PGMCP package must own its template.

### Deferred Strategy

**Human-approved 2026-08-24:** implement no new Python artifact types in issue 460. Preserve this non-exhaustive inventory as durable input for a future PGMCP Research phase, initially evaluating procedural modules, standard-library dataclasses, enums, and exceptions.

The approved Generic plain-class artifact may not absorb these deferred responsibilities. Its body-free contract is artifact-local and creates no blanket prohibition for specialized Python templates considered by future Research.

## Command/Query Service Artifact Family

Issue 460 confirms that the current universal `service` artifact is not a stable package contract. It renders one S1mpleTrader-derived asynchronous command implementation, while hidden engine routing names command, query, and orchestrator variants that are not publicly representable and mostly do not exist.

The current Service config, command renderer, legacy scaffolder, and hidden subtype routing are removed in issue 460. No compatibility alias or replacement artifact is retained.

Command and Query may justify explicit future templates because they can represent distinct side-effect and return-value contracts. That possibility is deferred to a dedicated issue rather than designed inside the already broad issue-460 refactor.

Future Research must establish:

- concrete repeated consumers inside supported workspaces;
- whether Command and Query are separate artifact responsibilities rather than variants behind one type;
- their side-effect, input, output, error, dependency, sync/async, and naming boundaries;
- language/framework qualification and relationship to Generic, Tool, DTO, and test artifacts;
- whether an Orchestrator responsibility has independent evidence or is merely an application-specific class role;
- which S1mpleTrader-specific logging, translation, result/error, and DI conventions belong only in that workspace.

No exact IDs, schemas, inheritance structure, or renderer topology are approved here.

## Component-Level Template-Suite Renewal — Returned to Issue 460

The 2026-08-31 decision to defer automatic component-level adoption is superseded by the human-directed F-10/S-10 amendment dated 2026-09-03. This boundary is active issue-460 Research and belongs to DI-06, not to a future issue.

The approved amendment does not create file-level merging or a package manager. It compares one current adopted checkpoint, actual, and candidate for whole components only: shared/ is one component and each manifest ID is one component. Non-conflicting candidate components may be selected; local-only and conflicting actual components are preserved. The result is built as one complete off-root suite, validated completely, and only then activated recoverably as the sole runtime root.

Explicit reconciliation may advance the current upstream checkpoint to candidate component states without overwriting locally merged actual content. For existing workspaces without a checkpoint, automatic bootstrap requires trustworthy equality evidence; otherwise actual remains byte-for-byte unchanged, candidate remains non-authoritative, and renewal returns `checkpoint_required` until the owner supplies a trusted prior suite or explicitly acknowledges the validated candidate as comparison basis. External workspaces never infer or activate a baseline automatically. The checkpoint has no history or per-file versions, and no missing-baseline path creates a retention or lookup obligation. The amendment adds no SemVer inference, compatibility matrix, automatic file merge, or provenance registry. Artifact metadata and the existing resolved-package/source-suite fingerprints remain unchanged.

The canonical decision is [F-10/S-10 in Research](research.md#approved-strategy-and-decision-status), with evidence and exact comparison rules in [Research Findings](research-findings.md#f-10--renewal-can-split-paired-assets) and Design ownership in [DI-06](design-intake-map.md#di-06--distribution-renewal-and-deployment-migration).

## Related Documentation

- [Issue 460 Research](research.md)
- [Issue 460 Research Findings](research-findings.md)
- [Issue 460 Template-Suite Catalog](template-suite-catalog.md)
- [Issue 460 Design Intake Map](design-intake-map.md)
- [Issue 460 Distribution Design](design-distribution.md)
- [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.15 | 2026-09-07 | Supersede verify_only deferral after explicit human scope expansion; route removal and full validation-policy alignment into the narrow Research amendment |
| 1.14 | 2026-09-07 | Defer verify_only removal to a separate issue; exclude further mode-specific Design from issue 460 except for evidenced conflicts introduced by its new functionality |
| 1.13 | 2026-09-07 | Record the human-approved 50-template Design escalation threshold for F-18, without runtime caps or enum truncation; require the follow-up to address discovery and compact invocation schemas together |
| 1.12 | 2026-09-07 | Align retained Design scope with no startup adapter probes and configuration-based choices; preserve health deferral without assuming future readiness evidence from issue 460 |
| 1.11 | 2026-09-06 | Record bounded source evidence and deferred server/subprocess isolation; distinguish application contracts from OS enforcement without expanding issue 460 |
| 1.10 | 2026-09-05 | Record the explicit Design-stage startup-health deferral; retain complete availability-aware check/test/fix inputs and ordinary operation outcomes without making future diagnostics a V3 prerequisite |
| 1.9 | 2026-09-04 | State explicitly that the F-20 check/test/fix adapter extension suite remains in issue 460 and is not a deferred language-feature, while future new product roles still require separate evidence and approval |
| 1.8 | 2026-09-03 | Align deferred portable-Python guidance with the corrected F-03/F-07 boundary: explicit rendered symbols, independent exact file/target operation controls, and no cross-boundary naming derivation |
| 1.7 | 2026-09-03 | Record the human-approved checkpoint-less bootstrap remediation while retaining component renewal inside issue 460 and outside deferred work |
| 1.6 | 2026-09-03 | Remove component-level suite adoption from deferred work and route the superseding F-10/S-10 three-way component renewal amendment back into issue 460 and DI-06 |
| 1.5 | 2026-08-31 | Align deferred component adoption with DI-06: selective reconciliation persists no acknowledgement or component state, and only exact complete candidate promotion updates installed-suite evidence |
| 1.4 | 2026-08-31 | Defer automatic component-level template-suite adoption without rejecting future extension; retain package-aware reporting and agent reconciliation while issue 460 mutates only complete suites |
| 1.3 | 2026-08-26 | Mark the five deferrals as closed approved Research exclusions and link their Design coverage authority without granting implementation authorization |
| 1.2 | 2026-08-24 | Defer any explicit command/query service artifact family after approving removal of the current broad Service and hidden subtype routing |
| 1.1 | 2026-08-24 | Add deferred F-18 runtime discovery, reconcile the approved Generic boundary, and remove any implied suite-wide method-body rule |
| 1.0 | 2026-08-24 | Consolidate all issue-460 deferred work and preserve the Generic Python approval boundary |

## Deferred Work Notice: Native Adapter Robustness for Large Selections

**Decision:** explicitly deferred outside issue #460 by the human owner during Validation on 2026-09-24.
**Future owner:** coordination, to create and triage a separate PGMCP issue; no issue has yet been created.
**Suggested issue title:** Audit and harden shipped adapters for large selections and native invocation limits.

The authoritative finding and follow-up acceptance boundaries are recorded as **D-VAL-01** in [Validation — Deferred Work](validation.md#deferred-work), with F-VAL-01 native launch evidence and command-length measurements. Audit all nine shipped adapter packages and every implemented check/test/fix role for analogous selection-to-native execution limits, recording applicability individually. Preserve the generic role contracts as the starting constraint; tool-specific execution strategies belong inside adapters. No universal batching strategy or contract expansion is approved.

This defers robustness follow-up, not the F-20 adapter extension suite itself. Missing validation evidence remains visible; this notice does not turn unavailable checks into passing evidence or authorize issue-460 repair cycles. Coordination should link its new issue back to the validation notice.
