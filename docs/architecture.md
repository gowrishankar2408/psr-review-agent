# Architecture

## Components

- `mcp-server/src/main.py` registers the five MCP tools and serves them over stdio.
- `tools/` contains small MCP-facing operations; `services/` owns external API calls.
- `CaseManagerService` connects to the case-management API. The starter assumes `GET /cases/{case_id}`, `GET /cases/{case_id}/notes`, and `POST /cases/{case_id}/close` with a `resolution_summary` JSON field.
- `ReasoningAgentService` sends `case_id` and `notes` as JSON to `REASONING_AGENT_API_URL` using HTTP POST.
- `parse_psr_notes` only normalizes whitespace and splits paragraphs. No PSR-specific note schema was supplied, so it deliberately does not infer fields or findings.

## Configuration

| Variable | Purpose |
| --- | --- |
| `CASE_MANAGER_API_URL` | Base URL for the case-management API |
| `CASE_MANAGER_API_TOKEN` | Optional bearer token for that API |
| `CASE_MANAGER_API_TIMEOUT` | Request timeout in seconds; defaults to 15 |
| `REASONING_AGENT_API_URL` | Full reasoning-agent HTTP endpoint |
| `REASONING_AGENT_API_TOKEN` | Optional bearer token for that endpoint |
| `REASONING_AGENT_API_TIMEOUT` | Request timeout in seconds; defaults to 60 |

All API calls expect JSON responses. Adapt endpoint paths, authentication, payloads, and response handling to the target systems before deployment. Case closure is a consequential write operation and should be protected by the production system's authorization, audit, and confirmation controls.

## Deployment

The Docker image starts the MCP server on stdio, appropriate for a local MCP host. The GitHub Actions workflow validates/builds the image on pull requests and pushes. On pushes to `main`, it publishes to ECR only when repository variables `AWS_ROLE_ARN`, `AWS_REGION`, and `ECR_REPOSITORY` are set. Configure the AWS role for GitHub Actions OIDC and ensure the ECR repository already exists. This workflow publishes an image; it does not deploy to ECS, EKS, or another runtime because no target runtime was specified.

The `infrastructure/terraform` directory is reserved for the chosen AWS runtime and its resources; no account-specific infrastructure is generated in this scaffold.

## MCP SDK

This project uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and follows its [server](https://py.sdk.modelcontextprotocol.io/get-started/first-steps/) and [stdio run](https://py.sdk.modelcontextprotocol.io/run/) guidance.
