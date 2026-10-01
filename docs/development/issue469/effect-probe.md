<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 469 / 474 — Isolated Native Write-Effect Evidence

**Status:** OBSERVED — Research evidence; independent QA pending
**Version:** 1.1
**Last Updated:** 2026-10-01


## Purpose

Persist reproducible effect evidence and the complete probe source for the human-approved combined issue-469/474/475 Research scope. Distinguish observational runner completion from adapter conformance.

## Scope In

Ruff check/fix format and lint, Mypy check types; cache routing through CLI, local native configuration, child-local environment and defaults; cache-disabled controls; existing explicit report-output rejection controls.

## Scope Out

Production repair, future regression-test design, public apply_fixes-route certification, actual host-external destinations, ACL/configuration changes, arbitrary executable-code confinement and the R-06 OS-sandbox boundary.



## Policy interpretation after Research reopening

The owner reopened B4 after this probe: PGMCP owns execution conditions and any write policy, and concrete restrictions must be feasible and proportionate to personal local use. The terms unauthorized and misrouted below refer to the original simulated B4 policy at the time of observation; they are not a current decision that every operator-configured native cache outside selected sources must be prohibited. The observed bytes, inventories, native outcomes and archived probe remain unchanged. See [current Research](research.md#approved-strategy) for the pending replacement policy and release-risk decision.

## Summary

Across 30 cache-effect cases, all 15 deliberately misrouted cases created native cache files in the simulated unauthorized destination. CLI, native config and child-local environment each reproduce the gap for all five role/capability combinations. Native defaults and explicit permitted cache controls wrote only the named allowed cache; disabled caching wrote none. Five additional report-output controls returned unavailable/unsupported_input with no created or changed files. All destinations remained within the approved temporary root.






## Sections


### Authorization and isolation


**Content:**

The human accepted S1, B1–B6 and the isolated effect-probe route on 2026-10-01: "Ja ik accepteer je voorstel". Native workspaces were distinct subdirectories of .pgmcp/temp/issue469-effect-probe/run-approved-20261001 or run-refusal-approved-20261001. Both basetemp paths were verified absent before their first Pytest use. The selected source, unselected decoy, default cache and simulated unauthorized destination are separate paths in those roots. The probe checks resolved root containment before choosing a destination. It does not attempt a real external write or establish OS confinement.

Local pyproject.toml controls native config discovery; only child-local RUFF_CACHE_DIR/MYPY_CACHE_DIR is varied, existing routing/cache environment overrides are removed from the child copy, and Python bytecode writing is disabled for the observed child entrypoints. No environment values or credentials are printed. Temporary file inventories and selected/unselected source bytes are inspected before and after each native operation.





### Exact runner invocations and native identities


**Content:**

The original cache probe completed one selected test in 24.12s and emitted exactly 30 EFFECT_OBSERVATION records. The refusal control completed one selected test with one deselected in 1.17s and emitted five REFUSAL_OBSERVATION records. Ruff reported 0.15.6; Mypy reported 1.19.1. Pytest runner reported 9.0.2.

```json
{
  "scope": "targets",
  "targets": [
    ".pgmcp/temp/issue469-effect-probe/test_write_effects.py"
  ],
  "tests": [
    "python_tests"
  ],
  "args": {
    "python_tests": [
      "-q",
      "-s",
      "-n",
      "0",
      "-o",
      "addopts=",
      "-p",
      "no:cacheprovider",
      "--basetemp",
      "C:/temp/pgmcp/.pgmcp/temp/issue469-effect-probe/run-approved-20261001"
    ]
  },
  "timeout_seconds": 180
}
```

The first invocation preceded adding the second test; its 30-case function is unchanged in the archived source. To reproduce only that function with the final source, additionally select `-k record_isolated_native_write_effects` and use a fresh, absent basetemp under the approved root.

```json
{
  "scope": "targets",
  "targets": [
    ".pgmcp/temp/issue469-effect-probe/test_write_effects.py"
  ],
  "tests": [
    "python_tests"
  ],
  "args": {
    "python_tests": [
      "-q",
      "-s",
      "-n",
      "0",
      "-o",
      "addopts=",
      "-p",
      "no:cacheprovider",
      "-k",
      "existing_output_write_routes_are_refused",
      "--basetemp",
      "C:/temp/pgmcp/.pgmcp/temp/issue469-effect-probe/run-refusal-approved-20261001"
    ]
  },
  "timeout_seconds": 90
}
```

Complete cached DTOs were read through contiguous resource windows with run ID, length and UTF-8 SHA-256 verified: [cache-effect run](pgmcp://cache/runs/310efd1225fe42828f73f881e982701d), [report-output refusal run](pgmcp://cache/runs/7ef68a12f021414bb07cfcfa99906281). The caches are supplementary transient evidence; the source and observations are persisted here.





### Cache effects by option source


**Content:**

| Adapter / role | Operation | Option source | Native decision | Allowed cache files | Simulated unauthorized cache files | Selected source changed |
|---|---|---|---|---:|---:|---|
| ruff_check | format | allowed_cli | failed | 2 | 0 | false |
| ruff_check | format | unauthorized_cli | failed | 0 | 2 | false |
| ruff_check | format | unauthorized_config | failed | 0 | 2 | false |
| ruff_check | format | unauthorized_environment | failed | 0 | 2 | false |
| ruff_check | format | native_default | failed | 2 | 0 | false |
| ruff_check | format | write_disabled | failed | 0 | 0 | false |
| ruff_check | lint | allowed_cli | failed | 3 | 0 | false |
| ruff_check | lint | unauthorized_cli | failed | 0 | 3 | false |
| ruff_check | lint | unauthorized_config | failed | 0 | 3 | false |
| ruff_check | lint | unauthorized_environment | failed | 0 | 3 | false |
| ruff_check | lint | native_default | failed | 3 | 0 | false |
| ruff_check | lint | write_disabled | failed | 0 | 0 | false |
| ruff_fix | format | allowed_cli | passed | 3 | 0 | true |
| ruff_fix | format | unauthorized_cli | passed | 0 | 3 | true |
| ruff_fix | format | unauthorized_config | passed | 0 | 3 | true |
| ruff_fix | format | unauthorized_environment | passed | 0 | 3 | true |
| ruff_fix | format | native_default | passed | 3 | 0 | true |
| ruff_fix | format | write_disabled | passed | 0 | 0 | true |
| ruff_fix | lint | allowed_cli | passed | 3 | 0 | true |
| ruff_fix | lint | unauthorized_cli | passed | 0 | 3 | true |
| ruff_fix | lint | unauthorized_config | passed | 0 | 3 | true |
| ruff_fix | lint | unauthorized_environment | passed | 0 | 3 | true |
| ruff_fix | lint | native_default | passed | 3 | 0 | true |
| ruff_fix | lint | write_disabled | passed | 0 | 0 | true |
| mypy_check | types | allowed_cli | passed | 119 | 0 | false |
| mypy_check | types | unauthorized_cli | passed | 0 | 119 | false |
| mypy_check | types | unauthorized_config | passed | 0 | 119 | false |
| mypy_check | types | unauthorized_environment | passed | 0 | 119 | false |
| mypy_check | types | native_default | passed | 119 | 0 | false |
| mypy_check | types | write_disabled | passed | 0 | 0 | false |

Every row preserved the unselected source. Checks preserved selected source bytes; each Ruff fix changed only the selected source. Ruff check format/lint deliberately analysed a source with formatting/F401 findings, so their native failed outcomes are substantive analysis results, separate from the effect violation. Mypy analysed a clean annotated source.

Ruff format check created .gitignore and CACHEDIR.TAG; Ruff lint check and both fix capabilities additionally wrote a versioned cache entry. Each Mypy routed/default-cache case created 119 files, including native metadata/data files. These counts are specific to this fixture and supported native versions, not product invariants. Cache-disabled controls used Ruff --no-cache and Mypy --cache-dir nul on Windows and created no files.





### Existing rejection controls


**Content:**

| Adapter / role | Operation | Request | Observed result | Created / changed files |
|---|---|---|---|---|
| ruff_check | format | --output-file <simulated unauthorized report> | unavailable / unsupported_input | 0 / 0 |
| ruff_check | lint | --output-file <simulated unauthorized report> | unavailable / unsupported_input | 0 / 0 |
| ruff_fix | format | --output-file <simulated unauthorized report> | unavailable / unsupported_input | 0 / 0 |
| ruff_fix | lint | --output-file <simulated unauthorized report> | unavailable / unsupported_input | 0 / 0 |
| mypy_check | types | --junit-xml <simulated unauthorized report> | unavailable / unsupported_input | 0 / 0 |

These controls show existing pre-write rejection for report-output options. They do not show destination-policy enforcement for the admitted cache routes; those routes remain defective under approved B4.





### Causal conclusion and evidence limits


**Content:**

Selected-file validation and source-byte preservation do not constrain operational cache writes. Native cache destinations come from CLI, configuration, environment and defaults. The adapter guards admit the cache routes without an effect-authority check; the native processes then create files at the admitted destination. CLI-only filtering would leave the reproduced configuration/environment routes open.

The observations extend F474-01 beyond Ruff fix to Ruff checks and Mypy checks. They do not attribute the same defect to other packages or prove those packages effect-safe. Existing source/metadata/write guards and the individual applicability audit remain relevant counterevidence. The producer-selected probe executes public adapter entrypoints directly through run_tests; it does not certify the public apply_fixes manager route, which was not exercised. No production fix was applied, and no issue or acceptance criterion is closed by a passed diagnostic runner.





### Inventory fingerprints


**Content:**

Each fingerprint covers the sorted relative-file-name to file-byte-SHA-256 snapshot serialized as JSON. Complete maps were computed in the probe; native cached observations contain fingerprint pairs, created-file counts and samples, and changed-file names. Equality in disabled-cache check controls corroborates no observed file effects in those workspaces. These fingerprints are probe evidence, not a new PGMCP provenance/registry contract.

| Case | Before inventory SHA-256 | After inventory SHA-256 |
|---|---|---|
| ruff_check/format/allowed_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `666d6939d42850036f8dfe6b6d639054c57260bf7e50dfc4605fddd3a0e44436` |
| ruff_check/format/unauthorized_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `41493e3b61c7642a5c3933b0f6e2b635cb9afd7ba3f4333ebbc19970514fcbd6` |
| ruff_check/format/unauthorized_config | `d02e35bb8ede867a322eb5a82f54cf287d9dd4b765b46142938c0b3d982513b7` | `e82cd0f8c6c77c5e4222eab171d07c6dff9f1217769d7947983c61ac20e61170` |
| ruff_check/format/unauthorized_environment | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `41493e3b61c7642a5c3933b0f6e2b635cb9afd7ba3f4333ebbc19970514fcbd6` |
| ruff_check/format/native_default | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `666d6939d42850036f8dfe6b6d639054c57260bf7e50dfc4605fddd3a0e44436` |
| ruff_check/format/write_disabled | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` |
| ruff_check/lint/allowed_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `16bdd2bb9ae12eef1d485c63dd45cb99f5850f1690988dfd778a83f2cdcb2c66` |
| ruff_check/lint/unauthorized_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `7dc0507ac50381af5f790d4cadea4a70699c151d64c09fcbe008a95ae2057001` |
| ruff_check/lint/unauthorized_config | `118e0f7a17c3a44d18b4012e63c65954fcee57ff48bfe9cd76d8762e4b3625e3` | `85692721ab22eb90ccd4abcc1fde007b9b31385cff315d355eef796c0ffc0ae3` |
| ruff_check/lint/unauthorized_environment | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `4bcc99722443c190d557fb65b68c20e95f9bc053d50925ac7b016ec8f9f2320e` |
| ruff_check/lint/native_default | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `4c667aa743330459e87966bfb5b3eeafa2d70a0203c2ae8f372bad7d4ab60acd` |
| ruff_check/lint/write_disabled | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` |
| ruff_fix/format/allowed_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `e847952cedf72b530b4eeb5642c8dd79d63bc7d26af84bf6393e257b9abe1f69` |
| ruff_fix/format/unauthorized_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `ec9129a62bc562774a55b9a5fe0016ceda58aee47333efd5fbb83eb1b51b3ebc` |
| ruff_fix/format/unauthorized_config | `62947ed3b52d653c7fce4af2f27c917d9265f0e3344669a07d40dddf5f69a02d` | `04da50ca1e2d973c078bc8cff0cf59857e7c84516132a8c70a589b7f0db421d4` |
| ruff_fix/format/unauthorized_environment | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `ad1e5dd8ca3ea315e24004a2a2cd6b1d9f150711611114654f59f6d4a17b839a` |
| ruff_fix/format/native_default | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `40a654a8c5486badfff2823e1ed1959a153984744842517619b2c90c3f6409f3` |
| ruff_fix/format/write_disabled | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `4daab2f25a77ae19371e8e5bee1c5aa2dbbbdf0475b7c1571cc0fb977f8577b4` |
| ruff_fix/lint/allowed_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `d8b6b886a459f32d95acea4468ffb908e6a324c498636ab860caf5627632b1b3` |
| ruff_fix/lint/unauthorized_cli | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `388f9bb502373ee9e515ef88d4d444f5f584e8eddbbc2ac053cb9a0d12b248df` |
| ruff_fix/lint/unauthorized_config | `d123d39372589fe1edc96af165e454805ecefe9f185fdfaca64225c63f2342d2` | `ba4bd18d5081c65b26690d917d2cb40f89eca6c77487c5f84dcdba0b2f0a6c61` |
| ruff_fix/lint/unauthorized_environment | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `61e3df67c9d902d5629b5a9d247ae8303fe246045b5720026a7cd4a11a0930d6` |
| ruff_fix/lint/native_default | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `40cdd9a4d392578fbeb6611c80dd61f961e27d0289d066c13f3e2ba1811ef586` |
| ruff_fix/lint/write_disabled | `767e54fe8d8865f93a7610afd9ecf3736019894ffde858c813296aaac728645e` | `c59bde9fafac884bdbd26b714e2f3f1231175719a262170a462a839c26820e16` |
| mypy_check/types/allowed_cli | `d57d13f31566fc9ea2528f88741a69212985c0a062338fcd6f45954f1f7d0603` | `be60815e5316b7b55f4a532afd2c93ae0308161459de2d093fdcf4e1ce2f7342` |
| mypy_check/types/unauthorized_cli | `d57d13f31566fc9ea2528f88741a69212985c0a062338fcd6f45954f1f7d0603` | `7f4210e1e498bf5f75c3757d68e75d1722a66f8b22126e75083d310b52b0a567` |
| mypy_check/types/unauthorized_config | `130ce42533a0d817499559f76f94d1bbcbaf9c5f65db5dc4572131f342beafb5` | `ae09ecd666c31dfebe4fa9d93a32b36427c323740c9b74df97d8eb5b70281c8d` |
| mypy_check/types/unauthorized_environment | `d57d13f31566fc9ea2528f88741a69212985c0a062338fcd6f45954f1f7d0603` | `abe474459901350f387cc9048703d2df6a7fbe34b65d281a0e3e8189a4b8a8b6` |
| mypy_check/types/native_default | `d57d13f31566fc9ea2528f88741a69212985c0a062338fcd6f45954f1f7d0603` | `9a5deba62f89c327b3b90771a68059cbbcacb8c453f66b316ca0579bb7a4edf8` |
| mypy_check/types/write_disabled | `d57d13f31566fc9ea2528f88741a69212985c0a062338fcd6f45954f1f7d0603` | `d57d13f31566fc9ea2528f88741a69212985c0a062338fcd6f45954f1f7d0603` |





### Archived probe source


**Content:**

The ephemeral Python script was scaffolded through pytest_integration_test and refined through safe_edit_file. It is ignored temporary material and is not a permanent regression suite. This archived source is the reproducible Research carrier. Its final filesystem byte SHA-256 is `4fc1bbde32af2b8684940326442adbd58aab0d85bad653f9a815da3242d4cf54`; Markdown newline presentation is not a promise of byte-identical extraction.

```python
# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=J4-Led_kGRhKPVHQ sf=9PfER5JkyAoFQLRi

"Owner-approved issue-474 Research effect probe. Successful runner completion is observation collection, not adapter conformance or repaired authority."

# Standard library
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

# Third party
import pytest





def test_record_isolated_native_write_effects(tmp_path: Path, pytestconfig: pytest.Config) -> None:
    "Record before/after effects through public bundled adapter entrypoints; never assert an existing defect as a passing regression requirement."
    repo = pytestconfig.rootpath
    entrypoints = {
        "ruff_check": repo / "mcp_server/bundled_adapters/ruff/check.py",
        "ruff_fix": repo / "mcp_server/bundled_adapters/ruff/fix.py",
        "mypy_check": repo / "mcp_server/bundled_adapters/mypy/check.py",
    }
    approved_root = repo / ".pgmcp/temp/issue469-effect-probe"
    assert tmp_path.resolve().is_relative_to(approved_root.resolve())

    def snapshot(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    cases = [
        (adapter, operation, source)
        for adapter, operations in (
            ("ruff_check", ("format", "lint")),
            ("ruff_fix", ("format", "lint")),
            ("mypy_check", ("types",)),
        )
        for operation in operations
        for source in ("allowed_cli", "unauthorized_cli", "unauthorized_config",
                       "unauthorized_environment", "native_default", "write_disabled")
    ]
    observations: list[dict[str, object]] = []
    for adapter, operation, option_source in cases:
        root = tmp_path / f"{adapter}-{operation}-{option_source}"
        root.mkdir()
        selected = root / "selected"
        selected.mkdir()
        target = selected / "source with spaces.py"
        decoy = selected / "unselected.py"
        initial = b"import os\n\nvalue=1\n" if adapter.startswith("ruff") else b"value: int = 1\n"
        target.write_bytes(initial)
        decoy.write_bytes(initial)
        cache_name = ".mypy_cache" if adapter == "mypy_check" else ".ruff_cache"
        allowed_cache = root / cache_name
        unauthorized_cache = root / "simulated-unauthorized-cache"
        destination = allowed_cache if option_source == "allowed_cli" else unauthorized_cache
        assert destination.resolve().is_relative_to(approved_root.resolve())
        config_text = (
            '[tool.mypy]\npython_version = "3.11"\n'
            if adapter == "mypy_check"
            else '[tool.ruff]\nline-length = 100\n[tool.ruff.lint]\nselect = ["F401"]\n'
        )
        if option_source == "unauthorized_config":
            config_text = config_text.replace(
                "[tool.ruff]\n" if adapter.startswith("ruff") else "[tool.mypy]\n",
                ("[tool.ruff]\ncache-dir = " if adapter.startswith("ruff")
                 else "[tool.mypy]\ncache_dir = ") + json.dumps(str(destination)) + "\n",
            )
        (root / "pyproject.toml").write_text(config_text, encoding="utf-8")
        environment = dict(os.environ)
        for variable in (
            "RUFF_CACHE_DIR", "RUFF_NO_CACHE", "RUFF_OUTPUT_FILE", "MYPY_CACHE_DIR",
        ):
            environment.pop(variable, None)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["TEMP"] = str(root)
        environment["TMP"] = str(root)
        args: list[str] = []
        if option_source in {"allowed_cli", "unauthorized_cli"}:
            args = ["--cache-dir", str(destination)]
        if option_source == "unauthorized_environment":
            environment["MYPY_CACHE_DIR" if adapter == "mypy_check" else "RUFF_CACHE_DIR"] = str(
                destination
            )
        if option_source == "write_disabled":
            args = ["--cache-dir", "nul"] if adapter == "mypy_check" else ["--no-cache"]
        before = snapshot(root)
        request = {"operation": operation, "targets": [str(target)], "args": args}
        result = subprocess.run(
            [sys.executable, str(entrypoints[adapter])],
            input=json.dumps(request).encode("utf-8"),
            cwd=root,
            env=environment,
            capture_output=True,
            check=False,
            timeout=45,
        )
        response = json.loads(result.stdout)
        assert isinstance(response, dict) and "decision" in response
        after = snapshot(root)
        created = sorted(set(after) - set(before))
        changed = sorted(name for name in before if after.get(name) != before[name])
        unauthorized_files = [
            name for name in created if name.startswith("simulated-unauthorized-cache/")
        ]
        allowed_files = [name for name in created if name.startswith(cache_name + "/")]
        assert decoy.read_bytes() == initial
        if adapter != "ruff_fix":
            assert target.read_bytes() == initial
        unexpected = [
            name for name in created
            if not name.startswith((cache_name + "/", "simulated-unauthorized-cache/"))
        ]
        assert not unexpected, unexpected
        row: dict[str, object] = {
            "adapter": adapter,
            "operation": operation,
            "option_source": option_source,
            "decision": response["decision"],
            "adapter_exit": result.returncode,
            "external_tools": response.get("external_tools"),
            "selected_source_changed": target.read_bytes() != initial,
            "unselected_source_changed": decoy.read_bytes() != initial,
            "created_file_count": len(created),
            "allowed_cache_files": len(allowed_files),
            "unauthorized_cache_files": len(unauthorized_files),
            "sample_created_files": created[:4],
            "changed_files": changed,
            "before_inventory_sha256": hashlib.sha256(
                json.dumps(before, sort_keys=True).encode("utf-8")
            ).hexdigest(),
            "after_inventory_sha256": hashlib.sha256(
                json.dumps(after, sort_keys=True).encode("utf-8")
            ).hexdigest(),
        }
        observations.append(row)
        print("EFFECT_OBSERVATION " + json.dumps(row, sort_keys=True), flush=True)
    assert len(observations) == len(cases)
    print("PROBE_COMPLETED " + str(len(observations)), flush=True)





def test_existing_output_write_routes_are_refused(tmp_path: Path, pytestconfig: pytest.Config) -> None:
    """Observe existing report-output refusal independently of cache-destination gaps."""
    repo = pytestconfig.rootpath
    approved_root = repo / ".pgmcp/temp/issue469-effect-probe"
    assert tmp_path.resolve().is_relative_to(approved_root.resolve())
    for adapter, operation in (
        ("ruff_check", "format"), ("ruff_check", "lint"),
        ("ruff_fix", "format"), ("ruff_fix", "lint"), ("mypy_check", "types"),
    ):
        root = tmp_path / f"refusal-{adapter}-{operation}"
        root.mkdir()
        target = root / "selected.py"
        target.write_bytes(b"value: int = 1\n")
        output = root / "simulated-unauthorized-report.xml"
        entrypoint = (
            repo / "mcp_server/bundled_adapters/mypy/check.py"
            if adapter == "mypy_check"
            else repo / "mcp_server/bundled_adapters/ruff" / (
                "fix.py" if adapter == "ruff_fix" else "check.py"
            )
        )
        (root / "pyproject.toml").write_text(
            '[tool.mypy]\npython_version = "3.11"\n[tool.ruff]\nline-length = 100\n',
            encoding="utf-8",
        )
        before = {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file()
        }
        option = "--junit-xml" if adapter == "mypy_check" else "--output-file"
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        for variable in ("RUFF_CACHE_DIR", "RUFF_NO_CACHE", "RUFF_OUTPUT_FILE", "MYPY_CACHE_DIR"):
            environment.pop(variable, None)
        request = {"operation": operation, "targets": [str(target)], "args": [option, str(output)]}
        result = subprocess.run(
            [sys.executable, str(entrypoint)],
            input=json.dumps(request).encode("utf-8"), cwd=root, env=environment,
            capture_output=True, check=False, timeout=30,
        )
        response = json.loads(result.stdout)
        after = {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file()
        }
        assert result.returncode == 3
        assert response["decision"]["status"] == "unavailable"
        assert response["decision"]["reason"] == "unsupported_input"
        assert before == after and not output.exists()
        print("REFUSAL_OBSERVATION " + json.dumps({
            "adapter": adapter, "operation": operation,
            "decision": response["decision"], "created_files": 0, "changed_files": 0,
        }, sort_keys=True), flush=True)
```







## Related Documents

- [Approved Research and strategy](<research.md>)
- [Ruff check entrypoint](<../../../mcp_server/bundled_adapters/ruff/check.py>)
- [Ruff fix entrypoint](<../../../mcp_server/bundled_adapters/ruff/fix.py>)
- [Mypy check entrypoint](<../../../mcp_server/bundled_adapters/mypy/check.py>)

