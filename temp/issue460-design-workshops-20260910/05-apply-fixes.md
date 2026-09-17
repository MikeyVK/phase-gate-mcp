<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\05-apply-fixes.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W05 — Lightweight native fix execution

**Status:** HUMAN-APPROVED — CONSOLIDATED IN DI-05 §7.18
**Canonical contract:** [DI-05 §7.18](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md#718-apply_fixes--approved-w05-contract)

The following workshop record is historical preparation. The canonical section supersedes
its proposal/open wording; use that section for implementation and independent review.
No Research, runtime or conformance completion is claimed.
**Owner:** DI-05
**Authority:** [Native-fix Research amendment](C:/temp/pgmcp/docs/development/issue460/research.md#lightweight-native-fix-amendment--2026-09-10)

## 1. Decision nucleus

apply_fixes runs explicitly selected native fix operations on authorized source targets.
The agent owns check/fix/recheck/safe-edit orchestration and optional Git checkpoints.
No generic copies, replacement proposals, compulsory validation, transactional writer,
rollback journal, automatic commit or clean-worktree requirement.

This replaces the previous W05 proposal in this same temporary artifact. Its
FixInput/content, Replacement, verification checks, recovery_path, recovery journal,
overlap admission for DI-04 and application_status transaction model are withdrawn.
No new safe-edit consumer or auto-repair mode is implied.

## 2. Current behavior and intentional improvement

[AutoFixInput](C:/temp/pgmcp/mcp_server/tools/quality_tools.py:196) exposes
auto/branch/project/files with auto default. [QAManager.run_auto_fix](C:/temp/pgmcp/mcp_server/managers/qa_manager.py:1077)
runs configured native fix commands sequentially on source, continues after failures,
has no post-check or rollback, and infers changes from Git dirty state.

Preserve simple native mutation, not Python-specific generic command construction,
auto selection, ambiguous public success or the dirty-file change attribution.
Direct source mutation may leave partial changes after any attempted call.

## 3. Proposed public input

| Field | Type | Meaning |
|---|---|---|
| scope | Required Literal["targets"] | Only approved scope; omission and other values reject |
| targets | Nonempty tuple[WorkspaceRelativeFilePath,...] | Concrete existing files only; no directories, glob/recursive selection or "." root shorthand |
| fixes | Nonempty unique ordered tuple[FixId,...] | Explicit fix choice and order; no automatic choice from previous findings |
| args | Optional mapping[FixId,tuple[StrictStr,...]] | Missing recipient uses binding defaults; supplied list replaces them; [] clears extras |
| timeout_seconds | Optional positive StrictInt | Existing per-invocation budget override |

Research approves files-only scope=targets and explicit ordered fixes. No configured,
branch or workspace scope, no implicit default, no directory recursion. This is a
deliberate V3 break from broad/default V2 selection. PGMCP resolves and validates the
explicit files; adapters do not discover a wider write set or perform Git selection.

One startup schema exposes configured FixIds for fixes and addressed args. Recipient
membership is checked against the resolved selection. No native flag enumeration or
generic CLI interpretation; no public verbose, fresh or allow_expansion.

## 4. Proposed fixes.yaml

```yaml
fixes:
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
```

Illustrative bindings, not a new shipped inventory. Exact fields are adapter_id,
capability, timeout_seconds and default_args. Remove mandatory verification checks
from this file. Existing manifest fix/check relations support discovery only; do not
automatically execute checks or equate fixability with guaranteed complete repair.

## 5. Responsibilities and proposed adapter request

Tool: validates public shape, delegates and presents existing manager-produced facts.
FixManager: resolves explicit bindings/targets, effective args and order; invokes the
shared managed runtime; associates results and unstarted obligations.
Adapter: translates native targets/args, invokes native fixing within authorized scope
and reports tool-specific outcomes without teaching the manager native semantics.

Proposed fix/v1 request, frozen/strict/extra-forbid:
operation: CapabilityId; targets: nonempty tuple[AbsoluteFilePath,...];
args: tuple[StrictStr,...].
No content copy, hash, Git fields, proposal, check request or recovery token.
The three field names match selection check/test transport; mutation permission is
provided by the selected fix role, not by a native argument or extra generic flag.

Native args cannot broaden authorized write scope or make check/test calls mutate.
Adapters must enforce their role and admitted-target contract. This is trusted-extension
conformance, not an OS sandbox guarantee. Unsupported safe routing must refuse honestly.

## 6. Approved order and stop policy

Research requires explicit caller order and stopping before the next fix on the first
non-success: failed, unavailable, request rejection, timeout, crash, malformed response,
cancellation or unconfirmed termination. Preserve earlier results and mutations; the
failed attempted call may also have mutated source. Remaining known obligations are
consumer-owned not_executed/not_started, not native failures. No continue-on-error flag.
This deliberately replaces current continue-on-error behavior. A successful no-change
operation allows continuation. No automatic checks or rollback are introduced.

A native tool may repair some issues yet report others. The adapter determines its
native outcome; generic PGMCP must not reinterpret nonzero as "nothing changed".
A passed fix outcome means native requested operation succeeded, not all checks pass.

## 7. Result nucleus — detailed DTO integration still open

Per selected execution: fix_id, typed native outcome/message/evidence, external_tools,
shared invocation diagnostics, args_source and effective_args. Reuse the shared
response/exit protocol; proposed role outcomes passed/failed/unavailable plus shared
invalid_request, with consumer-owned non-execution for unstarted obligations.
Do not copy check-only reason enums into fix without a real consumer.

Public root: operational success, requested_scope/requested_targets, selected_fixes,
ordered results and existing typed operation-error route. Exact aggregate status is
still Design work, not a new application transaction state machine.
Correctly reported failed native fixing can have success=true/isError=false.
Actual tool execution faults follow the established inverse-success/isError boundary.

Native reports may describe changes, but no exact changed_files/count guarantee,
directory-wide pre/post hashing, or Git-dirty inference is required. An attempted call
with missing/invalid response may have mutated source. Never present it as unchanged.
For rejected or unstarted work, report no invocation rather than fabricate native evidence.

## 8. Agentic recovery

The agent may explicitly commit intended current content before risky fixing, then
check, inspect and choose safe_edit or targeted Git restoration afterward.
apply_fixes never invokes Git mutation automatically and works on dirty inputs.
A commit protects captured content only; subsequent unrelated edits need preservation.
No automatic broad reset, backup store, monitor or hidden recovery requirement.

## 9. Independent evidence

Prove ordered native effects on real fixture files; failure after a write; no-op native
success; unavailable and unstarted steps; dirty inputs; bounded explicit targets;
omitted/unsupported scope and directory/glob rejection before invocation; stop-first
and unstarted obligations; args defaults/replacement; cancellation/timeout;
accurate unknown-change wording and operational success semantics.
Prove no implicit copies, checks, commits or rollback. Native fixture execution and
contract validation must exist independently of the new public tool.
These are required tests, not tests executed by this documentation turn.

## 10. Decision order

1. Realize the approved required scope=targets, concrete files and explicit fix-ID order.
2. Realize the approved stop-on-first-non-success behavior and unstarted-step reporting.
3. Finalize the small fix/v1 outcome DTO and public result projection.
4. Align existing discovery relationships and native configurations; prove conformance.

Keep F-10 renewal and F-20 fix migration in separate implementation cycles. No cycles
are planned here. The human supplied independent Research QA GO; no detailed W05 approval
is inferred from approval of the lightweight direction.

## 11. Concrete contract workshop — proposal, after Research GO

### Admission and exposure

The public object is closed and strict. scope/targets/fixes are required; args and
timeout_seconds may be omitted, never replaced by null. Keep explicit scope=targets
even though it has one allowed value: Research requires it. fixes and targets are
nonempty; duplicate fix IDs reject. Resolve all bindings/args recipients and all target
paths before the first invocation, so invalid later selection does not cause earlier writes.
Resolve workspace containment using the existing path authority; reject directories,
glob syntax, escaping paths and ".". Canonical duplicate target aliases become one
target, preserving first occurrence; this does not expand the selection.
Recheck file existence/containment before each invocation; a disappeared or escaped
target stops execution, not a skip-and-continue. No byte hash, snapshot or CAS guarantee.
Native input can still race with external writers; admission is not OS isolation.

At startup, derive the FixId enum and optional args recipient properties from the
same catalog. No native switches in inputSchema, no lazy-exposure-specific variation.
A no-bindings workspace receives an explicit selection error, not an empty passing run.

Example public call (binding IDs illustrative):
```json
{
  "scope": "targets",
  "targets": ["src/example.py"],
  "fixes": ["python_lint", "python_format"],
  "args": {"python_lint": ["--select", "I"]}
}
```

Each selected adapter receives exactly operation, nonempty absolute file targets and
effective args. The command entrypoint is unchanged; native args travel inside JSON.
The next fix sees the current on-disk content, not a preserved original.

### Proposed fix/v1 response alternatives

Reuse NativeEvidence, ExternalToolIdentity, AdapterInvalidRequest and the managed
process protocol. Separate Fix decision types share shape, not scaffold persistence
semantics. All models are frozen, strict and extra-forbid.

| Variant | decision fields | Other response fields | Adapter exit |
|---|---|---|---|
| FixPassed | status: Literal["passed"] | external_tools required; evidence optional | 0 |
| FixFailed | status: Literal["failed"]; message: NonBlankText | external_tools and evidence required | 1 |
| FixUnavailable | status: Literal["unavailable"]; reason: AdapterUnavailableReason; message: NonBlankText | external_tools required; evidence optional | 3 |
| AdapterInvalidRequest | No decision; existing reason/details only | No external_tools/evidence | 2 |

Passed does not imply a write occurred; a successful no-op uses passed too.
Failed does not imply no write occurred. Evidence is native text/JSON, not a generic
mandatory changed-file inventory. No proposed/unchanged/rolled_back variants.

The existing unavailable reasons have concrete fix consumers:
dependency_unavailable (native dependency cannot be used), unsupported_input (authorized
file selection cannot be handled), invalid_configuration (native settings reject),
execution_error (native execution failed without trustworthy outcome), invalid_result
(native output cannot be interpreted). These may not be used to hide known native
negative outcomes. No adapter timeout reason: generic PGMCP owns its process timeout.
Unknown/malformed adapter responses stay generic invocation failures.

### Consumer result and stop behavior

The manager associates each result with fix_id, args_source/effective_args and shared
invocation facts. It retains received role results, shared invocation failure records
and consumer not_executed with reason=not_started for remaining selected fixes.
Do not manufacture an adapter decision for a launch failure, timeout or crash.

The public root retains operational success, requested_scope=targets,
requested_targets, selected_fixes, ordered results and the existing typed operation
error route. As in W04, no run_status, aggregate passed boolean or generic mutation
count is needed. The ordered rows already identify the stopping outcome and all
remaining obligations. Empty success is impossible because fixes and targets are
required nonempty. No empty_selection variant.

For example, python_lint failed and python_format not_executed/not_started retain
both facts; if correctly handled and reported, success=true/isError=false. A captured
adapter timeout/crash also does not itself establish a PGMCP malfunction. It may have
left edits; shared invocation evidence remains authoritative, not an exit code alone.

No changed_files/count, did_write boolean or generic "safe to retry" flag is introduced.
The presenter explains possible partial mutation when execution was attempted and
refers to native evidence. It must not imply unchanged content after a failed call.
No new DTO-specific presenter branches or error text authored by the public tool.

### Remaining detailed integration

Section 12 proposes the frozen per-result union and operation-error detail types
using existing shared DTOs; human review remains required.
Independently prove registered schema, typed serialization, stop-first behavior and
unknown mutation after invalid responses. No implementation or conformance execution
is claimed by this draft.

## 12. Complete result workshop — proposal for human review

This proposal specializes W04's public result structure, not its continue policy.
Research's stop-first policy remains binding. The operation/capability and internal
absolute-path conventions in section 11 were separately accepted by the human.

### Public result types

All fields below are required unless explicitly stated otherwise. Models are frozen,
strict and extra-forbid; tuples are immutable in Python and serialize as JSON arrays.
Reuse W04/DI-05 shared types rather than introducing fix-specific copies.

ApplyFixesOutput fields:

| Field | Type | Consumer |
|---|---|---|
| success | StrictBool | Existing wrapper: inverse MCP isError, not fix verdict |
| requested_scope | Literal["targets"] | Caller request interpretation |
| requested_targets | nonempty tuple[WorkspaceRelativePath,...] | Requested authorization boundary, not changed-file census |
| selected_fixes | unique ordered tuple[FixId,...] | Caller order; empty only when selection cannot resolve |
| results | tuple[PublicFixResult,...] | Agent follow-up and existing presentation/cache |
| error_code | ApplyFixesErrorCode or null | Manager-detected operation problem |
| error_details | corresponding frozen detail type or null | Existing generic error presentation, no tool-authored domain message |

Public schema rejection uses the existing validation route; it need not construct an
ApplyFixesOutput. Do not fabricate valid requested fields for invalid input.

Each PublicFixResult contains fix_id: FixId, args_source:
Literal["configured","caller"]|null and effective_args: tuple[StrictStr,...]|null.
The argument fields are both known after resolution, otherwise both null. Explicit
caller [] is known and has source caller. Known defaults on an unstarted row do not
claim those arguments were executed.

The closed union adds exactly one of these mutually exclusive shapes:

| Shape | Required additional fields | Owner |
|---|---|---|
| Role result | decision: FixDecision; evidence: NativeEvidence or null; external_tools: tuple[ExternalToolIdentity,...]; adapter: AdapterRunIdentity | Adapter supplies role facts; manager associates binding and shared invocation identity |
| Invocation failure | invocation_failure: AdapterCallFailure; termination_problem: TerminationProblem or null; adapter: AdapterRunIdentity | Generic process runtime supplies failure facts |
| Internal request rejection | request_rejection: nonempty tuple[RequestValidationIssue,...]; adapter: AdapterRunIdentity | Adapter supplies typed rejection; manager classifies internal contract defect |
| Not started | not_executed: Literal["not_started"] | Manager; no adapter invocation identity invented |
| Interrupted invocation | not_executed: Literal["interrupted"]; adapter: AdapterRunIdentity | Shared cancellation projected by manager; an attempt occurred, mutation is possible |

No extra kind, origin or source envelope. FixDecision is the closed passed/failed/
unavailable union from section 11, not a free status string. AdapterRunIdentity is
the existing admitted package identity (adapter_id, version, fingerprint,
contract_version), not native-tool provenance. Native identity stays external_tools.
The interrupted shape deliberately retains attempted adapter identity: unlike a never
started fix it may already have mutated source. Any termination problem is retained
at operation level. This is not a new adapter response or cancellation protocol.

Once selection resolves, return one row per selected fix in caller order when a
response can be delivered. Before selection resolves, results is empty. Preserve all
completed evidence. Optional adapter evidence projects to explicit public null.

### Operation problems and transport success

| ApplyFixesErrorCode | Typed details | success when correctly reported |
|---|---|---|
| no_configured_fixes | null | true |
| selection_invalid | SelectionDetails(issues: nonempty tuple[SelectionIssue,...]); issue has field: Literal["fixes","args"], fix_id: FixId, reason: Literal["unknown_fix","unselected_args"] | true |
| scope_resolution_failed | ScopeDetails(issues: nonempty tuple[ScopeIssue,...]); issue has target: WorkspaceRelativePath, reason: Literal["missing","not_file","outside_workspace","unresolvable"], message: NonBlankText | true |
| adapter_request_rejected | RejectedRequestDetails(fix_id: FixId), referring to the rejection row | false: PGMCP constructed an invalid internal request |
| operation_interrupted | null | true if lifecycle permits delivery |
| termination_unconfirmed | TerminationDetails(fix_id: FixId, interrupted: StrictBool) | true for correctly reported safety stop |

These enum/detail shapes specialize the established operation-error route, not a new
presenter dispatcher. A null error_code requires null details; non-null codes require
their exact matching detail except the two explicitly detail-free codes above.
Scope details identify supplied relative targets, never resolved absolute escapes.
Unknown selected IDs in diagnostics retain the supplied ID rather than requiring
membership of the startup input-schema enum.

Native failed/unavailable and captured invocation failures use their row, with no
duplicated operation error. termination_unconfirmed takes precedence over interruption
and adapter_request_rejected; any rejection details remain in the row and a genuine
internal rejection still sets success=false. A generic PGMCP defect follows the
existing operational error route, never a forged native decision. No native or adapter
exit code directly sets success. Error precedence must not discard earlier evidence.

### Stop, partial mutation and presentation

| Observation | Current row | Subsequent selected fixes |
|---|---|---|
| Valid passed, including no-op | Role result: passed | Start next fix on current on-disk contents |
| Valid failed or unavailable | Corresponding role result | not_started |
| Timeout, crash, malformed/oversized response or launch failure | Shared invocation failure | not_started |
| Invalid internal request | Request rejection | not_started |
| Cancellation during invocation | interrupted, retaining attempted identity | not_started |
| Target admission fails before next invocation | Next and remaining rows not_started; scope error at root | No further calls |

Cancellation before an invocation does not fabricate an interrupted adapter row;
that binding remains not_started. No response is manufactured to a disconnected
caller. Preserve termination uncertainty whenever the lifecycle can report it.

The manager determines typed outcomes and sequencing. Tool code delegates and wraps;
cache serializes the concrete DTO; existing configured presentation summarizes it.
Presentation may warn that an attempted fix can have left changes, but neither native
failure nor interrupted execution means unchanged source. No did_write, changed_files,
automatic recovery, or post-check is introduced. Diagnostics may establish no launch;
do not turn that into a guarantee about earlier successful fixes.

### Required independent evidence before implementation cutover

- Schema and DTO serialization: reject mixed variants, unknown reasons, coercions and
  extra fields; preserve explicit nulls and ordered rows through cache/presentation.
- Passed/no-op continues; failed/unavailable and each shared execution-failure variant
  stop before the next invocation; remaining rows are not_started.
- Native failure and bounded invocation failure report success=true; internally
  invalid requests and genuine PGMCP defects report success=false.
- A fixture adapter mutates then fails/times out: earlier and attempted changes remain,
  later adapters are not launched, and presentation makes no rollback claim.
- Resolve the whole request before writes; recheck targets before subsequent calls;
  show partial results when a later target check fails, without snapshot guarantees.
- Cancellation distinguishes no attempt from interrupted attempt and retains
  unconfirmed termination. Native text/JSON evidence is not reinterpreted as a census.

These are design evidence obligations, not new test execution or Planning cycles.
After review, consolidate accepted W05 contracts into DI-05 and route presentation,
configuration migration and conformance obligations to their existing design owners.
