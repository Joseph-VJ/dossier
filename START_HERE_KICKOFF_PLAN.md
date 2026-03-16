# Dossier Kickoff Plan

Reviewed sources, in precedence order:
- `DOSSIER_FINAL_UNIFIED_ALGORITHM_PLAN.md`
- `DOSSIER_EXECUTION_ROADMAP_NO_TIMELINE.md`
- `DOSSIER_PRODUCT_PLAN.md`

## Current State

- This workspace is planning-only.
- There is no existing application scaffold.
- There is no Git repository initialized here yet.
- The docs consistently say to build `V0` as a Python CLI first, then add the web app in `V1`.

## Where To Start

Start with a thin, end-to-end `V0` backend path, not the UI.

The docs are clear on the order:
1. Freeze the core contracts and graph schema.
2. Build one working investigation flow in Python CLI.
3. Add instrumentation and benchmarks.
4. Only then add Docker + FastAPI + Next.js for `V1`.

If you start with the frontend or full multi-agent runtime now, you will burn time before proving the core thesis.

## Approach

Build the smallest version that can answer one question, search two lanes, store evidence packets, synthesize top candidates, and emit a Markdown dossier with traceability. Keep everything local-first and simple: Python, SQLite, LiteLLM, and one search adapter.

## Scope

- In:
  - Python package + CLI
  - contract schemas
  - evidence packet pipeline
  - one planner
  - two research lanes
  - one synthesis path
  - Markdown dossier output
  - SQLite storage
  - baseline metrics and benchmark prompts
- Out:
  - Next.js UI
  - FastAPI production API
  - Docker Compose packaging
  - Redis/Celery
  - PostgreSQL-by-default
  - Playwright-by-default
  - plugin ecosystem

## Action Items

- [ ] Initialize a real GitHub repo for the product and clone it locally into this workspace.
- [ ] Create the Python project skeleton: `pyproject.toml`, `src/`, `tests/`, `.env.example`, `README.md`.
- [ ] Add `contracts/` schemas first for `SOURCE_ORIGIN_CLUSTER`, `CONTRADICTION`, `HYPOTHESIS`, `MECHANISM`, `PROOF_TREE`, `PREDICTION`, `NOVELTY_SCORE`, and `COUNTERFACTUAL_TEST`.
- [ ] Implement core persisted entities for cases, sources, evidence items, claims, gaps, and insights in SQLite.
- [ ] Implement a CLI command like `dossier investigate "<question>"`.
- [ ] Add one planner call that turns a question into exactly two research lanes.
- [ ] Add one search/fetch/extract loop with one paid provider and one free fallback.
- [ ] Convert fetched content into evidence packets and store provenance for each packet.
- [ ] Implement one synthesis step that works on a subgraph slice and returns top-3 ranked invention outputs with assumptions and disconfirming signals.
- [ ] Render one Markdown dossier from stored evidence plus ranked outputs.
- [ ] Add baseline instrumentation for tokens, cost, latency, novelty score, grounded novelty, and coherence failures.
- [ ] Create a fixed benchmark prompt set with at least 20 prompts and run regression comparisons before expanding scope.

## Validation

- [ ] Verify one CLI investigation can complete end-to-end with stored evidence and a generated Markdown dossier.
- [ ] Verify every final output includes source atoms, assumptions, disconfirming signals, and score breakdowns.
- [ ] Verify the benchmark set can be rerun deterministically enough to compare prompt, retrieval, and ranking changes.

## What To Download Or Clone

## Required Now

- Your own product repo.
  - The product docs use `dossier-ai/dossier` as the intended canonical repo name, but this workspace does not contain that repo yet.
  - Practical step: create the GitHub repo first, then clone it here.

- Python 3.12+
- Node.js 20+ later for `V1`, not required for the first implementation pass
- Docker Desktop later for `V1`, not required for proving `V0`
- One LLM provider key
  - OpenAI or Anthropic for easiest first pass
  - Ollama only if you want local inference from day one
- One search provider
  - Tavily first
  - DuckDuckGo fallback

## Best Reference Repos

- `pydantic/pydantic-ai`
  - Use as the typed agent/workflow foundation.
  - Repo: `https://github.com/pydantic/pydantic-ai`

- `BerriAI/litellm`
  - Use for provider abstraction from day one.
  - Repo: `https://github.com/BerriAI/litellm`

- `hotchpotch/open_provence`
  - Reference for context pruning if long-context costs become a problem early.
  - Repo: `https://github.com/hotchpotch/open_provence`

## Optional Benchmark / Inspiration Repos

- `assafelovic/gpt-researcher`
  - Use for benchmark comparison, not as your runtime foundation.
  - Repo: `https://github.com/assafelovic/gpt-researcher`

- `langchain-ai/open_deep_research`
  - Use for benchmark comparison and eval ideas, not as your core architecture.
  - Repo: `https://github.com/langchain-ai/open_deep_research`

## Optional Infrastructure Repos

- `searxng/searxng`
  - Only needed if you want self-hosted free search.
  - Repo: `https://github.com/searxng/searxng`

- `microsoft/playwright`
  - Only needed when HTTP fetching fails on JS-heavy sites.
  - Repo: `https://github.com/microsoft/playwright`

## Recommendation

Do not clone every referenced project.

For the first build pass, only do this:
1. Create and clone your Dossier repo.
2. Install Python dependencies from packages.
3. Keep `GPT Researcher`, `Open Deep Research`, `OpenProvence`, `SearXNG`, and `Playwright` as reference or later-stage additions unless you hit a real blocker.
