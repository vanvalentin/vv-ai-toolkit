# Job offer evaluation methodology

This is the canonical method for evaluating a job posting, employer, and role against a
person's goals. It is designed for evidence-backed decisions, not automated hiring
judgments or a prediction of individual success.

## Principles

1. **Decision relevance first.** Research only claims that could change whether to
   apply, interview, negotiate, or decline.
2. **Evidence before scoring.** A score summarizes the evidence; it does not create it.
3. **Claims are not facts by default.** Preserve whether information came from the
   posting, the user, a public source, or an inference.
4. **Uncertainty is part of the result.** Missing, stale, blocked, or contradictory
   evidence must reduce confidence.
5. **Fit is contextual.** Evaluate against the user's goals and constraints, not a
   universal definition of a good job.
6. **Privacy by default.** Use the minimum personal information needed.

## 1. Frame the decision

Identify the decision stage:

- **Apply:** Is the expected value of applying worth the time?
- **Interview:** What needs validation before investing further?
- **Offer:** Is the complete package preferable to alternatives?
- **Negotiate:** Which evidence supports specific requests?

Capture the user's hard constraints, weighted preferences, career direction, relevant
skills, location or work-authorization limits, and compensation floor. If they are not
provided, use neutral assumptions and label them.

Do not require a CV. A short, redacted profile is enough. Never infer age, ethnicity,
health, family status, religion, gender identity, or another protected characteristic.

## 2. Normalize the posting

Preserve the original posting URL and access date when possible. Extract:

- title, employer, team, location, remote/hybrid expectations, and travel;
- employment type, schedule, contract duration, and probation;
- responsibilities, outcomes, seniority signals, and reporting line;
- required and preferred skills, experience, education, and certifications;
- salary range, currency, pay period, bonus, equity, benefits, and leave;
- application deadline, interview process, and sponsorship statements;
- ambiguous, internally inconsistent, or unusually broad requirements.

Quote only short passages needed to support analysis. A removed posting, repost, or
aggregator copy should be marked as such.

## 3. Build an evidence ledger

For each consequential claim, record:

| Field | Meaning |
| --- | --- |
| Claim | A narrow, testable statement |
| Status | Posting claim, user-provided, verified, inferred, contradicted, or unknown |
| Source | Publisher, page title, and direct URL |
| Date | Publication/update date and access date, when available |
| Quality | Primary, authoritative independent, reputable secondary, or anecdotal |
| Scope | Geography, business unit, job family, and period actually covered |
| Notes | Conflicts, caveats, sample size, or extraction limits |

Use direct page URLs rather than search-result URLs. A snippet is a lead, not final
evidence. Keep a source close to the exact claim it supports.

### Source hierarchy

No source is universally best. Match source type to claim type:

- **Original posting and employer pages:** strongest for what the employer currently
  states; weak for proving workplace quality.
- **Government records, regulators, official registries, and filings:** strongest for
  legal identity, regulated events, and reported financial facts.
- **Established journalism and industry research:** useful for independently reported
  events and market context.
- **Compensation datasets:** useful for ranges when role, level, location, date, and
  sample limitations are visible.
- **Employee-review platforms:** useful for recurring themes, not verified universal
  facts. Weight by recency, sample size, role, geography, and consistency.
- **Forums and social posts:** individual anecdotes or research leads only.

Glassdoor and similar sites may require authentication, show consent gates, rate-limit,
or block automated browsers. Live access is never guaranteed. Do not bypass those
controls. Report the limitation and use lawful public alternatives.

## 4. Research in passes

### Pass A: Identity and role

Confirm that the employer, domain, posting, location, and recruiter context are
coherent. Check whether the same role appears on the employer's careers site. A missing
copy is not proof of fraud, but it raises a question.

When only a short or ambiguous employer name is known, resolve the legal entity before
calling LinkedIn or Glassdoor MCP tools: use the host's **web search** to find the
official site and `linkedin.com/company/...` page (for example `"DASH" payment Hong
Kong LinkedIn`), cite that resolution, then pass the extracted LinkedIn slug to
`linkedin_collect_company`. Treat `linkedin_search_companies` as a last resort — it is
poor at disambiguating common names.

