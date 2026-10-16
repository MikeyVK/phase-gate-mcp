"""Public label behavior after composing identified defaults and workspace changes."""

from pathlib import Path

import yaml

from mcp_server.config.loader import ConfigLoader


def test_layered_labels_keep_inherited_metadata_and_order_patterns(tmp_path: Path) -> None:
    defaults = tmp_path / "defaults"
    defaults.mkdir()
    (defaults / "labels.yaml").write_text(
        yaml.safe_dump(
            {
                "version": "1.0.0",
                "labels": {
                    "task": {"name": "type:task", "color": "123456", "description": "Task"},
                },
                "label_patterns": {
                    "general": {
                        "order": 10,
                        "pattern": "^topic:",
                        "description": "General",
                        "color": "111111",
                    },
                    "specific": {
                        "order": 20,
                        "pattern": "^topic:special$",
                        "description": "Specific",
                        "color": "222222",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "labels.yaml").write_text(
        yaml.safe_dump(
            {
                "labels": {
                    "task": {"description": "Workspace task"},
                    "fix": {"name": "type:fix", "color": "654321"},
                },
                "label_patterns": {"specific": {"order": 5}},
            }
        ),
        encoding="utf-8",
    )

    config = ConfigLoader(tmp_path).load_label_config()

    inherited = config.get_label("type:task")
    assert inherited is not None
    assert (inherited.color, inherited.description) == ("123456", "Workspace task")
    assert config.label_exists("type:fix")
    assert list(config.label_patterns) == ["specific", "general"]
    assert config.validate_label_name("topic:special") == (True, "")
