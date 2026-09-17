<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\02-adapter-packages.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W02 — A small, explicit adapter package

**Status:** REVIEWED — W02-A–F approved; role-specific W03–W05 contracts remain open  
**Owner:** DI-05; dependencies: existing launch/process decisions; consumers: W01/W03/W04/W05/W09/W10  
**Decision nucleus:** Finish admission and shared runtime interfaces without making adapter authors implement a package manager or startup probe.

## 1. Purpose and authority

A workspace owner should be able to install a native development dependency, trust a package and reference its capability. Generic PGMCP should neither know the source language nor invent native commands.

[DI-05 §7.1–7.7 and §7.13](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md) already decides most launch/framing/lifecycle behavior. This workshop fills the remaining declaration and composition gaps.

### Consumer-led review card

The package describes what can be called, not what a workspace must check. Keep the
following authorities separate; these are the concrete consumers behind the fields.

| Authority | Owns | Does not own |
|---|---|---|
| Package manifest | Adapter ID/version, check/test/fix roles, entrypoints, supported operations and required input forms | Workspace profile composition, strictness or native rule settings |
| adapters.yaml under existing configroot | Approved explicit workspace package trust | Package self-certification, duplicated manifests or OS isolation |
| checks.yaml | Workspace check bindings/profiles used by scaffold, safe edit and run_checks | Duplicated native lint/type-check configuration |
| tests.yaml / fixes.yaml | Role-specific configured uses; exact contracts reviewed in W04/W05 | A second process launcher or automatic dependency installation |
| Native tool configuration | Actual native rules and settings, such as pyproject.toml | PGMCP consumer selection policy |

Human partial approval on 2026-09-10 covers source layout, explicit package file inventory,
fingerprint coverage/restart limitation, consumer-backed role descriptors and narrow
shared interfaces. Subsequent human approval closes exact trust configuration and native
provenance delivery; canonical DI-05 §§7.4.1–7.4.3 record the complete W02 boundary. Earlier executable/args,
no-shell/no-startup-probe and workspace-owned installation decisions remain unchanged.

## 2. Scope and exclusions

Package discovery, trust, schema assets, fingerprint inputs, immutable catalog and narrow process interfaces. No automatic adapter upgrade/reconciliation, installation, dependency probe, language registry, execution cache, fourth role, OS sandbox or health tool work.

## 3. Binding inputs

Research F-20/I-19/E-23; one adapter version/fingerprint per package; official plus explicitly trusted workspace packages; on-use unavailability. Startup configuration validity does not promise dependency readiness.

## 4. Decision review state

| ID | Proposal |
|---|---|
| W02-A | Approved W10 refinement: official mcp_server/bundled_adapters and owner resolved_server_root/workspace_adapters |
| W02-B | Approved: explicit required resolved_config_root/adapters.yaml with trusted_adapter_ids; no second settings source |
| W02-C | Approved: capability descriptors have named consumers and actual input requirements |
| W02-D | Approved: closed authored file inventory/fingerprint and restart limitation; not installed dependencies or import-graph inference |
| W02-E | Approved: one startup catalog, narrow readers and shared process runtime |
| W02-F | Approved: required external_tools in ordinary role results; existing scaffold payload explicitly amended, invalid_request unchanged, no new query tool |

## 5. Responsibilities and boundaries

Admission performs declaration/path/reference checks without executing packages. Trust decides whether workspace code is admitted for use; it does not attest safety. Binding resolution is role-config-owned. The process runtime receives a resolved start descriptor, a typed role request, its codec and a deadline; no check IDs, persistence policy or parser recipes.

Interface declarations, without implementations:

```python
class CheckCatalogReader(Protocol):
    def check(self, adapter_id: AdapterId, capability: CapabilityId) -> ResolvedCheck: ...

class TestCatalogReader(Protocol):
    def test(self, adapter_id: AdapterId, capability: CapabilityId) -> ResolvedTest: ...

class FixCatalogReader(Protocol):
    def fix(self, adapter_id: AdapterId, capability: CapabilityId) -> ResolvedFix: ...

class AdapterInvoker(Protocol):
    async def invoke(self, call: TypedAdapterCall[TResponse]) -> InvocationResult[TResponse]: ...
```

