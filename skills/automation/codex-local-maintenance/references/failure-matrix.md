# codex-local-maintenance failure matrix

## Version and update

| Signal | Likely cause | Action |
| --- | --- | --- |
| `codex` resolves under `~/.bun/bin` | Bun-global CLI install | Use Bun metadata and `codex --version` as local evidence |
| Bun install stalls | proxy-distorted registry fetch or network path issue | Try no-proxy or proxy-pinned download after inspecting current processes |
| package directory updated but metadata old | manual replacement skipped Bun global metadata | Inspect package dir, global `package.json`, lockfile, and final binary version |
| Desktop app version differs from CLI | App bundle and CLI release separately | Report both surfaces separately |

## Proxy

| Signal | Likely cause | Action |
| --- | --- | --- |
| Internal MCP returns external web/login page | shell proxy variables distort internal traffic | Strip uppercase/lowercase proxy env and npm proxy env at MCP startup |
| CLI works but Desktop does not | Electron app path differs from shell path | Inspect launcher, Proxifier/Clash routing, and app logs |
| Browser works but Codex app fails | browser and app use different network path | Compare proxy client rules and app process routing |

## Desktop latency

| Signal | Likely cause | Action |
| --- | --- | --- |
| long gap before first visible token | queueing, websocket, model routing, proxy, or local load | Use logs and timestamps before choosing cause |
| many old/local sessions active | local state or queued follow-up noise | Inspect current thread/session state before clearing anything |
| high CPU/memory pressure | local machine load | Inspect process list and report impact without killing unrelated processes |

## Safety

- Do not delete `~/.codex`, app support data, or caches without explicit user permission.
- Do not paste secret-bearing config lines into chat.
- Do not claim an update or fix is complete until a final command verifies it.
