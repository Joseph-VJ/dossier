# Deep-Research Foundations and Open-Source Building Blocks for a Human-Like “Original AI” That Can Also Invent Novel Outputs

## What you’re proposing and the feasibility constraints that matter

You’re describing an AI architecture that treats human cognition as the template: fast intuitive judgments first, slow deliberation second, actions triggered by motivation/ability/cue, rewards that *drive seeking*, and memory that is *not a faithful recorder* but a biased summarizer that shapes future choices. This is closely aligned with mainstream cognitive-science theories of **dual-process cognition** (fast/automatic vs slow/deliberate) and with behavioral/neuroscience work on **habit formation**, **reward prediction**, and **affect-guided judgment**. citeturn2search36turn2search37turn19search0turn10search5turn10search3turn16search4

At the same time, three constraints determine whether this becomes a real “new algorithm” versus a rebranding of existing agent/RL/RAG systems:

First, **dual-process theory is a descriptive psychological framework, not a complete computational specification**. Even within psychology it has multiple competing formalizations and ongoing debate about what “System 1/System 2” precisely mean and when they apply. citeturn2search33turn2search36turn2search37

Second, **human-like biases, heuristics, and memory distortions can be implemented**, but “replicating human psychology” in full implies modeling perception, embodiment, development, social learning, and physiological reward systems—not just a text agent. That gap is why “cognitive architectures” (Soar, ACT‑R, CLARION, LIDA, etc.) exist: they attempt partial, testable models rather than total replication. citeturn3search2turn3search6turn3search21turn3search4turn3search3turn3search7

Third, your “More Than Human” layer (“Flow” and “No‑Mind”) implies **meta-cognitive control**: dynamically allocating attention/compute and reducing self-referential rumination. In neuroscience terms, that intersects research on **default mode network (DMN)** activity, mind-wandering, and meditative practice, where experienced mindfulness/meditation is associated with differences in DMN activity/connectivity and reduced mind-wandering. citeturn2search35turn2search31turn13search19

You also uploaded internal “Dossier” documents that define a systematic invention workflow (research → synthesis → novelty scoring). I treat those as your *target operating doctrine* for the “create never-seen outputs from open sources” requirement. fileciteturn0file0 fileciteturn0file1 fileciteturn0file2

## Module-by-module: research-backed computational interpretations

### Dual-Processing Core: fast generative intuition plus lazy deliberation

Your Module 1 matches classic descriptions: fast associative processing versus slow controlled reasoning. citeturn2search36turn2search37turn19search0

A concrete computational interpretation that stays faithful to the psychology:

**System 1 (Intuitive Engine)** becomes a *parallel, low-latency proposal generator*. In modern AI terms, this can be:
- a generative model that proposes interpretations/actions instantly (pattern completion),
- a heuristic policy network (actor) that outputs candidate actions,
- or a “thought graph” generator that spawns multiple associative continuations. citeturn4search4turn4search0turn4search8

**System 2 (Rational Controller)** becomes a *resource-limited verifier/planner* that is invoked only when needed. The “lazy System 2” idea is consistent with the **Principle of Least Effort**: cognition tends to minimize effort unless the situation forces it. citeturn11search4turn11search12turn19search0

A practical trigger for System 2 is “cognitive conflict / surprise.” In RL/neuroscience terms, “surprise” can be approximated by prediction error signals (including reward prediction error); in LLM-agent terms, it can be: contradiction detection, failed tool calls, uncertainty spikes, or policy/value disagreement. citeturn10search3turn15search2turn14search0

### Behavioral Action Loop: Fogg’s B=MAT / B=MAP with habit automation

Your Module 2 uses BJ Fogg’s idea: behavior occurs when **motivation**, **ability**, and a **prompt/trigger** converge. Fogg’s model is widely presented as B=MAT (older) and B=MAP (newer term “Prompt”). citeturn0search16turn0search17turn0search20

A computational action loop that maps cleanly:

- **Motivation** → a time-varying utility/drive vector (multi-objective reward).
- **Ability** → an estimated cost-to-act (latency, compute, money, risk, friction).
- **Trigger/Prompt** → an event signal (external cue or internal thought/urge) that enables action selection *now*. citeturn0search16turn0search20

Habit formation is where System 2 compute is saved: repeated cue-action-reward patterns become automatic. In real-world habit data, habit automaticity tends to rise in an asymptotic curve, with substantial variability across people and behaviors. citeturn10search0turn10search15turn10search7

Neuroscience work links habits to cortico–basal ganglia loops and “chunking” of action sequences. citeturn10search5turn10search8turn10search27

### Motivation engine: variable rewards, prediction error, and “seeking” systems

Your Module 3 is directionally consistent with neuroscience of dopamine/reward learning:

- Dopamine neurons are strongly associated with **reward prediction error**: responses shift from unexpected reward to reward-predicting cues, and negative prediction errors appear when an expected reward fails to arrive. citeturn10search3turn15search2turn15search14
- “Wanting” (incentive salience) and “liking” (hedonic pleasure) are dissociable; dopamine is more tightly linked to cue-triggered “wanting” than to pleasure itself. citeturn15search1turn15search0turn15search11turn15search35

This provides a strong computational justification for **variable rewards** as a driver of persistent exploration: uncertainty maintains prediction error dynamics and cue-driven seeking. citeturn10search3turn15search1turn15search35

For “rewards of the tribe/hunt/self,” academic motivation mapping that is safer than pop-taxonomies is **Self-Determination Theory**: relatedness, competence, autonomy. It’s not identical to your taxonomy, but it’s close enough to serve as a formal “drive basis” that you can tune. citeturn9search3turn9search15

To make this “AI-relentlessly-driven” without external rewards, you can graft **intrinsic motivation** from RL:
- curiosity as prediction error in self-supervised forward dynamics (Pathak et al.),
- novelty search as optimizing for behavioral novelty rather than objective reward,
- intrinsic motivation frameworks surveyed by Barto and colleagues. citeturn9search0turn9search4turn9search1turn9search6

### Heuristics and bias filters: affect-first judgment, WYSIATI, loss/negativity dominance

Your Module 4 aligns tightly with established research:

**Affect heuristic.** Paul Slovic and colleagues describe affect as a fast “goodness/badness” tag that guides judgment and risk perception (“risk as feelings” vs “risk as analysis”). citeturn16search4turn19search28turn19search2

**“The emotional tail wags the rational dog.”** This phrase is explicitly discussed in entity["book","Thinking, Fast and Slow","kahneman 2011"] as a reference to entity["people","Jonathan Haidt","social psychologist"] in the context of affect-driven belief formation. citeturn16search6turn16search0

**WYSIATI.** “What you see is all there is” is one of the named principles in entity["book","Thinking, Fast and Slow","kahneman 2011"]: System 1 constructs coherent narratives from what’s immediately available and tends to neglect missing information. citeturn19search0turn19search29

**Loss aversion.** Prospect theory formalizes reference dependence and loss aversion; “losses loom larger than gains.” citeturn1search0turn12search0  
The often-quoted “twice as powerful” rule-of-thumb appears in many summaries, but the stronger academic core claim is simply *asymmetry*: losses have greater impact than equivalent gains, with empirical magnitude varying by context/task. citeturn12search0turn12search3turn12search7

**Negativity dominance / “bad is stronger than good.”** Reviews find negative events and information often have stronger psychological impact than positive equivalents across domains (learning, relationships, impression formation). citeturn12search1turn12search2turn12search30

Computationally, “bias filters” can be implemented as:
- asymmetric value functions (loss weight > gain weight),
- attention allocation favoring negative or threat-labeled signals,
- story-construction constraints that prefer coherence over completeness (WYSIATI),
- and affect tags that gate which evidence gets considered by System 2. citeturn19search29turn12search0turn16search4

### Memory storage protocol: experiencing self vs remembering self, peak–end and duration neglect

