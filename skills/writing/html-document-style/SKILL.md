---
name: html-document-style
description: "Create or improve self-contained HTML reports, proposals, technical plans, and research documents in the bundled paper-and-sidebar style, including responsive reading and optional offline reading tools. Use also for independent recreation of a document reference."
---

# HTML Document Style

Create readable document artifacts with the bundled visual identity: pale gray canvas, white paper, blue-purple structure, and a left table of contents. Content relationships determine the layout; visual consistency, reading comfort, and evidence traceability are separate quality goals.

## Reference boundary

Before implementing, read these files from this skill directory:

- `assets/reference.html` — the self-contained fictional demo page and canonical CSS/SVG treatment.
- `references/style-spec.md` — the distilled tokens, layout rules, component mapping, and required left navigation extension.

The bundled reference and examples use fictional people, projects, metrics, and plans. Use them for visual structure only; never present their content as real business evidence.

The reference supplies the visual identity and reconstruction baseline. The style specification also defines adaptive reading defaults for new documents. Read `references/reading-experience.md` when the document is long, contains dense tables or diagrams, or needs reading tools. `assets/reading-example.html` is an executable fictional example of those behaviors, not factual input or a mandatory page outline.

## Choose the document mode

- **New document or reading improvement**: preserve the paper-and-sidebar identity, then choose density, components, and diagrams from the content and audience. Use the reading defaults in `references/style-spec.md`.
- **Reference recreation**: preserve the requested content and visual relationships. Read `references/reconstruction.md` before coding; its coverage and visual ledgers apply to this branch.

When improving an existing artifact, retain its key facts, caveats, numbers, and source relationships. Keep the prior artifact available when the user needs a comparison.

## Workflow

### 1. Freeze the document outline

First identify the audience, reading task, and key conclusion. Decide the title, optional eyebrow or keyword chips, top-level sections, and meaningful subsections. For long proposals, add a short summary of the decision, evidence, and next step before the detailed chapters. Keep factual caveats beside the claims they qualify. Give every navigable top-level section a stable, URL-safe `id`. Use semantic `<main>`, `<section>`, `<h1>`, `<h2>`, `<h3>`, `<nav>`, `<ol>`, `<table>`, and `<figure>` elements so the visual hierarchy and the document outline agree.

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

The TOC is a narrow, white, rounded, lightly shadowed rail on the left; it is `position: sticky` on desktop, stays visible while the document scrolls, and highlights the section currently in view. Keep that active link visible by scrolling the navigation container when necessary, without moving the document. Add `scroll-margin-top` to section targets, visible keyboard focus, `aria-current="location"` for the active link, and a reduced-motion fallback. On narrow screens, turn the rail into a full-width horizontally scrollable sticky strip above the canvas; preserve the same ordering and anchors. Use subnavigation when long chapters have meaningful subsections. Match anchor offsets to the actual sticky stack and recheck after density changes or resize.

The document canvas remains the reference page's white paper: centered, capped at about `1240px`, with a thin border, `14px` radius, soft shadow, and generous inner padding. Do not replace the TOC with a floating button on desktop.

### 3. Render content with the reference vocabulary

Use the following mapping:

- Header: centered gradient `h1`, with an optional small English eyebrow and lavender keyword chips when those labels aid orientation.
- Top-level section: dark slate numbered badge, bold title, and muted one-line description.
- Subsection: short blue vertical rule, bold label, and an optional bordered tag.
- Sequential points: numbered circular list with bold lead-ins; use semantic `<ol>`. Use paragraphs or ordinary lists for points without a meaningful order.
- Parallel concepts: two-, three-, or four-column cards with pale surfaces, thin gray borders, and `10px` radius. Use prose, divided columns, or description rows when extra containers add no meaning. Keep prose line lengths comfortable even on a wide paper canvas.
- Comparison or evidence: plain bordered tables with slate header fill, tabular numbers, nowrap labels where useful, and no decorative zebra overload.
- Progress or stages: pastel status rows, horizontal timelines, split bars, and red left-accent challenge blocks.
- Diagrams: choose a flow for sequence, layers for dependency, and radial geometry for a genuine center-and-periphery relationship. A dark scoped panel is available for a major diagram; rings and English labels are optional. Keep connectors outside text. On narrow screens, preserve the complete reading order through reflow or an equivalent textual view; reserve panning for an optional detailed view.
- Ending: a light summary panel with a purple top rule and one strong takeaway.

