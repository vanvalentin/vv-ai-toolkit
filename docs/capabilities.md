# Capability catalog

This is a generalized snapshot of the capability pattern in the current deployment. Names describe boundaries, not published production endpoints or credentials.

## Shared capabilities

- Specialist-scoped durable memory with list and removal controls.
- Bounded public web discovery and safe GET-only fetching.
- Image, text-file, and PDF ingestion with size/page limits.
- Markdown, text, CSV, JSON, calendar/contact, and general PDF output.
- One-off and recurring Discord posts.
- Explicitly allowlisted autonomous specialist runs bound to their originating thread.
- Google Workspace access through MCP with read-only mail and guarded writes.
- Spreadsheet value editing through the Workspace tool plus separately constrained formatting and visual preview.
- Ordered model-provider fallback persisted per thread.

## Domain-specific examples

### Finance

- Dated reference FX conversions from a public central-bank-oriented source.
- One-shot threshold alerts clearly labelled as reference rates, not executable quotes.
- Optional read-only brokerage integration with narrow OAuth scope and a local deny layer for trade-like tools.

### Job search

- Structured CV and interview-document generation.
- Reference-aware rendering with bounded layout controls.
- An independent visual-review gate before final document delivery.
- Validated interview-deck export to a separate local practice application through a write-only spool boundary.

### Media operations

- Fixed actions for approved media applications rather than arbitrary container or shell access.
- Read-only diagnostics from a service allowlist with bounded, redacted logs.
- Confirmation for restarts, updates, retries, and other disruptive operations.

### Marketplace and shopping research

- Keyword validation separated from proof of actual listings.
- Guarded read-only search cards and product-detail inspection.
- Account-sensitive helpers that serialize requests, space visits, and stop on login or verification challenges.
- No cart, purchase, seller-message, account, or verification controls.

### Trends and intelligence

- Bounded public engagement snapshots from multiple sources.
- Clear separation between attention signals and evidence of demand, affiliation, or coordination.
- Recurring reviews that verify pricing and primary-source claims before recommendations.

### Project evaluation

- Deterministic financial models and supplier-quote normalization.
- Evidence-aware competitor comparison and infrastructure cost estimation.
- Public market-signal collection that cannot be represented as proven demand.
- Official-source discovery for regulatory issue spotting, with professional review called out where needed.

### Cooking and document workflows

- Structured recipe rendering with fixed fields and no arbitrary HTML or filesystem access.
- General document generation restricted to the current thread's output directory.

### Infrastructure

- A single privileged maintenance specialist with built-in file and shell tools.
- Permission to inspect services, make scoped reversible changes, test, and deploy.
- Stronger confirmation requirements for destructive actions, security changes, broad data migration, host reboot, or prolonged disruption.

## Companion services

Some workflows are better isolated as separate applications or helpers:

- a private interview-practice application with local transcription and evaluation;
- a scheduler that survives bridge restarts;
- account-sensitive browser/device adapters behind read-only schemas;
- document renderers running with fixed templates and network access disabled;
- service-specific helpers under dedicated Unix users and permissioned Unix sockets.

The specialist should receive only the operation it needs, not administrative access to the companion service.
