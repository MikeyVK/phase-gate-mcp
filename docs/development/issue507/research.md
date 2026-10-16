<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 507 — Test-harness diagnostic classification

**Status:** RESEARCH — OWNER STRATEGY APPROVED; INDEPENDENT REVIEW REQUESTED  
**Version:** 0.4  
**Last Updated:** 2026-10-16

## Purpose

Bound maintenance to demonstrated harness defects and honest expectations; distinguish production API warnings and intentional contracts.

## Scope In

Fresh targeted diagnostic baseline; restart coroutine/task ownership in existing tests; collection-name collisions; stale XPASS and empty manual placeholder; clean internal schema-field rename; Python >=3.13 and the supported Windows path check; MCP >=1.30.0,<2 and central resource return modernization.

## Scope Out

No zero-warning quota, global filters, replacement test framework, coverage campaign, broad helper/isolation refactor (#250/#140), general process/runtime timeout stabilization, release or automatic deployment. SDK2 migration and a Python floor above3.13 are explicitly deferred to a Coordination-owned assessment issue for the next major pgmcp release.

## Problem Statement

Earlier full suites pass while reporting warnings, a non-strict XPASS, a manual skip and restart-task stderr. Warning counts do not identify causes. Research must distinguish actual test defects from intentional contracts and production API maintenance before repair.

## Goals

- Repair genuine harness coroutine/task lifecycle defects in existing valuable tests.
- Remove false test-collection candidates and stale expectations without production pytest metadata.
- Retain a manual skip only when it protects real executable behavior.
- Modernize the three diagnosed production boundaries within the approved narrow scope; preserve public output and path-safety intent.

## Background

Main includes merged #506 at961d1edf1f17dd3ed1b570827c3da1a058365472. Its full confirmation2915passed/1skip/1xpass/253warnings is history, not #507 evidence. #319 DF-319.4 deferred this classification. #250 owns broader isolation/maintenance and #140 broader coverage debt; neither historical count/threshold is imported here.

## Findings

### Fresh classification

| Signal | Observed cause / responsibility | Proposed disposition |
| --- | --- | --- |
| Unawaited delayed_exit coroutine | unit/tools/test_health_tools.py patches create_task with a plain Mock, which never schedules or closes the supplied coroutine. GC can report it during a later unrelated test. | Fix test ownership at that boundary: consume/close the intentionally unexecuted coroutine. Preserve DTO assertions; no production change. |
| Task exception never retrieved / SystemExit42 | Three tools/test_admin_tools.py tests deliberately raise SystemExit42 from mocked sys.exit inside the real scheduled background task; asyncio.run propagates it but task outcome is not retrieved. | Test-only repair using owned/awaited scheduled tasks and a controlled exit boundary. Preserve marker, response-before-exit, restart marker/exit42 and meaningful audit evidence. Remove obsolete os.execv absence/duplicate test ballast rather than new regression cases. |
| Collection warnings | Imported TestCapability in integration/adapters/test_pytest.py and TestsConfig in unit/resources/test_standards.py look like pytest test classes. | Alias imports/usages locally. Do not put __test__ metadata into production models. |
| Non-strict XPASS | test_enforcement_runner_unit.py's note-rendering test is marked xfail for unrelated old neutralize_to_base behavior and has duplicate asyncio markers. It currently exercises NoteContext.render_to_response and passes. | Remove stale xfail/duplicate mark; describe the actual public rendering contract. No expectation for obsolete commit behavior. |
| Manual skip | core/test_proxy.py's TestProxyIntegration checks RUN_MANUAL_TESTS then contains comments only. With the flag enabled it would pass without execution/assertions. | Approved: remove the empty placeholder; do not claim manual restart coverage or build a replacement integration scenario. Retain other proxy tests. |
| Historical stale asyncio marks | Recent full output does not contain this warning; current module-wide marks inspected in create_issue_e2e and create_issue_label_assembly apply to async tests. | No demonstrated current defect; no general marker sweep. |
| SchemaAttachment.schema shadow warning | core/tool_execution.py intentionally replaces BaseModel's deprecated schema() method; the field is explicit in #460 shared contracts and used by attachment producers/presenter. | Approved clean rename to schema_document with direct constructors, presenter and existing test callers; remove collision-specific suppressions. No alias or public operation DTO change. |
| PureWindowsPath.is_reserved deprecation | Real production path safety in utils/path_resolver.py; package supports Python>=3.11. Replacement os.path.isreserved is Windows-only and added in3.13; old method is scheduled for removal in3.15. | Approved Python>=3.13 with aligned checkers/setup docs and os.path.isreserved under the existing Windows boundary. Review changed filename acceptance explicitly; no compatibility bridge or weaker guard. |
| SDK read_resource deprecation | Real production server.py handler returns str. Installed SDK1.25.0 accepts Iterable[ReadResourceContents] and warns for str/bytes. This is not caused by test assertions. | Approved MCP>=1.30.0,<2 and one central SDK-specific return wrapper. Keep resource classes returning text and preserve URI/MIME/content/error behavior; actually verify against1.30. |

Repeated worker warnings are multiple occurrences of a family, not independent bugs.
The selected94warnings comprise9schema-shadow,45SDKresource,39Windowsreserved-path and1unawaited-coroutine occurrences. Their count is scoped evidence, not a workspace acceptance target.

### Production boundary findings

SchemaAttachment's source comment acknowledges the BaseModel.schema collision and two
targeted type-checker suppressions. The #460 design records the field name but the
inspected material provides no functional reason to retain that spelling. Three production
constructors and the schema resource presenter's read access need the clean rename;
type-only consumers need no signature change. Three existing test modules construct it.

Recent native traces use Python313 and only Python313 is present under the inspected
local installation directory. Raising the declared floor from3.11 to3.13 removes the
3.11/3.12 support promise. Mypy, Ruff, Pyright and setup prerequisites must agree.
Older server environments need interpreter/environment/launch-path updates; application
code may use a separate environment. No interpreter migration was performed here.
Windows-only os.path.isreserved, available since3.13, covers more invalid name forms;
verify the filename acceptance boundary with existing meaningful path tests.

The SDK1.0/1.2 handlers accept str/bytes; SDK1.3 and1.30 support
Iterable[ReadResourceContents]. The current1.30 handler derives the public URI from the
request and defaults string content to text/plain. Explicitly retain that MIME at the
central boundary rather than silently switching to a resource's advertised MIME.

### Preparing the resource boundary for SDK2.3

The pinned SDK2.3 low-level signature returns ReadResourceResult (or InputRequiredResult);
SDK1.30's decorator expects str/bytes or an iterable of ReadResourceContents, not that
result model. Therefore a single SDK return object is not a supported common contract.

The minimal preparation uses the existing separation: BaseResource.read remains
SDK-independent text, while server.py alone performs the SDK1.30 wrapping with explicit
text/plain. A later SDK2 change replaces that boundary packaging/registration with the
protocol result object; it need not migrate resource classes. No new transport-neutral
DTO, extra resource facade, version switch, adapter registry, dual implementation or
future-only helper is justified. Existing integration tests must assert resource content,
requested URI, MIME and errors rather than add assertions for internal SDK1 wrapper types.
No claim is made that future migration will require no further integration/test work.

Primary sources:
- [Windows reserved-path API](https://docs.python.org/3.13/library/os.path.html#os.path.isreserved)
- [SDK1.30 resource handler](https://github.com/modelcontextprotocol/python-sdk/blob/v1.30.0/src/mcp/server/lowlevel/server.py)
- [SDK2.3 resource signature](https://github.com/modelcontextprotocol/python-sdk/blob/v2.3.0/src/mcp/server/lowlevel/server.py)
- [SDK migration guide](https://py.sdk.modelcontextprotocol.io/migration/)

### Consumer and verification boundary

Existing harness tests: tools/test_admin_tools.py, unit/tools/test_health_tools.py,
unit/managers/test_enforcement_runner_unit.py, core/test_proxy.py,
integration/adapters/test_pytest.py and unit/resources/test_standards.py.
Adapt valuable behavior; remove demonstrated empty/obsolete ballast. No new fixture
framework, global reset/filter or production restart/exit change. Collection-only results
are not executed test evidence.

Schema rename: core/tool_execution.py, tools/template_schema_tool.py, tools/scaffold_tool.py,
core/decorators/input_validation_decorator.py, presenters/schema_resource_presenter.py;
existing constructors in unit/test_presenter.py, unit/presenters/test_text_presenter_composition.py
and integration/test_tool_attachment_transport.py follow mechanically. Types in presenter
interfaces remain unchanged.

Python/API boundary: pyproject.toml, pyrightconfig.json, utils/path_resolver.py, relevant
setup documentation and existing path behavior tests. MCP resource boundary: server.py and
pyproject.toml; existing server startup/project-plan/cache/presentation/transport tests
exercise actual SDK wrapping. Resource implementations and public operation DTOs remain
unchanged. The concrete dependency upgrade must execute tests with SDK1.30, not merely
edit the declared requirement. A server upgrade/restart must preserve client access.

Implementation uses narrow tests and file gates; no extra old-behavior regression cases.
Validation owns the required full configured native suite and filtered branch/configured
production gates, preserving native arguments, coverage and the1200-second execution
budget within the1800-second client window. No broad Research test campaign.
The earlier #506 PID-readiness failure is not a presumed defect to fix here: no recurrence
was seen in its unchanged full confirmation and the cause remains unproven. Preserve and
investigate diagnostics if it recurs during required Validation.

### Execution checkpoint

- Issue/branch/parent: #507; chore/507-test-harness-restart-diagnostics; main.
- Phase/baseline: Research;961d1edf1f17dd3ed1b570827c3da1a058365472.
- Artifacts: this Research; #506 Validation is historical input only.
- Owner strategy: approved for the explicitly bounded maintenance below.
- Production/tests: unchanged; only targeted baseline and source inspection so far.
- QA boundary: Research to Implementation; separate independent review requested.
- Deferred: owner authorized Coordination to create an assessment issue for SDK2.3 and
  Python above3.13 for the next major pgmcp release. Administrative issue link pending.
- Next: commit/push Research and obtain independent QA; no phase progression on a
  producer-delegated review or an older issue's verdict.

## Questions

No unresolved owner decision for the bounded #507 scope. Independent QA and the
Coordination-issued deferred assessment link remain pending.

## Approved Strategy

APPROVED BY OWNER in the producer conversation on2026-10-16. The SDK1.30 choice and
explicit deferred major-release assessment close the remaining Research decision.

The owner approved the focused harness repairs, removal of the empty manual placeholder
without a replacement integration test, clean renaming of SchemaAttachment.schema to
schema_document with its direct consumers, and Python >=3.13 with aligned checker/setup
requirements and the supported Windows reserved-path API. Preserve schema content, public
operation DTOs, resource URI/MIME, restart/exit behavior and meaningful behavior coverage.
No alias/compatibility bridge, broad test rewrite, global warning filter or zero-warning
quota. The earlier test-only/retain recommendations in Findings are superseded by these
owner decisions.

The owner approved MCP>=1.30.0,<2 and resource modernization at the existing server
boundary. Investigate future readiness without introducing SDK2 code now. SDK2.3 and a
higher Python baseline are explicitly deferred for assessment before the next major pgmcp
release; Coordination owns the separate issue. No SDK upgrade or implementation has
been performed in Research.

### SDK upgrade and host compatibility follow-up

As checked on 2026-10-16, PyPI lists stable MCP 2.3.0 (2026-10-02) and latest 1.x
1.30.0 (2026-09-07). Installed 1.25.0 dates from 2025-12-19. The inspected 1.30 source
retains the decorator, request_handlers and ReadResourceContents APIs used here.
The 1.27 notes include stdio invalid-input and mid-request transport-close handling.
The 1.30 notes include schema-reference, redirect, OAuth and HTTP-session changes;
HTTP/OAuth fixes must not be presented as established vulnerabilities in this stdio
server. Source inspection is feasibility evidence, not a completed upgrade test.

SDK2 is a material migration for pgmcp: constructor handler registration replaces
decorators, results become explicit protocol result objects, request_handlers disappears,
protocol model attributes change and resource handlers return ReadResourceResult.
The directly coupled production surfaces are server.py, utils/mcp_converters.py and
core/proxy.py; existing transport/integration tests use the affected SDK models and handler
registry. Thus the earlier one-item ReadResourceContents proposal applies to SDK1,
not unchanged to SDK2. Do not enlarge this Chore into that migration without approval.

A server's Python SDK version and a host's SDK version need not match. Separate processes
exchange MCP messages; compatibility requires shared protocol/transport/capabilities and
valid payloads. SDK1.30's supported-version list retains 2024-11-05, 2025-03-26 and
2025-06-18 alongside LATEST_PROTOCOL_VERSION. Raising the server dependency floor
therefore does not by itself exclude a host using an older SDK. An environment that
installs server and client into one Python environment can still have a package constraint
conflict; an isolated server environment avoids that coupling. No harness compatibility
matrix or live 1.30 handshake has been executed yet.

Owner-approved target: MCP>=1.30.0,<2 for this bounded issue. Verify the actual1.30
environment with existing server/resource/proxy behavior. Prefer prompt review of maintained-line updates, prioritize applicable security
fixes, and treat major upgrades as explicit boundary migrations. A lower-bound declaration
does not upgrade already-installed satisfying dependencies by itself. It also does not
claim that only the tested patch will ever be installed. No updater, scheduled automation,
lockfile or new compatibility layer is proposed.

Primary sources:
- [Published SDK versions](https://pypi.org/project/mcp/)
- [SDK 1.27 release](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.27.0)
- [SDK 1.30 release](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.30.0)
- [SDK 1.30 supported protocols](https://github.com/modelcontextprotocol/python-sdk/blob/v1.30.0/src/mcp/shared/version.py)
- [Protocol negotiation](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#version-negotiation)
- [SDK2 migration](https://py.sdk.modelcontextprotocol.io/migration/)


## Expected Results

Targeted collection no longer misidentifies production classes. Restart tests own/consume
created coroutines/tasks and preserve observable protocol/audit facts. The stale XPASS
becomes an ordinary meaningful pass; the empty manual placeholder is removed without a
replacement scenario. SchemaAttachment no longer shadows BaseModel.schema. Python>=3.13
requirements agree and the Windows filename guard uses a supported API. Resource reads
through actual SDK1.30 retain content/URI/MIME/errors without the deprecated return form.
No zero-warning quota or unexecuted future compatibility claim.

## Evidence

### Both collection-name collisions reproduce.

27 tests collected, zero tests executed, exit0 in0.21s. Warnings: SchemaAttachment.schema shadow, TestCapability and TestsConfig collection. Supplemental d1972a95fb474f88955ccd75e08178d7.

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/integration/adapters/test_pytest.py','tests/mcp_server/unit/resources/test_standards.py'],tests=['python_tests'],args={'python_tests':['--collect-only','-q']},timeout_seconds=180).

### Fresh focused baseline separates test outcomes from diagnostics.

37passed,1skipped,1xpassed,94warnings,39items,33.25s,nativeexit0. Skip source is empty manual placeholder; XPASS reason is stale; unawaited coroutine reported later during unrelated test due to GC. Supplemental32186dd47f29453e83407c72f6c9e164.

- [Unowned restart coroutine](<../../../tests/mcp_server/unit/tools/test_health_tools.py>)
- [Stale expectation](<../../../tests/mcp_server/unit/managers/test_enforcement_runner_unit.py>)
- [Manual placeholder](<../../../tests/mcp_server/core/test_proxy.py>)

**Invocation:** run_tests(scope='targets',targets=["tests/mcp_server/tools/test_admin_tools.py","tests/mcp_server/unit/tools/test_health_tools.py","tests/mcp_server/unit/managers/test_enforcement_runner_unit.py","tests/mcp_server/core/test_proxy.py","tests/mcp_server/integration/test_project_plan_readback.py","tests/mcp_server/integration/test_cache_fidelity_v3.py","tests/mcp_server/integration/test_execution_presentation_v3.py","tests/mcp_server/unit/services/test_artifact_target_resolver.py"],tests=['python_tests'],args={'python_tests':['-r','sxX']},timeout_seconds=300).

### Restart stderr is caused by explicit test exit doubles.

6passed,9schema warnings,12.83s,nativeexit0. Native stderr section contains three restart markers and three task-not-retrieved traces, each ending at test mock_exit raising SystemExit42. This is not an established production restart incident. Supplemental b5b2b6e543334f1e84786facc55600a6.

- [Existing restart tests](<../../../tests/mcp_server/tools/test_admin_tools.py>)
- [Production restart boundary](<../../../mcp_server/tools/admin_tools.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/tools/test_admin_tools.py'],tests=['python_tests'],args={'python_tests':['-s','--log-cli-level=ERROR']},timeout_seconds=180).

### Production deprecations require real contract choices.

Baseline installed SDK1.25.0 accepts str/bytes or Iterable[ReadResourceContents]; the
string path creates text/plain. Source inspection subsequently confirmed SDK1.0 does not
support the replacement and SDK1.30 does. The Python baseline still declares>=3.11 in
unchanged code; the approved implementation raises that to3.13. Source feasibility is
not upgrade execution evidence.

- [Current declared support](<../../../pyproject.toml>)
- [SDK handler consumer](<../../../mcp_server/server.py>)
- [Windows path safety](<../../../mcp_server/utils/path_resolver.py>)
- [Python pathlib deprecation](<https://docs.python.org/3.13/library/pathlib.html#pathlib.PurePath.is_reserved>)
- [Python replacement availability](<https://docs.python.org/3.13/library/os.path.html#os.path.isreserved>)

## Related Documents

- [Issue507](<https://github.com/MikeyVK/phase-gate-mcp/issues/507>)
- [Broader maintenance250](<https://github.com/MikeyVK/phase-gate-mcp/issues/250>)
- [Coverage140](<https://github.com/MikeyVK/phase-gate-mcp/issues/140>)
- [Prior506evidence](<../issue506/validation.md>)
- [Approved attachment contract460](<../archive/issue460/design-shared-contracts.md>)
- [Architecture](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp researcher | Record targeted native baseline, causal harness findings, production warning limits and two owner choices. |
| 0.2 | 2026-10-16 | @imp researcher | Record approved placeholder removal; reassess schema naming, Python baseline impact and verified SDK resource API history for owner discussion. |
| 0.3 | 2026-10-16 | @imp researcher | Capture approved schema rename/Python 3.13 boundary; assess current SDK releases, SDK2 migration and host protocol independence before final SDK decision. |

| 0.4 | 2026-10-16 | @imp researcher | Finalize owner-approved SDK1.30 strategy, minimal SDK2 resource-boundary preparation and deferred major-release assessment; reconcile superseded recommendations. |
