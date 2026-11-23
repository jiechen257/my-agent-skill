# Independent reconstruction from a reference page

When the user asks to create a similar HTML from the reference page's content, separate four layers before writing code:

1. **Content** — facts, section themes, examples, and conclusions visible on the page.
2. **Information architecture** — the order and relationship of sections, cards, tables, flows, and diagrams.
3. **Visual language** — canvas, typography, colors, spacing, borders, cards, emphasis, and responsive behavior.
4. **Implementation** — new HTML structure, local class names, CSS rules, data, and scripts.

Use layers 1–3 as input and generate layer 4 independently. Do not copy the reference page's HTML subtree, CSS block, JavaScript, SVG coordinates, inline data arrays, class names as a batch, or source comments. Do not iframe the reference page, link to it as a stylesheet, or leave a remote URL as a runtime dependency. A similar result must be produced from the skill's style specification and a newly reasoned document outline.

For a content-heavy reference, preserve the meaning while recomposing the presentation: turn prose into a new combination of section summaries, comparison tables, maturity rows, stage flows, and evidence cards; create new diagram geometry from the concepts rather than tracing the original paths. Keep any quoted names or necessary factual labels, but write surrounding explanations and markup afresh.

For a reference-content recreation rather than a requested summary, build a coverage ledger before coding. Record every top-level section, numbered subsection, named list, table row family, diagram concept, metric, example, target, and conclusion from the visible reference. Map each item to a new section or component and preserve its factual value; only omit an item when the user explicitly asks for a summary, and state the omission boundary. A shorter page is not evidence of a successful reconstruction.

### Visual element and diagram ledger

For a high-fidelity recreation, keep a second ledger for visible elements, not just prose:

- Record the page skeleton: viewport baseline, outer canvas width, content width, side navigation width, sticky behavior, section spacing, and responsive breakpoints.
- Record repeated component geometry: heading bands, numbered pills, cards, tables, callouts, maturity rows, goal cards, proportion bars, timeline stages, and stacked layers. Preserve their visual role; do not replace a bar with cards or a diagram with a paragraph merely because the text is present.
- For each diagram, record the diagram type, number of visual groups, axes or rings, arrows, legends, labels, node families, core node, and approximate aspect ratio. Recompose the geometry independently with SVG or CSS primitives. A complex reference diagram must remain a complex visual component.
- Treat diagram layers as a visual reading order: background glow and rings first, connectors second, nodes third, labels and callouts last. Never draw a connector through readable text; reserve safe zones for annotations and use short leader lines when a label must sit near a path.
- Keep the SVG `viewBox` ratio consistent with its rendered box. Do not combine a wide viewBox with a tall fixed CSS box, which creates browser letterboxing and large blank bands. For radial diagrams, prefer a centered fixed-coordinate stage with deliberate outer whitespace; for flow diagrams, use distinct lanes, smooth curves, and clear endpoint labels rather than generic straight arrows.
- During comparison, inspect the same viewport and scroll position where possible. Compare element rectangles, computed typography, colors, borders, radii, gaps, SVG viewBox/aspect ratio, and visible node counts. If a local `file://` preview is blocked by browser automation policy, use source-level geometry checks and report that runtime measurement was unavailable; do not claim pixel-level verification.

The acceptance bar is separate for content coverage, information architecture, visual element fidelity, and implementation independence. Passing one bar does not imply the other three passed.

Before delivery, compare the output against that ledger by checking headings, named entities, numbers, examples, and conclusions—not only colors and layout. Treat these as separate completion bars: **content coverage**, **information-architecture similarity**, **visual similarity**, and **implementation independence**. Passing the last three cannot compensate for missing content coverage.

Completion criterion: the output has a new semantic structure and implementation, contains no copied source block or remote embed, and preserves the reference page's important content relationships and visual hierarchy.
