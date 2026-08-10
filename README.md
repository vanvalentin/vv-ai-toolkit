# AI Toolkit

A public, evolving collection of the prompts, configurations, tools, and notes I use to get more useful results from AI.

## What's here

- **Experts** — reusable AI personas and workflows for specific tasks, such as tailoring a CV to a job offer, adapting recipes, or evaluating a company and role against my profile.
- **Resources** — links, articles, examples, and ideas to explore or revisit.
- **Experiments** — code, writing, and prototypes created while testing AI-assisted workflows.

## Available experts

- [Portable Offer Intelligence](experts/job-offer-evaluation/README.md) — a local,
  evidence-first MCP gateway and Agent Skill for critical company, role, candidate,
  and compensation research in Cursor, Codex, and Claude Code.
- [Interview preparation](experts/interview-prep/README.md) — Agent Skill and
  methodology for CV+JD interview prep packs and optional mock rounds, reusing
  `offer-intel` for public interview-process research when available.

## Quick start

Install the Command Line Tools and Python, then provision the repository:

```bash
xcode-select --install
brew install python
git clone https://github.com/vanvalentin/vv-ai-toolkit.git
cd vv-ai-toolkit
python3 experts/job-offer-evaluation/scripts/setup.py
```

Open the repository in Cursor, Claude Code, or Codex and approve the checked-in
`offer-intel` MCP configuration. The clients launch `.venv/bin/python` directly.
Restart the client after the first setup, then confirm the MCP tool list includes
`create_offer_case`.

For LinkedIn research, establish the local browser session:

```bash
source .venv/bin/activate
python experts/job-offer-evaluation/scripts/linkedin_login.py
```

See the [Offer Intelligence guide](experts/job-offer-evaluation/README.md) for client
configuration, Glassdoor login, verification, privacy, and troubleshooting.

## Proposed structure

```text
experts/
  cv-tailoring/
  recipe-adjustment/
  job-offer-evaluation/
  interview-prep/
resources/
  to-explore.md
  explored.md
experiments/
```

Each expert can include:

- a `README.md` explaining the intended use and inputs;
- the prompt or configuration files;
- supporting templates, examples, or scripts;
- notes on what worked and what did not.

## Contributing and privacy

This is primarily a personal knowledge base shared publicly. Please do not add private information, credentials, personal contact details, or proprietary materials. Use anonymized examples when an expert needs a CV, job offer, company information, or other sensitive context.

## Status

Work in progress — tools and conventions will change as the collection grows.
