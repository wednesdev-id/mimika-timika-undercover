#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR" && pwd)"

PNPM_BIN="$(command -v pnpm || true)"

print_header() { echo "[manage] $*"; }

require_pnpm() {
  if [[ -z "${PNPM_BIN}" ]]; then
    echo "pnpm tidak ditemukan. Install pnpm terlebih dulu."
    exit 1
  fi
}

usage() { cat <<'EOF'
Usage: manage.sh <command> [options]

Commands:
  install                         Install semua dependencies workspace
  port:check [-p PORT] [--auto-kill]
  port:kill  [-p PORT]
  dev timika|mimika [--auto-kill] [-p|--port PORT]
  dev:all [--auto-kill] [--timika-port PORT] [--mimika-port PORT]
  build timika|mimika|packages|all
  docker:build api|mimika|timika|all [--tag TAG]
  docker:run api|mimika|timika|all [--api-port PORT] [--mimika-port PORT] [--timika-port PORT]
  podman:build api|mimika|timika|all [--tag TAG]
  podman:run api|mimika|timika|all [--api-port PORT] [--mimika-port PORT] [--timika-port PORT]
  compose:build [--env-file FILE]
  compose:up [--env-file FILE]
  compose:down [--env-file FILE]
  compose:logs [--env-file FILE]
  info                            Info pnpm & daftar paket

Options:
  -p, --port PORT                 Port target (default: timika=5173, mimika=5174)
      --auto-kill                 Kill proses pada port yang terpakai
      --timika-port PORT          Port khusus untuk timika
      --mimika-port PORT          Port khusus untuk mimika
      --api-port PORT             Port khusus untuk api (default: 3001)
      --tag TAG                   Tag image container (default: latest)
      --env-file FILE             File env untuk docker compose (default: infra/compose/.env)

Contoh:
  ./manage.sh install
  ./manage.sh port:check --port 5173 --auto-kill
  ./manage.sh dev timika --auto-kill
  ./manage.sh dev:all --auto-kill
  ./manage.sh docker:build all --tag v0.1 && ./manage.sh docker:run all --api-port 3000 --mimika-port 8081 --timika-port 8080
  ./manage.sh compose:build --env-file infra/compose/.env && ./manage.sh compose:up --env-file infra/compose/.env
EOF
}

default_ports() { TIMIKA_PORT="${TIMIKA_PORT:-5173}"; MIMIKA_PORT="${MIMIKA_PORT:-5174}"; }

run_port_check() {
  local port="$1"; local auto="${2:-0}"
  print_header "Check port ${port} (AUTO_KILL=${auto})"
  (
    cd "$REPO_ROOT"
    AUTO_KILL="$auto" NO_PROMPT=1 "$REPO_ROOT/infra/scripts/check-port.sh" "$port"
  )
}

sub_dev() {
  local app="$1"; shift || true
  local auto=0
  local port=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --auto-kill) auto=1; shift ;;
      -p|--port) port="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  default_ports
  case "$app" in
    timika)
      port="${port:-$TIMIKA_PORT}"
      run_port_check "$port" "$auto"
      # Bersihkan port otomatis saat Ctrl+C
      trap 'print_header "SIGINT: cleanup port $port"; AUTO_KILL=1 NO_PROMPT=1 "$REPO_ROOT/infra/scripts/check-port.sh" "$port"; exit 130' INT
      print_header "Start dev web-timika"
      ( cd "$REPO_ROOT" && "$PNPM_BIN" run dev:web:timika )
      ;;
    mimika)
      port="${port:-$MIMIKA_PORT}"
      run_port_check "$port" "$auto"
      # Bersihkan port otomatis saat Ctrl+C
      trap 'print_header "SIGINT: cleanup port $port"; AUTO_KILL=1 NO_PROMPT=1 "$REPO_ROOT/infra/scripts/check-port.sh" "$port"; exit 130' INT
      print_header "Start dev web-mimika"
      ( cd "$REPO_ROOT" && "$PNPM_BIN" run dev:web:mimika )
      ;;
    *) echo "App tidak dikenal: $app"; usage; exit 1 ;;
  esac
}