The “two selves” framing (experiencing vs remembering) is popularized by entity["people","Daniel Kahneman","nobel economist psychologist"] and connected to formal distinctions between **instant utility** and **remembered utility** in experienced-utility research. citeturn19search8turn19search1

In the classic pain-memory work, retrospective evaluations overweight the peak and end of an episode and show duration neglect (“when more pain is preferred to less” by adding a better end). citeturn0search0turn0search18turn19search11

A computational instantiation that mirrors your spec:
- **Experiencing Self** → high-resolution stream buffer (rich episodic trace).
- **Remembering Self** → compressed “scorekeeping” memory that stores:
  - peak moments (high affect intensity, high prediction error),
  - end moments (final affect/value),
  - semantic summaries for future policy bias. citeturn0search0turn10search3turn8search3

Notably, modern agent memory systems already separate *fast context* from *persistent storage* (virtual memory analogy). citeturn18search1turn18search0  
You can bias the consolidation step toward peak/end rather than uniform logging, aligning the memory system with human retrospective distortions. citeturn0search0turn19search11

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["dual process theory system 1 system 2 diagram","Fogg behavior model motivation ability prompt graph","dopamine reward prediction error cue vs reward diagram","default mode network meditation brain connectivity diagram"],"num_per_query":1}

## Research-paper shortlist you can directly reuse by module

This section names research that is (a) foundational, (b) implementable, and (c) useful as citations/justification in a serious technical design doc.

### Dual-processing and “lazy deliberation”
Core dual-process grounding:
- Sloman’s “two systems” synthesis (associative vs rule-based). citeturn2search36  
- Evans’ review of dual-process accounts. citeturn2search37  
- entity["book","Thinking, Fast and Slow","kahneman 2011"] for System 1/2 and WYSIATI framing (popular but influential). citeturn19search0  
Effort-minimization:
- entity["people","George Kingsley Zipf","linguist"], Principle of Least Effort (historical basis for “cognitive miser” style behavior). citeturn11search4turn11search12

### Behavior gating, prompts, and habit formation
- entity["people","B. J. Fogg","behavior scientist"]’s Behavior Model / Behavior Grid (official materials + paper). citeturn0search16turn0search17turn0search20  
- Real-world habit formation curve and variability (Lally et al.). citeturn10search0turn10search15  
- Basal ganglia “chunking” and habit circuitry (Graybiel). citeturn10search5turn10search8turn10search27

### Variable rewards, “seeking,” and intrinsic motivation
Reward prediction error:
- entity["people","Wolfram Schultz","neuroscientist"], entity["people","Peter Dayan","computational neuroscientist"], Montague (dopamine prediction error). citeturn10search3turn15search2turn15search29  
Incentive salience (wanting vs liking):
- entity["people","Kent C. Berridge","neuroscientist"] & entity["people","Terry E. Robinson","psychologist"], incentive salience / parsing reward. citeturn15search1turn15search0turn15search31  
Intrinsic motivation in AI:
- Pathak et al. curiosity as self-supervised prediction error. citeturn9search0turn9search4  
- Novelty search (Lehman & Stanley). citeturn9search1turn9search17  
- Barto’s intrinsic motivation + RL synthesis. citeturn9search6turn9search34  
Drive taxonomy grounding:
- entity["people","Richard M. Ryan","psychologist"] and entity["people","Edward L. Deci","psychologist"], Self‑Determination Theory (competence/autonomy/relatedness). citeturn9search3turn9search15

### Heuristics, WYSIATI, affect, loss and negativity
- Slovic et al. affect heuristic foundational paper. citeturn16search4turn19search2  
- Prospect theory (Kahneman & Tversky). citeturn1search0  
- Loss aversion in riskless choice (Tversky & Kahneman, 1991). citeturn12search0  
- Negativity dominance classic review (Rozin & Royzman) and “Bad is stronger than good.” citeturn12search2turn12search1  
- entity["people","Jonathan Haidt","social psychologist"]’s intuitionist model for affect-first judgment and post-hoc reasoning (useful analog for “System 2 rationalization”). citeturn16search0turn16search10

