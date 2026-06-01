# Cortex AI Modularni Monolit - Pregled Arhitekture

Ovaj dokument opisuje kako je monolit organizovan po paketima, koji je plan razvoja `cortex-core` biblioteke i kako ce se sistem postepeno pripremati za izdvajanje novih biblioteka i nezavisnih servisa.

> Plan refactora (big-bang): [REFACTOR-PLAN.md](REFACTOR-PLAN.md)  
> Onboarding tima: [docs/onboarding/README.md](docs/onboarding/README.md)

## 1) Visok nivo arhitekture (ciljna produkcija)

Tok zahteva i podataka:

1. `web-client` ide kroz edge sloj (WAF → LB → Rate Limiter) i auth (SSO → JWT).
2. `cortex-server` montira routove svih HTTP modula: platform, documents, chat, sync, ai.
3. `sync-worker` podize `module-dms-sync`, `ingestion-worker` podize `module-ingestion`.
4. Svi moduli dele `cortex-core`, `cortex-models`, `cortex-connectors`.
5. `module-documents` je jedini vlasnik `Document.status` (lifecycle metode).
6. `module-sync` drzi `SyncOrchestrator` i enqueue-uje sync task.
7. `module-dms-sync` vuče delta iz Alfresco, koristi `DocumentsModule` za metadata, Blob za fajlove.
8. `module-ingestion` radi OCR → chunk → embed → Weaviate preko `SearchPort`.
9. `module-ai` koristi LangGraph agente (RAG, NER, Laws, NLP) i cita iz Weaviate-a.
10. `module-chat` persistuje thread-ove u Redis-u; AI generise stream.

## 2) Podela paketa na pocetku aplikacije

### Aplikacioni shell sloj

- `apps/cortex-server`
  - Composition root: podize FastAPI app, ukljucuje rout-ove i middleware.
  - Treba da ostane tanak orchestration sloj bez domenske logike.
- `apps/sync-worker` i `apps/ingestion-worker`
  - Odvojeni Celery deployable-i (I/O vs CPU/GPU profil).
  - Domenska logika u `module-dms-sync` i `module-ingestion`.

### Domen/feature moduli

- `packages/module-platform` — auth, cases, audit, system
- `packages/module-documents` — Document CRUD + lifecycle (jedini menja status)
- `packages/module-chat` — chat threads, Redis persistence
- `packages/module-sync` — SyncOrchestrator, job trigger/polling
- `packages/module-dms-sync` — DMS delta sync → Blob + PG (bivši alfresco)
- `packages/module-ingestion` — OCR/chunk/embed pipeline, Weaviate write
- `packages/module-ai` — LangGraph agenti (rag, legal, nlp podfolderi)

### Deljeni lib sloj

- `libs/cortex-core` — ports (SearchPort, AlfrescoPort, OCRPort, LLM), celery, settings
- `libs/cortex-models` — ORM (User, Case, Document, SyncJob, AuditLog)
- `libs/cortex-connectors` — Alfresco, Blob, OCR adapter stubs
- `libs/cortex-observability` — metrics/tracing hooks (stub)

## 3) Smer razvoja `cortex-core` biblioteke

Predlog faznog razvoja:

1. **Stabilizacija contract-a**
  - Standardizovati port interfejse i domenske greske.
  - Uvesti konzistentne timeout/retry politike.
2. **Observability-first core**
  - Dodati telemetry hooks (latency, retries, queue depth, failures).
  - Obezbediti shared correlation-id mehanizam.
3. **Testabilnost i provider-agnostic pristup**
  - Jasni fake/stub adapteri za LLM, OCR, DMS i embedding.
  - Portovi da omoguce zamenu implementacija bez promene domena.
4. **Versioned core API**
  - Semver pravila za `cortex-core`.
  - Deprecation politika pre lomljenja API-ja.

## 4) Potencijalna prosirenja i izdvajanje novih biblioteka

### Nove biblioteke (u okviru monolita i mikroservisa)

