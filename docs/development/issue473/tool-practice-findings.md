<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Current Tool Practice Findings

**Status:** Validated correction; deferred findings ready for coordination
**Version:** 0.4
**Last Updated:** 2026-10-04

This assessment describes current practical behavior, with no pre-460 score or assumed regression attribution. Root issue473 template defects are corrected within their planned cycles; unrelated tool findings remain reproduction evidence for coordination. Exact actual scaffold requests, outputs and complete factual rows are in [first-output evidence](first-output-evidence.md).

## Observed working routes

Public schema discovery exposes complete resolved contexts and source fingerprints. Public scaffold enforces Python/TypeScript content syntax and current Markdown/commit profiles before create-only persistence. Every C_SHARED request has success, written, policy/status and individual native rows recorded separately.

Safe edit of production/fixture Python runs Python syntax preflight (Python 3.13.7). Jinja-source edits under report mode return written=true, validation_status=not_executed, profile=null, checks=[]: this is an explicit routing limitation, not admission proof. Real admission/render tests and refreshed public scaffolds supply that separate evidence.

Run tests preserves configured arguments and full native outcomes; the initial C_SHARED subset reported 183 passed accurately. Negative native results were retained and exposed two omitted filter-registration consumers. Run checks preserves independent format/lint/Mypy/Pyright outcomes; Pyright correctly detected protected-member access in the initial registration implementation. Existing pure filters were moved into the same engine module so the shared registration no longer crosses private class members. A subsequent check passed both typing rows; the later C_SHARED fix route below records the source-formatting correction.

## F1 — Markdown preflight misreads angle-bracket destinations

Status: reproducible current adapter finding; deferred tool triage. During C_SHARED the PR filled scaffold's explicit relative target is `../../../.pgmcp/template_suite/pr/context.schema.json`, an existing source file. The shared link macro renders a valid angle-bracket Markdown destination. Native markdown_body status is passed but warning says:
“Broken link: '<../../../.pgmcp/template_suite/pr/context.schema.json>' not found at C:\\temp\\pgmcp\\.pgmcp\\temp\\.pgmcp\\template_suite\\pr\\context.schema.json>”.

Reproduce: replay the exact `c1.pr.representative.md` request from the evidence document into a fresh three-level directory, validation=enforce. Expected assessment resolves the destination without Markdown delimiter characters. Actual assessment uses the '<' and '>' as path text. Adapter identity: markdown_preflight 1.0.0, fingerprint v0NjYjqP55u7eH7r; Python 3.13.7. File is persisted and the warning remains in the full JSON evidence row. Impact: noisy/incorrect link diagnostics on template-generated valid link syntax. This run proves one local destination case, not all Markdown grammar behavior or historical regression. The broader filled generic-document case also warned but its caller target may independently be stale; do not use that as sole proof.

Safe workaround for authored reports: ordinary parenthesized relative destinations. Do not rewrite the link macro's value/syntax contract or relax checks as an unrelated fix in #473. Later coordination should reproduce and classify the parser boundary.

## F2 — Large result reads require the supported cache windows

Status: practical client/read-boundary friction, no unsupported product-fault claim. The complete resolved Python class schema is 106874 Unicode codepoints. An ordinary resource read was incomplete and could not be parsed as JSON. The documented `?offset=...&limit=5000` route returned contiguous windows with stable run ID, length and SHA-256; assembled content verified against e8003eec64bf4016a4d07908e26fd7c563949324e4e699c1f9b1bff98846ff53 and parsed successfully.

Impact: agents must implement/observe bounded resource reading for resolved schemas and verbose native results. Exact window-reading behavior is documented by `pgmcp://docs/cache-reading`; this supported path worked. Cache lifetime is transient and fingerprints must be refreshed after a server restart. Preserve durable factual evidence before cache loss. The initial collector independently verified the assembled schema hash. Later root collections check contiguous windows, stable receipt hashes and full lengths before parsing, without independently recomputing every receipt SHA. No native result is inferred from the presented summary alone.

## Coverage limitations and remaining work

At the initial C_SHARED observation, fix and derived-tool routes still required evidence. The closure below now records the actual fix/check routes and bounded derived-route assessment. Syntax success does not certify arbitrary dependencies or final style. Markdown passed status does not erase warning issues. Shared fixture/native checks do not substitute for the actual public first-output pairs. Complete workspace tests and branch gates belong to Validation.

## C_SHARED fix route

A real production formatting finding was repaired through `apply_fixes(scope="targets", targets=["mcp_server/services/template_engine.py"], fixes=["python_format"])`. Native Ruff 0.15.6 reported one file reformatted; adapter sFWzvJZBN26YRZqa returned passed. The subsequent explicit format check reports one file already formatted. Source inspection confirms only an extra empty line before a module-level function changed. This proves a real fix/check route on source; the planned isolated first-output fix probe remains additional later evidence. Pristine scaffold evidence files were untouched.


## C_CODE actual fix and negative-result routes

