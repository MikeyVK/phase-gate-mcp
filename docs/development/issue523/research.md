<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#523 — Tool-output contracts, client delivery and overlap

**Status:** Research completed; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

Assess current output delivery and historical decisions without selecting a new runtime policy.

## Scope In

Current catalog metadata, actual operation and error results, text/resources/cache ownership, supported-client evidence, representative payload measurements and bounded follow-up.

## Scope Out

Runtime changes, wrapper forwarding, universal schema policy, channel removal, cache redesign, client-specific routing, compatibility bridges, dependency/client matrices and #524 implementation.

## Problem Statement

Actual structured operation delivery, optional published output schemas and bounded text are different contracts. Their combined behavior must be evaluated without equating a text limit with bounded model context or multiple projections with duplicated business ownership.

## Goals

- Locate output metadata loss in normal registration and examine actual success/error responses.
- Distinguish direct measurements, source observations, documentary statements and unknown client behavior.
- Reconcile #301, #390/#395, #456, #462 and #517; record durable evidence and bounded follow-up without changing policy.

## Findings

### Current ownership and advertised contract

| Boundary | Current source of truth and observation | Consequence |
|---|---|---|
| Operation | Core tool returns a Pydantic operation DTO, optionally inside ToolExecution. Wrappers can instead return validation, enforcement, configuration or execution error DTOs. | The operation is authoritative; notes and attachments have separate owners. |
| Catalog metadata | [ToolAssembly](../../../mcp_server/bootstrap.py) derives supported contracts from explicit metadata or generic core types for presentation validation. [ToolFactory](../../../mcp_server/core/tool_factory.py) registers wrapped tools; its three decorators do not forward output_model. [MCPServer.list_tools](../../../mcp_server/server.py) checks only registered-tool metadata. | Actual bootstrap: 37 tokenless / 49 credential-selected tools, zero advertised output schemas in both lists. The latter uses a placeholder token to select registrations, not authenticated GitHub execution. |
| Structured result | MCPServer serializes execution.operation.model_dump(mode="json", by_alias=True). | Actual DTO is delivered, independent of whether outputSchema is advertised. No Markdown reconstruction. |
| Human-readable text | Configured ResponsePresenter/TextPresenter projects operation fields and separately owned notes; configured ceiling is 8,000 UTF-8 bytes. | Bounds text, not structuredContent, attachments, cache or total response. |
| Embedded resource | SchemaResourcePresenter serializes the separately owned schema attachment. | In scaffold_schema and input validation, the attachment overlaps the schema field in the operation. This is duplicate delivery, not independently maintained schema ownership. |
| Cache | Operation is published before presentation; [serialize_cached_response](../../../mcp_server/utils/cache_serialization.py) omits only absent optional nulls and retains required/explicit nulls. [CachedResponseResource](../../../mcp_server/resources/cache.py) reads without rerunning the tool. | Complete normal operation data remains available on demand; cached JSON need not be byte-identical to wire JSON. Serialization/publication failure truth is separately owned by #524. |

The missing public metadata is confirmed, but enabling it is not automatically a one-property fix. The published success schema and wrapper-generated error shapes require one explicit contract; the optional server publication path does not establish that all outcomes conform to a success-only schema. The existing listing test manually attaches output_model to a wrapped test tool. It proves that optional path, not the normal catalog.

The installed SDK validates successful structured results against an advertised schema; it skips this validation for is_error results. The [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) makes outputSchema optional and requires conformance when supplied. SDK behavior alone does not settle a future all-outcomes schema policy. Unknown tools and processing/presenter failures currently return text-only errors; domain/input errors normally retain structured error DTOs. A native check with findings is a successfully executed operation whose row has status failed, rather than an MCP execution error.

### Measured response fields

Source baseline: main 78f270833f2ec85c8f80a8ad72a60559c3a4ea68, before any #523 product changes (none). Python 3.15.0, MCP SDK 2.3.0, pytest 9.1.1; repository config and bundled template suite, isolated temporary workspace.

| Actual call | isError | Text UTF-8 bytes | Compact structured JSON UTF-8 bytes | Embedded text UTF-8 bytes | Compact result JSON UTF-8 bytes | Cache total_chars |
|---|---:|---:|---:|---:|---:|---:|
| health_check({}) | false | 200 | 195 | 0 | 503 | 145 |
| scaffold_schema(python_class) | false | 159 | 11,927 | 12,635 | 26,857 | 11,927 |
| scaffold_schema(not_admitted) | true | 106 | 1,290 | 693 | 2,391 | 1,273 |
| run_checks: 100 undefined-name diagnostics | false | 200 | 24,896 | 0 | 25,202 | 24,896 |

