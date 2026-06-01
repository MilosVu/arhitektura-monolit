# Cortex AI — Documentation

Central entry point for all monolith repository documentation.

## Where to go

| I am… | Start here |
|-------|------------|
| **PM / product owner** | [product/README.md](product/README.md) |
| **User / customer success** | [product/README.md](product/README.md) → user guide (coming soon) |
| **New developer on the team** | [engineering/README.md](engineering/README.md) |
| **Dev implementing a feature** | [engineering/how-we-work/feature-placement.md](engineering/how-we-work/feature-placement.md) |
| **Architect / tech lead** | [engineering/decisions/README.md](engineering/decisions/README.md) |
| **AI assistant (Cursor)** | [AGENTS.md](../AGENTS.md) in the repo root |

## Layout

```
docs/
├── README.md              ← this file
├── product/               ← external docs (PM, users, ops — no implementation detail)
└── engineering/           ← internal docs (dev team, architecture, decisions)
    ├── architecture/
    ├── decisions/         ← ADR — architectural decisions and trade-offs
    ├── how-we-work/
    └── reference/
```

**Rule:** if a PM needs to understand *what* the system does → `product/`. If a dev needs to know *where and how* to write code → `engineering/`.