### 4. Apply visual tokens before polishing copy

Use the shared colors and paper treatment in `references/style-spec.md`. Choose its reading defaults for new long documents and its baseline geometry for faithful recreation. Preserve the visual balance: neutral page background, white paper, slate text, purple/blue structure, red emphasis, and restrained green/cyan/amber status colors. Keep Chinese body copy compact and readable; use English for eyebrows, diagram labels, and secondary taxonomy, not as decoration everywhere.

Use inline CSS and inline SVG by default so the HTML opens offline and can be copied as one artifact. Add external dependencies only when the user explicitly requests them. Keep all diagram geometry and component CSS inside the document or a clearly named local block; do not depend on an unavailable build step.

### 5. Add reading tools selectively

Navigation, focus visibility, and responsive reading are baseline behavior. Add other tools when they address a real task: search for long documents, progressive detail for supporting material, source backlinks for evidence, copy for reusable snippets, diagram expansion for dense figures, density controls for mixed reading needs, and print for sharing.

Use the behavior contracts and checks in `references/reading-experience.md`. Keep the article useful without JavaScript; reveal enhanced controls only when their behavior is available. Use a small local script, native controls, and in-memory state by default. Existing user choices and requested output take priority over the example's feature set.

Completion criterion: every visible control has a working result and failure behavior, and supporting details remain accessible without the enhancements.

### 6. Verify the artifact

Open the generated file in a real browser and check at least the desktop view plus a narrow view. Confirm:

- the first viewport shows the page background, left TOC, white canvas, title, and the first section;
- every TOC link jumps to the intended heading, active state updates during actual reading, and the active link remains visible inside the rail or strip;
- no section is hidden behind the sticky TOC or sticky mobile strip;
- cards, tables, diagrams, and long Chinese-English lines do not create accidental horizontal overflow; the primary diagram remains understandable without repeated sideways panning;
- the dark diagram remains readable and does not leak dark styles into surrounding cards;
- tablet and narrow-phone layouts collapse sensibly; test both sides of the chosen breakpoints and check the sticky stack at approximately 390px and 320px widths;
- inspect rendered print pages: heading/body continuity, repeated table headers, complete diagrams, readable code, and revealed supporting details. Keep small units together; allow long chapters to paginate;
- the file is self-contained and opens without network access.

Completion criterion: inspect desktop and phone screenshots, run the relevant reading-tool checks, and report exactly what was verified. Correct DOM state and lack of page overflow alone do not establish usability. If browser or print rendering is unavailable, state that limit rather than claiming visual acceptance.

## Guardrails

- Preserve the reference's document-first density and hierarchy. Do not turn it into a SaaS dashboard, marketing landing page, glassmorphism surface, or dark-mode-only page.
- Keep strong color for hierarchy and evidence. Avoid adding arbitrary colors, oversized illustrations, stock images, or large decorative gradients.
- Use red emphasis for risks, warnings, and critical conclusions; use blue or purple for structure and primary highlights; use green/cyan/amber for status families.
- Keep the left TOC outside the white paper on desktop so it reads as navigation, not as document content. The content column must remain the dominant visual surface.
- Preserve accessible contrast, semantic headings, keyboard focus, table headers, image/figure descriptions, and reduced-motion behavior while matching the appearance.
- When the request is for a proposal or technical plan, keep evidence, assumptions, decisions, risks, and next steps explicit inside the same visual system; style must not hide uncertainty.
