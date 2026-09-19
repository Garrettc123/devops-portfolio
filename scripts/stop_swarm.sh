#!/bin/bash
# Global Pause — Upgrade SOP Step 1
set -euo pipefail
echo "==================================="
echo " GLOBAL PAUSE — Upgrade SOP Step 1"
echo "==================================="
echo "[1/3] Stopping all containers..."
docker compose -f docker/docker-compose.agents.yml stop
echo "[2/3] Caching Redis state..."
mkdir -p backups
docker exec swarm-redis redis-cli BGSAVE && sleep 2
docker cp swarm-redis:/data/dump.rdb "backups/redis-$(date +%Y%m%d-%H%M%S).rdb" 2>/dev/null || echo "Redis backup skipped."
echo "[3/3] Removing containers..."
docker compose -f docker/docker-compose.agents.yml down
echo "[OK] Swarm stopped. Safe to upgrade."
