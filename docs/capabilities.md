# Capability catalog

This is a generalized snapshot of the capability pattern in the current deployment. Names describe boundaries, not published production endpoints or credentials. Each role links to a rewritten, sanitized reference persona. See the [tool catalog](tools.md) for exact interface names and current access scopes.

## Shared capabilities

- Specialist-scoped durable memory with list and removal controls.
- Bounded public web discovery and safe GET-only fetching.
- Image, text-file, and PDF ingestion with size and page limits.
- Markdown, text, structured data, calendar/contact, and general PDF output.
- One-off and recurring Discord posts.
- Explicitly allowlisted autonomous runs bound to their originating thread.
- Productivity-suite access with read-only mail and guarded writes.
- Spreadsheet value editing through a workspace tool plus separately constrained formatting and visual preview.
- Ordered model-provider fallback persisted per thread.

See the [specialist persona collection](../reference/specialists/README.md) for the difference between prompt policy and enforceable controls.

## Specialist roles

### [Cooking](../reference/specialists/cooking/AGENTS.md)

- Source-preserving recipe transcription, conversion, scaling, substitution, and technique clarification.
- Structured recipe rendering with fixed fields and no arbitrary HTML or filesystem access.
- Read-only ingredient and equipment sourcing with seller claims kept distinct from verification.

### [Finance](../reference/specialists/finance/AGENTS.md)

- Dated reference FX conversions from a public central-bank-oriented source.
- One-shot threshold alerts clearly labelled as reference rates rather than executable quotes.
- Optional read-only brokerage integration with narrow OAuth scope and a local deny layer for trade-like tools.
- Guarded spreadsheet calculations, formatting, and visual review.

### [Gardening](../reference/specialists/gardening/AGENTS.md)

- Climate-, exposure-, and container-aware plant selection and care.
- Evidence-labelled photo diagnosis and integrated pest management.
- Safety checks for loading, drainage, severe weather, toxicity, and chemicals.
- Read-only regional sourcing with species, viability, and importability left unverified unless evidenced.

### [Marketplace research](../reference/specialists/marketplace-research/AGENTS.md)

- Local-language keyword validation separated from proof of actual listings.
- Guarded read-only search cards and product-detail inspection.
- Account-sensitive helpers that serialize requests, space visits, and stop on login or verification challenges.
- No cart, purchase, seller-message, account, login, or verification controls.

### [Job search](../reference/specialists/job-search/AGENTS.md)

- Truth-preserving CV, cover-letter, role-fit, and interview coaching.
- Reference-aware document rendering with bounded layout controls.
- Independent visual-review gates before final document delivery.
- Validated interview-deck export to a separate practice application through a narrow spool or API boundary.

### [Shopping](../reference/specialists/shopping/AGENTS.md)

- Current price, availability, warranty, compatibility, and landed-cost research.
- Consistent comparison of exact variants and seller terms.
- Direct-source verification with marketplace evidence explicitly qualified.
- No merchant contact, purchasing, or account operation.

### [Media stack](../reference/specialists/media-stack/AGENTS.md)

- Fixed actions for approved media applications instead of arbitrary container or shell access.
- Exact-title lookup before requested additions and clear handling of ambiguous series or seasons.
- Read-only diagnostics from a service allowlist with bounded, redacted logs.
- Technical confirmation gates for retries, restarts, updates, and other disruptive operations.

### [Infrastructure](../reference/specialists/infrastructure/AGENTS.md)

- A single privileged maintenance role with reviewed file and shell tools.
- Permission to inspect services, make scoped reversible changes, test, deploy, and document.
- Stronger confirmation requirements for security changes, broad deletion, meaningful-risk migration, credential changes, reboot, or prolonged disruption.
- Responsibility for preserving the least-privilege boundary of every ordinary specialist.

### [Travel](../reference/specialists/travel/AGENTS.md)

- Constraint-aware itineraries, transport, packing, timing, and contingency planning.
- Current official-source checks for entry rules, advisories, schedules, weather risks, and opening hours.
- Careful handling of bookings and identity information with no booking, check-in, or account actions.

### [Trends and intelligence](../reference/specialists/trends/AGENTS.md)

- Bounded public engagement snapshots from multiple sources.
- Clear separation between verified facts, attention signals, and assessment.
- Persistence and promotion-resistance checks before recommendations.
- Recurring reviews that verify current pricing and primary-source claims.

### [Project evaluator](../reference/specialists/project-evaluator/AGENTS.md)

- Deterministic financial models and supplier-quote normalization.
- Evidence-aware competitor comparison and infrastructure-cost estimation.
- Public market-signal collection that cannot be represented as proven demand.
- Regulatory issue spotting with explicit professional-confirmation points.
- Staged validation with measurable stop/go thresholds before major commitments.

## Companion services

Some workflows are better isolated as separate applications or helpers:

- a private interview-practice application with transcription and evaluation;
- a scheduler that survives bridge restarts;
- account-sensitive browser or device adapters behind read-only schemas;
- document renderers using fixed templates with network access disabled;
- service-specific helpers under dedicated Unix users and permissioned Unix sockets.

A specialist should receive only the operation it needs, not administrative access to the companion service.
