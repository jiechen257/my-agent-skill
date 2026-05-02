---
name: colawd-ui-style
description: "UI design system for recreating the colawd-style workspace shown in the user's screenshots: black terminal shell, pale yellow grid canvas, oversized brutalist headings, thick black borders, hard offset shadows, neon status colors, dense dashboard cards, sidebar navigation, capture/library/create/publish workflows, and bilingual Chinese-English productivity UI. Use when designing, implementing, reviewing, or refactoring frontend screens that should match this specific visual style."
---

# Colawd UI Style

Use this skill to turn a product UI into the colawd-style local workspace seen in the screenshots. Treat the screenshots as the source of truth: a dense founder-operator dashboard with a black terminal frame, pale yellow grid work surface, thick black strokes, hard shadows, saturated status colors, and compact Chinese-English labels.

## Design Direction

Build a local-first command center with the attitude of a terminal app and the clarity of a production dashboard.

- Use a fixed black application shell with macOS traffic-light dots and a terminal path line.
- Use a dark left sidebar for project context, navigation, browser profiles, and counters.
- Use a pale yellow grid canvas for the main working area.
- Use oversized black display headings with a small pink square period.
- Use thick black outlines and hard offset shadows on interactive objects.
- Use high-saturation tiles to encode workflow status: lime, pink, sky, orange, lavender, cream, white, and black.
- Use dense, useful modules: KPI tiles, queues, inbox cards, research jobs, library cards, editor panels, charts, progress bars, and channel breakdowns.
- Use bilingual UI copy naturally: Chinese for workflow nouns, English for product/source labels, monospace for operational metadata.

## Visual Tokens

Use these values as defaults and tune only for local contrast or framework constraints.

```css
:root {
  --colawd-black: #080808;
  --colawd-ink: #101010;
  --colawd-cream: #fff9bf;
  --colawd-cream-2: #fff6a8;
  --colawd-paper: #fffefa;
  --colawd-grid: rgba(16, 16, 16, 0.07);
  --colawd-lime: #a5f12b;
  --colawd-pink: #ff6680;
  --colawd-orange: #ff9138;
  --colawd-sky: #75c9ee;
  --colawd-lavender: #b9a7f4;
  --colawd-muted: #77756e;
  --colawd-border: 4px solid var(--colawd-black);
  --colawd-radius-sm: 6px;
  --colawd-radius-md: 10px;
  --colawd-radius-lg: 16px;
  --colawd-shadow: 7px 7px 0 var(--colawd-black);
  --colawd-shadow-pink: 7px 7px 0 var(--colawd-pink);
}
```

Typography:

- Display: `Archivo Black`, `Arial Black`, `Impact`, system sans.
- UI/body: `Inter`, `Noto Sans SC`, `PingFang SC`, `Helvetica Neue`, sans-serif.
- Mono metadata: `JetBrains Mono`, `SFMono-Regular`, `Menlo`, monospace.
- H1: 52-72px, 0 letter spacing, 0.9-1.0 line height, weight 900.
- Section labels: uppercase mono, 12-14px, 0.14-0.22em letter spacing.
- Body text: 16-20px, weight 600-800 for important lines.

## Layout Recipe

Use this structure for full application screens:

1. App frame: black outer background with a 56-64px terminal top bar.
2. Sidebar: 320-370px fixed black rail with logo, version, project switcher, nav items, profile list, and dotted separators.
3. Main region: pale yellow workspace starting to the right of the sidebar.
4. Page header: 110-130px high, title left, subtitle/breadcrumb beside it, search/new/profile controls right.
5. Canvas: pale yellow grid background, 28-40px padding, 18-24px gaps.
6. Content grid: asymmetric dashboard columns, usually 3 columns or a wide center with narrow side panels.

CSS grid background:

```css
.colawd-canvas {
  background-color: var(--colawd-cream);
  background-image:
    linear-gradient(var(--colawd-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--colawd-grid) 1px, transparent 1px);
  background-size: 32px 32px;
}
```

## Component Patterns

### Sidebar

Use black as the full sidebar surface. Keep labels cream/white, secondary text muted gray, counters pink, and active navigation lime.

- Logo block: pink square icon, `colawd.` wordmark, small `v1.4 · local`.
- Project selector: cream fill, black border, pink hard shadow, compact project name.
- Nav item: icon tile at left, bold label, small Chinese subtitle, right-side count badge.
- Active nav item: lime fill, cream icon tile, pink hard shadow, white inner outline.
- Browser profiles: small colored dots with channel labels, dashed divider, dashed add button.

