<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\03-run-checks.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W03 — Select checks and scope independently

**Status:** APPROVED W03 — integrated into canonical DI-05 §7.14; temporary review record  
**Owner:** DI-05; upstream W02; consumers DI-04, W05, W06, W09 and DI-07  
**Decision nucleus:** Required configured/workspace/targets/branch scope; native tools retain their own behavior under DI-05 §7.17.

## 1. Purpose and authority

An agent can run a lightweight Python preflight, mixed-language maintenance checks or a single check against the same scope without learning YAML. A template consumes a preflight profile; run_checks can consume that same profile without claiming the same completeness purpose.

### Consumer-led review focus

Keep two decisions independent: which configured checks to run, and which workspace
inputs to inspect. A default profile answers only the first; it never supplies scope.
An agent gets selectors from the startup-built tool schema rather than reading YAML.
Templates/safe edit reuse profiles for proposed-content preflight; run_checks owns an
explicit native run over selected existing content, not an implicit full-quality claim.

The decisions in §4 were approved together on 2026-09-10. Most consolidate earlier
workshops rather than reopening choices. The caller timeout override is the explicit
addition; it leaves the internal termination budget unchanged. In particular, distinguish
empty selection, an explicit adapter not_applicable response and a successful native
run whose own selection/exclusion semantics accepted the request. The approved contract
aggregates explicit not_applicable as incomplete. That is deliberately conservative and
may occur routinely with mixed-language profiles; this is an explicit approved choice,
not permission to infer nonparticipation from quiet output. Canonical authority is
[DI-05 §7.14](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md#714-approved-run_checks-contract--w03-2026-09-10).

## 2. Scope and exclusions

Complete checks.yaml, public input, selection request, result and scope behavior. No auto, result replay, dependency graph, subproject model, per-file participation oracle or native-config parser.

## 3. Binding inputs

[Research required-scope amendment](C:/temp/pgmcp/docs/development/issue460/research.md) and [DI-05 §§7.5–7.13](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md). Approved scope spellings are configured, workspace, targets, branch under DI-05 §7.17. Profiles select checks; neither profiles nor args supplies scope.

## 4. Approved decisions

| ID | Approved contract |
|---|---|
| W03-A | checks and profiles remain reusable; run_checks config has only default_profile |
| W03-B | Call selects exactly one profile or nonempty checks list; omission uses configured default only |
| W03-C | Selection requests communicate a bounded expansion ceiling in one invocation |
| W03-D | Not-executed scope/non-applicability are explicit, not accepting empty checks |
| W03-E | Sequential binding order initially; independent checks continue after ordinary negative/unavailable results |
| W03-F | Positive strict timeout_seconds overrides each selected binding's invocation budget, not the fixed internal termination budget |

## 5. Responsibilities and boundaries

ScopeResolver owns workspace containment and Git selection, not language applicability. CheckRunManager resolves bindings, invokes every selected obligation, aggregates facts and owns requested-vs-actual reporting. Adapters decide native applicability, exclusions, expansion needs and interpretation. Tools do not build native commands.

## 6. Options and rationale

Explicit selection with an optional declared default is clearer than “all registered checks.” A mixed profile is an ordinary list, not another type. A single request carrying permission avoids rejected prepare/execute sessions. Sequential first implementation makes duplicate check order and resource pressure predictable; concurrency is not necessary for the public contract.

## 7. Detailed design

### Configuration example

Illustrative IDs and timeout values are not an approved shipped inventory; W09 owns exact official capabilities/settings:

```yaml
checks:
  python_syntax:
    adapter_id: python_syntax
    capability: syntax
    timeout_seconds: 30
    default_args: []
  python_format:
    adapter_id: ruff
    capability: format
    timeout_seconds: 60
    default_args: []
  python_lint:
    adapter_id: ruff
    capability: lint
    timeout_seconds: 60
    default_args: []
  python_types:
    adapter_id: mypy
    capability: types
    timeout_seconds: 120
    default_args: []
  markdown_structure:
    adapter_id: markdown
    capability: structure
    timeout_seconds: 30
    default_args: []
profiles:
  python_preflight:
    checks: [python_syntax]
  python_maintenance:
    checks: [python_format, python_lint, python_types]
  markdown_preflight:
    checks: [markdown_structure]
  workspace_review:
    checks: [python_format, python_lint, python_types, markdown_structure]
profiles_by_extension:
  ".py": python_preflight
  ".md": markdown_preflight
run_checks:
  default_profile: workspace_review
```

All objects closed. IDs unique; profiles nonempty and duplicate check references rejected rather than executed twice. No nested profiles. Bindings have exactly adapter_id, capability, timeout_seconds and default_args. default_profile is optional; absence means callers must select. Empty root maps are allowed for workspaces with no configured checks, but any dangling template/extension/default profile reference fails admission. Unknown root keys, old gate commands and obsolete quality.yaml produce migration errors, not dual reads.

Only profiles referenced by templates/extension fallbacks must be content-capable; a run-only profile may select selection-only checks. run_checks selections require selection support. The same binding can serve both where capability.inputs permits it. No consumer-specific copies of its command or verdict.

### Public input

| Field | Type / default | Constraint and consumer |
|---|---|---|
| scope | required configured\|workspace\|targets\|branch | ScopeResolver |
| targets | nonempty tuple[WorkspaceRelativePath,...] or omitted | Required only for targets, forbidden otherwise |
| profile | ProfileId or omitted | Mutually exclusive with checks |
| checks | nonempty unique tuple[CheckId,...] or omitted | Explicit exact selection |
| args | Optional mapping CheckId to tuple[StrictStr,...] | Replace selected binding default_args; omitted recipients use defaults |
| timeout_seconds | positive strict int or omitted | Per-invocation caller override; default from each binding |

No null substitutions, auto/project aliases or language input. No configured choice: published schema admits no valid selector and no implicit successful default; invocation reports no_configured_checks before native work. Schema representation must remain a valid object schema (for example impossible selector alternatives), not a truncated enum or omitted tool with a new health blockade.

### Scope resolution

targets accepts mixed existing files/directories, recursive overlap deduplication, workspace-relative normalized paths and containment checked after link resolution. Do not cross escaping symlinks/junctions. Missing explicit target is an input error. scope=workspace explicitly selects the workspace directory; public "." targets are rejected, with native selection/exclusion applied by adapters; no hidden Python-only include_globs. Existing native tools determine which discovered files they accept. Branch combines merge-base changes, staged/unstaged and nonignored untracked content. Missing parent/merge-base is an operation error, never empty success.

Approved internal SelectionCheckRequest is a closed object:
operation: CapabilityId; targets: tuple[AbsolutePath,...]; args: tuple[StrictStr,...].

D-ADAPTER-23 removes generic verbose. DI-05 §7.16 now owns default_args and selected CheckId caller replacement: omission uses defaults, explicit [] clears them, no merge or broadcast. The same startup catalog projects optional args recipients; actual profile/default membership is checked before launch. DI-05 §7.17 separately approves configured/workspace/targets/branch; the rejected public mutation-args proposal is not inherited.
targets=[] is allowed only for explicitly configured native selection. Nonempty targets
are existing absolute files/directories resolved by PGMCP. scope=workspace produces
one absolute workspace-directory target; "." is rejected as public target shorthand.
Branch Git resolution/deletion evidence stays PGMCP-owned; zero remaining existing
branch targets returns empty_selection without invocation. Adapters receive no Git
metadata, removed_targets, fresh, expansion_root or allow_expansion.
Default narrow behavior and explicit configured-use/caller args follow DI-05 §7.17.

The adapter preserves narrow targets by default. Supporting reads do not count as checked coverage. A deliberately configured use or explicit caller args may request broader native behavior; no generic permission field, flag parser or automatic fallback is added. A check unable to honor narrow targets returns scope_restricted and factual details.

No existing input selected from branch → manager outcome empty_selection with no adapters, explicitly not a passing certificate. PGMCP-owned removed_targets distinguishes deletions from no changes. Configured targets=[] intentionally invokes native discovery; it does not mean no applicable input.

### Selection-role response

Reuse existing check decision/evidence and invalid_request contracts, with selection-specific additions only:
coverage: CheckedCoverage|null; required_targets: tuple[WorkspaceRelativePath,...] (empty unless expansion refused). CheckedCoverage has targets (native execution boundary, not an exhaustive checked-file census) and expanded:bool.

Add a selection-only not_executed decision with required reason and factual message. Closed reasons: scope_restricted, not_applicable. Native exclusions remain in native evidence; no guessed excluded-file list. A tool that succeeds under its native selection semantics may report passed without proving every supplied path participated. Text says native run passed, not “every file validated.”

Exit mapping: passed=0; failed=1; invalid_request=2; unavailable=3; selection not_executed=3 (no trustworthy verdict). This extends the role-specific matching table, not the shared four exit categories. Scope restriction carries required_targets and no actual coverage. Fresh refusal occurs before substantive analysis. These selection fields do not enter the scaffold-only response shape. W02 has separately approved required external_tools on role results and amended the canonical scaffold payload. These approved selection-only additions must preserve that approved baseline.

Public RunChecksOutput has success, run_status (passed|failed|incomplete|empty_selection), requested_scope, requested_targets, selected_profile|null, PGMCP-owned removed_targets, and ordered results:tuple[SelectionCheckResult,...]. Each result has check_id, the factual verdict fields, coverage/required_targets and W01 invocation facts. Corrected by D-ADAPTER-22: success is operational, inversely mapped to MCP isError, never an all-checks-passed flag. Correctly reporting failed checks, ordinary unavailability/non-execution or an empty selection retains success=true/isError=false. Non-applicable members make run_status incomplete rather than inventing acceptance. Keep all native facts even when run_status is failed.

Operation errors use approved RunChecksErrorCode, not a free string: no_configured_checks, selection_invalid, default_profile_missing, branch_basis_unavailable, scope_resolution_failed, adapter_request_rejected, operation_interrupted, termination_unconfirmed. Required nullable error_code/error_details remain direct output fields, with a closed detail variant appropriate to the code. Native findings and ordinary unavailable check outcomes stay in their result records, not converted into these operation errors. Outer MCP-input rejection may prevent any run result from existing.

Aggregate deterministically: before any selection-derived summary exists, required run_status is null with the applicable error details (absence, not a new verdict); neither absence nor domain error details determines success. No selected inputs gives empty_selection. For a nonempty known obligation set, any unavailable or not_executed member makes run_status=incomplete, otherwise any failed member makes failed, otherwise all passed makes passed. Thus failed plus unavailable is incomplete **with the failed evidence retained**, not an all-pass claim or an MCP tool failure. Only actual tool execution faults use success=false/isError=true through the existing operational error route. Do not map native or adapter exits directly to isError. This run-completeness summary is consumer-owned and deliberately does not change DI-04's approved validation_status precedence.

When an interruption/internal blocker stops the operation, every remaining known check gets consumer-owned not_executed with the existing not_started or interrupted reason, message, null native evidence and invocation only if attempted. Those reasons are not adapter-returned selection reasons. Checks selected before execution remain visible; never fabricate records for selection that never completed.

## 8. Flow examples

python_preflight + one .py file selects syntax only. workspace_review + branch can run Python and Markdown checks; a check with no relevant inputs reports not_applicable, not dependency_unavailable. A type checker needing a whole native configuration boundary refuses an unsupported narrow request; the agent can choose broader targets or explicit native args in a new call. No resume token.

A file changed during native work is not claimed as an immutable verified revision. This proposal promises one selection view and observed native run, **not a filesystem snapshot certificate**. There is no result reuse downstream; workflows must rerun relevant evidence after edits. Disappearance reported by the tool/runtime stays factual, not silently removed.

## 9. Migration and removal

Retire quality_state.json runtime readership, baseline advancement and replay. Leave existing old state inert for owner cleanup; do not delete unknown history automatically. Remove its branch-local artifact registration without touching other workflow/test/fix state. Remove gate-number, Python-filter and parser authorities as W09 choices migrate.

## 10. Evidence

Registered-schema/runtime/default agreement; stale aliases; no startup processes; mixed targets; Git working-state matrix; expansion denial before substantive work; explicit native expansion; zero-target branch no-call; native exclusion evidence; no selected inputs; repeated invocation executes again; every status/code pair; full cached native evidence under text limits.

## 11. Review points

Default-profile behavior, empty/non-applicable result distinction, caller timeout override, and narrow-default/native-argument behavior are approved. Concrete DTO/detail declarations and registered-schema conformance still need integration proof. “Native passed” must not become an all-files participation claim.

## 12. Planning consequences

Scope resolution, role response completion, schema wiring and native adapters are separately provable boundaries. No cycle ordering is assigned.

## 13. Traceability

Q-ADAPTER-04/07/10 → contracts; I-16/I-19 → one authority; required-scope amendment → input/retirement; DI-04 → content-profile admission only; W06 → declarative profile fingerprint projection.

## 14. Related documentation and history

Next: [W04 tests](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/04-run-tests.md), then [W05 fixes](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/05-apply-fixes.md).  
0.3, 2026-09-10: W03 approved and integrated into DI-05 v0.71/hub v1.61; distinguish consolidation from new caller timeout override. Historical entries below retain their original review status.  
0.2, 2026-09-10: consume approved W02 native provenance, emphasize independent profile/scope decisions and expose the mixed-profile not_applicable aggregation trade-off for human review; W03 remains unapproved.  
0.1, 2026-09-10: temporary proposal.

### Approved argument-default amendment

Check bindings additionally require default_args: tuple[StrictStr,...], including explicit []. Per-execution public rows retain direct args_source and effective_args under canonical DI-05 §7.16. Profiles select use-specific bindings; no profile override layer. Content consumers use only configured arguments; run_checks may explicitly replace each selected binding's list. Native settings, safety and success/isError remain separate.
