# SVG Layout Best Practices

Apply these rules across all types.

## Canvas

- Keep all primary content inside the `viewBox`
- Reserve at least 24px right and bottom padding
- Keep at least 28px inner safety distance between any region boundary and the nearest node body, label chip, or routed edge; use 36px+ when a region also carries feedback lanes
- Put summary notes in a top note rail or bottom legend rail
- Keep note cards fully inside the inner frame with at least 40px right inset
- Keep every line of note-card text at least 10px above the card bottom border
- Keep top note cards at least 16px above the next major region boundary
- Prefer compact note cards over full-width top rails; for sequence diagrams, widen modestly and wrap early instead of spanning most of the canvas
- Keep legend rows fully inside the inner frame with at least 56px bottom inset
- If a top note needs more than two body lines, widen the card or move it left before adding more text
- If a legend row cannot fit cleanly inside the safe rail, wrap it into two rows instead of pushing it downward or outside the frame

## Text

- Default output is Chinese
- In Chinese output, entity titles must be Chinese-first and may append necessary English terms, APIs, product names, acronyms, or code identifiers
- Avoid pure-English node, bus, layer, phase, and matrix labels when a clear Chinese semantic role exists
- Use mixed Chinese-English subtitles to explain technical terms; do not let the title and subtitle both be pure English
- Keep titles on one line when possible
- Keep node titles, cell labels, and bar labels inside their containers; widen before shrinking the text
- Keep node subtitles within two lines
- Use `<tspan>` for manual wraps
- Put text on opaque backgrounds when it sits near lines or grids
- Keep copy away from borders and routed edges; if text feels crowded, grow the node or increase lane spacing before shrinking typography
- Keep chips, pills, and note cards from colliding with node bodies or each other; create air before adding more labels

## Edges

- Use visible ports
- For architecture diagrams, every directed route should declare `data-from` and `data-to` with node ids; the first and last point must land on the source and target borders
- Do not use one `<path>` with multiple `M` subpaths for a directed edge; split it into separate routes or a dedicated bus plus directed branches
- Keep arrowheads visually subordinate to nodes and labels; for typical `1.5-2px` edges, start around `4.8 x 4.8` markers and only scale up when density or stroke weight requires it
- Prefer orthogonal routing unless the type needs direct message arrows
- In top-down architecture diagrams, ordinary dependency arrows should follow the dominant direction; upward final entries are valid only for explicit feedback paths with dashed styling or clear feedback labeling
- For one-to-one cross-layer dependencies that are vertically aligned or nearly aligned, align the source and target ports and use one straight vertical segment; short `V-H-V` doglegs under 24px are invalid because they add visual noise without routing value
- Keep unrelated edges off the same corridor segment
- Split competing in/out traffic across opposite sides or distinct ports
- For fan-in or fan-out, draw an `edge-bus` trunk with no arrowhead, then attach short directed `edge` branches with clear ownership
- For fan-out to 3 or more destinations across a layer, prefer a labeled routing bus / hub shape; stacked parallel long `V-H-V` doglegs from one source are invalid
- Put every edge label on a chip with an opaque fill
- Give every labeled edge a stable `id`, then annotate the owning chip and its text with the same `data-edge-id`
- For text-only relation labels such as `<<include>>` or `<<extend>>`, attach the text to the edge with `data-edge-id` and keep it close to the routed relation
- Wrap or widen note text, phase titles, legends, and edge chips before shrinking type; the validator estimates obvious overflow
- For horizontal segments, place the label chip **above the segment** by default
- For vertical segments, place the label chip on the outer side of the corridor, not over the line itself
- For vertical spine flows, a centered chip is acceptable only when the chip still leaves clear air above and below and still reads as belonging to that exact segment
- When a shared trunk fans out into multiple branches, place each label chip on the branch-owned segment after the split or immediately beside that branch's vertical drop
- Never place different branch labels on the same uninterrupted trunk segment when they describe different downstream drops
- If a shared trunk does not provide distinct branch-owned segments, add elbows, short stubs, or leader ticks so every label has an unambiguous one-to-one anchor
- The full label chip must fit inside a real straight segment after reserving at least 10px endpoint padding
- If a segment is too short for the label chip, reroute the edge to create a longer label lane
- A chip with `data-edge-id` must sit close enough to its owning edge to read as attached; floating chips are invalid even when they stay inside the canvas
- If a chip label outgrows its chip, widen the chip or reroute the edge instead of reducing readability
- Label chips must not overlap arrowheads, icons, node borders, or node copy
- Avoid edge routes that touch node corners, skim unrelated chips, or hug node borders; keep a visible approach gap before entry

## Regions

- Region boundaries should read stronger than node borders
- Use phase bands, system boundaries, matrix headers, or timeline lanes as the main grouping device
- Keep at least 28px vertical separation between stacked regions
- Keep decorative pills, legends, and note rails aligned to the same inner safe area as the main regions
- In architecture diagrams, mark each layer region with `data-layer-id` and give every node body in that layer the same `data-layer-id`
- Keep one node body fill per `data-layer-id`; badges, dashed borders, or text can carry status, while the layer keeps visual consistency
- Every layer node body must sit fully inside the matching region with at least 24px inset unless the region is an intentionally tight table or swimlane

## Style Preservation

- When editing an existing SVG, preserve the source palette, radius, shadows, stroke weights, and typography unless the user asks for a restyle
- Fix geometry and routing before changing visual styling
- Do not introduce glassmorphism, neumorphism, backdrop blur, gradients, or decorative glow into an existing plain SVG

## Shape Variety

- Do not render every concept as the same rounded rectangle
- Use the smallest valid shape vocabulary for the chosen type
- Introduce subpanels when one area needs local detail

## Type-Specific Notes

### Flowchart

- Forward path should dominate visually
- Put feedback loops on outer corridors
- Decision branches need dedicated left/right or top/bottom exits
- Keep 24px+ pure whitespace between vertically adjacent nodes, excluding chips and arrows; framework diagrams usually want 32px+
- Prefer enlarging the canvas or phase band instead of compressing nodes, labels, and arrows into one cluster
- For branch convergence into one terminal/output node, route each branch as `down -> horizontal -> down` or an equivalent orthogonal fold that preserves branch ownership
- Avoid diagonal branch entries into shared terminal nodes unless the diagram type explicitly calls for direct vectors

### Sequence

- Lifelines align vertically
- Messages stay horizontally readable
- Use activation bars for processing windows
- Participant heads should end before the first phase band begins; phase titles belong inside the time area, not in the note rail
- Sequence message endpoints must land on the owning lifeline or on the centerline of an overlapping activation bar
- Every activation bar must overlap at least one message endpoint on the same centerline; dangling activation windows are invalid
- Lifelines should extend at least 24px below the last message to avoid clipped final arrows
- Branch frames must fully cover all branch-owned messages and activation bars
- When a branched frame carries semantic ownership, annotate the frame and separator with `data-frame-id`, then annotate branch titles and branch-owned message lines with matching `data-frame-id` and `data-branch`
- `data-branch="1"` content belongs above the separator; `data-branch="2"` content belongs below it unless a different branch convention is explicitly documented in the SVG

### Timeline

- One horizontal time scale per diagram
- Keep milestone labels from colliding with bars

### Comparison Matrix

- Header row must stay visually stronger than body rows
- Keep column count readable

### Use Case

- Actors remain outside the boundary
- Include and extend relationships should be dashed and labeled
