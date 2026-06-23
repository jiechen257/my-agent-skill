# Agent Plugins

这里收录完整 agent plugin。它们保留上游插件结构，和 `skills/` 下的单个 skill 分开管理。

## Ponytail

- Path: `plugins/ponytail`
- Upstream: https://github.com/DietrichGebert/ponytail
- Source ref: `main@dedc97ca7c8a1e7463ac5b36f7fe4b28c3c435a2`
- Version: `4.7.0`
- License: MIT

收录范围只包含 Codex 插件运行需要的文件：

- `.codex-plugin/plugin.json`
- `skills/`
- `hooks/`
- `commands/`
- `assets/logo.png`
- `README.md`
- `LICENSE`

本仓库没有为它生成 marketplace 入口。需要在 Codex 里安装时，优先使用上游 marketplace：

```bash
codex plugin marketplace add DietrichGebert/ponytail
```

然后在 Codex `/plugins` 中安装 `ponytail`，再到 `/hooks` 审核并信任它的 lifecycle hooks。
