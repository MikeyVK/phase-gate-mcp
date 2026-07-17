# mcp_server\utils\template_parser.py
# template=generic version=f35abd82 created=2026-07-17T16:48z updated=
"""TemplateParser module.

Jinja2 template header parser

@layer: Utils
@dependencies: [mcp_server.core.exceptions]
@responsibilities:
    - Extract semantic version headers from Jinja2 templates
"""

# Standard library
import logging
from pathlib import Path
import re

# Third-party

# Project modules
from mcp_server.core.exceptions import ConfigError

logger = logging.getLogger(__name__)

# Pattern to extract version from Jinja2 comment e.g. {#- Version: 1.0.0 -#}
VERSION_HEADER_REGEX = re.compile(r"\{#-\s*Version:\s*([^\s}]+)\s*-#\}")
SEMVER_REGEX = re.compile(r"^\d+\.\d+\.\d+$")


def extract_template_version(template_path: Path) -> str:
    """Extract semantic version from Jinja2 template header.

    Raises:
        ConfigError: If version header is missing or format is invalid.
    """
    try:
        content = template_path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise ConfigError(f"Template file not found at '{template_path}': {e}") from e

    match = VERSION_HEADER_REGEX.search(content)
    if not match:
        raise ConfigError(f"Version header missing in template '{template_path.name}'.")

    version_str = match.group(1)
    if not SEMVER_REGEX.match(version_str):
        raise ConfigError(
            f"Invalid version format '{version_str}' in template '{template_path.name}'."
        )

    return version_str
