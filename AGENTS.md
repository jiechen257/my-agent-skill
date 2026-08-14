# my-agent-skill 仓库规则

本仓库维护个人 Codex rules、skills、templates、registry 和上游 skill 镜像。

## 目录职责

- `rules/codex-global.md` 是 `~/.codex/AGENTS.md` 的版本化源，修改后保持两者一致。
- `skills/*` 是主动入口；本地策略、平台开关和兼容修正写在 wrapper 中。
- `vendor/skills/*` 是上游同步源，不是 active skill surface，不直接手改。
- `registry/skills.yaml` 只登记真实存在并需要安装或发布的 skill。
- `templates/trellis-matt-profile/` 是 Trellis + Matt Profile 的统一模板源。
- `docs/` 保存设计结论、调研证据和使用说明，不承担运行时注入。

## 修改边界

- 更新 wrapper 时保留上游来源关系；需要改变上游行为时在 wrapper 中覆盖并说明原因。
- 不把密钥、登录态、机器凭证或目标业务项目的运行数据写入本仓库。
- qianwen、nexview-devtools 的 Trellis Profile 保持本地-only；personal-kb 明确允许版本化。
- 目标项目已有脏改动不属于本仓库工作，安装或同步时只触碰明确的 Profile 文件。
- 新增或大改 skill 后运行 quick validation；涉及模板时验证源文件与目标副本一致。
- 只有用户明确要求时才执行 commit、push 或 PR。