### Pass B: Employer and business

Research only relevant dimensions:

- ownership, size, locations, products, and business model;
- material funding, layoffs, insolvency, regulatory action, or leadership changes;
- recent performance or growth claims;
- hiring patterns and role-specific workplace themes.

Distinguish the legal entity from a brand, parent, subsidiary, franchise, or staffing
agency.

### Pass C: Compensation and conditions

Normalize all compensation to a common currency and period, preserving exchange-rate
and tax assumptions. Separate base salary, variable pay, equity, pension, allowances,
leave, and one-time payments. Compare like with like by role, seniority, geography,
employment type, and date.

Never estimate take-home pay without clearly stated jurisdiction and assumptions.

### Pass D: Contradiction and gap check

Search for evidence that could disconfirm the emerging view. Reconcile different dates,
regions, entities, and job families before calling sources contradictory. List important
unknowns that only the recruiter, hiring manager, or contract can answer.

Stop researching when additional sources are unlikely to change the decision or when
access constraints make further work disproportionate.

## 5. Assess profile fit

Map the posting to evidence from the user's profile:

- **Demonstrated match:** direct evidence of the required capability.
- **Transferable match:** adjacent evidence with a credible bridge.
- **Learnable gap:** realistic to close within the expected ramp-up period.
- **Material gap:** likely screening or performance risk.
- **Preference mismatch:** possible but contrary to the user's goals.
- **Unknown:** insufficient information.

Separate genuine requirements from wish-list language. Do not treat every bullet as an
equal hard requirement. Explain which gaps are likely screening constraints and which
can be addressed through examples, learning, or interview questions.

## 6. Score transparently

Use the gateway's deterministic 0–10 scorecards only after gathering evidence. Keep
the cards separate rather than manufacturing one universal total:

- **Company health:** growth 30%, financial resilience 30%, leadership stability 15%,
  and employee sentiment 25%.
- **Role fit:** required-skill match 45%, preferred-skill match 20%, relevant experience
  25%, and differentiation 10%.
- **Leverage:** candidate scarcity 40%, interview signal 35%, and credible competing
  options 25%.
- **Compensation:** market alignment 60% and negotiation support 40%.

Required- and preferred-skill matches are entered as percentages; other rubric inputs
use 0–10. The compensation card interprets the estimated percentile of the user's
target in the relevant market, so the market definition and evidence must be explicit.

Pass the evidence IDs supporting every component to `score_offer_case`. Show component
weights, scores, rationales, confidence, and blind spots. If evidence is missing, use
the neutral default only as a visibly provisional input and accept the resulting lower
confidence. Do not silently score unknown as bad or use a score to erase a hard
constraint.

The recommendation is a reasoned synthesis of the four cards, the user's preferences,
hard constraints, and risks. A credible severe red flag can override otherwise strong
scores.

## 7. Calibrate confidence

Report confidence as:

- **High:** decisive claims are supported by recent, direct, mutually consistent
  evidence and the user's constraints are clear.
- **Medium:** enough evidence for a direction, with meaningful gaps or indirect sources.
- **Low:** sparse, stale, blocked, contradictory, or mostly anecdotal evidence; or
  unclear user priorities.

Confidence concerns evidence quality, not certainty about the future.

## 8. Identify risks without overclaiming

Potential risk signals include requests for money or sensitive documents too early,
identity or domain inconsistencies, implausible compensation, evasive contract terms,
unpaid work, persistent reposting, unexplained role breadth, or material discrepancies
between recruiter and official information.

For each risk, state:

1. what was observed;
2. plausible benign and concerning interpretations;
3. evidence strength;
4. a safe verification step.

Do not accuse a company or person of fraud, discrimination, or misconduct without
strong evidence. Do not treat isolated anonymous reviews as representative.

## 9. Produce the decision report

