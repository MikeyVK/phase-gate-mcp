<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=KoFPQ3-cAAWFeesb -->

# Phase-Gate MCP 2.0.0

**Status:** PUBLISHED  
**Version:** 1.1  
**Last Updated:** 2026-10-12

## Purpose

Describe the historical upgrade release, its reconstructed downloads and the installation environment proven for those artifacts.

## Summary

Version 2.0.0 adds an explicit upgrade route to the standalone distribution delivered by v1. The canonical source is commit `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b`, integrated on 2026-07-22 in [PR #441](https://github.com/MikeyVK/phase-gate-mcp/pull/441). This is the source integration date, separate from the present retrospective GitHub publication date.

## Changes from 1.0.0

- `pgmcp --upgrade` renews assets with timestamped backups and structured upgrade logs; dynamic workflow state is preserved.
- Workspace `.version` validation supplies actionable initialization/upgrade advice. Package version sources align on 2.0.0 and bootstrap delegates version validation.
- `safe_edit_file` supports replace, append, rewrite and pattern replacement of existing files through atomic writing.
- Configuration failure permits degraded startup with health diagnostics. Template/schema configuration consolidates under the then-current `templates/` root.
- Force phase transitions accept explicit `human_approval_message`; Git commit handling corrects dirty-worktree behavior.

## Install or upgrade with the historical CLI

Use Python 3.11 or newer in a dedicated virtual environment. Download `phase_gate_mcp-2.0.0-py3-none-any.whl`, then run:

```powershell
python -m venv .venv-pgmcp-v2
.\.venv-pgmcp-v2\Scripts\python.exe -m pip install "mcp==1.25.0" .\phase_gate_mcp-2.0.0-py3-none-any.whl
.\.venv-pgmcp-v2\Scripts\pgmcp.exe --version
```

This MCP constraint is part of the demonstrated historical installation route: the original dependency metadata admits today's incompatible MCP 2.3 API. Package runtime and metadata remain unchanged. Set `PGMCP_WORKSPACE_ROOT` to the absolute intended workspace path. Use the installed `pgmcp --init` for a fresh root or this version's `pgmcp --upgrade` for an existing installation, after preserving local configuration and consulting the shipped upgrade guidance. Initialization refuses an existing root. Provision the native quality tools specified by this historical configuration separately. V3's template-suite checkpoints, renewal flags and native adapter contracts are not v2 capabilities.

## Reconstructed downloads and provenance

The wheel and source distribution were reconstructed on 2026-10-11 using Python 3.13.7, build 1.4.0 and setuptools 84.0.0. Historical runtime and manifest content come from the July 22 source boundary, rather than the later local August build. The only overlay expands `pyproject.toml` package-data patterns to `assets/**/*`, `assets/**/.*` and `assets/**/.github/**/*`, recovering seven manifest-declared hidden Copilot files. GitHub automatic source archives are the unmodified tagged revision; attached installation assets include this explicit packaging correction. Neither original historical binaries nor byte-reproducible builds are claimed.

| Download | SHA-256 |
|---|---|
| `phase_gate_mcp-2.0.0-py3-none-any.whl` | `7c821bc9cae575ef5f470b013c8494707ed75cb3aa3d3e006bc1184cf49c85a0` |
| `phase_gate_mcp-2.0.0.tar.gz` | `1a2397943011d971f540fbe5595464f15d01897d83f657156e8fe3c47940bdaa` |

## Verification and limits

The isolated installation contains 171 Python files and all 169 declared assets. Exact wheel installation, CLI version, fresh initialization, existing-root refusal and server handshake succeeded; 51 tools are exposed. The sdist rebuild retains the complete payload. Use distribution metadata or CLI output to identify PGMCP 2.0.0: the historical handshake `serverInfo.version` reports SDK 1.25.0. This bounded proof does not rerun the historical full suite or certify every custom-workspace upgrade. GitHub is the publication destination; no PyPI release is included.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-12 | @imp documenter | Prepare distinct GitHub release notes from the selected source boundary and verified installation artifacts. |
| 1.1 | 2026-10-12 | @imp documenter | Record verified GitHub publication; published release excerpt is unchanged. |
