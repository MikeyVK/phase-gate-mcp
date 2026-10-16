<!-- docs\setup\agentic-bootstrap.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-08T20:40Z updated= -->
# Agentic Bootstrap Guide for New Projects

**Status:** APPROVED  
**Version:** 1.4  
**Last Updated:** 2026-10-16

---

## Purpose

To guide AI agents on how to bootstrap and configure a new project with the pgmcp workflow completely from scratch without user terminal interaction.

---

## Summary

This guide provides a step-by-step automation procedure for an AI coding assistant to set up a Python virtual environment, install phase-gate-mcp, initialize the server root, copy IDE-specific configurations and agent rules, and initialize the project state.





## Step-by-Step Agentic Bootstrap Procedure

When a user requests to set up `pgmcp` in a new empty workspace, the AI assistant must perform the following steps autonomously:

### 1. Initialize Git & Connect Remote
Since the entire Phase-Gate workflow (branching, commits, quality gates, and PR submission) relies on Git and GitHub, the repository must be initialized and connected to a remote host first:
```powershell
# Initialize local repository with base branch 'main'
git init -b main

# Link to the remote GitHub repository
git remote add origin https://github.com/Owner/Repo.git

# Create an initial commit so that the base branch exists and can be compared against
Set-Content .gitignore "# Git ignores`n.venv/`n.pgmcp/logs/`n.pgmcp/temp/`n.pgmcp/.restart_marker"
git add .gitignore
git commit -m "chore: initial commit"

# Push main branch to remote
git push -u origin main
```

### 2. Initialize Virtual Environment & Install Package
Run the following commands in the terminal using the terminal execution tool:
```powershell
# Create virtual environment
python -m venv .venv

# Install the reviewed release wheel in the MCP launch environment.
# Release downloads remain pending publication; do not assume a PyPI release.
.\.venv\Scripts\python -m pip install C:/path/to/phase_gate_mcp-3.0.0-py3-none-any.whl
```

### 3. Initialize or Renew the Server Root

This guide targets **PGMCP 3.0.0** and assumes an installed package with complete assembled assets. Exact package verification and limitations are recorded with the release evidence. Release preparation uses `scripts/build_package.py`; see the [release assets procedure](../reference/release-assets-procedure.md). A development checkout is not itself a release-ready wheel. Install the reviewed package first; configuration migration, template renewal and server/client restart are separate owner-controlled steps.

For a previously absent server root:

```powershell
.\.venv\Scripts\pgmcp --init
```

Initialization copies the packaged assets into the configured server root, normally `.pgmcp/`, and establishes the managed template state. Its materials include:

- `config/` — configuration assets from the selected reviewed package; the existing 3.0.0 wheel does not gain the unreleased layered layout through this document.
- `template_suite/` — concrete template packages and shared schema/Jinja support.
- `agents/` — distributable host instructions and configurations.
- `docs/` — packaged user, operator, and reference documentation.
- `installation.json` — installed package information and the managed template checkpoint.

An existing server root requires the owner-led renewal procedure:

```powershell
.\.venv\Scripts\pgmcp --upgrade
```

Renewal stages and validates a candidate for the managed template suite, compares it with the active suite and recorded checkpoint, and reports activation or required owner action. It does not refresh owner-managed configuration or workspace adapters. For an existing v2 workspace, explicitly reconcile effective configuration and changed tool inputs against the shipped defaults; preserve owner changes and external roots. Provision the applicable native executables/versions separately, as declared by the [adapter packages](../reference/execution-adapters.md). A missing trustworthy baseline can produce `checkpoint_required` and exit code 2; follow the explicit acceptance or verified-backup replacement procedure in the [workspace upgrade guide](workspace-upgrade.md). Restart after package, active-suite or startup-loaded configuration changes and reconnect the client to refresh tool discovery. Launch-environment changes may require closing and relaunching the client. Treat `installation.json` as the installation/checkpoint record rather than a root `.version` file. Check healthy admission after restart; an acknowledgement alone does not establish it.

### Unreleased #504 — deliberate source-contract adoption

The following applies only to an owner-prepared candidate containing #504. It is not
a description of the unchanged 3.0.0 wheel, and this issue supplies no new assembled
wheel, automatic migration or upgrade mechanism. Prepare a coherent candidate config
root with complete defaults/ bases and optional root overrides before adoption.

For that candidate, prepare repository identity in root config/github.yaml and reviewed quality choices
in root check/test/fix overrides. Prefer host GITHUB_TOKEN delivery. Launcher settings
have no GitHub identity; initialization preserves supplied choices. Read the
[composition contract](../reference/config-loading-architecture.md) before adopting an
existing root; no automatic config migration is provided.

### 4. Deploy IDE-Specific Configurations & Rules
Based on the active IDE, copy and set up the workspace rules and configurations:

#### For Google Antigravity
Copy the prepackaged Antigravity configuration files to the workspace root:
```powershell
# Create rules and workflows directory
New-Item -ItemType Directory -Path .agents/rules, .agents/workflows -Force

# Copy global AGENTS.md rules to the workspace root
Copy-Item .pgmcp/agents/antigravity/AGENTS.md AGENTS.md

# Copy specialized agent role instructions
Copy-Item .pgmcp/agents/antigravity/rules/* .agents/rules/ -Recurse

# Copy custom slash commands (workflows)
Copy-Item .pgmcp/agents/antigravity/workflows/* .agents/workflows/ -Recurse

# Copy the local mcp_config.json configuration
Copy-Item .pgmcp/agents/antigravity/mcp_config.json .agents/mcp_config.json
```
*Note: After copying `mcp_config.json`, the agent must edit `.agents/mcp_config.json` to replace placeholder paths with the absolute paths of the active workspace.*

#### For VS Code
Copy the prepackaged VS Code/Copilot configuration files to the workspace root:
```powershell
# Create vscode and github agent directories
New-Item -ItemType Directory -Path .vscode, .github -Force

# Copy global AGENTS.md rules to the workspace root
Copy-Item .pgmcp/agents/vscode/copilot/AGENTS.md AGENTS.md

# Copy VS Code MCP server configuration
Copy-Item .pgmcp/agents/vscode/copilot/mcp.json .vscode/mcp.json

# Copy specialized agent role instructions & prompts
Copy-Item .pgmcp/agents/vscode/copilot/.github/* .github/ -Recurse

# Enable always-on instructions in VS Code workspace settings
$settings = @{ "chat.useAgentsMdFile" = $true }
$settings | ConvertTo-Json | Set-Content .vscode/settings.json
```

### 5. Initialize Phase Gate State
Once the configuration is copied, the IDE will automatically start/restart the MCP server proxy in the background. The agent must then call:
```json
initialize_project(issue_number=1, issue_title="Bootstrap project", workflow_name="feature")
```
This tool call generates `.pgmcp/state.json` and transitions the project to the initial `research` phase.

---

## Scenario B: Integrating pgmcp into an Existing Project (No prior pgmcp setup)

When a developer wants to add the Phase-Gate workflow to an existing project/repository, the assistant can perform the integration autonomously:

### 1. Install phase-gate-mcp Package
The agent installs the package in the project's existing Python virtual environment:
```powershell
.\.venv\Scripts\python -m pip install C:/path/to/phase_gate_mcp-3.0.0-py3-none-any.whl
```

### 2. Run CLI Initializer
The agent initializes the server root config and templates under `.pgmcp/`:
```powershell
.\.venv\Scripts\pgmcp --init
```

### 3. Deploy IDE-Specific Configurations & Rules
The agent copies the prepackaged rules, prompts, workflows, and configurations from `.pgmcp/agents/` to the workspace root, exactly as described in **Scenario A, Step 3** (deploying `.agents/` or `.vscode/` & `.github/` structures).

### 4. Update Existing Git Ignore Patterns
Since the project already has a `.gitignore` file, the agent must append the `pgmcp` runtime exclusions to the existing `.gitignore` to prevent committing local logs and config secrets:
```powershell
# Append pgmcp ignores to the existing .gitignore
$ignores = "`n# Phase-Gate MCP Server ignores`n.pgmcp/logs/`n.pgmcp/temp/`n.pgmcp/.restart_marker`n.agents/mcp_config.json`n.vscode/mcp.json`n.logs/`ntemp/"
$ignores | Add-Content .gitignore
```

### 5. Initialize State & Commit the Integration
Once the MCP server proxy boots, the agent calls:
```json
initialize_project(issue_number=1, issue_title="Integrate phase-gate-mcp", workflow_name="feature")
```
Finally, the agent adds and commits the configuration files (`.pgmcp/`, `AGENTS.md`, `.agents/` or `.github/`, and the modified `.gitignore`) to the repository:
```powershell
git add .pgmcp/ AGENTS.md .agents/ .gitignore
git commit -m "chore: integrate phase-gate-mcp workflow"
git push
```
This ensures that the workflow configurations are tracked in Git, making them instantly available to other developers on the team.

---

## Related Documentation
- [Setup guide](README.md)
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-10-11 | @imp implementer | Target prepared v3 package; distinguish reviewed wheel installation, owner configuration, native prerequisites, suite renewal and server/client activation without claiming publication |
| 1.2 | 2026-10-01 | Implementation documenter | Describe current template_suite/checkpoint renewal, owner-led baseline handling and restart; retain complete-package assumption |
| 1.1 | 2026-07-20 | Agent | Document .version file creation during CLI init |
| 1.0 | 2026-07-08 | Agent | Initial draft |

| 1.4 | 2026-10-16 | @imp documenter | Separate unchanged 3.0.0 package setup from deliberate adoption of unreleased layered configuration. |

