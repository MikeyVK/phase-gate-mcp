<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=3zJkRylM4sIT4HzD sf=9PfER5JkyAoFQLRi -->

# Issue 460 Refactor Validation

**Status:** Fresh full-suite revalidation completed; independent QA returned NOGO on unresolved findings
**Version:** 1.6
**Last Updated:** 2026-09-27


## Purpose

Record observed validation evidence and blocking gaps without declaring independent QA approval.

## Scope In

Authoritative plan/strategy review, accepted deferral reconciliation, structural and host-carrier audits, one complete configured eight-worker suite, branch checks and diagnostic configured/targeted checks. The 2026-09-27 current validation pass supersedes earlier execution outcomes; earlier sections retain historical provenance.

## Scope Out

Production/test repairs, deferred adapter redesign, external-workspace migration, release, merge and phase progression. Test-environment dependencies were corrected during the historical follow-up investigation below; configured test defaults, exclusions and the local 300-second client deadline remain in force.

## Prerequisites

- Research Approved Strategy, Design package contracts, Planning and the completed 110-cycle plan remain binding.
- Implementation evidence is indexed by CY001–CY110 cycle cards; the current full-suite and gate outcomes are recorded below, with older cycle and validation results retained as provenance.




## Issue Number

#460




## Validation Status

FAIL



## Scope

Refactor issue #460, branch refactor/460-audit-scaffolding-schema-template-contracts. V460.1–V460.5 remain the binding completion obligations. The phase is validation; no production repair or strategy change is authorized by this report.



## Current validation pass — 2026-09-27

This section supersedes the earlier execution outcomes below. The previous investigations and proposed CY106–CY110 repairs remain provenance, not current failures. The native suite and branch-check evidence was captured after CY110. CY111 subsequently corrected five agent-documentation files only; no production or test code changed, so those native observations remain fresh for the changed-code surface. CY111's documentation evidence and the owner policy disposition are recorded below.

### Required native execution

| Selection | Observed native result | Cached operation |
|---|---|---|
| `run_tests(scope="configured", tests=["python_tests"], timeout_seconds=300)` | Pytest 9.0.2 created 8/8 workers, selected 2,621 items, **2,619 passed, 1 skipped, 1 XPASS**, 229 warnings, exit 0 in 213.57s. No adapter deadline, output truncation or termination problem. | `pgmcp://cache/runs/ff4505aaa13c44f5a828c05b6a0cca87` |
| `run_checks(scope="branch", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=300)` | **Incomplete:** Ruff format/lint and Mypy could not launch with WinError 206 (command line too long); Pyright could not launch Node with ENAMETOOLONG. All four native results are unavailable, not passed. | `pgmcp://cache/runs/70db1da0f6d142f4be719243eec72968` |

The full-suite XPASS is `test_server_renders_exclusion_note_in_response` in `tests/mcp_server/unit/managers/test_enforcement_runner_unit.py`. After Pytest's successful exit, a restart-tool unit test also emitted a `Task exception was never retrieved` / `SystemExit(42)` message. These are observable caveats, not additional failed test cases. The suite includes 159 passing shipped-adapter integration cases, 65 public V3 check/test/fix/scaffold/edit cases, three cache-fidelity cases, installed-distribution, startup, cut-over, activation and renewal coverage. The full cache is the authoritative item-level record.

Supplemental calls distinguish usable coverage from the unavailable branch gate:

- In the combined configured run of all four checks, Mypy 1.19.1 passed all 184 configured production source files (`pgmcp://cache/runs/8b61c921bb7f43cb9f2e42a818fea26c`).
- In that same configured run, Pyright 1.1.408 passed 184 production files with zero errors or warnings. Ruff format reported 469 already formatted files but ended unavailable on Windows access denied (os error 5). Ruff lint reported 130 T201 diagnostics confined to four archived demo files under `docs/development/archive/issue52` and `issue72`, alongside the access warning (`pgmcp://cache/runs/8b61c921bb7f43cb9f2e42a818fea26c`).
- Targeted `mcp_server, tests/mcp_server` Ruff format/lint passed: 459 already formatted files and all lint checks passed (`pgmcp://cache/runs/c04597b765624a429e7b13bea0186f51`). Targeted `scripts` Ruff format/lint passed: one already formatted file and all lint checks passed (`pgmcp://cache/runs/556b0e36ba1c4fc9808f65dad76735e8`). These selections are narrower than the required branch gate.
- Targeted `mcp_server, tests/mcp_server` Pyright passed 461 files. Mypy reported 1,183 errors in 101 of those 461 files; all reported diagnostic lines were under `tests/`, with zero production diagnostic lines (`pgmcp://cache/runs/ac4eb17630334251801020bd32277e82`). Baseline attribution for this expanded test-type selection is not established. It does not negate the passing configured production Mypy gate, and it is not silently covered by D-VAL-01.

### Expanded test-Mypy diagnosis and disposition boundary

The configured Mypy gate follows `pyproject.toml [tool.mypy].files = ["mcp_server"]` and passes 184 production sources. The separate explicit-target diagnostic adds `tests/mcp_server`, so it applies the project's strict Mypy settings to test fixtures and helper modules that the configured gate does not select. The `tests.*` override relaxes only `disallow_untyped_defs`; it does not suppress incorrect arguments, optional-member access, untyped return values, or unused ignores. Mypy 1.19.1 reports 1,183 errors in 101 of 461 selected files, with no production error lines in the bounded native capture. The adapter's stored native text contains a bounded head/tail rather than all 1,183 individual lines; the total and affected-file count come from Mypy's own summary, while the examples below come from visible lines.

The visible diagnostics show several distinct causes: constructors in older tests omit now-required `version` or `require_tdd_prefix` values (`call-arg`); dictionary-shaped fixtures and `object`-typed dependencies do not satisfy specific config models (`dict-item`/`arg-type`); optional result members and generic tool decorators are not sufficiently narrowed or typed for strict checking (`union-attr`/`arg-type`); some helpers return `Any` despite typed returns; and old `type: ignore` comments are no longer needed. Examples include `test_workphases_schema.py`, `test_label_startup.py`, `fixtures/server_process.py`, and the new public V3 check/test/fix/edit test composition. Passing runtime tests do not prove those static contracts.

CY107 already compared its **nine exact changed test/support paths** under identical targets, Mypy 1.19.1 and configuration: 418 pre-cycle diagnostics versus 417 afterward, with zero new normalized diagnostics and one removed `unused-ignore`. That documented exception was explicitly limited to CY107's paths. It does not establish a baseline for the present 101-file selection. The earlier Validation run on the same broad targets reported 1,223 test diagnostics plus nine production diagnostics before CY106–CY110; the current 1,183 test diagnostics and zero production diagnostics show improvement in aggregate but are not a line-by-line main-branch attribution.

