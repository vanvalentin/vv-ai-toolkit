---
name: interview-prep
description: >-
  Prepare for job interviews from a CV and job description: fit map, likely
  questions, STAR story bank, gap answers, questions to ask, then optional mock
  interview rounds with scored feedback. Use when the user asks to prep for an
  interview, practice interview questions, build STAR stories, or rehearse for a
  recruiter, hiring-manager, panel, or technical screen.
---

# Interview preparation

Use this skill when a user wants interview prep, mock practice, STAR stories, or
question rehearsal grounded in their CV and a job description. The canonical process
is in `interview-prep/methodology.md`; read it before a full prep pack or
graded mock.

For pursue/decline employer decisions, use `job-offer-evaluation` instead (or in
addition). This skill optimizes conversation performance, not offer scoring.

## Required inputs

Ask only for information that materially changes the prep:

- the JD text or URL;
- the CV or a short redacted experience summary;
- interview stage when known (recruiter, hiring manager, panel, technical, etc.);
- topics the user wants to emphasize or avoid.

Encourage redaction of names, addresses, contact details, IDs, and confidential
employer information. Proceed with labeled assumptions if stage or company research is
incomplete. Never invent employment history, metrics, or credentials.

## Default workflow

Unless the user asks for mock-only practice:

1. **Normalize the JD** — responsibilities, required vs preferred skills, seniority,
   process notes.
2. **Map CV → JD** — label demonstrated, transferable, learnable, material gap, or
   unknown for each material requirement.
3. **Optional research** — when `offer-intel` is available and the employer is known,
   collect public interview-process and company context (see below). If research is
   blocked or disproportionate, continue from CV+JD and disclose the limit.
4. **Deliver the prep pack** using the output contract in the methodology.
5. **Pause** — offer mock rounds; start them only if the user wants practice.

If the user explicitly wants a mock immediately, run a short setup (stage, length,
focus) and proceed; still avoid fabricating CV-unsupported claims.

### `offer-intel` research for prep

When the gateway is available:

1. Resolve ambiguous employers with host web search before LinkedIn/Glassdoor tools
   (same order as job-offer evaluation).
2. Call `create_offer_case` with minimum necessary, redacted input.
3. Collect company and interview-process material via read-only connectors; add
   host-collected facts with `add_external_evidence`.
4. Inspect `get_evidence_pack` for conflicts and blind spots.
5. Cite interview-process themes and company context in the prep pack. Treat review-
   site interview reports as anecdotal.
6. Skip `score_offer_case` / `validate_offer_report` unless the user also requested a
   full offer evaluation.

Never promise live Glassdoor access. Do not log in, bypass CAPTCHAs, or evade access
controls; the user alone may complete any manual connector login.

## Prep pack output

Keep the pack proportional to the stage. Include:

1. **Interview brief** — role, stage, format assumptions, confidence.
2. **Fit map** — strengths and gaps with CV anchors.
3. **Likely questions** — grouped and tagged with why each is likely.
4. **Story bank** — STAR outlines linked to JD themes; no invented metrics.
5. **Gap answers** — honest frames for weak spots.
6. **"Why this role / company"** — talking points; label inferences.
7. **Questions to ask them** — prioritized.
8. **Day-of checklist** — short rehearsal priorities.
9. **Sources and limits** — citations, blocked research, assumptions.

## Mock interview output

When running mocks:

1. Confirm round type, length (default 5 questions), and debrief style.
2. Ask one question at a time; probe like a real interviewer.
3. Score Relevance, Specificity, Impact, Structure, Credibility, and Stage fit (0–5).
4. Give the strongest moment, the highest-leverage fix, and an optional tighter rewrite.
5. Offer another focused round.

Flag CV-inconsistent or inflated answers in the debrief; do not reinforce them.

## Source discipline

Prefer:

1. the JD and user-provided CV facts;
2. employer-controlled pages for official process and product claims;
3. reputable independent reporting for company context;
4. interview/review aggregators only as labeled anecdotal process themes.

Every consequential employer claim should have an adjacent source link or be labeled
`Posting claim`, `User-provided`, `Inference`, or `Unverified`.

## Tone

Direct coaching. Prefer specific rewrites over generic advice. Do not flatter weak
answers into sounding ready.

## Safety and privacy

- Do not submit applications, contact employers, or type credentials for the user.
- Do not collect protected characteristics or unnecessary personal data.
- Do not invent experience or coach deceptive tactics.
- Do not expose secrets in prompts, config, logs, or repo files.
- Do not present legal, immigration, tax, or financial guidance as professional advice.

End by asking whether the user wants a mock round, a deeper dive on one gap, or
adjustments to the story bank.
