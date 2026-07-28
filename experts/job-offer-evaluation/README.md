# Offer Intelligence MCP

A local, read-only MCP gateway and shared methodology for evidence-first job-offer
evaluation. Cursor, Codex, and Claude can launch the same Python module over stdio.

The server helps retrieve public evidence. The agent remains responsible for selecting
relevant sources, checking contradictions, citing claims, and applying the methodology
in [`methodology.md`](methodology.md).

## What this project does

- supports public web research for a role and employer;
- returns source metadata suitable for citations and an evidence ledger;
- keeps the evaluation workflow consistent across supported clients;
- makes access failures and uncertainty visible rather than filling gaps with guesses.

It does not submit applications, contact employers, automate credential entry, or
guarantee access to any third-party website. Glassdoor and similar sites may block
automation, require the user to sign in manually, or expose only limited content.

## Requirements

- macOS with Command Line Tools (`xcode-select --install`)
- Python 3.12 through 3.14
- `pip` and `venv` (included with Python.org and Homebrew Python)
- a Chromium browser installed for Patchright when browser-backed retrieval is used
- Cursor, Codex, and/or Claude Code with MCP support

The package installs `uv` into the project environment because the optional LinkedIn
adapter launches its upstream package with `uvx`; no separate global `uv` install is
required.

## Install

Install Python with Homebrew if a compatible interpreter is not already available:

```bash
brew install python
python3 --version
```

Clone the repository and run the setup script:

```bash
git clone https://github.com/vanvalentin/vv-ai-toolkit.git
cd vv-ai-toolkit
python3 experts/job-offer-evaluation/scripts/setup.py
```

The script creates `.venv`, installs the package and development checks in editable
mode, and installs the managed Patchright Chromium build. It is safe to rerun; an
existing environment is reused.

Activate the environment for manual commands:

```bash
source .venv/bin/activate
python -c "import offer_intel; print(offer_intel.__file__)"
```

The checked-in Cursor, Claude Code, and Codex configurations launch
`.venv/bin/python -m offer_intel` directly, so no global package installation or PATH
modification is needed.

## Verify the module

With the environment active:

```bash
python -c "import offer_intel; print(offer_intel.__file__)"
python -m offer_intel.connectors.glassdoor
python -m offer_intel
```

The second command reports Glassdoor connector viability, browser backend, profile
location, and current session state without promising page access. The third starts an
MCP stdio process and may wait silently for a client. Stop it with `Ctrl+C`. Protocol
messages use standard input/output; diagnostics should go to standard error so they do
not corrupt MCP traffic.

## Client configuration

The repository includes:

- Cursor: `.cursor/mcp.json`
- Claude Code: `.mcp.json`
- Codex: `.codex/config.toml`

Each defines an `offer-intel` stdio server equivalent to:

```bash
.venv/bin/python -m offer_intel
```

with the repository root as its working directory. Restart or reload the client after
installation or configuration changes, then confirm that `offer-intel` appears in its
MCP server/tool list with tools such as `create_offer_case`.

### Cursor

Open the repository as the workspace. Cursor expands `${workspaceFolder}` in
`.cursor/mcp.json`. Enable the project MCP server if prompted. If startup fails, verify
the interpreter resolution from Cursor's environment and inspect MCP logs for an import
or browser-install error.

### Claude Code

Start Claude Code from the repository root. `.mcp.json` uses
`${CLAUDE_PROJECT_DIR}` for the working directory. Review and approve project MCP
configuration when Claude asks; project configuration is code and should be trusted
only after inspection.

The thin Claude skill is at
`.claude/skills/job-offer-evaluation/SKILL.md` and delegates to the canonical skill and
methodology.

### Codex

Start Codex from the repository root so the relative interpreter and `cwd` in
`.codex/config.toml` resolve correctly. If the client is launched elsewhere, use its
project-root option or machine-local absolute paths.

The canonical portable skill is at
`.agents/skills/job-offer-evaluation/SKILL.md`.

## Using the workflow

Provide a posting URL or redacted posting text and a concise profile:

- goals and hard constraints;
- relevant experience and transferable skills;
- location, work authorization, and work-arrangement constraints;
- compensation expectations when useful;
- specific concerns to verify.

Ask the agent to use the job-offer-evaluation skill. A full result should include a
recommendation, confidence, role snapshot, profile fit, employer evidence, risks,
weighted scorecards, questions to ask, citations, and limitations.

The gateway's core sequence is:

1. `create_offer_case` creates an in-memory case.
2. Connector output or host research is recorded; `add_external_evidence` assigns
   source and evidence IDs to host-collected material.
3. `get_evidence_pack` exposes sources, evidence, conflicts, and blind spots.
4. `score_offer_case` computes four inspectable scorecards from cited rubric inputs.
5. `validate_offer_report` checks material claim coverage, freshness, known IDs, and
   blind-spot disclosure before the final answer.

The server's `EV-*` and `SRC-*` identifiers provide traceability inside a case. Final
reader-facing claims should also link to the underlying source URL. Cases are
in-memory by default and disappear when the server process exits.

For good results:

1. Preserve the original posting.
2. Research only decision-relevant unknowns.
3. Prefer direct and authoritative sources.
4. Treat review platforms as sampled anecdotes, not ground truth.
5. Keep evidence, user statements, and inference visibly separate.
6. Resolve contradictions or lower confidence.
7. End with an actionable next step.

