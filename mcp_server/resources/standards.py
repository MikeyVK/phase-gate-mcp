"""Expose validated execution policy at the coding-standards resource URI."""

import json

from mcp_server.config.schemas import ChecksConfig, FixesConfig, TestsConfig
from mcp_server.resources.base import BaseResource


class StandardsResource(BaseResource):
    """Provide an immutable snapshot of configured check, test, and fix policies."""

    uri_pattern = "pgmcp://rules/coding_standards"
    description = "Project coding standards: configured check, test, and fix policies"

    def __init__(
        self,
        *,
        checks: ChecksConfig,
        tests: TestsConfig,
        fixes: FixesConfig,
    ) -> None:
        self._checks = checks
        self._tests = tests
        self._fixes = fixes

    async def read(self, uri: str) -> str:  # noqa: ARG002
        """Project configured policy facts, without claiming execution results."""
        policy = {
            "schema_version": 1,
            "run_checks": {
                "default_profile": self._checks.run_checks.default_profile,
                "profiles": {
                    profile_id: list(profile.checks)
                    for profile_id, profile in self._checks.profiles
                },
                "bindings": {
                    check_id: {
                        "adapter_id": binding.adapter_id,
                        "capability": binding.capability,
                    }
                    for check_id, binding in self._checks.checks
                },
            },
            "run_tests": {
                "bindings": {
                    test_id: {
                        "adapter_id": binding.adapter_id,
                        "capability": binding.capability,
                        "active": binding.active,
                    }
                    for test_id, binding in self._tests.tests
                }
            },
            "apply_fixes": {
                "bindings": {
                    fix_id: {
                        "adapter_id": binding.adapter_id,
                        "capability": binding.capability,
                    }
                    for fix_id, binding in self._fixes.fixes
                }
            },
        }
        return json.dumps(policy, indent=2)
