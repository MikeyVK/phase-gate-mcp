# Phase-Gate MCP Server

An MCP (Model Context Protocol) server that enforces structured software development lifecycles. It gives AI agents a toolset to navigate, manage, and execute work strictly within predefined project phases — ensuring consistent state management, quality enforcement, and repository orchestration.

---

## For AI Agents

> **STOP. Do not guess. Do not scan random files.**
>
> Read **[AGENTS.md](AGENTS.md)** immediately to initialize your cooperation protocol.
> It contains the binding tool priority matrix, TDD cycle protocol, three-agent model, and all operating constraints.
>
> For MCP server architecture details, see [docs/reference/mcp/mcp_vision_reference.md](docs/reference/mcp/mcp_vision_reference.md).

---

## What It Does

Phase-Gate MCP Server acts as an orchestrator and gatekeeper between an AI agent and a software repository. Rather than allowing arbitrary modifications, it mandates a structured workflow and prevents phase progression until all deliverables and quality contracts are fulfilled.

**Supported workflow types:** `feature`, `bug`, `refactor`, `docs`, `hotfix`, `epic`, `custom`

Each workflow defines an ordered sequence of phases (e.g. `research → design → planning → implementation → validation → documentation → ready`). The server tracks which phase is active, enforces transitions, and manages TDD cycle state within implementation phases.

---

## Core Capabilities

- **Phase & cycle state management** — tracks active phase and TDD cycle via `.pgmcp/state.json`; blocks progression until contracts are met
- **Intelligent scaffolding** — generates code, documents, and test files from a centralised template registry with schema validation
- **Quality gates** — runs Ruff (format + lint), Pyright, import checks, and line-length checks before allowing commits or PRs
- **Repository orchestration** — native Git and GitHub integrations for branching, committing, PR creation, issue tracking, and label management
- **Config-driven policy enforcement** — workflow rules, phase contracts, artifact requirements, and quality thresholds defined in YAML

---

## Architecture

```
mcp_server/
├── core/          # Phase state engine, proxy, operation notes, error handling
├── managers/      # State persistence, git operations, pytest runner, QA manager
├── tools/         # MCP tool interfaces exposed to the agent
├── scaffolders/   # Jinja2 template engine and scaffold orchestration
├── scaffolding/   # Templates, template registry, version hashing
├── validation/    # File and artifact validators
├── config/        # Settings, schema loading, config contracts
└── schemas/       # Pydantic schemas for all internal contracts
```

Configuration lives in `.pgmcp/config/` (per-project, not in this repo):

| File | Purpose |
|---|---|
| `workflows.yaml` / `workphases.yaml` | Phase sequences and lifecycle states |
| `policies.yaml` / `enforcement.yaml` | Transition rules and strictness levels |
| `artifacts.yaml` / `contracts.yaml` | Expected deliverables per phase |
| `quality.yaml` | Active quality gates and thresholds |
| `git.yaml` | Branch naming conventions |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `MCP_WORKSPACE_ROOT` | Yes | Absolute path to the repository root |
| `MCP_SERVER_PROJECT_DIR` | No | Phase-gate config dir (default: `.pgmcp`) |
| `GITHUB_TOKEN` | Yes | Personal access token with `repo` and `workflow` scopes |
| `GITHUB_OWNER` | Yes | GitHub account or org name |
| `GITHUB_REPO` | Yes | Repository name |
| `GITHUB_PROJECT_NUMBER` | No | GitHub Projects number for issue tracking |
| `MCP_SERVER_NAME` | No | Server name reported in MCP handshake (default: `phase-gate-mcp`) |
| `LOG_LEVEL` | No | Logging verbosity (default: `INFO`) |

---

## Installation

**Requirements:** Python 3.11+

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

*(Specify License Information Here)*
