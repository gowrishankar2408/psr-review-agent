from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ReasoningAgentService:
    """HTTP adapter for a separately deployed reasoning agent."""

    def __init__(self) -> None:
        self.endpoint = os.environ.get("REASONING_AGENT_API_URL", "")
        self.api_token = os.environ.get("REASONING_AGENT_API_TOKEN")
        self.timeout = float(os.environ.get("REASONING_AGENT_API_TIMEOUT", "60"))

    def invoke(self, case_id: str, notes: str) -> Any:
        if not self.endpoint:
            raise RuntimeError("Set REASONING_AGENT_API_URL before invoking the reasoning agent.")

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        body = json.dumps({"case_id": case_id, "notes": notes}).encode("utf-8")
        request = Request(self.endpoint, data=body, headers=headers, method="POST")

        try:
            with urlopen(request, timeout=self.timeout) as response:
                result = response.read()
        except HTTPError as error:
            raise RuntimeError(f"Reasoning agent returned HTTP {error.code}.") from error
        except URLError as error:
            raise RuntimeError("Could not reach the reasoning agent.") from error

        if not result:
            return {}
        try:
            return json.loads(result)
        except json.JSONDecodeError as error:
            raise RuntimeError("Reasoning agent returned invalid JSON.") from error