TResponse is the selected closed role-response model; it is never an arbitrary BaseModel/dict. Construction and wiring belong to bootstrap. One underlying catalog can implement these narrow readers. Check consumers receive only CheckCatalogReader; FixManager explicitly receives fix and verification-check readers. Consumers get neither unrelated role operations nor install/trust mutation APIs.

## 6. Options and rationale

| Alternative | Trade-off |
|---|---|
| Deep crawler / authored second adapter registry | Hidden work or duplicated manifest authority |
| Shallow packages and explicit trust IDs | Recommended: predictable discovery, identity stays manifest-owned |
| Fingerprint inferred language imports | Requires language knowledge and misses dynamic/data dependencies |
| Explicit package file inventory | Recommended: small maintenance cost, tool/language-neutral ownership |

## 7. Detailed design

### Sources and trust

Inspect only direct child package directories with manifest.yaml. Duplicate adapter_id across sources is an error, not an override. Official packages are distribution-owned. W10's approved refinement authors and ships them directly in mcp_server/bundled_adapters, outside workspace assets; no separate authoring-copy stage. A workspace's resolved_server_root/workspace_adapters is an extension source, not a second copy of official packages. Workspace packages require an exact ID in trusted_adapter_ids; no wildcard or trust-by-name-prefix. A discovered untrusted package is not offered; a config reference to it is an actionable admission error. Unused untrusted source is not executed.

Earlier W02-B proposed server.trusted_adapter_ids through the optional YAML selected by PGMCP_CONFIG_PATH. [Settings.from_env](C:/temp/pgmcp/mcp_server/config/settings.py:116) supports such a caller-selected file, but assigns no standard filename. That optional-settings proposal was rejected in favor of the following human-approved explicit configuration.

Approved: resolved_config_root/adapters.yaml, normally .pgmcp/config/adapters.yaml, with one required unique tuple[AdapterId,...] field trusted_adapter_ids. A managed V3 installation supplies an explicit empty list; missing config follows normal required-config failure, not silent trust fallback. Existing config_root resolution and the central ConfigLoader own loading; inject immutable policy into catalog admission. No duplicate trust setting in checks/tests/fixes or ServerSettings, no new environment variable, no server.yaml and no central package inventory. Trust authorizes owner-controlled content under an ID, not a digest or safety certification. Reusing that ID for changed code remains the owner's responsibility.

The user's remembered templates.yaml was an earlier alternative, not the approved endpoint. [D-SUITE-33 and template topology](C:/temp/pgmcp/docs/development/issue460/design-suite-resolution.md#4-owned-decisions) prohibit a duplicate inventory beside manifests. [DI-04 §3.2](C:/temp/pgmcp/docs/development/issue460/design-mutation-validation.md#32-chosen-configuration-authority) repurposes artifacts.yaml for produced-artifact locations. Neither file is an adapter trust authority, and neither approved boundary is changed by this proposal.

### Manifest shape

Retain approved adapter_id, version, roles.<role>.contract_version, entrypoint and capabilities. Add only:

| Field | Type / rule | Concrete consumer |
|---|---|---|
| files | nonempty unique tuple[PackageRelativeFilePath,...] | Admission, distribution completeness and fingerprint inputs |
| check capability.inputs | nonempty unique tuple of content\|selection | Profile admission and correct request variant |
| check capability.requires_file | required bool if content admitted; forbidden otherwise | Generic proposed-content materialization |
| test capability invocation input | Fixed native args transport; no options_schema | W04 approval supersedes the earlier per-capability options-schema proposal; DI-05 §7.15 |
| fix capability.addresses | nonempty tuple[CheckCapabilityReference,...] | fixes.yaml coherence and post-proposal validation selection |

No description is required without a display consumer. Capability IDs and package IDs use exact case-sensitive strict nonblank tokens matching [a-z][a-z0-9_]{0,63}; no case coercion. Adapter version uses valid SemVer without template-header's 11-character limit: adapter metadata has no 100-character source-header consumer. Contract version is integer literal 1, not inferred from package version.

CheckCapabilityReference has adapter_id and capability only; role is intrinsically check. A fix-only package can point to a different package. This is a foreign key, not duplicated declaration.

The files inventory is relative to the manifest, excludes manifest.yaml itself (included implicitly), rejects duplicate/escaping/missing paths, and includes every entrypoint/schema/dependency-contribution file. Runtime imports/data required for the package must be in it; conformance proves that promise. Unlisted execution files are not supported inputs. Native dependencies are installed outside this package inventory. No generic source-code scanner claims to discover imports.

