<!-- pgmcp:v1 id=planning pv=1.0.0 pf=CscfYyDLqj0OeHml sf=5--KpGf2wHUv2qAj -->

# Issue \#482 — Planning for declarative branch preselection

**Status:** Prepared for independent Planning → Implementation review  
**Version:** 0.1  
**Last Updated:** 2026-10-06

## Purpose

Execute approved Design 0.3 in one coherent clean-break cycle with bounded behavioral evidence and phase-appropriate gates.

## Scope In

Mandatory capability references/workspace policy, generic branch filtering, explicit descendants, truthful no-applicable results, coherent consumer/fixture migration, minimal behavioral evidence and active reference updates.

## Scope Out

Compat/legacy, native configuration/discovery interpretation, force-exclude or intent wire changes, branch test/fix operations, impacted-test selection, old-behavior regression expansion, content snapshots, new permanent harnesses and unrelated cleanup.

## Prerequisites

- Owner GO for Planning: 'Door naar planning'; independent QA Design → Planning GO at e4fc66e568281083318bc6120b8961493d5de917.
- Research 0.15 Approved Strategy and Design 0.3 are binding; no source/test mutation or test execution during Planning.

## Summary

One implementation cycle is required because strict metadata admission, workspace values, the selector/result cutover and existing consumers must become coherent together. Deliverables are dependency-ordered inside that cycle; no intermediate checkpoint/restart may ship mixed old/new contracts. This plan operationalizes [Research 0.15](research.md) and [Design 0.3](design.md), independently reviewed at e4fc66e568281083318bc6120b8961493d5de917. It does not redesign them.

### Actual change inventory

Paths below are workspace-relative. The Design contracts remain authoritative for field/pattern/result details.

| Surface | Planned files / action |
| --- | --- |
| Metadata, values and admission | mcp_server/config/schemas/adapter_manifest.py; checks_config.py; config/validator.py. Use existing ConfigLoader reads; no native parser or second YAML reader. |
| Filter and composition | New mcp_server/execution/configured_targets.py; core/interfaces/execution.py; bootstrap.py. Inject a narrow filter and the same canonical root used for scope paths. |
| Selection, execution and output | execution/check_selection.py; check_service.py; services/check_operation.py; schemas/execution_outputs.py. Replace the calls carrier coherently, preserve explicit descendants and distinguish planned no-applicable from actual native refusal. |
| Authored configuration | .pgmcp/config/checks.yaml; presentation.yaml; mcp_server/bundled_adapters/{ruff,mypy,pyright,lychee}/manifest.yaml. References, policy values, row reason and the four package-version updates follow Design. |
| Direct behavioral test surfaces | tests/mcp_server/unit/config/test_checks_config.py; unit/execution/test_check_selection.py; test_check_service.py; integration/test_checks_public_v3.py. Reuse existing composition/RecordingRuntime; do not add a harness. |
| Coupled fixture-only migration | tests/mcp_server/unit/execution/test_catalog.py; fixtures/adapter_process.py; integration/execution/test_content_input.py; integration/test_template_activation.py; test_template_proposal.py. Their inline manifests/configs or constructed selection capabilities need explicit declarations; existing behavior assertions stay relevant or are removed if obsolete. |
| Inspected preservation surfaces | Native adapter entrypoints, requirements/dependencies, execution/protocol.py; test/fix roles; unit/server/test_bootstrap.py; fixtures/installed_distribution.py; integration/test_installed_distribution_v3.py. No planned native/packaging repair or extra preservation test matrix. Change a consumer only if the actual cutover invalidates its setup. |

Bare .calls search hits in test/fix runtime doubles are not CheckSelectionPlan consumers and are excluded from the carrier cleanup. Repeat the bounded constructor/manifest search at cutover to catch actual missed consumers, rather than mass-editing similarly named fields.

### Execution and evidence budget

Start Implementation with the two existing focused green cases below. Then complete D482.1.1 → D482.1.2 → D482.1.3 before controlled reload and final focused evidence. Baseline failure is investigated and recorded before editing; it is not permission for unrelated cleanup. No artificial RED or characterization of removed behavior.