Public schema/scaffold routes correctly expose and enforce the clean input break. Missing required module prose and the removed description alias return context_invalid, written=false, no native execution. Empty optional TypeScript prose remains an explicitly supplied empty documentation carrier. The raw outputs agree with factual preflight DTOs.

Native checks exposed three generated format and three lint findings on intermediate examples, rather than hiding them behind syntax success. Ordered apply_fixes on separately scaffolded identical-context files fixed one I001 and formatted one pass gap with Ruff 0.15.6; complete rows/readback are in first-output-evidence.md. A recheck confirmed those two files have no remaining format/lint finding. This fulfills the planned isolated fix probe without modifying pristine evidence.

## F3 — Verbose expected failures can exceed adapter response bounds

Status: reproducible practical limitation; deferred triage, no false RED claim. During C_CODE existing-context migration, ordinary Pytest traceback output caused unavailable / response_too_large with 8,912,896 observed stdout bytes. The producer delegate inspected the complete failure DTO; its serialized cached object was approximately 5,076,661 codepoints and its complete native capture was not reconstructed. Therefore this unavailable response is not used as native RED evidence and unavailable log text is not claimed preserved.

Prerequisites: migrated seven existing code-family inputs against the old schemas, real delivered suite fixture and configured Pytest output. Reproduce with the exact RED target subset in Planning using normal traceback output. Workaround: caller args `["-q","-n","0","--tb=no","-rN"]`; the repeated root request then returned a complete negative native result, 32 failed / 2 passed, with verified cache windows. Large repeated resolved-schema ContextError tracebacks are the observed trigger; the precise response-budget and display-policy trade-off needs later tool coordination. This is not attributed as a regression introduced by #460 without historical proof.

## F4 — Immediate post-restart calls can reach the retiring process

Status: observed sequencing friction; deferred lifecycle/tool coordination. restart_server reported the old PID 14492 and explicitly instructed a three-second wait. An immediate get_work_context returned context from that process, followed by run_tests with no response until tools/call timed out after 300 seconds. A later health_check reported healthy new PID 8968; an attempted scaffold on that new process was rejected with context_not_loaded. Refreshing get_work_context on the new process resolved that condition and the same read-only test selection completed.

Expected safe use follows the tool's stated delay: wait at least three seconds, verify the changed healthy PID, then load work context before further calls. Later restarts used that sequence and remained operational. The observation demonstrates a producer sequencing mistake and a possible usability improvement around restart readiness; it does not prove a dead native process or failed tests. No outcome/receipt exists for the timed-out call and it contributes no test evidence. Cache entries are transient across restarts: an unread recheck cache disappeared as expected; the isolated check was rerun without replaying the fix mutation.

No unrelated adapter/server repair was introduced. Full suite/branch gates and independent QA remain outstanding.

## F6 — Template admission failure terminates bootstrap and leaves a falsely ready proxy

Status: confirmed startup/recovery defect; follow-up required. This is an operational defect in the current tools, separate from the issue473 template correction. It must not be accepted as normal handling of an invalid template. No claim is made that issue460 introduced it.

### Trigger and direct cause

During C_DOCS, the new shared Markdown document base selected the latest authored revision with `content.document_metadata.revisions[-1]`. Jinja accepts this expression, but actual startup admission rejected the resolved access. The first package inspected was architecture. Controlled local startup on 2026-10-03 returned exit code 1 and the following complete MCPError facts:

```json
{
  "message": "template_input_undeclared",
  "code": "ERR_CONFIG",
  "params": {
    "template_id": "architecture",
    "template": "shared/templates/bases/tier2_markdown_document.jinja2",
    "field": "content.document_metadata.revisions.-1",
    "line": 8
  }
}
```

The diagnostic command was `.venv/Scripts/python.exe -m mcp_server`. A second bounded diagnostic invoked `ServerBootstrapper(Settings.from_env()).bootstrap_target()` and printed only the caught MCPError message/code/params, exposing the actionable details absent from the first traceback. No production source was changed during diagnosis. Source-only producer delegation reached a contrary hypothesis about the negative index; the actual runtime exception above is authoritative evidence.

### Exception and recovery chain

1. `TemplateInputValidator.validate` in `mcp_server/services/template_catalog.py` raises MCPError with code ERR_CONFIG for the undeclared access. Template syntax failures likewise become MCPError in `TemplateGraphResolver`; that related path is established by source inspection, not a separate runtime reproduction.
2. `ServerBootstrapper.bootstrap_target` propagates this error from `admit_template_suite`/catalog loading.
3. `mcp_server/cli.py` catches ConfigError and FileNotFoundError to construct DegradedMCPServer. MCPError(code=ERR_CONFIG) is not ConfigError, so this admission error escapes that recovery boundary and terminates the process before MCP initialization.
4. The proxy starts its stderr reader only after initialize replay. Its subprocess owner may clear server_process when the failed startup exits. In the observed run this ordering lost the original stderr; the local audit log contained no startup exception.
5. The proxy treats an empty/non-JSON initialize response as a logged observation and continues to log server_ready/restart_completed without checking a successful initialize response and live server. The audit on 2026-10-03 19:10:27–19:10:34 UTC showed proxy PID30612, old server PID32992, failed new PID27152, non-JSON initialize, then server_pid=null and new_server_pid=null while still claiming ready.
6. `send_to_server` silently returns when server_process is None. The retained client connection therefore has no server to answer health/context/edit/restart requests. The root health request remained unanswered and was abandoned; it is not native test evidence. The built-in restart request also cannot recover through this dead forwarding path.

