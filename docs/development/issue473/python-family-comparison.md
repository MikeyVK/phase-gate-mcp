<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 473 — Remaining Python Family Comparison

**Status:** RESEARCH DISCUSSION — bounded native quality approved; whitespace criteria pending  
**Version:** 0.2  
**Last Updated:** 2026-10-03

## Purpose and scope

Use [Python Class](python-class-comparison.md) as the detailed code reference, then compare the other seven Python code/test families by their distinct capabilities. This follows the human-approved method of one concrete baseline followed by faster family-specific review. It supplies Research evidence and possible objectives; it does not implement templates or invent new acceptance guarantees.

The seven families are Protocol, Pydantic Config, Pydantic DTO, Adapter, Worker, Pytest Unit Test and Pytest Integration Test. Each uses the untouched minimal/filled v3 outputs and contexts from [the original survey](first-output-survey.md). Fourteen legacy counterparts were rendered, plus two additional hidden DTO-root examples, for sixteen legacy files. Both body equivalence and limits are recorded below.

The approved no-legacy strategy remains binding in [Research](research.md#approved-strategy-clean-break-no-legacy-compatibility--2026-10-02). The old renderer is comparison evidence, not a future compatibility path. The mandatory metadata/revision objective applies to the seven full-document Markdown families; it does not introduce document status/history tables into Python source.

## Renderer, source selection and comparison limits

The authorized renderer is `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/services/template_engine.py`, SHA-256 `ea6024a1612795b07161b50a6416ad40259757229c7a3885ed891f085d0eb382`. It was imported explicitly and called unmodified through TemplateEngine.render. Jinja uses trim_blocks=True, lstrip_blocks=True and keep_trailing_newline=True. Python -B exploratory calls wrote JSON to stdout and did not edit old source trees.

The original source root is `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/`. It contains Config, both DTO variants, Worker and the two pytest templates. It lacks the real Interface and Adapter templates. Those two use the separately found installed legacy root `C:/1Voudig/99_Programming/ST/.pgmcp/templates/`, with the same authorized renderer. Tool/service_command and plain Generic are not substitutes for Adapter/Protocol. Source parity with a historical issue460 snapshot is consequently weaker for these two families.

These are raw renderer calls, not old public MCP/context-enrichment pipeline evidence. Minimal means the current required nucleus translated into old fields, with explicit probe metadata and any old structural fields needed to render. It is not an assertion that every input satisfies an old public schema. Family shapes and their capacities differ.

Probe metadata explicitly supplies artifact_type, comparison-only version_hash, timestamp, Python format, title and compact output_path. comparison-only is not an actual historical fingerprint. Name/signature/default/checklist translations are recorded exactly. Old primitive defaults use explicit Python literal text; current defaults are JSON data. New-only content is not claimed to have an old render destination.

The old Worker has a fixed lifecycle and no equivalent current operation/constructor slot. Its name and module description are comparable; its body is a different recorded contract. Config/DTO roots ignore the modern grouped-import and constraint carriers, and their typed-ID factory import assumes a particular source project. Unit's old root does not render the supplied current fixture definition. These limits prevent “same schema, same full behavior” claims.

All sixteen files were persisted through MCP: scaffold a current python_class evidence container, then safe_edit_file rewrite with the exact raw string and explicit Python syntax validation in report mode. Sixteen stored SHA-256 values match the raw renderer strings. Thirteen final native syntax checks passed; three failed and remain unchanged evidence. Bootstrap output is not legacy evidence. None of the generated examples was imported or executed.

## Concrete files

| Family | v2 minimal nucleus | v2 filled | Original v3 minimal | Original v3 filled |
| --- | --- | --- | --- | --- |
| python_protocol | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/python_protocol.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/python_protocol.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/python_protocol.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/python_protocol.filled.py) |
| python_pydantic_config | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/python_pydantic_config.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/python_pydantic_config.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/python_pydantic_config.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/python_pydantic_config.filled.py) |
| python_pydantic_dto | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/python_pydantic_dto.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/python_pydantic_dto.filled.py) |
| python_adapter | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/python_adapter.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/python_adapter.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/python_adapter.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/python_adapter.filled.py) |
| python_worker | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/python_worker.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/python_worker.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/python_worker.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/python_worker.filled.py) |
| pytest_unit_test | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/pytest_unit_test.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/pytest_unit_test.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/pytest_unit_test.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/pytest_unit_test.filled.py) |
| pytest_integration_test | [Old minimal](../../../.pgmcp/temp/issue473-comparison-04/pytest_integration_test.v2-minimal-render.py) | [Old filled](../../../.pgmcp/temp/issue473-comparison-04/pytest_integration_test.v2-filled-render.py) | [Current minimal](../../../.pgmcp/temp/issue473-survey/pytest_integration_test.minimal.py) | [Current filled](../../../.pgmcp/temp/issue473-survey/pytest_integration_test.filled.py) |

DTO also has [the hidden old minimal](../../../.pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-minimal-hidden-render.py) and [hidden old filled](../../../.pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-filled-hidden-render.py). The old ArtifactManager code can select dto_v2 when its typed pipeline is enabled and that root exists. This call-path observation is not a replay of that entire pipeline. The rich dto.py source must not be presented as the only old public DTO baseline.

## Shared first-output quality

All fourteen current files still match the original survey SHA-256 exactly. Their original Python preflights passed. The original native quality receipt is no longer available from the live cache, so this batch ran a fresh narrow public run_checks over just these fourteen outputs with checks python_format/python_lint, timeout_seconds=120. No source edit or apply_fixes preceded the check.

Fresh receipt: `pgmcp://cache/runs/6bc2219eed2d401d901859251173301f`. Its complete structured DTO was read and retained below. Ruff 0.15.6 reports all fourteen would be reformatted and fifteen lint findings: ten I001 import-block findings, two W293 whitespace-only-line findings and three E501 line-length findings. The configured line-length boundary is 100.

| Family | Formatter, minimal / filled | Lint findings, minimal | Lint findings, filled |
| --- | --- | --- | --- |
| Protocol | failed / failed | I001 | I001 |
| Pydantic Config | failed / failed | I001, W293 | I001, E501 (153 columns) |
| Pydantic DTO | failed / failed | I001, W293 | I001, E501 (126 and 114 columns) |
| Adapter | failed / failed | None | I001 |
| Worker | failed / failed | None | I001 |
| Unit Test | failed / failed | None | I001 |
| Integration Test | failed / failed | None | I001 |

The defects are generated import framing, blank joins, indentation of an empty fields block and overly compact model expressions. Short caller strings/records are composed into long ConfigDict and Field lines. Current [Pydantic patterns](../../../.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2) produce these expressions on one line. Current [import patterns](../../../.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2) and family/base joins produce the actual import block; a heading existing does not prove native conformance.

Syntax success does not certify dependencies, model examples, test effectiveness, runtime behavior or typing. market_ports is an illustrative external dependency. The minimal integration arithmetic body and market/risk terminology are caller-authored examples, not invented by the template. The integration sample's weak collaboration meaning is a limitation of that sample, not evidence of a fabricated integration test.

