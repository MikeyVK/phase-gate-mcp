# Coding Standards

This directory contains the project’s coding and documentation standards. Use the linked
owner document for each binding contract; this index does not duplicate gate commands,
workflow policy, or tool schemas.

## Start here

- [Architecture principles](ARCHITECTURE_PRINCIPLES.md) — binding dependency, state,
  configuration, and object-design constraints.
- [Documentation standard](DOCUMENTATION_STANDARD.md) — requirements for governed
  documentation.
- [Quality gates](QUALITY_GATES.md) — configured checks, tests, evidence, and timing.
- [Code style](CODE_STYLE.md) — practical Python readability guidance.
- [Type-checking playbook](TYPE_CHECKING_PLAYBOOK.md) — how to resolve typing issues.

## Working with the project

Read [AGENTS.md](../../AGENTS.md) for the active cooperation protocol, tool priorities,
workflow-driven test strategy, and approval boundaries. The active workflow contract and
approved plan determine phase order and whether strict RED → GREEN → REFACTOR applies;
there is no universal phase sequence or commit-per-phase rule here.

Use the configured native checks and tests for the current scope. For MCP operations,
follow the active tool documentation and host instructions instead of copying shell
commands or parameter lists into this index.

Tests for the MCP server live under `tests/mcp_server/unit/` and
`tests/mcp_server/integration/`; consult the repository configuration and existing
owners for any additional suites or specialized placement.

## Related documentation

- [Architecture manual](../manuals/architecture.md)
- [Workflow guide](../manuals/phase-workflows.md)
- [Reference index](../reference/README.md)