### Reproduction and impact

Prerequisites: configured delivered suite, the uncorrected shared document base, working proxy/client connection, and normal server restart. In a disposable copy only: use the rejected revision expression, call restart_server, allow startup to complete/fail, inspect the audit events, then request health/context. Compare the direct startup exception with the false ready events and missing MCP response. Do not deliberately crash the working issue473 server again merely to repeat this result.

Impact: one invalid configured template can disable all tools, conceal its actionable package/file/field details from the client, and remove the tool-level recovery path. This is materially more severe than a single rejected scaffold request.

Required follow-up acceptance boundaries: retain the failed package/template/line/field/cause in accessible startup diagnostics; distinguish failed admission from healthy readiness; keep an explicit repair/retry or degraded recovery path available; drain/preserve startup stderr even when a child exits early; report failed initialize/process exit instead of logging ready or silently dropping client calls. Invalid suites must remain rejected. Do not solve this by relaxing admission or activating an invalid snapshot. Exception taxonomy and proxy lifecycle ownership must be reviewed together before repair.

### Authorized issue473 correction and evidence limits

The human authorized the single template source correction and this root-cause record outside MCP because the server was unavailable. The replacement is `content.document_metadata.revisions | last`, using the existing Jinja filter and retaining the approved latest-supplied-revision behavior. An in-memory substitution first completed bootstrap without changing files; after the authorized exact replacement, an unmodified bootstrap of the on-disk suite also completed successfully with exit code 0. The only emitted warning was the existing Pydantic SchemaAttachment.schema shadowing warning.

This local bootstrap is diagnosis/recovery evidence, not a public scaffold, native quality gate, family test run or independent approval. The client/proxy connection still requires reconnection before normal pgmcp execution can resume. No CLI/proxy production repair, additional regression test, admission change or generic issue476 work was performed. The startup/recovery defect remains an explicit current-tool finding for coordination, with the human requirement that invalid Jinja/templates must have diagnostics and a recovery path.


## F5 — Shared JSON schema authoring has no direct scaffold route

Status: observed authoring friction; deferred tool coordination. The new shared document-metadata.schema.json was initialized through the admitted generic_doc scaffold because repository instructions require scaffolding for new sources, but the live artifact set has no JSON-schema source package. The initial Markdown scaffold succeeded; replacing its content with the required JSON using safe_edit_file(report) retained the generic_doc selection and ran Markdown preflight. That edit reported written=true with failed validation (missing H1). The final file is JSON without a Markdown provenance line. This failed preflight is not JSON validity evidence.

Reproduce in a disposable directory: discover generic_doc; scaffold an exact *.schema.json filename with its admitted authored document context; replace the generated Markdown with a Draft202012 JSON schema under report policy and inspect selection/profile/check rows. Expected authoring route should assess the intended source role without a misleading inherited Markdown selection. The concrete limitation is the absence of an admitted schema-source scaffold and selection provenance on replacement; no claim is made about all JSON edits.

Separate evidence supplies correctness: the refreshed real catalog admitted all seven dependent document schemas, public discovery exposed their resolved required metadata, public old-root/absent/empty-revision requests were rejected before writing, and the delivered/installed existing tests passed. No new scaffold family, selection rule or JSON adapter was added in #473.


## C_DOCS current route evidence and recovery closure

After the authorized exact template correction, the client connection was re-established. The supported restart after the bounded structure repair used the documented delay, then get_work_context confirmed issue473 Implementation cycle3 and health_check confirmed healthy PID27688. F6 remains a startup/recovery defect; corrected package admission and restored normal tools do not repair the proxy/CLI failure chain.

