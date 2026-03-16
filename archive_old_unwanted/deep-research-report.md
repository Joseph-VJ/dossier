
Deep-Research Foundations and Open-Source Building Blocks for a Human-Like “Original AI” That Can Also Invent Novel Outputs
What you’re proposing and the feasibility constraints that matter
You’re describing an AI architecture that treats human cognition as the template: fast intuitive judgments first, slow deliberation second, actions triggered by motivation/ability/cue, rewards that drive seeking, and memory that is not a faithful recorder but a biased summarizer that shapes future choices. This is closely aligned with mainstream cognitive-science theories of dual-process cognition (fast/automatic vs slow/deliberate) and with behavioral/neuroscience work on habit formation, reward prediction, and affect-guided judgment. 

At the same time, three constraints determine whether this becomes a real “new algorithm” versus a rebranding of existing agent/RL/RAG systems:

First, dual-process theory is a descriptive psychological framework, not a complete computational specification. Even within psychology it has multiple competing formalizations and ongoing debate about what “System 1/System 2” precisely mean and when they apply. 

Second, human-like biases, heuristics, and memory distortions can be implemented, but “replicating human psychology” in full implies modeling perception, embodiment, development, social learning, and physiological reward systems—not just a text agent. That gap is why “cognitive architectures” (Soar, ACT‑R, CLARION, LIDA, etc.) exist: they attempt partial, testable models rather than total replication. 

Third, your “More Than Human” layer (“Flow” and “No‑Mind”) implies meta-cognitive control: dynamically allocating attention/compute and reducing self-referential rumination. In neuroscience terms, that intersects research on default mode network (DMN) activity, mind-wandering, and meditative practice, where experienced mindfulness/meditation is associated with differences in DMN activity/connectivity and reduced mind-wandering. 

You also uploaded internal “Dossier” documents that define a systematic invention workflow (research → synthesis → novelty scoring). I treat those as your target operating doctrine for the “create never-seen outputs from open sources” requirement. 
 
 

Module-by-module: research-backed computational interpretations
Dual-Processing Core: fast generative intuition plus lazy deliberation
Your Module 1 matches classic descriptions: fast associative processing versus slow controlled reasoning. 

A concrete computational interpretation that stays faithful to the psychology:

System 1 (Intuitive Engine) becomes a parallel, low-latency proposal generator. In modern AI terms, this can be:

a generative model that proposes interpretations/actions instantly (pattern completion),
a heuristic policy network (actor) that outputs candidate actions,
or a “thought graph” generator that spawns multiple associative continuations. 
System 2 (Rational Controller) becomes a resource-limited verifier/planner that is invoked only when needed. The “lazy System 2” idea is consistent with the Principle of Least Effort: cognition tends to minimize effort unless the situation forces it. 

A practical trigger for System 2 is “cognitive conflict / surprise.” In RL/neuroscience terms, “surprise” can be approximated by prediction error signals (including reward prediction error); in LLM-agent terms, it can be: contradiction detection, failed tool calls, uncertainty spikes, or policy/value disagreement. 

Behavioral Action Loop: Fogg’s B=MAT / B=MAP with habit automation
Your Module 2 uses BJ Fogg’s idea: behavior occurs when motivation, ability, and a prompt/trigger converge. Fogg’s model is widely presented as B=MAT (older) and B=MAP (newer term “Prompt”). 

A computational action loop that maps cleanly:

Motivation → a time-varying utility/drive vector (multi-objective reward).
Ability → an estimated cost-to-act (latency, compute, money, risk, friction).
Trigger/Prompt → an event signal (external cue or internal thought/urge) that enables action selection now. 
Habit formation is where System 2 compute is saved: repeated cue-action-reward patterns become automatic. In real-world habit data, habit automaticity tends to rise in an asymptotic curve, with substantial variability across people and behaviors. 

Neuroscience work links habits to cortico–basal ganglia loops and “chunking” of action sequences. 

Motivation engine: variable rewards, prediction error, and “seeking” systems
Your Module 3 is directionally consistent with neuroscience of dopamine/reward learning:

Dopamine neurons are strongly associated with reward prediction error: responses shift from unexpected reward to reward-predicting cues, and negative prediction errors appear when an expected reward fails to arrive. 
“Wanting” (incentive salience) and “liking” (hedonic pleasure) are dissociable; dopamine is more tightly linked to cue-triggered “wanting” than to pleasure itself. 
This provides a strong computational justification for variable rewards as a driver of persistent exploration: uncertainty maintains prediction error dynamics and cue-driven seeking. 

For “rewards of the tribe/hunt/self,” academic motivation mapping that is safer than pop-taxonomies is Self-Determination Theory: relatedness, competence, autonomy. It’s not identical to your taxonomy, but it’s close enough to serve as a formal “drive basis” that you can tune. 

