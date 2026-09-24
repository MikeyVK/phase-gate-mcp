# Phase-Gate MCP Architecture

This page orients readers to the active architecture. It is a navigation guide, not a second
module inventory, schema catalog, or operational policy. Source code, typed schemas, package
manifests, and the linked owner documents define the details.

## Runtime shape

The CLI enters the target runtime through `ServerBootstrapper.bootstrap_target()` in
`mcp_server/bootstrap.py`. The composition root loads resolved runtime and workspace
configuration, builds manager and execution dependencies, assembles supported and active
tools, then creates the MCP server with its resources and presenter.

Core tools implement `ICoreTool`; the target `ToolAssembly` validates supported names
and output contracts and selects the active subset. The core `ToolFactory` wraps active
tools with enforcement, input validation, and error handling before `MCPServer` registers
them. Native checks, tests, and fixes are separate configured operations backed by their
execution adapters; native settings and executable behavior remain adapter-owned.

## Configuration and package ownership

`Settings.from_env()` resolves runtime settings and roots. `ConfigLoader` reads typed
workspace declarations, including check, test, fix, adapter-trust, and artifact-location
configuration. Template manifests own package identity, policy, context schema, and
content. Configuration selects work; it does not install or probe native dependencies.

## Architecture references

- [System context](architectural_diagrams/00_system_context.md)
- [Module decomposition](architectural_diagrams/01_module_decomposition.md)
- [Tool layer](architectural_diagrams/03_tool_layer.md)
- [Configuration layer](architectural_diagrams/05_config_layer.md)
- [Runtime flows](architectural_diagrams/06_runtime_flows.md)
- [Scaffolding subsystem](architectural_diagrams/09_scaffolding_subsystem.md)
- [Configuration consumers](architectural_diagrams/10_config_consumers.md)
- [Configuration and template loading](../reference/config-loading-architecture.md)
- [Tool reference index](../reference/tools/README.md)
- [Resource reference](../reference/resources.md)
- [Workflow guide](phase-workflows.md)
- [GitHub setup](github-setup.md)

Use the relevant tool, configuration, resource, or package reference for exact public
contracts. The diagrams show selected responsibilities and dependencies; they are not an
exhaustive import guarantee.
