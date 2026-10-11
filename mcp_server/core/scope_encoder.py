"""Commit-scope encoding through the shared configured grammar."""

from mcp_server.core.scope_contract import ScopeContract, ScopeFields


class ScopeEncoder:
    """Encode commit scopes without loading configuration."""

    def __init__(self, contract: ScopeContract) -> None:
        self._contract = contract

    def generate_scope(
        self,
        phase: str,
        sub_phase: str | None = None,
        cycle_number: int | None = None,
    ) -> str:
        """Validate semantic fields and return their canonical scope."""
        return self._contract.encode(ScopeFields(phase, cycle_number, sub_phase))