All four actual DTOs passed JSON Schema validation against their concrete output models. Both schema-bearing calls had structurally equal schema fields and embedded schema JSON. Whitespace/encoding account for representation-size differences. Cache metadata was read with offset=0, limit=1; total_chars is Unicode code points, not bytes. The healthy DTO differs in size because of optional-null serialization policy.

These are field sizes and compact reserialization sizes, not measured network packet sizes, model tokens, billing, peak memory or startup/performance benchmarks. Four representative calls are not proof that every tool variant is valid. The diagnostics case runs native Ruff in a temporary workspace with the repository pyproject and 100 lines of value_N = missing_N; its row reports failed while the MCP operation succeeds.

### Supported client evidence and limits

| Consumer | Evidence class | What this establishes | What remains unmeasured |
|---|---|---|---|
| Python SDK 2.3 / real pgmcp handlers | Direct execution through connected_mcp_client | Programmatic text, structured DTO, embedded resources and cache windows are available; native successful-result schema validation exists when metadata is present. | Harness UI/model routing and token costs. The helper is an in-memory protocol transport, not a live IDE transcript. |
| This Codex chat / functions orchestration | Direct tool observations | Both content and structuredContent are programmatically accessible. The orchestrating call can print selected fields or whole results. | This does not establish every Codex stdio client, user UI or underlying model-context projection. |
| Codex Plugins/App integration | [Official reference](https://developers.openai.com/plugins/reference), documentary | That integration documents both content and structuredContent as model/component-visible; _meta is component-only. | This is not proof that every configured stdio MCP path uses the same routing. [Codex MCP setup docs](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) do not settle that question. |
| VS Code | [Pinned implementation](https://github.com/microsoft/vscode/blob/af18ca5130bd7164867b2784b3aba68b4de38116/src/vs/workbench/contrib/mcp/common/mcpLanguageModelToolContribution.ts#L329), source inspection | For truthy structuredContent, this source sends its compact JSON to the model and omits content text there; text is still added to UI details. Non-image embedded resources use a resource link for the model, with body in details. | No end-to-end test of the owner's installed VS Code build, truncation or token costs. [Issue 290063](https://github.com/microsoft/vscode/issues/290063) remains open; requested behavior is not accepted policy. |
| Antigravity | [MCP docs](https://antigravity.google/docs/mcp) and [CLI changelog](https://antigravity.google/docs/changelog?tab=cli), documentary | MCP tools/resources are supported. CLI 1.1.5 notes a fix for dropped embedded resources. | No authoritative per-channel structured/text model rule or installed IDE measurement established here; CLI release evidence is not an IDE guarantee. |
| Text-only consumer | Capability analysis, not a named measured client | Receives bounded text and possibly a resource locator; cannot be assumed to receive the full DTO automatically. | Whether it can and does fetch resources or process schema attachments. |

The current VS Code source implies two conditional risks: full structured diagnostics can bypass the intended model-context reduction of bounded text, and instructions that exist only in configured presentation text may not reach the model. For example, presentation configuration appends context_reset instructions on mutation tools; serializing an operation does not serialize independently owned presentation instructions. This is source-derived risk, not a demonstrated workflow failure in the installed client. Conversely, equal schema payloads on the wire do not prove twice the model tokens: that source treats embedded resources separately.

No blanket client-compatibility or token-saving guarantee follows from these observations. No client-specific server routing is selected.

### History, overlap and prior decisions

| Decision/history | Established fact | Interpretation now |
|---|---|---|
| [#301 Research](../archive/issue301/research.md) | Limited early VS Code observations and intended behavior differ within the artifact. Its later [closure](https://github.com/MikeyVK/phase-gate-mcp/issues/301#issuecomment-4681062484) explicitly says #390 / PR #395 resolved it. | Neither an indefinitely deferred issue nor current token measurements. |
| [#390 Research](../archive/issue390/research.md), [PR #395](https://github.com/MikeyVK/phase-gate-mcp/pull/395) | Merged 2026-06-11, b2f0bcdc1f35306b2550f2012795514a14d19afd; introduced structured transport for selected tools. | Historical architecture, not a prescription to reintroduce StructuredTool. |
| [#456 field audit](../archive/issue456/tool-presentation-field-audit.md) and [Research](../archive/issue456/research.md) | Explicit human decisions established compact configured text, complete cache and actionability-based omission of deep diagnostics. | Text-only and cache-only were projection classifications. #517 later adds full structured delivery; old labels are not a total wire-size promise. |
| [#462](https://github.com/MikeyVK/phase-gate-mcp/issues/462) | Owner closed without implementation on 2026-10-12. Four small cache reads in #469 QA were observed; routine status/health data was largely repeated. Other plan/diff/native-evidence reads were useful. | Bounded historical examples, not frequency, causal proof or quantified savings. Do not reopen conditional cache references automatically. |
| [#517 Approved Strategy](../issue517/research.md#approved-strategy) | Owner chose schema retention plus actual operation DTO structuredContent on 2026-10-18. | Applies at the output boundary; no SDK-1 facade, dependency matrix or legacy tests. Metadata exposure gap remains distinct from the corrected serialization. |

The operation, compact text, embedded schema and cached serialization are projections with distinct responsibilities. They are not separate business truths merely because bytes overlap. Real delivery redundancy exists for schema payloads, and whole-result printing by an orchestrator can repeat text and JSON. Neither observation proves that removing a channel preserves all consumers. Current AGENTS already tells agents to use summaries for routine status and fetch cache only for needed diagnostics/structured fields; another instruction layer would add little.

### Bounded follow-up for owner/Co consideration

| Finding | Evidence and dependency | Required decision before any implementation |
|---|---|---|
| Catalog schemas hidden by wrappers | Confirmed in both active selections; catalog metadata already exists at the composition root. | Define intended publication and success/error/fallback schema contract. Then select the smallest existing-boundary integration; no second static catalog. |
| Client-dependent information delivery | VS Code source and limited vendor documentation show different routing; native harness measurement is incomplete. | Identify required supported client guarantees, especially independently presented instructions, before choosing any channel change. |
| Unbounded structured diagnostics / schema overlap | Actual 24.9 kB diagnostics DTO and 26.9 kB schema result despite short text. | Set a measurable context/size objective and preserve outcome/diagnostic completeness before contemplating a separate delivery change. |
| Cache failure truth | Separate #524 sequence agreed by Co. | Keep #524 authoritative; no implementation here. |

No new issue creation, client matrix project or output redesign is authorized by this list. Co can assess findings without treating the observations as an approved implementation plan.

## Approved Strategy

This is a research-only completion under the published #523 scope and the owner's autonomous execution request. It adopts no new output policy. Human approval inherited from #517 applies to the existing output boundary; #462's owner closure remains in effect.

| Boundary | Binding strategy in this issue |
|---|---|
| Operation DTO / structuredContent | Retain actual operation delivery chosen by the owner in #517. No DTO transformation, contract change or legacy facade. |
| Advertised schemas | Record the confirmed exposure gap; do not introduce forwarding or a universal success/error schema contract without a boundary-specific owner decision. |
| Presentation / attachments | Retain configured projection and separate attachment ownership. Report client limitations honestly; do not claim a total-response or model-context ceiling. |
| Cache | Retain full operation publication and existing locators/reads. Do not reopen #462 or implement #524. |
| Consumers / compatibility | Clean break remains the agreed migration policy; no historical-version tests, client routing bridge or compatibility layer. Unknown native-client behavior remains unknown. |
| Verification | Temporary isolated observations and useful existing behavior tests only; no permanent regression cases, content snapshots or full-suite run for unchanged product code. |
| Remaining workflow | Implementation owns evidence packaging only; Validation checks the research claims and relevant existing transport behavior; Documentation makes the final evidence/findings index reviewable. Independent QA governs each boundary. |

A newly proposed runtime/schema/cache/compatibility change is the stop condition: discuss it with the owner before implementing rather than expanding this chore.

## Expected Results

A durable research report with exact reproducible measurements, clearly limited client claims, reconciled history and actionable follow-up boundaries. No production, runtime config or permanent test changes; no unsupported compatibility/token claims.

## Evidence

### Reproduce the measured output fields

Observation on 2026-10-19: one temporary research probe passed in 13.75 seconds, pytest exit 0. Receipt 94f3d34a00ef43d79b8fbdb033eaa362 is supplementary; the invocation, observed table and complete probe below are the durable evidence. The source was corrected after a probe-only wrong DTO import/internal-model-validation error; that setup failure was not a product failure.

To reproduce, scaffold pytest_unit_test into .pgmcp/temp/issue523 with force_target=true and replace its authored body with the probe below through safe_edit_file. Keep that path depth (parents[3] is the repository). Use the repository environment and existing configured python_tests adapter. The source below operates only in pytest tmp_path and uses a subprocess-local placeholder for catalog selection, with no authenticated GitHub call. Cache UUIDs/timestamps and timings will vary.

```python
"Temporary read-only output-contract observations for issue523; not durable test coverage."

# Standard library
import json
import re
import shutil
from pathlib import Path

# Third party
import pytest
from mcp.types import EmbeddedResource, TextContent

# Project
from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.schemas.execution_outputs import RunChecksOutput
from mcp_server.schemas.error_outputs import ValidationErrorOutput
from mcp_server.schemas.tool_outputs import HealthCheckOutput
from mcp_server.tools.template_schema_tool import ScaffoldSchemaOutput
from jsonschema import Draft202012Validator
from tests.mcp_server.test_support import connected_mcp_client


@pytest.mark.asyncio
async def test_observe_public_output_channels(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    "Measure actual source/server SDK fields without changing production or asserting a future policy."
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    root = Path(__file__).resolve().parents[3]
    shutil.copy2(root / "pyproject.toml", tmp_path / "pyproject.toml")
    (tmp_path / "diagnostics.py").write_text(
        "".join(f"value_{number} = missing_{number}\n" for number in range(100)),
        encoding="utf-8",
    )
    settings = Settings(server=ServerSettings(
        workspace_root=str(tmp_path), config_root=str(root / ".pgmcp/config"),
        template_root=str(root / ".pgmcp/template_suite"), bypass_version_check=True,
    ))
    server = ServerBootstrapper(settings).bootstrap_target()
    models = {
        "health": HealthCheckOutput,
        "schema": ScaffoldSchemaOutput,
        "input_error": ValidationErrorOutput,
        "diagnostics": RunChecksOutput,
    }
    calls = [
        ("health", "health_check", {}),
        ("schema", "scaffold_schema", {"artifact_type": "python_class"}),
        ("input_error", "scaffold_schema", {"artifact_type": "not_admitted"}),
        ("diagnostics", "run_checks", {
            "scope": "targets", "targets": ["diagnostics.py"],
            "checks": ["python_lint"], "timeout_seconds": 60,
        }),
    ]
    def compact(value):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    observations = []
    async with connected_mcp_client(server) as client:
        listing = await client.list_tools()
        catalog = {
            "active_tools": len(listing.tools),
            "published_output_schemas": [tool.name for tool in listing.tools if tool.output_schema is not None],
            "wrapper_types": sorted({type(tool).__name__ for tool in server.tools}),
        }
        for case, name, arguments in calls:
            response = await client.call_tool(name, arguments)
            dto = response.structured_content
            assert dto is not None
            Draft202012Validator(models[case].model_json_schema()).validate(dto)
            text = "\n".join(item.text for item in response.content if isinstance(item, TextContent))
            schemas = [item.resource.text for item in response.content if isinstance(item, EmbeddedResource)]
            schema_data = dto.get("schema_data", dto.get("input_schema"))
            duplicates = [json.loads(item) == schema_data for item in schemas]
            wire = response.model_dump(mode="json", by_alias=True, exclude_none=True)
            observation = {
                "case": case, "is_error": response.is_error,
                "text_utf8_bytes": len(text.encode("utf-8")),
                "structured_compact_utf8_bytes": len(compact(dto).encode("utf-8")),
                "embedded_utf8_bytes": sum(len(item.encode("utf-8")) for item in schemas),
                "compact_result_utf8_bytes": len(compact(wire).encode("utf-8")),
                "attachment_matches_dto_schema": duplicates,
                "native_statuses": [row.get("status") for row in dto.get("results", [])],
            }
            match = re.search(r"pgmcp://cache/runs/[a-f0-9]{32}", text)
            if match:
                window = await client.read_resource(match.group() + "?offset=0&limit=1")
                page = json.loads(window.contents[0].text)
                observation["cache_window_metadata"] = {
                    key: value for key, value in page.items() if key != "text"
                }
            observations.append(observation)
    monkeypatch.setenv("GITHUB_TOKEN", "research-placeholder-not-a-credential")
    enabled = ServerBootstrapper(settings).bootstrap_target()
    async with connected_mcp_client(enabled) as client:
        enabled_listing = await client.list_tools()
        catalog["credential_selected_tools"] = len(enabled_listing.tools)
        catalog["credential_selected_output_schemas"] = [
            tool.name for tool in enabled_listing.tools if tool.output_schema is not None
        ]
    print("ISSUE523_OBSERVATIONS=" + compact({"catalog": catalog, "results": observations}))
```

- [Server transport and serialization](<../../../mcp_server/server.py>)
- [Public client fixture](<../../../tests/mcp_server/test_support.py>)

**Invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue523/test_output_observation.py"], tests=["python_tests"], args={"python_tests":["-q","-n","0","-s"]}, timeout_seconds=300)

**Observed Result:** 1 passed; 37/49 active tools with zero schemas; four actual DTOs JSON-Schema-valid; sizes and error/native outcomes recorded in Findings.

## Related Documents

- [Issue #523](<https://github.com/MikeyVK/phase-gate-mcp/issues/523>)
- [Current presentation architecture](<../../reference/presentation_architecture.md>)
- [Actual transport behavior tests](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp researcher | Record current delivery contracts, reproducible observations, bounded client evidence and research-only strategy. |
