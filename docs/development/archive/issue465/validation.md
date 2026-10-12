<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 465 — artifact-family validation

**Status:** Validation complete — independent review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-11

## Purpose

Provide durable, source-bound evidence for the YAML, JSON Schema, ADR and SAD contracts.

## Scope In

Approved #465/#484/#498 package, shared rendering/reader, native-check and public mutation changes, including two bounded QA-reviewed repair rounds.

## Scope Out

Compatibility bridges, unrestricted JSON generation, automatic ADR lifecycle/synchronization, static template-compliance analysis and instruction rollout.

## Prerequisites

- Research Approved Strategy and Design/Planning remain binding.
- Independent QA reviewed implementation and each bounded return; this report records producer observations, not QA approval.

## Issue Number

#465

## Cycle

C_1–C_3

## Validation Status

PASS

## Obligations

### C\_1 D\_1.1/D\_1.2: pure YAML serialization, shared framing and bounded identity recognition.

**Evidence:**

- [Shared behavior tests](<../../../../tests/mcp_server/unit/services/test_template_engine.py>)
- [Reader behavior tests](<../../../../tests/mcp_server/unit/services/test_artifact_header_reader.py>)

**Outcome:** Native parser round trips preserve supported JSON value types, strings and multiline/control characters; bounded comment/first-root-$comment recognition preserves existing public value contract. Focused C1: 143 passed.

### C\_2 D\_2.1/D\_2.2: native checker adapter, pinned prerequisite admission, three checks/two profiles and branch filters.

**Evidence:**

- [Adapter native behavior](<../../../../tests/mcp_server/integration/adapters/test_check_jsonschema.py>)
- [Configured checks](<../../../../.pgmcp/config/checks.yaml>)

**Outcome:** 28 native adapter cases cover actual positives/negatives, dependency admission, strict wire input, unsupported operations, native inability and original-file isolation. Later adapter+rollout repair: 37 passed.

### C\_3 D\_3.1: \#465 YAML and \#484 JSON Schema packages, roots, consumer behavior and suite-only extension.

**Evidence:**

- [Data family behavior](<../../../../tests/mcp_server/integration/templates/test_data_artifacts.py>)

**Outcome:** 11 cases inspect parsed output, actual TemplateContractLoader consumer, representative schema instances, suite-only custom package and native-valid/consumer-unsupported $id distinction.

### C\_3 D\_3.2: \#498 architecture records on existing Markdown tiers, nested input consumption and component attribution.

**Evidence:**

- [Architecture behavior](<../../../../tests/mcp_server/integration/templates/test_architecture_records.py>)
- [Distributed SAD source/license](<../../../../.pgmcp/template_suite/sad/template.jinja2>)

**Outcome:** 12 cases cover proportional drafts, populated parent/nested fields, schema refusals, reader recognition and real Lychee relative/fragment acceptance and refusal. Exact pinned arc42 license/attribution remains in owning Jinja source, rendered attribution before terminal history.

### C\_3 D\_3.3: public scaffold/edit selection, validation policies and isolated proposed content.

**Evidence:**

- [Public mutation behavior](<../../../../tests/mcp_server/integration/test_data_artifact_mutations.py>)

**Outcome:** 8 native cases cover two-family create/edit, failed enforce preserving disk, report persistence with failed findings, original identity routing without suffix support, scratch cleanup and neighbor preservation.

### Release claim covers assembled and installed assets, not source presence alone.

**Evidence:**

- [Installed distribution proof](<../../../../tests/mcp_server/integration/test_installed_distribution_v3.py>)
- [Offline build fixture](<../../../../tests/mcp_server/fixtures/installed_distribution.py>)

**Outcome:** Full-suite installed-distribution test builds a fresh offline wheel, compares every admitted template/config/adapter source byte-for-byte with wheel and installed prefix, then loads installed catalogs outside the checkout. This includes all four packages, shared tiers, two check schemas, adapter requirements and embedded license.

## Evidence

### Full native-configured suite at final source snapshot.

Native pytest 9.0.2, Python 3.13.7, eight xdist workers; pyproject native arguments retained; no added exclusions or coverage flags.

**Sources:**

- [Native pytest configuration](<../../../../pyproject.toml>)

**Invocation:** run_tests(scope='configured', timeout_seconds=1800)

**Observed Result:** Source snapshot d84811c46771de29c6b22eaec7875264a5dbd556: 2923 passed, 1 skipped, 1 xpassed, 269 warnings in 306.13s (0:05:06) =====; native exit 0. Supplemental receipt 23b75a9c2ba24f4ba1aa3ec260f5245c.

### Branch and workspace checks use admitted file families.

Branch selection applies existing per-capability policies; Python gates receive only Python targets. Files-required YAML/schema checks are not invoked on an empty configured selection.

**Sources:**

