#!/usr/bin/env python3
"""Read installed skill entrypoints and their explicit local resource references.

Markdown links and inline resource paths are dependencies; fenced examples,
URLs, placeholders and output directories are not. This checks file packaging,
not the meaning of instructions or successful execution of referenced scripts.
"""

import argparse
from collections import deque
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


RESOURCE = re.compile(r"^(?:\.\.?/|\.upstream/|references/|scripts/|assets/|templates/|deps/|bundle/)")
PLACEHOLDER = re.compile(r"<\w[\w.-]*>|\{\w[\w.-]*\}")


def markdown_references(text):
    """Use CommonMark links and code spans, excluding code-block examples."""
    try:
        from markdown_it import MarkdownIt
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing audit dependency; run: uv run --with-requirements "
            "scripts/requirements-audit.txt python scripts/audit-skill-references.py"
        ) from exc

    line_offsets = [0] + [match.end() for match in re.finditer("\n", text)]
    for token in MarkdownIt("commonmark").parse(text):
        if token.type != "inline":
            continue
        offset = line_offsets[token.map[0]]
        for child in token.children or []:
            attribute = {"link_open": "href", "image": "src"}.get(child.type)
            if attribute is not None:
                yield child.attrGet(attribute), offset, False
            elif child.type == "code_inline":
                yield child.content, offset, True


def references(text):
    found = set()
    for value, offset, inline in markdown_references(text):
        if inline:
            # A code span is a filesystem spelling, including %, #, ? and =.
            # Whitespace-bearing command examples are outside this contract.
            if re.search(r"\s", value) or not RESOURCE.match(value):
                continue
            path = value
        else:
            # Only Markdown destinations have URI query/fragment/escaping rules.
            parts = urlsplit(value)
            if parts.scheme or parts.netloc:
                continue
            path = unquote(parts.path)
        if path.startswith(("/", "~")) or PLACEHOLDER.search(path) or "*" in path:
            continue
        if not path or inline and not Path(path).suffix:
            # Inline directory names can be output folders; explicit
            # Markdown links also cover directories and extensionless files.
            continue
        line = text.count("\n", 0, offset) + 1
        if (path, line) not in found:
            found.add((path, line))
            yield path, line, inline and not path.startswith(("./", "../"))


def discover_entries(root):
    """Discover visible nested skills, following directory links without cycles."""
    root = Path(root)
    queue = deque([root])
    visited = set()
    while queue:
        directory = queue.popleft()
        real = directory.resolve(strict=True)
        if real in visited:
            continue
        visited.add(real)
        entry = directory / "SKILL.md"
        if entry.is_file() or entry.is_symlink():
            yield entry
        for child in sorted(directory.iterdir()):
            if child.name.startswith("."):
                continue
            if child.is_symlink() and not child.exists():
                # A visible broken link is a packaging error at every depth.
                # Its target type cannot be recovered after deletion.
                yield child / "SKILL.md"
            elif child.is_dir():
                queue.append(child)


def owning_skill_root(real, fallback):
    """Choose the nearest physical SKILL.md owner, independently of caller order."""
    for directory in real.parents:
        if (directory / "SKILL.md").is_file():
            return directory
    return fallback


def audit_entry(entry):
    """Follow references using filesystem symlink semantics, opening each file."""
    entry = Path(entry).absolute()
    queue = deque([(entry, entry.parent)])
    files = set()
    visited = set()
    issues = []
    entry_real = None
    try:
        entry_real = entry.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        return {"files": files, "issues": [f"{entry}: unreadable entry: {exc}"]}
    while queue:
        path, skill_root = queue.popleft()
        try:
            real = path.resolve(strict=True)
            skill_root = owning_skill_root(real, skill_root)
            # File symlinks can share bytes while resolving ./ differently.
            # Canonicalize the parent directory only, preserving that context;
            # also distinguish a Markdown alias from an opaque resource alias.
            context = (real, skill_root, path.parent.resolve(strict=True), path.suffix.lower() == ".md")
            if context in visited:
                continue
            data = path.read_bytes()
        except (OSError, RuntimeError) as exc:
            issues.append(f"{path}: unreadable file: {exc}")
            continue
        files.add(real)
        visited.add(context)
        if path.suffix.lower() != ".md":
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            issues.append(f"{path}: invalid Markdown encoding: {exc}")
            continue
        for ref, line, skill_relative in references(text):
            # Inline `scripts/...` / `references/...` names address the skill
            # bundle; Markdown links and explicit ./ or ../ address the file.
            target = (skill_root if skill_relative else path.parent) / ref
            try:
                target.resolve(strict=True)
                if target.is_dir():
                    # Actually open directories as well as checking existence.
                    next(target.iterdir(), None)
                    continue
            except (OSError, RuntimeError) as exc:
                issues.append(f"{path}:{line}: missing resource {ref}: {exc}")
                continue
            if real == entry_real and ref.startswith("../"):
                normalized = Path(os.path.normpath(target))
                if normalized.resolve() != target.resolve():
                    issues.append(f"{path}:{line}: normalization-sensitive reference {ref}; bundle it under .upstream/")
            queue.append((target, skill_root))
    return {"files": files, "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", type=Path, help="Installed skill directory (repeatable)")
    parser.add_argument("--entry", action="append", type=Path, default=[], help="Explicit SKILL.md (repeatable)")
    args = parser.parse_args()
    roots = args.root if args.root is not None else ([] if args.entry else [
        Path.home() / ".codex/skills", Path.home() / ".agents/skills",
    ])
    entries = list(args.entry)
    for root in roots:
        if args.root is None and not root.exists() and not root.is_symlink():
            continue
        if not root.is_dir():
            parser.error(f"skill root does not exist: {root}")
        try:
            entries.extend(discover_entries(root))
        except (OSError, RuntimeError) as exc:
            parser.error(f"cannot discover skills under {root}: {exc}")
    failed = False
    files = set()
    for entry in entries:
        result = audit_entry(entry)
        files.update(result["files"])
        failed |= bool(result["issues"])
        for issue in result["issues"]:
            print(f"FAIL {issue}")
        print(f"{'FAIL' if result['issues'] else 'OK  '} references: {entry} ({len(result['files'])} files read)")
    print(f"Reference audit: {len(entries)} entrypoints, {len(files)} unique files read, {'FAILED' if failed else 'passed'}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