With the `offer-intel` gateway, create a case before collection and preserve each
source and claim in its evidence pack. Cite `EV-*` IDs in structured material claims,
include the corresponding `SRC-*` IDs, and disclose all registered blind spots. Run
`validate_offer_report` before presenting the result. Unsupported, stale, unknown, or
undisclosed items must be corrected, removed, refreshed, or explicitly handled as
limitations. Reader-facing prose should link to the underlying source URLs as well as
using the internal IDs.

A complete report contains:

1. recommendation: pursue, pursue conditionally, or pass;
2. confidence and the two or three decisive reasons;
3. normalized role and package snapshot;
4. profile-fit strengths, gaps, and constraints;
5. employer findings with inline citations;
6. risks, contradictions, and unknowns;
7. weighted scorecard with assumptions;
8. prioritized questions for recruiter, manager, and offer review;
9. sources, access dates, and limitations.

### Canvas employer-intelligence sections

When the deliverable is a Cursor canvas, extend the report with these structured
blocks (tables or equivalent layout). Each cell must be evidence-backed, explicitly
marked unknown, or labeled as inference — never generic placeholder text.

Treat each block as a separate research pass, not as formatting applied to the same
small evidence set. A detailed report should include dates, quantities, named actors,
product dependencies, and relevant comparisons. Identify company-reported figures,
distinguish current outcomes from targets, and add a compact claim audit for plausible
but unverified narratives. Never manufacture specificity about burn, runway,
workload, monopoly status, acquisition plans, team culture, or technical debt.

**Corporate Vitals & Architecture** — foundation history; headcount; tech-stack
reality (modern vs legacy); legal entity; funding/incubation; operating scale;
regulatory status; architecture dependencies.

**Executive Committee & Key Leadership** — name, role, one-line background per leader
where sources exist.

**Competitive Arbitrage Matrix** — named competitors with advantage and disadvantage
columns. Separate direct product rivals, regulated operators, substitutes/payment
rails, and talent competitors when those categories materially differ.

**Internal Peer Benchmarking** — peers in role, tenure patterns, and org

**Employee & Customer Sentiment** — theme, reality behind PR, red-flag level
(Low/Med/High). For consumer products, include app-store evidence with locale, sample
size, recency, and review-pattern limitations.

Keep citations adjacent to claims. Include publication dates where recency matters.
Clearly identify calculations and inferences. If no external research was possible,
say so prominently.

Use a professional-critical tone by default. A requested `cold-reader` mode may be
sharper and mildly sardonic, but it must not insult individuals, hide uncertainty, or
turn anecdote into fact.

## Authentication, access, and privacy

The research gateway is intended for public research. Some public-facing pages may
still require the user to establish a site session. When the connector provides a
headed manual-login flow, credentials are entered by the user directly into the site
and must never be passed through the model or MCP arguments. It must not:

- receive usernames, passwords, exported session cookies, API tokens, or private
  application links;
- automate credential entry, CAPTCHA solving, paywall bypass, rate-limit evasion, or
  access contrary to a site's controls;
- submit an application, contact a recruiter, or change external data;
- retain private CVs, correspondence, or identity documents in the repository.

An authenticated connector session is local and site-dependent, not guaranteed. The
user should complete any login or consent interaction personally, stop at a CAPTCHA or
challenge, and clear the local session when no longer needed. Alternatively, the user
may inspect a source manually and provide a short, non-confidential summary. Label that
summary `User-provided`; do not imply it was independently verified.

Redact names, addresses, phone numbers, email addresses, IDs, exact birth dates,
signatures, compensation documents, and confidential company material unless strictly
necessary. Prefer generalized profile facts and anonymized excerpts.

## Known limitations

- Public sources can be wrong, stale, incomplete, region-specific, or removed.
- Automated extraction can miss dynamic content, tables, PDFs, or consent-gated text.
- Employee-review and salary datasets have selection and survivorship bias.
- A company-level pattern may not describe a specific team or manager.
- Compensation comparisons vary with currency, tax, contract type, and total package.
- The workflow cannot verify private claims, predict hiring outcomes, or replace legal,
  immigration, tax, financial, or career advice.
