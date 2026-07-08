<!-- docs\setup\agentic-bootstrap.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-08T20:40Z updated= -->
# Agentic Bootstrap Guide for New Projects

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-08

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

# Install the phase-gate-mcp package
# (Once published: pip install phase-gate-mcp)
# (For local testing: pip install C:/path/to/local/wheel)
.\.venv\Scripts\python -m pip install phase-gate-mcp
```

### 3. Initialize the Server Root
Run the bootstrapping CLI command to generate the configuration files and templates:
```powershell
.\.venv\Scripts\pgmcp --init
```
This command automatically creates the `.pgmcp/` directory structure containing:
* `config/` (Contracts, enforcement, quality guidelines)
* `templates/` (Jinja2 templates for issues, PRs, etc.)
* `agents/` (Prepackaged IDE configurations and rule files)
* `docs/` (Workflow documentation templates)

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

## Related Documentation
- [docs/setup/README.md](file:///c:/temp/pgmcp/docs/setup/README.md)
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-08 | Agent | Initial draft |