### Two-selves memory, peak–end, duration neglect
- Fredrickson & Kahneman (1993) peak-end style result (“more pain preferred to less” by adding a better end). citeturn0search0turn0search18  
- Kahneman, Wakker, Sarin on instant vs remembered utility (more formal). citeturn19search8turn19search1  
- Additional medical/behavioral discussion of peak-end and duration neglect. citeturn19search11turn19search4

### “More Than Human”: Flow + “No‑Mind” as compute/attention control
Flow:
- entity["people","Mihaly Csikszentmihalyi","psychologist"]’s flow framing (book) and modern work-related meta-analysis showing associations with performance/engagement/creativity. citeturn2search30turn13search2  
- The popular “5× productivity” claim appears in entity["company","McKinsey & Company","management consulting"] material as self-reported peak productivity; treat it as anecdotal/corporate self-report rather than controlled lab effect. citeturn13search9turn13search32  
No‑Mind / reduced rumination:
- Meditation experience associated with differences in DMN activity/connectivity; consistent with decreased mind-wandering. citeturn2search35turn2search31  
- Work-related flow models increasingly connect flow, mindfulness, and cognitive control (modern organizational psych framing). citeturn13search19

## GitHub repositories and open-source stacks that directly support your build

Below are “reusable primitives” you can assemble into your architecture without reinventing infrastructure.

### Cognitive-architecture baselines (closest to your “human-like OS” idea)

These are valuable because they already implement *explicit modules* (memory, production rules, action selection, etc.) rather than monolithic end-to-end training.

- **Soar**: canonical open cognitive architecture implementation and ecosystem (good for action selection + symbolic reasoning experiments). citeturn3search2turn3search6  
- **ACT‑R Python implementations**: useful if you want to prototype “buffers + production rules + declarative memory” style cognition in code. citeturn3search17turn3search1  
- **CLARION** literature (dual implicit/explicit processes) is highly aligned with your System 1/System 2 requirements (implementation code is less centralized than Soar, but the architecture is conceptually on-point). citeturn3search4turn3search24turn3search0  
- **MicroPsi2**: neuro-symbolic agent toolkit explicitly oriented around cognition and motivation concepts. citeturn17search3turn17search27  
- **LIDA** (conceptual + partial computational model) for attention/action cycles; use as inspiration and references. citeturn3search3turn3search7turn3search11  
- **OpenCog** / **Hyperon**: ambitious integrative cognitive architecture; best treated as a research playground vs production-ready foundation. citeturn17search0turn17search8turn17search12  
- **OpenNARS (Non-Axiomatic Reasoning System)**: explicitly built for reasoning under insufficient knowledge/resources—philosophically aligned with bounded rationality and WYSIATI-like constraints. citeturn17search1turn17search25turn17search5

### Reinforcement learning + habit formation infrastructure (for Motivation/Ability/Policy)

To implement variable rewards, habits, and multi-objective drives, you need robust RL tooling.

- **Stable-Baselines3**: reliable PyTorch RL algorithms; practical for fast iteration. citeturn8search0turn8search24  
- **Dopamine**: compact RL research framework designed for “wild ideas” prototyping. citeturn7search1turn7search29  
- **Acme**: DeepMind’s RL building blocks; good reference implementations and scalable patterns. citeturn7search2turn7search10  
- **CleanRL**: single-file, research-friendly implementations; also has a JMLR paper documenting the approach. citeturn7search3turn7search23  
- **Gymnasium** environments + **PettingZoo** (multi-agent): standardized interfaces for building “human-like” simulated environments with cues/triggers and social dynamics. citeturn8search1turn8search2turn8search6  
- **MO‑Gymnasium** if your “tribe/hunt/self” drives are truly multi-objective reward vectors. citeturn8search25turn8search13

### Memory systems (for “two selves” and long-horizon identity)

