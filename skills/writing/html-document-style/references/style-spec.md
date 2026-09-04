# All in Agent HTML 视觉规范

来源：`https://61e92d00-8080.boz.alibaba-inc.com/artifacts/all-in-agent-share-v2.html`。本 skill 中的 `assets/reference.html` 是在 2026-09-04 下载的自包含源文件；网页内容可变化，生成时以本地副本和本规范为准。

## 页面骨架

```text
body (#eef1f6)
└── .page-shell
    ├── .toc（新增：桌面端左侧 sticky 目录）
    └── main.canvas（白色文档纸张）
        ├── .hd（居中标题、英文眉题、关键词）
        ├── section.sec（一级章节）
        │   ├── .sec__hd（编号、标题、描述）
        │   └── .sub__hd / .grid / .evo / .mat / .cross / .tl / .ch / .goal / .stack
        └── .end（总结）
```

推荐桌面壳层：`page-shell` 最大宽度约 `1510px`，两列为约 `208px` 目录栏和 `minmax(0, 1240px)` 内容栏，中间约 `18px` 间距。原始画布的 `max-width` 为 `1240px`；加入目录后不要压缩内容到难以阅读，而是让整个壳层变宽。

## 颜色与基础排版

```css
:root {
  --canvas: #ffffff;
  --page: #eef1f6;
  --text: #1a1a1a;
  --sub: #5a5a5a;
  --line: #e2e6ee;
  --line-2: #d0d6e0;
  --purple: #7c3aed;
  --purple-bg: #f5f3ff;
  --purple-bd: #c4b5fd;
  --blue: #2563eb;
  --blue-bg: #eff6ff;
  --blue-bd: #93c5fd;
  --cyan: #0891b2;
  --cyan-bg: #ecfeff;
  --cyan-bd: #67e8f9;
  --green: #059669;
  --green-bg: #ecfdf5;
  --green-bd: #6ee7b7;
  --amber: #d97706;
  --amber-bg: #fffbeb;
  --amber-bd: #fcd34d;
  --slate: #334155;
  --slate-bg: #f1f5f9;
  --slate-bd: #94a3b8;
  --red: #dc2626;
  --red-bg: #fef2f2;
  --red-bd: #fca5a5;
}
```

- 字体顺序：`"PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", -apple-system, sans-serif`。
- `body` 使用抗锯齿；原始外边距为顶部 `26px`、左右 `16px`、底部 `48px`。
- `.canvas`：白底、`1px` `--line` 边框、`14px` 圆角、`0 8px 32px rgba(15,23,42,.08)` 阴影、约 `34px 40px 38px` 内边距。
- 标题：约 `29px`、`800`、`1px` 字距，`#1e3a8a → #7c3aed` 的水平渐变文字。
- 正文：约 `12px–13.5px`，正文颜色 `#374151` 或 `#414b5c`，行高 `1.65–1.85`。
- 一级标题：约 `21px`、`800`；章节编号为白字 slate 背景、`5px` 圆角。

## 组件尺寸和表现

| 组件 | 参考表现 |
| --- | --- |
| `.sec` | 一级章节顶部约 `26px` 间距 |
| `.sec__hd` | 横向排列，编号/标题/描述间距约 `10px` |
| `.sub__hd` | 左侧 `4px × 17px` 蓝色竖条，约 `17px` 字号 |
| `.grid` | `10px` gap，支持 `g2/g3/g4` |
| `.card` | `1px` 灰边框、`10px` 圆角、`12px 14px` 内边距、极浅纵向渐变 |
| `.num` | `18px` 紫色浅底圆形编号 |
| `.allin` | 紫色边框，左侧 `4px` 紫色实线，浅紫到白色渐变 |
| `table` | 合并边框；单元格 `7px 10px`；表头 slate 浅底、紧凑字重 |
| `.plist` | 无默认 marker；自定义紫色圆形序号，左内边距约 `26px` |
| `.ch` | 白底、红色左侧 `4px` 强调线、`9px` 圆角 |
| `.goal` | 三列目标卡；大号数字约 `24px`，分别 blue/green/purple |
| `.stack` | 六层纵向排列，左侧标签区约 `150px`，右侧 chip 流式换行 |
| `.end` | 紫色顶部 `3px` 线、浅紫渐变、`11px` 圆角 |

