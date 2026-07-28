"""Restricted read-only adapter for stickerdaniel/linkedin-mcp-server."""

from __future__ import annotations

import asyncio
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, Field


class LinkedInUnavailable(RuntimeError):
    """The upstream LinkedIn MCP cannot be started or returned an invalid result."""


class LinkedInSnapshot(BaseModel):
    tool: str
    url: str | None = None
    sections: dict[str, str] = Field(default_factory=dict)
    references: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    section_errors: dict[str, dict[str, Any]] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    upstream_version: str = "latest-resolved-by-uvx"


class LinkedInConnector:
    """Calls a deliberately small allowlist; messaging tools are never exposed."""

    ALLOWED_TOOLS: ClassVar[frozenset[str]] = frozenset(
        {
            "search_companies",
            "get_company_profile",
            "get_company_posts",
            "get_company_employees",
            "get_person_profile",
            "search_jobs",
            "get_job_details",
        }
    )

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    @staticmethod
    def _find_uvx() -> str | None:
        discovered = shutil.which("uvx")
        if discovered:
            return discovered
        executable_dir = Path(sys.executable).parent
        for name in ("uvx.exe", "uvx"):
            candidate = executable_dir / name
            if candidate.is_file():
                return str(candidate)
        return None

    @staticmethod
    def status() -> dict[str, Any]:
        uvx = LinkedInConnector._find_uvx()
        return {
            "available": uvx is not None,
            "uvx_path": uvx,
            "package": "mcp-server-linkedin@latest",
            "allowed_tools": sorted(LinkedInConnector.ALLOWED_TOOLS),
            "excluded_capabilities": ["inbox", "conversation_search", "send_message"],
        }

    async def _call(self, tool: str, arguments: dict[str, Any]) -> LinkedInSnapshot:
        if tool not in self.ALLOWED_TOOLS:
            raise ValueError(f"LinkedIn tool is not allowlisted: {tool}")
        uvx = self._find_uvx()
        if uvx is None:
            raise LinkedInUnavailable(
                "uvx is not installed. Install uv, then authenticate with "
                "'uvx mcp-server-linkedin@latest --login'."
            )

        # Imported lazily so pure unit tests do not require spawning the upstream browser.
        from fastmcp import Client
        from fastmcp.client.transports import StdioTransport

        transport = StdioTransport(
            command=uvx,
            args=["mcp-server-linkedin@latest"],
            keep_alive=False,
        )
        async with self._lock, Client(transport) as client:
            result = await client.call_tool(tool, arguments)

        data = getattr(result, "data", None)
        if data is None:
            data = getattr(result, "structured_content", None)
        if hasattr(data, "model_dump"):
            data = data.model_dump(mode="json")
        if not isinstance(data, dict):
            raise LinkedInUnavailable(f"{tool} returned no structured object")
        return LinkedInSnapshot(
            tool=tool,
            url=data.get("url"),
            sections=data.get("sections") or {},
            references=data.get("references") or {},
            section_errors=data.get("section_errors") or {},
            raw=data,
        )

    async def search_companies(self, keywords: str) -> LinkedInSnapshot:
        return await self._call("search_companies", {"keywords": keywords})

    async def get_company_profile(
        self, company_slug: str, sections: str | None = "posts,jobs"
    ) -> LinkedInSnapshot:
        return await self._call(
            "get_company_profile",
            {"company_name": company_slug, "sections": sections},
        )

    async def get_company_employees(
        self, company_slug: str, keywords: str | None = None
    ) -> LinkedInSnapshot:
        return await self._call(
            "get_company_employees",
            {"company_name": company_slug, "keywords": keywords},
        )

    async def get_person_profile(
        self, linkedin_username: str, sections: str | None = "experience,skills"
    ) -> LinkedInSnapshot:
        return await self._call(
            "get_person_profile",
            {"linkedin_username": linkedin_username, "sections": sections},
        )

    async def search_jobs(self, keywords: str, location: str | None = None) -> LinkedInSnapshot:
        arguments: dict[str, Any] = {"keywords": keywords}
        if location:
            arguments["location"] = location
        return await self._call("search_jobs", arguments)

    async def get_job_details(self, job_id: str) -> LinkedInSnapshot:
        return await self._call("get_job_details", {"job_id": job_id})
