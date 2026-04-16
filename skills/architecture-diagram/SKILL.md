---
name: architecture-diagram
description: Use when the user asks for system architecture diagrams, technical flowcharts, framework principle diagrams, infrastructure diagrams, cloud architecture visualizations, security diagrams, network topology diagrams, or any technical diagram showing system components and their relationships as a standalone SVG deliverable.
license: MIT
metadata:
  version: "1.0"
  author: Cocoon AI (hello@cocoon-ai.com)
---

# Architecture Diagram Skill

Create professional technical architecture diagrams and flowcharts as standalone SVG files.

## Design System

### Theme Modes

Default to **light mode**. Use **dark mode** only when the prompt explicitly asks for a dark theme, dark background, slate theme, or presentation mode.

### Supported Style Profiles

Support two named style profiles.

- `default`: semantic phase colors, visible title pills, subpanels, grid background, and semantic connector colors. Use this for most architecture diagrams, framework flows, and system maps.
- `claude-official`: warm cream canvas, muted semantic fills, dark gray strokes, thicker borders, softer shadows, and neutral connector color. Use this when the prompt mentions Claude 官方风格, Anthropic, editorial card tone, or warm technical blog style.

Use `default` when the prompt does not specify a style.
Map vague requests such as “简洁技术风格” or “默认风格” to `default`.
Apply dark mode only to `default`.
Keep `claude-official` as a warm light deliverable.

### Output Language

**默认使用中文**：标题、标签、图例、副标题、注释、页脚文案默认都使用中文。

- Prefer concise Chinese phrasing for structural concepts such as "编译阶段", "运行时", "响应式更新"
- Keep well-known technical terms in English when they are clearer or more standard, such as `VNode`, `render`, `patch`, `effect`, `scheduler`, `setup()`
- Avoid mixed-language duplication such as `响应式 Reactive`; choose one phrase that reads naturally
- If the user explicitly asks for English, switch the entire diagram copy to English

### Default Style Tokens

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

### Claude Official Style Tokens

When style is `claude-official`, use these tokens:

- Page background: `#f8f6f3`
- Surface background: `#fffdf8`
- Surface border: `#d9d3ca`
- Primary text: `#1a1a1a`
- Secondary text: `#6a6a6a`
- Subtle text: `#5a5a5a`
- Grid stroke: `#ddd6cc`
- Arrowhead / neutral connector: `#5a5a5a`
- Opaque mask behind transparent component fills: `#fffdf8`
- Input / source fill: `#a8c5e6`
- Process / agent fill: `#9dd4c7`
- Infrastructure fill: `#f4e4c1`
- Storage / state fill: `#e8e6e3`
- Box stroke: `#4a4a4a`
- Preferred radius: `12`
- Preferred node stroke width: `2` to `2.5`

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

### Text Layout Rules

**CRITICAL:** Keep text on predictable rails. Node copy, annotation copy, and callout copy each need their own space budget.

- Node titles should stay on one line when possible; split into two lines only when the label clearly exceeds the box width
- Node sublabels should stay within two lines and use concise phrases instead of sentence-style prose
- Use `<tspan>` for every manual line break in notes or wrapped labels
- Keep at least 12px between any text block and the nearest border, edge corridor, or neighboring text block
- Reserve a dedicated **note rail** above the top phase band or below the legend for summary notes
- Keep summary note cards within 180-240px width and within two lines of body text
- Place node-specific callouts only when they add real explanatory value; anchor them with a leader line to the referenced node or edge
- Prefer moving excess explanation into the subtitle or footer note instead of adding a dense floating card in the core diagram area

### Shape Vocabulary

Use a small **shape vocabulary** so the diagram reads as a system map instead of a wall of identical rounded rectangles.

- **Phase band**: large rounded container with tinted fill for top-level sections
- **Title pill**: compact filled chip sitting on the band edge for section names
- **Standard node**: rounded rectangle for normal processing steps
- **Terminal node**: softer capsule or larger-radius box for inputs, bundles, DOM, external outputs
- **Subpanel**: dashed or softly tinted container for a local sub-flow such as compiler split, hook queue, or diff strategy
- **Decision node**: reserved for explicit binary branching in flowcharts; use it sparingly and only when the branch condition is central
- **Label chip**: tiny pill for edge labels, merge points, or lane markers
- **Note card**: compact callout in the note rail, never floating in the core routing corridor

Keep the number of shape types low, but make the semantic differences visible.

### Flowchart Layout Strategy

