# mcp_server\utils\versioning.py
# template=generic version=f35abd82 created=2026-07-17T16:41Z updated=
"""SemVerValidator module.

Centralized semantic versioning parser and validator

@layer: Utils
@dependencies: [mcp_server.core.exceptions]
@responsibilities:
    - Parse SemVer strings
    - Validate template and configuration version compatibility
"""

# Standard library
from dataclasses import dataclass
import logging
import re

# Third-party

# Project modules
from mcp_server.core.exceptions import ConfigError

logger = logging.getLogger(__name__)

# Strict SemVer regex (e.g. 1.0.0, 10.2.3, no prefix, no prerelease)
VERSION_REGEX = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, version_string: str) -> "SemVer":
        """Parse a version string into a SemVer object.

        Raises:
            ConfigError: If the version string format is invalid.
        """
        if not VERSION_REGEX.match(version_string):
            raise ConfigError(
                f"Invalid version format: '{version_string}'. Must match strict X.Y.Z."
            )
        parts = version_string.split(".")
        return cls(
            major=int(parts[0]),
            minor=int(parts[1]),
            patch=int(parts[2]),
        )


def validate_compatibility(expected_version: str, actual_version: str, context: str) -> None:
    """Validate version compatibility between an expected and actual version.

    Rules:
    - MAJOR mismatch: Raise ConfigError (breaking change)
    - MINOR mismatch (actual > expected): Log a warning (forward incompatibility)
    - MINOR mismatch (actual <= expected): Accept silently
    - PATCH mismatch: Accept silently

    Raises:
        ConfigError: On MAJOR version mismatch or invalid version strings.
    """
    expected = SemVer.parse(expected_version)
    actual = SemVer.parse(actual_version)

    if actual.major != expected.major:
        raise ConfigError(
            f"MAJOR version mismatch for {context}: "
            f"expected {expected_version}, got {actual_version}."
        )
    if actual.minor > expected.minor:
        logger.warning(
            "MINOR version mismatch for %s (forward-incompatible): "
            "engine expected %s, asset has newer version %s. "
            "Some features might not be supported.",
            context,
            expected_version,
            actual_version,
        )
