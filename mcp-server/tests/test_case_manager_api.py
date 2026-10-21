from __future__ import annotations
from typing import Any
from src.services.case_manager_service import CaseManagerService
from src.tools.parse_psr_notes import NoteParser
from src.tools.invoke_reasoning_agent import invoke_reasoning_agent


def get_case_details(case_id: str) -> Any:
    """Fetch the case record for a case identifier."""
    print("Fetching details for case_id:", case_id)
    return CaseManagerService().get_case_details(case_id)

def case_notes_parser(case_id: str, raw_notes: dict) -> Any:
    """case notes parser"""
    parsed_notes = NoteParser().extract_notes(raw_notes)
    return parsed_notes

if __name__ == "__main__":
    details = get_case_details("24910726")
    #print(details)
    parsed_notes = case_notes_parser("24910726", details)
    print(parsed_notes)
    reasoning_agent = invoke_reasoning_agent("24910726", parsed_notes)
    print(reasoning_agent)