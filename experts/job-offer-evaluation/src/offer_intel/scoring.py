"""Deterministic, inspectable scoring rubrics."""

from __future__ import annotations

from collections.abc import Iterable

from .models import (
    CaseScores,
    Confidence,
    RubricInput,
    ScoreCard,
    ScoreComponent,
)


def _weighted_card(
    name: str,
    definitions: Iterable[tuple[str, float, float, str, list[str]]],
    *,
    blind_spots: list[str] | None = None,
) -> ScoreCard:
    components = [
        ScoreComponent(
            name=component_name,
            score=round(score, 2),
            weight=weight,
            rationale=rationale,
            evidence_ids=evidence_ids,
        )
        for component_name, score, weight, rationale, evidence_ids in definitions
    ]
    total_weight = sum(component.weight for component in components)
    score = sum(component.score * component.weight for component in components) / total_weight
    cited = sum(bool(component.evidence_ids) for component in components)
    coverage = cited / len(components) if components else 0
    confidence = (
        Confidence.HIGH
        if coverage >= 0.8
        else Confidence.MEDIUM
        if coverage >= 0.5
        else Confidence.LOW
    )
    return ScoreCard(
        name=name,
        score=round(score, 2),
        confidence=confidence,
        components=components,
        blind_spots=blind_spots or [],
    )


def compensation_verdict(target_market_percentile: float) -> str:
    if target_market_percentile < 35:
        return "undercharging"
    if target_market_percentile <= 75:
        return "market_realistic"
    return "aggressive_premium"


def score_case(values: RubricInput) -> CaseScores:
    evidence = values.evidence_ids
    company_health = _weighted_card(
        "company_health",
        [
            (
                "growth",
                values.company_growth,
                0.30,
                "Observed hiring, revenue, customer, or headcount direction.",
                evidence.get("company_growth", []),
            ),
            (
                "financial_resilience",
                values.financial_resilience,
                0.30,
                "Liquidity, profitability, funding, or filing evidence.",
                evidence.get("financial_resilience", []),
            ),
            (
                "leadership_stability",
                values.leadership_stability,
                0.15,
                "Executive continuity and material leadership changes.",
                evidence.get("leadership_stability", []),
            ),
            (
                "employee_sentiment",
                values.employee_sentiment,
                0.25,
                "Recent review themes, weighted by relevance and sample quality.",
                evidence.get("employee_sentiment", []),
            ),
        ],
    )
    role_fit = _weighted_card(
        "role_fit",
        [
            (
                "required_skills",
                values.required_skill_match / 10,
                0.45,
                "Share of explicit required criteria supported by the candidate record.",
                evidence.get("required_skill_match", []),
            ),
            (
                "preferred_skills",
                values.preferred_skill_match / 10,
                0.20,
                "Share of preferred criteria supported by the candidate record.",
                evidence.get("preferred_skill_match", []),
            ),
            (
                "relevant_experience",
                values.relevant_experience,
                0.25,
                "Depth and recency of directly relevant delivery.",
                evidence.get("relevant_experience", []),
            ),
            (
                "differentiation",
                values.differentiation,
                0.10,
                "Evidence that distinguishes the candidate from plausible peers.",
                evidence.get("differentiation", []),
            ),
        ],
    )
    leverage = _weighted_card(
        "leverage",
        [
            (
                "candidate_scarcity",
                values.candidate_scarcity,
                0.40,
                "Scarcity of the candidate's proven skill combination.",
                evidence.get("candidate_scarcity", []),
            ),
            (
                "interview_signal",
                values.interview_signal,
                0.35,
                "Strength of concrete employer interest and interview feedback.",
                evidence.get("interview_signal", []),
            ),
            (
                "competing_options",
                values.competing_options,
                0.25,
                "Credible alternatives and ability to walk away.",
                evidence.get("competing_options", []),
            ),
        ],
    )
    percentile = values.target_market_percentile
    market_alignment = max(0.0, 10.0 - abs(percentile - 55.0) / 5.5)
    compensation = _weighted_card(
        "compensation",
        [
            (
                "market_alignment",
                market_alignment,
                0.60,
                f"Target is at estimated market percentile {percentile:.0f}; "
                f"verdict={compensation_verdict(percentile)}.",
                evidence.get("target_market_percentile", []),
            ),
            (
                "negotiation_support",
                leverage.score,
                0.40,
                "Ability to support the target with role fit, scarcity, and alternatives.",
                [
                    item
                    for key in ("candidate_scarcity", "interview_signal", "competing_options")
                    for item in evidence.get(key, [])
                ],
            ),
        ],
    )
    return CaseScores(
        company_health=company_health,
        role_fit=role_fit,
        leverage=leverage,
        compensation=compensation,
    )
