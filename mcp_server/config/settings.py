# mcp_server/config/settings.py
"""
Configuration settings for the MCP server.

Defines runtime settings loaded from environment variables and optional YAML
overrides for server and logging configuration.

@layer: Backend (Config)
@dependencies: [importlib.metadata, os, pathlib, pydantic, yaml]
@responsibilities:
    - Define typed settings models for MCP server runtime configuration
    - Load settings from environment variables with YAML overlay support
    - Resolve server version metadata from installed package information
"""

# Standard library
import os
from importlib import metadata
from pathlib import Path
from typing import Any

# Third-party
import yaml
from pydantic import BaseModel, ConfigDict, Field, computed_field


class LogSettings(BaseModel):
    """Logging configuration settings."""

    level: str = "INFO"
    audit_log: str | None = None


class ServerSettings(BaseModel):
    """Server configuration settings."""

    model_config = ConfigDict(extra="forbid")

    name: str = "phase-gate-mcp"
    workspace_root: str = Field(default_factory=os.getcwd)
    config_root: str | None = None
    template_root: str | None = None
    server_root_dir: str = ".pgmcp"
    logs_dir: str = "logs"
    bypass_version_check: bool = Field(
        default_factory=lambda: bool(os.environ.get("PYTEST_CURRENT_TEST"))
    )

    @property
    def resolved_server_root(self) -> Path:
        return Path(self.workspace_root) / self.server_root_dir

    @property
    def resolved_config_root(self) -> Path:
        if self.config_root:
            return Path(self.config_root)
        return self.resolved_server_root / "config"

    @property
    def resolved_template_root(self) -> Path:
        if self.template_root:
            return Path(self.template_root)
        return self.resolved_server_root / "template_suite"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def version(self) -> str:
        """Resolve server version from installed package metadata (read-only)."""
        return metadata.version("phase-gate-mcp")


class GitHubSettings(BaseModel):
    """Pure GitHub integration configuration shared by runtime consumers."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True, hide_input_in_errors=True)

    owner: str | None = None
    repo: str | None = None
    project_number: int | None = None
    token: str | None = Field(default=None, validate_default=True, repr=False)


class Settings(BaseModel):
    """Launcher settings for server and logging configuration."""

    model_config = ConfigDict(extra="forbid")

    server: ServerSettings = Field(default_factory=ServerSettings)
    logging: LogSettings = Field(default_factory=LogSettings)

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from env vars with optional PGMCP_CONFIG_PATH overlay."""
        config_data: dict[str, Any] = {}

        path_value = os.environ.get("PGMCP_CONFIG_PATH")
        if path_value:
            path = Path(path_value)
            if path.exists():
                with path.open(encoding="utf-8") as file_handle:
                    config_data = yaml.safe_load(file_handle) or {}
        server_data = config_data.setdefault("server", {})
        logging_data = config_data.setdefault("logging", {})

        if env_name := os.environ.get("PGMCP_SERVER_NAME"):
            server_data["name"] = env_name
        if env_workspace_root := os.environ.get("PGMCP_WORKSPACE_ROOT"):
            server_data["workspace_root"] = env_workspace_root
        if env_project_dir := os.environ.get("PGMCP_SERVER_PROJECT_DIR"):
            server_data["server_root_dir"] = env_project_dir
        if env_logs_dir := os.environ.get("PGMCP_LOGS_DIR"):
            server_data["logs_dir"] = env_logs_dir
        if env_config_root := os.environ.get("PGMCP_CONFIG_ROOT"):
            server_data["config_root"] = env_config_root
        if env_template_root := os.environ.get("PGMCP_TEMPLATE_ROOT"):
            server_data["template_root"] = env_template_root
        if env_bypass_version_check := os.environ.get("PGMCP_BYPASS_VERSION_CHECK"):
            server_data["bypass_version_check"] = env_bypass_version_check.lower() in (
                "true",
                "1",
                "t",
                "y",
                "yes",
            )

        if env_log_level := os.environ.get("LOG_LEVEL"):
            logging_data["level"] = env_log_level

        return cls(**config_data)
