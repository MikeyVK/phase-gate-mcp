"""Closed check configuration and catalog-reference admission."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import (
    CheckAddress,
    CheckCapability,
    FixCapability,
)
from mcp_server.config.schemas.adapter_manifest import (
    TestCapability as NativeTestCapability,
)
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.execution.catalog import AdapterCatalog
from tests.mcp_server.fixtures.suite_roots import write_package_tree

VALID_CHECKS = """checks:
  first:
    adapter_id: fixture
    capability: dual
    timeout_seconds: 30
    default_args: ["--literal", "", "a b"]
  second:
    adapter_id: fixture
    capability: content
    timeout_seconds: 10
    default_args: []
profiles:
  preflight:
    checks: [second, first]
  explicit:
    checks: [first]
profiles_by_extension:
  ".py": preflight
run_checks:
  default_profile: explicit
"""


def test_explicit_loader_keeps_order_and_exact_empty_or_nonempty_defaults(tmp_path: Path) -> None:
    root = write_package_tree(tmp_path / "config", {"checks.yaml": VALID_CHECKS.encode()})
    config = ConfigLoader(root, tmp_path / "templates").load_checks_config()
    assert tuple(dict(config.checks)) == ("first", "second")
    assert dict(config.checks)["first"].default_args == ("--literal", "", "a b")
    assert dict(config.checks)["second"].default_args == ()
    assert dict(config.profiles)["preflight"].checks == ("second", "first")
    assert config.run_checks.default_profile == "explicit"
    assert config.model_dump(mode="json")["profiles_by_extension"] == {".py": "preflight"}


def load_text(root: Path, text: str) -> ChecksConfig:
    directory = write_package_tree(root, {"checks.yaml": text.encode()})
    return ConfigLoader(directory, root / "templates").load_checks_config()


def catalog() -> AdapterCatalog:
    """Real role-separated catalog; missing executables are allowed at admission."""
    identity = AdapterPackageIdentity("fixture", "1.0.0", "fixture_snapshot")
    launch = AdapterLaunch(None, ())
    return AdapterCatalog(
        checks=(
            AdapterBinding(
                identity,
                "dual",
                1,
                launch,
                CheckCapability(inputs=("content", "selection"), requires_file=False),
            ),
            AdapterBinding(
                identity,
                "content",
                1,
                launch,
                CheckCapability(inputs=("content",), requires_file=True),
            ),
            AdapterBinding(
                identity,
                "selection",
                1,
                launch,
                CheckCapability(inputs=("selection",)),
            ),
        ),
        tests=(AdapterBinding(identity, "test_only", 1, launch, NativeTestCapability()),),
        fixes=(
            AdapterBinding(
                identity,
                "fix_only",
                1,
                launch,
                FixCapability(addresses=(CheckAddress(adapter_id="fixture", capability="dual"),)),
            ),
        ),
    )


def test_nested_immutable_configuration_retains_known_defaults_without_native_probe(
    tmp_path: Path,
) -> None:
    config = load_text(tmp_path / "config", VALID_CHECKS)
    ConfigValidator().validate_checks_config(
        config, catalog(), template_profiles=frozenset({"preflight"})
    )
    assert ChecksConfig.model_validate_json(config.model_dump_json()) == config
    binding = dict(config.checks)["first"]
    with pytest.raises(ValidationError, match="frozen"):
        binding.timeout_seconds = 1
    assert isinstance(config.checks, tuple)
    assert isinstance(dict(config.profiles)["preflight"].checks, tuple)
    assert config.run_checks.default_profile == "explicit"


@pytest.mark.parametrize(
    "original,replacement",
    [
        ("timeout_seconds: 30", "timeout_seconds: true"),
        ("timeout_seconds: 30", "timeout_seconds: 0"),
        ('default_args: ["--literal", "", "a b"]', "default_args: [17]"),
        ("    default_args: []\n", ""),
        ("    default_args: []", "    default_args: null"),
        ("    default_args: []", "    default_args: []\n    command: [shell]"),
        ("checks: [second, first]", "checks: []"),
        ("checks: [second, first]", "checks: [first, first]"),
        ("checks: [second, first]", "checks: [missing]"),
        ('".py": preflight', '".py": missing'),
        ("default_profile: explicit", "default_profile: missing"),
        ("default_profile: explicit", "default_profile: null"),
        ('".py": preflight', '".py": preflight\n  ".PY": preflight'),
        ('".py": preflight', '".p*": preflight'),
        ("checks:\n  first:", "gates:\n  first:"),
    ],
)
def test_closed_yaml_rejects_invalid_obligations_and_legacy_fields(
    tmp_path: Path, original: str, replacement: str
) -> None:
    with pytest.raises(ConfigError):
        load_text(tmp_path / "config", VALID_CHECKS.replace(original, replacement, 1))


@pytest.mark.parametrize(
    "text",
    [
        VALID_CHECKS.replace("timeout_seconds: 30", "timeout_seconds: 30\n    timeout_seconds: 20"),
        VALID_CHECKS + "run_checks: {}\n",
        "checks: {1: {}}\nprofiles: {}\nprofiles_by_extension: {}\nrun_checks: {}\n",
        "checks: []\nprofiles: {}\nprofiles_by_extension: {}\nrun_checks: {}\n",
        "checks: [\n",
    ],
)
def test_yaml_mapping_admission_rejects_duplicate_or_non_object_keys(
    tmp_path: Path, text: str
) -> None:
    with pytest.raises(ConfigError):
        load_text(tmp_path / "config", text)


def test_empty_config_is_explicit_and_missing_file_never_loads_legacy_quality(
    tmp_path: Path,
) -> None:
    config = load_text(
        tmp_path / "empty",
        "checks: {}\nprofiles: {}\nprofiles_by_extension: {}\nrun_checks: {}\n",
    )
    assert config.checks == config.profiles == config.profiles_by_extension == ()
    assert config.run_checks.default_profile is None
    ConfigValidator().validate_checks_config(config, catalog(), template_profiles=frozenset())
    root = write_package_tree(tmp_path / "legacy", {"quality.yaml": b"gates: {}"})
    with pytest.raises(ConfigError, match="checks.yaml"):
        ConfigLoader(root, tmp_path / "templates").load_checks_config()


@pytest.mark.parametrize("capability", ["missing", "test_only", "fix_only"])
def test_reference_cannot_fall_back_to_unknown_or_other_roles(
    tmp_path: Path, capability: str
) -> None:
    config = load_text(
        tmp_path / "config", VALID_CHECKS.replace("capability: dual", f"capability: {capability}")
    )
    with pytest.raises(ConfigError, match="adapter_capability_unavailable"):
        ConfigValidator().validate_checks_config(config, catalog(), template_profiles=frozenset())


def test_consumer_references_require_the_declared_content_or_selection_input(
    tmp_path: Path,
) -> None:
    validator = ConfigValidator()
    config = load_text(tmp_path / "valid", VALID_CHECKS)
    with pytest.raises(ConfigError, match="check_profile_unknown"):
        validator.validate_checks_config(
            config, catalog(), template_profiles=frozenset({"missing"})
        )

    default_content = load_text(
        tmp_path / "default_content",
        VALID_CHECKS.replace("default_profile: explicit", "default_profile: preflight"),
    )
    with pytest.raises(ConfigError, match="selection"):
        validator.validate_checks_config(default_content, catalog(), template_profiles=frozenset())

    selection_only = load_text(
        tmp_path / "selection_only",
        VALID_CHECKS.replace("capability: content", "capability: selection"),
    )
    with pytest.raises(ConfigError, match="content"):
        validator.validate_checks_config(selection_only, catalog(), template_profiles=frozenset())

    run_only = load_text(
        tmp_path / "run_only",
        VALID_CHECKS.replace("capability: content", "capability: selection").replace(
            'profiles_by_extension:\n  ".py": preflight', "profiles_by_extension: {}"
        ),
    )
    validator.validate_checks_config(run_only, catalog(), template_profiles=frozenset())
    with pytest.raises(ConfigError, match="content"):
        validator.validate_checks_config(
            run_only, catalog(), template_profiles=frozenset({"preflight"})
        )


def test_extension_lookup_is_longest_case_insensitive_and_requires_a_filename_stem(
    tmp_path: Path,
) -> None:
    mapping = '".ts": explicit\n  ".d.ts": preflight\n  ".md": explicit\n  ".gitignore": explicit'
    text = VALID_CHECKS.replace('".py": preflight', mapping)
    normal = load_text(tmp_path / "normal", text)
    reverse = load_text(
        tmp_path / "reverse",
        VALID_CHECKS.replace('".py": preflight', "\n  ".join(reversed(mapping.split("\n  ")))),
    )
    expected = {
        "orders.d.ts": "preflight",
        "orders.D.TS": "preflight",
        "orders.ts": "explicit",
        "README.MD": "explicit",
        "Dockerfile": None,
        ".gitignore": None,
        "unknown.py": None,
    }
    for filename, profile in expected.items():
        assert normal.profile_for_filename(filename) == profile
        assert reverse.profile_for_filename(filename) == profile
