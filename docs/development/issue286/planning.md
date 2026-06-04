<!-- docs\development\issue286\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-04T20:41Z updated= -->
# Issue #286: Implementation Plan — Template/Scaffolding Pipeline Gaps and Documentation Alignment

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-04

---

## Purpose

Translate the approved design into sequenced, implementation-sized TDD cycles with explicit deliverables, exit criteria, and test obligations for each gap.

## Scope

**In Scope:**
Documentation cluster revision (6 docs + README.md); MethodSpec value object; GenericContext fix; adapter/resource/interface full pipeline + legacy removal; validation_report full pipeline; generic_doc Layer 1+2 completion.

**Out of Scope:**
Issue #326 (V1 pipeline removal and PYDANTIC_SCAFFOLDING_ENABLED flag); issue #349 (source-code-free template contribution); artifact types not addressed in design; changes to existing templates other than those listed in the design.

## Prerequisites

Read these first:
1. docs/development/issue286/research.md — approved research artifact
2. docs/development/issue286/design.md — approved design artifact (v1.1)
3. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
4. docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md
---

## Summary

Five sequential TDD cycles to fix all six pipeline gaps identified in design: documentation cluster revision first (Approved Strategy), then MethodSpec introduction, three new code artifact types, validation-report type, and generic_doc Layer 1/2 completion.

---

## Dependencies

- C_286.1 must complete before C_286.2 (Approved Strategy: docs-first alignment is a prerequisite boundary)
- C_286.2 must complete before C_286.3 (MethodSpec is a shared value object used by AdapterContext, ResourceContext, InterfaceContext)
- C_286.3, C_286.4, C_286.5 are independent of each other; ordered by complexity

---

## TDD Cycles


### Cycle 1: C_286.1 — Documentation cluster revision

**Goal:** Revise all six reference documents and create docs/reference/mcp/README.md so the documentation cluster accurately describes the three-layer scaffolding architecture, is free of legacy content, and is actionable for future template editors.

**Tests:**
- No test changes in this cycle — documentation does not have automated tests
- Full test suite must remain green after all document edits (regression check)

**Success Criteria:**
- docs/architecture/TEMPLATE_LIBRARY.md: three-layer model is the primary architecture frame; no legacy paths or branding
- docs/reference/mcp/tools/scaffolding.md: legacy error paths removed; current architecture described; context schema referenced
- docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md: full rewrite with current paths; three-layer model usage guidance present
- docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md: full rewrite; artifact inventory updated to include all enabled types
- docs/reference/mcp/template_metadata_format.md: full rewrite; TEMPLATE_METADATA explicitly linked to Layer 3; Layer 1 cross-reference present
- docs/reference/mcp/validation_api.md: full rewrite; no S1mpleTraderV3 or .st3/ references
- docs/reference/mcp/README.md: created; navigates all six cluster documents with one-line descriptions
- No .st3/, S1mpleTraderV3, V1, V2, or legacy path strings appear in any touched document
- A reviewer can answer 'what do I create to add a new artifact type?' from the docs cluster alone
- pylint 10/10, mypy pass, full test suite green



### Cycle 2: C_286.2 — MethodSpec value object + GenericContext fix

**Goal:** Introduce the MethodSpec frozen Pydantic value object and fix GenericContext.methods from list[str] to list[MethodSpec], making Layer 1 and Layer 3 consistent for the generic artifact type.

**Tests:**
- RED: write failing unit tests for MethodSpec (frozen, name required, optional fields with defaults, extra fields forbidden)
- RED: confirm existing TestGenericContext.test_generic_context_all_optional_populated fails because methods=[string] is now rejected
- GREEN: implement MethodSpec in mcp_server/schemas/contexts/method_spec.py; update GenericContext.methods field; export from schemas/__init__.py
- GREEN: update TestGenericContext tests to supply list[MethodSpec] inputs instead of list[str]
- GREEN: update test_code_artifact_v2_parity.py — remove stale comment about 'list[str]' / 'Cycle 6 scope'; update _FULL dict to include methods as list[MethodSpec] or remove the omission note
- GREEN: update TestGenericContextParity in test_code_artifact_parity.py if parity checks fail due to field type change
- REFACTOR: verify full test suite green; run quality gates

