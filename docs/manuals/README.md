# MCP Server Documentation

This directory is the operational index for the PhaseGate MCP Server.

## What Is Authoritative

To avoid contract drift, the authoritative public MCP tool documentation starts at
[docs/reference/tools/README.md](../reference/tools/README.md). Its category references own
the current tool details:

- [docs/reference/tools/git.md](../reference/tools/git.md) for git workflow tools
- [docs/reference/tools/github.md](../reference/tools/github.md) for issue, PR, label, and milestone tools
- [docs/reference/tools/project.md](../reference/tools/project.md) for project and phase tools
- [docs/reference/tools/quality.md](../reference/tools/quality.md) for tests, gates, and validation
- [docs/reference/tools/scaffolding.md](../reference/tools/scaffolding.md) for `scaffold_artifact`
- [docs/reference/tools/discovery.md](../reference/tools/discovery.md) for `get_work_context`, health checks, and server restarts

[docs/reference/MCP_TOOLS.md](../reference/MCP_TOOLS.md) is a navigation entry point.
The modular tool references and live schemas own exact public contracts.

This directory links the MCP server architecture and operational guidance around those references.

## Core Documentation

- **[Architecture](architecture.md)**
  High-level design, layers, component responsibilities, and composition root.
- **[Presentation Architecture](../reference/presentation_architecture.md)**
  Runtime tool catalog alignment, bounded text projections, cache authority, and byte limiting.
- **[Phase Workflows](phase-workflows.md)**
  Development phase workflows and lifecycle guidance.
- **[GitHub Setup](github-setup.md)**
  GitHub integration and token setup.
- **[User Guide](user-guide.md)**
  Operational guidance for using the server.

## Standardized Development

The runtime resolves one template suite at startup. Discover an available package and
its required caller context with `scaffold_schema`, then use `scaffold_artifact` with
that schema. The package identity and schema come from the admitted suite; this index
intentionally keeps no copied ID, field, or path inventory.

See the [scaffolding tool reference](../reference/tools/scaffolding.md) for current
schemas and examples, and the [template library usage guide](../reference/TEMPLATE_LIBRARY_USAGE.md)
for extension and ownership guidance.

## Quick Reference

### Resources

| Resource URI | Description |
|--------------|-------------|
| `pgmcp://rules/coding_standards` | Startup snapshot of configured check, test, and fix policy; not an execution result |
| `pgmcp://status/phase` | Read-time branch and working-tree status snapshot |
| `pgmcp://github/issues` | Read-time snapshot of open issues from the configured GitHub adapter |
| `pgmcp://cache/runs/{run_id}` | Complete structured result for a tool run when published |

### Public Tool Surface

The current registered catalog and navigation by category are maintained in the
[modular MCP tools reference](../reference/tools/README.md). Use the category references
there for current tool names, schemas, result projections, and examples. This manual
index deliberately does not repeat a second tool inventory.

### PR Workflow

Use `submit_pr` for public PR creation. The tool:

1. Neutralizes branch-local artifacts against the merge-base.
2. Commits the neutralization in `ready` phase.
3. Pushes the branch.
4. Creates the GitHub PR.
5. Writes `PRStatus.OPEN` to cache.

`submit_pr` is blocked unless the workflow phase is `ready`, and all `branch_mutating` tools are blocked while the branch has an open PR.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.2 | 2026-08-22 | Agent | Add the bounded presentation architecture to the active documentation index |
| 1.1 | 2026-07-20 | Agent | Fix stale reference/mcp/ paths in tool index links |
| 1.0 | 2026-06-04 | Agent | Initial README |
