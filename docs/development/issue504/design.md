<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=KoFPQ3-cAAWFeesb -->

# Issue 504 — Native configuration composition

**Status:** DESIGN — INDEPENDENT REVIEW REQUESTED  
**Version:** 0.6  
**Last Updated:** 2026-10-15

## Purpose

Define defaults plus workspace overrides using native Pydantic Settings deep merge, addressable mapping objects, explicit deletion and explicit execution order.

## Scope In

Workspace configuration, ConfigLoader, existing config models and their directly affected consumers/tests; github.yaml and its approved bootstrap/Settings boundary; temporary init-reset removal; active setup/config documentation and the Documentation-phase PR closing-template correction.

## Scope Out

release_manifest.yaml in its entirety, builders, assets routing, distribution/upgrade/activation, releases, #505, #506/#508 implementation, native tool configuration changes, state/commit/planning DTO redesign, compatibility bridges and suite-wide test cleanup.

## Prerequisites

[Research](research.md) v0.19 records the owner's final mapping/native-merge decision and the earlier factual consumer inventory. Earlier list-id/materializer proposals are superseded.

## Problem Statement

Anonymous object lists require custom matching for targeted overrides. Several existing configs already use mappings and support native field inheritance. Represent all addressable object collections consistently as mappings; do not build a second merge implementation or source-to-runtime translation framework.

## Functional Requirements

- Read defaults/<file>.yaml and optional root <file>.yaml from exactly the selected config_root.
- Use the mapping key as the sole authored object identifier. No repeated id field and no use of dispatch type, display name or external login as an implicit selector.
- Nested object collections are mappings too. Scalar/value lists remain whole field values and may use dashes or flow notation.
- Native deep merge owns additions, nested field updates, inherited content and replacement of scalar/null/list values.
- Own composition extensions are limited to explicit $delete handling and order validation/use.
- Preserve configuration_choice:null startup acceptance and existing selected-use/report behavior.
- Preserve effective repository policy, references and meaningful ordering after source separation.
- Keep loading read-only and standalone package declarations independent.
- Interactive Implementation is an owner requirement: Planning must pause before starting work and define small reviewable implementation steps.

## Nonfunctional Requirements

No file/tool/workflow dispatch in merge code; no custom ID-list matcher, configurable merge strategy registry, parallel schema family or generic runtime-shape materializer. Existing Pydantic models own field/domain validation and existing model admission seams own container normalization. Diagnostics identify source and path without source dumps or secrets.

## Constraints

Clean break for changed authored config and technical identity contracts; no old-shape converter or compatibility aliases. Preserve ConfigLoader constructor and entry points. Source schema/model changes and directly required consumer changes are allowed; unrelated consumers do not learn layering. Existing reference values, shared CheckSpec, state, commit and public planning/tool contracts remain stable.

## Options

| Structure | Assessment |
| --- | --- |
| Anonymous object lists, even with id fields | Native deep merge replaces the list; custom matching would be needed. Rejected. |
| Shallow replacement of complete groups | Repeats inherited content and loses future additions. Rejected. |
| ID-keyed mappings, native deep merge, narrow delete/order extensions | Selected by owner; reuses the standard algorithm. |
| Per-file converters or metadata-driven runtime-shape engine | Unnecessary after source normalization. Rejected. |

## Decision

Use Pydantic Settings native source composition over strictly parsed documents. Object identity is the mapping key; order is independent data where sequence has meaning. Existing domain models remain authoritative. No additional declaration/translation metadata is introduced.

## Rationale

A path such as enforcement.branch_mutation_context.actions.loaded_context is directly addressable by recursive dictionary merge. The nested exempt_tools list remains one value. Changing dashes to brackets never changes merge semantics.

## Key Decisions

### Source and identity grammar

Object collections contain string keys and object values. IDs are nonempty and exact, without automatic case/whitespace conversion; existing narrower key constraints remain. Duplicate keys are rejected before dictionary construction. A key identifies only within its parent; local IDs may recur under different parents.

Singleton records, string maps (templates/commit types), references and ordinary field names do not acquire extra identity wrappers. Real payload name/login/number/field/type properties retain their domain meaning. Technical name/operation_id duplicates disappear where the mapping key already supplies identity.

### Leaf list grammar

