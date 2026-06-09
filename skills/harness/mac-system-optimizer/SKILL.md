---
name: mac-system-optimizer
description: Use when the user asks to optimize a Mac or local computer for performance, responsiveness, developer workflows, Claude/Codex agent sessions, shell startup, browser memory, login items, LaunchAgents, Docker/Homebrew/dev caches, or stale app leftovers. Follow a community-script style workflow: evidence-first diagnosis, explicit allow-lists, user confirmation before destructive changes, and verification after every change.
---

# Mac System Optimizer

## Core stance

Optimize from evidence, not vibes. Start with a read-only snapshot, rank bottlenecks by impact, then apply the smallest reversible change that improves responsiveness.

## Default workflow

1. Run a read-only diagnosis. Prefer `scripts/diagnose_macos.sh` when working on macOS.
2. Classify findings into CPU pressure, memory/swap pressure, browser pressure, startup/background pressure, shell startup, disk/cache pressure, and privacy/TCC blockers.
3. Present a ranked action list with expected benefit and risk.
4. Execute only the actions the user approves. Treat file deletion, app quitting, Docker prune, Chrome profile edits, TCC resets, LaunchAgent removal, and login-item changes as approval-required.
5. Verify with before/after measurements and report exact commands that ran.

## Safety rules

- Never delete user files, project folders, git repos, credentials, keychains, browser history/bookmarks/passwords, `.env` files, SSH/GPG keys, or application databases.
- Use explicit allow-lists for cleanup targets. Do not improvise broad `rm -rf` patterns.
- Prefer dry-run, listing, and exact object IDs before deletion.
- Preserve active Claude/Codex/terminal sessions unless the user explicitly asks to close them.
- Prefer graceful quit/unload over `kill -9`.
- For Docker, list resources first. Treat volumes and `docker system prune --volumes` as high-risk.
- For Chrome, back up `Local State`, `Preferences`, and `Secure Preferences` before editing profiles or extensions.

## Diagnostic checklist

- System: `sw_vers`, `uptime`, load average, Apple Silicon/Intel.
- Memory: `memory_pressure`, `vm_stat`, `sysctl vm.swapusage`.
- Processes: top CPU and RSS via `ps`; group app families such as Chrome, Codex, Claude, Slack, Docker, Electron apps.
- Startup: Login Items, `~/Library/LaunchAgents`, `/Library/LaunchAgents`, `/Library/LaunchDaemons`, failing `launchctl` jobs.
- Browser: Chrome process count, profile count, extension list, duplicate extension categories, Memory Saver state when discoverable.
- Shell: `zsh -lic` timing, `PATH` duplication, `brew shellenv`, heavy version managers, missing commands.
- Dev caches: npm/pnpm/yarn, pip, Cargo/Rustup, Go build, Xcode DerivedData, Docker build cache, Playwright/Puppeteer.
- Privacy blockers: macOS Documents/Desktop/Downloads access, Full Disk Access, Developer Tools, TCC prompts.

## Recommended actions by impact

1. Remove broken LaunchAgents and unused Login Items.
2. Close or disable high-idle CPU/RSS apps the user confirms are unnecessary.
3. Split browser profiles so developer extensions stay out of the daily profile.
4. Tune shell startup by replacing slow subshells with static PATH exports and lazy-loading version managers.
5. Reclaim disk only when space is tight or cache bloat is clearly wasteful.
6. Apply Docker cleanup conservatively: containers/images/build cache before volumes.

## References

Read `references/community-research.md` when shaping recommendations or extending this skill. It summarizes relevant GitHub/community skills and tools that informed this workflow.