### Header Controls

Make search and primary actions feel like hardware controls.

- Search input: white fill, black border, hard black shadow, `⌘K search everything...` placeholder.
- New button: lime fill, black border, hard shadow, `+ New`.
- Avatar: pink circle, thick black border, single letter.
- Status: top-right lime dot plus `local · synced` mono text.

### Cards And Panels

Use thick cards only for functional modules.

- Panel shell: black header strip, rounded top corners, white or cream content body, black border, hard shadow.
- Dashboard hero: black card with cream text, split by a vertical cream rule, large `day 47.` type.
- KPI tiles: saturated fill, black border, hard shadow, large numeric value, small label.
- List rows: white cards with black border, category stripe or colored badge, right arrow or status chip.
- Library cards: white large cards, category badge top-left, source top-right, quote/body content, tags bottom-left, usage count bottom-right.
- Editor: white or cream writing surface inside a black-framed panel; include character count and action buttons below.
- Research cards: colored job blocks with black border, progress bar, small metadata row.

### Buttons And Chips

Use compact button primitives with clear hierarchy.

- Primary: pink or lime fill, black border, hard shadow, bold label.
- Secondary: white or cream fill, black border, hard shadow.
- Small chip: 2px black border, 4-6px radius, mono uppercase label.
- Category chip colors map to content types: pink insight, lime hook/gold sentence, sky case/tweet, orange pain/diff, lavender talk/keyword, cream template.
- Pressed state: translate by the shadow offset and reduce shadow to 2px.
- Hover state: lift by 1-2px and keep the hard shadow.
- Focus state: add a clear pink or lime outline outside the black border.

### Data Visualization

Use chart elements that feel hand-built and operational.

- Bars: black for history, lime/pink for highlighted recent periods.
- Axes: black 2-3px rules, minimal labels, mono dates.
- Progress: black outer stroke, cream/white track, pink/lime/orange fill.
- Channel bars: colored square legend, outlined horizontal bars, numeric deltas at right.
- Tabs: rectangular chips attached to a panel header or chart top edge.

## Copy Rules

Write UI copy like a compact operator console.

- Page titles: `Dashboard.`, `Capture.`, `Library.`, `Create.`, `Publish.`
- Subtitle pattern: `总览 · 健康度 · 数据一览`, `采集 · 监听 · 调研`, `内容簇 · 多平台适配`.
- Status language: `queued`, `review`, `draft`, `LIVE`, `WATCH`, `PAUSED`, `2 running`.
- Action labels: `查看队列`, `编辑`, `跳过今天`, `导入剪藏`, `AI 整理`, `推送到 Publish`.
- Metadata uses mono separators: `local · synced`, `today · May 2 · Fri`, `MCP · 8m left`.
- Keep labels short enough for dense screens; use one-line labels in nav, cards, and buttons.

## Implementation Workflow

1. Identify the screen type: dashboard, capture inbox, library grid, content editor, or publish queue.
2. Create or reuse design tokens for color, border, radius, shadow, grid, typography, and spacing.
3. Build the shell first: top terminal bar, sidebar, page header, canvas.
4. Compose the main screen from functional modules, using thick cards only around real work areas.
5. Encode status through color and labels, then verify the screen still works in grayscale via shape, position, and text.
6. Check responsive behavior: keep the sidebar fixed on desktop; collapse to a bottom or drawer navigation on narrow screens while preserving the pale grid canvas and strong card language.
7. Verify the page with a real screenshot when possible. Compare against the four reference screens for density, contrast, stroke weight, and color balance.

## Quality Checklist

Before finishing a colawd-style screen, confirm:

- The first viewport clearly shows the black shell, left sidebar, pale grid canvas, and oversized page title.
- Borders are visually heavy, usually 3-5px, and shadows are hard offsets.
- Colors are saturated accents on top of black, cream, white, and pale yellow.
- Navigation state is obvious through lime fill, pink shadow, badge counts, and icon tiles.
- Cards contain real controls, metrics, queues, content, or charts.
- The UI has no soft gradients, glassmorphism, blurred shadows, decorative blobs, or stock-photo ambience.
- Typography is bold, compact, and readable in Chinese-English mixed copy.
- Dense modules align to a visible grid and maintain consistent gaps.
- Interactive states preserve the hard physical-button feeling.
- Mobile layouts preserve the same identity through color, border, shadow, and card hierarchy.
