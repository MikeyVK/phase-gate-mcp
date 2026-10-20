<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue \#518 — source-owned typing and precise checker exceptions

**Status:** Design complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Restore the approved checker signals through existing source owners, preserving runtime behavior except the explicitly approved model-only cutover and logging robustness repair.

## Scope In

Concrete remaining source/native/local groups from Research; core input/decorators and direct consumers, Literal attributes, independent adapter JSON validation, config/model/presentation/state/factory/YAML inference, logging producer/runtime boundaries and proportional helper cleanup.

## Scope Out

New adapter/logging/decoder frameworks, SDK/Python migration, legacy bridges, unchecked casts, lost runtime guards, altered config/admission/projection policy, suite-wide test-Mypy or #533 gate changes, unrelated syntax/import/coverage work, Windows readiness, release and deployment.

## Problem Statement

Native blind spots and source-local exceptions outlived the migration. Existing supported validation must become visible to the checkers without pretending raw JSON already satisfies a schema, changing runtime rejection, weakening variance or hiding malformed logging data.

## Functional Requirements

- Every core tool declares and receives a Pydantic input model; no-argument tools use typed empty models and existing wire {} admission.
- Stored reason/stage attributes preserve the existing narrow Literal contracts and unchanged public failure values/cause chains.
- Existing validators narrow raw object containers and carry validated values without new dependencies/coercion or changed field/index/error ordering.
- Logging preserves primary metadata, event/message/severity/traceback, valid context and explicit diagnosis of malformed payload/collisions.
- Remaining suppressions receive a concrete remove/narrow/retain disposition and reassessment trigger under restored final native policy.

## Nonfunctional Requirements

- One existing owner for each responsibility; preserve injection, read-only/CQS boundaries, immutable DTOs/default freshness, package isolation and existing operation/public-schema/cache semantics.
- Use precise supported annotations, actual runtime checks and standard library/Pydantic facilities before exact justified exceptions; no zero-suppression quota.
- Existing behavior tests and temporary non-masked type controls prove contracts; no permanent diagnostic matrix, content snapshots, whole-test Mypy gate or unrelated test rewrite.

## Constraints

- Research40d4683b and the inherited final #513 Approved Strategy are binding; independent QA granted Research→Design.
- The current Pyright and Mypy capability manifests select python_production_sources. Branchscope applies that per-check filter; it does not select changed tests for those checks. Explicit targets deliberately bypass the filter.
- The four native-default-none Pyright rules are not newly enabled. Existing checker/dependency pins, native discovery, filename exclusions and check bindings remain unchanged.
- Settings lookup in test_support stays invocation-time under patching; CLI routing delay, library nullability, immutable JSON rejection and explicit variance remain meaningful.

## Options

### 1. Repair at each existing typed/dynamic owner

Chosen: model-only core contracts, source-local raw-container narrowing, precise declarations/defaults, standard Pydantic logging admission and exact necessary exceptions.

**Pros:**

- Preserves validation owners and package isolation.
- No second decoder/presenter/logger framework.

**Cons:**

- Requires honest local annotations and focused consumer migration across multiple source groups.

### 2. Central adapter/JSON/logging abstraction or broad Any/casts

Rejected: moves tool-specific validation knowledge across boundaries or masks the diagnostics rather than describing actual source facts.

### 3. Delete all suppressions/guards or rewrite the suite

Rejected: confuses diagnostic counts with defects, breaks approved variance/runtime rejection and exceeds test/gate scope.

### 4. Move every log property into a new nested props field

Rejected: unnecessarily relocates all normal event fields and changes existing JSON log consumers; reserve only metadata/collision diagnosis.

## Decision

Retain existing runtime ownership and apply a clean model-only input cutover. Preserve normal flat logging fields, with formatter-owned metadata, a typed producer carrier and standard strict per-property JSON validation plus explicit payload diagnosis. Restore the inherited checker policy after the affected source contracts are sound; retain only exact demonstrated exceptions.

## Rationale

The structural debt is incomplete boundary typing and broad masking, not missing frameworks. Separate raw object containers from validated values, preserve declared contracts at storage/return boundaries and make logging failure explicit without replacing the primary event. Existing branch selection already bounds type-checker test impact.

## Production Design

### Responsibilities and exact boundaries

