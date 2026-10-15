<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 504 — Configuration basis and workspace override research

**Status:** RESEARCH COMPLETE — INDEPENDENT REVIEW PENDING  
**Version:** 0.16  
**Last Updated:** 2026-10-15

## Purpose

Reuse #319 findings to investigate a bounded configuration-source refactor. Preserve behavior and unrelated consumer contracts; carry canonical id into directly affected runtime models/consumers rather than translating it to a legacy name-as-identifier field.

## Scope In

Separate canonical product configuration from workspace differences; compose and validate them within the loader boundary; preserve existing public loader calls and complete typed results; adapt focused loader/configuration tests and directly affected test preparation. In Documentation, also correct the active/bundled-source PR template's operative issue-closing output with focused rendering evidence. Retain the previously approved removal of the temporary initialization-time configuration_choice reset as a narrow configuration-write cleanup, not a redesign of initialization. The owner now explicitly extends scope to move GitHub repository identity into workspace configuration, retain environment-first token delivery with an explicit workspace-token alternative, remove old launcher/settings identity sources and correct directly affected documentation. Composition-root changes required for this new source contract are authorized exceptions. The owner additionally permits carrying canonical id through directly affected runtime models and consumers; unrelated consumers remain unchanged. This removes the earlier blanket prohibition on identity-contract consumer changes, not the prohibition on general architecture expansion.

## Scope Out

Package-builder code and content transformations, release-manifest redesign, #505 assembly reliability, wheel/sdist distribution acceptance, managed-basis activation and upgrade/recovery machinery, installation-state extensions, releases, deployment, #506 and #508 implementation, broad test cleanup, and consumer changes unrelated to the approved identity normalization or GitHub source composition. QA orchestration remains owner-controlled. Earlier combined execution of #504/#505 is superseded by the owner's narrower scope; neither issue is closed by this research decision.

## Problem Statement

Current configuration combines product policy with workspace paths, choices and ownership data. Separating those sources can remove that coupling behind the existing loader interface. The package builder remains a source/target copier with no knowledge of configuration contents. Packaging ownership and adoption of a new basis are later concerns, not acceptance claims for this refactor.

## Goals

- Keep one canonical product basis and separately authored workspace differences.
- Resolve and validate both within the configuration boundary. Preserve loader entry points and behavior; permit directed identity-field changes in returned models and their direct consumers, with no id-to-name compatibility projection.
- Preserve the current workspace's effective values while moving their ownership; do not silently alter consumer policy.
- Prove composition, diagnostics and source immutability through focused behavior tests; use the existing suite as required by the active workflow without a suite-wide rewrite.

## Background

The owner directs an interactive process and coordinates QA. No independent review has been requested by the producer. #319's final strategy superseded native-config sample/export proposals: configuration_choice is an owner acknowledgement, not effective-source proof; unresolved choices refuse applicable use while setup/health remain available. Its fresh-init reset is implemented, while DF-319.2 deliberately left manifest content policy unapproved. Existing workspace settings and template-only renewal were preserved. Those findings are reused, not researched from zero. The owner subsequently narrowed #504 to configuration and loader refactoring, deferring the previously combined distribution/build work. The subsequent owner instruction explicitly restores the narrowly bounded PR-template closing fix for Documentation. Online issue bodies still describe the older combined scope; administrative reconciliation belongs to Coordination.

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

Whole-file/list replacement and deep mapping overlays were investigated but do not satisfy the later requirement for targeted inherited-object changes/removal. The owner now approved canonical id/order and generic contract-driven translation. Earlier alternatives are superseded by the approved id/order and explicit-removal strategy. Concrete operation notation and materialization contracts belong to Design.

External evidence remains bounded: mergedeep recursively combines mappings and replaces lists without supplying stable item identity; RFC7396 uses null for deletion, which conflicts with literal-null acknowledgement semantics; RFC6902 provides explicit operations but addresses current anonymous arrays positionally. No merge dependency has been selected or locally probed. Pydantic's existing model/field metadata and before-validators supply reusable admission seams, not automatic source-identity semantics.

