---
name: architecture-diagram
description: Create professional, light-themed architecture diagrams by default as standalone SVG deliverables. Use when the user asks for system architecture diagrams, infrastructure diagrams, cloud architecture visualizations, security diagrams, network topology diagrams, or any technical diagram showing system components and their relationships. Default output language is Chinese, with English technical terms preserved when clearer. Support dark mode when the user asks for it.
license: MIT
metadata:
  version: "1.0"
  author: Cocoon AI (hello@cocoon-ai.com)
---

# Architecture Diagram Skill

Create professional technical architecture diagrams as standalone SVG files.

## Design System

### Theme Modes

Default to **light mode**. Use **dark mode** only when the prompt explicitly asks for a dark theme, dark background, slate theme, or presentation mode.

### Output Language

**默认使用中文**：标题、标签、图例、副标题、注释、页脚文案默认都使用中文。

- Prefer concise Chinese phrasing for structural concepts such as "编译阶段", "运行时", "响应式更新"
- Keep well-known technical terms in English when they are clearer or more standard, such as `VNode`, `render`, `patch`, `effect`, `scheduler`, `setup()`
- Avoid mixed-language duplication such as `响应式 Reactive`; choose one phrase that reads naturally
- If the user explicitly asks for English, switch the entire diagram copy to English

**Light mode defaults:**

- Page background: `#f8fafc`
- Surface background: `#ffffff`
- Surface border: `#cbd5e1`
- Primary text: `#0f172a`
- Secondary text: `#475569`
- Subtle text: `#64748b`
- Grid stroke: `#cbd5e1`
- Arrowhead / neutral connector: `#475569`
- Opaque mask behind transparent component fills: `#ffffff`

**Dark mode overrides:**

- Page background: `#020617`
- Surface background: `rgba(15, 23, 42, 0.5)`
- Surface border: `#1e293b`
- Primary text: `#ffffff`
- Secondary text: `#94a3b8`
- Subtle text: `#475569`
- Grid stroke: `#1e293b`
- Arrowhead / neutral connector: `#64748b`
- Opaque mask behind transparent component fills: `#0f172a`

### Color Palette

Use these semantic colors for component types. In light mode, prefer pale fills with darker strokes for contrast. In dark mode, use the original deeper translucent fills.

| Component Type | Light Fill | Light Stroke | Dark Fill | Dark Stroke |
|---------------|------------|--------------|-----------|-------------|
| Frontend | `rgba(34, 211, 238, 0.12)` | `#0891b2` | `rgba(8, 51, 68, 0.4)` | `#22d3ee` |
| Backend | `rgba(52, 211, 153, 0.12)` | `#059669` | `rgba(6, 78, 59, 0.4)` | `#34d399` |
| Database | `rgba(167, 139, 250, 0.12)` | `#7c3aed` | `rgba(76, 29, 149, 0.4)` | `#a78bfa` |
| AWS/Cloud | `rgba(251, 191, 36, 0.18)` | `#d97706` | `rgba(120, 53, 15, 0.3)` | `#fbbf24` |
| Security | `rgba(251, 113, 133, 0.12)` | `#e11d48` | `rgba(136, 19, 55, 0.4)` | `#fb7185` |
| Message Bus | `rgba(251, 146, 60, 0.14)` | `#ea580c` | `rgba(251, 146, 60, 0.3)` | `#fb923c` |
| External/Generic | `rgba(148, 163, 184, 0.16)` | `#64748b` | `rgba(30, 41, 59, 0.5)` | `#94a3b8` |

### Typography

Use a renderer-safe font stack directly in the SVG so the asset stays self-contained:
```svg
<text style="font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;">
```

Font sizes: 12px for component names, 9px for sublabels, 8px for annotations, 7px for tiny labels.

### Visual Elements

**Background:** In light mode use `#f8fafc` with a subtle grid. In dark mode use `#020617` with the same pattern.
```svg
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#cbd5e1" stroke-width="0.5"/>
</pattern>
```

