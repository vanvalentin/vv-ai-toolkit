@AGENTS.md

# Claude-specific guidance

Use `.claude/skills/job-offer-evaluation/SKILL.md` for job-offer and employer
assessments. It delegates to the canonical process in
`offer-intelligence/methodology.md` and
`.agents/skills/job-offer-evaluation/SKILL.md`.

Use `.claude/skills/interview-prep/SKILL.md` for interview prep and mock practice from
a CV and JD. It delegates to `interview-prep/methodology.md` and
`.agents/skills/interview-prep/SKILL.md`.

The project MCP server is `offer-intel`. Use it only for public research, cite
decision-relevant claims, and disclose blocked or unavailable sources. Distinguish
posting claims, user-provided facts, inferences, and unverified claims. Never assume
that Glassdoor or another third-party site is accessible. Never invent interview
experience or metrics.

Ask users to redact unnecessary personal or confidential data. Do not put secrets in
configuration, prompts, logs, or output, and do not bypass access controls.