Lists of scalar values are literal ordered sequences. Their order and duplicates are retained and overrides replace the entire list, including []. Both YAML spellings are allowed. A collection of objects with fields uses a mapping even if each object contains only scalar fields. Empty object collections use {}, not []; the model defines the intended type.

### Order grammar

Every formerly ordered object-list collection gains an explicit order: strict integer on each complete/new member. Partial updates inherit it. Unique sibling ranks are required after composition; ascending rank determines execution/presentation, with no tie-break, auto-append or renumbering. Initial spaced ranks preserve the current sequence.

Lookup-only catalogs need no artificial order. Ordinary value lists retain their explicit sequence and do not need per-item ranks. Model-declared ordered members use one reusable pure order validator/helper in the config layer. Do not infer ordered collections by filename or by accidental payload keys. Order remains a typed config property, not a directive leaked into shared runtime DTOs.

### Deletion grammar

Only the exact singleton mapping {$delete: true} is a command; false, null, strings, sibling payload fields or a missing target are errors. The reserved key cannot be authored as ordinary config data. Defaults and standalone complete files reject commands.

Deletion targets an inherited mapping member or record field, never a list position. Null stays null and {} is a mapping no-op. Required-field/default/reference behavior is determined by final model validation.

## Questions

No owner strategy choice remains. Independent QA must assess these contracts before progression. Any need for additional composition operators, migration, a broad materializer or altered public runtime DTOs reopens the boundary rather than extending this design silently.

## Production Design

| Owner | Responsibility |
| --- | --- |
| ConfigLoader | Select required/optional files; strict safe parse; source/version errors; invoke composition and domain admission |
| config/composition.py | Pure delete preprocessing plus public native source composition; reject malformed/unknown commands; return fresh ordinary data |
| Pydantic Settings | Recursive mapping merge and standard scalar/null/list replacement |
| Existing config models/shared ordering helper | Object types, order validity, domain/reference validation and justified container admission |
| Existing direct consumers | Consume changed identity containers/order; no knowledge of defaults/overrides or commands |
| ConfigLayer/bootstrap | One resolved GitHub configuration and the existing registration/resource policy |
| CLI | Remove temporary acknowledgement reset, retain other lifecycle behavior |

### Native dependency and call boundary

Add pydantic-settings==2.13.1 as a direct runtime dependency, the inspected and demonstrated release. Let its declared Pydantic compatibility requirements be satisfied explicitly by dependency resolution; do not claim the present pydantic>=2.5 alone supplies this API. Use no experimental/private Pydantic functions.

compose_configuration(defaults, override) returns plain data. Internally a small config-owned BaseSettings context with extra-allow accepts two public InitSettingsSource inputs, override first (higher priority), defaults second. Explicitly omit environment, dotenv, secrets, CLI and other sources. No source-aware domain settings instances are exposed to consumers. The public BaseSettings source-composition merge is the algorithm proved in Research; do not reimplement recursive add/update.

Keep the current strict parser rather than routing file IO through the standard YAML source, whose missing-file and duplicate-key behavior would weaken admission. Parsed YAML becomes public native source input; a YAML deep_merge field is not introduced. The probe used this same public source-composition route.

### Deletion processing

1. Validate the complete defaults through the selected existing model; validate its keys/command absence first.
2. On fresh input copies, walk override mappings to validate every tombstone against the inherited document.
3. Remove requested members from the copied basis and omit their markers from the ordinary override document. Reject deletion beneath absent/scalar/list parents and deletion/update conflicts; never mutate caller-owned objects or YAML anchor aliases.
4. Pass the cleaned override and reduced basis to native composition.
5. Validate the final complete result with the selected existing model and cross-config validation before publishing it.

Deletion never disables domain validation. A removed optional field may receive its schema default; a removed required field/reference rejects admission. Reject shape-incompatible partial object updates rather than treating them as positional or ID-list mutations. The recursive walk interprets commands only; ordinary merging is native.

### Ordering and model admission

Object-list source fields become typed keyed mappings. Newly keyed config consumers iterate ordered values/items through the model-owned shared order helper; code needing identity uses the key. Existing mapping-to-keyed-tuple validators in bindings/locations remain reusable; they are not replaced by a general converter.

