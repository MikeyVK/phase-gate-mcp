<!-- docs/development/issue286/research.md -->
<!-- template=research version=43c84181 created=2026-06-04T16:40:00Z updated=2026-06-04 -->
# Issue #286 Research

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-04

---

## Purpose

Investigate the V2 template/scaffolding gaps in issue #286 with code as the source of truth, and determine the correct sequencing for documentation alignment versus implementation work.

## Scope

**In Scope:**
Generic schema-template mismatch, missing V2 support for adapter/resource/interface, validation-report artifact gap, template/scaffolding reference documentation alignment under `docs/reference/mcp/`, and removal of obsolete V1 or legacy branding references from the touched documentation set.

**Out of Scope:**
Implementation patch details, exact cycle breakdown, the broader Template Workspace Initiative in issue #349, and unrelated MCP reference cleanup outside the template/scaffolding documentation cluster.

## Prerequisites

Read these first:
1. `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`
2. `docs/coding_standards/DOCUMENTATION_STANDARD.md`

---

## Problem Statement

The V2 scaffolding pipeline and its reference documentation are out of sync at multiple boundaries:
- the generic artifact schema disagrees with its concrete template
- several artifact types still rely on legacy-only paths instead of first-class V2 support
- validation-report scaffolding is absent as a registered artifact
- the template/scaffolding reference docs still describe obsolete paths, legacy fallback behavior, and outdated product branding

This creates two linked risks:
1. the code path is harder to evolve safely because the documentation no longer reflects the actual V2 architecture
2. later template work for issue #286 and related follow-up issues such as issue #349 would start from a drifting reference baseline instead of an accurate one

## Research Goals

- Confirm the concrete code-level contract mismatch for the generic artifact path
- Identify the current V2-versus-legacy boundaries for adapter, resource, interface, and validation-report scaffolding
- Map the affected production surfaces, tests, helpers, and fixtures for issue #286
- Assess the template/scaffolding reference documentation set under `docs/reference/mcp/` for code drift, navigation gaps, and obsolete branding
- Establish the sequencing strategy for this issue so code-led reference documentation alignment happens before template-gap implementation work

## Background

Issue #286 combines three template-library gaps that all sit on the same architectural seam: the project has a V2 scaffolding pipeline, but some artifact types, tests, and reference docs still reflect older assumptions.

The user-directed research policy for this branch is explicit:
- no external research
- code is the authoritative source of truth
- reference documentation for templates and scaffolding must first be aligned to the V2 implementation and must not describe V1 behavior as the normative path
- the touched documentation set must not contain `S1mpleTraderV3` or `st3`-style branding references
- once the V2 architecture is documented accurately, implementation can proceed on the missing or broken template paths in issue #286

This makes documentation alignment a prerequisite for the rest of the issue rather than optional cleanup.

## Findings

### 1. Generic artifact path has a real schema-template contract break

The strongest confirmed bug is the generic artifact mismatch.

| Surface | Evidence |
|---|---|
| V2 schema | [mcp_server/schemas/contexts/generic.py](mcp_server/schemas/contexts/generic.py) defines `methods: list[str]` |
| Concrete template | [mcp_server/scaffolding/templates/concrete/generic.py.jinja2](mcp_server/scaffolding/templates/concrete/generic.py.jinja2) renders each method as an object with `method.name`, `method.params`, `method.return_type`, `method.docstring`, and `method.body` |
| Effect | Non-empty `methods` input is structurally incompatible with the declared V2 schema |

This is not a documentation-only problem. It is a hard contract mismatch between the declared V2 context model and the concrete Jinja2 consumer.

### 2. V2 support is incomplete for adapter, resource, and interface

The current registry and manager wiring show that V2 support is not complete for three artifact types.

| Artifact type | Current state | Evidence |
|---|---|---|
| `adapter` | Disabled in registry, no V2 context class in active registry map | [.phase-gate/config/artifacts.yaml](.phase-gate/config/artifacts.yaml), [artifact_manager.py](mcp_server/managers/artifact_manager.py) |
| `resource` | Disabled in registry, no V2 context class in active registry map | [.phase-gate/config/artifacts.yaml](.phase-gate/config/artifacts.yaml), [artifact_manager.py](mcp_server/managers/artifact_manager.py) |
| `interface` | Disabled in registry, no V2 context class in active registry map | [.phase-gate/config/artifacts.yaml](.phase-gate/config/artifacts.yaml), [artifact_manager.py](mcp_server/managers/artifact_manager.py) |

