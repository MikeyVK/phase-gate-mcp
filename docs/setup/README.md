# Setup — New Machine

This directory contains the setup guidelines and configuration files necessary to get the MCP server and agent environment running on a new machine.

## Prerequisites
Before starting, ensure the following are installed:
* **Python** (version 3.13 or later)
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

The running server obtains its version exclusively from installed `phase-gate-mcp`
package metadata. Development uses the editable installation above: source edits
remain directly usable after a server restart, while installation metadata supplies
the version. Re-run `pip install -e .` after changing the package version. Missing
or unreadable package metadata is an error; repository manifests and fixed defaults
are not runtime version sources.

For a new server root, `pgmcp --init` requires complete assembled package assets. A clean editable checkout installed with `pip install -e .` does not assemble those assets automatically. Release preparation requires running `scripts/build_package.py` manually before distributing the wheel; follow the [Release Assets Procedure](../reference/release-assets-procedure.md). Use initialization after provisioning a package with those assets:


```powershell
pgmcp --init
```

For an existing workspace, renew the managed template suite:

```powershell
pgmcp --upgrade
```

Renewal preserves owner-managed configuration. If it reports
`checkpoint_required`, review the local suite and follow the owner-led procedure in
the [Workspace Upgrade Guide](workspace-upgrade.md) before choosing an action.

