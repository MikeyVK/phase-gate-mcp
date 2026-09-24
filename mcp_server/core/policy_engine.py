# mcp_server/core/policy_engine.py
"""Policy decision engine (config-driven).

Purpose: Make policy decisions based on YAML configs (Issue #54)
Responsibility: Single source of policy enforcement
Used by: MCP tools for operation validation
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mcp_server.config.loader import ConfigLoader
from mcp_server.schemas import GitConfig, OperationPoliciesConfig


@dataclass
class PolicyDecision:
    """Result of a policy decision."""

    allowed: bool
    reason: str
    operation: str
    path: str | None = None
    phase: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class PolicyEngine:
    """Policy decision engine (config-driven).

    Applies operation policies and configured commit conventions.
    """

    def __init__(
        self,
        config_root: Path | str,
        operation_config: OperationPoliciesConfig,
        git_config: GitConfig,
    ) -> None:
        """Initialize PolicyEngine with injected configs and explicit reload root."""
        self._config_root = Path(config_root)
        self._operation_config = operation_config
        self._git_config = git_config

        # Audit trail
        self._audit_trail: list[dict[str, Any]] = []

    def decide(
        self,
        operation: str,
        path: str | None = None,
        phase: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """Make policy decision for operation.

        Decision algorithm:
        1. Check operation-level phase policy.
        2. Apply operation-specific path checks when a path is provided.
        3. Check configured commit prefixes for commit operations.

        Args:
            operation: Operation ID (scaffold, create_file, commit)
            path: Optional file path (for path-based policies)
            phase: Optional workflow phase (for phase-based policies)
            context: Optional context data (e.g., commit message)

        Returns:
            PolicyDecision with allowed/denied + reason
        """
        context = context or {}

        try:
            # Get operation policy
            op_policy = self._operation_config.get_operation_policy(operation)

            # Check phase (if specified)
            if phase and not op_policy.is_allowed_in_phase(phase):
                decision = PolicyDecision(
                    allowed=False,
                    reason=f"Operation '{operation}' not allowed in phase '{phase}'. "
                    f"Allowed phases: {op_policy.allowed_phases or 'all'}",
                    operation=operation,
                    phase=phase,
                    context=context,
                )
                self._log_decision(decision)
                return decision

            # Check operation-specific path policies (if a path is provided).
            if path:
                # Check blocked patterns (create_file operation)
                if operation == "create_file" and op_policy.is_path_blocked(path):
                    decision = PolicyDecision(
                        allowed=False,
                        reason=f"Path '{path}' matches blocked pattern. "
                        "Must use scaffold operation instead.",
                        operation=operation,
                        path=path,
                        phase=phase,
                        context=context,
                    )
                    self._log_decision(decision)
                    return decision

                # Check allowed extensions (create_file operation)
                if operation == "create_file" and not op_policy.is_extension_allowed(path):
                    decision = PolicyDecision(
                        allowed=False,
                        reason=f"File extension not allowed. "
                        f"Allowed: {op_policy.allowed_extensions or 'all'}",
                        operation=operation,
                        path=path,
                        phase=phase,
                        context=context,
                    )
                    self._log_decision(decision)
                    return decision

            # Check commit message (commit operation)
            # Convention #6: Use GitConfig-derived prefixes instead of hardcoded list
            if operation == "commit" and op_policy.require_tdd_prefix:
                message = context.get("message", "")
                valid_prefixes = self._git_config.get_all_prefixes()

                if not any(message.startswith(prefix) for prefix in valid_prefixes):
                    decision = PolicyDecision(
                        allowed=False,
                        reason=f"Commit message must start with TDD prefix. "
                        f"Valid: {valid_prefixes}",
                        operation=operation,
                        phase=phase,
                        context=context,
                    )
                    self._log_decision(decision)
                    return decision

            # All checks passed - operation allowed
            decision = PolicyDecision(
                allowed=True,
                reason=f"Operation '{operation}' allowed in phase '{phase or 'any'}'"
                + (f" for path '{path}'" if path else ""),
                operation=operation,
                path=path,
                phase=phase,
                context=context,
            )
            self._log_decision(decision)
            return decision

        except Exception as e:
            # Error in policy evaluation - log and deny by default (fail-safe)
            decision = PolicyDecision(
                allowed=False,
                reason=f"Policy evaluation error: {e}",
                operation=operation,
                path=path,
                phase=phase,
                context=context,
            )
            self._log_decision(decision)
            return decision

    def _log_decision(self, decision: PolicyDecision) -> None:
        """Log decision to audit trail."""
        self._audit_trail.append(
            {
                "timestamp": decision.timestamp.isoformat(),
                "operation": decision.operation,
                "path": decision.path,
                "phase": decision.phase,
                "allowed": decision.allowed,
                "reason": decision.reason,
                "context": decision.context,
            }
        )

    def get_audit_trail(self) -> list[dict[str, Any]]:
        """Get complete audit trail.

        Returns:
            List of all policy decisions with metadata
        """
        return list(self._audit_trail)

    def reload_configs(self) -> None:
        """Reload configs from disk (without restart)."""
        loader = ConfigLoader(self._config_root)
        self._operation_config = loader.load_operation_policies_config()
        self._git_config = loader.load_git_config()