sub_dev_all() {
  local auto=0
  local port_timika=""; local port_mimika=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --auto-kill) auto=1; shift ;;
      --timika-port) port_timika="$2"; shift 2 ;;
      --mimika-port) port_mimika="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  default_ports
  port_timika="${port_timika:-$TIMIKA_PORT}"
  port_mimika="${port_mimika:-$MIMIKA_PORT}"
  run_port_check "$port_timika" "$auto"
  run_port_check "$port_mimika" "$auto"
  print_header "Start dev timika & mimika"
  ( cd "$REPO_ROOT" && "$PNPM_BIN" run dev:web:timika ) &
  TIMIKA_PID=$!
  ( cd "$REPO_ROOT" && "$PNPM_BIN" run dev:web:mimika ) &
  MIMIKA_PID=$!
  print_header "PID timika=$TIMIKA_PID, mimika=$MIMIKA_PID"
  trap 'print_header "Stop dev"; kill "$TIMIKA_PID" "$MIMIKA_PID" 2>/dev/null || true; print_header "Cleanup ports"; AUTO_KILL=1 NO_PROMPT=1 "$REPO_ROOT/infra/scripts/check-port.sh" "$port_timika" "$port_mimika"; exit 130' INT TERM
  wait
}

sub_port_kill() {
  local port=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -p|--port) port="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  if [[ -z "$port" ]]; then echo "Harap set --port"; exit 1; fi
  print_header "Kill port ${port}"
  if command -v lsof >/dev/null 2>&1; then
    lsof -ti tcp:"$port" | xargs -r kill -9
  else
    echo "lsof tidak tersedia; gunakan port:check --auto-kill"
  fi
}

sub_install() { require_pnpm; ( cd "$REPO_ROOT" && "$PNPM_BIN" install ); }

sub_build() {
  local target="${1:-all}"
  require_pnpm
  case "$target" in
    timika) ( cd "$REPO_ROOT/apps/web-timika" && "$PNPM_BIN" run build ) ;;
    mimika) ( cd "$REPO_ROOT/apps/web-mimika" && "$PNPM_BIN" run build ) ;;
    packages) ( cd "$REPO_ROOT" && "$PNPM_BIN" --filter "./packages/**" run build || true ) ;;
    all) ( cd "$REPO_ROOT" && "$PNPM_BIN" run build || true ) ;;
    *) echo "Target build tidak dikenal: $target"; usage; exit 1 ;;
  esac
}

sub_info() {
  require_pnpm
  echo "Repo root: $REPO_ROOT"
  "$PNPM_BIN" --version
  ( cd "$REPO_ROOT" && "$PNPM_BIN" ls -r --depth 1 )
}

main() {
  [[ $# -lt 1 ]] && usage && exit 1
  case "$1" in
    install) shift; sub_install "$@" ;;
    port:check) shift;
      local port=""; local auto=0
      while [[ $# -gt 0 ]]; do
        case "$1" in
          -p|--port) port="$2"; shift 2 ;;
          --auto-kill) auto=1; shift ;;
          *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
        esac
      done
      if [[ -z "$port" ]]; then echo "Harap set --port"; exit 1; fi
      run_port_check "$port" "$auto"
      ;;
    port:kill) shift; sub_port_kill "$@" ;;
    dev) shift; sub_dev "$@" ;;
    dev:all) shift; sub_dev_all "$@" ;;
    build) shift; sub_build "$@" ;;
    docker:build) shift; docker_build "$@" ;;
    docker:run) shift; docker_run "$@" ;;
    podman:build) shift; podman_build "$@" ;;
    podman:run) shift; podman_run "$@" ;;
    compose:build) shift; compose_build "$@" ;;
    compose:up) shift; compose_up "$@" ;;
    compose:down) shift; compose_down "$@" ;;
    compose:logs) shift; compose_logs "$@" ;;
    info) shift; sub_info "$@" ;;
    *) echo "Perintah tidak dikenal: $1"; usage; exit 1 ;;
  esac
}
main "$@"
docker_build() {
  local target="$1"; shift || true
  local tag="latest"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --tag) tag="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  case "$target" in
    api)
      docker build -t undercover-api:"$tag" -f infra/docker/Dockerfile.api . ;;
    mimika)
      docker build -t undercover-web-mimika:"$tag" -f infra/docker/Dockerfile.web-mimika . ;;
    timika)
      docker build -t undercover-web-timika:"$tag" -f infra/docker/Dockerfile.web-timika . ;;
    all)
      docker_build api --tag "$tag" && docker_build mimika --tag "$tag" && docker_build timika --tag "$tag" ;;
    *) echo "Target docker tidak dikenal: $target"; usage; exit 1 ;;
  esac
}