| Behavioral group | Concrete uncovered risk / smallest evidence | Budget and location |
| --- | --- | --- |
| Policy/admission | Missing required selection declaration; malformed pattern; unresolved reference on a configured check outside the default profile. Existing tests cover ordinary content/selection admission; extend them instead of duplicating those cases. | Three new collected scenarios in existing test_checks_config.py; at most one new parametrized function. |
| Routing/explicit targeting | One mixed branch with two declared subsets proves anchoring, root/nested **, component * / ?, case sensitivity, exclusion precedence and deterministic order. Compare the effective ordinary request with explicit targeting. | One new scenario in existing test_check_selection.py; at most one new function. Representative candidates, no per-adapter/extension list. |
| Explicit descendants | Existing test_explicit_targets_are_canonical_language_agnostic_and_directory_covering encodes the behavior being removed. Replace/rename it to test_explicit_targets_preserve_descendants and retain its duplicate/order/workspace observations. Add explicit policy-bypass observation to that same scenario. | Adapt one existing case; no new collected scenario or legacy companion. |
| No-applicable aggregation | All preselected empty; pass + empty; fail + empty; attempted native refusal + empty; stopped applicable execution with preidentified empty and later not_started. Observe public rows, aggregate status and runtime call count. Existing global-empty case remains the distinction. | Five new collected scenarios in existing test_checks_public_v3.py; at most one new parametrized function using existing composition. No duplicate executor-level matrix. |

Hard budget: **zero new test modules/shared harnesses; at most three new test functions and nine new collected scenarios in total**. Prefer extending existing cases. Parameter rows and looped independent scenarios count toward the same nine; do not hide a matrix inside one function. Ordinary multiple candidate paths in the single mixed-selection scenario are its input, not a matrix of native tools. Mechanical fixture/caller changes do not authorize new tests. No snapshots of documents/YAML/manifests/full JSON/schema, package-version assertions, copied native-default lists, old-route regression tests or compatibility cases.

A demonstrated gap beyond this budget is a stop condition: document the exact uncovered public behavior and seek an explicit plan revision/review before expanding. No discretionary extra run or disposable duplicate demonstration when the focused cases already prove the claim.

### Exact evidence route and timing

**Implementation baseline, before edits** — one existing focused call, not a full module/suite run:

```python
run_tests(
    scope="targets",
    targets=[
        "tests/mcp_server/unit/config/test_checks_config.py",
        "tests/mcp_server/unit/execution/test_check_selection.py",
    ],
    tests=["python_tests"],
    args={"python_tests": [
        "-k",
        "consumer_references_require_the_declared_content_or_selection_input or profile_and_caller_order_determine_calls_with_binding_defaults",
    ]},
)
```

**Implementation exit** — one focused selection in the three existing behavioral files above. Use the names test_configured_targets_admission, test_branch_configured_targets_and_explicit_intent and test_branch_no_applicable_outcomes for new functions when needed, and the adapted explicit-descendant case. Reuse the existing public global-empty case and the two migrated baseline cases:

```python
run_tests(
    scope="targets",
    targets=[
        "tests/mcp_server/unit/config/test_checks_config.py",
        "tests/mcp_server/unit/execution/test_check_selection.py",
        "tests/mcp_server/integration/test_checks_public_v3.py",
    ],
    tests=["python_tests"],
    args={"python_tests": [
        "-k",
        "configured_targets or branch_no_applicable or explicit_targets_preserve_descendants or empty_branch_retains_no_invocation or consumer_references_require_the_declared_content_or_selection_input or profile_and_caller_order_determine_calls_with_binding_defaults",
    ]},
)
```

Record selected/collected evidence so zero matched tests cannot be called a pass. If extending an existing function changes the necessary selector name, update only this focused selector and the stored exit evidence before execution; do not broaden to all modules. Fixture-only consumers receive syntax/format/lint checks now and are covered by the single later suite, rather than separate broad regression runs.

Use actual Git selection at each code gate; partition by file type and production/test role. Changed production .py files receive run_checks(scope="targets", targets=production_python, checks=["python_format","python_lint","python_pyright"], timeout_seconds=600). Changed test/fixture .py files receive run_checks(scope="targets", targets=test_python, checks=["python_format","python_lint"], timeout_seconds=600). Do not offer Markdown/YAML/JSON to Python checks. Strict Mypy remains production-scoped through its native configured run at Validation. Pure declaration syntax/reference coherence is proved through the loader/startup path; no generic Python check is invented for YAML.

