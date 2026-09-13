# Career toolkit agent guidance

## Job offer evaluation

For job-offer, role, or employer assessments:

1. Read `.agents/skills/job-offer-evaluation/SKILL.md`.
2. Treat `offer-intelligence/methodology.md` as the canonical methodology.
3. Use the `offer-intel` MCP server for public research when available.
4. Cite decision-relevant factual claims and separate evidence from inference.
5. State assumptions, missing evidence, source failures, and confidence.
6. Minimize personal data and never place credentials or private source material in repository files, prompts, logs, or reports.

Live access to third-party sites is not guaranteed. Do not bypass authentication, CAPTCHAs, paywalls, rate limits, or other access controls.

## Interview preparation

For interview prep, STAR stories, or mock interview practice from a CV and job description:

1. Read `.agents/skills/interview-prep/SKILL.md`.
2. Treat `interview-prep/methodology.md` as the canonical methodology.
3. Deliver a prep pack before optional mock rounds unless the user asks for mock-only.
4. Use the `offer-intel` MCP server for public employer/interview-process research when available; continue from user-provided material when it is not.
5. Never invent experience, metrics, or credentials; encourage a redacted CV.
6. Minimize personal data and never place credentials or private source material in repository files, prompts, logs, or reports.

## Workspace boundary

Open `toolkits/career/` as the project root when using its client integrations. The virtual environment, MCP configuration, agent skills, and Claude adapters are intentionally local to this toolkit.
