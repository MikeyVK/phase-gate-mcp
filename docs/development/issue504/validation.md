<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 504 — Focused configuration validation

**Status:** FOCUSED EVIDENCE — BROAD COVERAGE EXCLUDED  
**Version:** 0.1  
**Last Updated:** 2026-10-16

## Purpose

Record source-bound behavioral evidence for the approved configuration refactor without claiming workspace-wide verification.

## Scope In

Native mapping composition, exact deletion and explicit order; canonical source/model/consumer cutover; GitHub singleton resolution; preservation of initialization choices.

## Scope Out

Full-suite, branch-wide and configured workspace gates by explicit owner direction. release_manifest, package builders, distribution/upgrade/releases and deferred #505 remain outside this issue.

## Issue Number

#504

## Validation Status

PARTIAL

## Scope

Implementation snapshot 899a1e19a768f03175926ab5ab450f3f4757a9b5. Focused evidence passes; the owner explicitly excluded broad execution scopes. Independent QA decisions are recorded separately.

## Obligations

### D\_1.1 — Native merge boundary

**Evidence:**

- [Native composition behavior](<../../../tests/mcp_server/unit/config/test_composition.py>)

**Outcome:** Passed; add/update delegated to public Pydantic Settings sources without ambient sources.

### D\_1.2 — Explicit deletion and order

**Evidence:**

- [Composition and alias isolation](<../../../tests/mcp_server/unit/config/test_composition.py>)
- [Order admission](<../../../tests/mcp_server/unit/config/test_ordering.py>)

**Outcome:** Passed; strict commands, final model validation and explicit unique ranks.

### D\_2.1 — Canonical source/model cutover

**Evidence:**

- [Source admission behavior](<../../../tests/mcp_server/unit/config/test_loader_behaviors.py>)
- [Product enforcement basis](<../../../.pgmcp/config/defaults/enforcement.yaml>)

**Outcome:** Passed; complete bases and difference-only overrides, guards inherited.

### D\_2.2 — Consumer/fixture cutover

**Evidence:**

- [Requirement projection](<../../../tests/mcp_server/unit/managers/test_phase_contract_resolver.py>)
- [Explicit root isolation](<../../../tests/mcp_server/unit/fixtures/test_suite_roots.py>)

**Outcome:** Passed after bounded QA repairs; no missing-root fallback.

### D\_3.1 — Single GitHub source

**Evidence:**

- [Resolution/bootstrap behavior](<../../../tests/mcp_server/unit/server/test_bootstrap.py>)
- [Layer/token behavior](<../../../tests/mcp_server/unit/config/test_settings.py>)

**Outcome:** Passed; one resolved immutable value, environment-first token without inferred identity.

### D\_3.2 — Initialization and obsolete-path cleanup

**Evidence:**

- [Initialization behavior](<../../../tests/mcp_server/unit/test_cli.py>)

**Outcome:** Passed; copied choices preserved and temporary reset removed.

## Evidence

### C\_1 — Native composition, exact deletion and order

16 composition cases and seven ordering cases passed. The adapted existing deletion case fails before path detachment and passes afterward; removing one addressed member leaves aliased unaddressed siblings and both inputs intact. Native additions/nested field updates, literal lists/null, malformed tombstones, required/default field admission, rank inheritance/tie rejection and exclusion of ambient settings sources are covered.

**Sources:**

