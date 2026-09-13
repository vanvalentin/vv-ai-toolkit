# Pi Discord Specialists

A sanitized reference architecture for a private Discord workspace backed by persistent [Pi](https://pi.dev) agent sessions.

This documents the current design pattern without publishing the production bridge, credentials, account identifiers, host details, conversation history, specialist memory, or integration state.

## What the setup does

- Maps each Discord text channel to one specialist role.
- Converts each top-level user message into a thread with an automatically generated title.
- Gives every thread an independent persistent Pi session.
- Keeps durable memory separate per specialist and injects it into new turns.
- Runs ordinary specialists with Pi built-in filesystem and shell tools disabled.
- Adds only purpose-built extension tools with bounded inputs, outputs, destinations, and side effects.
- Supports images, text files, PDFs, generated documents, and thread-local uploads.
- Falls back across configured model providers when a persistent provider failure occurs.
- Supports one-off and recurring posts plus explicitly authorized autonomous thread runs.
- Integrates selected services through constrained helpers or MCP instead of broad shell access.
- Retains one deliberately privileged infrastructure specialist for maintenance.

## Why threads are the session boundary

A channel provides the stable specialist identity; a thread provides the conversation identity. This gives a natural mapping:

```text
Discord channel -> specialist policy and tool set
Discord thread  -> Pi RPC process and persistent session
```

The bridge can stop idle processes while retaining their session files, then resume the same context when a new message arrives.

## Included here

- [Architecture](architecture.md)
- [Current capability catalog](capability-catalog.md)
- [Security and privacy controls](security.md)
- [Operations and deployment sequence](operations.md)
- [Sanitized configuration example](config.example.json)
- [Specialist persona template](specialist-template/AGENTS.md)
- [Blank specialist memory file](specialist-template/memory.md)
- [Example systemd units](systemd/)

## Deliberate omissions

This folder is not a turnkey copy of the private deployment. It does not contain:

- Discord bot tokens, guild/channel/thread IDs, user IDs, or webhook URLs;
- OAuth records, API keys, cookies, browser profiles, or private certificates;
- private hostnames, LAN addresses, tailnet names, routes, or device identifiers;
- user conversations, attachments, CVs, spreadsheets, specialist memories, or logs;
- production paths, service users, helper sockets, caches, or state files;
- private integration code whose assumptions are specific to one host.

Use this as a design and hardening guide. Implement integrations independently and review every dependency before granting it code execution.

## Current specialist pattern

The deployment currently uses specialist roles for cooking, finance, gardening, shopping, travel, job search, media operations, trends, project evaluation, marketplace research, and infrastructure. The exact channel identifiers and private role instructions are intentionally excluded.

## Minimal build order

1. Install and authenticate Pi locally; never place provider credentials in this repository.
2. Create a Discord application with only the intents and channel permissions the bridge needs.
3. Implement the bridge over Pi RPC using strict LF-delimited JSONL framing.
4. Store one session directory per specialist/thread pair.
5. start all non-infrastructure sessions with `--no-builtin-tools`.
6. Add reviewed Pi extensions for each bounded capability.
7. Put runtime configuration and secrets outside the source tree with restrictive permissions.
8. Run the bridge and scheduler as unprivileged systemd services.
9. Exercise the abuse, restart, fallback, and recovery checks in [operations.md](operations.md).

Pi's Node SDK is preferable to a subprocess when the bridge and Pi run in the same Node.js process. RPC remains useful when process isolation and independent lifecycle control are priorities.
