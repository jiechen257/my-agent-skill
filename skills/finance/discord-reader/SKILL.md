---
name: discord-reader
description: "Read Discord messages for financial research through opencli and the local Discord app. Requires an explicit Discord source."
---

# discord-reader

Repository routing wrapper for `himself65/finance-skills` (`discord-reader`).

Read [.upstream/SKILL.md](.upstream/SKILL.md) completely and follow it; local rules below take precedence.

Resolve upstream references, scripts and assets under `.upstream/` relative to this installed skill directory. Resolve wrapper-local files beside this file. Pass the full installed path to file tools; resolve symlinks first when a canonical path is needed. Keep upstream snapshots unchanged; local overrides belong in this wrapper.
