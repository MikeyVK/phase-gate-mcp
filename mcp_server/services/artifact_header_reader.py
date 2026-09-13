# mcp_server/services/artifact_header_reader.py
# template=service version=5d5b489a created=2026-09-13T17:18Z updated=
"""Bounded first-line recognition of the canonical artifact provenance dialect."""

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadResult


class ArtifactHeaderReader:
    """Interpret artifact text without selecting a package or modifying content."""

    def read(self, content: str) -> HeaderReadResult:
        """Recognize one complete first-line provenance record."""
        raise NotImplementedError
