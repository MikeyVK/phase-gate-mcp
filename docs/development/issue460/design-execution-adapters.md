<!-- docs\development\issue460\design-execution-adapters.md -->
<!-- template=design version=5827e841 created=2026-09-05T05:50Z updated= -->
# Issue 460 Execution Adapter Design

**Status:** DRAFT  
**Version:** 0.75
**Last Updated:** 2026-09-10  
**Primary Package:** DI-05  
**Upstream Dependencies:** Frozen F-08/F-19/F-20 strategy; DI-01/DI-02 template profile references  
**Downstream Consumers:** DI-04 scaffold/safe-edit, public check/test/fix operations, DI-07 workflow/documentation, DI-08 assurance  
**Lifecycle Status:** Drafting; manifest nucleus decided; shared check binding and profile-selection proposal open

## 1. Purpose and Authority

Own the execution adapter Design for issue 460: package contracts, catalog resolution,
generic process execution, separate check/test/fix contracts, consumer configuration,
fix application, operation evidence, and migration. The document is the dedicated
DI-05 owner required by the [documentation contract](README.md#design-documentation-structure).

Frozen Research supplies the product and compatibility decisions. The human owner
accepted implementation-based package grouping, the discovery/reference nucleus, and
native tool configuration as the tool-settings authority on 2026-09-05. Proposed
mechanisms remain explicitly open until discussed with the human owner. This document
does not yet specify complete executable interfaces or final per-tool migration values.

## 2. Scope and Exclusions

| In scope | Owning consequence |
|---|---|
| Official and trusted workspace adapter packages | One startup catalog, package identity/version/fingerprint, role declarations, dependencies, trust, and restart behavior |
| Generic process execution | Opaque launch instructions, transport, bounded execution, scratch space, capture, and execution failures |
| `check/v1` | Factual analysis used by output profiles and explicit checks |
| `test/v1` | Behavioral execution and framework-aware evidence for configured suites |
| `fix/v1` | Bounded proposals, PGMCP authorization, stale checks, application, and recovery |
| Consumer contracts | `run_checks`, `run_tests`, `apply_fixes`, `checks.yaml`, `tests.yaml`, `fixes.yaml`, results/cache/presentation, and migration |

DI-04 owns scaffold/safe-edit persistence and its policy decisions. DI-06 owns template
renewal and activation. DI-03 owns concrete template content and output-profile
assignments. No new product role, compatibility choice, or consumer family is added
to the frozen Research scope. Method bodies, cycle definitions, automatic dependency
installation, and external package-history retention are outside this workshop.

### Security Isolation Boundary

The human owner defers whole-server and subprocess sandboxing to a separate issue.
The [security isolation notice](deferred-work.md#deferred-work-notice-server-and-subprocess-security-isolation)
records bounded current-source evidence and future scope. Package admission and a
read-only check contract are not OS-enforced isolation. Issue 460 retains application
authorization, without promising safe execution of untrusted adapters. Path spelling
does not establish security. Continue Design without sandbox implementation or new
security manifest fields; exact adapter input fields remain open.

## 3. Binding Inputs

- [F-08](research-findings.md#f-08--schema-valid-rich-contexts-can-produce-invalid-source): applicable output evidence, dormant toolchains, and honest unavailability.
- [F-19](research-findings.md#f-19--output-validation-and-quality-gates-duplicate-executable-authority): one check authority with separate consumer policies.
- [F-20](research-findings.md#f-20--executable-tooling-is-split-into-language-bound-check-test-and-fix-paths): one process-based extension suite and distinct check/test/fix roles.
- [Approved Strategy](research.md#approved-strategy-and-decision-status): the exact F-08/S-14, F-19, and F-20 rows; [invariants](research.md#core-invariants) I-16/I-19; [expected results](research.md#expected-results) E-13/E-20/E-23.
- [DI-05 mandate](design-intake-map.md#di-05--language-agnostic-check-test-and-fix-adapter-suite), XC-01/XC-02, and RC-01.
- [Manageability conditions](README.md#binding-design-and-planning-manageability-conditions): binding decomposition, preservation, rollback, evidence, and cutover constraints.
- [DI-04 validation policy](design-mutation-validation.md#44-scaffold-validation-request-and-result-contract): accepted scaffold-facing outcomes that the check contract must support.
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md): SRP, OCP, ISP/DIP, configuration authority, fail-fast loading, explicit mutation, public test boundaries, and presentation separation.

## 4. Owned Decisions

| ID | Decision or proposal | Status |
|---|---|---|
| D-ADAPTER-01 | DI-05 has its own document; DI-04 retains scaffold/safe-edit mutation policy | Decided by the human topology condition |
| D-ADAPTER-02 | One resolved catalog and generic process boundary serve separate `check/v1`, `test/v1`, and `fix/v1` contracts | Binding Research decision |
| D-ADAPTER-03 | Group a package around a cohesive tool or implementation; allow several declared roles when they share that implementation | Decided; human agreement 2026-09-05 |
| D-ADAPTER-04 | Discover manifest-owned adapter packages through shallow startup enumeration of official and workspace sources; consumer references use declared identity | Decided; human agreement 2026-09-05; exact admission/binding schemas open |
| D-ADAPTER-05 | Native tool configuration owns tool settings; manifests describe packages and PGMCP configuration selects capabilities, scope, and execution policy without a second tool-settings layer | Decided; human direction 2026-09-05; concrete migration values open |
| D-ADAPTER-06 | Organize manifest declarations by role, with an explicit role-contract version, entrypoint, and named capabilities under each role | Decided; human agreement 2026-09-05; not a complete manifest schema |
| D-ADAPTER-07 | Define named check bindings once in `checks.yaml`; output profiles select those check IDs and explicit check operations reuse them | Human-approved W03 consolidation, 2026-09-10; §§7.5 and 7.14 |
| D-ADAPTER-08 | Construct configuration-derived public tool contracts during startup before publication; exposure, validation, defaults, and error-schema feedback use the same immutable startup contract | Decided lifecycle requirement; human direction 2026-09-05; exact interfaces and client evidence open |
| D-ADAPTER-09 | Startup validates declarations and builds configured check/test/fix selections without invoking adapters; dependency availability is reported on use and never silently weakens profiles | Human-approved correction 2026-09-07; supersedes 2026-09-05 preflight/filtering direction; sections 7.6–7.7 |
| D-ADAPTER-10 | Defer agent-facing startup health, health-first guidance, and new health-driven tool blockades to a separate issue; preserve current health/admin behavior | Explicit human scope decision 2026-09-05; see the [deferred-work notice](deferred-work.md#deferred-work-notice-agent-facing-startup-health-and-recovery); not a prerequisite for issue 460 |
| D-ADAPTER-11 | Separate requested check scope from supporting read context; wider check execution requires explicit caller permission and truthful effective-scope reporting | Human-approved nucleus §7.8; W03 §7.14 completes selection transport and outcomes |
| D-ADAPTER-12 | Branch selection includes committed branch changes, staged/unstaged changes, and non-ignored untracked files; checks inspect current working-tree content | Human-approved §7.9; W03 §7.14 records a selection view, not an immutable filesystem certificate |
| D-ADAPTER-13 | Require run_checks scope; remove auto/default and auto-only state | Binding amended Research; section 7.10; previous auto design superseded |
| D-ADAPTER-14 | Respect native optimization with explicit fresh intent; no PGMCP execution-result reuse | Binding amended Research; section 7.11; previous cross-scope reuse design superseded |
| D-ADAPTER-15 | Internal prepare/execute protocol with prepared work and reuse-state machinery | Withdrawn following the human-directed step back; work_id/session machinery is rejected, not an optional extension; section 7.12 |
| D-ADAPTER-16 | Declare proposed-content execution needs through required boolean requires_file; PGMCP owns the direct-content and controlled temporary-file routes, adapters own native translation; no target-location pre-write | Human-approved ownership and boolean field 2026-09-06; section 7.13 |
| D-ADAPTER-17 | W02 package boundary is approved: source layout, consumer-backed fields, explicit files/fingerprint, restart limitation and narrow interfaces; trust/provenance follow D-ADAPTER-18/19 | Human-approved W02, 2026-09-10; §§7.4.1–7.4.3 |
| D-ADAPTER-18 | Required adapters.yaml under resolved_config_root owns trusted_adapter_ids; ship empty, load centrally and inject into catalog admission; no second settings source or self-trust | Human-approved W02-B, 2026-09-10; §7.4.2 |
| D-ADAPTER-19 | Role results carry typed external_tools as ordinary invoked-run evidence; invalid_request stays minimal; no new query tool, startup survey or result-decision consumer | Human-approved W02-F, 2026-09-10; §7.4.3 and amended scaffold response |
| D-ADAPTER-20 | Consolidate run_checks selection, scope and result contracts; permit a positive per-invocation caller timeout override without changing the internal termination budget | Human-approved W03, 2026-09-10; §7.14; previous scope/profile decisions are not reopened |
| D-ADAPTER-21 | run_tests exposes flat tests selection and addressed CLI args in one startup-built schema; adapters/native tools own switch interpretation; supersede test options_schema without extending other consumers | Human-approved W04 input/exposure, 2026-09-10; §7.15; test results and exact remaining integration stay open |
| D-ADAPTER-22 | Public success is operational and inversely maps to MCP isError; correctly reported negative or unavailable domain results are not tool execution failures | Human-required correction, 2026-09-10; §7.14; applies across check/test/fix consumers, without deriving MCP errors from adapter exits |
| D-ADAPTER-23 | Remove generic native verbose interpretation across check/test/fix consumers and adapter inputs; native switches retain their documented meaning through addressed args | Human-approved correction, 2026-09-10; §7.15; exact non-test argument routing remains separately owned |
| D-ADAPTER-24 | run_tests requires configured or targets scope; configured preserves native selection, targets=["."] explicitly selects the workspace directory; retain passed for a successful requested operation | Human-approved W04 corrections, 2026-09-10; §7.15; no special collection status or redundant workspace scope |
| D-ADAPTER-25 | Execution bindings own default_args; mutation checks are configured-only, while explicit check/test/fix calls may replace arguments per selected binding; report args_source and effective_args | Human-approved consumer/default correction, 2026-09-10; §7.16; omission uses defaults, explicit [] clears them, no merging or public mutation args |

The decided rows establish ownership and approved contracts. W02/W03 close package
and check behavior in §§7.4.1–7.4.3 and 7.14; W04 §7.15 amends test input/exposure.
Concrete DTO/schema integration and independent conformance remain required. Test
results, remaining test configuration/transport, fix decisions, native-setting migration
and fix transaction mechanics remain open Design work.

## 5. Responsibilities and Boundaries

### 5.1 Consumers determine purpose

| Consumer | Question being answered | Input to execution | Consequence owned by consumer |
|---|---|---|---|
| Scaffolding | Is the complete proposed artifact a valid starting point under its output profile? | Proposed content, logical target, and selected profile checks | DI-04 applies `enforce`/`report` and creates the file when permitted |
| Safe edit | Does the complete proposed replacement satisfy the applicable profile? | Replacement content, logical target, and selected checks | DI-04 applies validation=enforce/report and controls replacement |
| `run_checks` | What do the requested checks report about the selected existing files? | Explicit check selection, scope, and relevant file content/context | DI-05 reports check evidence and owns the applicable run lifecycle |
| `run_tests` | Do the configured behavioral tests meet their expectations? | Selected configured test suites and declared options | DI-05 reports framework-aware execution evidence |
| `apply_fixes` | Can the requested changes be proposed and safely applied to these targets? | Authorized targets and selected fix capabilities | DI-05 validates proposals and controls authoritative mutation |
| Workflow gates | Is the evidence sufficient for the configured workflow condition? | Relevant completed operation evidence | DI-07 preserves workflow/policy ownership |

A scaffold profile selects checks appropriate to a first generated artifact. It does
not automatically select the workspace's full lint/type/test workload. Reusing a check
implementation does not make every consumer select the same checks or depth.

### 5.2 Vocabulary and implementation ownership

| Term | Meaning and owner |
|---|---|
| Adapter package | Distributed implementation with a manifest-owned `adapter_id`, one authored version, role declarations, and executable assets |
| Adapter | The package's executable implementation of one or more role contracts; it may call a library or an external tool |
| Capability | A declared operation offered by an adapter, such as checking formatting, proposing formatting changes, or executing a test suite |
| Role contract | The versioned request/result rules for `check`, `test`, or `fix`; shared process transport does not merge their results |
| Resolved catalog | The immutable startup view of admitted packages and their declared roles/capabilities; runtime consumers read this view |
| Consumer configuration | Selects capabilities, scope, suites, and policy; it contains no duplicate command builder, tool-output parser, or tool-specific exit rules |

The adapter owns external-tool invocation, library calls, parsing, and external-tool
version discovery. Generic server infrastructure launches the declared entry point
without understanding its language or command semantics. A Python adapter may use a
Python library within its own process; Python receives no special in-server execution
route. Implementations in other languages use the same role contracts.

PGMCP startup composes the catalog, process execution, and narrow role consumers through
injection. Scaffold/safe-edit consumers receive a check boundary without fix application
methods. The process runner receives no authority to decide persistence or workflow
progression. Exact interface signatures remain open.

## 6. Options and Rationale

### W-ADAPTER-01 — What belongs in one package?

The human owner accepted the implementation-based grouping below on 2026-09-05.
The comparison concerns grouping inside the approved process-based adapter suite.

| Option | Benefit | Cost or counterexample | Workshop position |
|---|---|---|---|
| One package per language | A single package is easy to associate with a language | A Python package could bind syntax parsing, Ruff, Mypy, Pyright, and Pytest to one release and dependency boundary despite separate implementations | Not recommended as the default |
| One package per role | Check/test/fix remain visibly separate on disk | Separate check and fix packages for one tool can duplicate its invocation, version discovery, and implementation maintenance | Use only when implementation ownership is actually separate |
| One package per cohesive tool/implementation, declaring supported roles | Related code, dependency knowledge, and package versions stay together; each role still has its own contract | A package change changes that package fingerprint even when one role is unaffected; independently distributed implementations may merit separate packages | Selected |

Illustrative package contents, not final IDs or a final official adapter inventory:

| Implementation package | Candidate role contents | Why grouped this way |
|---|---|---|
| Existing Python syntax implementation | A syntax check | Current `ast.parse` behavior can move behind the process contract without requiring a full lint/type run |
| Ruff integration | Retained formatting/lint checks and separately declared formatting/lint fix proposals | The existing configuration already uses one tool for check and fix commands |
| Pytest integration | Behavioral test execution | Collection, markers, coverage, and framework result interpretation share one implementation |

A capability that combines several tools may still justify one package when it has a
single cohesive implementation and dependency lifecycle. The grouping rule is not a
fixed one-executable-per-directory restriction. This decision creates no cross-package
inheritance, shared adapter base, package dependency solver, or role-level fingerprints.

A change only to a package's fix implementation changes that package fingerprint for
subsequent check invocations too. The package remains the versioned distribution unit.
An unrelated package keeps its own version and fingerprint. The human agreement includes
this trade-off; splitting identities per role is not part of the selected design.

### W-ADAPTER-02 — Finding packages and referring to their capabilities

**Status: Decided; human agreement 2026-09-05.** This workshop applies the package
boundary to source discovery and consumer selection. Trust configuration and exact
field schemas remain follow-up work.

| Option | Benefit | Cost or risk | Workshop position |
|---|---|---|---|
| Authored central list of packages plus per-package manifests | Explicit physical index | Every addition/move requires coordinated index maintenance; identity and package declarations still require loading each manifest | Not recommended as a second inventory |
| Recursive search below arbitrary workspace folders | Finds packages without a fixed placement contract | Can discover examples, copies, test fixtures, or nested implementation assets; scope is harder to explain | Not recommended |
| Shallow enumeration of known official and workspace suite roots | A package is added as one directory; the manifest owns its declarations; enumeration is bounded and performed at startup | Exact source/admission rules and duplicate diagnostics are required | Selected |

Selected source and reference nucleus:

- Official packages are resolved from the installed PGMCP distribution; workspace-owned
  packages are resolved from `.pgmcp/adapter_suite/`. Both contribute to one catalog.
- Each direct package directory contains `manifest.yaml`. Its `adapter_id` defines
  identity; the containing directory is a physical location only. Internal implementation
  folders are not scanned for additional packages.
- An absent optional workspace suite means no workspace packages. A present suite is
  validated as a package store; incomplete package directories return startup diagnostics.
  The exact treatment of non-package files, links, and packaged-resource access remains
  part of the full discovery contract.
- There is no implicit local-over-official override. Duplicate adapter identities fail
  before tool exposure, as required by F-20. A local alternative uses its own identity
  and explicit consumer selection.
- Discovery reads declarations without executing adapters. Explicit workspace trust
  remains a separate admission condition; copying a directory or selecting it in a role
  configuration must not silently grant that trust.
- Consumer configuration selects a package by `adapter_id` and a declared capability
  in the required role. It does not contain the executable path, command, or parser.
  An output profile states its required checks; the binding chooses their implementation
  without adding adapter commands to template packages. Exact check/profile IDs and the
  placement of their binding fields remain open.

Illustrative reference, not final YAML or registered IDs: a formatting check selection
can refer to the Ruff adapter's formatting-check capability, while a fix selection can
refer to its formatting-fix capability. The role disambiguates their different contracts;
availability of one never grants the other role permission to run.

The official source decision deliberately uses the installed distribution as authority.
The existing [workspace asset renewal](../../../mcp_server/services/workspace_upgrader.py)
recursively copies packaged assets; adapter distribution must explicitly account for that
consumer instead of accidentally creating a second official copy in the workspace.
The precise official asset path and migration treatment remain open. Template-suite
activation/reconciliation rules do not automatically become adapter upgrade rules.

### W-ADAPTER-03 — Manifest fields and role entrypoints

**Status: Decided; human agreement 2026-09-05.** The selected nucleus is the declaration
structure and each field's consumer. It does not settle process-launch syntax or complete capability
descriptors. Package versions/fingerprints and native tool-settings authority remain
unchanged.

| Entrypoint boundary | Consumer consequence | Trade-off | Workshop position |
|---|---|---|---|
| One mandatory package-wide entrypoint | Every supported role starts the same program | Compact, but separate role programs need a package-owned dispatcher solely to meet the layout contract | Not recommended as mandatory |
| One entrypoint declaration per role | The catalog resolves the role's start declaration; capabilities within that role share it | Several roles may reference the same program; independent role programs need no extra dispatcher | Selected |
| One entrypoint declaration per capability | Each individual operation has independent launch wiring | Repeats launch details for related operations and encourages a command-per-check inventory | Not recommended as the default |

An entrypoint starts the adapter implementation, not the underlying Ruff/Pytest/etc.
command. A shared implementation may be referenced by several roles; those references
do not duplicate its code or native tool settings. One role can dispatch its declared
capabilities internally while generic server infrastructure remains tool-neutral.

Section 7.4 supplies the selected field/consumer nucleus. The following workshop should
make a concrete consumer selection traceable from `checks.yaml` or an output profile to
one catalog capability, including the boundary with `fixes.yaml`. Process/environment
launching then supplies the exact entrypoint representation. These are Design workshops,
not implementation cycles.

### W-ADAPTER-04 — One check binding, different consumer selections

**Status: Proposed.** Keep a workspace check identity separate from its selected adapter
implementation. Define that binding once in `checks.yaml`, and let output profiles and
explicit check requests select the same check identity. This is selection configuration,
not a replacement for native tool settings.

| Alternative | Consequence | Workshop position |
|---|---|---|
| Repeat adapter/capability references in every profile and operation selection | Fewer names, but changing an implementation requires finding every consumer and maintaining repeated bindings | Not recommended |
| Bind a named check once; profiles and explicit operations reference it | Adds one meaningful check identity shared by different consumers; implementation selection has one owner | Recommended |
| Maintain a separate executable registry for scaffold profiles | Recreates the parallel execution authority rejected by F-19/F-20 | Rejected by binding Research |

The proposal places check bindings and output-profile selections in distinct `checks`
and `profiles` sections of `checks.yaml`. Section 7.5 illustrates the relation; exact
profile applicability, default/full-operation selections, scope, and configuration
schemas remain open. Profile placement also requires the DI-02 integration check below.

## 7. Detailed Design

### 7.1 Established package obligations

Official adapters ship with PGMCP. Workspace-owned adapters live under
`.pgmcp/adapter_suite/` and require explicit owner trust. Startup forms one catalog
without duplicate `adapter_id` values or incompatible contract declarations. Finding a
package is distinct from authorizing its code to execute; §7.4.2 fixes the explicit
trust configuration and its admission ownership.

One package has one authored version and one computed fingerprint over its manifest
and package-owned semantic implementation inputs. Runs record only invoked package
identities and external-tool identity/version. No adapter-suite hash is added to runs,
and adapter evidence does not enter scaffolded-artifact source metadata.

Section 7.4.1 now records the approved source layout, file inventory, role-field additions
and fingerprint boundary. Sections 7.4.2–7.4.3 complete trust and the native provenance
return amendment; role-specific binding/operation contracts keep their workshop owners.
The package declaration filename is `manifest.yaml`, as selected in W-ADAPTER-02.
The approved `template_suite/` layout does not automatically define `adapter_suite/`.

### 7.2 Version, fingerprint, and their consumers

The authored version is the package owner's readable release label. The computed
fingerprint identifies the covered package content, including local changes that have
not received a new version label. They are separate facts, not alternative spellings
of the same value. F-20 already requires both; this workshop clarifies their use.

| Consumer | Why it consumes this identity | Limit |
|---|---|---|
| Run-result construction and structured evidence storage | Associate the invoked role with the selected adapter ID, authored version, and computed package fingerprint | Records package provenance; it does not decide whether a check passes, a test succeeds, or a fix is authorized |
| Human or agent investigating a run, including an independent reviewer | Distinguish an unchanged release label from changed adapter implementation when comparing available evidence or owner-supplied package content | Diagnostic evidence, not automated compatibility judgment or historical-source lookup |

For example, editing a workspace adapter while retaining its version label changes its
package fingerprint. Editing only the workspace's native tool configuration does not:
that configuration is not part of the adapter package. Updating the external tool can
also change results without changing the adapter package; its separately reported
identity/version remains relevant. Equal adapter fingerprints therefore do not prove
equal inputs, configuration, environment, or run results.

There is no approved automatic adapter-upgrade, result-reuse, trust, or compatibility
decision based on this fingerprint. Check/test/fix execution does not require a hash
comparison to perform its role. No role-level hash, new history registry, configuration
hash, binary retention, or reproduction guarantee is introduced. Exact fingerprint
inputs, encoding, and computation lifecycle remain to be designed; package content
identity must not be presented as a complete execution-environment identity. The subsequent
partial W02 approval in §7.4.1 fixes coverage, compact encoding and restart assumptions.

### 7.3 Manifest and native tool configuration authority

A manifest is declarative package configuration as well as a description. That is not
an SSOT violation: the boundary is which facts it owns, not whether a file can be called
configuration. A consumer reference to an `adapter_id` is not a second declaration of
that identity. Copying the package's entrypoint or supported-role list into consumer
configuration would create a competing authority.

| Authority | Owns | Does not own |
|---|---|---|
| Package `manifest.yaml` | Package identity/version, supported role contracts/capabilities, and adapter entrypoints | Workspace lint rules, type-check strictness, test thresholds, or repeated external-tool command recipes |
| Adapter implementation | Tool integration, request translation, result interpretation, and tool-version discovery | A hidden PGMCP-specific replacement for native tool settings |
| Native tool configuration | The tool's rules, exclusions, language target, type-check options, test defaults, and tool-owned thresholds | PGMCP capability bindings, persistence decisions, or fix-application authority |
| PGMCP role configuration and operation request | Capability selection, requested scope/suites, bounded execution controls, and consumer policy | Duplicate native rule lists, stricter hidden defaults, or copied parser/command implementations |

The human direction selects one effective tool-settings authority through each tool's
normal configuration mechanism. Native inheritance, subproject configuration, and
documented defaults remain possible; this is not a requirement for exactly one physical
file per repository or a mandatory config file for an otherwise unconfigured tool.
PGMCP must not reimplement native configuration discovery/merging as a generic YAML DSL.

Adapters may set transport and role-safety options, such as machine-readable output,
non-writing check mode, or bounded fix-proposal generation. They may translate explicit
operation requests such as a selected test subset. Native verbosity switches are passed
through args without a generic boolean interpretation (D-ADAPTER-23). Those
options must not silently replace native rules or grant extra mutation authority.
A native setting that enables writing cannot turn a `check` into a `fix`; the adapter
must uphold its role contract. Exact request-option schemas remain open, not an arbitrary
command-line override bag. The later W04 approval in §7.15 specifically permits
addressed native CLI arguments for run_tests without a native option schema or mandatory
switch prevalidation. Section 7.16 extends that route to explicit check/fix calls and
adds use-specific default_args without relaxing role boundaries. Native configuration
still owns native rules; these defaults are a declared invocation recipe, not a second
generic representation of the tool's configuration. Mutation consumers use only their
selected check bindings' configured arguments, never public caller overrides.

For proposed content, the relevant configuration belongs to the intended project and
logical target, not accidentally to the scratch directory. Native path-relative rules
and import context must survive materialization. The mechanism belongs to Q-ADAPTER-03;
adapters must not compensate by maintaining duplicate rule settings. Equivalence is
scoped to comparable tool versions, inputs, purpose, and configuration, not a promise
that every IDE view or full-project run produces identical output.

#### Development dependency ownership

Human clarification (2026-09-06): PGMCP operates in a provisioned development workspace;
it is not responsible for creating that workspace's language environments. Selecting an
adapter does not relieve the workspace owner of installing its prerequisites. An adapter
package must supply an explicit dependency contribution that the owner can incorporate
into the workspace's development setup, not an adapter-owned automatic installation
obligation. This refines the existing F-20 provisioning boundary without reopening
Research or creating a new product role.

The contribution must distinguish what is required to use the adapter (including its
own implementation runtime and the native tool) from dependencies needed only to develop
the adapter itself. Do not infer adapter-runtime availability from the language of the
files being checked. Nor does an installation declaration prove current availability:
declaration admission remains separate from dependency failures reported on use. No
adapter dependency preflight is performed during startup.

No automatic installs, dependency upgrades, environment creation or edits to workspace
dependency files occur during discovery or invocation. The workspace owner retains
package-manager/version/lockfile choices and resolves dependency conflicts; PGMCP does
not silently choose a different environment to evade them. Official adapter distribution
obligations remain as defined by F-20; no runtime-bundling requirement is added here.

Exact contribution format remains a Design decision. Named first-executable resolution
follows the startup PATH contract below; package-file launch forms are specified below.
Prefer native dependency mechanisms without a second authored dependency list in
manifest.yaml or a PGMCP-owned resolver. Existing examples include this repository's
requirements-dev.txt including requirements.txt, Python package dependency metadata and
npm package metadata. These are alternatives appropriate to their ecosystems, not a
requirement for every package to ship every format. An installed prerequisite must still
be locatable by the selected start instruction; that launch boundary is not discharged
by assigning installation ownership to the workspace.

#### Named executable resolution from the startup environment

Human-approved direction (2026-09-06): for an entrypoint naming an installed program,
resolve that name against the PATH supplied to the PGMCP server at startup. The workspace
owner provisions that launch environment. It is not an independently activated terminal
environment or an environment inferred from the source language, .venv directories,
server interpreter or editor settings. The generic resolver uses the declared PATH
ordering, without an additional implicit search in the current working directory.

Resolve once into the catalog's internal absolute executable location, then use that
same location for actual launches without invoking it during startup. This fixes
selection, not binary content: no executable hash, environment lock or retention promise
is added. If the selected executable later disappears or fails to launch, preserve the
existing runtime failure rather than re-resolving to another installation. An unresolved
name remains an unresolved launch selection, not an invalid capability reference. It
does not remove configured choices from schemas or prevent otherwise valid startup;
attempted use produces the existing generic launch_failed outcome, not a fabricated
adapter response. This preserves startup PATH selection without dependency probing,
installation, activation, automatic fallback or a new server-wide health blockade.

Python and Node names receive the same generic treatment as other program names. Do
not add a language runtime registry, per-adapter interpreter guess, shell activation or
new PGMCP dependency configuration. A single program name has a single resolution in
this environment; a workspace needing different installations must supply distinguishable
start instructions. No per-invocation runtime selector is introduced.

The current proxy copies its own os.environ when starting/restarting the server
([proxy.py](../../../mcp_server/core/proxy.py)). Consequently, changing an unrelated
terminal's environment does not update a running server/proxy. Applying a changed MCP
launch environment may require a fresh launch from the client, not only restart_server.
Document this operational requirement without modifying proxy or deferred health logic.

Primary reference: Python's [subprocess documentation](https://docs.python.org/3/library/subprocess.html)
describes platform-dependent executable lookup and recommends a full path to avoid it;
Windows [environment inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/environment-variables)
establishes the parent-process boundary. The explicit launch-descriptor forms are
defined below; package-file admission is defined below and platform executable-name/
suffix handling remains detailed follow-up work. This does not claim sandbox isolation.

Conformance covers declared PATH ordering, no implicit cwd/server-Python fallback,
different terminal versus server environments, reuse of the resolved location, missing
executables at startup/on use, and no silent switch to another installation.

#### Workspace-root adapter working directory

Human-approved launch boundary (2026-09-06): start each adapter invocation with its
working directory set to the resolved workspace root supplied by existing workspace
context. Do not add a working_directory field to the manifest, role configuration or
request. Do not inherit an incidental server cwd, use the package installation directory,
or switch cwd to a temporary validation directory. Set the child process's working
directory without changing the server process's global working directory.

Adapter code location and working directory are separate: package-owned script/binary
references must resolve from the known package location into explicit launch paths,
not by requiring cwd to point at the package. The explicit package_file reference below
owns that representation. No machine-specific installation
prefix needs to be authored into a portable package merely to locate its own code.

The initial cwd supplies project context; it neither grants write authority nor broadens
the requested scope. It does not guarantee that all native tools discover appropriate
configuration automatically. The adapter remains responsible for native configuration
and intended-target semantics and may choose a justified working directory for its
native subprocess when that integration requires it. Generic PGMCP code does not search
or merge native configuration. Earlier target_path and input_path meanings remain intact;
the JSON request gains no duplicate workspace_root field for this scaffold slice.

Conformance covers an adapter package outside the workspace, moving that package,
unchanged workspace-root cwd across text and temporary-file input routes, and concurrent
calls without process-global cwd mutation. Native configuration behavior remains proven
by adapter-specific evidence, not inferred from this start-directory contract.

#### Explicit executable and argument references

Human-approved representation (2026-09-07): the role entrypoint has separate executable
and args fields. Use the explicit package_file object for a package-owned executable
as well as a package-owned argument. Reject the alternative ./ prefix convention for
selecting package-executable lookup. Both alternatives need the same semantic choice
between PATH and package lookup; the object makes that choice structural rather than
encoded in a string prefix. This is a readability/type-boundary decision, not a claim
of measured performance equivalence or a guarantee of identical implementation branches.

| Location | Allowed shape | Consumer and interpretation |
|---|---|---|
| executable | Non-blank program-name string | Generic launcher resolves the name through the startup PATH contract |
| executable | Closed object with required package_file string | Generic launcher resolves the named file within the admitted package and starts it directly |
| Each args item | Strict string | Pass exactly one literal argument, without splitting or interpreting it |
| Each args item | The same closed package_file object | Resolve the package file to one full path argument |

The entrypoint object is closed, with executable and args required; args is an ordered
array and may be empty. The package reference has exactly one required non-blank string
field, package_file, and no null/extra fields. Use one shared reference type/resolver for
both positions rather than a second executable-specific file descriptor. The PATH
variant is a program name, not a command line or alternative absolute/relative path
syntax. Package-relative location and admission obligations are defined below.

Illustrative Python entrypoint:

```yaml
entrypoint:
  executable: python
  args:
    - package_file: check.py
    - "--role"
    - "check"
```

Illustrative self-contained executable entrypoint:

```yaml
entrypoint:
  executable:
    package_file: adapter.exe
  args: []
```

These are start-descriptor examples, not official adapter IDs or platform support
claims. PGMCP does not inspect .py/.js suffixes to pick an interpreter, rewrite literal
arguments into file references, expand variables, or assemble a shell command. It
supplies the resolved executable and ordered arguments to process infrastructure.
On Windows the process library performs its required command-line encoding; this does
not imply that Windows process APIs natively accept an argv array. Python's
[subprocess documentation](https://docs.python.org/3/library/subprocess.html) recommends
argument sequences for preserving argument boundaries/quoting. Direct shell/batch
admission and explicitly selected script-interpreter semantics are bounded below.

Compared with a single command string, these fields preserve argument boundaries for
spaces, make executable resolution independent of command parsing, and keep package
references portable without a command-template language. Conformance covers PATH versus
package-executable selection, reuse of the same package reference in arguments, literal
argument preservation and ordering, empty args, spaces in resolved paths, and rejection
of unknown fields/types. No production code is introduced by this design decision.

#### Typed entrypoint contract

The following declaration makes the agreed shapes explicit; it adds no manifest fields.
It is an interface specification, not a loader or process implementation. The constrained
scalar types have the obligations below; their validators contain no filesystem access.

| Type | Required constraints | Direct consumer |
|---|---|---|
| ProgramName | Strict non-blank string; no NUL, path separator, root/drive qualifier, or standalone . or ..; preserve the authored name without trimming, splitting, or expansion | Startup PATH resolver, which looks up the entire name as one program |
| PackageRelativeFilePath | Strict non-blank string without NUL; package-relative rather than rooted/absolute/drive-relative; resolved containment and file existence remain admission checks below | Shared package-file resolver for both executable and argument positions |
| ProcessArgument | Strict string without NUL; an empty string and whitespace are meaningful and preserved | Generic launcher, which delivers exactly one argument |

```python
class PackageFileReference(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    package_file: PackageRelativeFilePath


AdapterExecutable = ProgramName | PackageFileReference
AdapterArgument = ProcessArgument | PackageFileReference


class AdapterEntrypoint(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    executable: AdapterExecutable
    args: tuple[AdapterArgument, ...]
```

Both entrypoint fields and package_file are required and non-null. There is no implicit
empty-args default. YAML/JSON represents args as an ordered array; the immutable runtime
model holds a tuple. The configuration decoding boundary must accept that array and
freeze its container without coercing numeric/boolean/null items into strings or
splitting a string into arguments. This wire-to-value-object conversion must be covered
through the actual configuration loader, not assumed from a direct model constructor.

The union is distinguished by its existing string-versus-object shape; add no kind or
runtime field. A string argument resembling a filename remains literal. A program name
containing spaces is still one lookup name, not a command to parse. The package reference
object cannot contain extra executable options. Loaded descriptors and nested sequences
remain immutable; resolution produces internal launch data without rewriting the
authored descriptor or adding resolved absolute paths to the manifest.

Conformance covers required versus absent/null fields, scalar type rejection, extra
fields at both object levels, array-to-tuple preservation, empty/literal arguments,
and the shared reference type in both positions. No per-interpreter option validation
or registry is implied by this type contract.

#### Package-file location and admission

Human-approved package-file boundary (2026-09-07): package_file identifies a file owned
by the adapter package containing its manifest. Both check.py and scripts/check.py
resolve from that package directory, never from the workspace cwd or startup PATH.
Absolute/rooted and drive-relative locations are invalid. A reference must not resolve
outside the admitted package; a symlink/junction must not bypass this containment rule.
This is a package ownership/admission contract, not a claim of OS sandboxing or protection
against all concurrent filesystem replacement attacks.

The shared constrained path type rejects null, non-string/coerced values, empty/blank
values and NUL characters in addition to the relative-location rules. Pure type checks
do not perform I/O. Package admission resolves the reference and verifies containment,
existence and that it names a file rather than a directory. Use the same contract for
executable references and argument references. Existence of an argument file does not
mean it is executable; native launch eligibility remains a separate use-specific concern.

A missing declared package file means an incomplete/invalid package and is reported
at package admission. It is not treated as a missing external dependency, searched for
in PATH, downloaded, repaired or replaced automatically. Retain the existing catalog
admission/diagnostic boundary; add no health-check redesign or tool blockade here.

Later filesystem changes do not retroactively make startup verification a guarantee.
If the executable cannot be started, generic process management owns launch_failed.
If an argument file disappears, the still-running adapter/interpreter may observe the
failure; preserve its contracted outcome or the existing process/response failure as
actually observed. PGMCP must not fabricate an adapter response or silently switch to
another file. Reloading changed package declarations remains subject to the startup
catalog lifecycle, not an implicit hot-reload behavior.

Conformance covers package-root and nested files, moved packages, spaces in names,
absolute/escaping paths, a resolved link outside the package, missing files, directories
instead of files, and disappearance after admission in both reference positions.
No file monitor, repair service or expanded filesystem security promise is introduced.

#### No implicit shell or direct Windows batch launch

Human-approved launch restriction (2026-09-07): PGMCP starts the declared executable
directly with its argument sequence. It does not choose a shell, enable shell=True,
fall back to a shell after launch failure, or select an interpreter from a script
extension. Packages needing an interpreter declare that program explicitly; a script
reference then occupies the appropriate argument position. This does not introduce
language-specific launch branches in generic PGMCP code.

On Windows, reject direct .bat/.cmd executable targets, whether selected from PATH or
through package_file. Apply this to the resolved executable rather than only to the
authored program name. A batch target must not cause a fallback to another same-named
program. Python's [subprocess security documentation](https://docs.python.org/3/library/subprocess.html#security-considerations)
notes that Windows may use a shell for batch files even without an explicit subprocess
shell request. The rejection preserves the direct-launch contract instead of adding
batch-specific command-string construction or quoting rules.

This rule concerns the executable position, not every package file or argument. It is
not a complete execution-security boundary or a prohibition of shell-authored adapters.
The explicit-interpreter contract below adds no per-language runtime allowlist or new
manifest shell flag. Keep existing package trust, managed process lifecycle and deferred
OS isolation boundaries intact.

Conformance covers direct Python/Node/native executable starts, direct batch rejection
through both resolution routes and case variants on Windows, unchanged literal argument
delivery, and no shell fallback on failure. These are design obligations, not a claim
that platform-specific launch tests have already run.

#### Explicitly declared script interpreters

Human-approved boundary (2026-09-07): an adapter may explicitly select a script
interpreter through the same executable/args contract as any other program. PGMCP does
not choose that interpreter, assemble a shell command, or apply interpreter-specific
argument rewriting. The adapter author owns the flags, script behavior and compliance
with the role's stdin/stdout/stderr and exit-code contract; the workspace owner supplies
the declared runtime dependencies.

Illustrative PowerShell-authored adapter start, not an official package requirement:

```yaml
entrypoint:
  executable: pwsh
  args:
    - "-NoProfile"
    - "-NonInteractive"
    - "-File"
    - package_file: check.ps1
```

The flags belong to this adapter declaration, not a PGMCP PowerShell policy. Their native
meaning is defined by [PowerShell's command-line interface](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh?view=powershell-7.6).
PGMCP resolves pwsh through the agreed startup PATH route and check.ps1 through package
admission, then starts that executable with the ordered arguments and workspace cwd.

Literal delivery describes the PGMCP-to-executable boundary only: the selected program
subsequently interprets its arguments according to its native behavior. This contract
does not promise that an explicitly selected interpreter cannot execute command text.
Do not add a shell-name allowlist, inspect adapter source, or classify native flags in
generic code to imply such a guarantee. Trust admission and adapter conformance retain
their existing responsibilities; OS-enforced isolation remains deferred.

Conformance must prove the same launch and protocol behavior through a declared script
interpreter, including spaces in package paths and no injected startup/progress output.
It does not grant the adapter dependency-installation duties or mutation authority
beyond its selected role and request. No new fields or runtime-specific launch routes
are introduced.

### 7.4 Role-organized manifest nucleus

These are human-approved field names and responsibilities, not a copy-ready complete YAML
schema. The fields below are explicit: supported roles or contract versions are not
inferred from filenames, implementation language, or the package version.

| Field | Meaning | Direct consumer |
|---|---|---|
| `adapter_id` | The package's identity, declared once | Catalog uniqueness, consumer references, and run evidence |
| `version` | One authored readable release label for the whole package | Package maintenance and run evidence; not role-protocol selection |
| `roles` | Non-empty named declarations of the supported `check`, `test`, and/or `fix` roles; an absent role is not offered | Catalog admission and narrow role consumers |
| `roles.<role>.contract_version` | Explicit role-protocol revision; integer `1` denotes the already-approved `<role>/v1` contract | Startup compatibility validation and role request/result validation |
| `roles.<role>.entrypoint` | Typed executable/args declaration for starting this role's adapter implementation; section 7.3 owns the complete launch descriptor | Catalog resolution and generic process execution |
| `roles.<role>.capabilities` | Non-empty named operations offered within the role; IDs are unique within that package/role | Configuration binding, request selection, and adapter dispatch |

The qualified reference consists of package identity, role, and capability identity.
The same local capability name may occur under different roles without ambiguity. A
role-specific configuration already supplies the role context; it need not duplicate
that field in every selection. Exact consumer-reference YAML remains the next workshop.

Illustrative declarations, not final official IDs or a final capability inventory:

| Package | Role | Capability | Consumer-visible purpose |
|---|---|---|---|
| Ruff integration | `check` | `format` | Report whether the selected content satisfies formatting |
| Ruff integration | `check` | `lint` | Report the selected content's native-configured lint findings |
| Ruff integration | `fix` | `format` | Propose formatting changes for explicitly authorized targets |

Identical names do not create a check-to-fix relationship or grant mutation authority.
F-20 still requires an explicit relation between fix capabilities and addressed checks;
its representation must support a fix-only package and therefore cannot assume that a
matching check lives in the same package. Capability applicability, proposed-content
support, and file/context requirements also remain required detailed contract work.
This nucleus must not be advertised as the final manifest before those consumers are
covered.

Do not add authored fingerprint fields, per-file versions, language-dispatch switches,
native tool-rule settings, parser recipes, `supports_autofix`, or a self-granted trust
flag. Do not copy role/capability declarations into a second package index. Concrete
identifier grammar, version syntax, and capability descriptor
schemas remain open; no free-form extension bag is selected here.

### 7.4.1 W02 Package Contract — approved 2026-09-10

The human first approved W02's source/file/capability/fingerprint/interface boundary,
then explicitly approved trust configuration and ordinary native-tool run provenance.
Sections 7.4.2–7.4.3 complete those two decisions; no runtime conformance is claimed.

| Approved boundary | Contract |
|---|---|
| Sources and identity | Official distributed packages under assets/adapter_suite; workspace extensions under resolved_server_root/adapter_suite. Shallow manifest discovery, manifest-owned adapter_id and duplicate-ID rejection; no override by directory name |
| Package files | Required nonempty unique files inventory, relative to the package. manifest.yaml is included implicitly and must not be repeated; reject missing/escaping/duplicate paths. Include package-owned entrypoints, schemas, dependency-contribution files and required runtime imports/data |
| Check capability fields | Nonempty unique inputs tuple of content or selection; requires_file is required boolean when content is supported and forbidden otherwise. Profile admission and input preparation are the consumers |
| Test capability input | W04 §7.15 supersedes the earlier options_schema field: native CLI arguments use the fixed args transport; no per-capability CLI-option schema |
| Fix capability field | Nonempty addresses references, each adapter_id plus check capability; may reference a different package. Fix/check configuration coherence is the consumer; exact fix application remains W05-owned |
| Generic composition | One immutable startup catalog, narrow CheckCatalogReader/TestCatalogReader/FixCatalogReader and one shared AdapterInvoker. Fix orchestration explicitly receives its separate verification-check reader; no consumer gets install/trust mutation APIs |

Use strict, immutable, extra-forbid declarations and exact case-sensitive IDs. Package
and capability IDs follow [a-z][a-z0-9_]{0,63}; adapter version is valid SemVer without
the template-header length cap. Role contract_version remains integer 1. The earlier
test options_schema declaration is superseded by §7.15 and is not a supported parallel
input route. Package file ownership and any independently needed schema assets remain
unchanged; this amendment does not delete files or implement runtime admission.

Fingerprint the canonical manifest including version, plus sorted package-relative file
names and exact declared file bytes using length-delimited records. Use domain
pgmcp:adapter-package:v1 and SHA-256 truncated to 96 bits, encoded as 16-character
unpadded Base64url. This reuses the compact value representation, not template graph
semantics. Native installations/configuration, other packages, outer directory location
and incidental runtime files are excluded. No generic import scanner or per-file versions.
Final canonical byte-record conformance belongs to DI-05, not each adapter author.

The explicit inventory has a consciously accepted maintenance cost: authors must keep
package-owned dependencies complete. Conformance proves that obligation; generic PGMCP
cannot prove arbitrary language imports through source scanning. The fingerprint labels
the admitted package snapshot, not safety, compatibility or full execution equivalence.
Restart after package edits; no monitoring, per-call rehashing or shadow-copy mechanism.
Workspace owners retain dependency installation and history/version policy.

Trust remains an explicit workspace decision, not a manifest self-grant or fingerprint
security check. Section 7.4.2 supersedes the unnamed optional settings-file proposal.
artifacts.yaml still owns produced-artifact locations; D-SUITE-33 still prohibits a
duplicate templates.yaml inventory. Section 7.4.3 exposes native-tool provenance through
the existing run result, never a new query tool, registry or persisted artifact header.

Preservation evidence must cover moved roots, unchanged unrelated packages, changed
declared files, manifest/file constraints, narrow reader injection, configuration-only
non-Python extension and no startup execution. Shared process/role conformance and
check/test/fix migration remain independently proven obligations, not completed evidence.

### 7.4.2 Explicit Adapter Trust Configuration

Human-approved W02-B (2026-09-10): resolved_config_root/adapters.yaml is the sole
workspace adapter-trust policy. Its default location is .pgmcp/config/adapters.yaml;
existing config_root/server-root resolution remains authoritative. No new path setting,
server.yaml, trust environment variable or duplicate trust field under ServerSettings,
checks.yaml, tests.yaml or fixes.yaml is introduced.

```yaml
trusted_adapter_ids: []
```

The closed immutable config has exactly one required field: a unique tuple of strict
AdapterId values. Empty explicitly trusts no workspace adapters; official packages
remain distribution-owned. Managed V3 installation supplies the file with this empty
list. Missing/invalid config follows normal required-config failure, never implicit
trust. ConfigLoader loads it once and injects the pure immutable policy into catalog
admission; the config value has no path knowledge, loader method or import-time work.
The list references manifest IDs, not package paths, aliases or a second inventory.

A discovered untrusted package is not offered; a consumer configuration referencing
one is an actionable admission error. Owner trust authorizes content under that ID,
not a digest, signature or safety certification. A manifest cannot trust itself.
No automatic installation, native settings override, dependency probe or sandbox claim.
DI-06 must include this config in managed V3 installation/distribution inventory;
adapter-package/template renewal must not silently replace owner trust.

Independent evidence covers empty/explicit policy, untrusted-reference failure,
default/overridden configroot, missing/malformed file, duplicate values and no second
trust authority. This is a Design contract, not a created runtime configuration file.

### 7.4.3 Native Tool Identity in Ordinary Run Evidence

Human-approved W02-F (2026-09-10): every check/test/fix role-result response includes
required external_tools: tuple[ExternalToolIdentity, ...]. This is part of the ordinary
invocation result, not a separate query operation or mandatory extra MCP call.

```python
class ExternalToolIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    tool_id: NonBlankText
    version: NonBlankText | None
```

Both fields are required; unknown version is explicit null. An entry describes a native
tool/library actually selected or observed during that invocation. An empty tuple means
no identity was obtained, for example before a missing dependency prevented native work;
it does not claim the package has no dependencies. Do not invent a version from the
manifest or enumerate unrelated installed tools. The adapter supplies observations;
generic PGMCP does not parse native reports or learn tool-specific version commands.
No startup version survey, new query protocol or automatic install is introduced.

Generic invocation evidence retains these records alongside its admitted package
ID/version/fingerprint/contract version. DI-04 and the separate check/test/fix consumers
carry them into the existing cached operation result. Normal concise text need not
print them. No extra resource store, registry or artifact metadata is added. The
human/agent diagnosing a run is the consumer: identical adapter bytes may invoke
different native tool versions. This is context, not proof of causality, complete
environment reproduction, compatibility, pass/fail or fix authorization.

This explicitly amends the earlier closed scaffold payload below. Passed, failed and
unavailable role results require external_tools; W03–W05 retain it in their role-result
variants. Shared invalid_request is unchanged and forbids external_tools, decision and
evidence. Generic launch/timeout/protocol failures invent no adapter response or native
version. Accepted response bytes are not duplicated as raw process capture.

Conformance covers missing field, wrong types, unknown keys, blank IDs/versions,
explicit-null unknown version, zero/multiple identities, all role-result alternatives,
unchanged invalid_request and real cached preservation. Role schemas remain independent.

### 7.5 Approved check bindings and profile selection

Illustrative excerpt of `.pgmcp/config/checks.yaml`, not a complete configuration or a
final official profile/check/adapter inventory:

```yaml
checks:
  python_format:
    adapter_id: ruff
    capability: format
    timeout_seconds: 60
    default_args: []

profiles:
  python_formatted:
    checks:
      - python_format
```

| Example value | Owner and purpose |
|---|---|
| `python_format` | Workspace check identity declared once in `checks`; reusable by explicit operations and profiles |
| `ruff` | Reference to the adapter manifest's `adapter_id`, not a new adapter declaration or directory name |
| `format` | Reference to a capability under that adapter's `check` role; the check configuration supplies the role context |
| `python_formatted` | Output-profile identity selecting required checks; a template manifest can reference it through `output_profile` |

A template declaring `output_profile: python_formatted` selects the profile, which
selects `python_format`, which resolves to the catalog's `ruff` / `check` / `format`
capability. The catalog supplies the admitted role contract and entrypoint. The adapter
performs the check using native tool settings. DI-04 consumes the resulting facts and
applies its already-decided persistence policy.

An explicit `run_checks` request selecting `python_format` uses the same binding and
check implementation for its requested existing-file scope. Section 7.14 owns its
approved public contract. Defining a check does not automatically add it to every
profile or a default/full run. A real scaffold profile can select only syntax/preflight
checks; the formatting-only illustration is not a default profile or a claim of full
Python validity. Safe edit shares the profile boundary, but how it selects a profile
for an existing file remains DI-04/DI-05 work.

Selecting this check never selects `ruff` / `fix` / `format`. Fixes require a separate
selection and authorization through the fix boundary. The explicit fix-to-check
relation remains Q-ADAPTER-07; no same-name relationship is inferred. Test suites retain
their own test contract rather than becoming check profiles.

Startup validates configured check/profile references against the admitted catalog,
without running adapters. Unknown caller selections are rejected before execution.
A structurally valid selected adapter with an unavailable underlying tool returns
on-use availability evidence; it is not confused with an unresolved configuration
reference. Rebinding a check to another adapter is explicit workspace configuration,
not automatic discovery fallback or proof of behavioral equivalence: the replacement
must actually provide the intended check, not merely speak `check/v1`.

DI-02 already includes referenced profile identity and resolved semantics in the
template provenance closure. Before cross-package integration, DI-02/DI-05 must
specify the exact projection of profile selections and bindings into that closure.
Do not silently omit existing profile semantics or include executable adapter bytes,
native tool configuration, or adapter execution fingerprints as template source inputs.
The present workshop does not change any fingerprint algorithm or promise whole-run
reproducibility.

#### Shared extension-to-profile assignment

Human-approved ownership: `profiles_by_extension` is a root key in
`.pgmcp/config/checks.yaml`, alongside `checks` and `profiles`; it is not nested under
`safe_edit_file`. Each entry references one profile declared in the same configuration.
The assignment means "use this profile when the consumer selects by extension," not
"every operation on this file type must use this profile."

For example, extending the illustrative configuration above:

```yaml
profiles_by_extension:
  ".py": python_formatted
```

The example reuses the declared profile; it does not designate formatting as the
official safe-edit preflight policy. Check bindings and native tool settings are not
duplicated in this map.

| Consumer | Use of the shared assignment |
|---|---|
| `safe_edit_file` | Extension-based fallback in its profile-selection contract; DI-04 owns selection precedence and the consequence of no applicable profile |
| `scaffold_artifact` | Continues to select the concrete template manifest's `output_profile`; the extension map does not override or supplement it |
| `run_checks` | No automatic adoption; its explicit/default selection and required scope remain authoritative. Any later extension-based selection must be explicit in its own contract |
| `run_tests` / `apply_fixes` | No selection is inferred from this check-profile map |

DI-05 owns the shared configuration contract and reference resolution. `ConfigLoader`
loads it once into the immutable runtime configuration supplied to consumers; consumers
do not reread YAML or maintain private copies of the mapping. Profile references follow
the existing startup validation boundary, without running adapters or probing native
dependencies. Shared placement does not justify a new configuration file or a speculative
consumer-policy framework.

#### Extension lookup semantics

Human-approved lookup uses only the intended target's basename, never a directory name
or the location/name of temporary check input. Among matching configured extensions,
select the longest one. Compare extensions case-insensitively on every supported host;
this comparison does not change filesystem path identity or path-safety rules.

| Filename and configuration | Selection |
|---|---|
| `orders.py` with `.py` configured | The profile referenced by `.py` |
| `orders.d.ts` with `.d.ts` and `.ts` configured | `.d.ts`, independent of YAML entry order |
| `orders.d.ts` with only `.ts` configured | `.ts`; no implicit declaration-file classification |
| `README.MD` with `.md` configured | `.md` |
| `Dockerfile` or `.gitignore` | No extension assignment; a leading dot alone is not an extension separator |
| A filename with an unconfigured extension | No extension assignment |

Only suffixes following a nonempty filename stem participate. No wildcard, directory
rule, basename registry, native-language detection or catch-all profile is introduced.
The selected suffix references exactly one profile, not a merged sequence of every
matching profile. Once selected, unavailable checks do not trigger a retry with a
shorter suffix or a different profile.

No matching assignment is a selection outcome, not a passing check and not evidence
that an adapter returned an error. A configured reference to an unknown profile remains
a startup configuration error under the existing reference contract. DI-04 owns the
consequence of an absent selection: enforce refuses mutation; report permits a write
only when independent operational/safety conditions allow it, with explicit no-profile
diagnostics and no claim of validation success (DI-04 §4.6). The human-reported independent
Research QA GO on 2026-09-07 permits the shared validation=enforce/report contract,
default enforce, and removal of safe-edit mode/verify_only without aliases or replacement
preview. The earlier deferral is superseded; adapter check facts remain unchanged.
The complete typed key grammar and rejection of ambiguous case-equivalent declarations
remain configuration-schema follow-up, not permission to use dictionary-order precedence.

Preservation evidence must exercise compound and ordinary suffixes, reordered mappings,
mixed-case filenames, dotfiles/extensionless files and no-match outcomes. Prove that
parent-directory and temporary-materialization changes do not alter selection, that a
more specific selected profile is not weakened after check failure, and that consumers
which do not request extension selection retain their own profile authority.

These extension decisions do not complete Q-MUT-04 or authorize automatic weaker-profile
fallback. DI-04 §4.8 separately records the human-approved narrow V3 reader and
read/check/write consistency; neither responsibility belongs to adapters. DI-04 owns
the approved mutation-policy change.

### 7.6 Startup-bound tool schema lifecycle

Human clarification: configuration-derived does not mean regenerated on schema access.
Construct the affected public tool contracts after catalog/configuration resolution and
before publishing the registered tools. An agent must be able to discover legal choices
and input constraints through tool exposure, without reading workspace YAML.

| Stage | Required ownership and behavior |
|---|---|
| Startup resolution | Load and validate package declarations, workspace selections, and defaults into one immutable runtime view; do not execute adapters to describe their interface |
| Dependency boundary | Do not invoke adapters or native tools for startup availability checks; package/path admission does not establish native dependency usability |
| Contract construction | Build the affected tool schemas and descriptions from the admitted catalog, configured selections, and public role/tool contracts; validate reference/default coherence, not dependency availability, before publishing tools |
| Registration | Associate each published tool with its completed contract and the matching execution dependencies; no partially populated or static-placeholder schema |
| Schema exposure | Return a serialization or protected copy of the completed contract; no YAML reread, adapter invocation, or schema reconstruction on access |
| Invocation | Validate selections and resolve omitted defaults against the same runtime view, even when no earlier schema-list request occurred |
| Error feedback | Use the same effective contract for relevant input-error feedback, rather than reconstructing a weaker schema from the static base model |
| Restart | Construct a new coherent view for changed package/selection configuration; no hot-reload mechanism is introduced |

Late client exposure may delay when an agent sees a tool, but must not affect which
server-side contract exists. If internal executor creation is ever deferred, its metadata
must already be complete and its execution dependencies must use the same startup view;
this requirement does not introduce internal lazy initialization. Separate server
instances must not share mutable class-level configuration or schema state.

The startup boundary concerns adapter declarations and PGMCP selection contracts. It
does not freeze native tool configuration or establish dependency availability. Each
actual invocation retains the existing honest on-use failure contract. Native
configuration retains its own selected semantics. Host-side caching across a restart is a separate integration concern: the server
must reject stale invalid input safely, but cannot guarantee that every host refreshes
its cached schema. Supported host/reconnect behavior requires independent evidence.

Direct current-code evidence, inspected rather than executed:

- [Server listing](../../../mcp_server/server.py) reads `t.input_schema` during each
  `handle_list_tools` request; this is not itself a precomputed registration descriptor.
- [ToolFactory](../../../mcp_server/core/tool_factory.py) wraps active core tools before
  exposure. [InputValidationDecorator](../../../mcp_server/core/decorators/input_validation_decorator.py)
  reconstructs its exposed schema and validation-error schema from `args_model`, and
  validates that static model. A core-tool schema override alone therefore cannot
  establish the required end-to-end configuration-derived contract.
- [Bootstrap](../../../mcp_server/bootstrap.py) currently composes and wraps active tools;
  no server-side lazy schema construction is established by these inspected paths.

Preservation evidence must exercise the real registered/decorated boundary: immediate
and delayed/repeated listing; first invocation without prior listing; invalid-selection
feedback; configuration edits between startup and first exposure; a subsequent fresh
startup; independent server instances; and protection against mutation of an exposed
schema object. Verify both legal selections and effective defaults, not only enum text.
Prove that startup and repeated/lazy schema exposure invoke no adapters/native tools,
and that an absent native dependency does not remove an otherwise valid configured
selection or default. Unknown references and structurally invalid declarations remain
startup errors; this is not permissive loading of malformed configuration.
Adapt [decorator coverage](../../../tests/mcp_server/unit/decorators/test_pipeline_decorators.py)
and [registration coverage](../../../tests/mcp_server/integration/mcp_server/test_server_tool_registration.py)
where their public seams fit. Client-side lazy-discovery tests remain a separate proof
obligation; no passing execution or cross-client guarantee is claimed here.

### 7.7 Configuration-based exposure and on-use availability

Human-approved correction (2026-09-07): do not query adapters or their native tools for
dependency availability during startup, including configured adapters. This supersedes
the 2026-09-05 availability-preflight/filtering decision and the proposed separate
startup request/response contract. No probe role/operation, readiness cache, background
monitor or availability-driven schema mutation is introduced.

The input-schema promise is now: a selection is validly configured and offered by an
admitted adapter declaration; it is not a guarantee that its runtime dependencies are
installed or usable. Fail-fast still applies to manifest shape, IDs, contract versions,
references, profile coherence and the established package-file admission rules. It
does not require executing dormant adapters to establish future usability.

- Derive public choices from the admitted catalog and each consumer's configuration.
  A missing native dependency does not remove a configured choice from the schema.
- Keep complete profile obligations and valid configured defaults. At use, an
  unavailable member remains factual unavailable evidence; never drop it, substitute
  a weaker profile, or report a successful empty/partial run as full-profile success.
- A running adapter reports dependency_unavailable through its existing unavailable
  response when it cannot use a required dependency. If PGMCP cannot start the adapter,
  the existing generic launch failure applies instead. Missing tooling is not evidence
  that the submitted content failed its check.
- Construct schemas once per startup view, including for lazy client exposure; calls
  do not change the selectable values based on observed availability. Changed package
  declarations or launch-environment selection retain their existing restart boundary.
  Do not add a universal restart requirement solely to refresh a readiness cache.
- Preserve scaffold report policy and the separate policies of other consumers. A
  dependency failure on first use is handled just like dependency loss after startup.
  A consumer with no configured legal selections is a separate configuration/input
  contract case, not the same as configured selections whose dependencies are absent.

This trades advance dependency feedback for simpler startup and adapter contracts in
an owner-provisioned development workspace. It is consistent with frozen F-08/S-14 and
F-20 on-use unavailability, not a Research scope or compatibility change. The existing
scaffold-facing failure types are reused; exact test/fix payloads remain role-owned.

Presentation follows [issue 456](../issue456/design.md), its
[field projection audit](../issue456/tool-presentation-field-audit.md),
[issue 459](../issue459/design.md), and the current
[presentation architecture](../../reference/presentation_architecture.md).

| Surface | Required treatment |
|---|---|
| Tool input schema | Valid configured values, input meanings, effective selection constraints, and defaults only; no dependency-readiness claim or startup diagnosis |
| Operation failure facts | Existing structured outcomes identify the affected capability and observed failure; a running adapter may report dependency_unavailable, while generic management owns failure to start it; no user-facing formatting in adapter, loader, or domain code |
| Tool-response text | Declarative presentation renders the relevant outcome, affected selection, concise reason, and justified next action; existing item bounds and the configured final UTF-8 byte ceiling apply |
| Complete operation evidence | The frozen operation DTO retains all relevant structured findings and diagnostics; publication precedes text projection so omission/truncation never removes cached evidence |
| Validation schema attachment | Use the existing separate structured-attachment boundary when applicable; do not hide JSON Schema in a prose field or change the agreed scaffold schema-delivery rules |
| Native detail/process diagnostics | Detailed process output remains resource-oriented; native verbosity switches do not bypass text limits or become the only way to see an actionable unavailability reason |

Schema exposure is not a tool-call response: the operation text limiter must not
truncate an input schema or remove valid choices. The earlier proposal to explain
startup omissions inside the schema is superseded. Agent-facing startup diagnostics
belong to the separately deferred `health_check` presentation route, not to input
schemas or dynamic tool descriptions. Issue 460 adds no health logic, health-first
instructions, restart health guidance, or general health-driven tool blockade.
See the [explicit notice](deferred-work.md#deferred-work-notice-agent-facing-startup-health-and-recovery).
That follow-up is not a prerequisite for issue-460 completion or V3 cutover.

All check/test/fix consumer input contracts, including defaults and no-configured-choice
cases, remain required Design work here. Ordinary operation failures and runtime
`unavailable` outcomes on first or later use retain their presentation obligations. Startup facts
do not imply a published diagnostic resource; this issue creates no new startup
report/log exposure. For operation evidence, advertise a cache URI only after actual
successful publication and retain truthful bounded feedback when publication fails.

Preserve the supported-versus-active distinction for presentation alignment: startup
validation still checks all supported tool/output contracts, not only the currently
exposed subset. Do not emit the entire startup diagnosis on every successful call;
operation responses carry relevant facts, not unrelated unavailable adapters.

Before integration, specify each affected DTO field's inline/cache-only/attachment
disposition and rationale, following issue 456's field-level audit. Required proof
includes retained configured defaults despite missing dependencies, failure on actual
use, no startup adapter/native invocation, no partial-profile success, schema/validator
agreement, preserved scaffold `report` semantics, structured message-only failures,
bounded declarative rendering with full cached evidence, cache-publication failure,
and presentation alignment when supported tools or choices are inactive. No execution
evidence is claimed by this documentation-only amendment.

#### DTO-independent error presentation

Human-approved architectural boundary (2026-09-06): adding either a new error reason
or a new error DTO must require no presenter-logic changes. Extend the typed result
contract and declare its presentation instead. Generic rendering and startup alignment
must not contain concrete error classes, consumer-specific field inventories, reason
lists or scaffold policy. Result producers own facts and consequences; presentation
configuration owns wording; the presenter owns only reusable rendering mechanics.

Reuse the existing cache-before-presentation route, text bounds, resource-publication
rules and generic formatting. Reuse does not mean that the current implementation
already satisfies this boundary: validate_presentation_alignment currently maintains
hardcoded error_class_fields, while the supported tool catalog carries a single normal
output_model. Error templates and normal output contracts therefore do not yet form a
complete, uniformly inspected set of possible responses. The current per-tool failure
template also takes precedence over global error-code fallback; merely adding a global
error entry does not prove that its explanation will be displayed.

Human-confirmed correction (2026-09-06): follow the structured-result route established
by [issue 456's SafeEdit contract](../issue456/design.md#33-structured-dto-cleanup-contracts)
and [issue 459](../issue459/design.md), now documented in
[Structured Quality-Gate Findings](../../reference/presentation_architecture.md#structured-quality-gate-findings).
Canonical diagnostic records remain in the consumer's complete typed output graph.
The cache stores that graph before generic declarative projection. Issue 459 added
nested findings through DTO/tool/YAML changes without changing presenter logic.

For an accepted scaffold operation, known operational failures, including
termination_unconfirmed, belong in its structured operation result. Do not introduce
a separate top-level exception DTO merely because a failure is operation-blocking.
Do not use NoteContext as the authoritative or alternative channel for these facts.
Existing outer input-validation, enforcement and unexpected-error handling retain
their boundaries; their continued existence does not require redesigning their taxonomy.

Human-approved W01-A–E integration (2026-09-10):
[DI-04 §4.10](design-mutation-validation.md#410-complete-mutation-operation-result--approved-2026-09-10)
fixes the direct operation error/detail fields, separately owned housekeeping, metadata
fallback explanation and concrete public check record. Invocation/capture facts stay
DI-05-owned; mutation managers decide their operation consequence and tools transfer it.
W01 did not expand the role payload. W02-F now explicitly approves external_tools under
§7.4.3; W05's recovery additions remain separate proposals.

The proposed new per-layer response registration, response identities and variant
dispatcher are withdrawn as prerequisites. Preserve existing runtime derivation from
tool type contracts; introduce no second maintained catalog. The observed legacy
alignment limitations are evidence, not automatic authorization for a broad presenter
refactor. First express scaffold outcomes through the existing typed output graph and
generic scalar/enum/collection mechanisms, then identify any narrowly evidenced gap.
Neither runtime formatting nor admission may gain scaffold-specific branches or copied
field lists. Essential error facts must survive cache publication independently of text.

Conformance uses the real scaffold output graph and presentation configuration to prove
that different operational failures render through unchanged generic mechanisms, full
diagnostics remain cached, invalid projections fail admission and text bounds hold.
This selects an ownership/presentation route, not a universal adapter finding schema.
Native evidence remains native; the earlier four-field sketch is not a complete approved
public DTO. Exact scaffold fields and their inline/cache dispositions remain Design work.

The [DI-04 public mutation nesting audit](design-mutation-validation.md#45-public-mutation-response-nesting-audit)
identifies concrete gaps: singleton validation/selection objects, internal decision/failure
wrappers and discriminated-union collection elements are not established public inline
shapes. Keep approved internal adapter/invocation contracts unchanged. DI-04/DI-05 must
agree direct public fields preserving diagnostic authority and complete native evidence,
without inferring findings from arbitrary JSON or extending the presenter by assumption.
The subsequent human-approved correction requires a factual `message` on failed
adapter decisions, resolving the missing inline explanation without parsing native JSON.
The public record adds no `origin` field: existing typed reason vocabularies distinguish
adapter unavailability from runtime failure, while internal responsibility remains intact.
See the [consolidated DI-04 workshop](design-mutation-validation.md#46-consolidated-public-result-workshop)
for the remaining proposed public field combinations and presentation dispositions.

### 7.8 Requested scope, supporting context, and authorized expansion

The human owner approved this boundary for `run_checks`. A mixed-language profile
selects checks, not a universal file-type filter. Generic scope resolution supplies
candidate paths without Python or other language branches; adapters own their
capability's applicability and required native project context. This does not copy
native tool configuration into `checks.yaml`.

| Situation | Required behavior |
|---|---|
| A check can inspect the requested files independently | Execute within the requested scope |
| A check needs imports, configuration, or other supporting context to inspect those files | Read necessary context within existing access/trust boundaries; supporting reads do not claim those files were checked |
| The tool can only execute a broader project check | Obtain explicit caller permission before broader execution; report the actual checked scope |
| Broader execution is necessary but not authorized | Do not execute that check; report the scope restriction, not success or non-applicability |
| No selected input is applicable to a check | Keep non-applicability distinct from missing tooling and denied expansion; exact result vocabulary remains open |

The accepted request-control nucleus is `allow_expansion: boolean`, default `false`.
Its consumer is PGMCP's check-execution admission boundary, not the adapter's native
rule configuration. `true` permits only necessary related scope expansion within
the workspace, not arbitrary additional paths. Its exact bounds remain Design work;
it does not introduce named PGMCP subprojects.
An adapter identifies the required scope; PGMCP owns authorization. Permission to
expand checks grants neither source mutation nor additional filesystem access.

Illustrative use: an agent selects `frontend/order.ts`. A capable adapter may read
its native configuration and imports while checking that file. If its underlying
tool instead requires checking the containing `frontend/` tree, it needs expansion
permission before that execution. The directory is not a PGMCP project or the
`workspace` scope. Discarding findings outside `order.ts` afterwards does not turn a
broader execution into a file-only check. This example describes alternative
adapter capabilities, not a verified promise about a particular TypeScript tool.

The operation result must distinguish requested scope from actual checked scope per
check where they differ. These are ordinary operation facts, not the deferred startup
health diagnosis. Exact DTO fields and inline/cache projections remain to be designed.

Rejected alternatives: silently widen execution, infer permission from profile
selection, or hide expansion by filtering the returned findings. None gives the caller
a truthful account of requested work, execution cost, and achieved coverage.

Before integration, define how the adapter communicates required project scope before
check execution, how PGMCP validates its bounds, and how mismatches are reported.
Do not invent an additional product role or unapproved protocol operation here.
Prove independent-file checks, context-only reads, denied expansion with no broader
check execution, authorized related-project expansion, rejection of unrelated scope,
and truthful mixed-profile results through the public adapter/consumer boundary.

The retained explicit-path, `branch`, and `workspace` purposes remain the scope-design
starting point. Research removes `auto` and requires explicit scope. Exact path-selector
naming and expansion bounds remain open; section 7.9 owns the approved
working-state selection boundary. In particular, a successful formatting-only run must not clear an
unrechecked type-check failure. No new history model or automatic adoption of these
scope rules by `run_tests`, scaffolding, safe edit, or fixes is approved here.

### 7.9 Branch selection includes current working state

The human owner approved extending the current commit-oriented selection to the
working state used by agents. `branch` selects the union of committed branch changes
relative to the parent merge-base, staged and unstaged changes, and non-ignored
untracked files. Selection is language-agnostic and deduplicated. Existing selected
files are checked using their current on-disk working-tree content, not index-only or
historical commit content. Unsaved editor buffers are not filesystem inputs.

This is a deliberate refinement of the existing behavior in
[QAManager scope resolution](../../../mcp_server/managers/qa_manager.py), which uses
commit-to-commit Git comparisons and Python filtering. An agent need not commit or
stage its work before requesting a branch check. Git-ignore treatment of untracked
files does not discard changes to already tracked files.

Deleted paths remain relevant change information but cannot be submitted as existing
file content. A deletion can require a related project check, for example to detect a
remaining import. It neither proves a passing check nor authorizes scope expansion.
Exact rename/deletion transport, parent-resolution failure behavior, and project
context routing must be completed in the scope/adapter contract before integration.

Concurrent edits must not be credited as checked solely because a path was selected;
the precise input-consistency guarantee remains part of the execution contract.

Preservation evidence starts with the existing
[scope tests](../../../tests/mcp_server/unit/managers/test_scope_resolution.py).
The old auto-scope tests follow the Research catalog's retirement/replacement disposition.
Add public-boundary cases for mixed-language committed changes, staged-only and
unstaged-only changes, staged content differing from working content, new ignored
versus non-ignored files, tracked files matching ignore rules, deduplication, and
deletions without implicit expansion. Preserve parent merge-base isolation and do
not conflate Git resolution failure with a successfully empty selection.

### 7.10 Required scope and removal of auto state

The [narrow F-20 amendment](research.md#narrow-check-retesting-amendment--2026-09-05)
supersedes the earlier auto and cross-scope evidence proposals. The owner authorized
Design resumption after the required-scope correction in Research commit `12665147`.

Every `run_checks` call requires `scope`. Omission is an input validation error
before check/adapter execution. There is no default, auto alias, or scope inferred
from check/profile selection or fresh intent. The startup-built schema and runtime
validation must enforce the same requirement, including lazy exposure.

Branch, workspace, and explicit path selection remain; section 7.9 governs branch
working-state coverage. Profiles select checks, scope selects coverage, and fresh
controls native analysis reuse. These are separate caller decisions.

Retire auto selection, baseline advancement, automatic failed-file replay, and their
exclusive state DTO/repository, wiring, workflow registration, and recovery messages.
The [catalog](template-suite-catalog.md#bounded-retesting-amendment--2026-09-05)
owns exact file dispositions. Do not migrate old state into a new validity cache.
Safe cleanup of existing inert state files remains a bounded Design question.
Unrelated workflow/test state, report caching, fix recovery and F-10 checkpoints remain.

### 7.11 Native optimization and explicit fresh intent

Each admitted check request reaches its adapter; PGMCP does not substitute previous
execution results or maintain cross-scope validity state. Native configuration remains
the authority for ordinary caching/incremental analysis. PGMCP does not force caching
on or duplicate native settings in its own configuration.

An explicit `fresh` request requires analysis without reuse of earlier analysis
results for the selected scope. It does not expand scope or authorize source writes
or shared-cache deletion. Workspace-wide fresh checking requires workspace scope as well.
A check that never reuses analysis already meets this intent. Unsupported fresh
semantics must be identified before that substantive check and never reported as met.
Concrete boolean/default projection and mixed-profile handling are still workshop work.

Cached operation reports, logs and invoked adapter provenance remain supported.
They describe completed runs; they are not permission to skip new execution.
A formatting-only result cannot certify syntax or erase an earlier syntax failure.
PGMCP does not build an unresolved-failure registry to enforce that reporting boundary.

### 7.12 Rejected structures and preservation evidence

The previous auto-state, shared-result-reuse, and prepare/execute proposals are
withdrawn, not optional extension features. Adapter authors are not required to supply
work IDs, sessions, dependency-validity keys, or a semantic invalidation engine.
Native optimization retains the useful performance seam without that generic machinery.
The supporting investigation and alternatives remain in
[Research evidence](research-findings.md#f-20-narrow-amendment--bounded-retesting-and-native-optimization).

Required public-boundary evidence:

- missing scope and obsolete auto input reject before adapter execution, including
  requests based on stale client metadata; profile/fresh cannot supply missing scope;
- retained branch/workspace/path selection and expansion authorization remain truthful;
- repeating a request invokes the adapter again, while report resources remain readable;
- normal execution respects native configuration; supported fresh is honored and
  unsupported fresh is not silently downgraded;
- auto-only state responsibilities disappear without affecting unrelated state/recovery.

Scope authorization before substantive checking remains necessary. The next workshop
must settle a simple bounded request/response contract for that purpose without
reintroducing the rejected preparation/session machinery. Native cache-write policy,
concurrent input changes, mixed-profile outcomes and precise result projection remain
explicit open contracts, not guarantees inferred from a successful process exit.

### 7.13 Contract work to complete

#### Approved single-invocation responsibility split

The human owner approved a single bounded check request/response as the default
interaction, without preparation sessions or persisted intermediate results.
PGMCP supplies the selected input, fresh intent and bounded execution permission.
The adapter determines what its native tool requires and checks that requirement
against the supplied permission before substantive execution. It executes only when
the requirement fits, then reports actual checked scope. Otherwise it does not run
the substantive check and reports the required expansion. A caller can authorize a
new request; the earlier response is not a retained execution plan or authorization.

PGMCP owns permission; the adapter owns native-tool requirements. Supporting context
reads retain section 7.8's distinction from broader checking. These are contractual
obligations of trusted adapters, not a claim that response validation can undo an
unauthorized subprocess execution. Generic bounds validation, conformance evidence,
and the exact request/result shapes remain to be completed before integration.

Required evidence covers execution within permission, denied expansion with no
substantive execution, truthful actual coverage, and a new authorized invocation
re-evaluating current inputs rather than consuming a stale prepared plan.

#### Approved scope-refusal outcome

When a check requires expansion that the caller has not authorized, its outcome is
`not_executed`, with a distinct scope-restriction reason, not `failed` or `unavailable`.
The response identifies the affected check, the required scope, and a short factual
explanation. PGMCP uses check identity for result association and the scope for generic
bounds validation; the agent uses the reason and required scope to request informed
authorization. Exact field names and reason codes remain part of the complete result
contract, not independently fixed by this semantic agreement.

No substantive check has run in this refusal case. The reported required scope is
not actual checked coverage and confers no permission. After authorization, a new
ordinary request re-evaluates current input; there is no resume token or retained plan.
Presentation follows the existing operation-result boundary, not tool-input schema
explanations or the deferred startup-health route. Conformance evidence must observe
the absence of substantive execution on refusal, not merely inspect a claimed status.

#### Workspace vocabulary and orthogonal profile selection

The [human-approved Research clarification](research.md#human-approved-scope-terminology-clarification)
names the whole-workspace scope `workspace`; V3 rejects `project` rather than treating
it as an alias. Coverage retains applicable inclusion/exclusion and check applicability.
Explicit files/directories and branch selection bound where checks are requested.
Profiles independently select which checks run and may be language-specific or mixed.
Adapters determine applicability; there is no extra language-selector field or special
profile type. Neither directory selection nor a native tool's configuration boundary
creates a named PGMCP subproject. Prove workspace vocabulary and project rejection
through startup schemas and runtime validation, and profile/scope independence through
public consumer cases without imposing a server-owned language taxonomy.

#### Approved explicit target selection

The human owner selected `targets` rather than `paths` to name the files and
directories requested for checking. The V3 scope values are `targets`, `branch`,
and `workspace`; scope remains required. Only `scope: targets` accepts and requires
a non-empty `targets` list of workspace-relative file/directory paths. The list must
be omitted for branch/workspace requests. File and directory entries may be mixed;
directory selection is recursive and overlapping selections are deduplicated.
A missing explicit target is an input error, not an empty successful selection.

The name expresses what the caller wants checked without suggesting directory-only
input. It does not add named subprojects, a language filter, or expansion permission.
Startup schemas, runtime validation and scope resolution consume this contract;
profiles continue to select checks independently. Public-boundary evidence must cover
mixed file/directory input, recursive and overlapping selection, missing targets,
empty lists, and forbidden targets with branch/workspace. Interaction with exclusions,
symlink containment, and concurrent filesystem changes remains explicit Design work.

#### Approved native exclusion boundary

Native configuration and its native interpretation remain authoritative; passing an
explicit target must not silently introduce an alternative PGMCP rule configuration.
An exclusion governing native discovery is not automatically an absolute prohibition
on explicit-file analysis. Known exclusion information returned by the native tool
is preserved rather than rewritten as evidence that the excluded target passed.
Exclusion differs from non-applicability: relevant input can be excluded by policy,
whereas a capability can have no applicable input in the requested selection.

This agreement does not prescribe a parser for native configuration or require generic
PGMCP to emulate native discovery. No skipped-file list or exclusion reason may be
fabricated. The subsequent native-first agreement below supersedes any reading of
this section as mandatory per-file participation accounting or additional inspection
runs. No exclusion-override flag or new result status is approved by this paragraph.

#### Binding native-first workshop constraint

The human owner explicitly requires thin generic infrastructure and adapters. Native
tools own selection, exclusion semantics, rule application and optimization. Adapters
invoke them appropriately and convey available results without recreating those
behaviors. PGMCP retains its own authorization, workspace access, mutation and recovery
responsibilities. Neither a dependency-validity engine nor mandatory per-file coverage
administration is introduced to make PGMCP appear more authoritative than its tools.

Results need not conform to one universal findings/test/fix structure. Standardize only
information a concrete consumer needs to perform its responsibility; retain native
evidence in its appropriate form under the existing presentation/cache boundary.
Process launch, timeout and crash facts remain distinct from native analysis verdicts.
No selected input, successful process exit, or empty diagnostics alone licenses a
stronger assertion than the native contract supports. Additional native inspection
is not a default requirement for adapters.

DI-04's small persistence-decision status contract remains binding for scaffold
validation; it is not automatically the full result schema for run_checks, run_tests,
or apply_fixes. Safe-edit profile-selection integration remains open in DI-04; its
enforce/report policy is fixed in DI-04 §4.6. The rejected proposal to require participation proof for every explicit file
is not an extension-conformance obligation.

Every following workshop must identify the consumer and its concrete decision before
adding a field or translating a native result. First ask whether the native tool
already owns the behavior and whether additional PGMCP complexity is justified.

#### Proposed-content execution routes

Human-approved nucleus (2026-09-06): known execution needs receive a small, explicit
generic route, not a general catalog of every external-tool limitation. The selected
check declaration drives route selection before execution. Do not materialize every
scaffold merely because some native tools require a file.

| Route | Generic PGMCP responsibility | Adapter responsibility |
|---|---|---|
| Direct content | Supply proposed text and the intended target context without creating a content file | Pass content through the tool's native API/stdin mechanism; preserve native configuration authority |
| Temporary file | Create a run-owned file with the intended basename/extension under the centrally resolved validation directory; supply physical and intended locations; own cleanup on completion/failure/cancellation | Translate those locations to native options, such as a logical filename, base URL or exact remap; do not reimplement native link/configuration semantics |

This scratch file is execution infrastructure, not the artifact's temporary persistence
destination in DI-04. It grants no permission to create or overwrite the intended target.
Neither route promises that every tool can inspect every proposed input. An adapter may
solve additional limitations in its own code within granted access/write boundaries,
or report a specific inability to check; it may not silently create target files or
invent a passing verdict. Known file needs must not be hidden behind the direct route.
Manifest declarations are a contract, not an OS sandbox or self-granted write permission.

**Approved minimal field (2026-09-06):**
`roles.check.capabilities.<id>.requires_file` is a required boolean for a check declared
to accept proposed content, with no implicit default. The generic check executor is
its consumer: `false` selects direct content delivery without a temporary content file;
`true` requests controlled temporary materialization. Missing or non-boolean values
are configuration errors, not runtime fallback choices. It belongs per check,
not package-wide, and is not duplicated in `checks.yaml`, profiles or caller inputs.
It does not choose a subprocess transport or describe existing-file, test or fix input.
Do not add per-tool limitation booleans or an automatic fallback to target writes.
Applicability to existing-file-only checks and complete conditional schema validation
remain part of the capability-schema workshop. The earlier `content_input: text | file`
proposal is superseded: the executor needs one yes/no materialization decision, not
an enum reserved for speculative future routes.

Bounded feasibility evidence, executed on Windows on 2026-09-06:

| Native tool | Observed evidence | Design implication |
|---|---|---|
| markdownlint 0.41.1, MD051, string API | Correctly rejected the missing TOC anchor; does not check filename-prefixed links | A direct-content route is useful; do not confuse limited rule coverage with a materialization problem |
| markdown-link-check 3.15.0 | Accepted missing fragments in existing file links; changing base location did not add fragment checks | Target persistence would not repair this coverage limitation |
| Lychee 0.24.2, offline, cache disabled, fragments enabled | A temporary document plus full intended file URL as base and an exact self-URL remap accepted all three valid references and rejected all four invalid references; a valid-only control returned exit 0 | The combined TOC/self-file/relative-neighbor case needs no target pre-write; native translation belongs in the adapter |
| Same Lychee version, Markdown stdin with full intended file URL and no remap to a physical source | Examined all seven references; neighbor checks worked, but valid self-references failed because the target did not exist | Stdin support alone does not prove file-free execution of this check |

The seven-reference fixture contains valid/invalid `#anchor`, valid/invalid
`installatie.md#anchor`, a valid neighbor anchor, a missing neighbor anchor, and a
missing neighbor file. The intended source file remained absent. These are bounded
native-tool observations, not official adapter selection or universal conformance.
Independent adapter evidence must reproduce positive and negative cases, no content
file for the direct route, target non-mutation, and scratch lifecycle behavior.
Cleanup policy is defined below; no crash-proof cleanup claim is made here.

#### Central temporary path authority

Human-approved refinement (2026-09-06): use the existing configurable server root,
not a new `execution_temp_dir` or independent temp-root setting. One central resolver
derives `resolved_temp_root = resolved_server_root / "temp"`; proposed-content files
belong under its fixed `validation` subdirectory. The name describes their purpose,
not execution of their contents. Runtime consumers receive resolved paths rather than
assembling them separately. The existing config-root override is unaffected.

DI-04's persisted temporary artifacts use the sibling `artifacts` directory, as defined
in [its path authority](design-mutation-validation.md#32-chosen-configuration-authority).
Its formerly designed `temporary_root` configuration field is removed. Both directories
follow a changed server root automatically. No per-adapter path override is introduced,
and validation cleanup owns neither the whole temp root nor the artifacts directory.
The cleanup contract below separates validation from housekeeping.

#### Per-check temporary isolation

Human-approved requirement (2026-09-06): every separate check invocation requiring a
file owns a fresh ID subdirectory under `resolved_temp_root / "validation"`. Repeating
the same check with identical content and target still receives a newly generated ID;
the ID is not a check-type name, content hash, template identity or reusable session key.
Checks within one profile do not share a directory. Concurrent server instances must
not claim the same existing directory. The intended basename/extension is preserved
inside the allocated directory. The direct-content route creates no such directory.

Allocation must use exclusive directory creation: an existing candidate is never
adopted, emptied or overwritten; a collision requires a fresh candidate or a safe
allocation failure. A fresh high-entropy identifier plus exclusive allocation provides
practical cross-run uniqueness and deterministic protection against live/leftover path
collisions, without historical-ID storage or reuse machinery. Verification covers
repeated identical checks, concurrent invocations and an intentionally forced collision.
Exact identifier encoding remains an implementation detail; no absolute mathematical
claim of never repeating a previously deleted random identifier is made.

#### Scaffold consumer input nucleus

The scaffold-specific input nucleus is recorded after human agreement to resume and
complete this boundary (2026-09-06). It does not settle safe-edit or run_checks inputs,
nor the complete check/v1 transport envelope, selection and provenance fields.

| Field | Scaffold meaning | Consumer |
|---|---|---|
| `target_path` | Full absolute intended file path in the adapter's execution environment; the file need not exist | Adapter native filename/base-location/configuration translation |
| `content` | Complete proposed text, present only for requires_file=false | Adapter forwards text through the native input mechanism |
| `input_path` | Absolute readable validation-file path, present only for requires_file=true | Adapter supplies the physical input to the native tool |

PGMCP resolves the public directory target and exact file_name before constructing
this internal file-valued target_path. Public scaffold target_path/output_path remain
workspace-relative; no public contract change or automatic exposure of host paths is
introduced. Provide exactly one of content/input_path according to the admitted check
manifest; empty text is still content, not a missing field. Do not send duplicate
authoritative copies of the proposed content. A physical input is not the intended
target and never authorizes an adapter to write that target.

A separate workspace_root field is not justified by the current scaffold evidence.
Its omission does not imply that workspace boundaries can be inferred from a filename;
another concrete consumer may demonstrate that separate need later. PGMCP retains
access/path ownership. These path fields are not a sandbox claim and do not require
future sandbox paths to equal host paths. Exact role schemas remain open.

#### Typed scaffold content input

Human-approved typing refinement (2026-09-06). The following are contract declarations,
not production implementations or the complete check/v1 request envelope:

```python
class ScaffoldTextInput(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    target_path: AbsoluteFilePath
    content: StrictStr


class ScaffoldFileInput(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    target_path: AbsoluteFilePath
    input_path: AbsoluteFilePath


ScaffoldContentInput = ScaffoldTextInput | ScaffoldFileInput
```

`AbsoluteFilePath` denotes one shared constrained domain type, not Pydantic's existing
file-existence type. Its wire representation is a strict, non-empty string describing
a fully qualified file location in the adapter execution environment. Reject null,
coerced numbers/booleans, NUL characters, relative or drive-relative paths, and a
directory-only designation. Path interpretation follows that environment, not the
calling agent's platform. This type validates representation without filesystem I/O;
it cannot prove that a syntactically valid file location is not currently a directory.
PGMCP owns that operational check together with target admission/collision policy.
The intended file and its parent may not exist yet; do not make existence a type rule.

Both fields in either model are required and have no defaults. The wire schema is
exactly one of the two closed object shapes (oneOf, each with additionalProperties=false).
Both payload fields, neither payload field, unknown fields and null values are invalid.
Empty content is valid input to a check, not an omitted field. No additional mode
discriminator or duplicate requires_file field is sent. The admitted manifest selects
the expected variant: false requires ScaffoldTextInput; true requires ScaffoldFileInput.
This is input validation, not an automatic retry or fallback between routes.

For the file route, PGMCP writes the exact proposed text as UTF-8 without adding a BOM
or translating line endings. The adapter reads that encoding. Unencodable input or
file creation failure is a preparation failure, not an empty file or passing check.
PGMCP owns validation-file allocation, containment and lifetime; the adapter handles
actual file-open/read failure because prior checks cannot guarantee continued access.

Pure immutable models own shape/type rules. The manifest loader validates declarations
at startup; the request boundary checks the selected variant before native execution.
Native invocation never starts for a malformed input. The generic framework must not
infer file ownership or write permission from an AbsoluteFilePath value alone.
Language-specific model implementations and wire schema must agree; the Python shapes
do not require adapters to be written in Python. Their schema projection must retain
closed alternatives; an unenforced format label is not sufficient path validation.

Required conformance cases: valid text/file variants; empty content; missing, null,
extra or mistyped fields; both/neither payload; manifest mismatch; relative paths;
nonexistent intended target; unavailable physical input; UTF-8/non-ASCII and unchanged
line endings; immutable Python DTOs. These models define the reusable content portion.
The complete operation-bearing scaffold requests are defined below; transport and
response sections own framing, limits and native-evidence packaging.

#### Request operation selection

Human-approved naming and selection boundary (2026-09-06): manifests describe offered
capabilities; an invocation directs the adapter to perform an operation. Retain
capability in checks.yaml as the reference to the manifest declaration. Use operation
in the adapter request, carrying exactly that selected capability identifier. Do not
add aliases, a translation table, or independently maintained operation identifiers.

| Information | Source | Direct consumer |
|---|---|---|
| operation | Resolved check binding's capability value | Selected role entrypoint dispatches the requested operation |
| target_path and exactly one of content/input_path | Existing scaffold input contract | Adapter native input/location translation |
| Workspace check ID and profile ID | Check/profile selection | PGMCP selection, aggregation and reporting; not adapter request fields |
| adapter_id and role | Resolved catalog selection | PGMCP chooses the admitted role entrypoint; not repeated for adapter dispatch |
| enforce/report | Scaffold policy | Consumer manager after collecting results; not adapter request fields |

operation is a required strict non-blank string selected from the admitted package's
capability identifiers for the selected role. Membership is exact; do not case-fold,
coerce or guess a default. Identifier grammar remains shared with the manifest, not
separately invented here. It is a root request field alongside target_path and the one
content source; the earlier closed content models describe the content portion, not
the complete operation-bearing request. The adapter need not read checks.yaml or infer
the selected operation from file type. A missing operation yields missing_field; an
unknown operation yields invalid_request with invalid_value at ["operation"] before
native work. This is not unsupported_input for an otherwise valid operation.

For the existing illustrative binding python_format -> ruff/check/format, PGMCP starts
the check entrypoint and sends operation="format". The same identifier under fix is a
different role's capability; selecting check/format never authorizes file mutation.
Conformance covers exact binding transfer, missing/unknown operation, no implicit
selection, and absence of profile/policy knowledge in adapter dispatch.

#### Contract version at the selected entrypoint

Human-approved boundary (2026-09-06): omit contract_version from the request. The
admitted roles.<role>.contract_version declaration selects PGMCP's request/response
contract for that role entrypoint. The adapter implementation implements the declared
contract; it does not negotiate or select a version per invocation. Package release
version and fingerprint remain provenance facts, not request fields or protocol-version
selectors. No multi-version dispatcher, handshake or per-call negotiation is introduced.

This omission is justified by the single declared contract per role entrypoint, not a
general claim that transmitting version information would violate SSOT. Manifest
declaration alone does not prove implementation conformance: the existing independent
adapter conformance obligations must establish agreement. Unsupported declared versions
are rejected at catalog admission; do not guess compatibility from matching fields.
Version-specific launch wiring, if ever needed, remains the entrypoint's responsibility
rather than implicit detection from request contents.

#### Complete scaffold-check request shapes

The approved operation selector extends each existing frozen content model. These are
the complete wire-field sets for the scaffold consumer slice, not the complete request
inventory for safe edit, run_checks, tests or fixes:

```python
class ScaffoldTextRequest(ScaffoldTextInput):
    operation: NonBlankText
    args: tuple[StrictStr, ...]


class ScaffoldFileRequest(ScaffoldFileInput):
    operation: NonBlankText
    args: tuple[StrictStr, ...]


ScaffoldCheckRequest = ScaffoldTextRequest | ScaffoldFileRequest
```

The inherited frozen/strict/extra-forbid contract remains in force. The wire schema
is exactly one of the closed objects {operation, target_path, content, args} and
{operation, target_path, input_path, args}. Every listed field is required. The args
tuple comes exclusively from configured default_args under §7.16; it is not public
scaffold input. Safe-edit proposed-content checks use the same argument ownership.
The selected
operation must be a declared capability of the invoked role, and its requires_file
declaration determines the permitted input alternative. This selected-contract
constraint is not a new server-side revalidation pass over its constructed request.
An empty content string remains valid; null, both content sources, neither source and
additional fields are invalid. No wrapper, mode, consumer, role, adapter identity,
profile, policy, workspace root or contract version is added to this request slice.

Illustrative Windows-environment requests below do not designate official adapter
capabilities or assert that a particular native tool supports both input routes. Each
example assumes a selected format operation with the corresponding requires_file
declaration. Paths and file contents are example data, not template inventory.

Direct content (requires_file=false):

```json
{
  "operation": "format",
  "target_path": "C:/work/demo/src/example.py",
  "content": "value = 1\n",
  "args": []
}
```

Materialized content (requires_file=true; illustrative resolved server root
C:/work/demo/.pgmcp, with a separately allocated invocation directory):

```json
{
  "operation": "format",
  "target_path": "C:/work/demo/src/example.py",
  "input_path": "C:/work/demo/.pgmcp/temp/validation/7f8bd0fe64624c4ea28c0186a3ef17b4/example.py",
  "args": []
}
```

The second example carries no duplicate content. input_path is the actual validation
file; target_path remains the intended destination, not permission to write there.
These are internal adapter paths, not new public absolute-path exposure. Neither route
falls back to the other after execution failure. Conformance proves complete field
sets, inherited constraints, operation membership and manifest-selected input shape.

The next open launch boundary is how the manifest identifies the adapter executable,
arguments and execution environment. It must support the admitted role/version without
coupling adapters to the server's Python interpreter or confusing native tool commands
with adapter entrypoints.

#### Scaffold-facing adapter decision types

Human-approved reason ownership (2026-09-06): adapter reasons describe observations
inside the adapter's native integration, not failures of PGMCP's adapter invocation.
This is the decision portion of a response; the native-evidence contract is defined
below. General process framing remains open. Contract declarations use closed immutable models:

```python
class AdapterUnavailableReason(StrEnum):
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    UNSUPPORTED_INPUT = "unsupported_input"
    INVALID_CONFIGURATION = "invalid_configuration"
    EXECUTION_ERROR = "execution_error"
    INVALID_RESULT = "invalid_result"


class ScaffoldCheckPassed(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    status: Literal["passed"]


class ScaffoldCheckFailed(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    status: Literal["failed"]
    message: NonBlankText


class ScaffoldCheckUnavailable(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    status: Literal["unavailable"]
    reason: AdapterUnavailableReason
    message: NonBlankText


ScaffoldAdapterDecision = Annotated[
    ScaffoldCheckPassed | ScaffoldCheckFailed | ScaffoldCheckUnavailable,
    Field(discriminator="status"),
]
```

`NonBlankText` is a shared strict string constraint: reject null, empty and
whitespace-only values without coercion. The message states concrete observed facts,
not preformatted tool-response prose. The existing presenter retains final wording,
path-exposure and output-budget authority. All shown fields are required, without
defaults. Passed decisions contain neither reason nor message. Failed decisions require
message but contain no generic reason code; native rule identifiers remain native evidence.
Human correction, 2026-09-07: the adapter supplies a factual rejection explanation so
bounded inline feedback is useful even when evidence is native JSON. This supersedes
the earlier message-free failed variant. The adapter owns the explanation; PGMCP does
not infer it from arbitrary evidence. The message is not a complete second finding list
or preformatted response; native evidence retains complete supporting detail.
Wire validation enforces the literal statuses and enum values as declared; unknown
values, extra fields and invalid combinations are adapter contract failures.

| Adapter reason | Required observation | Excluded interpretation |
|---|---|---|
| dependency_unavailable | A dependency of the running adapter cannot be used | The adapter process itself could not be started |
| unsupported_input | Contract-valid proposed input cannot be checked by this integration within the supplied context | Malformed adapter request or rejected artifact content |
| invalid_configuration | The native tool identifies invalid configuration preventing a verdict | Invalid PGMCP manifest or speculation about an unexplained failure |
| execution_error | Native launch/execution/read fails without a content verdict | Ordinary non-zero exit carrying a trustworthy rejecting verdict |
| invalid_result | Native output cannot yield a trustworthy verdict | PGMCP could not validate the adapter's response |

There is no adapter reason `timeout`. PGMCP owns the adapter-call time budget and
observes adapter launch failure, crash, deadline expiry and malformed response.
Those remain a separate runtime contract; never fabricate an adapter response for
them. A native tool's own reported timeout may be explained by the still-running
adapter as execution_error, without introducing a second generic timeout category.
PGMCP owns not_executed for unstarted/interrupted scaffold checks. Cleanup feedback
remains separate and non-blocking. This decision does not redefine DI-04's handling
of runtime failures or the run_checks/test/fix response schemas.

Independent evidence must cover all reason values, unknown strings, null/blank
messages, forbidden reason/status combinations and the distinction between a native
failure reported by an adapter and a failure to obtain a valid adapter response.

#### Native evidence and scaffold response shape

Human-approved evidence contract (2026-09-06), amended by W02-F on 2026-09-10: a
scaffold-facing role result has required `decision` and `external_tools` plus conditional
`evidence`. The provenance field follows §7.4.3. These are separate:
scaffolding consumes the decision for policy; agent-facing presentation and full
structured evidence consume native findings. No common rule/line/severity structure
is imposed on native payloads.

```python
class TextEvidence(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    format: Literal["text"]
    data: StrictStr


class JsonEvidence(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    format: Literal["json"]
    data: FrozenJsonValue


NativeEvidence = Annotated[
    TextEvidence | JsonEvidence,
    Field(discriminator="format"),
]
```

`FrozenJsonValue` is the immutable in-memory representation of the recursive JSON
value contract: null, boolean, string, finite number, array of JSON values or object
with string keys and JSON values. It is not Any and adds no native property semantics.
Wire arrays/objects remain ordinary JSON; validated domain collections must be
recursively immutable. A frozen outer Pydantic model alone is insufficient for nested
lists/dicts. Reject non-JSON objects, non-finite numbers and representation coercions.
Exact immutable collection implementation remains implementation-owned.

| Decision variant | Evidence presence | Explanation requirement |
|---|---|---|
| passed | Optional; omit when absent | A native tool may accept without findings |
| failed | Required | Required decision.message supplies a concrete rejection explanation; native evidence supplies its supporting detail, not only an exit code or empty report |
| unavailable | Optional; omit when absent | Mandatory decision reason/message already explain inability; evidence may add native detail |

The outer response is closed: only decision, evidence and external_tools, with no
unknown fields. If present, evidence must match one of the closed shapes; null is not
an absent evidence object (JSON data itself may legally be null). The decision/evidence
combination is validated as a cross-field rule. Evidence significance is an adapter
conformance obligation: generic code does not interpret arbitrary native JSON to
invent findings or prove completeness. An empty payload does not satisfy failed-case
explanation merely because it is valid JSON. Missing required evidence is a response
contract error, never an accepting verdict.

When a tool offers both native text and JSON, prefer the most informative suitable
form rather than duplicating both by default. Raw stdout/stderr remain process
diagnostics and are not automatically copied into evidence. The evidence format is
not a request for a second persistence/resource system: existing presentation, cache,
path-exposure and output-bound policies continue to govern consumer-facing delivery.
This defines the scaffold role-result payload only, not all check/test/fix consumer
outputs. The standard response also admits invalid_request, as defined below; that
variant contains none of decision/evidence/external_tools.

Conformance covers each format, unknown format values, wrong data types, unknown
wrapper fields, nested JSON immutability, missing failed evidence/message, blank messages,
message-to-evidence consistency, and preservation of native detail without forced
normalization. Real public projection must display the supplied rejection message
through existing scalar/collection presentation without native JSON parsing. Transport-size policy remains separate
protocol work; PGMCP-owned call failures are defined below.

#### PGMCP-owned adapter call failures

Human-approved runtime boundary (2026-09-06), refined by the shared invocation result
below: a non-cancelled adapter-call observation is either a validated adapter response
or a PGMCP-owned call failure; cancellation has its own result variant. Never manufacture
an adapter decision/evidence object when no valid response was obtained. This failure
type is separate from AdapterUnavailableReason:

```python
class AdapterCallFailureReason(StrEnum):
    LAUNCH_FAILED = "launch_failed"
    TIMEOUT = "timeout"
    PROCESS_FAILED = "process_failed"
    INVALID_RESPONSE = "invalid_response"
    RESPONSE_TOO_LARGE = "response_too_large"


class AdapterCallFailure(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    reason: AdapterCallFailureReason
    message: NonBlankText
```

All fields are required; unknown values, null/blank messages, extra fields and
coercions are invalid. The runtime owns construction of this type. It is not an
allowed adapter response variant. Process diagnostics remain separately available
under the existing presentation/cache contract.

| Reason | Runtime observation |
|---|---|
| launch_failed | The adapter process could not be started |
| timeout | The adapter-call time budget expired |
| process_failed | The adapter process terminated abnormally |
| invalid_response | The adapter response is missing or violates the response contract |
| response_too_large | Adapter stdout exceeded the formal response byte ceiling during receipt |

For a bounded, recognized call failure, DI-04 records that check as unavailable,
preserving runtime origin and the specific failure rather than attributing it to the
adapter. Independently executable selected checks continue. Existing enforce/report
policy applies to the collected evidence; report can permit creation only when other
operation conditions hold. A schema-invalid adapter output is invalid_response, but
PGMCP's own malformed request/configuration is an operation defect, not a suppressed
runtime unavailability. No arbitrary catch-all conversion of server exceptions is allowed.

Cancellation of the scaffold operation is not timeout of an individual call:
unfinished checks follow not_executed and the operation does not persist. Preparation
failures also remain operation failures. Cleanup errors remain non-blocking housekeeping.
This separation neither changes DI-04 aggregation nor turns runtime failure into an
adapter-authored reason. Completion and time-budget ownership are defined below;
response/diagnostic byte limits are defined below; remaining transport details remain
protocol work.

Conformance covers each failure reason and its runtime provenance, schema-invalid
adapter output versus malformed PGMCP input, per-call timeout versus operation
cancellation, continuation of independent checks, and unchanged enforce/report mapping.

#### Single-request input transport

Human-approved transport (2026-09-06), shared by check/test/fix: PGMCP starts the
configured role entrypoint, writes one complete UTF-8 JSON request to stdin, then
closes that input channel. EOF marks the end of the request, not cancellation. The
adapter reads and validates the complete request against the selected role contract,
handles that one invocation, emits one formal UTF-8 JSON response and terminates under
the existing completion rules.

JSON may span multiple lines. No line delimiter, length prefix, acknowledgement,
persistent session or second request is introduced. The existing call deadline covers
request delivery as well as response/completion; waiting for input consumption must
not bypass it. Output streams remain serviced during delivery under the bounded
capture rules. This transport does not prescribe how the adapter communicates with
its native tool.

Conformance covers multiline and non-ASCII requests, stdin closure without cancellation,
one invocation per process, and bounded delivery to an adapter that does not consume
input. Invalid-request ownership and response placement are defined below.

#### Request validation and rejection ownership

Human-approved correction (2026-09-06): PGMCP constructs the contract's typed request
model, enforcing its constraints at construction. Do not add a second validation pass
over that same model immediately before serialization/transmission. The receiving
adapter validates the received JSON at the process boundary before invoking its native
tool. This is boundary validation, not duplicate server-side validation.

An invalid request is represented by an explicit error variant within the standard
adapter output contract, shared across check/test/fix, with the closed reason
invalid_request and typed validation details. It is not a separate response channel,
standalone error protocol, or a check decision of failed/unavailable. The adapter starts
no native work for a rejected request. Do not infer this rejection by parsing stderr.

PGMCP-owned malformed input remains an operation/contract defect and must not become
ordinary runtime unavailability suppressed by scaffold report policy. Merely receiving
a rejection does not prove which implementation is defective; preserve the adapter's
structured report without claiming that it independently proves PGMCP sent bad input.
Consumer managers own the operation consequence; tools and presenters do not synthesize
it. Rejection uses exit 2 under the shared mapping below. Its exact field contract is
defined in the following section.

Conformance distinguishes valid construction, adapter-side rejection before native
execution, and typed rejection preserved through the existing output/presentation
route without stderr interpretation or a second server-side validation layer.

#### Complete scaffold-facing standard output contract

Human-approved shape completion (2026-09-06): one response is exactly one of four
logical alternatives. Preserve the existing role-result wire fields; do not add an
outer status, success flag, role label, exit_code field or second error channel.

| Alternative | Required root fields | Optional root fields | Exit |
|---|---|---|---|
| Passed | decision: ScaffoldCheckPassed; external_tools: tuple[ExternalToolIdentity, ...] | evidence: NativeEvidence | 0 |
| Failed | decision: ScaffoldCheckFailed; evidence: NativeEvidence; external_tools: tuple[ExternalToolIdentity, ...] | None | 1 |
| Invalid request | reason: Literal["invalid_request"]; details: non-empty tuple of RequestValidationIssue | None | 2 |
| Unavailable | decision: ScaffoldCheckUnavailable; external_tools: tuple[ExternalToolIdentity, ...] | evidence: NativeEvidence | 3 |

All alternatives are closed: fields outside the applicable row are forbidden, and
explicit null is not an omitted optional evidence field. NativeEvidence and the three
decision types retain the exact definitions and cross-field obligations above. The
invalid-request shape has none of decision, evidence or external_tools. Its reason distinguishes it
from role results without adding redundant fields to all responses.

```python
class RequestValidationCode(StrEnum):
    MISSING_FIELD = "missing_field"
    WRONG_TYPE = "wrong_type"
    INVALID_VALUE = "invalid_value"
    UNKNOWN_FIELD = "unknown_field"


RequestLocationPart = StrictStr | Annotated[StrictInt, Field(ge=0)]


class RequestValidationIssue(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    location: tuple[RequestLocationPart, ...]
    code: RequestValidationCode


class AdapterInvalidRequest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    reason: Literal["invalid_request"]
    details: Annotated[tuple[RequestValidationIssue, ...], Field(min_length=1)]
```

Both issue fields and both rejection fields are required. Locations serialize as JSON
arrays; strings are object keys and non-negative integers are array indexes. An empty
location identifies the request root. Do not use dot-delimited paths, numeric-string
index coercion or validator-specific union branch labels. Missing/unknown-field
locations include the relevant field name even if the field has no accepted value.
Details preserve immutable domain collections and serialize as a non-empty JSON array.

| Code | Meaning and boundary |
|---|---|
| missing_field | A contract-required field is absent |
| wrong_type | A present value has the wrong JSON type, including disallowed null |
| invalid_value | A value violates an allowed-value or other contract constraint; malformed JSON/UTF-8 identifies the root because no valid request value can be established |
| unknown_field | A field is not permitted by the applicable closed request shape |

These codes are adapter-contract vocabulary, not Pydantic or another library's error
identifiers. The adapter maps its boundary validator's observations to them; PGMCP does
not repeat request validation to reconstruct details. For cross-field constraints use
the relevant containing object when no single field owns the violation. No received
value, free-form message, raw library error object, recovery field or retry hint is
added. The existing request contract supplies expected field types/allowed values;
presentation can identify the location and category from these typed facts.

Example of a missing content field (illustrating an invalid request, not a new template):

```json
{
  "reason": "invalid_request",
  "details": [{"location": ["content"], "code": "missing_field"}]
}
```

The response schema must express exactly-one-of the four rows, not an unconstrained
dictionary or an object with every field optional. Frozen domain response types must
enforce the same alternatives. A schema-valid mixed decision/reason object, empty
details or null evidence is not allowed. The shared InvocationCompleted response type
must encompass the role-result and invalid-request alternatives through its concrete
validated response model; it must not wrap an unchecked union/dictionary merely to
satisfy its BaseModel bound. This is one standard response schema, not additional public
tool registrations. Test/fix reuse the rejection type without adopting scaffold result
fields. Their role-result shapes remain separately owned.

Conformance covers all four alternatives and their exit pairs, forbidden mixed fields,
unknown codes, empty details, root/nested/index locations, strict index types, omitted
versus null evidence, and preservation of typed details through cache/presentation.
Do not require identical error ordering or exhaustive error enumeration across validator
implementations; every reported issue must be factual and at least one must be present.

#### Adapter response completion

Human-approved completion rules (2026-09-06): PGMCP accepts a scaffold-check adapter
response only when exactly one complete contract-valid JSON object has been received,
the adapter process exits with a documented code matching that response, and call
completion occurs within its time budget. A matching non-zero code may carry a valid
error response; non-zero alone does not establish process_failed.
Completion also requires the managed invocation's associated subprocess work to have
finished, as defined under managed invocation termination below.
Receiving JSON alone is not completion. No streaming or separate acknowledgement
protocol is introduced.

Stdout is reserved for that JSON object with optional surrounding whitespace; missing,
multiple, malformed or schema-invalid responses are not accepted. Extra startup or
other non-JSON text violates the protocol; PGMCP does not extract a JSON object from
contaminated stdout to salvage a response.

Human-approved channel clarification (2026-09-06): stderr is exclusively optional
supplemental error diagnostics, not a logging or notification channel. Startup banners,
progress messages and informational logging are prohibited on both channels. Stderr
presence alone does not determine the outcome or invalidate a valid response; the
formal response and completion rules remain authoritative. Generic PGMCP code does
not classify free-text stderr to enforce this distinction; adapter conformance owns
compliance with its error-only purpose.

The adapter captures native stdout/stderr and interprets them under the native tool's
contract. It must not blindly forward either stream: native informational output does
not become permitted adapter stderr merely because the native tool emitted it there.

Human-approved correction (2026-09-06): exit code and typed response jointly express
the invocation outcome. This supersedes the earlier exit-zero-only acceptance rule and
the assignment of all decision variants to exit 0. Define a small shared exit-code
contract, not one code per detailed error or per native tool. The adapter translates
native tool exit semantics instead of blindly forwarding them. The following mapping
records the user-delegated numeric design selection (2026-09-06).

#### Shared adapter exit-code mapping

| Exit code | Meaning | Required matching response in the established scaffold contract |
|---|---|---|
| 0 | Successful role result | decision.status = passed |
| 1 | Negative role result, with usable evidence | decision.status = failed, with required message and native evidence |
| 2 | Request violates the adapter input contract | Standard output's invalid_request error variant with typed validation details; no native work |
| 3 | Adapter cannot produce a trustworthy role verdict/result | decision.status = unavailable with one of the existing AdapterUnavailableReason values and its required message |

These are four exit categories, not four new response statuses. All five established
unavailable reasons share code 3; do not allocate a code per reason. unsupported_input
is code 3 for contract-valid input the integration cannot handle, not code 2. A failed
content check is code 1, not invalid_request. A native execution_error reported by a
running adapter is code 3, not PGMCP's process_failed.

```python
class AdapterExitCode(IntEnum):
    SUCCESS = 0
    NEGATIVE_RESULT = 1
    INVALID_REQUEST = 2
    UNAVAILABLE = 3
```

Keep this numeric vocabulary shared by check/test/fix. Role response contracts bind
their own existing outcomes to it; they must not copy scaffold-specific decision fields
into test/fix payloads. Exact test/fix payload combinations remain owned by those role
contracts, not invented here. In particular, successful fix proposal production does
not assert that PGMCP has applied the proposal. Generic process management consumes the
selected contract's code/response validation; it does not interpret native evidence or
introduce per-tool/language branches. The exit code is observed from the process, not
duplicated as an authored JSON field or configurable manifest mapping.

Codes 0 through 3 all require a complete matching response and timely, confirmed
completion. Unknown codes and abnormal termination follow process_failed; missing or
mismatched responses with a documented code follow invalid_response. No crash code,
timeout code, cancellation code or cleanup code is added: those observations retain
their existing PGMCP-owned lifecycle handling. A recognized number alone never proves
that the adapter deliberately returned the corresponding outcome.

The distinction between 1 and 3 preserves the existing difference between a negative
verdict and inability to obtain a verdict. Code 2 separates bad requests from both.
Conformance covers all four valid pairs, all five unavailable reasons sharing code 3,
code/response mismatches, missing payloads, unknown exits, and native codes translated
instead of forwarded. Keep tests focused on this observable contract, not enum storage.

Do not add recoverable flags, a recovery taxonomy or automatic retry machinery.
Concrete typed reasons provide the needed information without claiming who can recover
or authorizing recovery actions. A valid error response is usable evidence, not evidence
that the requested check, test or fix succeeded. The existing generic completed outcome
means contract-compliant completion and may carry such an error variant within the
standard response. Consumer managers retain consequence ownership.

| Observation | PGMCP outcome |
|---|---|
| Valid response, matching documented exit code, timely completion | Accept the adapter response, including a contracted error response with non-zero exit |
| Response followed by abnormal termination or an undocumented exit code | process_failed; do not accept the response as a final verdict |
| Documented exit code with missing/invalid or mismatched response | invalid_response; the code alone is insufficient |
| Response received but process does not finish before the deadline | timeout |
| Scaffold operation cancelled before completion | Operation cancellation, not a per-call timeout; unfinished checks follow not_executed |

For failed calls, captured response bytes may remain diagnostic evidence but are not
an accepted decision. An abnormal termination takes precedence over parsing partial
output as invalid_response; a runtime-enforced timeout is not relabelled process_failed
merely because termination produces a non-zero exit. Once a call is accepted, its
verdict is not retroactively invalidated by separate cleanup failure. Process/stream
handling must not wait indefinitely after receiving an object; bound completion by
the call budget. Exact termination mechanics remain runtime design.

Conformance includes valid JSON then crash, valid JSON then hang, known exit without JSON,
multiple JSON objects, stdout log contamination, supplemental error diagnostics that
do not change a valid response, absence of routine adapter logging on stderr, and a
native rejecting exit translated under the shared adapter contract. Also cover accepted
non-zero/error-response combinations, code/response contradictions and preservation of
typed error details without recoverability fields or automatic retries.

#### Scaffold-check time budget

Human-approved direction (2026-09-06): the configured check binding in checks.yaml
owns `timeout_seconds`, not the adapter manifest, template package, output profile or
native tool configuration. Its type is a required strict integer greater than zero,
without an implicit default. Reject booleans, numeric strings and non-positive values
at configuration admission. A sample value such as 30 does not establish a universal
default or select migration values for existing checks.

The generic runtime consumes this budget for each adapter invocation. Measurement
starts immediately before process launch and covers launch, request delivery, native
work, complete response receipt and normal adapter-call completion. Temporary input
preparation and subsequent housekeeping are outside this budget. Scaffolding adds
no caller-level timeout override or duplicate profile/package setting in this slice.

On expiry, stop accepting a later verdict and terminate the owned invocation, including
native subprocess work, then report the existing runtime timeout. Termination overhead
means this is not an exact upper bound for the complete scaffold-tool response. Stopping
must itself be bounded; the approved behavior and internal stop budget are defined
below, while platform implementation remains open. Do not automatically retry,
raise the budget or rewrite the native tool's own timeouts. Independently executable
checks and existing enforce/report policy retain their approved behavior.

Conformance covers configuration typing, per-call timing (including response followed
by a hanging adapter), late-output rejection and unchanged native timeout settings.
Public run_checks/test/fix timeout controls are not settled by this scaffold slice.

#### Shared process diagnostics and consumer ownership

Human-approved responsibility boundary (2026-09-06): check, test and fix use the same
generic process-management diagnostics contract. The generic layer detects and types
process observations, including timeout, cancellation and unconfirmed termination.
It does not require tools to reconstruct reasons from exceptions, exit codes or text.

| Owner | Responsibility | Exclusion |
|---|---|---|
| Generic adapter process management | Detect process outcomes, execute bounded stopping and produce canonical typed process diagnostics | Scaffold persistence decisions, test verdict interpretation, fix recovery policy or presentation wording |
| Consumer manager | Apply its domain policy and report its actual consequences while retaining original process diagnostics | Relabel process observations or manufacture adapter decisions |
| Public tool | Forward validated requests and transfer the manager result, using structural adaptation only where necessary | Detect or formulate manager problems, infer outcomes, select recovery policy or construct user-facing messages |
| Presenter and presentation configuration | Declaratively project supplied facts through generic mechanisms | Domain decisions or concrete diagnostic-type branches |

Reuse the inward-owned, frozen diagnostic record directly where the public output
contract permits it, following issue 456's canonical validation-record pattern. Any
necessary structural adaptation preserves meaning, provenance and detail; a tool must
not create competing diagnostic definitions. Domain services do not import tool-output
DTOs. Cache publication preserves the complete consumer result before presentation.

For example, termination_unconfirmed is established by generic process management;
the fact that no scaffold was persisted is established by the scaffold manager. Test
and fix managers consume the same process observation but own their distinct result
and recovery consequences. Do not generalize 'nothing was written' from scaffolding
to test execution or fix application. This boundary does not settle those consumers'
remaining policies or change the earlier approved scaffold stop behavior.

The shared manager contract is refined below. The earlier scaffold-specific
field sketch does not define that shared record: check identity and temporary-input
ownership must not become mandatory fields for unrelated test/fix invocations.
Conformance proves shared observations survive consumer/tool transfer unchanged and
that tools do not reclassify them or synthesize consequences.

#### Preserve the original outcome alongside termination problems

Human-approved shared result semantics (2026-09-06): preserve the original invocation
outcome and add termination_unconfirmed only when process management cannot confirm
termination. The additional diagnostic does not replace timeout or cancellation and
does not become an adapter-authored response. Generic process management constructs
both observations; consumer managers and tools must not reconstruct them from prose.

| Observation | Original outcome | Additional process diagnostic |
|---|---|---|
| Valid response and complete managed invocation | Accepted adapter response | None |
| Deadline expired, termination confirmed | timeout | None |
| Deadline expired, termination unconfirmed | timeout | termination_unconfirmed |
| Cancellation, termination confirmed | Cancellation | None |
| Cancellation, termination unconfirmed | Cancellation | termination_unconfirmed |

Existing launch_failed, process_failed and invalid_response observations remain.
Associated subprocesses must not be ignored when handling an abnormal adapter exit
or invalid response; apply the same managed-termination obligation when needed.
No accepted response may coexist with unconfirmed completion. Captured late or partial
response bytes may remain diagnostics, never an accepted verdict.

Do not add a successful-termination diagnostic to ordinary completed calls or duplicate
outcomes through timed_out/cancelled/stopped/failed booleans. Completion guarantees
belong to the shared contract. The additional diagnostic is needed because timeout
alone does not establish whether stopping succeeded, while termination_unconfirmed
alone loses the original cause. Consumer policy remains separate: for scaffolding,
unconfirmed termination prevents persistence even when report would permit an ordinary
confirmed timeout. Test/fix consequences remain owned by their consumer managers.

The table defines semantics, not an untyped dictionary API. Exact frozen types and
serialization must preserve these combinations without opening free-form reason/status
fields, duplicating the original cause, or creating a new presentation protocol.
Conformance distinguishes confirmed and unconfirmed termination after both timeout
and cancellation, preserves original outcomes through transfer/cache, and excludes
fabricated successful-completion records.

#### Typed shared invocation result

Human-approved manager contract (2026-09-06): use three closed, frozen result variants.
They belong to generic adapter process management and are not three new public tool
response registrations. Reuse the existing AdapterCallFailure record above.

```python
TResponse = TypeVar("TResponse", bound=BaseModel)


class TerminationProblem(StrEnum):
    UNCONFIRMED = "termination_unconfirmed"


class InvocationResultBase(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class InvocationCompleted(InvocationResultBase, Generic[TResponse]):
    outcome: Literal["completed"]
    response: TResponse


class InvocationFailed(InvocationResultBase):
    outcome: Literal["failed"]
    failure: AdapterCallFailure
    termination_problem: TerminationProblem | None


class InvocationCancelled(InvocationResultBase):
    outcome: Literal["cancelled"]
    termination_problem: TerminationProblem | None
```

The consumer receives a union discriminated by outcome, specialized with the concrete
role response model. Never instantiate it with an arbitrary dictionary or an unbound
BaseModel payload; the accepted check/test/fix response retains its own validated,
immutable contract. Completed means protocol and managed-process completion, not that
content passed validation, tests passed, or a fix was applied.

All shown fields are required. termination_problem is explicitly null when no such
problem was established. Completed cannot contain failure or termination_problem;
failed/cancelled cannot contain response. Unknown fields, discriminator values, reason
values and coercions are rejected. A launch_failed observation in which no process
started cannot carry termination_unconfirmed. Enforce that cross-field invariant at
the result boundary, not in consumer tools. Any partial-launch cleanup must be handled
truthfully rather than misclassified as a no-process-started observation.

Late/partial output is diagnostic evidence only. Cancellation remains an internal
lifecycle outcome and does not guarantee a response can still reach a cancelled MCP
client. Cancellation propagation must not silently become ordinary successful execution.
These variants introduce no check identity, temporary-input ownership, persistence
decision, recovery instruction or presentation text. Those remain at their established
boundaries. Existing raw diagnostic transport is not redefined by these result fields.

Conformance exercises all three variants and permitted termination combinations,
role-specific response typing, nested contract immutability, extra/unknown/coerced
fields, missing versus explicit-null termination_problem, the no-process launch
invariant, and direct preservation through consumer-manager and tool transfer.

#### Managed invocation termination

Human-approved lifecycle boundary (2026-09-06): generic PGMCP process management owns
starting, waiting for and stopping the adapter invocation and its associated native
subprocess work. Native tools retain parallel-work scheduling; PGMCP neither schedules
individual pytest workers nor introduces per-worker time budgets. Adapters need no
separate stop protocol or lifecycle manifest switches.

The current workspace provides concrete motivation: [pytest configuration](../../../pyproject.toml)
selects `-n auto`, while [PytestRunner](../../../mcp_server/managers/pytest_runner.py)
uses subprocess.run without group termination. The [test tool](../../../mcp_server/tools/test_tools.py)
awaits that runner through asyncio.to_thread without a process-stop cancellation path.
Source inspection establishes a lifecycle gap, not evidence that every cancelled run
leaves processes behind. Existing parser/unit doubles do not prove process-tree cleanup.

Per-call timeout and whole-operation cancellation use the same bounded stop mechanism,
but retain different consumer outcomes. Sending a stop request is not confirmation of
termination. Receiving adapter JSON or observing only its exit is insufficient while
associated managed work remains active. No late verdict is accepted after timeout.

| Observation | Scaffold consequence |
|---|---|
| Timely valid response, matching documented adapter exit code, associated work finished | Accept the response, including a contracted error response |
| Timeout and termination confirmed | Runtime timeout; existing enforce/report policy applies |
| Operation cancelled and termination confirmed | Stop the operation without persistence |
| Termination cannot be confirmed within the bounded stop period | Operation failure, not ordinary unavailable evidence; do not persist or remove potentially used temporary inputs |
| Only temporary-file deletion fails after completion | Report housekeeping separately; preserve verdict and persistence policy |

Failure to confirm termination must explicitly report possible continuing processes,
not imply that execution stopped. It is outside the bounded call-failure conversion
above. The runtime-owned operation-error reason is `termination_unconfirmed`, a closed
typed value, not an adapter reason or an additional ordinary AdapterCallFailureReason.
Its placement in the scaffold operation result follows the structured-result route above;
exact fields remain follow-up contract work. Its presentation
must identify the trigger (timeout or cancellation), possible continuing processes,
absence of scaffold persistence and retained temporary inputs when any exist. Technical
diagnostics follow the existing bounded presentation/cache contract. This introduces
no background recovery, process monitoring, temp sweep,
automatic retry, or server-wide health blockade.

The execution model expects adapter/tool work to remain within the managed invocation.
Parallel child processes fit this model; detached background work and work delegated
to an external persistent service do not automatically inherit its termination promise.
Do not silently fall back to direct-parent-only termination when required lifecycle
management is unavailable. Platform-specific implementation stays behind generic
process management, not in public input or adapter contracts. Windows job objects and
Linux process groups are possible mechanisms, not equivalent confinement guarantees
or a declaration of verified Linux support. Each supported platform requires independent
lifecycle evidence before claiming support.

This is reliability-oriented lifecycle management, not safe execution of untrusted
code. OS sandboxing, credential/network restrictions and containment of escaping work
remain in the [security-isolation deferral](deferred-work.md#deferred-work-notice-server-and-subprocess-security-isolation).
Execution-environment selection remains separate Design work; do not silently adopt
the current pytest coupling to the server's Python interpreter as the V3 contract.

Conformance must exercise real child processes: normal parallel completion, timeout,
cancellation, adapter exit with associated work still active, and termination that
cannot be confirmed. Verify no premature input deletion or scaffold persistence,
unchanged non-blocking cleanup, and no misleading successful-completion report.

#### Internal termination budget

Human-approved replacement (2026-09-06): define `TERMINATION_TIMEOUT_SECONDS = 5`
once in generic adapter process management, shared by check, test and fix invocations.
This is an internal mechanical stop budget, not a ServerSettings field or a configurable
default. Add no YAML file, YAML key, environment variable, manifest/profile setting or
tool-input override for it.

This supersedes the v0.36 ServerSettings/YAML proposal. No concrete workspace need for
adjusting this mechanical budget has been established; exposing configuration would
add maintenance and user choices without an evidenced consumer need. Existing settings
loading remains unchanged. Reconsider configurability only if later evidence warrants
a new explicit decision. Execution budgets remain a separate concern: this decision
does not remove the configured scaffold-check timeout_seconds or settle public
check/test/fix execution-time controls.

Measurement starts when timeout or cancellation initiates stopping. One shared budget
covers termination and confirmation for the managed invocation, not a fresh allowance
per subprocess or stop stage. Any graceful and forced termination stages must fit
within it. This is a bounded runtime waiting policy, not a hard real-time OS guarantee.
The stop period never extends the expired execution budget or permits a late verdict.
Failure to confirm within the budget produces termination_unconfirmed as defined above.

Five seconds is an approved design value to validate during implementation, not an
empirically optimal duration for all hosts. Conformance covers a shared stop deadline
across multiple processes/stages, timeout versus cancellation, unconfirmed termination
and unchanged rejection of late results. Test observable lifecycle behavior rather than
the private constant's storage location. This decision does not change proxy/server
restart timing or expand the deferred security-isolation work.

#### Bounded response and diagnostic capture

Human-approved direction and delegated pragmatic limit selection (2026-09-06): bound
adapter-process output during receipt, not after unbounded capture. Define these limits
once in generic process management, shared by check/test/fix without YAML or per-adapter
overrides:

| Channel | Limit | Meaning |
|---|---|---|
| Adapter stdout | 8 MiB (8,388,608 bytes) | Maximum complete formal response, including evidence and surrounding whitespace |
| Adapter stderr | 256 KiB (262,144 bytes) retained | Supplemental error diagnostics only; not a ceiling on bytes emitted |

Use bounded chunk reads and service both streams concurrently. A single unbounded line
must not defeat the limits. Continue servicing channels during bounded termination
without accumulating discarded bytes. These bounds do not cap JSON/DTO overhead,
aggregate concurrent runs, total cache memory or adapter/native-tool memory. They are
pragmatic safeguards, not empirically optimal thresholds or OS sandbox guarantees.

Accept stdout at or below the ceiling only when all response and completion rules pass.
On the first byte beyond it, reject the response and use the existing stop route.
Record response_too_large, never a content rejection or a partial successful result.
Do not truncate JSON/evidence and accept the remainder. Preserve termination_unconfirmed
if stopping cannot be confirmed; the resulting forced-stop exit code does not replace
the size failure. Consumer managers own failure policy. For scaffolding, a confirmed
size failure becomes unavailable evidence under the existing enforce/report policy.

Retain stderr completely up to 256 KiB. Beyond that retain the first 128 KiB and a
rolling last 128 KiB, discard intervening bytes and continue draining until completion
or bounded stop handling ends. Do not duplicate overlapping fragments for short output.
Preserve fragment boundaries and explicitly record truncation; do not present fragments
as contiguous original output. Handle split multibyte characters safely when exposing
text. Never parse stderr to determine a verdict. Diagnostic truncation alone cannot
invalidate a valid adapter response. Useful information may be in the discarded middle;
this is explicitly bounded retention, not lossless capture.

The complete consumer result retains captured diagnostics and the truncation fact
before presentation. Bodies are cache-only; an inline omission notice follows existing
declarative presentation rules. Never claim omitted bytes exist in a full log without
actual evidence. Add no automatic disk spill, report store, new temp directory or log
retention service. Native evidence inside the formal response uses the stdout ceiling,
not the stderr retention policy.

Human-approved disclosure boundary (2026-09-10): apply
[DI-04's shared diagnostic disclosure policy](design-mutation-validation.md#diagnostic-disclosure--approved-2026-09-10)
across check/test/fix consumers. Bounded raw capture and native evidence may retain
incidental absolute paths in the existing on-demand resource cache; typed public
operation paths remain workspace-relative. That cache is client/agent-accessible output,
not private local storage or a secret-redaction guarantee. Do not rewrite arbitrary
native reports merely to strip paths, expose scratch locations as intended targets, or
automatically dump raw diagnostics inline. Keep existing capture bounds and declarative
presentation; add no private log route or diagnostic-ID-only replacement. This changes
the disclosure promise, not the adapter role payload, process limits or error ownership.

Conformance covers exact/one-byte-over boundaries, large single lines, simultaneous
streams, unchanged short output, head/tail and multibyte boundaries, visible truncation,
valid responses with excessive error diagnostics on stderr, and oversized responses with confirmed and
unconfirmed stopping. Measurements are not a prerequisite for these pragmatic limits;
later evidence may motivate an explicit revision.

#### Non-blocking cleanup

Human-approved correction (2026-09-06): cleanup is housekeeping, not a validation or
persistence gate. After collecting necessary evidence and once the invocation's
processes no longer use its files, PGMCP attempts to remove only that invocation's
owned temporary directory. Failure, timeout and cancellation also require an attempt
when safe; abrupt termination can leave residual files.

A detected cleanup failure is reported separately under the existing structured
evidence and bounded presentation rules. It must not replace a valid passing or
failing verdict, stop subsequent checks, or change the consumer's policy decision.
Scaffold enforce/report remains authoritative: cleanup failure alone neither blocks
permitted persistence nor permits rejected persistence. The earlier suggestion to
block scaffold creation on cleanup failure is rejected. Allocation/input-write
failures and genuinely interrupted checks are different: they can prevent a valid
verdict and retain their existing operation/error semantics.

No directory monitoring, startup sweep, periodic cleanup task, age-based deletion or
automatic residual-file recovery is introduced. Periodic inspection and removal of
leftovers remain manual workspace maintenance. Cleanup never claims other invocations'
directories or persisted artifacts. Conformance covers detected deletion failure with
both passing and failing verdicts and proves consumer decisions remain unchanged.

#### Remaining surfaces

This is an integration/proof inventory, not a reopening of the approved package and
check decisions. W02/W03 approval is authoritative in §§7.4.1–7.4.3 and 7.14.

| Surface | Exact design still required |
|---|---|
| Package/catalog | Manifest fields, source discovery, admission/trust, capability references, dependency availability, restart behavior, and official asset packaging |
| Process transport | Request/response schemas, protocol framing, limits, cancellation, execution failures, scratch lifecycle, and external stdout/stderr handling |
| Check | Integrate approved content/selection contracts into concrete typed declarations; prove profile admission, factual outcomes and registered schemas independently |
| Test | Suite selection, all-active-suites meaning, framework options, collection/no-tests outcomes, coverage, and detailed evidence |
| Fix | Proposal shape, authorized paths, stale-input checks, validation, application atomicity, and recovery |
| Public operations | Preserve approved diagnostic boundaries and D-ADAPTER-23 native-argument ownership; complete test/fix contracts and separate check/fix args routing |
| Native configuration | Per-tool project/configuration context, explicit invocation controls versus native settings, and canonical values for current conflicting configurations |

Human correction D-ADAPTER-23 supersedes generic verbose fields: native -v/-vv,
traceback and reporter switches keep their own meanings and are never mapped from a
PGMCP detail boolean. Current test_tools.py translates verbose into --tb=long/short
and pytest_runner.py gates traceback extraction; that accidental interpretation is
removed rather than preserved. Native configuration and explicit args own native detail.
Cache/presentation limits remain independent, with available requested detail retained
within bounds and any truncation explicit. No replacement detail flag or presenter
native-option parser. Native reporter options incompatible with an adapter's result
contract must be rejected honestly, not silently overridden. Check/fix recipient
routing and mutation-profile argument admission remain their own open design work.

### 7.14 Approved run_checks Contract — W03, 2026-09-10

This closes the prepared W03 workshop, chiefly consolidating already approved profile,
scope, native-first and single-invocation decisions in §§7.5–7.13. It does not reopen
Research or imply those decisions originated here. The explicit caller timeout override
is the additional invocation control approved at this checkpoint. Test/fix contracts,
official native capability inventory and independent conformance remain separate work.

#### Configuration and selection

D-ADAPTER-23 removes the old generic verbose field from this public request and the
selection adapter request. Section 7.16 owns the approved addressed check-args/default
contract. Existing targets/branch/workspace check scopes are unchanged by that
argument decision; the separate scope-alignment proposal is not silently approved here.

The required `checks.yaml` uses the existing resolved_config_root. Its closed root has
`checks`, `profiles`, `profiles_by_extension`, and `run_checks` objects. Check bindings
contain exactly adapter_id, capability, positive strict integer timeout_seconds and
default_args: tuple[StrictStr,...] (required; [] is a deliberate empty default).
Profiles contain a nonempty ordered, duplicate-free list of check IDs; nested profiles
are forbidden. The run_checks object has only optional default_profile. Empty maps are
allowed, but dangling check/profile/template/extension/default references fail admission.
The existing extension lookup contract remains unchanged. Template/extension-referenced
profiles require content-capable checks; run-only profiles may use selection-only checks.
Selection for run_checks requires selection support; it never invokes a content-only
capability through a guessed request conversion. Configuration and input schemas use
the same admitted catalog, without adapter startup execution or dependency probing.

Illustrative composition (IDs and timeout values do not approve a shipped inventory):

```yaml
checks:
  python_syntax:
    adapter_id: python_syntax
    capability: syntax
    timeout_seconds: 30
    default_args: []
  markdown_structure:
    adapter_id: markdown
    capability: structure
    timeout_seconds: 30
    default_args: []
profiles:
  python_preflight:
    checks: [python_syntax]
  markdown_preflight:
    checks: [markdown_structure]
  workspace_review:
    checks: [python_syntax, markdown_structure]
profiles_by_extension:
  ".py": python_preflight
  ".md": markdown_preflight
run_checks:
  default_profile: workspace_review
```

| Public field | Closed type / default | Consumer and constraint |
|---|---|---|
| scope | Required targets\|branch\|workspace | ScopeResolver; no auto/project aliases or implicit scope |
| targets | Nonempty tuple of WorkspaceRelativePath, or omitted | Required only for targets; mixed files/directories; forbidden otherwise |
| profile | ProfileId, or omitted | CheckRunManager; mutually exclusive with checks |
| checks | Nonempty unique ordered tuple of CheckId, or omitted | CheckRunManager; exact explicit obligations |
| args | Optional mapping CheckId to tuple[StrictStr,...] | Per selected binding replacement of default_args; §7.16 owns omission/empty semantics |
| fresh | Strict bool, false | Adapter; avoid prior native analysis reuse or refuse honestly |
| allow_expansion | Strict bool, false | Resolver/adapter; permit necessary related checked-content expansion inside workspace |
| timeout_seconds | Positive strict int, or omitted | Manager; override each selected binding's invocation budget, not a whole-run deadline |

No null substitutes for optional inputs. Neither profile nor checks uses only the
configured default_profile; absent default is default_profile_missing, never all checks.
No configured choices yields no_configured_checks, never empty success. Published input
remains a valid object schema admitting no usable selection, with no new health blockade
or removed tool. Final registered-schema evidence remains required. Old quality.yaml,
gate-command keys and unknown fields are migration errors, not supported dual reads.

The override does not alter the shared internal five-second termination budget. One
caller value applies independently to each selected check; omission preserves each
binding's budget. It is an execution control, not a native tool-settings authority.

#### Resolved request and truthful native scope

ScopeResolver normalizes/deduplicates overlapping targets, checks workspace containment
after link resolution and never traverses escaping symlinks/junctions. Missing explicit
targets are input errors. Workspace means the whole workspace; native tools own their
selection/exclusions, not hidden Python include_globs. Branch uses merge-base changes
plus current staged/unstaged and nonignored untracked content. Missing parent/merge-base
is an operation error. Actual Git deletions remain removed targets; rename is old removal
plus current new content. Empty branch/workspace input produces empty_selection without
adapter invocation, not a passing certificate.

SelectionCheckRequest is frozen, strict and extra-forbid, with these required fields:
operation: CapabilityId; targets: tuple[AbsolutePath,...];
removed_targets: tuple[AbsoluteFilePath,...]; expansion_root: AbsoluteDirectoryPath|null;
fresh: bool; args: tuple[StrictStr,...]. At least one target collection is nonempty; existing paths
and actual Git deletions are separate. cwd is workspace root. expansion_root is that
root iff expansion is authorized, otherwise null. There is no redundant scope label,
workspace-root field, preparation token, resume session or generic native selector parser.

The adapter establishes whether requested work fits before substantive checking.
Supporting reads do not expand checked scope. Necessary related expansion within an
authorized ceiling is allowed and reported; unrelated expansion violates conformance.
Generic code does not claim to prove semantic relatedness or per-file participation.

#### Selection outcome and consumer summary

Selection role results retain the approved decision, native evidence and external_tools
baseline. They add required nullable coverage and required required_targets (empty unless
scope expansion is refused). CheckedCoverage contains workspace-relative targets naming
the native execution boundary, not an exhaustive file census, and expanded: bool.
The selection-only not_executed variant has a closed reason enum
scope_restricted|fresh_unsupported|not_applicable and a required factual message.
Scope refusal has required_targets and null coverage; fresh refusal precedes substantive
analysis. Do not infer not_applicable from quiet output or missing findings. A native
passed result asserts native semantics, not that every supplied file participated.

| Selection response | Exit | Constraint |
|---|---|---|
| passed | 0 | Native completed success |
| failed | 1 | Native negative verdict with evidence |
| invalid_request | 2 | Existing minimal rejection; no invented role fields |
| unavailable | 3 | Existing unavailable reason and factual message |
| not_executed | 3 | Selection-only reason; no trustworthy verdict |

These selection fields do not widen the approved scaffold-only response. This completes
the role-specific exit matching table, not a new shared process exit category.

RunChecksOutput contains success, run_status, requested_scope, requested_targets,
required nullable selected_profile, fresh, allow_expansion, ordered results and direct
required nullable error_code/error_details. Each SelectionCheckResult identifies check_id
and preserves the factual outcome, coverage/required_targets and shared invocation facts.
RunChecksErrorCode is closed: no_configured_checks, selection_invalid,
default_profile_missing, branch_basis_unavailable, scope_resolution_failed,
adapter_request_rejected, operation_interrupted, termination_unconfirmed. Detail records
are code-matched frozen closed types, never free dictionaries. Native negative verdicts
and ordinary unavailability remain check facts, not invented operation errors.

Run status is passed|failed|incomplete|empty_selection when a selection-derived summary
exists. For an early operation error before one exists it is required null, paired with
error_code/error_details; this represents absence, not a fifth verdict. Neither a null
run_status nor the presence of domain error details determines success or MCP isError.
Outer MCP input rejection may produce no RunChecksOutput. Do not manufacture check rows
for a selection that never completed. Empty selected input means empty_selection.
For a nonempty known obligation set, any unavailable/not_executed makes incomplete;
otherwise any failed makes failed; otherwise all passed makes passed. Explicit
not_applicable therefore makes incomplete, including mixed-language profiles. Preserve
negative facts when failed plus unavailable aggregates to incomplete. DI-04's different
validation-summary precedence is unchanged.

Public success is an operational StrictBool, the inverse of MCP isError. It reports
whether the PGMCP tool correctly handled the call and reported its result, not whether
checks passed. Correctly reported failed checks have success=true and isError=false.
The same holds for correctly reported ordinary unavailable/not_executed outcomes and
empty_selection: none alone establishes a tool execution fault. Only an actual tool
execution failure follows the existing operational error route with success=false and
isError=true. Do not derive that route from run_status, a native exit code, an adapter
protocol exit code, or the mere presence of error_code/error_details. Expected domain
refusals remain structured results. Shared invocation fault classification keeps its
existing owner; the presenter must not acquire domain-status interpretation.

This corrects the former all-passing-set requirement; it is not a new product policy.
run_status and ordered result evidence remain the authority for the check outcome.
Consumers must not treat success=true as a quality verdict or a completed workflow gate.

Initially invoke sequentially in selected binding order; independent checks continue
after ordinary failure/unavailability. Interruption or an independent blocker stops work;
remaining known obligations get consumer-owned not_executed with not_started|interrupted,
message, null native evidence and invocation only if attempted. These are not adapter
reasons. Retain original causes and termination problems under the shared runtime rules.

This is a selection view and observed native run, not an immutable filesystem snapshot.
Subsequent edits require relevant evidence to be rerun; there is no PGMCP verdict reuse.
Retire quality_state runtime readership, baseline advancement/replay and its branch-local
registration; leave old history inert for owner cleanup, without touching other state.

#### Integration and evidence still required

DI-05 owns concrete frozen DTO declarations and all code-matched detail variants;
shared capture/null-preserving serialization and registered schema proof remain integration
obligations. Prove defaults/exclusivity/role-input admission, empty versus not_applicable,
every response/exit pair, Git working state, expansion denial/permission, native fresh
refusal, repeated execution and cached evidence independently from run_checks itself.
Prove the decorated MCP boundary, not only DTO construction: correctly reported failed,
ordinary unavailable/not_executed and empty selections retain success=true/isError=false;
an actual tool execution fault uses success=false/isError=true. Mixed negative and
unavailable facts retain run_status=incomplete without turning domain reporting into
a tool failure. Verify that native and adapter nonzero exits do not directly set isError.
W06 still owns the declarative profile projection into template fingerprints; W09 owns
native settings and shipped capabilities. No tests, runtime code or Planning cycles are
implemented or authorized by this documentation checkpoint.

### 7.15 Approved run_tests Input and Exposure — W04, 2026-09-10

Preserve the existing check architecture and shared adapter runtime. W04 is closed by
the human; its detailed configuration/output integration follows the accepted workshop
contract. The later §7.16 amendment is authoritative for argument defaults and consumers:
explicit check/test/fix tools may override them; scaffold/safe-edit never expose args.
The agent may use native tool knowledge instead of requiring PGMCP to hide every native
possibility behind a profile, capability or option schema.

#### Caller fields and selection

| Field | Type / default | Constraint and owner |
|---|---|---|
| scope | Required configured\|targets | Explicit native-configured selection or explicit filesystem targets; no implicit scope or workspace alias |
| targets | Nonempty tuple[WorkspaceRelativePath,...], or omitted | Required for targets; forbidden for configured; "." denotes the workspace directory |
| tests | Nonempty unique ordered tuple[TestId,...], or omitted | Select configured test bindings; omission uses the configured active test selection |
| timeout_seconds | Positive strict int, or omitted | Per-invocation override; otherwise use each binding's budget |
| args | Optional mapping TestId to tuple[StrictStr,...] | Explicit recipient list replaces default_args; omission uses configured defaults under §7.16 |

The request is closed and immutable after validation. Unknown fields and null substitutes
for omitted fields are rejected. TestId denotes a configured execution binding, not a
native test case, adapter ID or public tool name. The native operation is resolved from
that binding's capability; it is not inferred from the spelling tests. The JSON args
object uses the same configured TestId set as tests. Its arrays may be empty; an empty
mapping or omitted recipient uses that binding's default_args, while an explicit empty
recipient array replaces its defaults with no extra tokens. Preserve token order and string
values; do not whitespace-split, join into a shell string, or impose a flag/value grammar.

After resolving explicit/default selection, every args key must identify a selected
execution. Reject a mismatch before launching adapters, including an unselected key
whose array is empty. Never broadcast a recipient's arguments to other executions.
This is structural/routing validation, not validation of native option meaning. A missing
usable active selection is an explicit selection failure, never an empty passing run.

Native options work with either scope. The old markers/last_failed_only/coverage/
collect_only purposes and native test-ID selection remain expressible through their
native arguments rather than new PGMCP-specific option fields. For example:

```json
{
  "scope": "configured",
  "tests": ["python_tests"],
  "args": {"python_tests": ["-m", "not slow", "--collect-only"]}
}
```

The example assumes that configured binding; it does not declare a shipped inventory.
Existing generic path safety and adapter-owned native target interpretation still apply.
No branch affected-test inference, native-option allowlist or implicit execution-result
reuse is introduced. Fresh/expansion controls are not silently copied from run_checks.

#### One startup schema, all configured choices visible

Build one completed inputSchema for run_tests under §7.6. The tests item enum contains
the configured binding IDs. The args object has an optional property for each same ID,
each with type array and string items, and additionalProperties=false. Thus an agent
can identify valid recipients without reading YAML. Do not enumerate native switches
or generate adapter-specific options-schema alternatives. Example exposure fragment:

```json
{
  "tests": {
    "type": "array",
    "items": {"type": "string", "enum": ["python_tests", "browser_tests"]},
    "minItems": 1,
    "uniqueItems": true
  },
  "args": {
    "type": "object",
    "properties": {
      "python_tests": {"type": "array", "items": {"type": "string"}},
      "browser_tests": {"type": "array", "items": {"type": "string"}}
    },
    "additionalProperties": false
  }
}
```

This is the properties fragment, not a complete standalone schema: the public schema
also contains scope/targets/timeout_seconds and their required/combination rules.
IDs repeated in enum/properties are projections of one startup authority, not separately
maintained lists. Both recipients are visible at once. Selecting one does not replace,
hide or regenerate any part of the schema. Lazy exposure changes delivery timing only.
Configured exposure does not guarantee native dependencies are installed; availability
remains on use. With no configured choices, publish a valid schema that admits no usable
selection and fail direct/stale calls explicitly; never use an invalid empty enum or
silently successful default. Exact registered schema/validation evidence remains required.

#### Transport and native interpretation

Human-approved correction: configured supplies no explicit filesystem selector and
uses the native tool's configured discovery, modified only by explicit native args.
It does not promise to test every part of the workspace. targets supplies exact
normalized files/directories; targets=["."] explicitly supplies the workspace root.
Native explicit-target semantics may differ from default discovery (for example
Pytest testpaths); do not merge or reimplement those native rules in PGMCP.
Public scope remains mandatory. No branch scope or extra native-default/workspace
mode is added. Adapters translate explicit targets to their native selector syntax;
literal paths must not accidentally become broad regular expressions.

No generic verbose field survives in public or adapter test inputs. Pass native
-v/-vv/--tb options through args with their native meanings and precedence. Native
evidence and diagnostic capture remain bounded independently of those options.
Successful requested operations retain passed, including collection-only; do not add
a completed/collected domain status or infer a mode by parsing argument tokens.

TestRunManager resolves each binding and selects its effective args tuple under §7.16; that tuple is
carried to the selected test adapter as args, not as the public multi-recipient mapping.
The shared invoker still starts the manifest entrypoint and controls the process budget.
It does not splice these tokens into the adapter entrypoint command or interpret them.
The adapter decides how native arguments fit its native invocation. There is no new
launcher, shell route, adapter discovery tool or CLI schema query tool.

Structural adapter-request validation remains required at the process boundary. Native
switch/combinations prevalidation is not mandatory: the adapter may invoke the native
tool and report its rejection, or detect the problem earlier. A native usage error is
not automatically malformed protocol JSON or evidence of a PGMCP construction defect.
Its exact typed test result/exit classification belongs to the next result workshop.

Regardless of when native option validity is established, adapters must retain their
role, authorized scope and result-reporting obligations. Native arguments cannot grant
source mutation to tests or bypass shared safety controls. The analogous check/fix
obligations remain in force. Section 7.16 now owns the explicit check/fix argument route.
Native configuration stays the tool-settings authority; configured default_args and
explicit replacement arguments describe the execution use, not a duplicate native-rule DSL.

#### Remaining integration and independent evidence

The former test options_schema/SuiteRequest/options/test_ids design is superseded for
public test invocation. Do not preserve it as an alias alongside args. Exact tests.yaml
records and the full test/v1 request/result DTO graph accepted at W04 closure still
require detailed canonical integration; apply §7.16's later default_args amendment,
not the superseded temporary suite/options configuration.
The existing all-configured-active meaning from Research remains binding.

Prove the registered/decorated schema's enum/recipient agreement, first-call behavior,
default resolution, unknown/unselected recipient rejection, multi-recipient isolation,
token order/whitespace/empty-value preservation, configured versus explicit targets,
targets=["."], both scopes with args, native rejection with and without adapter
prevalidation, and native verbosity without hidden traceback overrides. Non-test
consumers follow D-ADAPTER-23 and §7.16's explicit mutation-versus-interactive distinction.
The schema fragment is documentation, not executed conformance evidence. Shared native
evidence, cache/presentation and process errors retain their existing owners; do not
introduce generic native-output parsing to support this addition.

### 7.16 Configured Arguments and Consumer Ownership — approved 2026-09-10

This amendment is the single authority for argument selection across consumers. It
supersedes omission-means-no-arguments wording in W04 and rejects public args for
scaffold/safe-edit. A native adapter request still carries one args tuple, regardless
of how the consumer obtained it. No native flag parsing, merging, rewriting or verbose
interpretation is introduced.

| Consumer | Argument source | Public override |
|---|---|---|
| scaffold_artifact | Selected output profile's check bindings | None; no args or verbose input |
| safe_edit_file | Selected template/metadata/extension profile's check bindings | None; no args or verbose input |
| run_checks | Each selected check binding's default_args | Optional args keyed by selected CheckId |
| run_tests | Each selected test binding's default_args | Optional args keyed by selected TestId |
| apply_fixes | Each selected fix binding's default_args | Optional args keyed by selected FixId; fix authority unchanged |

Each check/test/fix binding declares required default_args: tuple[StrictStr,...].
An explicit [] means no extra native options. The role config reader owns strict,
immutable loading and rejects null, non-string items and unknown fields; native
option validity remains adapter/tool-owned, not startup native probing. The field
lives beside adapter_id/capability/timeout_seconds, never in the adapter manifest,
artifact context, profile override bag or global server config. Distinct uses can bind
the same adapter/capability under different execution IDs with different defaults.
Profiles select those IDs; they do not carry another argument-override layer.

| Caller entry for a selected execution | Effective list | args_source |
|---|---|---|
| Omitted, including an omitted/empty public args mapping | Binding default_args | configured |
| Present nonempty array | Exact caller array replacing the whole default list | caller |
| Present [] | Empty tuple; native configuration still applies | caller |

Resolve the selected IDs before validating all argument recipients. An unknown or
unselected recipient is rejected before any launch, even with []. Omitted recipients
use their own defaults, never another recipient's values. No concatenation, per-flag
merge, fallback after native rejection or automatic broadcast. Explicit replacement
equal to the default list still has source caller. One complete startup schema exposes
the applicable configured execution IDs as optional args properties with string-array
values; the manager checks actual profile/default selection on use. No conditional
schema exposure or extra CLI-discovery tool. Mutation input schemas expose no args map.

The manager sends the effective list as required args in the role request; the adapter
does not read role YAML, resolve defaults or echo provenance. The public operation's
per-execution record gains direct args_source: Literal["configured","caller"] and
effective_args: tuple[StrictStr,...], authored by the manager. Until arguments have
actually been resolved, both are required null; after resolution neither is null,
and [] is a known empty list. The record's invocation state independently identifies
whether native work occurred. These fields describe supplied extra options, not the
whole native argv, native merged configuration, hidden environment or command history.
Scaffold/safe-edit check records can only have source configured when resolved.
Do not introduce a nested source object or DTO-specific presenter logic. Report source
in concise feedback and retain the effective list in the existing cached DTO under
the established presentation/disclosure rules; it remains available without rerunning.

Mutation profiles remain fixed preflight validations of the complete candidate text.
Neither call-specific native tuning nor filesystem scope selection is added to those
tools. requires_file materialization, intended path, cleanup, policy, atomicity and
profile selection stay unchanged. The generic content request gains only args from
its selected binding. apply_fixes caller args apply only to selected fix executions,
not implicitly to their verification checks; those use configured check defaults.
Native role/scope/input-source requirements cannot be bypassed by defaults or caller
args. Incompatible native options must be reported, not silently replaced.

No changes to native rule config or fingerprints are implemented here. W06's still-open
profile-projection proposal must account explicitly for use-specific default_args;
do not silently treat the prior adapter_id/capability-only projection as exhaustive.
Native config and adapter bytes remain distinct from this authored binding input.

Required evidence: omitted mapping/recipient, explicit [] and replacement, equal-value
caller provenance, token order/whitespace/empty values, selected-profile routing,
unselected-recipient rejection, no mutation override field, fixed content/file variants,
source/effective list preservation across negative results and bounded invocation
failures, no argument merge, no fix-to-verification broadcast, unchanged native
settings, and success/isError independence. Tests are design obligations, not executed
conformance. This amendment does not approve the separate run_checks scope proposal
or complete the remaining W05 recovery/output design.

## 8. Control, Data, and State Flow

1. Startup reads package/configuration declarations, validates their structure and
   references, applies trust policy, and supplies an immutable catalog to consumers.
2. A consumer selects a role capability for its purpose and provides the corresponding
   input. Output-profile selection remains separate from explicit check/test/fix scope.
3. Generic infrastructure selects the declared proposed-content route (section 7.13)
   and executes the adapter entry point. Only the file route materializes content in
   controlled scratch space. The adapter preserves native intended-target context;
   no route writes the authoritative target before the consumer's persistence decision.
4. The adapter returns role-specific evidence or a bounded fix proposal. Generic
   transport failure is distinguishable from a valid role response.
5. The consumer applies its policy. DI-04 alone decides scaffold/edit persistence;
   DI-05 controls explicit fix application. Workflow decisions consume the evidence.

Package/configuration defects fail at startup. A missing underlying toolchain for an
otherwise valid dormant package is an on-use availability outcome. A successful process
exit is insufficient to claim a passing check, passing tests, or a safely applied fix.
The accepted DI-04 `passed`/`failed`/`unavailable`/`not_executed` behavior is a preservation
constraint for check evidence; it is not automatically the test or fix result schema.

## 9. Compatibility, Migration, and Removal

F-20 fixes the target public vocabulary: `run_checks`, `run_tests`, and `apply_fixes`,
with `checks.yaml`, `tests.yaml`, and `fixes.yaml`. `run_quality_gates`, `auto_fix`, and
`quality.yaml` retire without supported aliases or dual reads. Old configuration gets
actionable migration feedback. Test semantics require migration even though the tool
keeps the `run_tests` name.

Direct source seams inspected for this workshop:

| Current source | Migration obligation |
|---|---|
| [PythonValidator](../../../mcp_server/validation/python_validator.py) | Move syntax/tool implementation behind adapters; preserve pre-mutation check purpose without promoting full QA to every scaffold |
| [quality.yaml](../../../.pgmcp/config/quality.yaml) and [QAManager](../../../mcp_server/managers/qa_manager.py) | Move integration/parser semantics into adapters, native tool settings into their native authority, and selection/policy into role consumers; do not copy whole legacy commands as hidden policy |
| [RunTestsTool](../../../mcp_server/tools/test_tools.py) and [PytestRunner](../../../mcp_server/managers/pytest_runner.py) | Move Pytest integration into its test adapter; separate explicit test requests from native test/coverage settings and remove hardcoded workspace thresholds |
| [quality_tools.py](../../../mcp_server/tools/quality_tools.py) | Replace the public V2 check/fix operations and explicitly map retained result behavior |
| [bootstrap.py](../../../mcp_server/bootstrap.py) | Compose catalog/process/role boundaries without tool-specific execution branches |
| [ConfigLoader](../../../mcp_server/config/loader.py), [quality schemas](../../../mcp_server/config/schemas/quality_config.py), and [loader/schema tests](../../../tests/mcp_server/unit/config/test_quality_config.py) | Preserve one loading authority, pure immutable schemas, and actionable invalid-config rejection; replace gate-command/parser/capability coupling with catalog role declarations and references |
| [pyproject.toml](../../../pyproject.toml) | Account for dependencies, native tool configuration, and shipped manifest/executable assets; prove installation from the built package |
| [pyrightconfig.json](../../../pyrightconfig.json) | Retain one native Pyright settings authority and resolve conflicting or duplicated settings during migration |

Concrete configuration discrepancies inspected on 2026-09-05:

- Ruff commands in `quality.yaml` use `--isolated` and provide rule selections, ignores,
  and language/line-length settings. `pyproject.toml` explicitly calls its own settings
  an IDE baseline; the command configuration describes itself as stricter.
- `pyrightconfig.json` sets Python `3.13`, while `quality.yaml` passes Python `3.11`.
  `pyproject.toml` also repeats a Pyright diagnostic setting.
- `RunTestsTool._build_cmd` hardcodes coverage sources and a `90` threshold. These are
  distinct from requesting that a particular run collect coverage at all.

The target does not preserve this two-layer arrangement. Before removing the old path,
the relevant Design work must choose the retained native values explicitly and identify
intentional behavior changes. Blindly dropping flags could weaken or otherwise change
checks; hiding those same flags inside adapters would preserve the rejected duplication.
Legacy numbered gate fragments are not a requirement for separate V3 capabilities.
No production configuration is changed by this workshop.

The documented mechanisms support this ownership: [Ruff configuration](https://docs.astral.sh/ruff/configuration/)
defines native discovery and CLI overrides (`--isolated` ignores configuration files);
[Pyright configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
defines `pyrightconfig.json` precedence over `pyproject.toml`; and
[Pytest configuration](https://docs.pytest.org/en/stable/reference/customize.html)
defines its native configuration discovery. Use the supported installed tool versions
when designing concrete adapters; these links do not select new dependency versions.

This is a workshop evidence index, not a replacement inventory. The frozen
[catalog](template-suite-catalog.md#runtime-and-active-consumer-ledger) owns all 126
consumer and 151 test/helper dispositions. Contracts, catalog, and independent
conformance evidence must exist before legacy runners/parsers disappear; public
cutover follows proven internal routes.

## 10. Test and Validation Design

| Boundary to prove | Required evidence and existing seam |
|---|---|
| Generic extension | A non-Python fixture adapter executes through the public process/role boundary with package/configuration changes only |
| Contract conformance | Independent request/response validation and malformed/crashed/unavailable cases; fixture responses alone cannot certify official adapters |
| Manifest admission and selection | Adapt public loader/schema tests: reject invalid or unsupported declarations and unresolved configured references before tool exposure; reject unknown caller selections before execution; prove role-qualified selection, check-only consumers cannot select fixes, and discovery does not execute adapter code; missing external toolchains remain on-use availability outcomes |
| Shared binding, separate selectors | Exercise scaffold-profile and explicit-check consumers against the same configured check binding; prove unrelated checks and all fixes remain unselected, and native settings are not copied into either selector |
| Profile versus operation purpose | Adapt [validation policy coverage](../../../tests/mcp_server/integration/test_validation_policy_e2e.py); selecting a syntax profile must not run unrelated workspace checks or tests |
| Check migration | Compare retained diagnostics/outcomes against direct known-input tool evidence; preserve mixed failure/unavailability and policy-independent facts |
| Native configuration authority | Compare adapter and direct native-tool behavior for the same tool version, inputs, and purpose; change a native setting and prove it affects the adapter without changing package/PGMCP settings; cover logical-target configuration for scratch input |
| Test migration | Adapt [Pytest behavior coverage](../../../tests/mcp_server/unit/managers/test_pytest_runner.py), preserving collection, failures, skips, coverage and native-requested detail without the old generic verbose interpretation |
| Fix migration | Compare authorized proposal/application results against before/after bytes, including already-dirty targets, stale inputs, out-of-scope proposals, and application interruption |
| Distribution | Inspect a built distribution and execute a retained official adapter from an installed copy; a source-tree import is insufficient packaging evidence |

DI-05 owns role behavior and conformance tests; DI-08 owns reusable fixtures/helpers.
Legacy private-parser tests are candidates for public-boundary adaptation, not a
requirement to preserve those methods. Concrete harness and fixture APIs remain open.
No production tests have run for this documentation-only workshop, and none of the
proposed conformance evidence is claimed as completed.

## 11. Integration Risks and Open Questions

| ID | Open Design question | Decision needed |
|---|---|---|
| Q-ADAPTER-02 | What completes role-specific bindings after W02/W03 and W04 input approval? | §§7.4.1–7.4.3, 7.14 and 7.15 fix package/check and public test-input behavior; test configuration/remaining transport/results and fix operations stay open; exact DTO integration/conformance is still required |
| Q-ADAPTER-03 | How does a tool that needs disk input observe proposed content and appropriate project configuration? | Define scratch, logical-path mapping, and context without authoritative source writes |
| Q-ADAPTER-04 | What are the exact three role schemas and transport rules? | Cover each role's outcomes, native-argument transport, and independent conformance |
| Q-ADAPTER-05 | How are fixes authorized and recoverably applied? | Define the separate F-20 mutation contract and stale/proposal/application evidence |
| Q-ADAPTER-06 | Which native values replace today's split tool-settings authorities? | DI-05 chooses retained per-tool settings and explicit request controls, records intentional changes, and supplies separate check/test/fix migration proof obligations |
| Q-ADAPTER-07 | What completes each capability declaration and its consumer binding? | Define profile/check selection, applicability and input requirements, and explicit fix-to-check references without same-package or same-name assumptions |
| Q-ADAPTER-08 | How do centrally selected profiles/bindings participate in the existing template provenance closure? | DI-02/DI-05 define the exact declarative projection and affected-package proof before integration; preserve exclusion of executable adapter provenance and native tool settings |
| Q-ADAPTER-09 | How do startup-built public contracts survive registration wrappers and lazy client exposure? | Define the contract holder and validation/presentation interfaces; prove the registered boundary and supported host reconnect/cache behavior without adding hot reload |
| Q-ADAPTER-10 | How does each real consumer expose configured choices and handle on-use unavailability without weakening its contract? | Complete check/test/fix inputs, defaults, no-configured-choice behavior, no startup probes/filtering, full profile obligations, preserved scaffold report mode, and ordinary response projections under issues 456/459; startup health diagnostics and general blockades remain separately deferred |

## 12. Planning Consequences

Planning consumes the [nine manageability conditions](README.md#binding-design-and-planning-manageability-conditions).
This package supplies independently provable contract/catalog, check, test, fix,
distribution, and cutover boundaries as they are designed. Check/test/fix migration
need separate proof; F-10 renewal activation and F-20 fix application require different
implementation cycles. Every cycle needs a bounded write set, preserved behavior,
rollback point, and independent stop/go evidence. Every catalog row needs a concrete
cycle owner; neither a DI-05 mega-cycle nor a remaining-consumers/tests bucket suffices.

Exact cycle names and scheduling remain Planning-owned.

## 13. Traceability Matrix

| Input | Current treatment | Completion state |
|---|---|---|
| DI-05; human dedicated-document condition | Sections 1–5 define exclusive ownership and consumer purposes | Nucleus recorded |
| F-08/S-14; E-13 | Sections 5, 8, and 10 preserve appropriate profile checks and honest on-use unavailability | Exact profiles/check types open |
| F-19; I-16; E-20 | Sections 5 and 10 require one check implementation authority with separate policy consumers and independent evidence | Exact interfaces/harness open |
| F-20; I-19; E-23 | Sections 5–9 retain shared catalog/process infrastructure, separate check/test/fix contracts, and bounded package-provenance consumers | D-ADAPTER-03/04/06 decided; D-ADAPTER-07 proposed; complete capability and launch contracts open |
| Human native-configuration direction; XC-01; existing DI-05 configuration consumers | Sections 7, 9, and 10 assign tool settings to native configuration and separate package/integration/consumer authority | D-ADAPTER-05 decided; concrete migration values and context mechanics open; Research unchanged |
| XC-01 | Section 5 requires injected narrow boundaries; section 10 requires public behavioral tests | Component/test architecture open |
| XC-02; 126/151 catalog | Sections 9–12 preserve per-row removal ownership and independent migration proof | Complete removal mapping remains open |
| RC-01; manageability conditions | Sections 2, 9, and 12 preserve scope freeze, clean break, cutover order, and cycle constraints | Binding throughout Design |

## 14. Related Documentation and Version History

- [Design hub](design.md)
- [Documentation contract](README.md)
- [Research](research.md)
- [Design intake](design-intake-map.md)
- [DI-04 mutation and persistence](design-mutation-validation.md)
- [Shared schema-delivery contract](design-shared-contracts.md)
- [DI-06 template distribution](design-distribution.md)

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.64 | 2026-09-07 | `@imp designer` | Require approved factual failed-decision message while preserving native evidence and exit codes; omit extra public origin and route the consolidated mutation-result proposal. |
| 0.63 | 2026-09-07 | `@imp designer` | Route mutation nesting, union-collection admission and native-evidence inline gaps to DI-04 audit without changing approved internal contracts or assuming presenter support. |
| 0.62 | 2026-09-07 | `@imp designer` | Limit ongoing safe-edit mode design to strict/interactive and reference the verify_only removal deferral and concrete-conflict-only boundary. |
| 0.65 | 2026-09-07 | `@imp designer` | Reconcile DI-04 references after human-reported Research QA GO: common enforce/report policy, default enforce and legacy mode retirement; no adapter-contract change. |
| 0.66 | 2026-09-08 | `@imp designer` | Reference DI-04's approved narrow V3 reader and original/proposed-content consistency; keep both outside adapter responsibility. |
| 0.67 | 2026-09-10 | `@imp designer` | Apply human-approved shared diagnostic disclosure: retain bounded incidental host paths in on-demand cached diagnostics without a private-log substitute; preserve relative public operation fields, process bounds and role payloads. |
| 0.68 | 2026-09-10 | `@imp designer` | Link approved W01 operation-result projection while retaining generic process ownership and the separate W02 native provenance return decision. |
| 0.69 | 2026-09-10 | `@imp designer` | Record partial W02 approval for package sources, consumer-backed fields, file inventory, fingerprint scope and narrow interfaces; keep exact trust configuration and native provenance return amendment open. |
| 0.70 | 2026-09-10 | `@imp designer` | Close W02-B/F: explicit adapters.yaml with central loading and typed external_tools in ordinary role results; amend existing closed scaffold payload and preserve minimal invalid_request; keep W03–W05 role work open. |
| 0.71 | 2026-09-10 | `@imp designer` | Integrate approved W03 as consolidation of existing selection/scope/native decisions plus explicit caller timeout override; specify honest completion and early-error absence without reopening Research or test/fix choices. |
| 0.75 | 2026-09-10 | `@imp designer` | Record default_args per execution binding, configured-only mutation checks, selected caller replacement for check/test/fix and direct args_source/effective_args evidence; amend prior empty-argument semantics and closed content requests. |
| 0.74 | 2026-09-10 | `@imp designer` | Consolidate approved W04 configured/targets scope and passed vocabulary; remove generic native verbose interpretation across consumers, retaining separate check/fix argument-routing work and unapproved W04 configuration/output proposals. |
| 0.73 | 2026-09-10 | `@imp designer` | Correct run_checks domain-derived success: restore operational success/inverse MCP isError, preserve negative domain evidence separately and require actual MCP-boundary regression evidence. |
| 0.72 | 2026-09-10 | `@imp designer` | Record approved run_tests flat tests selection, addressed args and fixed startup exposure; supersede test options_schema only; preserve other consumers and leave test results/configuration/full transport open. |
| 0.61 | 2026-09-07 | `@imp designer` | Record approved longest configured extension lookup, host-independent case matching and honest no-match behavior; bound suffix-only routing and identify preservation evidence and remaining schema/policy work. |
| 0.60 | 2026-09-07 | `@imp designer` | Record root-level profiles_by_extension ownership and consumer boundaries; preserve manifest and explicit/default selections while leaving exact lookup and safe-edit policy open. |
| 0.59 | 2026-09-07 | `@imp designer` | Supersede startup dependency preflight/filtering with configuration-based exposure and existing on-use failures; retain structural/path admission, stable schemas, defaults, full profiles, and health deferral without new protocol or Research changes. |
| 0.58 | 2026-09-07 | `@imp designer` | Allow explicitly declared script interpreters through the existing generic launch route; specify frozen typed executable/args/package_file shapes without new fields or a sandbox guarantee. |
| 0.57 | 2026-09-07 | `@imp designer` | Exclude implicit shell/interpreter selection and direct Windows batch execution; keep explicit script-interpreter semantics as the next bounded decision. |
| 0.56 | 2026-09-07 | `@imp designer` | Define package-file containment/existence admission and later disappearance ownership without fallback, automatic repair or sandbox claims. |
| 0.55 | 2026-09-07 | `@imp designer` | Select explicit package_file references for executable and args, retaining separate program/argument fields and rejecting prefix-based executable selection. |
| 0.54 | 2026-09-06 | `@imp designer` | Start adapters at the resolved workspace root; separate package-code location from project context without new cwd configuration or native config discovery. |
| 0.53 | 2026-09-06 | `@imp designer` | Resolve named executables once from the server startup PATH without language-specific fallback; preserve environment ownership and proxy restart limitations. |
| 0.52 | 2026-09-06 | `@imp designer` | Clarify adapter-supplied dependency contributions and workspace-owned provisioning; exclude automatic installation and retain explicit launch-resolution work. |
| 0.51 | 2026-09-06 | `@imp designer` | Keep contract-version selection at the admitted role entrypoint; complete operation-bearing text/file scaffold request shapes and examples. |
| 0.50 | 2026-09-06 | `@imp designer` | Use operation for the adapter request directive while retaining capability references in configuration; preserve identifiers and narrow field consumers. |
| 0.49 | 2026-09-06 | `@imp designer` | Complete four mutually exclusive scaffold-facing response shapes and typed invalid-request details; preserve existing result fields and shared presentation boundaries. |
| 0.48 | 2026-09-06 | `@imp designer` | Assign shared exit categories 0 success, 1 negative result, 2 invalid request, 3 unavailable; bind existing scaffold variants without new reasons or recovery machinery. |
| 0.47 | 2026-09-06 | `@imp designer` | Supersede exit-zero-only completion with matching documented exit/response pairs; exclude recovery flags and retry machinery; numeric mapping remains open. |
| 0.46 | 2026-09-06 | `@imp designer` | Reject duplicate server-side request validation; place typed invalid_request rejection within the standard adapter output contract. |
| 0.45 | 2026-09-06 | `@imp designer` | Record one UTF-8 JSON request via stdin followed by EOF, shared across roles without session or line-framing machinery. |
| 0.44 | 2026-09-06 | `@imp designer` | Restrict stderr to supplemental error diagnostics; prohibit routine logging and stdout salvage without generic free-text classification. |
| 0.43 | 2026-09-06 | `@imp designer` | Bound formal responses at 8 MiB and retained stderr at 256 KiB; define size failure and non-blocking head/tail diagnostic truncation. |
| 0.42 | 2026-09-06 | `@imp designer` | Define approved completed/failed/cancelled shared manager result variants with optional termination problem and concrete role response typing. |
| 0.41 | 2026-09-06 | `@imp designer` | Preserve original invocation outcomes alongside additional unconfirmed-termination diagnostics; avoid duplicated status flags and successful-stop records. |
| 0.40 | 2026-09-06 | `@imp designer` | Assign shared check/test/fix process diagnostics to generic management, policy to consumer managers and structural transfer only to tools. |
| 0.39 | 2026-09-06 | `@imp designer` | Restore the issue-456/459 structured-result route; withdraw new error registration/dispatch prerequisites and NoteContext as the diagnostic path. |
| 0.38 | 2026-09-06 | `@imp designer` | Require DTO- and reason-independent error presentation and startup validation; identify existing hardcoded error fields and single-output catalog gap without selecting a new error taxonomy. |
| 0.37 | 2026-09-06 | `@imp designer` | Supersede configurable termination timeout with one internal five-second process-management value shared by check/test/fix; remove YAML and ServerSettings obligations. |
| 0.36 | 2026-09-06 | `@imp designer` | Configure the shared termination budget in ServerSettings with explicit default 5; name termination_unconfirmed as a runtime-owned operation error and preserve existing configuration loading. |
| 0.35 | 2026-09-06 | `@imp designer` | Record approved managed-invocation termination, cancellation and unconfirmed-stop behavior; retain native parallelism and deferred security isolation. |
| 0.34 | 2026-09-06 | `@imp designer` | Record per-check strict positive timeout_seconds ownership and timing boundaries; preserve native timeouts and leave bounded process termination for the next workshop. |
| 0.33 | 2026-09-06 | `@imp designer` | Require one valid response plus timely exit 0; separate native verdict from adapter exit, reserve stdout and classify crash/hang/invalid-response completion. |
| 0.32 | 2026-09-06 | `@imp designer` | Define four runtime-owned adapter-call failure reasons and map recognized failures to scaffold unavailable evidence without fabricating adapter responses. |
| 0.31 | 2026-09-06 | `@imp designer` | Define approved decision/evidence split, closed text/JSON evidence, per-status presence rules and recursive immutable JSON ownership without normalizing native findings. |
| 0.30 | 2026-09-06 | `@imp designer` | Define closed scaffold adapter decision variants and five adapter-owned unavailable reasons; exclude outer timeout/crash/protocol facts and keep native evidence packaging open. |
| 0.29 | 2026-09-06 | `@imp designer` | Define approved closed immutable scaffold text/file input variants, constrained path semantics, manifest matching and exact UTF-8 materialization; separate shape from filesystem checks. |
| 0.28 | 2026-09-06 | `@imp designer` | Record scaffold-only intended-path and exclusive text/file payload nucleus; separate public path semantics and leave other consumers and full role schemas open. |
| 0.27 | 2026-09-06 | `@imp designer` | Link explicit security-isolation deferral and bound isolation claims without broadening issue 460. |
| 0.26 | 2026-09-06 | `@imp designer` | Make cleanup failures separately reported and non-blocking for valid verdicts and persistence policy; reject automated temp monitoring and sweeping. |
| 0.25 | 2026-09-06 | `@imp designer` | Require fresh per-check temporary IDs across repeated and concurrent calls, exclusive allocation and no shared/reused directories; keep cleanup policy open. |
| 0.24 | 2026-09-06 | `@imp designer` | Derive temp/validation centrally from the configured server root, without a new path setting; align sibling temp/artifacts authority with DI-04. |
| 0.23 | 2026-09-06 | `@imp designer` | Accept required requires_file boolean without a default; supersede the content_input enum and retain proposed-content-only scope. |
| 0.22 | 2026-09-06 | `@imp designer` | Record approved direct-content versus managed-file ownership, bounded native Markdown probe evidence and target non-mutation; propose a per-check content_input field without a general capability matrix. |
| 0.21 | 2026-09-05 | `@imp designer` | Bind future workshops to native behavioral authority, thin adapters and consumer-specific minimum results; withdraw mandatory per-file participation proof and universal result normalization. |
| 0.20 | 2026-09-05 | `@imp designer` | Record native exclusions remain authoritative for explicit targets; distinguish exclusions from non-applicability and prevent process success from implying unproven coverage. |
| 0.19 | 2026-09-05 | `@imp designer` | Record approved targets/branch/workspace selection and conditional targets list for mixed files/directories, including recursion, deduplication and invalid-input evidence. |
| 0.18 | 2026-09-05 | `@imp designer` | Align V3 workspace vocabulary with authorized Research clarification; correct directory-versus-project example and record ordinary language-specific/mixed profiles without a subproject model. |
| 0.17 | 2026-09-05 | `@imp designer` | Record agreed scope refusal as not_executed with check association, reason, required scope and explanation; preserve stateless retry and independent non-execution evidence. |
| 0.16 | 2026-09-05 | `@imp designer` | Record human-approved single-invocation permission/native-requirement split, pre-execution refusal and stateless caller retry; keep exact response/bounds contracts open. |
| 0.15 | 2026-09-05 | `@imp designer` | Resume Design after human GO; reconcile required scope, auto/state removal and native fresh intent with amended Research; replace withdrawn reuse/session proposals with concise rationale and proof obligations. |
| 0.14 | 2026-09-05 | `@imp designer` | Withdraw prepared-work/session design; reopen PGMCP-owned reuse and record bounded native-tool feasibility evidence without changing frozen Research. |
| 0.13 | 2026-09-05 | `@imp designer` | Record internal check/v1 prepare/execute agreement and optional adapter-owned reuse support; preserve input-schema, scope authorization, and evidence-binding boundaries. |
| 0.12 | 2026-09-05 | `@imp designer` | Record bidirectional evidence reuse across all run_checks scopes, truthful coverage/execution reporting, and explicit reuse bypass; supersede auto-only state ownership while leaving exact contracts open. |
| 0.11 | 2026-09-05 | `@imp designer` | Record approved auto selection/evidence semantics, preservation of unrequested failures, conservative reuse, and bounded current state; leave storage and cross-scope lifecycle policy open. |
| 0.10 | 2026-09-05 | `@imp designer` | Record approved working-tree-aware branch scope and the corresponding auto inclusion obligation; preserve deletion and expansion boundaries while leaving incremental state mechanics open. |
| 0.9 | 2026-09-05 | `@imp designer` | Record approved requested-scope versus read-context boundary, explicit bounded expansion permission, truthful per-check scope evidence, and remaining protocol/scope design obligations. |
| 0.8 | 2026-09-05 | `@imp designer` | Supersede diagnostic schema prose; retain complete availability-aware input contracts and defer health presentation, instructions, and general blockades without a V3 dependency. |
| 0.7 | 2026-09-05 | `@imp designer` | Record approved availability-aware startup exposure and unchanged profile obligations; carry issues 456/459 presentation, supported-catalog alignment, cache, attachment, and field-audit boundaries into the per-consumer follow-up. |
| 0.6 | 2026-09-05 | `@imp designer` | Record startup-bound schema construction and consistent lazy exposure/validation; identify the current validation-wrapper schema bypass and independent server/client proof obligations without changing runtime code. |
| 0.5 | 2026-09-05 | `@imp designer` | Record manifest-nucleus agreement; propose one named check binding shared by profiles and explicit operations; bound the illustrative configuration and route profile-provenance integration explicitly. |
| 0.4 | 2026-09-05 | `@imp designer` | Propose role-organized manifest fields with named consumers and per-role entrypoints; compare alternatives, preserve explicit fix/check relations as required follow-up, and identify the next binding and launch workshops. |
| 0.3 | 2026-09-05 | `@imp designer` | Record discovery/reference agreement, clarify version versus fingerprint consumers and limits, and select native tool configuration as settings authority; route concrete existing discrepancies and scratch-context evidence without changing frozen Research or runtime configuration. |
| 0.2 | 2026-09-05 | `@imp designer` | Record human agreement on implementation-based packages and package-wide identity; open the separate shallow-discovery, manifest-identity, trust, and consumer-reference proposal. |
| 0.1 | 2026-09-05 | `@imp designer` | Establish the dedicated DI-05 workshop nucleus from frozen Research; compare implementation-based package grouping; record consumer purposes, direct seams, and outstanding contracts without claiming complete Design. |
