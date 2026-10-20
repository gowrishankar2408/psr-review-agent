from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from src.tools.close_case import close_case as close_case_operation
from src.tools.get_case_details import get_case_details as get_case_details_operation
from src.tools.get_case_notes import get_case_notes as get_case_notes_operation
from src.tools.invoke_reasoning_agent import (
    invoke_reasoning_agent as invoke_reasoning_agent_operation,
)
from src.tools.parse_psr_notes import parse_psr_notes as parse_psr_notes_operation

mcp = MCPServer("PSR Review Agent")
print("Starting PSR Review Agent MCP server...")


@mcp.tool()
def get_case_details(case_id: str) -> Any:
    """Retrieve case details from the configured case-management API."""
    return get_case_details_operation(case_id)


@mcp.tool()
def get_case_notes(case_id: str) -> Any:
    """Retrieve notes for a case from the configured case-management API."""
    return get_case_notes_operation(case_id)


@mcp.tool()
def parse_psr_notes(notes: str) -> dict[str, object]:
    """Normalize PSR notes and split them into paragraphs."""
    return parse_psr_notes_operation(notes)


@mcp.tool()
def invoke_reasoning_agent(case_id: str, notes: str) -> Any:
    """Send case notes to the configured reasoning-agent API."""
    return invoke_reasoning_agent_operation(case_id, notes)


@mcp.tool()
def close_case(case_id: str, resolution_summary: str) -> Any:
    """Close a case through the configured case-management API."""
    return close_case_operation(case_id, resolution_summary)


if __name__ == "__main__":
    mcp.run()
