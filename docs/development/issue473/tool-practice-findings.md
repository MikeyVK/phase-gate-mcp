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

Impact: agents must implement/observe bounded resource reading for resolved schemas and verbose native results. Exact window-reading behavior is documented by `pgmcp://docs/cache-reading`; this supported path worked. Cache lifetime is transient and fingerprints must be refreshed after a server restart. Preserve durable factual evidence before cache loss. The producer now uses verified windows; no result is inferred from the presented summary alone.

## Coverage limitations and remaining work

Fix and derived-tool routes still require actual evidence in C_RECONCILE. Syntax success does not certify arbitrary dependencies or final style. Markdown passed status does not erase warning issues. Shared fixture/native checks do not substitute for the actual public first-output pairs. Complete workspace tests and branch gates belong to Validation.

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
