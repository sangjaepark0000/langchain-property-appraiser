from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document
from app.rag.retriever import RetrievalResult


@dataclass(frozen=True)
class RecentPeriodFilter:
    amount: int | None = None
    unit: str | None = None
    since: date | None = None
    preferred_date_fields: tuple[str, ...] = ("revision_date", "effective_date")
    status: str = "parsed"
    limitation_reason: str | None = None


@dataclass(frozen=True)
class RecentPeriodFilterResult:
    results: list[RetrievalResult]
    applied: bool
    date_field_used: str | None = None
    excluded_chunk_ids: list[int] = field(default_factory=list)
    missing_date_chunk_ids: list[int] = field(default_factory=list)
    limitation_reason: str | None = None


def parse_recent_period_filter(query: str, *, today: date | None = None) -> RecentPeriodFilter | None:
    if "최근" not in query:
        return None
    resolved_today = today or date.today()
    match = re.search(r"최근\s*(\d+)\s*(년|개월|달|일)", query)
    if match is None:
        return RecentPeriodFilter(status="needs_clarification", limitation_reason="Recent period expression is missing an amount/unit")
    amount = int(match.group(1))
    raw_unit = match.group(2)
    if raw_unit == "년":
        unit = "year"
        since = _subtract_years(resolved_today, amount)
    elif raw_unit in {"개월", "달"}:
        unit = "month"
        since = _subtract_months(resolved_today, amount)
    else:
        unit = "day"
        since = resolved_today - timedelta(days=amount)
    return RecentPeriodFilter(amount=amount, unit=unit, since=since)


def apply_recent_period_filter(
    session: Session,
    results: list[RetrievalResult],
    recent_filter: RecentPeriodFilter | None,
) -> RecentPeriodFilterResult:
    if recent_filter is None or recent_filter.status != "parsed" or recent_filter.since is None:
        return RecentPeriodFilterResult(results=results, applied=False, limitation_reason=recent_filter.limitation_reason if recent_filter else None)

    kept: list[RetrievalResult] = []
    excluded: list[int] = []
    missing: list[int] = []
    used_fields: list[str] = []

    for result in results:
        chunk = session.get(Chunk, result.chunk_id)
        document = session.get(Document, result.document_id)
        metadata = {}
        if document and document.metadata_:
            metadata.update(document.metadata_.get("domain_metadata") or {})
        if chunk and chunk.metadata_:
            metadata.update(chunk.metadata_.get("domain_metadata") or {})
        parsed_date: date | None = None
        field_used: str | None = None
        for field_name in recent_filter.preferred_date_fields:
            candidate = _parse_date(metadata.get(field_name))
            if candidate is not None:
                parsed_date = candidate
                field_used = field_name
                break
        if parsed_date is None:
            missing.append(result.chunk_id)
            continue
        used_fields.append(field_used or "unknown")
        if parsed_date >= recent_filter.since:
            kept.append(result)
        else:
            excluded.append(result.chunk_id)

    date_field_used = used_fields[0] if used_fields else None
    limitation = None
    if missing:
        limitation = "Recent period filter had missing date metadata for some chunks; dates were not fabricated."
    return RecentPeriodFilterResult(
        results=kept,
        applied=True,
        date_field_used=date_field_used,
        excluded_chunk_ids=excluded,
        missing_date_chunk_ids=missing,
        limitation_reason=limitation,
    )


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str) or value in {"", "unknown"}:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None


def _subtract_years(today: date, amount: int) -> date:
    try:
        return today.replace(year=today.year - amount)
    except ValueError:
        return today.replace(month=2, day=28, year=today.year - amount)


def _subtract_months(today: date, amount: int) -> date:
    month_index = today.year * 12 + today.month - 1 - amount
    year = month_index // 12
    month = month_index % 12 + 1
    day = min(today.day, _days_in_month(year, month))
    return date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - timedelta(days=1)).day
