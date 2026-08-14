# Codex 日常 Prompt 手册与 Hooks 方案

本文整理适合当前工作流的日常 Prompt，并设计一种不需要每次输入完整标准文案的使用方式。

当前状态：Prompt 文档和全局 rules 已落地；Hooks 部分仅为方案，不安装、不启用，也不修改现有 hook/config。

## 使用原则

- 日常优先输入“短触发词 + 当前任务”，不重复全局 rules 已覆盖的证据、权限和输出约束。
- 完整 Prompt 用作复杂任务、交接、纠偏和验收基线，不要求每次原样粘贴。
- 稳定个人约束放在全局 rules；可复用工作流交给 skills；hook 只承担轻量、确定性的自动路由。
- 如果简短意图已经能稳定触发正确 skill，不为自动化而额外增加 hook。

## 快速入口

| 场景 | 日常短 Prompt | 期望路由 |
| --- | --- | --- |
| 运行时根因分析 | `分析根因：[现象]，先不要改代码` | `diagnosing-bugs` |
| 根因明确的小修 | `最小修复：[目标]` | Inline；超出单文件或根因明确边界时再转 `implement` |
| Review 本地变更 | `review 本地变更，对照 [需求/Spec]` | `code-review` |
| QWork/Nano 验收 | `验收 Nano：[卡片/任务]` | `qwork-nano-runbook` |
| 持久任务规划 | `规划 Trellis：[目标]，先不实现` | 已有 `.trellis/workflow.md` 时用 `trellis-brainstorm`；否则 Inline 规划且不初始化 |
| 技术调研选型 | `调研选型：[决策问题]` | `tech-solution-radar` |
| 日报 | `生成今天的项目日报` | `project-daily-summary` |

## 完整 Prompt 模板

### 1. 当前运行时问题：只分析根因

```text
分析 [仓库/功能] 中的这个问题：[现象和复现方式]。

当前阶段只读，不修改代码。

成功标准：
- 以当前机器、分支、运行日志、网络请求和真实 UI 为证据
- 区分表面现象、直接阻塞层和根因
- 给出可核查的证据链，包括文件、行号、日志或运行结果
- 说明影响范围和最小修复方向，但不要实施

不要覆盖或还原现有脏改动。
如果证据不足，指出最小缺失信息，不要猜测。
结论成立后停止，不为补充非必要背景继续搜索。

输出：结论、证据链、影响范围、建议下一步。
```

### 2. 根因明确的小修

```text
在 [仓库/模块] 中修复：[期望行为]。

成功标准：
- 只修改实现该行为所必需的文件
- 保留现有组件、设计 token、数据流和响应式行为
- 不做无关重构，不新增依赖，不覆盖用户已有改动
- 对改动行为运行最相关的测试、类型检查或最小 smoke test
- 如果无法验证，明确说明原因和下一项可执行检查

不要 commit、push 或创建 PR。

最终只需给出：
1. 改了什么
2. 验证结果
3. 剩余风险或未验证项
```

### 3. Review 本地变更

```text
Review 当前分支的本地变更，结合 [需求、Spec 或任务描述] 判断是否引入 Bug。

这是只读 review，不修改代码。

重点检查：
- 实际行为是否偏离需求或原有契约
- 状态流转、边界条件、错误处理和跨层数据流
- 是否覆盖或绕过用户已有逻辑
- 测试是否能证明变更行为，而不只是执行通过

只报告具体、可操作、由当前 diff 引入的问题。
每条 finding 给出优先级、文件位置、触发条件、影响和修复方向。
如果没有 finding，明确说没有发现，并列出仍未覆盖的验证风险。
```

### 4. QWork/Nano 卡片验收

```text
验收 [卡片名称/任务目录] 的 Nano 开发结果。

以当前实际链路为准：
- Nano 配置和 MCP 注册
- 生成目录及产物
- build/preview 输出
- 真实 QWork/千问 UI
- DevTools 日志和网络请求

成功标准：
- Step 1–4 的状态和产物互相一致
- 卡片能在真实运行表面正常渲染和交互
- 区分代码问题、生成链路问题、缓存问题和宿主能力问题
- 给出每项结论对应的直接证据

当前只做验收，不修改代码。
如果某一步无法验证，指出阻塞条件和最小下一步。
```

### 5. Trellis 持久任务规划

```text
这是一个需要跨会话保留上下文的任务：[目标]。

如果项目已有 `.trellis/workflow.md`，使用现有 Trellis 生命周期管理任务；
如果没有，不要主动初始化。

当前阶段只做规划，不实现代码。

成功标准：
- 明确用户可见结果、范围和非目标
- 找出会改变实现方向的关键问题
- 写清涉及的文件、数据流、状态变化和失败行为
- 定义验收证据和验证命令
- 方案稳定后进行一次实现前压力 review
- 一个阶段只保留一个 workflow owner

输出可执行计划、开放问题和进入实现阶段的条件。
```

### 6. 技术调研与方案选择

```text
调研：[问题或候选方案]，用于支持 [具体决策]。

优先使用当前、可信的一手资料；时效性内容必须实时检索。
不要把搜索摘要或模型记忆当作已验证事实。

成功标准：
- 按 [功能适配、成熟度、维护成本、性能、迁移风险] 比较
- 区分来源直接支持的事实和推断
- 对冲突信息明确标注
- 给出有排序的推荐，而不是只罗列候选项
- 最终落到我在 [仓库/工作流] 中的具体使用方式和试用步骤

输出：结论、对比表、推荐顺序、风险、最小试用方案，并附来源。
```

