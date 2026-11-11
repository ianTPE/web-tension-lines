#!/usr/bin/env bash
# 每週：抓上游 modern-web-guidance，有新 commit 就叫 claude 照 PROMPT.md 拆成問題線。
# crontab: 0 9 * * 3  /path/to/web-tension-lines/scripts/weekly.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

mkdir -p .cache logs
LOG="logs/$(date +%F).log"
exec >>"$LOG" 2>&1
echo "=== $(date -Is) start"

UP=.cache/upstream
if [ -d "$UP/.git" ]; then
  git -C "$UP" fetch -q origin main && git -C "$UP" reset -q --hard origin/main
else
  git clone -q https://github.com/GoogleChrome/modern-web-guidance.git "$UP"
fi

FROM=$(python3 -c 'import json;print(json.load(open("state.json"))["last_commit"])')
TO=$(git -C "$UP" rev-parse --short HEAD)
if [ "$FROM" = "$TO" ]; then
  echo "no upstream change ($TO)"; exit 0
fi

git -C "$UP" diff --name-status "$FROM" "$TO" -- skills/modern-web-guidance/guides > .cache/diff.txt
if [ ! -s .cache/diff.txt ]; then
  echo "upstream moved $FROM..$TO but no guide changed"
  python3 - "$TO" <<'EOF'
import json,sys,datetime
s=json.load(open("state.json")); s["last_commit"]=sys.argv[1]; s["last_run"]=datetime.date.today().isoformat()
json.dump(s,open("state.json","w"),ensure_ascii=False,indent=2)
EOF
  exit 0
fi

export MWG_FROM="$FROM" MWG_TO="$TO"
export MWG_RELEASE="$(git -C "$UP" log -1 --format=%s "$TO" | sed 's/^Release //')"
echo "diff $FROM..$TO ($MWG_RELEASE): $(wc -l < .cache/diff.txt) files"

claude -p "$(cat PROMPT.md)

本次：MWG_FROM=$MWG_FROM MWG_TO=$MWG_TO MWG_RELEASE=$MWG_RELEASE 今天=$(date +%F)" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(git -C .cache/upstream:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(wc:*)" \
  --max-turns 200

NOW=$(python3 -c 'import json;print(json.load(open("state.json"))["last_commit"])')
if [ "$NOW" != "$TO" ]; then
  echo "WARN: run finished but state.json not advanced (still $NOW)"; exit 1
fi

python3 scripts/build_page.py && python3 scripts/build_weekly.py
git add -A lines ledger.csv weekly state.json docs i18n
if ! git diff --cached --quiet; then
  git commit -q -m "weekly: modern-web-guidance $MWG_RELEASE ($MWG_FROM..$MWG_TO)"
  git push -q origin main || echo "WARN: push failed"
fi
echo "=== $(date -Is) done"
