"""Offer Intelligence MCP server and its read-only external tool surface."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from .connectors.glassdoor import (
    CompanyIntel,
    GlassdoorConnector,
    ReviewFilter,
    check_viability,
    company_section_urls,
)
from .connectors.glassdoor import (
    logout as glassdoor_logout_session,
)
from .connectors.glassdoor import (
    manual_login as glassdoor_manual_login,
)
from .connectors.glassdoor import (
    session_status as glassdoor_session_status,
)
from .connectors.linkedin import LinkedInConnector, LinkedInSnapshot
from .models import (
    CaseInput,
    CaseScores,
    Conflict,
    ConflictInput,
    EvidenceItem,
    EvidencePack,
    ExternalEvidenceInput,
    ReportDraft,
    RubricInput,
    SourceKind,
    ValidationResult,
)
from .registry import CaseRegistry
from .scoring import score_case
from .validation import validate_report

registry = CaseRegistry()
linkedin = LinkedInConnector()
glassdoor = GlassdoorConnector()


def _snapshot_payload(snapshot: LinkedInSnapshot) -> dict[str, Any]:
    return snapshot.model_dump(mode="json")


def _add_linkedin_snapshot(case_id: str, snapshot: LinkedInSnapshot, topic: str) -> list[str]:
    evidence_ids: list[str] = []
    for section_name, text in snapshot.sections.items():
        if not text.strip():
            continue
        item = registry.add_evidence(
            case_id,
            source_title=f"LinkedIn {snapshot.tool}: {section_name}",
            source_kind=SourceKind.PROFESSIONAL_NETWORK,
            claim=f"LinkedIn {section_name} snapshot collected for the target research case.",
            excerpt=text,
            topic=topic,
            url=snapshot.url,
            publisher="LinkedIn",
            observed_at=snapshot.retrieved_at,
            metadata={
                "tool": snapshot.tool,
                "section": section_name,
                "references": snapshot.references.get(section_name, []),
                "section_error": snapshot.section_errors.get(section_name),
            },
            upstream_version=snapshot.upstream_version,
        )
        evidence_ids.append(item.id)
    if snapshot.section_errors:
        registry.add_blind_spot(
            case_id,
            f"LinkedIn returned section errors for {snapshot.tool}: "
            f"{', '.join(sorted(snapshot.section_errors))}",
        )
    return evidence_ids


def _add_glassdoor_intel(case_id: str, intel: CompanyIntel) -> list[str]:
    evidence_ids: list[str] = []
    sections = {
        "overview": (intel.overview, "company_profile", SourceKind.AGGREGATOR),
        "reviews": (intel.reviews, "employee_sentiment", SourceKind.EMPLOYEE_REVIEW),
        "salaries": (intel.salaries, "salary", SourceKind.AGGREGATOR),
        "benefits": (intel.benefits, "benefits", SourceKind.EMPLOYEE_REVIEW),
        "interviews": (intel.interviews, "interview_process", SourceKind.EMPLOYEE_REVIEW),
    }
    for section, (value, topic, source_kind) in sections.items():
        if value is None:
            continue
        company = value.company
        urls = company_section_urls(company)
        source_url = urls["interview" if section == "interviews" else section]
        serialized = value.model_dump_json(exclude_none=True)
        item = registry.add_evidence(
            case_id,
            source_title=f"Glassdoor {section}: {company.name or company.company_id}",
            source_kind=source_kind,
            claim=f"Glassdoor {section} snapshot collected for the target company.",
            excerpt=serialized,
            topic=topic,
            url=source_url,
            publisher="Glassdoor",
            metadata={
                "section": section,
                "company_id": company.company_id,
                "sample_limited": True,
            },
        )
        evidence_ids.append(item.id)
    for error in intel.errors:
        registry.add_blind_spot(
            case_id,
            f"Glassdoor {error.code}: {error.message}",
        )
    return evidence_ids


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        "offer-intel-mcp",
        version="0.1.0",
        mask_error_details=True,
        instructions=(
            "Collect evidence before analysis. Cite EV-* IDs for every material claim, "
            "then call validate_offer_report before presenting a final report."
        ),
    )

    @mcp.tool(title="Create Offer Research Case", tags={"case"})
    def create_offer_case(case: CaseInput) -> dict[str, Any]:
        """Create an in-memory case. Resume and job text are never persisted by default."""
        case_id, pack = registry.create(case)
        return {"case_id": case_id, "evidence_pack": pack.model_dump(mode="json")}

    @mcp.tool(title="Add External Evidence", tags={"evidence"})
    def add_external_evidence(case_id: str, evidence: ExternalEvidenceInput) -> EvidenceItem:
        """Ingest a claim found with the host's web, filing, labor, or ATS tools."""
        values = evidence.model_dump()
        if values["url"] is not None:
            values["url"] = str(values["url"])
        return registry.add_evidence(case_id, **values)

    @mcp.tool(
        title="Get Evidence Pack",
        annotations={"readOnlyHint": True},
        tags={"evidence"},
    )
    def get_evidence_pack(case_id: str) -> EvidencePack:
        """Return all sources, claim evidence, conflicts, and blind spots for a case."""
        return registry.get(case_id)

    @mcp.tool(title="Record Evidence Conflict", tags={"evidence"})
    def record_evidence_conflict(case_id: str, conflict: ConflictInput) -> Conflict:
        """Record incompatible source claims; never silently average them."""
        return registry.add_conflict(case_id, conflict)

    @mcp.tool(title="Score Offer Case", annotations={"readOnlyHint": True}, tags={"scoring"})
    def score_offer_case(case_id: str, rubric: RubricInput) -> CaseScores:
        """Compute reproducible score cards after checking cited evidence IDs."""
        pack = registry.get(case_id)
        known = {item.id for item in pack.evidence}
        cited = {item for values in rubric.evidence_ids.values() for item in values}
        unknown = sorted(cited - known)
        if unknown:
            raise ValueError(f"Rubric cites unknown evidence IDs: {unknown}")
        return score_case(rubric)

    @mcp.tool(
        title="Validate Offer Report",
        annotations={"readOnlyHint": True},
        tags={"validation"},
    )
    def validate_offer_report(case_id: str, report: ReportDraft) -> ValidationResult:
        """Fail unsupported/stale claims and undisclosed evidence gaps."""
        return validate_report(report, registry.get(case_id))

    @mcp.tool(
        title="LinkedIn Connector Status",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"linkedin"},
    )
    def linkedin_status() -> dict[str, Any]:
        """Check whether uvx is available and show the strict upstream allowlist."""
        return linkedin.status()

    @mcp.tool(
        title="Search LinkedIn Companies",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"linkedin"},
    )
    async def linkedin_search_companies(keywords: str) -> dict[str, Any]:
        """Resolve a display name to a LinkedIn company slug before collection."""
        return _snapshot_payload(await linkedin.search_companies(keywords))

    @mcp.tool(
        title="Collect LinkedIn Company Evidence",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"linkedin", "evidence"},
    )
    async def linkedin_collect_company(
        case_id: str,
        company_slug: str,
        sections: str | None = "posts,jobs",
    ) -> dict[str, Any]:
        snapshot = await linkedin.get_company_profile(company_slug, sections)
        evidence_ids = _add_linkedin_snapshot(case_id, snapshot, "professional_network_snapshot")
        return {"evidence_ids": evidence_ids, "snapshot": _snapshot_payload(snapshot)}

    @mcp.tool(
        title="Collect LinkedIn Peer Evidence",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"linkedin", "evidence"},
    )
    async def linkedin_collect_peers(
        case_id: str,
        company_slug: str,
        role_keywords: str,
    ) -> dict[str, Any]:
        snapshot = await linkedin.get_company_employees(company_slug, role_keywords)
        evidence_ids = _add_linkedin_snapshot(case_id, snapshot, "role_peers")
        return {"evidence_ids": evidence_ids, "snapshot": _snapshot_payload(snapshot)}

    @mcp.tool(
        title="Collect LinkedIn Job Search Evidence",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"linkedin", "evidence"},
    )
    async def linkedin_collect_jobs(
        case_id: str,
        keywords: str,
        location: str | None = None,
    ) -> dict[str, Any]:
        snapshot = await linkedin.search_jobs(keywords, location)
        evidence_ids = _add_linkedin_snapshot(case_id, snapshot, "job_posting")
        return {"evidence_ids": evidence_ids, "snapshot": _snapshot_payload(snapshot)}

    @mcp.tool(
        title="Collect LinkedIn Job Details",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"linkedin", "evidence"},
    )
    async def linkedin_collect_job_details(case_id: str, job_id: str) -> dict[str, Any]:
        snapshot = await linkedin.get_job_details(job_id)
        evidence_ids = _add_linkedin_snapshot(case_id, snapshot, "job_posting")
        return {"evidence_ids": evidence_ids, "snapshot": _snapshot_payload(snapshot)}

    @mcp.tool(
        title="Check Glassdoor Connector Viability",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"glassdoor", "session"},
    )
    async def glassdoor_check_viability() -> dict[str, Any]:
        """Check browser/profile/page state without claiming authenticated access."""
        return (await check_viability()).model_dump(mode="json")

    @mcp.tool(
        title="Get Glassdoor Session Status",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"glassdoor", "session"},
    )
    async def glassdoor_status() -> dict[str, Any]:
        return (await glassdoor_session_status()).model_dump(mode="json")

    @mcp.tool(
        title="Open Glassdoor Manual Login",
        annotations={"openWorldHint": True},
        tags={"glassdoor", "session"},
    )
    async def glassdoor_login(timeout_seconds: float = 300) -> dict[str, Any]:
        """Open a headed browser; the user must complete all authentication manually."""
        return (
            await glassdoor_manual_login(timeout_seconds=timeout_seconds)
        ).model_dump(mode="json")

    @mcp.tool(
        title="Clear Local Glassdoor Session",
        annotations={"destructiveHint": True},
        tags={"glassdoor", "session"},
    )
    async def glassdoor_logout() -> dict[str, Any]:
        """Clear cookies in the dedicated local profile without contacting a logout URL."""
        return (await glassdoor_logout_session()).model_dump(mode="json")

    @mcp.tool(
        title="Resolve Glassdoor Company",
        annotations={"readOnlyHint": True, "openWorldHint": True},
        tags={"glassdoor"},
    )
    async def glassdoor_resolve_company(value: str) -> dict[str, Any]:
        """Resolve a company URL directly or a name through rendered search results."""
        return (await glassdoor.resolve_company(value)).model_dump(mode="json")

    @mcp.tool(
        title="Collect Glassdoor Company Evidence",
        annotations={"openWorldHint": True},
        tags={"glassdoor", "evidence"},
    )
    async def glassdoor_collect_company(
        case_id: str,
        company: str,
        sections: list[str] | None = None,
    ) -> dict[str, Any]:
        """Collect selected read-only sections and add normalized snapshots to a case."""
        company_ref = await glassdoor.resolve_company(company)
        selected = tuple(sections or ["overview", "reviews", "salaries", "benefits", "interview"])
        intel = await glassdoor.collect_company_intel(company_ref, sections=selected)
        evidence_ids = _add_glassdoor_intel(case_id, intel)
        return {
            "evidence_ids": evidence_ids,
            "intel": intel.model_dump(mode="json"),
        }

    @mcp.tool(
        title="Collect Filtered Glassdoor Reviews",
        annotations={"openWorldHint": True},
        tags={"glassdoor", "evidence"},
    )
    async def glassdoor_collect_reviews(
        case_id: str,
        company: str,
        filters: ReviewFilter | None = None,
    ) -> dict[str, Any]:
        """Collect a bounded, filtered review sample with IDs and canonical dates."""
        company_ref = await glassdoor.resolve_company(company)
        reviews = await glassdoor.reviews(company_ref, filters)
        intel = CompanyIntel(reviews=reviews)
        evidence_ids = _add_glassdoor_intel(case_id, intel)
        return {
            "evidence_ids": evidence_ids,
            "reviews": reviews.model_dump(mode="json"),
        }

    return mcp
