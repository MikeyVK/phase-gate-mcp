# tests/mcp_server/unit/config/test_enforcement_config_schema.py
"""Unit tests for EnforcementRule schema — tool_category field and validator.

@layer: Tests (Unit)
@dependencies: [pytest, pydantic, mcp_server.config.schemas.enforcement_config]
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from mcp_server.config.schemas.enforcement_config import EnforcementAction, EnforcementRule


class TestEnforcementRuleToolCategory:
    """EnforcementRule.tool_category field and updated validate_target validator."""

    def test_rule_accepts_tool_category(self) -> None:
        rule = EnforcementRule(
            event_source="tool",
            timing="pre",
            tool_category="branch_mutating",
            actions=[],
        )
        assert rule.tool_category == "branch_mutating"

    def test_rule_with_tool_name_still_works(self) -> None:
        rule = EnforcementRule(
            event_source="tool",
            timing="pre",
            tool="submit_pr",
            actions=[],
        )
        assert rule.tool == "submit_pr"

    def test_neither_tool_nor_tool_category_raises(self) -> None:
        """event_source=tool requires tool OR tool_category."""
        with pytest.raises(ValidationError):
            EnforcementRule(event_source="tool", timing="pre", actions=[])

    def test_both_tool_and_tool_category_raises(self) -> None:
        """tool and tool_category are mutually exclusive."""
        with pytest.raises(ValidationError):
            EnforcementRule(
                event_source="tool",
                timing="pre",
                tool="submit_pr",
                tool_category="branch_mutating",
                actions=[],
            )

    def test_extra_fields_still_forbidden(self) -> None:
        with pytest.raises(ValidationError):
            EnforcementRule(
                event_source="tool",
                timing="pre",
                tool="submit_pr",
                unknown_field="x",
                actions=[],
            )


class TestEnforcementActionExemptTools:
    """EnforcementAction.exempt_tools field and model_validator."""

    def test_enforcement_action_exempt_tools_defaults_empty(self) -> None:
        action = EnforcementAction(type="check_branch_policy", rules={"bug": ["main"]})
        assert action.exempt_tools == []

    def test_enforcement_action_exempt_tools_accepted_on_check_context_loaded(
        self,
    ) -> None:
        action = EnforcementAction(type="check_context_loaded", exempt_tools=["create_branch"])
        assert action.exempt_tools == ["create_branch"]

    def test_enforcement_action_exempt_tools_accepted_on_check_pr_status(self) -> None:
        action = EnforcementAction(type="check_pr_status", exempt_tools=["create_branch"])
        assert action.exempt_tools == ["create_branch"]

    def test_enforcement_action_exempt_tools_accepted_on_check_phase_readiness(self) -> None:
        action = EnforcementAction(
            type="check_phase_readiness",
            policy="ready",
            exempt_tools=["create_branch"],
        )
        assert action.exempt_tools == ["create_branch"]

    def test_enforcement_action_enabled_defaults_true(self) -> None:
        action = EnforcementAction(type="check_context_loaded")
        assert action.enabled is True

    def test_enforcement_action_enabled_false_parses(self) -> None:
        action = EnforcementAction(type="check_context_loaded", enabled=False)
        assert action.enabled is False

    def test_enforcement_action_extra_fields_still_rejected(self) -> None:
        with pytest.raises(ValidationError):
            EnforcementAction(type="check_pr_status", unknown_field="x")
