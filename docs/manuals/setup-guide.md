# Setup — New Machine

This directory contains the setup guidelines and configuration files necessary to get the MCP server and agent environment running on a new machine.

## Prerequisites
Before starting, ensure the following are installed:
* **Python** (version 3.11 or 3.12 recommended)
* **Git**
* **VS Code** or **Google Antigravity** desktop IDE
* A **GitHub Personal Access Token (PAT)** with repository scopes

---

## 1. Environment Variables Setup

The MCP server reads the GitHub API token via the `GITHUB_TOKEN` environment variable. Set this as a permanent user-level environment variable:

### Windows (PowerShell)
```powershell
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_xxxxxxxxxxxx", "User")
```
*Note: Restart your IDE or terminal after setting this variable to ensure it is available.*

### Linux / macOS
Add the following to your shell configuration (e.g., `~/.bashrc`, `~/.zshrc`):
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

---

## 2. Python Virtual Environment

Clone the repository and install all dependencies:

```powershell
# Clone the repository
git clone https://github.com/MikeyVK/phase-gate-mcp.git
cd phase-gate-mcp

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# Initialize local workspace configuration and templates
pgmcp --init
```

---

## 3. IDE Configuration: VS Code vs. Google Antigravity

There are critical structural differences in how **VS Code** and **Google Antigravity** handle MCP server registration and agent rules. Choose the section below corresponding to your IDE:

### Option A: VS Code Setup

VS Code registers MCP servers at the workspace level, resolving variables dynamically based on the active project directory.

1. **Copy the MCP configuration:**
   Copy the `mcp.json` template from `docs/setup/mcp.json` into `.vscode/mcp.json` (which is gitignored):
   ```powershell
   Copy-Item docs/setup/mcp.json .vscode/mcp.json
   ```
   *Note: VS Code supports dynamic variables like `${workspaceFolder}` and `${env:GITHUB_TOKEN}`, allowing you to share the configuration across users without hardcoding absolute paths.*

2. **Configure Always-On Agent Rules:**
   To enable VS Code to read the global instructions file (`AGENTS.md`), add the following setting to your VS Code user or workspace `settings.json`:
   ```json
   "chat.useAgentsMdFile": true
   ```
   This configuration forces the VS Code chat/agent runner to prepend the instructions from the repository's root `AGENTS.md` file to every session.

3. **Reload Window:**
   Run the `Developer: Reload Window` command in VS Code. The MCP server proxy will start automatically in the background.

---

### Option B: Google Antigravity Setup

Google Antigravity manages MCP servers either globally or via a **workspace-local configuration file**. Using a workspace-local configuration is the recommended method. Note that dynamic workspace variables (like `${workspaceFolder}`) are not supported in Antigravity; therefore, you must configure absolute paths.

1. **Create the workspace-local configuration file:**
   Create a file named `mcp_config.json` under the `.agents/` directory (which is gitignored):
   ```json
   {
     "mcpServers": {
       "phase-gate-mcp": {
         "command": "C:/path/to/phase-gate-mcp/.venv/Scripts/python.exe",
         "args": ["-m", "mcp_server.core.proxy"],
         "cwd": "C:/path/to/phase-gate-mcp",
         "env": {
           "PYTHONPATH": "C:/path/to/phase-gate-mcp",
           "LOG_LEVEL": "INFO",
           "MCP_SERVER_NAME": "phase-gate-mcp",
           "MCP_WORKSPACE_ROOT": "C:/path/to/phase-gate-mcp",
           "MCP_SERVER_PROJECT_DIR": ".pgmcp",
           "GITHUB_OWNER": "MikeyVK",
           "GITHUB_REPO": "phase-gate-mcp",
           "GITHUB_PROJECT_NUMBER": "1"
         }
       }
     }
   }
   ```
   *Note: Use forward slashes (`/`) even on Windows to prevent JSON escaping issues.*

2. **Alternative: Global Configuration (Not Recommended):**
   If you prefer a global installation instead of the recommended workspace-local one, you can place the exact same JSON configuration under your system-wide `mcp_config.json` file. Note that workspace-local is the standard method:
   * **Windows:** `C:\Users\<username>\.gemini\config\mcp_config.json` (or `...\.gemini\antigravity\mcp_config.json`)
   * **Linux / macOS:** `~/.gemini/config/mcp_config.json`
3. **Agent Configuration & Rule Loading:**
   Unlike VS Code, Google Antigravity natively detects and registers agent rules, workflows, and prompts from the workspace root directory without requiring any manual configurations in a settings file. When you open the cloned repository as a workspace, Antigravity automatically detects:
   * `AGENTS.md` (Global project rules and priority matrix)
   * `.agents/workflows/` (Custom slash commands like `/start-issue`, `/end-issue`, and `/go`)
   * `.agents/rules/` (Specialized agent role prompts for Antigravity: `co.agent.md`, `imp.agent.md`, `qa.agent.md`)

4. **Restart Antigravity:**
   Fully restart the Google Antigravity application or reload your workspace session to apply the changes and start the MCP server.

## 4. Agent Files & Git Availability

All core files defining the agent behaviors, constraints, workflows, and role prompts are fully tracked in Git and immediately available when cloning the repository. 

Verify that the following files are present in your workspace:
* **Project Rules (Always-on instructions):** [AGENTS.md](file:///c:/temp/pgmcp/AGENTS.md)
* **Custom Slash Commands / Workflows:**
  * [create-issue.md](file:///c:/temp/pgmcp/.agents/workflows/create-issue.md)
  * [end-issue.md](file:///c:/temp/pgmcp/.agents/workflows/end-issue.md)
  * [go.md](file:///c:/temp/pgmcp/.agents/workflows/go.md)
  * [start-issue.md](file:///c:/temp/pgmcp/.agents/workflows/start-issue.md)
* **Specialized Agent Roles:**
  * **Coordination Authority (@co):** [.github/agents/co.agent.md](file:///c:/temp/pgmcp/.github/agents/co.agent.md) (VS Code) & [.agents/rules/co.agent.md](file:///c:/temp/pgmcp/.agents/rules/co.agent.md) (Antigravity)
  * **Implementation Executor (@imp):** [.github/agents/imp.agent.md](file:///c:/temp/pgmcp/.github/agents/imp.agent.md) (VS Code) & [.agents/rules/imp.agent.md](file:///c:/temp/pgmcp/.agents/rules/imp.agent.md) (Antigravity)
  * **QA Reviewer (@qa):** [.github/agents/qa.agent.md](file:///c:/temp/pgmcp/.github/agents/qa.agent.md) (VS Code) & [.agents/rules/qa.agent.md](file:///c:/temp/pgmcp/.agents/rules/qa.agent.md) (Antigravity)

*To activate an agent role in VS Code, load `@file:.github/agents/<role>.agent.md` (e.g., `@file:.github/agents/co.agent.md`). In Google Antigravity, load `@file:.agents/rules/<role>.agent.md` (e.g., `@file:.agents/rules/co.agent.md`).*

---

## 5. Verification

Verify that the MCP server is active by running the following command in the chat:
* **`health_check`** (or `/go` to trigger the active phase check). The server should return a healthy status.

---

## Untracked Files Overview

| File | Description | Action |
|---|---|---|
| `.vscode/mcp.json` | VS Code MCP server config | Copy from `docs/setup/mcp.json` (VS Code only) |
| `.agents/mcp_config.json` | Antigravity local MCP config | Create under `.agents/` directory (Antigravity only) |
| `GITHUB_TOKEN` | GitHub API token | Set as User environment variable |
| `.venv/` | Python virtual environment | Recreate via `requirements.txt` |
