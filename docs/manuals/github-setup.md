# GitHub Setup for PGMCP

**Status:** Active reference  
**Last Updated:** 2026-10-16

PGMCP composes GitHub settings through [ConfigLoader](../../mcp_server/config/loader.py), from defaults/github.yaml and optional root github.yaml. The workspace owner supplies repository credentials and controls GitHub-side permissions, labels, branch rules, projects, and milestones. Initializing or upgrading a local PGMCP workspace does not create or change those remote settings.

| Setting | Purpose |
|---|---|
| `github.yaml: owner` | Repository owner used by GitHub tools. |
| `github.yaml: repo` | Repository name used by GitHub tools. |
| `GITHUB_TOKEN` | Optional credential; token-dependent tools and resources become available only when configured. |
| `github.yaml: project_number` | Optional project metadata; no default or requirement for the existing issue/PR tools. |

Local startup and health do not require GitHub setup. GitHub operations require an explicit owner, repository name and token; incomplete setup is refused before client construction. Existing workspace enforcement can require a GitHub PR-status lookup before branch mutations, including file edits; local startup availability does not bypass that gate. There are no personal identity defaults or git-remote inference.

A nonempty GITHUB_TOKEN wins over an explicit token in github.yaml. Repository identity is not read from environment variables or the PGMCP_CONFIG_PATH launcher overlay. Keep the token outside source control. A changed launch environment may require starting a fresh MCP client session; package or active configuration changes require a server restart. See [server configuration](../reference/server-configuration.md) and [workspace upgrade](../setup/workspace-upgrade.md) for the local roots and lifecycle.

For current GitHub tool inputs and result contracts, use the [GitHub tools reference](../reference/tools/github.md) and the server's exposed tool schemas. Configured issue type, priority, and scope values come from the workspace's current declarations; this page does not duplicate them or prescribe external labels. GitHub repository rules remain owner-managed.

For branch and phase work, call `get_work_context` and follow the active workflow in [`contracts.yaml`](../../.pgmcp/config/contracts.yaml). The current [project tools reference](../reference/tools/project.md) documents project and phase operations. This page does not define a separate phase or GitHub Project workflow.