Legacy scaffolders still exist for these paths:
- [mcp_server/scaffolding/components/adapter.py](mcp_server/scaffolding/components/adapter.py)
- [mcp_server/scaffolding/components/resource.py](mcp_server/scaffolding/components/resource.py)
- [mcp_server/scaffolding/components/interface.py](mcp_server/scaffolding/components/interface.py)

That confirms the boundary clearly: the codebase is V2-led, but these types are not yet first-class V2 artifacts.

### 3. Validation-report is not currently a first-class registered artifact

No evidence was found that `validation-report` or `validation_report` is registered as an artifact type in the active artifact registry or the active scaffolding code path.

That matters because issue #286 explicitly carries the gap as part of the consolidated template-library work, and because validation documentation is a recurring governed artifact in the workflow system.

### 4. The reference documentation cluster is fragmented and partially stale

The reference documentation relevant to templates/scaffolding is spread across multiple files and does not currently have a single top-level navigation surface under `docs/reference/mcp/`.

#### Core affected documentation set

| File | Current role |
|---|---|
| [docs/reference/mcp/tools/scaffolding.md](docs/reference/mcp/tools/scaffolding.md) | Main tool reference for `scaffold_artifact` and `scaffold_schema` |
| [docs/architecture/TEMPLATE_LIBRARY.md](docs/architecture/TEMPLATE_LIBRARY.md) | Architecture rationale for the tiered template library |
| [docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md](docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md) | Usage guidance for template library and artifact registry |
| [docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md](docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md) | Quick inventory and tier overview |
| [docs/reference/mcp/template_metadata_format.md](docs/reference/mcp/template_metadata_format.md) | TEMPLATE_METADATA reference |
| [docs/reference/mcp/validation_api.md](docs/reference/mcp/validation_api.md) | Template validation API reference |

#### Navigation gap

There is a tools index at [docs/reference/mcp/tools/README.md](docs/reference/mcp/tools/README.md), but there is no top-level `docs/reference/mcp/README.md` that groups:
- template library architecture
- template metadata format
- validation API
- scaffolding tool reference
- template library quick reference and usage guidance

As a result, the template/scaffolding reference set is not cleanly discoverable as one coherent documentation cluster.

### 5. The touched reference docs contain code drift and legacy terminology

The requested documentation set contains both architectural drift and branding drift.

#### Code drift examples

| File | Drift evidence |
|---|---|
| [docs/reference/mcp/tools/scaffolding.md](docs/reference/mcp/tools/scaffolding.md) | Still documents `generic_doc` as a V1-only schema-discovery error path and still describes templates under `mcp_server/templates/` rather than the current scaffolding template root |
| [docs/reference/mcp/validation_api.md](docs/reference/mcp/validation_api.md) | Uses outdated example paths such as `mcp_server/templates/components/...` |
| [docs/reference/mcp/template_metadata_format.md](docs/reference/mcp/template_metadata_format.md) | Uses outdated template locations such as `mcp_server/templates/components/...` |
| [docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md](docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md) | References `.st3/config/artifacts.yaml` and `.st3/template_registry.json`, which no longer match the active repository layout |
| [docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md](docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md) | References `.st3/template_registry.json` as registry provenance location |

#### Branding and naming drift examples

| File | Drift evidence |
|---|---|
| [docs/reference/mcp/validation_api.md](docs/reference/mcp/validation_api.md) | Title includes `S1mpleTraderV3` |
| [docs/reference/mcp/template_metadata_format.md](docs/reference/mcp/template_metadata_format.md) | Title includes `S1mpleTraderV3` |
| [docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md](docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md) | Title includes `S1mpleTraderV3` |
| [docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md](docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md) | Title includes `S1mpleTraderV3` |

Additional `st3` / `.st3` references also remain throughout the broader `docs/reference/mcp/` tree, but the issue-specific cleanup focus is the template/scaffolding cluster first.

### 6. Tests already encode part of the current V2-versus-V1 boundary

Issue #286 does not start from zero. Existing tests already capture parts of the present boundary.

| Test | Current meaning |
|---|---|
| [tests/mcp_server/unit/tools/test_scaffold_schema_tool.py](tests/mcp_server/unit/tools/test_scaffold_schema_tool.py) | Confirms V1-only type error behavior for `generic_doc` |
| [tests/mcp_server/unit/templates/test_generic_doc_template.py](tests/mcp_server/unit/templates/test_generic_doc_template.py) | Confirms the structured generic markdown template behavior that still exists in the current codebase |

These tests matter for later design because they distinguish between:
- broken V2 contract paths that should be corrected
- still-supported legacy/fallback paths that may remain temporarily until the final flag-day removal of V1

