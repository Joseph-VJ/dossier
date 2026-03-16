# Dossier Final Unified Algorithm Plan (Invention Mode)

Research date: 2026-03-11  
Status: final unified spec updated for invention-first behavior  
Purpose: maximize generation of new, non-obvious information derived from available evidence, even when conclusions are speculative.

## Executive summary

This version intentionally shifts Dossier away from "trust-first investigation" and toward **invention-first deep synthesis**.

Primary objective:

- generate new candidate information that does not explicitly exist on the internet
- combine disparate evidence into novel explanatory models
- push hypothesis generation depth while still controlling token cost

Secondary objective:

- keep minimal internal coherence and traceability so outputs remain usable

Core architecture:

- **BAEGC-lite** as runtime engine (planning, retrieval, graph building, token control)
- **ADEPT-DS** as invention kernel (abduction, synthesis, mechanism generation, novelty ranking)

## Selective borrowings from `deep-research-report.md`

Kept from that research memo:

- dual-process gating as a compute policy: cheap proposal first, deeper deliberation only on conflict or surprise
- evidence loop plus invention loop as the clean architectural split
- curiosity and novelty search as ranking signals for candidate insights
- reusable reasoning templates (`Self-Discover`, `Buffer of Thoughts`)
- graph-grounded synthesis over evidence structures instead of raw transcript reasoning
- grounded novelty evaluation

Not kept as core:

- full cognitive-architecture frameworks (`Soar`, `ACT-R`, `CLARION`, `LIDA`, `OpenCog`, `OpenNARS`) as the runtime foundation
- broad RL and habit-formation infrastructure as the current implementation path
- human-bias replication as the default reasoning mode
- peak-end or memory-distortion modeling as a core product requirement

## What changed from the previous version

The old mode prioritized:

- strict trust gating
- adversarial rejection
- conservative promotion rules

This new mode prioritizes:

- novelty
- synthesis depth
- idea generation range
- mechanism creativity
- cross-domain recombination

Trust is no longer the top gate.  
Now the top gate is **invention value**.

## Final algorithm names

### Outer runtime layer

**BAEGC-lite**  
Budgeted Adversarial Evidence Graph Compiler

Role:

- one-shot planning
- parallel execution DAGs
- retrieval and extraction
- context pruning and compression
- graph materialization
- budget and token controls

### Inner reasoning layer

**ADEPT-DS**  
Abductive-Deductive Exploratory Proof Trees for Dossier Synthesis

Role:

- generate hidden hypotheses
- compose new mechanisms from partial evidence
- run counterfactual idea expansion
- score and rank novelty
- package outputs as candidate new information

## New objective function (invention-first)

Optimize for:

1. novelty distance from source text
2. cross-source synthesis depth
3. mechanism completeness
4. predictive richness
5. cross-domain transfer strength
6. token efficiency

De-prioritize:

- strict factual conservatism as a hard blocker

## Invention scoring model

Each candidate insight gets a score in [0, 1]:

`InventionScore = 0.30*NoveltyDistance + 0.20*SynthesisDepth + 0.20*MechanismQuality + 0.15*PredictivePower + 0.10*CrossDomainTransfer + 0.05*TokenEfficiency - 0.10*CoherencePenalty`

Classes:

- `Breakthrough candidate`: score >= 0.78
- `Strong novel candidate`: score >= 0.62
- `Exploratory candidate`: score >= 0.48
- discard below 0.48

## BAEGC-lite runtime pipeline

## Stage 0: case-memory warm start

Retrieve prior similar cases and prior invention patterns before new planning.

Use:

- `Memento`-style case memory

## Stage 1: one-shot planning

Generate one structured plan:

- objective
- lanes
- search strategy
- expansion budget
- novelty target profile

Use:

- `ReWOO`
- `Plan-and-Act`

Rule:

- one planner call by default
- replan only if search yield is too sparse

## Stage 2: compile to execution DAG

