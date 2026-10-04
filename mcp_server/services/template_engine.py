"""Render selected templates through an injected Jinja environment.

@layer: Backend (Services)
@dependencies: [jinja2, re]
@responsibilities:
    - Render the selected template with caller context and server provenance
    - Provide generic name filters for authored Jinja sources
"""

import re
from collections.abc import Mapping
from typing import Any

from jinja2 import Environment, Template
from pydantic import JsonValue


class TemplateEngine:
    """Render catalog-selected Jinja templates from one admitted source snapshot."""

    def __init__(self, *, environment: Environment) -> None:
        self._env = environment
        register_template_filters(self._env)

    @property
    def env(self) -> Environment:
        """Return the injected environment without reading a filesystem root."""
        return self._env

    def get_template(self, template_name: str) -> Template:
        """Load a template by name.

        Args:
            template_name: Relative path to template (e.g., "concrete/dto.py.jinja2")

        Returns:
            Loaded Jinja2 Template object

        Raises:
            TemplateNotFound: If template does not exist
        """
        return self.env.get_template(template_name)

    def render(self, template_name: str, **kwargs: Any) -> str:  # noqa: ANN401
        """Render a template with variables.

        Args:
            template_name: Relative path to template
            **kwargs: Template context variables

        Returns:
            Rendered string output

        Raises:
            TemplateNotFound: If template does not exist
            Exception: If template rendering fails (missing variables, etc.)

        The injected environment determines the available templates.
        """
        template = self.get_template(template_name)
        return str(template.render(**kwargs))

    def render_context(self, template_name: str, context: Mapping[str, JsonValue]) -> str:
        """Render an explicit content/provenance envelope without transforming its values."""
        return str(self.get_template(template_name).render(context))


def _filter_pascalcase(value: str) -> str:
    """Convert string to PascalCase.

    Args:
        value: Input string (snake_case, kebab-case, or mixed)

    Returns:
        PascalCase string

    Example:
        >>> _filter_pascalcase("test_name")
        'TestName'
    """
    # Split on underscores, hyphens, and existing capitals
    words = re.split(r"[_\-]+", value)
    return "".join(word.capitalize() for word in words if word)


def _filter_snakecase(value: str) -> str:
    """Convert string to snake_case.

    Args:
        value: Input string (PascalCase, kebab-case, or mixed)

    Returns:
        snake_case string

    Example:
        >>> _filter_snakecase("TestName")
        'test_name'
    """
    # Insert underscore before capitals (except first)
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    # Insert underscore before capital sequences
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Replace hyphens with underscores
    s3 = s2.replace("-", "_")
    return s3.lower()


def _filter_kebabcase(value: str) -> str:
    """Convert string to kebab-case.

    Args:
        value: Input string (PascalCase, snake_case, or mixed)

    Returns:
        kebab-case string

    Example:
        >>> _filter_kebabcase("TestName")
        'test-name'
    """
    # Use snakecase logic, then replace underscores with hyphens
    snake = _filter_snakecase(value)
    return snake.replace("_", "-")


def _filter_validate_identifier(value: str) -> str:
    """Validate and return Python identifier.

    Args:
        value: String to validate as Python identifier

    Returns:
        Original value if valid identifier

    Raises:
        ValueError: If value is not a valid Python identifier

    Example:
        >>> _filter_validate_identifier("valid_name")
        'valid_name'
        >>> _filter_validate_identifier("123invalid")
        ValueError: Invalid Python identifier: 123invalid
    """
    if not value.isidentifier():
        raise ValueError(f"Invalid Python identifier: {value}")
    return value


def text_block(value: str) -> str:
    """Remove only blank edge lines and the final retained line terminator.

    Space/tab-only edge lines are padding. Retained indentation, trailing spaces
    on meaningful lines and internal line endings belong to the caller.
    """
    if not value.strip(" \t\r\n"):
        return ""
    without_leading = re.sub(r"\A(?:[ \t]*(?:\r\n|\r|\n))*", "", value)
    return re.sub(r"(?:(?:\r\n|\r|\n)[ \t]*)+\Z", "", without_leading)


def register_template_filters(environment: Environment) -> None:
    """Expose the same real filter vocabulary to admission and rendering."""
    environment.filters["pascalcase"] = _filter_pascalcase
    environment.filters["snakecase"] = _filter_snakecase
    environment.filters["kebabcase"] = _filter_kebabcase
    environment.filters["validate_identifier"] = _filter_validate_identifier
    environment.filters["text_block"] = text_block
