# Template Examples

This folder stores denser reference diagrams copied before the starter reset.

- `templates/` now contains starter skeletons for generation
- `examples/` preserves richer, example-like layouts for visual reference only
- When updating presets, prefer changing `templates/` first and keep `examples/` as snapshots or inspiration

## Review Notes

The examples are also a UI regression surface. Keep them passing:

```bash
bash skills/content/architecture-diagram/scripts/test-all.sh
```

Current visual contracts:

- Flowchart arrows land on node borders; branch merges do not leave orphan arrows in whitespace.
- Comparison matrices include the top-left dimension header cell.
- Architecture routes avoid sitting on region borders and start from real source nodes.
- Data-flow feedback lanes start and end on entity borders.
- State-machine retry edges start from state borders.
- Use-case include / extend relations are dashed and land on use-case ellipses.
