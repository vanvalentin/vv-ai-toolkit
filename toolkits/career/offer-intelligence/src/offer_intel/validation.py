"""Fail-closed report validation against an evidence pack."""

from __future__ import annotations

from .models import EvidencePack, ReportDraft, ValidationIssue, ValidationResult
from .source_policy import assess_freshness


def validate_report(report: ReportDraft, pack: EvidencePack) -> ValidationResult:
    evidence_by_id = {item.id: item for item in pack.evidence}
    sources_by_id = {source.id: source for source in pack.sources}
    issues: list[ValidationIssue] = []
    material_claims = [claim for claim in report.claims if claim.material]
    cited_material = 0

    for index, claim in enumerate(report.claims):
        if claim.material and not claim.evidence_ids:
            issues.append(
                ValidationIssue(
                    code="uncited_material_claim",
                    message="Material factual claim has no evidence IDs.",
                    claim_index=index,
                )
            )
            continue
        if claim.material:
            cited_material += 1

        for evidence_id in claim.evidence_ids:
            item = evidence_by_id.get(evidence_id)
            if item is None:
                issues.append(
                    ValidationIssue(
                        code="unknown_evidence",
                        message=f"Claim cites unknown evidence {evidence_id}.",
                        claim_index=index,
                        evidence_id=evidence_id,
                    )
                )
                continue
            source = sources_by_id[item.source_id]
            freshness = assess_freshness(item, source)
            if not freshness.fresh:
                issues.append(
                    ValidationIssue(
                        code="stale_evidence",
                        message=(
                            f"{evidence_id} is stale for topic '{item.topic}': "
                            f"{freshness.reason}."
                        ),
                        claim_index=index,
                        evidence_id=evidence_id,
                    )
                )

    omitted_blind_spots = set(pack.blind_spots) - set(report.disclosed_blind_spots)
    for blind_spot in sorted(omitted_blind_spots):
        issues.append(
            ValidationIssue(
                code="undisclosed_blind_spot",
                message=f"Evidence-pack blind spot was not disclosed: {blind_spot}",
            )
        )

    unknown_sources = set(report.source_ids) - set(sources_by_id)
    for source_id in sorted(unknown_sources):
        issues.append(
            ValidationIssue(
                code="unknown_source",
                message=f"Report lists unknown source {source_id}.",
            )
        )

    coverage = 100.0 if not material_claims else (cited_material / len(material_claims)) * 100
    return ValidationResult(
        valid=not issues,
        issues=issues,
        citation_coverage=round(coverage, 2),
        checked_claims=len(report.claims),
    )
