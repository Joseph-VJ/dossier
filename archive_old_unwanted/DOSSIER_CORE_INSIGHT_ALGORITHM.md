# Dossier Core Insight Algorithm

Research date: 2026-03-11
Purpose: define the new core algorithm for Dossier's deepest differentiator:

**derive novel conclusions from evidence that are not explicitly stated in any single source, while staying traceable, adversarially reviewable, and token-efficient**

This file is the focused follow-up to `DOSSIER_DEEP_ONLINE_ALGORITHM_STACK.md`.

## Bottom line

The broad stack is not enough.

Dossier needs a dedicated core reasoning algorithm for **insight synthesis**.

My recommendation is to build a new Dossier-native core:

**ADEPT: Abductive-Deductive Evidence Proof Trees**

ADEPT is the reasoning heart.

The broader runtime stack remains:

- `ReWOO` / `Plan-and-Act` for low-token planning
- `LLMCompiler` for parallel task execution
- `TRACE` / `NodeRAG` / evidence graph structures for evidence storage
- `Provence` / `LongLLMLingua` for token reduction
- `AgentSys` / `AgentSentry` / `AgentSpec` for safe tool boundaries

But the thing that makes Dossier stronger than other deep-research systems is ADEPT.

## What ADEPT is trying to do

Standard deep-research systems do this:

- search
- retrieve
- summarize
- cite

Dossier should do this instead:

- search
- extract atomic evidence
- connect evidence into a graph
- generate candidate hidden explanations
- test those explanations against the graph
- reject weak ones
- surface only the novel conclusions that survive proof and falsification pressure

That is not normal summarization.
That is **abductive hypothesis generation plus deductive proof plus adversarial falsification**.

## The core insight

Your product idea is correct:

the best output is often not "what the sources say", but "what becomes true or likely when the sources are combined".

That means Dossier needs to reason in three modes:

1. **Deduction**
   - Given established facts and rules, what follows?
2. **Abduction**
   - What hidden explanation best accounts for these facts together?
3. **Defeasible revision**
   - What should be weakened or withdrawn if stronger counter-evidence appears?

Most current deep-research tools barely do mode 1, perform mode 2 badly, and mostly ignore mode 3.

ADEPT is designed to do all three.

## The new algorithm

## ADEPT: Abductive-Deductive Evidence Proof Trees

### High-level definition

ADEPT is a graph-first reasoning algorithm that:

1. atomizes evidence into typed facts
2. constructs candidate hidden hypotheses from cross-evidence patterns
3. builds proof trees for and against each hypothesis
4. runs symbolic, executable, and probabilistic verification passes
5. stress-tests each conclusion with counterfactual and adversarial checks
6. only publishes insights that survive the gates

### Why this is stronger than the current design

The current Dossier plan already has an `Analyst` agent and derivation chains.

ADEPT makes that layer much stronger by adding:

- explicit abductive hypothesis generation
- proof-tree construction instead of plain narrative reasoning
- symbolic or quasi-symbolic verification where possible
- novelty detection
- counterfactual stress tests
- defeasible reasoning and downgrade logic

This turns "interesting insight generation" into a more defensible reasoning system.

## ADEPT pipeline

### Phase 1: Evidence atomization

Convert evidence into small, typed units:

- entity facts
- numeric facts
- temporal events
- causally suggestive events
- source claims
- contradictions
- gaps

Each atom gets:

- source id
- origin cluster id
- lane
- time
- source class
- freshness
- extraction confidence
- support or contradiction relation

Use from research:

- `TRACE` for evidence-backed reasoning chains
- `GraphFC` for claim and evidence graph decomposition
- `FactCG` for document-level graph reasoning
- `NodeRAG` as the heterogeneous node design pattern

Why:

- the LLM should not reason over full pages
- it should reason over well-formed atomic evidence

### Phase 2: Insight trigger detection

Before expensive reasoning, detect whether a region of the graph is worth synthesis.

Trigger conditions:

- multiple independent weak signals point at the same possible conclusion
- timeline anomalies exist
- cross-lane events align unusually well
- there is a contradiction that implies a hidden cause
- an expected source or event is missing
- the same source-origin cluster is inflating apparent certainty

If no trigger exists, do not run deep insight synthesis.

This is a major token-saving gate.

### Phase 3: Abductive hypothesis generation

This is the most important new piece.

Given evidence atoms A, B, C, generate candidate hidden hypotheses H1..Hn that would best explain them together.

Examples:

- "the CEO replacement was likely strategic preparation for litigation"
- "the product launch delay was likely caused by regulatory or reliability issues"
- "the public narrative of growth is inconsistent with internal distress indicators"

Use from research:

