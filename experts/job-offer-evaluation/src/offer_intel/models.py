"""Shared structured contracts for collection, scoring, and report auditing."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, Field, HttpUrl, model_validator


class SourceKind(StrEnum):
    PRIMARY = "primary"
    REGULATORY = "regulatory"
    PROFESSIONAL_NETWORK = "professional_network"
    EMPLOYEE_REVIEW = "employee_review"
    LABOR_MARKET = "labor_market"
    NEWS = "news"
    AGGREGATOR = "aggregator"
    USER_PROVIDED = "user_provided"


class ClaimType(StrEnum):
    FACT = "fact"
    ESTIMATE = "estimate"
    INFERENCE = "inference"
    OPINION = "opinion"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CaseInput(BaseModel):
    company: str = Field(min_length=1)
    role_title: str = Field(min_length=1)
    location: str = Field(min_length=1)
    currency: str = Field(min_length=3, max_length=3)
    job_description: str | None = None
    resume_text: str | None = None
    target_compensation: str | None = None
    employment_type: str = "full-time"
    preferred_tone: str = "professional-critical"


class SourceRef(BaseModel):
    id: str = Field(pattern=r"^SRC-[A-Za-z0-9_-]+$")
    title: str
    url: HttpUrl | None = None
    kind: SourceKind
    publisher: str | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    published_at: datetime | date | None = None
    upstream_version: str | None = None


class EvidenceItem(BaseModel):
    id: str = Field(pattern=r"^EV-[A-Za-z0-9_-]+$")
    claim: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    source_id: str = Field(pattern=r"^SRC-[A-Za-z0-9_-]+$")
    topic: str = Field(min_length=1)
    claim_type: ClaimType = ClaimType.FACT
    confidence: Confidence = Confidence.MEDIUM
    observed_at: datetime | date | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Conflict(BaseModel):
    topic: str
    evidence_ids: list[str] = Field(min_length=2)
    explanation: str
    resolution: str | None = None


class ConflictInput(BaseModel):
    topic: str = Field(min_length=1)
    evidence_ids: list[str] = Field(min_length=2)
    explanation: str = Field(min_length=1)
    resolution: str | None = None


class EvidencePack(BaseModel):
    case: CaseInput
    sources: list[SourceRef] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    blind_spots: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def references_exist(self) -> EvidencePack:
        source_ids = {source.id for source in self.sources}
        evidence_ids = {item.id for item in self.evidence}
        missing_sources = {
            item.source_id for item in self.evidence if item.source_id not in source_ids
        }
        missing_conflicts = {
            evidence_id
            for conflict in self.conflicts
            for evidence_id in conflict.evidence_ids
            if evidence_id not in evidence_ids
        }
        if missing_sources:
            raise ValueError(f"Unknown source IDs: {sorted(missing_sources)}")
        if missing_conflicts:
            raise ValueError(f"Unknown conflict evidence IDs: {sorted(missing_conflicts)}")
        return self


class ExternalEvidenceInput(BaseModel):
    source_title: str = Field(min_length=1)
    source_kind: SourceKind
    claim: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    url: HttpUrl | None = None
    publisher: str | None = None
    published_at: datetime | date | None = None
    observed_at: datetime | date | None = None
    claim_type: ClaimType = ClaimType.FACT
    confidence: Confidence = Confidence.MEDIUM
    metadata: dict[str, Any] = Field(default_factory=dict)


Percent = Annotated[float, Field(ge=0, le=100)]
Score10 = Annotated[float, Field(ge=0, le=10)]


class ScoreComponent(BaseModel):
    name: str
    score: Score10
    weight: Annotated[float, Field(gt=0, le=1)]
    rationale: str
    evidence_ids: list[str] = Field(default_factory=list)


class ScoreCard(BaseModel):
    name: str
    score: Score10
    confidence: Confidence
    components: list[ScoreComponent]
    blind_spots: list[str] = Field(default_factory=list)


class CaseScores(BaseModel):
    company_health: ScoreCard
    role_fit: ScoreCard
    leverage: ScoreCard
    compensation: ScoreCard


class RubricInput(BaseModel):
    company_growth: Score10 = 5
    financial_resilience: Score10 = 5
    leadership_stability: Score10 = 5
    employee_sentiment: Score10 = 5
    required_skill_match: Percent = 50
    preferred_skill_match: Percent = 50
    relevant_experience: Score10 = 5
    differentiation: Score10 = 5
    candidate_scarcity: Score10 = 5
    interview_signal: Score10 = 5
    competing_options: Score10 = 5
    target_market_percentile: Percent = 50
    evidence_ids: dict[str, list[str]] = Field(default_factory=dict)


class ReportClaim(BaseModel):
    text: str = Field(min_length=1)
    evidence_ids: list[str] = Field(default_factory=list)
    material: bool = True


class ReportDraft(BaseModel):
    claims: list[ReportClaim]
    source_ids: list[str] = Field(default_factory=list)
    disclosed_blind_spots: list[str] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    code: str
    message: str
    claim_index: int | None = None
    evidence_id: str | None = None


class ValidationResult(BaseModel):
    valid: bool
    issues: list[ValidationIssue] = Field(default_factory=list)
    citation_coverage: Percent
    checked_claims: int