- `cortex-ai-kits` (prompt templates, response parsing, guardrails)
- `cortex-observability` (logging/tracing/metrics helperi)
- `cortex-connectors` (uniformni adapteri za DMS i storage konektore)
- `cortex-doc-pipeline` (shared chunking/embedding utility bez hard dependency na runtime)

### Kandidati za nezavisne servise

- **AI runtime servis**
  - Razlog: odvojeno skaliranje chat/RAG opterecenja i GPU/LLM cost control.
- **Ingestion servis**
  - Razlog: odvojeni throughput profil i batch obrada.
- **Connector/sync servis**
  - Razlog: izolacija spoljasnjih API limita i credentials lifecycle-a.

## 5) Nezavisni servisi i integracije

- `PostgreSQL` - transakcioni podaci (users, cases, documents, audit, sync jobs)
- `Redis` - cache/session, chat i Celery result backend
- `RabbitMQ` - message broker za Celery queue-e
- `Weaviate` - hybrid pretraga (BM25 + vector) i RAG retrieval
- `Neo4j` - law graph sada, general graph kasnije
- `Blob Storage` - S3/MinIO za originalne fajlove posle sync-a
- `Alfresco` - izvor istine za dokumente

## 6) Tehnologije ukljucene u trenutno resenje

- **Backend/API:** Python 3.12, FastAPI, Uvicorn
- **Async processing:** Celery, Flower
- **Data access:** SQLAlchemy 2.x, psycopg3
- **Security/Auth:** JWT (`python-jose`)
- **HTTP i integracije:** `httpx`, Redis client, Neo4j driver, Weaviate client
- **Frontend:** React web-client (Vite/pnpm tok)
- **Build i dev:** `uv` workspace, Makefile orchestration, import-linter
- **Deployment:** Docker Compose (lokalno), Kubernetes/Minikube (k8s manifesti)

## 7) Arhitekturni principi koje treba zadrzati

1. Aplikacioni shell je tanak, moduli nose domenu.
2. `cortex-core` definise ports i shared contracts, ne business use-case flow.
3. Novi konektori ulaze kroz adapter sloj, ne direktno u feature API layer.
4. Ekstrakcija u mikroservise ide kada metrika (latency, queue backlog, deploy coupling) to opravda.

## 8) Dijagram (Mermaid)

> Za Mermaid Live Editor kopiraj samo sadrzaj iz [`architecture.mmd`](architecture.mmd).

