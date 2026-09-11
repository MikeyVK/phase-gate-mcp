<!-- docs\development\issue460\design-distribution.md -->
<!-- template=design version=5827e841 created=2026-08-31T18:55Z updated= -->
# Issue 460 Template-Suite Distribution and Renewal Design

**Status:** DRAFT  
**Version:** 1.11  
**Last Updated:** 2026-09-11  
**Primary Package:** DI-06  
**Upstream Dependencies:** Research Approved Strategy, DI-01/DI-02 suite validation and identities, final DI-03 package set, DI-05 adapter source contract  
**Downstream Consumers:** DI-07, DI-08, CLI/init/upgrade, owner workspace migration  
**Lifecycle Status:** Renewal decided; W10 adapter location/delivery boundary approved; W10 configuration integration open

---

## 1. Purpose and Authority

This document owns DI-06 template-suite installation, component-aware renewal,
customization preservation, checkpoint bootstrap, candidate staging, reconciliation,
recoverable activation, explicit forced replacement, and owner-deployment migration for
issue 460.

The [Suite Resolution Design](design-suite-resolution.md) owns suite discovery,
validation, resolved package graphs, package versions, resolved package fingerprints, and
the generation-only source-suite fingerprint. The human clarification of 2026-09-11
confirms operational component fingerprints as the separate third identity kind; Research
QA GO was reported by the human on 2026-09-11. This document cannot use pf/sf for full installed-state equality. DI-06 separately owns operational component equality
for renewal; those checkpoint identities are not artifact metadata.

The design nucleus is a three-way comparison of one current adopted checkpoint, the
actual active suite, and the supplied candidate. Selection occurs at indivisible
component boundaries. The selected components are assembled off-root and validated as
one complete suite before the sole runtime root can change.

## 2. Scope and Exclusions

### In Scope

- fresh installation of a managed template suite and its first adopted checkpoint;
- safe bootstrap of existing managed and external workspaces without a checkpoint;
- one current adopted checkpoint, one actual active suite, and one supplied candidate;
- `shared/` and every concrete `template_id` value as indivisible comparison components;
- presence and absence as component states, covering additions and removals;
- deterministic adopted/actual/candidate classification and whole-component selection;
- complete off-root proposal construction and full resolved-suite validation;
- recoverable complete-tree activation while preserving one runtime root;
- non-authoritative candidate staging for unresolved conflicts and checkpoint bootstrap;
- explicit checkpoint advancement after human or agent reconciliation;
- explicit forced complete-candidate replacement for a managed root;
- actionable factual comparison and renewal outcomes;
- removal of current file-class renewal that can split paired suite assets;
- migration of the current owner's supported workspaces.

### Out of Scope

- automatic line, text, file, or semantic merging inside a component;
- package-to-package dependencies or runtime overlays;
- multiple active roots, precedence rules, or partial writes into the active tree;
- SemVer compatibility inference, bump classification, or compatibility matrices;
- checkpoint history, per-file versions, or a historical component ledger;
- changing artifact metadata or repurposing resolved-package/source-suite fingerprints;
- automatic artifact-content upgrades;
- historical snapshot lookup, external source retention, Git inspection, release
  association, or external SemVer-policy enforcement;
- implementation sequencing, Planning cycles, or patch instructions.

Component-aware renewal is not a package manager. It has one current upstream checkpoint,
copies only complete source components, performs no content merge, and makes no semantic
compatibility claim. A failed complete-suite validation stops activation rather than
searching alternative component combinations.

## 3. Binding Inputs