- `DARK` as the conceptual inspiration for combining deduction and abduction
- `AGoT` for adaptive graph expansion only where the graph looks promising
- `Graph of Thoughts` for non-linear combination of evidence fragments
- `Self-Discover` and `Buffer of Thoughts` for reusable reasoning templates

Important rule:

The LLM does not output one final answer.
It outputs a **small candidate set of hypotheses**.

### Phase 4: Deductive proof-tree construction

For each candidate hypothesis, build a proof tree:

- premises
- intermediate inferences
- final conclusion
- alternative explanations
- explicit missing assumptions

Tree node types:

- observed fact
- derived fact
- assumption
- rule
- contradiction
- uncertainty marker

Proof edges:

- entails
- supports
- weakly supports
- contradicts
- depends_on
- undermines

Use from research:

- `Graph of Thoughts`
- `GraphFC`
- `VeriCoT` for logic-checking inspiration
- `TabVer` for natural-logic and arithmetic verification ideas

Important rule:

Dossier should store **proof trees**, not only prose derivation chains.

The prose chain shown to the user is a rendered view of the proof tree.

### Phase 5: Symbolic and executable verification

Not every reasoning step should be trusted as pure language output.

ADEPT should route verifiable subproblems into deterministic checks.

Use symbolic or executable verification for:

- dates and temporal ordering
- arithmetic and ratios
- threshold checks
- count aggregation
- set overlap
- identity or alias normalization
- explicit rule application

Use from research:

- `Program of Thoughts` for externalized computation
- `ProbLog` / `DeepProbLog` / `PSL` as inspiration for uncertain rule systems
- `AgentSpec` for explicit runtime rules

Practical recommendation:

For V1, do not build a full theorem prover.

Build a **lightweight proof executor**:

- numeric functions
- temporal reasoning functions
- rule predicates
- source-independence constraints
- contradiction predicates

That gets you most of the value with much lower complexity.

### Phase 6: Defeasible and probabilistic scoring

Some insights are not strictly proven.
They are best-supported explanations under uncertainty.

This requires more than binary true or false.

ADEPT should score each proof tree with:

- deductive validity score
- abductive explanatory score
- independence strength
- contradiction pressure
- novelty score
- falsifiability score
- fragility score

Use from research:

- `PSL` for soft probabilistic rule weighting
- `ProbLog` and probabilistic argumentation ideas for uncertain proof support
- default and defeasible reasoning benchmarks as warning signs that LLMs alone are not sufficient here

Practical recommendation:

Use LLMs to propose rules and links.
Use deterministic or probabilistic engines to score them.

This follows the same lesson seen in causal discovery:

LLMs should guide the search, not be the final authority on formal structure.

### Phase 7: Counterfactual falsification

An insight is not strong unless it survives stress.

For each candidate insight, run:

1. **Leave-one-premise-out test**
   - does the insight collapse if one evidence atom disappears?
2. **Leave-one-origin-cluster-out test**
   - does the insight depend on one underlying source masquerading as many?
3. **Alternative-hypothesis test**
   - can another explanation account for the same evidence just as well?
4. **Contradiction insertion test**
   - if the strongest known counter-evidence is injected, does the conclusion survive, weaken, or fail?
5. **Missing-evidence sensitivity test**
   - what one missing fact would most change the conclusion?

This is where Dossier becomes more like a careful analyst than a summarizer.

### Phase 8: Novelty gate

Dossier must know when an "insight" is actually novel versus when it is merely restating a source.

An insight should be labeled `novel` only if:

- it is not explicitly stated in any source quote
- it requires at least two independent evidence clusters or two distinct research lanes
- it has a non-trivial proof tree with intermediate inferences
- it survives the counterfactual stress tests above

Novelty scoring should include:

- explicit-statement overlap score
- cross-lane synthesis score
- source-independence span
- inference-depth score

If the overlap with a source is too high, downgrade from:

- `novel deduction`

to:

- `strong synthesis`

This prevents fake novelty.

### Phase 9: Detective-chain rendering

The user should see a human-readable chain:

1. Fact A from source X
2. Fact B from source Y
3. Fact C from source Z
4. Why these facts fit together
5. Alternative explanation considered
6. Why the chosen explanation is stronger
7. What would falsify it

This is the output layer, not the reasoning layer itself.

The important thing is that it is rendered from the proof tree.

## The stronger main stack

## Keep as the outer runtime stack

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
- `AgentSys`
- `AgentSentry`
- `AgentSpec`

## Add as the deeper reasoning stack

