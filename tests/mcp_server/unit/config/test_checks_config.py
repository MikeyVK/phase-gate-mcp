"""Closed check configuration and catalog-reference admission."""

from __future__ import annotations

from pathlib import Path

from mcp_server.config.loader import ConfigLoader
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
