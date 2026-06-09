---
name: mcp-healthcheck
description: Use when the user asks to inspect, validate, or troubleshoot Codex MCP servers on this Mac, including reachability, authentication class, proxy/no-proxy behavior, command availability, tool-list drift, or write-tool risk.
---

# MCP Healthcheck

Run a read-only health check for configured Codex MCP servers. Keep the output safe: redact credentials, classify failures, and do not mutate `~/.codex/config.toml` unless the user explicitly asks for a config change.

## Scope

Use this skill for:

- MCP reachability and auth-state checks
- proxy versus no-proxy diagnosis for internal endpoints
- local stdio MCP command availability
- checking whether configured MCPs expose risky write tools
- explaining MCP failures such as timeout, 401, 403, 405, invalid URL, missing command, or stale `npx` cache

Do not use this skill to install new MCP servers. Do not print tokens, headers, cookies, database URLs, or full env values.

## Workflow

```text
[1] Inspect configured servers
      -> read ~/.codex/config.toml and identify remote HTTP endpoints plus local stdio commands

[2] Run read-only probes
      -> use scripts/check-mcp-health.sh for command checks, endpoint HEAD/initialize probes, and proxy comparison

[3] Classify each result
      -> reachable/auth-needed, wrong route, missing command, timeout, or config-risk

[4] If tool-list detail is needed
      -> use available MCP client/tool discovery surfaces; do not hand-roll auth protocol framing

[5] Report the action path
      -> exact server, observed class, likely cause, and smallest safe fix
```

## Rules

- Treat `401` on an initialize probe as an auth-required but reachable endpoint.
- Treat `405` on a HEAD/GET probe as a useful reachability signal for MCP HTTP endpoints that only accept POST.
- For Alibaba internal MCPs, compare current proxy env with a proxy-stripped run before blaming auth or the service.
- For local stdio MCPs, verify command existence first. Launch only when the user asks for deeper runtime debugging.
- For write tools, prefer disabling high-risk tools in config or adding approval gates.
- Keep `basic-memory.write_note` behind approval unless the user explicitly changes the policy.

## Helper

Run from this skill directory or with an absolute path:

```bash
scripts/check-mcp-health.sh
```

Optional:

```bash
CODEX_CONFIG=/path/to/config.toml scripts/check-mcp-health.sh
```

## Verification

Minimum completion evidence:

- list the checked MCP server names
- include endpoint status classes or command availability
- state whether proxy/no-proxy behavior differs for internal endpoints
- state any skipped checks and why
