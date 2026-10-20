from __future__ import annotations


def parse_psr_notes(notes: str) -> dict[str, object]:
    """Normalize notes and return non-empty paragraphs without assuming a PSR schema."""
    normalized = "\n".join(line.rstrip() for line in notes.splitlines()).strip()
    paragraphs = [
        paragraph.strip()
        for paragraph in normalized.split("\n\n")
        if paragraph.strip()
    ]
    return {"normalized_text": normalized, "paragraphs": paragraphs}