### Concrete override needs, without a general patch language

Demonstrated needs are workspace check arguments/acknowledgements, production and artifact roots, local identities/trust, and targeted policy additions, changes or removals without copying unrelated inherited defaults. Earlier whole-object-list replacement and omission-only removal restrictions were evaluated and superseded by the owner's canonical id/order decision.

Scalar/null values retain literal meaning. The final owner clarification below settles nonidentified sequences as whole field values. Earlier set-like operation proposals are superseded; no positional patching or inference from tool-specific list contents is authorized.

### Approved composition and source-admission boundaries

Approved source invariants: canonical id for addressable objects; explicit order, independent of YAML position; targeted addition/change and explicit deletion; unrelated basis entries continue inheriting. Null remains a value. Existing object updates can inherit order; new objects require it; effective sibling ID/order collisions are errors. No implicit append, tie-break or renumbering. New ID-bearing entries must become complete valid objects after composition.

### Identity-based addressability: final owner clarification

The owner defines addressability through explicit identity, not YAML list syntax or tool-specific semantics. An id-bearing object is independently addressable; its named fields and nested fields can be mutated. Nested id-bearing objects are independently addressable in their own parent collection. Elements without their own id are not individually targeted; their containing field value is the mutation unit.

Do not introduce argv-aware merging, set-like scalar-list operations, positional selectors or type-specific list policies. A declared object collection identifies objects by id; an ordinary field containing a list is one whole value. The generic configuration contract distinguishes declared identities from opaque user data; it never invents identity from a field spelling, array index, dispatch type or domain selector.

Explicit removal remains required. Its notation belongs to Design. This clarification supersedes earlier discussion of optional set-like value-list operations; it does not reopen the approved canonical id/order or consumer normalization strategy.

### Approved uniform id contract: concrete impact inventory

The owner approved one consistent id for independently addressable configuration objects and requested impact review before Design. Named source mapping entries and list name fields that currently carry identity must use the same canonical source identity. Structural singleton fields and scalar/value dictionaries do not all become objects. Classification must be explicit in the config contract, not guessed from arbitrary YAML shape.

Read-only source inventory: 18 current top-level YAML files = 17 runtime configuration files plus release_manifest build input; two additional JSON quality-policy assets. Fourteen runtime files contain affected object collections. Three have scalar/value-only contents. Empty contributor/milestone lists still have affected populated source contracts even though today's documents have no entries to annotate.

| File | Addressable source collections and observed population | Existing runtime baseline; identity names now subject to directed change |
| --- | --- | --- |
| artifacts.yaml | artifacts: 23 keyed location objects | Existing keyed location collection / tuple representation and default_root/additional_roots values. |
| checks.yaml | configured_targets: 6; checks: 11; profiles: 7 | Current keyed tuple collections, exact arguments, choice admission and profile references. profiles_by_extension stays a scalar lookup map. |
| contracts.yaml | workflows: 7; phases: 39; exit_requires: 17; branch_local_artifacts: 2; schema also admits cycle_exit_requires lists | ID-keyed workflow lookup; phase technical name becomes id. CheckSpec.id already has correct semantics. Branch-local artifacts need identity independent of path; numeric cycle keys and artifact path/reason remain domain data. |
| contributors.yaml | contributors: currently 0, populated schema has login/name | ContributorEntry login and optional human name. A display name is not blindly renamed to id. |
| enforcement.yaml | enforcement: 6; actions: 6 | Ordered EnforcementRule/Action objects gain explicit configuration identity; existing type/tool/category/policy fields keep their dispatch meaning. The runner does not interpret source operations. |
| fixes.yaml | fixes: 2 keyed binding objects | Existing keyed binding collection; arguments and acknowledgement behavior. |
| issues.yaml | issue_types: 7; optional_label_inputs: 2 policy objects | Existing name-bearing issue entries and keyed input-policy payload. |
| labels.yaml | labels: 18; label_patterns: 2 | Existing GitHub label name and existing pattern/color/description fields. |
| milestones.yaml | milestones: currently 0, populated schema has number/title/state | Remote milestone number remains domain data, independent of any source collection identifier. |
| policies.yaml | operations: 3 keyed policy objects | Existing operation map and operation_id; currently loaded, #506 removal not absorbed. |
| presentation.yaml | tools: 49; global note groups: 4; collections: 24 direct + 1 child; enum cases: 7 | Existing tool/group dictionaries and collection/enum tuples, field selectors, placeholders and render order. Note-template/enum-case text lookup maps remain data, not object identity inferred from their values. |
| tests.yaml | tests: 1 keyed binding | Existing keyed test collection and active/choice semantics. |
| workflows.yaml | workflows: 7 keyed objects with name | Existing workflow dictionary and WorkflowTemplate.name duplicate technical identity. Carry id into the model and its consumers; do not preserve name via a source-id projection. |
| workphases.yaml | phases: 8 keyed objects; schema also admits entry/exit expectation objects | Same phase dictionary, codec vocabulary, terminal detection and metadata. No new workflow semantics or completion mechanism. |

