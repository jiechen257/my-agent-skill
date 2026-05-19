# DingTalk / Yuque URL and error matrix

## URL shapes

| URL shape | Meaning | Preferred handling |
| --- | --- | --- |
| `alidocs.dingtalk.com/spaces/.../overview` | Space or knowledge-base overview | Ask for the exact document permalink or use a directory/list tool if available |
| `alidocs.dingtalk.com/i/nodes/...` | Node/page clue, often not accepted by directory URL readers | Use the proper repo/page read path or search path; do not retry as a space URL |
| Concrete AliDocs document permalink | Specific document target | Try the DingTalk/AliDocs MCP read tool directly |
| Yuque document URL | Specific Yuque document target | Try Yuque/aone-km MCP read path before browser/curl |
| Repo/page identifiers | Internal knowledge-base page target | Use repo/page content tools when available |

## Error classes

| Error | Meaning | Next action |
| --- | --- | --- |
| `INVALID_URL` | The tool rejects the URL shape | Reclassify the link and request a supported permalink or repo/page identifier |
| `READ_FAILED` | Tool reached the repo/index but did not read that page | Check repo/page mismatch, search nearby titles, or ask for the exact link |
| `UNAUTHORIZED` | Current account lacks access under that tool/auth scope | Tell the user the current auth cannot read it and request access or exported content |
| OAuth/auth challenge | MCP endpoint is reachable but auth is missing/expired | Complete auth flow or use the configured authenticated tool |
| External web/login response | Internal access may be routed through the wrong proxy | Use no-proxy MCP startup or the documented internal route |
| Transport/framing error | Manual MCP framing or client transport issue | Use the platform tool/client instead of hand-built protocol text |

## Output guidance

- For read success, produce the requested artifact and mention the access path.
- For read failure, lead with the concrete verdict: invalid link shape, unreadable page, no permission, or transport/auth issue.
- For overview links, request the exact document permalink as the next action.
