"""Local, read-only Glassdoor browser connector.

The exported async functions can be wrapped directly by FastMCP tools, but this
module deliberately performs no server registration.
"""

from .browser import (
    BrowserConfig,
    check_viability,
    classify_session,
    default_profile_directory,
    logout,
    manual_login,
    session_status,
)
from .connector import GlassdoorConnector
from .errors import (
    AuthenticationRequired,
    ChallengeDetected,
    GlassdoorConnectorError,
    UnsupportedPage,
)
from .models import (
    BenefitData,
    BenefitRecord,
    CompanyIntel,
    CompanyOverview,
    CompanyRef,
    ConnectorErrorInfo,
    ConnectorState,
    InterviewData,
    RatingBreakdown,
    ReviewFilter,
    ReviewRecord,
    ReviewSummary,
    SalaryData,
    SalaryRecord,
    SessionStatus,
    ViabilityReport,
)
from .parsing import (
    parse_benefits,
    parse_company_overview,
    parse_interviews,
    parse_reviews,
    parse_salaries,
)
from .resolver import company_from_url, company_section_urls, resolve_company

__all__ = [
    "AuthenticationRequired",
    "BenefitData",
    "BenefitRecord",
    "BrowserConfig",
    "ChallengeDetected",
    "CompanyIntel",
    "CompanyOverview",
    "CompanyRef",
    "ConnectorErrorInfo",
    "ConnectorState",
    "GlassdoorConnector",
    "GlassdoorConnectorError",
    "InterviewData",
    "RatingBreakdown",
    "ReviewFilter",
    "ReviewRecord",
    "ReviewSummary",
    "SalaryData",
    "SalaryRecord",
    "SessionStatus",
    "UnsupportedPage",
    "ViabilityReport",
    "check_viability",
    "classify_session",
    "company_from_url",
    "company_section_urls",
    "default_profile_directory",
    "logout",
    "manual_login",
    "parse_benefits",
    "parse_company_overview",
    "parse_interviews",
    "parse_reviews",
    "parse_salaries",
    "resolve_company",
    "session_status",
]
