"""Unit tests for the injected-environment TemplateEngine contract."""

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined, TemplateNotFound, UndefinedError

from mcp_server.services.template_engine import TemplateEngine


@pytest.fixture
def engine() -> TemplateEngine:
    """Provide an engine backed only by an explicitly supplied environment."""
    environment = Environment(
        loader=DictLoader(
            {
                "selected": "{{ artifact_type }}|{{ version_hash }}",
                "content": "{{ content.flag }}|{{ content.count }}",
            }
        ),
        undefined=StrictUndefined,
    )
    return TemplateEngine(environment=environment)


def test_renders_named_template_from_injected_environment(engine: TemplateEngine) -> None:
    output = engine.render("selected", artifact_type="test", version_hash="abc123")
    assert output == "test|abc123"


def test_render_context_preserves_explicit_values(engine: TemplateEngine) -> None:
    assert engine.render_context("content", {"content": {"flag": False, "count": 0}}) == "False|0"


def test_raises_on_missing_template(engine: TemplateEngine) -> None:
    with pytest.raises(TemplateNotFound, match="missing/template.jinja2"):
        engine.render("missing/template.jinja2")


@pytest.mark.parametrize(
    ("filter_name", "value", "expected"),
    [
        ("pascalcase", "test_name", "TestName"),
        ("snakecase", "TestName", "test_name"),
        ("kebabcase", "TestName", "test-name"),
    ],
)
def test_custom_case_filters(
    engine: TemplateEngine,
    filter_name: str,
    value: str,
    expected: str,
) -> None:
    template = engine.env.from_string("{{ value | " + filter_name + " }}")
    assert template.render(value=value) == expected


def test_validate_identifier_filter_rejects_invalid_identifier(
    engine: TemplateEngine,
) -> None:
    template = engine.env.from_string("{{ value | validate_identifier }}")
    assert template.render(value="valid_name") == "valid_name"
    with pytest.raises((ValueError, UndefinedError)):
        template.render(value="123invalid")


def test_missing_variable_raises_under_strict_undefined(
    engine: TemplateEngine,
) -> None:
    template = engine.env.from_string("{{ required_var.field }}")
    with pytest.raises(UndefinedError):
        template.render()
