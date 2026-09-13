# Pi Discord Specialists

A public, sanitized blueprint for a private self-hosted Discord workspace backed by persistent [Pi](https://pi.dev) agent sessions.

The platform is the primary focus of this repository. It documents the architecture, capability boundaries, security model, operations, and reusable configuration patterns from a working deployment without publishing production code, credentials, account identifiers, private network details, user data, conversation history, or service state.

## What the platform does

- Maps each Discord text channel to a specialist role.
- Turns each top-level request into a thread with its own persistent Pi session.
- Keeps durable memory separate per specialist while conversation history remains thread-specific.
- Runs ordinary specialists without Pi's built-in filesystem or shell tools.
- Exposes only purpose-built extension tools with bounded inputs, outputs, destinations, and side effects.
- Supports images, text files, PDFs, generated documents, and thread-local uploads.
- Falls back across model providers when a persistent provider failure occurs.
- Supports scheduled posts and explicitly authorized autonomous thread runs.
- Integrates external services through constrained helpers or narrowly scoped MCP servers.
- Retains one deliberately privileged infrastructure specialist for maintenance.

## Start here

- [Architecture](docs/architecture.md) — components, session lifecycle, policy layers, tool boundaries, scheduling, integrations, and reliability.
- [Capability catalog](docs/capabilities.md) — generalized snapshot of the current specialist and companion-service capabilities.
- [Tool catalog and access scopes](docs/tools.md) — current extension tools, specialist assignments, enforcement layers, and access diagrams.
- [Security and privacy](docs/security.md) — least privilege, secret handling, prompt-injection resistance, scoped-tool checklist, and release gate.
- [Operations](docs/operations.md) — deployment sequence, validation, backups, updates, and recovery practices.

## Reference material

- [Sanitized configuration](reference/config.example.json)
- [Eleven sanitized specialist personas](reference/specialists/README.md)
- [Specialist persona template](reference/specialist-template/AGENTS.md)
- [Blank specialist memory](reference/specialist-template/memory.md)
- [Example systemd units](reference/systemd/)

These are reference files, not a turnkey export of the private deployment. Replace placeholders locally and keep runtime configuration outside the checkout.

## Architecture at a glance

```text
Discord channel -> specialist policy and bounded tool set
Discord thread  -> independent persistent Pi RPC session
Scheduler       -> signed, thread-bound scheduled instructions
Extensions      -> narrow tools and service adapters
Local helpers   -> isolated service users and permissioned sockets
```

The bridge can stop idle Pi processes while retaining session files, then resume the same context when a later thread message arrives.

## Repository structure

```text
docs/                       Platform architecture and operating guidance
reference/                  Sanitized configuration and service templates
resources/                  Explored and prospective AI workflow ideas
experiments/                Prototypes and tests
scripts/check_public_repo.py
```


## Privacy gate

Before publishing changes, run:

```bash
python3 scripts/check_public_repo.py
```

GitHub Actions runs the same dependency-free check on pushes and pull requests. It detects high-confidence secrets and private deployment identifiers, but it complements rather than replaces manual review and a maintained secret scanner.

## Scope and roadmap

The current release is an implementation-oriented blueprint. A future milestone is a clean, runnable reference bridge and extension set designed for public reuse instead of copying tightly coupled production files.

## License and status

Work in progress. Interfaces, tools, and operational recommendations will evolve as Pi and the deployment change.
