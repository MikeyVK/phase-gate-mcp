# mcp_server/utils/violation_parser.py
# template=generic version=f35abd82 created=2026-06-15T06:17:00Z
"""ViolationParser module.

Violation parser utility for linter and typechecker outputs.

@layer: Utility
@dependencies: [re, typing, mcp_server.schemas]
@responsibilities:
    - Parse text/regex based violations
    - Parse JSON based violations
    - Resolve JSON pointers and fields
"""

from __future__ import annotations

import logging
import re
from typing import Any

from mcp_server.schemas import (
    JsonViolationsParsing,
    TextViolationsParsing,
    ViolationDTO,
)

logger = logging.getLogger(__name__)


class ViolationParser:
    """Violation parser utility for linter and typechecker outputs."""

    @staticmethod
    def resolve_json_pointer(data: dict[str, object], pointer: str) -> object:
        """Resolve a JSON Pointer (RFC 6901) against parsed JSON data."""
        if pointer == "/":
            return data

        segments = pointer.lstrip("/").split("/")
        current: object = data
        for segment in segments:
            if isinstance(current, dict):
                current = current.get(segment)
            elif isinstance(current, list):
                try:
                    current = current[int(segment)]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return current

    @classmethod
    def parse_text_violations(
        cls,
        output: str,
        parsing: TextViolationsParsing,
        supports_autofix: bool = False,
    ) -> list[ViolationDTO]:
        """Parse line-based tool output into ViolationDTOs using a named-group regex."""
        pattern = re.compile(parsing.pattern)
        gate_fixable = parsing.fixable_when == "gate" and supports_autofix
        result: list[ViolationDTO] = []
        for raw_line in output.splitlines():
            m = pattern.search(raw_line)
            if m is None:
                continue
            groups = m.groupdict()
            safe_groups = {k: (v or "") for k, v in groups.items()}

            raw_line_num = cls.resolve_text_field("line", groups, safe_groups, parsing.defaults)
            raw_col_num = cls.resolve_text_field("col", groups, safe_groups, parsing.defaults)
            result.append(
                ViolationDTO(
                    file=(
                        cls.resolve_text_field("file", groups, safe_groups, parsing.defaults) or ""
                    ),
                    message=cls.resolve_text_field("message", groups, safe_groups, parsing.defaults)
                    or "",
                    line=int(raw_line_num) if raw_line_num is not None else None,
                    col=int(raw_col_num) if raw_col_num is not None else None,
                    rule=cls.resolve_text_field("rule", groups, safe_groups, parsing.defaults),
                    fixable=gate_fixable,
                    severity=cls.resolve_text_field(
                        "severity", groups, safe_groups, parsing.defaults
                    )
                    or parsing.severity_default,
                )
            )
        return result

    @staticmethod
    def resolve_text_field(
        field: str,
        groups: dict[str, str | None],
        safe_groups: dict[str, str],
        defaults: dict[str, str],
    ) -> str | None:
        """Return captured group value or an interpolated default for field."""
        val = groups.get(field)
        if val is not None:
            return val
        template = defaults.get(field)
        if template is None:
            return None
        try:
            return template.format_map(safe_groups) or None
        except KeyError:
            return None

    @staticmethod
    def extract_violations_array(
        payload: list[dict[str, Any]] | dict[str, Any],
        parsing: JsonViolationsParsing,
    ) -> list[dict[str, Any]]:
        """Extract the violations array from payload using parsing.violations_path."""
        if parsing.violations_path is None:
            return payload if isinstance(payload, list) else []

        current: Any = payload
        for segment in parsing.violations_path.split("."):
            if not isinstance(current, dict):
                return []
            current = current.get(segment)
            if current is None:
                return []

        return current if isinstance(current, list) else []

    @staticmethod
    def resolve_field_path(item: dict[str, Any], path: str) -> Any:  # noqa: ANN401
        """Resolve a field value from item using a flat or nested path."""
        if "/" not in path:
            return item.get(path)
        current: Any = item
        for segment in path.split("/"):
            if not isinstance(current, dict):
                return None
            current = current.get(segment)
        return current

    @classmethod
    def parse_json_violations(
        cls,
        payload: list[dict[str, Any]],
        parsing: JsonViolationsParsing,
    ) -> list[ViolationDTO]:
        """Map a root-array JSON payload to a list of ViolationDTOs."""
        result: list[ViolationDTO] = []
        resolve = cls.resolve_field_path
        fixable_key = parsing.fixable_when or parsing.field_map.get("fixable")
        for item in payload:
            fmap = parsing.field_map
            raw_line = resolve(item, fmap["line"]) if "line" in fmap else None
            line = (raw_line + parsing.line_offset) if isinstance(raw_line, int) else raw_line
            fixable_val = resolve(item, fixable_key) if fixable_key else None
            raw_msg = resolve(item, fmap["message"]) if "message" in fmap else None
            if isinstance(raw_msg, str):
                raw_msg = raw_msg.replace("\u00a0", " ").replace("\n", " — ").strip()
            result.append(
                ViolationDTO(
                    file=(resolve(item, fmap["file"]) or "") if "file" in fmap else "",
                    message=raw_msg or "",
                    line=line,
                    col=resolve(item, fmap["col"]) if "col" in fmap else None,
                    rule=resolve(item, fmap["rule"]) if "rule" in fmap else None,
                    fixable=bool(fixable_val),
                    severity=(resolve(item, fmap["severity"]) if "severity" in fmap else None),
                )
            )
        return result
