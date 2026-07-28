@AGENTS.md

# Claude-specific guidance

Use `.claude/skills/job-offer-evaluation/SKILL.md` for job-offer and employer
assessments. It delegates to the canonical process in
`experts/job-offer-evaluation/methodology.md` and
`.agents/skills/job-offer-evaluation/SKILL.md`.

The project MCP server is `offer-intel`. Use it only for public research, cite
decision-relevant claims, and disclose blocked or unavailable sources. Distinguish
posting claims, user-provided facts, inferences, and unverified claims. Never assume
that Glassdoor or another third-party site is accessible.

Ask users to redact unnecessary personal or confidential data. Do not put secrets in
configuration, prompts, logs, or output, and do not bypass access controls.
