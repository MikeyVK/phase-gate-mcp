<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Current Tool Practice Findings

**Status:** Implementation in progress
**Version:** 0.1
**Last Updated:** 2026-10-03

This assessment describes current practical behavior, with no pre-460 score or assumed regression attribution. Root issue473 template defects are corrected within their planned cycles; unrelated tool findings remain reproduction evidence for coordination. Exact actual scaffold requests, outputs and complete factual rows are in [first-output evidence](first-output-evidence.md).

## Observed working routes

Public schema discovery exposes complete resolved contexts and source fingerprints. Public scaffold enforces Python/TypeScript content syntax and current Markdown/commit profiles before create-only persistence. Every C_SHARED request has success, written, policy/status and individual native rows recorded separately.

Safe edit of production/fixture Python runs Python syntax preflight (Python 3.13.7). Jinja-source edits under report mode return written=true, validation_status=not_executed, profile=null, checks=[]: this is an explicit routing limitation, not admission proof. Real admission/render tests and refreshed public scaffolds supply that separate evidence.

Run tests preserves configured arguments and full native outcomes; the initial C_SHARED subset reported 183 passed accurately. Negative native results were retained and exposed two omitted filter-registration consumers. Run checks preserves independent format/lint/Mypy/Pyright outcomes; Pyright correctly detected protected-member access in the initial registration implementation. Existing pure filters were moved into the same engine module so the shared registration no longer crosses private class members. A subsequent check passes both typing rows; module-level function-spacing formatting is being corrected.

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

All findings are documentation for later triage; no unrelated CLI/proxy/adapter repair was added. No unresolved known #473 correction blocker is intentionally hidden; independent QA may identify further blockers. Full configured tests, branch gates, later documentation/ready progression and merge remain outstanding at this hand-over.