Convert plan into parallel tasks:

- lane searches
- fetch + parse
- extraction
- packetization

Use:

- `LLMCompiler`

## Stage 3: retrieval reduction

Apply:

- adaptive chunking
- context pruning
- prompt compression

Use:

- `SmartChunk Retrieval`
- `Provence` / `OpenProvence`
- `LongLLMLingua`

Rule:

- analyst layer consumes evidence packets and graph slices, not raw full pages

## Stage 4: graph materialization

Represent evidence as typed graph atoms.

Core nodes:

- source
- source_origin_cluster
- evidence_item
- claim
- contradiction
- gap
- hypothesis
- mechanism
- deduction
- prediction
- proof_tree

Core edges:

- supports
- contradicts
- derived_from
- cites
- clustered_with
- implies
- explains
- analog_to
- undermines

Use:

- `TRACE`
- `GEAR`
- `NodeRAG` (as design pattern)

## ADEPT-DS invention kernel

## Phase 1: evidence atomization

Convert evidence packets into typed atoms:

- entities
- events
- numerics
- temporal relations
- contradictions
- absences
- weak signals

## Phase 2: trigger-gated deep synthesis

Run deep synthesis only when triggers appear:

- unusual cross-lane convergence
- high contradiction density
- unexplained event sequences
- meaningful missing-data patterns
- repeated weak-signal alignment

No trigger: do not spend deep reasoning tokens.

## Phase 3: hypothesis beam generation

Generate a broad candidate beam (not one answer):

- default beam size 16-32 hypotheses per region
- include at least 20% cross-domain analogical hypotheses

Use:

- `Graph of Thoughts`
- `Adaptive Graph of Thoughts`
- `Self-Discover`
- `Buffer of Thoughts`

## Phase 4: mechanism synthesis

For each hypothesis, create an explicit mechanism:

- causal chain or structural explanation
- required assumptions
- failure points
- rival explanations

Use:

- `DARK`-style abductive + deductive combination

## Phase 5: lightweight executable checks

Do deterministic checks where possible:

- arithmetic
- temporal order
- thresholds
- counts
- set relations

Use:

- `Program of Thoughts` ideas

This is not for strict truth proof.  
It is for removing low-quality, internally broken hypotheses.

## Phase 6: counterfactual expansion

For top candidates, generate:

- what-if variants
- environmental shifts
- parameter perturbations
- single-premise removal outcomes

Goal:

- increase insight richness
- detect fragile hypotheses

## Phase 7: novelty and synthesis ranking

Compute:

- novelty distance from known source statements
- synthesis depth (how many independent components are fused)
- mechanism quality
- predictive richness
- cross-domain transfer strength
- coherence penalty

Then rank using `InventionScore`.

## Phase 8: invention packaging

Publish top candidates as:

- `Novel Deduction`
- `Speculative Mechanism`
- `Exploratory Prediction`

Each item includes:

- source atoms used
- synthesis chain
- mechanism summary
- expected observable outcomes
- disconfirming signals
- invention score

## Minimal quality constraints (not trust-first gates)

Even in invention mode, enforce:

1. no output without source atom references
2. no output with hard internal contradiction unresolved
3. no output without explicit assumptions
4. no output without at least one disconfirming condition
5. no output without novelty score breakdown

These are coherence constraints, not strict truth constraints.

## Main stack (use now)

- `LiteLLM`
- `Pydantic AI`
- custom Python state machine or `LangGraph`
- `ReWOO`
- `Plan-and-Act`
- `LLMCompiler`
- `TRACE`
- `NodeRAG`
- `Provence` / `OpenProvence`
- `LongLLMLingua`
- `Memento`
- `Graph of Thoughts`
- `Adaptive Graph of Thoughts`
- `Self-Discover`
- `Buffer of Thoughts`
- `DARK` (as method inspiration)
- `Program of Thoughts` (for deterministic sanity checks)

## Main stack (use later)

