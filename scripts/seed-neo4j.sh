#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Seeding Neo4j law nodes..."
docker compose -f infra/docker-compose.yml exec -T neo4j \
  cypher-shell -u neo4j -p cortex123 < infra/neo4j/seed.cypher
echo "Neo4j seed complete."
