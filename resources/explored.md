# Explored resources and applied lessons

Reviewed public references and generalized lessons from building and operating the specialist platform. Private conversations and user-specific memory are intentionally excluded.

## Agent harness and Discord integration

### Pi agent harness

- **URL:** https://pi.dev/
- **Reviewed:** 2026-09-13
- **Finding:** Pi provides RPC and SDK modes, persistent tree-structured sessions, project instructions, extensions, model selection, and tool control without requiring a fork of the harness.
- **Applied decision:** Use one persistent Pi RPC session per Discord thread, specialist-specific `AGENTS.md`, extension tools, and `--no-builtin-tools` for ordinary roles.
- **Limitation:** Extensions execute with host-process authority unless the deployment constrains them; Pi configuration alone is not a sandbox.

### Discord developer platform

- **URL:** https://discord.com/developers/docs/intro
- **Reviewed:** 2026-09-13
- **Finding:** Text channels, threads, message events, attachments, permissions, and application APIs provide a natural interaction layer for specialist agents.
- **Applied decision:** Treat the channel as the specialist boundary and each generated thread as the conversation/session boundary. Suppress link previews without removing clickable URLs.
- **Limitation:** Discord permissions, rate limits, event delivery, attachment limits, and thread lifecycle must be handled independently from Pi.

## Tool and integration security

### Model Context Protocol authorization

- **URL:** https://modelcontextprotocol.io/specification/latest/basic/authorization
- **Reviewed:** 2026-09-13
- **Finding:** Current MCP authorization builds on OAuth, protected-resource metadata, issuer validation, resource indicators, audience binding, and least-privilege scope selection.
- **Applied decision:** Bind OAuth records to exact server URLs, request minimal scopes, keep tokens outside model context, hide unnecessary tools, and add a local deny layer for write-like operations.
- **Limitation:** A remote server can publish inconsistent metadata or an overly broad tool surface; the client still needs fail-closed validation and local policy.

### OWASP SSRF prevention

- **URL:** https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- **Reviewed:** 2026-09-13
- **Finding:** User-controlled fetching needs protocol, host, port, redirect, DNS, private-address, and response-size controls, preferably with network-layer defense in depth.
- **Applied decision:** Public fetching is GET-only, rejects credential-bearing URLs, blocks private and link-local destinations, revalidates redirects, limits ports and downloads, and truncates model-visible output.
- **Limitation:** URL and DNS validation remain subtle; application checks should not be treated as a substitute for egress restrictions.

### systemd service sandboxing

- **URL:** https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
- **Reviewed:** 2026-09-13
- **Finding:** Dedicated users, restrictive filesystem access, private temporary space and devices, capability reduction, address-family restrictions, and controlled writable paths reduce helper blast radius.
- **Applied decision:** Run the bridge, scheduler, renderers, and account-sensitive helpers as separate services or users where useful; expose narrow Unix sockets instead of generic administration.
- **Limitation:** Sandboxing must be tested against each workload. A hardened unit with broad writable paths or a powerful helper protocol can still be unsafe.

## Search and account-sensitive automation

### DonSeTch local web research

- **URL:** https://github.com/dondai44423/donsetch
- **Reviewed:** 2026-09-13
- **Finding:** A local multi-engine search process can provide keyless discovery, consensus signals, bounded extraction, and explicit failure states.
- **Applied decision:** Keep search provider selection configurable, pin reviewed versions, retain a simpler fallback, separate discovery from direct-source verification, and record query-free operational metrics.
- **Limitation:** Search coverage, ranking, upstream engines, licensing, and anti-bot behavior change. Search snippets remain leads rather than evidence.

### Playwright browser isolation

- **URL:** https://playwright.dev/docs/api/class-browsercontext
- **Reviewed:** 2026-09-13
- **Finding:** Browser contexts and request routing support isolated sessions and network interception, but storage state can contain highly sensitive cookies and credentials.
- **Applied decision:** Keep authenticated profiles outside Pi sessions, block arbitrary navigation and non-required actions, use network-disabled rendering where possible, and stop rather than bypass login or verification challenges.
- **Limitation:** Browser automation is fragile and account-sensitive. A general browser or raw coordinate interface is too broad for ordinary specialists.

### Android Debug Bridge

- **URL:** https://developer.android.com/tools/adb
- **Reviewed:** 2026-09-13
- **Finding:** ADB is a powerful device administration and shell interface, far broader than a product-research workflow requires.
- **Applied decision:** Keep ADB inside a dedicated helper boundary and expose only fixed read-only search/detail actions. Do not expose arbitrary coordinates, shell, account, cart, purchase, messaging, login, or verification controls to specialists.
- **Limitation:** UI layouts and application risk controls change; automation must fail closed and require manual recovery after authentication or verification events.

## Deterministic data and visual quality loops

### Google Sheets batch updates

- **URL:** https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate
- **Reviewed:** 2026-09-13
- **Finding:** Sheets batch updates validate the request set and apply accepted updates atomically, but the API includes both presentation and destructive operations.
- **Applied decision:** Split ordinary value editing from formatting, allowlist non-destructive presentation operations for existing sheets, and grant a broader surface only to sheets the agent verifiably created. Render a preview after formatting.
- **Limitation:** API success does not guarantee a readable layout; visual inspection and ownership-aware authorization remain necessary.

### Frankfurter reference-rate API

- **URL:** https://frankfurter.dev/
- **Reviewed:** 2026-09-13
- **Finding:** The API exposes dated official-source and blended daily exchange rates without requiring an API key and explicitly states that it is not a live trading feed.
- **Applied decision:** Return effective date and provider attribution, use deterministic conversion arithmetic, and label alerts as daily reference-rate checks rather than executable market prices.
- **Limitation:** Reference rates exclude bank, card, broker, timing, liquidity, and fee effects.

### Independent critic and visual review loops

- **URL:** https://somethingbig.ai/gauntlet-loop
- **Reviewed:** 2026-09-13
- **Finding:** Separating generation from an independent critic can improve adherence to a concrete quality bar and reduce self-approval bias.
- **Applied decision:** Use fresh, context-minimized reviewers and explicit gates for reference-matched documents; require revision rather than silently finalizing a failed draft.
- **Limitation:** Automated reviewers can still miss defects or overfit a rubric. Deterministic overflow and safety checks remain authoritative.

## Cross-specialist lessons

- **Prompts are not permissions.** Persona rules help behavior, but schemas, allowlists, service identities, OAuth scopes, and network policy enforce it.
- **Discovery is not verification.** Search snippets, social engagement, listing cards, reviews, and seller text require direct-source qualification.
- **Visual outputs need visual checks.** PDFs and spreadsheets that are structurally valid can still be clipped, crowded, or visually wrong.
- **High-stakes arithmetic should be deterministic.** Finance, project economics, supplier quotes, and infrastructure estimates benefit from explicit calculators and replaceable assumptions.
- **Account-sensitive automation should stop, not fight.** Cooldowns, login loss, CAPTCHA, and risk-control responses must halt retries and preserve manual recovery.
- **Artifacts often matter more than prose.** Thread-scoped PDFs, text files, sheets, trackers, and practice decks need explicit destination and overwrite controls.
- **Scheduled agency needs provenance.** Autonomous runs require explicit scope, destination binding, signatures, replay resistance, caps, and failure shutdown.
- **Memory must be minimal and scoped.** Durable memory should contain concise confirmed facts, never source documents, secrets, or broad personal histories.
- **Regional research needs regional language and sources.** Local-language discovery should complement—not replace—verification on original official or primary sources.
- **Fallbacks must not change authority.** Switching models must preserve the same tool set and policy boundary.
