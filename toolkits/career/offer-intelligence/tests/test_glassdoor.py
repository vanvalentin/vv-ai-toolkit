from contextlib import asynccontextmanager
from pathlib import Path

import pytest

from offer_intel.connectors.glassdoor import (
    BrowserConfig,
    CompanyRef,
    ConnectorState,
    GlassdoorConnector,
    ReviewFilter,
    classify_session,
    company_section_urls,
    default_profile_directory,
    parse_benefits,
    parse_company_overview,
    parse_interviews,
    parse_reviews,
    parse_salaries,
    resolve_company,
)

FIXTURES = Path(__file__).parent / "fixtures" / "glassdoor"
OVERVIEW_URL = (
    "https://www.glassdoor.com/Overview/Working-at-Acme-Robotics-EI_IE123.htm"
)


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_browser_config_defaults_collection_to_headed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GLASSDOOR_HEADLESS", raising=False)
    config = BrowserConfig(profile_directory=tmp_path / "glassdoor")
    assert config.collection_headless is False
    assert config.headless is True


def test_default_profile_directory_uses_macos_application_support(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    monkeypatch.setattr("offer_intel.connectors.glassdoor.browser.sys.platform", "darwin")
    assert default_profile_directory() == (
        Path.home()
        / "Library"
        / "Application Support"
        / "vv-ai-toolkit"
        / "browser-profiles"
        / "glassdoor"
    )


def test_browser_config_honors_glassdoor_headless_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GLASSDOOR_HEADLESS", "true")
    config = BrowserConfig(profile_directory=tmp_path / "glassdoor")
    assert config.collection_headless is True


def test_session_classification_is_fail_closed() -> None:
    assert classify_session("https://www.glassdoor.com/", fixture("challenge.html")).state == (
        ConnectorState.CHALLENGE
    )
    assert classify_session(
        "https://www.glassdoor.com/profile/login_input.htm",
        fixture("unauthenticated.html"),
    ).state == ConnectorState.UNAUTHENTICATED
    assert classify_session(
        "https://www.glassdoor.com/", fixture("authenticated.html")
    ).authenticated
    assert classify_session(
        "https://www.glassdoor.com.hk/Community/index.htm",
        "<html><body>Welcome</body></html>",
    ).authenticated


def test_company_section_urls_follow_regional_host() -> None:
    company = resolve_company(
        "https://www.glassdoor.com.hk/Overview/Working-at-Acme-Robotics-EI_IE123.htm"
    )
    urls = company_section_urls(company)
    assert urls["overview"].startswith("https://www.glassdoor.com.hk/")


def test_resolve_company_requires_an_exact_name() -> None:
    company = resolve_company("Acme Robotics", fixture("search-results.html"))
    assert company.company_id == "123"
    assert company.name == "Acme Robotics"


def test_parse_all_supported_sections() -> None:
    overview = parse_company_overview(fixture("overview.html"), OVERVIEW_URL)
    reviews = parse_reviews(
        fixture("reviews.html"),
        "https://www.glassdoor.com/Reviews/Acme-Robotics-Reviews-E123.htm",
    )
    salaries = parse_salaries(
        fixture("salaries.html"),
        "https://www.glassdoor.com/Salaries/Acme-Robotics-Salaries-E123.htm",
    )
    benefits = parse_benefits(
        fixture("benefits.html"),
        "https://www.glassdoor.com/Benefits/Acme-Robotics-Benefits-EI_IE123.htm",
    )
    interviews = parse_interviews(
        fixture("interviews.html"),
        "https://www.glassdoor.com/Interview/Acme-Robotics-Interview-Questions-E123.htm",
    )

    assert overview.founded == 2012
    assert overview.ratings.overall == 4.2
    assert reviews.total_reviews == 1234
    assert reviews.highlights == [
        "Supportive engineering culture",
        "Fast growth can change priorities",
    ]
    assert reviews.records[0].review_id == "987"
    assert reviews.records[0].date.isoformat() == "2026-06-20"
    assert reviews.records[0].helpful_count == 12
    assert salaries.records[0].base_median == 82000
    assert salaries.records[0].sample_size == 18
    assert benefits.records[1].name == "Remote Work"
    assert interviews.common_stages[-1] == "Panel interview"


@pytest.mark.asyncio
async def test_review_pagination_deduplicates_records() -> None:
    class FakePage:
        url = "https://www.glassdoor.com/Reviews/Acme-Robotics-Reviews-E123.htm"

    class FakeBrowser:
        def __init__(self) -> None:
            self.urls: list[str] = []

        @asynccontextmanager
        async def session(self):
            yield FakePage()

        collection_session = session

        async def rendered_html(self, page, url: str) -> str:
            self.urls.append(url)
            page.url = url
            return fixture("reviews.html")

    connector = GlassdoorConnector()
    browser = FakeBrowser()
    connector.browser = browser
    company = CompanyRef(
        name="Acme Robotics",
        company_id="123",
        canonical_url=OVERVIEW_URL,
    )

    reviews = await connector.reviews(company, ReviewFilter(limit=20))

    assert len(reviews.records) == 1
    assert len(browser.urls) == 2
    assert "_P2.htm" in browser.urls[1]
