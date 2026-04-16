# SVG Layout Best Practices

Apply these rules across all types.

## Canvas

- Keep all primary content inside the `viewBox`
- Reserve at least 24px right and bottom padding
- Put summary notes in a top note rail or bottom legend rail

## Text

- Default output is Chinese
- Keep titles on one line when possible
- Keep node subtitles within two lines
- Use `<tspan>` for manual wraps
- Put text on opaque backgrounds when it sits near lines or grids

## Edges

- Use visible ports
- Prefer orthogonal routing unless the type needs direct message arrows
- Keep unrelated edges off the same corridor segment
- Split competing in/out traffic across opposite sides or distinct ports
- Put every edge label on a chip with an opaque fill

## Regions

- Region boundaries should read stronger than node borders
- Use phase bands, system boundaries, matrix headers, or timeline lanes as the main grouping device
- Keep at least 28px vertical separation between stacked regions

## Shape Variety

- Do not render every concept as the same rounded rectangle
- Use the smallest valid shape vocabulary for the chosen type
- Introduce subpanels when one area needs local detail

## Type-Specific Notes

### Flowchart

- Forward path should dominate visually
- Put feedback loops on outer corridors
- Decision branches need dedicated left/right or top/bottom exits

### Sequence

- Lifelines align vertically
- Messages stay horizontally readable
- Use activation bars for processing windows

### Timeline

- One horizontal time scale per diagram
- Keep milestone labels from colliding with bars

### Comparison Matrix

- Header row must stay visually stronger than body rows
- Keep column count readable

### Use Case

- Actors remain outside the boundary
- Include and extend relationships should be dashed and labeled
