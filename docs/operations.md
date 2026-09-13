# Operations

## Suggested filesystem layout

Use installation-specific paths outside the repository. A generic layout is:

```text
/opt/pi-discord-specialists/       # root-owned deployed application code
/etc/pi-discord-specialists/       # root-owned configuration and secret references
/var/lib/pi-discord-specialists/   # sessions, state, specialist memory
/var/cache/pi-discord-specialists/ # disposable caches
/var/log/pi-discord-specialists/   # optional rotated logs
```

Generated thread files should live below a thread-scoped directory under the state root. Do not let a model choose an absolute output path.

## Deployment sequence

1. Create an unprivileged service user with no interactive login.
2. Install a pinned Pi version and reviewed dependencies.
3. Deploy root-owned bridge code to `/opt`.
4. Copy [`reference/config.example.json`](../reference/config.example.json) to a non-repository location and replace placeholders locally.
5. Store secrets separately with mode `0600`.
6. Create state/cache directories owned only by the service user.
7. Install and adapt the example systemd units.
8. Run configuration, protocol, and tool-policy tests.
9. Start the socket/helper services before the bridge if applicable.
10. Enable the scheduler only after normal interactive turns are stable.

The included units are examples, not copy-paste production defaults. Review paths, users, hardening flags, write directories, and network requirements for the host.

## Validation checklist

### Bridge

- A top-level channel message creates exactly one thread.
- The starter prompt is delivered exactly once.
- Two different threads receive different session files.
- Restarting the bridge resumes both sessions.
- Concurrent messages in one thread are serialized.
- A message in an unconfigured channel is ignored.
- Bot-authored ordinary messages do not trigger agent runs.
- Oversize or unsupported attachments fail safely.

### Tools

- Ordinary specialists cannot call filesystem or shell built-ins.
- Each specialist sees only its configured extension tools.
- Invalid hosts, paths, services, IDs, and action names are rejected.
- Destructive actions require the intended confirmation.
- Responses and errors are bounded and redact credentials.
- Cancellation reaches subprocesses and network requests.
- Tests do not touch live accounts or production state.

### Scheduler

- One-off, recurring, and cancellation flows are deterministic.
- Jobs persist across scheduler restarts.
- Duplicate delivery is prevented or safely idempotent.
- Autonomous runs require a valid fresh signature.
- A signature for one thread cannot be replayed into another.
- Repeated delivery failures disable or quarantine the job.

### Provider fallback

- Persistent provider failures advance one level.
- Transient connection failures remain visible and retryable.
- The active fallback level survives bridge restart.
- Replies disclose the active model when not on the configured primary.
- A fallback cannot gain a broader tool set.

## Routine commands

Adapt unit names to the deployment:

```bash
sudo systemctl status pi-discord-specialists
sudo journalctl -u pi-discord-specialists --since '30 minutes ago'
sudo systemctl status pi-discord-scheduler
sudo systemctl restart pi-discord-scheduler
```

A bridge restart interrupts active turns. Validate first, then restart during a controlled window or use a delayed service action after reporting completion.

## Backups

Back up only what is actually needed for recovery:

- sanitized application/config templates;
- specialist personas and intentionally retained memory;
- session state if conversation recovery is required;
- scheduler state;
- integration metadata that cannot be recreated.

Encrypt backups that include sessions, memory, OAuth material, or user documents. Keep credentials logically separate so restoring a conversation archive does not automatically restore broad external access.

## Updating

1. Read upstream Pi release notes and relevant installed documentation.
2. Review extension API changes.
3. Test RPC framing, event handling, session resume, and tool schemas in staging or with temporary state.
4. Run privacy and secret scans on any public changes.
5. Deploy code without copying development logs or fixtures containing user data.
6. Restart only affected services.
7. Check status and recent logs after deployment.
8. Keep a known rollback artifact and configuration backup.
