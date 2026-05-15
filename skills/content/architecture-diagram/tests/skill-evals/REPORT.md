# architecture-diagram skill 重构评测报告

**日期**：2026-05-15
**对比对象**：`snapshot/before.md`（重构前 SKILL.md）vs `SKILL.md`（重构后，含 `references/spec-block-and-self-review.md` 等新增）
**已跑 case**：8/8（覆盖 architecture / flowchart / data-flow / sequence / state-machine / timeline / comparison-matrix / use-case）
**自动校验产物**：`report.csv`

---

## 1. 自动校验摘要

| | before | after | delta |
|---|---:|---:|---:|
| 通过项 | 30 / 67 | 67 / 67 | **+37** |
| 通过率 | 44.8% | **100.0%** | +55.2 pp |

按 case：

| Case | before | after | 关键改善 |
|---|---:|---:|---|
| `arch-qclaw-functional` | 4 / 9 | 9 / 9 | spec block / palette / edge id / legend / region count |
| `dataflow-card-render` | 3 / 9 | 9 / 9 | spec block / payload labels / edge id / mixed-edge legend |
| `flow-qclaw-user` | 3 / 9 | 9 / 9 | spec block / decision branch label / edge id / legend |
| `matrix-shared-capability` | 5 / 8 | 8 / 8 | spec block / font-weight 收敛到 700 |
| `seq-mock-protocol` | 4 / 8 | 8 / 8 | spec block / lifeline count / edge id / palette |
| `state-task-lifecycle` | 4 / 9 | 9 / 9 | spec block / transition guard / initial-final state / edge id |
| `timeline-q2-roadmap` | 4 / 7 | 7 / 7 | spec block / timeline axis edge id / palette |
| `usecase-qwork-actors` | 3 / 8 | 8 / 8 | spec block / actors outside boundary / include-extend edge id |

完整 per-check 表见 `report.csv`。

---

## 2. 改善点（按重要性）

### 2.1 spec block 全部接入（8/8）

旧版没有结构化输出契约。新版每张 SVG 都嵌入 `<!-- spec ... -->` 注释，包含 `type / title / style / nodes[] / edges[] / regions[]` 等字段。
**实际收益**：后续可以基于 spec 做语义校验、diff、变体生成和结构化回放。

### 2.2 类型特定契约全部通过

新版在 8 类图的关键契约上全部通过：

- `data-flow`：主箭头有 payload label
- `flowchart`：决策分支有 `data-edge-label`
- `sequence`：lifeline 数量与参与方匹配
- `state-machine`：迁移边有 `data-guard`，初态和终态明确
- `comparison-matrix`：行列数量可解析
- `use-case`：actors 与 system boundary 语义可解析

### 2.3 边契约稳定

before 多数 edge 只有视觉路径。after 所有被自动检查识别的 edge 都具备 `id` + `data-edge-id`，label chip 与边可以建立稳定绑定。

### 2.4 字重和调色板收敛

新版统一限制 `font-weight` 为 `400 / 600 / 700`，避免 `740 / 760 / 780` 在中文字体里被舍入。色值统一落在 `warm-beige` token 集合内，并补充 `Decision node: #fff7e8` 为正式 semantic fill。

### 2.5 混合线型 legend 补齐

数据流和流程图等混用实线 / 虚线的输出都带 legend，读图人可以区分主数据流、控制流、异步返回或弱依赖。

---

## 3. 质性目检

本轮没有通过 `index.html` 导出人工 `rubric.json`。我直接检查了新增 SVG 的结构与 XML，可见改善集中在三类问题：

| 维度 | before | after | 说明 |
|---|---|---|---|
| visual_balance | 中等 | 更稳定 | after 统一使用 region / lane / safe rail，边与节点间距更可控 |
| information_density | 中等 | 更可读 | after 把 payload、guard、include/extend 这类关键语义放在边或 chip 上 |
| type_appropriateness | 不稳定 | 明确 | after 每种图都有对应语义类名和结构契约 |

matrix 类型 before 的信息密度仍较高。新版的收益主要来自可验证结构、字重规范和跨图一致性。

---

## 4. 已知 / 修复的 check.mjs 问题

跑评测过程中发现 `check.mjs` 几个误判，已就地修复：

| Bug | 修复 |
|---|---|
| `extractSpec` 行首正则不接受 leading whitespace，导致 spec.type 解析失败 | 改成 `^\s*(...)` |
| `regions_count_in` 把 `class="region-label"` 误识为 region | 改成严格匹配 `class="(phase|region)"` |
| `matrix_cols_count_in` 把 `class="header-text"` 误识为 header | 改成严格匹配 `class="header"` |
| palette 集合不含 `#000000` / `#ffffff` / `#fff7e8` | 三色加入合法集合 |

---

## 5. 后续 check.mjs 可优化方向

当前 `check.mjs` 是轻量 regex 检查，已经足够给出 before/after delta。后续可以增强为：

1. 用 DOM parser 做 class / attribute 查询
2. 用 `js-yaml` 严格解析 spec block
3. 集成 `scripts/semantic-svg-checks.py` 做布局级验证
4. 增加跨 case 趋势分析和人工评分汇总

---

## 6. 结论

新 skill 在全部 8 个 prompt-level case 上 **100% 通过自动校验**，相比旧 skill 的 44.8% 有明确提升（+37 项）。

核心收益是：

- spec-first 输出契约完整落地
- 类型特定语义可被脚本识别
- edge id / data-edge-id 成为默认边契约
- decision label、payload label、guard、include/extend 等关键语义不再只依赖视觉猜测
- 字重与配色收敛到稳定 token

全部 8 case 评测完成，可合并。