- [Research F-10/S-10 Approved Strategy](research.md#approved-strategy-and-decision-status)
- [Research F-10 renewal evidence](research-findings.md#f-10--renewal-can-split-paired-assets)
- [Research distribution option decision](research-findings.md#s-10--distribution-and-local-customization)
- [DI-06 Design Intake](design-intake-map.md#di-06--distribution-renewal-and-deployment-migration)
- [Suite Resolution Design](design-suite-resolution.md)
- [Pre-Implementation Documentation Contract](README.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)
- [Deferred Work](deferred-work.md)

Binding constraints include one active runtime authority, no overwrite of a conflicting
actual component, no assumed checkpoint, no package-to-package dependencies, no
provenance-history replacement registry, and no silent change to the Approved Strategy.

## 4. Owned Decisions

| ID | Decision | Status |
|---|---|---|
| D-DIST-01 | The complete validated suite is the only runtime and activation unit; component selection never writes individual entries into the active root | Decided |
| D-DIST-02 | The actual root is the sole runtime authority; a staged candidate and off-root proposal are never loaded implicitly | Decided |
| D-DIST-03 | `.pgmcp/installation.json` owns PGMCP compatibility plus one optional current adopted component checkpoint with required `shared` and `packages` members; package entries are keyed only by `manifest.yaml:template_id`; it stores no history, per-file versions, actual/candidate snapshots, timestamps, or artifact provenance | Decided |
| D-DIST-04 | Renewal compares adopted, actual, and candidate independently for `shared/` and every `template_id` component, with absence as a first-class state | Decided |
| D-DIST-05 | `shared/` is one indivisible source component and every concrete `template_id` value is one indivisible source component; physical package-directory names do not define identity | Decided |
| D-DIST-06 | Candidate is selected for upstream-only and converged states; actual is retained for unchanged, local-only, and conflicting states | Decided |
| D-DIST-07 | Selection builds one complete off-root proposal; only a fully validated proposal may replace the managed actual root through the same-filesystem activation and deterministic recovery protocol in §§7.5 and 8 | Decided |
| D-DIST-08 | Fresh managed installation creates actual content and the first checkpoint together; checkpoint-less workspaces bootstrap automatically only from Research-approved trustworthy equality evidence, while `pgmcp --upgrade --accept-template-baseline` explicitly derives the complete checkpoint from the current validated staged candidate without copying it into a valid v3-format actual root | Decided |
| D-DIST-09 | Component comparison reports actual, upstream, converged, and conflicting changes factually without inferring SemVer severity or semantic compatibility | Decided |
| D-DIST-10 | Automatic file merge, runtime overlay, compatibility matrix, history ledger, and combinatorial fallback search are excluded | Decided |
| D-DIST-11 | Analysis and selection are side-effect-free queries; staging, activation, backup, and checkpoint persistence remain separate injected boundaries, while one activation coordinator exclusively owns their mutation order and recovery | Decided |
| D-DIST-12 | Renewal returns one immutable structured operation result; a dedicated CLI presenter derives concise action-oriented text from those facts without preformatted domain strings, duplicated fact collections, or normal fingerprint exposure | Decided |
| D-DIST-13 | `pgmcp --upgrade` is the sole public renewal entry point; `--accept-template-baseline`, `--resolve-template`, and `--force-template-upgrade` are mutually exclusive intent modifiers that cannot run without it, and the CLI delegates policy and mutation to injected boundaries | Decided |
| D-DIST-14 | `pgmcp --upgrade --force-template-upgrade` explicitly requests complete candidate replacement for a managed actual root and requires a verified timestamped backup of the prior `template_suite/` plus `installation.json` outside the active `.pgmcp/` root before replacement begins | Decided |
| D-DIST-15 | `pgmcp --upgrade --resolve-template <component-id> [<component-id> ...]` advances only the named currently conflicted adopted entries to their machine-computed current candidate states after full validation; IDs are `shared` or exact `manifest.yaml:template_id` values, and no fingerprint input or content copy is accepted | Decided |
| D-DIST-16 | External roots never acquire managed overwrite authority from content equality; bootstrap or checkpoint advancement requires explicit owner action | Decided |
| D-DIST-17 | `.pgmcp/upgrade/` is the complete current non-authoritative candidate root and never becomes a history store | Decided |
| D-DIST-18 | Operational component fingerprints are distribution-only SHA-256/96 Base64url equality facts derived with the shared canonical source normalization; distinct shared/package domains prevent identity-kind aliasing, and these fingerprints never appear in scaffolded artifact provenance or package-directed scaffold/schema DTOs | Decided |
| D-DIST-19 | The first PGMCP v3 suite rollout has no predecessor v3 suite or checkpoint: no value is fabricated or converted from `.version` or `template_registry.json`; a checkpoint is computed only from a supplied, fully validated v3-format suite and becomes authoritative only through fresh installation, forced replacement, or explicit owner migration | Decided |
| D-DIST-20 | The CLI returns exit code `0` when renewal completed and no corrective renewal action remains, `2` when state is safe but baseline, reconciliation, retry, or recovery action remains, and `1` for validation, activation, or recovery failure; because renewal is CLI-only, it creates no MCP resource, JSON output mode, or persisted result report | Decided |
| D-DIST-21 | Activation uses one cross-process lock, a fully validated `template_suite.next/`, a temporary `template_suite.previous/`, and one immutable `template_upgrade.json` recovery record beside the active root; all directory moves stay on the same filesystem | Decided |
| D-DIST-22 | Recovery derives the only safe action from recorded prior/target identities and the durable trees/checkpoint: restore the prior pair before checkpoint publication, finish a complete target pair after publication, and fail without guessing when neither state is proven | Decided |
| D-DIST-23 | A running server keeps its already resolved immutable catalog; a new startup briefly takes the upgrade lock and rejects an unresolved recovery record; whenever actual changes, CLI presentation derives a restart hint from `actual_changed` without changing a successful exit code | Decided |
| D-DIST-24 | Forced replacement retains the verified pre-force suite/checkpoint backup at `.pgmcp_template_backup_<UTC-timestamp>/`; the result exposes its path, while PGMCP creates no backup index, pruning policy, or checkpoint authority from it | Decided |
| D-DIST-25 | Official adapters are authored and shipped directly in mcp_server/bundled_adapters, outside workspace assets; resolved_server_root/workspace_adapters remains owner-controlled. No separate adapter authoring-copy stage or adapter renewal mechanism | Human-approved W10 location boundary; remaining W10 configuration integration open |

## 5. Responsibilities and Boundaries

### 5.1 State Roles

The renewal boundary uses three state roles but still has one runtime suite:

| Role | Representation | Authority |
|---|---|---|
| Adopted | One complete current map of upstream component presence and operational fingerprints | Three-way comparison base |
| Actual | Complete configured active suite snapshot | Sole runtime authority and customization source |
| Candidate | Complete newly supplied and validated upstream suite snapshot | Non-authoritative selection and reconciliation source |

Adopted does not mean “current actual.” It records the last upstream component state
accepted beneath each component. A customized actual can therefore remain different from
adopted without blocking unrelated components.

The checkpoint is not a retained suite, locator, history, contributor list, package
version ledger, or artifact-provenance record. Actual and candidate facts are computed
from currently supplied trees.

### 5.2 Component Ownership and Operational Equality

The component key set is deterministic:

- reserved key `shared` owns the complete admitted `shared/` source subtree;
- every concrete component is keyed by `manifest.yaml:template_id`;
- a missing key in a complete checkpoint means that component was absent at the adopted
  state;
- duplicate `template_id` values and invalid suites fail before comparison;
- physical concrete-package directory names remain discovery details and never become
  component identity.

DI-06 requires an operational source fingerprint that changes when the complete admitted
source content of that component changes and remains independent of other components.
It is distinct from:

- package `version`, which is human release intent;
- resolved package fingerprint, which covers effective package semantics plus reachable
  shared support;
- source-suite fingerprint, which identifies only supplied generation sources, excluding
  .version/policy.yaml; it cannot prove installed-state equality.

Operational component fingerprints reuse the canonical record framing, source
normalization, digest truncation, and encoding fixed by D-SUITE-30: deterministic records
stream through SHA-256, the first 12 digest bytes are encoded as 16 unpadded Base64url
characters, all admitted source text (including JSON/YAML comments and descriptions where allowed)
is UTF-8 without a byte-order mark with LF line endings. Do not discard source details
through semantic-only serialization; this normalized source equality is not literal
byte-for-byte equality across encoding/line-ending variants.

The shared record uses the domain `pgmcp:template-component:shared:v1` and contains every
admitted member below `shared/`, keyed by its normalized path relative to `shared/`. The
package record uses the domain `pgmcp:template-component:package:v1`, the exact
`manifest.yaml:template_id` as logical component identity, and the normalized complete source contents
of ALL admitted package-local files, including manifest.yaml, context.schema.json,
template.jinja2, .version and policy.yaml. Version and policy remain included because
the checkpoint compares complete upstream component state, not generation identity. Shared content is excluded from a package component;
its change is represented by the independent `shared` component.

Both records exclude outer concrete-package directory names, modification times,
filesystem enumeration order, machine paths, runtime state, and every other concrete
package. No full-length parallel digest or per-file digest inventory is persisted.

### 5.3 Three-Way Selection

For each component, equality is determined from presence plus operational fingerprint:

| Adopted / actual / candidate relation | Classification | Proposed content | Checkpoint after successful activation |
|---|---|---|---|
| `X = A` and `C = A` | Unchanged | Actual | Adopted remains `A` |
| `X = A` and `C != A` | Upstream only | Candidate | Advance to `C` |
| `X != A` and `C = A` | Local only | Actual | Remain at `A` |
| `X = C` and both differ from `A` | Converged | Actual/candidate, which are equal | Advance to `C` |
| `X != A`, `C != A`, and `X != C` | Conflict | Actual | Remain at `A` pending explicit reconciliation |

`A`, `X`, and `C` each include absence. The selector is a pure query and returns an
immutable proposed source and checkpoint delta. It never mutates actual, candidate, or
installation state.

A conflict does not block selection of unrelated components. The conflicting actual
component remains in the proposal while non-conflicting candidate components may be
selected. Activation still requires the resulting complete suite to validate.

### 5.4 Additions and Removals

The same relation table covers lifecycle changes:

| Adopted | Actual | Candidate | Result |
|---|---|---|---|
| Absent | Absent | Present | Upstream addition; select candidate |
| Present | Same as adopted | Absent | Upstream removal; select absence |
| Present | Locally changed | Absent | Modification/removal conflict; retain actual |
| Absent | Present | Absent | Local addition; retain actual |
| Absent | Present | Different present value | Dual addition conflict; retain actual |
| Present | Absent | Same as adopted | Local removal; retain absence |
| Present | Absent | Changed present value | Removal/modification conflict; retain absence |

Package identity changes are represented as removal of one `template_id` value plus addition of
another; directory rename alone is not an identity change.

### 5.5 Proposal Validation and Activation

The proposal builder materializes a complete suite outside the active root from selected
actual and candidate components. It never edits actual in place. DI-01/DI-02 then applies
the same complete resolved-suite validation required for runtime catalog publication.

Validation proves that the proposed tree satisfies the known suite topology, schema,
graph, renderer, naming, profile, and startup-coherence contracts. It does not claim
general semantic or cross-version compatibility. A candidate release can establish
coherence of its own official packages; a locally customized package combined with
changed shared support must still pass proposal validation.

If validation succeeds, the activator replaces the complete managed actual tree through
the recoverable protocol defined in §§7.5 and 8. Checkpoint changes become authoritative only
with the corresponding active tree. If validation fails, actual and checkpoint remain
unchanged, the complete candidate is staged, and the result identifies proposal
validation rather than a component equality conflict.

DI-06 does not try other component combinations after validation failure.

### 5.6 Checkpoint Bootstrap

Bootstrap is resolved before ordinary three-way selection:

| Workspace condition | Bootstrap behavior |
|---|---|
| Fresh managed install | Validate candidate, install it, and establish its full component map in one authoritative operation |
| Existing managed actual with trustworthy persisted full operational component evidence matching actual | Require equal component presence and every full operational fingerprint against the supplied prior suite; never accept pf/sf or an untyped legacy hash; derive checkpoint only from the proven source |
| Existing managed actual equal to the validated candidate under full operational component comparison | Derive checkpoint from candidate without copying actual |
| Owner supplies a trusted complete prior suite | Validate it and derive the adopted component checkpoint; do not make it runtime authority |
| Existing workspace with no trustworthy basis | Preserve actual byte-for-byte, stage candidate, return `checkpoint_required`, and perform no component selection or activation |
| Existing external root | Never infer a checkpoint; require an owner-supplied prior suite or explicit `--accept-template-baseline` after a complete valid v3-format actual suite exists |

Bootstrap compares full operational component presence and values against an available
validated source tree. pf/sf cannot prove this equality or be decomposed into component
states. Missing or ambiguous identity-kind evidence requires checkpoint_required, never
a generation-hash fallback or a newly invented whole-suite hash.

`pgmcp --upgrade --accept-template-baseline` is the explicit checkpoint-less owner
action. It is accepted only when the current staged candidate and the complete actual
v3-format suite both validate and no checkpoint exists. PGMCP computes every component
fingerprint internally, records the candidate's complete component map as the upstream
comparison basis, and leaves actual content untouched. It accepts no component selector
or fingerprint argument because an initial checkpoint must be complete and callers do
not own computed identity values. The following ordinary comparison classifies actual
differences honestly as local, upstream, converged, or conflicting.

### 5.7 Candidate, Reconciliation, and Forced Replacement

Under the default server root, `.pgmcp/upgrade/` is itself the complete candidate suite
root. It has the same internal layout as `template_suite/`; no
`candidate/template_suite/` or history subtree is introduced. Runtime composition never
scans or loads it.

The staged candidate is replaced by the newest valid supplied candidate when staging is
needed again. Supersession does not change adopted state or actual content. If an
activation succeeds without remaining conflicts, no candidate is retained. When
conflicts or `checkpoint_required` remain, the complete candidate stays available for
human or agent work.

After content reconciliation, the owner or cooperating agent runs:

```text
pgmcp --upgrade --resolve-template <component-id> [<component-id> ...]
```

Each component ID is either the reserved `shared` identity or an exact concrete
`manifest.yaml:template_id`. The command accepts one or more unique IDs so independent package
conflicts can be closed without accepting unrelated unresolved components. It:

1. requires an existing complete checkpoint and current staged candidate;
2. validates the complete actual and staged candidate suites;
3. recomputes adopted, actual, and candidate component states internally;
4. rejects the complete request without checkpoint mutation when any named ID is
   unknown, duplicated, or not currently classified as a conflict;
5. advances each named adopted entry to its machine-computed current candidate state;
6. does not accept or expose a caller-supplied fingerprint and does not copy candidate
   content into actual;
7. removes the staged candidate only after no unresolved component conflicts remain.

No automatic observation of changed files can substitute for explicit owner intent when
a reconciled actual differs from both adopted and candidate. Candidate replacement is
itself an explicit `--upgrade` action; resolution always concerns the current validated
staged candidate and reports the accepted component fingerprints as output facts only.

`pgmcp --upgrade --force-template-upgrade` is deliberately different. It requires a
valid staged candidate and a managed actual root, writes and verifies a retained backup
at `.pgmcp_template_backup_<UTC-timestamp>/`, replaces actual with the complete candidate,
and replaces the checkpoint with the candidate component map. The backup contains only
the prior `template_suite/` and matching `installation.json`, is reported to the caller,
and is never a runtime or checkpoint authority. The command is rejected for external
roots. Backup failure prevents replacement from starting.

### 5.8 Responsibility Separation

The target separates:

- suite parsing, full validation, graph resolution, and existing provenance identities,
  owned by DI-01/DI-02;
- operational component-state derivation, pure three-way comparison, and immutable
  selection facts, owned by DI-06 queries;
- bootstrap and renewal disposition selection, owned by DI-06 policy;
- complete proposal construction and candidate staging, owned by narrow mutation
  services;
- cross-process exclusion, same-filesystem preparation, retained force backup,
  complete-tree activation, and interruption recovery, owned by one activation
  coordinator;
- current checkpoint reading and atomic file persistence, owned by one installation-state
  repository invoked within the activation coordinator's ordered mutation boundary;
- the thin `pgmcp --upgrade` CLI, consuming one injected orchestration boundary and
  presenting its result without deriving policy;
- package-specific behavior, remaining with DI-03;
- shared fixtures and cross-package assurance, remaining with DI-08.

Read-only consumers receive no mutation-capable interface. State readers and repositories
remain separate under ISP/CQS. The CLI depends on one renewal operation, not directly on
filesystem or checkpoint repositories. Composition-root wiring injects filesystem,
lock, state, identity, validation, and presentation dependencies.

## 6. Options and Rationale

### Selected — Component-Wise Three-Way Selection with Complete-Suite Activation

Compare adopted, actual, and candidate at `shared/` and `template_id` boundaries. Select
whole non-conflicting components, preserve conflicting actual components, construct one
complete proposal, validate it, and activate the complete tree recoverably.

Selected because package-local customization no longer blocks unrelated upstream
packages, while fingerprints provide stronger equality evidence than SemVer. The design
retains one runtime authority and avoids file merge, compatibility matrices, and history.

### Rejected — Complete-Suite-Only Fast-Forward

Replace candidate only when the whole actual tree equals one installed suite fingerprint.

Superseded because one local package customization indefinitely blocks unrelated package
and shared updates. Complete operational component equality remains a possible fast path,
not as the governing renewal model.

### Rejected — Automatic File or Semantic Merge

Merge differing files or interpret template semantics to synthesize conflict resolutions.

Rejected because it splits indivisible components, needs merge-base and conflict policy
per file type, and cannot provide a generic semantic-compatibility proof.

### Rejected — Runtime Overlays

Load official and workspace suites as precedence layers.

Rejected because it creates multiple runtime authorities, precedence rules, and hidden
composition state.

### Rejected — SemVer or Compatibility Matrix

Use version ranges or a base/package compatibility table to authorize renewal.

Rejected because package versions express human intent rather than actual local equality,
while a matrix creates ongoing authored maintenance and still cannot describe unversioned
workspace changes.

## 7. Detailed Design

### 7.1 Immutable Analysis Facts

The comparison result must carry, at minimum:

- actual and candidate operational component fingerprints for full installed-state equality
  (presence and every component must match); pf/sf cannot serve this purpose;
- checkpoint availability and bootstrap-evidence disposition;
- adopted, actual, and candidate presence/fingerprint facts per component;
- component classification and selected source;
- proposed checkpoint action per component;
- direct conflicts and candidate additions/removals;
- complete-proposal validation result when selection was permitted;
- no mutation performed by the DTO itself.

Facts are frozen and deterministically ordered: `shared` first, then concrete manifest
IDs lexicographically. Exact class names remain implementation-owned.

### 7.2 Current Installation State

The configured server root continues to own one `.pgmcp/installation.json`. Its exact
minimum contract is:

```json
{
  "pgmcp_version": "<installed-pgmcp-version>",
  "template_checkpoint": {
    "shared": "<16-character-fingerprint>",
    "packages": {
      "<manifest.yaml:template_id>": "<16-character-fingerprint>"
    }
  }
}
```

`pgmcp_version` is required and owns workspace/server compatibility. It does not identify
template-suite content. `template_checkpoint` is optional as a whole so the document can
represent a migrated or detected workspace for which no trustworthy adopted state yet
exists. When `template_checkpoint` is present, `shared` and `packages` are both required;
`shared` is exactly one operational fingerprint and `packages` is an object that may be
empty; every package value is also an operational fingerprint, never pf. The fixed JSON
shape is unchanged; sf is not a field in this checkpoint.

Every `packages` key is copied from the `template_id` of a validated concrete package manifest.
The directory name is never written as a key, inferred as an ID, or checked for textual
equality with the ID. Checkpoint writers reject duplicate `template_id` values before state
creation and serialize package keys lexicographically. A missing package ID in a complete
checkpoint means that package was absent at the adopted state; a missing checkpoint is
different from a complete checkpoint containing no packages.

The document is closed to additional fields. It contains no actual or candidate snapshot,
history, timestamps, artifact provenance, backup/transaction data, Git or release
locator, separate schema version, or ownership flag. Ownership is supplied by the
configured root boundary, and the installed PGMCP version is sufficient to select the
reader/migration contract; adding a second version field has no current consumer.

One fail-fast reader/repository owns the document. Writers publish it atomically only
when the corresponding bootstrap, activation, or explicit checkpoint-advancement command
has succeeded.

### 7.3 Operation Outcomes

The renewal operation classifies its completed attempt with one factual outcome. The
outcome, state effects, and candidate disposition determine the CLI exit code; prose does
not.

| Outcome | Exit | Actual effect | Checkpoint effect | Candidate disposition |
|---|---:|---|---|---|
| Fresh installed | `0` | Complete candidate activated | Complete checkpoint created | Removed |
| Unchanged | `0` | Unchanged | Unchanged | Removed or absent |
| Baseline established | `0` | Unchanged | Complete checkpoint created | Removed |
| Activated | `0` | Complete proposal activated | Complete checkpoint advanced | Removed |
| Activated with conflicts | `2` | Complete valid proposal activated | Only selected non-conflicting or converged entries advanced | Retained |
| Checkpoint required | `2` | Unchanged | Not created | Staged and retained |
| Reconciliation completed | `0` when no corrective action remains; otherwise `2` | Unchanged | Only named, revalidated conflicted entries advanced | Removed when no conflict remains; otherwise retained |
| Upgrade busy | `2` | Unchanged | Unchanged | Existing candidate unchanged |
| Interrupted activation rolled back | `2` | Prior actual restored | Prior checkpoint restored | Retained |
| Forced candidate installed | `0` | Complete candidate activated after backup | Complete checkpoint created or replaced | Removed |
| Candidate unavailable or invalid | `1` | Unchanged | Unchanged | Existing staged candidate is not silently reclassified |
| Proposal invalid | `1` | Unchanged | Unchanged | Retained |
| Activation or recovery failed | `1` | Last proven tree is preserved or recovery material is left untouched | Never names an uninstalled state | Retained until recovery completes |

Exit code `2` means that the command left the workspace in a safe state but corrective
renewal action is still required. It is not collapsed into an execution failure. `checkpoint_required`,
component conflicts, proposal invalidity, and activation or recovery failure remain
distinct factual outcomes.

### 7.4 Structured Result and CLI Presentation

The renewal operation returns one immutable structured result for its direct CLI
consumer. It contains only the facts needed to present and act on the completed attempt:

| Fact group | Required content | CLI use |
|---|---|---|
| Outcome | One outcome from §7.3 | Select heading and exit code |
| State effects | Whether actual changed and whether the checkpoint was unchanged, created, or advanced | State what became authoritative |
| Candidate | Disposition and optional `.pgmcp/upgrade/` path | State whether reconciliation material remains |
| Backup | Optional verified force-backup path | Show where the replaced suite/checkpoint pair remains recoverable |
| Components | Deterministically ordered component records with ID, kind, three-way relation, selected source, and checkpoint action | Derive updated, locally preserved, conflicting, and resolved groups |
| Validation or failure | Factual stage and validation/recovery evidence when applicable | Explain why activation did not complete |
| Available actions | Action kind plus affected component IDs | Render the exact permitted next command |

The ordered component records are the single source for component groupings. The result
does not repeat them in separately stored `updated_components`, `conflicts`, or similar
presentation collections, and it carries no human sentences or preformatted commands.

A dedicated CLI presenter owns wording, grouping, line wrapping, and command rendering.
Normal output shows the outcome, actual/checkpoint effects, actionable component groups,
candidate path when retained, factual failure evidence when relevant, and the next
permitted command when owner action remains. Every actionable component ID is shown;
wrapping is allowed, silent truncation is not, because this CLI path has no resource
fallback. Fingerprints remain internal comparison facts: callers never provide them and
normal CLI output does not display them.

Whenever `actual_changed` is true, the presenter appends: `Restart any running pgmcp
server to load the new template suite.` It omits the hint when actual is unchanged. The
hint is derived from the existing state-effect fact, adds no duplicate `restart_required`
field, and does not change a successful exit code.

`pgmcp --upgrade` is a CLI operation, not an MCP operation. It therefore creates no MCP
resource or cache URI, adds no JSON-output mode, and persists no duplicate result report.
Ordinary diagnostic logging remains outside this presentation contract and never becomes
checkpoint authority. A future MCP renewal tool would require its own Design decision
and would then follow the workspace MCP DTO/cache presentation standard rather than
retroactively changing this CLI contract.

#### Consumer-facing projection examples

A completed renewal with no required action returns `0`:

```text
Template upgrade completed.

Actual suite: updated
Checkpoint: advanced
Updated from candidate: shared, planning
Preserved locally: design
Candidate: removed

Restart any running pgmcp server to load the new template suite.
```

A renewal that safely activates non-conflicting components but retains a conflict returns
`2`:

```text
Template upgrade completed with conflicts.

Actual suite: updated
Checkpoint advanced: shared, planning
Preserved locally: research
Conflicts: design
Candidate: .pgmcp/upgrade/

Reconcile package "design", then run:
pgmcp --upgrade --resolve-template design

Restart any running pgmcp server to load the new template suite.
```

A workspace without a trustworthy adopted state remains unchanged and returns `2`:

```text
Template upgrade requires a baseline.

Actual suite: unchanged
Checkpoint: not created
Candidate: .pgmcp/upgrade/
Reason: no trustworthy adopted template state is available.

Next:
- migrate local templates and run:
  pgmcp --upgrade --accept-template-baseline
- or replace the managed suite using:
  pgmcp --upgrade --force-template-upgrade
```

A successful final reconciliation returns `0`:

```text
Template conflict resolved.

Actual suite: unchanged
Checkpoint advanced: design
Remaining: none
Candidate: removed
```

If other conflicts remain, the same reconciliation projection lists them, retains the
candidate, renders their next permitted command, and returns `2`. A proposal-validation
failure returns `1`:

```text
Template upgrade failed: proposed suite invalid.

Actual suite: unchanged
Checkpoint: unchanged
Candidate: retained
Validation stage: complete proposal
Failure: <factual validator evidence>
```

### 7.5 Activation Filesystem State

The activation boundary uses fixed, self-explanatory paths relative to the workspace. Only
`template_suite/` and `installation.json` are authoritative:

| Path | Lifetime | Role |
|---|---|---|
| `.pgmcp/template_suite/` | Persistent | Sole active suite read at startup |
| `.pgmcp/installation.json` | Persistent | PGMCP compatibility and current adopted checkpoint |
| `.pgmcp/upgrade/` | Until no conflict or migration action remains | Complete non-authoritative candidate |
| `.pgmcp/template_suite.next/` | One activation attempt | Fully constructed and validated target tree |
| `.pgmcp/template_suite.previous/` | One activation attempt | Prior actual tree available for rollback |
| `.pgmcp/template_upgrade.json` | One activation attempt | Immutable facts required to recognize prior and target states |
| `.pgmcp/template_upgrade.lock` | Lock endpoint | Cross-process exclusion for recovery, activation, and startup catalog construction |
| `.pgmcp_template_backup_<UTC-timestamp>/` | Retained after forced replacement | Verified copy of prior `template_suite/` and `installation.json` |

The recovery record is written atomically before the first authoritative move. It stores
only the prior and target suite presence and complete operational component maps, the prior and target installation
payloads, the intended candidate disposition, and the optional force-backup path. These
are internal recovery facts, not caller input or history. The record has no mutable
`phase` field: recovery determines progress by comparing the durable paths and checkpoint
with the recorded prior and target identities.

The activation command owns the cross-process lock for its complete recovery and mutation
window. A runtime startup takes the same lock only while checking recovery state and
building its immutable catalog. If an unresolved recovery record exists, startup fails
before catalog construction and directs the owner to rerun `pgmcp --upgrade`; startup
never mutates recovery state. A server that completed startup earlier keeps its old
in-memory catalog safely and is explicitly told to restart after an actual-suite change.

The retained force backup is complete and verified before authoritative mutation begins.
It is outside the active `.pgmcp/` root, is never scanned at runtime, and is not indexed
or pruned by PGMCP. Its timestamp prevents replacement of earlier owner recovery material;
retention and deletion remain owner decisions.

### 7.6 Bundled and Workspace Adapter Delivery

**Human-approved W10 location decision, 2026-09-11.** This section implements
DI-05 D-ADAPTER-30 without changing template renewal, adapter roles or trust policy.

| Material | Authoring / distribution location | Workspace delivery |
|---|---|---|
| Official adapter packages | Authored directly in `mcp_server/bundled_adapters/`; retained there in the installed distribution | Never copied into the workspace extension store |
| Workspace adapter packages | `resolved_server_root/workspace_adapters/` | Owner-managed, explicitly trusted; never collected as official build input or replaced by server asset renewal |
| Template suite | `.pgmcp/template_suite/` to installed `mcp_server/assets/template_suite/` | Existing DI-06 coherent suite/checkpoint operations |

The current CLI init copies the complete assets tree and WorkspaceUpgrader walks its
files. Keeping bundled adapters outside that tree avoids an adapter-specific exclusion
in both consumers. Selective asset copying could work but offers no benefit for code
that never belongs in workspace installation material. Direct authoring also removes
the proposed `adapter_packages/` to `assets/adapter_suite/` build-copy stage. This does
not remove the already required distinction between template renewal and config delivery.

`pyproject.toml` must include all declared bundled adapter files in the distribution,
not only Python modules. Installed-package evidence must verify manifests, scripts,
schemas and dependency contributions from outside the source checkout, including the
commit adapter's shared header-reader dependency. No copied parser, source-path import
fallback or native dependency auto-installer is introduced. DI-08 may provide a reusable
built-wheel fixture; DI-06 owns its delivery assertions, DI-05 its adapter conformance.

Both roots contain the same manifest-driven, language-agnostic package kind. Directory
placement is excluded from package fingerprint inputs under DI-05; these source names
do not create another version or fingerprint layer. Duplicate IDs remain errors, not
overrides. Bundled packages change with the installed server release and are loaded
into the next startup catalog; workspace packages remain independently owner-controlled.

The older workspace `adapter_suite` label in frozen Research is concretized by this
human-approved Design naming decision; no alias or dual discovery is supported.
W10 configuration integration remains a separate open workshop item. No config merge,
overwrite policy or whole-W10 approval is implied by this location decision.

## 8. Control, Data, and State Flow

### Fresh Managed Install

1. Validate and resolve the supplied candidate.
2. Derive its complete component checkpoint.
3. Prepare candidate content and checkpoint as one recoverable operation.
4. Activate the complete managed actual root.
5. Publish checkpoint state only for the activated tree.
6. Leave no `.pgmcp/upgrade/` candidate.
7. Runtime startup later loads only actual.

### Checkpoint-Less Bootstrap

1. Validate actual and candidate without mutating either.
2. Evaluate only the trustworthy evidence routes approved by Research.
3. If evidence proves an available prior suite equals actual, derive adopted from that
   suite.
4. Else if actual equals candidate, derive adopted from candidate without copying.
5. Else if the owner supplies a trusted complete prior suite, validate it and derive
   adopted from it.
6. Otherwise stage candidate, return `checkpoint_required`, and leave actual and
   installation state unchanged.
7. A checkpoint-less owner may run `pgmcp --upgrade --accept-template-baseline` only
   after actual is a complete valid v3-format suite; the command derives the full
   checkpoint from the current candidate and copies no content.
8. External roots always require explicit owner action even when equality is observed.

### Managed Component-Aware Renewal

1. Validate actual and candidate independently and load the complete checkpoint.
2. Derive operational states for adopted, actual, and candidate components.
3. Classify and select each component using §5.3.
4. Construct the complete proposal outside actual.
5. Validate and resolve the complete proposal.
6. If invalid, preserve actual/checkpoint and stage candidate.
7. If valid, activate the complete proposal recoverably and publish only its successful
   checkpoint delta.
8. Retain candidate when conflicts remain; otherwise remove stale staging.
9. Runtime continues to load only the complete actual root.

### Human or Agent Reconciliation

1. Inspect actual, the adopted comparison facts, and `.pgmcp/upgrade/`.
2. Reconcile conflicted actual components without making candidate a runtime root.
3. Run `pgmcp --upgrade --resolve-template` with one or more reconciled `shared` or
   `template_id` component names.
4. Validate complete actual and candidate suites and recompute their component facts.
5. Advance only the named conflicted checkpoint entries to current machine-computed
   candidate states without copying content.
6. Remove candidate only when the current candidate has no remaining conflicts.

### Explicit Forced Candidate Replacement

1. Require a managed actual root and valid staged candidate.
2. Complete the explicit backup before any replacement.
3. Prepare candidate and its complete checkpoint.
4. Replace the complete actual tree recoverably.
5. Publish the complete candidate checkpoint only for installed content.
6. Remove candidate only after success.
7. On any pre-activation failure, actual and checkpoint remain unchanged.

### Recoverable Complete-Tree Activation

Every fresh install, managed proposal activation, and forced replacement uses the same
ordered boundary:

1. Acquire the cross-process upgrade lock.
2. If a recovery record exists, resolve it before accepting a new attempt.
3. Validate actual, candidate, and the intended checkpoint transition.
4. Construct `template_suite.next/` on the same filesystem as `template_suite/` and run
   complete DI-01/DI-02 validation against it.
5. For forced replacement, create and verify the retained timestamped backup. Failure
   here leaves actual and installation state untouched.
6. Atomically write the immutable recovery record containing the proven prior and target
   facts.
7. Rename existing `template_suite/` to `template_suite.previous/`, then rename
   `template_suite.next/` to `template_suite/`. A concurrent startup cannot enter this
   window because it requires the same lock.
8. Atomically publish the target `installation.json` only after the complete target tree
   occupies the active path.
9. Verify the active tree and installation state against the recorded target facts.
10. Apply the decided candidate disposition, remove transient prior/next material and the
    recovery record, then release the lock.

Directory moves are never described as one atomic tree-plus-checkpoint write. Safety
comes from same-filesystem moves, exclusion, retained rollback material, one atomic
checkpoint file write, and deterministic recovery.

### Failure, Interruption, and Recovery

Candidate validation, selection, proposal validation, staging, backup, activation, and
checkpoint persistence expose distinct failure stages. Runtime must never observe a
partially written tree. Installation state must never authorize a component state that
was not activated or explicitly accepted.

After acquiring the lock, recovery compares the durable paths and `installation.json`
with the immutable record:

| Proven durable state | Recovery action | Result |
|---|---|---|
| Prior actual and prior installation still authoritative | Remove incomplete `next` material and the recovery record | Prior pair retained |
| Actual missing and `previous` proves the prior actual | Rename `previous` back to actual and restore the prior installation payload | Prior pair restored |
| Target actual active but prior installation still published | Move the uncommitted target aside, restore `previous`, and atomically restore the prior installation payload | Prior pair restored; candidate retained |
| Target actual and target installation both authoritative | Finish candidate/transient cleanup according to the record | Target pair retained |
| Any tree or installation state matches neither recorded prior nor target facts | Preserve every path and stop without mutation | Manual inspection required |

A successful rollback after interruption returns the safe/action-required exit code `2`
and retains the candidate for a deliberate retry. An unrecognized or failed recovery
returns `1`. Normal runtime startup never performs these writes: it fails fast on the
record and tells the owner to rerun `pgmcp --upgrade`.

The current per-file atomic writer remains suitable for the recovery record and
`installation.json`; it is not treated as evidence that the multi-path transition itself
is atomic. Successful ordinary activation leaves no recovery record or retained
`previous` tree. Only explicit forced replacement leaves the separately reported backup.

## 9. Compatibility, Migration, and Removal

The clean break removes current per-file renewal that preserves configuration while
overwriting template assets independently. It also supersedes the interim
complete-suite-only Design model.

The following do not become checkpoint authority:

- `template_registry.json`, because it is usage-dependent artifact provenance;
- scaffolded artifact `pf` or `sf`, because they identify artifact source rather than the
  current upstream baseline beneath every component;
- upgrade logs or backups, because they are evidence/recovery rather than current state;
- Git history, because PGMCP does not inspect or require it;
- package SemVer, because equality requires actual content evidence.

The legacy scalar `.pgmcp/.version` supplies only its existing PGMCP compatibility value
to the first `pgmcp --upgrade` migration. It supplies no component checkpoint. After
successful state migration, normal startup reads only `installation.json`; no permanent
dual-read shell remains.

### First PGMCP v3 Suite Rollout

Before issue 460 is implemented and packaged, no released v3-format `template_suite/`
or operational component checkpoint exists. Design examples therefore contain
metavariables rather than claimed current fingerprints. Packaging must first construct
and fully validate the actual v3 candidate, then compute its real `shared` and `template_id`
component fingerprints from those supplied bytes. A missing or invalid candidate cannot
create or advance `template_checkpoint`.

An existing pre-v3 workspace is not classified as a fresh installation merely because
its new `template_suite/` root is absent. Its legacy `.pgmcp/templates/` tree has no
validated `template_id` component boundaries, so PGMCP cannot honestly derive adopted
v3 component states from that tree. Neither `.pgmcp/.version` nor
`template_registry.json` is converted into component fingerprints: the former records
only compatibility and the latter is usage-dependent, incomplete provenance state.

The first `pgmcp --upgrade` therefore treats such a workspace as checkpoint-less. It
preserves the legacy actual bytes, validates and stages the complete v3 candidate, and
returns `checkpoint_required`; it does not silently switch the runtime root. The owner
then chooses one of the already approved explicit migration routes:

- for a managed root, `--force-template-upgrade` backs up the legacy installation,
  installs the complete candidate, and creates the candidate checkpoint;
- for retained local customization, the owner or cooperating agent first produces a
  complete valid v3-format actual suite, after which `--accept-template-baseline`
  records the current candidate as adopted without overwriting that reconciled actual
  content;
- for an external root, the external owner performs or authorizes the equivalent content
  migration and checkpoint decision; PGMCP never assumes overwrite authority.

Only the successful explicit migration establishes the first authoritative v3 checkpoint.
All later upgrades use ordinary component-wise three-way selection. This one-time clean
break implements the approved manual deployment migration without a legacy-layout
adapter, invented mapping, fabricated fingerprint, or permanent compatibility shell.

Earlier trustworthy persisted full operational component evidence may bootstrap only
when its available source suite matches actual in component presence and every complete
operational fingerprint. A prior sf/pf or unknown hash kind is insufficient. Where current workspaces have no
such evidence and actual differs from candidate, migration returns
`checkpoint_required`. The owner may then supply a trusted prior suite, run
`--accept-template-baseline` without copying candidate content after actual is a valid
v3-format suite, or force the managed candidate after backup.

The superseded 2026-08-31 component-adoption deferral is removed from active Design.
No dormant complete-suite-only policy interface or compatibility switch is retained.

## 10. Test and Validation Design

DI-06 package-owned evidence must prove:

- fresh managed installation establishes one coherent actual root and complete checkpoint
  together;
- operational component equality is content-derived and independent of SemVer;
- package-local change does not change another package's operational fingerprint;
- shared change does not masquerade as a package-local change;
- physical package-directory rename leaves `template_id` component identity stable;
- all five three-way relations select the required source and checkpoint action;
- absence covers upstream/local additions and removals, dual additions, and
  modification/removal conflicts;
- a conflict preserves actual while unrelated non-conflicting components remain
  selectable;
- proposal validation happens before activation and invalid proposals leave actual and
  checkpoint unchanged;
- activated content and checkpoint cannot become an authoritative mismatched pair;
- fresh, persisted-equality, candidate-equality, and owner-supplied bootstrap paths derive
  the correct complete checkpoint;
- the installation document accepts only the exact closed contract, requires `shared`
  whenever a checkpoint exists, and keys every package entry by validated
  `manifest.yaml:template_id` rather than its storage directory;
- the first v3 rollout computes no checkpoint before a complete candidate exists and
  converts neither legacy `.version` nor `template_registry.json` into component state;
- a missing or invalid first v3 candidate leaves checkpoint state unchanged, while a
  pre-v3 workspace with a valid staged candidate remains byte-identical and returns
  `checkpoint_required` until explicit migration;
- missing, mismatched, or untrusted bootstrap evidence returns `checkpoint_required`,
  stages candidate, and leaves actual byte-identical;
- external workspaces never infer managed overwrite authority;
- `--accept-template-baseline` creates only a complete checkpoint and
  `--resolve-template` advances only named conflicted entries; neither accepts a
  fingerprint input nor copies candidate content;
- forced replacement requires a complete backup and never targets an external root;
- stale candidate replacement retains only the current complete candidate and creates no
  history;
- every recognized interruption point either restores the proven prior tree/checkpoint
  pair or completes the proven target pair, while an unrecognized state is preserved and
  fails without a guessed mutation;
- concurrent upgrades are excluded across processes, and a concurrent startup cannot
  construct a catalog during activation;
- an already running server retains its old immutable catalog, a later startup loads only
  the committed actual suite, and the CLI restart hint appears exactly when actual changed;
- forced replacement exposes a verified timestamped backup containing the prior suite and
  matching installation document, while backup failure prevents activation;
- successful ordinary activation leaves no recovery record or previous tree;
- runtime catalog construction never reads candidate, proposal, rollback, or backup
  trees;
- no artifact metadata or scaffold/schema DTO acquires operational checkpoint identities;
- the immutable renewal result carries facts rather than human sentences, preformatted
  commands, or duplicate component groupings;
- CLI projection derives action-oriented groups and exact permitted next commands from
  those facts, shows every actionable component ID, and maps completed/no-action,
  safe/action-required, and failed outcomes to exit codes `0`, `2`, and `1`;
- fingerprints remain absent from caller input and normal CLI output;
- the CLI path creates no MCP resource, JSON output, or persisted result report;
- ordinary fixtures require no history archive, Git association, compatibility matrix, or
  provenance registry.

DI-08 may supply temporary suite builders, component-state factories, filesystem fakes,
interruption fixtures, and comparison assertions. DI-06 retains behavioral ownership.
Tests use public analysis, renewal, bootstrap, reconciliation, and state-reader boundaries
rather than private helpers or full prose snapshots.

## 11. Integration Risks

| ID | Item | Resolution Condition |
|---|---|---|
| R-DIST-01 | Operational identities are confused with artifact provenance | Keep distinct names, domains, state stores, DTOs, and absence from artifact/scaffold outputs |
| R-DIST-02 | Current checkpoint grows into a historical registry | Persist exactly one complete adopted map and replace entries; never append versions or snapshots |
| R-DIST-03 | Component selection is mistaken for in-place partial mutation | Build and validate a complete proposal; activate only the whole tree |
| R-DIST-04 | Suite validation is presented as semantic compatibility proof | Report known invariant validation only and make no generic compatibility claim |
| R-DIST-05 | Reconciliation acceptance silently blesses unresolved content | Require explicit owner intent, complete actual/candidate validation, recomputed current candidate component facts, and bounded conflict evidence |
| R-DIST-06 | Activation and checkpoint persistence diverge after interruption | The immutable recovery record and §8 state table must prove rollback, forward completion, or fail-without-mutation for every durable transition state |

## 12. Planning Consequences

Planning must later separate deliverables for:

- operational component-state derivation and pure three-way selection;
- installation-state reading, the exact `template_id` checkpoint contract, checkpoint
  bootstrap, and legacy `.version` migration;
- first-v3-rollout handling that never fabricates or converts a component checkpoint;
- complete proposal construction and DI-01/DI-02 validation integration;
- flat candidate-root staging and supersession;
- the fixed activation paths, cross-process lock, immutable recovery record,
  same-filesystem tree moves, atomic checkpoint publication, deterministic recovery, and
  timestamped force-backup boundary;
- the immutable renewal-result contract, dedicated CLI presenter, and `0`/`2`/`1`
  exit-code mapping, including complete actionable component output and a restart hint
  derived only from actual-suite change, without an MCP or persisted-report fallback;
- thin `--upgrade` dispatch with mutually exclusive baseline acceptance,
  component-bounded `--resolve-template`, and complete forced-replacement policies;
- migration from current file-class and interim complete-suite-only renewal;
- package-owned behavioral evidence and DI-08 shared infrastructure.

Planning may not introduce file merging, runtime overlays, per-file versions, checkpoint
history, SemVer compatibility inference, artifact-provenance reuse, or package-by-package
active-tree writes.

## 13. Traceability Matrix

| Obligation | Design Coverage |
|---|---|
| F-10 mixed-version renewal | D-DIST-01–D-DIST-24 and §§5.3–5.8, 7.5, 8–10 |
| Amended F-10/S-10 component renewal | Three-way selection and complete-proposal activation in §§5.3–5.5 |
| Checkpoint-less bootstrap remediation | D-DIST-08/D-DIST-16 and §§5.6, 8, 9 |
| F-11 generation identities are amended | pf/sf exclude version/policy/external validation; §§1 and 5.2 keep full operational component equality separate for all upgrade/checkpoint/recovery decisions |
| I-03 package isolation | Manifest-ID components and package-local operational equality in §§5.2–5.4 |
| I-14 shared test architecture | DI-08 supplies infrastructure; DI-06 owns renewal behavior |
| I-17 component-aware one-root renewal | D-DIST-01/D-DIST-04–D-DIST-07 and §§5.3–5.5 |
| I-18 trustworthy checkpoint bootstrap | D-DIST-08/D-DIST-16 and §5.6 |
| E-10 coherent renewal | Complete proposal validation plus the exclusion, activation, and recovery protocol in §§7.5 and 8 |
| E-17 durable test architecture | Public-boundary evidence in §10 |
| E-21 component-aware renewal result | §§5.3–5.7 and 7.3 |
| E-22 safe checkpoint bootstrap | §§5.6, 8, and 10 |
| DI-06 | Entire document |
| XC-01 | SRP/CQS separation, frozen query facts, narrow mutation/state interfaces, and fail-fast validation |
| XC-02 | Current file-class renewal, obsolete registry authority, and superseded interim policy are removed in §9 |
| RC-01 | The amended Approved Strategy is implemented without altering F-11 or unrelated compatibility decisions |

## 14. Related Documentation and Version History

### Related Documentation

- [Design Hub](design.md)
- [Suite Resolution Design](design-suite-resolution.md)
- [Shared Contracts Design](design-shared-contracts.md)
- [Research](research.md)
- [Research Findings](research-findings.md)
- [Design Intake Map](design-intake-map.md)
- [Deferred Work](deferred-work.md)
- [Pre-Implementation Documentation Contract](README.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

### Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.11 | 2026-09-11 | `@imp designer` | Record approved bundled/workspace adapter delivery separation, direct authoring outside assets and installed-package evidence; leave W10 config integration open. |
| 1.10 | 2026-09-11 | `@imp designer` | Record human-reported independent generation-identity QA GO and Design resumption; preserve remaining workshop decisions. |
| 1.9 | 2026-09-11 | `@imp researcher` | Clarify operational fingerprint consumers, complete source coverage, bootstrap/recovery maps and generation-identity exclusion after QA; no new metadata or merge policy. |
| 1.8 | 2026-09-10 | `@imp researcher` | Preserve full component equality including .version/policy.yaml while generation pf/sf excludes them; no change to three-way policy. |
| 1.7 | 2026-09-03 | `@imp designer` | Align every distribution component and checkpoint key with the clarified `manifest.yaml:template_id` authority; compact persisted provenance retains `id` only as its versioned short-form dialect. |
| 1.6 | 2026-09-03 | `@imp designer` | Close recoverable activation with cross-process exclusion, fixed same-filesystem transient paths, immutable fact-based recovery, a timestamped force backup, startup fail-fast behavior, and an `actual_changed`-derived server-restart hint. |
| 1.5 | 2026-09-03 | `@imp designer` | Close the CLI presentation workshop with one immutable factual result, a dedicated action-oriented presenter, explicit `0`/`2`/`1` exit semantics, complete actionable IDs, and no MCP resource, JSON mode, persisted report, caller fingerprint, or normal fingerprint display. |
| 1.4 | 2026-09-03 | `@imp designer` | Close the owner-intent CLI workshop: keep computed fingerprints internal, define whole-candidate `--accept-template-baseline`, and use component-bounded `--resolve-template` with `shared` or `template_id` values after content reconciliation. |
| 1.3 | 2026-09-03 | `@imp designer` | Close the checkpoint-contract workshop: require `shared`, key packages by `manifest.yaml:template_id`, fix the 16-character operational fingerprint records, and define the no-fabrication first-v3 migration from a legacy suite without a predecessor checkpoint. |
| 1.2 | 2026-09-03 | `@imp designer` | Reconcile the human-approved F-10/S-10 amendment: component-wise adopted/actual/candidate selection, trustworthy checkpoint bootstrap, operational component equality, complete off-root validation, recoverable one-root activation, explicit reconciliation, and removal of the superseded component-adoption deferral. |
| 1.1 | 2026-08-31 | `@imp designer` | Fix `.pgmcp/installation.json` with one optional installed-suite checkpoint, flatten the staged candidate to `.pgmcp/upgrade/`, route renewal through `pgmcp --upgrade`, add explicit complete `--apply-candidate` promotion, and keep selective reconciliation state-free. |
| 1.0 | 2026-08-31 | `@imp designer` | Establish package-aware actual/candidate comparison and agent-oriented candidate reconciliation while retaining the complete suite as the only automatic mutation unit and deferring component-level adoption. |
