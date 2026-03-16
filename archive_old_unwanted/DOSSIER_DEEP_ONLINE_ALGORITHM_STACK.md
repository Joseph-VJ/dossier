# Dossier Deep Online Algorithm Stack

Research date: 2026-03-11
Scope: merge the local research files in `F:\research` with a deeper online review of papers, official GitHub repos, and protocol/framework docs.
Goal: make Dossier stronger than the current plan while using fewer LLM tokens.

## Bottom line

Do not build Dossier around one giant "reasoning agent".

Build it around a new hybrid algorithm stack:

**BAEGC: Budgeted Adversarial Evidence Graph Compiler**

BAEGC is not a single paper copied into the product. It is a Dossier-specific composition of the strongest ideas from the local research and the online sources:

- decoupled planning from `ReWOO` and `Plan-and-Act`
- parallel execution from `LLMCompiler`
- graph-shaped evidence modeling from `GEAR`, `TRACE`, and `NodeRAG`
- adaptive reasoning expansion from `AGoT`
- selective hard-case escalation from `MCTS-RAG`
- context pruning from `Provence` / `OpenProvence`
- prompt compression from `LongLLMLingua`
- case-memory reuse from `Memento`
- tool and memory isolation from `AgentSentry`, `AgentSys`, and `MCP` security guidance

This is the strongest path I found because it improves quality and trust while cutting the biggest token sinks:

- repeated planner calls
- sending raw pages to the model
- sequential tool loops for independent subtasks
- global expensive reasoning on every claim
- re-solving patterns the system has already seen before

## What to keep from your current Dossier plan

Keep these as non-negotiable:

- evidence graph as the system of record
- planner / researcher / adversary / analyst / writer separation
- source independence as a first-class algorithm
- support-strength and challenge-strength as separate axes
- deductions must have derivation chains
- explicit gap logging
- deterministic orchestration and validation around every LLM output

These remain the right foundation.

## The new algorithm to use

### BAEGC: Budgeted Adversarial Evidence Graph Compiler

#### Stage 0: Case-memory warm start

Before planning, retrieve similar past investigations, past failure modes, and prior successful source strategies.

Use:

- `Memento` style case bank and case-based reasoning
- simple non-parametric memory first
- parametric retriever later if needed

Why:

- reduces repeated planning tokens
- improves lane selection
- avoids re-learning the same source patterns

#### Stage 1: one-shot structured planning

Generate one structured plan up front:

- objective
- hypotheses
- lanes
- source classes
- stop conditions
- budget

Use:

- `ReWOO` style decoupled reasoning from observation
- `Plan-and-Act` style planner/executor split

Why:

- avoids repeated "think after every tool call" token burn
- produces a reusable plan artifact

Rule:

- planner gets exactly one main call per investigation
- replanning only happens on major contradiction or user challenge

#### Stage 2: compile plan into an execution DAG

Convert the plan into a tool execution graph:

- independent lane searches run in parallel
- fetches and extractions run in parallel where dependencies allow
- only dependency-linked tasks stay sequential

Use:

- `LLMCompiler`

Why:

- cuts latency and redundant prompts
- lets one planner call produce many tool actions
- better than ReAct-only loops for multi-lane investigations

Rule:

- compile once, then execute many
- researcher nodes consume structured task specs, not the whole investigation chat history

#### Stage 3: adaptive retrieval before reasoning

Do not send raw documents to the reasoning model.

Use a retrieval stack:

1. search
2. fetch
3. chunk adaptively
4. prune irrelevant text
5. extract atomic evidence
6. store quotes plus metadata

Use:

- `SmartChunk Retrieval` for adaptive chunk granularity
- `Provence` / `OpenProvence` for context pruning
- `LongLLMLingua` for prompt compression when context is still large

Why:

- strongest direct token savings
- also improves quality by removing noise

Rule:

- the analyst and writer should usually see quote packets, not full pages
- only escalate to larger context when quote packets are insufficient

#### Stage 4: evidence graph materialization

Represent the investigation as a heterogeneous graph, not just a message log.

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

Core edge types:

- supports
- contradicts
- derived_from
- cites
- clustered_with
- belongs_to_lane
- reviewed_by
- falsified_by

Use:

- `TRACE` reasoning-chain idea
- `GEAR` evidence aggregation idea
- `NodeRAG` heterogeneous graph design

Why:

- lets Dossier reason over evidence structures directly
- keeps token usage down because the system can retrieve subgraphs instead of full histories

Important:

- use `NodeRAG` as a design influence, not a full product dependency
- for Dossier, the graph should center on evidence and provenance, not on generic entity extraction theater

#### Stage 5: deterministic claim building before expensive reasoning

Build claims in a deterministic-plus-validated pass:

- cluster equivalent evidence
- assign source class
- compute freshness
- compute independence heuristics
- attach support and contradiction links

Use LLMs only for:

- extraction normalization
- semantic contradiction detection
- cross-evidence deduction

Do not use LLMs for:

