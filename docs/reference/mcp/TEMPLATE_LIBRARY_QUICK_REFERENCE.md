<!-- docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md -->
<!-- template=reference version=064954ea created=2026-02-07T00:00Z updated=2026-06-05 -->
# Template Library Quick Reference

**Status:** DEFINITIVE
**Version:** 2.1
**Last Updated:** 2026-06-05

**Source:** [mcp_server/scaffolding/templates/][source]
**Tests:** [tests/mcp_server/integration/test_smoke_all_types.py][tests]

---

## Purpose

Quick-lookup inventory of all registered artifact types, their required context fields, and their template locations. For full usage guidance see docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md.

---

## Artifact Type Inventory

Use `scaffold_schema(artifact_type="<type>")` to get the full JSON Schema for any type's context.

Registry: `.pgmcp/config/artifacts.yaml`

### Code Artifacts

| Type | Minimum required context | Template |
|---|---|---|
| `dto` | `dto_name: str`, `fields: list[str]` | `concrete/dto.py.jinja2` |
| `worker` | `name: str`, `layer: str` | `concrete/worker.py.jinja2` |
| `adapter` | `name: str` | `concrete/adapter.py.jinja2` |
| `tool` | `name: str` | `concrete/tool.py.jinja2` |
| `resource` | `name: str` | `concrete/resource.py.jinja2` |
| `schema` | `name: str` | `concrete/config_schema.py.jinja2` |
| `interface` | `name: str` | `concrete/interface.py.jinja2` |
| `service` | `name: str` | `concrete/service_command.py.jinja2` |
| `generic` | `name: str` | `concrete/generic.py.jinja2` |
| `unit_test` | `module_under_test: str`, `test_class_name: str` | `concrete/test_unit.py.jinja2` |
| `integration_test` | `test_scenario: str`, `test_class_name: str` | `concrete/test_integration.py.jinja2` |

### Document Artifacts

| Type | Minimum required context | Template |
|---|---|---|
| `research` | `title: str`, `problem_statement: str`, `goals: list[str]` | `concrete/research.md.jinja2` |
| `planning` | `title: str`, `summary: str`, `cycles: list` | `concrete/planning.md.jinja2` |
| `design` | `title: str`, `status: str`, `version: str`, `problem_statement: str`, `requirements_functional: list[str]`, `requirements_nonfunctional: list[str]`, `decision: str`, `rationale: str` | `concrete/design.md.jinja2` |
| `architecture` | `title: str`, `concepts: list[str]` | `concrete/architecture.md.jinja2` |
| `reference` | `title: str` | `concrete/reference.md.jinja2` |
| `validation_report` | `title: str`, `status: str`, `version: str`, `last_updated: str` | `concrete/validation_report.md.jinja2` |
| `generic_doc` | `title: str`, `status: str`, `version: str`, `last_updated: str`, `purpose: str`, `summary: str` | `concrete/generic.md.jinja2` |

### Tracking Artifacts

| Type | Minimum required context | Template |
|---|---|---|
| `commit` | `workflow_phase: str`, `message: str` | `concrete/commit.txt.jinja2` |
| `pr` | `title: str` | `concrete/pr.md.jinja2` |
| `issue` | `title: str` | `concrete/issue.md.jinja2` |

> **Note:** "Minimum required context" shows fields that Pydantic will reject if missing. All other fields are optional with sensible defaults. Always run `scaffold_schema` for the full field list.

---

## Template Location Reference

Templates root: `mcp_server/scaffolding/templates/`

| Tier | Purpose | Examples |
|---|---|---|
| 0 | Universal SCAFFOLD header | `tier0_base_artifact.jinja2` |
| 1 | Format structure | `tier1_base_code.jinja2`, `tier1_base_document.jinja2` |
| 2 | Language/syntax | `tier2_base_python.jinja2`, `tier2_base_markdown.jinja2` |
| 3 | Pattern macros | `tier3_pattern_python_logging.jinja2`, `tier3_pattern_markdown_status_header.jinja2` |
| Concrete | Artifact outputs | `concrete/dto.py.jinja2`, `concrete/design.md.jinja2` |

---

## Element Flow (Code vs Document)

### Code artifacts

| Element | Tier responsibility |
|---|---|
| SCAFFOLD provenance header | Tier 0 |
| Module docstring + class skeleton | Tier 1 |
| Python language syntax | Tier 2 |
| Optional patterns (logging, DI, async, error, ...) | Tier 3 (`{% import %}`) |
| Artifact-specific behavior | Concrete |

### Document artifacts

| Element | Tier responsibility |
|---|---|
| SCAFFOLD provenance header | Tier 0 |
| Purpose/Scope/Related Documentation structure | Tier 1 |
| Markdown link definitions and code-block syntax | Tier 2 |
| Optional patterns (status header, version history, ...) | Tier 3 (`{% import %}`) |
| Doc-specific sections | Concrete |

---

## Enforcement Levels

| Level | Where used | Behavior |
|---|---|---|
| STRICT | Tiers 0–2 (base templates) | Violations are errors — blocks generation or validation |
| ARCHITECTURAL | Tier 3 patterns + code concretes | Strict rules are errors; guidelines are warnings |
| GUIDELINE | Most concrete templates | All violations are warnings only |

---

## Related Documentation
- **[docs/reference/mcp/README.md][related-1]**
- **[docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md][related-2]**
- **[docs/architecture/TEMPLATE_LIBRARY.md][related-3]**
- **[docs/reference/mcp/template_metadata_format.md][related-4]**

<!-- Link definitions -->
[source]: ../../mcp_server/scaffolding/templates/
[tests]: ../../tests/mcp_server/integration/test_smoke_all_types.py
[related-1]: README.md
[related-2]: TEMPLATE_LIBRARY_USAGE.md
[related-3]: ../../docs/architecture/TEMPLATE_LIBRARY.md
[related-4]: template_metadata_format.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.1 | 2026-06-05 | Agent | Reconciled artifact inventory with validated branch state: added adapter/resource/interface and validation_report; generic_doc minimum context updated to current schema-validated contract |
| 2.0 | 2026-06-04 | Agent | Full rewrite: artifact inventory updated to all 17 registered types; correct template paths; three-layer model integrated; removed legacy paths and branding (#286) |
| 1.0 | 2026-02-07 | Agent | Initial draft |
