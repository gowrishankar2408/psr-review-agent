# MCP server guidance

- Use the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and its [Python documentation](https://py.sdk.modelcontextprotocol.io/).
- Follow the SDK's [server setup](https://py.sdk.modelcontextprotocol.io/get-started/first-steps/) and [transport guidance](https://py.sdk.modelcontextprotocol.io/run/); local MCP hosts launch this server over stdio.
- Keep MCP tool registration in `mcp-server/src/main.py`, API operations in `tools/`, and external-system logic in `services/`.
- Do not put credentials in source, configuration committed to git, or logs.