- **Letta (formerly MemGPT)**: open-source stateful agents with explicit memory tiers; directly matches the “fast/slow memory” architecture and can be adapted to implement peak/end biased consolidation. citeturn18search0turn18search1turn18search5  
- **Differentiable Neural Computer (DNC)**: memory-augmented neural network with an official DeepMind repo; useful if you want neural external memory as *part of* System 1. citeturn18search2turn18search3  
- **Episodic Memory Deep Q-Networks (EMDQN)**: biologically inspired RL leveraging episodic memory for sample efficiency (useful if you want “episodic peaks” to supervise learning). citeturn18search9turn18search17

### Open-source “Deep Research” and evidence-graph tooling (your novelty-from-open-sources requirement)

If your agent must continuously form *new* stories/novels/ideas based on open information, your bottleneck is not generation—it’s **retrieval planning, evidence structuring, and citation control**.

Deep research agents:
- **GPT Researcher**: open deep-research agent that outputs citation-backed reports. citeturn6search2turn6search10  
- **LangChain Open Deep Research** (LangGraph-based): configurable deep-research pipeline across tools/providers. citeturn6search3turn6search22  

Graph-based RAG (critical for multi-hop “new synthesis”):
- **Microsoft GraphRAG**: pipeline to extract a knowledge graph, build community hierarchy, summarize, then answer via structured retrieval. citeturn6search0turn6search4turn6search19  
- **NodeRAG**: heterogeneous nodes for graph-centric RAG; official repo exists. citeturn6search1turn6search9  
- **TRACE the Evidence**: constructs knowledge-grounded reasoning chains from retrieved docs by turning them into a knowledge graph and reasoning chain. citeturn5search3turn5search23turn5search7  

Context pruning / compression (to prevent “WYSIATI by overload”):
- **LongLLMLingua** (prompt compression) for long-context pipelines. citeturn14search2turn5search5  
- **Provence / OpenProvence** for context pruning + reranking in RAG workflows. citeturn5search18turn14search3turn5search2  

Reasoning/agent orchestration patterns (for System 2 planning + laziness + parallel execution):
- **ReWOO** (reasoning without observation interleaving) reduces redundant tool prompting and improves efficiency. citeturn14search0turn4search7turn4search3  
- **LLMCompiler** executes tool calls in parallel via a DAG-like compiler approach. citeturn14search1turn5search4turn5search0  
- **Graph of Thoughts** (official implementation) for graph-structured “thought operations” (very compatible with your System 1 associative engine). citeturn4search4turn4search0turn4search32  
- **Self-Discover** and **Buffer of Thoughts** for meta-reasoning templates and reusable reasoning structures. citeturn4search21turn4search9turn4search22turn4search6

## A concrete open-source blueprint for “create never-seen outputs” from web evidence

Your final requirement is not only “human-like reactions,” but also **systematic novelty**: generating new novels/stories/ideas from existing information without plagiarism, while staying grounded in sources.

The most robust way to do this (and keep it genuinely “new”) is to separate your system into two coupled loops:

### Evidence loop: build a structured, citeable world model from open sources

1) **Research planning**: produce a search plan and subquestions (System 2). Use a deep-research framework that already supports iterative search + citation capture, such as GPT Researcher or Open Deep Research. citeturn6search2turn6search3  

2) **Acquisition + dedup + reliability scoring**: retrieve sources, then prune aggressively.
- Use OpenProvence / Provence-style pruning to remove tangential context while keeping relevance scores. citeturn5search18turn14search3turn5search2  
- Use LongLLMLingua-style compression if you must fit long evidence into limited windows. citeturn14search2turn5search5  

3) **Evidence graph construction**: convert documents into an explicit graph:
- GraphRAG or NodeRAG for graph index + community summaries. citeturn6search0turn6search4turn6search1turn6search9  
- TRACE for evidence-chains grounded in a KG extracted from retrieved docs. citeturn5search3turn5search7turn5search23  

4) **Calibration**: attach confidence and provenance edges (“claim → source spans → contradictions”). This is how you prevent WYSIATI from becoming hallucination. The Kahneman framing is literally: what you see is all there is—so your system must *explicitly represent what it has not seen*. citeturn19search0turn19search29  

### Invention loop: generate novelty as a controlled search over the evidence graph

