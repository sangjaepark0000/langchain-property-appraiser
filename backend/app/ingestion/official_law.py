from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

from app.schemas.document import CanonicalDocument


class OfficialLawParseError(ValueError):
    pass


_TEXT_TAGS = ("Body", "본문", "Text", "조문내용", "ArticleText")


def _text(root: ElementTree.Element, *tags: str) -> str | None:
    for tag in tags:
        value = root.findtext(tag)
        if value is not None and value.strip():
            return value.strip()
    return None


def _required_body(root: ElementTree.Element) -> str:
    body_parts: list[str] = []
    for tag in _TEXT_TAGS:
        for node in root.findall(f".//{tag}"):
            if node.text and node.text.strip():
                body_parts.append(node.text.strip())
    if not body_parts:
        raise OfficialLawParseError("Official law XML is missing body text")
    return "\n\n".join(body_parts)


def load_official_law_xml(path: Path, data_mode: str = "official", source_id: str | None = None) -> CanonicalDocument:
    try:
        root = ElementTree.parse(path).getroot()
    except ElementTree.ParseError as exc:
        raise OfficialLawParseError(f"Invalid official law XML: {exc}") from exc

    if root.tag != "LawDocument":
        raise OfficialLawParseError(f"Expected LawDocument root, got {root.tag!r}")

    resolved_source_id = source_id or "official-law-open-api"
    source_title = _text(root, "SourceTitle", "자료명", "LawName", "법령명") or "unknown"
    law_name = _text(root, "LawName", "법령명")
    notice_name = _text(root, "NoticeName", "고시명")
    article_number = _text(root, "ArticleNumber", "조항", "조문번호")
    article_title = _text(root, "ArticleTitle", "조문제목")
    revision_date = _text(root, "RevisionDate", "개정일")
    effective_date = _text(root, "EffectiveDate", "시행일")
    created_date = _text(root, "CreatedDate", "작성일")
    source_url = _text(root, "SourceUrl", "원문URL")
    source_authority = _text(root, "SourceAuthority", "소관부처", "발행기관") or "unknown"
    collected_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    body = _required_body(root)

    domain_metadata = {
        "source_title": source_title,
        "law_name": law_name,
        "notice_name": notice_name,
        "article_number": article_number,
        "article_title": article_title,
        "revision_date": revision_date,
        "effective_date": effective_date,
        "created_date": created_date,
        "collected_at": collected_at,
        "appraisal_base_date": None,
        "source_url": source_url or "unknown",
        "source_authority": source_authority,
        "source_authority_type": "public_agency" if source_authority != "unknown" else "unknown",
        "jurisdiction": "KR",
        "version_label": _text(root, "VersionLabel", "버전") or "unknown",
        "manual_supplementation_status": "not_reviewed",
    }
    metadata = {
        "source_id": resolved_source_id,
        "source_name": source_title,
        "source_path": str(path),
        "source_url": source_url,
        "source_type": "official_law_xml",
        "data_mode": data_mode,
        "domain_metadata": domain_metadata,
        "loader": "official_law_xml",
        "loader_limitations": [
            "Recorded/local XML parser only; live official API access requires credentials and source fixtures.",
            "Missing source metadata remains unknown/null and is not fabricated.",
        ],
        "manual_supplementation": "Human reviewers may verify visible source_title, law_name, article_number, dates, and source_url from the official source.",
        "prerequisite_work": "Configure official API credentials and add recorded response fixtures before live API ingestion.",
    }
    return CanonicalDocument(
        source_id=resolved_source_id,
        source_path=str(path),
        source_url=source_url,
        source_name=source_title,
        source_type="official_law_xml",
        data_mode=data_mode,
        text=body,
        metadata=metadata,
        title=source_title,
        status="loaded",
    )
