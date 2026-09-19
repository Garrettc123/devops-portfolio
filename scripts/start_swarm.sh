#!/bin/bash
set -euo pipefail
echo "===================================="
echo " Zero-Human Enterprise Grid — Swarm"
echo " Starting Phase 1 Agent Swarm..."
echo "===================================="
docker compose -f docker/docker-compose.agents.yml up --build -d
echo ""
echo "[OK] Swarm online."
docker compose -f docker/docker-compose.agents.yml ps
echo ""
echo "API:    http://localhost:8000"
echo "Health: http://localhost:8000/health"
echo "Docs:   http://localhost:8000/docs"
