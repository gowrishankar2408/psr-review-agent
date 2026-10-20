# PSR Review Agent

An MCP server scaffold for reviewing PSR case notes. The server exposes case lookup, note parsing, reasoning-agent invocation, and case closure tools.

## Run locally on Windows

From the repository root:

```powershell
py -3.11 -m venv mcp-server\.venv
.\mcp-server\.venv\Scripts\Activate.ps1
python -m pip install -r mcp-server\requirements.txt
$env:CASE_MANAGER_API_URL = "https://your-case-api.example"
$env:REASONING_AGENT_API_URL = "https://your-reasoning-agent.example/review"
python mcp-server\src\main.py
```

Set `CASE_MANAGER_API_TOKEN` and `REASONING_AGENT_API_TOKEN` when the corresponding APIs require bearer-token authentication. Do not commit credentials. The VS Code MCP server entry is in `.vscode/mcp.json`; open this repository as a folder to use it.

The API routes and request/response shapes are starter assumptions, not integrations with a particular case-management platform. See [docs/architecture.md](docs/architecture.md) before connecting production systems.

## Container

```powershell
docker build -t psr-review-agent:local mcp-server
docker run --rm -i `
  -e CASE_MANAGER_API_URL `
  -e CASE_MANAGER_API_TOKEN `
  -e REASONING_AGENT_API_URL `
  -e REASONING_AGENT_API_TOKEN `
  psr-review-agent:local
```

The GitHub Actions workflow builds the image on pushes and pull requests. Publishing to ECR is enabled on pushes to `main` after the AWS repository variables are configured; see the workflow notes in [docs/architecture.md](docs/architecture.md).
