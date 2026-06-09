---
name: codex-local-maintenance
description: Use when the user asks to inspect, update, or troubleshoot local Codex CLI/Desktop on this Mac, including version checks, Bun-global installs, proxy routing, first-token latency, logs, or launcher/state issues.
---

# codex-local-maintenance

Maintain and troubleshoot the local Codex environment with evidence from this machine. Use direct verification before claiming a version, update, routing path, or fix.

## Scope

Use this skill for:

- Codex CLI and Codex Desktop version checks
- local Codex CLI updates, especially Bun-global installs
- proxy routing problems involving shell env, Clash, Proxifier, or launcher scripts
- Codex Desktop first-token latency or stuck-session diagnosis
- read-only inspection of `~/.codex`, app logs, process state, and local launchers

Do not use this skill as permission to delete caches, edit global config, kill unrelated processes, or overwrite launcher scripts. Ask or state the exact boundary before mutating global state.

## Inputs

| Input | Meaning |
| --- | --- |
| Requested action | Check version, update CLI, diagnose proxy, inspect latency, or repair state |
| Target surface | CLI, Desktop app, MCP startup, proxy path, or all relevant surfaces |
| Network mode | Default shell env, no-proxy, or proxy-pinned path such as `127.0.0.1:7890` |

## Workflow

```text
[1] Classify request
      -> version/update/proxy/latency/state

[2] Collect local evidence
      -> run scripts/inspect-codex-local.sh when local paths, versions, logs, and proxy env matter

[3] Choose the narrow action
      -> read-only answer, update through installed package source, proxy-specific retry, or config review

[4] Verify result
      -> rerun version command, log check, network check, or user-requested target operation
```

## Rules

- When the user asks to update a local tool, perform the update and verify the binary/version at the end.
- For OpenAI product version facts, verify current official/latest metadata before comparing versions.
- Treat CLI and Desktop as separate surfaces: `codex` binary, Bun package metadata, and `Codex.app` bundle version can differ.
- For proxy issues, inspect shell proxy variables and launcher behavior before assuming a network root cause.
- For Desktop latency, prefer logs and timestamps over generic model/network speculation.
- Do not expose tokens, cookies, credentials, or full auth config values in chat.

## Read-Only Helpers

- `scripts/inspect-codex-local.sh`: collects Codex binary paths, versions, app bundle version, proxy env names, relevant process list, and recent log file candidates.

Run helper scripts from this skill directory or with an absolute path.

## References

Read [`references/failure-matrix.md`](./references/failure-matrix.md) when the task involves update failures, proxy confusion, or Desktop latency.

## Verification

Minimum completion evidence:

- version/update task: final `codex --version` plus package/app source inspected
- proxy task: current proxy env and at least one concrete routing or endpoint signal
- Desktop latency task: log/process/config evidence and the likely bottleneck stated as evidence-backed
- repair task: exact file/process/action changed plus post-change check