For the unreleased branch registration contract, coordination must supply the explicit
parent at initialization. Existing workspaces must reconcile branch state and refresh
client discovery deliberately; follow the [registration and recovery guidance](workspace-upgrade.md#unreleased-branch-registration-contract).

Configure owner/repo in root config/github.yaml, with optional project_number and
token alternative. Prefer host GITHUB_TOKEN delivery; launcher settings contain no
repository identity. See [GitHub setup](../manuals/github-setup.md).

### Choose the workspace quality policy

Provision each required adapter's pinned native dependencies, then choose the native
policy for this workspace: source/test roots, language/platform versions, rules,
severities, exclusions and any native CLI arguments. Native discovery, a native
file, explicit schema/arguments or a capability requiring no extra policy are all
legitimate; pgmcp does not determine the effective native configuration for you.

The new defaults/checks.yaml, defaults/tests.yaml and defaults/fixes.yaml leave
acknowledgements null. Declare reviewed choices in root workspace overrides.
Initialization copies supplied assets without clearing choices; it does not make
arbitrary assets neutral. Unresolved choices permit startup/health but refuse
applicable quality execution. See [source composition](../reference/config-loading-architecture.md).

| configuration_choice | Owner declaration |
| --- | --- |
| null or omitted | Setup is unresolved; applicable use is refused |
| native_discovery | Deliberately accept the native tool's discovery behavior |
| configured_arguments | Deliberately use the binding's native argument policy |
| not_applicable | This capability needs no additional native policy configuration |

Record the choice only after reviewing the relevant binding. It does not prove
that a particular file exists or was consumed. Caller arguments still replace
configured defaults and are reported through args_source; they cannot acknowledge
an unresolved binding. A mixed applicable batch with an unresolved choice starts
no checks/tests/fixes. Scaffold and safe-edit enforce refuse writing when setup
prevents an obligation from starting. With a valid server startup basis,
`safe_edit_file(validation="report")` may instead perform a guarded edit of existing
configuration files while choices are unresolved. It returns `written=true` only
for a completed write and `validation_status=not_executed`, preserving each check's
reason without native invocation or validation scratch. Use this route for initial
configuration; then restart/reload the server as required and verify the chosen
bindings. Original-file and persistence errors still block the edit. Report also
retains its existing behavior for executed failed/unavailable check outcomes.

Use a small representative `run_checks(scope="targets", ...)` and, when needed,
a focused `run_tests(scope="targets", ...)` to verify the installed tool, intended
policy and target selection. Review the returned diagnostics before expanding
scope. Template-only renewal preserves the owner's bindings and does not reset
acknowledgements.

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
            "PGMCP_SERVER_NAME": "phase-gate-mcp",
            "PGMCP_WORKSPACE_ROOT": "C:/path/to/phase-gate-mcp",
            "PGMCP_SERVER_PROJECT_DIR": ".pgmcp",
           "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
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

### Option C: Codex Setup

- Keep machine-specific paths and secrets in the Git-ignored `.codex/config.toml`.
- Set the existing PGMCP connection's client window to the approved value:

```toml
[mcp_servers.phase_gate_mcp]
tool_timeout_sec = 1800
```

- Preserve the connection's existing command, cwd, environment and other settings.
- Activate the changed setting in the Codex client connection; restarting only PGMCP does not prove activation.
- Keep normal check/test/fix calls focused and retain their configured default execution budgets.
- For the required full native-configured suite, use `run_tests(scope="configured", timeout_seconds=1200)`. Keep native execution arguments unchanged.
- The client window covers the complete MCP call, including adapter execution, bounded stopping and result delivery. Account for all selected bindings when choosing per-call budgets.
- Do not partition a required full run solely because its known workload exceeds a short default timeout. A timed-out or incomplete run remains incomplete evidence.
- Rationale: the client previously stopped waiting before the full-suite result could be delivered. The owner approved a 1800-second client window and a 1200-second full-test execution budget on 2026-10-04, superseding the [issue460 300-second/partition decision](https://github.com/MikeyVK/phase-gate-mcp/blob/8770607492aeb6d076dfe5aae1dc78f79515dd07/docs/development/issue460/validation.md#owner-decision--client-timeout-2026-09-26). Neither setting promises completion of an arbitrarily long run.

This tracked setup policy and the tracked AGENTS.md instructions survive cloning and branch integration. On every host using main, apply this policy to the local connection and activate it. A Git merge cannot update or activate a Git-ignored client configuration; retain existing machine paths and secrets.

## 4. Agent Files & Git Availability

All core files defining the agent behaviors, constraints, workflows, and role prompts are fully tracked in Git and immediately available when cloning the repository. 

Verify that the following files are present in your workspace; links show their tracked product sources:
* **Project Rules (Always-on instructions):** [AGENTS.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/AGENTS.md)
* **Custom Slash Commands / Workflows:**
  * [create-issue.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/workflows/create-issue.md)
  * [end-issue.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/workflows/end-issue.md)
  * [go.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/workflows/go.md)
  * [start-issue.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/workflows/start-issue.md)
* **Specialized Agent Roles:**
  * **Coordination Authority (@co):** [.github/agents/co.agent.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.github/agents/co.agent.md) (VS Code) & [.agents/rules/co.agent.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/rules/co.agent.md) (Antigravity)
  * **Implementation Executor (@imp):** [.github/agents/imp.agent.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.github/agents/imp.agent.md) (VS Code) & [.agents/rules/imp.agent.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/rules/imp.agent.md) (Antigravity)
  * **QA Reviewer (@qa):** [.github/agents/qa.agent.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.github/agents/qa.agent.md) (VS Code) & [.agents/rules/qa.agent.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/.agents/rules/qa.agent.md) (Antigravity)

*To activate an agent role in VS Code, load `@file:.github/agents/<role>.agent.md` (e.g., `@file:.github/agents/co.agent.md`). In Google Antigravity, load `@file:.agents/rules/<role>.agent.md` (e.g., `@file:.agents/rules/co.agent.md`).*

### Workspace Rule Synchronization
Because VS Code and Google Antigravity resolve agent files and slash commands from different directory structures (under `.github/` and `.agents/` respectively), any manual modifications made to rules, prompts, or workflows must be manually synchronized between these directories to keep the workspace aligned across both IDEs.

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
| `.codex/config.toml` | Codex local MCP config | Apply Option C; set tool_timeout_sec=1800 and activate the client connection |
| `GITHUB_TOKEN` | GitHub API token | Set as User environment variable |
| `.venv/` | Python virtual environment | Recreate via `requirements.txt` |