adapters.yaml (trusted ID values), git.yaml (conventions) and scopes.yaml (strings) need C ownership/location handling but no object-ID wrappers for their current fields. New github.yaml is a singleton integration declaration, not an addressable object collection. release_manifest.yaml and its asset list, adapter manifests, template manifests/policies/context schemas and the two check_schemas files keep their separate contracts; the ID rule does not silently rewrite all YAML/JSON in the repository.

### Completed runtime identity and consumer impact analysis

The owner approved carrying id through directly affected models and consumers, with no id-to-name compatibility projection. This table records source inspection, not implemented behavior. Existing string identity values remain stable, so the change is field/representation normalization rather than renaming configured workflows or phases.

| Boundary | Observed current dependency | Directed consequence and preservation limit |
| --- | --- | --- |
| WorkflowTemplate.name / workflows.py | get_workflow returns the catalog entry; production lookup uses workflow dictionary keys, not the entry's name attribute | Replace the technical identity field with id. Preserve ID-keyed catalog lookup and execution-mode values. Direct entry-name reads found only in tests. |
| WorkflowPhaseEntry.name / contracts_config.py | Cycle-owner validation, first/last phase checks, ordered phase lookup and get_phase_names read name | Use id throughout this model/helper boundary. The name-specific helper has one direct production caller in discovery_tools and two test callers; do not preserve a name alias. |
| Phase references outside the contract model | ConfigValidator._validate_phase_contracts reads phase_entry.name; ProjectManager._validate_planning reads phase.name | These two direct consumers change to id. Preserve unknown-phase rejection, cycle ownership and planning validation behavior. |
| IssueTypeEntry.name / issue_config.py | _index is built from entry.name; GitHubManager.validate_issue_params and CreateIssueTool.input_schema read it | Use id for indexing, valid-type errors and schema enum generation. Existing issue_type values and tool input field stay unchanged. |
| OperationPolicy.operation_id / operation_policies_config.py | ConfigLoader injects the field from a mapping key. No direct production attribute read was found; two tests read it | Replace the technical field with id and remove the special injection. Preserve policy lookup/decisions. Do not absorb #506's assessment/removal. |
| Existing keyed object collections | Workflow/phase catalogs, checks/targets/profiles, fixes/tests, artifact locations, operation maps and presentation tool/group maps already use stable keys | Source id remains canonical through object models and ID-keyed runtime lookup. A key is an index of that same identity, not another authored identity. Design may retain useful dictionary/keyed-tuple interfaces; no legacy field alias or implicit second identity. |
| Currently anonymous objects | EnforcementRule/Action, BranchLocalArtifact, LabelPattern, presentation Collection/EnumCase declarations, and populated contributor/label/milestone entries lack independent configuration identity | Add explicit identity at the configuration model boundary. Keep payload/selector/external-domain fields. Most consumers use those fields and iteration, so adding identity does not imply changing execution logic. |
| Existing runtime CheckSpec.id | Shared by configured gates and deliverables.json admission; PhaseContractResolver merges checks by id, WorkflowGateRunner executes them | Already canonical. Preserve its shared planning/deliverable contract; source composition metadata must not introduce required order/removal fields into planning input. |