| Existing owner | Target contract and preservation |
| --- | --- |
| ICoreTool / ITool / prepared inputs | args_model is mandatory type[BaseModel]; prepared input TypeVar bound becomes BaseModel. Keep explicit covariance/invariance declarations. InputValidationDecorator always yields a model before core execution; optional injected prepared contract remains an injection seam, not a None-input mode. |
| Concrete tools / forwarding decorators | Remove optional return annotations and impossible no-model fallbacks, retaining each existing model and wire shape. Empty models retain extra=forbid. Enforcement and outer exception wrappers keep order, facts and attachments. |
| Exception attributes | Explicit Literal annotations on the existing four exception types match their constructor contracts. Consumers keep current response literals; no cast, renamed error or widened value set. |
| Raw adapter JSON | Decode to object; source-local stdlib guards describe dict[object,object]/list[object] only. Existing key/field/path/item checks establish actual values; carry typed validated targets/args/scratch into the existing runner. Separate native report/prerequisite/config parsing remains at each package owner. |
| Config/model input | Before validators remain object→object. Preserve each original dict-versus-Mapping/list/tuple acceptance and error ordering; Pydantic still performs final domain admission. Existing string-key checks can justify dict[str,object], not an assumed final model. |
| Presentation/cache/stored context | Narrow dynamic reads before use, using existing DTO/config/schema types. Preserve required-null/unset distinctions, template/collection order, native errors, query purity and corruption/version handling; no new output or state policy. |
| Local inference/factories | Annotate existing containers and generic bindings; parameterize zero-argument list/dict/set constructors where supported. Fresh-per-instance defaults and constructors stay identical; concrete typed factory only when necessary. |
| Native library seams | Pydantic schema callback uses its supported schema type; Git branch HEAD uses the already-resolved commit hexsha, never a later-resolved literal HEAD. YAML calls the existing native represent_scalar through its precise string boundary; no replacement ScalarNode implementation or narrower LSP-breaking override. |
| Ordinary helper/local cleanup | Correct the three indexed annotations, typed lambdas and unnecessary private parameters; remove demonstrated unused codes/dormant Pylint/dead helper. Public keywords/interface/fixture/negative-input requirements receive exact source-specific treatment. |
| Logging | Existing core/logging.py remains the sole formatter/producer-carrier owner. Standard JsonValue admission handles nested JSON, not a custom recursive framework. Nine current producer modules use the typed carrier; process cleanup joins the existing props route. |

Private adapter context validation may return its already-proved scratch string alongside its existing error alternative, instead of returning success=None and re-indexing raw nested data. This is an internal seam only; wire protocol, native invocation, errors/order, prerequisites and writes are unchanged. No host-Pydantic/pgmcp model is introduced into independent packages; Commitlint's existing injected header reader is preserved.

Native raw guards certify only their actual check. Positive dict/list guards cannot claim string keys or valid JSON until those facts are checked. Do not widen accepted Mapping/subclass/tuple behavior or add finite-number/unknown-key rules as an adapter typing side effect.

### Logging metadata and data shape

Keep valid non-reserved props at their current top-level JSON keys. The formatter owns timestamp, level, logger, message, exception and the diagnostic key logging_payload. exception is reserved even without exc_info, so a payload cannot invent a traceback. The base timestamp continues using the existing LogRecord/formatter time representation.

_create_audit_props retains its per-event ISO time as event_timestamp. RestartServerOutput.timestamp, the on-disk restart marker, the three event identities, reason/pid/marker facts, restart exit42 and protocol signaling are unchanged. This names two existing facts explicitly; it does not silently discard producer time or label every event as the one restart instant.

logging_extra provides static typing only. StructuredFormatter validates every actual record.props, including raw stdlib Logger.extra callers that bypass the helper. Absent props is ordinary absence; props=None is an explicit malformed root. Nullable property values remain valid.

Use one formatter-owned standard TypeAdapter(JsonValue, config=ConfigDict(strict=True, allow_inf_nan=False)) on each top-level property. The existing project finite-JSON boundary already uses this library contract. validate_python is required for Python objects; validate_json is not a substitute. No new recursive validator, dataclass hierarchy, loggerwrapper, registry, error framework or default=str conversion is added.

A malformed property is not partially reconstructed: retain valid sibling properties and add its explicit validation diagnosis. ValidationError contributes only safe loc/type facts, prefixed with the property name; exclude raw input/context/URL data. These are validator locations (which may include union tags), not a promised JSON Pointer. Non-string top-level keys are diagnosed by parent location/index/type without stringifying the key. Native cycle/non-finite/object rejection must be proven in focused behavior.