- URL normalization
- dedup
- score bookkeeping
- citation linking

#### Stage 6: selective adaptive reasoning

Do not run expensive graph/tree reasoning on all claims.

Use a budget gate:

- if support is strong and challenge is weak, no heavy reasoning
- if claim is contested, sparse, contradictory, or strategically important, expand reasoning

Use:

- `AGoT` for adaptive DAG expansion
- `MCTS-RAG` only for hard unresolved cases

Why:

- `AGoT` allocates compute only where needed
- `MCTS-RAG` is powerful, but too expensive to run globally

Rule:

- default reasoning mode = shallow structured synthesis
- escalation mode = adaptive graph reasoning
- rare escalation mode = retrieval plus tree-search on the hardest contested claims

#### Stage 7: adversarial review in isolated memory

The adversary must not inherit the same full conversational memory as the researchers.

Use:

- `AgentSentry` ideas for tool-return boundary checking
- `AgentSys` ideas for hierarchical memory isolation

Why:

- reduces indirect prompt injection risk from fetched web content
- prevents contaminated tool outputs from propagating across the whole case

Rule:

- untrusted web content stays isolated until sanitized
- adversary receives evidence packets, provenance, and claims, not arbitrary raw execution state

#### Stage 8: compressed final writing

The writer should operate on:

- validated claims
- deductions with derivation chains
- high-severity counter-evidence
- logged gaps

The writer should not read the entire retrieval history unless necessary.

This keeps final generation cheap and reduces hallucination surface area.

## The exact online algorithms and repos to use

### Use now

| Item | Use in Dossier | Why |
|---|---|---|
| `ReWOO` | planner and research execution separation | strong token reduction by decoupling reasoning from observations |
| `Plan-and-Act` | structured planner + executor split | better long-horizon planning than ad hoc loops |
| `LLMCompiler` | compile lane tasks into parallel tool DAGs | lower latency and lower token cost than sequential tool use |
| `TRACE` | reasoning chains over retrieved evidence | better multi-hop evidence selection than dumping all retrieved text |
| `NodeRAG` | heterogenous evidence graph design inspiration | better graph structure and minimal retrieval tokens |
| `Provence` / `OpenProvence` | prune noisy retrieval context | near-zero-cost context reduction before generation |
| `LongLLMLingua` | compress long prompts and evidence packets | major prompt cost reduction without large quality loss |
| `Memento` | case bank for repeated investigation patterns | cheaper and stronger planning through reuse |
| `Pydantic AI` | typed contracts, validation, evals, graph support | safer structured outputs and easier observability |
| `LangGraph` or custom state machine | deterministic orchestration | graph/state workflow is a better fit than agent chat loops |

### Use later

| Item | Use later for | Why later |
|---|---|---|
| `AGoT` | adaptive deeper reasoning on contested claims | strong, but should be gated to avoid cost blowups |
| `MCTS-RAG` | hard-case inference-time search | powerful but too expensive for default use |
| `Microsoft GraphRAG` | offline cross-case indexing and corpus mining | valuable, but heavy for per-investigation live web workflows |
| `MCP` everywhere | standardizing external tools/connectors | useful once Dossier exposes a larger tool ecosystem |
| `RAGChecker` | internal retrieval-plus-generation diagnostics | excellent for evals once the first retrieval pipeline exists |
| `AgentSentry` style defense | robust prompt-injection mitigation | should arrive before exposing broad browser/tool surfaces |
| `AgentSys` style isolated memory | stronger compartmentalization | more relevant once tools and nested workers grow |

### Do not use in V1

| Item | Why not now |
|---|---|
| full RL / offline RL / world models | too far from the current product problem |
| free-form multi-agent debate | expensive and usually lower signal than a dedicated adversary |
| full GraphRAG indexing on every investigation | too costly and slow for live web research |
| CodeAct as the default action model | too much power and attack surface for a trust-first investigation engine |
| MCTS everywhere | token sink |
| unrestricted browser-first retrieval | too costly and too risky; browser should be fallback only |

## Token-saving rules that should be hard-coded

1. Never send raw retrieved pages directly to the analyst or writer.
2. Run pruning before synthesis: retrieval -> pruning -> quote extraction -> graph insertion -> reasoning.
3. Use a smaller model for planning, routing, pruning, compression, and triage.
4. Use the strongest model only for:
   - cross-evidence deduction
   - adversarial contradiction analysis
   - final dossier writing
5. Parallelize independent tool calls by default.
6. Cache:
   - fetched pages
   - parsed text
   - extracted evidence packets
   - search result sets
   - contradiction checks
7. Reuse prior cases through a case bank before issuing fresh wide searches.
8. Escalate reasoning only on contested or high-value claims.
9. Keep the writer on quote packets and graph summaries, not full-doc context.
10. Make browser automation fallback-only.

## Strongest recommended v1 stack

If I had to choose one practical v1 stack today, it would be:

- Orchestration: custom Python state machine or `LangGraph`
- Contracts and validation: `Pydantic AI`
- Provider abstraction: `LiteLLM`
- Planning style: `ReWOO` + `Plan-and-Act`
- Parallel execution: `LLMCompiler` ideas
- Retrieval reduction: `Provence` / `OpenProvence`
- Prompt compression: `LongLLMLingua`
- Evidence chain building: `TRACE`
- Evidence graph schema: `NodeRAG` style heterogeneous graph, adapted for Dossier
- Memory: `Memento` style case bank
- Security hardening: `AgentSentry` and `AgentSys` patterns
- Deep reasoning escalation: `AGoT`
- Rare hard-mode reasoning: `MCTS-RAG`

## My recommended Dossier-specific algorithm design

### Name

**BAEGC-lite** for V1, later evolving to full **BAEGC**

### V1 algorithm definition

`BAEGC-lite = ReWOO planning + LLMCompiler execution + Provence pruning + LongLLMLingua compression + TRACE chain extraction + NodeRAG-style evidence graph + Memento case reuse + selective AGoT escalation + adversarial review`

### Why this is stronger than the current plan

- better planning discipline
- less prompt repetition
- less noisy context
- more parallelism
- better graph structure for evidence reasoning
- reusable case memory
- safer tool boundaries
- more targeted use of expensive reasoning

### Why this uses fewer tokens

- planner thinks once instead of after every tool call
- independent tasks execute in parallel without repeated LLM narration
- pruning happens before synthesis
- only evidence packets reach the large model
- hard reasoning is gated, not global
- repeated investigations reuse memory

## Implementation order

### Phase 1

- keep your current Dossier evidence graph and five-role model
- replace broad ReAct loops with one-shot structured planning
- add plan compilation for parallel lane execution
- add retrieval pruning before evidence extraction
- keep browser automation fallback-only

### Phase 2

- add case-bank memory
- add adaptive reasoning escalation for contested claims
- add isolated adversary memory and tool-return sanitization
- add retrieval and generation eval metrics

### Phase 3

- add offline cross-case graph indexing
- add rare hard-case MCTS-RAG mode
- add stronger source-origin clustering and independence inference

## What I would personally build first

If the objective is strongest product progress per week of work, build these first:

1. `ReWOO` style planner/executor split
2. `LLMCompiler` style parallel tool DAG
3. `Provence` style context pruning
4. `LongLLMLingua` prompt compression
5. `TRACE` style evidence-chain extraction
6. `Memento` style case memory
7. gated `AGoT` for only the hardest claims

That order gives the biggest quality and cost gains earliest.

## Online sources used

Primary papers:

- ReWOO: <https://arxiv.org/abs/2305.18323>
- LLMCompiler: <https://arxiv.org/abs/2312.04511>
- TRACE: <https://arxiv.org/abs/2406.11460>
- GEAR: <https://arxiv.org/abs/1908.01843>
- LongLLMLingua: <https://arxiv.org/abs/2310.06839>
- Provence: <https://arxiv.org/abs/2501.16214>
- Adaptive Graph of Thoughts (AGoT): <https://arxiv.org/abs/2502.05078>
- Plan-and-Act: <https://arxiv.org/abs/2503.09572>
- MCTS-RAG: <https://arxiv.org/abs/2503.20757>
- NodeRAG: <https://arxiv.org/abs/2504.11544>
- AgentSentry: <https://arxiv.org/abs/2602.22724>
- AgentSys: <https://arxiv.org/abs/2602.07398>
- SmartChunk Retrieval: <https://arxiv.org/abs/2602.22225>
- RAGChecker: <https://arxiv.org/abs/2408.08067>

Official or primary GitHub / protocol sources:

- ReWOO repo: <https://github.com/billxbf/ReWOO>
- LLMCompiler repo: <https://github.com/SqueezeAILab/LLMCompiler>
- TRACE repo: <https://github.com/jyfang6/trace>
- LangGraph repo: <https://github.com/langchain-ai/langgraph>
- Pydantic AI repo: <https://github.com/pydantic/pydantic-ai>
- Microsoft GraphRAG repo: <https://github.com/microsoft/graphrag>
- NodeRAG repo: <https://github.com/Terry-Xu-666/NodeRAG>
- LightRAG repo: <https://github.com/HKUDS/LightRAG>
- OpenProvence repo: <https://github.com/hotchpotch/open_provence>
- LLMLingua repo: <https://github.com/microsoft/LLMLingua>
- Memento repo: <https://github.com/Agent-on-the-Fly/Memento>
- MCP specification: <https://modelcontextprotocol.io/specification/2024-11-05/index>

## Final recommendation

For Dossier, the best "new algorithm" is not a bigger agent swarm.

It is a **budgeted evidence compiler**:

- plan once
- compile tasks
- prune aggressively
- reason over an evidence graph
- escalate only when contested
- reuse prior cases
- isolate unsafe tool outputs

That is the highest-signal path I found from the local files plus the deeper online research.
