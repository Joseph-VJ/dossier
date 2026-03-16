# Dossier Final Unified Algorithm Plan

Research date: 2026-03-11
Status: consolidated final algorithm direction
Purpose: merge the deeper online algorithm stack and the core insight-synthesis design into one final Dossier algorithm specification.

## Executive summary

Dossier should not be built as a generic deep-research chatbot or a larger swarm of agents.

It should be built as a **budgeted evidence system** with a **dedicated insight-synthesis core**.

The final recommendation is:

- use **BAEGC-lite** as the outer runtime system
- use **ADEPT-DS** as the inner reasoning kernel

In short:

- `BAEGC-lite` gets the right evidence cheaply, safely, and in parallel
- `ADEPT-DS` turns that evidence into novel, defensible, adversarially-tested insight

This is the strongest architecture I found for your goal:

- outperform standard deep-research tools
- use fewer tokens where possible
- produce deeper and more accurate conclusions
- surface conclusions that are not explicitly written in any one source
- show the detective-style reasoning chain that led there

## Final algorithm names

### Outer runtime layer

**BAEGC-lite**

`Budgeted Adversarial Evidence Graph Compiler`

Role:

- planning
- task compilation
- retrieval
- context reduction
- graph materialization
- orchestration
- budget control
- tool safety

### Inner reasoning layer

**ADEPT-DS**

`Abductive-Deductive Evidence Proof Trees for Dossier Synthesis`

Role:

- generate hidden hypotheses
- prove or weaken them
- test alternatives
- detect novelty
- produce defensible deductions

## The full final architecture

### Core principle

The system should reason over **evidence structures**, not over raw page text or chat history.

The architecture should be:

1. plan once
2. execute many tasks in parallel
3. prune context aggressively
4. convert evidence into typed graph atoms
5. run deep insight synthesis only where graph triggers justify it
6. prove, falsify, and downgrade candidate insights before publication

### The final split

#### BAEGC-lite handles:

- one-shot structured planning
- parallel execution DAGs
- search, fetch, parse, extract
- evidence packet generation
- evidence graph storage
- source independence heuristics
- contradiction collection
- gap logging
- token budgeting
- tool and memory isolation

#### ADEPT-DS handles:

- abductive hypothesis generation
- deductive proof-tree construction
- executable verification
- defeasible scoring
- counterfactual falsification
- novelty gating
- detective-chain rendering

## Why this is stronger than normal deep research

Most deep-research systems stop at:

- retrieve
- summarize
- cite

Dossier should go further:

- retrieve evidence
- convert it to atomic facts
- identify hidden patterns across lanes
- propose explanations that are not stated directly
- test those explanations against counter-evidence
- render only the insights that survive pressure

That means Dossier is not just a research aggregator.
It becomes an **investigation engine with a proof-backed deduction layer**.

## BAEGC-lite: the outer runtime system

## Stage 0: case-memory warm start

Before fresh planning, retrieve similar prior investigations, failure modes, and source patterns.

Use:

- `Memento` style case memory
- simple non-parametric memory first

Benefits:

- lower planning token cost
- better lane selection
- faster convergence on useful sources

## Stage 1: one-shot structured planning

Generate one structured plan:

- objective
- hypotheses
- lanes
- source classes
- stop conditions
- budget

Use:

- `ReWOO`
- `Plan-and-Act`

Rules:

- one main planner call per investigation
- replanning only on major contradiction, failed stop condition, or user challenge

Benefits:

- fewer repeated reasoning prompts
- cleaner execution contracts

## Stage 2: compile the plan into an execution DAG

Convert the plan into a dependency graph:

- independent lane searches run in parallel
- fetch and parse tasks run in parallel
- only dependency-linked tasks stay sequential

Use:

- `LLMCompiler`

Rules:

- compile once, execute many
- each worker receives a structured task, not the whole case conversation

Benefits:

- lower latency
- lower token repetition
- better reproducibility

## Stage 3: adaptive retrieval and context reduction

Never feed raw fetched pages directly into the analyst or writer.

Retrieval pipeline:

1. search
2. fetch
3. adaptive chunking
4. context pruning
5. quote extraction
6. evidence packet creation
7. graph insertion

Use:

- `SmartChunk Retrieval`
- `Provence` / `OpenProvence`
- `LongLLMLingua`

Benefits:

- strongest direct token savings
- less noise
- stronger factual grounding

## Stage 4: evidence graph materialization

Represent the case as a heterogeneous graph.

Core node types:

- source
- source_origin_cluster
- evidence_item
- claim
- contradiction
- gap
- deduction
- review_note
- lane
- retrieval_chain
- proof_tree
- proof_node

