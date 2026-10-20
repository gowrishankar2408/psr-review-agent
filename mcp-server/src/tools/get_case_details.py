from __future__ import annotations

from typing import Any

from src.services.case_manager_service import CaseManagerService


def get_case_details(case_id: str) -> Any:
    """Fetch the case record for a case identifier."""
    return CaseManagerService().get_case_details(case_id)