- [Composition behavior](<../../../tests/mcp_server/unit/config/test_composition.py>)
- [Order behavior](<../../../tests/mcp_server/unit/config/test_ordering.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_composition.py','tests/mcp_server/unit/config/test_ordering.py'], tests=['python_tests'], timeout_seconds=180). Files were executed in focused implementation calls; combine only for reproduction.

**Observed Result:** Both named modules passed; no broad suite claim.

### C\_2 — Source admission and direct consumer behavior

Focused loader/version/binding, catalog, contract/resolver, enforcement, presentation and public operation selections passed. The final loader plus safe-edit selection passed after preserving the domain diagnostic text and updating enum-case iteration. Startup initialization, resource registration/read and all retained schema-loader paths passed. Fifteen historical label-content assertions were reduced to one layered lookup/order behavior test.

**Sources:**

- [Layer admission](<../../../tests/mcp_server/unit/config/test_loader_behaviors.py>)
- [Contract admission](<../../../tests/mcp_server/unit/config/test_contracts_loader.py>)
- [Phase requirement projection](<../../../tests/mcp_server/unit/managers/test_phase_contract_resolver.py>)
- [Enforcement execution](<../../../tests/mcp_server/unit/managers/test_enforcement_runner.py>)
- [Collection rendering](<../../../tests/mcp_server/unit/presenters/test_collection_text_renderer.py>)
- [Layered label behavior](<../../../tests/mcp_server/unit/config/test_labels_yaml_conventions.py>)

**Invocation:** Each cited behavior module was selected with scope='targets', tests=['python_tests']; implementation timeouts 180–300 seconds. Native yaml_configuration check on the exact18 defaults documents and18 root overrides passed.

**Observed Result:** Selected behavior and YAML checks passed; complete file and optional enforcement semantics remain explicit.

### C\_3 — One GitHub source, registration consistency and initialization preservation

Settings/bootstrap/CLI selection:53 passed. Discovery/server/argument/lifecycle selection:52 passed. Additional affected PR/rollout/fixture/execution selection:81 passed. A later Settings rerun after extending the existing secret-diagnostic case:27 passed, including malformed YAML. No token fixture value appeared in the model or parser exception/cause; no speculative parser rewrite was made.

**Sources:**

- [Settings and secret-safe diagnostics](<../../../tests/mcp_server/unit/config/test_settings.py>)
- [Composition root behavior](<../../../tests/mcp_server/unit/server/test_bootstrap.py>)
- [Initialization behavior](<../../../tests/mcp_server/unit/test_cli.py>)
- [Server behavior](<../../../tests/mcp_server/unit/test_server.py>)
- [Submission behavior](<../../../tests/mcp_server/integration/test_submit_pr_atomic_flow.py>)
- [Effective source consumers](<../../../tests/mcp_server/integration/test_rollout_configuration.py>)

**Invocation:** run_tests(scope='targets', tests=['python_tests'], targets=<exact named modules>, timeout_seconds=180–300). Core targets:unit/config/test_settings.py, unit/server/test_bootstrap.py, unit/test_cli.py. Direct targets:unit/tools/test_discovery_tools.py, unit/test_server.py, unit/server/test_validate_tool_arguments.py, integration/mcp_server/test_server_lifecycle.py. Cleanup targets:integration/test_submit_pr_atomic_flow.py, integration/test_rollout_configuration.py, integration/test_c5_cleanup_and_prstatus.py, unit/fixtures/test_suite_roots.py, unit/execution/test_fix_service.py, unit/execution/test_test_service.py. All paths use tests/mcp_server/ prefix.

**Observed Result:** All selections passed. Search found no remaining Settings.github, old identity environment readers or _reset_binding_choices in production/tests.

### Directed code quality

Ruff format/lint and Pyright passed on the21 C_3/cleanup Python files; Mypy passed on config/settings.py, config/github_resolution.py, config/loader.py, bootstrap.py, cli.py and config/composition.py. Earlier focused C_1/C_2 file gates and production typing also passed. Native arguments and strictness were preserved.

**Sources:**

- [Implementation checkpoint](<planning.md#implementation-checkpoint>)
- [Loader](<../../../mcp_server/config/loader.py>)
- [GitHub resolution](<../../../mcp_server/config/github_resolution.py>)

**Invocation:** run_checks(scope='targets', targets=<changed Python files>, checks=['python_format','python_lint','python_pyright'], timeout_seconds=240); separate production-only run_checks(...checks=['python_types'], timeout_seconds=240). No configured or branch scope was used.

**Observed Result:** Passed. Formatting/fixing was followed by actual checks.

### Independent Implementation review repairs

The root enforcement override is now empty and inherits all unchanged guards. The existing root-isolation test was extended with absent explicit workspace/config selections under hostile ambient settings: RED before the helper fix, GREEN afterward. A directed8module consumer selection passed81 cases and exposed57 cases in3modules still reading the root override as a standalone complete policy; those3modules now use normal layered loading and their rerun passed. Targeted helper/fixture/policy Python gates and both enforcement YAML checks passed.

**Sources:**

- [Root isolation behavior](<../../../tests/mcp_server/unit/fixtures/test_suite_roots.py>)
- [Ready admission behavior](<../../../tests/mcp_server/integration/test_ready_phase_enforcement.py>)
- [Open-PR protection behavior](<../../../tests/mcp_server/integration/test_pr_status_lockdown.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/fixtures/test_suite_roots.py'], tests=['python_tests'], timeout_seconds=180); after policy fixture correction run_tests(scope='targets', targets=['tests/mcp_server/integration/test_ready_phase_enforcement.py','tests/mcp_server/integration/test_pr_status_lockdown.py','tests/mcp_server/unit/tools/test_submit_pr_tool.py'], tests=['python_tests'], timeout_seconds=240).

**Observed Result:** Passed after bounded repairs; no known remaining implementation blocker pending independent recheck.

### Phase-owned focused Validation

The selected composition, ordering, layer-admission and actual server-startup modules passed on the reviewed899a1e19 implementation snapshot. The phase reused all still-valid directed implementation evidence; no broad gate was substituted or silently represented as passed.

**Sources:**

- [Actual startup behavior](<../../../tests/mcp_server/integration/mcp_server/test_server_startup.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_composition.py','tests/mcp_server/unit/config/test_ordering.py','tests/mcp_server/unit/config/test_loader_behaviors.py','tests/mcp_server/integration/mcp_server/test_server_startup.py'], tests=['python_tests'], timeout_seconds=240).

**Observed Result:** Passed. Independent QA granted Implementation→Validation GO on899a1e19 after both P2 repairs.

## Preservation

Public CheckSpec and planning/state/commit DTO contracts stay unchanged. Existing workflow, enforcement, rendering and execution behavior is preserved through canonical keyed configuration and explicit ordering. All current workflow guards are inherited from the complete product basis; the workspace enforcement override is a no-op. Explicit test configuration context remains authoritative even when its directory is missing.

## Containment

Composition only receives caller-owned documents: environment/dotenv/secret settings sources are not used by the native merge. Complete basis admission precedes optional workspace composition; explicit complete-file/package routes do not acquire layering. Readers do not rewrite source documents. YAML alias deletion is path-local. GitHub resolution accepts only the configured identity and an explicit nonempty host token.

## Caveats

- This is focused passing evidence with an explicitly accepted coverage limit; the full native suite, branch gates and workspace-wide checks were not run.
- Existing SchemaAttachment.schema-shadow warnings remain; prior directed resource/Windows path cases also emitted deprecation warnings. These are not newly repaired here.
- The local Codex tool catalog temporarily retained recovery-only tools after a server restart. A separate read-only MCP catalog probe exposed49 tools; native client tools subsequently returned. Current source server admission was healthy. This does not establish distribution or installation portability.
- Initial independent Implementation review returned NOGO on54a9551d for duplicated enforcement defaults and absent explicit-root fallback in test support. Both were corrected within Implementation and independently accepted with GO on899a1e19.

## Related Documents

- [Design](<design.md>)
- [Plan and implementation checkpoint](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp validator | Record focused behavior, quality results and explicit owner-directed coverage limitations. |

## Documentation and PR Package Evidence

The active configuration/setup/GitHub references and three launcher examples now follow the implemented source chain. Eleven changed Markdown documents passed the targeted markdown_links check. All three launcher examples parsed as JSON through an explicit read-only parser check; their safe-edit result was not_executed because no check profile was selected, not a native validation pass.

The PR package's authored version remains 1.0.0; this branch changes only pr/template.jinja2 and its existing consumer test. The context schema, Markdown tracking base and shared issue_refs macro are unchanged. The closes array now emits one operative Closes #N paragraph per entry, preserving integer normalization, order and explicit-empty structure. The existing delivered-package module tests/mcp_server/integration/templates/test_pr.py passed under run_tests(scope='targets', targets=['tests/mcp_server/integration/templates/test_pr.py'], tests=['python_tests'], timeout_seconds=180); Ruff format/lint and Pyright passed on that test file. Native caller arguments were not weakened. Source paths and the eventual PR's Documentation commit identify this unreleased package change; it is not a new published package release or a claim about every valid context.

Reviewed unchanged: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md remains applicable without new architectural exceptions; authoritative agent instructions contain no superseded GitHub identity/reset claims in the scoped search; docs/reference/mcp_vision_reference.md is explicitly historical context and retains that distinction. release_manifest, build/distribution and upgrade implementation remain excluded. The independent Documentation review is the remaining package-source review before Ready.

### Documentation Review Repairs and Actual PR Outputs

Independent Documentation review returned NOGO on 830257407f7677b02991c0da0b4c6cba27f3fb3c for the missed explicitly scoped userguide passage, an ambiguous release/source boundary in the bootstrapguide, and missing native checks on inspectable package outputs. The userguide now requires explicit PGMCP_CONFIG_PATH and excludes GitHub identity from the launcher overlay. The bootstrapguide separates unchanged 3.0.0-wheel setup from deliberate adoption of the unreleased #504 contract; no assembled new wheel or migration is claimed.

After a normal restart the source server admitted healthy. The existing scaffold_artifact route rendered the following exact contexts with artifact_type='pr', target_path='.pgmcp/temp/artifacts/issue504', force_target=true and validation='enforce': pr-minimal.md with {"changes":"","deferred_work":[]} and pr-multi.md with {"changes":"Verify ordered issue-closing output.","deferred_work":[],"closes":[42,7]}. Both scaffolds passed their declared markdown_link_review obligation. A separate run_checks(scope='targets', targets=['.pgmcp/temp/artifacts/issue504/pr-minimal.md','.pgmcp/temp/artifacts/issue504/pr-multi.md'], checks=['markdown_links'], timeout_seconds=120) also passed. I inspected both generated files. They carry template id pr, authored version1.0.0, package fingerprint pgtLHy3YYnG_d0Pd and suite fingerprint WI5iXHBKVOU91bYE. Package source is the PR template introduced at 830257407f7677b02991c0da0b4c6cba27f3fb3c. Temporary files are supplementary; the complete rendered bodies below preserve the evidence after temporary cleanup.

Minimal body, excluding only its technical provenance marker:

```markdown
## Changes

## Deferred Work

No deferred work identified.
```

Representative multi-issue body, excluding only its technical provenance marker:

```markdown
## Changes

Verify ordered issue-closing output.

## Deferred Work

No deferred work identified.

## Closes

Closes #42

Closes #7
```

The minimal context has no closing section; the representative context preserves ordered integer references. The existing delivered-package test separately covers the 42.0 normalization case. These native outputchecks supplement the already passed existing PR behavior module; no new test module or general package audit was added.
