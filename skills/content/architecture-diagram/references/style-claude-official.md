# Claude Official Style

Use this as the default style profile for new diagrams.

## Restyle Boundary

When revising an existing SVG, preserve its current UI language first: palette, radius, shadows, stroke weights, typography, and spacing rhythm. Fix structure, routing, labels, and containment without replacing the visual style.

Do not add glassmorphism, neumorphism, backdrop blur, gradients, decorative glow, or a new shadow system unless the user asks for a restyle.

## Tokens

- Page background: `#f8f6f3`
- Surface background: `#fffdf8`
- Surface border: `#d9d3ca`
- Grid stroke: `#ddd6cc`
- Primary text: `#1a1a1a`
- Secondary text: `#6a6a6a`
- Subtle text: `#5a5a5a`
- Main connector: `#5a5a5a`
- Shadow: `feDropShadow dx=0 dy=2 stdDeviation=4 flood-color=#00000012`

## Semantic Fills

- Source / Input: `#a8c5e6`
- Process / Agent: `#9dd4c7`
- Infrastructure / Timeline bar: `#f4e4c1`
- Storage / State / Passive area: `#e8e6e3`
- Note card: `#dff3ef`
- Decision node: `#fff7e8`

For architecture diagrams, prefer layer fills over semantic fills: all node bodies inside one layer share the same fill. Use badges, strokes, dash, or small labels for status differences.

## Geometry

- Corner radius: `12`
- Primary stroke width: `2` to `2.4`
- Region stroke width: `1.6`
- Label chip radius: `5` to `6`

## Typography

- Font weight is restricted to `400`, `600`, or `700`. Do not emit values like `740`, `760`, `780` — most fonts round them to the nearest 100, flattening the visual hierarchy.
- Sizes (px): title `30`, subtitle `15`, region label `12`, node title `14`, node subtitle `11`, tiny chip `10–11`.
- Use `<foreignObject>` with `xmlns="http://www.w3.org/1999/xhtml"` when CJK copy exceeds 8 characters; do not hand-break CJK across multiple `<text>` lines.

## Tone

- Warm, editorial, documentation-ready
- Low saturation, high readability
- Keep arrow colors restrained unless the type absolutely needs semantic color separation

## Best Fit

- architecture
- flowchart
- sequence
- state-machine
- timeline
- comparison-matrix
- use-case
