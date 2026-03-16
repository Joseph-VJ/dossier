# Dossier

Dossier is an open-source investigation engine scaffold for evidence-traced research and invention-first synthesis.

This repository currently implements the `V0` foundation:
- Python package + CLI
- contract schemas for the core invention-mode entities
- SQLite-backed local persistence
- pluggable search and LLM interfaces
- deterministic demo providers so the thin path runs without API keys
- Markdown dossier output

## Current Scope

Implemented now:
- `dossier investigate "<question>"` CLI
- LLM-driven multi-lane planning (with deterministic demo fallback)
- search provider abstraction
- evidence packet storage
- evidence atomization (`entity`, `event`, `numeric`, `temporal`, `contradiction`, `absence`, `weak_signal`)
- top-3 ranked insight generation
- dossier Markdown rendering with full score-component breakdown
- JSON schema export for contracts

Intentionally deferred:
- FastAPI API
- Next.js UI
- Docker Compose deployment
- Playwright browser worker
- Redis/Celery
- PostgreSQL-first deployment

## Quickstart

1. Create a virtual environment:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

2. Copy the environment file:

```powershell
Copy-Item .env.example .env
```

3. Run the thin path:

```powershell
dossier investigate "Should Acme acquire Beta?"
```

By default, the app uses deterministic demo providers so it works without API keys.

## Real Providers

You can switch providers in `.env`.

- `SEARCH_PROVIDER=tavily` requires `SEARCH_API_KEY`
- `SEARCH_PROVIDER=duckduckgo` needs no key
- `LLM_PROVIDER=litellm` uses `LLM_MODEL` and `LLM_API_KEY`

If a real provider fails, the runtime falls back to the demo provider instead of crashing the whole investigation.

## Useful Commands

Initialize the database:

```powershell
dossier init-db
```

Export JSON schemas to `contracts/`:

```powershell
python scripts\export_contract_schemas.py
```

Run validation:

```powershell
ruff check src tests
mypy src
bandit -r src -ll
pytest
```

## Layout

- `src/dossier`: package code
- `tests`: automated tests
- `contracts`: exported JSON schemas
- `benchmarks`: benchmark prompt set
- `DOSSIER_FINAL_UNIFIED_ALGORITHM_PLAN.md`: authoritative algorithm spec
- `DOSSIER_EXECUTION_ROADMAP_NO_TIMELINE.md`: execution order
- `DOSSIER_PRODUCT_PLAN.md`: product context
