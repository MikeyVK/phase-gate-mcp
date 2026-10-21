<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue \#536 — Live response-mode observations

**Status:** Partial live observations — owner acceptance pending  
**Version:** 0.2  
**Last Updated:** 2026-10-21

## Purpose

Record the owner-requested live Codex comparison after activating merged #537.

## Scope In

Restart, two modes, phase instructions, separate schema attachment, safe missing-file refusal, large response and paging.

## Scope Out

Production changes, phase transitions, broad tests, package builds/installs, final acceptance, tags and publication.

## Summary

The actual agent received the expected structured/resource outputs and read real cache references through the connected MCP resources/read interface. The temporary shared override is restored; the server is healthy in structured mode. This is partial observation, not full issue or release acceptance.

## Candidate and activation

HEAD 31b71953134df7e49aab9ef79bc3873f45822e4b on chore/536-live-agent-acceptance-and-release includes main merge 5e23196733557b2e988ce51a2554928e2d55f131. Actual Codex connection launches .venv315/Scripts/python.exe -m mcp_server.core.proxy with workspace PYTHONPATH. Health reports installed version 3.0.0; no new release was published. Owner requested restart and explicitly approved temporarily setting the shared global.response_mode to resource and restoring it. Child PIDs: structured 73884, resource 7132, restored structured 22824; all post-restart health responses healthy. Uptime samples do not measure startup duration.

## Paired tool requests

Live invocations in both modes: health_check(); get_work_context(); get_project_plan(issue_number=536); scaffold_schema(artifact_type='research'); safe_edit_file(path='.pgmcp/temp/issue536-live-missing.md', operation={op:'replace',target_content:'not present',replacement:'still absent'}, validation='report'); get_issue(issue_number=536).

| Surface | Structured | Resource |
| --- | --- | --- |
| Inline text | Structured-result footer | Real cache-URI footer |
| Full operation | data.operation | No structuredContent; actual cached operation read successfully |
| Phase instructions | Inline and full structured output | Inline and cache; phase_instructions equals structured operation |
| Available schema | Separate embedded-resource block and URI/MIME structured metadata | Same separate embedded-resource block |
| Missing file | original_missing, success=false, written=false, isError=true | Same refusal and complete cached diagnostic |

The schema URI was schema://template/research/context, MIME application/schema+json, body 4209 characters; content/URI/MIME matched across modes. Structured attachments contained metadata without a second body copy. Plan issue/workflow/phases matched; planning_deliverables was null in both modes and no planning mutation was attempted. The missing file did not exist before the refusal.

## Large response and cache read

get_issue(536) inline text: structured 7953 UTF-8 bytes, resource 7643 bytes; both within configured 8000 bytes, with shortening notice and intact route footer. Structured presentation retained 14368 UTF-8 bytes. The cached operation was 14495 Unicode codepoints. resources/read on the actual URI with ?offset=0&limit=1000 returned offset 0, next_offset 1000 and 1000 characters; the inner fragment was not parsed as a full operation. After checking this small total size, a separate complete read yielded valid JSON. Its 13945-character issue body equalled the structured operation body. Complete context, plan, schema and refusal cache reads also succeeded. No CLI substitute, multipart assembly or routine hash claim was used.

## Restoration and observations not claimed

The workspace presentation override was restored to its original comment plus empty mapping and restarted. Health confirms structured mode; git_status was clean before this document. Native YAML validation passed on both temporary edits. No production/launcher/state/plan modifications remain. An initial post-restart attempt to scaffold this observation was correctly refused with context_not_loaded/written=false; get_work_context then restored normal admission. Optional resources/templates/list discovery returned method-not-found, while resources/list and actual resources/read worked. This initial comparison did not inspect the catalog. The subsequent bounded catalog observation below covers fresh protocol connections; no universal client support, cache-failure recovery, complete oversized instructional text or final owner release acceptance is claimed.

## Catalog, quality and input validation — 2026-10-21

The owner requested these bounded probes and discussion before any phase transition or test-wheel preparation. Source code remains the candidate above; observation-only commit 02568afeda946d4c9ad48a4c450bbec7d3d53178 does not change running code.

### Native catalog

A temporary stdin-fed Python smoke command used the existing ServerProcess fixture to launch the configured .venv315 Python with -m mcp_server.core.proxy twice, sequentially, against this workspace. Each child received its own PGMCP_RESPONSE_MODE, followed initialize, tools/list and tools/call health_check, and closed through the existing context manager. It did not invoke pytest, save a new script/test, replace the active connection or edit the shared default.

| Observation | structured | resource |
| --- | --- | --- |
| Published tools / unique names | 49 / 49 | 49 / 49, identical name set |
| Tools with outputSchema | 49 | 0 |
| Health structuredContent | Present | Absent |
| Health response | isError=false; structured envelope validates against the advertised health schema | isError=false; expected text-only operation route |

The probe exited 0. Schema presence was inspected for all 49 tools; response-to-schema validation exercised health_check only. This is native catalog evidence from two fresh protocol connections, not proof that this Codex chat refreshed an already cached catalog. The actual agent response/cache paths were separately observed in the earlier round.

### Live quality calls

run_checks(scope='targets', targets=['docs/development/issue536/live-observations.md'], checks=['markdown_links'], timeout_seconds=120) returned operation success=true, run_status=passed, native exit 0. Its only discovered URI was an excluded schema identity: zero successful links, one protocol exclusion, zero errors. This proves invocation/reporting, not meaningful document link coverage.

A second equally narrow call selected only [the current presentation reference](../../reference/presentation_architecture.md), with the same check and timeout. It returned success=true, run_status=passed, native Lychee 0.24.2 exit 0, 26 successful link occurrences, two configured schema-protocol exclusions, zero errors. No native policy, exclusion or scope was broadened to produce success; no full suite ran. Link results are not a claim of semantic document quality.

### Live invalid model input

get_project_plan(issue_number='536-not-an-integer') through the actual Codex tool connection returned MCP isError=true, structured success=false, error_type=ValidationError and validation_errors naming issue_number with its integer-type failure. A separate schema://validation embedded resource contains the complete advertised GetProjectPlanInput JSON Schema; structured attachments references its URI/MIME without another attachment body. The diagnostic includes the rejected input, so an agent can correct it.

A subsequent valid get_project_plan(536) succeeded, still Research with other phases pending and planning_deliverables=null. health_check confirmed healthy structured output from the unchanged active child PID 22824. git_status was clean before recording this addition. No phase/state/planning/configuration mutation, production repair, wheel preparation or owner acceptance followed these probes.


## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-21 | @imp researcher | Record paired live requests, byte counts, real cache readback and configuration restoration. |
| 0.2 | 2026-10-21 | @imp researcher | Record native two-mode catalog discovery, meaningful focused link evidence and actual agent input rejection; preserve limitations and phase boundary. |