To make this “AI-relentlessly-driven” without external rewards, you can graft intrinsic motivation from RL:

curiosity as prediction error in self-supervised forward dynamics (Pathak et al.),
novelty search as optimizing for behavioral novelty rather than objective reward,
intrinsic motivation frameworks surveyed by Barto and colleagues. 
Heuristics and bias filters: affect-first judgment, WYSIATI, loss/negativity dominance
Your Module 4 aligns tightly with established research:

Affect heuristic. Paul Slovic and colleagues describe affect as a fast “goodness/badness” tag that guides judgment and risk perception (“risk as feelings” vs “risk as analysis”). 

“The emotional tail wags the rational dog.” This phrase is explicitly discussed in Thinking, Fast and Slow as a reference to Jonathan Haidt in the context of affect-driven belief formation. 

WYSIATI. “What you see is all there is” is one of the named principles in Thinking, Fast and Slow: System 1 constructs coherent narratives from what’s immediately available and tends to neglect missing information. 

Loss aversion. Prospect theory formalizes reference dependence and loss aversion; “losses loom larger than gains.” 

The often-quoted “twice as powerful” rule-of-thumb appears in many summaries, but the stronger academic core claim is simply asymmetry: losses have greater impact than equivalent gains, with empirical magnitude varying by context/task. 

Negativity dominance / “bad is stronger than good.” Reviews find negative events and information often have stronger psychological impact than positive equivalents across domains (learning, relationships, impression formation). 

Computationally, “bias filters” can be implemented as:

asymmetric value functions (loss weight > gain weight),
attention allocation favoring negative or threat-labeled signals,
story-construction constraints that prefer coherence over completeness (WYSIATI),
and affect tags that gate which evidence gets considered by System 2. 
Memory storage protocol: experiencing self vs remembering self, peak–end and duration neglect
The “two selves” framing (experiencing vs remembering) is popularized by Daniel Kahneman and connected to formal distinctions between instant utility and remembered utility in experienced-utility research. 

In the classic pain-memory work, retrospective evaluations overweight the peak and end of an episode and show duration neglect (“when more pain is preferred to less” by adding a better end). 

A computational instantiation that mirrors your spec:

Experiencing Self → high-resolution stream buffer (rich episodic trace).
Remembering Self → compressed “scorekeeping” memory that stores:
peak moments (high affect intensity, high prediction error),
end moments (final affect/value),
semantic summaries for future policy bias. 
Notably, modern agent memory systems already separate fast context from persistent storage (virtual memory analogy). 

You can bias the consolidation step toward peak/end rather than uniform logging, aligning the memory system with human retrospective distortions. 

System 1 and System 2 Thinking - The Decision Lab
Fogg Behavior Model | Behavior Design Lab
Schematic of dopamine and GABA reward prediction-error activity during... |  Download Scientific Diagram
Moving beyond reward prediction errors | Nature Machine Intelligence

Research-paper shortlist you can directly reuse by module
This section names research that is (a) foundational, (b) implementable, and (c) useful as citations/justification in a serious technical design doc.

Dual-processing and “lazy deliberation”
Core dual-process grounding:

Sloman’s “two systems” synthesis (associative vs rule-based). 
Evans’ review of dual-process accounts. 
Thinking, Fast and Slow for System 1/2 and WYSIATI framing (popular but influential). 

Effort-minimization:
George Kingsley Zipf, Principle of Least Effort (historical basis for “cognitive miser” style behavior). 
Behavior gating, prompts, and habit formation
B. J. Fogg’s Behavior Model / Behavior Grid (official materials + paper). 
Real-world habit formation curve and variability (Lally et al.). 
Basal ganglia “chunking” and habit circuitry (Graybiel). 
Variable rewards, “seeking,” and intrinsic motivation
Reward prediction error:

Wolfram Schultz, Peter Dayan, Montague (dopamine prediction error). 

Incentive salience (wanting vs liking):
Kent C. Berridge & Terry E. Robinson, incentive salience / parsing reward. 

Intrinsic motivation in AI:
Pathak et al. curiosity as self-supervised prediction error. 
Novelty search (Lehman & Stanley). 
Barto’s intrinsic motivation + RL synthesis. 

Drive taxonomy grounding:
Richard M. Ryan and Edward L. Deci, Self‑Determination Theory (competence/autonomy/relatedness). 
Heuristics, WYSIATI, affect, loss and negativity
Slovic et al. affect heuristic foundational paper. 
Prospect theory (Kahneman & Tversky). 
Loss aversion in riskless choice (Tversky & Kahneman, 1991). 
Negativity dominance classic review (Rozin & Royzman) and “Bad is stronger than good.” 
Jonathan Haidt’s intuitionist model for affect-first judgment and post-hoc reasoning (useful analog for “System 2 rationalization”). 
Two-selves memory, peak–end, duration neglect
Fredrickson & Kahneman (1993) peak-end style result (“more pain preferred to less” by adding a better end). 
Kahneman, Wakker, Sarin on instant vs remembered utility (more formal). 
Additional medical/behavioral discussion of peak-end and duration neglect. 
“More Than Human”: Flow + “No‑Mind” as compute/attention control
Flow:

