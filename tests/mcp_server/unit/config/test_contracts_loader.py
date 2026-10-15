"""Public loader behavior for canonical workflow contract sources."""

from pathlib import Path

import pytest
import yaml

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.contracts_config import ContractsConfig
from mcp_server.core.exceptions import ConfigError


def _document() -> dict[str, object]:
    return {
        "version": "1.0.0",
        "merge_policy": {"pr_allowed_phase": "done", "branch_local_artifacts": {}},
        "workflows": {
            "sample": {
                "phases": {
                    "done": {
                        "order": 30,
                        "instructions": {"sub_role": "test", "phase_instructions": "Finish."},
                    },
                    "draft": {
                        "order": 10,
                        "instructions": {"sub_role": "test", "phase_instructions": "Draft."},
                        "exit_requires": {
                            "document": {"order": 10, "type": "file_exists", "file": "draft.md"}
                        },
                    },
                    "build": {
                        "order": 20,
                        "instructions": {"sub_role": "test", "phase_instructions": "Build."},
                    },
                }
            }
        },
    }


def _write(tmp_path: Path, document: dict[str, object]) -> Path:
    source = tmp_path / "contracts.yaml"
    source.write_text(yaml.safe_dump(document), encoding="utf-8")
    return source


def test_complete_explicit_source_preserves_order_and_check_payload(tmp_path: Path) -> None:
    source = _write(tmp_path, _document())
    contracts = ConfigLoader(tmp_path).load_contracts_config(config_path=source)
    assert isinstance(contracts, ContractsConfig)
    assert contracts.get_phases("sample") == ["draft", "build", "done"]
    check = contracts.workflows["sample"].get_phase("draft").exit_requires["document"]
    assert check.file == "draft.md"
    assert check.required is True


@pytest.mark.parametrize("content", ["bad: [", "[]", ""])
def test_invalid_source_is_rejected_without_rewriting(tmp_path: Path, content: str) -> None:
    source = tmp_path / "contracts.yaml"
    source.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load_contracts_config(config_path=source)
    assert source.read_text(encoding="utf-8") == content


def test_missing_explicit_source_reports_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load_contracts_config(config_path=tmp_path / "missing.yaml")


def test_source_terminal_contract_is_enforced(tmp_path: Path) -> None:
    document = _document()
    document["merge_policy"] = {"pr_allowed_phase": "elsewhere"}
    source = _write(tmp_path, document)
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load_contracts_config(config_path=source)
