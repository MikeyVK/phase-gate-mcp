# pgmcp:v1 id=python_class pv=1.0.0 pf=u_KOYBekCfsMbBaW sf=zJbLuUrs_I33kpX4

"""Pure YAML emission for admitted finite JSON-shaped template data."""

from collections.abc import Mapping

import yaml
from pydantic import JsonValue
from yaml.nodes import MappingNode, ScalarNode


class YamlDumper(yaml.SafeDumper):
    """Isolate template string representation from other PyYAML consumers."""


def _string_node(dumper: yaml.SafeDumper, value: str) -> ScalarNode:
    """Delegate escaping and chomping to PyYAML, preserving multiline values."""
    literal = "\n" in value and all(
        char == "\n" or (ord(char) >= 32 and char not in "\x85\u2028\u2029") for char in value
    )
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|" if literal else '"')


def _mapping_node(dumper: yaml.SafeDumper, value: dict[str, JsonValue]) -> MappingNode:
    """Quote string keys independently of multiline value representation."""
    node = dumper.represent_mapping("tag:yaml.org,2002:map", value)
    for key, _ in node.value:
        if isinstance(key, ScalarNode):
            key.style = '"'
    return node


YamlDumper.add_representer(str, _string_node)
YamlDumper.add_representer(dict, _mapping_node)


def yaml_text(value: Mapping[str, JsonValue]) -> str:
    """Emit admitted mapping values without IO or consumer-specific settings."""
    return yaml.dump(
        dict(value),
        Dumper=YamlDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        indent=2,
        line_break="\n",
    )