Direct production identity-reading changes outside schema classes are confined to ConfigLoader, ConfigValidator, ProjectManager, GitHubManager and CreateIssueTool; DiscoveryTools is additionally affected by normalization of the get_phase_names helper. This is the identified direct set, not a guarantee that every file in the wider configuration-source refactor is listed here.

The model population remains the 14 inventoried runtime configuration contracts. In particular: PhaseDefinition/WorkflowEntry and binding/location/profile models need consistent identity handling; EnforcementRule/Action and presentation declarations need independent id rather than reusing dispatch type or DTO field. IssueConfig.optional_label_inputs and workphase expectation payloads currently use broad dictionaries; Design must declare their object-versus-opaque role and validate the supported structure without filename branches. Adding identity must not silently turn the materializer into another domain validator.

| Preserve as real domain/reference data | Reason |
| --- | --- |
| Label.name, ContributorEntry.login/name, MilestoneEntry.number/title | External GitHub names/numbers or human-readable content; lookup by an external value is not the configuration object's override identity. Preserve those lookup functions. |
| Presentation field, cases, templates and tool registration names | DTO selection, text data and MCP tool identity; do not substitute a newly invented configuration id into a DTO property path or tool API. |
| adapter_id, capability, workflow and phase references | References keep their meaning and existing target values. A reference field need not be called plain id; id defines the referenced object. |
| State workflow_name/current_phase, planning phase keys and commit scope values | These store/carry references. Unchanged target values allow preserving state schema, tool DTOs, encoder/decoder and Git history. No new state migration is justified. |
| CheckSpec.id and existing cycle/deliverable identifiers | Already defined shared domain contracts; do not widen this config refactor into planning identifiers or cycle rules. |

Data-shape consumers inspected beyond the direct rename set include PhaseStateEngine and PhaseContractResolver (get_phase and unchanged payload fields), EnforcementRunner (rule/action fields), PR submission (artifact.path), check/test/fix execution selectors (ID-keyed binding collections), ArtifactTargetResolver (template-ID-keyed locations), StandardsResource (explicit policy projection) and TextPresenter/collection renderer (tool-ID lookup and field selectors). Preserve their behavior; only actual changed identity access/representation warrants edits. No consumer receives layer merge logic.

Primary navigation:
- [Workflow identity](<../../../mcp_server/config/schemas/workflows.py>)
- [Phase and shared gate identities](<../../../mcp_server/config/schemas/contracts_config.py>)
- [Issue identity](<../../../mcp_server/config/schemas/issue_config.py>)
- [Operation identity](<../../../mcp_server/config/schemas/operation_policies_config.py>)
- [Cross-config references](<../../../mcp_server/config/validator.py>)
- [Planning phase consumer](<../../../mcp_server/managers/project_manager.py>)
- [Issue manager consumer](<../../../mcp_server/managers/github_manager.py>)
- [Issue enum consumer](<../../../mcp_server/tools/issue_tools.py>)
- [Discovery helper consumer](<../../../mcp_server/tools/discovery_tools.py>)
- [Unchanged shared gate merge](<../../../mcp_server/managers/phase_contract_resolver.py>)
- [Explicit resource projection](<../../../mcp_server/resources/standards.py>)

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
- tests/mcp_server/test_support.py::_NopGateRunner.is_cycle_based_phase directly reads p.name. Update this existing shared preparation seam for id rather than patching every consumer test or installing a compatibility converter.
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

### Explicit order: requirement, options and limits

The owner approved id/order. Source order uses integer ranks local to sibling objects; initial ranks preserve current runtime order. YAML physical position is not execution order. New objects require order; partial overrides inherit it unless they explicitly move the object; duplicate effective ranks fail. Gaps permit insertion but are not unlimited; explicit rank updates are needed if necessary. No automatic renumbering or alphabetical tie-break.