Complete declarations/code/callers before restart_server; then health_check and get_work_context must confirm healthy admission and the current branch/cycle. No early restart with half-migrated packages. Reuse evidence until relevant code/config changes invalidate it.

**Validation, once at the required phase**:

```python
run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200)

run_checks(
    scope="branch",
    checks=[
        "python_format", "python_lint", "python_types",
        "python_pyright", "markdown_links",
    ],
    timeout_seconds=600,
)

# Final native-configured workspace check; declared production roots
# remain native Mypy/Pyright policy, and Ruff uses its native settings.
run_checks(scope="configured", profile="python_review", timeout_seconds=600)
```

The branch call is appropriate only after the admitted, behavior-proven per-check filtering cutover: each check receives its own applicable candidates, not the unfiltered mixed inventory. Markdown no-applicable and Python no-applicable rows remain factual. The final configured python_review runs all four declared Python checks; it preserves native discovery and does not include Lychee without input roots. Use directed Markdown targets for active document links.

The native configured suite retains pyproject defaults, including -n auto; no -m/-k/coverage/scope reduction is added to that call. Confirm the approved 1800-second client window is activated as required by docs/setup/README.md; 1200 seconds is the full-run execution budget. Never split merely to fit a short window. Timeout, unavailable or failed gates remain incomplete/failing evidence.

Any discovered findings outside the issue scope are recorded with their exact source and evidence. No #481 waiver, automatic exclusion or unrelated archive/config repair is inherited. Stop for the explicit disposition required by the workflow instead of silently passing.

**Documentation** updates only active references below; run markdown_links on changed Markdown targets and reuse valid native/test evidence. No new phase report is invented beyond the required Validation artifact. Ready owns the normal PR/evidence handover after those phases; this Planning request authorizes no Implementation work.

## Dependencies

- Cycle 1 depends on approved Research/Design only. D482.1.1 precedes D482.1.2, and D482.1.3 verifies/cleans their combined cutover; all three exit together.
- Validation depends on completed Cycle 1; Documentation depends on accepted Validation; Ready depends on completed Documentation. No parallel legacy implementation or partial admission checkpoint.

## Risks

### Strict metadata and callers become invalid if migrated in fragments.

One cycle and one complete cutover before restart; no compatibility checkpoint.

**Consequence:** An incomplete migration blocks exit.

### Bounded scenarios could miss an actual public-boundary gap.

Map the nine scenarios to Design obligations; use existing relevant coverage. Stop and justify any expansion instead of multiplying tool/extension cases.

### Native configured verification may expose unrelated findings.

Preserve native settings and actual evidence; request explicit issue-specific disposition instead of inheriting #481 exceptions.

## Milestones

- C482.1: one completed clean-break implementation cycle.
- V482.1: accepted full configured suite, branch and final configured gates with truthful evidence.
- DOC482.1: minimal active references reconciled; then normal Ready/Coordination handover.

## Work Units

### C482.1 — Coherent configured-targets cutover

**Goal:** Admit and apply the complete generic branch policy/result contract without changing ordinary native invocation or leaving legacy consumers.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

The actual production/declaration and coupled consumer inventory in Summary. Update metadata/policies and matcher, then selector/result/carrier/explicit-target behavior, then invalidated fixtures and minimal behavioral evidence. These are dependency steps within one cycle, not independently shippable transitions.

#### Scope Out

All Scope Out exclusions; no full suite, configured workspace Python run or branch gates during Implementation.

#### Deliverables

##### D482.1.1

Admit explicit configured-target policy references and workspace values; provide the generic frozen policy/filter seam with deterministic matching and composition-root injection.

##### D482.1.2

Cut over branch per-check planning/execution/public results and explicit descendant preservation; migrate all affected declarations and active callers without compatibility paths while preserving ordinary native requests.

##### D482.1.3