**Component boxes:** Rounded rectangles (`rx="6"`) with 1.5px stroke, semi-transparent fills.

**Security groups:** Dashed stroke (`stroke-dasharray="4,4"`), transparent fill, rose color.

**Region boundaries:** Larger dashed stroke (`stroke-dasharray="8,4"`), amber color, `rx="12"`.

**Arrows:** Use SVG marker for arrowheads:
```svg
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#475569" />
</marker>
```

**Arrow z-order:** Draw connection arrows early in the SVG (after the background grid) so they render behind component boxes. SVG elements are painted in document order, so arrows drawn first will appear behind shapes drawn later.

### Edge Routing Rules

**CRITICAL:** Default to anchored orthogonal routing. Every meaningful edge should have a clear source port, a clear target port, a reserved lane for labels, and a path that stays off unrelated nodes. 在中文语境下，把这些固定挂点称为**端口锚点**，把 `H` / `V` 为主的 routed path 称为**正交走线**。

- Define ports before drawing the edge: `left`, `right`, `top`, `bottom` midpoint anchors for every node
- Same-row flows should usually connect `right -> left`
- Cross-row flows should usually connect `bottom -> top`
- Draw edges as orthogonal paths with `H` / `V` segments: `M x y H ... V ... H ...`
- Reserve routing corridors between rows and columns; keep at least 24px between a corridor and the nearest node border
- Long feedback loops should use outer perimeter corridors instead of grazing component boxes
- Dependency edges such as `track()` / `trigger()` must terminate on the semantically correct node, not on the nearest empty space
- Keep parallel edges on separate lanes with at least 12px of lane separation
- Keep arrow endpoints 6-12px away from rounded corners; prefer side midpoints over corners

**Arrow labels need their own lane.** Do not place labels directly on top of a node title or subtitle.

- Reserve a dedicated label band above or below the routed segment
- Put every label on an opaque background chip so the text stays legible over the grid and crossings
- Keep at least 10px between the label chip and the nearest node text
- For dense rows, move the label into a higher lane or widen the gap between nodes

**Preferred edge pattern:**
```svg
<path d="M 250 200 H 330" fill="none" stroke="#d97706" stroke-width="1.5" marker-end="url(#arrowhead)"/>
<rect x="276" y="150" width="28" height="16" rx="4" fill="#ffffff" stroke="#e2e8f0" stroke-width="0.8"/>
<text x="290" y="161" fill="#475569" font-size="9" text-anchor="middle">编译</text>
```

**Preferred cross-row pattern:**
```svg
<path d="M 760 230 V 270 H 240 V 330" fill="none" stroke="#d97706" stroke-width="1.5" marker-end="url(#arrowhead)"/>
<rect x="766" y="246" width="34" height="16" rx="4" fill="#ffffff" stroke="#e2e8f0" stroke-width="0.8"/>
<text x="783" y="257" fill="#475569" font-size="9" text-anchor="middle">加载</text>
```

### Anti-Truncation Rules

**CRITICAL:** Deliverables must show the full diagram without requiring horizontal scrolling or thumbnail cropping.

- Do **not** rely on `overflow-x: auto`, viewport scrolling, or oversized `min-width` values to reveal core content
- Keep every essential node, arrow, label, legend, and footer inside the SVG `viewBox`
- Reserve at least 24px of right and bottom padding inside the `viewBox`
- If the diagram is dense, increase the `viewBox` size or split the content into two diagrams instead of letting content run off the edge
- Keep the standalone `.svg` as the canonical deliverable and source of truth
- Use `rsvg-convert` only for local verification or when the user explicitly asks for a bitmap export

