# Explored and decided together

Only items discussed directly together are listed here. Implementation details chosen independently to meet a goal are intentionally omitted.

## Repository scope

### Specialist platform is the repository focus

- **Discussed:** current thread — you asked whether the Pi infrastructure should be the main thing, approved the restructure, and approved deleting `toolkits/`.
- **Outcome:** Root README, `docs/`, and `reference/` describe the specialist platform. Career code and client auto-configuration were removed.
- **See:** `README.md`, `docs/architecture.md`.

### Sanitized personas

- **Discussed:** current thread — you asked whether each specialist's `AGENTS.md` should be published as an example, then approved it.
- **Outcome:** Eleven rewritten reference personas under `reference/specialists/`, linked from `docs/capabilities.md`. No memories, conversations, identifiers, credentials, or deployment details included.
- **See:** `reference/specialists/README.md`.

### Tool catalog with diagrams

- **Discussed:** current thread — you asked to document the different tools across specialists, with screenshots and graphs if needed.
- **Outcome:** `docs/tools.md` catalogs current extension tools, specialist assignments, and enforcement layers with Mermaid diagrams. Real screenshots were deliberately omitted to avoid leaking channels, accounts, conversations, or service state; synthetic visuals remain a backlog item.
- **See:** `docs/tools.md`.

### Privacy release guard

- **Discussed:** current thread — you asked to update the repo without putting personal or secret material in it.
- **Outcome:** Dependency-free `scripts/check_public_repo.py` plus GitHub Actions, explained in `scripts/README.md`. Manual diff review is still required.
- **See:** `scripts/README.md`.

## Guarded automation boundaries

### Marketplace research stays read-only

- **Discussed:** you authorized read-only product-page inspection, approved removing rate caps and incomplete-page pauses while keeping serialization, spacing, and halts on login or risk signals, and asked for a shorter pause on the physical device.
- **Outcome:** Search and detail tools expose no cart, purchase, seller-message, account, login, or verification actions and stop on risk responses rather than retrying.
- **See:** `docs/tools.md`, `reference/specialists/marketplace-research/AGENTS.md`.

### Physical device as a scoped backend

- **Discussed:** you asked for the physical phone's shopping app to become a scoped agent automation backend for search and product-page matching, not just a manual screen.
- **Outcome:** Fixed read-only search and detail actions with annotated visual evidence and variant reads; no SKU selection, purchasing, messaging, or verification bypass.
- **See:** `docs/tools.md`.

### Brokerage stays read-only

- **Discussed:** you approved a server-scoped issuer-validation bypass for the Finance-only official brokerage MCP endpoint.
- **Outcome:** Narrow read-only OAuth scope, hidden and locally denied trade-like tools, and user-completed authorization. No orders or account changes.
- **See:** `docs/tools.md`, `reference/specialists/finance/AGENTS.md`.

### Finance tracking with reference data

- **Discussed:** you asked for a reusable finance tracker and an end-of-month check-in.
- **Outcome:** Aggregate tracking with dated reference-rate conversion and one-shot threshold alerts, explicitly labelled as reference data rather than executable quotes.
- **See:** `docs/tools.md`, `reference/specialists/finance/AGENTS.md`.

### Private interview practice

- **Discussed:** you asked for a private hosted interview-practice app with spaced repetition and AI comparison.
- **Outcome:** Separate practice application with a narrow deck-import boundary and layered evaluation fallbacks; role decks are built from postings without inventing requirements.
- **See:** `docs/tools.md`, `reference/specialists/job-search/AGENTS.md`.
