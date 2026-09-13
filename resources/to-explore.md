# Prioritized exploration backlog

Future work derived from current platform limitations and repeated cross-specialist needs. Each item has a concrete question and completion criterion.

## 1. Publish a runnable sanitized core

- **Reference:** https://pi.dev/
- **Question:** What is the smallest reusable Discord-to-Pi bridge that demonstrates thread sessions, streaming, attachment handling, model fallback, and least-privilege extensions without production coupling?
- **Success criterion:** A clean-room implementation starts from placeholder configuration, passes integration tests with temporary state, exposes no private assumptions, and can be deployed under the example systemd units.

## 2. Generate the tool manifest from code

- **Reference:** https://pi.dev/
- **Question:** Can extension registrations, specialist allowlists, schemas, side-effect classes, and helper dependencies generate `docs/tools.md` and a machine-readable manifest automatically?
- **Success criterion:** CI fails when runtime tool scope differs from the committed manifest, and the generated output contains no environment values or identifiers.

## 3. Reduce the shared tool surface

- **Reference:** https://www.openpolicyagent.org/docs/latest/
- **Question:** Should every specialist receive an explicit active-tool allowlist rather than relying on persona instructions not to use irrelevant globally registered tools?
- **Success criterion:** Each role has a reviewed machine-enforced allowlist, unnecessary tools are inactive, and regression tests prove that a fallback model or prompt injection cannot activate them.

## 4. Audit memory isolation and retention

- **Reference:** https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html
- **Question:** How should host-wide, specialist-wide, thread-local, and companion-application memory be separated, expired, exported, and deleted?
- **Success criterion:** Automated tests demonstrate no cross-specialist leakage; every memory class has an owner, purpose, retention rule, deletion path, and maximum injection budget.

## 5. Build adversarial tool-policy evaluations

- **Reference:** https://www.promptfoo.dev/docs/intro/
- **Question:** Can a local evaluation corpus test prompt injection, forged scheduled instructions, malicious documents, SSRF variants, path traversal, output flooding, invented identifiers, and confirmation bypasses?
- **Success criterion:** High-risk cases fail closed in CI across the primary and fallback models without sending private fixtures to third-party services.

## 6. Add privacy-preserving observability

- **Reference:** https://opentelemetry.io/docs/
- **Question:** Which metrics and traces are useful for RPC latency, model fallback, tool failure, scheduler delivery, helper health, and truncation without recording prompts, URLs, file contents, account data, or identifiers?
- **Success criterion:** A documented telemetry schema supports operational diagnosis using bounded cardinality and redaction, with content capture disabled by default.

## 7. Formalize authorization policy

- **Reference:** https://modelcontextprotocol.io/specification/latest/basic/authorization
- **Question:** Would a small policy-as-code layer simplify rules based on specialist, tool, action, destination class, thread, ownership, confirmation, and scheduled versus interactive context?
- **Success criterion:** Policy decisions are deterministic, locally testable, fail closed, and enforced at the tool/helper boundary rather than only in prompts.

## 8. Strengthen supply-chain verification

- **Reference:** https://slsa.dev/spec/v1.2/
- **Question:** How should Pi versions, extension dependencies, browser binaries, models, helper releases, checksums, and GitHub Actions be pinned and attested?
- **Success criterion:** Every executable dependency has a documented source, version, integrity check, update process, and rollback path; CI actions are commit-pinned.

## 9. Exercise backup and recovery

- **Reference:** https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
- **Question:** Can sessions, scheduler state, specialist memory, and integration metadata be restored independently without bundling credentials or private attachments unnecessarily?
- **Success criterion:** A documented recovery drill restores a synthetic deployment, verifies service ownership and permissions, and proves that missing credentials fail safely.

## 10. Create synthetic visual documentation

- **Reference:** https://playwright.dev/docs/screenshots
- **Question:** Which public screenshots would materially improve setup and troubleshooting without revealing real channels, accounts, conversations, hostnames, or service state?
- **Success criterion:** A synthetic demo workspace produces reproducible screenshots with placeholder data and automated image-metadata/privacy checks.

## 11. Add visual regression tests for generated artifacts

- **Reference:** https://playwright.dev/docs/test-snapshots
- **Question:** Can recipe PDFs, general documents, CV-like layouts, and spreadsheet previews be checked against deterministic fixtures without requiring model judgment for basic geometry?
- **Success criterion:** CI catches clipping, overflow, missing fonts, broken page counts, and major layout drift using synthetic inputs; independent model review remains a secondary semantic/aesthetic check.

## 12. Evaluate model chains with workload-specific evidence

- **Reference:** https://www.promptfoo.dev/docs/intro/
- **Question:** Which primary and fallback models offer the best quality, latency, tool reliability, and cost for each specialist workload without changing authority?
- **Success criterion:** A repeatable benchmark uses sanitized tasks, records provider terms and prices by date, resists launch promotions, and recommends changes only when gains are material and persistent.
