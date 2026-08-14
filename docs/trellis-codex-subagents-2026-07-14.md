# Trellis 在 Codex 下采用子 Agent 的调研结论

日期：2026-07-14

## 结论

Codex 当前支持子 agent，Trellis 0.6.6 也修复了多项递归派发和收尾问题；但本机实际使用中，子 agent 的启动、上下文恢复和交接延迟高于收益。因此当前决策是：**默认不主动调用子 agent，Codex 保持 `inline`，由主会话完成实现和检查。**

`trellis-matt-implement`、`trellis-matt-check` 定义暂时保留为回滚资产，只有用户明确要求重新启用时才派发。平台能力“可用”不再等同于默认 workflow“值得使用”。

brainstorm、plan review、research、implement、check、最终验收和 spec promotion 均留在主会话。

## 一手资料证据

### Codex 当前能力

- OpenAI 当前文档说明，新版 Codex 默认启用 subagent workflow；自定义 agent 可以放在项目级 `.codex/agents/*.toml`。
- Codex 默认 `agents.max_depth = 1`：主会话可以派生直接子 agent，但子 agent 默认不能继续派生下一层。
- 子 agent 继承父会话的 sandbox 与 approval 设置；并行 agent 更适合只读探索、测试和总结，写密集型任务需要避免工作区冲突。

来源：[OpenAI Codex subagents](https://developers.openai.com/codex/subagents)

### Trellis 的修复轨迹

- [Issue #240](https://github.com/mindfold-ai/Trellis/issues/240) 记录了 Codex 子 agent 被 Trellis prompt 再次劫持、递归进入 implement 流程并自等待的问题。
- [Issue #241](https://github.com/mindfold-ai/Trellis/issues/241) 记录了父会话在收到完成通知后仍继续等待的问题。
- [0.5.5 migration](https://github.com/mindfold-ai/Trellis/blob/v0.6.6/packages/cli/src/migrations/manifests/0.5.5.json) 移除了会注入子会话的 Codex `SessionStart` bootstrap。
- [0.5.6 migration](https://github.com/mindfold-ai/Trellis/blob/v0.6.6/packages/cli/src/migrations/manifests/0.5.6.json) 要求 `fork_turns="none"`，并补充父会话的 list/verify/close/wait 收尾循环。
- [0.5.7 migration](https://github.com/mindfold-ai/Trellis/blob/v0.6.6/packages/cli/src/migrations/manifests/0.5.7.json) 引入 `codex.dispatch_mode`，并在 Trellis 子 agent 中关闭嵌套 multi-agent 工具，阻止递归派生与自等待。
- [0.5.9 migration](https://github.com/mindfold-ai/Trellis/blob/v0.6.6/packages/cli/src/migrations/manifests/0.5.9.json) 将默认值改为 `inline`，原因是 `fork_turns="none"` 的子会话可能丢失父任务上下文；`sub-agent` 保留为 opt-in。
- 当前 [trellis-implement agent](https://github.com/mindfold-ai/Trellis/blob/v0.6.6/packages/cli/src/templates/codex/agents/trellis-implement.toml) 仍显式关闭子会话的 multi-agent 能力。

## 本机现状

- `trellis --version`：`0.6.6`
- `codex --version`：`codex-cli 0.144.1`
- 全局规则已改为不主动调用子 agent；Profile 模板默认 `codex.dispatch_mode: inline`。
- qianwen、nexview-devtools 已同步为 `inline` 和主会话 implement/check；保留的 `trellis-matt-*` 文件不再自动使用。
- personal-kb 中已安装的 agent 定义仍可作为回滚参考，但不构成主动派发授权。
- Profile 的版本化源文件统一由 `templates/trellis-matt-profile/` 管理。
- Agent Space 仍维持先前的 Lite/inline 定制，不在本轮首批改造范围内。

因此本机版本与首批项目配置均满足受控试点条件；仍需通过真实任务 smoke test 验证完成通知和父会话回收。

## 对 Trellis + Matt 融合的约束

原生 Matt `research` 和 `code-review` 会继续派生子 agent，而 Trellis 子 agent 为避免历史死锁明确禁用了嵌套派生。因此不能在 `trellis-research` 或 `trellis-check` 子 agent 内原样调用这些 skill。

可采用两种方式：

1. 主会话调用 Matt skill，再把结果写回 Trellis task；或
2. 将 Matt 的方法压平到自定义 Trellis agent prompt 中，不在子会话里继续派生。

当前采用主会话压平流程：

```text
主会话
  -> trellis-brainstorm
  -> Matt grill 方法做 plan review
  -> task start
  -> 主会话应用 Matt implement/TDD 方法
  -> 主会话应用 review/check 方法并验收
  -> 可选 spec promotion
  -> finish/archive
```

## 未来重新启用子 agent 的条件

1. 项目显式设置 `codex.dispatch_mode: sub-agent`。
2. 恢复并定制 `trellis-implement`、`trellis-check`，需要时再恢复 `trellis-research`。
3. 派发 prompt 明确包含 active task 路径；所有上下文通过文件和 prompt 提供，不依赖继承会话历史。
4. 保持 `fork_turns="none"`，并保留子 agent 禁止嵌套派生的配置。
5. 同一工作区只允许一个写入 agent；implement 与 check 顺序执行。
6. 父会话按 list -> verify deliverable -> close -> wait 的确定性循环收尾。
7. 不继承 Matt `implement` 的自动 commit 行为；commit/push/PR 仍只在用户明确要求时执行。
8. 先做一次最小 smoke test，验证任务上下文、文件改动、完成通知和父会话回收，再扩大范围。

## 风险判断

| 项目 | 状态 | 判断 |
| --- | --- | --- |
| Codex 子 agent 平台能力 | 已可用 | 当前版本默认支持 |
| Trellis 子 agent 递归/自等待 | 基本解决 | 通过移除注入和禁用子会话协作工具结构性限制 |
| 父会话完成后的收尾 | 改善 | 仍依赖 prompt 与调度行为，不是硬协议保证 |
| 子会话任务上下文 | 部分解决 | 需要 pull-based context；也是 Trellis 仍默认 inline 的主要原因 |
| 并发写入 | 未自动解决 | 必须顺序执行或使用独立 worktree |
| 首批三个项目直接启用 | 已配置，待 smoke test | 使用自定义非嵌套 implement/check agent |

最终建议：**当前不采用主动子 agent；维持 inline 主会话流程。只有出现明确的并行收益并由用户点名时，才临时恢复受控、顺序的子 agent。**