The map key remains canonical through model lookups. Do not introduce duplicate authored/runtime technical name aliases solely to avoid consumer edits. No blanket requirement to add id fields to every model follows from this decision. Existing shared domain IDs are separate output contracts.

### Shared CheckSpec boundary

CheckSpec is also a planning/runtime DTO and retains its id and existing field contract. Configuration exit_requires and cycle_exit_requires entries become mappings keyed by check ID, with ordered config requirement payloads. Reuse shared payload field definitions/validation rather than duplicating domain constraints. At the existing PhaseContractResolver boundary, construct the existing CheckSpec from the key and validated payload, excluding config order. This is a directed existing domain projection, not another loader or generic translation subsystem. Its two exit-resolution paths and their tests are directly in scope; issue planning checks and execution remain unchanged.

### Concrete source inventory and consumers

| Config | Change | Direct consumer obligation |
| --- | --- | --- |
| enforcement | Rules/actions become keyed mappings with order | EnforcementRunner ordered rule/action iteration; registry dispatch unchanged |
| contracts | phases, exit_requires, cycle_exit_requires members and branch_local_artifacts become keyed object maps | Contract helper/terminal/cycle-owner validation; ConfigValidator, ProjectManager, discovery helper, PhaseContractResolver and bootstrap merge-readiness projection |
| presentation | collections, nested children, enum_cases become keyed ordered maps | TextPresenter and collection renderer iterate configured values; DTO field/cases/templates remain payload |
| issues | issue_types becomes keyed map; remove technical name duplicate | IssueConfig index, GitHubManager valid-type reporting, CreateIssueTool enums |
| labels | labels and patterns become maps; preserve label.name | Label lookup and pattern matching iterate values; explicit order where existing precedence matters |
| contributors / milestones | Empty and populated catalogs become maps | Lookup helpers iterate values, preserve login/name/number/title |
| workflows / workphases / policies | Retain keyed catalogs; remove redundant technical name/operation_id and its injection | Catalog lookups and direct technical-name reads use keys; helpers remain behaviorally equivalent |
| checks / tests / fixes / artifacts | Retain existing keyed mapping admission | Existing execution/location outcomes and key references unchanged |
| adapters / git / scopes | Keep ordinary value lists | No per-value targeting |
| workphase exit_requires / phase expectations / optional_label_inputs | Model-declared object entries use mapping keys; singleton/value payloads stay ordinary records/maps | Existing getter/projection behavior remains; no inference from arbitrary id-looking content |

Preserve real GitHub names/numbers and presentation selector values. Do not rename every field ending in name. The older Research direct consumer inventory is expanded by the newly required mapping iterations above; construction counts remain search candidates, not edit quotas. Remove ignored workflows.phase_source metadata.

### Source routes

| Route | Admission |
| --- | --- |
| Required normal workspace config | Require complete defaults/<file>.yaml; optional partial root override |
| Optional enforcement | Neither source means existing empty policy; present basis or override-only complete file must be valid |
| Explicit config_path | Exactly one complete canonical document; no companion lookup or directives |
| Package adapter/template declarations | Existing explicit file semantics, no new layering or identity normalization |
| release_manifest / check_schemas | Existing routes/content, excluded from composition |

Absent override inherits; {} is a no-op. Present empty YAML, nonmapping roots, unreadable sources and duplicate keys fail. Existing typed integer keys, notably cycle_exit_requires, remain permitted by their models; duplicate detection cannot globally impose adapter string-only rules. Overrides cannot contradict existing source schema versions. External roots are self-contained; no repo/install fallback.

### Source ownership by file


