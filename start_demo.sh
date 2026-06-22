#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

if command -v python3 >/dev/null 2>&1; then
  python_command=python3
elif command -v python >/dev/null 2>&1; then
  python_command=python
else
  echo "Launch failed: Python was not found." >&2
  exit 1
fi

url="http://localhost:8600/"
echo "Starting prototype at ${url}"
echo "Press Ctrl+C to stop the server."

if command -v xdg-open >/dev/null 2>&1; then
  (sleep 2 && xdg-open "${url}" >/dev/null 2>&1) &
fi

exec "${python_command}" -m http.server 8600 --bind 127.0.0.1