### 7. The three-layer V2 SSOT model is confirmed in code but absent from all reference documentation

The V2 pipeline is built on a three-layer architecture where each layer carries a distinct and non-overlapping responsibility. What appears at first glance to be DRY duplication or SSOT drift across the three surfaces is in fact a deliberate and correct division of concern.

#### Layer responsibilities confirmed from code

| Layer | Representative code | Responsibility | Must NOT do |
|---|---|---|---|
| 1 — Context schema | [mcp_server/schemas/contexts/](mcp_server/schemas/contexts/) | Defines the user-facing API contract: which fields are required, their types, and Pydantic fail-fast validation. Never includes lifecycle fields. | Render output. Know about templates, output paths, or scaffold timestamps. |
| 2 — RenderContext schema | [mcp_server/schemas/base.py](mcp_server/schemas/base.py), naming convention `*Context → *RenderContext` | Adds lifecycle fields (`template_id`, `scaffold_created`, `version_hash`, `output_path`) via `LifecycleMixin`. Created by `ArtifactManager._enrich_context_v2()`. Never user-facing. | Re-define fields already in Layer 1. Accept direct user input. |
| 3 — Jinja2 template | [mcp_server/scaffolding/templates/concrete/](mcp_server/scaffolding/templates/concrete/) | Consumes the fully-validated RenderContext to render the output artifact. Trusts that all contract fields are present and valid. The `TEMPLATE_METADATA` block is the SSOT for what variable names the template expects. | Validate input. Decide lifecycle values. |

#### Why this is not DRY duplication

Each layer holds information that the other two layers cannot provide:
- Layer 1 holds the *user intention* (what the agent or developer specifies).
- Layer 2 holds the *system state* at render time (timestamp, output path, version hash).
- Layer 3 holds the *structural output contract* (how the artifact is formatted).

Three different concerns, three separate surfaces, zero accidental overlap when the contract is intact.

#### The generic mismatch as an SSOT breach between Layer 1 and Layer 3

The `generic` artifact demonstrates what happens when the three-layer contract breaks:
- Layer 1 (`GenericContext.methods: list[str]`) specifies that methods are plain strings.
- Layer 3 (`concrete/generic.py.jinja2`) accesses `method.name`, `method.params`, `method.return_type`, `method.docstring`, and `method.body` — expecting structured objects.
- There is no Layer 2 RenderContext that could bridge or transform the shape mismatch.

The consequence is that any non-empty `methods` input will cause a runtime rendering failure. This is a real, code-confirmed production defect that should be treated as the primary implementation target after the reference documentation is accurate.

#### Evidence that the three-layer SSOT model is absent from current reference documentation

| Document | Coverage of three-layer model |
|---|---|
| [docs/architecture/TEMPLATE_LIBRARY.md](docs/architecture/TEMPLATE_LIBRARY.md) | Describes the Jinja2 tier hierarchy (Layer 3 only). Context schemas and RenderContext schemas are not mentioned. |
| [docs/reference/mcp/tools/scaffolding.md](docs/reference/mcp/tools/scaffolding.md) | Describes the `scaffold_artifact` / `scaffold_schema` tool API. Does not describe the schema contract that determines what context is valid. |
| [docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md](docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md) | Describes usage patterns from an agent/caller perspective. Does not explain how context schemas relate to templates or what fields each layer owns. |
| [docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md](docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md) | Quick artifact inventory. No explanation of the three-layer model. |
| [docs/reference/mcp/validation_api.md](docs/reference/mcp/validation_api.md) | Documents the template validation API. Does not explain the Context vs RenderContext split or how validation relates to the layers. |
| [docs/reference/mcp/template_metadata_format.md](docs/reference/mcp/template_metadata_format.md) | Documents `TEMPLATE_METADATA` block format. Does not explain the relationship between template variable names and the context schema contract. |

The net result: no existing reference document explains that the three layers jointly constitute the SSOT. An agent reading the current docs cannot determine why `methods: list[str]` in a context schema combined with `method.name` in a template is a real bug rather than acceptable V2 variation. This absence is the root cause of the documentation gap that issue #286 must address.


## Affected Surface

### Production / configuration surfaces

