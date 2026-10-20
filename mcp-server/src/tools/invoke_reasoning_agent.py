from __future__ import annotations

from typing import Any

from src.services.reasoning_agent_service import ReasoningAgentService


def invoke_reasoning_agent(case_id: str, notes: str) -> Any:
    """Submit case notes to the configured reasoning-agent endpoint."""
    return ReasoningAgentService().invoke(case_id, notes)