Core edge types:

- supports
- contradicts
- derived_from
- cites
- clustered_with
- belongs_to_lane
- reviewed_by
- falsified_by
- entails
- undermines
- depends_on

Use:

- `TRACE`
- `GEAR`
- `NodeRAG`

Benefits:

- graph retrieval instead of transcript replay
- better reasoning over cross-evidence structure
- better provenance and auditing

## Stage 5: deterministic pre-reasoning normalization

Before deep synthesis:

- deduplicate sources
- assign source classes
- compute freshness
- cluster origin relationships
- attach support and contradiction edges
- compute initial confidence primitives

Use LLMs only for:

- extraction normalization
- contradiction interpretation
- semantic grouping where deterministic methods are insufficient

Do not use LLMs for:

- URL normalization
- hashing
- citation bookkeeping
- score storage
- basic aggregation

## Stage 6: trigger-gated insight regions

Do not run deep insight synthesis over the whole graph.

Create **insight triggers** that activate ADEPT-DS only on graph regions that look promising.

Trigger examples:

- multiple independent weak signals converge
- temporal anomaly
- cross-lane inconsistency
- hidden-cause pattern
- contradiction implying an unstated explanation
- missing expected evidence
- inflated certainty from one origin cluster

Benefits:

- token savings
- attention focused on high-yield graph regions

## Stage 7: adversarial isolation

The adversary should not inherit contaminated raw tool memory.

Use:

- `AgentSys`
- `AgentSentry`
- `AgentSpec`

Rules:

- fetched web content remains untrusted until sanitized
- tool returns are schema-checked
- adversary receives evidence packets and proof artifacts, not arbitrary raw execution logs

Benefits:

- lower prompt injection risk
- better review integrity

## ADEPT-DS: the inner insight-synthesis kernel

ADEPT-DS is the main differentiator.

It is the part that turns:

- evidence A
- evidence B
- evidence C

into:

- conclusion D

even when no source explicitly states D.

## ADEPT-DS phase 1: evidence atomization

Convert each evidence packet into typed fact atoms:

- entity facts
- numeric facts
- temporal events
- source claims
- contradictions
- gaps
- causally suggestive events

Every atom carries:

- source id
- origin cluster id
- lane
- time
- freshness
- source class
- extraction confidence

Use:

- `TRACE`
- `GraphFC`
- `FactCG`
- `NodeRAG`

## ADEPT-DS phase 2: abductive hypothesis generation

Given a graph region, generate a small set of candidate hidden explanations that best account for the evidence together.

Examples:

- leadership change was likely driven by legal pressure
- launch delay was likely driven by certification or reliability problems
- revenue narrative is inconsistent with operational stress signals

Use:

- `DARK` as conceptual guidance
- `Graph of Thoughts`
- `AGoT`
- `Self-Discover`
- `Buffer of Thoughts`

Critical rule:

- generate a beam of candidate hypotheses
- do not jump directly to one answer

## ADEPT-DS phase 3: deductive proof-tree construction

For each candidate hypothesis, build a proof tree with:

- premises
- intermediate inferences
- assumptions
- alternative explanations
- uncertainty markers
- final conclusion

Proof node types:

- observed_fact
- derived_fact
- assumption
- rule
- contradiction
- uncertainty

Proof edge types:

- entails
- supports
- weakly_supports
- contradicts
- depends_on
- undermines

Use:

- `Graph of Thoughts`
- `GraphFC`
- `VeriCoT`
- `TabVer`

Critical rule:

- store proof trees as first-class artifacts
- the user-facing derivation chain is a rendered view of the proof tree

## ADEPT-DS phase 4: executable verification

Not every reasoning step should remain free-form language reasoning.

Route verifiable subproblems into deterministic functions:

- date ordering
- arithmetic
- ratios
- threshold checks
- counts
- set overlap
- alias or identity normalization
- rule predicates

Use:

- `Program of Thoughts`
- `AgentSpec`
- `PSL` / `ProbLog` / `DeepProbLog` as inspiration for uncertain rule evaluation

Practical v1 recommendation:

Build a lightweight proof executor:

- numeric functions
- temporal checks
- contradiction predicates
- independence constraints
- explicit rule predicates

Do not build a full theorem prover in v1.

## ADEPT-DS phase 5: defeasible and probabilistic scoring

Some insights are not strictly provable.
They are best-supported explanations under uncertainty.

Score each candidate proof tree on:

- deductive validity
- abductive explanatory power
- independence strength
- contradiction pressure
- novelty
- falsifiability
- fragility

Use:

- `PSL`
- `ProbLog`
- probabilistic argumentation ideas