Twenty fresh minimal/filled calls passed their individual Markdown document/body or commit_message preflight rows and persisted untouched. Seven real old-root status requests, missing document_metadata and empty revisions were rejected with context_invalid and written=false. Independent configured offline Lychee link review of the 18 Markdown examples plus active scaffolding reference/findings returned 23 successful, 0 errors, 0 excluded (receipt pgmcp://cache/runs/fa81c9d40c684c89b73d643c73dfdaa1), while filled preflight rows still expose F1 angle-destination warnings. That comparison distinguishes actual valid destinations from the preflight parser's warning.

Existing tests after the structure correction: 47 passed, 1 existing warning, 69.79s in the twelve planned files; the two narrow current contract/docflow consumers additionally passed with 22 deselected and 9 existing warnings in 2.23s. Test gates passed format/lint/Pyright on twelve files. Native Ruff formatting on four migrated tests corrected actual source layout, followed by explicit passing checks. Full configured tests and branch gates remain Validation work. No additional automated content test or permanent harness was created.

## F7 — Catalog refresh is per MCP client

Observed during C_DOCS: the root client refreshed the server/catalog after source edits and discovered Architecture fingerprint F3GiYxoJo0WTq92r, while the delegated collector's separate client still returned its earlier Architecture fingerprint after get_work_context. The collector stopped before producing final output; the root then collected the six final cases with the current fingerprint. Reproduction: use two independent MCP clients, edit a shared template, restart/refresh one client, then request get_work_context and scaffold_schema from the other. Compare complete schema receipt fingerprints, not merely the shared filesystem or context summary. Each client's immutable admitted catalog requires its own refresh. This is a lifecycle/usage constraint; the observation does not establish a new template-engine bug or certify every client implementation. Independent QA must refresh its own client and verify fingerprints before public scaffold evidence. Disposition: document for coordination/tool usability triage; no new catalog layer is built in #473.

### C_DOCS final route refresh

Actual final public scaffolds: 20 pairs plus six boundaries, all written with their individual document/body/message preflight rows passed. Existing template/install tests: 47 passed, 1 warning, 67.13s; actual contracts/docflow consumers: 2 passed, 22 deselected, 9 warnings, 2.36s. Earlier 69.79s/2.23s runs remain historical evidence. Exact final requests, complete DTOs, source identity and file effects are in first-output-evidence.md. Manual reading found substantive presentation defects despite passing content preflights; those preflights prove their narrow configured responsibilities, not all document structure or caller facts.

## C_RECONCILE current-tool verdict and route coverage

The currently upgraded tools proved useful for real implementation: they discover closed contexts, reject stale inputs before writes, run configured content preflights, preserve individual native outcomes and arguments, apply ordered real fixes and expose evidence through resources. Those routes do not replace manual output review; passing syntax/Markdown preflight did not detect the substantive decision/table/list/revision presentation defects corrected in C_DOCS. The observations below describe current correctness and usability, with no numerical or causal comparison against pre-460 behavior.

| Route | Actual exercised evidence | Limits / disposition |
| --- | --- | --- |
| scaffold_schema | Complete resolved inputs/identities for all 19 families; final code graph freshness readback. | Large schemas require cache windows (F2); refresh is per client (F7). |
| scaffold_artifact | All 38 final first-call pairs plus boundary/presence/rejection cases; written/status/individual rows inspected. | Syntax is not arbitrary dependency execution or semantic quality; F1 false link warnings remain. |
| safe_edit_file | Real source/schema/template/test/doc edits; enforce/report write/status inspected. | Jinja report profile has no admission check; real refresh/bootstrap supplies admission. Shared schema initialization friction F5 remains. |
| run_checks | Actual generated Python format/lint, production format/lint/Mypy/Pyright, test format/lint/Pyright and offline Markdown links. | Syntax adapters are content-only and cannot be selected; full branch checks belong to Validation. |
| run_tests | Genuine context-migration failures, corrected existing family/native/CLI/installed/docflow results with configured args. | F3 verbose failures exceed response budgets; bounded traceback request recovers usable negative evidence. No unavailable response is counted as RED/pass. |
| apply_fixes | Real source formatting and isolated generated-output lint/format probes with readback and explicit recheck. | Separate instances preserve pristine first outputs; fixes do not certify the original generated output. |
| get_work_context / get_project_plan / cycle / commit | Actual stored deliverable readback, active branch/cycle instructions, intermediate progression and scoped commits. | Lifecycle replies are operation facts, not independent QA approval. |
| create-issue derived route | Actual Issue body preflights/output, live context/source consumers reviewed, workflow and mirror reconciled. | No live GitHub issue was created solely as a probe. Publication source review establishes body/envelope responsibility, not end-to-end remote publication. |

Current findings F1–F7 have individual reproductions, impact, uncertainty and disposition above. Coordination should prioritize the confirmed bootstrap/proxy diagnostic and recovery failure F6: corrected template admission restores this branch, while the tool defect still needs a separate owned repair. The human requirement that invalid templates retain diagnostics and a recovery path is explicit. Other candidates are Markdown link parsing, schema-source authoring, bounded-failure usability and client/restart guidance. F2/F4/F7 distinguish supported usage constraints or producer sequencing from confirmed product defects. Issue #476 remains separately scoped to generic schema/template consumption; #473 corrected its concrete packages and does not build generic coverage enforcement.

The initial implementation-report scaffold request omitted required purpose/summary and used section.title instead of the discovered section.heading; the public tool rejected it with context_invalid and no write. The immediately corrected admitted request succeeded. This was a producer input error, not a tool finding, and is excluded from product-fault claims.

All findings are documentation for later triage; no unrelated CLI/proxy/adapter repair was added. No unresolved known #473 correction blocker is intentionally hidden; independent QA may identify further blockers. At that Implementation hand-over, full configured tests, branch gates and later progression were outstanding. [Validation](validation.md#independent-validation-closure--2026-10-04) now records independent GO and the explicitly accepted issue-specific gate disposition; Documentation/Ready/merge retain their own boundaries.


## Selection intent applicability audit — 2026-10-04

**Disposition:** owner-requested cross-adapter research for later coordination. The selection-intent direction has been discussed with the owner; this audit identifies current behavior and required work, not an implemented or independently approved adapter contract.

### Inventory and method

Nine bundled adapter packages are available: Ruff, Mypy, Pyright, Pytest, Lychee, Python syntax, TypeScript syntax, Markdown preflight and Commitlint. Their manifests declare ten check capabilities, one test capability and two fix capabilities. Lychee links admits both selection and content input. The configured workspace_adapters directory is absent and trusted_adapter_ids is empty; no additional workspace adapter was found. Read [catalog admission](../../../mcp_server/execution/catalog.py), [bootstrap roots](../../../mcp_server/bootstrap.py) and the configured [checks](../../../.pgmcp/config/checks.yaml), [tests](../../../.pgmcp/config/tests.yaml), [fixes](../../../.pgmcp/config/fixes.yaml) and [adapter trust](../../../.pgmcp/config/adapters.yaml).

The review inspected all nine manifests, the corresponding request/launch paths, native dependency declarations, current native configurations and applicable native documentation/source. Current selection semantics were also exercised through six existing integration cases. No production/test code, native configuration or adapter contract was changed. No new automated content or regression test was added. Source review and passing existing tests do not certify a future selection_intent implementation.

The proposed meanings are:

| Intent | Meaning |
| --- | --- |
| configured_candidates | Assess only supplied candidates that belong to the native configured/discovered initial source selection for the requested operation. |
| explicit_sources | Preserve the native meaning of explicit files/directories, replacing default starting paths where the native tool normally does so; retain native analysis settings and applicable native exclusions. |

A file is a concrete source; a directory remains a native discovery root. Neither intent is permission to turn off quality rules, override every exclusion, expand to unrelated start sources or copy native configuration into PGMCP configuration.

### Applicability and concrete adapter work

| Package / input / operation | Current observable semantics | Meaning of the proposed intent | Required behavior change |
| --- | --- | --- | --- |
| Ruff selection check: lint | Supplied paths are explicit native arguments. They can bypass discovery includes/excludes and ignore rules unless native force-exclude requires exclusions. | Candidate mode must use effective native discovery and lint applicability; explicit mode retains normal explicit-source semantics. | Yes for candidate mode. Reuse native configuration/discovery; force-exclude alone does not prove discovery includes/file applicability. |
| Ruff selection check: format | Supplied files/directories reach native format; formatting has operation-specific exclusions/applicability. | Same intent distinction, resolved for format rather than inferred from lint's source list. | Yes for candidate mode. A lint --show-files result is not by itself proof of the formatter's effective selection. |
| Ruff fix: lint / format | Public apply_fixes admits explicit regular files only. The adapter preserves native configuration and source/write guards. | Current public route has explicit_sources semantics. There is no current branch/candidate fix route. | No new candidate filtering is required for the current fix API. Retain explicit semantics; admit/validate a new field only if the eventual fix wire contract carries it. Share operation-appropriate native selection machinery if a candidate fix route is later approved. |
| Mypy selection check: types | Explicit sources replace files/modules/packages defaults. Native exclude affects recursive discovery, not explicit files. Configured calls preserve native defaults. | Candidate mode must retain native configured initial sources, including configured modules/packages where used. Explicit mode preserves outside-root files/directories and module overrides. | Yes for candidate mode. Reuse the native parser/configuration/source discovery; do not recopy files or exclude rules. |
| Pyright selection check: types | Nonempty adapter targets use the native filename channel. Native CLI overrides configured include roots while retaining exclude and analysis settings. | Candidate mode retains configured include/exclude/discovery eligibility; explicit mode preserves native explicit include override. | Yes for candidate mode. Reuse native configuration/enumeration; do not parse include/exclude/extends independently in PGMCP. |
| Lychee selection check: links | Files/directories reach native Lychee via the owned filename channel. Native directory traversal applies extensions and ignore rules. Explicit files/glob matches bypass the extension discovery filter; exclude_path still applies. | Candidate mode applies effective source discovery restrictions. Explicit mode retains native explicit-file handling. URL filters are link policy, not a project file allowlist. | Yes for candidate mode. Native dump-inputs/get_sources can inform a native resolver investigation, but passing the same explicit files to dump-inputs would still bypass extensions. Do not add a Markdown-only rule or a second extension list. |
| Lychee content check: links | One proposed snapshot has an owned logical path/base/remap. | No candidate discovery occurs; exact supplied content remains the subject. | None. Keep selection_intent out of the content request. |
| Pytest test: tests | Empty targets use configured discovery/testpaths; explicit files/directories replace starting paths. Native collectors/plugins determine tests; explicit .py sources can bypass python_files discovery patterns. | Explicit mode already matches current targets behavior. Candidate mode would require native configured collection eligibility, not a hardcoded test_*.py/.py filter. | No behavior change required for the currently admitted configured/targets routes. run_tests has configured/workspace/targets, with no branch scope. A future candidate route would require native collection-aware filtering. The workspace route's intent must be decided explicitly, not silently narrowed to testpaths. |
| Python syntax content check: syntax | Parses exactly the supplied Python snapshot. No source selection. | None. | None; no intent field needed. |
| TypeScript syntax content check: syntax | Checks exactly the supplied TypeScript snapshot. Native project selection diagnostics are deliberately outside snapshot validity. | None; tsconfig analysis options remain relevant, project include/exclude roots do not select the snapshot. | None; do not filter supplied content by tsconfig file lists. |
| Markdown preflight content check: document / body | Examines exactly one supplied document/body snapshot. | None. | None; no intent field needed. |
| Commitlint content check: message | Checks the supplied message under native commit rules. | None. | None; source directories do not select a message. |

**Concrete new candidate behavior is therefore needed in four packages:** Ruff (lint and format checks), Mypy, Pyright and Lychee selection. Pytest and Ruff fixes already expose explicit-source routes; do not invent an additional candidate operation solely to give the new field work. All four content-only packages and Lychee's content route have no selection-intent responsibility.

### Native evidence and reuse constraints

- Ruff: [native discovery documentation](https://docs.astral.sh/ruff/configuration/#python-file-discovery) distinguishes discovered paths from explicit inputs and supports operation-specific exclusions. [force-exclude](https://docs.astral.sh/ruff/settings/#force-exclude) enforces configured exclusions on explicit paths. The passing existing pinned-native exclusion case proves current explicit/discovery distinction, not a complete new candidate resolver.
- Mypy 1.19.1: [native option handling](https://github.com/python/mypy/blob/v1.19.1/mypy/main.py#L1360) selects configured roots only when explicit source selectors are absent. [native source creation](https://github.com/python/mypy/blob/v1.19.1/mypy/find_sources.py#L25) distinguishes files from recursive directory discovery. The current adapter already uses the installed native option/config parser.
- Pyright 1.1.408: [service include override](https://github.com/microsoft/pyright/blob/1.1.408/packages/pyright-internal/src/analyzer/service.ts#L1032) replaces include specs for explicit CLI sources. [SourceEnumerator](https://github.com/microsoft/pyright/blob/1.1.408/packages/pyright-internal/src/analyzer/sourceEnumerator.ts#L151) still applies native exclusions to roots. Include/exclude/ignore are different responsibilities; imports may pull in dependencies beyond the initial selected roots.
- Lychee 0.24.2: [native InputResolver](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-lib/src/types/input/resolver.rs) applies extension/ignore filters to traversal, deliberately bypasses extension filtering for explicit files/glob matches, and retains excluded-path filtering. This source qualifies the shorter [CLI extensions description](https://lychee.cli.rs/guides/cli/#--extensions). No native project-root allowlist equivalent to Mypy files is established here.
- Pytest 9.0.2: [native Python collection](https://github.com/pytest-dev/pytest/blob/9.0.2/src/_pytest/python.py#L183) distinguishes explicitly supplied files from discovery patterns. Collection hooks/plugins remain authoritative; a generic filename predicate cannot represent all native test collectors.

Public/stable native discovery routes sufficient for the new candidate behavior have not been established for every pinned operation. In particular, Ruff format and Pyright require a bounded native-resolver feasibility decision before implementation. A private native helper, extra discovery invocation or full analysis followed by diagnostic filtering is not implicitly approved. Filtering diagnostics after checking/fixing unrelated initial sources would not meet the intended selection restriction.

### Existing behavior verification and reproduction

Run run_tests with scope=targets on the five existing adapter integration files and python_tests arguments:

```json
{
  "python_tests": [
    "-q", "-n", "0", "--tb=short", "-k",
    "native_fixture_exclusion_distinguishes_discovery_from_explicit_targets or configured_roots_and_explicit_tests_use_native_selection or native_discovery_and_literal_targets or configured_discovery_and_deliberate_native_expansion or native_literal_selection"
  ]
}
```

Use timeout_seconds=240. Targets: [Ruff checks](../../../tests/mcp_server/integration/adapters/test_ruff_checks.py), [Mypy](../../../tests/mcp_server/integration/adapters/test_mypy.py), [Pyright](../../../tests/mcp_server/integration/adapters/test_pyright.py), [Pytest](../../../tests/mcp_server/integration/adapters/test_pytest.py) and [Lychee](../../../tests/mcp_server/integration/adapters/test_lychee.py).

Observed: **6 passed, 207 deselected, 2 warnings, 29.26 seconds**; receipt pgmcp://cache/runs/902905bb03fd44d387d59792b2ec9b30. The cached result was read once for exact selected counts and native evidence. The two warnings concern SchemaAttachment.schema shadowing and TestCapability collection. These cases exercise current native root override, Ruff exclusion, Pytest default/expanded selection and Lychee file/directory transport. They do not directly exercise the proposed candidate filter or Lychee's extension bypass; the latter is established by pinned native source inspection.

### Contract and generic boundary findings for follow-up

- Current selection/test/fix wire validators reject unknown keys. If a role receives selection_intent, its wire schema, validator and admitted role contract must be updated even when both intents have identical behavior. Do not broadcast the field to content requests or silently send it to existing v1 packages.
- Preserve the established configured empty-target call. An originally nonempty candidate selection filtered to nothing must not become native default discovery; no remaining candidate must never expand to the whole configured project. Define the empty-applicable outcome explicitly without inventing a successful native run.
- No per-file skip report is required by the owner's current preference. That does not remove the need to distinguish no applicable sources from a failed/incomplete run.
- Preserve explicit directory plus explicit descendant-file combinations. The current [ScopeResolver collapse](../../../mcp_server/execution/check_selection.py) removes contained paths: targets=[tests/, tests/generated.py] can lose the deliberate explicit file. Native discovery may exclude that file while direct file selection admits it. This is a concrete generic selection reconciliation item, separate from adapter-specific filtering.
- Do not use the type checkers' transitive import closure as the initial configured source set. Native import following and diagnostic suppression remain native analysis policy.
- Existing apply_fixes requires files and has only targets scope; directory or branch fixing would be a separate API/scope decision. Existing run_tests has no branch scope. The intent mapping for workspace and configured calls remains to be specified without weakening their existing behavior.
- Select the contract migration/breakage strategy explicitly for the affected adapter roles. The earlier no-legacy template strategy does not automatically authorize an adapter-wire migration.
- Respect [architecture SRP/DRY/SSOT/explicitness](../../coding_standards/ARCHITECTURE_PRINCIPLES.md): generic code owns selection intent, adapters own native applicability, and native configuration remains authoritative. No duplicated native extension/glob/exclusion/config hierarchy is approved.

This audit is follow-up triage evidence. It does not broaden issue473's template correction into adapter implementation, close its pending full Validation obligations or claim independent QA approval.

## Deferred branch-wide check solution — owner disposition, 2026-10-04

**Decision:** carry this investigation into a separate follow-up issue. Issue473 records the evidence and performs its required Validation; it does not implement selection_intent, adapter filtering, target-collapse changes or native-selection infrastructure. The owner explicitly requested this separation before further Validation. Coordination owns later issue creation, prioritization and assignment; no follow-up issue number is fabricated.

### Problem and reproduction index

The current branch Python profile passes the same mixed Git-derived selection to every selected native adapter. Explicit native inputs can bypass discovery restrictions or replace configured start roots, so merely forwarding branch paths does not mean "check the applicable changed sources". The exact failed broad request, native outcomes and scoped Python workaround are preserved in [Validation V-F8](validation.md#v-f8--branch-python-profile-sends-mixed-source-kinds-to-native-python-tools). The preceding applicability audit contains all nine packages, native references and the six existing-case reproduction (6 passed); it is the primary research inventory.

Additional source-level reproduction: request explicit targets tests/ and tests/generated.py together, where native recursive discovery excludes the descendant but direct file input admits it. ScopeResolver._collapse_targets currently removes the descendant before the adapter receives it. This is source evidence, not a claimed newly executed reproduction.

### Discussed direction and unresolved design decisions

| Boundary | Discussed direction | Follow-up obligation |
| --- | --- | --- |
| Generic selection | Translate caller intent to configured_candidates or explicit_sources; retain Git/branch knowledge here. | Decide configured/workspace mappings and preserve deliberate directory-plus-file inputs. Do not flatten directories generically. |
| Adapter applicability | Candidate checks assess the native configured/discovered initial source set; explicit checks retain native explicit-source semantics. | Implement only meaningful responsibilities: Ruff lint/format, Mypy, Pyright and Lychee selection; avoid invented candidate behavior in content, existing fixes or Pytest routes. |
| Native configuration | Reuse native configuration and discovery, including operation-specific applicability and exclusions. | Establish a supported resolver for each pinned native operation, especially Ruff format and Pyright. Do not duplicate extension, glob, root or exclusion settings in generic code or adapter configuration. |
| Empty result | A nonempty candidate request with no applicable sources must not fall back to configured full-project discovery. | Define an honest no-applicable-sources result without claiming a native pass. Per-file skip reporting is not requested. |
| Wire contract | Only receiving selection roles need the semantic field; content requests remain exact snapshots. | Choose compatibility/migration strategy per affected role before Design. Current strict validators reject unknown fields; the template clean-break decision is not adapter migration approval. |
| Feasibility and coverage | Existing native discovery tests establish today's behavior. | Resolve native API/private-helper and extra-invocation trade-offs; define meaningful evidence in the follow-up plan. No extra content/regression suite or permanent harness is authorized by this research record. |

### Issue473 execution order

1. Record and commit this deferred research first.
2. Execute the single configured full-suite run with the approved 1200-second native budget and 1800-second client window.
3. Complete branch-check evidence using the current tools, retaining historical failures and any required-gate limitation; no production repair or silent gate substitution.
4. Finalize the Validation report and request the external Beoordeel designplan review.

In the owner's overall completion list, deferral is the fourth obligation, performed first. Later Documentation/Ready must carry this hand-off forward. The follow-up implementation is not a prerequisite that expands issue473; incomplete required Validation evidence remains explicitly reviewable.

## Documentation closure and coordination triage — 2026-10-04

The template correction and missed existing consumer are validated. External QA returned Validation → Documentation GO on 2756f8dd; [Validation 0.7](validation.md#independent-validation-closure--2026-10-04) indexes the independent 2775-pass full suite and accepted changed-file gates. The source-level examples above retain their original dates/stages; corrected issue473 defects are not reopened as current defects by historical negative evidence.

| Follow-up | Evidence / reproduction entry point | Current disposition / boundary |
| --- | --- | --- |
| F6 bootstrap/proxy diagnostics and recovery | F6 above: invalid Jinja package admission, startup stderr and false ready proxy chain | Confirmed separate repair candidate; prioritize preserved startup diagnostics and an actionable recovery path. The package correction restores this branch but does not repair CLI/proxy lifecycle behavior. |
| F1 Markdown angle destinations | F1 above and exact PR scaffold request in first-output-evidence.md | Confirmed bounded false-positive example; investigate native parsing separately, preserving valid destinations. |
| F2 cache windows and V-F10 excessive reads | F2 above and Validation V-F10 | Supported bounded reading plus producer efficiency failure. Follow the current AGENTS cache/hash instructions; assess selective diagnostics/export as later usability work, without routine full downloads. |
| F3 verbose native failure bounds | F3 above, same existing RED subset with native traceback output | Reproducible operational limit; do not count unavailable output as RED/pass. Investigate negative-result usability without promising unlimited native responses. |
| F4 immediate restart race and F7 client catalog refresh | Exact multi-client/restart steps above | Current lifecycle constraints; improve guidance/triage only after separating expected client ownership from a confirmed implementation defect. |
| F5 schema-source authoring friction | F5 above | Missing direct schema-authoring route, separately triaged. No new artifact type or schema pipeline was added. |
| Branch-check selection | Full nine-package audit and Deferred branch-wide check solution above; historical broad failures in Validation | Owner explicitly deferred production/adapter/wire/resolver implementation to another issue. Preserve proposed intent, native config reuse, file/folder semantics and unresolved migration/feasibility choices. |
| Four AGENTS source/runtime link locations | Validation's exact 41 native failures, nine root-relative targets and release deployment context | Reviewed issue473-specific coverage exception. Preserve source/deploy conventions; no blanket link-check exclusion or directory-relative rewrite is approved. |
| Cross-session receipt visibility | Producer run 8d4a6cb1a32e40eaac12bdf9bb1d1743 and Markdown receipts were unavailable through QA's MCP session; QA independently reran the configured suite and accepted Markdown selection | Observed hand-off friction, with no established storage/expiry/transport root cause. Triage result accessibility and durable hand-off options separately; do not infer native failure from an inaccessible receipt. |
| Issue476 generic schema/template consumption | Research's explicit separate-scope decision and actual/manual nineteen-family evidence | Keep generic field-consumption analysis/enforcement separate. The concrete corrected outputs do not prove generic consumption of every admitted field. |

Cross-session reproduction: produce a result receipt through one MCP session, attempt that exact URI through an independent session, and record native/resource outcomes separately. In this review the producer had a complete passed result, while QA could not read it and obtained its own passing result (02ec0cdfbc5b465a821db8bd5d5e85f0); unavailable resource access did not invalidate native completion. This records an observed case, not a claim that every receipt is session-local or always inaccessible.

Coordination receives candidate findings with these reproduction indexes, actual impact and limitations. No new issue number, prioritization approval or implemented remedy is fabricated. Ready should carry this index forward; only coordination assigns follow-up issues. F6, generic476 and the branch-selection proposal must remain distinct work units unless a later explicit owner decision combines them.

Routine success/status uses tool summaries. Read cached DTOs only for needed structured facts or diagnostics, check size before paging, reuse prior reads and verify multipart identity once when needed. The prior excessive cache exercise remains disclosed as producer inefficiency; it is not the recommended workflow.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | Not recorded in the original document | Existing current-tool implementation findings and route assessment. |
| 0.2 | 2026-10-04 | @imp validator | Audit all nine available adapter packages for selection-intent applicability, record existing native verification and identify bounded follow-up contract/resolver work. |
| 0.3 | 2026-10-04 | @imp validator | Explicitly defer the branch-check solution to a separate issue, preserve boundary decisions and unresolved design/migration questions, and record the owner-ordered Validation continuation. |
| 0.4 | 2026-10-04 | @imp documenter | Close stale current-status claims after independent Validation GO and finalize bounded coordination triage, including cross-session receipt visibility and explicit deferred-work separation. |