- [mcp_server/managers/artifact_manager.py](mcp_server/managers/artifact_manager.py)
- [mcp_server/schemas/contexts/generic.py](mcp_server/schemas/contexts/generic.py)
- [mcp_server/scaffolding/templates/concrete/generic.py.jinja2](mcp_server/scaffolding/templates/concrete/generic.py.jinja2)
- [.phase-gate/config/artifacts.yaml](.phase-gate/config/artifacts.yaml)
- [mcp_server/tools/scaffold_artifact.py](mcp_server/tools/scaffold_artifact.py)
- [mcp_server/tools/scaffold_schema_tool.py](mcp_server/tools/scaffold_schema_tool.py)
- [mcp_server/scaffolders/template_scaffolder.py](mcp_server/scaffolders/template_scaffolder.py)

### Documentation surfaces

- [docs/reference/mcp/tools/scaffolding.md](docs/reference/mcp/tools/scaffolding.md)
- [docs/architecture/TEMPLATE_LIBRARY.md](docs/architecture/TEMPLATE_LIBRARY.md)
- [docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md](docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md)
- [docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md](docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md)
- [docs/reference/mcp/template_metadata_format.md](docs/reference/mcp/template_metadata_format.md)
- [docs/reference/mcp/validation_api.md](docs/reference/mcp/validation_api.md)
- Potential new navigation surface: `docs/reference/mcp/README.md`

### Tests / helpers / fixtures

- [tests/mcp_server/unit/tools/test_scaffold_schema_tool.py](tests/mcp_server/unit/tools/test_scaffold_schema_tool.py)
- [tests/mcp_server/unit/templates/test_generic_doc_template.py](tests/mcp_server/unit/templates/test_generic_doc_template.py)
- Registry and artifact-manager tests that cover V2 schema exposure and disabled artifact paths

## Architectural Constraints

| Constraint | Research implication |
|---|---|
| Code is the source of truth | Reference docs must be aligned to the implemented V2 architecture before they are used as design guidance |
| Config-first / SSOT | Registry, template root, context schema, and tool docs must not describe conflicting sources of truth |
| Fail-fast | Documentation should not normalize broken or legacy-only paths as the recommended happy path |
| No accidental preservation of faulty behavior | Research must distinguish supported temporary fallback from the desired long-term normative path |

## Strategy-Sensitive Boundaries

### Boundary 1: Documentation sequencing versus template implementation

A meaningful user decision was provided during research:
- documentation alignment to the V2 codebase comes first
- only after the reference set is accurate should implementation continue on missing or broken template paths

This establishes a boundary-level ordering constraint: the documentation baseline must reflect the implemented V2 code before decisions about missing or broken template paths move forward, so later work is anchored to an accurate reference model rather than a drifting one.

### Boundary 2: Supported fallback versus normative documentation

The codebase currently has a V2 pipeline with a temporary legacy fallback boundary. Research therefore distinguishes between:
- **supported temporary behavior**: legacy fallback may still exist in code during the migration window
- **normative reference behavior**: reference documentation should describe the V2 architecture and must not present V1 paths as the normal recommended operating model

This means the documentation can acknowledge temporary fallback existence where materially necessary, but it must not teach or normalize V1 as the primary path.

### Boundary 3: Documentation cleanup breadth

The cleanup target for this issue is the template/scaffolding documentation cluster first. The broader `docs/reference/mcp/` tree still contains legacy `.st3` and branding references, but those should only be pulled in when directly required by the touched navigation and reference set.

## Unknowns
- Whether the currently identified template/scaffolding documentation cluster is sufficient to establish an accurate V2 reference baseline, or whether directly linked reference surfaces must also be corrected to avoid partial V1-shaped guidance
- Whether `validation-report` should be introduced as a first-class artifact type once the reference baseline is corrected, or deferred to later follow-up work
- Which existing tests beyond the currently read files most directly encode the supported temporary fallback boundary for V1-only document types

## Regression Risks

| Risk | Why it matters |
|---|---|
| Documentation remains partially V1-shaped while code is V2-led | Later template work would be planned against stale references |
| Cleanup reaches too far outside the template/scaffolding cluster | The issue could turn into a broad MCP docs rewrite instead of a bounded bug fix |
| V1 fallback documentation is removed without clarifying temporary support boundary | Future contributors may misread the remaining runtime behavior as undocumented breakage |
| Three-layer SSOT model remains undocumented | Agents and contributors will continue to make false-positive SSOT and DRY violation calls on architecturally correct code |

## Corrected Behavior Framing

Issue #286 should result in a state where:
- the template/scaffolding reference set explicitly describes the three-layer V2 architecture (Context schema, RenderContext schema, Jinja2 template) and the role of each layer
- an agent or contributor reading the reference docs can determine whether a given change violates the SSOT contract or is correct architecture
- the reference set is discoverable as one coherent documentation cluster from `docs/reference/mcp/`
- the touched documentation no longer contains `S1mpleTraderV3` or `st3`-style branding references
- only after that alignment should later decisions about missing or broken template paths proceed from an accurate V2 reference baseline