The detailed scoring rubric, evidence ledger, source hierarchy, and stopping rules are
in [`methodology.md`](methodology.md).

## Privacy

Assume prompts and tool arguments may appear in local client logs. Use the minimum
personal information necessary:

- redact name, address, phone, email, IDs, exact birth date, and signatures;
- remove private application tokens and tracking links;
- summarize a CV rather than passing the original when possible;
- do not include current-employer secrets, customer data, or confidential interview
  material;
- do not commit real CVs, correspondence, offers, credentials, or generated reports
  containing private data.

The checked-in MCP configs contain no secrets; their only environment setting
suppresses the server banner on stdio. Do not add passwords, cookies, API keys, or
tokens to them.

## Authentication and access controls

The gateway is intended for public research. The Glassdoor connector uses a dedicated
persistent browser profile outside the repository. Its default location is:

```text
~/Library/Application Support/vv-ai-toolkit/browser-profiles/glassdoor
```

Use the MCP tools `glassdoor_check_viability`, `glassdoor_login`, `glassdoor_status`,
and `glassdoor_logout` for the local Glassdoor profile. The current implementation
stops and reports a challenge rather than trying to bypass it.

Company data collection opens a **visible Chromium window by default** (same profile as
login). This improves success rates on regional sites and Cloudflare-protected pages.
Set `GLASSDOOR_HEADLESS=true` in the MCP server environment to return to headless
collection. Status and viability checks remain headless.

Authenticate the upstream LinkedIn server separately:

```bash
python experts/job-offer-evaluation/scripts/linkedin_login.py
```

Complete all credentials, verification, and CAPTCHA steps yourself in the browser
window. The gateway never receives those credentials.

If an exposed session-status check reports that authentication is required, an exposed
manual-login action may open a headed browser. The user must enter credentials directly
on the website. Credentials must never be sent in chat or as MCP arguments. The
connector does not fill login forms, and it stops rather than solving a CAPTCHA or
verification challenge. A local logout action clears cookies from this dedicated
profile without sending a website logout request.

An authenticated session may expire, may not unlock a page, and may be rejected by the
site at any time. It does not guarantee live Glassdoor access. The profile can contain
sensitive session cookies: keep it private, do not sync or commit it, and delete or
clear it when no longer needed.

The server should not be given:

- account credentials;
- exported browser profiles or session cookies;
- CAPTCHA-solving services;
- private document or application URLs;
- instructions to evade a paywall, robots policy, rate limit, or access restriction.

If a site presents a challenge, stop using that source. The user can instead inspect it
themselves and provide a short, non-confidential summary, which must be labeled as
user-provided rather than independently verified.

No claim should imply guaranteed live access to Glassdoor, LinkedIn, or another
protected or dynamic site. Availability varies by location, session, site policy,
anti-bot controls, and page implementation.

The optional LinkedIn adapter is deliberately read-only and excludes messaging
capabilities. It uses the `uvx` executable installed beside the project interpreter and
reports unavailable if that executable cannot be found. This does not prevent the main
`offer-intel` gateway from starting. Do not add tokens to the project configs; any
optional upstream authentication should be completed using that upstream tool's own
local flow.

## Troubleshooting

### `No module named offer_intel`

The client is using a different Python interpreter or the editable package was not
installed. Run:

```bash
python -m pip show offer-intel-mcp
python -c "import sys; print(sys.executable)"
```

Repeat those checks in the environment from which the client starts, then install with
that interpreter.

### Browser executable is missing

Install the managed browser with the same interpreter:

```bash
python -m patchright install chromium
```

### MCP stays on "loading" or only shows `mcp_auth`

Cursor launches MCP with a minimal environment. A bare `python` command may resolve to
the wrong interpreter or not resolve at all, so the server never finishes starting.

- confirm `.cursor/mcp.json` points at `${workspaceFolder}/.venv/bin/python`;
- reload MCP or restart Cursor after editing the config;
- start a new chat once the server shows tools such as `create_offer_case`;
- smoke test manually with `.venv/bin/python -m offer_intel` from the repository
  root.

### Server exits or tools do not appear

- run `python -m offer_intel` manually and inspect standard error;
- verify the client opened the repository root;
- validate the JSON/TOML config and working directory;
- restart the client after changing its environment;
- confirm that server logs are not written to standard output.

### A page is blocked or empty

This can be normal for authenticated, dynamic, consent-gated, rate-limited, or
anti-bot-protected sites. Do not retry aggressively or bypass the control. Record the
failure, use a lawful public alternative, and lower confidence if the missing evidence
matters.

## Limitations

- Public data may be stale, inaccurate, incomplete, or scoped to another region or
  business unit.
- Dynamic pages and PDFs may extract imperfectly.
- Salary and employee-review datasets are self-selected and may have small samples.
- Company-wide evidence may not represent a specific team or manager.
- The workflow cannot validate private recruiter claims or predict hiring outcomes.
- Scores depend on user priorities and evidence quality; they are not objective ratings.
- Results are not legal, immigration, tax, financial, or professional career advice.

## Development

Install development dependencies with ordinary `pip`:

```bash
python experts/job-offer-evaluation/scripts/check.py
```

The check script runs the tests, linter, factuality evaluation, and dependency check
using the project virtual environment.

Do not emit secrets or fetched personal content in fixtures, snapshots, logs, or error
messages. Use synthetic or anonymized test data.
