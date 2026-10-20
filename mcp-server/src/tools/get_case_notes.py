from __future__ import annotations

from typing import Any

from src.services.case_manager_service import CaseManagerService


def get_case_notes(case_id: str) -> Any:
    """Fetch notes associated with a case identifier."""
    return CaseManagerService().get_case_notes(case_id)