**Masking arrows behind transparent fills:** Since component boxes use semi-transparent fills, arrows behind them will show through. To fully mask arrows, draw an opaque background rect at the same position before drawing the semi-transparent styled rect on top. Use `fill="#ffffff"` in light mode and `fill="#0f172a"` in dark mode:
```svg
<!-- Opaque background to mask arrows -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#ffffff"/>
<!-- Styled component on top -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="rgba(167, 139, 250, 0.12)" stroke="#7c3aed" stroke-width="1.5"/>
```

**Auth/security flows:** Dashed lines in rose color (`#fb7185`).

**Message buses / Event buses:** Small connector elements between services. In light mode use a pale orange fill with a darker stroke. In dark mode use the original higher-contrast orange:
```svg
<rect x="X" y="Y" width="120" height="20" rx="4" fill="rgba(251, 146, 60, 0.14)" stroke="#ea580c" stroke-width="1"/>
<text x="CENTER_X" y="Y+14" fill="#ea580c" font-size="7" text-anchor="middle">Kafka / RabbitMQ</text>
```

### Spacing Rules

**CRITICAL:** When stacking components vertically, ensure proper spacing to avoid overlaps:

- **Standard component height:** 60px for services, 80-120px for larger components
- **Minimum vertical gap between components:** 40px
- **Inline connectors (message buses):** Place IN the gap between components, not overlapping

**Example vertical layout:**
```
Component A: y=70,  height=60  → ends at y=130
Gap:         y=130 to y=170   → 40px gap, place bus at y=140 (20px tall)
Component B: y=170, height=60  → ends at y=230
```

**Wrong:** Placing a message bus at y=160 when Component B starts at y=170 (causes overlap)
**Right:** Placing a message bus at y=140, centered in the 40px gap (y=130 to y=170)

### Legend Placement

**CRITICAL:** Place legends OUTSIDE all boundary boxes (region boundaries, cluster boundaries, security groups).

- Calculate where all boundaries end (y position + height)
- Place legend at least 20px below the lowest boundary
- Expand SVG viewBox height if needed to accommodate

**Example:**
```
Kubernetes Cluster: y=30, height=460 → ends at y=490
Legend should start at: y=510 or below
SVG viewBox height: at least 560 to fit legend
```

**Wrong:** Legend at y=470 inside a cluster boundary that ends at y=490
**Right:** Legend at y=510, below the cluster boundary, with viewBox height extended

### SVG Structure

1. **Title row** - Title and subtitle inside the SVG canvas
2. **Main diagram area** - Boundaries, nodes, and routed edges
3. **Legend / notes** - Compact legend and any required notes inside the same SVG
4. **Footer metadata** - Optional minimal metadata line inside the `viewBox`

### Component Box Pattern

```svg
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL_COLOR" stroke="STROKE_COLOR" stroke-width="1.5"/>
<text x="CENTER_X" y="Y+20" fill="PRIMARY_TEXT" font-size="11" font-weight="600" text-anchor="middle">LABEL</text>
<text x="CENTER_X" y="Y+36" fill="SECONDARY_TEXT" font-size="9" text-anchor="middle">sublabel</text>
```

## Template

Copy and customize the SVG template:

- `assets/template.svg` for the export-safe image version

Key customization points:

1. Update the title and subtitle in the SVG file
2. Modify the SVG `viewBox` dimensions if needed
3. Add, remove, or reposition component boxes
4. Draw connection arrows between components with anchored orthogonal routing and label lanes
5. Keep legends and labels inside the `viewBox`
6. Update the legend and footer notes inside the SVG when needed

## Output

Always produce this deliverable by default:

1. A standalone `.svg` file

Output rules:

- Embedded `<style>` inside the SVG is allowed; no JavaScript required
- The `.svg` file must render correctly with `rsvg-convert`
- Do not generate `.html` files by default
- Do not generate `.png` files by default
- The default edge style is anchored orthogonal routing with opaque label chips
- Default to Chinese unless the user explicitly asks for English
- Default to light mode unless the user explicitly asks for dark mode