## Distinct family findings and #460 intent

The [Code/Test Artifact Design](../issue460/design-code-test-artifacts.md), especially §7.3–7.7 and §9, and [Research catalog](../issue460/template-suite-catalog.md) are the recorded contract sources. They were agent-authored under the human's explicit W07/W08 Design delegation and independently reviewed; this comparison does not claim a separate human instruction for every individual field.

### Protocol

The real old Interface and current Protocol both derive from Protocol and use ellipsis for contract methods. Current explicit method names, parameter/return annotations and descriptions survive the filled output. Structured imports, extra bases and async signatures remain available; the old interface root has no equivalent async rendering.

Old minimal invents execute() even when the caller supplies no methods. Current minimal creates a valid empty marker protocol. Catalog rows 77/119 and Design §7.5 explicitly remove the invented execute and Backend header. This is recorded intent, not missing method capacity.

Primary current sources: [template](../../../.pgmcp/template_suite/python_protocol/template.jinja2), [schema](../../../.pgmcp/template_suite/python_protocol/context.schema.json).

### Pydantic Config

BaseModel, extra="forbid", field types/descriptions, defaults/factories and examples remain. Current frozen is required caller input; the old root has a hidden false fallback. Pure configuration model generation does not add a loader, singleton or import-time I/O.

The filled current output preserves False, zero and empty string. JSON-data-to-Python literal rendering replaces raw native default text; flat constraints now have explicit destinations. Factory capacity remains, while the old automatic backend.utils.id_generators import is explicitly removed as source-project specialization. ConfigDict replaces the old dictionary spelling.

These are recorded Design §7.4 and catalog 187 choices. Caller frozen=False in the sample is not a generated architecture violation: the owning consumer contract determines whether a given object is a mutable configuration or an immutable query-result value. No sample execution establishes that role.

Primary current sources: [template](../../../.pgmcp/template_suite/python_pydantic_config/template.jinja2), [schema](../../../.pgmcp/template_suite/python_pydantic_config/context.schema.json).

### Pydantic DTO: two old roots

The rich old dto.py accepts field records, descriptions, factories, caller frozen and examples. The hidden dto_v2.py takes primitive "name: type" fields, fabricates field descriptions, hardcodes frozen=False and does not render explicit examples. #460 merges these into one structured, immutable DTO contract. Current DTO is always frozen=True and extra="forbid"; Config keeps its separately owned explicit mutability choice.

DTO with concrete fields requires at least one example; an empty DTO does not require invented example metadata. Fields remain required when neither default nor factory is supplied. Model-level semantic example execution was explicitly withdrawn; this comparison does not restore it.

The old rich class docstring repeats a Fields summary. Current descriptions appear in the Field definitions instead; no description information is lost in the sample. No separate rationale for deleting that redundant summary was found. This is a presentation preference for discussion, not a demonstrated lost field/validator contract.

The old rich root mentions validators and conditionally imports field_validator, but it does not render a validator body loop. A standalone old shared validator macro does not establish reachable concrete DTO capability. The new bounded schema does not acquire an arbitrary validator/computed-field DSL.

Three native old-output failures are preserved:
- Rich minimal and hidden minimal place pass outside the class before an indented model_config, producing unexpected indent.
- Rich filled turns the modern datetime.datetime.now factory into `from backend.utils.id_generators import datetime.datetime.now`, producing invalid syntax. This exposes the old specialized factory domain; it is not proof that an equivalent public old context was admissible.
- Hidden filled is syntactically valid but lacks the rich description/constraint/factory/example capacity.

These differences support using both old baselines and avoiding an automatic “restore v2” objective. Catalog 73/115–116/187 and Design §7.4/§9 explicitly replace the hidden variant and typed-ID specialization.

Primary current sources: [template](../../../.pgmcp/template_suite/python_pydantic_dto/template.jinja2), [schema](../../../.pgmcp/template_suite/python_pydantic_dto/context.schema.json).

### Adapter

The genuine old adapter always creates module logging and Backend/target-interface prose. It invents adapt() pass when no methods are given. target_interface is documentary rather than a generated inheritance relationship, and it has no separate constructor carrier.

Current Adapter preserves caller concrete method bodies and explicitly supports imports, bases, constructor injection and opt-in logging. The filled sample preserves PriceClient injection and read_price. An empty class remains honest without a fabricated successful operation. The example's external module/runtime is not certified.

Catalog 69 and Design §7.6 explicitly retain the portable boundary adapter while removing forced logging, fabricated methods and source-project metadata. It is ordinary application code; it does not generate an execution-adapter manifest package.

Primary current sources: [template](../../../.pgmcp/template_suite/python_adapter/template.jinja2), [schema](../../../.pgmcp/template_suite/python_adapter/context.schema.json).

### Worker

The old Worker generates BuildSpec/IWorker/IWorkerLifecycle, strategy cache, initialize, LogEnricher, Translator, shutdown and optional async warmup. The current Worker takes one explicit sync/async operation, plus optional constructor injection and logger. Its filled body preserves the supplied publish call. This is a substantial recorded boundary change, not an equivalent rendering of the old lifecycle.

Catalog 90/176–179/186 and Design §7.6/§9 explicitly remove the consumer-local lifecycle/translator/cache assumptions. Optional logging remains portable and opt-in. No proof requires putting that application-specific lifecycle back into PGMCP's shipped generic suite.

The old root also emits `__all__ = [class_name]`; the current Worker does not. No separate disposition for this exact export-list choice was found in the inspected #460 sources. Direct named import capability remains, while wildcard-export behavior can differ. This is a bounded consumer question, not a claim of an affected real consumer or an approved __all__ restoration objective.

Primary current sources: [template](../../../.pgmcp/template_suite/python_worker/template.jinja2), [schema](../../../.pgmcp/template_suite/python_worker/context.schema.json).

### Pytest Unit Test and Integration Test

Current families require at least one explicitly supplied nonblank case. Cases, optional fixtures, module/case markers, sync/async and optional class grouping are rendered from caller content. Current Unit filled preserves the selected fixture decorator, scope/autouse, body, marker and assert. Integration filled preserves the file-round-trip body and typed tmp_path parameter.

Old Unit forces a class, mocking/import defaults and AAA framing; absent case content can yield assert True or a placeholder comparing None == None. Old Integration assumes filesystem/workspace cleanup, E2E/full-stack prose, async/plugin imports and an inferred workspace fixture. Those guesses are intentionally removed by catalog 76/88/418 and Design §7.7/§9.

AAA behavior and comments remain expressible in the case body; fixtures and mocking remain explicit source/dependencies. Removing automatic AAA comments is not deleting Arrange/Act/Assert capacity. Current schemas do not certify that a case has a useful assertion or truly tests collaboration.

