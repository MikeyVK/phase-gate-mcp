"""Schema utilities for normalizing JSON Schema structures."""

import copy
from typing import Any, cast


def resolve_schema_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """Inline all $ref references in a JSON Schema.

    This ensures the schema can be transmitted to MCP clients that don't handle
    $ref indirection or nested $defs. See issue #99 C9: VS Code Copilot Chat
    cannot construct tool calls if input_schema contains $ref.

    Args:
        schema: JSON Schema dict (typically from model_json_schema())

    Returns:
        Normalized schema with all $ref resolved and $defs removed
    """
    schema = copy.deepcopy(schema)
    defs: dict[str, Any] = schema.pop("$defs", {})

    def _resolve(node: Any) -> Any:  # noqa: ANN401
        if isinstance(node, dict):
            if "$ref" in node:
                ref_path: str = node["$ref"]
                def_name = ref_path.rsplit("/", maxsplit=1)[-1]
                resolved = copy.deepcopy(defs.get(def_name, {}))
                for key, value in node.items():
                    if key != "$ref":
                        resolved[key] = value
                return _resolve(resolved)
            return {key: _resolve(value) for key, value in node.items()}
        if isinstance(node, list):
            return [_resolve(item) for item in node]
        return node

    return cast(dict[str, Any], _resolve(schema))