| File | Product basis | Workspace override |
| --- | --- | --- |
| adapters.yaml | Empty trusted_adapter_ids | Explicit local trust grants; whole field value |
| artifacts.yaml | Existing package IDs and useful docs roots; Python roots src, test roots tests/unit and tests/integration; TypeScript root src | Existing mcp_server/backend/frontend roots and additional allowed roots; full values for unidentified root lists |
| checks.yaml | Existing adapter/capability/profile references, timeouts and native argument policy; all acknowledgement values null; python_production_sources uses src patterns; general cache/build exclusions where already policy | Restore current acknowledgements, mcp_server production patterns, validation-fixture/archive-specific exclusions and other actual local differences |
| tests.yaml / fixes.yaml | Existing binding/capability/timeout/active policy and arguments; choice null | Current explicit choices and any local arguments |
| contributors.yaml / milestones.yaml | Empty identified collections | Only local identities/catalog entries |
| scopes.yaml / labels.yaml / issues.yaml | Current useful taxonomy and relationships, mapping-key identities | Workspace-specific additions/changes/removals only |
| git.yaml | Current useful branch/commit conventions, including existing protected branches | Actual deviations only; no repo identity/token |
| enforcement.yaml | Current strict reusable categories/rules, including open-PR, context and phase-readiness protection | Only repository-specific differences; effective protections retained |
| contracts.yaml / workflows.yaml / workphases.yaml | Current workflow policy/instructions, useful documentation paths, mapping-key identities and order where execution/presentation is ordered | Only actual local differences |
| presentation.yaml | Current product strings/policy with mapping-key identities and explicit presentation order | Only actual local text/policy changes |
| policies.yaml | Preserve currently loaded policy with canonical IDs | Actual differences only; #506 remains separate |
| github.yaml | Existing neutral owner/repo/project_number/token values (null), no personal data | Explicit owner/repo and optional project_number/token alternative |
| release_manifest.yaml / check_schemas | Existing locations and meanings | Not part of this layering refactor |

A file with no workspace differences needs no root override. Empty catalogs can still be populated explicitly. General cache exclusions remain policy data; do not infer or rewrite native tool configuration.

The existing literal check-schema arguments under .pgmcp/config/check_schemas stay intact. This issue does not solve arbitrary relocation of native arguments or claim portable installation. Preserve existing runtime instructions rather than launching a workflow/template rewrite.

Remove ignored workflows.phase_source source metadata: catalogs already reach the phase contracts through injected configuration, and no runtime model consumes this key. It must not survive merely because an old extra-ignore model discarded it.


### GitHub composition


Keep the existing GitHubSettings value model (owner, repo, project_number, token) as the shared resolved contract to manager/adapter. ConfigLoader.load_github_config reads the workspace source into that same model. It is a singleton record, not an id-bearing collection.

Remove github from the launcher/runtime Settings input contract and remove GITHUB_OWNER/GITHUB_REPO/GITHUB_PROJECT_NUMBER loading. Settings.from_env continues loading server/logging configuration but does not supply a GitHub configuration fallback. Retain the GitHubSettings class as a pure value model; no file/env access is added to it.

Bootstrap obtains GITHUB_TOKEN as an explicit input to a pure resolution function in config/github_resolution.py:

```python
def resolve_github_settings(
    configured: GitHubSettings,
    environment_token: str | None,
) -> GitHubSettings: ...
```

A nonempty environment token wins; otherwise use the explicitly configured token; otherwise token is absent. Do not infer owner/repo from environment, Git remotes, the token holder or personal defaults. No OS-vault client is added: existing host delivery of the environment remains external.

Add one resolved github_settings value to ConfigLayer. The manager injection, active-tools selection and GitHub resource registration all use this same value, replacing the three old settings.github reads. Existing Settings/github setup tests change at this approved boundary. Renewal and ordinary config readers do not need to load GitHub merely to operate.

Preserve current startup-valid neutral integration, lazy API failure and token-presence registration policy. Do not add a credential probe, auto-unlisting framework or automatic enforcement bypass. Preserve project_number as optional data even though it currently has no active feature consumer. Do not inspect, copy or log the owner's actual token while splitting source files.


## Flow

ConfigLoader strictly reads selected sources, validates the complete basis, preprocesses deletion on copies, invokes native merge, then admits final models and cross-config references. Ordered model collections expose rank-based iteration. Consumers receive resolved configuration only. No write, backup, materialized effective file, checkpoint or partial publication occurs.

## State and Failures

| Condition | Outcome |
| --- | --- |
| Required source missing, invalid YAML/duplicate keys/version | ConfigError identifying source/cause |
| Invalid or unknown tombstone / mixed command payload | Reject with target path |
| Invalid order, absent required rank, equal sibling ranks | Reject before consumer use |
| Incomplete new object, unknown closed-model field, invalid reference | Existing final model/cross-config rejection |
| Null configuration_choice | Preserve startup and selected-use behavior |
| Missing GitHub token/identity | Preserve existing registration/use-time behavior; no inference or bypass |
| Any failure | Sources unchanged; chained diagnostics without secret/source dumps |

