<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 504 — Configuration basis and workspace override research

**Status:** RESEARCH COMPLETE — INDEPENDENT REVIEW PENDING  
**Version:** 0.19  
**Last Updated:** 2026-10-15

## Purpose

Reuse #319 findings to investigate a bounded configuration-source refactor. Preserve behavior and unrelated consumer contracts; use canonical mapping-key identities through directly affected configuration models/consumers rather than translating them to legacy technical-name fields.

## Scope In

Separate canonical product configuration from workspace differences; compose and validate them within the loader boundary; preserve existing public loader calls and complete typed results; adapt focused loader/configuration tests and directly affected test preparation. In Documentation, also correct the active/bundled-source PR template's operative issue-closing output with focused rendering evidence. Retain the previously approved removal of the temporary initialization-time configuration_choice reset as a narrow configuration-write cleanup, not a redesign of initialization. The owner now explicitly extends scope to move GitHub repository identity into workspace configuration, retain environment-first token delivery with an explicit workspace-token alternative, remove old launcher/settings identity sources and correct directly affected documentation. Composition-root changes required for this new source contract are authorized exceptions. The final owner decision selects mapping-key identity and native deep merge; directly affected configuration containers/consumers may change, unrelated consumers remain unchanged. This removes the earlier blanket prohibition on identity-contract consumer changes, not the prohibition on general architecture expansion.

## Scope Out

Package-builder code and content transformations, all release_manifest.yaml changes, #505 assembly reliability, wheel/sdist distribution acceptance, managed-basis activation and upgrade/recovery machinery, installation-state extensions, releases, deployment, #506 and #508 implementation, broad test cleanup, and consumer changes unrelated to the approved identity normalization or GitHub source composition. The owner now authorizes producer-monitored external QA through Planning, then interactive Implementation. Earlier combined execution of #504/#505 is superseded by the owner's narrower scope; neither issue is closed by this research decision.

## Problem Statement

Current configuration combines product policy with workspace paths, choices and ownership data. Separating those sources can remove that coupling behind the existing loader interface. The package builder remains a source/target copier with no knowledge of configuration contents. Packaging ownership and adoption of a new basis are later concerns, not acceptance claims for this refactor.

## Goals

- Keep one canonical product basis and separately authored workspace differences.
- Resolve and validate both within the configuration boundary. Preserve loader entry points and behavior; permit directed identity-field changes in returned models and their direct consumers, with no id-to-name compatibility projection.
- Preserve the current workspace's effective values while moving their ownership; do not silently alter consumer policy.
- Prove composition, diagnostics and source immutability through focused behavior tests; use the existing suite as required by the active workflow without a suite-wide rewrite.

## Background

The owner initially coordinated QA directly; the latest instruction authorizes producer-monitored independent Research/Design/Planning reviews and requires interactive Implementation thereafter. #319's final strategy superseded native-config sample/export proposals: configuration_choice is an owner acknowledgement, not effective-source proof; unresolved choices refuse applicable use while setup/health remain available. Its fresh-init reset is implemented, while DF-319.2 deliberately left manifest content policy unapproved. Existing workspace settings and template-only renewal were preserved. Those findings are reused, not researched from zero. The owner subsequently narrowed #504 to configuration and loader refactoring, deferring the previously combined distribution/build work. The subsequent owner instruction explicitly restores the narrowly bounded PR-template closing fix for Documentation. Online issue bodies still describe the older combined scope; administrative reconciliation belongs to Coordination.

## Findings

### Existing content inventory and proposals

The config tree contains 18 YAML files and two JSON check schemas. The inventory below predates the narrower scope: use it to distinguish basis values from workspace differences. It does not authorize distribution changes or new product policy. Preserve this workspace's effective values through the separation; starter layout and ownership decisions below reflect the owner's subsequent approvals.

| File | Proposed distribution role |
| --- | --- |
| adapters.yaml | Product basis has an empty workspace-adapter trust list; local grants belong only to overrides. |
| artifacts.yaml | Preserve template identities and useful document locations; replace mcp_server/backend/frontend assumptions with an explicit product starter layout. Use the owner-approved src and tests/unit/tests/integration starter layout; preserve repository-specific paths in overrides. |
| checks.yaml | Preserve useful bindings/profiles; product acknowledgement values null; move workspace production roots and fixture exclusions into overrides. Retain general cache/build exclusions subject to content approval. |
| tests.yaml | Preserve binding/capability; product acknowledgement null; local setup chooses policy. |
| fixes.yaml | Preserve useful capabilities; product acknowledgements null. |
| contributors.yaml | Empty product list; local identities only in overrides. |
| milestones.yaml | Empty product list; repository-specific milestones only in overrides. |
| scopes.yaml | Preserve a useful approved starter taxonomy rather than deleting valid categories automatically. |
| labels.yaml | Preserve corresponding types/priorities/scopes and dynamic label rules as an approved starter taxonomy. |
| issues.yaml | Preserve issue/workflow/label relationships. |
| git.yaml | Preserve approved branch/commit policy; main/master/develop are not inherently invalid defaults. |
| enforcement.yaml | Preserve required admission and policy as product defaults; workspace deviations remain explicit. |
| contracts.yaml | Preserve approved workflow contracts and instructions; starter artifact/root conventions need explicit ownership. |
| workflows.yaml | Preserve catalog metadata; do not absorb #506 infrastructure assessment. |
| workphases.yaml | Preserve phase/commit metadata. |
| presentation.yaml | Preserve product presentation; future strings still require product-source review. |
| policies.yaml | Avoid new transformation investment pending #506; do not remove a currently loaded file by assumption. |
| release_manifest.yaml | Build input remains unchanged; routing, exclusions and self-copy policy are deferred distribution work. |
| check_schemas/yaml_configuration.schema.json | Product schema asset; preserve binding/source dependency. |
| check_schemas/json_schema_source.schema.json | Product schema asset; preserve binding/source dependency. |

The two native schema arguments currently contain literal .pgmcp/config/check_schemas paths. Preserve existing effective arguments in this refactor; do not introduce a relocation solution. Native configuration files stay owner-managed.

### Primary-source precedent and limits

Grafana separates defaults.ini and custom configuration. Django combines global_settings and project overrides behind one settings interface. VS Code registers defaults/type/scope and stores user/workspace values separately. Helm packages values.yaml, combines user values and validates the final object; package exclusions are separate. JupyterHub/Traitlets derives configurable defaults and generated examples from definitions. None of these inspected contracts establishes automatic semantic detection of future workspace data in a product source.

Multiple sources can own different facts without duplicating authority. Product defaults and workspace differences should not be repeated as a third set of manifest values. Per-field default/workspace wrappers remain possible but are not an owner-approved schema.

### Composition evidence and approved boundary

The owner's final decision supersedes the earlier list-id matching and generic materializer proposal. Use native Pydantic Settings deep merge for additions/field changes; own composition extensions are limited to $delete and explicit order. release_manifest.yaml and its consumers remain excluded.

### Identity-based addressability: final owner clarification

An object collection is a mapping with one canonical key identifier per object, including nested object collections. No repeated authored id, name alias or selector matching. An object with only scalar fields is still an object. Singleton records, references and real domain fields retain their meaning.

Scalar/value lists are whole field values, preserve order/duplicates, and allow either dashes or brackets. Empty object collections are {}, empty value lists are []. Omission inherits; null remains literal; deletion uses the reserved singleton {$delete: true}. No positional/set/argv operations.

Formerly ordered object collections have strict integer order, inherited for partial updates and required on complete/new members, unique among siblings. No auto-append/renumber/tie-break. Lookup-only catalogs need no artificial execution order.

### Concrete object-collection inventory