- `ADEPT` as the new Dossier-native core
- `AGoT` for adaptive graph expansion
- `GraphFC` for claim graph decomposition
- `DARK` as conceptual guidance for joint deductive + abductive reasoning
- `Program of Thoughts` for numeric and executable proof steps
- `PSL` or `ProbLog` style uncertain reasoning
- `Buffer of Thoughts` for reusable insight templates
- `Self-Discover` for task-appropriate reasoning structure selection
- `FactCG` for graph-based grounded fact checking

## Add as the evaluation stack

- `FActScore` / `OpenFActScore`
- `SAFE`
- `RAGChecker`
- `VERISCORE`

These should be used to evaluate Dossier output, not as the main insight engine itself.

## The exact Dossier-native algorithm I recommend

### Name

**ADEPT-DS**

Short for:

**Abductive-Deductive Evidence Proof Trees for Dossier Synthesis**

### Definition

`ADEPT-DS = Evidence Atomization + Trigger Detection + Abductive Hypothesis Generation + Deductive Proof Trees + Executable Verification + Probabilistic/Defeasible Scoring + Counterfactual Falsification + Novelty Gating + Detective-Chain Rendering`

### Why this is better than standard deep research

It is better than standard deep-research systems because it does not stop at retrieval or contradiction detection.

It tries to answer:

- what hidden explanation best accounts for the total evidence?
- what follows if these facts are jointly true?
- which explanation survives the strongest alternative?
- what part of the conclusion is actually novel?

That is a much stronger product thesis.

## The token-efficiency strategy

This deeper reasoning layer can become expensive if built badly.

So ADEPT-DS must be budgeted.

### Hard token rules

1. Run abductive hypothesis generation only on graph regions with insight triggers.
2. Limit hypotheses per region to a small beam.
3. Run symbolic and executable checks before any second-pass LLM reflection.
4. Use `Buffer of Thoughts` or `Self-Discover` structures instead of regenerating reasoning templates every time.
5. Retrieve proof-relevant subgraphs, not whole case history.
6. Keep proof executor deterministic.
7. Escalate to `AGoT` only for contested or high-value graph regions.
8. Escalate to `MCTS-RAG` only for rare, unresolved hard cases.

This is how you get both better insight quality and lower cost.

## What to build first

### V1

- evidence atomizer
- insight triggers
- hypothesis generator
- proof-tree schema
- numeric and temporal proof executor
- novelty gate
- detective-chain renderer

### V2

- soft probabilistic rule engine using `PSL`-style scoring
- stronger alternative-hypothesis search
- source-origin abduction patterns
- proof-fragility metrics

### V3

- richer defeasible rule learning
- domain-specific reasoning templates
- adaptive learned case selector for insight regions
- cross-case deduction over prior dossiers

## What not to do

- do not let the writer invent insights
- do not treat every synthesis as a novel conclusion
- do not rely on one monolithic CoT prompt
- do not run tree search on every claim
- do not let raw web text directly shape the main reasoning memory
- do not trust LLM causal judgment without verification pressure

## Recommended architecture relationship

Use this split:

- `BAEGC-lite` from the broader stack manages planning, retrieval, token control, and orchestration
- `ADEPT-DS` becomes the deep reasoning kernel inside the `Analyst` phase

In short:

- `BAEGC-lite` gets the right evidence cheaply
- `ADEPT-DS` turns that evidence into real insight

That is the cleanest architecture I found.

## The strongest papers and repos for this idea

Core reasoning and synthesis:

- `Graph of Thoughts`: <https://arxiv.org/abs/2308.09687>
- `Adaptive Graph of Thoughts`: <https://arxiv.org/abs/2502.05078>
- `DARK`: <https://arxiv.org/abs/2510.11462>
- `Self-Discover`: <https://arxiv.org/abs/2402.03620>
- `Buffer of Thoughts`: <https://arxiv.org/abs/2406.04271>

Evidence graph, claim graph, and factual grounding:

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

Memory, planning, and low-token execution:

- `ReWOO`: <https://arxiv.org/abs/2305.18323>
- `Plan-and-Act`: <https://arxiv.org/abs/2503.09572>
- `LLMCompiler`: <https://arxiv.org/abs/2312.04511>
- `Memento` / `AgentFly`: <https://arxiv.org/abs/2508.16153>
- `Memento` repo: <https://github.com/Agent-on-the-Fly/Memento>

Context reduction and retrieval quality:

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

## Final recommendation

If your core idea is that Dossier should behave more like a detective than a search engine, then the product should be built around:

- an evidence graph
- an abductive hypothesis generator
- a deductive proof-tree builder
- executable verification
- defeasible scoring
- counterfactual stress tests
- novelty gating

That is the right core algorithm.

For Dossier, I would make **ADEPT-DS** the center of the `Analyst` layer and keep the rest of the stack in service of it.
