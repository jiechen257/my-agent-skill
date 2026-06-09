#!/usr/bin/env bash
set -euo pipefail

echo "## codex binary"
if command -v codex >/dev/null 2>&1; then
  command -v codex
  codex --version || true
else
  echo "codex not found on PATH"
fi

echo
echo "## common install paths"
for path in \
  "$HOME/.bun/bin/codex" \
  "$HOME/.bun/install/global/node_modules/@openai/codex/package.json" \
  "$HOME/.bun/install/global/node_modules/@openai/codex-darwin-arm64/package.json" \
  "/Applications/Codex.app/Contents/Info.plist"
do
  if [ -e "$path" ]; then
    echo "$path"
  fi
done

echo
echo "## app bundle version"
if [ -e "/Applications/Codex.app/Contents/Info.plist" ]; then
  /usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "/Applications/Codex.app/Contents/Info.plist" 2>/dev/null || true
fi

echo
echo "## bun global codex packages"
if command -v bun >/dev/null 2>&1; then
  bun pm ls -g 2>/dev/null | grep -E '@openai/codex|codex' || true
else
  echo "bun not found on PATH"
fi

echo
echo "## proxy env names"
env | grep -E '^(HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|http_proxy|https_proxy|all_proxy|npm_config_proxy|npm_config_https_proxy)=' | sed -E 's/=.*/=<set>/' || true

echo
echo "## codex-related processes"
ps aux | grep -Ei 'Codex|codex|Proxifier|Clash|clash|mihomo' | grep -v grep || true

echo
echo "## recent log candidates"
{
  find "$HOME/Library/Logs" "$HOME/Library/Application Support/Codex" "$HOME/.codex" \
    -maxdepth 5 \
    \( -iname '*codex*log*' -o -path '*Codex*/*.log' -o -path '*codex*/*.log' \) \
    -type f \
    -mtime -7 \
    2>/dev/null || true
} | sed -n '1,80p'
