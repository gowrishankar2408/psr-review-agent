from __future__ import annotations

from typing import Any
import requests

from src.services.case_manager_service import CaseManagerService


def close_case(case_id: str, resolution_summary: str) -> Any:
    """Close a case with a supplied resolution summary."""
    return CaseManagerService().close_case(case_id)
