# tests/mcp_server/unit/config/test_presentation_config.py
# template=unit_test version=3d15d309 created=2026-08-21T00:00Z updated=2026-08-21
"""Presentation configuration and startup alignment contract tests.

@layer: Tests (Unit)
@dependencies: [pytest, pydantic, presentation_config, text_presenter]
@responsibilities:
    - Verify frozen declarative presentation policy
    - Verify complete supported-catalog startup alignment
    - Verify generic ordered-sequence, collection, enum, and budget contracts
"""

from enum import StrEnum
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import BaseModel, ValidationError

from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.core.exceptions import ConfigError
from mcp_server.presenters.text_presenter import (
    TextPresenter,
    validate_presentation_alignment,
)


class _Status(StrEnum):
    AVAILABLE = "available"
    MISSING = "missing"


class _GrandChild(BaseModel):
    code: str


class _Child(BaseModel):
    name: str
    tags: tuple[str, ...]
    grandchildren: list[_GrandChild]


class _Output(BaseModel):
    title: str
    labels: list[str]
    codes: tuple[str, ...]
    children: list[_Child]
    status: _Status
    unsupported: set[str]


class _OtherOutput(BaseModel):
    value: str


def _global_config(max_bytes: int = 8_000) -> dict[str, Any]:
    return {
        "response_mode": "structured",
        "max_text_response_bytes": max_bytes,
        "formatting": {
            "none_value": "-",
            "inline_sequence_separator": ", ",
            "inline_sequence_omission_template": "… {omitted_count} more",
            "collection_omission_template": "- … {omitted_count} more {field}",
            "truncation_notice": "Output truncated; complete details are cached.",
            "cache_unavailable_truncation_notice": (
                "Output truncated; complete details are unavailable."
            ),
        },
        "next_instruction_texts": {
            "uri_reference": "View resource: pgmcp://cache/runs/{run_id}",
            "structured_reference": "Full structured result.",
            "attachment_reference": "See attached resources.",
            "delivery_failure_outcome": "Outcome={success}; result unavailable.",
            "cache_publication_failed": "Cache publication unavailable.",
            "operation_serialization_failed": "Operation serialization unavailable.",
            "diagnostic_excerpt_label": "Incomplete diagnostic excerpt:",
            "diagnostic_unavailable": "Diagnostic unavailable.",
            "response_processing_failed": "Operation success={success}; presentation failed.",
            "recovery_cache_unavailable": "No cached operation is available.",
            "processing_diagnostic_truncated": "Diagnostic details shortened.",
        },
    }


def _tool_config(**overrides: object) -> dict[str, object]:
    config: dict[str, object] = {"template_success": "{title}"}
    config.update(overrides)
    return config


def _presenter(
    tools: dict[str, dict[str, Any]],
    *,
    max_bytes: int = 8_000,
) -> TextPresenter:
    return TextPresenter(
        config_data={
            "global": _global_config(max_bytes),
            "tools": tools,
        }
    )


def _contracts() -> tuple[SupportedToolContract, ...]:
    return (
        SupportedToolContract(name="sample", output_model=_Output),
        SupportedToolContract(name="other", output_model=_OtherOutput),
    )