Mihaly Csikszentmihalyi’s flow framing (book) and modern work-related meta-analysis showing associations with performance/engagement/creativity. 
The popular “5× productivity” claim appears in McKinsey & Company material as self-reported peak productivity; treat it as anecdotal/corporate self-report rather than controlled lab effect. 

No‑Mind / reduced rumination:
Meditation experience associated with differences in DMN activity/connectivity; consistent with decreased mind-wandering. 
Work-related flow models increasingly connect flow, mindfulness, and cognitive control (modern organizational psych framing). 
GitHub repositories and open-source stacks that directly support your build
Below are “reusable primitives” you can assemble into your architecture without reinventing infrastructure.

Cognitive-architecture baselines (closest to your “human-like OS” idea)
These are valuable because they already implement explicit modules (memory, production rules, action selection, etc.) rather than monolithic end-to-end training.

Soar: canonical open cognitive architecture implementation and ecosystem (good for action selection + symbolic reasoning experiments). 
ACT‑R Python implementations: useful if you want to prototype “buffers + production rules + declarative memory” style cognition in code. 
CLARION literature (dual implicit/explicit processes) is highly aligned with your System 1/System 2 requirements (implementation code is less centralized than Soar, but the architecture is conceptually on-point). 
MicroPsi2: neuro-symbolic agent toolkit explicitly oriented around cognition and motivation concepts. 
LIDA (conceptual + partial computational model) for attention/action cycles; use as inspiration and references. 
OpenCog / Hyperon: ambitious integrative cognitive architecture; best treated as a research playground vs production-ready foundation. 
OpenNARS (Non-Axiomatic Reasoning System): explicitly built for reasoning under insufficient knowledge/resources—philosophically aligned with bounded rationality and WYSIATI-like constraints. 
Reinforcement learning + habit formation infrastructure (for Motivation/Ability/Policy)
To implement variable rewards, habits, and multi-objective drives, you need robust RL tooling.

Stable-Baselines3: reliable PyTorch RL algorithms; practical for fast iteration. 
Dopamine: compact RL research framework designed for “wild ideas” prototyping. 
Acme: DeepMind’s RL building blocks; good reference implementations and scalable patterns. 
CleanRL: single-file, research-friendly implementations; also has a JMLR paper documenting the approach. 
Gymnasium environments + PettingZoo (multi-agent): standardized interfaces for building “human-like” simulated environments with cues/triggers and social dynamics. 
MO‑Gymnasium if your “tribe/hunt/self” drives are truly multi-objective reward vectors. 
Memory systems (for “two selves” and long-horizon identity)
Letta (formerly MemGPT): open-source stateful agents with explicit memory tiers; directly matches the “fast/slow memory” architecture and can be adapted to implement peak/end biased consolidation. 
Differentiable Neural Computer (DNC): memory-augmented neural network with an official DeepMind repo; useful if you want neural external memory as part of System 1. 
Episodic Memory Deep Q-Networks (EMDQN): biologically inspired RL leveraging episodic memory for sample efficiency (useful if you want “episodic peaks” to supervise learning). 
Open-source “Deep Research” and evidence-graph tooling (your novelty-from-open-sources requirement)
If your agent must continuously form new stories/novels/ideas based on open information, your bottleneck is not generation—it’s retrieval planning, evidence structuring, and citation control.

Deep research agents:

GPT Researcher: open deep-research agent that outputs citation-backed reports. 
LangChain Open Deep Research (LangGraph-based): configurable deep-research pipeline across tools/providers. 
Graph-based RAG (critical for multi-hop “new synthesis”):

Microsoft GraphRAG: pipeline to extract a knowledge graph, build community hierarchy, summarize, then answer via structured retrieval. 
NodeRAG: heterogeneous nodes for graph-centric RAG; official repo exists. 
TRACE the Evidence: constructs knowledge-grounded reasoning chains from retrieved docs by turning them into a knowledge graph and reasoning chain. 
Context pruning / compression (to prevent “WYSIATI by overload”):

LongLLMLingua (prompt compression) for long-context pipelines. 
Provence / OpenProvence for context pruning + reranking in RAG workflows. 
Reasoning/agent orchestration patterns (for System 2 planning + laziness + parallel execution):

