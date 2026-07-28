---
name: job-offer-evaluation
description: Evaluate a job offer and employer with cited evidence, explicit uncertainty, profile fit, risks, and actionable follow-up questions.
---

# Job offer evaluation

Use this skill when a user wants to assess a role, job posting, employer, compensation
claim, or interview opportunity. The canonical process and scoring rules are in
`experts/job-offer-evaluation/methodology.md`; read that file before producing a full
evaluation.

## Required inputs

Ask only for information that materially changes the result:

- the posting text or URL;
- the user's goals, constraints, and relevant experience;
- location, work authorization, seniority, and compensation expectations when relevant;
- any claims or concerns the user especially wants checked.

Proceed with stated assumptions if the user prefers not to provide personal details.
Never require a CV. Encourage redaction of names, addresses, contact details, IDs,
application links, and confidential employer information.

## Evidence-first workflow

1. Preserve the posting as a primary artifact. Distinguish its exact claims from your
   interpretation.
2. Extract role facts: responsibilities, requirements, location, work arrangement,
   contract, compensation, reporting line, hiring process, and stated benefits.
3. Build a research plan around unresolved, decision-relevant questions.
4. Use the `offer-intel` MCP server when available. Research public first-party sources
   before reputable independent sources. Browser-derived evidence may fail because of
   authentication, consent pages, rate limits, anti-bot controls, or site changes.
5. Record each source's title, publisher, URL, publication/update date when visible,
   access date, and the claim it supports.
6. Corroborate consequential claims. Do not convert an absence of evidence into a
   negative fact.
7. Compare the evidence with the user's profile. Label hard gaps, learnable gaps,
   preferences, and unknowns separately.
8. Apply the rubric in the canonical methodology. Show assumptions and confidence;
   do not manufacture precision when inputs are incomplete.
9. Produce a decision-oriented report with citations adjacent to factual claims.

If MCP research is unavailable, continue from user-provided material and clearly mark
external claims as unverified. Never imply that Glassdoor or any other source is
available live.

### `offer-intel` MCP sequence

When the gateway is available:

1. Call `create_offer_case` with the minimum necessary, redacted input.
2. Use read-only connectors and host research tools to collect relevant material.
3. Add host-collected facts with `add_external_evidence`; preserve narrow claims,
   excerpts, source type, URL, dates, and confidence.
4. Inspect `get_evidence_pack` for conflicts and blind spots.
5. Call `score_offer_case` with evidence IDs for each supported rubric component.
6. Build material report claims with their `EV-*` IDs and disclose every blind spot.
7. Call `validate_offer_report`. Resolve citation, freshness, source, and disclosure
   issues before presenting the report. If an issue cannot be resolved, omit the claim
   or state the limitation rather than bypassing validation.

Cases are in memory by default. Do not mistake MCP evidence IDs for reader-facing
citations: the final answer should still link the underlying source URLs.

### Employer resolution before connector calls

Do not rely on bare company names or `linkedin_search_companies` alone when the employer
is ambiguous. LinkedIn's internal company search is a weak disambiguator for short names
(`DASH`, `Mercury`, `Atlas`) and often returns unrelated entities.

**Default order when the user gives only a name, role, and location:**

1. **Host web search first** (Google/Bing/general web — not LinkedIn search MCP):
   - Example queries: `"DASH" payment Hong Kong company LinkedIn`, `"DASH" fintech
     Hong Kong official site`.
   - Goal: find the **official website** and **`linkedin.com/company/...` URL**.
   - Record the chosen match with `add_external_evidence` (URL, access date, short
     excerpt of why this entity fits the posting context).
2. **Extract the LinkedIn slug** from the resolved company URL and call
   `linkedin_collect_company` with that slug.
3. **Use explicit URLs from the user or posting** when available — skip search.
4. **`linkedin_search_companies` is a last resort** only when web search and the posting
   did not yield a confident company page. Prefer an exact name/location match over the
   first hit; record near-misses as blind spots.
5. **Glassdoor:** use the same web-search-first pattern as LinkedIn:
   - Search for `"<company>" <location/industry> site:glassdoor.com OR site:glassdoor.com.hk`.
   - If a company overview or reviews URL is found, pass that **full URL** to
     `glassdoor_collect_company` or `glassdoor_resolve_company`. This skips Glassdoor's
     internal search, which often triggers verification challenges.
   - If web search finds **no Glassdoor profile**, record that as a blind spot — do not
     treat it as proof the employer is bad. Many small HK employers have no listing.
   - A challenge on `glassdoor.com` in `glassdoor_check_viability` does not automatically
     invalidate a regional `.com.hk` session — call `glassdoor_status` after local login.
     Collection may still fail if Glassdoor challenges automated page loads even with a
     direct URL.

## Source discipline

Prefer sources in this order:

1. the original job posting and employer-controlled pages for what the employer claims;
2. official registries, filings, regulator notices, and government statistics;
3. established reporting and recognized industry research;
4. employee-review and compensation aggregators as anecdotal or sampled indicators;
5. forums and social posts only as leads or clearly labeled individual experiences.

First-party sources are authoritative about stated policies, not necessarily about
quality or lived experience. Employee reviews can reveal patterns but are
self-selected, difficult to verify, and sensitive to recency, geography, function, and
sample size.