This is where your uploaded “Dossier” design philosophy fits: treat invention as a guided search, not a single-shot generation. fileciteturn0file1 fileciteturn0file2

A research-backed way to do this with open-source components:

- Use **Graph of Thoughts** to explore multiple “idea continuations” as a graph search rather than a linear chain. This operationalizes System 1 associative branching. citeturn4search4turn4search0  
- Use **Buffer of Thoughts** (meta-buffer of thought templates) as your “habit library” for reasoning patterns: it is literally a stored set of reusable reasoning templates. citeturn4search22turn4search6  
- Use **Self-Discover** to dynamically choose reasoning modules per task (story, scientific hypothesis, business plan) to avoid sameness. citeturn4search21turn4search9  

Then, to force “new kinds of outputs,” you need **explicit novelty objectives** (not just temperature):

- **Novelty search** principle: optimize for behavioral/structural novelty rather than single objective reward. In creative generation, “behavior” can be narrative structure, character arcs, causal graphs, or thematic combinations. citeturn9search1turn9search17  
- **Curiosity/intrinsic reward** as prediction error: reward the system for discovering evidence-supported connections it can’t yet predict (new cross-domain links). citeturn9search0turn9search4  

Finally, attach your **human-like biases** intentionally as style/selection filters, not as uncontrolled errors:
- affect tags steer which themes feel “important,” citeturn16search4  
- negativity/loss aversion can shape conflict and stakes in narratives, citeturn12search1turn12search0  
- peak–end memory rules determine what gets turned into “canon” for the system’s ongoing story world. citeturn0search0turn19search11

## Risks, evaluation metrics, and guardrails that keep it “new” but not “wrong”

A system built to be human-like will also inherit human failure modes unless you formally control them.

### Hallucination and WYSIATI amplification
WYSIATI is a perfect description of how a generative model will confidently narrate from incomplete context. The fix is not “be more rational” but to enforce **structural representation of unknowns** and contradiction checks before finalization. citeturn19search0turn19search29

### Bias as a feature vs bias as contamination
Loss/negativity dominance can be used as a narrative engine, but if you let it drive factual claims it will skew conclusions. Psychological negativity effects are robust, but they are not a license to distort evaluation of evidence. citeturn12search1turn12search2turn12search30

### A practical evaluation suite for your “Original AI”

To measure whether the system is truly doing what you want, you need metrics that correspond to your modules:

- **Dual-process gating quality**: how often does System 2 intervene only on conflict/surprise, and does that reduce errors without huge compute cost? (Use tool-failure tests + contradiction benchmarks.) citeturn14search0turn14search1  
- **Habit formation**: does repeated cue→action→reward reduce latency/compute and become more automatic over time (asymptotic curve)? citeturn10search0turn10search15  
- **Motivation persistence**: does intrinsic reward (curiosity/novelty) keep exploration going in sparse-reward domains? citeturn9search0turn9search1  
- **Memory distortion fidelity**: do “remembered summaries” overweight peaks/ends and ignore duration—*and does that measurably change downstream choices*? citeturn0search0turn19search11  
- **Grounded novelty**: quantify novelty (distance/diversity of generated structure) *subject to evidence grounding constraints* (citations + claim graph). GraphRAG/TRACE-style evidence chains help here. citeturn6search4turn5search7turn5search23  

If your goal is “a new kind of algorithm no one has seen,” the differentiator is not any single component (dual-process, RL, RAG, graph reasoning all exist). The differentiator is the **tight coupling** of:
- psychologically faithful control laws (lazy System 2 + habit automation + peak/end consolidation) citeturn11search12turn10search5turn0search0  
with
- graph-grounded research synthesis (GraphRAG/NodeRAG/TRACE) citeturn6search0turn6search1turn5search3  
and
- explicit novelty objectives (curiosity + novelty search) citeturn9search0turn9search1  
compiled into an efficient tool-using agent runtime (ReWOO + LLMCompiler + pruning/compression). citeturn14search0turn14search1turn14search3turn14search2