Subsequent W04 input approval supersedes the test options_schema field: run_tests exposes configured test IDs and addressed native CLI argument lists in one startup schema. It does not enumerate native switches. Structural request validation remains mandatory; native switch prevalidation does not. Canonical DI-05 §7.15 owns this amendment; package identity, trust, files and other roles are unchanged.

### Illustrative check package

This is a proposed workspace-authored Ruff integration, not an official package ID,
shipped capability list, conformance result or dependency-version recommendation.
Its owner supplies the actual adapter implementation and installs its native dependencies.

```yaml
adapter_id: team_ruff
version: "1.0.0"
files:
  - check.py
  - requirements-dev.txt
roles:
  check:
    contract_version: 1
    entrypoint:
      executable: python
      args:
        - package_file: check.py
    capabilities:
      lint:
        inputs: [content, selection]
        requires_file: false
```

The manifest is implicitly part of its own fingerprint and is not repeated in files.
The declared input support is an adapter obligation, not proof supplied by the manifest.
PGMCP passes proposed content for scaffold/safe edit or an admitted selection for
run_checks; the adapter translates that request into the native call. Profiles decide
which consumers actually select lint. Native lint rules remain in the native settings.
The dependency file contributes installation instructions, never an automatic install.

Approved workspace trust is explicit in resolved_config_root/adapters.yaml:

```yaml
trusted_adapter_ids: [team_ruff]
```

This adapter-wide config is approved in DI-05 §7.4.2, but not implemented. It selects trusted
manifest IDs, not package paths, capabilities, native rule settings or installed versions.

### Fingerprint scope and limits

Approved: one domain-separated SHA-256/96 Base64url identity, reusing the compact value type but **not template graph semantics**. Domain pgmcp:adapter-package:v1. Hash canonical manifest (including version) plus sorted package-relative file names and exact file bytes with explicit lengths. One byte change in a declared script/data/schema/dependency asset changes the fingerprint. Outer package location, installed executable, native workspace config, unrelated packages and runtime files do not.

Exact bytes avoid pretending to canonicalize arbitrary executable languages/binaries. This identity is a diagnostic content label, not authenticity, compatibility or reproducibility proof. No file-level versions or run-level adapter-suite fingerprint.

Catalog descriptors are restart-stable. Editing executable package files while the server runs violates that content-stability assumption; restart after edits. No monitoring/hash-before-every-call or shadow-copy engine is proposed. Record this limitation explicitly with run evidence: fingerprint is the admitted package snapshot identity, not an attestation of all bytes executed after arbitrary external changes.

### Native provenance return channel — approved amendment

This is not a new discovery/query tool or a second mandatory call. It is a typed part
of the ordinary execution response retained with invoked-adapter evidence in the existing
operation cache. A caller reads that existing cache only when full details are useful;
normal text need not print versions. The consumer is a human/agent diagnosing results,
not automated compatibility or pass/fail logic.

Concrete motivation: two runs can use identical adapter bytes/version while the workspace
updates Ruff itself. Different native versions are then a useful first explanation for
different findings; a package fingerprint alone cannot show that difference. This remains
diagnostic context, not proof of causality or full environment reproducibility. No separate
version-query operation, startup inventory or generic tool-specific version parser is proposed.

The previous DI-05 contract required native identity/version but closed the scaffold payload to decision/evidence. Human-approved W02-F resolves that gap: §7.4.3 and the complete scaffold-facing output table in §7.13 now explicitly include external_tools. Do not read versions out of arbitrary NativeEvidence or make the generic runtime discover tool-specific versions.

Approved: required external_tools:tuple[ExternalToolIdentity,...] to successful, negative and unavailable **role-result** responses for check/test/fix. Each record is closed: tool_id:NonBlankText, version:NonBlankText|null. It identifies a native tool or library actually selected/observed during that call; unknown version remains null. Empty means no such identity was obtained, for example a missing dependency before native work. It does not claim no dependencies exist. Shared invalid_request retains its existing minimal shape with no external_tools; generic call failures have no forged adapter response.

