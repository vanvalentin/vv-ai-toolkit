"""Source ranking and field-specific freshness rules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from .models import EvidenceItem, SourceKind, SourceRef

SOURCE_RANK: dict[SourceKind, int] = {
    SourceKind.REGULATORY: 100,
    SourceKind.PRIMARY: 90,
    SourceKind.LABOR_MARKET: 80,
    SourceKind.PROFESSIONAL_NETWORK: 65,
    SourceKind.EMPLOYEE_REVIEW: 60,
    SourceKind.NEWS: 55,
    SourceKind.USER_PROVIDED: 50,
    SourceKind.AGGREGATOR: 40,
}

# Current-state fields need short windows. Historical facts intentionally have no TTL.
TOPIC_MAX_AGE: dict[str, timedelta | None] = {
    "founding": None,
    "company_history": None,
    "headcount": timedelta(days=90),
    "leadership": timedelta(days=120),
    "financial_health": timedelta(days=550),
    "layoffs": timedelta(days=730),
    "job_posting": timedelta(days=45),
    "tech_stack": timedelta(days=365),
    "employee_sentiment": timedelta(days=550),
    "salary": timedelta(days=550),
    "benefits": timedelta(days=365),
    "competitors": timedelta(days=365),
}
DEFAULT_MAX_AGE = timedelta(days=365 * 5)


@dataclass(frozen=True)
class FreshnessAssessment:
    fresh: bool
    age_days: int | None
    max_age_days: int | None
    reason: str


def _as_datetime(value: datetime | date | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(UTC) if value.tzinfo else value.replace(tzinfo=UTC)
    return datetime(value.year, value.month, value.day, tzinfo=UTC)


def assess_freshness(
    evidence: EvidenceItem,
    source: SourceRef,
    *,
    now: datetime | None = None,
) -> FreshnessAssessment:
    """Assess an item using its observation date, then source publication/retrieval date."""
    maximum = TOPIC_MAX_AGE.get(evidence.topic, DEFAULT_MAX_AGE)
    if maximum is None:
        return FreshnessAssessment(True, None, None, "Historical topic has no freshness limit")

    timestamp = (
        _as_datetime(evidence.observed_at)
        or _as_datetime(source.published_at)
        or _as_datetime(source.retrieved_at)
    )
    if timestamp is None:
        return FreshnessAssessment(False, None, maximum.days, "No usable date")

    reference = now or datetime.now(UTC)
    age = max(reference - timestamp, timedelta())
    is_fresh = age <= maximum
    return FreshnessAssessment(
        fresh=is_fresh,
        age_days=age.days,
        max_age_days=maximum.days,
        reason="Within freshness window" if is_fresh else "Older than freshness window",
    )


def rank_source(source: SourceRef) -> int:
    return SOURCE_RANK[source.kind]


def choose_preferred_source(sources: list[SourceRef]) -> SourceRef | None:
    """Prefer authority first and newest observation second."""
    if not sources:
        return None
    return max(
        sources,
        key=lambda source: (
            rank_source(source),
            _as_datetime(source.published_at)
            or _as_datetime(source.retrieved_at)
            or datetime.min.replace(tzinfo=UTC),
        ),
    )