The rejected alternatives remain separate global ID-order lists (duplicated references and inherited additions problem) and before/after graphs (references/cycles/ambiguous placements). Native argv and other ordered values are data sequences, not id-bearing policy objects; their handling is called out separately rather than silently resorted.

### Generically materialize source contracts without file dispatch

The owner approved generic contract-driven translation. Design must assign one config-owned materialization component explicitly. The loader retains file IO, source/target selection and Pydantic model construction; a pure materializer returns ordinary runtime-input data. Managers/presenters/tools never see source directives or perform projection.

Two bounded storage choices remain:

| Contract storage | Benefits | Cost |
| --- | --- | --- |
| Typed immutable metadata beside existing model fields, e.g. Annotated metadata (recommended) | Mapping facts beside their fields; reuse actual model types/aliases and existing validators; no copied domain schema | Existing schema modules gain metadata declarations. Identity fields may change under the owner-approved directed consumer expansion; unrelated types/validators/behavior remain stable. |
| Separate typed Python contract registry referencing models | Runtime schema declarations physically untouched | A second location tracks field paths; validate bindings against model_fields to catch drift. It remains declarative, not one callback/converter per file. |

A user-editable translation YAML and duplicate source model families are not recommended. Runtime models stay the single authority for field types, allowed values and domain validators; metadata states source representation only. All declarations remain pure and immutable, with no loader/file/env/secret IO in schema classes or import-time initialization.

Minimum metadata identifies: addressable collection versus record/atomic or opaque value data; item model/contract for otherwise untyped payloads; representation as a list or ID-keyed mapping input; nested collection relationships. Canonical identity stays id across the affected source/model/consumer boundary; no metadata binding turns id into name to preserve an old technical field. id/order operation semantics are uniform rather than repeated in each file. Existing aliases such as global/global_settings come from model_fields. Reflection supplies structure but never guesses identity from a field's spelling.

A useful simplification follows from current code: ChecksConfig, TestsConfig, FixesConfig and ArtifactLocationsConfig already accept mapping inputs through before-validators and produce their keyed tuple runtime values. The new materializer can emit dictionaries for those collections; it need not implement a bespoke tuple-pair protocol or change the validators. List consumers receive ordered list input. The previous proposal to map workflow/phase id to existing technical name fields is withdrawn. The completed identity inventory above distinguishes technical fields from domain data and identifies the directly affected consumers. Existing mapping-admission validators are reuse candidates, not a reason to preserve obsolete identity names.

Code may branch/dispatch on finite generic node/operation kinds (object collection, mapping/list projection, deletion), never on a filename, tool, phase or policy. A file/model registration is expected; 14 handwritten conversion functions behind a registry would still fail the generic requirement. Another supported-shape config should add declarations/registration without editing materialization algorithms.

Expected impact: the 14 inventoried runtime config contracts remain the starting population. They may gain representation metadata and directed identity changes; the completed inventory identifies direct consumers and model-construction preparation, while unrelated runtime interfaces remain unchanged. This refines the earlier claim that those schema files could stay textually untouched. Source representation necessarily needs declarations somewhere; co-location avoids copying domain constraints. No new package dependency has been established as necessary for this finite traversal.

No prototype or runtime proof was produced. Public Pydantic metadata supports the proposed seam; preservation must be proved through focused source-contract tests and the existing runtime consumer behavior tests during implementation.

