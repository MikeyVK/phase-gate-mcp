# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=TDVmp2pacKoBW_qk sf=KoFPQ3-cAAWFeesb

"""Validate and order identified configuration objects without IO."""

from collections.abc import Mapping
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StrictInt, StringConstraints

ConfigId = Annotated[str, StringConstraints(strict=True, min_length=1)]


class OrderedConfigEntry(BaseModel):
    """A configuration object with an explicit sibling execution rank."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    order: StrictInt


def ordered_mapping[Entry: OrderedConfigEntry](entries: Mapping[str, Entry]) -> dict[str, Entry]:
    """Reject ambiguous ranks and return objects in explicit execution order."""
    ranks: set[int] = set()
    for entry in entries.values():
        if entry.order in ranks:
            raise ValueError(f"Duplicate configuration order: {entry.order}")
        ranks.add(entry.order)
    return dict(sorted(entries.items(), key=lambda item: item[1].order))
