#!/usr/bin/env bash
# Google Fonts에서 렌더링용 폰트(TTF)를 내려받는다. local.css는 이 파일명들을 가리킨다.
set -euo pipefail
cd "$(dirname "$0")/fonts"
curl -sS -A "Mozilla/4.0" "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;900&family=Noto+Serif+KR:wght@900&family=JetBrains+Mono:wght@300;500&display=swap" \
  | grep -oE "https://[^)]+\.ttf" | while read -r u; do [ -f "$(basename "$u")" ] || curl -sS -O "$u"; done
