# ADR 0007: DMS-agnostic module name (`module-dms-sync`)

- **Status:** accepted
- **Date:** 2025
- **Author(s):** architecture team

## Context

The sync module was named `module-alfresco`, coupling the package name to one document management system. The product may integrate other DMS backends or abstract Alfresco behind a port.

## Options

### Option A — Rename to `module-dms-sync`

Generic name; Alfresco implementation lives in `cortex-connectors`.

- **Pros:** Accurate domain language, easier future DMS swap.
- **Cons:** One-time rename cost (imports, K8s, docs).

### Option B — Keep `module-alfresco`

- **Pros:** No rename.
- **Cons:** Misleading name if another DMS is added.

## Decision

Rename **`module-alfresco` → `module-dms-sync`**. Alfresco-specific code moves to **`cortex-connectors`** (`AlfrescoPort` adapter).

## Consequences

- Celery tasks live under `module_dms_sync.tasks`.
- Import-linter contract uses `module-dms-sync` package name.
- Do not reintroduce `module-alfresco` or a single combined worker name.

## References

- [reference/comparison-project-2.md](../reference/comparison-project-2.md)
