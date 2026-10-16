# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=TDVmp2pacKoBW_qk sf=KoFPQ3-cAAWFeesb

"""Resolve explicit GitHub configuration and a host-supplied environment token."""

from mcp_server.config.settings import GitHubSettings


def resolve_github_settings(
    configured: GitHubSettings,
    environment_token: str | None,
) -> GitHubSettings:
    """Prefer a nonempty host token without inferring any repository identity."""
    return GitHubSettings(
        owner=configured.owner,
        repo=configured.repo,
        project_number=configured.project_number,
        token=environment_token or configured.token,
    )
