"""Pure parsers for rendered Glassdoor HTML.

The parsers prefer explicit ``data-gd-field``/``data-gd-record`` hooks used by
fixtures and adapters, then fall back to common ``data-test``/``data-testid``
attributes. Missing values remain ``None`` instead of being guessed.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from html.parser import HTMLParser

from .errors import GlassdoorConnectorError
from .models import (
    BenefitData,
    BenefitRecord,
    CompanyOverview,
    ConnectorState,
    ErrorCode,
    InterviewData,
    RatingBreakdown,
    ReviewRecord,
    ReviewSummary,
    SalaryData,
    SalaryRecord,
)
from .resolver import company_from_url


class _Node:
    def __init__(self, tag: str, attrs: dict[str, str], parent: _Node | None = None):
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children: list[_Node] = []
        self.data: list[str] = []

    @property
    def text(self) -> str:
        parts = [*self.data]
        for child in self.children:
            parts.append(child.text)
        return re.sub(r"\s+", " ", " ".join(parts)).strip()

    def walk(self) -> Iterable[_Node]:
        yield self
        for child in self.children:
            yield from child.walk()


class _TreeParser(HTMLParser):
    _VOID = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "source",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Node("document", {})
        self._stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = _Node(tag, {key: value or "" for key, value in attrs}, self._stack[-1])
        self._stack[-1].children.append(node)
        if tag not in self._VOID:
            self._stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self._VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                break

    def handle_data(self, data: str) -> None:
        self._stack[-1].data.append(data)


def _tree(html: str) -> _Node:
    parser = _TreeParser()
    parser.feed(html)
    return parser.root


def _matches(node: _Node, key: str, value: str) -> bool:
    return node.attrs.get(key, "").casefold() == value.casefold()


def _find(root: _Node, name: str) -> _Node | None:
    aliases = (name, name.replace("_", "-"))
    for node in root.walk():
        for attr in ("data-gd-field", "data-test", "data-testid"):
            if any(_matches(node, attr, alias) for alias in aliases):
                return node
    return None


def _value(root: _Node, name: str) -> str | None:
    node = _find(root, name)
    if not node:
        return None
    return node.attrs.get("content") or node.attrs.get("value") or node.text or None


def _records(root: _Node, kind: str) -> list[_Node]:
    return [
        node
        for node in root.walk()
        if _matches(node, "data-gd-record", kind)
        or _matches(node, "data-testid", f"{kind}-record")
    ]


def _number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"-?\d[\d,.]*", value)
    if not match:
        return None
    token = match.group().rstrip(".,")
    if "," in token and "." not in token:
        final_group = token.rsplit(",", 1)[-1]
        token = token.replace(",", ".") if len(final_group) <= 2 else token.replace(",", "")
    elif "," in token:
        token = token.replace(",", "")
    return float(token)


def _integer(value: str | None) -> int | None:
    number = _number(value)
    return int(number) if number is not None else None


def _year(value: str | None) -> int | None:
    match = re.search(r"\b(?:18|19|20)\d{2}\b", value or "")
    return int(match.group()) if match else None


def _rating(root: _Node, name: str) -> float | None:
    return _number(_value(root, name))


def _ratings(root: _Node) -> RatingBreakdown:
    return RatingBreakdown(
        overall=_rating(root, "overall_rating"),
        culture_and_values=_rating(root, "culture_and_values"),
        diversity_and_inclusion=_rating(root, "diversity_and_inclusion"),
        work_life_balance=_rating(root, "work_life_balance"),
        senior_management=_rating(root, "senior_management"),
        compensation_and_benefits=_rating(root, "compensation_and_benefits"),
        career_opportunities=_rating(root, "career_opportunities"),
    )


def _parse[T](
    html: str,
    source_url: str,
    page: str,
    factory: Callable[[_Node], T],
) -> T:
    if not html.strip():
        raise GlassdoorConnectorError(
            ErrorCode.PARSE_FAILED,
            f"The rendered {page} HTML was empty.",
            state=ConnectorState.UNSUPPORTED,
        )
    root = _tree(html)
    try:
        return factory(root)
    except GlassdoorConnectorError:
        raise
    except (TypeError, ValueError) as exc:
        raise GlassdoorConnectorError(
            ErrorCode.PARSE_FAILED,
            f"Could not parse the Glassdoor {page} page.",
            state=ConnectorState.UNSUPPORTED,
            details={"url": source_url, "reason": str(exc)},
        ) from exc


def parse_company_overview(html: str, source_url: str) -> CompanyOverview:
    def build(root: _Node) -> CompanyOverview:
        return CompanyOverview(
            company=company_from_url(source_url, _value(root, "company_name")),
            description=_value(root, "description"),
            headquarters=_value(root, "headquarters"),
            size=_value(root, "size"),
            founded=_year(_value(root, "founded")),
            industry=_value(root, "industry"),
            website=_value(root, "website"),
            ratings=_ratings(root),
        )

    return _parse(html, source_url, "overview", build)


def parse_reviews(html: str, source_url: str) -> ReviewSummary:
    def build(root: _Node) -> ReviewSummary:
        highlights = [node.text for node in _records(root, "review-highlight") if node.text]
        records = []
        seen: set[str] = set()
        for node in _records(root, "review"):
            review_id = node.attrs.get("data-review-id") or _value(node, "review_id")
            dedupe_key = review_id or "|".join(
                filter(
                    None,
                    (
                        _value(node, "date"),
                        _value(node, "headline"),
                        _value(node, "job_title"),
                    ),
                )
            )
            if dedupe_key and dedupe_key in seen:
                continue
            if dedupe_key:
                seen.add(dedupe_key)
            records.append(
                ReviewRecord(
                    review_id=review_id,
                    permalink=_value(node, "permalink"),
                    date=_value(node, "date"),
                    headline=_value(node, "headline"),
                    job_title=_value(node, "job_title"),
                    location=_value(node, "location"),
                    employment_status=_value(node, "employment_status"),
                    tenure=_value(node, "tenure"),
                    overall_rating=_number(_value(node, "overall_rating")),
                    pros=_value(node, "pros"),
                    cons=_value(node, "cons"),
                    advice_to_management=_value(node, "advice_to_management"),
                    helpful_count=_integer(_value(node, "helpful_count")),
                )
            )
        return ReviewSummary(
            company=company_from_url(source_url, _value(root, "company_name")),
            total_reviews=_integer(_value(root, "total_reviews")),
            recommend_to_friend_percent=_integer(_value(root, "recommend_to_friend")),
            ceo_approval_percent=_integer(_value(root, "ceo_approval")),
            positive_outlook_percent=_integer(_value(root, "positive_outlook")),
            ratings=_ratings(root),
            highlights=highlights,
            records=records,
        )

    return _parse(html, source_url, "reviews", build)


def parse_salaries(html: str, source_url: str) -> SalaryData:
    def build(root: _Node) -> SalaryData:
        rows = []
        for node in _records(root, "salary"):
            title = _value(node, "title")
            if not title:
                continue
            rows.append(
                SalaryRecord(
                    title=title,
                    location=_value(node, "location"),
                    pay_period=_value(node, "pay_period"),
                    currency=_value(node, "currency"),
                    base_low=_number(_value(node, "base_low")),
                    base_high=_number(_value(node, "base_high")),
                    base_median=_number(_value(node, "base_median")),
                    additional_median=_number(_value(node, "additional_median")),
                    sample_size=_integer(_value(node, "sample_size")),
                )
            )
        return SalaryData(
            company=company_from_url(source_url, _value(root, "company_name")),
            records=rows,
        )

    return _parse(html, source_url, "salaries", build)


def parse_benefits(html: str, source_url: str) -> BenefitData:
    def build(root: _Node) -> BenefitData:
        rows = []
        for node in _records(root, "benefit"):
            name = _value(node, "name")
            if name:
                rows.append(
                    BenefitRecord(
                        name=name,
                        rating=_number(_value(node, "rating")),
                        review_count=_integer(_value(node, "review_count")),
                        description=_value(node, "description"),
                    )
                )
        return BenefitData(
            company=company_from_url(source_url, _value(root, "company_name")),
            overall_rating=_number(_value(root, "benefits_rating")),
            records=rows,
        )

    return _parse(html, source_url, "benefits", build)


def parse_interviews(html: str, source_url: str) -> InterviewData:
    def build(root: _Node) -> InterviewData:
        stages = [node.text for node in _records(root, "interview-stage") if node.text]
        return InterviewData(
            company=company_from_url(source_url, _value(root, "company_name")),
            total_interviews=_integer(_value(root, "total_interviews")),
            positive_percent=_integer(_value(root, "positive_experience")),
            negative_percent=_integer(_value(root, "negative_experience")),
            neutral_percent=_integer(_value(root, "neutral_experience")),
            difficulty=_number(_value(root, "difficulty")),
            duration=_value(root, "duration"),
            common_stages=stages,
        )

    return _parse(html, source_url, "interviews", build)