Every factual claim that could affect the decision should either have an adjacent
source link or be labeled as:

- `Posting claim`
- `User-provided`
- `Inference`
- `Unverified`

Do not cite a search-result snippet as final evidence when the underlying page can be
opened. Do not cite one source for a broader claim than it supports.

## Output contract

Keep the answer proportional to the decision. A full report should contain:

1. **Verdict** — pursue, pursue conditionally, or pass; confidence; decisive reasons.
2. **Role snapshot** — verified facts and important unknowns.
3. **Fit assessment** — strengths, gaps, constraints, and transferable evidence.
4. **Employer evidence** — business stability, reputation, work environment, and
   compensation signals, with source quality and dates.
5. **Risks and red flags** — observed facts separated from interpretations.
6. **Scorecards** — rubric dimensions, weights, scores, and the evidence behind them.
7. **Questions to ask** — prioritized questions that resolve the largest uncertainties.
8. **Sources and limitations** — links, access dates, blocked sources, stale evidence,
   and remaining unknowns.

### Canvas deliverable (full evaluations)

When producing a standalone evaluation canvas (see the Cursor canvas skill), include
the chat verdict and scorecards **plus** the employer-intelligence sections below.
Omit a section only when it would be entirely empty; otherwise populate it with
cited facts, explicit **Unknown / not verified** cells, and blind-spot callouts —
never placeholder filler.

The canvas must be an analytical report, not a thin summary. Before rendering it:

1. Research each employer-intelligence section as a separate question.
2. Prefer at least two independent sources for decisive claims; identify first-party
   metrics as company-reported.
3. Separate **Observed fact**, **First-party claim**, and **Inference**. Strong prose
   does not justify silently upgrading an inference into a fact.
4. Include concrete dates, quantities, named products, and relevant comparators.
5. Add a short **Claim audit** for attractive but unsupported narratives discovered
   during research (for example, monopoly, runway, burn rate, team stress, or market
   share).
6. Explain what each fact means for this role without predicting culture, workload,
   acquisition, or failure from company size alone.

#### Corporate Vitals & Architecture

| Metric | Telemetry Data |
|---|---|
| **Foundation History** | Origins, founding year, founders, and baseline narrative |
| **Total Global Headcount** | Exact count or narrow estimated range with source |
| **Tech Stack Reality** | Modern asset vs legacy burden; cite posting, engineering signals, or mark unknown |

Also cover legal entity, funding/incubator status, verified operating scale, product
architecture and dependencies, regulatory position, and whether growth targets are
historical, current, achieved, or missed.

#### Executive Committee (ExCo) & Key Leadership

| Name | Role | Background / Strategic Vibe |
|---|---|---|
| … | … | One-sentence background or leadership focus per row |

Include founder/CEO and any hiring-manager or engineering-lead signals from LinkedIn,
filings, or reputable press. Do not invent titles.

#### Competitive Arbitrage Matrix

| Competitor | Company Advantage vs. Them | Company Disadvantage vs. Them |
|---|---|---|
| … | … | … |

Compare against direct category peers (same market, product, and customer). Cite
sources; label inference. Segment competitors when useful: direct product rivals,
substitutes/payment rails, regulated fleet operators, and talent competitors. For each
row explain the evidence for both advantage and disadvantage; do not use generic
phrases such as "larger engineering budget."

#### Internal Peer Benchmarking

- **Existing Peers in Role:** Current employees with the same or adjacent title,
  typical tenure, team size, and org distribution — from LinkedIn people/search,
  posting context, or marked unverified.

Do not infer "sole engineer" from a small search result. State the visible sample and
search limitations.

#### Employee & Customer Sentiment

| Key Theme | The Reality behind the PR | Red Flag Level (Low/Med/High) |
|---|---|---|
| … | Detailed feedback analysis with source quality | Low / Med / High |

Pull from Glassdoor/reviews when available; otherwise first-party claims vs
independent reporting. Include app-store/customer evidence where the product is a
consumer app, with locale, rating count, date, and examples of recurring themes.
Never treat absent Glassdoor data as negative proof or one review as a pattern.

Use ranges where appropriate. Treat a score as a summary of evidence, never as an
objective prediction. If evidence is sparse or contradictory, lower confidence and
explain what would change the recommendation.

## Tone

Default to professional, critical, and direct. If the user requests `cold-reader`
tone, make the prose sharper and mildly sardonic, but never let style turn uncertainty
into fact, insult individuals, or overstate weak evidence.

## Safety and privacy

- Do not submit applications, type credentials for the user, bypass access controls,
  solve CAPTCHAs, or evade rate limits. If a connector supports a manual login window,
  the user alone may authenticate there.
- Do not collect protected or highly sensitive personal data that is unnecessary for
  the evaluation.
- Do not infer protected characteristics about the user, employees, or hiring team.
- Do not present legal, immigration, tax, or financial guidance as professional advice.
- Do not expose credentials in prompts, config files, logs, citations, or output.
- Do not make allegations about people or companies from weak or anonymous evidence.

End with the smallest useful next action: apply, decline, request clarification, or
investigate a short list of unresolved questions.
