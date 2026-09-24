<!-- docs/manuals/architectural_diagrams/08_naming_landscape.md -->
# Naming Landscape

**Status:** Architecture overview; public names are defined by runtime schemas.
**Last Updated:** 2026-09-24

## Purpose

Explain the boundary between implementation module names, public MCP tool names, and
public template-package identities. This page is not an exhaustive tool or template
inventory. The registered schemas and resolved template catalog provide the active
names.

## Names at the public boundaries

| Boundary | Naming authority | Example |
|---|---|---|
| MCP operation | Registered tool name and input schema | `scaffold_artifact`, `scaffold_schema` |
| Template package | `manifest.yaml:template_id` | `python_pydantic_dto`, `typescript_dto` |
| Stored package directory | Suite discovery/storage only | Directory name does not define package identity |

The package identifier is language/framework-qualified where the artifact contract
requires it. The runtime resolves unique package IDs from the admitted suite and exposes
the available IDs through the tool schema. Do not infer a public name from a Python
filename, class name, or physical package directory.

Tool source filenames may reflect implementation structure and are not required to
mirror public MCP names. For current tool inputs and outputs, use the
[modular tool reference](../../reference/tools/README.md) and the registered schemas.
For the package identity and extension contract, use the
[template library usage guide](../../reference/TEMPLATE_LIBRARY_USAGE.md).

## Historical filename note

The former `template_validation_tool.py` / `validate_template` operation is retired.
Suite admission and configured output checks own their respective validation boundaries;
there is no separate public template-validation tool.

## Related architecture

- [Tool layer](03_tool_layer.md)
- [Scaffolding subsystem](09_scaffolding_subsystem.md)
- [Configuration consumers](10_config_consumers.md)
- [Template package identity and resolution](../../development/issue460/design-suite-resolution.md)

