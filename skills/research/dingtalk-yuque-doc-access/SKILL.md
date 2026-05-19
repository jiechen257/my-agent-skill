---
name: dingtalk-yuque-doc-access
description: Use when the user asks to read, verify, summarize, or troubleshoot DingTalk, AliDocs, Yuque, or Alibaba internal document links, especially with aone-km, MCP direct access, INVALID_URL, READ_FAILED, UNAUTHORIZED, or overview/permalink confusion.
---

# dingtalk-yuque-doc-access

Read and diagnose internal DingTalk, AliDocs, and Yuque documents through the right document-access path. Start from the link shape and available MCP tools, then report whether the document is readable under current auth.

## Scope

Use this skill for:

- DingTalk / AliDocs / Yuque link readability checks
- `aone-km` direct-access attempts
- URL-shape diagnosis for overview, node, space, repo, and page links
- failure interpretation for `INVALID_URL`, `READ_FAILED`, `UNAUTHORIZED`, OAuth, or MCP routing errors
- converting readable internal docs into Markdown, summaries, reports, or module-based merges

Do not use this skill for browser-first browsing of internal docs when an MCP path is available. Do not claim a permission issue until the correct URL/tool path has been tested.

## Inputs

| Input | Meaning |
| --- | --- |
| Source link | DingTalk, AliDocs, Yuque, repo/page, or raw node URL |
| Desired output | Readability verdict, Markdown extraction, summary, report merge, or troubleshooting |
| Tool hint | User may explicitly request `aone-km`, MCP, or direct internal access |

## Workflow

```text
[1] Classify URL
      -> overview / node / document permalink / repo-page / Yuque doc

[2] Choose access path
      -> use available DingTalk/Yuque/aone-km MCP tools first when present

[3] Read or prove unreadable
      -> try the tool path that matches the URL shape; avoid repeating a known-invalid path

[4] Interpret result
      -> map success or failure to link format, auth, repo index, or MCP routing

[5] Produce requested output
      -> original extraction, Markdown, summary, module merge, or next action
```

## Rules

- When the user explicitly says `aone-km` or `直连`, start with that path.
- Treat `spaces/.../overview` as a space entry point, not a concrete document permalink.
- Treat `i/nodes/...` as a node clue; use a proper repo/page or supported document read path when required.
- Report exact failure class before giving general advice.
- If a readable document contains sensitive content, summarize safely unless the user explicitly needs exact text.
- Keep source URLs and document identifiers in the output when they are safe and useful for traceability.

## References

Read [`references/url-and-error-matrix.md`](./references/url-and-error-matrix.md) before interpreting document URL shapes or MCP errors.

## Verification

Minimum completion evidence:

- readability task: state which tool/path was tried and the observed success/failure class
- extraction task: show the source link/path and produce directly usable Markdown or summary
- troubleshooting task: map the error to one of link format, permission, repo/index mismatch, OAuth, MCP routing, or network/proxy
