# Interview preparation methodology

Canonical method for preparing a candidate for interviews from a CV and job
description (JD). Designed for evidence-backed prep and optional mock practice — not
to invent experience or guarantee interview outcomes.

## Principles

1. **CV and JD first.** Map the posting to demonstrated experience before researching
   the employer.
2. **Honest fit.** Separate demonstrated matches, transferable bridges, learnable gaps,
   and material gaps. Never fabricate employment history, metrics, or credentials.
3. **Prep before mock.** Produce a prep pack, then offer mock rounds only if the user
   wants practice.
4. **Research is optional enrichment.** Use `offer-intel` for public interview-process
   and employer context when available; continue from CV+JD when it is not.
5. **Privacy by default.** Prefer a redacted CV. Do not commit CVs, offer letters, or
   confidential interview materials to the repository.
6. **Uncertainty is visible.** Label posting claims, user-provided facts, inferences,
   and unverified third-party interview anecdotes.

## Decision modes

Identify which mode the user wants:

| Mode | Goal |
| --- | --- |
| **Prep pack** | One-shot briefing: likely questions, story bank, gaps, questions to ask |
| **Mock interview** | Interactive Q&A with scoring and coaching |
| **Both** (default) | Prep pack first, then optional mock rounds |

If the user only asks to "prep for an interview," run **Both** and pause after the
prep pack before starting mocks.

## 1. Required inputs

Ask only for what changes the prep:

- JD text or URL (required);
- CV or a short experience summary (required for story mapping; a redacted profile is
  enough);
- interview stage if known (recruiter screen, hiring manager, panel, technical,
  system design, behavioral, offer/comp);
- role seniority and location/work arrangement when not obvious from the JD;
- any topics the user especially wants to practice or avoid.

Do not require unredacted contact details, government IDs, salary history, or current
employer secrets. Encourage stripping names, addresses, phone numbers, and private
links when the user pastes a CV.

If the CV is missing, build a prep pack from the JD alone with clearly labeled
**story placeholders** the user must fill, and skip graded mock scoring.

## 2. Normalize the JD

Preserve the posting URL and access date when available. Extract:

- title, employer, team, location, remote/hybrid, employment type;
- responsibilities and outcomes;
- required vs preferred skills, tools, domain knowledge, and seniority signals;
- interview-process statements in the posting;
- ambiguous or unusually broad requirements.

Quote only short passages needed to justify likely questions or gap callouts.

## 3. Map CV to JD

For each material JD requirement or responsibility, classify evidence from the CV:

| Label | Meaning |
| --- | --- |
| **Demonstrated** | Direct evidence with a usable story |
| **Transferable** | Adjacent evidence with a credible bridge sentence |
| **Learnable** | Can be addressed as growth plan or recent learning |
| **Material gap** | Likely probing risk; prepare an honest answer |
| **Unknown** | Insufficient CV detail; ask the user or mark placeholder |

Prefer fewer strong stories over many thin ones. Cap the core story bank at roughly
6–10 STAR narratives unless the user asks for more.

### Story quality bar

Each prepared story should have:

- **Situation** — context in one or two sentences;
- **Task** — the user's ownership;
- **Action** — concrete steps the user took (tools, decisions, trade-offs);
- **Result** — outcome with metrics when the user provided them;
- **JD link** — which requirement or theme it supports.

Do not invent metrics. If the CV lacks numbers, coach the user to add honest
approximations later rather than fabricating them in the prep pack.

## 4. Optional public research (`offer-intel`)

When the gateway is available and the employer is known, enrich prep — do not replace
the CV↔JD map.

### Research targets for interview prep

Prioritize signals that change questions or framing:

1. stated interview process on careers pages or the posting;
2. Glassdoor/interview-aggregator process themes (stages, question themes, difficulty)
   when accessible;
3. company product, customers, and recent news useful for "why us" and domain questions;
4. tech/stack or domain clues from first-party engineering/blog pages when relevant.

Skip full offer-evaluation scorecards unless the user also asked for an offer decision.

### MCP sequence (when available)

1. Resolve the employer with host web search before LinkedIn/Glassdoor calls (same
   disambiguation rules as job-offer evaluation).