Use the same layout discipline for architecture diagrams and framework/process flowcharts.

- Build the page from 3 to 5 horizontal phase bands or vertical swimlanes before placing nodes
- Keep same-layer nodes aligned on a shared baseline
- Reserve one feedback corridor above or below each main row before drawing return edges
- Use terminal nodes for source and sink, standard nodes for process, subpanels for local detail, decision nodes for true branch points, and note cards for commentary
- Split long return edges onto top and bottom ports so forward flow and feedback flow can terminate cleanly on the same node
- Prefer one strong explanatory note card per major area over many floating annotations
- Keep edge labels on dedicated chips and keep local explanations inside subpanels when the section has dense detail

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
- Keep every arrowhead attached to a visible node port; corridor-only endpoints and whitespace endpoints are invalid
- Keep every edge label centered on a real rendered segment; labels floating in blank space are invalid
- Name the source and target mentally before drawing the path, for example `scheduleUpdateOnFiber.right -> renderRoot.left`
- When multiple edges connect to the same node, split them across **opposite sides** or distinct ports such as `top` and `bottom`; opposing flows should not terminate on the same border point
- Two unrelated edges must not share the same **corridor segment**; reserve separate lanes when the flows are semantically different

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

**Preferred note-callout pattern:**
```svg
<rect x="720" y="84" width="210" height="34" rx="6" fill="#fff7ed" stroke="#f59e0b" stroke-width="1"/>
<text x="732" y="97" fill="#9a3412" font-size="8">
  <tspan x="732" dy="0">说明放进上方 note rail，节点批注用 leader line。</tspan>
  <tspan x="732" dy="12">长句拆成两行，避免压到主流程。</tspan>
</text>
```

### Region Clarity Rules

**CRITICAL:** Top-level regions need stronger separation than a thin dashed outline.

- Use a tinted background fill strong enough to distinguish adjacent phase bands at a glance
- Use a **title pill** or colored label chip at the top-left of each region so the section name stays readable over the grid
- Keep at least 28px vertical space between neighboring phase bands
- Use thicker or more saturated borders for region boundaries than for node borders
- Keep note cards fully outside the band border unless the note belongs to a local subpanel inside that region
- Prefer one local **subpanel** over several floating notes when a section needs extra explanation

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
2. **Note rail** - Optional note cards above the top phase band or below the legend
3. **Main diagram area** - Phase bands, title pills, nodes, subpanels, and routed edges
4. **Footer metadata** - Optional minimal metadata line inside the `viewBox`

### Component Box Pattern

```svg
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL_COLOR" stroke="STROKE_COLOR" stroke-width="1.5"/>
<text x="CENTER_X" y="Y+20" fill="PRIMARY_TEXT" font-size="11" font-weight="600" text-anchor="middle">LABEL</text>
<text x="CENTER_X" y="Y+36" fill="SECONDARY_TEXT" font-size="9" text-anchor="middle">sublabel</text>
```

## Template

Copy and customize the SVG template:

- `assets/template.svg` for the `default` style
- `assets/template-claude.svg` for the `claude-official` style

Key customization points:

1. Update the title and subtitle in the SVG file
2. Modify the SVG `viewBox` dimensions if needed
3. Add, remove, or reposition phase bands, title pills, nodes, and subpanels
4. Draw connection arrows between components with anchored orthogonal routing and label lanes
5. Split competing edges across opposite sides or separate corridors
6. Keep note cards in the note rail and keep node callouts anchored with leader lines
7. Keep legends, labels, and footer notes inside the `viewBox`

## Output

Always produce this deliverable by default:

1. A standalone `.svg` file

Output rules:

- Embedded `<style>` inside the SVG is allowed; no JavaScript required
- The `.svg` file must render correctly with `rsvg-convert`
- Do not generate `.html` files by default
- Do not generate `.png` files by default
- Support `default` and `claude-official` as the two named style profiles
- Use `default` when the style is unspecified
- The default edge style is anchored orthogonal routing with opaque label chips
- Every arrow must terminate on a visible node port
- Competing in/out flows should use opposite sides of the node or separate named ports
- Distinct flows should not overlap on the same corridor segment
- Regions should use tinted phase bands with title pills
- Use at least one additional shape type such as subpanel or terminal node when the diagram has 8 or more nodes
- Summary notes belong in the note rail, not in the core routing corridor
- Default to Chinese unless the user explicitly asks for English
- Default to light mode unless the user explicitly asks for dark mode