Migrate affected test fixtures/consumers, remove obsolete expectations and prove the three behavioral groups within the approved evidence budget; complete focused applicable file gates and cleanup.

#### Exit Criteria

D482.1.1–D482.1.3 are complete together; coherent startup admission and healthy server confirmed after controlled reload; branch subsets, explicit descendants and truthful no-applicable rows/aggregates proven through bounded public behavior evidence; no compat/legacy/native-intent route or directory covering remains; affected callers/fixtures are migrated; focused tests and file-type-appropriate Python gates pass within the evidence budget; ordinary native request/role behavior is preserved; no full suite or workspace-wide checks run before Validation. Missing, failed or incomplete evidence blocks exit.

#### Dependencies

- Research 0.15 and Design 0.3, reviewed at e4fc66e568281083318bc6120b8961493d5de917.

#### Obligations

- Preserve native wire contract_version=1, native pins/configuration/commands/guards and configured/workspace/content/test/fix meanings; apply authored policies only to branch selection checks.
- Use pure frozen schemas, one ConfigLoader, startup cross-validation, constructor-injected narrow filter and no tool IDs/default dialects in generic code.
- Complete all declarations and active callers in the same cycle; remove CheckSelectionPlan.calls and directory covering, with no compat alias/fallback.
- Restore the complete implementation-owned change set to the approved Planning checkpoint if cutover cannot be completed. Recovery must preserve workflow audit and user changes; never use a partial package/code rollback as a compatibility bridge.
- Honor the three-function/nine-scenario/zero-new-module evidence budget and remove obsolete expectations.

#### Verification

##### D482.1.1 admission and policy semantics

**Method:** Run the bounded policy/admission and mixed-candidate cases through existing public loader/validator/selector seams; inspect generic dependency direction.

**Expected Result:** Explicit active refs resolve; malformed/missing refs fail before operation; declared patterns select deterministic subsets without native/tool knowledge.

##### D482.1.2 routing and truthful results

**Method:** Use the existing explicit-descendant case and five public output scenarios; compare actual requests and adapter-call counts.

**Expected Result:** Explicit file intent survives; other scopes keep ordinary input meanings; no request/identity for preselected empty work; attempted refusal and stopped work stay incomplete.

##### D482.1.3 consumer migration, cleanup and applicable gates

**Method:** Repeat the bounded constructor/inline-manifest/plan-carrier search; perform focused exit tests and Git-selected production/test Python gates from Summary; controlled reload plus health/context.

**Expected Result:** Healthy coherent admission, migrated callers, no obsolete covering/alias route, passing focused behavior and applicable code gates; actual selected/collected tests recorded.

#### Stop Conditions

- Approved Design/Strategy conflict, native invocation/guard change or a second policy authority becomes necessary.
- An actual coupled consumer cannot migrate coherently, or startup becomes unhealthy after the complete cutover.
- A gate/test fails, matches no tests, times out or is unavailable; investigate within scope and do not claim exit.
- Additional coverage exceeds the budget or only pins content/implementation shape; require a justified plan revision/review before expansion.
- Baseline or final workspace findings require unrelated repair or an exception not explicitly granted to #482.

## Phase Deliverables

### Validation

#### V482.1

Record the single full native-configured test run, per-check branch gates, final native-configured workspace checks, behavioral/deliverable/cleanup mapping and actual limitations in the required Validation report.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue482/validation.md"

### Documentation

#### DOC482.1

Update the smallest active execution-adapter, quality-tool and server-configuration reference surface for required policy declarations, branch-only matching, no-applicable results and the clean break; verify links and record material reviewed-unchanged surfaces.

## Related Documents

- [Research 0.15 and Approved Strategy](<research.md>)
- [Design 0.3](<design.md>)
- [Quality and evidence standards](<../../coding_standards/QUALITY_GATES.md>)
- [Client/full-run budget policy](<../../setup/README.md>)
- [Active execution-adapter reference](<../../reference/execution-adapters.md>)
- [Active quality-tool reference](<../../reference/tools/quality.md>)
- [Active server-configuration reference](<../../reference/server-configuration.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-06 | @imp planner | Plan one coherent cutover, actual consumer migration, nine-scenario behavioral budget and exact focused/branch/configured evidence routes. |
