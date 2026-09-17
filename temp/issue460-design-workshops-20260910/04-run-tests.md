<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\04-run-tests.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W04 — run_tests consolidated review

**Status:** CLOSED W04 v1.0 — human-closed; canonical configuration/request/result integration completed 2026-09-12; runtime and combined QA pending  
**Owner:** DI-05; consumers DI-07/DI-08; shared integration W06/W09/W11/W12  
**Canonical owner:** [DI-05 §7.15](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md#715-approved-run_tests-input-and-exposure--w04-2026-09-10), v0.89; [Design hub](C:/temp/pgmcp/docs/development/issue460/design.md), v1.90.

The canonical §§7.15.1–7.15.5 supersede these working notes. Integration preserves
the accepted behavior and later default_args/scopes. It clarifies ConfigLoader as
file reader (TestsConfig stays pure), requested_targets=[] for configured/workspace,
and known adapter identity on an interrupted attempted invocation. Shared types and
complete error details remain owned there; this temporary document is no longer an
implementation or review authority.

## 1. Decision boundary

The human closed W04 before the check-consumer alignment workshop. This record retains the accepted W04 contracts and incorporates the later approved default_args amendment. DI-05 §7.16 is the single authority for defaults, caller replacement and argument evidence; detailed integration of the remaining accepted W04 types into its canonical owner is documentation work, not a new product-approval gate.

| Boundary | Status |
|---|---|
| Flat tests IDs, addressed args, one startup schema, native switch ownership | Approved, DI-05 §7.15 |
| Required scope configured, workspace or targets; workspace explicitly selects the workspace directory | Approved, D-ADAPTER-24 |
| No generic verbose; native options retain their native meanings | Approved, D-ADAPTER-23, across check/test/fix consumers |
| passed remains successful requested-operation status, including collection-only | Approved, D-ADAPTER-24 |
| Operational success / inverse MCP isError, independent of domain results | Approved, D-ADAPTER-22 |
| Exact tests.yaml records, test/v1 transport shape, result/error DTOs and execution details below | W04 closed by human; integrate the accepted detailed types into the canonical owner |
| Binding default_args, caller replacement and args_source/effective_args | Approved amendment, DI-05 §7.16; supersedes omission-means-empty |

Research remains frozen; preserve F-20's all-active configured test executions, language-neutral process-based adapters, native configuration authority and clean break. No new role, native-option parser, branch test scope, generic collection mode, alias or dual-read route.

## 2. Approved public input and exposure

| Field | Type / default | Rule |
|---|---|---|
| scope | Required configured, workspace or targets | No implicit scope; no auto/project aliases |
| targets | Optional nonempty tuple[WorkspaceRelativePath,...] | Required iff scope=targets; forbidden for configured/workspace; "." is rejected with guidance to use scope=workspace |
| tests | Optional nonempty unique ordered tuple[TestId,...] | Omission selects configured active bindings |
| timeout_seconds | Optional positive StrictInt | Overrides each selected binding budget; not a whole-call deadline |
| args | Optional mapping TestId -> tuple[StrictStr,...] | Missing recipient uses default_args; explicit array replaces it, including []; selected recipients only |

Closed, strict, frozen DTOs; reject unknown fields and explicit null substitutes. Preserve argument token order, whitespace and empty string values. Validate recipient routing before launching any adapter. Do not validate native flag semantics in generic PGMCP code.

```json
{
  "scope": "configured",
  "tests": ["python_tests"],
  "args": {"python_tests": ["-vv", "--tb=long"]}
}
```

Configured means native configured selection, modified by explicit native args. It does not claim whole-workspace coverage. With targets, use native explicit-target semantics instead. workspace explicitly supplies the resolved workspace directory as a target, rather than native default discovery. All three operate from the resolved workspace root.

One startup-built input schema exposes all configured execution IDs in tests and the same args recipient properties; each args value accepts string arrays without native switch enums. Lazy exposure changes delivery timing only. Selecting an ID does not regenerate the schema. A configured binding is not proof of installed dependencies; availability remains on use.

No generic verbose at either public or adapter level. Native settings remain in the tool's own configuration. No hidden --tb override or generic boolean-gated evidence extraction. Cache/presentation bounds are separate; available requested native detail stays in bounded evidence/diagnostics, and truncation must be explicit.

## 3. Accepted configuration: execution bindings, not native settings

Configuration file: resolved_config_root/tests.yaml. Example IDs are illustrative; this does not promise a shipped browser adapter.

```yaml
tests:
  python_tests:
    adapter_id: pytest
    capability: tests
    timeout_seconds: 300
    default_args: []
    active: true
  browser_tests:
    adapter_id: playwright
    capability: tests
    timeout_seconds: 600
    default_args: []
    active: true
```

| Field | Exact type / presence | Consumer |
|---|---|---|
| tests | Required immutable mapping TestId -> TestBinding; empty allowed | One TestsConfig reader, startup schema projection and TestRunManager |
| adapter_id | Required AdapterId | Admitted TestCatalogReader |
| capability | Required CapabilityId, under the referenced adapter's test role | Catalog validation; copied to adapter request operation |
| timeout_seconds | Required positive StrictInt | Shared invocation budget unless caller overrides |
| default_args | Required tuple[StrictStr,...]; [] allowed | Manager selects defaults unless caller supplies this recipient |
| active | Required StrictBool | Default selection only; not trust, installation or exposure |

TestId uses the existing case-sensitive ID grammar [a-z][a-z0-9_]{0,63}. All records are closed, strict and frozen; reject unknown/legacy fields, duplicate YAML keys, unknown/untrusted adapters, missing test roles and unknown capabilities at startup. Native availability is not probed. The distribution supplies tests.yaml; a missing required file is not silently replaced with defaults.

Omitted public tests selects every active binding in declaration order. Explicit tests selects exactly the requested IDs in caller order, including a configured inactive binding. All configured bindings appear in the one startup schema; active=false means only “not part of the default run.” An empty mapping and a mapping with no active bindings remain distinguishable and yield no_configured_tests / no_active_tests when appropriate. Never launch an arbitrary discovered adapter as a fallback.

No separate active-ID list, profile tree, test root, native command, parser settings or duplicated native rule settings. This avoids duplicate membership/configuration authorities. A workspace owner adds languages by installing/trusting an adapter and adding bindings. Configured scope with omitted tests means all active native test selections, not all installed tools.

## 4. Accepted test/v1 request

The later human-approved DI-05 §7.17 alignment replaces the presence-based union.
One strict, frozen, extra-forbid TestRequest has exactly these required fields:
operation: CapabilityId; targets: tuple[AbsolutePath,...]; args: tuple[StrictStr,...].

targets=[] selects native configured discovery. Nonempty targets are resolved existing
files/directories. Missing/null targets is invalid. Public scope remains required;
empty public targets is still invalid. PGMCP rejects "." workspace shorthand and
resolves scope=workspace into one absolute root target; adapters have no scope or
Git fields. The effective args tuple follows §7.16, not the public recipient mapping.

Configured example sent to one adapter:

```json
{
  "operation": "tests",
  "targets": [],
  "args": ["-vv", "--tb=long"]
}
```

Targeted public example:

```json
{
  "scope": "targets",
  "targets": ["tests/mcp_server/unit"],
  "tests": ["python_tests"],
  "args": {"python_tests": ["-v"]}
}
```

Corresponding adapter request:

```json
{
  "operation": "tests",
  "targets": ["C:/temp/pgmcp/tests/mcp_server/unit"],
  "args": ["-v"]
}
```

The example absolute path is internal request data, not public operation output. scope=workspace resolves to the workspace root and uses TestRequest. Public "." targets (including equivalent root-only spellings) are rejected rather than silently converted. Native configured discovery and explicit root discovery are not equivalent: in this workspace native Pytest defaults use testpaths=["tests/mcp_server"], whereas an explicit directory target supplies its own start location. Do not reimplement or merge these rules.

The adapter translates filesystem targets into native selectors: Pytest accepts positional files/directories; Playwright uses path regex filters and requires literal-path escaping and directory-boundary handling. This native translation belongs to the adapter, never generic command construction. Exact cross-platform conformance remains required.

Working directory is the resolved workspace root. The selected manifest entrypoint supplies test/v1; operation is the configured capability. No workspace_root, timeout, test_id, adapter_id, role or public multi-recipient mapping is duplicated in the adapter payload. The shared invoker owns the budget. Args are JSON request data, not arguments appended to the adapter launcher.

Native option validation can happen in the tool; early adapter validation is optional. Role/scope safety is not optional. Native selectors may narrow or refine the request within the authorized boundary, not silently widen explicit targets or authorize source writes. An unhonorable combination is a directed unavailable result. This is not an OS sandbox, and test execution may read imported production dependencies and create normal native outputs/caches.

## 5. Accepted adapter result: passed applies to the requested operation

Use a test-specific result contract with shared NativeEvidence, ExternalToolIdentity and AdapterUnavailableReason value types. Do not inherit the scaffold DTO and do not change the check status vocabulary.

All decision variants are closed, strict and frozen:

| Decision variant | Required fields | Adapter exit |
|---|---|---|
| TestPassed | status: Literal["passed"]; message: NonBlankText | 0 |
| TestFailed | status: Literal["failed"]; message: NonBlankText | 1 |
| TestUnavailable | status: Literal["unavailable"]; reason: AdapterUnavailableReason; message: NonBlankText | 3 |

TestDecision is their status-discriminated union. Passed means the requested native operation succeeded; it does not assert an unrequested behavioral run or certify a workflow gate. A successful collection-only request is passed without a special status. Failed means a trustworthy negative native result. Unavailable means the requested result could not be established. Every variant supplies a concise factual message so native JSON does not require a PGMCP parser to generate a meaningful explanation.

TestRoleResponse has exactly decision: TestDecision, external_tools: tuple[ExternalToolIdentity,...], and optional evidence: NativeEvidence. Evidence is mandatory and substantive for failed, optional otherwise; absence is omission, not null. Messages must agree with evidence. Native counts, IDs, failure details, duration, coverage, last-failed observations and native exit codes retain their native meanings in evidence; unknown values are never fabricated as zero. No generic mode, collection state, coverage model or per-test-case taxonomy.

TestResponse is TestRoleResponse or the existing minimal invalid_request response (reason plus typed RequestValidationIssue list), with adapter exit 2 and no native work. A native usage rejection after a structurally valid request is not invalid_request.

| Situation observed by adapter | Decision / reason | Evidence |
|---|---|---|
| Ordinary native success, including requested collection | passed | Explain actual work; collection is not a generic mode |
| Tests fail or native negative result such as configured threshold rejection | failed | Native explanation and details required |
| Pytest native exit 5: no tests found | passed | Explicit no-tests message; preserve native exit/count evidence, no passing-test claim |
| Well-shaped args rejected by the native tool | unavailable / unsupported_input | Native usage explanation |
| Native dependency missing | unavailable / dependency_unavailable | Explain observed missing dependency |
| Native configuration prevents the request | unavailable / invalid_configuration | Native configuration explanation |
| Native execution fails without a usable result | unavailable / execution_error | Native diagnostics where available |
| Native output cannot be interpreted truthfully | unavailable / invalid_result | Explain inability; do not guess |
| Requested targets cannot be honored | unavailable / unsupported_input | Explain scope/selector limitation, no silent expansion |

Successful native requests use passed/exit 0, not a new completed domain status. The listed Pytest no-tests mapping is the accepted W04 native adapter policy, not an automatic inference from tool success or a completed process. Adapter exit codes are not native exit-code identity. Native exit 5 need not become adapter exit 5. Pytest-specific policy lives in the official adapter and its conformance cases; generic PGMCP never learns Pytest exit numbers. A native tool whose own semantics make absence a negative result need not be forced into Pytest's policy.

## 6. Accepted public output: addressed results and operational faults remain distinct

Accepted RunTestsOutput is closed/frozen and contains these required fields:

| Field | Type | Consumer |
|---|---|---|
| success | StrictBool | Existing wrapper maps to inverse MCP isError; never a domain verdict |
| requested_scope | Literal["configured","workspace","targets"] | Human/agent interpretation of request |
| requested_targets | tuple[WorkspaceRelativePath,...], empty for configured | Scope evidence; no routine absolute paths |
| selected_tests | unique ordered tuple[TestId,...] | Resolved selection, including defaults; empty if unresolved |
| results | ordered tuple[PublicTestResult,...] | Addressed results and retained partial evidence |
| error_code | RunTestsErrorCode or null | Expected selection/operation problem, not a derivation of success |
| error_details | matching typed detail or null | Existing generic presentation/cache path |

No root run_status, tests_passed boolean or generic count total. The ordered result list is enough; combining different framework meanings into a second verdict adds no required behavior here. The root success is not that missing aggregate.

Every addressed result also carries direct args_source: Literal["configured","caller"]|null and effective_args: tuple[StrictStr,...]|null under DI-05 §7.16. Both are present once resolved; explicit caller [] is source caller and a known empty list. Before resolution both are null. These manager fields do not imply native execution or reconstruct native configuration.

PublicTestResult is a closed union of four record shapes. The variant-specific required fields define an unambiguous union without an extra kind/origin/source envelope:

- Role result: test_id: TestId; decision: TestDecision; evidence: NativeEvidence|null; external_tools: tuple[ExternalToolIdentity,...]; adapter: AdapterRunIdentity.
- Invocation failure: test_id: TestId; invocation_failure: AdapterCallFailure; termination_problem: TerminationProblem|null; adapter: AdapterRunIdentity.
- Internal request rejection: test_id: TestId; request_rejection: nonempty tuple[RequestValidationIssue,...]; adapter: AdapterRunIdentity. This retains the actual typed internal-contract failure, not a native result.
- Not started/interrupted: test_id: TestId; not_executed: Literal["not_started","interrupted"]. No adapter/native provenance is invented for a binding that was never invoked.

AdapterRunIdentity contains exactly adapter_id: AdapterId, version: SemVer, fingerprint: AdapterFingerprint and contract_version: Literal[1], populated by the generic runtime from the admitted package. It records an actual invocation attempt, including a launch attempt that fails; it does not claim native work happened. Reuse this package identity shape across consumers rather than defining test-only fingerprint logic. Keep it grouped because its four values describe one package snapshot, not a generic source hierarchy.

Only one of decision, invocation_failure, request_rejection or not_executed may occur. A valid adapter role response projects into the role-result shape; shared InvocationFailed into the invocation-failure shape. A shared cancellation that still permits reporting uses not_executed for interrupted work, with any termination problem retained at operation level. Shared invalid_request indicates the server constructed an invalid internal request: retain its typed details in the rejection row, reference that test_id at operation level, stop and use the genuine operational-fault route. It is not a native failed-test row.

Results follow selected_tests order and have one row per known obligation after resolution, including work not started because a safety stop occurred. No fabricated rows before selection resolves. Successfully returned evidence is never discarded because another binding fails. Adapter evidence omission projects to explicit null in the cached public role-result record; the established null-preserving cache obligation applies.

RunTestsErrorCode and matching details:

| Code | Details | Tool success when correctly reported |
|---|---|---|
| no_configured_tests | null; no further fact needed | true |
| no_active_tests | null; configured bindings remain explicitly selectable | true |
| selection_invalid | SelectionDetails: nonempty tuple of SelectionIssue(field: Literal["tests","args"], test_id: TestId, reason: Literal["unknown_test","unselected_args"]) | true |
| scope_resolution_failed | ScopeDetails: nonempty tuple of ScopeIssue(target: WorkspaceRelativePath, reason: Literal["missing","outside_workspace","unresolvable"], message: NonBlankText) | true |
| adapter_request_rejected | RejectedRequestDetails(test_id: TestId), referencing the request_rejection row without duplicating its issues | false: internally constructed request violates our contract |
| operation_interrupted | null; row facts retain known work | true if cancellation permits a factual response; do not manufacture a response to a disconnected caller |
| termination_unconfirmed | TerminationDetails(test_ids: nonempty unique tuple[TestId,...], interrupted: StrictBool) | true for correctly reported safety stop |

Types above are immutable and extra-forbid; path/error presentation follows W01. For scope errors involving an unresolvable/escaping target, target is the original lexically workspace-relative supplied path, not an absolute resolved escape. Input rejected by the public schema stays in the existing public validation route and may have no RunTestsOutput. Do not invent a second transport-error DTO for it.

error_code is null iff error_details is null except the three explicitly detail-free codes above (no_configured_tests, no_active_tests, operation_interrupted). A null error_code forbids non-null details. For concurrent stop facts, termination_unconfirmed takes precedence over operation_interrupted and retains interrupted in its typed details. No catch-all domain conversion of PGMCP programming exceptions: those follow the existing wrapper's operational error route, success=false/isError=true where a response can be produced.

Important distinction: an expected adapter launch/timeout/crash/protocol failure successfully captured as invocation_failure is not itself evidence that PGMCP malfunctioned. It remains success=true/isError=false with the precise shared failure, rather than a forged adapter verdict. Native domain rejection also remains success=true. A genuine PGMCP internal defect remains a tool failure. No native or adapter exit code maps directly to MCP isError.

## 7. Accepted execution and ownership

Resolve and structurally validate the entire selection/args routing/target scope before launch. Execute selected bindings sequentially in resolved order. Continue after passed, failed, unavailable and bounded InvocationFailed when the shared runtime confirms process cleanup. There is no automatic retry or fallback adapter. An unconfirmed termination stops subsequent launches; retain its original failure and mark remaining rows not_started. Native tool failures do not gain source-write permission. Cancellation follows the established lifecycle contract.

RunTestsTool is a thin public DTO/delegation surface. TestRunManager owns resolved selection, result projection and bounded stop behavior. TestsConfig is the sole config reader. ScopeResolver owns path preparation. The shared invoker owns process framing, timeout, capture and termination. The adapter owns native selection/options, invocation and interpretation. The wrapper/cache/presenter handles serialization and presentation without learning native output semantics.

## 8. Accepted outcomes and presentation

All following ordinary outcomes have success=true/isError=false:

| Selected work | Addressed result |
|---|---|
| python_tests: tests pass | decision.passed; message describes passed native tests |
| python_tests: two tests fail | decision.failed; failure evidence retained |
| python_tests: --collect-only | decision.passed; native message says collected, not executed |
| python_tests: no tests found | decision.passed; explicit zero-test explanation |
| python_tests: invalid native argument | decision.unavailable, unsupported_input, native explanation |
| python_tests fails, browser_tests passes | Both respective role rows; no invented aggregate success verdict |
| python_tests passes, browser_tests times out | Role row plus invocation_failure(timeout); no fabricated browser verdict |

Representative public role-result fragment (provenance omitted from this fragment only):

```json
{
  "success": true,
  "requested_scope": "configured",
  "requested_targets": [],
  "selected_tests": ["python_tests"],
  "results": [{
    "test_id": "python_tests",
    "args_source": "configured",
    "effective_args": [],
    "decision": {"status": "failed", "message": "2 tests failed; 36 passed."},
    "evidence": {"format": "text", "data": "Native failure details..."},
    "external_tools": [{"tool_id": "pytest", "version": null}]
  }],
  "error_code": null,
  "error_details": null
}
```

Normal presented text lists execution IDs, native outcome messages and actionable reasons. It must not describe success=true as “tests passed.” Full native evidence, actual adapter/native versions, invocation details and bounded diagnostics use the existing cache. Stable public operation paths remain workspace-relative; incidental absolute native paths obey W01. No new presenter branching, native JSON parser, NoteContext route, discovery tool or output cache.

## 9. Preservation, deletion and independent proof

- Preserve file/directory/specific native test selection, full native configured discovery, markers, last-failed, coverage, collection, verbosity and time budgets through the approved route; framework-specific flags move to args.
- Remove the public Python-only fields/path splitting and generic server Pytest command builder/parser after independent adapter evidence exists. No aliases, dual reads, adapter options_schema or conditional native-option exposure.
- Move existing Pytest policy/parser cases to official adapter tests; preserve tool-boundary behavior through generic test-role doubles. Keep counts/failures/coverage/last-failed facts in native evidence, not a forced cross-framework DTO.
- Prove the public registered input schema, lazy exposure consistency, config admission/defaults, explicit inactive selection, per-recipient token isolation, configured discovery versus explicit targets including the workspace root, and target containment with actual adapter conformance.
- Prove every response/exit combination and closed/null/type constraint, real cache/presenter projection, failed-tests success=true/isError=false, correctly captured invocation failures, actual internal operational failures, no-tests/native-usage distinctions, partial results and safety stopping.
- Use independent native-versus-adapter evidence for retained Pytest behavior and a non-Python adapter fixture; the migrated run_tests cannot be its own sole proof. W09 owns shipped native settings; W12 owns independent evidence integration. No “all tests passed” certificate from collection/empty/native evidence absence.
- W04 is closed by the human. This record does not claim implementation/schema conformance or complete DI-05. W05 fixes and the separate run_checks args reassessment remain next work; Research stays frozen.

## 10. Cross-consumer integration

| Owner | Integration after this correction |
|---|---|
| W03 / DI-05 §7.14 | DI-05 §7.16 owns selected check default/replacement routing. Separate check scope alignment is not inferred from W04 scope |
| W05 | Use configured default_args with selected FixId replacement; never broadcast fix args to verification checks; recovery/output completion remains W05-owned |
| Scaffold/safe-edit / DI-04 | Configured check defaults only; no public args/verbose; keep complete-content validation and persistence policy |
| W06 | Project final scope fields and tests/args IDs from one startup authority; no native option schemas |
| W09 | Preserve native config values; remove hidden server overrides, not user-authored settings |
| W11/W12 | Align examples, migration and independent native-option/output preservation evidence |

No wholesale approval of neighboring packages follows from W04. No production code, tests, native configs or Research are edited here.

## 11. Source evidence and review

Read-only inspection, not runtime conformance:

- [Current RunTestsInput and command builder](C:/temp/pgmcp/mcp_server/tools/test_tools.py:26): old path/full selection, native flags and hidden traceback mapping.
- [PytestRunner](C:/temp/pgmcp/mcp_server/managers/pytest_runner.py:75): native exit policy, counts, failures, no-tests and traceback parsing.
- [Native configuration](C:/temp/pgmcp/pyproject.toml:45): testpaths and native verbosity/traceback settings.
- [MCP wrapper](C:/temp/pgmcp/mcp_server/server.py:172): success maps inversely to is_error.
- [Tool tests](C:/temp/pgmcp/tests/mcp_server/unit/tools/test_test_tools.py:150), [runner tests](C:/temp/pgmcp/tests/mcp_server/unit/managers/test_pytest_runner.py:162) and [runner double](C:/temp/pgmcp/tests/mcp_server/fixtures/fake_pytest_runner.py).
- [Research F-20](C:/temp/pgmcp/docs/development/issue460/research-findings.md:1644) and [catalog test routing](C:/temp/pgmcp/docs/development/issue460/template-suite-catalog.md:496).
- [Pytest output options](https://docs.pytest.org/en/stable/how-to/output.html), [testpaths](https://docs.pytest.org/en/stable/reference/reference.html#confval-testpaths), [Playwright CLI](https://playwright.dev/docs/test-cli): native semantics, not PGMCP policy.

Integrate the accepted detailed configuration, wire and output records into DI-05 without reopening W04. Apply §7.16's later default-argument amendment, complete the separate check-scope alignment, and continue [W05](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/05-apply-fixes.md).

[Guide](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/00-README.md) · [Audit](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/13-consistency-audit.md)

## 12. Revision record

0.9, 2026-09-10: record human W04 closure and approved default_args/replacement/evidence amendment; configuration and public omission no longer imply an empty native list. No runtime or conformance claim.

0.8, 2026-09-10: consolidate approved configured/targets, native args and passed corrections; remove superseded review alternatives and repeated history from the active contract; retain explicit total-review status for remaining proposals. Canonical corrections are DI-05 v0.74 / hub v1.64.