Translation limits: old comparison bodies are placed intact in the assertions fragment; empty Arrange/Act fragments cause old TODO comments. Typed parameters occupy the old fixture-text insertion slots. The old Unit uses explicit builtins/sum or pathlib/Path probe imports, and module usefixtures is projected onto its one case. Its root cannot render the supplied sample_path fixture definition. Old Integration's inferred temp_workspace remains extra generated behavior. These old files are syntax evidence, not standalone runnable equivalent test suites.

Primary current sources: [Unit template](../../../.pgmcp/template_suite/pytest_unit_test/template.jinja2), [Unit schema](../../../.pgmcp/template_suite/pytest_unit_test/context.schema.json), [Integration template](../../../.pgmcp/template_suite/pytest_integration_test/template.jinja2), [Integration schema](../../../.pgmcp/template_suite/pytest_integration_test/context.schema.json), [shared pytest pattern](../../../.pgmcp/template_suite/shared/templates/patterns/testing/pytest.jinja2).

## Human-qualified whitespace decision — 2026-10-03

The human agreed to the bounded Python native format/lint objective, while explicitly requiring a separate assessment of tidy whitespace. [Eight targeted untouched probes](whitespace-comparison.md) distinguish generated joins, omitted/empty carriers, EOF and caller-owned internal spacing. All four Python examples would be reformatted; the formatter also changes a deliberately authored body separator.

