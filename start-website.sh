#!/usr/bin/env bash
set -euo pipefail

# Simple starter script for AI-Career-Navigator (dev)
# - starts backend (venv) and frontend (Vite)
# - prints accessible URLs and log locations

ROOT="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$ROOT/tmp"

echo "Starting AI Career Navigator (dev)..."

# Backend
echo "-> Backend: setting up and starting"
cd "$ROOT/app/backend"
if [ ! -d venv ]; then
  echo "Creating virtualenv..."
  python3 -m venv venv
  ./venv/bin/python -m pip install --upgrade pip setuptools wheel
  ./venv/bin/python -m pip install -r requirements.txt
fi
nohup ./venv/bin/python app.py > "$ROOT/tmp/backend.log" 2>&1 &
echo $! > "$ROOT/tmp/backend.pid"

# Wait for backend to respond (max ~30s)
echo -n "Waiting for backend at http://127.0.0.1:8000/health"
for i in {1..30}; do
  if curl -sS http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo " — ready"
    break
  fi
  echo -n "."
  sleep 1
done

# Frontend
echo "-> Frontend: installing (if needed) and starting"
cd "$ROOT/app/frontend"
if [ ! -d node_modules ]; then
  npm install --no-audit --no-fund
fi
nohup npm run dev -- --host 127.0.0.1 > "$ROOT/tmp/frontend.log" 2>&1 &
echo $! > "$ROOT/tmp/frontend.pid"

echo
echo "Frontend: http://127.0.0.1:5173/"
echo "Backend:  http://127.0.0.1:8000/"
echo
echo "Logs: $ROOT/tmp/frontend.log  $ROOT/tmp/backend.log"
echo "PIDs: $(cat "$ROOT/tmp/frontend.pid" 2>/dev/null || echo -) (frontend), $(cat "$ROOT/tmp/backend.pid" 2>/dev/null || echo -) (backend)"

exit 0
