# Reference Documentation

## Overview

This directory contains templates, examples, and reference implementations for the Model Context Protocol (MCP) server. Use these as guides for configuring workflows, policies, templates, and tools.

## Key Reference Guides

### 📋 Model Context Protocol (MCP)
- **[MCP Tools Reference](mcp/MCP_TOOLS.md)**: Inventory of public MCP tools exposed by the server.
- **[Template Library Usage](mcp/TEMPLATE_LIBRARY_USAGE.md)**: Guidance on using `scaffold_artifact` and `scaffold_schema` to generate project files.
- **[Template Library Quick Reference](mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md)**: Quick lookup of enabled artifact types, templates, and schemas.
- **[Template Metadata Format](mcp/template_metadata_format.md)**: Specifications for writing metadata contracts inside Jinja2 templates.
- **[Validation API](mcp/validation_api.md)**: Overview of the layered validation and template validation systems.

### ⚙️ Server Configuration & Architecture
- **[Server Configuration](mcp/server-configuration.md)**: Configuration environment variables and YAML overlays.
- **[Config Loading Architecture](mcp/config-loading-architecture.md)**: Details on settings resolution and the bootstrapper lifecycle.
- **[MCP Vision Reference](mcp/mcp_vision_reference.md)**: Global design principles and architectural boundaries.
- **[Copilot Agent Instructions Model](mcp/copilot-agent-instructions-model.md)**: Orientation instructions and runtime context mapping.

## Directory Structure

```
docs/reference/
├── README.md                           # This file
└── mcp/
    ├── README.md                       # Scaffolding cluster index
    ├── MCP_TOOLS.md                    # Public tools catalog
    ├── TEMPLATE_LIBRARY_USAGE.md       # How to use scaffolding
    ├── TEMPLATE_LIBRARY_QUICK_REFERENCE.md # Artifact types list
    ├── server-configuration.md         # Env vars and yaml configs
    ├── config-loading-architecture.md  # Startup resolution
    ├── mcp_vision_reference.md         # Philosophy and limitations
    └── copilot-agent-instructions-model.md # Agent instruction mappings
```