A JSON-valid reserved-field collision is retained under logging_payload.reserved_fields with a reserved_field issue; it never overrides the base field. The diagnostic key is itself reserved, with a supplied same-name value retained as one nested conflicting value, not recursive envelope construction. Invalid collision values get an explicit diagnosis, not serialization or silent disappearance.

| Output field | Form |
| --- | --- |
| Existing base metadata / exception | Unchanged formatter-owned event fields and original traceback |
| Valid non-reserved props | Existing flat JSON properties, including explicit null |
| logging_payload.issues | Nonempty JSON list when malformed data/collision is present; entries have location, code, observed_type and optional entry_index |
| logging_payload.reserved_fields | JSON-valid conflicting values, keyed by their original reserved field; empty when no such values |
| No payload issue | No invented warning or diagnostic field |

Known producers supply only their actual typed JSON facts. The process cleanup directory/cause fields must be present in formatted JSON, not merely caplog metadata. Marker/result data must not be cast from raw decoded JSON into a claimed valid domain model merely to satisfy logging. Preserve its current business admission/error semantics; repair the existing typed producer values at their owner.

### Final policy and exception treatment

Remove broad tests ANN/ARG and tests.* untyped-definition relaxations after affected helpers/necessary exceptions are explicit. Remove approved false Pyright settings to restore strict defaults; deletion of missing-super/uninitialized-instance/default-initializer/implicit-string-concatenation flags does not opt into those four policies.

Every remaining equivalent group follows the Research/#513 disposition, including the seven independent versus twelve test-policy-dependent Ruff components, B017, terminal/cleanup/presentation BLE001, CLI/restart T201, ANN/ARG boundaries, variance/Pydantic/property limitations, frozen/invalid/mock/private cases and imports. Remove dormant Pylint, known unused ignores, genuinely dead helper and unused private workflow parameter. Narrow B017 to the observed ValidationError.

Ordinary local imports move only with source/patch/fixture proof. Keep route-dependent CLI imports and invocation-time Settings attribute lookup; do not eagerly bind a patchable class. Preserve source-demonstrated import timing if a focused counterexample establishes necessity, recording the exact rationale/trigger. This is suppression repair, not unrelated mass style rewriting.

For library signatures that remain incomplete, first use precise supported boundary types and runtime checks. A remaining exact source-local exception is allowed only under the inherited last-resort rule, with positive/negative evidence, native/version facts and a reassessment trigger. No new broad suppression or unchecked cast can replace source repair.

## Test Design

Adapt valuable existing tests at the public boundary; use isolated native adapter packages and existing factories/fixtures rather than a new harness. No durable test of code strings, checker version pins, legacy no-model behavior or implementation absence.

| Surface | Existing test owner / obligation |
| --- | --- |
| Core input | unit/decorators/test_pipeline_decorators.py, integration/test_prepared_tool_contract.py and interface tests: typed-empty success plus unknown-key rejection, supplied model identity, same prepared schema/admission and whole-schema rejection attachment, no core execution after rejection. Replace explicit None-route assertions; migrate RecordingCore/ordinary doubles. |
| Literals/persistence/Git | Existing atomic file writer, branch selection, check/edit/scaffold public tests preserve known reason/stage/cause/housekeeping/bytes and actual selected HEAD snapshot. |
| Adapter admission | Existing integration/adapters tests preserve malformed root, exact field/index/reason/order, prerequisite-before-execution, effective native config and mutation refusal. Source guards need no duplicate implementation-mirroring test when these cases already prove them. |
| Config/model/context/presentation/factories | Existing composition/loader/admission/immutable JSON, model defaults, cache serialization and public presentation cases preserve rejection/null/ordering/freshness/query/error contracts. |
| Logging | Extend unit/core/test_logging.py with a small behavior matrix: valid flat/null property, absent-versus-null/nonmapping root, invalid nested value/stringkeys/nonfinite/cycle, valid siblings, reserved collisions and true primary traceback. Use real stdlib makeRecord for a raw-extra bypass case; no private implementation assertion. Existing admin restart and process-cleanup tests prove emitted context, event_timestamp and unchanged marker/response/event/exit behavior. |
| Helpers/imports/precise exceptions | Run affected existing tests for fixture injection, private/public behavior, delayed CLI/recovery imports and invocation-time Settings patching; use observed ValidationError rather than broad exception snapshots. |

