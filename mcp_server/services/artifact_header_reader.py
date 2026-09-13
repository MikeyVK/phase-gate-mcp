# mcp_server/services/artifact_header_reader.py
# template=service version=5d5b489a created=2026-09-13T17:18Z updated=
"""Bounded first-line recognition of the canonical artifact provenance dialect."""

from __future__ import annotations

import re

from pydantic import ValidationError

from mcp_server.core.interfaces.artifact_header_reader import (
    HeaderReadResult,
    HeaderReadStatus,
)
from mcp_server.services.artifact_identity import ArtifactIdentity


class ArtifactHeaderReader:
    """Interpret original text without selecting a package or modifying content."""

    def read(self, content: str) -> HeaderReadResult:
        """Inspect at most the budget plus one BOM, CRLF and overflow character.

        A pgmcp: marker within that first-line prefix is header-like even when
        its surrounding frame is malformed. No body content is inspected.
        """
        prefix = content[:104]
        if prefix.startswith("\ufeff"):
            prefix = prefix[1:]
        line, newline, _ = prefix.partition("\n")
        if newline and line.endswith("\r"):
            line = line[:-1]
        if "pgmcp:" not in line:
            return HeaderReadResult(status=HeaderReadStatus.ABSENT, provenance=None)
        rejected = HeaderReadResult(status=HeaderReadStatus.INVALID, provenance=None)
        if len(line) > 100:
            return rejected
        if line.startswith("<!-- ") and line.endswith(" -->"):
            record = line[5:-4]
        elif line.startswith("// "):
            record = line[3:]
        elif line.startswith("# "):
            record = line[2:]
        else:
            return rejected
        match = re.fullmatch(r"pgmcp:v1 id=(\S+) pv=(\S+) pf=(\S+) sf=(\S+)", record)
        if match is None:
            return rejected
        template_id, version, package_fp, suite_fp = match.groups()
        try:
            provenance = ArtifactIdentity(id=template_id, pv=version, pf=package_fp, sf=suite_fp)
        except ValidationError:
            return rejected
        return HeaderReadResult(status=HeaderReadStatus.RECOGNIZED, provenance=provenance)
