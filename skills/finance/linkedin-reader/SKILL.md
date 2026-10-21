---
name: linkedin-reader
description: "Read LinkedIn feeds and job search through opencli. Use when LinkedIn is the requested source."
---

# linkedin-reader

Repository routing wrapper for `himself65/finance-skills` (`linkedin-reader`).

Read [.upstream/SKILL.md](.upstream/SKILL.md) completely and follow it; local rules below take precedence.

Resolve upstream references, scripts and assets under `.upstream/` relative to this installed skill directory. Resolve wrapper-local files beside this file. Pass the full installed path to file tools; resolve symlinks first when a canonical path is needed. Keep upstream snapshots unchanged; local overrides belong in this wrapper.
