<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 507 — Test-harness diagnostic classification

**Status:** RESEARCH — APPROVED; BOUNDED CHECKER IMPLEMENTATION VERIFIED  
**Version:** 0.9  
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
- Deferred: [issue513](https://github.com/MikeyVK/phase-gate-mcp/issues/513) records SDK2
  and higher-Python assessment for the next major, high priority and first after508.
- Next: commit/push Research and obtain independent QA; no phase progression on a
  producer-delegated review or an older issue's verdict.

## Questions

Independent QA issued GO for Research to Implementation on70ee58e5. Coordination
published [assessment issue513](https://github.com/MikeyVK/phase-gate-mcp/issues/513),
priority high, first after the current sequence/#508 closeout, for the next major.

Implementation exposed an additional Python typing boundary. With the approved3.13
checker settings, targeted Ruff reports UP046 on ToolExecution and InputValidationDecorator;
targeted Mypy reports "Cannot use a covariant type variable as a parameter" for
ToolExecution.operation. An isolated diagnostic check of the same changed file with
python_types args ["--python-version","3.11"] passes. This is comparison evidence,
not a waiver of the3.13 gate. Static source inventory finds Generic class declarations
in13 production files; it does not establish13 failing files or justify a broad rewrite.
Ruff documents that PEP695 migration may change variance and marks its fix unsafe:
[UP046](https://docs.astral.sh/ruff/rules/non-pep695-generic-class/).

The owner chose to retain3.13 and investigate the smallest correct checker adjustment.
No generic contracts or runtime compatibility code have been changed in response.
The remaining decision is focused checker policy versus an explicitly scoped typing migration;
the Python baseline remains3.13.

A reversible native-config probe enabled Pydantic's bundled Mypy plugin. ToolExecution
passed unchanged at3.13; all seven changed production files also passed. A further probe
with init_typed=true and init_forbid_extra=true passed the same seven files, retaining
typed constructors and rejecting extra constructor keywords instead of relaxing them.
Mypy1.19.1's dataclass plugin synthesizes __replace__ for Python>=3.13; the installed
Pydantic2.11.7 plugin replaces generic dataclass-transform handling with model-specific
analysis. No dependency install or runtime model change is needed for the plugin.
All temporary config edits were restored after the checks.

A bounded syntax inventory used files returned by:
rg -l 'TypeAlias|TypeVar\\(|Generic\\[' mcp_server -g '*.py'.
Passing those29 explicit production targets to
run_checks(scope='targets',checks=['python_lint'],
args={'python_lint':['--select','UP040,UP046,UP047','--statistics']},
timeout_seconds=180) reports15 UP040,13 UP046 and8 UP047:36 syntax-migration findings.
This is not a workspace gate or a count of broken type contracts. Ruff marks these
migrations unsafe because they can change variance and/or runtime alias behavior.

Earlier unapproved option, superseded by the bounded rule proposal below:
enable plugins=['pydantic.mypy'] with
[tool.pydantic-mypy] init_typed=true and init_forbid_extra=true; intentionally retain
supported explicit-TypeVar/TypeAlias syntax by excluding only UP040/UP046/UP047 in
native Ruff config. Other rules and strict Mypy/Pyright settings remain active.
This is an explicit syntax-policy choice, not an already approved gate waiver.
No broad PEP695 migration, per-class suppression campaign or new framework is proposed.

Probe evidence:
- run_checks(scope='targets',targets=['mcp_server/core/tool_execution.py'],
  checks=['python_types'],timeout_seconds=180), with temporary plugin config:
  passed, native exit0. Supplemental917b6555ecf34da4b813a978096a622b.
- The same check on the seven changed production files listed in Consumer and
  verification boundary passed with the plugin alone and with both strict plugin
  options; native exit0. Supplemental91ac61c4ff8b417682cc0ac60034c59d and
  5ee2a6c30d5f403f86730d2db987a3b7.
- run_checks on the18 changed Python files, checks=['python_format','python_lint'],
  args={'python_lint':['--extend-ignore','UP040,UP046,UP047']},timeout_seconds=180:
  both passed, native exit0. This caller-argument experiment is not a configured gate
  pass; no permanent rule selection has yet changed. Supplemental42f8c1f3891140138cb3c01df7f81159.
- At this checkpoint there was no additional test execution or broad check campaign;
  the subsequent owner-requested three-case comparison is recorded below.

Primary references:
[Pydantic Mypy integration](https://docs.pydantic.dev/latest/integrations/mypy/),
[UP040 runtime/typing caveats](https://docs.astral.sh/ruff/rules/non-pep695-type-alias/),
[UP046 variance caveats](https://docs.astral.sh/ruff/rules/non-pep695-generic-class/).
Workspace-wide confirmation remains for the required Validation phase.

### Representative PEP695 comparison (2026-10-16)

Owner request: establish contract preservation with three targeted experiments before
approving a broader migration or a permanent Ruff policy. Temporary candidates under
.pgmcp/temp/artifacts/test_issue507_pep695_probe.py reproduce ToolExecution,
AdapterBinding and FrozenJsonValue with the new syntax; production declarations are
unchanged. Runtime: Python3.13.7/Pydantic2.11.7. Static checkers: Mypy1.19.1 and
Pyright1.1.408. The probe is not added to the durable test suite.

| Case | Observed runtime comparison | Observed static comparison at3.13 |
| --- | --- | --- |
| ToolExecution | Construction, dumps, frozen assignment rejection, invalid operation/extra-field rejection and operation_output_model metadata/schema agree. | Both checkers accept current ToolExecution[DetailedOutput] as ToolExecution[BaseOutput]; both reject that assignment for the PEP695 candidate as invariant. Reverse assignments and the BaseModel bound remain rejected in both forms. |
| AdapterBinding | Identity/launch/capability fields and frozen assignment rejection agree. | Both checkers accept current AdapterBinding[DetailedOutput] as AdapterBinding[BaseOutput]; both reject that assignment for the PEP695 candidate as invariant. Reverse assignments remain rejected. |
| FrozenJsonValue | Recursive freeze/thaw, detached nested containers, invalid JSON/nonfinite numbers, immutable-entry checks, and JsonEvidence construction/JSON serialization/schema properties and definitions agree. | Both checkers accept the mixed immutable tuple/object example and reject mutable list/dict values for both aliases. No alias-contract difference in these probes. |

Reproduction and observed outcomes:
- run_tests(scope='targets',targets=[the temporary probe],tests=['python_tests'],
  timeout_seconds=180): three cases passed in3.90s, native exit0. Supplemental
  d6b836d59f464669889efb54b43c7176.
- run_checks(scope='targets',targets=[the temporary probe],
  checks=['python_types','python_pyright'],timeout_seconds=180): each reports12 errors,
  native exit1. Ten are deliberate negative controls (four reverse assignments, four
  mutable-alias assignments and two invalid bounds); the two additional errors are the
  newly rejected widening assignments above. No other diagnostics.
  Supplemental437d2210ffae4cea9fa8e950b6c9dcca. Positive assignment pattern:
  a function receives ToolExecution[DetailedOutput] and assigns that parameter to a
  ToolExecution[BaseOutput] variable; repeat with the candidate and AdapterBinding.
  DetailedOutput extends BaseOutput with an extra field. Argument variables prevent
  inferred concrete values from masking variance differences.
- On the earlier probe revision, a reversible Mypy plugin configuration with
  init_typed=true/init_forbid_extra=true retained both candidate widening failures.
  It fixes the separately observed current-model declaration diagnostic, but does not
  make the PEP695 candidate preserve covariance. Supplemental32fff1b3303d46cab501c31692b65276.
- A diagnostic comparison of the same three-case source with only caller arguments
  python_types=['--python-version','3.12'] and
  python_pyright=['--pythonversion','3.12'] yielded11 errors per checker: ten deliberate
  controls plus the ToolExecution widening failure. Candidate AdapterBinding widening
  succeeds at3.12. This is a checker comparison, not a lowered supported baseline or
  a3.13 gate waiver. Supplementale11db754d33d42d0a5a4a4757c13bb8d.
- The first runtime attempt failed because the probe requested the full baseline
  ToolExecution envelope's JSON schema, which the baseline itself cannot generate.
  Production unwraps its operation model before schema generation (server/bootstrap).
  Correcting the experiment to that real path passed; this was a probe error, not
  evidence of a PEP695 regression. No production repair was made for it.

PEP695 replaces explicit variance declarations with inferred variance. The dataclass
result agrees with the installed Mypy plugin's Python>=3.13 synthesized __replace__
and the upstream Pyright discussion. The ToolExecution result also occurs with3.12
checker settings; do not attribute that entire result solely to the3.13 change.
The new alias is a TypeAliasType at runtime, but no existing alias-as-isinstance use
was found; such a hypothetical is not presented as an observed production defect.
Sources: [PEP695 variance](https://peps.python.org/pep-0695/#variance-inference),
[Ruff unsafe UP046 migration](https://docs.astral.sh/ruff/rules/non-pep695-generic-class/),
[Pyright frozen dataclass discussion](https://github.com/microsoft/pyright/issues/11011).

Checkpoint before the UP047 follow-up: a syntax-only migration does not preserve the two
explicitly covariant contracts with the installed checkers. Runtime success does not
override that finding. The alias probe supports its specific migration but is not a
suite-wide alias guarantee; generic functions/UP047 were not tested. These findings
justify protecting the affected class contracts, not automatically disabling all three
Ruff rules. The earlier all-three-rule exclusion proposal remains unapproved and must
be weighed separately. No permanent checker config, broader migration or extra suite
tests were applied. All reversible native-config experiments were restored.

### UP047 follow-up and bounded rule proposal (2026-10-16)

The owner approved retaining explicit covariance and requested a targeted UP047
investigation before a per-rule decision. No permanent Ruff exclusion or syntax
migration was authorized by that request.

Fresh rule-only inventory over the same29 explicitly selected declaration files:
15 UP040 aliases in8 files;13 UP046 classes in12 files;8 UP047 functions in6 files.
Invocation: run_checks(scope='targets',targets=the29-file inventory above,
checks=['python_lint'],args={'python_lint':['--select','UP040,UP046,UP047',
'--output-format','concise']},timeout_seconds=180). Ruff0.15.6, native exit1.
Supplemental99f77d2234fd4da8a910407d392eab40. These are migration suggestions,
not36 demonstrated type defects.

The temporary probe is
.pgmcp/temp/artifacts/test_issue507_up047_probe.py/test_issue507_up047_probe.py.
It copies the existing bodies of ordered_mapping, prepare_model_input,
tool_error_handler and _shielded, changing only the function name and local generic
declaration. Imported exception aliases preserve the original error-handler binding.
The private _shielded import has one probe-only reportPrivateUsage exception;
no assignment, inference or generic-contract diagnostic is suppressed.
Candidate declarations use Entry:OrderedConfigEntry, TModel:BaseModel, T and TCleanup,
respectively; class declarations and their explicit TypeVars remain unchanged.

| UP047 surface | Observed comparison |
| --- | --- |
| Bounded mapping and prepared-input closure | Both checkers preserve dict[str,DetailedEntry] and PreparedToolInputContract[DetailedOutput] via assert_type. Runtime preserves explicit ordering/identity, duplicate-rank rejection, paired schema and concrete admission, and rejection of missing/extra fields. |
| Async exception wrapper | Both checkers preserve Callable[...,Awaitable[DetailedOutput]]. Runtime preserves the concrete returned object, functools wrapper metadata and the existing ValueError-to-ToolResult payload. |
| Shielded task result | Both checkers preserve DetailedOutput from Task[DetailedOutput]. Runtime preserves results, exception propagation, rejection of an already-cancelled task, and continuation of inner work after outer cancellation. |

Reproduction/evidence:
- run_tests(scope='targets',targets=[the UP047 probe],tests=['python_tests'],
  timeout_seconds=180):3 passed in4.35s, native exit0; no warnings reported.
  Supplemental7c89d6442e2c4296869efe541d8ea9eb.
- Eight deliberate negative assignments (current/candidate pairs for mapping,
  admitted-model, wrapped-result and task-result types assigned to incompatible str
  destinations) yield exactly8 diagnostics in each checker. Mypy sometimes reports
  the task argument under contextual inference; both reject the same invalid use.
  Supplemental3413073ed0b54ca8ac76ddae2804d33f.
- Removing only those negative controls leaves the positive assert_type checks.
  run_checks(scope='targets',targets=[the UP047 probe],
  checks=['python_lint','python_types','python_pyright'],
  args={'python_lint':['--select','UP047']},timeout_seconds=180):
  all passed, native exit0. Supplemental2e8d913160e04f82b2299c6fed3906b6.
  Mypy1.19.1/Pyright1.1.408; no permanent checker settings changed.
- Runtime coverage directly compares four functions. The other inventoried functions
  (_select, _stop_reason, _stop_protected, _stop) were source-reviewed, not independently
  runtime-proven by this probe. Their bounded/constrained parameters must be preserved;
  in particular TCheck remains constrained to ContentCheckResponse/SelectionCheckResponse.

Proposal subsequently approved by the owner; the implementation outcome below supersedes
the earlier all-three-rule exclusion option:

| Rule | Proposed policy and bounded application |
| --- | --- |
| UP040 | Keep enabled. Address only the15 inventoried aliases, preserving existing consumer behavior. The FrozenJsonValue comparison supports that alias only. Check Pydantic admission/schema consumers explicitly, especially ScaffoldContentInput/ScaffoldContentRequest; do not assume a named TypeAliasType has no effect on schemas. A demonstrated contract change calls for retaining that alias with an exact local exception, not a general ignore or a schema refactor. |
| UP046 | Keep enabled. Retain the explicitly covariant ToolExecution, AdapterBinding and PreparedToolInputContract declarations with declaration-local, reasoned UP046 exceptions. ITool already escapes this diagnostic because it has a defaulted TypeVar; retain its explicit covariance too. Do not classify the other10 findings as broken or exempt them en masse: convert only if the existing variance/bounds/consumer contract remains demonstrably identical; otherwise retain the declaration with a targeted exception. |
| UP047 | Keep enabled; no exclusion currently justified. Convert only the8 inventoried function declarations, retaining their bounds/constraints and bodies. Remove module TypeVars only when actually unused elsewhere; do not touch generic methods which this rule does not flag or convert their owning classes. Verify changed files and existing focused behavior tests. |

This proposal makes no promise that all remaining UP040/UP046 candidates can be
mechanically converted. A changed contract or need for consumer redesign stops that
candidate; it must not be disguised as a safe syntax update. No broad production
rewrite, permanent diagnostic test growth, whole-suite run or phase transition was
performed for this research. Sources:
[typing generic functions](https://typing.python.org/en/latest/spec/generics.html),
[Ruff UP047 scope and caveats](https://docs.astral.sh/ruff/rules/non-pep695-generic-function/).

### Approved rule implementation and focused evidence (2026-10-16)

The owner approved targeted execution of the per-rule proposal, followed by explicit
approval of plugins=['pydantic.mypy'], init_typed=true, init_forbid_extra=true and one
field-local Mypy misc exception preserving AdapterBinding covariance. No global Ruff
ignore, weakened Pyright setting, dependency upgrade or new permanent test was added
for this syntax work. [Issue513](https://github.com/MikeyVK/phase-gate-mcp/issues/513)
now requires reassessment of existing/new global and local checker suppressions.

| Rule | Final bounded treatment |
| --- | --- |
| UP040 | Convert the15 inventoried aliases in8 files. Existing schema/admission, JSON and template consumers pass the focused tests. No UP040 exception. |
| UP047 | Convert the8 inventoried functions in6 files, preserving bodies/bounds/constraints. Keep module TypeVars still used by other methods; no UP047 exception. |
| UP046 | Convert6 classes: InputValidationDecorator, CheckExecution, InvocationCompleted, AdapterResponseContract, _BaseIToolTransition and _BaseTransitionTool. Retain7 exact declarations with reasoned line-local exceptions; no file-wide exclusion. |

Retained UP046 exceptions: ToolExecution, AdapterBinding and PreparedToolInputContract
preserve explicit covariance; ToolErrorHandlerDecorator, ICoreTool and
AdapterRequestContract preserve their existing invariant contracts; AdapterRole avoids
the observed Pydantic2.11.7 validator-type-resolution failure. Existing ITool and
IToolInputContract covariance stays unchanged. ITool now imports TypeVar from typing
because Python3.13 natively supports its existing default parameter (UP035).

Isolated copies of the actual remaining class bodies showed why three invariant
declarations stay: the new ToolErrorHandlerDecorator is inferred covariant; ICoreTool
becomes input-contravariant/output-covariant; AdapterRequestContract becomes contravariant.
No such contract expansion was implemented. The final temporary static comparison
(scope='targets', the UP047 probe, checks=['python_types','python_pyright'],
timeout_seconds=180) reports exactly22 deliberate rejected assignments in each checker,
with no unrelated errors. Supplemental86ac6a29113b4a3ca9d5bac565b77bd5.
Static agreement alone did not establish runtime compatibility for AdapterRole:
after conversion, the targeted behavior run reported19 failures/172passes, all failures
at the catalog/manifest boundary with PydanticUserError requiring CapabilityT.
Restore its original Generic/TypeVar declaration with the local UP046 exception:
the27 catalog tests pass in7.38s. No model_rebuild workaround or new compatibility path.

Focused implementation evidence:
- run_tests(scope='targets',targets=[unit/config/test_ordering.py,
  unit/execution/test_catalog.py,unit/core/test_tool_error_handler_c4.py,
  unit/utils/test_schema_utils.py,unit/services/test_template_graph.py,
  unit/services/test_template_components.py,unit/services/test_artifact_identity.py,
  integration/execution/test_content_input.py,integration/test_schema_public_v3.py,
  unit/execution/test_check_service.py,integration/execution/test_process_stopping.py,
  integration/test_prepared_tool_contract.py,unit/tools/test_transition_phase_tool.py,
  unit/tools/test_cycle_tools_business_logic.py,
  unit/schemas/test_structured_tool_output_migration.py],tests=['python_tests'],
  args={'python_tests':['-r','sxX']},timeout_seconds=300), with every target prefixed
  tests/mcp_server/:191passed in19.77s, native exit0, no warnings/skip/XPASS reported.
  Supplemental fd5b8844983743e48566c8c76a1b78cc.
- run_checks(scope='targets',targets=the25 explicitly changed Python files in this
  syntax slice,checks=['python_format','python_lint','python_pyright'],
  timeout_seconds=180): all passed, native exit0. Supplemental2211a466257f4bcba9f90a416838460b.
- Same targets restricted to the24 production files, checks=['python_types']:
  passed with the approved strict plugin/one local exception, native exit0.
  Supplemental4b78f8ad151043ab87e50708021c6385.
- The original29-file syntax inventory, checks=['python_lint'], configured arguments:
  passed, native exit0. Supplementale9ff183bbecb4b3f8c40cab419b0ab41.
- Final scope covers all41 changed Python files relative to70ee58e5, selected explicitly
  from the branch diff: python_format/python_lint/python_pyright all passed, native exit0
  (ea118b2af74246079d1c9a9b0b4e9647). Filter that set to its29 mcp_server/ production
  files for python_types: passed, native exit0 (c4b5a582ed0c411d88421aeb542c8672).
  Both run_checks calls used scope='targets', configured arguments and timeout_seconds=180;
  no Markdown, workflow JSON or test callers were sent to the production-scoped Mypy gate.
- The first151-test run found one previously missed SchemaAttachment.schema read in
  test_schema_public_v3.py. Correct that existing assertion to schema_document;
  no new case or production contract change. The later191-test run includes it.

All Python changes were reviewed against the pushed70ee58e5 baseline using repository
file reads. Changes remain declarations/imports, exact diagnostic exceptions and the
previously approved #507 maintenance; method bodies were not redesigned for PEP695.
The native test/check outcomes above are focused implementation evidence, not a
workspace Validation verdict. The full configured suite and phase-boundary QA remain
owned by the later workflow gates.

## Approved Strategy

APPROVED BY OWNER in the producer conversation on2026-10-16 and independently reviewed
at70ee58e5. Subsequent typing/checker impact of the Python-floor change is explicitly
reopened under Questions. The owner subsequently approved the bounded per-rule proposal,
retention of explicit covariance, and strict Pydantic Mypy integration plus one localized
Mypy misc exception for AdapterBinding. Preserve existing contracts; present any intentional
contract change before implementation. Other approved boundaries stay binding.

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
| 0.5 | 2026-10-16 | @imp implementer | Link published deferred513; explicitly reopen newly observed Python typing/checker impact without silently changing generic contracts. |
| 0.6 | 2026-10-16 | @imp implementer | Retain owner-chosen3.13; record reversible native plugin/syntax probes and the remaining explicit checker policy choice. |
| 0.7 | 2026-10-16 | @imp implementer | Record owner-requested three-case PEP695 behavior/type comparison, demonstrated variance changes and bounded evidence before a migration/policy decision. |
| 0.8 | 2026-10-16 | @imp implementer | Record approved covariance retention, bounded UP047 function comparisons and a per-rule proposal without global exclusions or automatic class migration. |
| 0.9 | 2026-10-16 | @imp implementer | Record approved per-rule execution, strict Mypy integration, exact contract-preserving exceptions and focused runtime/type evidence. |




