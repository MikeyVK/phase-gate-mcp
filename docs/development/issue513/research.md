<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 513 — MCP SDK and Python Baseline Assessment

**Status:** Research in progress — executed SDK and Python 3.15 boundaries; decisions open  
**Version:** 0.3  
**Last Updated:** 2026-10-17

## Purpose

Assess upgrade boundaries and checker exceptions before choosing a bounded delivery strategy for the next major release.

## Scope In

MCP SDK 2.3 assessment against the final #507 baseline; Python versions above 3.13; active checker suppression inventory and targeted reassessment.

## Scope Out

No production migration, active-environment dependency upgrade, release/deployment, compatibility bridge, new framework, or permanent diagnostic-suite expansion. Research remains open.

## Problem Statement

SDK 2.x and a higher Python floor can improve supported infrastructure, but change different contracts. A package-version bump alone cannot establish pgmcp compatibility, supported harness behavior, or preservation of existing type contracts. The complete suppression inventory must be reassessed rather than treating historical approval or local placement as sufficient justification.

## Goals

- Separate executed compatibility facts, source-backed impact, proposed choices and owner-approved strategy.
- Identify the smallest affected production boundaries and direct/indirect test consumers.
- Compare actual candidate execution and preserve meaningful negative diagnostic signals.
- Finish with an explicit human decision per boundary; do not automatically migrate or progress.

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

**Checker limitation:** the quality calls used the installed adapters: Mypy host3.13, Pyright Node, Ruff native binary. Their target language/dependency path was3.15; the native Mypy process/plugin still used its host Pydantic 2.11.7. Installing/importing Mypy in the3.15 lab is separate evidence and does not prove its entire execution there. [Mypy 2.4 release notes](https://mypy.readthedocs.io/en/stable/changelog.html#python-3-15-support) explicitly document3.15 support; that newer checker was not installed or approved. Simple target-version acceptance and preserved covariance do not prove all3.15 language features are supported by current pins.

**Provisional recommendation, not an approved strategy:** keep Python>=3.13 while assessing a bounded SDK 2 migration independently. The measured source runtime can operate on 3.15 with the stated installation variant, but no used pgmcp behavior currently requires the higher minimum. Raising it now also needs explicit dependency-installation and checker-version decisions.3.15 provides a longer maintenance horizon; that benefit alone is not proof of a necessary floor increase. No cross-platform, full-suite, candidate wheel, broad performance, or completely migrated application claim is made.

### Proportional remaining evidence

- Candidate wheel/package installation and deployment remain open: direct dependency sets and unchanged source startup on Python 3.15 were measured above; no migrated SDK 2 wheel exists.
- Invalid handler input and actual pgmcp error-wrapper transport; minimal SDK explicit-error/resource-failure controls are now recorded above.
- Whole-application candidate startup and the final migrated proxy's cancellation/deadline/subprocess behavior. Native-proxy/candidate-child restart, failed replacement and old/new client negotiation are already executed above.
- Decide the Python floor using the executed 3.15 boundary comparison above; no separate 3.14 installation unless it becomes an owner-selected alternative. Preserve the distinction between runtime feasibility, installation prerequisites and checker support.
- Grouped suppression probes and final dispositions before Research completion.

## Questions

- After remaining probes, should SDK 2.3 be a next-major migration target while preserving the current initialized protocol route, or should protocol-lifecycle expansion be a separately approved change?
- Which Python floor is justified by actual dependency/runtime/checker execution and lifecycle benefits?
- Which suppressions can be removed or narrowed, and which need retained, version-triggered exceptions?
- Does the resulting migration still fit a chore, or should implementation be delegated to a separate bounded refactor issue?

## References

- [SDK 2.3 release](<https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0>)
- [SDK package versions](<https://pypi.org/project/mcp/>)
- [Python lifecycle](<https://devguide.python.org/versions/>)
- [Python 3.14.8](<https://www.python.org/downloads/release/python-3148/>)
- [Python 3.15.0](<https://www.python.org/downloads/release/python-3150/>)

## Approved Strategy

**Research authorization only; migration strategy is not yet approved.**

| Boundary | Current human decision |
| --- | --- |
| SDK experiment | Approved: create an isolated environment under .pgmcp/temp/issue513, install SDK 2.3 and its dependencies on existing Python 3.13, and run targeted positive/negative probes. Active server/source remain unchanged. |
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
- Expected intended Pyright report signals for all27 negative controls and zero positive diagnostics, using the final refinements explicitly recorded there.
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
