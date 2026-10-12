<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=KoFPQ3-cAAWFeesb -->

# Phase-Gate MCP 1.0.0

**Status:** PREPARED FOR PUBLICATION  
**Version:** 1.0  
**Last Updated:** 2026-10-12

## Purpose

Provide release-specific installation, capability and provenance notes for the reconstructed standalone release.

## Summary

The first complete standalone Phase-Gate MCP distribution provides an installable Python package and the pgmcp CLI. This retrospective release selects the source integrated on 2026-07-08 in [PR #426](https://github.com/MikeyVK/phase-gate-mcp/pull/426), commit `3bfcef80fa97303d2b51738005b022edbcb0afbd`. The package name/version appeared earlier; this boundary completes standalone packaging. The source date is separate from the present GitHub publication date.

## Included capabilities

- Configured engineering workflows expose Git/GitHub operations, project initialization, phase transitions, quality execution and Jinja scaffolding with context-schema discovery.
- Standalone CLI supports `pgmcp --version` and fresh-workspace `pgmcp --init`; `PGMCP_*` environment settings select the workspace and server roots.
- Manifest-driven packaging delivers default configuration, templates, setup documentation and host instructions, including Coordination, Implementation and independent QA roles.

## Install this historical version

Use Python 3.11 or newer in a separate virtual environment. Download `phase_gate_mcp-1.0.0-py3-none-any.whl` from this release, then run:

```powershell
python -m venv .venv-pgmcp-v1
.\.venv-pgmcp-v1\Scripts\python.exe -m pip install "mcp==1.25.0" .\phase_gate_mcp-1.0.0-py3-none-any.whl
.\.venv-pgmcp-v1\Scripts\pgmcp.exe --version
```

The explicit MCP constraint is required for the demonstrated historical route. The original dependency metadata admits today's incompatible MCP 2.3 API; this release preserves that metadata and runtime. In a fresh workspace, set `PGMCP_WORKSPACE_ROOT` to its absolute path, then invoke the installed `pgmcp --init`. An existing server root is refused. Configure the MCP client to launch the installed server using this environment. Quality executables are separate prerequisites; consult this version's shipped configuration and setup instructions rather than applying the v3 adapter requirements.

## Reconstructed downloads and provenance

The wheel and source distribution were reconstructed on 2026-10-11 with Python 3.13.7, build 1.4.0 and setuptools 84.0.0. Runtime code and manifest-mapped contents retain the selected historical revision. The only source overlay expands package-data patterns to `assets/**/*`, `assets/**/.*` and `assets/**/.github/**/*`, including seven previously omitted Copilot dotfiles. GitHub's automatic source archives reflect the unmodified tagged commit; the attached wheel/sdist include this stated packaging correction. These are new reconstructed artifacts, not the original binaries or a claim of byte-reproducible builds.

| Download | SHA-256 |
|---|---|
| `phase_gate_mcp-1.0.0-py3-none-any.whl` | `b8fe7f0aa8244506039c640a28292e5015b99965e4404fc1b21942e611906546` |
| `phase_gate_mcp-1.0.0.tar.gz` | `4e5b79362309dbfa6f0a0408e3ba6a984613ed894f515bc6e7611a75d0208b8e` |

## Verification and limits

The isolated installation contains 212 Python files and all 139 declared assets. Exact-artifact installation, CLI version, fresh initialization, existing-root refusal and server handshake succeeded; the historical catalog exposes 51 tools. Installed distribution metadata and CLI identify PGMCP 1.0.0. The historical handshake's `serverInfo.version` reports MCP SDK 1.25.0 instead of the PGMCP version. The sdist rebuild retains the complete payload. No historical full-suite campaign or compatibility guarantee for arbitrary modern dependency environments is implied. Publication is on GitHub; this is not a PyPI release.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-12 | @imp documenter | Prepare distinct GitHub release notes from the selected source boundary and verified installation artifacts. |