Rule:

- LLMs propose rules and links
- scoring is performed by deterministic or probabilistic evaluators

## ADEPT-DS phase 6: counterfactual falsification

Every candidate insight should be stress-tested.

Required tests:

1. leave-one-premise-out
2. leave-one-origin-cluster-out
3. alternative-hypothesis comparison
4. contradiction insertion
5. missing-evidence sensitivity

These tests decide whether an insight is:

- promoted
- weakened
- downgraded
- rejected

## ADEPT-DS phase 7: novelty gating

Dossier must distinguish real novelty from paraphrase.

An insight is `novel` only if:

- it is not explicitly stated in any source quote
- it spans at least two independent origin clusters or two research lanes
- it has a non-trivial proof tree
- it survives falsification tests

Novelty features:

- explicit-statement overlap
- source-span
- cross-lane synthesis
- inference depth

Downgrade path:

- `novel deduction`
- `strong synthesis`
- `ordinary synthesis`

This prevents fake innovation theater.

## ADEPT-DS phase 8: detective-chain rendering

The executive-summary insight chain should be rendered as:

1. fact A from source X
2. fact B from source Y
3. fact C from source Z
4. why they fit together
5. alternative explanation considered
6. why chosen explanation is stronger
7. what would falsify it

This is the output layer.
The real reasoning object remains the proof tree.

## Final main stack

## Use now

| Layer | Item | Role |
|---|---|---|
| orchestration | custom Python state machine or `LangGraph` | deterministic control flow |
| contracts | `Pydantic AI` | structured inputs, outputs, validation |
| providers | `LiteLLM` | provider abstraction |
| planning | `ReWOO` | decoupled planner logic |
| planning | `Plan-and-Act` | planner-executor separation |
| execution | `LLMCompiler` | compile task DAGs for parallel execution |
| retrieval | `SmartChunk Retrieval` | adaptive chunking |
| pruning | `Provence` / `OpenProvence` | context reduction |
| compression | `LongLLMLingua` | prompt compression |
| graph | `TRACE` | evidence chains |
| graph | `GEAR` | evidence aggregation |
| graph | `NodeRAG` | heterogeneous graph inspiration |
| memory | `Memento` | case-based warm starts |
| safety | `AgentSys` | memory isolation |
| safety | `AgentSentry` | tool boundary defense |
| safety | `AgentSpec` | explicit runtime rules |
| core reasoning | `ADEPT-DS` | insight synthesis kernel |
| adaptive reasoning | `AGoT` | deeper reasoning only on triggered graph regions |
| verification | `Program of Thoughts` | executable reasoning steps |
| proof scoring | `PSL` or `ProbLog` style logic | uncertain rule scoring |

## Use later

| Item | Why later |
|---|---|
| `MCTS-RAG` | powerful but too expensive for default use |
| `Microsoft GraphRAG` | better for larger offline corpora and cross-case indexing |
| stronger probabilistic logic engine | useful after v1 proof executor exists |
| domain-specific reasoning template libraries | valuable after one strong general template exists |
| cross-case deduction over multiple dossiers | strong v2 or v3 feature |

## Do not use in v1

| Item | Why not now |
|---|---|
| full RL / world-model stacks | wrong abstraction level for the current product |
| free-form multi-agent debate | high token cost, often weak signal |
| browser-first retrieval everywhere | costly and high attack surface |
| monolithic CoT prompting as the reasoning core | weak control and poor auditability |
| full theorem prover implementation | too heavy for v1 |
| MCTS everywhere | token sink |

## Token-efficiency rules

Hard rules:

1. never send raw fetched pages to the analyst or writer by default
2. prune before synthesis
3. compress before expensive reasoning
4. operate on evidence packets and proof-relevant subgraphs
5. use small models for planning, routing, pruning, and triage
6. reserve strong models for adversarial contradiction work, insight synthesis, and final writing
7. cache fetched pages, parsed text, evidence packets, and contradiction checks
8. use case memory before starting broad fresh search
9. activate ADEPT-DS only on triggered graph regions
10. escalate to `AGoT` or `MCTS-RAG` only for contested high-value cases

## Accuracy and performance rules

Hard rules:

1. the writer never invents insights
2. no insight is published without a proof tree
3. no `novel` label without novelty gating
4. no confidence score without contradiction pressure
5. no deduction survives if an alternative explanation scores equally and is simpler
6. every insight must declare what would falsify it
7. independence inflation must be checked before confidence promotion
8. the adversary reviews both claims and deductions

## Recommended data model additions

Add to the existing Dossier graph:

- `PROOF_TREE`
- `PROOF_NODE`
- `HYPOTHESIS`
- `HYPOTHESIS_TEST`
- `NOVELTY_SCORE`
- `FRAGILITY_SCORE`
- `ALTERNATIVE_EXPLANATION`
- `COUNTERFACTUAL_TEST`

Suggested proof-node fields:

- node_id
- case_id
- proof_tree_id
- node_type
- statement
- source_evidence_ids
- derived_from_node_ids
- rule_id
- executable_check
- validity_score
- uncertainty

Suggested hypothesis fields:

- hypothesis_id
- case_id
- graph_region_id
- hypothesis_text
- generation_reason
- candidate_rank
- novelty_precheck
- status

## Recommended implementation order

### Phase 1

- keep the current evidence graph and five-role model
- add one-shot planning and compiled task execution
- add pruning and compression
- add case-memory warm start
- add proof-tree schema
- add evidence atomization
- add trigger detection
- add abductive hypothesis generation
- add lightweight proof executor
- add detective-chain rendering

### Phase 2

- add probabilistic rule scoring
- add stronger alternative-hypothesis search
- add formal novelty gate scoring
- add counterfactual falsification suite
- add retrieval and synthesis evaluation harnesses

### Phase 3

- add cross-case graph reasoning
- add stronger source-origin inference
- add rare hard-mode `MCTS-RAG`
- add domain-specific insight templates and rule packs

## Strongest paper and repo set behind this final plan

Core reasoning and synthesis:

- `Graph of Thoughts`: <https://arxiv.org/abs/2308.09687>
- `Adaptive Graph of Thoughts`: <https://arxiv.org/abs/2502.05078>
- `DARK`: <https://arxiv.org/abs/2510.11462>
- `Self-Discover`: <https://arxiv.org/abs/2402.03620>
- `Buffer of Thoughts`: <https://arxiv.org/abs/2406.04271>

Evidence graph and factual grounding:

- `TRACE`: <https://arxiv.org/abs/2406.11460>
- `GEAR`: <https://arxiv.org/abs/1908.01843>
- `GraphFC`: <https://arxiv.org/abs/2503.07282>
- `FactCG`: <https://arxiv.org/abs/2501.17144>
- `NodeRAG`: <https://arxiv.org/abs/2504.11544>

Verification and formal reasoning:

- `Program of Thoughts`: <https://arxiv.org/abs/2211.12588>
- `VeriCoT`: <https://arxiv.org/abs/2511.04662>
- `TabVer`: <https://arxiv.org/abs/2411.01093>
- `PSL`: <https://github.com/linqs/psl>
- `ProbLog`: <https://github.com/ML-KULeuven/problog>
- `DeepProbLog`: <https://github.com/ML-KULeuven/deepproblog>

Planning, memory, and low-token execution:

- `ReWOO`: <https://arxiv.org/abs/2305.18323>
- `Plan-and-Act`: <https://arxiv.org/abs/2503.09572>
- `LLMCompiler`: <https://arxiv.org/abs/2312.04511>
- `Memento`: <https://arxiv.org/abs/2508.16153>
- `Memento` repo: <https://github.com/Agent-on-the-Fly/Memento>

Retrieval quality and token control:

- `Provence`: <https://arxiv.org/abs/2501.16214>
- `OpenProvence`: <https://github.com/hotchpotch/open_provence>
- `LongLLMLingua`: <https://arxiv.org/abs/2310.06839>
- `SmartChunk Retrieval`: <https://arxiv.org/abs/2602.22225>
- `RaDeR`: <https://arxiv.org/abs/2505.18405>

Safety and control:

- `AgentSys`: <https://arxiv.org/abs/2602.07398>
- `AgentSentry`: <https://arxiv.org/abs/2602.22724>
- `AgentSpec`: <https://arxiv.org/abs/2503.18666>

Evaluation:

- `SAFE`: <https://arxiv.org/abs/2403.18802>
- `FActScore`: <https://arxiv.org/abs/2305.14251>
- `OpenFActScore`: <https://github.com/lflage/OpenFActScore>
- `VERISCORE`: <https://arxiv.org/abs/2406.19276>
- `RAGChecker`: <https://arxiv.org/abs/2408.08067>

## Final decision

The final Dossier algorithm plan should be:

- outer system: **BAEGC-lite**
- core reasoning engine: **ADEPT-DS**

If Dossier is supposed to behave like a detective rather than a search engine, this is the right core:

- evidence graph
- abductive hypothesis generation
- deductive proof trees
- executable verification
- defeasible scoring
- counterfactual falsification
- novelty gating
- detective-chain rendering

That is the merged final algorithm direction.
