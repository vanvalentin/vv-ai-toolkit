"""Serialized, read-only browser lifecycle for Glassdoor.

Patchright is preferred when installed; Playwright is a compatible fallback.
No clicks, form submissions, CAPTCHA handling, or website mutations occur here.
"""

from __future__ import annotations

import asyncio
import os
import random
import shutil
import sys
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib import import_module
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field, model_validator

from .errors import ChallengeDetected, GlassdoorConnectorError, UnsupportedPage
from .models import (
    ConnectorErrorInfo,
    ConnectorState,
    ErrorCode,
    SessionStatus,
    ViabilityReport,
)
from .resolver import _is_allowed_glassdoor_host

GLASSDOOR_HOME = "https://www.glassdoor.com/"
GLASSDOOR_LOGIN = "https://www.glassdoor.com/profile/login_input.htm"
_LOCKS: dict[str, asyncio.Lock] = {}


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().casefold() in {"1", "true", "yes", "on"}


def default_profile_directory() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / "vv-ai-toolkit" / "browser-profiles" / "glassdoor"
    if sys.platform == "darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "vv-ai-toolkit"
            / "browser-profiles"
            / "glassdoor"
        )
    return Path.home() / ".local" / "share" / "vv-ai-toolkit" / "browser-profiles" / "glassdoor"


def _repository_root() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    return None


class BrowserConfig(BaseModel):
    profile_directory: Path = Field(default_factory=default_profile_directory)
    headless: bool = True
    collection_headless: bool = Field(
        default_factory=lambda: _env_bool("GLASSDOOR_HEADLESS", False)
    )
    navigation_timeout_ms: int = Field(default=45_000, ge=5_000, le=180_000)
    pace_min_seconds: float = Field(default=2.0, ge=1.0, le=30.0)
    pace_max_seconds: float = Field(default=4.0, ge=1.0, le=60.0)
    lock_timeout_seconds: float = Field(default=10.0, ge=1.0, le=120.0)

    @model_validator(mode="after")
    def validate_safety(self) -> BrowserConfig:
        if self.pace_max_seconds < self.pace_min_seconds:
            raise ValueError("pace_max_seconds must be at least pace_min_seconds")
        profile = self.profile_directory.expanduser().resolve()
        root = _repository_root()
        if root and (profile == root or root in profile.parents):
            raise ValueError("Glassdoor browser profiles must be stored outside the repository")
        self.profile_directory = profile
        return self


