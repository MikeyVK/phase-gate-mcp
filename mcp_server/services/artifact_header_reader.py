# mcp_server/services/artifact_header_reader.py
# template=service version=5d5b489a created=2026-09-13T17:18Z updated=
"""Bounded recognition of canonical comment and JSON provenance carriers."""

from __future__ import annotations

import json
import re

from pydantic import ValidationError

from mcp_server.core.interfaces.artifact_header_reader import (
    HeaderReadResult,
    HeaderReadStatus,
)
from mcp_server.schemas.template_identity import ArtifactIdentity


class ArtifactHeaderReader:
    """Interpret original text without selecting a package or modifying content."""

    def read(self, content: str) -> HeaderReadResult:
        """Inspect a 100-character comment line or a 512-character JSON opening.

        The JSON route examines only its first root comment string. Existing
        comment framing retains BOM, CRLF and overflow lookahead.
        """
        json_prefix = content[:514].removeprefix("\ufeff")
        if json_prefix.lstrip(" \t\r\n").startswith("{"):
            return self._read_json(json_prefix[:512])
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
        return self._read_record(record)

    @staticmethod
    def _read_record(record: str) -> HeaderReadResult:
        rejected = HeaderReadResult(status=HeaderReadStatus.INVALID, provenance=None)
        match = re.fullmatch(r"pgmcp:v1 id=(\S+) pv=(\S+) pf=(\S+) sf=(\S+)", record)
        if match is None:
            return rejected
        template_id, version, package_fp, suite_fp = match.groups()
        try:
            provenance = ArtifactIdentity(id=template_id, pv=version, pf=package_fp, sf=suite_fp)
        except ValidationError:
            return rejected
        return HeaderReadResult(status=HeaderReadStatus.RECOGNIZED, provenance=provenance)

    def _read_json(self, prefix: str) -> HeaderReadResult:
        """Decode only the first root comment's bounded string token."""
        absent = HeaderReadResult(status=HeaderReadStatus.ABSENT, provenance=None)
        rejected = HeaderReadResult(status=HeaderReadStatus.INVALID, provenance=None)
        key = re.match(r'\A[ \t\r\n]*\{[ \t\r\n]*"\$comment"', prefix)
        if key is None:
            return absent
        value_prefix = prefix[key.end() :].lstrip(" \t\r\n")
        if not value_prefix.startswith(":"):
            return rejected if value_prefix.startswith('"pgmcp:') else absent
        value_prefix = value_prefix[1:].lstrip(" \t\r\n")
        if not value_prefix.startswith('"'):
            return absent
        try:
            record, end = json.JSONDecoder().raw_decode(value_prefix)
        except json.JSONDecodeError:
            # Only the first bounded token is eligible; never search later members.
            token = re.match(r'"(?:\\.|[^"\\])*', value_prefix)
            return rejected if token is not None and "pgmcp:" in token[0] else absent
        if not isinstance(record, str) or "pgmcp:" not in record:
            return absent
        following = value_prefix[end:].lstrip(" \t\r\n")
        if len(record) > 91 or not following or following[0] not in ",}":
            return rejected
        return self._read_record(record)
