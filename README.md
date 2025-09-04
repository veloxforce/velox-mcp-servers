# Velox MCP Servers

Centralized repository for all organizational MCP (Model Context Protocol) servers.

## Structure

```
velox-mcp-servers/
├── adr-server/           # ADR (Architecture Decision Records) server
│   ├── server.py         # FastMCP server implementation
│   └── fastmcp.json      # Dependencies and configuration
└── [future-servers]/     # Additional MCP servers
```

## Deployment

Each server uses FastMCP with UV virtual environment management:

```bash
# Navigate to server directory
cd adr-server/

# Run with UV (auto-installs dependencies from fastmcp.json)
uv run --with fastmcp fastmcp run server.py

# Inspect server (development/testing)
uv run --with fastmcp fastmcp inspect server.py
```

## Integration

Servers are designed to integrate with MetaMCP for centralized hosting and universal client access.

## ADR Server

Provides access to organizational Architecture Decision Records via GitHub API integration.

- **Repository**: veloxforce/velox-global-adrs
- **Dependencies**: requests, python-frontmatter
- **Resources**: ADR list, individual ADR content, metadata