**Owner disposition for issue 460, 2026-09-27:** The explicit test-target Mypy run is exploratory diagnostic evidence, not a required Validation gate. [Issue 72's documented config-driven hybrid policy](../archive/issue72/qa_alignment.md#decision-option-c-config-driven-hybrid) deliberately excludes tests from strict Mypy because dynamic test doubles such as `Mock`/`AsyncMock` create noise and false positives; production code retains strict Mypy, while test typing receives lighter treatment. Both legacy Mypy gates excluded tests. DI-05 §7.20 approves the capability to inspect explicitly supplied test targets with native Mypy, but that capability does not change the required workflow selection or revoke the prior policy. The configured production-Mypy pass is the applicable Mypy gate for #460; the 1,183 test diagnostics are neither a pass nor a blocker by count, and a whole-test-tree Mypy baseline comparison is not a #460 exit criterion. Individual diagnostics still merit action if they expose a concrete violation of a separately binding test or architecture contract. No global disable, blanket ignore, or claim of test-Mypy conformance follows from this disposition. Any future change making strict test-Mypy mandatory requires an explicit owner decision, stated scope, baseline/remediation strategy, and amended workflow/check configuration before QA applies it. Documentation phase must make this distinction durable in the quality/QA guidance so a diagnostic invocation cannot silently become a gate.

### V460.1–V460.5 evidence and open boundaries

| Obligation | Current assessment |
|---|---|
| V460.1 exact structural closure | The ownership ledger has contiguous unique C001–C126, T001–T151, A001–A079 and S001–S057 rows with no cross-register duplicate. Current files: C 74 present/52 absent, T 26/125, A 0/79, S 52/5. The five absent S paths have retirement dispositions; C084 and remaining retired package initializers are docstring-only. Bounded active-runtime search found no retired scaffolding/validation/quality imports or old template/config paths. All 121 new template-suite files are enumerated in the proposed-new register. The register has 288 unique existing proposed paths, whereas its prose says 279 originals plus one CY059 addition. The owner-card reconciliation below resolves this as stale aggregate-count provenance rather than eight unowned implementation paths (F-VAL-06); retained-assertion semantics and dependency direction still need independent judgment. |
| V460.2 native, consumer and public behavior | The single passing full suite includes native adapter integration, public V3 check/test/fix/scaffold/edit routes and cache-fidelity tests; no new failure was observed. Prior cycle evidence and the full item log support this obligation within the tested boundaries. Deferred native option/selection fidelity across nine adapters remains D-VAL-01, not an assertion of complete native semantic conformance. |
| V460.3 installed package, migration, recovery and rediscovery | The full suite passed the complete installed-distribution test, six target-startup tests, two isolated V3 cut-over tests, ten template-activation tests and nine renewal CLI tests. After the final implementation changes, the active server was restarted; a new process (PID 31568) returned `get_work_context`, health status and live `scaffold_schema(validation_report)` (`pgmcp://cache/runs/51ea607dd0db400d9d3ddc5e8899790f`, `a36d9196598f425fa42fbab85f08b102`, `4685761f8120453c90766c70f9b68bf1`). This proves current client rediscovery and loaded schema availability. The CY072 real cut-over/first migration and historical client demonstration remain separately indexed in Planning/rehearsal; isolated tests and this later reload do not retroactively prove every historical cut-over step. |
| V460.4 suite and branch gates | Full configured suite passed with native parallel workers and the agreed 300-second deadline. Branch-wide checks remain unavailable under D-VAL-01; supplemental configured/target checks above are not branch-equivalent. The owner has retained the production-only strict-Mypy gate for #460; the explicit test-target run is non-gating diagnostic evidence under the prior policy. Do not claim a green branch gate. |
| V460.5 carriers and instruction parity | All 19 workflow-phase carriers are present. A dedicated four-worker selection passed 2/2 real catalog/schema/render/persist tests (`pgmcp://cache/runs/0edb37f9e26d4a2689cd80d10e23221c`); bounded review found no missing carrier or direct phase-meaning contradiction. All eight documented authoritative source/copy pairs are byte-identical on this branch. CY111 corrected the active scaffold instructions against the live contract (F-VAL-05), and independent QA gave GO for that cycle. The sentinel-based tests do not alone certify every natural-language meaning; Validation review still owns the full carrier judgment. |

The eight current byte-identical source/copy mappings are `docs/agents/vscode/copilot/AGENTS.md` → `AGENTS.md`; `docs/agents/codex/AGENTS.md` → `.agents/AGENTS.md`; `docs/agents/codex/reboot.md` → `.agents/reboot.md`; `docs/agents/codex/rules/research.agent.md` → `.agents/rules/research.agent.md`; `docs/agents/codex/workflows/create-issue.md` → `.agents/workflows/create-issue.md`; `docs/agents/codex/rules/qa.agent.md` → `.agents/rules/qa.agent.md`; `docs/agents/vscode/copilot/.github/agents/qa.agent.md` → `.github/agents/qa.agent.md`; and `docs/agents/vscode/copilot/.github/agents/co.agent.md` → `.github/agents/co.agent.md`. The current equality comparison is authoritative for this branch; historical pre-cut-over hashes are not the current comparison basis.

**F-VAL-05 — Resolved in CY111.** The former active guidance passed rejected `name`, cited unregistered `artifact_type` aliases and pointed at the retired registry. CY111 replaced only that scaffolding block in the three authoritative host sources and two mapped active copies. The new text requires the live admitted `artifact_type`, exact `file_name` basename with extension and schema-matching `context`, while identifying `.pgmcp/template_suite/` as the configured source suite rather than a public ID registry. Both source/copy pairs are byte-identical; no stale examples or registry claim remain in the five files. All five `safe_edit_file(validation="enforce")` Markdown preflights passed, with only pre-existing relative-link warnings outside the edited block. Independent QA reviewed the full structured preflight DTOs as producer-provided evidence, independently checked content/parity and warning provenance, and gave CY111.D1/D2 GO on commit `c9ee1e57bc448668d021e21c89ecf280b09c7ab1`. This resolves the documentation defect, not the broader Validation-NOGO.

**F-VAL-06 — Stale aggregate count, with exact path ownership reconciled.** The proposed-new table in `planning-path-ownership.md` contains 288 unique paths; all 288 exist and none overlaps the frozen C/T/A/S registers. The prose value, 279 originals plus one CY059 addition, totals 280 and undercounts the current table by eight. Each of the 288 paths has an exact owner and card link. In the referenced Planning cards, 285 appear under their own owner's `New exact paths` section. The other three have explicit earlier new-path cards and later CY074 ownership amendments: `test_scaffold_public_v3.py` (CY057 → CY074), `fixtures/installed_distribution.py` (CY062 → CY074), and `test_target_startup.py` (CY071 → CY074). Thus the eight-path arithmetic difference is not eight missing or unapproved implementation files. The text does not preserve an immutable 279-path pre-amendment subset, so it cannot identify a unique set of eight later insertions; the remaining defect is the stale aggregate count and its explanation. The owner chose to resolve this in Validation provenance without rewriting pre-implementation Planning. Independent QA has not yet reviewed this reconciliation.

**Structural review risk, not a confirmed violation.** `mcp_server/core/interfaces/artifact_header_reader.py` and `mcp_server/config/schemas/installation.py` import identity/fingerprint types from `mcp_server/services/artifact_identity.py`, which itself imports the service template graph. This outward dependency deserves explicit review against Design's fixed dependency direction and the architecture principles. The passing suite does not decide that architectural question.

D-VAL-01 retains the adapter invocation/selection and native-semantics audit outside #460; D-VAL-02 retains the safe-edit text-model/line-ending design review outside #460. F-VAL-05 is resolved by QA-reviewed CY111; F-VAL-06's path-count provenance and the existing Mypy selection policy are now explained above but await independent Validation assessment. The unreviewed architectural boundary and unavailable branch-gate evidence remain open. Documentation phase must update the repository quality and QA guidance to distinguish configured required selections from optional diagnostic calls; it must not silently change test-Mypy policy or generic adapter contracts. The earlier independent Validation NOGO is recorded below and remains historical evidence pending a new Validation review.


**DOC-VAL-01 — Prevent a future scope-to-gate mistake in this issue's Documentation phase.** Update the repository quality standard and the authoritative host QA guidance, then propagate mapped instruction copies, to require reviewers to name the active workflow/configuration source and exact selection before calling a check mandatory. A wider explicit target call remains diagnostic unless that source explicitly makes it a gate. State the retained issue-72 strict-Mypy production scope and its test-noise rationale, alongside the separately approved ability to request native Mypy on tests. QA must still investigate any diagnostic that demonstrates a concrete violation of another binding contract; a count from a non-gating selection cannot alone produce NOGO. Future strict test-Mypy enforcement needs a separately approved scope, baseline/remediation plan and configured workflow change. Verify guidance against current tool schemas and both host source/copy mappings; this is policy clarification, not a server or adapter change.

### Independent QA disposition — 2026-09-27

The separately invoked `@qa validation-reviewer` returned **NOGO** on producer commit `e65c09942c0a7088119ef3668b5ef08c578c39c7`. QA independently reran the exact branch selection: all four checks were unavailable with WinError 206 / ENAMETOOLONG (`pgmcp://cache/runs/07c960773abc44bf9cdfb52408beb467`, on QA's separate server). QA also directly confirmed F-VAL-05, counted 288 unique existing proposed paths for F-VAL-06, and confirmed the core/config → identity service → template-graph import chain. QA classified the latter as coupling requiring an explicit architectural ownership decision, not a proven runtime defect or automatic breach based only on module names. At that review point QA required an equivalent full-coverage gate disposition, provenance reconciliation for the eight extra proposed paths, correction of the published scaffold guidance, and same-selection baseline comparison or an explicitly bounded quality disposition for expanded test-Mypy diagnostics. Subsequent CY111 QA resolved the scaffold-guidance finding, and the owner has now explicitly retained the existing production-only Mypy gate for #460; QA has not yet adjudicated these later Validation dispositions.

The original producer suite and gate resource caches were unavailable after the subsequent server restart. The current producer reran the full suite and required branch checks and read their complete structured results at the new URIs above. QA's separate task could not read the producer's new suite cache, so the item-level suite result remains producer evidence, not independently certified by QA; no concurrent QA full-suite run was requested. The independent NOGO remains valid on the directly confirmed blockers. This QA decision does not withdraw the earlier CY110 implementation GO and does not reopen D-VAL-01 or D-VAL-02 within #460.

## Follow-up: environment correction and failure diagnosis — 2026-09-26

This follow-up supersedes the environment and cause assessments below; the earlier 2,601-item result remains the historical complete-selection attempt. No complete suite was repeated after dependency correction, so do not recalculate its aggregate pass/fail totals as if all cases were rerun.

### Test environment

The MCP test runner uses system Python 3.13.7. It had Ruff 0.14.13 and no `wheel`; the bundled Ruff requirements specify 0.15.6, and `pyproject.toml` requires `wheel` for package builds. The project's existing `.venv` already held Ruff 0.15.6 and wheel 0.46.3, but that was not the interpreter used by `run_tests`. After the sandbox denied pip network access (WinError 10013), an escalated pip installation placed Ruff 0.15.6 and wheel 0.48.0 in the runner's Python. This changed the local Python environment, not repository files or adapter contracts.

Focused `run_tests` receipts after correction:

| Selection | Result | Cache |
|---|---|---|
| Ruff check and fix native integration modules, `-q --tb=short -n 2` | 33 passed, 3 warnings, 12.59s | pgmcp://cache/runs/b56c361e7cca4d7e8cf99ee190869fe1 |
| Complete installed-distribution integration test, `-q --tb=short -n 0` | 1 passed, 1 warning, 28.04s | pgmcp://cache/runs/c6e143bb841642d080f61657069898f5 |

These directly clear the prior 16 Ruff-version failures and one missing-wheel failure in focused reruns. They do not certify the other former suite failures or every V460.3 migration case.

### Cause and baseline assessment

- **Seven observed lock-related failures have distinct fixture and scheduling causes.** `unit/test_server.py::_bootstrap_workspace_configs` copies the entire active `.pgmcp` into `tmp_path`, including `template_upgrade.lock`; Windows copy raises WinError 33 in two tests. Three pipeline tests create a temporary workspace but call `make_test_server()` without passing its settings, so `Settings.from_env()` boots against this repository. Two real subprocess handshake tests explicitly use this repository. The DI-06 lock is released in `bootstrap_target()`'s `finally` after startup; it is not held for the server's lifetime. In a fresh four-worker integration run, three pipeline tests and one handshake test failed with `template_upgrade_locked` (pgmcp://cache/runs/b92b5fc1768242b2b788e779c6614f8a), while both handshake tests passed when selected serially (2/2; pgmcp://cache/runs/633735ef2edd487caaf1dc868364d978). This supports a shared-workspace scheduling/fixture conflict, not an inherent prohibition on a second server. The two WinError 33 copy cases and all three pipeline cases also passed when selected serially (5/5; pgmcp://cache/runs/4b103ae5aef3410e8ef3af57c3c70013); copying the operational lock remains an unsafe fixture assumption under parallel bootstrap. The tests check fresh proxy/stdio startup and V3 catalog; they do not by themselves prove reconnection of an existing client. A bounded source audit also found eight registration tests in `integration/mcp_server/test_server_tool_registration.py` calling `make_test_server()` without settings, the two audit lifecycle tests in `integration/mcp_server/test_server_lifecycle.py` explicitly rooted at this repository, and a unit validation fixture in `unit/server/test_validate_tool_arguments.py` that defaults its patched workspace to this repository. They were not among the observed seven lock failures, but are subject to the same shared-root bootstrap risk and belong in the fixture review. No lock was deleted or bypassed.
- **Audit logging is a branch regression.** The two failing lifecycle tests are byte-identical to `main` and fail again in isolation (pgmcp://cache/runs/cb2a5a622d9d4ec19b90263587ead87b). Main's `ServerBootstrapper.bootstrap` called `setup_logging(settings.logging.level, audit_log)` and logged `MCP server starting via bootstrapper`. Current `bootstrap_target` neither calls `setup_logging` nor logs any startup message; only `shutdown` still logs. The configured audit path is never opened on this runtime path. Preserve this as a current issue-460 behavior gap rather than treating both tests as obsolete.
- **Stale test path is already designed for retirement.** The unchanged `unit/test_pytest_config.py` asserts that `integration/test_qa.py` exists. It exists on `main` but issue-460 path ledger T107/CY026 explicitly moves its claims to successor tests and retires that file. This single surviving assertion conflicts with the approved retirement.
- **Parallel process lifetime remains unresolved, with a test-oracle ambiguity.** The first full integration partition observed live child PIDs in timeout/crash cases. The nine-case module passed serially (pgmcp://cache/runs/5f24cfe4b51b4122a79d95d95301374d), with four workers (9/9; pgmcp://cache/runs/b3b768e74a60457fb1e9db00f8b86a71), and as part of the execution directory with four workers (39/39; pgmcp://cache/runs/4a90ffd9f1a94e17a64aee7507c3b7be). A second broad four-worker integration run again failed one crash case, with 429/436 passing overall (pgmcp://cache/runs/b92b5fc1768242b2b788e779c6614f8a). The test records child PIDs and opens process handles only after the invocation; [Windows permits PID reuse after exit](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port), so `is_alive(pid)` may inspect a different process under heavy parallel work. This is a plausible cause, not established proof. Capture handles while the original children are alive and compare their signaled state after invocation; that discriminates oracle error from a real child-cleanup failure without changing the approved five-second termination budget.

### Quality provenance

Installing `types-jsonschema` 4.26.0.20260518 in the runner clarified Mypy output. `run_checks(scope="configured", checks=["python_types"])` then checked 184 production files and failed with **7 errors in 5 issue-460-touched files**: three `jsonschema` schema-argument types, one HealthCheckTool decorator variance, one non-exported `ContentInputPreparer`, and two publisher/reader union mismatches (pgmcp://cache/runs/1621b4147ec3432a874f435b08e25e13). Before stubs, this same configured selection showed nine errors, five of them missing-stub reports (pgmcp://cache/runs/be1c0dbb155646d1a1140ff4c03f0ca8). The earlier 1,232-error invocation explicitly selected `mcp_server` plus `tests/mcp_server`; the configured native Mypy scope is production `mcp_server`. The 1,232 result is broad diagnostic debt, not the configured gate result.

With Ruff 0.15.6, a bounded target check of `mcp_server, tests/mcp_server, scripts` passed format on 460 files and failed lint with 61 diagnostics (pgmcp://cache/runs/1684a3432c8a4c709c32888350c55fcf). The prior two formatting findings were version-sensitive and no longer reproduce. All 61 lint diagnostics are in 14 files whose SHA-256 bytes exactly match `main`; their codes are E402 ×50, T201 ×6, ANN401 ×3, ARG002 ×1 and PLC0415 ×1. Compared with main's `pyproject.toml`, this branch removed global ANN401 and ARG002 ignores, accounting for four newly admitted diagnostics in unchanged source. The other rule selections remain, but no native main-branch lint run was executed; source identity alone does not certify baseline pass/fail. On 2026-09-26 the issue owner explicitly chose to remediate all 61 bounded Ruff lint findings within issue 460 instead of recording a baseline exception or deferring that cleanup. This broadens the fix write-set beyond the original runtime/test regressions; the approved stricter native Ruff configuration remains binding.

`run_checks(scope="configured", checks=["python_format","python_lint"])` expanded Ruff's native discovery into archived documentation: format returned unavailable after access denied (os error 5), reporting 469 formatted files; lint reported 191 errors, including archived examples, and a native access warning (pgmcp://cache/runs/bfb9ce644ab842f39d000ce974851cf4). This selection is not equivalent to the bounded directory or required branch check. Add the configured-discovery/access case to the deferred all-adapter selection audit; do not mark any unavailable gate passed.

Current fix candidates are the seven production typing errors, audit bootstrap behavior, the retired-test assertion, the owner-selected 61 Ruff lint findings, and lock-safe test fixtures. The owner's initial 2026-09-26 serial-test choice is superseded by the explicit requirement that future complete suites run reliably with parallel workers. `pyproject.toml` retains native `-n auto`; selecting `-n 0` was diagnostic only. The two handshake tests passed serially (2/2), as did both lock-file copy cases and all three pipeline cases (5/5), but broad four-worker runs reproduced lock failures. A marker alone would not stop the default suite from selecting them; excluding the marker by default would remove their required evidence. Rebuild repeatable bootstrap and handshake tests on per-test isolated workspaces, copy only required stable configuration/template inputs rather than the operational lock, and pass explicit workspace settings to test-server factories. Preserve launcher-config assertions and assess the historical live cut-over and actual client rediscovery separately as V460.3 provenance. The full suite must be rerun with parallel workers after the fixtures change. For the process-lifetime failure, a test that holds original child process handles is needed before changing runtime cleanup: the present post-run PID lookup cannot distinguish PID reuse from a surviving child. Validation remains **FAIL**; independently reviewed closure of V460.1–V460.5 is still pending.


### Proposed issue-460 fix cycles (not yet activated)

These are bounded candidates for a Planning amendment after the Validation findings; they do not silently reopen the completed 105-cycle payload or authorize implementation from the active Validation phase. Each cycle retains its own preimage/recovery point, focused native evidence and independent review. The indicated order limits shared-file rework and leaves complete parallel-suite verification to Validation.

| Candidate | Bounded result and write ownership | Exit evidence |
|---|---|---|
| CY106 — bootstrap and type contracts | Restore configured audit startup logging and resolve the seven production Mypy errors in `mcp_server/bootstrap.py`, `mcp_server/server.py`, `mcp_server/core/interfaces/tool_input_contract.py`, `mcp_server/config/validator.py`, and `mcp_server/core/decorators/input_validation_decorator.py`. No generic adapter-contract change. | Both existing audit lifecycle cases pass; configured production Mypy passes; affected startup/schema tests and file gates pass. |
| CY107 — parallel-safe test workspaces | Replace shared-repository bootstrap in `tests/mcp_server/unit/test_server.py`, `tests/mcp_server/integration/test_pipeline_e2e.py`, `tests/mcp_server/integration/test_target_startup.py`, `tests/mcp_server/integration/test_v3_cutover.py`, `tests/mcp_server/integration/mcp_server/test_server_tool_registration.py`, `tests/mcp_server/integration/mcp_server/test_server_lifecycle.py`, and `tests/mcp_server/unit/server/test_validate_tool_arguments.py`; use the existing `tests/mcp_server/test_support.py` and integration `conftest.py` only for the required shared fixture. Retire the obsolete `test_qa.py` path assertion in `tests/mcp_server/unit/test_pytest_config.py` while retaining its current config-selection proof. | Preserve real proxy/stdio V3 catalog and launcher checks; the seven formerly lock-sensitive cases and additional shared-root cases pass with at least four Pytest workers. No operational lock or whole workspace is copied. |
| CY108 — process lifetime discriminator | In `tests/mcp_server/integration/execution/test_process_stopping.py`, hold handles to the original child processes before invocation completes, then assert those exact handles are signaled afterward. Do not relax the approved five-second stop budget or edit runtime speculatively. | Nine lifecycle cases and the wider parallel integration selection pass. If an original child remains live, record that fact and add a separately scoped runtime repair; a recycled PID alone is not a runtime defect. |
| CY109 — Ruff test imports | Resolve the 50 E402 findings in the ten unchanged test files named by the Ruff 0.15.6 receipt `pgmcp://cache/runs/1684a3432c8a4c709c32888350c55fcf`. Preserve test collection and assertions; no global ignore. | Those exact files pass native Ruff lint/format and their relevant tests pass. |
| CY110 — Ruff production lint | Resolve six T201, three ANN401, one ARG002 and one PLC0415 in `mcp_server/#Archief/supervisor_old.py`, `mcp_server/core/proxy.py`, `mcp_server/managers/phase_state_engine.py`, and `mcp_server/tools/cycle_tools.py`. Preserve proxy stdout/stderr transport bytes and public constructor behavior; no blanket suppression. | Exact files pass native Ruff lint/format and affected proxy/phase/cycle behavior tests pass. |

After these cycles, repeat the complete configured Pytest selection with parallel workers, in disjoint bounded partitions only if the agreed 300-second deadline requires it, and repeat the available branch/configured quality checks. V460.1 structural closure, V460.3 actual client-rediscovery provenance, V460.5 carrier/source parity, and independent QA remain Validation obligations rather than extra implementation cycles. D-VAL-01 native adapter selection/argv limitations and the all-adapter semantic audit stay in deferred follow-up issues; unavailable branch checks cannot be reported as passed.

## Previous complete-selection revalidation — 2026-09-26

This was the producer validation result before the follow-up dependency correction above; it was not independent QA approval. Accepted adapter deferrals are described in [deferred work](deferred-work.md): large native argument lists and native option/result semantics across all nine adapters remain coordination follow-up. They do not reopen generic adapter contracts. The approved lazy cache-guide deviation is provenance reconciliation, not a missing implementation.

### Complete selected suite

All calls used `run_tests`, Pytest 9.0.2, `-q -n 4 --tb=short`. Targets and configured exclusions form disjoint partitions of the previously collected 2,601 items. No failing tests were excluded from this accounting.

| Selection | Passed | Failed | Other | Native duration | Cached result |
|---|---:|---:|---|---:|---|
| targets: tests/mcp_server/unit | 1888 | 3 | 1 XPASS | 88.23s | pgmcp://cache/runs/ef7bc031d1a74b499b08bb8d443020a7 |
| configured; ignore unit and integration directories | 113 | 0 | 1 skipped | 5.33s | pgmcp://cache/runs/ad91721208c54f16a15e9ea3dc3d8460 |
| targets: tests/mcp_server/integration; ignore adapters subdirectory | 426 | 10 | none | 202.04s | pgmcp://cache/runs/0cfa5092dc0d480e9282f1ced51dfc87 |
| targets: tests/mcp_server/integration/adapters | 143 | 16 | none | 95.46s | pgmcp://cache/runs/959642df909140b3bd52e06cc77adeb1 |
| Total | 2570 | 29 | 1 skipped, 1 XPASS | | |

The full configured attempt first reached its explicit 240-second adapter deadline and returned `unavailable/timeout/adapter_deadline_expired`, with `termination_problem=null` (pgmcp://cache/runs/c60499b1de374e6b9af647b7ef805d82). It supplied no partial native counts. The completed partitions used 240-second deadlines except the residual configured partition (90 seconds). This replaces the earlier unknown 120-second client outcome with bounded evidence; it does not turn the timed-out attempt into a pass.

### Failure interpretation

- **16 Ruff conformance failures:** installed Ruff is 0.14.13; assertions require 0.15.6. This is a validation-environment mismatch, not evidence that all sixteen native behaviors are broken. No dependency was silently upgraded and no assertion was relaxed.
- **Seven live-workspace lock failures:** two unit tool-registration tests copy the active `.pgmcp/template_upgrade.lock` and receive WinError 33; three pipeline tests attempt bootstrap against the occupied template-upgrade lock; two real stdio handshake tests subsequently time out after their child server exits with `template_upgrade_locked`. These are concrete fixture/workspace-isolation concerns. They are distinct from workspace traversal exclusions and deferred long argv handling.
- **Two audit lifecycle failures:** startup creates no expected `test_audit.log`; shutdown then cannot read that file. Tests: `integration/mcp_server/test_server_lifecycle.py`.
- **One obsolete path assertion:** `unit/test_pytest_config.py::test_qa_tests_relocated_to_integration_directory` expects missing `integration/test_qa.py`.
- **One installed-distribution prerequisite failure:** wheel construction stops at `ERROR Missing dependencies: wheel`. Installed catalog/entrypoint assertions are therefore not reached; this is not proof of a malformed wheel.
- **Two process-lifecycle failures under parallel load:** timeout/crash cases observed a child still alive at `test_process_stopping.py:180`. A focused rerun of that entire module with `-q --tb=short -n 0`, deadline 90 seconds, passed all nine tests in 13.92s (pgmcp://cache/runs/5f24cfe4b51b4122a79d95d95301374d). Keep this as an unresolved timing/isolation finding, not a confirmed deterministic process-termination defect and not an adapter deferral.

Warnings, the XPASS, and noisy restart-test stderr remain in the full caches. Native exit zero for the residual partition is not a claim of silent stderr.

### Quality checks

The exact branch call again could not launch its four native checks: WinError 206 for Ruff/Mypy and ENAMETOOLONG for Pyright (pgmcp://cache/runs/e1cb79d60bd348808cf0425f43aa5170). This is the accepted D-VAL-01 deferral, not a passing branch gate.

Diagnostic targets `mcp_server, tests/mcp_server, scripts` yielded:

- Ruff format: two files would change, 457 already formatted. Files: `unit/config/test_contracts_loader.py` and `unit/services/test_artifact_identity.py`.
- Ruff lint: 61 diagnostics, including 50 E402 import-order findings in tests, six T201 print findings, and five typing/import findings. Cache: pgmcp://cache/runs/b7d8048ed53140619c191a161262bf20.
- Pyright: 462 files, zero errors/warnings, 31.19s. Cache: pgmcp://cache/runs/af35264dddd349e68b4220f61a6d3f16.
- Mypy initially stopped after six errors: missing jsonschema stubs and duplicate module identity for `scripts/build_package.py` (pgmcp://cache/runs/0b45ac5b34e54532822bf3de0bb3e0ad). Repeating with only `mcp_server, tests/mcp_server` completed: 1,232 errors in 126 of 461 checked files, nine production diagnostics and 1,223 test diagnostics (pgmcp://cache/runs/0d9e2905575d4eccb4d37118f68ca598).

Directory discovery differs from explicit branch-file semantics, including native exclusions and archived paths. These are useful diagnostic results, not an equivalent branch gate or proof that every diagnostic is introduced by #460. Baseline attribution remains open; accepted adapter deferrals do not automatically waive native findings.

### Obligation assessment at the prior run

| Obligation | Current assessment |
|---|---|
| V460.1 | Partial: all 79 legacy template paths absent, C084 docstring-only; bounded active-code search finds no retired runtime imports or generic executor tool coupling. Complete 126/151/79/57 semantic closure and review of every new path are not certified by path presence alone. |
| V460.2 | Substantial fresh public/consumer/native coverage; aggregate not passing, notably Ruff version mismatch and parallel lifecycle failures. Adapter repairs remain deferred. |
| V460.3 | Not established: fresh installed-distribution proof blocked by missing wheel; two real configured-workspace handshake tests hit the active lock. Other renewal/recovery tests are included in the completed integration partition. |
| V460.4 | Complete selected-suite execution obtained, but failures remain. Branch invocation limitation is deferred; diagnostic checks do not establish a green gate. |
| V460.5 | Fresh unit carrier tests passed, including nineteen variants and rendered/persisted carrier semantics; all eight documented source/copy pairs are SHA256-identical. Mocked consumer checks are not counted as native-tool proof. |

No production repair or new strategy change was made during revalidation. Non-deferred findings and evidence gaps above need disposition before closure. Independent QA review is requested against this current assessment, the full cached diagnostics and the accepted deferral boundaries.

## Historical obligations and initial assessment

The following obligation details and later dated investigation sections retain the earlier record. Their execution statuses are superseded by the current revalidation above.



### V460.1 — exact source closure and architecture review

**Evidence:**

- [Exact path ledger](<planning-path-ownership.md>)
- [Retirement and CY105 evidence](<planning-rollout.md>)
- [Test architecture](<design-test-architecture.md>)


**Outcome:** PARTIAL. Read-only closure inspection confirms all 79 A001–A079 legacy template paths absent, plus 47 C-register paths with retirement dispositions absent. C084 survives only as an empty package docstring, consistent with lifecycle-export removal. The 126/151/79/57 ledger and 279 proposed paths are not thereby fully behaviorally certified. Full retained-assertion and architecture closure remains open.



### V460.2 — native, consumer and real public evidence

**Evidence:**

- [Native Ruff conformance](<../../../tests/mcp_server/integration/adapters/test_ruff_checks.py>)
- [Native Pytest conformance](<../../../tests/mcp_server/integration/adapters/test_pytest.py>)
- [Public scaffold](<../../../tests/mcp_server/integration/test_scaffold_public_v3.py>)
- [Public edit](<../../../tests/mcp_server/integration/test_edit_public_v3.py>)
- [Cache fidelity](<../../../tests/mcp_server/integration/test_cache_fidelity_v3.py>)


**Outcome:** PARTIAL. Source inspection confirms direct native subprocess comparisons, isolated workspaces and public persistence/cache assertions, rather than only a mocked executor. No fresh aggregate native/public passing result was returned in this session. Live schema discovery succeeded; that is not certification of every artifact contract.



### V460.3 — fresh installed distribution, migration, recovery and client rediscovery

**Evidence:**

- [Installed distribution test](<../../../tests/mcp_server/integration/test_installed_distribution_v3.py>)
- [Installed startup and handshake](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Activation recovery](<../../../tests/mcp_server/integration/test_template_activation.py>)
- [Renewal](<../../../tests/mcp_server/integration/test_renewal_cli.py>)
- [Historical rehearsal](<rollout-rehearsal.md>)


**Outcome:** UNPROVEN for the current validation run. Existing tests build an offline wheel, separately install it, compare packaged bytes and assert import origins, real MCP handshakes and recovery. Their presence and historical rehearsal do not establish a fresh successful execution after all later edits.



### V460.4 — one full suite and branch gates

**Evidence:**

- [Branch check operation](<pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777>)


**Outcome:** BLOCKED. The workspace test call timed out at the MCP client boundary after 120 seconds without a result URI. Its completion and pass/fail counts are unknown. All four branch checks report unavailable/execution_error, with run_status=incomplete. Operation success=true means the operation returned facts, not that checks passed.



### V460.5 — nineteen workflow carriers and host source/copy consistency

**Evidence:**

- [Workflow design](<design-workflow-documentation.md>)
- [Host mapping](<rollout-host-input.md>)
- [Carrier tests](<../../../tests/mcp_server/unit/config/test_contracts_loader.py>)


**Outcome:** PARTIAL. Bounded read-only review found all eight direct source/consumer pairs byte-identical. Existing tests address nineteen carrier meanings and render four phase artifacts, with separate family integration coverage. Fresh passing execution and full semantic closure remain unproven.





## Evidence


### Branch-wide required checks

Configured python_review selected python_format, python_lint, python_types and python_pyright. All four returned status=unavailable, reason=execution_error, adapter exit code=3, evidence=null. Removed-target inventory contains 266 entries.

**Sources:**

- [Complete cached check operation](<pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777>)


**Invocation:** run_checks(scope="branch", timeout_seconds=300)



**Observed Result:** incomplete




### Exact native launch failures

python_format/python_lint: Ruff launch failed: [WinError 206] De bestandsnaam of -extensie is te lang. python_types: Mypy launch failed: [WinError 206] De bestandsnaam of -extensie is te lang. python_pyright: Pyright execution failed: spawnSync C:\Program Files\nodejs\node.exe ENAMETOOLONG. Observed native identities: Ruff 0.14.13, Mypy 1.19.1, Pyright 1.1.408. All adapter package versions 1.0.0; fingerprints Ruff Ny0reoegAdrc-QS5, Mypy Qz4DehR5ukmWj2cr, Pyright UC15y_s27GyMRNMP.

**Sources:**

- [Cached native failure facts](<pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777>)
- [Ruff process construction](<../../../mcp_server/bundled_adapters/ruff/check.py>)
- [Mypy process construction](<../../../mcp_server/bundled_adapters/mypy/check.py>)





### One workspace-wide test attempt

The tool returned: timed out awaiting tools/call after 120s. No run ID/cache URI, test counts or completion acknowledgement were returned. The requested adapter timeout does not override the observed client transport limit. No second full run was started; native process completion/termination is not inferred.

**Sources:**




**Invocation:** run_tests(scope="workspace", timeout_seconds=1200)



**Observed Result:** UNKNOWN — missing completion evidence




### Structural removal and retained helpers

A001–A079 absence counts by CY094–CY104: 9/11/8/6/6/6/7/6/6/5/9. T004 artifact_test_harness and T106 fake_pytest_runner are absent. Hidden-aware search of active server/tests/template-suite/config/root project configuration found no retired dotted-module imports, get_template_root or old tier/pattern references. tests/conftest.py retains workflow_fixtures and suite_roots and selects template_suite. make_project_manager remains used by project tools/manager/readback tests. This bounded delegated review was findings-only and did not run tests.

**Sources:**

- [Retirement ledger](<planning-path-ownership.md>)
- [Conftest](<../../../tests/conftest.py>)
- [Retained test support](<../../../tests/mcp_server/test_support.py>)





### Live public discovery and server availability

scaffold_schema(validation_report) returned the current closed content schema and its schema attachment. A subsequent health_check reported healthy, process 21540, win32, version 2.0.0. Server health is not a test-job status query or validation verdict.

**Sources:**

- [Schema result](<pgmcp://cache/runs/25647f89bbbd4bd88ae197b061d8866f>)
- [Health result](<pgmcp://cache/runs/02d14e2ef1c74944802f47acaffc4ef2>)







## Demonstration

Observed end-to-end fallback: live schema discovery and the real branch check operation returned structured facts. Full behavioral demonstration remains unavailable. Existing installed-distribution/startup/activation tests are the intended current-source demonstration entry points; no fresh success is inferred from inspecting them.



## Preservation

The Approved Strategy retains the explicit V3 clean break, separate check/test/fix roles, generation fingerprints distinct from renewal checkpoints, enforce/report persistence and independent native evidence. No compatibility bridge, weakened assertion or changed check configuration was introduced. Structural absence supports planned cleanup only; all 19 invariants and 23 expected results remain subject to complete behavioral and architecture evidence.



## Containment

Only this validation report and the existing phase-transition state are intended for the validation commit. Startup status contained .pgmcp/installation.json, .pgmcp/template_upgrade.lock and a retained template backup tree among 136 untracked files; these operational artifacts are excluded from the commit.



## Failures

- F-VAL-01: Required branch checks could not launch native tools with the current branch target selection on Windows. Repair is explicitly deferred outside #460 as D-VAL-01 below, including an audit of all shipped adapters. This remains an observed evidence limitation, not an issue-460 implementation task; no blanket batching workaround or equivalent coverage is assumed.
- F-VAL-02: Full-suite completion evidence is unavailable after the MCP client timeout. Determine the existing run's fate or a supported durable-result route before authorizing/repeating a replacement run.



## Caveats

- This FAIL is a producer validation outcome because required proof is missing, not an independent QA GO/NOGO.
- CY105 previously recorded 14 Mypy errors in unchanged lines; that historic failure was not resolved or freshly re-established by the unavailable branch run.
- Native Ruff source conformance asserts 0.15.6 while the live check adapter reports 0.14.13. This is an observed environment-version discrepancy, not a claimed test failure.
- The all-cycle hand-over is represented by distributed cycle evidence. No separate final implementation QA verdict was found in the inspected issue-local files.
- Full architecture/retained-test auditing stopped short of certification after the execution blockers; no additional temporary tests or implementation changes were added.



## Risks


### Treating operation success or structural absence as behavioral completion would hide unavailable checks and missing tests.

Keep V460.1–V460.5 explicitly incomplete until required evidence is available; independent QA reviews exact results.


**Consequence:** Validation cannot be closed or progressed on this evidence.





## Deferred Work


### D-VAL-01 — Audit native execution robustness across all shipped adapters

**Disposition:** Deferred outside issue #460 by explicit owner decision on 2026-09-24. Coordination owns creation and triage of a separate issue; no follow-up issue has been created here.

**Suggested issue title:** Audit and harden shipped adapters for large selections and native invocation limits.

**Confirmed trigger:** F-VAL-01: the branch selection becomes one oversized native command line in Ruff, Mypy and Pyright, producing WinError 206 / ENAMETOOLONG. See the cached branch operation and the command-length diagnosis below.

**Follow-up scope:** Inventory every shipped adapter package and each implemented check/test/fix role. Review selection-to-native invocation, platform command/argument limits, quoting and path handling, large selections, native discovery semantics, and actionable failure evidence. Establish applicability per adapter instead of assuming every adapter has the same defect. Where internal batching or alternative transport is considered, prove preserved cross-file semantics, complete coverage, aggregate outcomes and diagnostics, lifecycle limits, and fix-role mutation/failure behavior. Exercise representative boundary cases on supported platforms.

**Contract boundary:** Preserve the existing generic role request/response contracts as the starting constraint. Keep native-tool execution knowledge inside adapters; do not make agents or generic orchestration calculate tool-specific command limits. No contract expansion or universal batching design is approved by this deferral.

**Issue-460 consequence:** No adapter repair or additional implementation cycle for D-VAL-01 belongs to this issue. The observed unavailable branch checks remain recorded validation evidence; deferring the repair does not convert them into passing checks or by itself close V460.4. Missing full-suite completion evidence remains a separate finding, not part of this deferral.

**Coordination hand-off:** Create the separate issue from this notice and link it back here. Future Research must distinguish confirmed defects, equivalent risks in other adapters, and tool-specific non-applicability; define acceptance evidence before choosing remedies.





### D-VAL-02 — Reconcile the safe-edit text model and line-ending semantics

**Disposition:** Deferred outside issue #460 by explicit owner decision on 2026-09-27 after independent QA GO for CY110 D1–D4. Coordination owns triage and creation of a separate PGMCP issue; no follow-up issue has been created here.

**Suggested issue title:** Unify safe-edit text representations, edit planning, and line-ending invariants.

**Observed trigger:** CY110 preserved original CRLF/LF/CR terminators while retaining universal-newline matching. The reader now exposes both normalized text and source-preserving text; targeted edits reconstruct physical content from logical patches. The CY110 no-op correction was necessary because a logically identical replacement could otherwise alter mixed line endings. Current integration coverage also explicitly expects identical persisted bytes with `content_changed=True` when an explicit CRLF replacement is compared with a normalized LF original. This is evidence of a semantic choice that needs review, not a new proven violation of the approved CY110 contract.

**Follow-up scope:** In Research, inventory all four safe-edit operations and direct consumers; decide the exact meanings of logical text, physical content, `content_changed`, identical edits, explicit line endings, and replacement spans in mixed-terminator files. Record compatibility and migration strategy per affected boundary before Design. In Design, compare a single immutable source-span edit plan with alternatives; retain one original read, matching cardinality, validation/write-byte identity, the original-byte race guard, and exact whole-file rewrite unless Research explicitly approves a change. In implementation, remove redundant or divergent construction routes where justified and verify operation-wide invariants across LF, CRLF, CR and mixed sources, search windows, regex backreferences/zero-width matches, no-op and explicit rewrite. Tests must prove observable behavior, not merely mirror helper branches.

**Issue-460 consequence:** CY110's independently reviewed correction and current public contracts remain in force. This deferral neither weakens the Validation obligations V460.1–V460.5 nor authorizes a contract change or another issue-460 fix cycle. Validation should report any newly observed concrete failure separately; it must not relabel a failing obligation as deferred design work.

**Coordination hand-off:** Create a separate issue from this notice and link it back to [the CY110 evidence](planning-rollout.md#cy110-completion-evidence-d1d4-2026-09-27), [the approved line-ending amendment](design-mutation-validation.md#cy110-line-ending-preservation-amendment-2026-09-27), and the [deferred-work register](deferred-work.md#deferred-work-notice-safe-edit-text-model-and-line-ending-semantics). Deduplicate against existing safe-edit work before assigning scope.

## Related Documents

- [Planning](<planning.md>)
- [Research strategy and invariants](<research.md>)
- [Design](<design.md>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)


## Investigation addendum — 2026-09-24

### F-VAL-03 withdrawn: documented intentional refinement

The prior classification missed [CY011.D1/D2](planning-execution.md#cy011): it explicitly records the **session-approved refinement of 2026-09-17**, with a short budget-triggered guide reference and the packaged resource owning unchanged window/integrity/safe-retry instructions. [Host preparation](rollout-host-input.md#22-contractual-separation-and-lazy-cache-discovery) deliberately implements lazy discovery. The owner has also explicitly reconfirmed that this is intentional. This is not an implementation blocker. Stale generalized CY069/hub wording and unavailable historical fresh-agent proof are documentation/provenance reconciliation, not a reason to replay cutover.

### Scope and command-length diagnosis

The read-only current branch selection at HEAD 625b29a4 contains 593 existing paths, including 136 nonignored untracked files, with 266 deleted paths recorded separately. Only 217 selected paths have a .py extension. The longest individual absolute path is 128 characters. Reconstruction with the local interpreter and Python Windows list2cmdline yields 41,939/41,946/41,917 UTF-16 units including terminating NUL for Ruff format/lint and Mypy. These are reconstructed argv measurements, not an intercepted native process command; the live adapter's PATH-selected interpreter can differ. All exceed CreateProcessW's 32,767-unit command-line limit. With untracked paths excluded analytically, the reconstructed Ruff lint command is 28,351 units. No files were removed or ignored to obtain this comparison.

GitAdapter.get_branch_changes includes tracked merge-base/index/worktree changes and nonignored untracked paths. ScopeResolver converts existing paths to absolute paths; adapters append all targets to one native argv. Therefore ignored-by-native extensions still consume command-line space before the native process can filter them. This is native-child launch failure, not a long individual filename, MCP payload limit, or test timeout. The measured backup/untracked contribution materially pushes the current selection past the Windows limit. There is no automatic native argv batching or response-file route in the inspected implementation.

### Workspace traversal and Windows access failures

Workspace passes one root path; configured passes no explicit native targets. Consequently workspace Pytest bypasses testpaths selection and recursively discovers from the root under native recursion rules. Pytest does not inherit Git ignores. Current norecursedirs does not exclude all local scratch locations.

A diagnostic-only collection run with scope=workspace, args python_tests=[--collect-only,-q,-n,0], timeout_seconds=90 returned native exit 2: **2,602 tests collected, five collection errors in 13.52 seconds**. Full cached tracebacks name:
- .pytest_cache_ci
- .tmp/pytest-of-1Voudig
- temp/cy086-ruff
- temp/cy087-ruff-after
- temp/cy087-ruff-baseline

Each raises PermissionError/WinError 5 while os.scandir enumerates a directory. This identifies denied filesystem reads, not a generic timeout. Resource: pgmcp://cache/runs/e6c5f7f5e27b42bdbb830ac813601599.

With the same collection options but scope=configured, native discovery used testpaths=tests/mcp_server: **2,601 tests collected, exit 0, in 2.13 seconds**. Resource: pgmcp://cache/runs/eb1ed8a32dd749e09e94dc42f86c2a10. This proves successful collection only, not passing test execution; it does not retroactively determine the earlier timed-out run.

Ruff format also reproduces access errors when targeting .pytest_cache_ci, .tmp and temp separately (resources 2161c16436354c689bb93c36a48e7ade, 81d6da3976014585b4ca6971a1adbf40, 3ba7e8d9532a472a9284662c00c20c3f). The native Ruff diagnostic omits the exact denied child path. Targeting mcp_server/docs/scripts instead returns 184/6/1 already-formatted files. Targeting tests reports two actual formatting differences and 276 already-formatted files, without access errors. The two differences are test_contracts_loader.py and test_artifact_identity.py. Disabling Ruff caching does not remove the workspace access failure (9a35c9cbb205441284079c6cfd4311a7).

### F-VAL-04 — Ruff diagnostic classification changes under verbose output

The same workspace formatting failure without verbose yields execution_error and the access-denied message. With --verbose it yields invalid_configuration and a benign first debug line about using pyproject.toml, although the native evidence still ends in the access-denied error. Source: mcp_server/bundled_adapters/ruff/check.py _message and _classify_native_failure. The latter scans all output for broad markers including configuration; the former can select the first debug line. This is a concrete error-classification/message defect, distinct from cache loss. Resource: pgmcp://cache/runs/b43a3af617c74b62ba0f0d5ea13859b9 (complete operation 177,822 characters, fully read through windows).

### Cache contract and actual retention

[DI-05 diagnostic capture](design-execution-adapters.md) and [Shared presentation boundary](design-shared-contracts.md) require native evidence, typed error details and ProcessCapture in the complete operation cache, not inline dumps. Formal adapter stdout is limited to 8 MiB; supplemental adapter stderr retains at most 256 KiB with explicit head/tail truncation. Accepted JSON stdout intentionally has null capture fragments: the decoded role response is stored instead. Native stdout/stderr belongs in evidence.data.

For WinError 206 the native child never started, so no native stdout/stderr exists: the OS exception is retained in message and evidence is null. For actual native failures, the inspected cache contains diffs, complete available native error text and Pytest tracebacks. The verbose Ruff operation and workspace collection operation were reconstructed through all cache windows. No confirmed cache-retention contract violation was found. The producer's earlier summary failed to explain available evidence sufficiently.

The adapter uses subprocess capture_output for its native child and emits its formal response only after completion. Thus native progress is buffered inside the adapter, not streamed as cache entries; the server publishes the final DTO after tool execution. A client timeout before receipt may leave no delivered resource URI. No background-job handle or timeout-recovery lookup is exposed by the current run_tests tool.

### Timeout history and runtime identity

.codex/config.toml is Git-ignored. Its local creation and last-write timestamps are both 2026-09-23 08:00:24 UTC. Available session history first confirms this exact workspace configuration with tool_timeout_sec=120 at 2026-09-23 17:59:57 UTC. These facts establish it predates this validation; they do not prove the exact original edit or author. The producer made no timeout-config change.

The original full-suite request already specified timeout_seconds=1200, while the MCP client failed after 120 seconds. Those are separate budgets. Raising the adapter budget alone cannot address the client deadline; nor can either timeout repair the now-confirmed root-scope collection failures.

Adapter manifests request executable=python; bootstrap resolves it through shutil.which, not automatically the server's sys.executable. The observed live Ruff version is 0.14.13 and Pytest is 9.0.2; cache traces use the system Python313 installation. The server launcher being a venv Python does not itself establish native adapter environment parity.

### Remaining work

D-VAL-01 length-safe native execution and the all-adapter robustness audit are deferred outside issue #460 for coordination to create a separate issue. Other findings remain under discussion: misleading Ruff failure classification, the intended full-suite native discovery boundary, client/adapter timeout budgets and native environments. No remediation of those other findings is selected by the D-VAL-01 deferral. No production files, ACLs, scratch directories, dependencies or client configuration were changed.

## Refactor / Validation Hand-over

### Scope

Partial validation of V460.1–V460.5. Production repair, native environment changes and phase progression excluded.

### Deliverables

- [Validation report](validation.md)
- [Planning and validation obligations](planning.md#validation-and-documentation-deliverables)
- [Structural ownership ledger](planning-path-ownership.md)
- [Native check failure evidence](pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777)

### Evidence

One workspace test attempt returned only a 120-second MCP timeout. One branch check run returned four unavailable execution errors. All 79 legacy template paths were absent in the bounded structural review; eight mapped host source/copy pairs matched. No complete behavioral or architecture verdict is claimed.

### Open Work

D-VAL-01 / F-VAL-01: adapter launch robustness is explicitly deferred outside #460; coordination must create a separate issue covering all shipped adapters and link it to this notice. The unavailable branch-check evidence remains visible. F-VAL-02 missing full execution completion and the separately diagnosed root-scope collection failures, plus F-VAL-04 misleading Ruff classification, remain under discussion. F-VAL-03 is withdrawn by the investigation addendum. Full V460.1–V460.5 closure and independent review remain open. Native Ruff version discrepancy and historical Mypy failures remain recorded above.

### Review Request

Review requested. Resume an independently invoked `pgmcp-qa` validator review before deciding the bounded remediation and resumption route.


## Owner-approved validation configuration correction — 2026-09-24

The owner explicitly authorized fixing point 2 inside issue #460: validation workflow instructions must use run_tests(scope='configured') for the complete native-configured suite, while explicit directories/files remain scope='targets'. The five prescribed test invocations in contracts.yaml now use configured; full-suite wording is aligned. Explicit workspace root selection remains available for deliberate native discovery from the root. No adapter contract or selection implementation changes.

Pytest norecursedirs replaces its defaults rather than extending them. Restore all native default exclusions, retain repository-specific exclusions, and exclude temp/tmp scratch directories. The restored .* excludes hidden cache, temporary and template-backup trees. testpaths remains tests/mcp_server; no marker filters or narrower testpaths were introduced. This addresses traversal selection, not the underlying Windows ACLs.

YAML/TOML edits use safe_edit_file(validation='report') because no artifact validation profile is selected for these files (enforce returned validation_blocked with selected_source=none and selection_reason=absent). Verification uses existing contract/config tests and native collection. This bounded owner-authorized configuration correction does not reopen the deferred D-VAL-01 adapter robustness implementation scope.

### Verification of the approved scope/configuration correction

- run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_contracts_loader.py', 'tests/mcp_server/unit/config/test_contracts_config.py', 'tests/mcp_server/unit/test_pytest_config.py'], args={'python_tests': ['-q', '-n', '0']}, timeout_seconds=90): 58 passed, 1 failed. Both contract test modules passed. The failure is test_qa_tests_relocated_to_integration_directory, asserting that the absent tests/mcp_server/integration/test_qa.py exists; it is unrelated to discovery exclusions or scope instruction changes and remains open. Cache: pgmcp://cache/runs/a7351c2facea434b91e706eae790d5ca.
- run_tests(scope='configured', args={'python_tests': ['--collect-only', '-q', '-n', '0']}, timeout_seconds=90): 2,601 tests collected, exit 0, 2.57 seconds. Cache: pgmcp://cache/runs/e84ab6dbd3ec4386ad0e2160d51e436d.
- Identical collection options with scope='workspace': 2,601 tests collected, exit 0, 2.25 seconds; the five former access-denied collection errors are absent. Cache: pgmcp://cache/runs/01900aa049184f14949034cddfeec15c.
- Both collection resources were read completely in contiguous windows. Successful collection does not establish full-suite execution or passing tests. The configured collection count is unchanged from the pre-edit 2,601 baseline; root collection previously found 2,602 plus five errors.

After the supported server restart, get_work_context returned the updated configured-scope validation instruction (pgmcp://cache/runs/b4e49d3d05cc4526b77de42a93bdad91), proving the active server loaded the revised contract. Independent review remains requested; full-suite completion, deferred adapter launch robustness and other unresolved findings remain separate.

## Timeout provenance and authorization investigation — owner scope refinement, 2026-09-26

**Owner-provided historical evidence:** Before issue #460, run_tests calls could run longer than 120 seconds. This is an explicit regression baseline to investigate; it is not yet independently reconstructed from old run receipts. The owner does not recall authorizing introduction of the observed 120-second client limit. Do not infer unauthorized implementation or an author solely from this discrepancy.

**Required investigation:**
- Reconstruct the earlier successful long-running call path: host/client, configuration, native execution budget, elapsed time and returned evidence. Distinguish the prior run_tests timeout parameter from a whole MCP-call deadline.
- Trace the introduction of .codex/config.toml tool_timeout_sec=120 through available local configuration/session history and setup scripts. Git ignores this file; timestamps and first observed reads are not proof of writer, approval or introduction time.
- Map each budget independently: native tool, PGMCP adapter invocation, bounded termination, complete multi-adapter tool operation and MCP client/transport. Identify owners, defaults, overrides and aggregate overhead.
- Trace Research/Approved Strategy, Design, Planning, implementation commits and user authorization for each changed boundary. A document labelled human-approved is a claim to trace, not independent proof that a separate client limit was approved.
- Establish actual client timeout/cancellation behavior, process-tree termination, late result handling, cache publication/discoverability, and what the agent/user can know before retrying. Do not infer the fate of the original interrupted run from code inspection alone.
- Extend the provenance audit to adjacent issue-460 execution/client settings and materially changed defaults to identify other unapproved decisions, distinguishing approved changes, missing provenance, implementation departures and host-only configuration.

**Owner requirement:** Tool deadlines are acceptable when intentionally designed with clear PGMCP behavior and correct failure/result handling. Merely increasing a client value does not close the finding or authorize a new asynchronous execution design. No timeout setting or execution code is changed by this investigation refinement.

### Bounded timeout follow-up — 2026-09-26

The owner requested a focused follow-up rather than a separate broad investigation. Read-only local session search found tool_timeout_sec=120 already present in the S1mpleTrader PGMCP v2 Codex workspace configuration on 2026-08-17 at 14:55:30 UTC (session 01a01037-51bb-7802-b314-022c6d29681d, explicit read of C:/1Voudig/99_Programming/ST/.codex/config.toml). This is a different workspace: it proves the value was used before the current adapter rollout, not that today's pgmcp file was copied from it or who chose it. In the inspected available history, the current pgmcp file is first observed on 2026-09-23 at 17:59:57 UTC; no attributable write or specific approval was found. No unauthorized issue-460 introduction is established.

The legacy RunTestsInput at c8f46c6a^ already exposed timeout=300; PytestRunner passed that value to subprocess.run. The current python_tests binding also uses 300 seconds. The 120-second client boundary is distinct from either server-side default. A client/workspace configuration difference is a plausible explanation for earlier long calls, not a demonstrated reconstruction of those calls.

Current source inspection: the proxy forwards ordinary JSON-RPC traffic and has no 120-second per-call timer; the shared adapter runtime types deadline expiry, attempts bounded process-tree stopping, and returns cancellation observations. Existing real-process tests cover timeout and cancellation stopping, including a Pytest xdist descendant test. These tests were inspected, not rerun. The server publishes the operation cache only after tool.execute returns; no early recoverable job handle is supplied. Therefore proper server-side timeout handling does not guarantee receipt of a final result after an earlier client deadline. No observed cancellation delivery or final fate of the original 120-second run is established by this source review.

Disposition: treat this as an unaligned host/client deadline and unresolved end-to-end completion evidence, not a proven missing generic timeout implementation. A bounded remedy should align the host deadline with the selected PGMCP execution budget plus termination/response overhead (and cumulative work when multiple bindings run), then verify a representative call beyond 120 seconds with an observable final result. Do not infer support for arbitrary long calls or cancellation delivery from configuration alone. No settings changed, no long run started, and no unrelated scope/authorization audit was performed.

### Owner decision — client timeout, 2026-09-26

The owner ended the historical provenance investigation and explicitly selected tool_timeout_sec=300 for the local Codex phase_gate_mcp connection. The setting was changed from 120 to 300 in the Git-ignored .codex/config.toml using safe_edit_file(validation='report'). Runs expected to exceed 300 seconds should be split into bounded selections with recorded coverage rather than extending the deadline again. This session refinement permits partitioned validation evidence without dropping suite coverage; prior instructions demanding one indivisible full-suite invocation do not override this owner decision.

The native test binding remains at 300 seconds; equal client and adapter budgets do not guarantee delivery of an adapter timeout result after cleanup. Keep actual planned calls comfortably within the client limit. The new client configuration value is verified on disk; activation in the already-running Codex connection is not established by editing it or by restarting only the PGMCP server. No long test run or end-to-end timeout certification is claimed. Earlier missing execution evidence remains unknown, not retroactively passing.