### 7. 日报生成

```text
根据今天的 Git 提交、当前分支变更和已完成任务，生成我的日报。

只写有直接证据支持的内容，不根据文件名夸大业务成果。
把确认完成、仍在进行、风险阻塞分开。

按主题组织，而不是逐条复制 commit：
- 今日进展
- 问题与处理
- 明日计划
- 风险与协作事项

语言简洁、面向团队同步。
写入 `~/work-pro/daily-report/daily/`，生成后告诉我文件路径和证据范围。
```

## Hooks 结合方案

### 结论

推荐采用“全局 rules + skills + 可选短前缀 hook”的三层结构，不把完整 Prompt 注入 `UserPromptSubmit`。

| 层级 | 职责 | 内容规模 |
| --- | --- | --- |
| 全局 rules | 语言、证据、授权、路由、验证和输出偏好 | 稳定且精简 |
| Skills | 诊断、实现、review、Nano、Trellis、调研、日报的完整工作流 | 按需加载 |
| 可选 hook | 将显式短前缀映射到 skill/工作模式 | 每次命中只注入一条短提示 |

官方 Codex hooks 文档说明：所有匹配 hook 都会运行；`UserPromptSubmit` 当前不支持 matcher；命令 stdout 会作为额外 developer context 注入。因此，在这里输出完整模板会造成每轮上下文膨胀，也会叠加现有 hooks 的延迟和行为。

参考：

- [Codex Hooks](https://learn.chatgpt.com/docs/hooks)
- [GPT-5.6 Prompting Guidance](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)

### 当前本机约束

- 全局 `UserPromptSubmit` 已运行 `guard-prompt.sh`，用于安全检测并刻意保持 stdout 静默。
- qianwen、nexview-devtools、agent-space、daily-report 等项目已有 `UserPromptSubmit`，用于注入 Trellis workflow state。
- 多个 matching hooks 会并行启动，新增 hook 不能阻止其他 hook 启动。
- 修改 hook 定义后需要重新 review/trust 对应 hash。

因此，不建议：

- 把路由逻辑合并进安全职责明确的 `guard-prompt.sh`；
- 每轮注入七套完整 Prompt；
- 使用宽泛关键词猜测用户意图；
- 在 hook 中访问网络、读取大文件或调用模型；
- 依赖 `UserPromptSubmit.matcher` 过滤场景。

### 推荐的可选 Hook 设计

如后续短 Prompt 的 skill 路由仍不稳定，再增加独立的 `prompt-router` hook：

1. 读取 `UserPromptSubmit` 的 `prompt` 和 `cwd`。
2. 只识别显式前缀，不做语义分类，例如 `分析根因：`、`最小修复：`、`验收 Nano：`。
3. 未命中时 stdout 为空并立即退出。
4. 命中时只输出不超过约 240 个汉字的 `additionalContext`，说明目标 skill、授权层和完成标准摘要。
5. 保留用户原始 Prompt，不替换、不重写用户提供的具体值。
6. 本地纯计算、fail-open、无网络、无日志正文读取，目标耗时低于 50 ms，硬超时不超过 1 秒。
7. 路由 hook 与安全 hook 分离，单独版本化、安装和 trust。

默认映射保持一对一：

| 前缀 | 默认路由 |
| --- | --- |
| `分析根因：` | `diagnosing-bugs`，只读 |
| `最小修复：` | Inline 小修 |
| `review 本地变更：` | `code-review`，只读 |
| `验收 Nano：` | `qwork-nano-runbook`，只读验收 |
| `规划 Trellis：` | 已有 `.trellis/workflow.md` 时用 `trellis-brainstorm`；否则 Inline 规划且不初始化 |
| `调研选型：` | `tech-solution-radar` |
| `生成日报：` | `project-daily-summary` |

短前缀只定义默认路径。Trellis 路由只做 `cwd` 向上查找 `.trellis/workflow.md` 的本地存在性检查，不创建目录或任务。用户在原始 Prompt 中明确点名其他 skill 或增加不同授权时，显式请求优先，hook 不覆盖用户值。

示例路由结果，不是最终实现：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Route: diagnosing-bugs. This turn is read-only. Establish the runtime evidence chain, identify the blocking layer and root cause, then report the smallest next step."
  }
}
```

### 分阶段落地建议

1. **先观察，无 hook**：使用本文快速入口和现有 skill descriptions，记录实际误路由案例。
2. **只补 measured gaps**：如果某个短前缀反复误路由，先调整对应 skill description 或增加一个轻量 router skill。
3. **最后考虑 hook**：只有需要跨项目、确定性前缀路由且 skills 仍不能稳定覆盖时，才 draft `prompt-router`。
4. **安装前验收**：验证未命中零输出、命中内容长度、耗时、fail-open、与 Trellis/ponytail/guard hooks 的叠加结果。

### Hook 方案验收标准

- 七类短前缀均路由到预期 workflow。
- 普通自然语言 prompt 不产生额外上下文。
- 不重复全局 rules 或完整 Prompt。
- 不改变安全 hook 和项目 Trellis hook 的行为。
- 单次执行延迟稳定在预算内。
- hook 错误不会阻断用户请求。
- 通过 `codex debug prompt-input` 验证最终注入内容短且无冲突。
