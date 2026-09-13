# Sanitized specialist personas

These standalone `AGENTS.md` examples show how a specialist's mission, working method, evidence standard, tool use, confirmation rules, and response style can be expressed.

They are rewritten public examples—not exports of deployed prompts. They intentionally omit user profiles, shared memory, conversations, account identifiers, credentials, private URLs, hostnames, network details, device information, filesystem paths, and integration state.

## Important security distinction

An `AGENTS.md` communicates policy intent to the model. It is not an access-control boundary. Enforce every material restriction in tool schemas, extension code, service permissions, OAuth scopes, filesystem ownership, network policy, and confirmation gates.

Tool names in these examples are illustrative. A deployment should expose only tools that actually exist and are technically constrained as described.

## Examples

- [Cooking](cooking/AGENTS.md)
- [Finance](finance/AGENTS.md)
- [Gardening](gardening/AGENTS.md)
- [Marketplace research](marketplace-research/AGENTS.md)
- [Job search](job-search/AGENTS.md)
- [Shopping](shopping/AGENTS.md)
- [Media stack](media-stack/AGENTS.md)
- [Infrastructure](infrastructure/AGENTS.md)
- [Travel](travel/AGENTS.md)
- [Trends and intelligence](trends/AGENTS.md)
- [Project evaluator](project-evaluator/AGENTS.md)

## Adapting a persona

1. Replace generic jurisdiction, language, unit, and workflow assumptions with explicit deployment configuration.
2. List only tools exposed to that specialist.
3. Put destructive or externally visible actions behind technical confirmation checks.
4. Keep durable memory in a separate file and store only concise, non-secret facts.
5. Test the tool boundary with adversarial pages, attachments, logs, and prompts.
6. Re-run the public-repository privacy gate before publishing changes.

Use the [blank memory template](../specialist-template/memory.md) rather than publishing real specialist memory.
