"""Regression tests for label config freshness after the C_LOADER migration.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.config.loader, mcp_server.config.schemas
"""

import time
from pathlib import Path

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas import LabelConfig
from tests.mcp_server.test_support import get_default_server_root

_PGMCP_CONFIG = Path(__file__).resolve().parents[4] / get_default_server_root() / "config"


def _load_label_config(config_path: Path) -> LabelConfig:
    return ConfigLoader(_PGMCP_CONFIG).load_label_config(config_path=config_path)


class TestLabelConfigReloadBehavior:
    """Verify fresh loads reflect on-disk file changes."""

    def test_reloads_after_file_change(self, tmp_path: Path) -> None:
        config_file = tmp_path / "labels.yaml"
        config_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:feature\n"
                "    color: 1D76DB\n"
                "freeform_exceptions: []\n"
            ),
            encoding="utf-8",
        )

        config1 = _load_label_config(config_file)
        assert len(config1.labels) == 1

        time.sleep(0.01)
        config_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:feature\n"
                "    color: 1D76DB\n"
                "  label_2:\n"
                "    name: type:bug\n"
                "    color: D73A4A\n"
                "freeform_exceptions: []\n"
            ),
            encoding="utf-8",
        )

        config2 = _load_label_config(config_file)

        assert len(config2.labels) == 2
        assert config1 is not config2

    def test_reloads_label_patterns(self, tmp_path: Path) -> None:
        config_file = tmp_path / "labels.yaml"
        config_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:feature\n"
                "    color: 1D76DB\n"
                "freeform_exceptions: []\n"
            ),
            encoding="utf-8",
        )

        config1 = _load_label_config(config_file)
        assert not config1.label_patterns

        time.sleep(0.01)
        config_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:feature\n"
                "    color: 1D76DB\n"
                "freeform_exceptions: []\n"
                "label_patterns:\n"
                "  label_pattern_1:\n"
                "    pattern: ^parent:issue-\\d+$\n"
                "    description: Parent issue reference\n"
                "    color: EDEDED\n"
                "    example: parent:issue-18\n"
                "    order: 10\n"
            ),
            encoding="utf-8",
        )

        config2 = _load_label_config(config_file)

        assert len(config2.label_patterns) == 1
        assert config2.label_patterns["label_pattern_1"].example == "parent:issue-18"
        assert config1 is not config2

    def test_consecutive_loads_of_unchanged_file_are_equivalent(self, tmp_path: Path) -> None:
        config_file = tmp_path / "labels.yaml"
        config_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:feature\n"
                "    color: 1D76DB\n"
                "freeform_exceptions: []\n"
            ),
            encoding="utf-8",
        )

        config1 = _load_label_config(config_file)
        config2 = _load_label_config(config_file)

        assert config1 == config2

    def test_different_config_paths_remain_independent(self, tmp_path: Path) -> None:
        config1_file = tmp_path / "config1.yaml"
        config2_file = tmp_path / "config2.yaml"

        config1_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:feature\n"
                "    color: 1D76DB\n"
                "freeform_exceptions: []\n"
            ),
            encoding="utf-8",
        )
        config2_file.write_text(
            (
                "version: 1.0.0\n"
                "labels:\n"
                "  label_1:\n"
                "    name: type:bug\n"
                "    color: D73A4A\n"
                "  label_2:\n"
                "    name: priority:high\n"
                "    color: FF0000\n"
                "freeform_exceptions: []\n"
            ),
            encoding="utf-8",
        )

        cfg1 = _load_label_config(config1_file)
        cfg2 = _load_label_config(config2_file)

        assert len(cfg1.labels) == 1
        assert len(cfg2.labels) == 2
        assert cfg1 != cfg2
