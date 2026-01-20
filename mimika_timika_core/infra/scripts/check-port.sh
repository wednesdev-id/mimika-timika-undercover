#!/usr/bin/env bash
set -euo pipefail

# Cek dan (opsional) kill proses yang menggunakan port
# Penggunaan: ./infra/scripts/check-port.sh 3000 5173 5174 6379
# Non-interaktif:
#   NO_PROMPT=1 ./infra/scripts/check-port.sh 3000 5173
# Auto-kill tanpa prompt:
#   AUTO_KILL=1 NO_PROMPT=1 ./infra/scripts/check-port.sh 3000 5173

# Default environment flags jika tidak di-set
AUTO_KILL=${AUTO_KILL:-false}
NO_PROMPT=${NO_PROMPT:-false}

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <port1> [port2 ...]"
  exit 1
fi

check_port() {
  local PORT=$1
  local PIDS
  PIDS=$(lsof -ti tcp:"$PORT" || true)
  if [ -z "$PIDS" ]; then
    echo "[OK] Port $PORT kosong"
  else
    echo "[BUSY] Port $PORT digunakan oleh PID: $PIDS"
    if [[ "$AUTO_KILL" == "true" || "$AUTO_KILL" == "1" ]]; then
      echo "[AUTO] Menghentikan proses: $PIDS"
      kill -9 $PIDS || true
      sleep 1
      local CHECK
      CHECK=$(lsof -ti tcp:"$PORT" || true)
      if [ -z "$CHECK" ]; then
        echo "[OK] Port $PORT sekarang kosong"
      else
        echo "[WARN] Masih ada proses di port $PORT: $CHECK"
      fi
    else
      if [[ "$NO_PROMPT" == "true" || "$NO_PROMPT" == "1" ]]; then
        echo "[INFO] Mode tanpa prompt: tidak melakukan kill otomatis."
      else
        read -p "Ingin kill proses pada port $PORT? (y/N): " ans
        ans=${ans:-N}
        if [[ "$ans" =~ ^[yY]$ ]]; then
          echo "Menghentikan proses: $PIDS"
          kill -9 $PIDS || true
          sleep 1
          local CHECK
          CHECK=$(lsof -ti tcp:"$PORT" || true)
          if [ -z "$CHECK" ]; then
            echo "[OK] Port $PORT sekarang kosong"
          else
            echo "[WARN] Masih ada proses di port $PORT: $CHECK"
          fi
        fi
      fi
    fi
  fi
}

for p in "$@"; do
  check_port "$p"
done

echo "Selesai cek port."