- [Checks and selectors](<../../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','markdown_links','yaml_configuration','json_schema_shape','json_schema_metaschema'], timeout_seconds=900); run_checks(scope='configured', profile='python_review', timeout_seconds=900)

**Observed Result:** All seven final branch checks passed (45878ccb465a4389bb0f53e85a12329d) on d84811c4; all four configured Python checks passed (4709e09265a4469c9f517ef7089eb0c9) on 681813a1. Only SAD Jinja whitespace and the already checked architecture test changed afterward; production-scoped configured evidence remains valid.

### Bounded failure repair retains acceptance criteria.

Initial full run: 2921 passed,1 skipped,1 xpassed,269 warnings,3 stale fixture errors (306.75s). Configured Mypy found two local assignment inference errors. QA approved return to C3; 681813a1 fixes types and uses real catalog admission/current authored locations, removing fixed package count and copied inventory while retaining coherence/unknown-ID/atomic/drift checks. Full rerun then passed 2923 tests (309.87s). Live SAD rendering later found a leading newline hiding provenance. QA approved package-only whitespace repair; definitive RED b5d9630c had 1 failed/11 passed, GREEN d84811c4 all12 passed.

**Sources:**

- [Rollout behavior](<../../../../tests/mcp_server/integration/test_rollout_configuration.py>)
- [SAD render/reader behavior](<../../../../tests/mcp_server/integration/templates/test_architecture_records.py>)

**Observed Result:** No suppressions, skipped failures, generic reader changes, new test modules or compatibility paths were introduced.

## Demonstration

On the live healthy server, scaffold all four IDs under .pgmcp/temp/artifacts/issue465 with validation='enforce'. YAML settings.yaml context includes data={enabled:false,retries:0,label:'yes',nested:{threshold:1.5,tags:['a','b']},message:'first line\nsecond line\n'}; emitted types/strings remain authored. JSON settings.schema.json uses Draft 2020-12, object/properties.enabled.boolean/required/envelope and runs both shape/metaschema checks. ADR decision.md uses caller-owned ADR-465-demo/status=proposed and a link to architecture.md#5-building-block-view. SAD provides all twelve required carriers, explicit proposed perspective and authored metadata; after both files exist insert its decision.md#decision link. Real Lychee validates the pair. Malformed YAML proposal and JSON type=7 proposals are blocked with written=false; original bytes stay unchanged. Corrected SAD scaffold architecture-final.md and subsequent index edit report selected_source='metadata', written=true, validation_status='passed'; native Lychee passes. Live receipt 3e3f7b517a97430993130d8e904d47bd is supplemental. Readback confirmed unchanged YAML enabled=false and JSON type='object' after blocked proposals. Durable minimal/populated context and invocation reproductions are in linked data/architecture/mutation tests; temporary outputs are excluded from the committed branch.

## Preservation

Ordinary YAML mappings preserve supported types and authored values through PyYAML 6.0.3. JSON Schema serialization preserves caller members except the reserved root provenance carrier. Existing Markdown metadata/history and package ownership remain. Public tool DTOs and generic execution architecture are unchanged.

## Containment

Permanent behavioral coverage remains within the four planned new modules; existing tests/helpers are adapted. Tests use isolated temporary workspaces, not live state/deliverables. Live examples occupy the ignored configured scratch root. Adapter uses actual native check-jsonschema 0.38.2, orjson 3.13.0, ruamel.yaml 0.18.16 and jsonschema 4.25.1 from the actual selected interpreter; package requirements own these pins.

## Failures

- Initial Validation failures and live SAD defect were repaired through explicit independent QA returns; final unresolved failures: none.

## Caveats

- Native YAML acceptance proves parsing and an object root, not application-specific keys or semantics.
- JSON Schema checks prove the explicit Draft 2020-12 envelope and native metaschema validity, not support by every consumer; actual TemplateContractLoader still rejects unsupported $id.
- Empty required ADR/SAD carriers admit drafts. Native link checks do not certify meaningful architecture, status correctness or template structural conformance.
- Full suite retains one skip, one XPASS and existing warning categories; these are reported, not silently converted or repaired outside scope.
- Run IDs are supplemental connection-local receipts, not durable evidence. Reproduce exact invocations from source-bound tests and this report after cache expiry.

## Risks

### Native prerequisite or installed suite changes can invalidate the source-bound claim.

Keep exact adapter prerequisites, rediscover context schemas after updates and resolve the suite via a healthy restart; follow the existing package development/release procedure.

## Deferred Work

## Related Documents

- [Approved Design](<design.md>)
- [Planning](<planning.md>)
- [Approved Research](<research.md>)
- [Package development and release procedure](<../../schema-template-maintenance.md#develop-and-release-a-package>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-11 | @imp validator | Record scoped implementation, full native verification, live routes and bounded repair evidence. |
