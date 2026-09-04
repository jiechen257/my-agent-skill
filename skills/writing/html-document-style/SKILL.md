---
name: html-document-style
description: "Use when generating or independently reconstructing a self-contained HTML document, proposal, report, technical plan, research note, or presentation-like artifact from the All in Agent reference page: pale gray canvas, centered white paper, blue-purple title, compact numbered sections, pastel cards and tables, red-blue emphasis, inline SVG diagrams, and a sticky left table of contents; use the reference's content and visual language without copying its source code."
---

# HTML Document Style

Generate HTML documents with the visual language of the saved All in Agent reference page. The output is a readable document artifact, not a generic landing page: content density, hierarchy, evidence blocks, and scanability come first.

## Reference boundary

Before implementing, read these files from this skill directory:

- `assets/reference.html` — the downloaded, self-contained source page and canonical CSS/SVG treatment.
- `references/style-spec.md` — the distilled tokens, layout rules, component mapping, and required left navigation extension.

Treat the local source as the visual source of truth. Reuse its values and component ideas, adapting copy and structure to the requested document. Do not claim the generated page is pixel-identical when the content, viewport, or diagram geometry differs.

## Independent reconstruction from a reference page

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

## Workflow

### 1. Freeze the document outline

First decide the title, optional English eyebrow, keyword chips, top-level sections, and meaningful subsections. Give every navigable top-level section a stable, URL-safe `id`. Use semantic `<main>`, `<section>`, `<h1>`, `<h2>`, `<h3>`, `<nav>`, `<ol>`, `<table>`, and `<figure>` elements so the visual hierarchy and the document outline agree.

Completion criterion: the outline is explicit, every TOC target exists exactly once, and no section is reachable only through visual position.

### 2. Build the shell and left TOC

Use this page shape on desktop:

```html
<body>
  <div class="page-shell">
    <aside class="toc" aria-label="文档目录">
      <div class="toc__title">目录 <span>CONTENTS</span></div>
      <nav>
        <a href="#section-id"><span class="toc__no">一</span><span>章节标题</span></a>
      </nav>
    </aside>
    <main class="canvas">
      <!-- header and document sections -->
    </main>
  </div>
</body>
```

The TOC is a narrow, white, rounded, lightly shadowed rail on the left; it is `position: sticky` on desktop, stays visible while the document scrolls, and highlights the section currently in view. Add `scroll-margin-top` to section targets, visible keyboard focus, `aria-current="location"` for the active link, and a reduced-motion fallback. On narrow screens, turn the rail into a full-width horizontally scrollable sticky strip above the canvas; preserve the same ordering and anchors.

The document canvas remains the reference page's white paper: centered, capped at about `1240px`, with a thin border, `14px` radius, soft shadow, and generous inner padding. Do not replace the TOC with a floating button on desktop.

### 3. Render content with the reference vocabulary

Use the following mapping:

- Header: centered gradient `h1`, small uppercase English eyebrow, and compact lavender keyword chips.
- Top-level section: dark slate numbered badge, bold title, and muted one-line description.
- Subsection: short blue vertical rule, bold label, and an optional bordered tag.
- General points: numbered circular list with bold lead-ins; use semantic `<ol>` rather than manually typed numbers.
- Explanatory content: two-, three-, or four-column cards with pale gradient surfaces, thin gray borders, `10px` radius, and compact Chinese-English typography.
- Comparison or evidence: plain bordered tables with slate header fill, tabular numbers, nowrap labels where useful, and no decorative zebra overload.
- Progress or stages: pastel status rows, horizontal timelines, split bars, and red left-accent challenge blocks.
- Architecture or relationship: use a single dark, scoped diagram panel with inline SVG, layered rings, colored nodes, and concise English labels; keep diagram styles namespaced under its panel.
- Ending: a light summary panel with a purple top rule and one strong takeaway.

### 4. Apply visual tokens before polishing copy

Start from the exact tokens in `references/style-spec.md`. Preserve the visual balance: neutral page background, white paper, slate text, purple/blue structure, red emphasis, and restrained green/cyan/amber status colors. Keep Chinese body copy compact and readable; use English for eyebrows, diagram labels, and secondary taxonomy, not as decoration everywhere.

Use inline CSS and inline SVG by default so the HTML opens offline and can be copied as one artifact. Add external dependencies only when the user explicitly requests them. Keep all diagram geometry and component CSS inside the document or a clearly named local block; do not depend on an unavailable build step.

### 5. Add behavior without changing the document character

Use a small inline script only for behavior that improves reading:

- intersection-based active TOC state;
- optional smooth scrolling, disabled under `prefers-reduced-motion: reduce`;
- responsive sizing of a fixed-coordinate SVG diagram, following the reference page's scale-to-container approach.

Do not add app-like routing, modal onboarding, animated hero effects, or unrelated interaction. A generated document should still be useful with JavaScript disabled.

### 6. Verify the artifact

Open the generated file in a real browser and check at least the desktop view plus a narrow view. Confirm:

- the first viewport shows the page background, left TOC, white canvas, title, and the first section;
- every TOC link jumps to the intended heading and active state updates while scrolling;
- no section is hidden behind the sticky TOC or sticky mobile strip;
- cards, tables, diagrams, and long Chinese-English lines do not create accidental horizontal overflow;
- the dark diagram remains readable and does not leak dark styles into surrounding cards;
- at `max-width: 1024px`, grids collapse sensibly and the TOC remains usable; at `640px`, cards become one column and the TOC becomes horizontal;
- print preview removes the page-gray background and shadow, preserves colors, and avoids splitting a section when practical;
- the file is self-contained and opens without network access.

Completion criterion: the HTML opens successfully, the TOC is functional or gracefully static without JavaScript, the reference visual system is visible in a screenshot, and the responsive/print checks have been run or their untested scope is stated.

## Guardrails

- Preserve the reference's document-first density and hierarchy. Do not turn it into a SaaS dashboard, marketing landing page, glassmorphism surface, or dark-mode-only page.
- Keep strong color for hierarchy and evidence. Avoid adding arbitrary colors, oversized illustrations, stock images, or large decorative gradients.
- Use red emphasis for risks, warnings, and critical conclusions; use blue or purple for structure and primary highlights; use green/cyan/amber for status families.
- Keep the left TOC outside the white paper on desktop so it reads as navigation, not as document content. The content column must remain the dominant visual surface.
- Preserve accessible contrast, semantic headings, keyboard focus, table headers, image/figure descriptions, and reduced-motion behavior while matching the appearance.
- When the request is for a proposal or technical plan, keep evidence, assumptions, decisions, risks, and next steps explicit inside the same visual system; style must not hide uncertainty.
