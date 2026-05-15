# Spec Block and Self-Review

Render only after a structured spec is settled, then self-review before delivering.

## Spec Block

Before drawing any path, decide the structure as a YAML-shaped spec, then embed it as the **first child** of the SVG element using an HTML comment so downstream tooling can parse it:

```svg
<svg ...>
  <!-- spec
  type: flowchart
  title: QClaw 用户使用流程图
  style: claude-official
  direction: top-to-bottom
  regions:
    - id: r1
      label: 入口与任务归一
  nodes:
    - id: n1
      label: 用户发起请求
      shape: terminal
      region: r1
  edges:
    - id: e1
      from: n1
      to: n2
      label: ""
      style: solid
  notes: []
  -->
  ...
</svg>
```

Required fields: `type`, `title`, `style`, `nodes[]`, `edges[]`. Optional: `regions[]`, `notes[]`, `direction`.

Keep the spec compact — names and ids only, no commentary. The spec is the contract; the SVG is its render. If the SVG output diverges from the spec, fix the SVG, not the spec.

## Clarification Protocol

Before drawing, ask one short question only when **at least one** of these is unset and cannot be inferred from the prompt:

- 受众（工程师 / 产品 / 高管）→ decides node detail depth
- 抽象层级（overview / detailed）→ decides node count cap
- 方向（top-to-bottom / left-to-right）
- 是否需要拆图 → mixed "architecture + flow + sequence" requests almost always want two diagrams instead of one

If the prompt already pins these, skip the question and emit the spec.

## Anti-patterns

- Non-standard `font-weight` values (`740`/`760`/`780`) that get rounded to the nearest 100
- Hand-breaking CJK paragraphs across multiple `<text>` lines instead of using `<foreignObject>`
- Decision diamonds with multiple outgoing edges but no `data-edge-label` per branch
- Decision nodes with more than 3 outgoing branches; split or insert a grouping bus
- Mixing palettes inside one diagram
- Mixing `edge` and `edge-soft` styles without a legend
- Multi-branch convergence that lets edges cross through unrelated regions
- A single diagram trying to express architecture + flow + sequence + state at once — split it
- Arrowheads landing in node centers or on whitespace instead of the node border
- Region borders weaker than node borders (defeats the grouping device)

## Self-Review Checklist

Walk through every item before delivering. If any item fails, fix in place and re-state which items now pass.

- [ ] Spec block is embedded as the first comment inside `<svg>`, with all required fields filled
- [ ] viewBox covers all content with no element clipped at the edges
- [ ] Every `<text>` is fully inside the viewBox; no manual CJK line breaks for paragraphs
- [ ] Palette is exactly one of `claude-official` or `default` — no foreign hex values
- [ ] Every `font-weight` is one of `400`, `600`, `700`
- [ ] Every decision node has `data-edge-label` on each outgoing edge
- [ ] When both `edge` and `edge-soft` styles appear, a legend row sits in the bottom safe rail
- [ ] Every routed edge has stable `id` and `data-edge-id`; chips reference the same `data-edge-id`
- [ ] Arrowheads land on real node borders, not on whitespace or chip backgrounds
- [ ] If the diagram mixes architecture and flow, it has been split into two SVGs

## Escape Hatches

- Highly dynamic structure (data-driven dashboards, real-time state) → render with Mermaid at runtime instead
- 50+ nodes → split into 2–3 sub-diagrams; lead with an overview, follow with detail expansions
- User asked for "草图" / quick sketch → emit only the spec block first, request confirmation, then render the SVG
