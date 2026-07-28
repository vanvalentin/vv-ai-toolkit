"""Typed values returned by the local Glassdoor connector."""

from __future__ import annotations

from datetime import date as Date
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConnectorState(StrEnum):
    READY = "ready"
    AUTHENTICATED = "authenticated"
    UNAUTHENTICATED = "unauthenticated"
    CHALLENGE = "challenge"
    UNSUPPORTED = "unsupported"
    UNAVAILABLE = "unavailable"


class ErrorCode(StrEnum):
    AUTH_REQUIRED = "auth_required"
    CHALLENGE_DETECTED = "challenge_detected"
    COMPANY_NOT_FOUND = "company_not_found"
    CONFIGURATION = "configuration"
    NAVIGATION_FAILED = "navigation_failed"
    PARSE_FAILED = "parse_failed"
    UNSUPPORTED_PAGE = "unsupported_page"
    BROWSER_UNAVAILABLE = "browser_unavailable"


class ConnectorErrorInfo(BaseModel):
    code: ErrorCode
    message: str
    state: ConnectorState
    retryable: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class SessionStatus(BaseModel):
    state: ConnectorState
    authenticated: bool = False
    current_url: str | None = None
    message: str | None = None


class ViabilityReport(BaseModel):
    state: ConnectorState
    browser_backend: str | None = None
    profile_directory: Path
    profile_writable: bool
    homepage_reachable: bool = False
    session: SessionStatus | None = None
    error: ConnectorErrorInfo | None = None


class CompanyRef(BaseModel):
    name: str | None = None
    company_id: str
    canonical_url: str


class RatingBreakdown(BaseModel):
    overall: float | None = None
    culture_and_values: float | None = None
    diversity_and_inclusion: float | None = None
    work_life_balance: float | None = None
    senior_management: float | None = None
    compensation_and_benefits: float | None = None
    career_opportunities: float | None = None


class CompanyOverview(BaseModel):
    model_config = ConfigDict(extra="ignore")

    company: CompanyRef
    description: str | None = None
    headquarters: str | None = None
    size: str | None = None
    founded: int | None = None
    industry: str | None = None
    website: str | None = None
    ratings: RatingBreakdown = Field(default_factory=RatingBreakdown)


class ReviewRecord(BaseModel):
    review_id: str | None = None
    permalink: str | None = None
    date: Date | None = None
    headline: str | None = None
    job_title: str | None = None
    location: str | None = None
    employment_status: str | None = None
    tenure: str | None = None
    overall_rating: float | None = None
    pros: str | None = None
    cons: str | None = None
    advice_to_management: str | None = None
    helpful_count: int | None = None


class ReviewFilter(BaseModel):
    language: str | None = Field(default=None, pattern=r"^[A-Za-z]{3}$")
    employment_status: str | None = None
    current_job: bool | None = None
    job_title: str | None = None
    ratings: list[int] = Field(default_factory=list)
    sort_by: str = Field(default="DATE", pattern=r"^(DATE|HELPFULNESS|RATING_DESC|RATING_ASC)$")
    ascending: bool = False
    limit: int = Field(default=20, ge=1, le=100)

    @field_validator("ratings")
    @classmethod
    def ratings_are_stars(cls, values: list[int]) -> list[int]:
        if any(value < 1 or value > 5 for value in values):
            raise ValueError("ratings must contain only values from 1 through 5")
        return list(dict.fromkeys(values))


class ReviewSummary(BaseModel):
    company: CompanyRef
    total_reviews: int | None = None
    recommend_to_friend_percent: int | None = None
    ceo_approval_percent: int | None = None
    positive_outlook_percent: int | None = None
    ratings: RatingBreakdown = Field(default_factory=RatingBreakdown)
    highlights: list[str] = Field(default_factory=list)
    records: list[ReviewRecord] = Field(default_factory=list)
    filters_applied: dict[str, Any] = Field(default_factory=dict)


class SalaryRecord(BaseModel):
    title: str
    location: str | None = None
    pay_period: str | None = None
    currency: str | None = None
    base_low: float | None = None
    base_high: float | None = None
    base_median: float | None = None
    additional_median: float | None = None
    sample_size: int | None = None


class SalaryData(BaseModel):
    company: CompanyRef
    records: list[SalaryRecord] = Field(default_factory=list)


class BenefitRecord(BaseModel):
    name: str
    rating: float | None = None
    review_count: int | None = None
    description: str | None = None


class BenefitData(BaseModel):
    company: CompanyRef
    overall_rating: float | None = None
    records: list[BenefitRecord] = Field(default_factory=list)


class InterviewData(BaseModel):
    company: CompanyRef
    total_interviews: int | None = None
    positive_percent: int | None = None
    negative_percent: int | None = None
    neutral_percent: int | None = None
    difficulty: float | None = None
    duration: str | None = None
    common_stages: list[str] = Field(default_factory=list)


class CompanyIntel(BaseModel):
    overview: CompanyOverview | None = None
    reviews: ReviewSummary | None = None
    salaries: SalaryData | None = None
    benefits: BenefitData | None = None
    interviews: InterviewData | None = None
    errors: list[ConnectorErrorInfo] = Field(default_factory=list)
