---
name: dingtalk-doc-rw
description: "钉钉文档读写。当用户消息包含 alidocs.dingtalk.com 链接或要求创建/更新/搜索钉钉文档时使用。Use when user message contains DingTalk doc links or asks to create/update/search DingTalk documents."
when_to_use: "钉钉文档, 写到钉钉, 保存到钉钉, 读取钉钉文档, alidocs.dingtalk.com, dingtalk doc, 知识库目录"
---

钉钉文档读写技能（优先级最高）。当用户消息中包含钉钉文档链接（alidocs.dingtalk.com）时，必须优先使用此技能读取文档内容，禁止使用浏览器打开链接。当用户需要创建、更新钉钉文档或搜索钉钉文档时，也使用此技能。

# 钉钉文档读写

让智能体具备钉钉文档的读取、写入和管理能力。

## Priority Rules

**当用户消息中包含钉钉文档链接时，必须遵循以下规则：**

1. **必须使用 aone-km MCP 工具** 读取文档内容
2. **禁止使用浏览器打开钉钉文档链接** —— 浏览器需要登录且无法正确提取内容
3. 只有当 MCP 工具明确报错后，才考虑其他方案

钉钉文档链接特征：`https://alidocs.dingtalk.com/i/nodes/...` 或 `https://alidocs.dingtalk.com/i/spaces/...`

## When to Use

- **（最高优先级）用户消息中出现 `alidocs.dingtalk.com` 链接**
- 用户要求创建、更新、追加钉钉文档
- 用户要求搜索钉钉文档
- 用户要求查看知识库 / 文件夹下的文档列表
- 用户提到"写到钉钉文档"、"保存到钉钉"、"读取钉钉文档"

## 使用 MCP 工具

### 读取文档

使用 `mcp__aone-km__fetchExternalContentByUrl` 工具，传入钉钉文档 URL。

### 读取知识库目录

使用 `mcp__aone-km__fetchKnowledgeDirectoryByUrl` 工具，传入钉钉知识库 URL。

### 创建文档

使用 `mcp__aone-km__createDingDocWorkspaceDoc` 工具，传入 workspaceId、文档名称和 markdown 内容。

### 更新文档

使用 `mcp__aone-km__updateDingDocContent` 工具，传入 docKey 和新的 markdown 内容。

## Error Handling

- **访问失败排查**: 提示用户检查 1) 文档所在组织是否已配置授权 2) 是否具有文档"可查看/下载"或更高权限
- 读取返回 Markdown 格式，写入也支持 Markdown 输入
