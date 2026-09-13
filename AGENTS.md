# Agent guidance

## Job offer evaluation

For job-offer, role, or employer assessments:

1. Read `.agents/skills/job-offer-evaluation/SKILL.md`.
2. Treat `experts/job-offer-evaluation/methodology.md` as the canonical methodology.
3. Use the `offer-intel` MCP server for public research when available.
4. Cite decision-relevant factual claims and separate evidence from inference.
5. State assumptions, missing evidence, source failures, and confidence.
6. Minimize personal data and never place credentials or private source material in
   repository files, prompts, logs, or reports.

Live access to third-party sites, including Glassdoor, is not guaranteed. Do not bypass
authentication, CAPTCHAs, paywalls, rate limits, or other access controls.

## Self-hosted specialist platform

For work on the Pi Discord Specialists blueprint:

1. Read `platforms/pi-discord-specialists/README.md` and its linked architecture,
   security, and operations documents.
2. Keep examples portable: do not copy production paths, account identifiers,
   network details, service state, logs, sessions, or specialist memory.
3. Preserve least privilege: ordinary specialists have no built-in filesystem or shell
   tools; capabilities are exposed through bounded extension tools.
4. Treat personas as guidance and enforce security controls in code or service policy.
5. Keep model/provider choices configurable because availability and pricing change.

## Interview preparation

For interview prep, STAR stories, or mock interview practice from a CV and JD:

1. Read `.agents/skills/interview-prep/SKILL.md`.
2. Treat `experts/interview-prep/methodology.md` as the canonical methodology.
3. Deliver a prep pack before optional mock rounds unless the user asks for mock-only.
4. Use the `offer-intel` MCP server for public employer/interview-process research when
   available; continue from CV+JD when it is not.
5. Never invent experience, metrics, or credentials; encourage a redacted CV.
6. Minimize personal data and never place credentials or private source material in
   repository files, prompts, logs, or reports.

## Public-repository gate

Before committing or publishing changes, run:

```bash
python3 scripts/check_public_repo.py
```

Also review the staged diff manually. The script is a high-confidence safety check, not
proof that every personal or confidential detail has been removed.
