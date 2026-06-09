# Community Research

This skill is modeled on community macOS cleanup and agent-workstation optimization workflows rather than generic OS documentation.

## Reviewed sources

- ForgeKit `mac-optimize`: focuses on Claude Code / Codex workstation resource pressure, including load average, swap, zombie agent processes, Node heap caps, LaunchAgent audits, Spotlight pruning, and explicit "do not" rules. Source: https://forgekit.lucassantana.tech/skills/mac-optimize/ and https://github.com/LucasSantana-Dev/forgekit
- daymade `macos-cleaner`: uses a safety-first disk cleanup workflow with staged analysis, Mole integration, exact object listing, and confirmation before deletion. Source: https://skills.sh/daymade/claude-code-skills/macos-cleaner and https://github.com/daymade/claude-code-skills
- `dancolta/claude-cleanup-skill`: demonstrates an explicit allow-list cleanup model for macOS caches across package managers, editors, browsers, chat apps, Docker, and system logs while excluding user files, configs, credentials, git repos, and `node_modules`. Source: https://github.com/dancolta/claude-cleanup-skill
- `tw93/Mole`: mature open-source Mac cleanup/optimization tool. Useful patterns: dry-run support, safety-first defaults, protected-directory rules, operation logs, app-leftover cleanup, and system monitoring. Source: https://github.com/tw93/Mole
- `bysiber/cleardisk`: developer-cache-focused Mac tool. Useful patterns: cache categories, visual size breakdown, preview before cleaning, local-only/privacy-first execution. Source: https://github.com/bysiber/cleardisk and https://bysiber.github.io/cleardisk/
- Reddit/devtools thread for `claude-cleanup-skill`: reinforces the allow-list pattern, full coverage of real developer tools, and the effect of parallel agent workflows on cache growth. Source: https://www.reddit.com/r/devtools/comments/1s1lumf/open_sourced_a_claude_code_cleanup_skill_for/

## Design lessons

- The best skills separate diagnosis from cleanup. A one-shot cleanup command creates trust problems; a measured report with exact targets is easier to approve.
- Performance optimization and disk cleanup are related but distinct. CPU, memory, browser processes, shell startup, and login items often matter more than caches.
- Developer machines need cache nuance. npm/pnpm, Docker, Playwright, Xcode, Cargo, Go, and Homebrew caches can be useful; clean them when there is pressure or obvious waste.
- Browser optimization should handle extension sets and profiles, not only tab count. Developer extensions belong in a development profile when they are not needed daily.
- Agent-heavy machines need special checks for stale Claude/Codex processes, high load before parallel work, and Node/V8 memory growth.
- Safe cleanup skills use allow-lists, exact paths, dry-runs, and confirmation gates. They avoid broad matching and never touch user data.

## Recommended local policy

- Default to read-only diagnosis.
- Ask before quitting apps, removing login items, unloading LaunchAgents, changing Chrome profiles, pruning Docker, deleting caches, or resetting macOS privacy decisions.
- For repeated user-approved actions, keep a small reusable script and make it visibly read-only unless its name and prompt clearly say it mutates state.
- After every optimization, rerun the relevant measurement and report the delta.
