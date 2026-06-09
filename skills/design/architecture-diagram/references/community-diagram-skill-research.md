# Community Diagram Skill Research

Research date: 2026-05-17

## Observed Patterns

- Mermaid skills dominate community examples because `.mmd` source is text-based, diffable, and easy to render in GitHub or local tooling. Examples include [WH-2099/mermaid-skill](https://github.com/WH-2099/mermaid-skill) and [Agents365-ai/mermaid-skill](https://github.com/Agents365-ai/mermaid-skill).
- Rendering-first Mermaid skills add a validation loop before export and use local `mmdc` or a fallback renderer. Agents365 highlights validation before PNG/SVG/PDF export and a Kroki fallback.
- Beautiful Mermaid-style workflows separate source generation, SVG rendering, HTML wrapping, and high-resolution PNG capture. This is useful as a preview discipline even when this skill's canonical output remains SVG.
- YAML/spec-first tools such as [diagrams.sh](https://www.diagrams.sh/) use a compact intermediate representation with `nodes` and `edges`, then render from that contract. This maps well to this skill's embedded `spec` comment.
- D2 exposes multiple layout engines and makes layout choice explicit. Its docs list Dagre, ELK, and TALA, with TALA aimed at software architecture diagrams. This supports keeping a type-specific layout contract instead of relying on one universal routing style.
- C4-oriented skills and community posts emphasize audience, abstraction level, editability, and review. The [C4 model](https://c4model.info/) uses hierarchical abstraction levels; community C4 skills often emit editable `.drawio` or C4-PlantUML outputs for stakeholder review.
- Research on diagram generation, including [DiagrammerGPT](https://arxiv.org/abs/2310.12128), supports a two-stage approach: produce a diagram plan, then render and audit the visual output.

## Implications For This Skill

1. Keep `spec` as the intermediate representation.
   The spec should remain the contract between intent and SVG. It gives the validator a future path to check parity between declared nodes, edges, labels, and rendered geometry.

2. Treat layout as a typed contract.
   Architecture, flowchart, sequence, timeline, matrix, state-machine, data-flow, and use-case diagrams need different endpoint, lane, frame, and label rules. Type-specific validators catch the UI failures that XML validation misses.

3. Add render-and-review as a quality gate for dense diagrams.
   Validator success proves structural safety. A local preview catches visual rhythm, empty table corners, awkward whitespace, and line-border overlap.

4. Prefer deterministic SVG for polished docs, use DSLs as layout references when needed.
   Mermaid, PlantUML, Graphviz, or D2 can help pressure-test graph structure. The final output can still be hand-routed SVG when editorial control, typography, and exact label placement matter.

5. Maintain an eval set with visual probes.
   A prompt-only test set should cover branch merges, cross-layer routing, matrix headers, data feedback lanes, alt frames, retry loops, timeline milestones, use-case relations, and split-diagram decisions.

6. Keep optional editable-output ideas separate from the current scope.
   draw.io and Excalidraw workflows are useful for collaborative editing. This skill's current scope remains standalone SVG, so editable exports should be a future extension or sibling skill.
