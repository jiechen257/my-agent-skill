---
name: opencli-reader
description: "Read a named website through opencli when no dedicated source reader applies. Use for explicit opencli or supported-site requests."
---

# opencli-reader

Repository routing wrapper for `himself65/finance-skills` (`opencli-reader`).

Read [.upstream/SKILL.md](.upstream/SKILL.md) completely and follow it; local rules below take precedence.

Resolve upstream references, scripts and assets under `.upstream/` relative to this installed skill directory. Resolve wrapper-local files beside this file. Pass the full installed path to file tools; resolve symlinks first when a canonical path is needed. Keep upstream snapshots unchanged; local overrides belong in this wrapper.
