"""Public contract tests for the configured standards resource."""

import json

import pytest

from mcp_server.config.schemas import ChecksConfig, FixesConfig, TestsConfig
from mcp_server.resources.standards import StandardsResource


def resource() -> StandardsResource:
    """Inject a small validated policy snapshot with active and inactive entries."""
    checks = ChecksConfig.model_validate(
        {
            "checks": {
                "lint": {
                    "adapter_id": "ruff",
                    "capability": "lint",
                    "timeout_seconds": 30,
                    "default_args": [],
                },
                "format": {
                    "adapter_id": "ruff",
                    "capability": "format",
                    "timeout_seconds": 30,
                    "default_args": [],
                },
            },
            "profiles": {"review": {"checks": ["lint", "format"]}},
            "profiles_by_extension": {".py": "review"},
            "run_checks": {"default_profile": "review"},
        }
    )
    tests = TestsConfig.model_validate(
        {
            "tests": {
                "unit": {
                    "adapter_id": "pytest",
                    "capability": "tests",
                    "timeout_seconds": 60,
                    "default_args": [],
                    "active": True,
                },
                "optional": {
                    "adapter_id": "pytest",
                    "capability": "tests",
                    "timeout_seconds": 60,
                    "default_args": [],
                    "active": False,
                },
            }
        }
    )
    fixes = FixesConfig.model_validate(
        {
            "fixes": {
                "format": {
                    "adapter_id": "ruff",
                    "capability": "format",
                    "timeout_seconds": 30,
                    "default_args": [],
                }
            }
        }
    )
    return StandardsResource(checks=checks, tests=tests, fixes=fixes)


@pytest.mark.asyncio
async def test_standards_resource_projects_validated_policy_without_legacy_gates() -> None:
    policy = json.loads(await resource().read("pgmcp://rules/coding_standards"))
    assert policy == {
        "schema_version": 1,
        "run_checks": {
            "default_profile": "review",
            "profiles": {"review": ["lint", "format"]},
            "bindings": {
                "lint": {"adapter_id": "ruff", "capability": "lint"},
                "format": {"adapter_id": "ruff", "capability": "format"},
            },
        },
        "run_tests": {
            "bindings": {
                "unit": {"adapter_id": "pytest", "capability": "tests", "active": True},
                "optional": {"adapter_id": "pytest", "capability": "tests", "active": False},
            }
        },
        "apply_fixes": {"bindings": {"format": {"adapter_id": "ruff", "capability": "format"}}},
    }


def test_standards_resource_keeps_public_uri_and_description() -> None:
    configured = resource()
    assert configured.matches("pgmcp://rules/coding_standards")
    assert not configured.matches("pgmcp://rules/other")
    assert "coding standards" in configured.description
