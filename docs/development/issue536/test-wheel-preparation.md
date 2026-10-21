<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue \#536 — Portable test-wheel preparation

**Status:** External installation trial accepted; final release pending

**Version:** 0.2

**Last Updated:** 2026-10-21

## Purpose

Identify the exact preliminary artifacts for an owner-led fresh installation on another machine, and record the bounded preparation evidence.

## Scope In

Manifest asset selection, five direct documentation links, source-only release procedure, one existing installed-distribution test and exact candidate preparation.

## Scope Out

Builder/runtime/loader changes, a new test suite, global cleanup, final release-version selection, remote installation changes performed by this producer, tags and final release publication. Full #536 Validation is not claimed.

## Summary

Independent QA admitted Research to Implementation at a4ba3d4c52e89053b85e2a9f9f13f3573aa8ec6e. The existing manifest now selects generic defaults/shared schemas and explicit installable references, excluding workspace overrides and the source-workspace release procedure. The exact wheel installs and initializes in an isolated local prefix. The owner supplied the other-machine agent's report and accepted that external installation trial on 2026-10-21. It proves the reported capability slice after explicit dependency/launcher setup; final release acceptance remains separate. A verified test-wheel copy is downloadable from the issue branch. No final release publication or active-environment replacement occurred.

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

Provision only selected native tools/pins and review their policies before setting configuration_choice. Supply the target GitHub owner/repo and token only if those capabilities are chosen. Record the checklist's actual done/open/blocked/N/A outcomes and any missing setup handholds. The owner-observed installation feedback below completes this external trial; successful health alone is not final release acceptance.

## Accepted external installation trial

On 2026-10-21 the owner supplied the Antigravity agent's installation hand-over and
accepted the trial as successful. This section preserves its material observations;
the producer did not independently inspect the other machine or obtain all raw logs.
The source report identified `D:/temp/mybrain`, repository
[MikeyVK/MyBrain](https://github.com/MikeyVK/MyBrain), Python 3.15.1 and the exact
823238-byte wheel/hash listed above.

| Operation or setup fact reported | Outcome and limitation |
| --- | --- |
| Wheel download, hash verification and fresh environment | Exact SHA-256 match; installed wheel and dependencies in a separate Python 3.15.1 environment. PyYAML 6.0.3 needed the explicit `PYYAML_FORCE_LIBYAML=0` source-build route. |
| Installed `python -m mcp_server --init` | Created the selected server root; interpreter, package/module origin and workspace/config/template roots verified by the external agent. |
| Actual agent connection | Ready, 49 tools and 5 advertised resources; healthy version 3.0.0, PID 28596 in the reported run. GitHub identity came from workspace override and token from host environment. This is not proof of every GitHub operation. |
| Agent-visible response delivery | Resource mode retained inline context instructions and actual full operation readback through `read_resource`. A `python_protocol` schema was supplied separately as an embedded resource (reported 12533 bytes). The report says the structured bridge dropped structured data; this is a connection-specific observation, not a universal host/version guarantee. |
| Scratch creation and edit | `scaffold_schema(artifact_type="python_protocol")`, then `scaffold_artifact` for `.pgmcp/temp/scratch_probe.py` and `safe_edit_file(validation="enforce")` succeeded with `python_syntax` after correcting the launch `PATH`. |
| Invalid edit | Proposed `def broken_syntax( -> None:` failed syntax validation at line 12, column 10; `validation_blocked`, `written=false`, original intact. |
| Invalid template input | Non-ASCII class identifier `ScratchPröbeProtocol` was refused as `context_invalid`, with schema feedback. |
| Unconfigured quality binding | Targeted `run_checks` selecting `python_lint` returned `not_executed/configuration_choice_required`. This proves the refusal contract, not lint success. |

The agent selected `python_syntax.configuration_choice="not_applicable"` for that
stdlib-only capability. Other quality choices remained null. The repository had no
initial commit, so real issue-branch workflows were not demonstrated; no main
commit/push was performed. Neither fact invalidates the accepted artifact/edit slice.

The source report found a launch `PATH` mismatch, unavailable structured data in its
bridge, an incorrect suggested MCP registration location, a PyYAML source-build
prerequisite and stale project/path assumptions in supplied host instruction examples.
Remediation uses the shared setup checklist/runtime guide: inspect actual host
capabilities, agree instruction placement with the owner, verify native executables
and select an existing response mode by demonstrated access. The owner additionally approved excluding existing host-specific examples from the
installation package. The manifest no longer maps `docs/agents/`; source examples
and existing target files remain untouched. Shared setup and its direct reference
consumers now describe capability-based placement. The existing installed-distribution
inventory and startup rehearsal are adjusted, without adding a test or runtime code.
No new host-specific setup procedure, detection logic, dependency change or runtime
fallback is authorized.
The existing wheel remains the tested artifact; subsequent documentation edits do
not modify or retroactively validate a rebuilt candidate.

## Focused verification of post-trial corrections

After the explicit owner choice to exclude host bundles, the existing integration
tests were adapted in place: inventory the shipped setup documentation, require
the host asset directory to be absent, and verify fresh CLI initialization still
provides the checklist. The startup test's candidate snapshot now copies its build
manifest explicitly instead of relying on the former whole-config asset mapping.

`run_tests(scope="targets", targets=["tests/mcp_server/integration/test_installed_distribution_v3.py",
"tests/mcp_server/integration/test_target_startup.py"], tests=["python_tests"],
args={"python_tests":["-n","0","-k","complete_wheel_and_installed_catalogs_and_entrypoints or installed_candidate_init_migration_and_mcp_handshake","--tb=short"]},
timeout_seconds=600)`: **2 passed, 10 deselected in 156.12s**, exit 0. This builds
temporary distributions through the existing helpers; it does not replace the
downloadable accepted test wheel or constitute full #536 Validation.

Targeted format/lint on both changed test files and YAML validation of the manifest
passed. A supplemental explicit Pyright run on those test files reported six
Unknown-type diagnostics at the existing request dictionary, GitPython index.add
and jsonschema.validate calls; those lines are unchanged by this work. The normal
configured Pyright target set is production-scoped. An attempted comparison against
the earlier source snapshot under the hidden temp path analyzed zero files, so its
zero-diagnostic exit is not passing baseline evidence. No suppression, type policy
or unrelated API change is introduced. These negative observations remain visible
for phase review.

The final targeted Markdown link check across the six changed documents reported
55 successful link occurrences, 15 existing offline exclusions and zero errors,
exit 0. The complete diff has no whitespace errors. No full suite or new test was
added for this bounded correction.

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
| 0.2 | 2026-10-21 | @imp implementer | Record owner-accepted external installation, actual agent operations, setup remedies and remaining limits without broadening release acceptance. |