Read-only inspection of every root config YAML and the empty-catalog schemas establishes:

| Files | Normalization |
| --- | --- |
| enforcement | Rules/actions to keyed ordered maps; tool/category/exemption/pattern values remain lists |
| contracts | Phases, exit requirements, cycle exit check entries and branch-local artifacts to keyed ordered maps |
| presentation | Collections, children and enum declarations to keyed ordered maps; templates/cases/references stay payload |
| issues / labels | Issue types, labels and label patterns to maps; retain actual label.name and scalar categories/exceptions |
| contributors / milestones | Empty maps and populated object maps; retain login/name/number/title |
| checks / tests / fixes / artifacts | Already keyed; argument/root/pattern/reference lists remain whole values |
| workflows / workphases / policies | Retain keyed catalogs, remove redundant technical identities; typed nested object declarations follow same rule |
| adapters / git / scopes | Existing value lists remain |
| release_manifest / check_schemas | Explicitly outside composition; manifest/build and JSON Schema semantics unchanged |

[Existing schemas](../../../mcp_server/config/schemas/) own field/object types. Strings containing Markdown/Jinja/YAML are data, not recursively parsed structures.

### Completed runtime identity and consumer impact analysis

The prior list-id census is a historical baseline, not the chosen representation. The final mapping-key contract changes affected config containers/iterations. It does not inject duplicate id fields into every model or translate source identity back to name.

Direct seams: config models/loader/validator; EnforcementRunner; workflow/phase helpers and ProjectManager/discovery; IssueConfig/GitHubManager/CreateIssueTool; label/contributor/milestone lookups; TextPresenter/collection renderer; PhaseContractResolver and bootstrap merge-readiness projection. Consumers use keys for identity and explicit validated order; they do not merge layers.

WorkflowTemplate.name, WorkflowPhaseEntry.name, IssueTypeEntry.name and OperationPolicy.operation_id are redundant technical identities and are removed without aliases. Preserve real label.name, login/name, milestone number/title, presentation field/type and existing reference values.

Shared CheckSpec.id is a planning/runtime contract and stays unchanged. Config requirement maps supply key identity and ordered payloads; existing PhaseContractResolver constructs CheckSpec without config order. Reuse shared payload constraints rather than duplicate validation. This directed projection and both resolution paths are in scope; planning/state/commit/tool DTO redesign is excluded.

[Loader](../../../mcp_server/config/loader.py), [contract models](../../../mcp_server/config/schemas/contracts_config.py), [resolver](../../../mcp_server/managers/phase_contract_resolver.py), [runner](../../../mcp_server/managers/enforcement_runner.py), [presenter](../../../mcp_server/presenters/text_presenter.py) and [validator](../../../mcp_server/config/validator.py) are primary seams. Counts below remain preparation candidates, not edit quotas.

### Test impact: source-boundary preparation versus runtime behavior

Read-only AST census over tests/*.py found 67 files with 130 direct ConfigLoader constructor calls. Method-reference classification found 53 with workspace loaders and 14 using only package declaration methods. The latter include all 10 native-adapter conformance test files plus adapter_process fixture and template declaration readers: the constructor call alone does not require a new configuration tree. Counts are static inventory, not test failures or edit counts; embedded Python strings/indirect helpers require direct inspection.

A second static screen found 45 files containing a short config filename literal and file-IO method usage. This intentionally broad candidate set includes build-only and unrelated IO; it is not a list of confirmed edits.

| Confirmed preparation surface / examples | Required handling |
| --- | --- |
| unit/config/test_loader.py, test_loader_behaviors.py, test_config_version.py, test_checks_config.py, test_contracts_loader.py, test_c_loader_schema_structural.py | Update source YAML fixtures and layer locations; retain useful admission/output behavior. Do not rewrite runtime model contracts to make old YAML pass. |
| unit/config/test_contributor_config.py, test_milestone_config.py, test_issue_config.py, test_label_config.py, test_labelconfig_singleton_bug.py, test_workflow_config.py | Populated complete-file fixtures need canonical source identity. Direct runtime model preparation changes only where the approved runtime identity contract changes. |
| unit/config/test_tool_presentation_rollout.py and test_labels_yaml_conventions.py | Direct raw active-YAML reads couple behavior tests to physical source syntax. Route retained behavior through ConfigLoader; assess content-only/legacy-negative cases rather than preserving every historical assertion. |
| Integration enforcement fixtures: test_context_loaded_enforcement.py, test_ready_phase_enforcement.py, test_pr_status_lockdown.py; raw readers test_c5_cleanup_and_prstatus.py/test_submit_pr_atomic_flow.py | Author explicit source rules/IDs or load effective models; preserve actual admission/PR-lock outcomes. |
| unit/execution/test_test_service.py, test_fix_service.py and unit/services/test_artifact_target_resolver.py | Adapt loader-facing synthetic YAML only. Other execution tests use runtime model data and need no ID-source conversion. |
| fixtures/suite_roots.py, workflow_fixtures.py, delivered_templates.py and test_support.py | Reuse existing filesystem/delivered loaders. test_support currently probes top-level files before a repository fallback: candidate C makes that probe unreliable, so affected test preparation must select the intended explicit context and not silently test the live repository instead. No test compatibility converter for old YAML. |
| integration/test_renewal_cli.py, test_template_activation.py/test_template_proposal.py | Existing preparation copies only top-level checks/adapters. It must copy the needed defaults plus overrides; renewal production logic need not change. |
| unit/test_cli.py; unit/server/test_bootstrap.py; unit/config/test_settings.py | Adapt approved init-reset removal and GitHub source/token/visibility preparation. Manager/adapter value-contract behavior stays stable. |
| unit/config/test_presentation_config.py; unit/execution/test_check_service.py | Direct model_validate preparation is unaffected by layering alone; inspect it for genuinely changed runtime identity contracts. No source-directive leakage into consumer tests. |
| integration/templates/test_pr.py | Adapt existing multiple-issue rendering evidence during Documentation; no whole-template snapshot campaign. |

Evidence strategy: a compact behavior matrix for duplicate/missing source IDs, nested targeting, addition/change/explicit deletion, unaffected inheritance, order and invalid targets; representative public loader projections; preserved null/argument/reference behavior. Reuse runtime consumer tests instead of duplicating coverage for every YAML value. No new tests, quality gates, package builds or full-suite runs were executed during this impact research.

- [Runtime config models](<../../../mcp_server/config/schemas/>)
- [Loader boundary](<../../../mcp_server/config/loader.py>)
- [Runtime-only check-service preparation](<../../../tests/mcp_server/unit/execution/test_check_service.py>)
- [Direct presentation-source reader](<../../../tests/mcp_server/unit/config/test_tool_presentation_rollout.py>)
- [Synthetic source tree helper](<../../../tests/mcp_server/fixtures/suite_roots.py>)
- [Shared test-root selection](<../../../tests/mcp_server/test_support.py>)
- [Renewal fixture preparation](<../../../tests/mcp_server/integration/test_renewal_cli.py>)

### Focused identity-test impact and evidence limits

Read-only Python AST inspection of tests/**/*.py resolved directly imported class aliases and counted constructor calls plus model_validate/model_validate_json/model_construct calls; it did not import server modules or execute tests.

