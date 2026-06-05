# temp\validation_scaffold\i_example_interface.py
# template=interface version=3fb28c28 created=2026-06-05T08:50Z updated=
"""IExampleInterface module.

Live validation scaffold — interface template structure check

@layer: Backend (Contracts)
"""

# Standard library
from typing import Protocol

# Third-party

# Project modules


class IExampleInterface(Protocol):
    """Live validation scaffold — interface template structure check"""

    def fetch(self, key: str) -> object:
        """Fetch data by key."""
        ...

    def store(self, key: str, value: object) -> None:
        """Persist data."""
        ...
