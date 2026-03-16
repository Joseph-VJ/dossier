# Dossier Execution Roadmap (No Timeline)

Reference docs:
- `DOSSIER_PRODUCT_PLAN.md`
- `DOSSIER_FINAL_UNIFIED_ALGORITHM_PLAN.md`

## Approach

Build by capability gates, not calendar dates.
Only move to the next stage when the current stage is stable, measurable, and testable.
Treat `BAEGC-lite` as the runtime backbone and `ADEPT-DS` as the core differentiator.

## Scope

- In:
  - Core investigation engine, evidence graph, adversarial review, insight synthesis, safety, and evals.
  - Self-hosted first, BYOK, local-first defaults.
- Out:
  - Heavy RL stacks, generic multi-agent debates, broad multimodal/robotics scope, and premature enterprise extras.

## Action Items

[ ] 1. Freeze the canonical spec baseline.
- Lock architecture decisions from `DOSSIER_FINAL_UNIFIED_ALGORITHM_PLAN.md`.
- Freeze names and contracts for `Planner`, `Researcher`, `Adversary`, `Analyst`, `Writer`.
- Freeze required output sections and trust rules.

[ ] 2. Define the data contracts before implementation.
- Finalize schemas for `CASE`, `SOURCE`, `EVIDENCE_ITEM`, `CLAIM`, `REVIEW_NOTE`, `GAP`, `INSIGHT`.
- Add new ADEPT entities: `PROOF_TREE`, `PROOF_NODE`, `HYPOTHESIS`, `COUNTERFACTUAL_TEST`, `NOVELTY_SCORE`.
- Write strict validation rules for every model output that enters the graph.

[ ] 3. Implement the BAEGC-lite runtime first.
- Add one-shot structured planning (`ReWOO` style).
- Add plan-to-DAG compilation (`LLMCompiler` style) for parallel lane execution.
- Add strict budgets and stop conditions at orchestrator level.
- Ensure browser automation is fallback only.

[ ] 4. Build retrieval reduction before deep reasoning.
- Add adaptive chunking and context pruning (`Provence` style).
- Add prompt compression (`LongLLMLingua` style) where contexts exceed threshold.
- Enforce evidence-packet generation so analyst and writer consume packets, not raw pages.

[ ] 5. Build evidence graph and source independence engine.
- Materialize typed nodes and edges required by the final plan.
- Implement source-origin clustering and independence scoring.
- Implement contradiction and gap logging as first-class graph artifacts.

[ ] 6. Implement ADEPT-DS core reasoning.
- Add insight trigger detection to gate expensive synthesis.
- Add abductive hypothesis generation (small candidate beam).
- Add deductive proof-tree construction for each candidate.
- Add deterministic proof executor (numeric, temporal, threshold, set checks).
- Add novelty gate (`novel deduction` vs `strong synthesis` downgrade path).

[ ] 7. Add adversarial and falsification loops.
- Run dedicated adversary pass on claims and deductions.
- Implement counterfactual tests:
  - leave-one-premise-out
  - leave-one-origin-cluster-out
  - alternative hypothesis comparison
  - contradiction insertion
  - missing-evidence sensitivity
- Auto-downgrade or reject insights that fail stress tests.

[ ] 8. Build output assembly and detective-chain rendering.
- Keep writer constrained to graph-backed artifacts only.
- Render executive summary from proof trees, not free-form generation.
- Show falsification conditions and strongest counter-evidence per key insight.

[ ] 9. Build evaluation harness before launch.
- Add retrieval metrics, reasoning metrics, and trust metrics.
- Add hallucination and citation-faithfulness checks (`SAFE`, `FActScore`, `RAGChecker` style).
- Track per-stage cost, token usage, and latency.
- Add fail reasons taxonomy and regression tests.

[ ] 10. Harden security and release workflow.
- Add tool boundary isolation and memory compartmentalization (`AgentSentry` and `AgentSys` patterns).
- Add prompt-injection handling for fetched content.
- Add CI checks for schema validity, deterministic scoring, and output safety constraints.
- Prepare launch-ready docs: quickstart, architecture, config matrix, troubleshooting, contribution guide.

## What You Need to Check at Every Stage

1. Evidence integrity:
- Every claim maps to specific evidence items and source provenance.
- No narrative-only claim survives publication.

2. Independence integrity:
- Confidence cannot be promoted from duplicated-origin support.
- Source inflation factor is visible and used in scoring.

3. Reasoning integrity:
- No deduction without proof tree.
- No `novel deduction` label without novelty gate pass.

4. Adversarial integrity:
- Strongest contradiction is always surfaced.
- High-severity adversarial findings cannot be hidden by the writer layer.

5. Token and cost integrity:
- Large models are only used where necessary.
- Planning, pruning, routing, and triage use cheaper paths by default.

6. Security integrity:
- Untrusted web/tool content is isolated until sanitized.
- Tool selection and arguments are schema constrained.

7. Product integrity:
- User can challenge any claim or deduction.
- Re-investigation flow works on specific contested points.

## Stage Exit Gates (No Timeline)

A stage is complete only when all three are true:

1. Correctness gate:
- Tests pass and no blocking integrity violation remains.

2. Trust gate:
- Provenance, contradiction, and gap sections are complete and accurate.

3. Efficiency gate:
- Token usage and latency are within target bounds for the selected depth tier.

## Start Here (Immediate First Moves)

1. Create a `contracts/` package for all structured schemas and validators.
2. Create an `orchestrator/` package with explicit investigation state machine states.
3. Implement one end-to-end happy path:
- one question
- one plan
- two research lanes
- one adversary pass
- one ADEPT insight
- one dossier output
4. Add baseline metrics logging from day one (tokens, cost, latency, failures).
5. Add a fixed evaluation set of 20 investigation prompts to track regressions.

## Open Questions to Resolve Early

1. Which minimum model tier is acceptable for each role (`Planner`, `Researcher`, `Adversary`, `Analyst`, `Writer`)?
2. What is the exact threshold policy for promoting `strong synthesis` to `novel deduction`?
3. Which initial domain template gets first-class optimization after due diligence?