## 左侧目录扩展

目录不是原始页面的一部分，是本 skill 的统一新增层。推荐 CSS：

```css
.page-shell {
  max-width: 1510px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 208px minmax(0, 1240px);
  gap: 18px;
  align-items: start;
}
.toc {
  position: sticky;
  top: 24px;
  max-height: calc(100vh - 48px);
  overflow: auto;
  padding: 12px 10px;
  background: rgba(255,255,255,.9);
  border: 1px solid var(--line);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(15,23,42,.07);
}
.toc__title {
  padding: 2px 8px 10px;
  color: var(--slate);
  font-size: 13px;
  font-weight: 800;
}
.toc__title span {
  margin-left: 5px;
  color: var(--sub);
  font-size: 9px;
  letter-spacing: .16em;
}
.toc nav { display: grid; gap: 3px; }
.toc a {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 6px;
  align-items: center;
  padding: 7px 8px;
  color: #475569;
  border-radius: 7px;
  font-size: 12px;
  line-height: 1.35;
  text-decoration: none;
}
.toc a:hover, .toc a[aria-current="location"] {
  color: #4c1d95;
  background: var(--purple-bg);
}
.toc__no {
  display: inline-flex;
  width: 20px;
  height: 20px;
  align-items: center;
  justify-content: center;
  color: var(--purple);
  background: #ede9fe;
  border-radius: 50%;
  font-size: 10px;
  font-weight: 800;
}
.toc a:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}
main section[id] { scroll-margin-top: 28px; }
@media (max-width: 1024px) {
  .page-shell { display: block; }
  .toc {
    top: 8px;
    z-index: 5;
    max-height: none;
    margin-bottom: 12px;
    padding: 8px;
  }
  .toc nav { display: flex; overflow-x: auto; }
  .toc a { flex: 0 0 auto; }
}
```

目录脚本只需要观察一级 `section[id]`：进入视口时给对应链接加 `aria-current="location"`，滚动到顶部时保留第一个 active。`scroll-behavior: smooth` 只能在 `prefers-reduced-motion: no-preference` 下启用。

## 深色架构图

原页面的 `#osmap` 是独立的深色关系图，不要把它的颜色覆盖到整页。关键特征：

- `#070b16` 基底，`#1b2440` 边框，约 `12px` 圆角；叠加绿色、青色、紫色的径向微光。
- 固定 `1000 × 742` 的内部 stage，使用 `transform: scale(...)` 按容器宽度缩放，最大缩放约 `0.68`。
- 中心为约 `212px` 的绿色发光圆形；内圈/外圈为低透明度椭圆。
- 工具、Skill、Surface 节点为紧凑半透明卡片；专家套件使用粉色胶囊；开放平台使用荧光黄绿色环线和箭头。
- SVG 线、箭头、标签与节点共用同一几何坐标系，缩放时整体缩放，不单独拉伸文本。

如果文档没有架构关系需要表达，使用普通卡片、表格或时间线，不要为了装饰强行加入深色图。

## 响应式与打印

- `1024px` 以下：画布内边距收窄，`g3/g4/goal` 至少降为两列；成熟度和分层布局转单列。
- `640px` 以下：标题约 `21px`；所有网格和目标卡单列；时间线纵向排列；All in Agent 允许换行。
- 打印：`body` 白底零外边距，画布去阴影/边框并放宽；保留背景色（`print-color-adjust: exact`）；章节尽量 `break-inside: avoid`。目录在打印时可隐藏或保留为普通目录，但不能遮挡正文。
