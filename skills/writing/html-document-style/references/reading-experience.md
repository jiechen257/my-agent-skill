# Reading experience

Read when generating long documents, adapting dense figures/tables, or adding reading tools. These are behavior contracts, not a requirement to add every feature. The runnable fictional example is `../assets/reading-example.html`.

## Content before components

Map the reader's tasks to the document before choosing surfaces:

| Reader task | Suitable treatment |
| --- | --- |
| Decide whether to continue | Short conclusion, evidence, and next step near the start |
| Follow an argument | Prose with a bounded line length and informative headings |
| Compare alternatives | Table with explicit comparison dimensions |
| Understand a sequence | Directional flow; vertical steps on phones |
| Understand dependencies | Layered structure with labeled relationships |
| Understand a center and its ecosystem | Radial diagram with a real semantic center |
| Verify a conclusion | Local citation, evidence fragment, version/date, and return link |
| Inspect optional detail | Native `details` with a descriptive summary |

Core conclusions, failure conditions, and caveats stay visible. Optional details must not become the only location for an important constraint. Preserve the source's numbers and their meaning: targets, assumptions, observed results, and fictional values remain distinct.

Use cards for genuinely parallel concepts. Repeated borders, labels, and English eyebrows should carry information rather than decorate every paragraph. Use text, whitespace, and rules to express simpler relationships.

## Density and width

For a new long document, start with 15px body text, 1.85–1.95 line height, and prose around 60–72ch. Tables may use 12.5–14px depending on density; key judgments should not live only in small muted type. Compact reference recreation can retain the original 12–13.5px scale.

A density switch is useful for mixed scanning and close reading. Change spacing and type within a readable range, keep the current location meaningful, and recheck anchors. It is optional for short documents.

## Navigation

- Keep every anchor unique and stable, including navigable subsections.
- Update `aria-current="location"` from the reading position. When the active item is outside the visible rail/strip, adjust that container's scroll position only. Do not use a global `scrollIntoView` that pulls the body backward.
- Test normal body scrolling as well as clicking links. A correct active attribute on an invisible link does not pass.
- Use either scroll padding or target margin deliberately. Avoid adding two offsets that leave excessive blank space; check the combined sticky toolbar and mobile strip.
- Progress reflects the actual document scroll range, recomputes on layout changes, and does not announce every scroll to screen readers.

## Feature contracts

| Tool | Required behavior when present | Browser check |
| --- | --- | --- |
| Local search | Search local text only; show context and a no-result state; keep the document intact; open enclosing `details` and focus the hit below sticky navigation | Find a hidden code term, follow the result, then search for absent and markup-like text |
| Search/diagram dialog | Accessible name, keyboard operation, Escape close, focus restoration, viewport-bounded height; native `dialog` where supported | Open by button and shortcut; close from the input and the figure; verify focus returns |
| Citation/backlink | Match a real supplied source or clearly fictional case fragment; preserve source version and return context | Follow citation to source and return; inspect printed labels |
| Copy snippet | Copy the intended text; report failure truthfully; offer manual selection when unavailable | Exercise success and denied/unavailable clipboard separately |
| Figure expansion | Preserve a readable main view; let readers inspect more detail without losing context | Open/close with keyboard; on phone confirm the primary flow already shows all steps |
| Supporting detail | Native summary with meaningful wording; content remains reachable without JS | Open without JS; search into it; include it when printing |
| Print/PDF entry | Label browser print clearly; hide controls; expose supporting text; restore disclosure state afterward | Check print entry and before/after state; inspect every rendered page |

Render search excerpts with text nodes or properly escaped text. Do not interpolate search terms into HTML or unescaped regular expressions. Keyboard shortcuts should avoid unrelated modifier combinations and active modal conflicts. Show enhancements only when initialized and supported; leave native reading and browser find/print available otherwise.

Clipboard behavior varies with local-file permissions; a simulated success test checks UI logic, not actual clipboard permission on the user's browser. State that distinction in validation notes.

## Narrow screens and figures

For the primary document, choose reflow, stacked rows, abbreviated labels plus full descriptions, or a readable equivalent view before accepting horizontal panning. Keep the same order, values, and relationships in alternate representations. Use one content source when practical and verify parity when both views are authored separately.

For responsive tables, preserve row labels, dimensions, values, and states. If rows become stacked cards, retain semantic header associations or provide an accessible equivalent; do not assume visual reflow proves screen-reader support. Local scrolling is appropriate for irreducible large matrices or optional expanded figures, with a visible cue and keyboard access.

## Print and completion evidence

Use print CSS for page shape; use `beforeprint`/`afterprint` only when state needs temporarily changing. Restore the original disclosure state, including canceled printing. Rendered output should include supporting content, repeated table headers, complete figures, and code wrapping or appropriate scaling.

Apply `break-inside: avoid` to small logical units such as a short figure, row, or example. Let long chapters paginate. Inspect actual pages for large empty bordered fragments, orphan headings, clipped content, and excessive blank space; the existence of a print stylesheet is insufficient.

A useful validation record separates:

1. **Structure/content**: valid anchors, retained facts, versions, caveats, and alternate-view parity.
2. **Behavior**: reading-position navigation, visible active item, focus, search disclosure, copy failure, print restoration, no-JS fallback, and no remote runtime requests.
3. **Visual inspection**: desktop and phone screenshots plus print pages. Include tablet/breakpoint checks for layout changes.

Test the behaviors included in the document; do not add features solely to make the checklist longer. Report viewport, browser, actual checks, and material untested scope.
