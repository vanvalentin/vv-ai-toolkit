# Career toolkit

Optional, self-contained workflows for evidence-first job-offer evaluation and CV-plus-job-description interview preparation.

This toolkit is retained as a secondary part of the repository. Its client-specific files live here so they activate only when `toolkits/career/` is opened as the project root.

## Included workflows

- [Offer Intelligence](offer-intelligence/README.md) — local MCP gateway and methodology for employer, role, candidate-fit, and compensation research.
- [Interview preparation](interview-prep/README.md) — Agent Skill and methodology for preparation packs and optional mock rounds.

## Client integration files

- `.agents/skills/` — canonical portable Agent Skills, including Pi discovery.
- `.claude/skills/` — thin Claude Code discovery adapters.
- `.codex/config.toml` — Codex MCP registration.
- `.cursor/mcp.json` — Cursor MCP registration.
- `.mcp.json` — Claude Code MCP registration.
- `CLAUDE.md` — toolkit-local Claude guidance.

These files are intentional here, but should not be moved to the repository root: the career toolkit is optional and should not configure unrelated Pi platform work.

## Setup

From the repository root:

```bash
cd toolkits/career
python3 offer-intelligence/scripts/setup.py
```

Then open `toolkits/career/`—not the repository root—as the project in Cursor, Claude Code, Codex, or another Agent Skills-compatible client. Restart the client after initial setup and confirm that the `offer-intel` MCP tools are available.

For browser-backed LinkedIn research:

```bash
python offer-intelligence/scripts/linkedin_login.py
```

See the [Offer Intelligence guide](offer-intelligence/README.md) for privacy, authentication, verification, and troubleshooting details.

## Privacy

Use redacted inputs. Do not commit CVs, offer documents, contact details, credentials, browser profiles, session cookies, private case artifacts, or generated reports containing personal information.