Temporary static positive/negative controls must enable the relevant restored diagnostics and explicitly avoid local/global masking. They verify typed logging producer rejection, model-only core input, narrow Literal consumers and preserved variance/library/runtime guards. Negative native exit1 is intentional sensitivity evidence, not a failed passing-gate claim. Do not add a permanent diagnostic suite or whole-test Mypy gate.

Source-declaration/library controls for retained covariance/AdapterRole/property/YAML exceptions use actual supported declarations with valid construction/serialization/schema and invalid cases where applicable; reuse unchanged exact-version evidence only when its source and dependency assumptions still hold. If changed evidence invalidates it, run only the affected controls, not a compatibility matrix.

## Contracts

### Model-only public Python contracts

The clean break changes Python input declarations/consumers, not the normal wire request/response. Signatures below state contracts only; they do not prescribe method bodies.

```python
# Existing interfaces/decorators/concrete implementations:
@property
def args_model(self) -> type[BaseModel]: ...

# Existing prepared contract; retain explicit covariance:
TInput_co = TypeVar("TInput_co", bound=BaseModel, covariant=True)

def validate(self, raw: JsonObject) -> TInput_co: ...

# Core execute already requires TInput bound to BaseModel.
# Existing no-argument inputs retain their empty extra=forbid models.
```

Update ICoreTool, ITool, PreparedToolInputContract/IToolInputContract, forwarding decorators, concrete optional-return annotations and direct test doubles/None calls together. Keep protocol variance and validation-before-execution/error attachments; no optional no-model admission or compatibility branch remains.

### Source-local raw container guards

```python
def _is_object_dict(value: object) -> TypeGuard[dict[object, object]]: ...
def _is_object_list(value: object) -> TypeGuard[list[object]]: ...
```

These stdlib-only positive guards describe existing checks; they do not certify schemas. Use only the container kind already admitted at that source. Validated lists and scratch values have precise return/element types after existing checks. Do not introduce a shared adapter framework or repeat tool-specific rules in generic execution code.

### Typed logging producer carrier

The existing logging module owns this one small static carrier. Its helper adds no logger/runtime/persistence service and cannot replace formatter admission.

```python
class LoggingExtra(TypedDict):
    props: Mapping[str, JsonValue]

def logging_extra(props: Mapping[str, JsonValue]) -> LoggingExtra: ...
```

Keep stdlib Logger and setup_logging/get_logger responsibilities unchanged. Static producer controls must reject None as the props root and non-JSON values; nullable property values remain valid. Raw Logger.extra is still admitted by StructuredFormatter. Runtime diagnosis/output follows the table above, without exposing arbitrary input/context.

### Literal attributes

FileCreationError stores its existing stage Literal["write_staging","create"] and reason Literal["permission_denied","io_error"]; OriginalReadError stores reason Literal["permission_denied","invalid_encoding","io_error"]; FileReplacementError stores stage Literal["write_staging","replace"] and the existing permission/io reasons. BranchBasisUnavailableError stores Literal["parent_unavailable","merge_base_unavailable"]. Constructor values and public consumer DTOs do not change.

## Flow

Raw transport JSON → existing wire/schema validation → typed model → existing enforcement/core → existing DTO/attachments → unchanged response projection. Raw adapter objects → existing source-local container/field validation → precisely typed native request/report. Logging producers → typed props carrier → real LogRecord → formatter-owned metadata and per-property standard admission → valid siblings + explicit safe issue/collision data → complete JSON log.

## State and Failures

No state format, workflow selection, persistence protocol or public operation outcome changes. Query methods stay pure. Input rejection retains existing schema/error attachments and skips core execution. Typed annotations/defaults cannot create success fallbacks. Adapter malformed/native/dependency failures stay distinct. Logging data problems do not substitute a different primary message/severity/traceback, recurse through another log call or serialize unsafe original values; a field that cannot be represented has a visible diagnostic. Base-message/handler/transport failures outside payload admission remain their existing native boundaries.

## Preservation

Preserve all supported normal request/response/schema/cache/profile behavior; only the approved None-input Python contract and logging malformed/collision handling change. Preserve existing branch production-only type selection, configured Mypy scope, native args and required full-suite timing. Keep runtime validators, original failure/cancellation/traceback facts, library nullable guards, immutable JSON rejection, fresh defaults, intentional variance and actual Git snapshot. No historical workaround is retained without its source/trigger, and no unchanged migration fix is duplicated.

## Transition and Cleanup