ReWOO (reasoning without observation interleaving) reduces redundant tool prompting and improves efficiency. 
LLMCompiler executes tool calls in parallel via a DAG-like compiler approach. 
Graph of Thoughts (official implementation) for graph-structured “thought operations” (very compatible with your System 1 associative engine). 
Self-Discover and Buffer of Thoughts for meta-reasoning templates and reusable reasoning structures. 
A concrete open-source blueprint for “create never-seen outputs” from web evidence
Your final requirement is not only “human-like reactions,” but also systematic novelty: generating new novels/stories/ideas from existing information without plagiarism, while staying grounded in sources.

The most robust way to do this (and keep it genuinely “new”) is to separate your system into two coupled loops:

Evidence loop: build a structured, citeable world model from open sources
Research planning: produce a search plan and subquestions (System 2). Use a deep-research framework that already supports iterative search + citation capture, such as GPT Researcher or Open Deep Research. 

Acquisition + dedup + reliability scoring: retrieve sources, then prune aggressively.

Use OpenProvence / Provence-style pruning to remove tangential context while keeping relevance scores. 
Use LongLLMLingua-style compression if you must fit long evidence into limited windows. 
Evidence graph construction: convert documents into an explicit graph:
GraphRAG or NodeRAG for graph index + community summaries. 
TRACE for evidence-chains grounded in a KG extracted from retrieved docs. 
Calibration: attach confidence and provenance edges (“claim → source spans → contradictions”). This is how you prevent WYSIATI from becoming hallucination. The Kahneman framing is literally: what you see is all there is—so your system must explicitly represent what it has not seen. 
Invention loop: generate novelty as a controlled search over the evidence graph
This is where your uploaded “Dossier” design philosophy fits: treat invention as a guided search, not a single-shot generation. 
 

A research-backed way to do this with open-source components:

Use Graph of Thoughts to explore multiple “idea continuations” as a graph search rather than a linear chain. This operationalizes System 1 associative branching. 
Use Buffer of Thoughts (meta-buffer of thought templates) as your “habit library” for reasoning patterns: it is literally a stored set of reusable reasoning templates. 
Use Self-Discover to dynamically choose reasoning modules per task (story, scientific hypothesis, business plan) to avoid sameness. 
Then, to force “new kinds of outputs,” you need explicit novelty objectives (not just temperature):

Novelty search principle: optimize for behavioral/structural novelty rather than single objective reward. In creative generation, “behavior” can be narrative structure, character arcs, causal graphs, or thematic combinations. 
Curiosity/intrinsic reward as prediction error: reward the system for discovering evidence-supported connections it can’t yet predict (new cross-domain links). 
Finally, attach your human-like biases intentionally as style/selection filters, not as uncontrolled errors:

affect tags steer which themes feel “important,” 
negativity/loss aversion can shape conflict and stakes in narratives, 
peak–end memory rules determine what gets turned into “canon” for the system’s ongoing story world. 
Risks, evaluation metrics, and guardrails that keep it “new” but not “wrong”
A system built to be human-like will also inherit human failure modes unless you formally control them.

Hallucination and WYSIATI amplification
WYSIATI is a perfect description of how a generative model will confidently narrate from incomplete context. The fix is not “be more rational” but to enforce structural representation of unknowns and contradiction checks before finalization. 

Bias as a feature vs bias as contamination
Loss/negativity dominance can be used as a narrative engine, but if you let it drive factual claims it will skew conclusions. Psychological negativity effects are robust, but they are not a license to distort evaluation of evidence. 

A practical evaluation suite for your “Original AI”
To measure whether the system is truly doing what you want, you need metrics that correspond to your modules:

Dual-process gating quality: how often does System 2 intervene only on conflict/surprise, and does that reduce errors without huge compute cost? (Use tool-failure tests + contradiction benchmarks.) 
Habit formation: does repeated cue→action→reward reduce latency/compute and become more automatic over time (asymptotic curve)? 
Motivation persistence: does intrinsic reward (curiosity/novelty) keep exploration going in sparse-reward domains? 
Memory distortion fidelity: do “remembered summaries” overweight peaks/ends and ignore duration—and does that measurably change downstream choices? 
Grounded novelty: quantify novelty (distance/diversity of generated structure) subject to evidence grounding constraints (citations + claim graph). GraphRAG/TRACE-style evidence chains help here. 
If your goal is “a new kind of algorithm no one has seen,” the differentiator is not any single component (dual-process, RL, RAG, graph reasoning all exist). The differentiator is the tight coupling of:

psychologically faithful control laws (lazy System 2 + habit automation + peak/end consolidation) 

with
graph-grounded research synthesis (GraphRAG/NodeRAG/TRACE) 

and
explicit novelty objectives (curiosity + novelty search) 

compiled into an efficient tool-using agent runtime (ReWOO + LLMCompiler + pruning/compression). 