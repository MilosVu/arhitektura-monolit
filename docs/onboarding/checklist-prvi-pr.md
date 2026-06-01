# Checklist — prvi PR / svaki PR

## Pre otvaranja PR-a

- [ ] Feature je u **ispravnom modulu** ([gde-sta-ide.md](gde-sta-ide.md))
- [ ] Novi kod prati [hexagonal-layout.md](hexagonal-layout.md) gde je primenjivo
- [ ] Cross-module samo preko `module_*/api.py`
- [ ] `Document.status` samo `DocumentsModule.mark_*` (ako dira dokumente)
- [ ] Celery task imena iz `cortex_core.messaging.tasks`

## Komande (u `arhitektura-monolit/`)

```bash
make lint-imports
make flct    # format + lint + mypy + import-linter + test (isto kao CI)
```

## Šta uključiti u PR opis

- Koji modul / use-case
- Da li menja granice modula (import-linter)
- Da li menja API (breaking change)
- Kako ručno testirati (korak 1–2–3)

## Red flags za review

- Business logika u `apps/cortex-server/main.py`
- Import `module_* .services` ili `module_* .agents` iz drugog modula
- Direktan ORM write na `Document.status` u workeru
- Novi hardcoded Celery task string
