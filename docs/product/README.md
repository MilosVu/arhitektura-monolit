# Cortex AI — Product Documentation

Documentation for **external users**, product owners, customer success, and operations teams.

This section describes **what Cortex does**, how to use it, and how to operate it — without implementation details (import paths, modules, Celery task names).

## Planned structure

| Folder | Content | Status |
|--------|---------|--------|
| `overview/` | Product value, main flows, user roles | Coming soon |
| `features/` | By domain: cases, documents, chat, sync, AI | Coming soon |
| `integrations/` | Alfresco, AD/SSO, Weaviate, Neo4j (business perspective) | Coming soon |
| `user-guide/` | How to use the web UI | Coming soon |
| `operations/` | Deploy, monitoring, backup (no code) | Coming soon |

## For developers

Technical documentation lives in [engineering/](../engineering/README.md).

## How to write product docs

- Plain language; no code citations or `make` commands.
- Focus on system behavior and user flows.
- Implementation decisions belong in [engineering/decisions/](../engineering/decisions/README.md) (ADR), not here.