class TestPresentationConfig:
    """Frozen schema and cross-field policy behavior."""

    def test_loads_recursive_list_tuple_and_enum_policy_as_frozen_models(self) -> None:
        config = PresentationConfig.model_validate(
            {
                "global": _global_config(),
                "tools": {
                    "sample": _tool_config(
                        max_items=3,
                        template_success="{title}: {labels} / {codes}",
                        collections={
                            "entry_1": {
                                "order": 10,
                                "field": "children",
                                "heading": "Children",
                                "item_template": "- {name}: {tags}",
                                "children": {
                                    "entry_1": {
                                        "order": 10,
                                        "field": "grandchildren",
                                        "item_template": "  - {code}",
                                    }
                                },
                            }
                        },
                        enum_cases={
                            "entry_1": {
                                "order": 10,
                                "field": "status",
                                "cases": {"missing": "Missing: {title}"},
                            }
                        },
                    )
                },
            }
        )

        tool = config.tools["sample"]
        assert tool.max_items == 3
        assert tool.collections["entry_1"].children["entry_1"].field == "grandchildren"
        assert tool.enum_cases["entry_1"].cases == {"missing": "Missing: {title}"}
        with pytest.raises(ValidationError):
            tool.max_items = 4  # type: ignore[misc]

    @pytest.mark.parametrize(
        "formatting_update",
        [
            {"inline_sequence_omission_template": "{field}"},
            {"collection_omission_template": "{unknown}"},
            {"truncation_notice": "{run_id}"},
            {"cache_unavailable_truncation_notice": "{unknown}"},
        ],
    )
    def test_rejects_invalid_generic_formatting_placeholders(
        self,
        formatting_update: dict[str, str],
    ) -> None:
        global_config = _global_config()
        global_config["formatting"].update(formatting_update)

        with pytest.raises(ValidationError, match="placeholder"):
            PresentationConfig.model_validate({"global": global_config, "tools": {}})

    @pytest.mark.parametrize(
        ("key", "text"),
        [
            ("response_processing_failed", "{unknown}"),
            ("response_processing_failed", "{success.real}"),
            ("response_processing_failed", "{success[0]}"),
            ("response_processing_failed", "{success!r}"),
            ("response_processing_failed", "{success:>10}"),
            ("response_processing_failed", "{success"),
            ("recovery_cache_unavailable", "{success}"),
            ("processing_diagnostic_truncated", "{success}"),
        ],
    )
    def test_rejects_unsupported_recovery_placeholders(self, key: str, text: str) -> None:
        global_config = _global_config()
        global_config["next_instruction_texts"][key] = text

        with pytest.raises(ValidationError, match="placeholder"):
            PresentationConfig.model_validate({"global": global_config})

    @pytest.mark.parametrize(
        "key",
        [
            "response_processing_failed",
            "recovery_cache_unavailable",
            "processing_diagnostic_truncated",
        ],
    )
    @pytest.mark.parametrize("text", [None, " "])
    def test_requires_nonempty_recovery_notices(self, key: str, text: str | None) -> None:
        global_config = _global_config()
        if text is None:
            del global_config["next_instruction_texts"][key]
        else:
            global_config["next_instruction_texts"][key] = text

        with pytest.raises(ValidationError, match=key):
            PresentationConfig.model_validate({"global": global_config})

    def test_rejects_budget_that_cannot_hold_delivery_notices(self) -> None:
        with pytest.raises(ValidationError, match="configured notices"):
            PresentationConfig.model_validate({"global": _global_config(max_bytes=1)})


