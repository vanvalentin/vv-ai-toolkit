from datetime import UTC, datetime, timedelta

import pytest
from fastmcp import Client

from offer_intel.models import (
    CaseInput,
    Confidence,
    EvidenceItem,
    EvidencePack,
    ReportClaim,
    ReportDraft,
    RubricInput,
    SourceKind,
    SourceRef,
)
from offer_intel.scoring import compensation_verdict, score_case
from offer_intel.server import create_mcp_server
from offer_intel.source_policy import assess_freshness
from offer_intel.validation import validate_report


def case_input() -> CaseInput:
    return CaseInput(
        company="Example Corp",
        role_title="Staff Engineer",
        location="London",
        currency="GBP",
    )


def test_freshness_uses_topic_specific_windows() -> None:
    old = datetime.now(UTC) - timedelta(days=600)
    source = SourceRef(
        id="SRC-test",
        title="Old review",
        kind=SourceKind.EMPLOYEE_REVIEW,
        retrieved_at=old,
    )
    sentiment = EvidenceItem(
        id="EV-sentiment",
        claim="Sentiment changed",
        excerpt="Review excerpt",
        source_id=source.id,
        topic="employee_sentiment",
    )
    history = sentiment.model_copy(update={"id": "EV-history", "topic": "founding"})

    assert assess_freshness(sentiment, source).fresh is False
    assert assess_freshness(history, source).fresh is True


def test_scoring_is_deterministic_and_citation_aware() -> None:
    values = RubricInput(
        company_growth=8,
        financial_resilience=7,
        leadership_stability=6,
        employee_sentiment=5,
        required_skill_match=90,
        preferred_skill_match=70,
        relevant_experience=8,
        differentiation=7,
        target_market_percentile=80,
        evidence_ids={
            "company_growth": ["EV-growth"],
            "financial_resilience": ["EV-finance"],
            "leadership_stability": ["EV-leadership"],
            "employee_sentiment": ["EV-sentiment"],
        },
    )
    first = score_case(values)
    second = score_case(values)

    assert first == second
    assert first.company_health.confidence == Confidence.HIGH
    assert compensation_verdict(20) == "undercharging"
    assert compensation_verdict(50) == "market_realistic"
    assert compensation_verdict(80) == "aggressive_premium"


def test_report_validation_fails_uncited_material_claim() -> None:
    pack = EvidencePack(case=case_input(), blind_spots=["No verified salary data"])
    report = ReportDraft(claims=[ReportClaim(text="Revenue is growing.")])

    result = validate_report(report, pack)

    assert result.valid is False
    assert result.citation_coverage == 0
    assert {issue.code for issue in result.issues} == {
        "uncited_material_claim",
        "undisclosed_blind_spot",
    }


@pytest.mark.asyncio
async def test_mcp_exposes_no_linkedin_mutation_tools() -> None:
    async with Client(create_mcp_server()) as client:
        tools = await client.list_tools()
    names = {tool.name for tool in tools}

    assert "linkedin_collect_company" in names
    forbidden = ("message", "connect_with", "apply", "follow", "submit", "write_review")
    assert not any(token in name for name in names for token in forbidden)
