import json
import os
import tomllib
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

WORKSPACE_DIR = Path(__file__).resolve().parents[2]


def test_all_clients_launch_the_same_stdio_module() -> None:
    cursor = json.loads((WORKSPACE_DIR / ".cursor" / "mcp.json").read_text(encoding="utf-8"))
    claude = json.loads((WORKSPACE_DIR / ".mcp.json").read_text(encoding="utf-8"))
    codex = tomllib.loads(
        (WORKSPACE_DIR / ".codex" / "config.toml").read_text(encoding="utf-8")
    )

    cursor_server = cursor["mcpServers"]["offer-intel"]
    claude_server = claude["mcpServers"]["offer-intel"]
    codex_server = codex["mcp_servers"]["offer-intel"]

    assert cursor_server["type"] == claude_server["type"] == "stdio"
    servers = (cursor_server, claude_server, codex_server)
    assert all(server["args"] == ["-m", "offer_intel"] for server in servers)
    assert cursor_server["command"].endswith(".venv/bin/python")
    assert claude_server["command"].endswith(".venv/bin/python")
    assert codex_server["command"] == ".venv/bin/python"
    assert cursor_server["cwd"] == "${workspaceFolder}"
    assert claude_server["cwd"] == "${CLAUDE_PROJECT_DIR}"
    assert codex_server["cwd"] == "."
    assert all(
        server.get("env", {}).get("FASTMCP_SHOW_SERVER_BANNER") == "false"
        for server in (cursor_server, claude_server)
    )
    assert codex_server["env"]["FASTMCP_SHOW_SERVER_BANNER"] == "false"


def test_portable_skill_and_claude_adapter_share_the_name() -> None:
    canonical = (
        WORKSPACE_DIR / ".agents" / "skills" / "job-offer-evaluation" / "SKILL.md"
    ).read_text(encoding="utf-8")
    claude = (
        WORKSPACE_DIR / ".claude" / "skills" / "job-offer-evaluation" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "name: job-offer-evaluation" in canonical
    assert "name: job-offer-evaluation" in claude
    assert "offer-intelligence/methodology.md" in canonical
    assert "offer-intelligence/methodology.md" in claude


@pytest.mark.asyncio
async def test_project_interpreter_launches_the_stdio_server() -> None:
    interpreter = (
        WORKSPACE_DIR / ".venv" / "Scripts" / "python.exe"
        if os.name == "nt"
        else WORKSPACE_DIR / ".venv" / "bin" / "python"
    )
    transport = StdioTransport(
        command=str(interpreter),
        args=["-m", "offer_intel"],
        cwd=str(WORKSPACE_DIR),
        keep_alive=False,
    )
    async with Client(transport) as client:
        names = {tool.name for tool in await client.list_tools()}

    assert {
        "create_offer_case",
        "linkedin_collect_company",
        "glassdoor_collect_company",
        "validate_offer_report",
    } <= names