- `MCTS-RAG` for rare hard exploration paths
- `PSL` or `ProbLog` for richer uncertain-rule scoring
- stronger cross-case analogical retrieval
- domain-specific synthesis templates

## Avoid in v1

- full RL/world-model stacks
- free-form multi-agent debate as default
- browser-first everywhere
- expensive tree search on all graph regions
- strict rejection-heavy trust filtering as primary objective

## Token strategy for invention mode

Hard rules:

1. use small/medium models for broad hypothesis beam generation
2. reserve strongest model for top-K candidates only
3. prune and compress before deep reasoning
4. reason on subgraphs, not full-case context
5. cap deep synthesis calls by trigger gate
6. cache hypothesis beams and mechanism templates
7. reuse case-memory motifs before generating from scratch

## Output schema (recommended)

Each published insight should contain:

- `insight_id`
- `class` (`Novel Deduction` | `Speculative Mechanism` | `Exploratory Prediction`)
- `title`
- `hypothesis`
- `source_atoms[]`
- `synthesis_chain[]`
- `mechanism`
- `assumptions[]`
- `predicted_observables[]`
- `disconfirming_signals[]`
- `invention_score`
- `score_breakdown`

## Execution roadmap (no timeline)

1. Freeze contracts and graph schema for invention mode entities.
2. Implement BAEGC-lite runtime with one-shot planning and DAG execution.
3. Implement pruning/compression pipeline.
4. Implement ADEPT atomization and trigger detector.
5. Implement hypothesis beam and mechanism synthesis.
6. Implement deterministic sanity checker.
7. Implement invention scoring and top-K ranking.
8. Implement invention output rendering and export.
9. Add evaluation harness for novelty, coherence, and prediction quality.
10. Tune beam size and model mix for best novelty-per-token ratio.

## What you need to check continuously

1. Novelty rate:
- percent of outputs that are semantically non-redundant with source statements.

2. Synthesis depth:
- average number of independent source clusters used per top insight.

3. Mechanism quality:
- does each insight provide a coherent mechanism, not just a claim?

4. Prediction utility:
- are predicted observables specific and testable?

5. Token efficiency:
- novelty-per-token ratio by stage and by model tier.

6. Failure modes:
- empty novelty
- fake novelty (paraphrase)
- incoherent mechanism
- over-fragmented hypothesis beam

## Recommended papers and repos behind this mode

Core synthesis:

- Graph of Thoughts: <https://arxiv.org/abs/2308.09687>
- Adaptive Graph of Thoughts: <https://arxiv.org/abs/2502.05078>
- Self-Discover: <https://arxiv.org/abs/2402.03620>
- Buffer of Thoughts: <https://arxiv.org/abs/2406.04271>
- DARK: <https://arxiv.org/abs/2510.11462>

Runtime efficiency:

- ReWOO: <https://arxiv.org/abs/2305.18323>
- Plan-and-Act: <https://arxiv.org/abs/2503.09572>
- LLMCompiler: <https://arxiv.org/abs/2312.04511>
- LongLLMLingua: <https://arxiv.org/abs/2310.06839>
- Provence: <https://arxiv.org/abs/2501.16214>
- OpenProvence: <https://github.com/hotchpotch/open_provence>
- Memento: <https://arxiv.org/abs/2508.16153>

Evidence graph and grounding:

- TRACE: <https://arxiv.org/abs/2406.11460>
- GEAR: <https://arxiv.org/abs/1908.01843>
- NodeRAG: <https://arxiv.org/abs/2504.11544>
- Program of Thoughts: <https://arxiv.org/abs/2211.12588>

## Final decision

For your stated goal, Dossier should run in **Invention Mode**:

- prioritize novel information synthesis over strict trust filtering
- keep only minimal coherence and structural constraints
- maximize high-quality speculative insight per token

Final unified algorithm:

`BAEGC-lite (runtime) + ADEPT-DS (invention kernel)`
