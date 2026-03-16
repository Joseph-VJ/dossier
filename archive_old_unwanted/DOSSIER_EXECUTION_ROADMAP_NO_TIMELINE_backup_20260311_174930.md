# Dossier Execution Roadmap (No Timeline, Invention Mode)

Reference docs:
- `DOSSIER_FINAL_UNIFIED_ALGORITHM_PLAN.md` (authoritative)
- `DOSSIER_PRODUCT_PLAN.md` (legacy product context with override)

## Approach

Build by capability gates, not dates.
Optimize for **novel insight generation per token** with minimal coherence constraints.
Treat `BAEGC-lite` as runtime and `ADEPT-DS` as the invention kernel.

## Scope

- In:
  - evidence graph, synthesis triggers, hypothesis beam generation, mechanism synthesis, novelty scoring, counterfactual expansion, invention packaging
  - self-hosted BYOK defaults and budget controls
- Out:
  - strict trust-first filtering as primary objective
  - heavy RL stacks and broad multimodal/robotics expansion

## Action Items

[ ] 1. Freeze invention-mode contracts.
- Lock `BAEGC-lite + ADEPT-DS` names and interfaces.
- Freeze insight classes: `Novel Deduction`, `Speculative Mechanism`, `Exploratory Prediction`.
- Freeze invention scoring and ranking policy.

[ ] 2. Finalize data schema for invention outputs.
- Keep existing entities (`CASE`, `SOURCE`, `EVIDENCE_ITEM`, `CLAIM`, `GAP`, `INSIGHT`).
- Add or finalize: `HYPOTHESIS`, `MECHANISM`, `PROOF_TREE`, `PREDICTION`, `NOVELTY_SCORE`, `COUNTERFACTUAL_TEST`.
- Validate all model outputs before graph insertion.

[ ] 3. Build BAEGC-lite runtime backbone.
- Implement one-shot planner (`ReWOO` style).
- Compile plan into parallel DAG (`LLMCompiler` style).
- Enforce budgets, call caps, and fallback rules.
- Keep browser usage fallback-only.

[ ] 4. Build retrieval reduction pipeline.
- Add adaptive chunking and pruning.
- Add prompt compression for long contexts.
- Enforce evidence packets for analyst and writer stages.

[ ] 5. Build graph materialization and signal detection.
- Materialize typed graph nodes/edges from evidence packets.
- Add source-origin clustering.
- Add invention triggers:
  - cross-lane convergence
  - contradiction density
  - timeline anomalies
  - meaningful absences

[ ] 6. Implement ADEPT-DS phase core.
- Add hypothesis beam generation (not single-answer generation).
- Add mechanism synthesis per hypothesis.
- Add deterministic sanity checks (temporal, arithmetic, thresholds, set checks).
- Add counterfactual expansion per top hypotheses.

[ ] 7. Add invention ranking and gating.
- Compute `InventionScore` with score breakdown.
- Rank and keep top-K hypotheses only.
- Apply minimal coherence gate:
  - source atom references required
  - assumptions required
  - disconfirming signals required

[ ] 8. Build output assembly for invention mode.
- Render detective-chain style synthesis for each top candidate.
- Include assumptions, mechanism, predicted observables, and disconfirming signals.
- Export with insight class and full score breakdown.

[ ] 9. Build evaluation harness tuned for invention mode.
- Track novelty rate and novelty distance.
- Track synthesis depth and mechanism quality.
- Track prediction richness and coherence failure rate.
- Track novelty-per-token and latency-per-insight.

[ ] 10. Harden safety and release workflow.
- Add tool and memory isolation checks.
- Add prompt-injection handling for untrusted retrieval.
- Add CI checks for schema validity and scoring consistency.
- Add docs describing invention mode behavior and limitations.

## What You Need to Check Continuously

1. Novelty quality:
- output is not a paraphrase of one source
- output combines independent evidence clusters

2. Synthesis depth:
- top candidates use multi-lane evidence, not single-lane restatements

3. Mechanism quality:
- each insight includes mechanism, assumptions, and failure points

4. Prediction utility:
- each insight includes specific predicted observables and disconfirming signals

5. Coherence floor:
- no internally broken logic or unresolved hard contradictions in top outputs

6. Cost discipline:
- novelty-per-token improves over iterations
- expensive models only run for top-K candidates

## Stage Exit Gates (No Timeline)

A stage is complete only if:

1. Correctness gate:
- tests pass and no blocking schema/logic errors remain

2. Invention gate:
- novelty rate and synthesis depth meet target for that stage

3. Efficiency gate:
- token and latency budgets remain within configured limits

## Start Here (Immediate First Moves)

1. Create `contracts/` schemas for `HYPOTHESIS`, `MECHANISM`, `NOVELTY_SCORE`, `COUNTERFACTUAL_TEST`.
2. Implement one end-to-end thin path:
- one question
- one plan
- two lanes
- hypothesis beam
- top-3 ranked invention outputs
3. Add baseline instrumentation:
- tokens, cost, latency, novelty score distribution, coherence failures
4. Create a fixed benchmark prompt set (20 prompts minimum) for regression.

## Open Questions to Resolve Early

1. What exact beam size and top-K policy balances novelty and cost?
2. What minimum coherence threshold should block publication?
3. Which domains produce the strongest novelty-per-token in early testing?
