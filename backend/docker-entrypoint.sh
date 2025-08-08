#!/usr/bin/env bash
set -euo pipefail
cmd="${1:-api}"

case "$cmd" in
  dbinit)
    echo "[entrypoint] dbinit"
    python -m cli dbinit
    alembic upgrade head
    ;;
  api)
    echo "[entrypoint] api"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;
  *)
    exec "$@"
    ;;
esac
