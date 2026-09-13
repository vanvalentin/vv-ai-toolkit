"""High-level read-only Glassdoor connector APIs."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any
from urllib.parse import quote_plus, urlencode

from .browser import (
    BrowserConfig,
    GlassdoorBrowser,
    classify_session,
    warm_authenticated_session,
)
from .errors import AuthenticationRequired, GlassdoorConnectorError
from .models import (
    BenefitData,
    CompanyIntel,
    CompanyOverview,
    CompanyRef,
    ConnectorState,
    InterviewData,
    ReviewFilter,
    ReviewSummary,
    SalaryData,
)
from .parsing import (
    parse_benefits,
    parse_company_overview,
    parse_interviews,
    parse_reviews,
    parse_salaries,
)
from .resolver import company_section_urls, resolve_company

Parser = Callable[[str, str], Any]


class GlassdoorConnector:
    """Fetch rendered company pages sequentially from one persistent session."""

    def __init__(self, config: BrowserConfig | None = None) -> None:
        self.browser = GlassdoorBrowser(config)

    @staticmethod
    def _assert_page_access(url: str, html: str) -> None:
        status = classify_session(url, html)
        if status.state == ConnectorState.UNAUTHENTICATED:
            raise AuthenticationRequired()

    async def resolve_company(self, value: str) -> CompanyRef:
        try:
            return resolve_company(value)
        except GlassdoorConnectorError as exc:
            if not exc.info.details.get("company"):
                raise
        async with self.browser.collection_session() as page:
            base = await warm_authenticated_session(page)
            search_url = f"{base}/Search/results.htm?keyword={quote_plus(value)}"
            html = await self.browser.rendered_html(page, search_url)
            self._assert_page_access(page.url, html)
            return resolve_company(value, html)

    async def _fetch_one(
        self,
        company: CompanyRef,
        section: str,
        parser: Parser,
    ) -> Any:
        url = company_section_urls(company)[section]
        async with self.browser.collection_session() as page:
            html = await self.browser.rendered_html(page, url)
            self._assert_page_access(page.url, html)
            return parser(html, page.url)

    async def overview(self, company: CompanyRef) -> CompanyOverview:
        return await self._fetch_one(company, "overview", parse_company_overview)

    async def reviews(
        self,
        company: CompanyRef,
        filters: ReviewFilter | None = None,
    ) -> ReviewSummary:
        selected = filters or ReviewFilter()
        parameters: list[tuple[str, str]] = [
            ("sort.sortBy", selected.sort_by),
            ("sort.ascending", str(selected.ascending).lower()),
        ]
        if selected.language:
            parameters.append(("filter.iso3Language", selected.language.lower()))
        if selected.employment_status:
            parameters.append(("filter.employmentStatus", selected.employment_status))
        if selected.current_job is not None:
            parameters.append(("filter.currentJob", str(selected.current_job).lower()))
        if selected.job_title:
            parameters.append(("filter.jobTitleFTS", selected.job_title))
        parameters.extend(("filter.ratings", str(rating)) for rating in selected.ratings)

        base_url = company_section_urls(company)["reviews"]
        query = urlencode(parameters)
        pages = min(10, math.ceil(selected.limit / 10))
        combined: ReviewSummary | None = None
        seen: set[str] = set()
        async with self.browser.collection_session() as page:
            for page_number in range(1, pages + 1):
                page_url = (
                    base_url
                    if page_number == 1
                    else base_url.replace(".htm", f"_P{page_number}.htm")
                )
                html = await self.browser.rendered_html(page, f"{page_url}?{query}")
                self._assert_page_access(page.url, html)
                parsed = parse_reviews(html, page.url)
                page_records = parsed.records
                if combined is None:
                    combined = parsed.model_copy(update={"records": []})
                new_records = 0
                for record in page_records:
                    key = record.review_id or record.permalink or repr(record.model_dump())
                    if key in seen:
                        continue
                    seen.add(key)
                    combined.records.append(record)
                    new_records += 1
                    if len(combined.records) >= selected.limit:
                        break
                if len(combined.records) >= selected.limit or new_records == 0:
                    break
        assert combined is not None
        combined.filters_applied = selected.model_dump(mode="json")
        return combined

    async def salaries(self, company: CompanyRef) -> SalaryData:
        return await self._fetch_one(company, "salaries", parse_salaries)

    async def benefits(self, company: CompanyRef) -> BenefitData:
        return await self._fetch_one(company, "benefits", parse_benefits)

    async def interviews(self, company: CompanyRef) -> InterviewData:
        return await self._fetch_one(company, "interview", parse_interviews)

    async def collect_company_intel(
        self,
        company: CompanyRef,
        *,
        sections: tuple[str, ...] = (
            "overview",
            "reviews",
            "salaries",
            "benefits",
            "interview",
        ),
    ) -> CompanyIntel:
        """Collect requested sections in one browser session, never concurrently."""
        parsers: dict[str, Parser] = {
            "overview": parse_company_overview,
            "reviews": parse_reviews,
            "salaries": parse_salaries,
            "benefits": parse_benefits,
            "interview": parse_interviews,
        }
        unknown = set(sections) - parsers.keys()
        if unknown:
            raise ValueError(f"Unsupported Glassdoor sections: {sorted(unknown)}")

        result = CompanyIntel()
        urls = company_section_urls(company)
        async with self.browser.collection_session() as page:
            await warm_authenticated_session(page)
            for section in sections:
                try:
                    html = await self.browser.rendered_html(page, urls[section])
                    self._assert_page_access(page.url, html)
                    value = parsers[section](html, page.url)
                    field = "interviews" if section == "interview" else section
                    setattr(result, field, value)
                except GlassdoorConnectorError as exc:
                    result.errors.append(exc.info)
                    if exc.info.state in {
                        ConnectorState.CHALLENGE,
                        ConnectorState.UNAUTHENTICATED,
                    }:
                        break
        return result
