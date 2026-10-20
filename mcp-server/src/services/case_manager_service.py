from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class CaseManagerService:
    """HTTP adapter for the case-management system."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("CASE_MANAGER_API_URL", "").rstrip("/")
        self.api_token = os.environ.get("CASE_MANAGER_API_TOKEN")
        self.timeout = float(os.environ.get("CASE_MANAGER_API_TIMEOUT", "15"))

    def get_case_details(self, case_id: str) -> Any:
        return self._request("GET", f"/cases/{quote(case_id, safe='')}")

    def get_case_notes(self, case_id: str) -> Any:
        return self._request("GET", f"/cases/{quote(case_id, safe='')}/notes")

    def close_case(self, case_id: str, resolution_summary: str) -> Any:
        return self._request(
            "POST",
            f"/cases/{quote(case_id, safe='')}/close",
            {"resolution_summary": resolution_summary},
        )

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        if not self.base_url:
            raise RuntimeError("Set CASE_MANAGER_API_URL before calling case-management tools.")

        headers = {"Accept": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")

        request = Request(f"{self.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read()
        except HTTPError as error:
            raise RuntimeError(f"Case-management API returned HTTP {error.code}.") from error
        except URLError as error:
            raise RuntimeError("Could not reach the case-management API.") from error

        if not body:
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError as error:
            raise RuntimeError("Case-management API returned invalid JSON.") from error
