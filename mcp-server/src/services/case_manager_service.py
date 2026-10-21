from __future__ import annotations
from dotenv import load_dotenv
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

load_dotenv()

class CaseManagerService:
    """HTTP adapter for the case-management system."""

    def __init__(self) -> None:
        print("Initializing CaseManagerService...")
        self.host_name = os.getenv("hostName")
        self.entry_point = os.getenv("entryPoint")
        self.endpoint = os.getenv("endpoint")
        self.clientID = os.getenv("clientid")
        self.clientSecret = os.getenv("clientsecret")
        self.timeout = 10  # seconds

    def get_case_details(self, case_id: str) -> Any:
        notesURL = self.host_name + self.entry_point + self.endpoint.format(caseNumber=case_id) + 'notes'
        return self._request("GET", notesURL)

    def get_case_notes(self, case_id: str) -> Any:
        notesURL = self.host_name + self.entry_point + self.endpoint.format(caseNumber=case_id) + 'notes'
        return self._request("GET", notesURL)

    def close_case(self, case_id: str, resolution_summary: str) -> Any:
        return self._request(
            "POST",
            f"/cases/{quote(case_id, safe='')}/close",
            {"resolution_summary": resolution_summary},
        )

    def _request(self, method: str, path: str | None = None) -> Any:
        if not self.host_name or not self.entry_point or not self.endpoint:
            raise RuntimeError("Set CASE_MANAGER_API_URL before calling case-management tools.")

        headers={"client_id": self.clientID, "client_secret": self.clientSecret }

        request = Request(path, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read()
                #print(f"Received response from case-management API: {body.decode('utf-8')}")
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
