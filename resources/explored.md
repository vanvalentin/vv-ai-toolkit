# Explored resources

## Career intelligence and MCP

### LinkedIn MCP Server

- **URL:** https://github.com/stickerdaniel/linkedin-mcp-server
- **Reviewed:** 2026-07-28
- **Summary:** Apache-2.0 FastMCP server using a persistent authenticated browser
  session for profiles, companies, employees, jobs, and posts.
- **Decision:** Use behind a local allowlist that excludes messaging and connection
  actions. Record upstream versions and preserve source URLs.
- **Limitation:** Unofficial browser automation can break or lead to account
  restrictions. Authentication remains a manual user action.

### Glassdoor data access

- **URL:** https://www.glassdoor.com/
- **Reviewed:** 2026-07-28
- **Summary:** No usable public review/salary extraction API was identified. The
  implementation therefore uses a read-only, manually authenticated browser adapter
  with fixture-tested parsers and explicit challenge/authentication states.
- **Decision:** Keep the browser backend replaceable and fail closed when the rendered
  page cannot be verified.

### Agent Skills

- **URL:** https://agentskills.io/
- **Reviewed:** 2026-07-28
- **Summary:** Portable `SKILL.md` format supported by Cursor, Codex, and Claude Code,
  with client-specific discovery paths.
- **Decision:** Do not place optional client-discovery configuration at the repository
  root; cloned platform documentation should not auto-activate unrelated tools.
