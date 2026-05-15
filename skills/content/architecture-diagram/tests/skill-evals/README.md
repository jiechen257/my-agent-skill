# architecture-diagram skill — 端到端评测

补充现有 `tests/fixtures/` + `tests/regression.sh` 的**单元层 SVG 校验**，提供**端到端 prompt 评测**：用同一组 prompt 在重构前后跑一次，量化对比输出质量。

## 目录

```
tests/skill-evals/
├── cases/                    # 8 个 prompt-level case（覆盖 8 种图类型）
├── snapshot/before.md        # 重构前 SKILL.md 的冻结副本（参考）
├── out/
│   ├── before/               # 旧 skill 输出 SVG（已预填 3 张真实 baseline）
│   └── after/                # 新 skill 输出 SVG（待生成）
├── check.mjs                 # 结构性自动校验（spec block / palette / font-weight / edge id 等）
├── index.html                # 并排目检 + 1–5 分人工评分录入
├── report.csv                # check.mjs 输出（自动生成）
└── README.md
```

## 与现有测试的分工

| 测试 | 输入 | 关注 | 谁跑 |
|---|---|---|---|
| `tests/regression.sh` | 静态 fixture SVG | layout / 几何 / chip 归属 / safe inset | CI + 本地 |
| `tests/fixtures/*good*` & `*bad*` | 手写正反例 | validate-svg.sh 的覆盖率 | regression.sh |
| `tests/skill-evals/check.mjs` | 模型新生成的 SVG | spec block / palette / 字重 / data-edge-id 等 prompt 层面契约 | 改 SKILL.md 后手动跑 |
| `index.html` | 同 case 的 before/after | 视觉美感 / 信息密度 / 类型契合 | 人工目检 |

## 跑评测的步骤

### Step 1 — 冻结基线

`snapshot/before.md` 已是某次重构前的 SKILL.md 副本。如果你又改了 SKILL 但还没走评测，重置一次：
```bash
cp ../../SKILL.md snapshot/before.md
```

### Step 2 — 捕获 before

`out/before/` 已预填 3 张真实历史 baseline：
- `arch-qclaw-functional.svg`
- `flow-qclaw-user.svg`
- `matrix-shared-capability.svg`

剩余 5 个（dataflow / seq / state / timeline / usecase）需要在**重构 SKILL 之前**跑一遍，把产物 `cp` 到 `out/before/<id>.svg`。建议在 paseo agent 或独立 conductor workspace 里跑，避免会话上下文污染。

### Step 3 — 重构 SKILL

修改 `SKILL.md` / `references/*.md` / `templates/*.svg`。完成后：
```bash
bash ../regression.sh
```
确保单元层不破。

### Step 4 — 捕获 after

8 个 prompt 在新会话里逐个再跑一次，输出到 `out/after/<id>.svg`。

### Step 5 — 自动校验

```bash
node check.mjs            # before vs after
node check.mjs after      # 只校验 after
```
输出 `report.csv` 和摘要，例：
```
=== 评测摘要 ===
  before: 11/72 (15.3%)
  after:  60/72 (83.3%)
  delta: +49 项检查改善
```

### Step 6 — 人工目检

```bash
open index.html
```
为每个 case 给 1–5 分（visual_balance / information_density / type_appropriateness）+ 备注，导出剪贴板存到 `rubric.json`。

### Step 7 — 写最终报告

把自动 + 人工分数汇总到 `REPORT.md`：

```markdown
## 自动校验 delta

| 检查项 | before | after | delta |
|---|---|---|---|
| spec_block_present | 0/8 | 8/8 | +8 |
| ...

## 人工评分均分（1–5）

| 维度 | before | after |
|---|---|---|
| visual_balance | x.x | x.x |

## 净改善 / 回退条目
```

## check.mjs 检查项（17 种）

详见脚本顶部 `CHECKS` 对象。重点：
- `spec_block_present` / `spec_type_equals` — 新 skill 的契约
- `palette_subset` (warm-beige / cool-blue) — 调色板内聚
- `font_weight_in {400,600,700}` — 防止 740/760 被舍入
- `edge_ids_stable` — 每条 edge 必须 id + data-edge-id
- `decision_branches_labeled` / `edges_have_payload_labels` — 出边必须有 data-edge-label
- `legend_present_if_mixed_edges` — 同图混 edge 风格时必须给 legend

## 已知局限

- check.mjs 只做结构性检查，视觉美感走 `index.html` 人工目检
- before/after 严格隔离需要新会话——同一 Claude 进程跑过新 skill 后再跑旧 skill 会被污染。最严格的做法是每个 case 一个 paseo agent 或新 conductor workspace
- 旧 skill 不强制 `data-edge-label`，所以旧产物的 `decision_branches_labeled` 全 fail；这是预期的，重点看 delta
