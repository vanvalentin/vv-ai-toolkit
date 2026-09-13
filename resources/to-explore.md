# To explore

Only items with prior evidence are kept here: entries saved before the platform rewrite, plus one new item from the current thread. Anything I cannot trace to a previous conversation or to work already in the repo does not belong here.

## Developer tools → AI-ready design systems

### Astryx

- **URL:** https://github.com/facebook/astryx
- **Added:** 2026-07-28
- **Summary:** Meta's open-source React design system, built for both developers and AI agents. It provides accessible components, theming, templates, and CLI tooling so teams and agents can work from the same UI conventions.
- **Why explore it:** Evaluate whether its component library and agent-oriented workflow could be useful for future AI-assisted frontend projects.
- **Status:** Carried over from the pre-rewrite backlog; no specialist conversation found yet. Remove it if it is no longer relevant.

## Agent workflows → iterative quality improvement

### How to Run a Gauntlet Loop

- **URL:** https://somethingbig.ai/gauntlet-loop
- **Added:** 2026-08-04
- **Summary:** A builder-and-independent-critic prompting method that repeatedly compares agent output against a concrete quality bar.
- **Why explore it:** Evaluate whether the approach could improve long-running, quality-driven agent workflows.
- **Status:** Carried over from the pre-rewrite backlog. A similar independent-reviewer pattern already exists for reference-matched documents; keep this only if further rollout is wanted.

## Memory → OKF as a memory.md replacement

### Google OKF (Open Knowledge Format) as a `memory.md` replacement

- **Added:** 2026-09-13
- **Source:** current thread — you asked to explore Google's OKF to replace `memory.md`.
- **Spec:** https://github.com/GoogleCloudPlatform/open-knowledge-format (canonical repo, v0.2 `SPEC.md`; the older `knowledge-catalog/okf/` copy is a frozen snapshot)
- **Background:** https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals/
- **Summary:** vendor-neutral Markdown plus YAML frontmatter for agent knowledge. v0.2 adds optional `generated`, `verified`, `sources`, `status`, and `stale_after` signals, trust tiers derived from verification, progressive disclosure via `index.md`, and graph-shaped cross-links. Only `type` is required; custom keys are preserved.
- **Why it may fit:** current specialist memory is already Markdown and git-adjacent; OKF would add per-fact provenance, verification state, freshness dates, and selective loading instead of injecting the whole file. Its tooling story (reference producer, visualizer, ecosystem linters) matches the TX-style memory workflow.
- **Open questions:** OKF targets catalog knowledge, not conversational memory — scoping (specialist vs thread), retention, expiry, deletion, and privacy mapping still need a trial design. Private memories must never enter the public repo, even as OKF bundles.
- **Success criterion:** convert one specialist's memory to a trial OKF bundle with a selective loader, then prove scoped injection, retention/expiry, deletion, and no cross-specialist leakage before any migration.

## Tool documentation → synthetic visuals

### Synthetic screenshots for the tool catalog

- **Added:** 2026-09-13
- **Source:** Current thread — you asked for tool documentation with screenshots and graphs where useful.
- **Question:** Which setup or troubleshooting screenshots would materially help `docs/tools.md` without exposing real channels, accounts, conversations, hostnames, or service state?
- **Success criterion:** A synthetic demo workspace produces reproducible placeholder screenshots with stripped metadata, or the Mermaid diagrams in `docs/tools.md` are confirmed sufficient and this item is closed.
