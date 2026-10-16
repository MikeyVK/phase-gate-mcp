# pgmcp:v1 id=pytest_unit_test pv=1.0.0 pf=PbcHYV4rwlUcaINu sf=KoFPQ3-cAAWFeesb

"""Explicit configuration ranks govern sibling iteration."""

from typing import Annotated

import pytest
from pydantic import AfterValidator, BaseModel, ValidationError

from mcp_server.config.composition import compose_configuration
from mcp_server.config.ordering import OrderedConfigEntry, ordered_mapping


class _Entry(OrderedConfigEntry):
    value: str


class _Configuration(BaseModel):
    entries: Annotated[dict[str, _Entry], AfterValidator(ordered_mapping)]


def test_sorts_identified_entries_without_mutating_input() -> None:
    """Canonical identities and values survive sorting without input mutation."""
    later = _Entry(order=20, value="later")
    earlier = _Entry(order=-5, value="earlier")
    entries = {"later_guard": later, "earlier_guard": earlier}

    result = ordered_mapping(entries)

    assert list(result) == ["earlier_guard", "later_guard"]
    assert list(entries) == ["later_guard", "earlier_guard"]
    assert result["earlier_guard"] is earlier
    assert ordered_mapping({}) == {}


@pytest.mark.parametrize("rank", [None, True, "10", 1.5])
def test_rejects_noninteger_order(rank: object) -> None:
    """A declared rank is a strict integer; booleans are not ranks."""
    with pytest.raises(ValidationError):
        _Entry.model_validate({"order": rank, "value": "guard"})


def test_model_admission_rejects_missing_and_colliding_ranks() -> None:
    """Required ranks and unique sibling ranks fail before consumer iteration."""
    with pytest.raises(ValidationError):
        _Configuration.model_validate({"entries": {"guard": {"value": "missing"}}})

    with pytest.raises(ValidationError, match="Duplicate configuration order"):
        _Configuration.model_validate(
            {
                "entries": {
                    "first": {"order": 10, "value": "one"},
                    "second": {"order": 10, "value": "two"},
                }
            }
        )


def test_merged_entries_inherit_or_override_explicit_ranks() -> None:
    """Native merge inherits untouched ranks and admits a ranked addition."""
    merged = compose_configuration(
        {
            "entries": {
                "first": {"order": 10, "value": "one"},
                "second": {"order": 20, "value": "two"},
            }
        },
        {
            "entries": {
                "first": {"value": "changed"},
                "second": {"order": 5},
                "third": {"order": 15, "value": "three"},
            }
        },
    )

    result = _Configuration.model_validate(merged)
    assert list(result.entries) == ["second", "first", "third"]
    assert result.entries["first"].order == 10
    assert result.entries["first"].value == "changed"

    with pytest.raises(ValidationError):
        result.entries["first"].order = 100