Adapters discover their tool/library version during ordinary invocation, not through a startup probe or new operation. Generic invocation evidence copies these records and adds the package/contract provenance it already owns. Consumers are the cached check/test/fix report and diagnostic comparison; the values never decide status, compatibility or authorization. Accepted role responses are not duplicated as raw stdout.

This explicitly changes the earlier closed Design payload; its canonical field list and output alternatives have been updated together. Schema/conformance implementation remains required. W03's selection additions stay separate and must preserve this now-approved scaffold baseline.

### Process completion interface

Retain one UTF-8 JSON request + EOF, one response, exit mapping 0/1/2/3, stdout 8 MiB, stderr head/tail 256 KiB, five-second shared stop budget, startup PATH resolution, explicit executable/args, no shell fallback and workspace cwd. W03–W05 bind their own response variants to the shared exit categories.

Platform mechanics stay behind an injected managed-process boundary. Windows uses a managed job capable of tracking associated descendants; supported POSIX operation needs process-group/session management and separately proven limits. Failure to establish required lifecycle management must not silently degrade to parent-only termination. No claim of verified Linux support.

### Native data and public paths

Use the approved W01-F boundary in [DI-04 §4.6](C:/temp/pgmcp/docs/development/issue460/design-mutation-validation.md#diagnostic-disclosure--approved-2026-09-10). Public operation locations remain workspace-relative, including in cached DTO fields. Bounded raw/native diagnostic content may incidentally contain absolute paths in the existing on-demand cache; the adapter does not have to rewrite native evidence merely to strip host paths. Preserve truthful location meaning: never label a physical scratch location as the user's intended target. Ordinary inline presentation stays bounded without automatic raw stream/stack-trace dumps. The cache is agent/client-accessible, not private local storage; retrieval can disclose content to models/providers or client logs. No diagnostic-ID-only replacement, separate private log, generic secret/path scrubber or universal redaction guarantee is introduced. Disclosure and W02-A–F are approved; actual conformance and role-specific W03–W05 contracts remain open.

## 8. Flow and failures

Manifest malformed / duplicate / invalid reference → admission failure. Missing external executable → unresolved launch selection, still configured schema choice, launch_failed on use. Native dependency absent after adapter starts → dependency_unavailable. No startup execution. Call failure and stop problem remain separate facts; late JSON cannot reverse timeout. Cleanup stays nonblocking and only after no process owns the inputs.

## 9. Migration and removal

Retire QAManager command/parser ownership and PytestRunner as generic privileged routes only after role conformance and selected migration evidence. Do not import executable adapters into server Python. Official packages follow release packaging, not F-10 template renewal; workspace packages are never overwritten merely because an official update occurs.

## 10. Evidence

Admission type/path/trust tests; declared files completeness; same content at moved roots; one changed declared file; separate package unaffected; no startup process; explicit interpreter launch; real descendant completion/timeout/cancellation; both output ceilings; non-Python package through unchanged generic code. Manifest conformance and native behavior are separate proof sets.

## 11. Review points and risks

W02 decisions are closed, including explicit adapters.yaml and ordinary native provenance.
Next review is W03; completed decisions do not claim implemented conformance. Platform conformance and hostile detached-work limits
remain evidence obligations, not a claim of process sandboxing.

## 12. Planning consequences

Catalog/protocol conformance precedes deleting old runners. Separate check/test/fix migration evidence and separate platform lifecycle evidence; no cycles specified.

## 13. Traceability

Q-ADAPTER-02/04/07 → manifest/catalog/contracts; Q-ADAPTER-03 → content capability route; F-20 provenance/trust → file inventory/fingerprint; XC-01 → injected generic runtime; DI-06 → distribution boundary.

## 14. Related documentation and history

Next: [W03 checks](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/03-run-checks.md). W04/W05 add role-specific contracts, not another launcher.  
0.4, 2026-09-10: close W02-B/F after human approval; update canonical scaffold response and downstream role proposals; advance to W03.  
0.3, 2026-09-10: record partial W02 approval; propose explicit adapters.yaml, preserve approved artifacts.yaml/template-discovery roles, and clarify native provenance as ordinary cached execution evidence; trust and provenance decisions remain open.  
0.2, 2026-09-10: begin W02 after W01 approval; add the consumer authority map and explicit illustrative package/trust configuration, without approving W02 or changing canonical package contracts.  
0.1, 2026-09-10: temporary proposal.
