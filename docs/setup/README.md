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
```

---

## 3. IDE Configuration

Follow the steps below depending on whether you are using **VS Code** or **Google Antigravity**.

### Option A: VS Code Setup

VS Code reads the MCP server configuration locally from the workspace.

1. **Copy the MCP configuration:**
   Copy the `mcp.json` template from `docs/setup/mcp.json` into `.vscode/mcp.json` (which is gitignored):
   ```powershell
   Copy-Item docs/setup/mcp.json .vscode/mcp.json
   ```
   *The template uses `${workspaceFolder}` and `${env:GITHUB_TOKEN}`, so no hardcoded paths are needed.*

2. **Configure Agent Rules:**
   Ensure the always-on instructions file (`AGENTS.md`) is loaded by adding the following setting to your VS Code `settings.json` (user or workspace):
   ```json
   "chat.useAgentsMdFile": true
   ```

3. **Reload Window:**
   Run `Developer: Reload Window` in VS Code. The MCP server will start automatically.

---

### Option B: Google Antigravity Setup

Google Antigravity manages MCP servers through a system-wide configuration file located in the user's home directory.

1. **Locate the configuration file:**
   Open the `mcp_config.json` file:
   * **Windows:** `C:\Users\<username>\.gemini\config\mcp_config.json` (or `...\.gemini\antigravity\mcp_config.json`)
   * **Linux / macOS:** `~/.gemini/config/mcp_config.json`

2. **Add the MCP server definition:**
   Add the `phase-gate-mcp` entry under the `mcpServers` object. Replace path placeholders with the absolute path to your cloned repository, and ensure `command` points to the virtual environment's python executable:
   ```json
   {
     "mcpServers": {
       "phase-gate-mcp": {
         "command": "C:/path/to/phase-gate-mcp/.venv/Scripts/python",
         "args": ["-m", "mcp_server.core.proxy"],
         "cwd": "C:/path/to/phase-gate-mcp",
         "env": {
           "PYTHONPATH": "C:/path/to/phase-gate-mcp",
           "LOG_LEVEL": "INFO",
           "MCP_SERVER_NAME": "phase-gate-mcp",
           "MCP_WORKSPACE_ROOT": "C:/path/to/phase-gate-mcp",
           "MCP_SERVER_PROJECT_DIR": ".phase-gate",
           "GITHUB_OWNER": "MikeyVK",
           "GITHUB_REPO": "phase-gate-mcp",
           "GITHUB_PROJECT_NUMBER": "1",
           "GITHUB_TOKEN": "<YOUR_GITHUB_TOKEN>"
         }
       }
     }
   }
   ```

3. **Restart Antigravity:**
   Restart the Antigravity application or reload your agent session to apply the configuration.

---

## 4. Agent Rules, Workflows, and Prompts

When you open the cloned repository as a workspace in your IDE (VS Code or Google Antigravity), the rules, workflows, and prompts are loaded automatically from the repository:

* **Global Rules (`AGENTS.md`):** Loaded automatically to define coding, testing (TDD), and phase-gate standards.
* **Slash Commands / Workflows (`.agents/workflows/`):** Custom workflows (like `/start-issue`, `/end-issue`, and `/go`) are registered automatically as skills/shortcuts.
* **Role prompts (`.github/agents/`):** To start a session in a specific agent role, open a clean chat and mention/load the corresponding agent prompt (e.g. `@file:co.agent.md`, `imp.agent.md`, or `qa.agent.md`).

---

## 5. Verification

Controleer of de MCP server actief is door het volgende commando in de chat te typen:
* **`health_check`** (or `/go` to trigger the active phase check). The server should return a healthy status.

---

## Untracked Files Overview

| File | Description | Action |
|---|---|---|
| `.vscode/mcp.json` | VS Code MCP server config | Copy from `docs/setup/mcp.json` (VS Code only) |
| `~/.gemini/config/mcp_config.json` | Antigravity MCP server config | Modify system config (Antigravity only) |
| `GITHUB_TOKEN` | GitHub API token | Set as User environment variable |
| `.venv/` | Python virtual environment | Recreate via `requirements.txt` |