One clean cutover under the approved strategy: remove optional no-model contract branches and migrate direct consumers to typed models together. No dual APIs, aliases, legacy None tests or temporary production bridge. Remove obsolete directives, dead/private helper debt and broad test relaxations only with actual final combined-policy evidence. Keep independent packages independent and current Commitlint injection intact. Historical #513 artifacts remain evidence; the #518 final durable disposition records actual outcomes/rationales/triggers rather than retroactively editing those old measurements.

## Validation

### Approved strict policy actually observes wrong contracts

**Method:** Focused production checks plus small isolated positive/negative controls through run_checks; relevant signals unmasked, explicit native identities/codes. Actual combined-policy check after repair, not RUF100 under old test masking alone.

**Expected Result:** Correct cases pass; deliberately invalid model/Literal/logging/variance cases produce their intended diagnostics. No blanket disable, unchecked cast or guard deletion.

### Runtime contracts and truthful failures survive

**Method:** Narrow existing behavior tests per owner, including real adapter package and SDK/public surfaces. Meaningful RED for newly repaired behavior before implementation, not artificial RED for annotation-only cleanup.

**Expected Result:** Known valid/invalid inputs, field/index/native distinctions, bytes/causes/attachments/query purity and no repeated side effects remain correct.

### Malformed logging cannot replace the primary event

**Method:** Real LogRecord formatter behavior with positive/negative data and traceback; existing restart/process tests verify formatted output and unchanged marker/exit lifecycle.

**Expected Result:** Complete parseable JSON with original message/severity/logger/traceback, valid siblings and explicit safe issue/collision facts; event_timestamp/process context remain available.

### Final exception disposition is supported

**Method:** Review current actual directives/native policy; exact source removal/narrowing and necessary retained exceptions with rationale and trigger. Focused native unused-code checks after final policy.

**Expected Result:** No blind nineteen-removal, zero-quota claim or obsolete migration repair. Each actual residual group has a disposition; no newly hidden signal.

### Required final workspace evidence

**Method:** Planning specifies one full native configured suite and required branch/configured gates in Validation, preserving defaults/args and production-only type selection. Reuse fresh focused evidence until invalidated.

**Expected Result:** Complete native results, honest negatives/timeouts and independent phase QA; no testgate/coverage-policy expansion or forward waiver.

## Risks

### An annotation could silently widen admissible input or delete a runtime rejection.

Guard only actual objectcontainers, retain existing schema validation/invalid controls and exact error/order facts.

### Pydantic JSON admission might have an unverified cycle/nonfinite detail or a checker might reject a proposed factory view.

Prove the narrow positive/negative case during bounded implementation; use the existing supported source owner, never a new framework or blind cast. Stop if the approved contract cannot be preserved.

### Restored test ANN/ARG/explicit-target diagnostics can tempt broad test rewrites.

Correct the actual indexed helper/interface/fixture groups; keep existing production-only branch/configured type selection and classify diagnostic-only wider runs before execution.

## Planning Consequences

Group work by existing owner and dependencies; no source changes in Design. Each bounded implementation group needs its directly affected behavior/check evidence and meaningful RED only for behavior repair. Preserve explicit activation/restart/fresh-context verification for tool-facing core changes before live claims. Validation owns full native suite and branch/configured gates; no new coverage threshold/test-Mypy gate. Final documentation updates current checker/input/logging contracts and the durable exact disposition without expanding instruction files. Independent QA governs all phase boundaries; owner is consulted only for an actual strategy/policy contradiction.

## Sources

- [Approved Research](<research.md>)
- [Inherited disposition and source controls](<../issue513/suppression-inventory.md>)
- [Core input](<../../../mcp_server/core/interfaces/icore_tool.py>)
- [Prepared input](<../../../mcp_server/core/interfaces/tool_input_contract.py>)
- [Input decorator](<../../../mcp_server/core/decorators/input_validation_decorator.py>)
- [Logging owner](<../../../mcp_server/core/logging.py>)
- [Existing finite JSON authority](<../../../mcp_server/core/interfaces/template_catalog.py>)
- [Native policy](<../../../pyproject.toml>)
- [Production branch selection](<../../../mcp_server/execution/check_selection.py>)
- [Type checker selection](<../../../mcp_server/bundled_adapters/pyright/manifest.yaml>)
- [Architecture](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Test/gate evidence scope](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp designer | Define model-only interfaces, source-local narrowing, minimal typed logging/payload diagnosis, final native policy and preservation evidence under the approved #513 strategy. |