- For WorkflowTemplate, WorkflowPhaseEntry, IssueTypeEntry and OperationPolicy, 20 direct calls occur in 8 files: test_workflow_config.py, test_workflow_config_c6.py, test_contracts_config.py, test_contracts_loader.py, test_consumers_c4.py, test_phase_contract_resolver_c3.py, test_discovery_tools.py and config/test_operation_policies.py. No direct IssueTypeEntry construction was found; its nested dictionary preparation is affected separately.
- Across the 14 affected root-model class names, the same AST screen found 109 direct construction/validation sites in 45 unique test files. This is a static preparation candidate set, not 109 tests, 45 failures or 45 mandatory edits. It overlaps the earlier ConfigLoader inventory; do not add the counts. Dynamic imports, embedded subprocess scripts and indirect dictionaries are not comprehensively classified by that screen.
- Nested issue-type name dictionaries are confirmed in test_github_manager.py and YAML in test_issue_config.py. Assertions reading workflow.name, phase.name and operation_id occur in the config tests; get_phase_names callers also occur in test_discovery_tools.py and test_phase_contract_resolver.py.
- tests/mcp_server/test_support.py::_NopGateRunner.is_cycle_based_phase directly reads p.name. Update this shared preparation seam for key-based phase identity rather than patching every consumer test or installing a compatibility converter.
- New identity-bearing anonymous model construction is concentrated in existing helper/fixture seams: enforcement runner/schema tests, _collection in test_collection_text_renderer.py, branch-artifact fixtures in test_submit_pr_atomic_flow.py and phase-contract tests, and populated label/contributor/milestone tests. Empty catalogs do not need invented entries.
- workflow_fixtures.py has an obsolete workflow_phases fixture accessing WorkflowTemplate.phases; repository search found no fixture request or other use. It is not a reason to restore that removed model field. Assess removal only when touching this fixture; no broad fixture cleanup is authorized.

The maintenance strategy is to adapt existing public-behavior tests and affected shared preparation, keep direct contract tests explicit, and avoid per-file content snapshots, old-format rejection campaigns or a suite-wide helper rewrite. New behavior evidence should cover representative identity, order, inheritance, removal, reference rejection and read-only failure outcomes; ordinary domain tests continue proving their existing behavior. No new regressions-for-legacy suite, broad test rewrite or test-count target is approved.

Reproduction route for this static evidence: search active mcp_server Python for name/operation_id attribute reads and the four model names; inspect the listed methods and their direct callers. For test counts, parse tests/**/*.py with ast, resolve ImportFrom aliases for the four leaf or 14 root model names, and count Call nodes for direct constructors and the three explicit model-admission methods. These are source census results; runtime/type-check evidence belongs to Implementation/Validation.

- [Shared test identity consumer](<../../../tests/mcp_server/test_support.py>)
- [Workflow model behavior](<../../../tests/mcp_server/unit/config/test_workflow_config.py>)
- [Contract model behavior](<../../../tests/mcp_server/unit/config/test_contracts_config.py>)
- [Cross-config behavior](<../../../tests/mcp_server/unit/config/test_validator_c3.py>)
- [Nested issue preparation](<../../../tests/mcp_server/unit/managers/test_github_manager.py>)
- [Operation policy behavior](<../../../tests/mcp_server/config/test_operation_policies.py>)
- [Presentation preparation seam](<../../../tests/mcp_server/unit/presenters/test_collection_text_renderer.py>)
- [PR artifact preparation seam](<../../../tests/mcp_server/integration/test_submit_pr_atomic_flow.py>)

### Explicit order: requirement and chosen limits

Explicit order belongs to formerly ordered object collections and other execution/presentation sequences. Native mapping merge inherits/updates the order field but does not sort or reject collisions. Existing model-declared ordered collections use one reusable config-owned strict-integer/rank helper; partial overrides inherit order, new members provide it and final sibling ranks must be unique. Physical YAML order, alphabetical sorting and implicit append are not substitutes. Value lists retain their own sequence. No extra per-file representation metadata is selected.

### Pydantic facilities and limits

Supplemental investigation during Design, requested by the owner after questioning extra merge/translation machinery. This is library/source evidence, not a runtime prototype or a new implementation decision.

Dependency contract: pyproject.toml declares pydantic>=2.5.0, with no exact pin and no direct pydantic-settings dependency. Metadata inspection found Pydantic 2.12.5 / pydantic-settings 2.13.1 in .venv and Pydantic 2.11.7 / pydantic-settings 2.12.0 under the default python command. These are inspected environments, not proof of which interpreter the live server process uses. No package was installed or changed.

| Existing facility | Observed semantics | Fit for the approved configuration contract |
| --- | --- | --- |
| BaseModel.model_validate and field/model validators | Construct/validate complete data; existing schemas already perform domain/reference checks and input normalization | Reuse as complete configuration authority. No parallel domain-validation schema or generic runtime-shape metadata is justified merely by their existence. |
| model_fields / model_fields_set | Authoritative declared fields/types and the fields explicitly set on an admitted model | Reuse structural information and omission-versus-explicit-null distinctions where models are already admitted. A complete model does not automatically become a partial override model. |
| model_dump(exclude_unset=True) | Serialize only explicitly supplied fields | Useful for an already valid partial-input representation, not native merge or removal. Do not substitute exclude_none, because explicit null is meaningful. |
| model_dump(exclude=...) | Supports nested field/position exclusions in the exported data | A serialization facility; it does not interpret $delete, select list objects by id, validate missing targets or remove fields from the source/model itself. |
| model_copy(update=..., deep=True) | Deep-copy existing model, then update the outer copied dictionary without validating new values | Not recursive validated configuration merging; deep means copying, not recursive patch semantics. Revalidating a plain complete result remains necessary. |
| del model.field / assignment | Ordinary mutation facilities, with frozen-model checks | Not a validated removal protocol. Preserve frozen config objects and create a newly validated result rather than deleting fields from them. |
| pydantic-settings sources | Separate public package supports multiple YAML files and deep_merge=True in inspected 2.13.1 | It does provide ordinary nested dictionary combination; this should have been explicitly compared earlier. It does not supply the approved identity/deletion/order policy. |
| Settings nested_model_default_partial_update | Allows field updates on nested default model objects when explicitly enabled | Useful nested-default behavior, not a universal partial-override schema or identified-list/$delete operation. |
| Settings deep_update behavior | Recurse only when both old/new values are dictionaries; otherwise replace the value, including lists | Does not merge identified list objects, handle $delete, check ranks/unknown targets or maintain the custom operation invariants. This is supported by the versioned source, not just absence from an example. |
| Settings YAML file discovery | Inspected _read_files skips a nonexistent file before merge | Cannot be adopted unchanged for required defaults/invalid-presence admission. Our explicit selected-root and required-source contracts still need ownership. |
| Experimental partial validation | A facility for incomplete input and trailing errors; not universal optional-field patch validation | Not the override contract and unsuitable as a way to ignore invalid patch input. |
| Experimental MISSING sentinel | Available in inspected 2.12.5 to represent absent/unset data | Not $delete and not an ID-aware mutation operation. It is not guaranteed by the declared >=2.5.0 minimum; do not add an experimental dependency assumption. |

Inspected installed code: pydantic/main.py::BaseModel.model_copy and __delattr__; pydantic/_internal/_utils.py::deep_update; pydantic_settings/sources/providers/yaml.py::YamlConfigSettingsSource; pydantic_settings/sources/base.py::ConfigFileSourceMixin._read_files; and the settings source-combination call in main.py. The private deep_update function is evidence about behavior, not a proposed import. The public YAML source has a deep_merge argument; a claim that the ecosystem only offers shallow replacement would be incorrect.

The remaining custom semantics are narrowly defined by the owner: resolve a nested object by id; add/update it while retaining unmentioned objects; interpret the reserved $delete command with strict target/conflict errors; preserve literal field values; and enforce explicit ordering. Existing Pydantic model validation should retain type/required/domain validation. Ordinary dictionary traversal can be part of the same small operation function rather than introducing a second library/source framework.

