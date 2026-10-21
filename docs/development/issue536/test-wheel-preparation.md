<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue \#536 — Portable test-wheel preparation

**Status:** Preliminary test artifacts — owner installation feedback pending  
**Version:** 0.1  
**Last Updated:** 2026-10-21

## Purpose

Identify the exact preliminary artifacts for an owner-led fresh installation on another machine, and record the bounded preparation evidence.

## Scope In

Manifest asset selection, five direct documentation links, source-only release procedure, one existing installed-distribution test and exact candidate preparation.

## Scope Out

Builder/runtime/loader changes, a new test suite, global cleanup, final release-version selection, external installation, tags and publication. Full #536 Validation is not claimed.

## Summary

Independent QA admitted Research to Implementation at a4ba3d4c52e89053b85e2a9f9f13f3573aa8ec6e. The existing manifest now selects generic defaults/shared schemas and explicit installable references, excluding workspace overrides and the source-workspace release procedure. The exact wheel installs and initializes in an isolated local prefix. Other-machine dependency resolution, the owner's selected harness/capabilities and final acceptance remain open. No publication or active-environment replacement occurred.

## Exact source and artifact identities

Source commit: db7fdaa7d27310fda9ac7e14ef6aa12486632920. Exported committed files to an isolated build tree; no source overlay or metadata-version edit. Version 3.0.0 is retained only as the current provisional package metadata, not the next-release decision. Install the exact wheel path supplied here.

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| phase_gate_mcp-3.0.0-py3-none-any.whl | 823238 | 7b10e0bb3e6d0610b3abc22829dd6c0c5dff12e15fbda8dc1f7d416f6e15dca6 |
| phase_gate_mcp-3.0.0.tar.gz | 611016 | 2bfd4e44b1cb64816494e9faf9964d5eba5cd88bfe07de54a69161fbd9c2d6e1 |

Local build output directory: .pgmcp/temp/issue536/test-wheel-db7fdaa7d273/dist/. At the owner's request, an identical copy of the wheel is tracked at [test-wheel/phase_gate_mcp-3.0.0-py3-none-any.whl](test-wheel/phase_gate_mcp-3.0.0-py3-none-any.whl) on this issue branch for download on another machine. Its size and SHA-256 match the table above. This is preliminary test-artifact distribution, not a GitHub release or final publication; the sdist remains local. Portable wheel tag: py3-none-any; Requires-Python: >=3.15. No broader platform claim is made for third-party dependencies.

## Changed distribution boundary

release_manifest.yaml selects .pgmcp/config/defaults→config/defaults and .pgmcp/config/check_schemas→config/check_schemas. Config root overrides, build manifest and this workspace's repository identity/quality acknowledgements are not distributed. Installable docs/reference files and its tools directory are explicit mappings; release-assets-procedure.md is absent. Five shipped references now link to the source repository procedure instead of a nonexistent installed local file. The generic builder remains unchanged. The existing installed-distribution test retains byte-for-byte inventories for all selected config/schema/template/adapter/contract files and adds exclusions plus neutral GitHub identity checks.

## Build and verification evidence

Existing scripts.build_package public read_manifest/clean_assets/copy_assets helpers assembled declared assets under the isolated snapshot. Invocation: the selected Python 3.15 interpreter ran python -I -m build --no-isolation --outdir <candidate>/dist in that snapshot. The native build created the sdist and then built the wheel FROM that sdist; build exit 0. No custom builder/content-transform logic was introduced. Toolchain: Python 3.15.0, build 1.6.1, setuptools 84.0.0, wheel 0.48.0, pip 26.2.1.

Verified every one of 257 assembled asset files in both wheel and sdist against the selected source bytes, including declared hidden assets. All 20 config files lie under defaults or check_schemas. Both archives lack the release procedure; packaged GitHub owner/repo/token are null.

run_tests(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py','tests/mcp_server/integration/test_installed_distribution_v3.py'], tests=['python_tests'], args={'python_tests':['-n','0','--tb=short']}, timeout_seconds=600): 30 passed in 86.45s, native exit 0. run_checks targets on the modified test with python_format/python_lint passed; yaml_configuration on the manifest passed. markdown_links on the six changed docs reported 53 successful occurrences, 15 configured offline GitHub exclusions, zero errors, exit 0. No full suite, new skip, suppression or threshold change.

## Exact-wheel local installation proof and limits

pip install --no-index --no-deps --no-compile --target <isolated-prefix> <exact-wheel> succeeded, followed by installed CLI --init in a previously absent server root. Dependencies were intentionally reused from the existing Python 3.15 environment; this is not a clean dependency-resolution test.

All 70 observed PGMCP module origins came from the installed prefix, not checkout sources. Installed catalog: 23 templates and 9 adapters. Fresh copied config root contains only defaults/check_schemas; GitHub identity and checks/tests/fixes configuration_choice remain unset. The setup guide is present and the release procedure absent.

Installed stdio initialize/tools/list/health in each mode succeeds: structured 37 tools with matching schema presence, resource 37 tools without structuredContent/outputSchema. The missing token deliberately excludes credential tools per ServerBootstrapper's existing token-driven active-tools selection; the owner-configured workspace previously exposed 49. This is not a tool-loss defect. Native quality use and credential-dependent workflows still require deliberate target configuration. The active source server remained healthy PID22824 and was not installed over or restarted.

## Owner installation on another machine

Use Python 3.15 or later supported by the selected artifact. Create a new isolated environment and install the exact wheel file: <python> -m venv <new-env>, then <env-python> -m pip install <exact-wheel-path>. The placeholders identify owner-selected paths; no OS-specific activation or harness launcher is prescribed.

From the intended new repository root (or with explicit PGMCP_WORKSPACE_ROOT), run <env-python> -m mcp_server --init only while the selected server root is absent. Do not copy this repository's workspace overrides or local launcher. Then give the chosen agent the installed .pgmcp/docs/setup/agentic-bootstrap.md guide and ask it to follow that fresh-setup checklist, establish the intended capabilities and unresolved owner choices, and preserve existing data. Configure that harness with the selected environment's Python, -m mcp_server.core.proxy and the intended workspace root. Select structured/resource per connection when desired.

Provision only selected native tools/pins and review their policies before setting configuration_choice. Supply the target GitHub owner/repo and token only if those capabilities are chosen. Record the checklist's actual done/open/blocked/N/A outcomes and any missing setup handholds. That owner-observed installation feedback is the next step; successful health alone is not final acceptance.

## Evidence locations and remaining issue work

Local candidate directory .pgmcp/temp/issue536/test-wheel-db7fdaa7d273/ contains build.log, install.log, init.log, catalog.log and artifact-evidence.json with exact values. This committed report carries the material invocations/outcomes and identities independently of transient cache IDs.

The source-workspace housekeeping/release procedure completion, final release version/notes/source, full workflow Validation and independent subsequent phase reviews remain within #536. Owner acceptance of exact final artifacts and publication approval remain separate hard gates. Nothing here closes #536 or authorizes tags/uploads.

## Related Documents

- [Live observations](<live-observations.md>)
- [Authoritative setup checklist](<../../setup/agentic-bootstrap.md>)
- [Source-workspace build procedure](<../../reference/release-assets-procedure.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-21 | @imp implementer | Record source/artifact identities, manifest-only portability changes, focused checks and isolated installed-wheel proof. |