class TestPresentationAlignment:
    """Complete supported-catalog and recursive output-model alignment."""

    def test_accepts_complete_catalog_including_non_active_contract(self) -> None:
        presenter = _presenter(
            {
                "sample": _tool_config(),
                "other": {"template_success": "{value}"},
            }
        )

        validate_presentation_alignment(presenter, _contracts())

    @pytest.mark.parametrize(
        ("tools", "message"),
        [
            ({"sample": _tool_config()}, "other"),
            (
                {
                    "sample": _tool_config(),
                    "other": {"template_success": "{value}"},
                    "obsolete": {"template_success": "obsolete"},
                },
                "obsolete",
            ),
        ],
    )
    def test_rejects_missing_or_unknown_catalog_keys(
        self,
        tools: dict[str, dict[str, Any]],
        message: str,
    ) -> None:
        with pytest.raises(ConfigError, match=message):
            validate_presentation_alignment(_presenter(tools), _contracts())

    def test_rejects_duplicate_supported_identity(self) -> None:
        duplicate_contracts = (
            SupportedToolContract(name="sample", output_model=_Output),
            SupportedToolContract(name="sample", output_model=_OtherOutput),
        )

        with pytest.raises(ConfigError, match="Duplicate"):
            validate_presentation_alignment(
                _presenter({"sample": _tool_config()}),
                duplicate_contracts,
            )

    def test_validates_every_supported_model_even_when_not_active(self) -> None:
        presenter = _presenter(
            {
                "sample": _tool_config(),
                "other": {"template_success": "{missing_field}"},
            }
        )

        with pytest.raises(ConfigError, match="other"):
            validate_presentation_alignment(presenter, _contracts())

    def test_accepts_scalar_sequences_recursive_models_and_enum_cases(self) -> None:
        presenter = _presenter(
            {
                "sample": _tool_config(
                    max_items=2,
                    template_success="{title}: {labels} / {codes}",
                    collections={
                        "entry_1": {
                            "order": 10,
                            "field": "children",
                            "heading": "Children",
                            "item_template": "- {name}: {tags}",
                            "children": {
                                "entry_1": {
                                    "order": 10,
                                    "field": "grandchildren",
                                    "item_template": "  - {code}",
                                }
                            },
                        }
                    },
                    enum_cases={
                        "entry_1": {
                            "order": 10,
                            "field": "status",
                            "cases": {"missing": "Missing: {title}"},
                        }
                    },
                ),
                "other": {"template_success": "{value}"},
            }
        )

        validate_presentation_alignment(presenter, _contracts())

    @pytest.mark.parametrize(
        "sample_config",
        [
            _tool_config(template_success="{labels}"),
            _tool_config(max_items=2),
            _tool_config(
                max_items=2,
                collections={"entry_1": {"order": 10, "field": "title", "item_template": "{item}"}},
            ),
            _tool_config(
                max_items=2,
                collections={
                    "entry_1": {"order": 10, "field": "children.name", "item_template": "{item}"}
                },
            ),
            _tool_config(
                max_items=2,
                collections={
                    "entry_1": {"order": 10, "field": "children", "item_template": "{unknown}"}
                },
            ),
            _tool_config(max_items=2, template_success="{children}"),
            _tool_config(
                max_items=2,
                collections={
                    "entry_1": {"order": 10, "field": "unsupported", "item_template": "{item}"}
                },
            ),
            _tool_config(
                max_items=2,
                collections={
                    "entry_1": {
                        "order": 10,
                        "field": "labels",
                        "item_template": "{item}",
                        "children": {
                            "entry_1": {"order": 10, "field": "anything", "item_template": "{item}"}
                        },
                    }
                },
            ),
            _tool_config(
                enum_cases={
                    "entry_1": {
                        "order": 10,
                        "field": "status",
                        "cases": {"unknown": "Unknown: {title}"},
                    }
                }
            ),
        ],
    )
    def test_rejects_invalid_sequence_collection_and_enum_contracts(
        self,
        sample_config: dict[str, Any],
    ) -> None:
        presenter = _presenter(
            {
                "sample": sample_config,
                "other": {"template_success": "{value}"},
            }
        )

        with pytest.raises(ConfigError):
            validate_presentation_alignment(presenter, _contracts())


class TestResponseModes:
    """Two named local choices share immutable configured budgets."""

    def test_local_selection_does_not_mutate_shared_default(self) -> None:
        config = PresentationConfig.model_validate({"global": _global_config()})
        assert config.resolve_response_mode() == "structured"
        assert config.resolve_response_mode("resource") == "resource"
        assert config.resolve_response_mode() == "structured"
        with pytest.raises(ValidationError):
            config.global_settings.response_mode = "resource"  # type: ignore[misc]

    @pytest.mark.parametrize("mode", [None, "", "unknown"])
    def test_requires_an_explicit_valid_default(self, mode: str | None) -> None:
        data = _global_config()
        if mode is None:
            del data["response_mode"]
        else:
            data["response_mode"] = mode
        with pytest.raises(ValidationError, match="response_mode"):
            PresentationConfig.model_validate({"global": data})

    @pytest.mark.parametrize(
        "field",
        ["max_text_response_bytes", "max_cache_failure_detail_bytes", "cache_read_budget_chars"],
    )
    @pytest.mark.parametrize("value", [0, -1])
    def test_requires_positive_shared_budgets(self, field: str, value: int) -> None:
        data = _global_config()
        data[field] = value
        with pytest.raises(ValidationError, match=field):
            PresentationConfig.model_validate({"global": data})

    def test_existing_loader_composes_mode_and_budget_overrides(self, tmp_path: Path) -> None:
        defaults = tmp_path / "defaults"
        defaults.mkdir()
        (defaults / "presentation.yaml").write_text(
            yaml.safe_dump({"version": "2.0.0", "global": _global_config()}), encoding="utf-8"
        )
        (tmp_path / "presentation.yaml").write_text(
            yaml.safe_dump(
                {"global": {"response_mode": "resource", "max_text_response_bytes": 9000}}
            ),
            encoding="utf-8",
        )
        config = ConfigLoader(tmp_path).load_presentation_config()
        assert config.version == "2.0.0"
        assert config.resolve_response_mode() == "resource"
        assert config.global_settings.max_text_response_bytes == 9000