**Success Criteria:**
- mcp_server/schemas/contexts/method_spec.py exists with MethodSpec frozen Pydantic model: name required, params/return_type/docstring/body optional with defaults, extra=forbid
- GenericContext.methods: list[MethodSpec] with default []
- MethodSpec exported from mcp_server/schemas/__init__.py
- Minimal usage: GenericContext(name='X', methods=[{'name': 'calculate'}]) validates without error
- Rich usage: all MethodSpec fields populated validates without error
- list[str] input for methods is now rejected by Pydantic validation
- All unit tests in test_code_artifact_schemas.py TestGenericContext pass
- test_code_artifact_parity.py TestGenericContextParity passes
- test_code_artifact_v2_parity.py stale comment removed; _FULL dict updated
- pylint 10/10, mypy pass, full test suite green

**Dependencies:** C_286.1 must be complete


### Cycle 3: C_286.3 — adapter/resource/interface full pipeline + legacy scaffolder removal

**Goal:** Create complete three-layer pipeline support for adapter, resource, and interface artifact types; enable them in the registry and config; delete the three orphaned legacy scaffolders.

**Tests:**
- RED: write failing unit tests for AdapterContext, ResourceContext, InterfaceContext (name required, optional fields, methods as list[MethodSpec])
- RED: write failing integration smoke test entries for adapter, resource, interface in test_v2_smoke_all_types.py
- RED: uncomment the three disabled lines in test_artifacts_type_field_cycle1.py for adapter/resource/interface
- GREEN: create mcp_server/schemas/contexts/adapter.py, resource.py, interface.py
- GREEN: create mcp_server/schemas/render_contexts/adapter.py, resource.py, interface.py
- GREEN: create mcp_server/scaffolding/templates/concrete/adapter.py.jinja2, resource.py.jinja2, interface.py.jinja2 (each with TEMPLATE_METADATA block)
- GREEN: add 6 exports to mcp_server/schemas/__init__.py
- GREEN: add 3 entries to _v2_context_registry in artifact_manager.py
- GREEN: enable adapter/resource/interface in .phase-gate/config/artifacts.yaml; remove commented-out scaffolder_class lines
- GREEN: delete mcp_server/scaffolding/components/adapter.py, resource.py, interface.py
- REFACTOR: verify full test suite green; run quality gates

**Success Criteria:**
- scaffold_artifact('adapter', {'name': 'MyAdapter'}) succeeds end-to-end
- scaffold_artifact('resource', {'name': 'MyResource'}) succeeds end-to-end
- scaffold_artifact('interface', {'name': 'IMyInterface'}) succeeds end-to-end
- All three types accept methods: list[MethodSpec] as optional field
- Components/adapter.py, components/resource.py, components/interface.py are deleted
- test_artifacts_type_field_cycle1.py: adapter/resource/interface lines are active (not commented) and test passes
- test_v2_smoke_all_types.py: smoke test covers 19 types (16 + 3 new)
- No import of AdapterScaffolder/ResourceScaffolder/InterfaceScaffolder anywhere in production code
- pylint 10/10, mypy pass, full test suite green

**Dependencies:** C_286.2 must be complete (MethodSpec must exist before Context schemas import it)


### Cycle 4: C_286.4 — validation_report full pipeline

**Goal:** Create complete three-layer pipeline support for the validation_report artifact type and enable it in the registry and config.

**Tests:**
- RED: write failing unit tests for ValidationReportContext (title required, optional fields: issue_number, cycle, phase, status, scope)
- RED: write failing integration smoke test entry for validation_report in test_v2_smoke_all_types.py
- GREEN: create mcp_server/schemas/contexts/validation_report.py
- GREEN: create mcp_server/schemas/render_contexts/validation_report.py
- GREEN: create mcp_server/scaffolding/templates/concrete/validation_report.md.jinja2 (with TEMPLATE_METADATA block)
- GREEN: add 2 exports to mcp_server/schemas/__init__.py
- GREEN: add 1 entry to _v2_context_registry: 'validation_report': 'ValidationReportContext'
- GREEN: enable validation_report in .phase-gate/config/artifacts.yaml
- REFACTOR: verify full test suite green; run quality gates

**Success Criteria:**
- scaffold_artifact('validation_report', {'title': 'Cycle 1 Validation'}) succeeds end-to-end
- ValidationReportContext uses underscore key 'validation_report' consistent with registry and config
- test_v2_smoke_all_types.py: smoke test covers 20 types (19 + 1)
- pylint 10/10, mypy pass, full test suite green

**Dependencies:** C_286.1 must be complete; C_286.3 is independent (can run in either order)


### Cycle 5: C_286.5 — generic_doc Layer 1 and Layer 2 completion