```mermaid
flowchart TB
    WC["web-client<br/>React / Vite"]

    subgraph EDGE [Edge and Auth]
        direction LR
        EDGE_PIPE["WAF · LB · Rate Limit"] --> AUTH_PIPE["SSO · JWT"]
    end

    WC --> EDGE

    subgraph MONOLITH [Modularni Monolit]
        direction TB

        CS["cortex-server · FastAPI shell"]

        subgraph HTTP_ROW [ ]
            direction LR
            MP["module-platform<br/>──────────────<br/>Auth · Cases · Audit · System"]
            MDOC["module-documents<br/>──────────────<br/>Document CRUD · Lifecycle"]
            MCHAT["module-chat<br/>──────────────<br/>Threads · Redis"]
            MSYNC["module-sync<br/>──────────────<br/>SyncOrchestrator"]
            MA["module-ai<br/>──────────────<br/>RAG · NER · Laws · NLP"]
        end

        CORE["libs/cortex-core · cortex-models · connectors"]

        MQ[(RabbitMQ)]

        subgraph WORKER_ROW [ ]
            direction LR
            MDMS["module-dms-sync<br/>──────────────<br/>sync-worker shell"]
            MING["module-ingestion<br/>──────────────<br/>ingestion-worker shell"]
        end

        CS --> HTTP_ROW
        MSYNC --> MQ
        MQ --> MDMS
        MDMS --> MING

        HTTP_ROW --> CORE
        WORKER_ROW --> CORE
    end

    EDGE --> CS

    subgraph DATA [Data and Storage]
        direction LR
        PG[(PostgreSQL)]
        RD[(Redis)]
        WV[(Weaviate)]
        N4J[(Neo4j)]
        BLOB[(Blob)]
    end

    subgraph EXT [External]
        direction LR
        ALF[Alfresco]
        SAAS["LLM · OCR"]
    end

    subgraph OPS [Ops]
        direction LR
        OBS["Observability<br/>Prometheus · Jaeger · ELK"]
        INFRA["Infra<br/>Vault · Consul · CB"]
        BAK["Backup · DR"]
    end

    CORE --> DATA
    MDMS --> ALF
    MA -.-> SAAS
    MING -.-> SAAS
    MONOLITH -.-> OPS
    DATA --> BAK

    classDef clientStyle fill:#fecaca,stroke:#991b1b,stroke-width:2px,color:#0f172a
    classDef edgeStyle fill:#e5e7eb,stroke:#4b5563,stroke-width:2px,color:#111827
    classDef shellStyle fill:#dbeafe,stroke:#1e3a8a,stroke-width:2px,color:#0f172a
    classDef platformStyle fill:#fef08a,stroke:#a16207,stroke-width:3px,color:#0f172a
    classDef docsStyle fill:#fde68a,stroke:#b45309,stroke-width:3px,color:#0f172a
    classDef chatStyle fill:#fbcfe8,stroke:#be185d,stroke-width:3px,color:#0f172a
    classDef syncStyle fill:#ddd6fe,stroke:#5b21b6,stroke-width:3px,color:#0f172a
    classDef aiStyle fill:#bfdbfe,stroke:#1e3a8a,stroke-width:3px,color:#0f172a
    classDef dmsStyle fill:#86efac,stroke:#166534,stroke-width:3px,color:#0f172a
    classDef ingestionStyle fill:#6ee7b7,stroke:#047857,stroke-width:3px,color:#0f172a
    classDef coreStyle fill:#fee2e2,stroke:#991b1b,stroke-width:3px,color:#0f172a
    classDef mqStyle fill:#bbf7d0,stroke:#166534,stroke-width:2px,color:#0f172a
    classDef dataStyle fill:#fde68a,stroke:#b45309,stroke-width:2px,color:#0f172a
    classDef extStyle fill:#f3f4f6,stroke:#4b5563,stroke-width:2px,color:#111827
    classDef opsStyle fill:#ddd6fe,stroke:#5b21b6,stroke-width:2px,color:#0f172a

    class WC clientStyle
    class EDGE_PIPE,AUTH_PIPE edgeStyle
    class CS shellStyle
    class MP platformStyle
    class MDOC docsStyle
    class MCHAT chatStyle
    class MSYNC syncStyle
    class MA aiStyle
    class MDMS dmsStyle
    class MING ingestionStyle
    class CORE coreStyle
    class MQ mqStyle
    class PG,RD,WV,N4J,BLOB dataStyle
    class ALF,SAAS extStyle
    class OBS,INFRA,BAK opsStyle

    style MONOLITH fill:#f8fafc,stroke:#334155,stroke-width:3px,color:#0f172a
    style HTTP_ROW fill:#fffbeb,stroke:#d97706,stroke-width:1px,stroke-dasharray:4
    style WORKER_ROW fill:#ecfdf5,stroke:#059669,stroke-width:1px,stroke-dasharray:4
    style DATA fill:#fffbeb,stroke:#b45309,stroke-width:2px
    style EXT fill:#f9fafb,stroke:#6b7280,stroke-width:2px
    style OPS fill:#f5f3ff,stroke:#7c3aed,stroke-width:2px
```

### Legenda

| Vizuelni element | Značenje |
|------------------|----------|
| Veliki okvir **Modularni Monolit** | Ceo repo — 7 modula + shared libs |
| Isprekidani okvir **HTTP row** | HTTP moduli na cortex-server-u |
| Isprekidani okvir **Worker row** | Async moduli na Celery workerima |
| **cortex-core / models / connectors** | Deljeni kernel |