## Design Input

This section captures the minimum design questions that issue #286 research has surfaced and that design must answer. These are not design decisions; they are boundaries and open questions that need design-phase resolution.

### Question 1: Which document is the authoritative home for the three-layer SSOT model?

Research confirmed that the three-layer architecture is not described anywhere in the current reference set. Design must decide:
- whether the three-layer model belongs in a new or updated top-level architecture document under `docs/architecture/` (e.g., an update to `TEMPLATE_LIBRARY.md`)
- or whether it belongs in the main `docs/reference/mcp/` reference cluster alongside the scaffolding tool reference
- or whether both surfaces need coverage at different levels of detail (architecture rationale versus operational how-to)

The answer must be architecturally coherent: the home for this model is the document where an agent starts when it wants to understand the V2 scaffolding system.

### Question 2: Which documents in the current reference cluster need to change, and what is the minimum coherent scope?

Research identified six documents in the primary cluster plus adjacent drift (navigation, branding, paths). Design must decide:
- which documents can be updated in place
- whether any documents should be merged or split to reduce fragmentation
- what the top-level `docs/reference/mcp/README.md` entry-point should group and how deeply

The scope must be bounded: design should explicitly name what stays out of scope so that later implementation does not expand into a full MCP reference rewrite.

### Question 3: How should the three-layer contract be presented so it prevents false SSOT/DRY violation calls?

Research showed that the SSOT model is architecturally sound but looks like duplication from the outside. Design must determine:
- whether a table, a short prose summary, or a combination is sufficient to communicate the unique role of each layer
- whether the `TEMPLATE_METADATA` block in templates should be the SSOT for Layer 3 variable names, and whether that link to the context schema contract should be made explicit in the docs
- whether worked examples (e.g., the `dto` artifact as a correct three-layer specimen) should be part of the reference documentation

### Question 4: What is the correct before/after for the `generic` artifact schema-template contract?

Research confirmed the mismatch. Design must determine:
- whether the fix aligns Layer 1 to Layer 3 (promote `methods` to structured objects in the context schema)
- or Layer 3 to Layer 1 (rewrite the template to render plain string method names)
- which direction is consistent with how other artifact types (e.g., `dto.fields`) handle structured versus flat method/field lists

This is a code design choice that belongs in the design phase, not in research. Research only surfaces the gap and the two option categories.

## Approved Strategy
| Boundary / consumer scope | Selected strategy | Rationale |
|---|---|---|
| Template/scaffolding reference documentation for issue #286 | Clean break in normative documentation toward V2 | Code is already V2-led; reference docs must stop teaching obsolete V1 paths as the normal model |
| Temporary runtime fallback boundary where legacy paths still exist | Preserve temporary support in code, but do not present it as normative docs guidance | The current migration state still contains fallback behavior, but research must not let stale docs become the source of truth |
| Documentation sequencing versus template-gap changes | Establish documentation alignment as the prerequisite boundary | Any later decisions about template-path corrections depend on an accurate V2 architectural reference baseline |

Constraints for follow-on work:
- subsequent work must treat code as SSOT
- documentation cleanup must stay bounded to the template/scaffolding cluster unless directly linked surfaces are required
- no touched documentation in this cluster may retain `S1mpleTraderV3` or `st3`-style branding references
- design must address the three-layer model question before implementation proceeds

## Related Documentation

- **[docs/reference/mcp/tools/scaffolding.md][related-1]**
- **[docs/architecture/TEMPLATE_LIBRARY.md][related-2]**
- **[docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md][related-3]**
- **[docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md][related-4]**
- **[docs/reference/mcp/template_metadata_format.md][related-5]**
- **[docs/reference/mcp/validation_api.md][related-6]**

<!-- Link definitions -->

[related-1]: docs/reference/mcp/tools/scaffolding.md
[related-2]: docs/architecture/TEMPLATE_LIBRARY.md
[related-3]: docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md
[related-4]: docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md
[related-5]: docs/reference/mcp/template_metadata_format.md
[related-6]: docs/reference/mcp/validation_api.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-06-04 | Agent | Added Finding 7 (three-layer SSOT architecture), Design Input section with four design questions, updated Corrected Behavior Framing and Regression Risks |
| 1.0 | 2026-06-04 | Agent | Initial research draft for issue #286 with docs-first V2 alignment strategy and code-backed template/scaffolding drift findings |
