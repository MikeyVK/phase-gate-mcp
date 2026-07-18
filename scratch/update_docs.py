import os
import glob

docs_dir = r"c:\temp\pgmcp\docs"

targets = [
    r"manuals\README.md",
    r"manuals\architecture.md",
    r"manuals\architectural_diagrams\09_scaffolding_subsystem.md",
    r"manuals\architectural_diagrams\10_config_consumers.md",
    r"reference\MCP_TOOLS.md",
    r"reference\README.md",
    r"reference\TEMPLATE_LIBRARY_QUICK_REFERENCE.md",
    r"reference\TEMPLATE_LIBRARY_USAGE.md",
    r"reference\tools\scaffolding.md",
    r"development\schema-template-maintenance.md",
]

for target in targets:
    path = os.path.join(docs_dir, target)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    
    # 1. Global path replacements
    content = content.replace(".pgmcp/config/artifacts", ".pgmcp/templates/config")
    # if it explicitly mentioned artifacts.yaml without directory
    # wait, the diagram in schema-template-maintenance.md says Yaml[".pgmcp/config/artifacts/*.yaml"]
    # the replace above covers this.

    # 2. Add brief note on strict Version pairing in TEMPLATE_LIBRARY_USAGE.md
    if target.endswith("TEMPLATE_LIBRARY_USAGE.md") and "Strict Version Pairing" not in content:
        note = "\n\n## Strict Version Pairing\nTemplates and their configurations are strictly paired using Semantic Versioning. Every Jinja2 template MUST include a header like `{#- Version: X.Y.Z -#}` that exactly matches the `template_version` specified in its corresponding YAML configuration. A mismatch in the major version will cause a strict configuration error at startup.\n"
        content += note
        
    # 3. Update schema-template-maintenance.md to explain central validation
    if target.endswith("schema-template-maintenance.md") and "Strict Version Pairing" not in content:
        note = "\n\n## Strict Version Pairing\nConfiguration files loaded by `ConfigLoader` from `.pgmcp/templates/config/` must specify `template_version`. `ArtifactManager` centrally validates this version against the `{#- Version: X.Y.Z -#}` header in the corresponding Jinja2 template via `mcp_server/utils/versioning.py`.\n"
        content += note

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {target}")
    else:
        print(f"No changes for {target}")

print("Done.")