- [Existing keyed-mapping admission](<../../../mcp_server/config/schemas/checks_config.py>)
- [Test-binding mapping admission](<../../../mcp_server/config/schemas/tests_config.py>)
- [Fix-binding mapping admission](<../../../mcp_server/config/schemas/fixes_config.py>)
- [Pydantic field metadata](<https://docs.pydantic.dev/latest/concepts/fields/#inspecting-model-fields>)

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

Keep two dependencies distinct: PR operations inherently need the configured hosted service; the optional check_pr_status workspace rule can also make local branch mutations depend on that service. Moving this rule into workspace policy preserves current repository behavior without imposing it on every new target.

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

No unresolved owner strategy choice remains after the directed identity-impact analysis. The owner approved id/order through affected models and consumers, generic contract-driven composition, and explicit removal. The concrete removal notation is a Design decision.

Design owns the exact source/operation grammar, metadata storage and types, configuration-owned component interfaces, ID-keyed runtime representation and identity-based field-value handling. The alternatives already researched are inputs, not approved syntax. Required nonoptional configuration remains required; optional overrides and optional enforcement preserve the approved absence behavior; malformed present input is an error. Explicit complete-file and standalone package reads remain distinct from workspace layering.

Research is complete and prepared for owner-coordinated independent review. No QA message or phase transition is performed here. If Design discovers a need for different reference values, public state/tool DTO changes, bespoke per-file transformation algorithms or build/upgrade machinery, reopen that boundary with the owner rather than silently expanding scope.

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
| Source ownership | C: product defaults under config_root/defaults; workspace differences at config_root. Existing effective repository values preserved through deliberate source separation. |
| Configuration objects | One canonical id and explicit order; targeted addition/change and explicit removal retain unrelated inheritance. Physical YAML order is not runtime order. Concrete directive and metadata storage are Design-owned decisions. |
| Runtime consumer interface | Preserve loader entry points, operational/reference behavior and unrelated contracts. Carry canonical id into affected runtime models and direct consumers; no id-to-name compatibility projection, duplicate authored technical identity or consumer-owned composition. Completed direct impact inventory constrains Design. |
| Generic implementation | Contract-driven materialization, with no filename if/else or registry of bespoke per-file algorithms. Design must name its config-owned responsibility. |
| Enforcement | Optional without placeholders; useful strict defaults include open-PR protection. Preserve current repository protections; missing credentials are no automatic bypass. |
| GitHub sources | github.yaml owns repository identity and explicit token alternative; normal token source is environment. Remove old owner/repo launcher/env/settings fallbacks, no remote inference or personal defaults. Narrow Settings/bootstrap registration changes and documentation are approved exceptions. |
| Existing acknowledgement semantics | Keep configuration_choice valid-null-at-startup/use-time refusal and current safe-edit report behavior; no new NULL mechanisms. |
| Initialization | Remove the temporary configuration_choice rewrite; no broader init/upgrade lifecycle. |
| Documentation | Correct affected configuration/setup descriptions and the operative multi-issue PR closing template; targeted evidence. |
| Deferred | Builder/content transforms, packaging proof, upgrades, release, #505, #506/#508 implementation and broad test cleanup. No automatic migration/legacy bridge or new generic readiness/vault framework. |

The owner-approved directed runtime identity expansion is now supported by model/consumer/test evidence. Removal notation, metadata placement and concrete operation contracts remain Design choices. No owner strategy question remains; QA stays owner-coordinated and Design has not started.

## Expected Results

Canonical basis and workspace differences resolve to complete, validated configuration through preserved loader entry points. Affected model/consumer identity contracts use id consistently. Current repository settings retain their effective values. Invalid source/composition data produces actionable diagnostics without modifying either source. Focused behavior evidence demonstrates inheritance, precedence, list/null handling and unaffected standalone package reads. The two bounded exceptions are deletion of the temporary init reset and operative PR-closing output in Documentation. Unrelated consumer changes or a need for build/upgrade machinery fail the agreed scope boundary. Approved identity-consumer changes remain directed and evidence-backed.

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

Read-only inspection found loader callers, fresh-init choice tests, shared installed-wheel construction and renewal integration tests. The broader build/renewal inventory is background for deferred work; it does not expand this refactor's test surface. No tests or builds were executed for this Research.

- [Builder behavior](<../../../tests/mcp_server/unit/test_build_package.py>)
- [CLI behavior](<../../../tests/mcp_server/unit/test_cli.py>)
- [Installed fixture](<../../../tests/mcp_server/fixtures/installed_distribution.py>)
- [Renewal behavior](<../../../tests/mcp_server/integration/test_renewal_cli.py>)

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
