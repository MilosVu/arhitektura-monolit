# Skripte

Operativni helperi za lokalni razvoj i održavanje. **Nisu** deo runtime Python paketa.

| Skripta | Opis |
|---------|------|
| `dev.sh` | API + sync-worker + ingestion-worker + flower + web-client |
| `seed-neo4j.sh` | Seed law grafa (Cypher iz `infra/neo4j/`) |

Makefile (`make dev`, `make seed-neo4j`) ostaje primarni interfejs; skripte su alternativa ili za CI shell korak.
