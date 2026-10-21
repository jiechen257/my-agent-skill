---
name: yc-reader
description: "Look up Y Combinator companies and batches through the public yc-oss API."
---

# yc-reader

Repository routing wrapper for `himself65/finance-skills` (`yc-reader`).

Read [.upstream/SKILL.md](.upstream/SKILL.md) completely and follow it; local rules below take precedence.

Resolve upstream references, scripts and assets under `.upstream/` relative to this installed skill directory. Resolve wrapper-local files beside this file. Pass the full installed path to file tools; resolve symlinks first when a canonical path is needed. Keep upstream snapshots unchanged; local overrides belong in this wrapper.
