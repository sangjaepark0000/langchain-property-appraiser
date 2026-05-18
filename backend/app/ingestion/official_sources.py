from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.schemas.document import CanonicalDocument

_DATE_RE = re.compile(r"(\d{4})[.\-]\s*(\d{1,2})[.\-]\s*(\d{1,2})")


def parse_source_notes(path: str | Path) -> dict[str, Any]:
    notes_path = Path(path)
    metadata: dict[str, Any] = {}
    for raw_line in notes_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {"", "null", "None"}:
            metadata[key] = None
        else:
            metadata[key] = _normalize_note_value(value)
    return metadata


def load_normalized_official_source(directory: str | Path) -> CanonicalDocument:
    source_dir = Path(directory)
    text_path = source_dir / "extracted.txt"
    notes_path = source_dir / "source-notes.md"
    if not text_path.exists():
        raise FileNotFoundError(f"Missing normalized text file: {text_path}")
    if not notes_path.exists():
        raise FileNotFoundError(f"Missing source notes file: {notes_path}")

    notes = parse_source_notes(notes_path)
    text = _clean_extracted_text(text_path.read_text(encoding="utf-8"))
    source_title = str(notes.get("source_title") or text_path.parent.name)
    source_id = str(notes.get("source_id") or source_dir.name)
    source_url = notes.get("source_url") if isinstance(notes.get("source_url"), str) else None
    domain_metadata = {
        "source_title": source_title,
        "law_name": notes.get("law_name") or source_title,
        "notice_name": notes.get("notice_name"),
        "article_number": None,
        "article_title": None,
        "revision_date": notes.get("revision_date") or notes.get("promulgation_date"),
        "effective_date": notes.get("effective_date"),
        "created_date": None,
        "collected_at": notes.get("downloaded_at") or "unknown",
        "appraisal_base_date": None,
        "source_url": source_url or "unknown",
        "source_authority": notes.get("source_authority") or "unknown",
        "source_authority_type": "public_agency",
        "jurisdiction": "KR",
        "version_label": notes.get("promulgation_number") or "unknown",
        "manual_supplementation_status": notes.get("manual_supplementation_status") or "not_reviewed",
    }
    metadata = {
        **notes,
        "source_id": source_id,
        "source_name": source_title,
        "source_path": str(text_path),
        "source_url": source_url,
        "source_type": notes.get("source_type") or "official_pdf_extracted_text",
        "data_mode": "official",
        "domain_metadata": domain_metadata,
        "loader": "normalized_official_source",
        "original_files": [notes.get("raw_file")] if notes.get("raw_file") else [],
    }
    return CanonicalDocument(
        source_id=source_id,
        source_path=str(text_path),
        source_url=source_url,
        source_name=source_title,
        source_type=str(metadata["source_type"]),
        data_mode="official",
        text=text,
        metadata=metadata,
        title=source_title,
        status="loaded",
    )


def _normalize_note_value(value: str) -> str:
    date_match = _DATE_RE.fullmatch(value)
    if date_match:
        year, month, day = date_match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return value


def _clean_extracted_text(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        if stripped.startswith("법제처") and "국가법령정보센터" in stripped:
            continue
        if stripped.startswith("https://www.law.go.kr/"):
            continue
        if re.fullmatch(r"\d+/\d+", stripped):
            continue
        cleaned_lines.append(line.rstrip())
    return "\n".join(cleaned_lines).strip() + "\n"
