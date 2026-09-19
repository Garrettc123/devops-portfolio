#!/bin/bash
echo "=== Swarm Health ==="
curl -s http://localhost:8000/health | python3 -m json.tool