class _ProfileFileLock:
    def __init__(self, profile: Path, timeout: float) -> None:
        self.path = profile / ".connector.lock"
        self.timeout = timeout
        self._file: Any = None

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("a+b")
        if self._file.tell() == 0:
            self._file.write(b"\0")
            self._file.flush()
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self._file.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(self._file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except OSError:
                if time.monotonic() >= deadline:
                    self._file.close()
                    self._file = None
                    raise TimeoutError(
                        "Another Glassdoor browser session owns the profile"
                    ) from None
                time.sleep(0.1)

    def release(self) -> None:
        if not self._file:
            return
        self._file.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(self._file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
        self._file.close()
        self._file = None


def _load_backend() -> tuple[Any, str]:
    failures: list[str] = []
    for package in ("patchright.async_api", "playwright.async_api"):
        try:
            return import_module(package).async_playwright, package.split(".", 1)[0]
        except ImportError as exc:
            failures.append(f"{package}: {exc}")
    raise GlassdoorConnectorError(
        ErrorCode.BROWSER_UNAVAILABLE,
        "Install Patchright or Playwright and its Chromium browser.",
        state=ConnectorState.UNAVAILABLE,
        details={"imports": failures},
    )


def glassdoor_regional_base(url: str) -> str:
    """Return the Glassdoor site root for the locale implied by *url*."""
    host = (urlparse(url).hostname or "www.glassdoor.com").lower()
    if host.endswith(".com.hk") or host.endswith("glassdoor.com.hk"):
        return "https://www.glassdoor.com.hk"
    return "https://www.glassdoor.com"


def _is_authenticated_glassdoor_url(url: str) -> bool:
    """Recognise common post-login regional landing pages when DOM markers are sparse."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = (parsed.path or "/").casefold()
    if "login" in path or "authwall" in path:
        return False
    return host.endswith("glassdoor.com.hk") and path.startswith("/community/")


def classify_session(url: str, html: str) -> SessionStatus:
    """Classify visible browser state without attempting to defeat challenges."""
    html_sample = html[:250_000].casefold()
    combined = f"{url}\n{html_sample}"
    auth_markers = (
        'data-test="header-member-menu"',
        'data-testid="header-member-menu"',
        'data-gd-authenticated="true"',
    )
    if any(marker in combined for marker in auth_markers) or _is_authenticated_glassdoor_url(
        url
    ):
        return SessionStatus(
            state=ConnectorState.AUTHENTICATED,
            authenticated=True,
            current_url=url,
        )

    parsed = urlparse(url)
    path = (parsed.path or "/").casefold()
    challenge_markers = (
        "captcha",
        "/challenge/",
        "verify you are human",
        "unusual activity",
        "security check",
    )
    if any(marker in html_sample for marker in challenge_markers) or "/challenge/" in path:
        return SessionStatus(
            state=ConnectorState.CHALLENGE,
            current_url=url,
            message="A verification challenge requires manual completion.",
        )
    if "login_input" in combined or 'data-gd-authenticated="false"' in combined:
        return SessionStatus(
            state=ConnectorState.UNAUTHENTICATED,
            current_url=url,
            message="No authenticated Glassdoor session was detected.",
        )
    return SessionStatus(
        state=ConnectorState.READY,
        current_url=url,
        message="Glassdoor loaded, but authentication could not be determined.",
    )


class GlassdoorBrowser:
    def __init__(self, config: BrowserConfig | None = None) -> None:
        self.config = config or BrowserConfig()
        self.backend_name: str | None = None
        self._last_navigation = 0.0

    @asynccontextmanager
    async def session(self, *, headless: bool | None = None) -> AsyncIterator[Any]:
        key = os.path.normcase(str(self.config.profile_directory))
        process_lock = _LOCKS.setdefault(key, asyncio.Lock())
        async with process_lock:
            file_lock = _ProfileFileLock(
                self.config.profile_directory, self.config.lock_timeout_seconds
            )
            try:
                await asyncio.to_thread(file_lock.acquire)
            except TimeoutError as exc:
                raise GlassdoorConnectorError(
                    ErrorCode.CONFIGURATION,
                    str(exc),
                    state=ConnectorState.UNAVAILABLE,
                    retryable=True,
                ) from exc
            try:
                async_playwright, self.backend_name = _load_backend()
                async with async_playwright() as runtime:
                    resolved_headless = (
                        self.config.headless if headless is None else headless
                    )
                    context = await runtime.chromium.launch_persistent_context(
                        user_data_dir=str(self.config.profile_directory),
                        headless=resolved_headless,
                    )
                    context.set_default_navigation_timeout(self.config.navigation_timeout_ms)
                    try:
                        page = context.pages[0] if context.pages else await context.new_page()
                        yield page
                    finally:
                        await context.close()
            finally:
                await asyncio.to_thread(file_lock.release)

    @asynccontextmanager
    async def collection_session(self) -> AsyncIterator[Any]:
        """Open the persistent profile for data collection (headed by default)."""
        async with self.session(headless=self.config.collection_headless) as page:
            yield page

    async def _pace(self) -> None:
        target = random.uniform(
            self.config.pace_min_seconds, self.config.pace_max_seconds
        )
        elapsed = time.monotonic() - self._last_navigation
        if elapsed < target:
            await asyncio.sleep(target - elapsed)

    async def rendered_html(
        self,
        page: Any,
        url: str,
        *,
        allow_challenge: bool = False,
    ) -> str:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        if parsed.scheme != "https" or not _is_allowed_glassdoor_host(host):
            raise UnsupportedPage(url)
        await self._pace()
        try:
            await page.goto(url, wait_until="domcontentloaded")
            self._last_navigation = time.monotonic()
            html = await page.content()
        except Exception as exc:
            raise GlassdoorConnectorError(
                ErrorCode.NAVIGATION_FAILED,
                "Glassdoor navigation failed.",
                state=ConnectorState.UNAVAILABLE,
                retryable=True,
                details={"url": url, "reason": str(exc)},
            ) from exc
        status = classify_session(page.url, html)
        if status.state == ConnectorState.CHALLENGE and not allow_challenge:
            raise ChallengeDetected()
        return html


async def warm_authenticated_session(page: Any) -> str:
    """Load the regional site and return its base URL for follow-on navigation."""
    await page.goto(GLASSDOOR_HOME, wait_until="domcontentloaded")
    status = await _probe_session_status(page, await page.content())
    if status.state == ConnectorState.CHALLENGE:
        raise ChallengeDetected()
    if not status.authenticated:
        raise GlassdoorConnectorError(
            ErrorCode.AUTH_REQUIRED,
            "A manual Glassdoor login is required.",
            state=ConnectorState.UNAUTHENTICATED,
        )
    return glassdoor_regional_base(page.url)


async def _probe_session_status(page: Any, html: str | None = None) -> SessionStatus:
    """Probe the regional Glassdoor site, including HK community landing pages."""
    content = html if html is not None else await page.content()
    status = classify_session(page.url, content)
    if status.authenticated:
        return status

    probe_urls = [f"{glassdoor_regional_base(page.url)}/Community/index.htm"]
    if "glassdoor.com.hk" not in page.url.casefold():
        probe_urls.append("https://www.glassdoor.com.hk/Community/index.htm")

    for community_url in probe_urls:
        if page.url.rstrip("/").casefold() == community_url.rstrip("/").casefold():
            continue
        await page.goto(community_url, wait_until="domcontentloaded")
        await asyncio.sleep(1.0)
        status = classify_session(page.url, await page.content())
        if status.authenticated:
            return status
    return status


async def session_status(config: BrowserConfig | None = None) -> SessionStatus:
    browser = GlassdoorBrowser(config)
    async with browser.session() as page:
        html = await browser.rendered_html(page, GLASSDOOR_HOME, allow_challenge=True)
        return await _probe_session_status(page, html)


async def manual_login(
    config: BrowserConfig | None = None,
    *,
    timeout_seconds: float = 300,
) -> SessionStatus:
    """Open a headed login page and wait for the user to authenticate manually."""
    browser = GlassdoorBrowser(config)
    async with browser.session(headless=False) as page:
        await browser.rendered_html(page, GLASSDOOR_LOGIN, allow_challenge=True)
        deadline = time.monotonic() + timeout_seconds
        last_status = classify_session(page.url, await page.content())
        while time.monotonic() < deadline:
            last_status = classify_session(page.url, await page.content())
            if last_status.authenticated:
                return last_status
            await asyncio.sleep(1.0)
        if last_status.state == ConnectorState.CHALLENGE:
            last_status.message = (
                "The manual login window timed out while a verification challenge "
                "was still visible."
            )
            return last_status
        return SessionStatus(
            state=ConnectorState.UNAUTHENTICATED,
            current_url=page.url,
            message="Manual login window timed out without a detectable session.",
        )


async def logout(config: BrowserConfig | None = None) -> SessionStatus:
    """Delete only local browser session data; no Glassdoor logout request is sent."""
    selected = config or BrowserConfig()
    browser = GlassdoorBrowser(selected)
    async with browser.session() as page:
        await page.context.clear_cookies()
    await asyncio.to_thread(shutil.rmtree, selected.profile_directory, True)
    return SessionStatus(
        state=ConnectorState.UNAUTHENTICATED,
        authenticated=False,
        message="The dedicated local Glassdoor browser profile was cleared.",
    )


async def check_viability(config: BrowserConfig | None = None) -> ViabilityReport:
    selected = config or BrowserConfig()
    writable = False
    try:
        selected.profile_directory.mkdir(parents=True, exist_ok=True)
        probe = selected.profile_directory / ".write-probe"
        probe.write_text("", encoding="utf-8")
        probe.unlink()
        writable = True
        browser = GlassdoorBrowser(selected)
        async with browser.session() as page:
            html = await browser.rendered_html(
                page,
                GLASSDOOR_HOME,
                allow_challenge=True,
            )
            status = await _probe_session_status(page, html)
            return ViabilityReport(
                state=status.state,
                browser_backend=browser.backend_name,
                profile_directory=selected.profile_directory,
                profile_writable=writable,
                homepage_reachable=True,
                session=status,
            )
    except GlassdoorConnectorError as exc:
        return ViabilityReport(
            state=exc.info.state,
            browser_backend=None,
            profile_directory=selected.profile_directory,
            profile_writable=writable,
            error=exc.info,
        )
    except OSError as exc:
        error = ConnectorErrorInfo(
            code=ErrorCode.CONFIGURATION,
            message="The browser profile directory is not writable.",
            state=ConnectorState.UNAVAILABLE,
            details={"reason": str(exc)},
        )
        return ViabilityReport(
            state=ConnectorState.UNAVAILABLE,
            profile_directory=selected.profile_directory,
            profile_writable=False,
            error=error,
        )