Recommendation for the next Design revision: use existing BaseModel admission and field information first; evaluate only the missing identity/command semantics. Do not claim Pydantic is a ready-made complete override engine, and do not use that absence to justify a generic translator, per-file metadata, dynamic partial-model family or wholesale BaseSettings migration. This historical facility audit did not select a dependency; the final native route and concrete dependency are specified in Design.

Reproduction: inspect pyproject.toml; query importlib.metadata for package versions using both python and .venv/Scripts/python.exe; read the named package source methods. This facility audit mutated no models or packages and ran no suite. The later native-source demonstration below is separate evidence.

- [Dependency declaration](<../../../pyproject.toml>)
- [Current complete-model admission](<../../../mcp_server/config/loader.py>)
- [Existing presence/null distinction](<../../../mcp_server/config/schemas/checks_config.py>)
- [Pydantic 2.12 model-copy API](<https://docs.pydantic.dev/2.12/api/base_model/#pydantic.BaseModel.model_copy>)
- [Pydantic serialization/presence](<https://docs.pydantic.dev/2.11/concepts/serialization/>)
- [Public settings file/deep-merge support](<https://docs.pydantic.dev/latest/concepts/pydantic_settings/>)
- [Versioned settings file-source implementation](<https://github.com/pydantic/pydantic-settings/blob/v2.13.1/pydantic_settings/sources/base.py>)
- [Versioned recursive-dictionary helper](<https://github.com/pydantic/pydantic/blob/v2.12.5/pydantic/_internal/_utils.py>)
- [Experimental feature limits](<https://docs.pydantic.dev/latest/concepts/experimental/>)

### Native-first YAML alternatives after owner reopening

The owner explicitly asks to reconsider the earlier mutation/YAML strategy rather than evaluating native facilities only against the previously chosen id/order/$delete design. Those representation/operation choices are reopened for comparison; source ownership and bounded issue scope remain. The later final owner decision selects native deep-merged mappings with explicit delete/order; other alternatives below remain comparison evidence.

BaseModel itself has no declarative configuration-source merge/add/delete API. The official separate pydantic-settings package provides deterministic multi-file shallow/deep combination followed by model validation. The source constructor, not an ordinary YAML field, chooses deep_merge. The following are actual native alternatives rather than custom ID semantics.

Shared base fragment, omitting unrelated checks.yaml sections for readability:

```yaml
# defaults/checks.yaml
checks:
  python_lint:
    adapter_id: ruff
    capability: lint
    timeout_seconds: 60
    configuration_choice: null
    default_args: []
  python_format:
    adapter_id: ruff
    capability: format
    timeout_seconds: 60
    configuration_choice: null
    default_args: []
```

With YamlConfigSettingsSource(..., yaml_file=[base, workspace], deep_merge=True), a workspace fragment can update a leaf and add an object:

```yaml
# checks.yaml
checks:
  python_lint:
    timeout_seconds: 120
  python_types:
    adapter_id: mypy
    capability: types
    timeout_seconds: 120
    configuration_choice: null
    default_args: []
```

Result: python_lint inherits adapter/capability/arguments/choice but changes timeout; python_format remains; python_types is added. Mapping keys are the natural identifiers in this native format. No extra id property, command or model-shape description is required by the merge library. This mapping form is now selected by the owner; duplicate authored IDs are not introduced.

Native deep merge cannot delete the inherited python_format key by omission. checks: {} leaves the inherited mapping intact. python_format: null replaces that value with None; it does not remove the key. A nullable value schema could admit it as data, but filtering/disable interpretation would be an additional explicit domain decision. $delete is not a native operator.

With the same base but deep_merge=False on that one multi-file YAML source, this complete replacement of the top-level checks member is native:

```yaml
# checks.yaml
checks:
  python_lint:
    adapter_id: ruff
    capability: lint
    timeout_seconds: 120
    configuration_choice: null
    default_args: []
```

Result: checks contains only python_lint; python_format is absent. The operation is replacement of the entire top-level checks value, not key-targeted deletion or nested field inheritance. Unmentioned top-level sections still come from the base. To retain other checks, repeat their complete definitions (except values supplied by the final schema's own defaults). Future base additions inside this replaced group are not inherited.

A list-valued section also replaces as a whole under native deep merge. For example enforcement: [] produces an empty enforcement list; retaining all but one rule means supplying the complete remaining rule list. id/order fields in list entries are ordinary data; native merge does not match or sort them. If explicit ranks remain a requirement, their validation/use must be designed separately rather than attributed to the library.

| Native route | Add/update | Actual removal | Cost to workspace/base behavior |
| --- | --- | --- | --- |
| Deep-merged mappings | Add key or patch named nested fields | No directed removal of an inherited key | Compact differences, future base keys inherited |
| Shallow multi-file source | Supply a complete top-level member | Omit an item from that member's replacement | Repeat retained content; no future inheritance inside that member |
| Whole-list replacement (also within deep merge) | Supply full desired list | Omit an item or use [] | Repeat retained objects; no item-level inheritance |
| Nullable map values | Replace a key's value with null | Key remains present | Requires schema/domain agreement; not native deletion |

These are source-level capabilities verified in installed pydantic-settings 2.13.1 and public source/docs. They are not an end-to-end pgmcp integration run. A native adoption still requires an explicit dependency/version decision and bounded integration with ConfigLoader's required-source/invalid-input rules. Standard settings file loading skips nonexistent files and must not silently weaken those existing rules or introduce ambient settings sources.

The owner selects native mapping inheritance, explicit deletion and order; shallow group replacement and custom list-ID matching are rejected. Leaf value-list replacement is retained.

- [Public file-source and merge options](<https://docs.pydantic.dev/latest/concepts/pydantic_settings/>)
- [Versioned YAML source read/merge implementation](<https://github.com/pydantic/pydantic-settings/blob/v2.13.1/pydantic_settings/sources/base.py>)
- [Native dictionary/list replacement behavior](<https://github.com/pydantic/pydantic/blob/v2.12.5/pydantic/_internal/_utils.py>)

### Generic native composition without file dispatch

The earlier metadata/materializer alternative is withdrawn. ConfigLoader keeps strict safe parsing/source selection, public Pydantic Settings source composition supplies recursive mapping merge, a pure config wrapper handles explicit tombstones on copies, and existing models/shared helpers own order and domain admission.

No filename/tool/phase if-chain, bespoke converters, list-ID matching, second schema family or private deep_update API. Existing mapping admission remains reusable; direct map consumers change as inventoried. See [Design](design.md) for dependency, source precedence, errors and CheckSpec boundaries.

### Concrete source and consumer seams

- ConfigLoader has two parsing/admission paths: _load_yaml/_validate_schema and strict _load_declaration. It also reads explicit adapter manifests, template manifests and policies. Workspace layering must apply to workspace configuration only, not automatically to those package contracts.
- Bootstrap, renewal CLI, fresh CLI initialization and PolicyEngine are the four production files constructing ConfigLoader. The narrowed contract requires their existing consumer-facing calls to remain valid. No new required constructor argument, layer-aware consumer, alternate model or consumer-side fallback is permitted. The separately approved removal of the temporary init reset is the sole bounded initialization cleanup.
- Repository text search found ConfigLoader construction in 68 test files. This is a coupling inventory, not 68 required edits or failing tests. Inspect affected existing fixture/factory seams before changing constructor requirements; avoid live-repository config as implicit test preparation.
- Fresh --init copies package assets and _reset_binding_choices then serializes complete checks/tests/fixes models to the fresh config directory. Applying that write to layered effective models would materialize inherited product values into local overrides. The owner now explicitly requires retiring this temporary init reset; acknowledgements must be product-source defaults plus explicit workspace choices, not a post-copy rewrite.
- load_enforcement_config currently treats a missing file as empty enforcement. In a layered model, an absent optional override must not be confused with a missing required product basis or disable inherited admission. Preserve/revise the existing absence contract explicitly.
- Settings.resolved_config_root selects a default or explicit external root. A new basis/override contract must define that root's meaning explicitly; no search through parent directories, guessed source or silent legacy interpretation is assumed.
- Template renewal currently stages package assets/template_suite and checks it against effective config; it does not publish a new config basis. InstallationState records package version and a template checkpoint, not a configuration-basis checkpoint. Reusing template checkpoints as config proof would be false.

### Root and authoring options

The existing explicitly selected config_root remains sufficient. The owner selected C. The table retains A/B as evaluated alternatives, not open decisions. Source inspection finds no need for consumer-call changes with the selected layout:

| Candidate | Basis path | Workspace override path | Trade-off |
| --- | --- | --- | --- |
| A | checks.yaml | overrides/checks.yaml | Least movement of complete-file fixtures, but the workspace edit path moves into a subdirectory. |
| B | defaults/checks.yaml | overrides/checks.yaml | Both owners are explicit in directories; all complete-file preparation moves and overrides are also nested. |
| C (owner approved) | defaults/checks.yaml | checks.yaml | Workspace edits stay at the selected config root; managed basis is grouped for later distribution/adoption. Existing complete-file synthetic fixtures need deliberate source-role updates. |

For C, no-path workspace reads load defaults/<name>.yaml plus optional <name>.yaml. Missing override inherits the basis. Enforcement remains optional as explicitly approved; nonoptional configuration still requires a valid complete basis; optional override absence does not relax final validity. External config_root selects that same self-contained context, with no borrowing from another root or installation. No automatic old-flat-root interpretation is proposed: existing effective YAML must be deliberately split into complete defaults and partial root overrides. The selected C layout entails deliberate source splitting and targeted fixture updates within the already approved scope. It does not authorize a loader-driven migration or an old-layout compatibility mode.

An explicit config_path retains its standalone complete-document meaning, with no implicitly selected companion or fallback. Design must define admission of the new canonical representation without adding another source-discovery rule. Under C, a root override is generally partial and cannot serve as that standalone complete input. Production inspection found workspace configuration consumers already use no-path calls; existing explicit-path tests and standalone package readers must remain meaningful. This distinction must be documented, not inferred from file placement.

JSON check-schema assets can stay at config_root/check_schemas so current native arguments stay valid. They are tool input assets, not composable workspace YAML sources. release_manifest remains unchanged build input and is not layered. Preserve the loader constructor and entry points. Returned models and directly affected consumers may change only for approved identity normalization or the separately approved GitHub composition boundary; source layering does not justify unrelated consumer changes.

The loader stays read-only. Product defaults and overrides are source documents, not an effective-output cache. Deployment, packaging exclusion and managed-basis adoption are separate future work; C alone does not solve current whole-directory copying.

### Check-schema assets and their actual role

The direct file consumer is the external check-jsonschema CLI. Its generic adapter passes request.args unchanged to the native module and appends input files. Neither schema is read by ConfigLoader to admit PGMCP runtime configuration.

| File / binding passing --schemafile | Consumers selecting the binding |
| --- | --- |
| yaml_configuration.schema.json / yaml_configuration | The yaml_configuration template policy selects yaml_configuration_review at scaffold. Safe-edit selects its template profile or .yaml/.yml extension profile. run_checks can select the binding/profile for YAML targets. |
| json_schema_source.schema.json / json_schema_shape | The json_schema template policy selects json_schema_review at scaffold. Safe-edit selects its template profile or .schema.json extension profile. run_checks can select the binding/profile for schema targets. |

The first schema requires an object/mapping root. The second requires an object with the Draft 2020-12 $schema declaration. The same JSON profile separately invokes json_schema_metaschema with --check-metaschema for native schema validity. These assets express configured artifact-quality policy, not adapter protocol or loader schemas.

Their location under config/check_schemas is a current convention, not a runtime requirement: checks.yaml chooses paths via native arguments, and no production code hardcodes these filenames. Alternative policies can use other assets elsewhere. Keeping current paths avoids unrelated argument changes; relocating would require corresponding binding changes, not consumer-code changes. Generic YAML shape acceptance does not prove a partial override composes to valid PGMCP configuration.

- [Binding paths and extension profiles](<../../../.pgmcp/config/checks.yaml>)
- [YAML scaffold policy](<../../../.pgmcp/template_suite/yaml_configuration/policy.yaml>)
- [Schema scaffold policy](<../../../.pgmcp/template_suite/json_schema/policy.yaml>)
- [Native consumer invocation](<../../../mcp_server/bundled_adapters/check_jsonschema/check.py>)
- [YAML mapping schema](<../../../.pgmcp/config/check_schemas/yaml_configuration.schema.json>)
- [Schema-source shape](<../../../.pgmcp/config/check_schemas/json_schema_source.schema.json>)

### Valid null acknowledgements versus missing enforcement

Complete/valid configuration does not mean every acknowledgement is resolved. Check/test/fix schemas admit configuration_choice: null and startup reference/capability validation does not require a choice. Selected execution can refuse its batch with configuration_choice_required before launch. Existing consumers stay unchanged: scaffold retains its refusal path; safe-edit report permits writing for this blocker while enforce refuses.

The owner approved preserving optional enforcement. Missing enforcement resolves to an empty model and runs no configured rules; no placeholder file is required. Portable strict rules belong to the product basis, including open-PR protection. Repository-specific deviations belong to the root override, preserving current effective protections. Earlier all-rules-in-root proposals are superseded; optional file presence does not imply an empty product policy.

| Layered situation | Approved optional-policy direction |
| --- | --- |
| Basis rules present; local file absent | Inherit rules. Missing override is not clearing policy. |
| Both sources absent | Preserve optional policy: existing empty EnforcementConfig, no placeholder required. |
| Only workspace file exists | Admit it with existing schema/version requirements. |
| Workspace explicitly requests removal | Use the Design-defined explicit object-removal contract; do not infer clearing inherited objects from an empty list. |
| A present source is malformed/invalid | ConfigError; optional absence does not hide broken present input. |

The owner explicitly rejects new NULL mechanisms. No enforcement acknowledgement/enabled flag is introduced. This repository retains its current effective rules through the basis plus explicit workspace differences. Optional enforcement does not require an empty policy. Existing configuration_choice and unconfigured-integration admission semantics stay stable; GitHub Settings source ownership changes as approved.

### Deployment-default candidates and actual gate effects

| Surface | Valid neutral representation | Current consequence and scope recommendation |
| --- | --- | --- |
| configuration_choice for checks/tests/fixes | null | Startup-valid; relevant selected execution refuses. Preserve established deployment choice. |
| GitHubSettings owner/repo/token | None, already default | Adapter is lazy. Without token, credential-tool registrations are absent; remaining API-backed calls fail when adapter use requires missing data. Token with incomplete identity also fails at use. Settings/environment is a different source from ConfigLoader YAML; preserve, do not invent personal defaults. |
| GitHub project_number | None | Search found declaration/environment loading only, no active feature consumer. Not a current gate. |
| run_checks default_profile | Omit field; explicit null rejected | Without explicit checks/profile, selection returns default_profile_missing. A possible deliberately defaultless basis, not approved. Approved overlay cannot remove an inherited key merely by omission. |
| Workspace adapter trust | [] | Untrusted nonofficial packages skipped; references to absent capabilities can fail startup admission. Empty list, not null. |
| TestBinding.active | false | Excluded from automatic test selection, explicit selection still possible. Ordinary switch, not null acknowledgement. |
| Contributors / milestones | [] | Valid empty catalogs; no universal startup gate. |
| Git policy | Valid nonempty lists/regex/limits | Null fails schema admission; no existing general Git-only configuration_choice gate. Keep usable policy rather than a deliberate startup failure. |
| Artifact roots, required target includes, workflow contracts | Valid starter values and consistent references | Null can fail structural admission. Use approved src/tests starter conventions; adding unresolved modes would require forbidden consumer changes. |
| Settings config_root/template_root; logging.audit_log | None | Existing conventional-root selection or absent optional audit path, not unresolved-choice gates. |

No new nullable policy requiring consumer behavior changes is proposed. Source inspection supplies this inventory; no new runtime scenarios were executed.

A concrete indirect dependency matters for deployment: configured check_pr_status enforcement on branch_mutating operations uses PRStatusCache, whose cache miss calls GitHubManager and its lazy GitHubAdapter. Missing GitHub token/identity can therefore prevent otherwise local Git actions when that policy is active. Git itself does not inherently require GitHub. Record the combination for an explicit default-policy choice; do not silently change enforcement consumers.

- [Settings and environment defaults](<../../../mcp_server/config/settings.py>)
- [Registration and composition](<../../../mcp_server/bootstrap.py>)
- [Lazy GitHub adapter](<../../../mcp_server/managers/github_manager.py>)
- [Credential/identity admission](<../../../mcp_server/adapters/github_adapter.py>)
- [PR-status dependency](<../../../mcp_server/state/pr_status_cache.py>)
- [Enforcement dispatch](<../../../mcp_server/managers/enforcement_runner.py>)
- [Git policy requirements](<../../../mcp_server/config/schemas/git_config.py>)
- [Existing check-default semantics](<../../../mcp_server/config/schemas/checks_config.py>)

### Reassessment: optional enforcement can have useful defaults

Strict enforcement remains useful default behavior, including the full open-PR branch lock. GitHub dependency is a documented prerequisite, not a reason to weaken defaults. A less strict target must express its own explicit change/removal. No automatic credential-based bypass is approved.

The owner now rejects whole-list replacement as sufficient for these overrides: it would require copying unchanged rules and mask later basis additions. This is the concrete requirement reopening composition, not a hypothetical enhancement. Existing repository protections and their execution order must remain unchanged after source separation.

### GitHub resolution: approved github.yaml ownership

Historical observation: Settings.from_env currently reads optional PGMCP_CONFIG_PATH YAML and then overlays GITHUB_OWNER/GITHUB_REPO/GITHUB_PROJECT_NUMBER/GITHUB_TOKEN from the environment. The supplied MCP example transports these through its env section. PGMCP does not parse harness config. The owner now explicitly replaces that identity-source arrangement; it is no longer a deferred-only topic.

Approved ownership direction:
- Owner/repo come from the selected .pgmcp/config layer (including an explicitly selected external config_root), never inferred from Git remotes or supplied as hidden code defaults.
- MCP launcher examples no longer carry GitHub repository settings. Old runtime Settings/YAML/environment owner/repo routes must not survive as compatibility fallbacks.
- Token normally comes from GITHUB_TOKEN delivered by the process environment; explicit workspace-configured token remains an allowed alternative where environment delivery is unavailable. Proposed precedence is usable environment token first, otherwise explicitly configured token, otherwise existing unresolved/use-time refusal.
- Preserve existing startup/use-time admission semantics and the resolved GitHub value contract where possible; no new NULL mechanisms or readiness framework.
- Revise directly affected setup, launch examples, runtime/configuration references and behavior tests.

| Source option | Benefit | Cost / concern |
| --- | --- | --- |
| git.yaml with a named github section (evaluated alternative) | One repository-related source file | Current GitConfig is a broadly consumed Git-conventions contract. Extending it with service identity/credential data can widen model coupling and incidental fixture preparation. Physical colocation is not inherently forbidden; Design must keep unrelated Git consumers from acquiring new requirements or credentials. |
| github.yaml (owner selected) | Narrow integration declaration; GitConfig and its existing callers can remain unchanged | Adds a source file/schema/load operation. Existing directory-based asset copying already supports an additional source; no builder feature is required. |

Do not pick filename by convenience alone. Both can use the approved defaults/ root convention. Defaults contain no personal repository identity or credentials. The owner has selected github.yaml for repository identity and the explicit configured-token alternative, keeping it separate from git.yaml. Preserve existing startup-valid unconfigured integration and use-time failure semantics, with the approved environment-first token precedence and explicit workspace-token alternative. Do not introduce new null gates. The existing optional project_number has no active feature consumer; do not silently remove it or use it as a new gate while relocating identity.

Consumer inventory: ConfigLoader and configuration schema admission; runtime Settings source parsing; bootstrap's manager injection, credential-tool selection and GitHub resource selection; narrow GitHub value-object import/export ownership; affected Settings/bootstrap/adapter-manager tests. GitHubManager and GitHubAdapter already accept an explicitly resolved value object and need no new resolution behavior. No broad Git/workflow consumer rewrite or suite-wide fixture change is authorized.

Vault finding: targeted source/dependency inspection found no keyring/Windows Credential Manager reader in PGMCP. Settings reads os.environ; proxy copies os.environ into the server process. A vault-to-environment bridge may exist in the host installation but was not verified, and no local credentials or secret-store values were read. Preserve the environment endpoint; do not claim direct vault support or build a new secret backend.

Documentation findings now in scope: fix the source-priority table in github tools reference, remove the user-guide's unselected automatic mcp_config.yaml claim, replace GitHub identity env fields in launch/setup examples and document new workspace identity plus token precedence. Do not expand into unrelated stale logging/settings documentation.

- [Current Settings sources](<../../../mcp_server/config/settings.py>)
- [Current Git conventions contract](<../../../mcp_server/config/schemas/git_config.py>)
- [GitHub value consumers](<../../../mcp_server/managers/github_manager.py>)
- [Credential-dependent registration](<../../../mcp_server/bootstrap.py>)
- [Inherited token environment](<../../../mcp_server/core/proxy.py>)
- [MCP launch example](<../../../docs/setup/mcp.json>)
- [GitHub setup](<../../../docs/manuals/github-setup.md>)
- [Source-priority documentation](<../../../docs/reference/tools/github.md>)
- [Existing bootstrap behavior tests](<../../../tests/mcp_server/unit/server/test_bootstrap.py>)

### Existing PR routes require hosted repository access

Focused inspection confirms SubmitPRTool uses registered branch/head and parent/base, calls GitManager.prepare_submission, then GitHubManager.create_pr and GitHubAdapter's repository API. This is a hosted GitHub PR route: it requires successful Git push access and GitHub API credentials/repository identity with appropriate permissions. Merely configuring a Git remote does not establish API access. The refactor preserves these consumers and admission paths.

Local drafting/scaffolding of a PR body is possible; it creates a text artifact, not a hosted PR with number/status/reviews. Git request-pull generates a textual request referring to a repository URL; it is not a local GitHub PR implementation. No local-PR subsystem, automatic remote inference, new startup probe or GitHub readiness gate is included.

Keep two dependencies distinct: PR operations inherently need the configured hosted service; the optional check_pr_status workspace rule can also make local branch mutations depend on that service. The final owner choice retains this protection in strict defaults; workspace removal must be explicit and missing credentials never imply bypass.

- [PR submission orchestration](<../../../mcp_server/tools/pr_tools.py>)
- [GitHub repository API adapter](<../../../mcp_server/adapters/github_adapter.py>)
- [GitHub PR model](<https://docs.github.com/en/pull-requests/reference/pull-requests>)
- [Git request-pull contract](<https://git-scm.com/docs/git-request-pull>)

### Actual bootstrap tool visibility

Current bootstrap chooses a fixed active subset using only truthiness of settings.github.token. MCPServer lists exactly the supplied active tools. There is no general dependency probe that unlists every tool likely to fail.

| Condition | Current visible/hidden behavior |
| --- | --- |
| Token absent | credential_tools excluded: PR submission/read/list/merge, labels and milestones. |
| Token absent | Issue create/list/get/close/update and local Git/base tools remain active. API-backed issue calls can therefore fail on use. |
| Token present but owner/repo missing or credentials invalid | Token-based registration still includes credential_tools. Lazy adapter/API use may reject the request. |
| Local operation with PR-status enforcement | Remains listed; configured enforcement can reject on its GitHub lookup. |

Git transport credentials (SSH/credential helper etc.) and GitHub API token are different inputs. Bootstrap does not test all Git remote authentication, API permissions, branch state or native-tool readiness. Do not reinterpret this factual answer as permission to redesign registration. The approved new token source must feed all existing registration/resource gates consistently; whether to strengthen the visibility policy is a separate owner decision.

No credentials were changed or probed; this is inspected code behavior, supported by existing bootstrap tests.

- [Active-tool selection](<../../../mcp_server/bootstrap.py>)
- [MCP tools/list implementation](<../../../mcp_server/server.py>)
- [Current token-dependent bootstrap test](<../../../tests/mcp_server/unit/server/test_bootstrap.py>)

### Managed-basis activation and distribution

Deferred. The earlier investigation of a managed basis adopted at deployment remains background for a later issue. This refactor introduces no adoption command, config checkpoint, activation record, rollback mechanism or installation-state extension.

The builder remains unchanged and treats selected assets as opaque content. Its current whole-directory mapping does not distinguish basis from overrides. Therefore this issue cannot claim that a later wheel is portable or excludes workspace differences merely because the loader separates their ownership. Asset routing and installation/init/upgrade acceptance need a subsequent explicit distribution decision.

### Light upgrade reuse: evidence and limits

Deferred research findings: existing atomic writers provide single-file replacement, while the current activation service, checkpoint models and renewal results are template-specific. No generic upgrader, lock extraction or renewal contract change is part of this issue. These observations are retained to avoid restarting the later upgrade investigation from zero.

- [Template activation and locking](<../../../mcp_server/services/template_activation.py>)
- [Atomic JSON writer](<../../../mcp_server/utils/atomic_json_writer.py>)

### #505 and bounded PR-template obligations

#505 remains deferred. The confirmed fail-open paths are malformed mappings being skipped and cleanup errors suppressed; no contaminated wheel was reproduced. This refactor does not resolve those findings and must not claim Closes #505.

The owner explicitly restored one Documentation deliverable: repair PR closing statements in the active source suite so published bodies emit an operative statement for each issue. The live PR schema uses closes (an array of issue numbers); closes_issues is rejected by the existing schema. Current pr/template.jinja2 delegates to sections.issue_refs, which emits references without an operative closing keyword. The current test proves #42/#7 identity and order, but does not require working closing instructions. Adapt that behavior evidence to multiple operative closing statements; retain existing input schema and unrelated rendering.

Bundled assets are generated from the active source suite by the unchanged manifest/builder. Do not treat the ignored generated assets tree as another authored template source, add a new rendering architecture or run a general template audit. The Documentation fix is the second explicit exception alongside removal of the init reset; it does not authorize unrelated consumer changes.

- [PR template](<../../../.pgmcp/template_suite/pr/template.jinja2>)
- [PR context contract](<../../../.pgmcp/template_suite/pr/context.schema.json>)
- [Current PR rendering evidence](<../../../tests/mcp_server/integration/templates/test_pr.py>)

## Questions

No owner strategy question remains. The owner authorizes producer-monitored independent Research/Design/Planning QA, followed by a stop before Implementation for interactive execution. New operators, materializers, public DTO changes, migration or release/build work require renewed discussion.

## References

- [Grafana default/custom ownership](<https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/>)
- [Django resolved settings](<https://docs.djangoproject.com/en/5.2/topics/settings/>)
- [VS Code setting definitions](<https://code.visualstudio.com/api/references/contribution-points#contributes.configuration>)
- [Helm values/schema ownership](<https://helm.sh/docs/topics/charts/>)
- [JupyterHub generated configuration](<https://jupyterhub.readthedocs.io/en/stable/tutorial/getting-started/config-basics.html>)
- [mergedeep v1.3.4 source](<https://github.com/clarketm/mergedeep/blob/v1.3.4/mergedeep/mergedeep.py>)
- [Pydantic Settings sources](<https://docs.pydantic.dev/latest/concepts/pydantic_settings/#other-settings-source>)
- [JSON Merge Patch](<https://www.rfc-editor.org/rfc/rfc7396.html>)
- [JSON Patch](<https://www.rfc-editor.org/rfc/rfc6902.html>)

## Approved Strategy

| Boundary | Owner-approved strategy |
| --- | --- |
| Sources | C: defaults/<file>.yaml plus optional root override; external root self-contained; complete-file/package routes separate |
| Identity | Object collections use one mapping-key ID, including nested objects; no duplicate authored id or technical-name aliases |
| Native merge | Public Pydantic Settings owns add/update/inheritance and scalar/null/value-list replacement |
| Extensions | Only explicit $delete preprocessing and order validation/use; no list matcher/materializer/metadata registry |
| Lists | Scalar/value lists remain whole values; dashes/brackets equal; preserve order/duplicates |
| Runtime | Existing Pydantic validation; directed config-map consumers change; reference values and shared CheckSpec/planning/state/commit/tool DTOs stay stable |
| Enforcement | Optional with no placeholder; strict reusable guards including PR lock; no credential bypass |
| GitHub | github.yaml identity/project_number/explicit token alternative; environment-first GITHUB_TOKEN; old owner/repo launcher/env fallbacks removed |
| Acknowledgements/init | Null startup/use-time/report behavior preserved; remove temporary init rewrite |
| Documentation | Correct active config/setup/launcher descriptions and multi-issue PR close output |
| Exclusions | release_manifest.yaml and builders/distribution/upgrades/releases; #505/#506/#508 work; compat bridges and broad test cleanup |
| Progression | Independent QA for revised Research, Design and Planning; stop at Implementation boundary for interactive work |

This strategy supersedes earlier list-id and generic translation alternatives. Exact operational contracts and dependency choices belong to Design.

## Expected Results

Native mapping inheritance resolves the canonical basis and compact workspace differences into complete validated config. Meaningful object order is explicit; leaf lists and null stay literal. Existing loader/package routes remain, directed config-container consumers change without aliases, and invalid input leaves sources intact. GitHub source changes, init-reset removal and Documentation PR closing correction remain bounded obligations. No packaging/portability claim is made.

## Evidence

### The current package takes active repository config verbatim.

release_manifest maps the complete .pgmcp/config directory. copy_assets uses direct copies; fresh CLI resets only acknowledgements.

- [Manifest](<../../../.pgmcp/config/release_manifest.yaml>)
- [Builder](<../../../scripts/build_package.py>)
- [Fresh CLI](<../../../mcp_server/cli.py>)

### Workspace configuration and package declarations share loader helpers.

Global binding loaders and explicit adapter/template readers share _load_declaration/_load_yaml, so layering cannot be inserted indiscriminately.

- [ConfigLoader](<../../../mcp_server/config/loader.py>)

### Renewal is currently template-scoped.

build_default_operation supplies package assets/template_suite; InstallationState has only pgmcp_version and template_checkpoint.

- [Renewal composition](<../../../mcp_server/cli_renewal.py>)
- [Installation state contract](<../../../mcp_server/config/schemas/installation.py>)

### Direct API and composition edge evidence.

The loader has existing no-path workspace reads and explicit complete-file reads. Missing enforcement currently returns an empty model. ChecksConfig distinguishes omission from explicit null for default_profile, rejects empty profile checks and validates local references. Synthetic fixtures can author isolated source documents without repository-wide preparation. These findings bound the proposed source and merge contract; no new behavior was executed.

- [Existing loader behavior](<../../../tests/mcp_server/unit/config/test_loader_behaviors.py>)
- [Check configuration schema](<../../../mcp_server/config/schemas/checks_config.py>)
- [Check configuration behavior](<../../../tests/mcp_server/unit/config/test_checks_config.py>)
- [Explicit source-tree fixture](<../../../tests/mcp_server/fixtures/suite_roots.py>)

### Existing evidence infrastructure is reusable.

Read-only inspection found loader callers, fresh-init choice tests, shared installed-wheel construction and renewal integration tests. The broader build/renewal inventory is background for deferred work; it does not expand this refactor's test surface. No full suite/builds were executed; the later directed native probe is exploratory evidence.

- [Builder behavior](<../../../tests/mcp_server/unit/test_build_package.py>)
- [CLI behavior](<../../../tests/mcp_server/unit/test_cli.py>)
- [Installed fixture](<../../../tests/mcp_server/fixtures/installed_distribution.py>)
- [Renewal behavior](<../../../tests/mcp_server/integration/test_renewal_cli.py>)

### Executed native-source demonstration

A read-only exploratory probe used actual checks.yaml/enforcement.yaml with in-memory overrides, public BaseSettings settings_customise_sources, higher-priority InitSettingsSource and a basis YamlConfigSettingsSource, omitting env/dotenv/secrets. Versions: Pydantic 2.12.5, pydantic-settings 2.13.1, PyYAML 6.0.3. No private merge/custom recursive add-update code.

Observed: python_lint timeout 60 to 90 retained remaining fields; adding demo_lint increased checks 11 to 12 with all unrelated content retained; ChecksConfig validated. One enforcement override replaced six rules with one while categories survived; EnforcementConfig validated. python_pyright.default_args changed from [--level, warning, --warnings] to [--level, error]. Both source byte sequences remained unchanged; native process exit 0.

Reproduction: use these actual sources; provide the nested timeout/new-binding, single-rule and default_args overrides as higher-priority public sources; validate through existing models and compare source bytes. This is library behavior evidence, not implemented pgmcp layering. The future enforcement map resolves the demonstrated list limitation. The inspected multi-file YAML deep_merge=True API was not the executed route.

## Risks

### Treating the effective merged model as writable source reintroduces copies and drift.

Keep source identity/ownership separate. Retire the temporary fresh-init choice reset as decided by the owner; source composition must not silently materialize inherited defaults into workspace files.

### New basis values can change inherited behavior even when workspace files do not change.

Runtime composition must have explicit precedence and validation. Deliberate basis adoption and upgrade/recovery guarantees remain deferred; do not implement them to complete this refactor.

### Missing overrides could disable enforcement, or layering could alter package declarations.

Separate optional override absence from required basis and explicit package reads; retain existing typed/cross-config validation.

### A constructor/root change could spread into incidental test setup.

Preserve current consumer-facing loader calls; source-layout choices must fit that constraint. Inspect existing fixture seams and adapt only affected behavior tests; 68 textual test callers are not a rewrite authorization.

## Related Documents

- [Inherited #319 research](<../issue319/research.md>)
- [#319 configuration-choice contract](<../issue319/design.md>)
- [Deferred distribution boundary](<../issue319/deferred.md>)
- [Release assets procedure](<../../reference/release-assets-procedure.md>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-15 | @imp researcher | Reuse #319 decisions; record content proposals, primary-source patterns and bounded managed-basis/override feasibility with unresolved semantic and activation choices. |
| 0.2 | 2026-10-15 | @imp researcher | Clarify demonstrated override needs and light upgrade reuse limits; record the owner decision to retire the temporary init-time configuration_choice reset. |
| 0.3 | 2026-10-15 | @imp researcher | Apply owner scope reduction to configuration, loader and focused tests; preserve consumer calls/models/values; defer build, distribution, upgrade, #505 and PR-template work. |
| 0.4 | 2026-10-15 | @imp researcher | Present bounded source-layout, composition and admission choices; identify null/empty/enforcement contracts; restore the owner-requested PR-closing fix specifically for Documentation. |
| 0.5 | 2026-10-15 | @imp researcher | Record approved composition and starter choices; investigate candidate C, explain check-schema assets and distinguish valid null acknowledgements from missing enforcement policy. |
| 0.6 | 2026-10-15 | @imp researcher | Trace native schema consumers and asset ownership; reconsider optional enforcement without placeholders; inventory deployment gates and the PR-status/GitHub dependency of local mutations. |
| 0.7 | 2026-10-15 | @imp researcher | Record owner selection of C, optional workspace-owned enforcement and no new NULL mechanisms; establish existing hosted PR dependency and narrow remaining Research confirmations. |
| 0.8 | 2026-10-15 | @imp researcher | Reassess useful enforcement defaults; distinguish harness environment delivery, settings precedence and Git/GitHub identities; record the reopened ownership choice and active documentation drift. |
| 0.9 | 2026-10-15 | @imp researcher | Record strict enforcement direction and explain full-list replacement; add owner-approved workspace GitHub source scope, file alternatives, token/vault evidence and bounded consumer/documentation impact. |
| 0.10 | 2026-10-15 | @imp researcher | Select github.yaml; reopen targeted composition with explicit removal; identify anonymous-list addressing cost and actual token-dependent tool visibility without weakening strict defaults. |
| 0.11 | 2026-10-15 | @imp researcher | Record approved canonical ID strategy; inventory 14 affected runtime source contracts, unchanged output boundaries and concrete fixture/raw-reader impact; identify ordering as the remaining material contract choice. |
| 0.12 | 2026-10-15 | @imp researcher | Require explicit order and generic translation; compare placement strategies and finite typed-contract materialization, preserve existing runtime validation, and reserve concrete ownership/interfaces for Design. |
| 0.13 | 2026-10-15 | @imp researcher | Record approved id/order and generic translation; present inline removal/error semantics and model-adjacent metadata versus registry; separate ordered values from set-like mutations and consolidate current strategy. |
| 0.14 | 2026-10-15 | @imp researcher | Record directed id normalization through runtime consumers; withdraw id-to-name preservation; reserve removal notation for Design and reopen bounded consumer/test impact research. |
| 0.15 | 2026-10-15 | @imp researcher | Complete identity-model/consumer/test impact evidence; preserve external/reference contracts, identify shared fixture coupling, reconcile superseded wording and close Research for independent review. |
| 0.16 | 2026-10-15 | @imp designer | Record owner clarification: identity determines addressability; unidentifiable elements are whole field values; discard tool-specific/set-like list mutation proposals. |
| 0.17 | 2026-10-15 | @imp designer | Audit existing Pydantic/settings copy, presence, serialization, source merge and experimental facilities; bound the remaining id/$delete semantics without selecting new machinery. |
| 0.18 | 2026-10-15 | @imp designer | Reopen mutation/YAML strategy for native-first evaluation; show deep mapping merge versus native block/list replacement and exact deletion/null consequences. |

| 0.19 | 2026-10-15 | @imp designer | Apply final mapping-key/native-merge decision; reconcile obsolete metadata/identity alternatives, retain leaf lists, record actual probe, exclude manifest and require interactive Implementation. |
