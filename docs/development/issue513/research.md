<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 513 — MCP SDK and Python Baseline Assessment

**Status:** Research in progress — source-removal impact measured; owner policy and delivery decisions pending  
**Version:** 0.7  
**Last Updated:** 2026-10-17

## Purpose

Assess upgrade boundaries and checker exceptions before choosing a bounded delivery strategy for the next major release.

## Scope In

MCP SDK 2.3 assessment against the final #507 baseline; Python versions above 3.13; impact of removing all active global and local checker suppressions, including differences caused by the aligned candidate versions. Inventory and synthetic rule controls alone do not complete that source-impact assessment.

## Scope Out

No production migration, active-environment dependency upgrade, release/deployment, compatibility bridge, new framework, or permanent diagnostic-suite expansion. Research remains open.

## Problem Statement

SDK 2.x and a higher Python floor can improve supported infrastructure, but change different contracts. A package-version bump alone cannot establish pgmcp compatibility, supported harness behavior, or preservation of existing type contracts. The complete suppression inventory must be reassessed rather than treating historical approval or local placement as sufficient justification.

## Goals

- Separate executed compatibility facts, source-backed impact, proposed choices and owner-approved strategy.
- Identify the smallest affected production boundaries and direct/indirect test consumers.
- Compare actual candidate execution and preserve meaningful negative diagnostic signals.
- Finish with an explicit human decision per boundary; do not automatically migrate or progress.

## Current Decision Proposal

**Owner scope decision:** migration implementation will not occur in #513; plan targeted follow-up issue(s). The complete global/local suppression-removal impact assessment remains in #513. The recommendations below are not blanket approval to retain exceptions or to change production contracts.

This is the concrete proposed outcome of Research, **not owner approval or an implementation/release commitment**. The latest-alignment experiments replace the earlier old-pin-led recommendation. No additional combination matrix is needed for this proposal.

| Boundary | Recommended strategy for owner decision |
| --- | --- |
| Python/dependencies | Target Python>=3.15 with the coherent current stable snapshot above. Update project/native-checker/adapter prerequisites consistently; no bridge for a3.13 production deployment. Installation and full migrated-application verification remain delivery gates. |
| SDK API | Cleanly replace SDK 1 handler registration/result/field contracts at the existing server, converter and proxy boundaries. Keep managers/tools/presenters free of SDK-specific adaptation. Adapt valuable existing consumers; do not recreate request_handlers. |
| Protocol lifecycle | Preserve the initialized2025-11-25 operation already demonstrated through SDK 2 native support. Do not add a pgmcp compatibility layer. Initialization-free2026 lifecycle/proxy support is a separate explicit scope; adopting SDK 2 does not automatically implement it. |
| YAML installation | Use the supported PyYAML pure-Python installation route on this Windows3.15 target until a supported wheel exists. pgmcp already selects SafeLoader/SafeDumper and their own subclasses, with no C-loader/dumper selection; this does not require changing its parser implementation. Document/install the prerequisite explicitly. |
| Type contracts / necessary cleanup | Preserve covariance and intentional protocol variance. Remove proven redundant annotations, narrow five broad ValidationError tests and make the three newly selected Ruff style corrections. Align the local GitAdapter variable annotation without changing accepted values. |
| None input contract | Proposed clean break: remove the no-model/None admission-to-core route and its test-only consumers; use typed empty models for no-argument tools. All 49 production args_model properties already return models. This is a small but real internal contract choice requiring owner approval, not an automatic lint fix. |
| Wider checker/test policy | Complete the removal-impact assessment for all global and local suppressions within #513, against actual affected source and the relevant baseline/candidate versions. Synthetic controls establish diagnostic sensitivity, not full source impact. Remediation may be split into later issues; neither retention nor deferral of the assessment is approved. Distinguish static test diagnostics from runtime failures. |

**Why separate delivery scope:** #513 is explicitly a research/decision chore. SDK boundary and prerequisite migration are substantive refactor delivery; they should be scoped from this decision with Design/Planning and existing phase-boundary QA. This issue does not silently become an open-ended suppression-cleanup or new protocol architecture project. Follow-up issue administration remains with Coordination after owner approval.

**Bounded acceptance for delivery:** clean install with the agreed prerequisite route; actual migrated server initialize/list/call/read-resource/error behavior; initialized proxy restart, cancellation and process cleanup; preserved type widening/rejection controls; targeted existing consumers and the workflow-owned full Validation gates. A package-wide migrated-server pass has not yet been claimed. There is no release authorization.

### Actual suppression-removal impact and policy discussion

