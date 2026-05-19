#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
REGISTRY="$ROOT/registry/skills.yaml"

list_skills() {
  awk '
    function emit() {
      if (name != "") {
        print name "|" path "|" kind "|" source_type "|" source_path "|" source_url "|" source_ref "|" source_subdir
      }
    }
    /^[[:space:]]*-[[:space:]]name:/ {
      emit()
      name=$3
      path=kind=source_type=source_path=source_url=source_ref=source_subdir=""
      next
    }
    /^[[:space:]]*path:/ { path=$2; next }
    /^[[:space:]]*kind:/ { kind=$2; next }
    /^[[:space:]]*source_type:/ { source_type=$2; next }
    /^[[:space:]]*source_path:/ { source_path=$2; next }
    /^[[:space:]]*source_url:/ { source_url=$2; next }
    /^[[:space:]]*source_ref:/ { source_ref=$2; next }
    /^[[:space:]]*source_subdir:/ { source_subdir=$2; next }
    END { emit() }
  ' "$REGISTRY"
}

want_skill() {
  local name=$1
  if [ "$#" -eq 1 ]; then
    return 0
  fi
  shift
  local wanted
  for wanted in "$@"; do
    [ "$wanted" = "$name" ] && return 0
  done
  return 1
}

assert_repo_target() {
  local target=$1
  case "$target/" in
    "$ROOT"/*) return 0 ;;
    *) printf 'Refusing to sync outside repo: %s\n' "$target" >&2; return 1 ;;
  esac
}

sync_local_copy() {
  local name=$1
  local source=$2
  local target=$3

  if [ ! -d "$source" ]; then
    printf 'ERROR %-28s source missing: %s\n' "$name" "$source" >&2
    return 1
  fi
  mkdir -p "$target"
  rsync -a --delete --exclude '.git' "$source/" "$target/"
  printf 'SYNC  %-28s local-copy %s -> %s\n' "$name" "$source" "$target"
}

sync_git() {
  local name=$1
  local url=$2
  local ref=$3
  local subdir=$4
  local target=$5
  local tmp

  tmp=$(mktemp -d "/tmp/${name}.sync.XXXXXX")
  git clone --depth 1 --branch "$ref" --filter=blob:none --sparse "$url" "$tmp/repo" >/dev/null
  git -C "$tmp/repo" sparse-checkout set "$subdir" >/dev/null
  while IFS= read -r -d '' link; do
    local link_target
    link_target=$(readlink "$link")
    case "$link_target" in
      /*) continue ;;
    esac
    local target_path
    target_path=$(cd -- "$(dirname -- "$link")" && printf '%s/%s\n' "$PWD" "$link_target")
    case "$target_path/" in
      "$tmp/repo"/*)
        git -C "$tmp/repo" sparse-checkout add "${target_path#"$tmp/repo/"}" >/dev/null
        ;;
    esac
  done < <(find "$tmp/repo/$subdir" -type l -print0)
  if [ ! -d "$tmp/repo/$subdir" ]; then
    printf 'ERROR %-28s source_subdir missing: %s\n' "$name" "$subdir" >&2
    return 1
  fi
  mkdir -p "$target"
  rsync -aL --delete --exclude '.git' "$tmp/repo/$subdir/" "$target/"
  local head
  head=$(git -C "$tmp/repo" rev-parse HEAD)
  printf 'SYNC  %-28s git %s %s -> %s\n' "$name" "$url" "$head" "$target"
  rm -rf "$tmp"
}

status=0
while IFS='|' read -r name path kind source_type source_path source_url source_ref source_subdir; do
  [ -n "$name" ] || continue
  [ "$kind" = "vendored" ] || continue
  want_skill "$name" "$@" || continue

  target="$ROOT/$path"
  assert_repo_target "$target" || { status=1; continue; }

  case "$source_type" in
    local)
      printf 'SKIP  %-28s local source\n' "$name"
      ;;
    local-copy)
      sync_local_copy "$name" "$source_path" "$target" || status=1
      ;;
    git)
      sync_git "$name" "$source_url" "${source_ref:-main}" "$source_subdir" "$target" || status=1
      ;;
    *)
      printf 'ERROR %-28s unknown source_type: %s\n' "$name" "$source_type" >&2
      status=1
      ;;
  esac
done < <(list_skills)

exit "$status"
