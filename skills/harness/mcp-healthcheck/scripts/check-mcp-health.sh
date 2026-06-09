#!/usr/bin/env bash
set -euo pipefail

CONFIG=${CODEX_CONFIG:-"$HOME/.codex/config.toml"}
TIMEOUT=${MCP_HEALTHCHECK_TIMEOUT:-8}

if [ ! -f "$CONFIG" ]; then
  printf 'ERROR config missing: %s\n' "$CONFIG" >&2
  exit 1
fi

json_body='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"codex-mcp-healthcheck","version":"0"}}}'

section_pairs() {
  awk '
    /^\[mcp_servers\.[^.]+\]$/ {
      section=$0
      sub(/^\[mcp_servers\./, "", section)
      sub(/\]$/, "", section)
      next
    }
    /^\[/ { section=""; next }
    section != "" {
      n=split($0, parts, "\"")
      for (i = 2; i <= n; i += 2) {
        if (parts[i] ~ /^https?:\/\//) {
          print section "|" parts[i]
        }
      }
    }
  ' "$CONFIG" | sort -u
}

command_pairs() {
  awk '
    /^\[mcp_servers\.[^.]+\]$/ {
      section=$0
      sub(/^\[mcp_servers\./, "", section)
      sub(/\]$/, "", section)
      next
    }
    /^\[/ { section=""; next }
    section != "" && /^[[:space:]]*command[[:space:]]*=/ {
      n=split($0, parts, "\"")
      if (n >= 3) print section "|" parts[2]
    }
  ' "$CONFIG" | sort -u
}

curl_status() {
  local mode=$1
  local url=$2

  if [ "$mode" = "head" ]; then
    curl -sS -I --max-time "$TIMEOUT" -o /dev/null -w '%{http_code} %{content_type} %{time_total}s' "$url" 2>/dev/null || printf '000 curl-error timeout=%ss' "$TIMEOUT"
    return
  fi

  curl -sS --max-time "$TIMEOUT" -o /dev/null -w '%{http_code} %{content_type} %{time_total}s' \
    -H 'accept: application/json, text/event-stream' \
    -H 'content-type: application/json' \
    -d "$json_body" \
    "$url" 2>/dev/null || printf '000 curl-error timeout=%ss' "$TIMEOUT"
}

no_proxy_status() {
  local mode=$1
  local url=$2

  if [ "$mode" = "head" ]; then
    /usr/bin/env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy -u npm_config_proxy -u npm_config_https_proxy \
      curl -sS -I --max-time "$TIMEOUT" -o /dev/null -w '%{http_code} %{content_type} %{time_total}s' "$url" 2>/dev/null || printf '000 curl-error timeout=%ss' "$TIMEOUT"
    return
  fi

  /usr/bin/env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy -u npm_config_proxy -u npm_config_https_proxy \
    curl -sS --max-time "$TIMEOUT" -o /dev/null -w '%{http_code} %{content_type} %{time_total}s' \
      -H 'accept: application/json, text/event-stream' \
      -H 'content-type: application/json' \
      -d "$json_body" \
      "$url" 2>/dev/null || printf '000 curl-error timeout=%ss' "$TIMEOUT"
}

printf '## MCP config\n%s\n\n' "$CONFIG"

printf '## Stdio command availability\n'
if ! command_pairs | grep -q .; then
  printf 'No stdio command entries found.\n'
else
  command_pairs | while IFS='|' read -r name command_name; do
    if [[ "$command_name" = /* ]]; then
      if [ -x "$command_name" ]; then
        printf 'OK   %-28s %s\n' "$name" "$command_name"
      elif [ -e "$command_name" ]; then
        printf 'WARN %-28s exists but is not executable: %s\n' "$name" "$command_name"
      else
        printf 'FAIL %-28s missing: %s\n' "$name" "$command_name"
      fi
    elif command -v "$command_name" >/dev/null 2>&1; then
      printf 'OK   %-28s %s -> %s\n' "$name" "$command_name" "$(command -v "$command_name")"
    else
      printf 'FAIL %-28s command not found: %s\n' "$name" "$command_name"
    fi
  done
fi

printf '\n## Remote endpoint probes\n'
if ! section_pairs | grep -q .; then
  printf 'No remote endpoint URLs found.\n'
else
  section_pairs | while IFS='|' read -r name endpoint; do
    printf '%s %s\n' "$name" "$endpoint"
    printf '  current HEAD       %s\n' "$(curl_status head "$endpoint")"
    printf '  current initialize %s\n' "$(curl_status post "$endpoint")"
    if [[ "$endpoint" == *"mcp.alibaba-inc.com"* ]]; then
      printf '  no-proxy HEAD      %s\n' "$(no_proxy_status head "$endpoint")"
      printf '  no-proxy init      %s\n' "$(no_proxy_status post "$endpoint")"
    fi
  done
fi

printf '\n## Notes\n'
printf '401 usually means auth-required but reachable. 405 usually means endpoint reachable but method unsupported.\n'
printf 'Headers, env values, and tokens are intentionally not printed.\n'
