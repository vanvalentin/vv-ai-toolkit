"""Pure company URL resolution and section URL construction."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from .errors import GlassdoorConnectorError, UnsupportedPage
from .models import CompanyRef, ConnectorState, ErrorCode

_COMPANY_RE = re.compile(
    r"/(?:Overview|Reviews|Salary|Salaries|Benefits|Interview)/"
    r"(?P<slug>[^/?#]*?)-(?:EI_)?(?:IE|E)(?P<id>\d+)(?:[^/?#]*)\.htm",
    re.IGNORECASE,
)
_ALLOWED_HOSTS = {
    "glassdoor.com",
    "www.glassdoor.com",
    "glassdoor.com.hk",
    "www.glassdoor.com.hk",
}


def _is_allowed_glassdoor_host(host: str) -> bool:
    lowered = host.lower()
    if lowered in _ALLOWED_HOSTS:
        return True
    return lowered.endswith(".glassdoor.com") or lowered.endswith(".glassdoor.com.hk")


def _normalise_url(url: str) -> str:
    absolute = urljoin("https://www.glassdoor.com", url)
    parsed = urlparse(absolute)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not _is_allowed_glassdoor_host(host):
        raise UnsupportedPage(url)
    return parsed._replace(scheme="https", netloc=host, query="", fragment="").geturl()


def company_from_url(url: str, name: str | None = None) -> CompanyRef:
    canonical = _normalise_url(url)
    match = _COMPANY_RE.search(canonical)
    if not match:
        raise UnsupportedPage(url)
    base_slug = _base_slug(match.group("slug"))
    inferred_name = re.sub(r"[-_]+", " ", base_slug).strip()
    return CompanyRef(
        name=name or inferred_name or None,
        company_id=match.group("id"),
        canonical_url=_section_url(canonical, "Overview"),
    )


def _section_url(url: str, section: str) -> str:
    match = _COMPANY_RE.search(url)
    if not match:
        raise UnsupportedPage(url)
    slug = _base_slug(match.group("slug"))
    company_id = match.group("id")
    paths = {
        "Overview": f"Working-at-{slug}-EI_IE{company_id}.htm",
        "Reviews": f"{slug}-Reviews-E{company_id}.htm",
        "Salaries": f"{slug}-Salaries-E{company_id}.htm",
        "Benefits": f"{slug}-Benefits-EI_IE{company_id}.htm",
        "Interview": f"{slug}-Interview-Questions-E{company_id}.htm",
    }
    host = urlparse(_normalise_url(url)).netloc
    return f"https://{host}/{section}/{paths[section]}"


def _base_slug(slug: str) -> str:
    value = slug.strip("-")
    value = re.sub(r"^Working-at-", "", value, flags=re.I)
    value = re.sub(
        r"-(?:Reviews|Salaries|Salary|Benefits|Interview-Questions)$",
        "",
        value,
        flags=re.I,
    )
    return value


def company_section_urls(company: CompanyRef) -> dict[str, str]:
    return {
        section.lower(): _section_url(company.canonical_url, section)
        for section in ("Overview", "Reviews", "Salaries", "Benefits", "Interview")
    }


class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None


def resolve_company(value: str, rendered_search_html: str | None = None) -> CompanyRef:
    """Resolve a direct company URL, or select an exact company search result."""
    if value.startswith(("http://", "https://", "/")):
        return company_from_url(value)
    if not rendered_search_html:
        raise GlassdoorConnectorError(
            ErrorCode.COMPANY_NOT_FOUND,
            "A company name requires rendered Glassdoor search results.",
            state=ConnectorState.UNSUPPORTED,
            details={"company": value},
        )

    collector = _LinkCollector()
    collector.feed(rendered_search_html)
    wanted = re.sub(r"\W+", "", value).casefold()
    candidates: list[CompanyRef] = []
    for href, label in collector.links:
        try:
            candidate = company_from_url(href, label or None)
        except UnsupportedPage:
            continue
        candidate_name = re.sub(r"\W+", "", candidate.name or "").casefold()
        if candidate_name == wanted:
            return candidate
        candidates.append(candidate)
    raise GlassdoorConnectorError(
        ErrorCode.COMPANY_NOT_FOUND,
        f"No exact Glassdoor company result matched {value!r}.",
        state=ConnectorState.UNSUPPORTED,
        details={
            "company": value,
            "candidates": [item.model_dump(mode="json") for item in candidates[:5]],
        },
    )