docker_run() {
  local target="$1"; shift || true
  local api_port="3000"; local mimika_port="8081"; local timika_port="8080"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --api-port) api_port="$2"; shift 2 ;;
      --mimika-port) mimika_port="$2"; shift 2 ;;
      --timika-port) timika_port="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  docker network inspect undercover-net >/dev/null 2>&1 || docker network create undercover-net
  case "$target" in
    api)
      docker rm -f undercover-api >/dev/null 2>&1 || true
      docker run -d --name undercover-api --network undercover-net -p "$api_port":3000 undercover-api:latest ;;
    mimika)
      docker rm -f undercover-web-mimika >/dev/null 2>&1 || true
      docker run -d --name undercover-web-mimika --network undercover-net -p "$mimika_port":80 undercover-web-mimika:latest ;;
    timika)
      docker rm -f undercover-web-timika >/dev/null 2>&1 || true
      docker run -d --name undercover-web-timika --network undercover-net -p "$timika_port":80 undercover-web-timika:latest ;;
    all)
      docker_run api --api-port "$api_port"
      docker_run mimika --mimika-port "$mimika_port"
      docker_run timika --timika-port "$timika_port" ;;
    *) echo "Target docker tidak dikenal: $target"; usage; exit 1 ;;
  esac
}

podman_build() {
  local target="$1"; shift || true
  local tag="latest"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --tag) tag="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  case "$target" in
    api)
      podman build -t undercover-api:"$tag" -f infra/docker/Dockerfile.api . ;;
    mimika)
      podman build -t undercover-web-mimika:"$tag" -f infra/docker/Dockerfile.web-mimika . ;;
    timika)
      podman build -t undercover-web-timika:"$tag" -f infra/docker/Dockerfile.web-timika . ;;
    all)
      podman_build api --tag "$tag" && podman_build mimika --tag "$tag" && podman_build timika --tag "$tag" ;;
    *) echo "Target podman tidak dikenal: $target"; usage; exit 1 ;;
  esac
}

podman_run() {
  local target="$1"; shift || true
  local api_port="3000"; local mimika_port="8081"; local timika_port="8080"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --api-port) api_port="$2"; shift 2 ;;
      --mimika-port) mimika_port="$2"; shift 2 ;;
      --timika-port) timika_port="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  podman network inspect undercover-net >/dev/null 2>&1 || podman network create undercover-net
  case "$target" in
    api)
      podman rm -f undercover-api >/dev/null 2>&1 || true
      podman run -d --name undercover-api --network undercover-net -p "$api_port":3000 undercover-api:latest ;;
    mimika)
      podman rm -f undercover-web-mimika >/dev/null 2>&1 || true
      podman run -d --name undercover-web-mimika --network undercover-net -p "$mimika_port":80 undercover-web-mimika:latest ;;
    timika)
      podman rm -f undercover-web-timika >/dev/null 2>&1 || true
      podman run -d --name undercover-web-timika --network undercover-net -p "$timika_port":80 undercover-web-timika:latest ;;
    all)
      podman_run api --api-port "$api_port"
      podman_run mimika --mimika-port "$mimika_port"
      podman_run timika --timika-port "$timika_port" ;;
    *) echo "Target podman tidak dikenal: $target"; usage; exit 1 ;;
  esac
}

compose_env_file_default() { COMPOSE_ENV_FILE="${COMPOSE_ENV_FILE:-infra/compose/.env}"; }

compose_build() {
  local env_file=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env-file) env_file="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  compose_env_file_default
  env_file="${env_file:-$COMPOSE_ENV_FILE}"
  print_header "Compose build (env=$env_file)"
  docker compose --env-file "$env_file" -f infra/compose/docker-compose.yml build
}

compose_up() {
  local env_file=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env-file) env_file="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  compose_env_file_default
  env_file="${env_file:-$COMPOSE_ENV_FILE}"
  print_header "Compose up (env=$env_file)"
  docker compose --env-file "$env_file" -f infra/compose/docker-compose.yml up -d
}

compose_down() {
  local env_file=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env-file) env_file="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  compose_env_file_default
  env_file="${env_file:-$COMPOSE_ENV_FILE}"
  print_header "Compose down (env=$env_file)"
  docker compose --env-file "$env_file" -f infra/compose/docker-compose.yml down
}

compose_logs() {
  local env_file=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env-file) env_file="$2"; shift 2 ;;
      *) echo "Argumen tidak dikenal: $1"; usage; exit 1 ;;
    esac
  done
  compose_env_file_default
  env_file="${env_file:-$COMPOSE_ENV_FILE}"
  print_header "Compose logs (env=$env_file)"
  docker compose --env-file "$env_file" -f infra/compose/docker-compose.yml logs --tail=100
}