The [actual-source measurements](suppression-inventory.md#actual-source-removal-impact-2026-10-17) now cover473 source files, all local directive locations and the global settings' actual affected scope. This supersedes earlier synthetic-control-only assumptions.

| Surface | Confirmed effect | Proposed discussion |
| --- | --- | --- |
| Ruff local removal |+188 diagnostics on both reference and aligned stacks. The root tests/conftest.py adds3 previously omitted PLC0415 comments;281 comments/77 files are now indexed. | Retain behavioral/error/variance contracts; distinguish delayed imports from ordinary local imports. Source-removal diagnostics do not prove safe hoisting. |
| Ruff test ANN/ARG exemption removal |Further+98 diagnostics on either stack:26 annotation and72 unused-argument findings. | Consider stricter ordinary test-helper annotations separately from fixture/interface/dynamic-boundary exceptions. |
| Global/local overlap |Removing global ANN/ARG exemption while retaining local comments changes RUF100-unused19 to7. Twelve formerly redundant test comments become effective. | Decide the final test policy before deleting those12 comments. |
| Mypy local removal |Reference:71 new diagnostics and4 unused-ignore messages disappear. Candidate:67 new and8 unused-ignore messages disappear. | Preserve deliberate invalid/frozen/abstract test cases; fix preparation types and remove only redundant whole ignores/codes. |
| Mypy test override removal |Exactly3 extra untyped-definition diagnostics on either stack. | Small helper-annotation cleanup is a concrete alternative to retaining a test-wide relaxation. |
| Pyright global/local removal |On191 production+10 locally suppressed tests:0/1 retained,7/8 without local directives,1294/869 after also deleting false settings (reference/candidate). | Restore basic argument/call/attribute signals through bounded delivery; classify correlated Unknown/dynamic-boundary diagnostics before committing to broader hardening. These are diagnostic counts, not runtime defects. |
| Four Pyright native-default-none rules |Deleting their false settings does not enable them. Explicitly opting in adds195 diagnostics on either stack. | New style/construction policy must be an explicit choice, not disguised as suppression removal. |
| Type boundary |input_validation_decorator.py:115 passes None to an ICoreTool bounded by BaseModel. Both checkers expose it once unmasked. All49 production tools already supply models; prior None consumers are tests. | Owner decision required before deleting the None-input route or widening the core contract. No implicit contract change. |
| Defensive runtime checks |23 unnecessary-isinstance and4 unnecessary-comparison signals remain on either stack. | Preserve actual runtime validation; choose boundary typing/scoped policy after source review rather than remove guards for a static rule. |

The full explicit Mypy test survey is outside the configured production gate: retained1071 reference /618 candidate diagnostics are mostly existing test-typing findings. They are not caused by suppression removal and are not a requirement to repair1071 tests. Final details distinguish native completed diagnostic failures from outer research-probe completion and exclude preliminary wrong-CWD/stale-venv measurements.

Candidate retained-view differences include21 extra Ruff messages (10 ISC004,11 UP037) and a Pyright contextmanager return-annotation deprecation at template_activation.py:257. These are separate migration findings. SDK2 constructor typing rejects several old alias spellings even where prior converter runtime probes accepted them; do not conflate static incompatibility with independently observed runtime failure.

No production or permanent test changes, active-config edits or migrations were made. The existing covariance decision remains binding. Actual import-hoisting behavior, final per-boundary disposition and owner approval remain open; migration execution is delegated to later scoped issues.

## Background

Issue #507 is closed and delivered Python >=3.13, MCP >=1.30,<2, the central ReadResourceContents boundary, schema_document, strict Pydantic Mypy constructor policy and seven local UP046 exceptions. Historical pending wording in #513 does not reopen that work. Local baseline: Python 3.13.7, MCP 1.30.0, Pydantic 2.11.7, Ruff 0.15.6, Mypy 1.19.1 and Pyright 1.1.408.

## Findings

### Current candidates and independent decisions

| Boundary | Established fact | Decision still required |
| --- | --- | --- |
| SDK target | MCP 2.3.0 is the current verified stable candidate. It installed and executed on existing Python 3.13.7. | Migrate, defer, or select another target after remaining boundary probes. |
| Dependency environment | The isolated SDK install resolved Pydantic 2.14.1 and additional SDK dependencies. The project still declares mcp<2. | Candidate project dependency resolution and deployment strategy; SDK-only installation is not whole-project compatibility. |
| Python floor | Python 3.15.0 is the latest verified stable release. The unchanged source starts healthy on it with SDK 1.30 and the measured dependency set; SDK 2 requires its separate API migration. | Whether raising the minimum is justified despite the PyYAML installation prerequisite and checker-support limitations below. No floor change approved. |
| Harness compatibility | A native SDK 1.30 client completed a real stdio session with an isolated SDK 2.3 server using protocol 2025-11-25. | Required harness/protocol/capability matrix; package-version equality is not a criterion. |
| Checker policy | Complete baseline index exists; 19 unused Ruff directives were observed. | Every rule/equivalent group still needs a disposition and reassessment trigger. |

### SDK boundary: executed facts

The approved environment is `.pgmcp/temp/issue513/sdk23-py313`. It is separate from the active server environment. Installation used the existing Python 3.13 interpreter and `pip --isolated --no-cache-dir install --index-url https://pypi.org/simple "mcp==2.3.0"`.

Three temporary research cases passed. They are exploratory evidence, not new permanent regression coverage:

1. Candidate-only API/model controls constructed Tool, CallToolResult and ReadResourceResult. URI `research://issue513/example?offset=0`, MIME `text/plain`, resource text `payload` and explicit error flag survived the checked model/wire conversion. Snake-case attributes and `model_dump(by_alias=True)` behaved as expected.
2. Five rejected v1 assumptions were exercised: missing Server.list_tools decorator, missing request_handlers registry, missing inputSchema attribute, ClientRequest.model_validate no longer being the RootModel route, and passing AnyUrl where a resource string is required. The first four produced AttributeError; the last produced ValidationError.
3. The native SDK 1.30 ClientSession launched candidate SDK 2.3 low-level handlers through stdio. Initialization, tools/list, resources/list, resources/read and tools/call succeeded; echo returned `preserved`. A deliberately raised ValueError surfaced as client McpError containing `research513-original-error`; its child traceback was visible on stderr.

This proves that specific old-client/new-server session. It does **not** prove the unchanged pgmcp server starts under SDK 2.3, all harnesses interoperate, or restart behavior is correct. Deliberate negative-case stderr is not an unexpected production failure.

### SDK error and process-session controls — additional execution

Two separate real stdio sessions were opened and closed against fresh SDK 2.3 child servers. Both negotiated 2025-11-25. Explicit `CallToolResult(is_error=True)` returned a normal tool response with `controlled-error`. A missing resource raised client McpError with `research513-resource-error`. Returning the old bare content list from a low-level handler raised McpError with `handler returned list; expected BaseModel, dict, or None`. After each failure, echo still returned `still-responsive`.

This distinguishes intentional tool-error output from protocol error delivery and verifies repeatable fresh-process sessions. It is not a live pgmcp proxy restart/cancellation test. Expected child tracebacks were observed for the deliberate rejected cases.

### Actual pgmcp converter — additional executed comparison

The unchanged `convert_tool_result_to_mcp_result` was imported from repository source in both the baseline and isolated candidate subprocess. Checked output included text, JSON rendered as text, an image, an embedded text resource and `isError=True`. The selected wire fields matched under MCP 1.30/Pydantic 2.11.7 and MCP 2.3/Pydantic 2.14.1. Resource URI `research://issue513/converter?offset=0`, MIME `text/plain` and text `payload` were preserved. Missing image data raised KeyError and an incomplete embedded resource raised ValidationError in both environments.

This supports retaining the converter behavior without a speculative rewrite. It does not establish whole-server compatibility or equality of every SDK model field.

### Production and test impact

| Entry point | Observed coupling | Bounded implication |
| --- | --- | --- |
| [server.py](../../../mcp_server/server.py) | Four decorator registrations, list returns, ReadResourceContents, AnyUrl construction and protocol constructors. | SDK 2 registration/result contracts need an explicit migration; managers and tool business logic need no SDK knowledge. |
| [mcp_converters.py](../../../mcp_server/utils/mcp_converters.py) | Constructs SDK content/results at one outward boundary. | Verify text, image, embedded-resource and isError behavior; do not scatter serialization changes into tools/presenters. |
| [proxy.py](../../../mcp_server/core/proxy.py) | InitializeResult validation and protocolVersion attribute; caches/replays initialization for restart. | Attribute migration is separate from changing supported initialization/restart semantics. |
| Test consumers | AST found 17 test files importing MCP directly; 12 files access request_handlers. | Adapt valuable behavior tests to the selected SDK boundary rather than recreate its removed registry. |
| [test_support.py](../../../tests/mcp_server/test_support.py) | Shared MCPServer construction is an indirect consumer. | Keep SDK-specific setup at shared boundaries where behavior permits; avoid a suite-wide mechanical rewrite. |

Direct test-import index:

- [test_server_startup.py](../../../tests/mcp_server/integration/mcp_server/test_server_startup.py)
- [test_cache_fidelity_v3.py](../../../tests/mcp_server/integration/test_cache_fidelity_v3.py)
- [test_checks_public_v3.py](../../../tests/mcp_server/integration/test_checks_public_v3.py)
- [test_edit_public_v3.py](../../../tests/mcp_server/integration/test_edit_public_v3.py)
- [test_execution_presentation_v3.py](../../../tests/mcp_server/integration/test_execution_presentation_v3.py)
- [test_fixes_public_v3.py](../../../tests/mcp_server/integration/test_fixes_public_v3.py)
- [test_pipeline_e2e.py](../../../tests/mcp_server/integration/test_pipeline_e2e.py)
- [test_project_plan_readback.py](../../../tests/mcp_server/integration/test_project_plan_readback.py)
- [test_scaffold_public_v3.py](../../../tests/mcp_server/integration/test_scaffold_public_v3.py)
- [test_schema_public_v3.py](../../../tests/mcp_server/integration/test_schema_public_v3.py)
- [test_tests_public_v3.py](../../../tests/mcp_server/integration/test_tests_public_v3.py)
- [test_tool_attachment_transport.py](../../../tests/mcp_server/integration/test_tool_attachment_transport.py)
- [test_pipeline_decorators.py](../../../tests/mcp_server/unit/decorators/test_pipeline_decorators.py)
- [test_tool_result_conversion.py](../../../tests/mcp_server/unit/server/test_tool_result_conversion.py)
- [test_validate_tool_arguments.py](../../../tests/mcp_server/unit/server/test_validate_tool_arguments.py)
- [test_server.py](../../../tests/mcp_server/unit/test_server.py)
- [test_cycle_tools.py](../../../tests/mcp_server/unit/tools/test_cycle_tools.py)

Counts reflect direct AST imports, not every import of the local `mcp_server` package. No AST/tokenization errors occurred in the 472-file scan.

### Actual proxy with candidate child and old/new clients

The **unchanged native SDK 1.30 pgmcp proxy** launched an injected SDK 2.3 child server. A real SDK 1.30 client initialized through it, called the restart tool, observed a different executing child PID, then received `after-proxy-restart` from echo and `payload` from resource read. The proxy replayed initialize at protocol 2025-11-25. Requests during replacement received the existing restarting/unavailable error. Windows launcher PID and executing Python PID are different identities; the assertions compare the child's own before/after PID.

A second scenario deliberately replaced the child with a process that exits before initialization. Audit emitted `restart_failed` (first observed reason `stdout_closed`, exit code not yet available at that event); the client received McpError indicating unavailable. This is an intentional negative control, not a new production incident.

A raw pre-initialize `server/discover` request was rejected with JSON-RPC -32000 and structured `ERR_SERVER_UNAVAILABLE / forwarding_unavailable / starting`. The real **SDK 2.3 Client** was then tested through the same native proxy and SDK 2 child:

| Client / mode | Executed outcome |
| --- | --- |
| SDK 1.30 ClientSession initialize | Connected at 2025-11-25, including successful transparent child restart. |
| SDK 2.3 Client default auto | Connected at 2025-11-25 and echoed sdk2-client. Native SDK auto negotiation owns the fallback after discovery rejection. |
| SDK 2.3 Client explicit handshake (SDK option named legacy) | Connected at 2025-11-25 and echoed sdk2-client. No pgmcp bridge was introduced. |
| SDK 2.3 Client forced 2026-07-28 | Failed with ExceptionGroup containing MCPError: proxy unavailable/starting. The initialization-free lifecycle is not admitted by the current proxy. |

The [SDK Client guide](https://py.sdk.modelcontextprotocol.io/client/) describes automatic negotiation; the installed pinned SDK 2.3 `client/_probe.py` confirms fallback on the observed RPC error. Executed results distinguish this supported fallback from assuming all new clients work.

**Scope limit:** these runs retain the proxy's native SDK 1 imports and inject only its child process. They prove current lifecycle forwarding to SDK 2 and the measured client negotiation routes. They do not prove the entire unmodified pgmcp process running with SDK 2. Its protocolVersion attribute still needs migration, and whole-package startup/deployment remains unproved. Cancellation/deadline behavior under the final migrated application also remains open.

A bounded candidate strategy is therefore available: cleanly replace the internal SDK 1 API while preserving initialized 2025 protocol operation through SDK 2's native support. Adding initialization-free 2026 operation can be a separate owner decision. No such migration strategy is approved yet.

### Checker reassessment

See [the complete suppression index](suppression-inventory.md) for every path/line, exact comment, native setting and the 19 RUF100 findings. It records 278 directive-bearing comment lines in 76 files: 201 Ruff, 59 Mypy, 13 Pyright and nine historical Pylint entries; families overlap on four lines.

The Ruff diagnostic preserved existing rule selection and added RUF100. It found exactly 19 unused directives, native exit 1, with no other diagnostic code. This is research evidence proposing annotation removal, not a failed release gate or permission to remove catches.

All ten local Ruff rule groups and all 27 disabled Pyright report flags now have paired positive/negative diagnostic controls. The pinned Pyright strict defaults show **23 actual signal suppressions and four explicit default-none policies**. A targeted SDK 2 check shows that native policy masks four obsolete API accesses; enabling the diagnoses exposes all four while the paired correct source passes.

Six production-source Mypy copies without their nine ignores expose 13 diagnostics. Thirteen Pyright-bearing source copies without local directives/masking type ignores expose seven diagnostics. An additional targeted static check of the 20 original test files containing 50 Mypy directives reports 132 static errors in nine files; this is outside the configured production-only Mypy gate, not 132 runtime test failures.

Provisional recommendations distinguish redundant annotations, intentional test/CLI/interface policy, library/checker limitations and genuine declaration gaps. Four Mypy annotations join the 19 Ruff entries as demonstrated redundant candidates. Five B017 assertions can be narrowed to ValidationError on both Pydantic versions. Full AdapterRole PEP695 conversion still fails under Pydantic 2.14.1, so its exception remains justified. The admitted None core-input path versus a BaseModel-bound protocol is a separate contract-alignment question, not an SDK limitation.

The detailed inventory retains exact sources, controls, scope/outcomes and reassessment triggers. Some source-specific dispositions (especially unexplained local imports and test typing) and the candidate Python/checker comparison remain open. No blanket enabling, global relaxation or silent variance change is proposed.

### Python 3.15: isolated installation and actual execution

The owner approved investigating the **newest stable Python release**. On 2026-10-17, [Python.org](https://www.python.org/downloads/) identifies **3.15.0**, released 2026-10-09; 3.16 is prerelease. Only 3.15 was installed. The [official Windows NuGet route](https://docs.python.org/3.15/using/windows.html#the-nuget-org-packages) supplied standard 64-bit CPython under `.pgmcp/temp/issue513/python315-runtime/tools/python.exe`. Executed version is 3.15.0, MSVC 1951, AMD64, `Py_GIL_DISABLED=0`. This is a conventional GIL build; free-threaded behavior/performance was not tested.

Two venvs, `baseline-py315` and `sdk23-py315`, were created under the same research directory and invoked by absolute path. They use MCP 1.30.0 and 2.3.0 respectively. Both use Pydantic 2.14.1, pydantic-settings 2.13.1, PyYAML 6.0.3, GitPython 3.1.45, PyGithub 2.8.1, Jinja2 3.1.6 and jsonschema 4.25.1. Pydantic 2.14.1 is shared to keep the SDK comparison controlled; the active3.13 environment retains2.11.7. Current Mypy 1.19.1 and Ruff 0.15.6 also installed/imported in the SDK 2/3.15 lab. No active dependency, source, checker pin, PATH or system default changed.

| Installation route with those exact direct pins | Observed result |
| --- | --- |
| pip with `--only-binary=:all:` | No matching Windows CP315 wheel for PyYAML 6.0.3; both resolutions stopped. |
| Ordinary pip installation | PyYAML source build failed because Microsoft C++14+ Build Tools are absent. This establishes an unmet local installation prerequisite, not intrinsic Python incompatibility. |
| Same PyYAML version, process-local `PYYAML_FORCE_LIBYAML=0` | Both environments installed successfully; PyYAML built a py3-none-any wheel. Actual `yaml.__with_libyaml__` is false and YAML load/dump round-trip passed. |
| Dependency consistency with `python -I -m pip --isolated check` outside the source import context | Both isolated dependency sets report no broken requirements. This does not install/validate a migrated pgmcp wheel. |
| pip check with repository metadata visible | SDK 1 set passes; SDK 2 reports the existing pgmcp requirement mcp<2. The visible local egg-info has the older lower-bound wording >=1.0.0; current pyproject requires>=1.30.0,<2. Both exclude2.x. |

The pure-Python build flag is supported by [PyYAML 6.0.3 setup.py](https://raw.githubusercontent.com/yaml/pyyaml/6.0.3/setup.py). It was an explicit lab installation variant, not an approved deployment recommendation or dependency change. No C++ toolchain was installed. Performance parity of the pure-Python parser was not measured.

| Executed boundary on Python 3.15 | Observed result and limit |
| --- | --- |
| Real source imports | settings, ConfigLoader, bootstrap, server, proxy and converter imported under both SDK sets; no warnings in these captured import operations. Import success alone does not prove handler construction. |
| Unchanged CLI/bootstrap with SDK 1.30 | Actual stdio initialization negotiated2025-11-25;49 tools, five resources, healthy health_check, successful cache-reading-guide URI/MIME/text read. Version bypass explicitly false. state.json and deliverables.json bytes matched before/after. |
| Same unchanged CLI/bootstrap with SDK 2.3 | Child exits at server.py:84: AttributeError, Server has no list_resources decorator; client sees connection closed. This reproduces the SDK API boundary and does not establish a Python defect. |
| Minimal native SDK 2 handlers, real SDK 1 client | Initialization, tool listing, echo and resource URI/MIME/text succeed; deliberate ValueError becomes McpError with original message/child traceback; next echo succeeds. This is not the migrated pgmcp application. |
| Unchanged proxy running on 3.15/SDK 1, injected3.15/SDK 2 child | Restart changes executing child PID; proxy replays2025-11-25 initialization; following echo/resource succeed. Existing restarting errors occur during replacement. The proxy has not been migrated to SDK 2. |
| Actual unchanged converter | Checked text/JSON-text/image/resource/error fields preserved under both SDK sets; invalid image/resource controls retain KeyError/ValidationError. |
| Actual AdapterRole source | Retained declaration constructs, serializes, generates schema and rejects five invalid/immutable cases. Full PEP695 conversion still raises class-not-fully-defined PydanticUserError under 2.14.1;3.15 does not remove this workaround. |
| CreateBranchInput/CreateIssueInput source declarations | Valid inputs construct and all five selected invalid inputs raise ValidationError, supporting the narrower B017 proposal on 3.15 too. |
| Current Mypy/Pyright with targetPython3.15 and candidate dependency path | Actual ToolExecution/AdapterBinding widening succeeds; two reversed returns produce exactly two expected errors in each checker. Positive controls have no messages. |
| Ruff 0.15.6 target py315 | Reports the intended PLC0415 negative and no message for its paired positive, but warns3.15 support is under development/may be unstable. Preview was not enabled to hide it. |

**Checker limitation:** the quality calls used the installed adapters: Mypy host3.13, Pyright Node, Ruff native binary. Their target language/dependency path was3.15; the native Mypy process/plugin still used its host Pydantic 2.11.7. Installing/importing Mypy in the 3.15 lab is separate evidence and does not prove its entire execution there. [Mypy 2.4 release notes](https://mypy.readthedocs.io/en/stable/changelog.html#python-3-15-support) explicitly document3.15 support; that newer checker was not installed or approved. Simple target-version acceptance and preserved covariance do not prove all 3.15 language features are supported by current pins.

**Superseded preliminary recommendation:** the earlier suggestion to retain Python>=3.13 relied too heavily on current-pin limitations. The owner redirected Research toward alignment with the newest stable Python and a coherent appropriate dependency/checker set. The earlier measurements remain useful boundary evidence; they do not decide the target against a properly aligned candidate. The next section is the current research direction.

### Current direction: align dependencies and checkers to Python 3.15

The owner selected **latest-stable Python alignment as the research target** and explicitly asked to choose suitable dependencies together and test that combination. This supersedes using old fixed pins as the main basis for a floor recommendation. Production migration, release and the final minimum-support policy remain separate decisions.

A fresh `.pgmcp/temp/issue513/aligned-py315` environment was created using the existing standard CPython 3.15.0 runtime. Pip resolved current stable releases without --pre; the selected versions below were checked against official [PyPI metadata](https://pypi.org/) and [npm Pyright metadata](https://registry.npmjs.org/pyright/latest) on 2026-10-17. SDK/Pydantic stayed within major2. This is a fixed observed research snapshot, not a policy to install floating dependencies in production.

| Boundary | Aligned candidate |
| --- | --- |
| Runtime and protocol | Python 3.15.0; MCP 2.3.0 and mcp-types 2.3.0; Pydantic 2.14.1 |
| Settings / configuration | pydantic-settings 2.16.0; PyYAML 6.0.3; jsonschema 4.26.0 |
| Repository / templates | GitPython 3.2.1; PyGithub 2.10.0; Jinja2 3.1.6 |
| Type/lint tools | Mypy 2.4.0; Ruff 0.17.1; native Node Pyright 1.1.414 |
| Test tools | pytest 9.1.1; pytest-asyncio 1.4.0; pytest-cov 7.1.0; pytest-xdist 3.8.0; coverage 7.16.2 |
| Checker prerequisites | types-PyYAML 6.0.12.20260906; types-jsonschema 4.26.0.20261006 |

PyYAML 6.0.3 is still the latest stable release, so its missing Windows CP315 wheel is not an obsolete-pin finding. The explicit supported pure-Python installation variant was retained for the lab; no compiler was installed. All candidate dependencies install and isolated `python -I -m pip --isolated check` passes. Installation policy for deployment remains open.

Adapter prerequisite declarations are part of alignment: exact old versions are not silently bypassed. The probe copies only each manifest's declared files for Mypy, Ruff, Pyright and Pytest below the lab, then updates only their requirements/package version declarations to the installed candidates. Adapter bodies and active manifests remain unchanged. The final Pytest snapshot retains all five original prerequisite entries. The unchanged catalog computes identities from those candidate bytes and resolves Python explicitly to the candidate interpreter.

Check and test probes call the actual existing **RunChecksTool → CheckOperation/CheckSelector/CheckService → AdapterProcessRuntime** and **RunTestsTool → TestRunManager → AdapterProcessRuntime** paths. The native research test driver launches a candidate subprocess which performs this composition. It is an isolated core-tool/adapter execution, not a fully migrated MCP server or a production gate verdict.

| Aligned execution | Outcome / implication |
| --- | --- |
| Runtime imports, production converter and model controls | Imports succeed without captured import warnings; converter text/JSON/image/resource/error controls preserve the measured fields and negative behavior. Retained AdapterRole and valid/invalid planning-related input models behave as before. |
| Mypy 2.4 actually hosted on 3.15 with Pydantic 2.14 plugin | ToolExecution and AdapterBinding widening accepted; both deliberate narrowing returns rejected. The previous3.13-host limitation is removed for this experiment. |
| AdapterBinding source without ignore | No misc error. The real unchanged production file with its retained ignore reports exactly unused-ignore at execution.py:57. This exception is a demonstrated removal candidate for the aligned baseline; explicit covariance need not change. |
| Ruff 0.17.1 target py315 | Intended PLC0415 negative reported, paired positive clean; no prior under-development warning, no preview flag. |
| Pyright 1.1.414 | Both variance negatives and argument negative reported as intended; paired positives clean. The actual 1.1.414 adapter identity is confirmed. |
| Five Mypy production copies with local ignores removed, with current stubs | Five diagnostics remain: invariant ICoreTool input/output expectations; computed_field/property decorator limitation; Commit/string local assignment; None passed to a BaseModel-bound core input. AdapterBinding's former misc message is gone. These five are not automatically caused by the upgrade. |
| Three unchanged existing behavior-test files | **92 passed in3.11s**, native exit0, no warning/skip/xfail summary. Python 3.15/Pytest9.1.1 actually executed the tests. Includes real temporary-Git-repository behavior, not production branch mutation. Workflow/planning bytes unchanged before/after. |

Pyright initially resolved the repository's old 1.1.408 dependency, correctly failing its aligned exact-version guard. The final experiment uses a separate lab workspace containing1.1.414, copies the same diagnostic policy, explicitly selects target3.15 and adds the source repository as an import path. This respects existing workspace-owned Node resolution; no active node_modules, guard bypass or adapter code change was needed. Missing YAML/jsonschema stubs in the initial Mypy lab were supplied as the proper checker prerequisites; final five-message evidence above supersedes that incomplete environment.

**Current assessment:** a coherent current 3.15 candidate is feasible in the tested boundaries and removes at least two earlier obstacles (old Ruff target warning and AdapterBinding's Mypy workaround). Python 3.15 plus oldpins is no longer the primary decision model. The remaining SDK handler/result/proxy API migration is normal work required to adopt SDK 2; repeated unchanged-server failure is not useful evidence against the new target. Full migrated-server startup, protocol/lifecycle verification and package validation belong to a bounded implementation proposal after the remaining strategy decisions. Preserve existing meaningful type contracts; do not retain obsolete suppressions merely because they were previously approved.

### Final aligned suppression controls and source review

All established paired controls were replayed on the aligned versions: **27 Pyright groups /54 sources /28 intended errors** (the unknown-lambda negative has two), and **ten Ruff groups /20 sources /ten intended errors**. Neither checker reports any paired positive source. Pyright 1.1.414 strict defaults still have the same four relevant default-none settings; the other23 listed false flags suppress real strict signals. This is diagnostic sensitivity proof, not a reason to enable all of them without scope/cost approval.

The original20 Mypy-bearing test files report **131 static errors in nine files** on Mypy 2.4, compared with132 on the old baseline. Codes:117 arg-type, four unused-ignore, three attr-defined, two func-returns-value, two misc, two var-annotated, one assignment. The four exact redundant Mypy comments remain the same. This is outside the configured production-only Mypy gate; no runtime failure or new regression-test requirement follows from that count.

Native Ruff 0.17.1 over the 56 existing noqa-bearing source files with RUF100 added finds the same **19 redundant directives**, plus **three new style diagnoses** in label_config.py: ISC004 at109/152 (parenthesize intentional adjacent strings in returned tuples), and UP037 at134 (unquote the helper's type annotation after adopting3.15 delayed annotations). Preserve returned strings/behavior. Do not apply the 3.15-specific annotation simplification on the unchanged3.13 baseline.

A token-aware source review locates145 PLC0415 imports: eight production and137 test sites. Production groups are CLI optional paths(3), recovery-server composition(3), capture_exception(1) and phase input-schema generation(1). Most test imports are ordinary output/input models or mocks; their original historical rationale is generally unknown, and being local does not prove a cycle. The proposed disposition is ordinary module imports when those test files are migrated, retain a narrowly justified delayed import only for demonstrated timing/dependency need, and defer unrelated mass import reformatting. See the final disposition table in the inventory.

The None/core mismatch has a bounded consumer explanation:49 args_model definitions in production tools return a model; none returns None. The optional prepared-input contract type and two explicit tests in test_pipeline_decorators.py preserve None acceptance. Tightening that internal admission contract touches the validation decorator, prepared-input contract and those test doubles/cases; it does not require changing public JSON inputs of the 49 tools. This is a proposed contract decision, not already approved removal.

Source inspection found **no CLoader/CSafeLoader/CDumper/CSafeDumper selection** in active production Python. ConfigLoader's two loaders subclass yaml.SafeLoader; YamlDumper subclasses yaml.SafeDumper; the remaining reads use safe_load. The aligned runtime MRO and serialization round-trip confirm the selected Python implementation. Thus an unavailable optional C extension is an installation concern for the proposed route, not evidence that pgmcp needs another YAML implementation or loses an application-selected C parser.

### Proportional remaining evidence

- Candidate wheel/package installation and deployment remain open: direct dependency sets and unchanged source startup on Python 3.15 were measured above; no migrated SDK 2 wheel exists.
- Invalid handler input and actual pgmcp error-wrapper transport; minimal SDK explicit-error/resource-failure controls are now recorded above.
- Whole-application candidate startup and the final migrated proxy's cancellation/deadline/subprocess behavior. Native-proxy/candidate-child restart, failed replacement and old/new client negotiation are already executed above.
- Complete the Python 3.15 alignment assessment using the current candidate set, including deployment/installability and relevant remaining suppression controls. No further old-pin combination matrix or separate 3.14 run unless a concrete question requires it.
- Discuss the measured actual-source removal impact and final dispositions, including global/local overlap and the four native-default-none rules. Investigate safe import timing only where needed to justify an actual hoisting proposal; removing a directive alone proves no runtime import behavior. Record owner decisions on type boundaries, test policy and bounded later delivery before Research closes.

## Questions

The proposal above consolidates migration options. Research remains incomplete until actual global/local suppression-removal impact is assessed and the resulting strategy is discussed; implementation verification belongs to later delivery.

- After remaining probes, should SDK 2.3 be a next-major migration target while preserving the current initialized protocol route, or should protocol-lifecycle expansion be a separately approved change?
- Which Python floor is justified by actual dependency/runtime/checker execution and lifecycle benefits?
- Which suppressions can be removed or narrowed, and which need retained, version-triggered exceptions?
- Does the resulting migration still fit a chore, or should implementation be delegated to a separate bounded refactor issue?

## Migration Benefits and Initialization Boundary

The concrete benefits must be separated from migration feasibility and from an assumption that newer automatically means faster.

- Python 3.15 has a longer support horizon and active bugfix maintenance; 3.13 remains security-supported. No pgmcp performance gain has been measured. The aligned checker/dependency set removes the demonstrated AdapterBinding unused-ignore requirement while preserving covariance; that observation belongs to the combined stack, not Python alone.
- SDK 2 supplies explicit typed handler parameters/results and validates outgoing protocol shapes against the negotiated version. Its stdio runner isolates the wire descriptors from ordinary stdout. These are useful integration safeguards, not replacements for pgmcp business validation or error presentation. SDK 1 still receives critical fixes/security patches; migration is not justified by claiming it is unsupported.
- The 2026 protocol carries version/client context per request rather than requiring initialize plus initialized for a session. For pgmcp's proxy this could remove cached initialize replay after child replacement. That is an architectural benefit inferred from the existing proxy and upstream lifecycle, not an implemented simplification or measured latency improvement.
- Configuration/bootstrap, child readiness, process supervision, in-flight request handling and workspace initialize_project/state requirements remain. Supporting both protocol eras retains the old handshake route; a smaller proxy is not guaranteed merely by adopting SDK 2. Current SDK 2 clients already connect through the existing proxy using their native fallback; forced 2026 operation currently fails.

Sources: [SDK changes](https://py.sdk.modelcontextprotocol.io/whats-new/), [SDK migration contract](https://py.sdk.modelcontextprotocol.io/migration/), [Python maintenance status](https://devguide.python.org/versions/).

## References

- [SDK 2.3 release](<https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0>)
- [SDK package versions](<https://pypi.org/project/mcp/>)
- [Python lifecycle](<https://devguide.python.org/versions/>)
- [Python 3.14.8](<https://www.python.org/downloads/release/python-3148/>)
- [Python 3.15.0](<https://www.python.org/downloads/release/python-3150/>)

## Approved Strategy

**Research and delivery-boundary authorization; concrete migration and suppression-remediation strategies remain unapproved.**

| Boundary | Current human decision |
| --- | --- |
| Delivery boundary | Approved: no migration implementation within #513. Plan targeted follow-up issue(s); no new issue administration or production change is authorized by this record alone. |
| Suppression assessment | Confirmed #513 work package: establish the impact of removing global and local suppressions, including their relationship to newer Python/dependency/checker versions. Source-impact assessment may not be deferred merely because migration delivery is separate. |
| SDK experiment | Approved: create an isolated environment under .pgmcp/temp/issue513, install SDK 2.3 and its dependencies on existing Python 3.13, and run targeted positive/negative probes. Active server/source remain unchanged. |
| Latest-stable alignment | Approved research direction: use Python 3.15 as the target and select/test appropriate current dependencies and checkers together; the previous retain3.13 preliminary recommendation is superseded. No production minimum change or release authorized. |
| Additional interpreters | Approved: investigate the newest stable Python release. Prepared standard CPython 3.15.0 and two isolated environments below .pgmcp/temp/issue513; no system/PATH/default or active-server changes. This does not authorize a higher minimum. Python 3.14 was not installed. |
| Variance/type contracts | Carry forward the owner decision from #507 to preserve explicit covariance. No silent migration may weaken it. |
| Production SDK, protocol/proxy, Python floor and checker remediation | No implementation choice approved yet. Discuss findings and record per-boundary strategy before Research closes. |

## Expected Results

An evidence-backed migrate/defer decision with bounded consumer impact, compatible protocol/result/error behavior, actual candidate-runtime evidence, and a justified disposition of the complete suppression inventory. Research completion must not be claimed while these items or owner strategy remain open.

## Evidence

### Candidate API and old-client interoperability probes executed

Three research cases: SDK API/result positive+negative controls; real SDK 1.30-client/SDK 2.3-server stdio session; token-aware source/native-policy collector.

- [SDK v2 migration guide](<https://py.sdk.modelcontextprotocol.io/migration/>)

**Invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue513/test_issue513_research.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s","--tb=short"]}, timeout_seconds=180)

**Observed Result:** 3 passed in 9.41s; native exit 0. Candidate SDK 2.3/Pydantic 2.14.1/Python 3.13.7. Session negotiated 2025-11-25; exact URI/MIME/text/echo preserved in the checked route. Expected child ValueError traceback and client McpError observed. Receipt 535b0461c7b44d10ab929a30f7b53151 supplements these durable facts.

### Native Ruff reports 19 redundant directives

56 exact source files containing actual Ruff comments were targeted; native selection/per-file policy retained, only RUF100 added.

- [Complete native/local suppression inventory](<suppression-inventory.md>)

**Invocation:** run_checks(scope="targets", targets=<the 56 Ruff-bearing files indexed in suppression-inventory.md>, checks=["python_lint"], args={"python_lint":["--extend-select","RUF100","--output-format","json"]}, timeout_seconds=180)

**Observed Result:** 19 RUF100 messages, native exit 1; no other code. Receipt 44e745d0213c4739b5ad69c4dc4f6e1e is supplemental; durable paths/lines are in the inventory.

### Unchanged production converter executes under both SDK dependency sets

One focused temporary case imported the real ToolResult/converter in separate baseline and candidate subprocesses; compared selected wire fields and two negative controls.

- [Production converter](../../../mcp_server/utils/mcp_converters.py)
- [ToolResult](../../../mcp_server/tools/tool_result.py)

**Invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue513/test_issue513_research.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s","--tb=short","-k","unchanged_converter"]}, timeout_seconds=120)

**Observed Result:** 1 passed, 3 deselected in 3.99s; native exit 0; no stderr. Text/JSON-text/image/resource/error fields matched; missing image data -> KeyError, incomplete resource -> ValidationError on both. Receipt 69da50da594d47a48f535fcb7373c218 supplements these facts.

### SDK errors and fresh process sessions

**Invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue513/test_issue513_research.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s","--tb=short","-k","error_contracts"]}, timeout_seconds=120)

**Observed Result:** 1 passed, 4 deselected in 3.82s; native exit 0. Two separate sessions completed initialization, explicit tool-error output, missing-resource and invalid-list-return controls, followed by successful echo. Deliberate child tracebacks remained visible. Receipt c0a20d6b6fd64d1999655a79cbea04fa is supplemental.

### Real proxy/candidate child and client negotiation

- `run_tests(scope="targets", targets=[".pgmcp/temp/issue513/test_issue513_research.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s","--tb=short","-k","native_proxy"]}, timeout_seconds=90)`: **1 passed, 5 deselected in 5.81s**, native exit0. Actual proxy replayed initialize; executing child PID changed; echo/resource succeeded. Supplemental `8bcb78d14ced4a34a7392a9e54d29649`.
- Same file/tool, `-k "b017_validation or preinitialize_discovery or failed_sdk_child"`, timeout 90: **3 passed, 10 deselected in 6.48s**. Both Pydantic model-validation comparisons succeeded; raw discovery was rejected; failed child replacement produced an audit/client diagnosis. Supplemental `690bc161489049999aa1022dc6a291b3`.
- Same file/tool, `-k sdk2_client_auto`, timeout 90: **1 passed, 15 deselected in 9.59s**. SDK 2 auto and explicit-handshake modes connected at2025-11-25; forced2026-07-28 failed as recorded. Supplemental `d70f3043b96e4692a2f155e8a0ae5cf1`.

Reproduction route: inject MCPProxy.process_factory with a Popen launching the isolated SDK 2 interpreter and a minimal Server with on_list_tools/on_call_tool/on_read_resource. Echo returns its argument, pid returns os.getpid, restart returns a receipt then asynchronously emits the existing restart marker to stderr. Use a native SDK 1 ClientSession or isolated SDK 2 Client over stdio. For failed replacement, make the second factory launch exit before initialize; retain the ordinary proxy code. Put probe logs below an isolated temporary workspace root. No business-tool implementation or active server restart is required.

### Diagnostic sensitivity, source copies and candidate Pydantic

Exact final positive/negative sources and all native invocations/outcomes are in [the suppression inventory](suppression-inventory.md). It includes:

- Ten expected Ruff diagnostics in20 controls, zero positive diagnostics.
- Expected intended Pyright report signals for all 27 negative controls and zero positive diagnostics, using the final refinements explicitly recorded there.
- Native root policy accepting three simple invalid call/type/attribute examples; candidate SDK 2 policy masking four old API attributes until explicitly enabled.
- Six Mypy production copies:13 errors;13 Pyright-bearing copies:7 errors;20 original Mypy-bearing test files:132 static errors and 4 redundant ignores.
- Six native Mypy policy controls: untyped application function is rejected, untyped tests.* function is accepted, typed positives pass and bad typed assignment is rejected in both packages.
- Actual AdapterRole source in isolated modules under Pydantic 2.11.7 and 2.14.1: retained declaration passes valid construction/schema/serialization and five invalid/immutable controls; full PEP695 conversion without the obsolete global TypeVar fails with PydanticUserError. `-k adapter_role_retained`:1 passed in1.76s; supplemental `ebdc0b4fe6674fd4bab42df9faef6745`.

These diagnostic failures are deliberate research measurements. Production/configuration/checker pins and the permanent test suite remain unchanged.

### Python 3.15 reproduction and outcomes

Installation: download the official `python/3.15.0` NuGet package, extract below the ignored research root, invoke its tools/python.exe with `-m venv --copies <env>`. Use each env's Scripts/python.exe with `-m pip --isolated --disable-pip-version-check --no-cache-dir install --index-url https://pypi.org/simple` and the exact versions above. Compare binary-only, ordinary, and process-local `PYYAML_FORCE_LIBYAML=0` routes. Both successful pure-Python installation reports remain temporary research aids; durable outcomes are recorded above.

All runtime probes used `run_tests(scope="targets", targets=[".pgmcp/temp/issue513/test_issue513_research.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s","--tb=short","-k",<selection>]}, timeout_seconds=<below>)`. The native pytest 3.13 driver launched explicit candidate 3.15 subprocesses; it was not a claim that the entire pytest toolchain ran on 3.15.

| Selection | Outcome | Supplemental receipt |
| --- | --- | --- |
| python315_runtime_boundary_matrix;120s | 1 passed,16 deselected; eight subprocess measurements, all exit0. Runtime/ converter/AdapterRole/validation observations above include deliberate rejected variants. | ded70aadf4da4e8dbfdc7b06e2a2dba8 |
| python315_actual_server;120s | 1 passed,17 deselected,16.92s. Observation harness records healthy SDK 1 and failed SDK 2 startup; its pass is not a successful SDK 2 startup claim. | d2ec8c3827bc4e0a9a9a78587891dd8c |
| python315_sdk2_stdio;90s | Selected case passed in an initial two-case run; other case failed on the expected repository mcp<2 dependency conflict. Echo/resource/error/recovery facts above were observed. | 248e06d3e8f14080bc3acd266296768f |
| python315_prepare_variance;90s | Final1passed,19 deselected,4.10s. Compare source-context metadata with isolated Python-I; both isolated sets pass pip check, SDK 2/source conflict retained explicitly. Earlier attempts without Python-I inherited the repository search path and were not isolated consistency checks. | 804b5b537302423cacd50297148b9194 |
| python315_proxy_runtime;90s | 1 passed,20 deselected,5.82s. Actual proxy on 3.15, changed child PID, initialize_replayed and restart_completed, successful subsequent echo/resource. | a64e0b0d81a84dcabf1a2a6abd6cfcd5 |

Startup reproduction launches each candidate interpreter with `-m mcp_server` from the unchanged repository, `PGMCP_WORKSPACE_ROOT=<repository>`, `PGMCP_BYPASS_VERSION_CHECK=false`, logs below the lab. Call initialize, tools/list, health_check, resources/list and resources/read(pgmcp://docs/cache-reading). Read workflow/planning bytes before/after and require equality. Repository-visible package metadata supplies3.0.0; no candidate wheel was installed or fabricated. The source CLI takes/releases its normal startup lock. Do not invoke workflow/planning mutations or active-server restart.

Native checker calls all used scope=targets and only the named positive/negative controls:

- Mypy: python_types, args `--python-version 3.15 --python-executable <repository>/.pgmcp/temp/issue513/sdk23-py315/Scripts/python.exe`, timeout 90. Ordinary positive/wrong-assignment pair: exactly one assignment error (ca75c2d77a294f4d8abc07eaf059d470); ToolExecution/AdapterBinding pair: exactly two return-value errors and none in positive (00b4a05a079c42889dded64cfd8078a1).
- Pyright: python_pyright, args `--pythonversion 3.15 --pythonpath <same interpreter> --outputjson`, timeout 90. Argument pair: exactly one reportArgumentType and none in positive (708a739df7cd439e92ac12f81446f443); covariance pair: exactly two reportReturnType and none in positive (e93dcc7ceda54244ae22bc86ad7ce618).
- Ruff: python_lint, args `--target-version py315 --select PLC0415 --output-format json`, timeout 60. Exactly one expected negative/zero positive diagnostics; native 3.15 instability warning retained (3437fe05ca9147f481f9a243f1a2df30). The initial native-selection run also emitted ANN201/I001 from the deliberately minimal fixtures; those incidental style messages do not establish runtime incompatibility.

Exact covariance sources and remaining suppression dispositions are indexed in [the inventory](suppression-inventory.md). Negative checker exit1 results above are the required diagnostic controls, not failed release validation.

### Aligned candidate: reproducible scope and outcomes

Install into a fresh aligned-py315 venv with `PYYAML_FORCE_LIBYAML=0` in that installation process only, using pip --isolated --no-cache-dir, official PyPI, mcp>=2,<3, pydantic>=2,<3 and current stable runtime/test/checker packages listed above. Add the two current stub packages; install pyright@1.1.414 with npm --prefix <lab>/aligned-node --ignore-scripts --no-audit --no-fund --no-save. The observed direct pins above fix the reproduction snapshot; transitive dependency records remain in the ignored pip report. No active dependency installation or package-source constraint was changed.

The temporary driver file remains `.pgmcp/temp/issue513/test_issue513_research.py`, run through the normal run_tests MCP tool, scope=targets, tests=[python_tests], args `-n 0 -s --tb=short -k <selection>`:

| Selection / timeout | Observed evidence | Supplemental receipt |
| --- | --- | --- |
| python315_aligned_runtime or python315_aligned_checks /240s | 2 passed in34.27s. Actual3.15 imports/converter/model/pip consistency, Mypy 2.4 variance, Ruff 0.17.1 paired diagnostic. Initial Pyright was correctly unavailable on old workspace dependency; initial Mypy source-copy run also lacked two stub packages. | 8cacb6cdc6324b47b0bc12c098dd12ae |
| aligned_refined_pyright /180s | 1 passed. Only corrected Pyright workspace resolution and Mypy source-copy run after stubs: two variance/one argument negative with clean positives; five remaining Mypy source diagnostics. | b2d29ed3436e4b0cba2eaa9a2b7a98bb |
| aligned_retained_binding /120s | 1 passed measurement; actual production execution.py emits exactly one unused-ignore, native checker exit1. Not a passing production quality gate. | 8e8ea93bdb604f0a918b5fde30ef0360 |
| aligned_existing_behavior /210s | 1 passed research driver in8.21s; inner candidate run_tests tool reports92passed in3.11s, native exit0. | 3abe4e05254249e399b06f23742edb95 |

The inner **run_checks** calls retain scope=targets and source definitions recorded in the suppression inventory. Mypy args: `--python-version 3.15 --python-executable <aligned interpreter>`; source-copy/retained-source measurements also use `--follow-imports=silent`. Pyright args: `--pythonversion 3.15 --pythonpath <aligned interpreter> --outputjson`. Ruff args: `--target-version py315 --select PLC0415 --output-format json`. Exact adapter prerequisite files are updated only in lab copies; evidence confirms actual selected external versions. Do not disable version guards.

The inner **run_tests** request is scope=targets, tests=[python_tests], args `-n 0 --tb=short`, timeout_seconds=120, with exactly:
- [test_template_engine.py](../../../tests/mcp_server/unit/services/test_template_engine.py)
- [test_artifact_header_reader.py](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py)
- [test_git_adapter_skip_paths.py](../../../tests/mcp_server/unit/adapters/test_git_adapter_skip_paths.py)

The final adapter-snapshot preparation preserves each original prerequisite line and replaces only its version. Its first draft used an overbroad regex which dropped some Pytest prerequisite lines; that lab setup was corrected and the existing-test request rerun. No permanent test, source, active adapter/configuration or workflow position changed.

### Final candidate group controls

Using the same ignored research driver, run_tests scope=targets, tests=[python_tests], args `-n 0 -s --tb=short -k final_aligned_group_diagnostic`, timeout240: **1 passed in19.10s**. Inner existing RunChecksTool calls use the aligned adapter snapshots and versions; their native exit1 results are intentional diagnostic measurements. Pyright targets all 27 established positive/negative pairs in its isolated workspace; args `--pythonversion 3.15 --pythonpath <aligned interpreter> --outputjson`. Ruff targets the 20 existing group sources with `--target-version py315 --select PLC0415,T201,BLE001,UP046,ANN401,ARG001,ARG002,N818,SLF001,B017 --output-format json`. Mypy targets the 20 original files listed in the directive index with `--python-version 3.15 --python-executable <aligned interpreter> --follow-imports=silent --no-incremental --show-error-codes`. Outcomes and codes are above; supplemental 82faca7bceb64f1abb984a2c1455d95d. All native captures were untruncated.

Same driver, selection `final_aligned_unused_ruff`, timeout150: measurement passed. Inner Ruff targets the 56 original noqa-bearing files, keeps native rule/per-file policy and adds `--target-version py315 --extend-select RUF100 --output-format json`:19 RUF100 plus the three exact style messages above, native exit1. The aligned YAML MRO probe and bool/int/multiline-string round-trip succeeded; supplemental 095c040a6e434d96969c6d5dbea77642. Exact paths remain in the inventory; no permanent tests added.

Read-only AST/token review resolves all 145 local-import directive locations/enclosing functions and all 49 production args_model returns. Search active production for YAML calls/C-loader names, inspect ConfigLoader/YamlDumper bases, and compare the runtime MRO; [PyYAML 6.0.3 safe_load source](https://raw.githubusercontent.com/yaml/pyyaml/6.0.3/lib/yaml/__init__.py) confirms SafeLoader selection. [Pyright 1.1.414 strict-default source](https://raw.githubusercontent.com/microsoft/pyright/1.1.414/packages/pyright-internal/src/common/configOptions.ts) confirms the default-level classification. These source observations are not full application execution claims.

## Risks

### A successful minimal SDK server can be mistaken for pgmcp migration proof.

Keep executed route explicit; verify actual server, converters and proxy separately before any delivery claim.

### A newer runtime/checker can make an old workaround unnecessary or hide a weakened type contract.

Use positive and negative controls with the particular suppression removed and masking disabled; retain owner-approved variance.

### Research could turn into a broad migration or suppression-cleanup project.

No production remediation in this phase; obtain per-boundary strategy and split delivery scope when no longer mechanical.

## Related Documents

- [Issue #513](<https://github.com/MikeyVK/phase-gate-mcp/issues/513>)
- [Final #507 research](<../issue507/research.md>)
- [Suppression inventory](<suppression-inventory.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-17 | @imp researcher | Record approved isolated SDK probes, executed results, consumer boundaries, complete inventory navigation and unfinished decisions. |
| 0.2 | 2026-10-17 | @imp researcher | Add actual proxy/restart/failure and SDK 2 client negotiation evidence, diagnostic masking, candidate Pydantic findings and bounded migration option; retain open strategy decisions. |
| 0.3 | 2026-10-17 | @imp researcher | Record owner-approved latest-stable Python experiment, actual 3.15 installation/runtime/CLI/proxy/type controls, unresolved installation/checker limits and provisional independent floor recommendation. |
| 0.4 | 2026-10-17 | @imp researcher | Supersede old-pin-led recommendation with owner-directed current Python alignment; record actual aligned checker/core-tool runs,92 existing passing tests and removable AdapterBinding workaround. |
| 0.5 | 2026-10-17 | @imp researcher | Consolidate owner decision proposal; finish aligned group controls and source-specific dispositions, clarify existing Python YAML route and the bounded None-input contract choice. |
| 0.6 | 2026-10-17 | @imp researcher | Record separate migration delivery, restore complete global/local removal-impact research scope, correct evidence limits and distinguish protocol initialization from bootstrap/project initialization. |
| 0.7 | 2026-10-17 | @imp researcher | Add actual-source global/local removal measurements, corrected reference/CWD evidence, overlapping exceptions, native-default effects and concrete owner policy questions without production changes. |