2. `create_offer_case` with minimum redacted input.
3. Collect company and interview-process material via connectors; add host-found facts
   with `add_external_evidence`.
4. Inspect `get_evidence_pack` for conflicts and blind spots.
5. Use interview-process and company-context evidence in the prep pack with citations.
6. Do **not** require `score_offer_case` or `validate_offer_report` for prep-only work
   unless producing a joint evaluation+prep deliverable.

If research fails, is blocked, or the user wants speed, continue with CV+JD and mark
employer interview anecdotes as unavailable.

Treat Glassdoor interview reports as **anecdotal and self-selected**. Prefer recurring
themes over single posts. Never present them as the employer's official process.

## 5. Prep pack output contract

Produce a decision-useful pack proportional to the stage. Default sections:

1. **Interview brief** — role, employer, stage, format assumptions, confidence.
2. **Fit map** — demonstrated / transferable / learnable / material gaps with CV
   anchors.
3. **Likely questions** — grouped by type (motivational, behavioral, role/technical,
   company/product, compensation/logistics when stage-appropriate). Tag each with why
   it is likely (JD bullet, seniority, research theme, or common practice).
4. **Story bank** — STAR outlines linked to JD themes; note missing metrics.
5. **Gap answers** — honest frames for material and learnable gaps (no resume
   inflation).
6. **"Why this role / company"** — draft talking points from JD + verified company
   context; label inferences.
7. **Questions to ask them** — prioritized by what the user still needs to learn.
8. **Day-of checklist** — logistics, materials, and 3–5 rehearsal priorities.
9. **Sources and limits** — URLs, access dates, blocked research, assumptions.

Tone: direct coaching. Critique weak or generic answers. Do not flatter.

## 6. Mock interview protocol

Start mocks only after the prep pack (or when the user explicitly skips to mock).

### Setup

Confirm:

- round type (recruiter, HM, behavioral, technical deep-dive, system design, mixed);
- length (default: 5 questions or ~20–30 minutes of Q&A);
- difficulty (baseline from seniority in the JD);
- whether answers should be timed.

Play the interviewer. Stay in character during the round; put coaching in a short
debrief after each answer or at the end — ask the user which they prefer once.

### During the round

- Ask one question at a time.
- Follow up once or twice as a real interviewer would (clarify, probe depth, challenge
  inconsistencies).
- Do not reveal ideal answers mid-round unless the user asks for a hint.
- If the user invents experience not supported by the CV, flag it in the debrief —
  never reinforce fabricated claims.

### Debrief rubric (0–5 each)

| Dimension | Looks for |
| --- | --- |
| **Relevance** | Answers the question asked; tied to the JD |
| **Specificity** | Concrete actions, tools, constraints |
| **Impact** | Outcomes; honest about missing metrics |
| **Structure** | Clear arc; appropriate length |
| **Credibility** | Consistent with CV; no inflation |
| **Stage fit** | Depth matches interviewer type |

After scores: one strongest moment, one highest-leverage fix, and a tighter rewrite of
the weakest answer (optional second take).

Offer another round focused on weak dimensions or a different interviewer persona.

## 7. Confidence

Report prep confidence as:

- **High** — CV and JD are detailed; stage known; research themes consistent or
  unnecessary for this stage.
- **Medium** — usable stories with some gaps; stage or process partly assumed.
- **Low** — thin CV, vague JD, unknown stage, or research heavily blocked.

## 8. Safety and privacy

- Do not submit applications, message recruiters, or log into employer systems.
- Do not bypass CAPTCHAs, paywalls, or access controls when researching.
- Do not invent credentials, employers, degrees, or metrics.
- Do not coach discriminatory, deceptive, or illegal interview tactics.
- Do not put secrets, full unredacted CVs, or private offer terms into repo files.
- Do not present legal, immigration, or compensation advice as professional counsel.

## Relationship to job-offer evaluation

Interview prep optimizes for **performance in conversations**. Job-offer evaluation
optimizes for **whether to pursue the opportunity**. They may share `offer-intel`
evidence. Prefer the evaluation expert when the user is deciding apply/decline;
prefer this methodology when they are preparing to interview. If both are needed, run
evaluation first or keep the deliverables clearly separated.
