"""Remaining legacy commit tests pending CY051 migration.

Issue/PR behavior is covered by the delivered-package integration tests.

@layer: Tests (Unit)
@dependencies: pytest, jinja2, pathlib, mcp_server.scaffolding.templates
"""

import pytest
from jinja2 import Environment, FileSystemLoader

from tests.mcp_server.test_support import get_template_root

TEMPLATES_DIR = get_template_root()


@pytest.fixture
def jinja_env() -> Environment:
    """Create Jinja2 environment with templates loader."""
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def test_tier1_base_tracking_exists() -> None:
    """tier1_base_tracking.jinja2 must exist."""
    template_path = TEMPLATES_DIR / "tier1_base_tracking.jinja2"
    assert template_path.exists(), "tier1_base_tracking.jinja2 not found"


def test_tier2_tracking_text_exists() -> None:
    """tier2_tracking_text.jinja2 must exist."""
    template_path = TEMPLATES_DIR / "tier2_tracking_text.jinja2"
    assert template_path.exists(), "tier2_tracking_text.jinja2 not found"


def test_concrete_commit_txt_exists() -> None:
    """concrete/commit.txt.jinja2 must exist."""
    template_path = TEMPLATES_DIR / "concrete" / "commit.txt.jinja2"
    assert template_path.exists(), "concrete/commit.txt.jinja2 not found"


def test_commit_txt_renders_conventional_commits_format(jinja_env: Environment) -> None:
    """Test commit.txt renders Conventional Commits format."""
    template = jinja_env.get_template("concrete/commit.txt.jinja2")

    context = {
        "tracking_type": "commit",
        "type": "feat",
        "scope": "tracking",
        "message": "add tracking templates",
        "body": "Implements tier1_base_tracking + tier2 text/markdown + 3 concrete templates.",
        "refs": ["#72"],
    }

    output = template.render(**context)

    # Verify Conventional Commits format
    assert "feat(tracking): add tracking templates" in output
    assert "Implements tier1_base_tracking" in output
    assert "Refs: #72" in output


def test_commit_txt_renders_breaking_change(jinja_env: Environment) -> None:
    """Test commit.txt renders BREAKING CHANGE footer."""
    template = jinja_env.get_template("concrete/commit.txt.jinja2")

    context = {
        "tracking_type": "commit",
        "type": "feat",
        "message": "change API signature",
        "breaking_change": True,
        "breaking_description": "Removed deprecated parameter from public API",
    }

    output = template.render(**context)

    # Verify breaking change marker
    assert "feat!: change API signature" in output
    assert "BREAKING CHANGE: Removed deprecated parameter" in output


def test_commit_txt_minimal_context(jinja_env: Environment) -> None:
    """Test commit.txt renders with minimal required fields."""
    template = jinja_env.get_template("concrete/commit.txt.jinja2")

    context = {
        "tracking_type": "commit",
        "type": "fix",
        "message": "resolve bug",
    }

    output = template.render(**context)

    assert "fix: resolve bug" in output
    # Should not have optional sections
    assert "Refs:" not in output
    assert "BREAKING CHANGE:" not in output


def test_tier1_extends_tier0() -> None:
    """Verify tier1_base_tracking extends tier0_base_artifact."""
    template_source = (TEMPLATES_DIR / "tier1_base_tracking.jinja2").read_text(encoding="utf-8")
    assert '{%- extends "tier0_base_artifact.jinja2" -%}' in template_source


def test_tier2_text_extends_tier1() -> None:
    """Verify tier2_tracking_text extends tier1_base_tracking."""
    template_source = (TEMPLATES_DIR / "tier2_tracking_text.jinja2").read_text(encoding="utf-8")
    assert '{%- extends "tier1_base_tracking.jinja2" -%}' in template_source


def test_commit_extends_tier2_text() -> None:
    """Verify concrete/commit.txt extends tier2_tracking_text."""
    template_source = (TEMPLATES_DIR / "concrete" / "commit.txt.jinja2").read_text(encoding="utf-8")
    assert '{%- extends "tier2_tracking_text.jinja2" -%}' in template_source