## Preservation

Current repository native args, policy, references, meaningful order and enforcement outcomes survive the split. ConfigLoader calls, explicit package readers, public CheckSpec/planning/state/commit formats and existing tool DTOs stay stable. Directed config container/technical-identity consumers intentionally change without aliases. No distribution-portability or wheel claim follows.

## Transition and Cleanup

Implementation performs one clean source/model/consumer cutover under interactive owner control. Remove obsolete object-list source forms, redundant technical identities/injection, temporary _reset_binding_choices function/call and reset-only tests, and ignored phase_source metadata. Reuse existing test preparation; no old-shape converter. Keep release_manifest/build/upgrade logic untouched. Documentation updates active descriptions and makes each PR closes entry produce its own Closes #N statement using the existing input schema.

## Test Design

| Behavior | Evidence strategy |
| --- | --- |
| Native inheritance/addition/update and leaf list/null replacement | Compact public-loader matrix, adapted existing tests; no per-file content snapshots |
| Deletion | Existing/unknown target, mixed marker, required/reference rejection and no source mutation |
| Order | Inherited/update/new ranks, tie and invalid rank, actual execution/presentation/workflow ordering |
| Config projections | Existing helpers/consumer behavior; shared CheckSpec remains valid planning input/output |
| Roots/package routes | Temp-root fixtures, explicit complete files, unchanged package reads; prevent live-root fixture fallback |
| GitHub/init | Adapt existing Settings/bootstrap/init tests, env-first token and no acknowledgement rewriting |
| PR closing | Adapt current multi-issue render test during Documentation |

Tests exercise behavior rather than YAML spelling, field inventories or private implementation. No retained legacy rejection campaign, no duplicated cases per config, and no suite-wide fixture rewrite. Narrow implementation tests/checks; full suite and configured gates belong to Validation under its phase contract.

## Validation

Planning specifies actual changed-file targets per tool/check; Python tools never receive Markdown/YAML targets. Test selection is per meaningful seam; use existing focused behavior tests and native arguments. Reuse fresh evidence. Validation owns the required full suite, production type checking and configured workspace checks. No broad suite is requested for Research/Design/Planning QA. Documentation owns changed-doc link checks and focused PR-template evidence.

## Risks

Native settings-source precedence must be isolated from ambient sources. Native YAML loading cannot replace our stricter parser. Object-map consumer changes extend beyond mere name renames; preserve behavior with existing tests. Source-only concepts must not spread into shared planning DTOs. Overrides are not packaged-portability proof. Never copy actual tokens into docs/commits.

## Planning Consequences

Plan bounded, reviewable steps for native composition/delete/order, model/source cutover and direct consumers, GitHub/init, focused evidence and Documentation. The user wants interactive Implementation: after independent Planning GO stop at the Planning-to-Implementation boundary and await the owner's next instruction. No implementation transition, source migration, dependency edit, production/test edit or automatic cycle execution is authorized by this preparation run.

## Sources

- [Loader](../../../mcp_server/config/loader.py)
- [Config models](../../../mcp_server/config/schemas/)
- [Contract resolver](../../../mcp_server/managers/phase_contract_resolver.py)
- [Enforcement runner](../../../mcp_server/managers/enforcement_runner.py)
- [Settings](../../../mcp_server/config/settings.py)
- [Bootstrap](../../../mcp_server/bootstrap.py)
- [PR template](../../../.pgmcp/template_suite/pr/template.jinja2)
- [Pydantic Settings public source composition](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#customise-settings-sources)
- [YAML source and native merge](https://github.com/pydantic/pydantic-settings/blob/v2.13.1/pydantic_settings/sources/base.py)

## Related Documents

- [Research](research.md)
- [Architecture contract](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Documentation standard](../../coding_standards/DOCUMENTATION_STANDARD.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1–0.5 | 2026-10-15 | @imp designer | Earlier list-ID/materializer design and native-first reassessment; superseded by the owner decision below. |
| 0.6 | 2026-10-15 | @imp designer | Select mapping-key identity and native merge; narrow custom logic to delete/order, specify consumer and shared-CheckSpec seams, exclude manifest and require interactive Implementation. |
