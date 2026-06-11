import os
from mcp_server.config.settings import Settings
from mcp_server.adapters.github_adapter import GitHubAdapter

def main():
    settings = Settings.from_env()
    adapter = GitHubAdapter(settings)
    issue = adapter.get_issue(397)
    print("BODY_START")
    print(issue.body)
    print("BODY_END")

if __name__ == "__main__":
    main()
