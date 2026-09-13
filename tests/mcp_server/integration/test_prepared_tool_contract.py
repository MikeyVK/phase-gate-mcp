# tests/mcp_server/integration/test_prepared_tool_contract.py
# template=integration_test version=c2e61372 created=2026-09-13T17:49Z updated=
"""Prepared input preserves the schema authority of an existing real tool model."""

from dataclasses import FrozenInstanceError

import pytest
from pydantic import ValidationError

from mcp_server.core.interfaces.template_catalog import freeze_json, thaw_json
from mcp_server.core.interfaces.tool_input_contract import prepare_model_input
from mcp_server.tools.project_tools import GetProjectPlanInput


def test_prepared_schema_is_a_detached_immutable_snapshot() -> None:
    contract = prepare_model_input(GetProjectPlanInput)
    exposed = thaw_json(contract.schema)
    assert isinstance(exposed, dict)
    exposed.clear()
    assert "properties" in contract.schema
    with pytest.raises(FrozenInstanceError):
        contract.schema = freeze_json({})


def test_prepared_existing_model_enforces_its_exposed_input_type() -> None:
    contract = prepare_model_input(GetProjectPlanInput)
    with pytest.raises(ValidationError):
        contract.validate({"issue_number": "460"})
    assert contract.validate({"issue_number": 460}).issue_number == 460
    # Static legacy admission remains unchanged when no prepared contract is supplied.
    assert GetProjectPlanInput.model_validate({"issue_number": "460"}).issue_number == 460
