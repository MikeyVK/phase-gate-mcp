# tests/mcp_server/unit/execution/test_catalog.py
# template=unit_test version=8825c0bb created=2026-09-13T19:16Z updated=
"""Adapter admission through real configuration readers and isolated package files."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.core.exceptions import ConfigError
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from tests.mcp_server.fixtures.suite_roots import write_package_tree


MANIFEST = """adapter_id: sample
version: 1.2.3-alpha.1+build.456
files: [check.ps1, requirements.txt]
roles:
  check:
    contract_version: 1
    entrypoint:
      executable: pwsh
      args: ["-File", {package_file: check.ps1}, "", "a b"]
    capabilities:
      syntax: {inputs: [content, selection], requires_file: false}
  test:
    contract_version: 1
    entrypoint: {executable: missing_program, args: []}
    capabilities: {suite: {}}
  fix:
    contract_version: 1
    entrypoint: {executable: pwsh, args: [{package_file: check.ps1}]}
    capabilities:
      repair:
        addresses: [{adapter_id: sample, capability: syntax}]
"""


def package(root: Path, name: str = "directory label", manifest: str = MANIFEST) -> Path:
    """Create exactly the declared synthetic package, without executable test helpers."""
    return write_package_tree(
        root / name,
        {
            "manifest.yaml": manifest.encode(),
            "check.ps1": b"# package script\r\n",
            "requirements.txt": b"runtime contribution\n",
        },
    )


def catalog_loader(
    root: Path, trusted: tuple[str, ...] = ()
) -> AdapterCatalogLoader:
    """Inject actual config/file readers and an explicit startup program selection."""
    config = ConfigLoader(root / "config", root / "templates")
    return AdapterCatalogLoader(
        root / "official",
        root / "workspace",
        AdapterTrustConfig(trusted_adapter_ids=trusted),
        read_manifest=config.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: root / "bin" / "pwsh.exe" if name == "pwsh" else None,
        windows=True,
    )


def test_real_loader_preserves_descriptors_and_catalog_identity(tmp_path: Path) -> None:
    directory = package(tmp_path / "official")
    catalog = catalog_loader(tmp_path).load()
    binding = catalog.get_check("sample", "syntax")
    assert binding.identity.version == "1.2.3-alpha.1+build.456"
    assert binding.launch.executable == tmp_path / "bin" / "pwsh.exe"
    assert binding.launch.args == ("-File", str(directory / "check.ps1"), "", "a b")
    assert binding.capability.inputs == ("content", "selection")
    assert catalog.get_test("sample", "suite").launch.executable is None
    assert catalog.get_fix("sample", "repair").capability.addresses[0].capability == "syntax"
    manifest = ConfigLoader(tmp_path / "config", tmp_path / "templates").load_adapter_manifest(
        directory / "manifest.yaml"
    )
    assert manifest.roles.check is not None
    assert isinstance(manifest.roles.check.capabilities, tuple)
    assert isinstance(manifest.roles.check.entrypoint.args, tuple)
    with pytest.raises(ValidationError):
        manifest.version = "2.0.0"


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("adapter_id: sample", "adapter_id: Sample"),
        ("version: 1.2.3-alpha.1+build.456", "version: 01.2.3"),
        ("contract_version: 1", "contract_version: true"),
        ('executable: pwsh', 'executable: ./pwsh'),
        ('args: ["-File", {package_file: check.ps1}, "", "a b"]', "args: [42]"),
        ("requires_file: false", "requires_file: null"),
        ("inputs: [content, selection], requires_file: false", "inputs: [selection], requires_file: false"),
        ("capabilities: {suite: {}}", "capabilities: {suite: {options_schema: x}}"),
        ("files: [check.ps1, requirements.txt]", "files: [check.ps1, check.ps1]"),
        ("adapter_id: sample", "adapter_id: sample\ntrusted: true"),
        ("capabilities: {suite: {}}", "capabilities: {suite: {}, suite: {}}"),
    ],
)
def test_invalid_manifest_is_rejected_by_config_loader(
    tmp_path: Path, old: str, new: str
) -> None:
    directory = package(tmp_path / "official", manifest=MANIFEST.replace(old, new, 1))
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path / "config", tmp_path / "templates").load_adapter_manifest(
            directory / "manifest.yaml"
        )


@pytest.mark.parametrize("reference", ["../outside", "missing.ps1", "folder", "undeclared.ps1"])
def test_package_file_admission_is_shared_by_reference_positions(
    tmp_path: Path, reference: str
) -> None:
    # The executable and argument use the same reference contract; each is exercised.
    manifest = MANIFEST.replace("executable: pwsh", f"executable: {{package_file: {reference}}}", 1)
    directory = package(tmp_path / "official", manifest=manifest)
    write_package_tree(directory, {"undeclared.ps1": b"not inventoried"})
    (directory / "folder").mkdir()
    with pytest.raises(ConfigError):
        catalog_loader(tmp_path).load()
    manifest_path = directory / "manifest.yaml"
    manifest_path.write_text(MANIFEST.replace("package_file: check.ps1", f"package_file: {reference}", 1))
    with pytest.raises(ConfigError):
        catalog_loader(tmp_path).load()


def test_resolved_escape_and_windows_batch_are_rejected(tmp_path: Path) -> None:
    directory = package(tmp_path / "official")
    outside = write_package_tree(tmp_path / "outside", {"check.ps1": b"outside"})
    reader = FileAdapterPackageReader()
    with pytest.raises(ConfigError):
        reader.resolve_file(directory, "../outside/check.ps1")
    # Deterministic injected resolution represents an escaping link without OS link privileges.
    class EscapingReader(FileAdapterPackageReader):
        def resolve_file(self, root: Path, relative: str) -> Path:
            return outside / "check.ps1"

    config = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    with pytest.raises(ConfigError):
        AdapterCatalogLoader(
            tmp_path / "official", tmp_path / "workspace",
            AdapterTrustConfig(trusted_adapter_ids=()),
            read_manifest=config.load_adapter_manifest, files=EscapingReader(),
            resolve_program=lambda _: tmp_path / "bin" / "tool.CMD", windows=True,
        ).load()
    directory.joinpath("manifest.yaml").write_text(
        MANIFEST.replace("executable: pwsh", "executable: {package_file: tool.CMD}", 1)
        .replace("files: [check.ps1, requirements.txt]", "files: [check.ps1, requirements.txt, tool.CMD]")
    )
    directory.joinpath("tool.CMD").write_bytes(b"exit /b 0")
    with pytest.raises(ConfigError, match="batch"):
        catalog_loader(tmp_path).load()


def test_trust_reference_and_duplicate_admission(tmp_path: Path) -> None:
    package(tmp_path / "workspace")
    assert catalog_loader(tmp_path).load().checks == ()
    with pytest.raises(ConfigError):
        catalog_loader(tmp_path).load().get_check("sample", "syntax")
    assert len(catalog_loader(tmp_path, ("sample",)).load().checks) == 1
    package(tmp_path / "official")
    with pytest.raises(ConfigError, match="duplicate"):
        catalog_loader(tmp_path, ("sample",)).load()


@pytest.mark.parametrize("text", [None, "trusted_adapter_ids: null", "trusted_adapter_ids: [sample, sample]"])
def test_invalid_or_missing_trust_has_no_fallback(tmp_path: Path, text: str | None) -> None:
    if text is not None:
        write_package_tree(tmp_path / "custom_config", {"adapters.yaml": text.encode()})
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path / "custom_config", tmp_path / "templates").load_adapter_trust()


def test_empty_and_explicit_trust_from_selected_config_root(tmp_path: Path) -> None:
    config_root = write_package_tree(tmp_path / "selected", {"adapters.yaml": b"trusted_adapter_ids: []"})
    loader = ConfigLoader(config_root, tmp_path / "templates")
    assert loader.load_adapter_trust().trusted_adapter_ids == ()
    config_root.joinpath("adapters.yaml").write_text("trusted_adapter_ids: [sample]")
    assert loader.load_adapter_trust().trusted_adapter_ids == ("sample",)


def test_missing_check_address_rejects_complete_catalog(tmp_path: Path) -> None:
    package(tmp_path / "official", manifest=MANIFEST.replace("capability: syntax", "capability: unknown"))
    with pytest.raises(ConfigError):
        catalog_loader(tmp_path).load()


def test_fingerprint_matches_independent_records_and_moves_with_package(tmp_path: Path) -> None:
    directory = package(tmp_path / "official")
    first = catalog_loader(tmp_path).load().get_check("sample", "syntax").identity.fingerprint
    canonical = json.dumps(yaml.safe_load(MANIFEST), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    records = [b"pgmcp:adapter-package:v1", canonical]
    for name in ["check.ps1", "requirements.txt"]:
        records.extend([name.encode(), (directory / name).read_bytes()])
    framed = b"".join(len(record).to_bytes(8, "big") + record for record in records)
    expected = base64.urlsafe_b64encode(hashlib.sha256(framed).digest()[:12]).decode().rstrip("=")
    assert first == expected
    moved = tmp_path / "moved"
    package(moved / "official", name="another directory")
    assert catalog_loader(moved).load().get_check("sample", "syntax").identity.fingerprint == first
    directory.joinpath("unrelated.cache").write_bytes(b"ignored")
    assert catalog_loader(tmp_path).load().get_check("sample", "syntax").identity.fingerprint == first
    directory.joinpath("check.ps1").write_bytes(b"# changed")
    assert catalog_loader(tmp_path).load().get_check("sample", "syntax").identity.fingerprint != first
