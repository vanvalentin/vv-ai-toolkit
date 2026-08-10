# Interview preparation

Agent Skill and methodology for preparing interviews from a CV and job description.
Produces a prep pack first, then optional mock rounds. Reuses the project
`offer-intel` MCP server for public employer and interview-process research when
available.

## What this expert does

- maps JD requirements to CV evidence and builds a STAR story bank;
- drafts likely questions, gap answers, "why us" points, and questions to ask;
- optionally enriches with public interview-process and company context via
  `offer-intel`;
- runs interactive mock interviews with a short scoring debrief.

It does not submit applications, invent experience, or guarantee hiring outcomes.
Glassdoor and similar sources may be blocked; prep continues from CV+JD when research
fails.

## Requirements

- Cursor, Claude Code, and/or Codex with Agent Skills discovery for this repository;
- optional: the Offer Intelligence environment and `offer-intel` MCP from
  [`../job-offer-evaluation/README.md`](../job-offer-evaluation/README.md) for employer
  research.

No separate Python package is required for interview prep itself.

## How to use

1. Open this repository in your client.
2. Ask to prep for an interview and provide the JD (text or URL) plus a redacted CV
   or experience summary.
3. The agent should load `.agents/skills/interview-prep/SKILL.md` (Claude discovery
   via `.claude/skills/interview-prep/SKILL.md`).
4. Review the prep pack, then request mock rounds if you want practice.

Example prompts:

```text
Prep me for the hiring-manager interview using my CV and this JD: <url or paste>
```

```text
Run a 5-question behavioral mock based on the prep pack we just built.
```

## Privacy

- Prefer a redacted CV (strip contact details and unnecessary identifiers).
- Do not commit CVs, interview recordings, or confidential employer materials.
- Use anonymized examples if documenting fixtures later.

## Files

| Path | Role |
| --- | --- |
| [`methodology.md`](methodology.md) | Canonical process and output contracts |
| [`.agents/skills/interview-prep/SKILL.md`](../../.agents/skills/interview-prep/SKILL.md) | Portable skill instructions |
| [`.claude/skills/interview-prep/SKILL.md`](../../.claude/skills/interview-prep/SKILL.md) | Thin Claude discovery adapter |

## Related

- [Job offer evaluation](../job-offer-evaluation/README.md) — pursue/decline decisions
  and deeper employer research; share `offer-intel` evidence when useful.