[Research](research.md#human-approved-python-quality-and-independent-whitespace-objective--2026-10-03) records the authoritative approval boundary. Numerical generated-join limits, exact EOF criteria and runtime enforcement remain discussion choices. Existing comparison evidence stays unchanged; no caller-content normalization or production fix follows from this decision.

## Standards assessment and possible objectives

[CODE_STYLE](../../coding_standards/CODE_STYLE.md) assigns whitespace/import/line-length conventions to configured native tools, documentation to meaningful contracts and mutability/examples to their owner. [Architecture](../../coding_standards/ARCHITECTURE_PRINCIPLES.md) requires constructor injection, frozen query-result values and pure configuration models. [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) governs evidence and Research/Design ownership.

Current templates support explicit injection, immutable DTOs, distinct Config mutability and pure configuration models. They do not establish architecture compliance for arbitrary caller-authored bodies or the semantic role of a generated model. A one-line quoted Python string can be a valid docstring; absence of triple quotes alone is not a current standards violation. The old layer/dependency/responsibility prose and mandatory logger are not universal current style requirements.

The actionable first-output problems in this batch are native formatting/lint defects in generated structure and overcompact model expressions. Possible objectives, still awaiting human choice:
- Template-generated Python structure should be native formatter/linter clean under the configured baseline for appropriate minimal/representative and meaningful boundary contexts; preserve caller body/value semantics.
- Model configuration/examples/field arguments should remain readable and within the configured baseline rather than concatenate ordinary caller records into overlong lines.
- Preserve explicit portable contracts; no automatic restoration of forced logger, lifecycle, test class, fabricated passing tests or project-specific factory imports.
- Decide whether a repeated DTO Fields docstring summary is useful presentation and whether Worker should explicitly declare exports, based on a concrete need. Neither is automatically required by current standards.

No broader model-example execution, schema/template consumption analyzer, new runtime formatter or automatic dependencies are introduced. #476 remains separate; these package-level examples can inform it without assuming its enforcement or implementation scope.

The rendered examples are representative rather than exhaustive: async/class grouping, richer import mixtures, all scalar/container/default/constraint combinations and every fixture/marker branch need meaningful targeted evidence if selected objectives require them. The existing #460 conformance obligations are distinct from this new first-output quality question. Delegated source checks were findings-only; they did not issue independent QA GO.

## Exact translated legacy contexts

The original v3 contexts remain in the survey. The following records are enough to reproduce each raw legacy call with the selected root/template and authorized renderer. Where the new contract has no old equivalent slot, the family sections explicitly identify that limit.

### python_pydantic_dto — minimal

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/dto.py.jinja2`.

```json
{
  "artifact_type": "dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceSnapshot",
  "name": "PriceSnapshot",
  "description": "A price snapshot.",
  "frozen": true,
  "examples": [],
  "fields": []
}
```

### python_pydantic_dto — filled

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/dto.py.jinja2`.

```json
{
  "artifact_type": "dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceSnapshot",
  "name": "PriceSnapshot",
  "description": "A price snapshot.",
  "module_description": "Validated market data.",
  "frozen": true,
  "examples": [
    {
      "symbol": "ABC",
      "mid": 101.25
    }
  ],
  "fields": [
    {
      "name": "symbol",
      "type": "str",
      "description": "Instrument identifier."
    },
    {
      "name": "mid",
      "type": "float",
      "description": "Mid-market price."
    },
    {
      "name": "observed_at",
      "type": "datetime.datetime",
      "description": "Observation time.",
      "default_factory": "datetime.datetime.now"
    }
  ]
}
```

### python_pydantic_config — minimal

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/config_schema.py.jinja2`.

```json
{
  "artifact_type": "schema",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "RiskSettings",
  "name": "RiskSettings",
  "description": "Risk settings.",
  "frozen": true,
  "examples": [],
  "fields": []
}
```

### python_pydantic_config — filled

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/config_schema.py.jinja2`.

```json
{
  "artifact_type": "schema",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "RiskSettings",
  "name": "RiskSettings",
  "description": "Risk settings.",
  "module_description": "Risk controls for one strategy.",
  "frozen": false,
  "examples": [
    {
      "enabled": true,
      "max_order_size": 5,
      "label": "primary"
    }
  ],
  "fields": [
    {
      "name": "enabled",
      "type": "bool",
      "description": "Enable order submission.",
      "default": "False"
    },
    {
      "name": "max_order_size",
      "type": "int",
      "description": "Maximum permitted order size.",
      "default": "0"
    },
    {
      "name": "label",
      "type": "str",
      "description": "Optional operator label.",
      "default": "''"
    }
  ]
}
```

### python_worker — minimal

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/worker.py.jinja2`.

```json
{
  "artifact_type": "worker",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceWorker",
  "name": "PriceWorker",
  "layer": "Backend (Workers)",
  "module_description": "Processes a price update."
}
```

### python_worker — filled

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/worker.py.jinja2`.

```json
{
  "artifact_type": "worker",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceWorker",
  "name": "PriceWorker",
  "layer": "Backend (Workers)",
  "module_description": "Publishes a price update."
}
```

### pytest_unit_test — minimal

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/test_unit.py.jinja2`.

```json
{
  "artifact_type": "unit_test",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "First-output test comparison",
  "description": "Check a small arithmetic result.",
  "test_description": "Check a small arithmetic result.",
  "test_class_name": "TestFirstOutputSamples",
  "module_under_test": "builtins",
  "imported_classes": [
    "sum"
  ],
  "test_methods": [
    {
      "name": "test_sum",
      "description": "Add two values.",
      "async": false,
      "fixtures": [],
      "return_type": "None",
      "arrange": "",
      "act": "",
      "assertions": "result = sum([2, 3])\nassert result == 5",
      "markers": []
    }
  ]
}
```

### pytest_unit_test — filled

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/test_unit.py.jinja2`.

```json
{
  "artifact_type": "unit_test",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "First-output test comparison",
  "description": "Check serialized fixture content.",
  "test_description": "Check serialized fixture content.",
  "test_class_name": "TestFirstOutputSamples",
  "module_under_test": "pathlib",
  "imported_classes": [
    "Path"
  ],
  "test_methods": [
    {
      "name": "test_sample_content",
      "description": "Read the fixture file.",
      "async": false,
      "fixtures": [
        "sample_path: Path"
      ],
      "return_type": "None",
      "arrange": "",
      "act": "",
      "assertions": "assert sample_path.read_text(encoding=\"utf-8\") == \"ready\"",
      "markers": [
        "usefixtures(\"sample_path\")"
      ]
    }
  ]
}
```

### pytest_integration_test — minimal

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/test_integration.py.jinja2`.

```json
{
  "artifact_type": "integration_test",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "First-output test comparison",
  "description": "Check a rendered integration result.",
  "test_description": "Check a rendered integration result.",
  "test_class_name": "TestFirstOutputSamples",
  "test_scenario": "Check a rendered integration result.",
  "test_methods": [
    {
      "name": "test_total",
      "description": "Add two values.",
      "async": false,
      "fixtures": [],
      "return_type": "None",
      "arrange": "",
      "act": "",
      "assertions": "result = sum([2, 3])\nassert result == 5",
      "markers": []
    }
  ]
}
```

### pytest_integration_test — filled

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/test_integration.py.jinja2`.

```json
{
  "artifact_type": "integration_test",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "First-output test comparison",
  "description": "Check a temporary file round trip.",
  "test_description": "Check a temporary file round trip.",
  "test_class_name": "TestFirstOutputSamples",
  "test_scenario": "Check a temporary file round trip.",
  "test_methods": [
    {
      "name": "test_file_round_trip",
      "description": "Write and read a temporary file.",
      "async": false,
      "fixtures": [
        "tmp_path: Path"
      ],
      "return_type": "None",
      "arrange": "",
      "act": "",
      "assertions": "source = tmp_path / \"input.txt\"\nsource.write_text(\"payload\", encoding=\"utf-8\")\nassert source.read_text(encoding=\"utf-8\") == \"payload\"",
      "markers": []
    }
  ]
}
```

### python_adapter — minimal

Root: `C:/1Voudig/99_Programming/ST/.pgmcp/templates`; template: `concrete/adapter.py.jinja2`.

```json
{
  "artifact_type": "adapter",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceAdapter",
  "name": "PriceAdapter",
  "description": "Adapts a price source."
}
```

### python_adapter — filled

Root: `C:/1Voudig/99_Programming/ST/.pgmcp/templates`; template: `concrete/adapter.py.jinja2`.

```json
{
  "artifact_type": "adapter",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceAdapter",
  "name": "PriceAdapter",
  "description": "Adapts a price source.",
  "module_description": "Market data adapter.",
  "methods": [
    {
      "name": "read_price",
      "params": "symbol: str",
      "return_type": "int",
      "docstring": "Return the latest price.",
      "body": "return self._client.read_price(symbol)"
    }
  ]
}
```

### python_protocol — minimal

Root: `C:/1Voudig/99_Programming/ST/.pgmcp/templates`; template: `concrete/interface.py.jinja2`.

```json
{
  "artifact_type": "interface",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceSource",
  "name": "PriceSource",
  "description": "Provides price data."
}
```

### python_protocol — filled

Root: `C:/1Voudig/99_Programming/ST/.pgmcp/templates`; template: `concrete/interface.py.jinja2`.

```json
{
  "artifact_type": "interface",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceSource",
  "name": "PriceSource",
  "description": "Provides price data.",
  "module_description": "Contract for reading market prices.",
  "methods": [
    {
      "name": "read_price",
      "params": "symbol: str",
      "return_type": "int",
      "docstring": "Return a price for one symbol."
    },
    {
      "name": "close",
      "params": "",
      "return_type": "None",
      "docstring": "Release the source resources."
    }
  ]
}
```

### python_pydantic_dto — minimal — hidden_dto_v2

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/dto_v2.py.jinja2`.

```json
{
  "dto_name": "PriceSnapshot",
  "description": "A price snapshot.",
  "artifact_type": "dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceSnapshot",
  "fields": []
}
```

### python_pydantic_dto — filled — hidden_dto_v2

Root: `C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates`; template: `concrete/dto_v2.py.jinja2`.

```json
{
  "dto_name": "PriceSnapshot",
  "description": "A price snapshot.",
  "artifact_type": "dto",
  "version_hash": "comparison-only",
  "timestamp": "2026-10-02T12:00:00Z",
  "format": "python",
  "output_path": "",
  "title": "PriceSnapshot",
  "fields": [
    "symbol: str",
    "mid: float",
    "observed_at: datetime.datetime"
  ]
}
```

## Source and file identities

Relevant root/base/model/testing source identities are indexed below. The complete original/alternate Jinja manifests were also measured for the earlier [document-family comparison](document-family-comparison.md#source-identities). This manifest does not assert a common historical checkout for the two roots.

```json
[
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/config_schema.py.jinja2",
    "sha256": "d6b8025522cd44824c4d373f1eed6b1cc9c1f8dab94de620af93de3948f9b911"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/dto.py.jinja2",
    "sha256": "8745373f84582dbe1cde01faf109f563b3115e73b8b334120d15f821c2f2b5f8"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/dto_v2.py.jinja2",
    "sha256": "07d3e0f6f88b6e0eb77162116dc0259e3dc1a9876a356de4bd91e57d366db1c1"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/test_integration.py.jinja2",
    "sha256": "e6d4c37b8cc5361a39d891da70bc100627aff6c6561c942e2810a43d08bc3f47"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/test_unit.py.jinja2",
    "sha256": "bea94ac07eabc0eb4be49effad832dc567b3947bb51616e4f3953fd7eb7b0adb"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/concrete/worker.py.jinja2",
    "sha256": "9a25c23fd71ec931a85cec6eb563925c8db6d1a0d23ada24c724d92b72cde1d0"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier0_base_artifact.jinja2",
    "sha256": "07c1ebf7df1accfe88cdfcd28fbaa07d4182c099411e344b68fd2c43d0576875"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_code.jinja2",
    "sha256": "b7cc8a03c49c613241947e0825eea96f3e7b8ccbcaae849888c5c36d054d1187"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_config.jinja2",
    "sha256": "b624150db5499f7c37cc8f60e82ab1d9ab45685b5f3fe89f9306eb0db8c8bc21"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_document.jinja2",
    "sha256": "53638c9c61478a747b969a4e2444de01e276f569fc4a20cbdd7f790a27da3ce1"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier1_base_tracking.jinja2",
    "sha256": "92b133451d44b1e9ae469dff9a585f43136df06bead19be552c7f1243b7b7d7f"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_base_markdown.jinja2",
    "sha256": "1b659bbbb5cae1dab79d8b1d941c5d6a4dfb7d9f1fcde9a254e852893b6f2e71"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_base_python.jinja2",
    "sha256": "29361d5d8df6c5d6b8a8fe26640e38e508e8fe8dec44e57b87fd0653329d12f7"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier2_base_yaml.jinja2",
    "sha256": "5cd78e1f28c5985fbbb007cc8c54fb47ab7d0d99353d0155f5a04906811cf87f"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_logging.jinja2",
    "sha256": "efd77d62436d84a17f4cf8bb6d7c0bfe3d95fa64f12767fa162d165df8ff7c0e"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_pydantic.jinja2",
    "sha256": "8845488b0b1f57d6df0ed648466deec21a4a70380b6eeba78da664574661b205"
  },
  {
    "path": "C:/temp/st3.worktrees/agents-bugfixget-project-plan-phase-8383c97a/mcp_server/scaffolding/templates/tier3_pattern_python_typed_id.jinja2",
    "sha256": "af9e67f6238f3acf0e01bcaf523f854248d947f555432bf70ec9c9ec31571299"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/adapter.py.jinja2",
    "sha256": "d3f53a6c0fc875ab96942657406840b8e1bcf76aec73407fc68a7ab9b38c559e"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/concrete/interface.py.jinja2",
    "sha256": "93d1c6401ec9297dc370152d71ec2680d1c205c30c4027416ec1b07e317a0620"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier0_base_artifact.jinja2",
    "sha256": "8b531031e82c7315ce95deebe1e88e12e46aaffb86a5707bafba5869443d4b18"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_code.jinja2",
    "sha256": "b7cc8a03c49c613241947e0825eea96f3e7b8ccbcaae849888c5c36d054d1187"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_config.jinja2",
    "sha256": "b624150db5499f7c37cc8f60e82ab1d9ab45685b5f3fe89f9306eb0db8c8bc21"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_document.jinja2",
    "sha256": "c8005bc960f83bc1f0a5b132b83e80afb6ff9a09ef26b0bef664ef50f69c6042"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier1_base_tracking.jinja2",
    "sha256": "92b133451d44b1e9ae469dff9a585f43136df06bead19be552c7f1243b7b7d7f"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_markdown.jinja2",
    "sha256": "1b659bbbb5cae1dab79d8b1d941c5d6a4dfb7d9f1fcde9a254e852893b6f2e71"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_python.jinja2",
    "sha256": "29361d5d8df6c5d6b8a8fe26640e38e508e8fe8dec44e57b87fd0653329d12f7"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_typescript.jinja2",
    "sha256": "cd7afe9f3e57d832cad092eff62caf54ee32f9dd447630dbef2d3130c7498bfb"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier2_base_yaml.jinja2",
    "sha256": "5cd78e1f28c5985fbbb007cc8c54fb47ab7d0d99353d0155f5a04906811cf87f"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_logging.jinja2",
    "sha256": "efd77d62436d84a17f4cf8bb6d7c0bfe3d95fa64f12767fa162d165df8ff7c0e"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_pydantic.jinja2",
    "sha256": "8845488b0b1f57d6df0ed648466deec21a4a70380b6eeba78da664574661b205"
  },
  {
    "path": "C:/1Voudig/99_Programming/ST/.pgmcp/templates/tier3_pattern_python_typed_id.jinja2",
    "sha256": "af9e67f6238f3acf0e01bcaf523f854248d947f555432bf70ec9c9ec31571299"
  }
]
```

All sixteen legacy files match their raw render strings; all fourteen v3 files match the original survey hashes. File identities:

```json
[
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-minimal-render.py",
    "sha256": "9c44ec94767bad1072ab6a5194e5c55949a365c5c5502149bf9d7da8fcc7f81e",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-filled-render.py",
    "sha256": "796c641925f591ad9acf9e31059960103cde9934e15c4e93e7e1346c9d7c7443",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_config.v2-minimal-render.py",
    "sha256": "77df5ad338ac61ac342c87c370124768abb662fe7d635dadb803023227e8528f",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_config.v2-filled-render.py",
    "sha256": "65b7421694716b3b73811ff95ec18419a42170372bc60b04b4dcf3366fa25de8",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_worker.v2-minimal-render.py",
    "sha256": "cfb1c0a6f851edcb3053f8dc604db9f3f02a6bf23383ded87f8f3008f21b73c4",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_worker.v2-filled-render.py",
    "sha256": "47a6550033c8f5e95a88dcfe06ecc06f5fa6e5c90f7e1614f66119672240ccd8",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_unit_test.v2-minimal-render.py",
    "sha256": "c32e9dd365f483e9734612f308b22aa6b636e0756cfccd460211ec80e08c3588",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_unit_test.v2-filled-render.py",
    "sha256": "db77696380859a49e9e12f2474e8d593bc874c9cee772d6d28ec96c124a6e787",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_integration_test.v2-minimal-render.py",
    "sha256": "cbfc699bca5fe4aee3909b0f7c72d1fd3c0643d399956e06796009a60c0de797",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_integration_test.v2-filled-render.py",
    "sha256": "515c4223f7466e00aa5af5003339302d88ac8d7026f30d5aba64bb76beda94a7",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_adapter.v2-minimal-render.py",
    "sha256": "1a4e0bd3ef60e40ee87e0900998e73abe90a342158c54bea7d6a185584240a40",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_adapter.v2-filled-render.py",
    "sha256": "5c255716d895110ee1eebe8d8aa1b27a655a3fb8930ba0abae2d0dabedd97a80",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_protocol.v2-minimal-render.py",
    "sha256": "75b2a773e8d7ebbedae4ef2bf64480edcfec286fafa90b7681518c0cd01cc21f",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_protocol.v2-filled-render.py",
    "sha256": "e67d0b4602dc560bbf466e73bf540e106c8132266f5a07a1cf0d52eeafb660a3",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-minimal-hidden-render.py",
    "sha256": "ab11b191bc46c0c38f2a252495fbbaad3eda98a025408bcdc826d60dcfce3fca",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-filled-hidden-render.py",
    "sha256": "54a2f06ad4c84600c05a2adca84a3238b819b48517da1b6ad2bc73a828354f5c",
    "matches_raw": true
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_pydantic_dto.minimal.py",
    "sha256": "4caafa43388bd02a622927bb5e9ea7f6e93cef600fb9a880df9a42fe651e06c7"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_pydantic_dto.filled.py",
    "sha256": "d59202a33d7ae2ca91f13ae2b9f7665a29b1455a5f6ee06d2a135a1afe8445ef"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_pydantic_config.minimal.py",
    "sha256": "4c16609539b813e6ab583c40e108c7c26cdc539e46cf3a4d431b1c78965ee21f"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_pydantic_config.filled.py",
    "sha256": "f501b7eda3e79fcad545bb65476cf0fb4f21a38df44e5bad826d629ecef61aab"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_worker.minimal.py",
    "sha256": "bfe07c8a73bdbb11fc1052a5d53fba59f7ecedd0ea4f8ffce664c81dfc020a5f"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_worker.filled.py",
    "sha256": "63ba23aea0003bae0b1abbef2491c9936b48665ee14fc824090627e353f76d1f"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/pytest_unit_test.minimal.py",
    "sha256": "7c88e587df1bdeb914a02257f41a4923e3a792e4f925f1837b5e47b13be7bfb4"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/pytest_unit_test.filled.py",
    "sha256": "2219a7ceb1435ed9313a1dffe8986fb66079071ccb992760209a311f38e37227"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/pytest_integration_test.minimal.py",
    "sha256": "4a424715f8cefe8f0b16c90628eccfacd3a5c016c4d3c3d615da24bd6c16e5e4"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/pytest_integration_test.filled.py",
    "sha256": "b9695e5d94812327baa9453133630ed45854ba1af1f37effd5b5d051ff4d1adc"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_adapter.minimal.py",
    "sha256": "8b9e724fe4571c037457e9f6838b0d363ae8efabfe8a4a1123f806d7152401d9"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_adapter.filled.py",
    "sha256": "9e9c1002268d8280433ae210285e8249eb0a7f5404b1d61e95089b130e672e6e"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_protocol.minimal.py",
    "sha256": "cfa3a7443a096ca9e7bf231b7869813fa98715eea36b6a031f8b1de760f4ac4b"
  },
  {
    "path": ".pgmcp/temp/issue473-survey/python_protocol.filled.py",
    "sha256": "4b3a9256073a93cc41dc7f5c260652f64a67b5d32d18ff57ba83f09e01db7983"
  }
]
```

## Native evidence and persistence receipts

The public syntax result of each final rewrite, including the three failed old DTO outputs, is retained below. All complete cached DTOs were read. The worker module-description mapping was refined before final hash verification; these are its final rewrite receipts. Source bytes were not repaired.

```json
[
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/9437ab18d7034779b94e23c03c2a38a0",
    "status": "failed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "failed",
        "evidence": {
          "format": "text",
          "data": "filename: C:\\temp\\pgmcp\\.pgmcp\\temp\\issue473-comparison-04\\python_pydantic_dto.v2-minimal-render.py\nline 24, column 4\nsource:     model_config = {\nmessage: unexpected indent"
        },
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 1,
            "stdout": {
              "observed_bytes": 343,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/1f1a9409712e4fd39cc2128fc1a327f3",
    "status": "failed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "failed",
        "evidence": {
          "format": "text",
          "data": "filename: C:\\temp\\pgmcp\\.pgmcp\\temp\\issue473-comparison-04\\python_pydantic_dto.v2-filled-render.py\nline 15, column 49\nsource: from backend.utils.id_generators import datetime.datetime.now\nmessage: invalid syntax"
        },
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 1,
            "stdout": {
              "observed_bytes": 378,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_config.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/c2d56e9179dc4ed8823a7a18b68d785d",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_config.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/bbf996a312034af39848f94f0f8f37cf",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_worker.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/d09e41b33bf94062aba28cd3577367c7",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_worker.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/7f28ea62c0104315ae45f47ddc6d25cf",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_unit_test.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/55257991611f470b82c38536ad6db90d",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_unit_test.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/4962290fc087465aa132b638dd20958e",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_integration_test.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/79f9ed42d8374b9897e962888afcc655",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/pytest_integration_test.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/25a88d2b082240a4a120d73ddd4a52e5",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_adapter.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/bb5f1b352a0a41568df15369a59ddf07",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_adapter.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/fe85b3a2fe3f4fdc9b4fa54f5bc60a88",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_protocol.v2-minimal-render.py",
    "uri": "pgmcp://cache/runs/fc2d0b67660a427ebc2599094975d7d8",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_protocol.v2-filled-render.py",
    "uri": "pgmcp://cache/runs/51ad33c3b3b945e0a8e32cf334912f55",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-minimal-hidden-render.py",
    "uri": "pgmcp://cache/runs/82e55b94cf314782882278fd9390eeb7",
    "status": "failed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "failed",
        "evidence": {
          "format": "text",
          "data": "filename: C:\\temp\\pgmcp\\.pgmcp\\temp\\issue473-comparison-04\\python_pydantic_dto.v2-minimal-hidden-render.py\nline 23, column 4\nsource:     model_config = {\nmessage: unexpected indent"
        },
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 1,
            "stdout": {
              "observed_bytes": 350,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  },
  {
    "path": ".pgmcp/temp/issue473-comparison-04/python_pydantic_dto.v2-filled-hidden-render.py",
    "uri": "pgmcp://cache/runs/4e14b43208d446ed8aff9f9c88dfc465",
    "status": "passed",
    "checks": [
      {
        "check_id": "python_syntax",
        "status": "passed",
        "evidence": null,
        "invocation": {
          "adapter": {
            "adapter_id": "python_syntax",
            "version": "1.0.0",
            "fingerprint": "fFdZApJt3--_OH0o",
            "contract_version": 1
          },
          "capture": {
            "exit_code": 0,
            "stdout": {
              "observed_bytes": 92,
              "head": null,
              "tail": null,
              "truncated": false
            },
            "stderr": {
              "observed_bytes": 0,
              "head": "",
              "tail": "",
              "truncated": false
            }
          },
          "external_tools": [
            {
              "tool_id": "python",
              "version": "3.13.7"
            }
          ]
        }
      }
    ]
  }
]
```

Fresh fourteen-target public native quality result, fully read from the cache:

```json
{
  "success": true,
  "run_status": "failed",
  "requested_scope": "targets",
  "requested_targets": [
    ".pgmcp/temp/issue473-survey/python_pydantic_dto.minimal.py",
    ".pgmcp/temp/issue473-survey/python_pydantic_dto.filled.py",
    ".pgmcp/temp/issue473-survey/python_pydantic_config.minimal.py",
    ".pgmcp/temp/issue473-survey/python_pydantic_config.filled.py",
    ".pgmcp/temp/issue473-survey/python_worker.minimal.py",
    ".pgmcp/temp/issue473-survey/python_worker.filled.py",
    ".pgmcp/temp/issue473-survey/pytest_unit_test.minimal.py",
    ".pgmcp/temp/issue473-survey/pytest_unit_test.filled.py",
    ".pgmcp/temp/issue473-survey/pytest_integration_test.minimal.py",
    ".pgmcp/temp/issue473-survey/pytest_integration_test.filled.py",
    ".pgmcp/temp/issue473-survey/python_adapter.minimal.py",
    ".pgmcp/temp/issue473-survey/python_adapter.filled.py",
    ".pgmcp/temp/issue473-survey/python_protocol.minimal.py",
    ".pgmcp/temp/issue473-survey/python_protocol.filled.py"
  ],
  "selected_profile": null,
  "removed_targets": [],
  "results": [
    {
      "check_id": "python_format",
      "status": "failed",
      "reason": null,
      "message": "14 files would be reformatted",
      "evidence": {
        "format": "text",
        "data": "stdout:\n--- .pgmcp\\temp\\issue473-survey\\pytest_integration_test.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\pytest_integration_test.filled.py\n@@ -6,14 +6,8 @@\n from pathlib import Path\n \n \n-\n-\n-\n def test_file_round_trip(tmp_path: Path) -> None:\n     \"Write and read a temporary file.\"\n     source = tmp_path / \"input.txt\"\n     source.write_text(\"payload\", encoding=\"utf-8\")\n     assert source.read_text(encoding=\"utf-8\") == \"payload\"\n-\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\pytest_integration_test.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\pytest_integration_test.minimal.py\n@@ -3,13 +3,7 @@\n \"Check a rendered integration result.\"\n \n \n-\n-\n-\n def test_total() -> None:\n     \"Add two values.\"\n     result = sum([2, 3])\n     assert result == 5\n-\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\pytest_unit_test.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\pytest_unit_test.filled.py\n@@ -11,18 +11,15 @@\n \n pytestmark = [pytest.mark.usefixtures(\"sample_path\")]\n \n+\n @pytest.fixture(scope=\"function\", autouse=False)\n def sample_path(tmp_path: Path) -> Path:\n     \"Write a temporary text file.\"\n     path = tmp_path / \"sample.txt\"\n     path.write_text(\"ready\", encoding=\"utf-8\")\n     return path\n-\n \n \n def test_sample_content(sample_path: Path) -> None:\n     \"Read the fixture file.\"\n     assert sample_path.read_text(encoding=\"utf-8\") == \"ready\"\n-\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\pytest_unit_test.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\pytest_unit_test.minimal.py\n@@ -3,13 +3,7 @@\n \"Check a small arithmetic result.\"\n \n \n-\n-\n-\n def test_sum() -> None:\n     \"Add two values.\"\n     result = sum([2, 3])\n     assert result == 5\n-\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_adapter.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\python_adapter.filled.py\n@@ -2,16 +2,13 @@\n \n \"Market data adapter.\"\n \n-\n # Standard library\n import logging\n \n # Project\n from market_ports import PriceClient\n-\n \n \n-\n logger = logging.getLogger(\"market.adapter\")\n \n \n@@ -20,11 +17,7 @@\n \n     def __init__(self, client: PriceClient) -> None:\n         self._client = client\n-\n \n     def read_price(self, symbol: str) -> int:\n         \"Return the latest price.\"\n         return self._client.read_price(symbol)\n-\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_adapter.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\python_adapter.minimal.py\n@@ -3,14 +3,7 @@\n \"Adapts a price source.\"\n \n \n-\n-\n-\n class PriceAdapter:\n     \"Adapts a price source.\"\n-\n \n-\n     pass\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_protocol.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\python_protocol.filled.py\n@@ -2,10 +2,8 @@\n \n \"Contract for reading market prices.\"\n \n-\n # Standard library\n from typing import Protocol\n-\n \n \n class PriceSource(Protocol):\n@@ -18,5 +16,3 @@\n     def close(self) -> None:\n         \"Release the source resources.\"\n         ...\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_protocol.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\python_protocol.minimal.py\n@@ -2,15 +2,11 @@\n \n \"Provides price data.\"\n \n-\n # Standard library\n from typing import Protocol\n-\n \n \n class PriceSource(Protocol):\n     \"Provides price data.\"\n \n     pass\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_pydantic_config.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\python_pydantic_config.filled.py\n@@ -2,20 +2,20 @@\n \n \"Risk controls for one strategy.\"\n \n-\n-\n-\n # Third party\n from pydantic import BaseModel, ConfigDict, Field\n-\n \n \n class RiskSettings(BaseModel):\n     \"Risk settings.\"\n \n-    model_config = ConfigDict(extra=\"forbid\", frozen=False, json_schema_extra={\"examples\": [{\"enabled\": True, \"max_order_size\": 5, \"label\": \"primary\"}]})\n+    model_config = ConfigDict(\n+        extra=\"forbid\",\n+        frozen=False,\n+        json_schema_extra={\n+            \"examples\": [{\"enabled\": True, \"max_order_size\": 5, \"label\": \"primary\"}]\n+        },\n+    )\n     enabled: bool = Field(default=False, description=\"Enable order submission.\")\n     max_order_size: int = Field(default=0, description=\"Maximum permitted order size.\", ge=0)\n     label: str = Field(default=\"\", description=\"Optional operator label.\", min_length=0)\n-\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_pydantic_config.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\python_pydantic_config.minimal.py\n@@ -2,17 +2,11 @@\n \n \"Risk settings.\"\n \n-\n-\n-\n # Third party\n from pydantic import BaseModel, ConfigDict\n \n \n-\n class RiskSettings(BaseModel):\n     \"Risk settings.\"\n \n     model_config = ConfigDict(extra=\"forbid\", frozen=True)\n-    \n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.filled.py\n@@ -2,23 +2,23 @@\n \n \"Validated market data.\"\n \n-\n-\n-\n # Standard library\n import datetime\n \n # Third party\n from pydantic import BaseModel, ConfigDict, Field\n-\n \n \n class PriceSnapshot(BaseModel):\n     \"A price snapshot.\"\n \n-    model_config = ConfigDict(extra=\"forbid\", frozen=True, json_schema_extra={\"examples\": [{\"symbol\": \"ABC\", \"mid\": 101.25}]})\n+    model_config = ConfigDict(\n+        extra=\"forbid\",\n+        frozen=True,\n+        json_schema_extra={\"examples\": [{\"symbol\": \"ABC\", \"mid\": 101.25}]},\n+    )\n     symbol: str = Field(description=\"Instrument identifier.\", min_length=1)\n     mid: float = Field(description=\"Mid-market price.\", gt=0)\n-    observed_at: datetime.datetime = Field(default_factory=datetime.datetime.now, description=\"Observation time.\")\n-\n-\n+    observed_at: datetime.datetime = Field(\n+        default_factory=datetime.datetime.now, description=\"Observation time.\"\n+    )\n\n--- .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.minimal.py\n@@ -2,17 +2,11 @@\n \n \"A price snapshot.\"\n \n-\n-\n-\n # Third party\n from pydantic import BaseModel, ConfigDict\n \n \n-\n class PriceSnapshot(BaseModel):\n     \"A price snapshot.\"\n \n     model_config = ConfigDict(extra=\"forbid\", frozen=True)\n-    \n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_worker.filled.py\n+++ .pgmcp\\temp\\issue473-survey\\python_worker.filled.py\n@@ -2,16 +2,13 @@\n \n \"Publishes a price update.\"\n \n-\n # Standard library\n import logging\n \n # Project\n from market_ports import PriceClient\n-\n \n \n-\n logger = logging.getLogger(\"market.worker\")\n \n \n@@ -24,4 +21,3 @@\n     def process(self, symbol: str, value: int) -> None:\n         \"Publish the accepted price update.\"\n         self._client.publish(symbol, value)\n-\n\n--- .pgmcp\\temp\\issue473-survey\\python_worker.minimal.py\n+++ .pgmcp\\temp\\issue473-survey\\python_worker.minimal.py\n@@ -3,13 +3,9 @@\n \"Processes a price update.\"\n \n \n-\n-\n-\n class PriceWorker:\n     \"Processes a price update.\"\n \n     def process(self, value: int) -> int:\n         \"Return one accepted value.\"\n         return value\n-\n\n\nstderr:\n14 files would be reformatted\n"
      },
      "external_tools": [
        {
          "tool_id": "ruff",
          "version": "0.15.6"
        }
      ],
      "adapter": {
        "adapter_id": "ruff",
        "version": "1.0.0",
        "fingerprint": "Y2FKuZ8LbIQH27t4",
        "contract_version": 1
      },
      "capture": {
        "exit_code": 1,
        "stdout": {
          "observed_bytes": 7424,
          "head": null,
          "tail": null,
          "truncated": false
        },
        "stderr": {
          "observed_bytes": 0,
          "head": "",
          "tail": "",
          "truncated": false
        }
      },
      "termination_problem": null,
      "request_rejection": null,
      "args_source": "configured",
      "effective_args": [],
      "coverage": null,
      "required_targets": []
    },
    {
      "check_id": "python_lint",
      "status": "failed",
      "reason": null,
      "message": "I001 [*] Import block is un-sorted or un-formatted",
      "evidence": {
        "format": "text",
        "data": "stdout:\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\pytest_integration_test.filled.py:6:1\n  |\n5 | # Standard library\n6 | from pathlib import Path\n  | ^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\pytest_unit_test.filled.py:6:1\n  |\n5 |   # Standard library\n6 | / from pathlib import Path\n7 | |\n8 | | # Third party\n9 | | import pytest\n  | |_____________^\n  |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n  --> .pgmcp\\temp\\issue473-survey\\python_adapter.filled.py:7:1\n   |\n 6 |   # Standard library\n 7 | / import logging\n 8 | |\n 9 | | # Project\n10 | | from market_ports import PriceClient\n   | |____________________________________^\n   |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\python_protocol.filled.py:7:1\n  |\n6 | # Standard library\n7 | from typing import Protocol\n  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\python_protocol.minimal.py:7:1\n  |\n6 | # Standard library\n7 | from typing import Protocol\n  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\python_pydantic_config.filled.py:9:1\n  |\n8 | # Third party\n9 | from pydantic import BaseModel, ConfigDict, Field\n  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nE501 Line too long (153 > 100)\n  --> .pgmcp\\temp\\issue473-survey\\python_pydantic_config.filled.py:16:101\n   |\n14 | …\n15 | …\n16 | …json_schema_extra={\"examples\": [{\"enabled\": True, \"max_order_size\": 5, \"label\": \"primary\"}]})\n   |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n17 | … order submission.\")\n18 | …mum permitted order size.\", ge=0)\n   |\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\python_pydantic_config.minimal.py:9:1\n  |\n8 | # Third party\n9 | from pydantic import BaseModel, ConfigDict\n  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nW293 [*] Blank line contains whitespace\n  --> .pgmcp\\temp\\issue473-survey\\python_pydantic_config.minimal.py:17:1\n   |\n16 |     model_config = ConfigDict(extra=\"forbid\", frozen=True)\n17 |     \n   | ^^^^\n   |\nhelp: Remove whitespace from blank line\n\nI001 [*] Import block is un-sorted or un-formatted\n  --> .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.filled.py:9:1\n   |\n 8 |   # Standard library\n 9 | / import datetime\n10 | |\n11 | | # Third party\n12 | | from pydantic import BaseModel, ConfigDict, Field\n   | |_________________________________________________^\n   |\nhelp: Organize imports\n\nE501 Line too long (126 > 100)\n  --> .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.filled.py:19:101\n   |\n17 |     \"A price snapshot.\"\n18 |\n19 |     model_config = ConfigDict(extra=\"forbid\", frozen=True, json_schema_extra={\"examples\": [{\"symbol\": \"ABC\", \"mid\": 101.25}]})\n   |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^\n20 |     symbol: str = Field(description=\"Instrument identifier.\", min_length=1)\n21 |     mid: float = Field(description=\"Mid-market price.\", gt=0)\n   |\n\nE501 Line too long (114 > 100)\n  --> .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.filled.py:22:101\n   |\n20 |     symbol: str = Field(description=\"Instrument identifier.\", min_length=1)\n21 |     mid: float = Field(description=\"Mid-market price.\", gt=0)\n22 |     observed_at: datetime.datetime = Field(default_factory=datetime.datetime.now, description=\"Observation time.\")\n   |                                                                                                     ^^^^^^^^^^^^^^\n   |\n\nI001 [*] Import block is un-sorted or un-formatted\n --> .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.minimal.py:9:1\n  |\n8 | # Third party\n9 | from pydantic import BaseModel, ConfigDict\n  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  |\nhelp: Organize imports\n\nW293 [*] Blank line contains whitespace\n  --> .pgmcp\\temp\\issue473-survey\\python_pydantic_dto.minimal.py:17:1\n   |\n16 |     model_config = ConfigDict(extra=\"forbid\", frozen=True)\n17 |     \n   | ^^^^\n   |\nhelp: Remove whitespace from blank line\n\nI001 [*] Import block is un-sorted or un-formatted\n  --> .pgmcp\\temp\\issue473-survey\\python_worker.filled.py:7:1\n   |\n 6 |   # Standard library\n 7 | / import logging\n 8 | |\n 9 | | # Project\n10 | | from market_ports import PriceClient\n   | |____________________________________^\n   |\nhelp: Organize imports\n\nFound 15 errors.\n[*] 12 fixable with the `--fix` option.\n"
      },
      "external_tools": [
        {
          "tool_id": "ruff",
          "version": "0.15.6"
        }
      ],
      "adapter": {
        "adapter_id": "ruff",
        "version": "1.0.0",
        "fingerprint": "Y2FKuZ8LbIQH27t4",
        "contract_version": 1
      },
      "capture": {
        "exit_code": 1,
        "stdout": {
          "observed_bytes": 5230,
          "head": null,
          "tail": null,
          "truncated": false
        },
        "stderr": {
          "observed_bytes": 0,
          "head": "",
          "tail": "",
          "truncated": false
        }
      },
      "termination_problem": null,
      "request_rejection": null,
      "args_source": "configured",
      "effective_args": [],
      "coverage": null,
      "required_targets": []
    }
  ],
  "error_code": null,
  "error_details": null
}
```

The original quality cache expired during this batch; its durable evidence remains in the survey. The fresh result independently confirms the same selected-surface defects. No whole-workspace Validation or generated-source runtime test was run.

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-02 | @imp researcher | Compare seven remaining Python families, both old DTO roots, exact legacy renders and fresh native quality evidence. |
| 0.2 | 2026-10-03 | @imp researcher | Record qualified native quality and independent whitespace assessment; index eight targeted raw examples without selecting numerical limits. |
