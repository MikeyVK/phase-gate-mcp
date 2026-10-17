# Phase-Gate MCP Server

> [!IMPORTANT]
> **Set up or upgrade a workspace?** Give the **[agent-guided checklist](docs/setup/agentic-bootstrap.md)** to your chosen agent chat. It separates owner decisions, health and demonstrated capability use. Installation does not start an agent. The **[Workspace Upgrade Guide](docs/setup/workspace-upgrade.md)** explains template renewal and checkpoint recovery; see **[CHANGELOG.md](CHANGELOG.md)** for release notes.

For installed documentation, give the agent the local file
`<server-root>/docs/setup/agentic-bootstrap.md` supplied by the selected package.
The repository links above describe checkout paths; older installed artifacts keep
their own supplied documentation and behavior.

An MCP (Model Context Protocol) server that enforces structured software development lifecycles. It gives AI agents a toolset to navigate, manage, and execute work strictly within predefined project phases — ensuring consistent state management, quality enforcement, and repository orchestration.

---

## For AI Agents

> **STOP. Do not guess. Do not scan random files.**
>
> Read **[AGENTS.md](AGENTS.md)** immediately to initialize your cooperation protocol.
> It contains the binding tool priority matrix, TDD cycle protocol, three-agent model, and all operating constraints.
>
For MCP server architecture details, see [docs/reference/mcp_vision_reference.md](docs/reference/mcp_vision_reference.md).

---

## What It Does

Phase-Gate MCP Server acts as an orchestrator and gatekeeper between an AI agent and a software repository. Rather than allowing arbitrary modifications, it mandates a structured workflow and prevents phase progression until all deliverables and quality contracts are fulfilled.

**Supported workflow types:** `feature`, `bug`, `refactor`, `docs`, `hotfix`, `chore`, `epic`

Each workflow defines an ordered sequence of phases (e.g. `research → design → planning → implementation → validation → documentation → ready`). The server tracks which phase is active, enforces transitions, and manages TDD cycle state within implementation phases.

---

## Core Capabilities

- **Phase & cycle state management** — tracks active phase and TDD cycle via `.pgmcp/state.json`; blocks progression until contracts are met
- **Schema-guided scaffolding** — resolves a selected template suite, validates its context schema, and renders the requested artifact
- **Configured checks, tests, and fixes** — runs the adapters selected by the active workflow and requested scope
- **Repository orchestration** — native Git and GitHub integrations for branching, committing, PR creation, issue tracking, and label management
- **Config-driven policy enforcement** — workflow rules, phase contracts, configured check/test/fix selection, and evidence requirements defined in YAML

---

## Architecture

```
mcp_server/
├── core/          # Phase state engine, proxy, operation notes, error handling
├── managers/      # State persistence, git operations, and workflow services
├── tools/         # MCP tool interfaces exposed to the agent
├── config/        # Settings, schema loading, config contracts
├── schemas/       # Pydantic schemas for all internal contracts
└── assets/        # Packaged release assets (templates, configs, docs)
```

Workspace policy uses complete `config/defaults/<file>.yaml` bases and optional root `config/<file>.yaml` overrides. The selected config root is self-contained and owner-controlled. See [configuration composition](docs/reference/config-loading-architecture.md); template renewal does not overwrite workspace policy.

| File | Purpose |
| :--- | :--- |
| `workflows.yaml` / `workphases.yaml` / `contracts.yaml` | Workflow order, phase rules, and deliverables |
| `enforcement.yaml` | Tool admission and pre/post enforcement |
| `checks.yaml` / `tests.yaml` / `fixes.yaml` | Configured check, test, and fix selections |
| `adapters.yaml` / `artifacts.yaml` | Adapter trust and artifact locations |
| `git.yaml` | Branch naming conventions |
| `github.yaml` | Explicit repository owner/name, optional project metadata and token alternative |

---

## Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `PGMCP_WORKSPACE_ROOT` | No | Workspace root; defaults to the process working directory. Set explicitly for a launcher whose working directory differs. |
| `PGMCP_SERVER_PROJECT_DIR` | No | Server-root directory under the workspace (default: `.pgmcp`). |
| `PGMCP_CONFIG_ROOT` | No | Owner-controlled configuration-root override. |
| `PGMCP_TEMPLATE_ROOT` | No | Template-suite-root override. |
| `GITHUB_TOKEN` | No | Credential for token-dependent GitHub tools and resources. |
| `PGMCP_SERVER_NAME` | No | Server name reported in MCP handshake (default: `phase-gate-mcp`). |
| `LOG_LEVEL` | No | Logging verbosity (default: `INFO`). |

---

## Getting Started & Installation

**Requirements:** Python 3.13+

Depending on your use case, choose one of the following guides to get started:

- 🔄 **[Workspace Upgrade Guide](docs/setup/workspace-upgrade.md)**: Owner-led instructions for initializing a new server root or reconciling an existing managed template suite with `pgmcp --upgrade`.
- 🚀 **[Runtime and Host Reference](docs/setup/README.md)**: Package/environment, native quality policy and selected VS Code, Antigravity or Codex connection details supporting the checklist.
- 🤖 **[Agent-guided Workspace Checklist](docs/setup/agentic-bootstrap.md)**: The authoritative fresh-setup and upgrade/delta route, explicitly invoked in an agent chat; records owner choices and verified operations while preserving customizations.

### Local Development Setup

To clone and set up the repository for local development:

```bash
git clone https://github.com/MikeyVK/phase-gate-mcp.git
cd phase-gate-mcp
pip install -e .[dev]
```

### Starting the server

The entry point is `mcp_server.core.proxy` — a thin proxy that handles stdio transport and auto-restart on exit code 42:

```bash
python -m mcp_server.core.proxy
```

### CLI Commands (`pgmcp`)

- **`pgmcp --init`**: Initialize a new server root from packaged assets. It refuses when the configured server root already exists; it does not merge into or replace an existing root.
- **`pgmcp --upgrade`**: Reconcile the managed template suite with a staged candidate. A missing trustworthy baseline may return `checkpoint_required` with exit code `2`; review the local suite, then explicitly accept it with `--accept-template-baseline` or replace the managed suite with `--force-template-upgrade`. Force replacement creates a backup. Neither action overwrites the external configuration root. See the **[Workspace Upgrade Guide](docs/setup/workspace-upgrade.md)**.

For MCP client configuration, see [docs/setup/mcp.json](docs/setup/mcp.json) for a reference server definition.

---

## Running Tests

```bash
pytest tests/mcp_server/
```

For coverage:

```bash
pytest tests/mcp_server/ --cov=mcp_server --cov-branch --cov-fail-under=90
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


