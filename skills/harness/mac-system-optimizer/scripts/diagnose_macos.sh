#!/usr/bin/env bash
set -u

section() {
  printf '\n## %s\n' "$1"
}

run() {
  printf '+ %s\n' "$*"
  "$@" 2>&1 || true
}

section "System"
run sw_vers
run uname -a
run uptime
printf 'memory_bytes='
sysctl -n hw.memsize 2>/dev/null || true
printf 'swap='
sysctl -n vm.swapusage 2>/dev/null || true

section "Memory"
memory_pressure 2>/dev/null | sed -n '1,45p' || true
vm_stat 2>/dev/null | sed -n '1,30p' || true

section "Top CPU"
ps axo pid,ppid,stat,%cpu,%mem,rss,comm | sort -k4 -nr | head -25

section "Top RSS"
ps axo pid,ppid,stat,%cpu,%mem,rss,comm | sort -k6 -nr | head -35

section "App RSS Groups"
for pat in "Google Chrome" "Safari" "Codex" "Claude" "Docker" "Slack" "Spotify" "Discord" "Cursor" "Code" "Electron" "Raycast" "Maccy" "Snipaste"; do
  ps axo rss=,command= | awk -v pat="$pat" '
    index($0, pat) && $0 !~ /awk -v pat/ { rss += $1; n += 1 }
    END { if (n) printf "%-18s %3d procs %8.1f MB RSS\n", pat, n, rss / 1024 }
  '
done

section "Disk And Caches"
df -h / /System/Volumes/Data 2>/dev/null || df -h /
du -sh ~/.cache ~/.npm ~/.pnpm-store ~/.yarn ~/.bun ~/.cargo ~/.rustup ~/Library/Caches 2>/dev/null | sort -h

section "Login Items"
osascript -e 'tell application "System Events" to get the name of every login item' 2>/dev/null || true

section "Launch Files"
find ~/Library/LaunchAgents /Library/LaunchAgents /Library/LaunchDaemons -maxdepth 1 -type f \
  \( -name '*.plist' -o -name '*.disabled' \) -print 2>/dev/null | sort

section "Nonzero Launchctl Jobs"
launchctl list 2>/dev/null | awk 'NR == 1 || $2 != 0 {print}' | sed -n '1,80p'

section "Brew Services"
if command -v brew >/dev/null 2>&1; then
  brew services list 2>/dev/null || true
else
  echo "brew not found"
fi

section "Docker"
if command -v docker >/dev/null 2>&1; then
  docker ps -a 2>/dev/null || true
  docker system df 2>/dev/null || true
else
  echo "docker not found"
fi
pgrep -fl 'Docker|com.docker|containerd|dockerd' 2>/dev/null || true

section "Shell Startup"
if command -v zsh >/dev/null 2>&1; then
  /usr/bin/time -p zsh -lic '
    echo "fd=$(ulimit -n)"
    for c in brew codex claude node npm mise zoxide pyenv conda nvm; do
      r=$(whence -v $c 2>/dev/null || true)
      if [[ -z $r ]]; then print -r -- "$c missing"; else print -r -- "$c $r"; fi
    done
    exit
  '
fi

section "Chrome Profiles And Extensions"
if command -v node >/dev/null 2>&1; then
  node <<'NODE'
const fs = require("fs");
const path = require("path");
const chrome = path.join(process.env.HOME, "Library/Application Support/Google/Chrome");

function readJson(file) {
  try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return null; }
}

function resolveName(root, raw) {
  const match = String(raw || "").match(/^__MSG_(.+)__$/);
  if (!match) return raw || "";
  const key = match[1].toLowerCase();
  for (const loc of ["en", "en_US", "zh_CN", "zh", "zh_TW"]) {
    const messages = readJson(path.join(root, "_locales", loc, "messages.json"));
    if (!messages) continue;
    const found = Object.keys(messages).find((name) => name.toLowerCase() === key);
    if (found && messages[found].message) return messages[found].message;
  }
  return raw;
}

const securePrefs = new Map();
function extensionState(profile, id) {
  if (!securePrefs.has(profile)) {
    securePrefs.set(profile, readJson(path.join(chrome, profile, "Secure Preferences")) || {});
  }
  const settings = securePrefs.get(profile).extensions?.settings?.[id];
  if (!settings) return "unknown";
  const disabled = settings.state === 0 || (settings.disable_reasons || []).length > 0;
  return disabled ? "disabled" : "enabled";
}

const localState = readJson(path.join(chrome, "Local State"));
if (localState && localState.profile && localState.profile.info_cache) {
  for (const [dir, info] of Object.entries(localState.profile.info_cache)) {
    console.log(`profile\t${dir}\t${info.name || ""}`);
  }
}

function walk(dir, depth = 0) {
  if (depth > 5) return;
  let entries = [];
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, depth + 1);
    if (entry.isFile() && entry.name === "manifest.json" && full.includes("/Extensions/")) {
      const manifest = readJson(full);
      if (!manifest) continue;
      const parts = full.split("/Extensions/")[1].split("/");
      const profile = full.split("/Google/Chrome/")[1].split("/Extensions/")[0];
      console.log(`extension\t${profile}\t${extensionState(profile, parts[0])}\t${resolveName(path.dirname(full), manifest.name)}\t${parts[0]}\t${parts[1]}`);
    }
  }
}

walk(chrome);
NODE
else
  echo "node not found; skipping Chrome extension parse"
fi