**Goal:** Create GenericDocContext (Layer 1) and GenericDocRenderContext (Layer 2) for generic_doc; add registry entry; rewrite the test that currently asserts generic_doc is V1-only.

**Tests:**
- RED: write failing unit tests for GenericDocContext (title required, all other fields optional)
- RED: update test_returns_error_for_v1_type in test_scaffold_schema_tool.py to assert generic_doc now returns a valid schema (not a ConfigError) — this test currently passes; the rewrite makes it RED against the new expected behavior
- RED: add generic_doc smoke entry to test_v2_smoke_all_types.py with {'title': 'My Doc'}
- GREEN: create mcp_server/schemas/contexts/generic_doc.py with GenericDocContext
- GREEN: create mcp_server/schemas/render_contexts/generic_doc.py with GenericDocRenderContext
- GREEN: add 2 exports to mcp_server/schemas/__init__.py
- GREEN: add 1 entry to _v2_context_registry: 'generic_doc': 'GenericDocContext'
- GREEN: rewrite test_returns_error_for_v1_type to assert generic_doc returns valid schema
- GREEN: update test_v2_smoke_all_types.py docstring from '16' to '21 artifact types'
- REFACTOR: verify full test suite green; run quality gates

**Success Criteria:**
- scaffold_artifact('generic_doc', {'title': 'My Guide'}) succeeds end-to-end via V2 pipeline
- GenericDocContext: title is required; all other fields (purpose, summary, status, version, scope_in, scope_out, prerequisites, related_docs, key_changes, migration_steps, validation_checklist, faq, custom_sections) are optional
- test_scaffold_schema_tool.py test_returns_error_for_v1_type is rewritten: generic_doc now returns valid schema
- test_generic_doc_template.py still passes (Layer 3 template unchanged; Jinja2 direct test unaffected)
- test_v2_smoke_all_types.py: smoke test covers 21 types (20 + 1); docstring updated
- _v2_context_registry has 21 entries total
- No V1-only types remain in the active registry after this cycle
- pylint 10/10, mypy pass, full test suite green

**Dependencies:** C_286.1 must be complete; C_286.3 and C_286.4 are independent

---

## Risks & Mitigation

- **Risk:** test_code_artifact_parity.py TestGenericContextParity may fail in unexpected ways when methods field type changes from list[str] to list[MethodSpec] — the parity test introspects schema field types and compares them to template variable contracts
  - **Mitigation:** Run failing test in C_286.2 RED phase first; examine exact failure before patching; the fix should be to update the expected field-type contract in the parity test to match the new MethodSpec type
- **Risk:** adapter/resource/interface concrete templates do not exist yet — implementation must create syntactically valid Jinja2 templates consistent with the Layer 3 TEMPLATE_METADATA contract before the smoke test can go GREEN
  - **Mitigation:** Model new templates on existing patterns (tool.py.jinja2, worker.py.jinja2); include TEMPLATE_METADATA block; verify render passes with minimal context dict before proceeding to REFACTOR
- **Risk:** artifacts.yaml disabled entries for adapter/resource/interface have commented-out scaffolder_class lines — enabling them requires removing those comments cleanly without introducing config parse errors
  - **Mitigation:** Read current artifacts.yaml entries before editing; verify config loads without error in GREEN phase

---

## Milestones

- After C_286.1: full test suite green; documentation cluster fully revised and clean
- After C_286.2: MethodSpec exists; GenericContext.methods is list[MethodSpec]; all schema unit tests pass
- After C_286.3: adapter/resource/interface scaffoldable end-to-end; legacy scaffolders deleted; smoke test covers 19 types
- After C_286.4: validation_report scaffoldable end-to-end; smoke test covers 20 types
- After C_286.5: generic_doc scaffoldable end-to-end via V2 pipeline; smoke test covers 21 types; _v2_context_registry has 21 entries; no V1-only types remain

## Related Documentation
- **[docs/development/issue286/research.md][related-1]**
- **[docs/development/issue286/design.md][related-2]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-3]**
- **[docs/architecture/TEMPLATE_LIBRARY.md][related-4]**
- **[docs/reference/mcp/tools/scaffolding.md][related-5]**

<!-- Link definitions -->

[related-1]: docs/development/issue286/research.md
[related-2]: docs/development/issue286/design.md
[related-3]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-4]: docs/architecture/TEMPLATE_LIBRARY.md
[related-5]: docs/reference/mcp/tools/scaffolding.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |