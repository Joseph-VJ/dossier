# Dossier

## Open-Source Investigation Engine — Bring Your Own API Key

**Working product name:** Dossier
**Document version:** 2.0
**Date:** 2026-03-10
**Status:** Final plan — ready to build (Invention Mode override active as of 2026-03-11)
**License:** MIT (open-source)
**Model:** BYOK (Bring Your Own API Key) — self-hosted, provider-agnostic

---

## 0. Invention Mode Override (2026-03-11)

This section supersedes conflicting sections below.

Authoritative precedence:
1. `DOSSIER_FINAL_UNIFIED_ALGORITHM_PLAN.md` (current canonical algorithm spec)
2. This override section
3. Remaining sections in this document

### Objective override

Primary objective changes from trust-first investigation to invention-first synthesis.

Dossier now optimizes for:
- novel information generation from cross-evidence synthesis
- mechanism-level hypothesis construction
- predictive insight generation
- novelty-per-token efficiency

Dossier no longer treats strict factual conservatism as the top blocker.
It enforces minimal coherence constraints, then prioritizes high-value novel candidates.

### Core algorithm override

The active algorithm stack is:
- `BAEGC-lite` for planning, retrieval, graph building, token control
- `ADEPT-DS` for abductive-deductive invention synthesis

The active output classes are:
- `Novel Deduction`
- `Speculative Mechanism`
- `Exploratory Prediction`

### Gate and scoring override

Primary score is `InventionScore`, not trust score.

`InventionScore = 0.30*NoveltyDistance + 0.20*SynthesisDepth + 0.20*MechanismQuality + 0.15*PredictivePower + 0.10*CrossDomainTransfer + 0.05*TokenEfficiency - 0.10*CoherencePenalty`

Promotion is based on invention ranking and minimal coherence floor, not strict adversarial rejection.

### Section interpretation override

Read existing sections with the following reinterpretation:
- "Trust Architecture" and strict confidence language are advisory, not primary objective gates.
- Adversarial review remains useful, but acts as a refinement signal rather than an absolute blocker.
- "Evidence-Backed Deductions" now explicitly includes speculative-but-structured invention outputs.
- Build and metrics sections should prioritize novelty rate, synthesis depth, and novelty-per-token.

---

## Table of Contents

0. [Invention Mode Override (2026-03-11)](#0-invention-mode-override-2026-03-11)
1. [Executive Summary](#1-executive-summary)
2. [The Problem](#2-the-problem)
3. [The Product](#3-the-product)
4. [Core Innovation: The Evidence Engine](#4-core-innovation-the-evidence-engine)
5. [Architecture](#5-architecture)
6. [Agent Model](#6-agent-model)
7. [Research Lifecycle](#7-research-lifecycle)
8. [Trust Architecture](#8-trust-architecture)
9. [Data Model](#9-data-model)
10. [User Experience](#10-user-experience)
11. [Output Design](#11-output-design)
12. [Technical Stack](#12-technical-stack)
13. [Sustainability Model](#13-sustainability-model)
14. [Go-to-Market](#14-go-to-market)
15. [Build Plan](#15-build-plan)
16. [Team and Community Model](#16-team-and-community-model)
17. [Risks and Mitigations](#17-risks-and-mitigations)
18. [Success Metrics](#18-success-metrics)
19. [Long-Term Vision](#19-long-term-vision)

---

## 1. Executive Summary

**One sentence:**
Dossier is an open-source, self-hosted investigation engine that gathers evidence, challenges it, derives evidence-backed deductions, shows exactly how it derived them, and lets you challenge them — producing a traceable, adversarially-reviewed dossier powered by your own API key.

**The gap in the world:**
Every day, millions of people make consequential decisions — hiring a vendor, choosing a medical treatment, investing in a company, entering a market, changing a policy — based on research they did with tools that cannot tell them where the evidence came from, whether it was challenged, or what they missed. ChatGPT, Perplexity, and Google give you answers. Nobody gives you a *case*.

But there is an even deeper gap: even the best research tools only report what already exists online. They find, summarize, and cite. They never *reason across what they found*. When you have fifty evidence items from twenty sources, the most valuable conclusions are often the ones that no single source states — they emerge only when you connect the dots across all the evidence at once.

That is what Dossier does. It derives evidence-backed deductions, shows exactly how it derived them, and lets you challenge them.

**What Dossier does:**
A user submits one hard question. The system scopes it, dispatches parallel investigators, gathers evidence with full provenance, actively searches for contradictions, scores confidence against real evidence weight, names the gaps — and then does something no other tool does: it **derives evidence-backed deductions and clearly labels them as deductions**. It cross-references timelines, connects patterns across unrelated sources, identifies implications hidden in the intersections of evidence, and surfaces conclusions that only become visible when the full evidence graph is analyzed as a whole. Every deduction comes with the full chain of reasoning so you can see exactly how it was derived — and challenge it if you disagree. Finally, it publishes a structured dossier where every claim links to a source, every deduction shows its derivation chain, and every gap is named. If the evidence is weak, the dossier says so. If counter-evidence exists, the dossier shows it. If information was unavailable, the dossier lists what could not be found.

**How it works — the BYOK model:**
You clone the repo, add your LLM API key (OpenAI, Anthropic, Google, Groq, Mistral, or any OpenAI-compatible endpoint including local models via Ollama), optionally add a search API key (Tavily, Serper, or SearXNG for fully free search), run `docker compose up`, and you have a full investigation engine running on your own machine. No account creation. No subscription. No data leaves your infrastructure. Your API keys, your data, your dossiers.

**What Dossier is not:**
It is not a chatbot. It is not a report prettifier. It is not a search engine with better formatting. It is not an AI agent demo dressed up as a product. It is an investigation engine that produces a trust artifact: the dossier.

**Why open-source:**
The investigation methodology — adversarial review, source independence tracking, gap transparency — should be a public standard, not a proprietary advantage. Open-sourcing Dossier means: (1) anyone can audit how evidence is gathered and scored, (2) the community can build domain-specific templates for any industry, (3) security-conscious users can self-host with zero data exposure, (4) cost is controlled by the user — you pay only for the LLM and search API calls you make, with no markup.

**The deduction principle:**
Think of Detective Conan (Case Closed). When Conan solves a case, he does not find a document that says "Person X committed the crime." That document does not exist. Instead, he collects evidence — a footprint, a train ticket timestamp, a contradictory alibi, a missing umbrella — and through cross-evidence reasoning, he derives a conclusion that nobody else could see. The answer was always *in* the evidence, but it was invisible until someone reasoned *across* all of it simultaneously.

Dossier works the same way. A Researcher agent finds that Company X's CEO resigned in January. Another Researcher finds a patent lawsuit filed in December. Another finds the new CEO's background is in IP law. No single source says "Company X replaced their CEO to prepare for patent litigation." But Dossier's Analyst agent connects these three facts, builds a deduction chain, and surfaces this as an **evidence-backed deduction** — labeled clearly as a deduction, not a sourced fact, with the full derivation chain visible for the user to inspect, challenge, or dismiss.

This is the core differentiator. Every other tool tells you what the internet already says. Dossier derives what the evidence implies, shows you exactly how, and lets you challenge it.

**Why now:**
LLMs are now good enough at cross-evidence reasoning to serve as the analytical backbone inside a disciplined investigation framework. What they are NOT good at is self-discipline: knowing when evidence is thin, challenging their own conclusions, tracking source independence, and being honest about gaps. Every competitor uses LLMs to generate answers. Dossier uses LLMs as evidence workers AND deduction engines inside a framework where the framework enforces rigor the models would not apply to themselves.

**Who needs it:**
Everyone who has ever said "I need to research this properly before I decide" and then spent 6 hours in browser tabs, or paid someone thousands of dollars, or just went with their gut because proper research was too expensive or too slow. Everyone who needs a tool that does not just collect information, but *reasons across it* — derives evidence-backed deductions, shows exactly how it derived them, and lets you challenge them. Now they can run it themselves, on their own hardware, with their own API key.

---

## 2. The Problem

### 2.1 The universal problem

People make important decisions based on unverified information.

This is not a niche problem. It is the default state of human decision-making in the information age. The information exists, but the work of finding it, verifying it, cross-checking it, and assembling it into something defensible is so painful that most people skip it.

### 2.2 The specific failure modes of current tools

**Google Search:**
- You get links, not answers.
- You have to read, evaluate, cross-reference, and synthesize manually.
- No provenance chain. No contradiction checking. No confidence scoring.
- Works: when you know what you are looking for. Fails: when you do not know what you do not know.

**ChatGPT / Gemini / Claude (standard chat):**
- Fast, articulate, and confidently wrong.
- No evidence chain. You get claims without sources.
- Hallucinations are indistinguishable from facts.
- No persistence. The answer disappears when the chat ends.

**ChatGPT Deep Research / Perplexity Pro / Gemini Deep Research:**
- Better: multi-step browsing, citations at the end.
- But: citations are often decorative (the source does not actually support the claim).
- No adversarial review. No contradiction search. No gap awareness.
- No persistence. No living updates. No source independence analysis.
- The report *looks* thorough but is structurally the same as a single prompt — just with more browsing steps.

**Professional analysts (human):**
- Excellent quality when done well.
- Cost: $200-$500/hour. A single due diligence report costs $5,000-$50,000.
- Speed: days to weeks.
- Availability: limited to those who can afford it.

**The gap Dossier fills:**
Professional-grade investigation rigor, available to anyone, at 1-10% of the cost of hiring a human analyst, with evidence traceability that exceeds what most human analysts provide.

### 2.3 Who feels this pain (concrete examples)

| Person | Decision | Current approach | What goes wrong |
|--------|---------|-----------------|----------------|
| Startup founder | Should we use Vendor X for our infrastructure? | Googles reviews, asks Twitter, reads G2 | Misses a critical outage history buried in a Hacker News thread from 2024 |
| Parent | Is Treatment Y safe for my child's condition? | Reads WebMD, asks ChatGPT, panics on Reddit | Cannot distinguish between rigorous clinical evidence and anecdotal reports |
| VC analyst | Should we invest $2M in Company Z? | Reads pitch deck, Googles the founders, checks Crunchbase | Misses that the CEO's previous company had an SEC investigation |
| Procurement lead | Which of these 3 SaaS vendors should we choose? | Reads marketing sites, schedules demos, asks peers | No systematic comparison of security, compliance, or financial stability |
| Journalist | Is Politician's claim about Policy X true? | Manual research across government databases and news archives | Takes days. Misses counter-evidence. Cannot show full evidence chain to editors |
| Small business owner | Should I sign this 3-year commercial lease? | Asks a friend, reads Yelp reviews of the landlord | No structured investigation of landlord's litigation history, property conditions, or market comparables |
| Patient | Doctor recommended Surgery A. Should I get a second opinion? | Googles success rates, reads patient forums | No systematic review of published outcomes, surgeon track records, or alternative treatments |
| Policy researcher | What is the strongest evidence for and against Policy Y? | Reads think tank reports from both sides | No systematic source independence check; both sides may cite the same flawed study |

These are not edge cases. This is how most people research important decisions. The common thread: **they all deserve better evidence, and none of them can afford a professional analyst.**

### 2.4 Why existing AI products do not solve this

The core failure is architectural, not capability-based:

1. **No separation between evidence and narrative.** Current tools generate text that blends facts and inference. You cannot inspect the evidence layer independently.
2. **No adversarial process.** No product actively tries to disprove its own conclusions before presenting them.
3. **No source independence tracking.** If 5 sources all repeat the same press release, current tools count that as strong evidence. It is not.
4. **No gap awareness.** No product tells you what it could not find. Silence is presented as completeness.
5. **No persistence.** Research disappears after the session. You cannot return to it, update it, or share it as a living artifact.
6. **No cross-evidence deduction.** No product reasons *across* the evidence it collects to derive new conclusions. They report what they find. They never derive what the evidence *implies*. No AI research tool surfaces evidence-backed deductions, shows how they were derived, and lets you challenge them.

These are not features that can be bolted on. They require a fundamentally different architecture.

---

## 3. The Product

### 3.1 What Dossier is

Dossier is an open-source, self-hosted investigation engine that turns one hard question into a structured, evidence-traced, adversarially-reviewed research dossier — with **evidence-backed deductions derived from cross-evidence reasoning** — powered entirely by your own API keys.

**Setup experience:**
```bash
git clone https://github.com/dossier-ai/dossier.git
cd dossier
cp .env.example .env
# Add your API keys to .env:
#   LLM_API_KEY=sk-...        (OpenAI, Anthropic, Google, Groq, Mistral, or Ollama)
#   SEARCH_API_KEY=tvly-...   (Tavily, Serper, or use built-in SearXNG for free)
docker compose up
# Open http://localhost:3000
```

That is the entire setup. No account creation. No subscription. No telemetry. No data leaves your machine.

**How it works:**
1. You submit a question or decision you need to research.
2. The system scopes the investigation: what hypotheses to test, what sources to search, what would constitute strong evidence.
3. Parallel investigators gather evidence from diverse source classes.
4. An adversarial reviewer actively searches for contradictions, gaps, and weaknesses.
5. All evidence is stored with full provenance: source URL, retrieval timestamp, extracted quote, and relevance assessment.
6. An analyst agent reasons across the full evidence graph to derive evidence-backed deductions — conclusions that no single source states but that the combined evidence implies. Each deduction includes its full derivation chain.
7. Claims are scored by evidence weight, source independence, and challenge strength.
8. The final dossier presents: findings, evidence-backed deductions, evidence, counter-evidence, confidence levels, and explicit gaps.
9. The dossier persists locally. You can return to it, share it, challenge it, or request deeper investigation on any point.

### 3.2 Core design principles

1. **BYOK (Bring Your Own Key).** Dossier never handles, stores, or proxies API keys through any external service. Your keys stay in your `.env` file on your machine. The system calls LLM and search APIs directly from your instance.

2. **Provider-agnostic.** Works with any LLM provider that speaks OpenAI-compatible API: OpenAI, Anthropic (via LiteLLM), Google Gemini, Groq, Mistral, Together AI, Fireworks, or local models via Ollama/vLLM/LM Studio. Switch providers by changing one environment variable.

3. **Local-first.** All data (cases, evidence, dossiers) is stored locally. Default database is SQLite (zero config) with optional PostgreSQL for power users. No cloud dependency.

4. **Zero telemetry.** No analytics, no tracking, no phone-home. The application is fully air-gappable.

5. **Composable.** Every component (search, LLM, storage, extraction) is a pluggable interface. Swap Tavily for SearXNG. Swap Claude for a local Llama model. Swap S3 for local disk. The investigation framework does not care.

6. **Open-source core.** The full investigation engine, all agent logic, all domain templates, all output formats — MIT licensed. No "open core" bait-and-switch. No features behind a paywall.

### 3.3 What Dossier is not

- **Not a chatbot.** You do not have a conversation. You commission an investigation and receive a dossier.
- **Not a search engine.** It does not return a list of links. It returns structured findings with evidence chains.
- **Not a report generator.** The evidence structure comes first. The narrative layer is optional and always subordinate to the evidence.
- **Not an agent demo.** The backend uses AI agents, but the user never sees, manages, or thinks about agents. They think about their investigation.
- **Not a search aggregator.** It does not just compile what the internet already says. It reasons across evidence to find what nobody has stated.
- **Not a real-time tool.** Investigations take minutes to hours. This is a feature, not a bug. Depth requires time.
- **Not a SaaS.** There is no hosted version you must pay for. You run it yourself. (A managed cloud option may exist later for convenience, but the self-hosted version is always the full product.)

### 3.4 The product in one interaction

```
USER:
    Should our company switch from AWS to Google Cloud
    for our SaaS platform? We spend about $40K/month.
    Main concerns: cost, reliability, migration risk, and
    vendor lock-in.

DOSSIER (after 25 minutes):
    ┌─────────────────────────────────────────────┐
    │  INVESTIGATION: AWS vs. GCP Migration        │
    │  Status: Complete                            │
    │  Evidence items: 47                          │
    │  Sources: 31 (26 independent)               │
    │  Confidence: Moderate (0.71)                 │
    │  Deductions: 3                               │
    │  Strongest finding: [link to claim #1]       │
    │  Strongest challenge: [link to claim #4]     │
    │  Key deduction: GCP's recent enterprise push  │
    │    + pricing changes + AWS cost increases       │
    │    suggest a 12-month window of aggressive     │
    │    GCP migration incentives. [DEDUCTION]       │
    │  Notable gap: Limited data on GCP pricing    │
    │    for your specific workload pattern.       │
    └─────────────────────────────────────────────┘

    FINDINGS (5 claims, each with evidence chain)
    EVIDENCE-BACKED DEDUCTIONS (3 deductions, each
      with full derivation chain — conclusions no single
      source states, but the evidence implies)
    COUNTER-EVIDENCE (3 challenges)
    WHAT WE COULD NOT DETERMINE (2 gaps)
    FULL EVIDENCE BOARD (47 items, filterable)
    SOURCE MAP (31 sources, independence graph)
```

The user did not manage agents. They did not configure workflows. They asked a question and received a dossier with sourced findings AND evidence-backed deductions they can inspect, challenge, and share.

---

## 4. Core Innovation: The Evidence Engine

This is the technical heart of Dossier and the primary source of differentiation. Everything else — agents, UI, business model — is built on top of this.

### 4.1 The Evidence Provenance Chain

Every claim in a dossier is backed by a chain:

```
CLAIM: "GCP's sustained-use discounts reduce compute costs by 20-30%
        compared to on-demand pricing."

  └─ EVIDENCE ITEM #14
      ├─ Source: Google Cloud Pricing Documentation
      │   URL: cloud.google.com/compute/pricing#sustained-use
      │   Retrieved: 2026-03-10T14:23:00Z
      │   Source class: Primary (vendor documentation)
      │   Freshness: Current (last updated 2026-02)
      │
      ├─ Extracted quote: "Compute Engine automatically gives you a
      │   discount for every incremental hour... up to a 30% net
      │   discount for instances that run the entire month."
      │
      └─ Independence: PRIMARY SOURCE (not derived from another source)

  └─ EVIDENCE ITEM #22
      ├─ Source: CloudOptimize benchmark report (2025)
      │   URL: cloudoptimize.io/reports/gcp-pricing-2025
      │   Retrieved: 2026-03-10T14:25:00Z
      │   Source class: Third-party analysis
      │   Freshness: Recent (published 2025-11)
      │
      ├─ Extracted quote: "In our testing, sustained-use discounts
      │   applied automatically, resulting in a 22-28% reduction
      │   for always-on workloads."
      │
      └─ Independence: INDEPENDENT (does not cite Google's documentation;
         based on original benchmark testing)

  CLAIM ASSESSMENT:
      Support strength: 0.82 (2 independent sources, one primary)
      Challenge strength: 0.15 (no direct contradictions found)
      Confidence: Strong
```

This chain is always present. It is never truncated. It is the product.

### 4.2 Source Independence Graph

This is the feature no competitor has and the single most important trust mechanism in the system.

**The problem it solves:** Most AI research tools count "number of sources" as a proxy for evidence strength. But if 5 news articles all cite the same press release, that is 1 source of evidence, not 5. Counting derived sources as independent support is the most common way AI research tools produce false confidence.

**How it works:**

For each set of sources that support a claim, the Evidence Engine builds a citation graph:

```
Source A (press release from Company X)
  ↑ cited by
Source B (TechCrunch article citing Source A)
  ↑ cited by
Source C (blog post citing Source B)
Source D (independent analyst report — original research)
Source E (SEC filing — primary document)

TRUE INDEPENDENCE: 3 independent sources (A, D, E)
APPARENT INDEPENDENCE: 5 sources
INFLATION FACTOR: 1.67x
```

The dossier reports **true independent source count**, not raw source count. This is a genuinely novel feature that directly addresses the #1 reliability problem in AI-generated research.

**Implementation approach:**
- Extract citation/reference links from each source document.
- Check if Source B's claims appear verbatim or near-verbatim in Source A (published earlier).
- Check if Source B explicitly cites/links to Source A.
- Use publication timestamps to establish temporal citation direction.
- Cluster sources by originating information (same press release, same study, same government filing).
- Report: total sources, independent sources, and the independence graph for inspection.

### 4.3 Adversarial Confidence Model

Instead of a single confidence score (which is always either meaninglessly high or anxiety-inducing), Dossier reports evidence quality on two independent axes:

**Support Strength:** How strong is the evidence FOR this claim?
- Source count (independent only)
- Source quality (primary > third-party > aggregator > social)
- Source diversity (different source classes increase strength)
- Recency (recent evidence weighted higher)
- Specificity (specific numbers/quotes > vague claims)

**Challenge Strength:** How strong is the evidence AGAINST this claim?
- Direct contradictions found
- Missing expected evidence (should exist but does not)
- Source quality of contradicting evidence
- Logical inconsistencies identified by the adversarial reviewer

**The result is a 2x2 space, not a single number:**

| | Weak Challenge | Strong Challenge |
|---|---|---|
| **Strong Support** | Settled — high confidence, act on this | Contested — evidence exists on both sides, investigate further |
| **Weak Support** | Uncertain — not enough evidence either way | Doubtful — more evidence against than for |

This is more honest and more useful than a single "0.78 confidence" number.

### 4.4 Gap Transparency

Every dossier includes a section titled **"What We Could Not Determine"** that lists:

1. **Searches that returned no results.** "We searched for lawsuits involving Company X in federal courts and found nothing. This may mean no lawsuits exist, or that records are not digitally indexed."
2. **Sources that were unavailable.** "The full 2025 annual report for Company X is behind a paywall on S&P Capital IQ. Our evidence for revenue claims relies on press coverage of the earnings call instead."
3. **Questions that remain unanswered.** "We could not determine whether Company X's patent portfolio covers the specific technology relevant to your use case. A patent attorney review is recommended."
4. **Evidence that would change the conclusion.** "If Company X's 2026 Q1 revenue is below $50M (to be reported in April 2026), the growth trajectory claim would be significantly weakened."

This section is the single most trust-building feature in the product. No competitor does this. Most competitors present silence as completeness. Dossier presents silence as a named gap.

### 4.5 Evidence Freshness Decay

All evidence is timestamped and claims carry a freshness indicator:

- **Current:** Supporting sources were published or verified within the last 90 days.
- **Recent:** Supporting sources are 90 days to 1 year old. Findings are likely still valid but should be verified for time-sensitive decisions.
- **Aging:** Supporting sources are 1-3 years old. Findings may have changed. Consider requesting a refresh.
- **Stale:** Supporting sources are 3+ years old. Findings should not be relied upon without current verification.

In living dossiers (persistent cases that can be refreshed), claims automatically show degraded freshness over time, and the system can be set to re-investigate claims whose freshness drops below a threshold.

### 4.6 Cross-Evidence Deduction (The Deduction Engine)

This is the feature that transforms Dossier from a research aggregator into an investigation engine. It is the reason the product exists.

**The problem it solves:** Every existing AI research tool — Perplexity, ChatGPT Deep Research, Gemini Deep Research — does the same fundamental thing: find information that already exists online and present it. They are search engines with better formatting. They can find a needle in a haystack, but they cannot look at a haystack and deduce that a needle *should* be there even though nobody has ever mentioned it.

Dossier does something fundamentally different. It collects evidence — individually mundane facts — and then reasons *across* all of them simultaneously to derive conclusions that exist in no single source. The conclusion emerges from the *intersection* of the evidence, not from any one piece of it.

**How it works:**

After the Researcher agents gather evidence and the Adversary agent challenges it, the **Analyst agent** examines the complete evidence graph and performs cross-evidence reasoning:

1. **Temporal pattern detection.** The Analyst looks at dates and timelines across evidence items to find suspicious sequences. Example: A CEO resigns (January 5), a major lawsuit is filed (January 20), the company announces "strategic restructuring" (February 1). No single source connects these events. The Analyst derives: "The CEO departure may have been related to the upcoming litigation and restructuring."

2. **Cross-source contradiction exploitation.** When Source A says "revenue was $50M" and Source B says "the company laid off 30% of staff," neither source mentions the other's fact. But the combination raises a question: a company with $50M revenue does not normally lay off 30% of staff unless something is wrong. The Analyst flags this as an **evidence-backed deduction**.

3. **Absence-as-evidence reasoning.** When the investigation plan expected to find certain information (e.g., a company's annual report, a product's safety data) and the Researchers found nothing despite thorough search, the Analyst evaluates whether this absence is itself meaningful. A company that should have a public annual report but doesn't — that absence tells a story.

4. **Pattern matching across research lanes.** The Analyst examines findings from different lanes to find connections the individual Researchers could not see (since each Researcher works on one lane). Example: The "Financial" lane found declining revenue. The "Legal" lane found patent disputes. The "Market" lane found a competitor launching a similar product. Individually, these are three separate findings. Together, the Analyst derives: "This company is facing a convergence of financial pressure, legal exposure, and competitive threat that may compound."

5. **Implication extraction.** Given a set of established facts, the Analyst identifies logical implications that no source has stated. If Fact A is true AND Fact B is true, what must also be true? What becomes likely? What becomes unlikely?

**The derivation chain:**

Every deduction the Analyst produces comes with a fully transparent derivation chain:

```
DEDUCTION: "Company X likely replaced their CEO specifically to prepare for
          patent litigation."

  DERIVATION CHAIN:
  ├─ EVIDENCE #7:  CEO Jane Smith resigned January 5, 2026.
  │   Source: Company X Press Release
  │   Type: Directly sourced fact
  │
  ├─ EVIDENCE #18: Patent infringement lawsuit filed by Competitor Y
  │   against Company X on December 12, 2025.
  │   Source: Court filing, PACER database
  │   Type: Directly sourced fact
  │
  ├─ EVIDENCE #23: New CEO Robert Chen was previously Chief IP Counsel
  │   at MegaCorp for 8 years, specializing in patent defense.
  │   Source: LinkedIn profile + interview in IP Law Journal
  │   Type: Directly sourced fact
  │
  ├─ REASONING: The temporal proximity (lawsuit filed Dec 12, CEO
  │   replaced Jan 5) combined with the new CEO's specific background
  │   in patent defense litigation strongly suggests the leadership
  │   change was driven by the need for patent litigation expertise
  │   at the executive level.
  │
  ├─ CONFIDENCE: Moderate-High
  │   Support: 3 independent facts align coherently
  │   Challenge: No direct source confirms this connection; it is
  │   possible the timing is coincidental and the CEO change was
  │   planned independently.
  │
  └─ LABEL: EVIDENCE-BACKED DEDUCTION (not a directly sourced claim)
```

**Critical safety mechanism:** The derivation chain is mandatory. A deduction without a chain is rejected. The chain must reference specific evidence items (not vague reasoning). And every deduction is **labeled distinctly from sourced claims** — the user always knows whether they are looking at a fact from a source or a deduction from cross-evidence reasoning. The Adversary agent reviews deductions with the same rigor it applies to claims. And the user can challenge any deduction directly.

**Why this matters:**

This is what separates an investigation from a search result. Google can find the CEO resignation press release. Perplexity can find the lawsuit filing. But neither will connect these two seemingly unrelated facts, combine them with the new CEO's background, and reason that they suggest a deliberate strategic move. That is analytical judgment — and it is exactly what Dossier does, transparently, with a full derivation chain the user can inspect and challenge.

Dossier surfaces evidence-backed deductions and clearly labels them as deductions. It shows exactly how it derived them. And it lets you challenge them.

---

## 5. Architecture

### 5.1 Design principles

1. **The evidence graph is the core. Everything else is a view or a worker.** The evidence graph (sources, extracts, claims, links, reviews) is the persistent, authoritative data structure. Agents are stateless workers that read from and write to this graph. The dossier is a view rendered from this graph. The UI is a set of views on this graph.

2. **Agents are workers, not personalities.** Each agent type has a clear, bounded job. They do not have "opinions" or "expertise." They execute defined evidence operations: search, extract, score, challenge, synthesize. The intelligence is in the framework and the graph constraints, not in the prompt theater.

3. **Deterministic where possible, generative only where necessary.** Retrieval, parsing, storage, linking, citation assembly, scoring, and review logging are all deterministic operations. LLM generation is used only for: scoping questions, reading and extracting from sources, detecting semantic contradictions, cross-evidence deduction, and writing the final narrative layer.

4. **Fail visibly.** When a source cannot be reached, it is logged as a gap. When an extraction is uncertain, it is marked uncertain. When evidence is insufficient, the conclusion says "insufficient evidence." The system never papers over failure with confident-sounding text.

5. **Self-contained deployment.** The entire system runs from a single `docker compose up` command. No external services required beyond the LLM and search API keys the user provides. No accounts, no auth server, no cloud dependencies.

6. **Provider abstraction at every layer.** LLM calls go through a unified provider interface (LiteLLM). Search calls go through a search adapter interface. Storage goes through a storage adapter. Swapping any provider is a config change, not a code change.

### 5.2 System architecture (high level)

```
┌──────────────────────────────────────────────────────┐
│                     USER LAYER                        │
│  Web UI (localhost:3000) • REST API • CLI • Embeds    │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│                  API GATEWAY                           │
│  POST /investigate                                    │
│  GET  /investigate/{id}                               │
│  GET  /investigate/{id}/evidence                      │
│  GET  /investigate/{id}/dossier                       │
│  POST /investigate/{id}/challenge                     │
│  POST /investigate/{id}/continue                      │
│  GET  /investigate/{id}/trace                         │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│               ORCHESTRATOR (state machine)             │
│                                                       │
│  Manages investigation lifecycle:                      │
│  Intake → Scoping → Evidence → Review → Publish       │
│                                                       │
│  Deterministic state machine (not an LLM).            │
│  Routes work to agent pools. Enforces budgets,        │
│  timeouts, quality gates, and stop conditions.        │
│                                                       │
│  Implemented as: custom state machine backed by        │
│  the local database + in-process task queue.          │
└───────┬───────────┬───────────┬───────────┬──────────┘
        │           │           │           │
   ┌────▼───┐ ┌────▼───┐ ┌────▼───┐ ┌────▼────┐
   │Planner │ │Research│ │Adversa│ │ Writer  │
   │ Agent  │ │ Agents │ │ry     │ │ Agent   │
   │        │ │ (pool) │ │ Agent │ │         │
   └────┬───┘ └────┬───┘ └───┬───┘ └────┬────┘
        │          │         │           │
   ┌────▼──────────▼─────────▼───────────▼─────────┐
   │          PROVIDER ABSTRACTION LAYER            │
   │                                                │
   │  LLM Adapter (LiteLLM):                       │
   │    OpenAI │ Anthropic │ Google │ Groq │        │
   │    Mistral │ Ollama │ vLLM │ LM Studio │      │
   │    Any OpenAI-compatible endpoint              │
   │                                                │
   │  Search Adapter:                               │
   │    Tavily │ Serper │ Brave │ SearXNG (free)   │
   │    DuckDuckGo (free, no key) │ Custom          │
   │                                                │
   │  Storage Adapter:                              │
   │    Local disk │ S3 │ MinIO                     │
   └───────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────┐
│                  EVIDENCE GRAPH                        │
│                                                       │
│  SQLite (default, zero config) or PostgreSQL (scale)  │
│  Local file storage: raw documents, screenshots, PDFs │
│  Full-text search: SQLite FTS5 (default) or PG FTS   │
│                                                       │
│  This is the single source of truth.                  │
│  All agents read from and write to this graph.        │
│  The dossier is a rendered view of this graph.        │
└──────────────────────────────────────────────────────┘
```

### 5.3 Deployment model

**Minimum deployment (one machine, one command):**
```bash
docker compose up
# Starts: API server, web UI, task worker, SQLite database
# Requirements: Docker, 2GB RAM, one LLM API key
```

**Full deployment (power users):**
```bash
docker compose --profile full up
# Starts: API server, web UI, task workers (multiple),
#   PostgreSQL, Redis, Playwright browser worker
# Requirements: Docker, 4GB+ RAM, LLM API key, search API key
```

**Developer deployment (from source):**
```bash
pip install -e ".[dev]"
cd frontend && npm install && npm run dev
python -m dossier.server
```

**Configuration is one file:**
```env
# .env — the only file you need to edit

# LLM Provider (required — pick one)
LLM_PROVIDER=openai                    # or: anthropic, google, groq, ollama, custom
LLM_API_KEY=sk-...                     # your key (not needed for Ollama)
LLM_MODEL=gpt-4o                       # or: claude-sonnet-4-20250514, gemini-2.0-flash, llama3, etc.

# Search Provider (optional — SearXNG or DuckDuckGo work without a key)
SEARCH_PROVIDER=tavily                 # or: serper, brave, searxng, duckduckgo
SEARCH_API_KEY=tvly-...               # not needed for searxng or duckduckgo

# Database (optional — defaults to SQLite)
DATABASE_URL=sqlite:///data/dossier.db # or: postgresql://user:pass@localhost/dossier

# Storage (optional — defaults to local disk)
STORAGE_BACKEND=local                  # or: s3, minio
STORAGE_PATH=./data/storage            # local path or S3 bucket

# Advanced (optional)
MAX_PARALLEL_RESEARCHERS=5             # how many researcher agents run in parallel
INVESTIGATION_BUDGET_CAP=50            # max LLM calls per investigation
PLAYWRIGHT_ENABLED=false               # enable browser automation for JS-heavy sites
```

### 5.4 Fully offline mode (Ollama + SearXNG)

For users who want zero data to leave their machine:

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1:70b
LLM_API_KEY=                           # not needed
SEARCH_PROVIDER=searxng                # self-hosted SearXNG instance
SEARCH_API_KEY=                        # not needed
```

The docker-compose includes an optional SearXNG service:
```bash
docker compose --profile offline up
# Starts everything + a local SearXNG instance
# Fully air-gapped operation (except SearXNG's outbound search requests)
```

Investigation quality scales with model capability. GPT-4o and Claude Sonnet produce excellent results. Llama 3.1 70B produces good results. Smaller models produce usable but lower-fidelity results. The README includes a model compatibility matrix with quality ratings.

### 5.5 What is NOT in the architecture

These things were in the original blueprint but have been removed for good reason:

| Removed | Why |
|---------|-----|
| Governing Board agent | Policy is a config file, not an LLM decision. Source quality rules, safety boundaries, and tool permissions are static configuration loaded at startup. |
| Operations Controller agent | Queue management, retries, budgets, and timeouts are infrastructure code in the Orchestrator. An LLM should not manage infrastructure. |
| Librarian agent | Deduplication, indexing, and citation formatting are algorithmic functions inside the Evidence Graph service. Not an LLM task. |
| Chief Scientist agent | Method selection and evidence thresholds are encoded in the Planner prompt and the quality gate configuration. One planning step, not a separate agent. |
| Ethics/Compliance agent | Safety boundaries are enforced by the Orchestrator's policy config: blocked domains, content filters, rate limits. Deterministic, not generative. |
| Director agent | The Orchestrator state machine handles routing, budgets, and lifecycle. The Planner agent handles scoping. The "Director" was orchestration logic wearing an LLM costume. |
| Postdoc / Research Scientist / RA distinction | These are all variations of the same job: search, read, extract. The Researcher agent type handles all of this with task-specific instructions per assignment. |
| Managed cloud infrastructure | Dossier is self-hosted. There is no cloud service to manage. Users bring their own compute, their own API keys, their own storage. |
| User account system | For self-hosted single-user or small-team deployment, authentication is optional. Multi-user auth can be added via environment config (basic auth, reverse proxy, or OIDC). |

**Result:** 5 agent types instead of 12 (Planner, Researcher, Adversary, Analyst, Writer). Self-contained deployment. Same evidence-gathering capability as the original 12-agent design, plus a deduction capability (Analyst) the original lacked. 60% less LLM spend. 90% less prompt-engineering surface area. Easier to debug, test, and improve.

---

## 6. Agent Model

### 6.1 The five agent types

Dossier uses exactly five agent types. Each has a single, well-defined purpose, a bounded input/output contract, and a clear tool whitelist.

#### Planner Agent

**Purpose:** Turn a user question into a scoped investigation plan.

**Input:**
- User's question
- User's stated constraints (time, budget, output type, focus areas)
- Domain template (if applicable)

**Output (structured, not prose):**
- Investigation title
- Restated objective (one sentence)
- 3-8 hypotheses to test or subquestions to answer
- Recommended research lanes (e.g., financial, legal, technical, market, competitor)
- Suggested source classes per lane (e.g., SEC filings, news, academic, social, government)
- Estimated depth tier (quick scan / standard / deep investigation)
- Stop conditions (what would constitute "enough evidence")
- Exclusions (what is explicitly out of scope)

**Tools allowed:** None. The Planner has read-only access to domain templates and the user's question. It does not search, browse, or fetch.

**LLM calls:** 1 (one structured planning call). This is not a multi-turn conversation. It is a single, well-prompted call that returns structured JSON.

**Why one agent, not three (Director + Chief Scientist + PI):**
Scoping, method selection, and question decomposition are one cognitive act, not three. Splitting them into separate agents creates unnecessary round-trips, increases latency, and adds failure modes without improving output quality. A single well-designed planning prompt produces better results than three agents negotiating.

#### Researcher Agent (parallelized pool)

**Purpose:** Gather evidence for one research lane or subquestion.

**Input:**
- One subquestion or hypothesis to investigate
- Assigned source classes to search
- Evidence quality standards (from investigation plan)
- Budget cap (max searches, max tokens)

**Output (structured):**
- List of sources found (with full metadata)
- Extracted evidence items (quote, context, relevance)
- Initial relevance and quality assessment per item
- Gaps encountered (paywalled sources, empty searches, ambiguous results)
- Suggested follow-up searches (if budget allows)

**Tools allowed:**
- Web search API (Tavily, Serper, or Brave Search)
- Web page fetcher (HTTP client with HTML extraction)
- PDF parser
- Browser automation (Playwright — fallback only, for JS-heavy or interactive pages)
- Screenshot capture (for evidence preservation)

**Parallelism:** Multiple Researcher agents run simultaneously, one per research lane. A standard investigation runs 3-5 Researchers in parallel. A deep investigation runs 5-10.

**Key constraint:** Researchers gather and extract. They do not synthesize, conclude, or score. Every output is an evidence item with provenance, not a judgment.

#### Adversary Agent

**Purpose:** Challenge the evidence and conclusions. Find contradictions. Identify weaknesses.

**Input:**
- The current evidence graph (all claims, evidence items, and sources)
- The investigation plan (to understand what was supposed to be investigated)

**Output (structured):**
- Challenged claims (with specific reason for each challenge)
- Contradictory evidence found (with full provenance chain)
- Source independence issues identified (derived sources counted as independent)
- Freshness issues (stale evidence supporting current claims)
- Missing evidence (what should exist but was not found)
- Overclaiming (conclusions that go beyond what the evidence supports)
- Unsupported inferences (logical leaps without evidence)

**Tools allowed:**
- Same search and fetch tools as Researcher agents
- Evidence Graph read access (to inspect existing evidence)
- Review annotation write access (to flag issues on specific claims)

**Key design principle:** The Adversary has a fundamentally different system prompt than the Researchers. It is not trying to support the emerging conclusions. It is trying to break them. Its explicit instruction is: "Your job is to find the strongest possible case against each major claim. Search for contradictions. Identify weak evidence. Name the gaps. If the conclusion cannot survive your challenge, it should not appear in the dossier."

**Why this matters:** This is the single strongest argument for multi-agent architecture in the entire system. A single LLM asked to "research and then challenge your own work" produces weak, performative challenges. A separate agent with a separate prompt, separate search strategy, and adversarial framing produces genuine challenges that improve the final output.

#### Writer Agent

**Purpose:** Produce the final dossier from the structured evidence graph. No new research. No new claims. Only assembly and narration.

**Input:**
- The complete evidence graph (claims, evidence items, reviews, gaps)
- Investigation metadata (title, objective, scope, completion status)
- Output format specification (executive brief, full dossier, memo, etc.)

**Output:**
- Structured dossier with sections mapped to evidence
- Every paragraph references specific evidence items
- Counter-evidence section drawn from Adversary output
- Gaps section drawn from logged gaps across all agents
- Confidence assessment based on evidence scoring (not LLM improvisation)

**Tools allowed:**
- Evidence Graph read access ONLY
- No search tools. No fetch tools. No browser.

**Key constraint:** The Writer cannot introduce new information. It can only organize, narrate, and format information that already exists in the evidence graph. If the Writer needs a fact that is not in the evidence graph, it must flag it as a gap, not generate it.

This constraint is the most important safety mechanism in the entire system. It prevents the most common failure mode of AI research: the final report containing claims that were never actually found in any source.

#### Analyst Agent (The Deduction Engine)

**Purpose:** Reason across the complete evidence graph to derive evidence-backed deductions that no single source contains. Each deduction shows exactly how it was derived, and all deductions are clearly labeled as deductions.

**Input:**
- The complete evidence graph (all claims, evidence items, sources, reviews, and gaps)
- The investigation plan (hypotheses, research lanes, objective)
- Adversary review notes (which claims are strong, which are weak, what gaps remain)

**Output (structured):**
- List of evidence-backed deductions, each with:
  - Deduction statement (the derived conclusion)
  - Derivation chain (which specific evidence items, combined with what reasoning, produce this deduction)
  - Deduction type (temporal pattern, cross-source contradiction, absence-as-evidence, cross-lane connection, implication extraction)
  - Confidence assessment (how strong is the logical chain?)
  - Falsification condition (what would disprove this deduction?)
- Cross-lane connections identified
- Anomalies flagged (things that do not add up across the evidence)

**Tools allowed:**
- Evidence Graph read access ONLY
- No search tools. No fetch tools. No browser.

**Key constraints:**
1. **Every deduction must have a derivation chain.** A deduction without a chain linking it to specific evidence items is rejected by the Orchestrator. No "I think..." without showing the evidence-to-conclusion path.
2. **Deductions are labeled distinctly from claims.** The user always knows whether they are reading a directly sourced fact or a derived conclusion. There is no blending.
3. **The Adversary reviews deductions.** After the Analyst produces deductions, the Adversary agent gets a second pass to challenge them. Is the reasoning sound? Are there alternative explanations? Is the Analyst overclaiming?
4. **The Analyst cannot search.** Like the Writer, the Analyst works only with what the Researchers already found. It cannot introduce new external information. Its power comes from reasoning across existing evidence, not from finding new evidence.

**LLM requirements:** The Analyst agent benefits most from the strongest available model. For cross-evidence reasoning, GPT-4o, Claude Sonnet/Opus, or Gemini 1.5 Pro are recommended. Smaller models can still find simple temporal patterns but will miss subtle cross-lane connections.

**Why this is a separate agent, not part of the Writer:**
The Writer's job is narration — organizing existing information into a readable dossier. The Analyst's job is deduction — deriving conclusions that don't exist yet. Mixing these two capabilities in one agent produces either a Writer that invents unsupported conclusions (dangerous) or an Analyst that gets distracted by formatting (wasteful). Separation of concerns makes both agents better at their specific job.

### 6.2 Agent interaction model

```
                    User question
                         │
                         ▼
                   ┌──────────┐
                   │ PLANNER  │  (1 call — produces investigation plan)
                   └────┬─────┘
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
      ┌──────────┐┌──────────┐┌──────────┐
      │RESEARCH-1││RESEARCH-2││RESEARCH-3│  (parallel — evidence gathering)
      └────┬─────┘└────┬─────┘└────┬─────┘
           │           │           │
           └───────────┼───────────┘
                       │
                       ▼
              ┌────────────────┐
              │   ADVERSARY    │  (challenges evidence + claims)
              └───────┬────────┘
                      │
               ┌──────┴──────┐
               │             │
               ▼             ▼
        Evidence is     Gaps or weak
        sufficient      claims found
               │             │
               │             ▼
               │     (loop: dispatch more Researchers
               │      to address specific gaps, then
               │      Adversary reviews again)
               │             │
               │      Max 2 review loops
               │             │
               └──────┬──────┘
                      │
                      ▼
              ┌────────────────┐
              │    ANALYST     │  (cross-evidence reasoning —
              │  (deduction    │   derives evidence-backed deductions)
              │   engine)      │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │  ADVERSARY #2  │  (challenges the Analyst's
              │  (deduction    │   derived deductions)
              │   review)     │
              └───────┬────────┘
                      │
                      ▼
               ┌──────────┐
               │  WRITER  │  (produces dossier from evidence
               └──────────┘   graph + evidence-backed deductions)
                      │
                      ▼
                  DOSSIER
```
                      │
                      ▼
                  DOSSIER
```

**The review loop is bounded:** Maximum 2 rounds of Adversary → additional Research → Adversary. This prevents infinite investigation spirals while ensuring the most important gaps are addressed.

---

## 7. Research Lifecycle

### 7.1 Phase overview

| Phase | Name | Duration | What happens | Who acts |
|-------|------|----------|-------------|----------|
| 1 | Intake | Instant | User submits question. System validates it, creates case. | Orchestrator |
| 2 | Scoping | 10-30 sec | Planner decomposes question, creates investigation plan. User reviews if enabled. | Planner Agent |
| 3 | Evidence Gathering | 2-40 min | Researchers search, fetch, read, and extract evidence in parallel. | Researcher Agents (pool) |
| 4 | Adversarial Review | 2-15 min | Adversary challenges conclusions, finds contradictions, identifies gaps. | Adversary Agent |
| 5 | Gap Filling (optional) | 2-20 min | Additional targeted research on gaps identified by Adversary. | Researcher Agents (targeted) |
| 6 | Second Review (optional) | 2-10 min | Adversary re-reviews with new evidence. | Adversary Agent |
| 7 | **Deduction** | 1-5 min | **Analyst agent reasons across the full evidence graph to derive evidence-backed deductions — conclusions that no single source contains but that the combined evidence implies. Each deduction includes its full derivation chain.** | **Analyst Agent** |
| 8 | Deduction Review | 1-3 min | Adversary reviews the Analyst's deductions for logical soundness, alternative explanations, and overclaiming. | Adversary Agent |
| 9 | Assembly | 30-120 sec | Writer produces dossier from evidence graph + evidence-backed deductions. | Writer Agent |
| 10 | Publication | Instant | Dossier is stored, indexed, and optionally shared. | Orchestrator |

**Total time:**
- Quick scan: 5-15 minutes
- Standard investigation: 20-50 minutes
- Deep investigation: 1-4 hours

### 7.2 Phase 1 — Intake

**Input from user:**
- Primary question (free text, required)
- Focus areas (optional; e.g., "focus on financial risk and legal exposure")
- Depth preference (quick / standard / deep)
- Output format preference (executive brief / full dossier / evidence pack only)
- Constraints (optional; e.g., "only sources from 2024 or later", "focus on EU market")

**System actions:**
- Validate question (is it a researchable question? reject if it is a greeting, command, or harmful request)
- Create case record in database
- Assign case ID
- Select domain template if one matches (e.g., the question mentions a company name → company due diligence template)
- Pass to Planner

**What the user sees:**
"Your investigation has been opened. Scoping in progress."

### 7.3 Phase 2 — Scoping

**The Planner Agent receives:**
- User's question + constraints
- Domain template (if applicable)
- System-level policy config (max sources, max budget, etc.)

**The Planner produces (structured JSON):**
```json
{
  "title": "AWS vs GCP Migration Assessment for Mid-Scale SaaS",
  "objective": "Determine whether migrating from AWS to GCP is advisable given $40K/month spend, with focus on cost, reliability, migration risk, and vendor lock-in.",
  "hypotheses": [
    "GCP offers meaningful cost savings for the described workload profile.",
    "GCP reliability is comparable to or better than AWS for SaaS workloads.",
    "Migration risk is manageable within 6 months with standard tooling.",
    "Vendor lock-in risk is similar or lower with GCP compared to AWS."
  ],
  "research_lanes": [
    {
      "lane": "Cost Comparison",
      "subquestions": ["What is GCP's pricing for compute, storage, and networking vs AWS?", "What discounts apply (sustained use, committed use)?", "What are real-world cost comparison reports?"],
      "source_classes": ["vendor_documentation", "third_party_benchmarks", "user_reports"]
    },
    {
      "lane": "Reliability and Performance",
      "subquestions": ["What are GCP's SLA guarantees vs AWS?", "What major outages has each had in the past 2 years?", "What do users report about real-world reliability?"],
      "source_classes": ["vendor_documentation", "incident_reports", "user_forums", "analysis_reports"]
    },
    {
      "lane": "Migration Risk",
      "subquestions": ["What are the common migration challenges?", "What tooling exists?", "What do companies that have migrated report?"],
      "source_classes": ["case_studies", "technical_documentation", "user_reports"]
    },
    {
      "lane": "Vendor Lock-in",
      "subquestions": ["Which services have GCP-specific APIs vs open standards?", "How does Kubernetes/Anthos compare to EKS for portability?", "What is the switching cost analysis?"],
      "source_classes": ["technical_analysis", "vendor_documentation", "industry_reports"]
    }
  ],
  "depth_tier": "standard",
  "researcher_count": 4,
  "stop_conditions": [
    "Each lane has at least 3 independent sources supporting its main finding.",
    "At least one contradiction search has been completed per lane.",
    "All user-specified focus areas have been addressed."
  ],
  "exclusions": ["We will not estimate exact migration cost for the specific workload (requires detailed usage data). We will provide ranges from comparable migrations."]
}
```

**Human-in-the-loop checkpoint (optional, configurable):**
For paid tier users, the system can pause here and show the investigation plan before proceeding. The user can:
- Approve the plan
- Add or remove research lanes
- Narrow or expand scope
- Adjust depth

This checkpoint prevents wasting compute on an investigation that is scoped incorrectly.

### 7.4 Phase 3 — Evidence Gathering

The Orchestrator dispatches one Researcher agent per research lane.

Each Researcher:
1. Takes its assigned subquestions and source classes.
2. Executes searches (3-15 search queries per lane, depending on depth tier).
3. Fetches and reads promising results.
4. Extracts structured evidence items:
   - Source metadata (URL, title, author, publisher, date, source class)
   - Extracted text (the specific quote or data point)
   - Relevance to the subquestion
   - Initial quality assessment (is this primary data, analysis, or opinion?)
5. Stores all evidence items in the Evidence Graph.
6. Logs gaps (paywalled sources, empty searches, ambiguous results).

**Parallel execution:** All Researchers run simultaneously. The Orchestrator waits for all to complete (with a timeout per agent).

**Budget control:** Each Researcher has:
- A maximum number of search queries (e.g., 15 for standard tier)
- A maximum number of pages to fetch (e.g., 30 for standard tier)
- A maximum token budget for LLM extraction calls
- A timeout (e.g., 10 minutes for standard tier)

### 7.5 Phase 4 — Adversarial Review

The Adversary Agent receives the complete evidence graph and investigation plan.

It systematically:
1. **Checks source independence.** Builds the source citation graph. Identifies derived sources. Recalculates true independent source count per claim.
2. **Searches for contradictions.** Runs targeted searches designed to find evidence AGAINST each major finding. Uses different search queries than the Researchers used.
3. **Checks freshness.** Flags evidence items that are stale relative to the decision's time-sensitivity.
4. **Checks for overclaiming.** Identifies claims where the evidence is "Company X grew 20% in 2024" but the claim says "Company X is a fast-growing company" (overgeneralization).
5. **Identifies gaps.** What should have been found but was not? What source classes were underrepresented?
6. **Writes review notes.** Each issue is a structured annotation on the relevant claim or evidence item.

**Output:** The Adversary does NOT rewrite the dossier. It writes structured review notes attached to specific claims and evidence items. These notes are then used by:
- The Orchestrator (to decide if a second research round is needed)
- The Writer (to include counter-evidence and caveats in the dossier)

### 7.6 Phase 5 & 6 — Gap Filling and Second Review

If the Adversary identifies significant gaps or contradictions:
- The Orchestrator dispatches targeted Researcher agents to address SPECIFIC gaps (not general re-research).
- After gap filling, the Adversary runs a second pass on the new evidence.
- Maximum 2 total review cycles to prevent infinite loops.

**Stop conditions (evaluated after each review cycle):**
- All critical gaps have been addressed or flagged as unfillable.
- No new high-severity contradictions found.
- Evidence coverage meets the threshold from the investigation plan.
- Budget or time cap reached.

### 7.7 Phase 7 — Deduction (The Cross-Evidence Reasoning Phase)

This is the phase that differentiates Dossier from every other research tool.

The Analyst agent receives the complete evidence graph — all claims, all evidence items, all sources, all Adversary review notes, all gaps — and performs cross-evidence reasoning to derive deductions that no single source contains.

**What the Analyst looks for:**

1. **Temporal patterns.** Events across different research lanes that form suspicious sequences when placed on a timeline. No source connects them, but the timing implies a relationship.

2. **Cross-lane connections.** Findings from the "Financial" lane that, when combined with findings from the "Legal" lane, produce a conclusion neither lane could reach alone.

3. **Contradiction implications.** When two sources contradict each other, the *existence* of the contradiction may itself be meaningful. Why do these sources disagree? What does the disagreement imply?

4. **Absence patterns.** Information that should exist but doesn't. A company that should have public financial filings but doesn't. A product that should have safety certifications but doesn't. The absence — when combined with other evidence — may lead to a derived conclusion.

5. **Convergence signals.** Multiple independent weak signals that, individually, mean little, but collectively point to the same conclusion with high confidence.

**Output:** A set of structured deductions, each with a derivation chain, confidence assessment, and falsification condition. These are stored as INSIGHT entities in the evidence graph, distinct from CLAIM entities.

**Budget:** The Analyst makes 1-3 LLM calls (one for the primary analysis pass, optional refinement calls for complex evidence graphs). This phase adds minimal cost (typically < $0.50 even with GPT-4o).

### 7.8 Phase 8 — Deduction Review

The Adversary agent runs a focused second pass, this time reviewing ONLY the Analyst's deductions (not re-reviewing the original claims, which were already reviewed in Phase 4/6).

For each deduction, the Adversary evaluates:
- Is the derivation chain logically sound?
- Are there alternative explanations the Analyst did not consider?
- Is the Analyst overclaiming (weak evidence presented as strong deduction)?
- Is the deduction trivially obvious (restating what a source already said, disguised as a deduction)?

Deductions that fail review are either downgraded in confidence or removed entirely. Deductions that survive review are marked as "Adversary-reviewed" and included in the dossier with full transparency.

### 7.9 Phase 9 — Assembly

The Writer Agent produces the dossier from the evidence graph AND the Analyst's evidence-backed deductions.

Rules:
1. Every claim paragraph references at least one evidence item.
2. Deductions are presented in a dedicated section, clearly labeled as "Evidence-Backed Deductions" — never blended with directly sourced findings.
3. Each deduction includes its full derivation chain so the user can see exactly how it was derived — and challenge it.
4. The counter-evidence section includes all high-severity Adversary findings (for both claims and deductions).
5. The gap section lists ALL logged gaps from ALL agents.
6. Confidence assessments use the Adversarial Confidence Model (support strength + challenge strength, NOT a made-up number).
7. The Writer cannot introduce claims or deductions not already in the evidence graph.
8. Language that indicates false certainty (e.g., "it is clear that," "undoubtedly," "certainly") is prohibited by the Writer's system prompt.

### 7.10 Phase 10 — Publication

The dossier is:
- Stored in the database with full evidence graph and deduction records
- Assigned a permanent URL (for sharing)
- Indexed for future cross-case knowledge
- Optionally: emailed or pushed to the user's integration

---

## 8. Trust Architecture

Trust is not a feature. It is the product. If users do not trust the dossier, it has zero value regardless of how sophisticated the backend is.

### 8.1 The six pillars of trust

#### Pillar 1: Full provenance

Every claim → evidence item → source → extracted quote → retrieval timestamp.

The user can always drill down from a conclusion to the raw source material. This chain is never broken, never summarized away, and never hidden. If the chain is incomplete for any claim, that claim is automatically marked as "insufficiently supported" regardless of how plausible it sounds.

#### Pillar 2: Source independence

The user can see which sources are truly independent and which are derived from the same original source. The source independence graph is visible in the evidence board.

When the dossier says "supported by 4 independent sources," it means 4 entities that arrived at the same conclusion independently. Not 4 articles that all cite the same press release.

#### Pillar 3: Active challenge

Every dossier includes a counter-evidence section. This is not optional.

The system actively searched for reasons the conclusion might be wrong. The strongest counter-evidence is presented alongside the main findings. If no counter-evidence was found, the system says "We searched for contradictory evidence and found none" — which is itself a meaningful finding.

#### Pillar 4: Named gaps

The "What We Could Not Determine" section exists in every dossier. It lists:
- What was searched for but not found
- What was found but inaccessible (paywalled, restricted)
- What questions remain unanswered
- What additional information would strengthen or weaken the conclusion

This section is the single most honest thing any research product can offer. It puts a boundary around the dossier's knowledge and shows the user exactly where that boundary is.

#### Pillar 5: No false certainty

The system is designed to produce accurate calibration, not impressive-sounding confidence scores.

Rules:
- If evidence is insufficient, the dossier says "insufficient evidence" instead of presenting a weak conclusion as moderate.
- Confidence assessments are two-dimensional (support strength + challenge strength), not a single misleading number.
- Language constraints prevent the Writer from using certainty-signaling words ("clear," "obvious," "undoubtedly") unless support strength exceeds 0.85 AND challenge strength is below 0.20.
- If the answer to the user's question is genuinely "we cannot determine this from available public sources," the system says that rather than generating a plausible-sounding answer.

#### Pillar 6: Transparent deduction

When Dossier derives an evidence-backed deduction through cross-evidence reasoning, the deduction is always:
- **Labeled distinctly** from directly sourced claims. The user always knows whether they are reading a fact from a source or a conclusion the system derived.
- **Accompanied by a full derivation chain** showing exactly which evidence items, combined with what reasoning, produced the deduction.
- **Adversary-reviewed.** The same adversarial process applied to sourced claims is applied to deductions.
- **Falsifiable.** Each deduction states what evidence would disprove it.
- **Challengeable.** The user can inspect the full chain and challenge the deduction directly.

This pillar exists because cross-evidence deduction is the most powerful capability in the system — and the most dangerous if presented without transparency. A deduction presented as a sourced fact would be a hallucination with extra steps. The mandatory labeling and derivation chain prevent this.

### 8.2 What would break trust

These are the failure modes that the architecture is specifically designed to prevent:

| Failure mode | Prevention mechanism |
|---|---|
| Source says X, dossier claims Y | Evidence Provenance Chain — every claim links to an exact quote |
| 5 sources cited but all from the same press release | Source Independence Graph — derived sources are flagged |
| Confident conclusion from thin evidence | Adversarial Confidence Model — weak support is visible |
| Missing important counter-evidence | Adversary Agent — dedicated contradiction search |
| Stale information presented as current | Evidence Freshness Decay — timestamps and freshness labels on all sources |
| Silent gaps (user does not know what is missing) | Gap Transparency — explicit "what we could not determine" section |
| Writer invents facts not in evidence | Writer Agent has no search tools; can only render the evidence graph |
| User finds an error and loses trust in everything | Challenge endpoint — user can dispute specific claims, triggering re-investigation of that claim |
| Deduction presented as sourced fact | Mandatory labeling — deductions are always visually and structurally distinct from claims; derivation chain is always visible |
| Analyst makes a logical leap without evidence | Derivation chain requirement — deductions without chains referencing specific evidence items are rejected by the Orchestrator; Adversary reviews all deductions |

---

## 9. Data Model

### 9.1 Core entities

```
CASE
├── case_id            (uuid, primary key)
├── title              (text)
├── user_question      (text)
├── objective          (text)
├── depth_tier         (enum: quick, standard, deep)
├── status             (enum: intake, scoping, investigating, reviewing,
│                       assembling, published, archived)
├── created_at         (timestamp)
├── updated_at         (timestamp)
├── published_at       (timestamp, nullable)
├── owner_user_id      (uuid, foreign key)
├── overall_support    (float, 0-1)
├── overall_challenge  (float, 0-1)
├── evidence_count     (int)
├── source_count       (int)
├── independent_source_count (int)
└── gap_count          (int)

INVESTIGATION_PLAN
├── plan_id            (uuid, primary key)
├── case_id            (uuid, foreign key)
├── hypotheses         (jsonb — array of hypothesis objects)
├── research_lanes     (jsonb — array of lane objects with subquestions)
├── stop_conditions    (jsonb — array of condition strings)
├── exclusions         (jsonb — array of exclusion strings)
├── researcher_count   (int)
├── depth_tier         (enum)
├── approved_by_user   (boolean, default false)
└── created_at         (timestamp)

AGENT_RUN
├── run_id             (uuid, primary key)
├── case_id            (uuid, foreign key)
├── agent_type         (enum: planner, researcher, adversary, analyst, writer)
├── lane               (text, nullable — which research lane this agent worked on)
├── status             (enum: running, completed, failed, timeout)
├── started_at         (timestamp)
├── completed_at       (timestamp, nullable)
├── token_budget       (int)
├── tokens_used        (int)
├── search_budget      (int)
├── searches_used      (int)
└── error              (text, nullable)

SOURCE
├── source_id          (uuid, primary key)
├── case_id            (uuid, foreign key)
├── url                (text)
├── canonical_url      (text — normalized, deduplicated)
├── title              (text)
├── publisher          (text, nullable)
├── author             (text, nullable)
├── published_at       (timestamp, nullable)
├── retrieved_at       (timestamp)
├── source_class       (enum: primary, vendor_documentation, government,
│                       academic, news, analysis, industry_report,
│                       user_report, social, aggregator, unknown)
├── freshness          (enum: current, recent, aging, stale)
├── extraction_quality (enum: high, medium, low)
├── cites_sources      (jsonb — array of source_ids this source cites/derives from)
├── is_independent     (boolean — computed from citation graph)
├── raw_content_path   (text — path to stored raw HTML/PDF in object storage)
└── found_by_run_id    (uuid, foreign key to agent_run)

EVIDENCE_ITEM
├── evidence_id        (uuid, primary key)
├── case_id            (uuid, foreign key)
├── source_id          (uuid, foreign key)
├── extracted_text     (text — the exact quote or data point)
├── context            (text — surrounding context for the extract)
├── lane               (text — which research lane this belongs to)
├── relevance_to       (text — which subquestion this addresses)
├── extracted_by_run   (uuid, foreign key to agent_run)
├── quality            (enum: high, medium, low)
└── created_at         (timestamp)

CLAIM
├── claim_id           (uuid, primary key)
├── case_id            (uuid, foreign key)
├── statement          (text)
├── lane               (text)
├── support_strength   (float, 0-1)
├── challenge_strength (float, 0-1)
├── confidence_label   (enum: settled, contested, uncertain, doubtful,
│                       insufficient)
├── independent_support_count (int)
├── status             (enum: draft, reviewed, challenged, final)
└── created_at         (timestamp)

CLAIM_EVIDENCE_LINK
├── link_id            (uuid, primary key)
├── claim_id           (uuid, foreign key)
├── evidence_id        (uuid, foreign key)
├── relation           (enum: supports, contradicts, partially_supports,
│                       context_only)
└── strength           (float, 0-1 — how strongly this evidence supports
                        or contradicts the claim)

REVIEW_NOTE
├── review_id          (uuid, primary key)
├── case_id            (uuid, foreign key)
├── claim_id           (uuid, foreign key, nullable — if about a specific claim)
├── evidence_id        (uuid, foreign key, nullable — if about specific evidence)
├── reviewer_run_id    (uuid, foreign key to agent_run)
├── issue_type         (enum: contradiction_found, stale_evidence,
│                       overclaiming, source_dependence, missing_evidence,
│                       unsupported_inference, circular_citation)
├── severity           (enum: critical, high, medium, low)
├── description        (text)
├── counter_evidence   (jsonb, nullable — array of evidence_ids that contradict)
└── created_at         (timestamp)

GAP
├── gap_id             (uuid, primary key)
├── case_id            (uuid, foreign key)
├── gap_type           (enum: no_results, paywalled, restricted, ambiguous,
│                       unanswerable_from_public_sources, time_sensitive)
├── description        (text)
├── search_query_used  (text, nullable)
├── logged_by_run_id   (uuid, foreign key to agent_run)
└── created_at         (timestamp)

DOSSIER
├── dossier_id         (uuid, primary key)
├── case_id            (uuid, foreign key)
├── version            (int)
├── format             (enum: executive_brief, full_dossier, evidence_pack)
├── content            (jsonb — structured dossier with section references)
├── rendered_markdown  (text)
├── rendered_html      (text)
├── published_at       (timestamp)
├── share_token        (text, unique — for public share URLs)
└── is_public          (boolean, default false)

INSIGHT
├── insight_id         (uuid, primary key)
├── case_id            (uuid, foreign key)
├── statement          (text — the derived conclusion)
├── deduction_type     (enum: temporal_pattern, cross_source_contradiction,
│                       absence_as_evidence, cross_lane_connection,
│                       implication_extraction, convergence_signal)
├── derivation_chain   (jsonb — ordered array of:
│                       { evidence_id, role_in_chain, reasoning_step })
├── confidence         (float, 0-1)
├── confidence_label   (enum: strong_deduction, moderate_deduction,
│                       speculative, rejected)
├── falsification      (text — what would disprove this deduction)
├── adversary_reviewed (boolean, default false)
├── adversary_verdict  (enum: confirmed, weakened, rejected, nullable)
├── adversary_notes    (text, nullable)
├── analyst_run_id     (uuid, foreign key to agent_run)
└── created_at         (timestamp)
```

### 9.2 Storage architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Relational data | PostgreSQL | All entities above. The evidence graph. Case metadata. User accounts. |
| Raw content | S3-compatible object storage (MinIO for self-hosted, S3 for cloud) | Raw HTML pages, PDF files, screenshots. Stored so evidence can always be re-verified. |
| Full-text search | OpenSearch or PostgreSQL full-text (start with PG, migrate to OpenSearch at scale) | Search across evidence items, source text, and claim statements. Needed for cross-case knowledge and duplicate detection. |
| Queue | Redis + BullMQ (Node.js) or Redis + Celery (Python) | Task distribution for parallel agent runs. |
| Cache | Redis | Rate limiting, session state, investigation status polling. |

### 9.3 What is NOT in the data model

- No separate "agent personality" or "agent memory" storage. Agents are stateless workers. Their only persistent output is evidence items, claims, deductions, review notes, and gaps stored in the evidence graph.
- No conversation history with agents. There is no back-and-forth. Each agent run is a single invocation with structured input and output.
- No "institutional knowledge base" for the agents. Cross-case knowledge is handled by the search index over completed cases, not by a separate memory system.

---

## 10. User Experience

### 10.1 Interaction model

The user interacts with Dossier at the investigation level, never at the agent level.

**Primary actions:**
1. **Submit investigation** — type a question, optionally set constraints, click "Investigate."
2. **Watch progress** — see which lanes are being researched, how many sources found, when review starts.
3. **Review plan** (optional) — if enabled, approve or modify the investigation plan before evidence gathering begins.
4. **Read dossier** — when published, read the structured dossier with all sections.
5. **Explore evidence** — drill into the evidence board: filter by lane, source class, support/contradict, and freshness.
6. **Challenge a claim** — click "I don't believe this" on any claim to trigger a targeted re-investigation of that specific claim.
7. **Continue investigation** — request deeper research on a specific lane or subquestion.
8. **Share** — generate a shareable link to the dossier (public or private).

### 10.2 Core views

#### Home / Dashboard

```
┌─────────────────────────────────────────────┐
│                                             │
│  What do you need to investigate?           │
│  ┌─────────────────────────────────────┐    │
│  │                                     │    │
│  │  [Your question here]               │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Depth: [Quick ▾]  Focus: [Optional]       │
│                                             │
│  [Investigate →]                            │
│                                             │
│  ─────────────────────────────────────────  │
│  Recent Investigations                      │
│                                             │
│  • AWS vs GCP Migration — Completed ✓      │
│    47 evidence items • 31 sources • 0.71    │
│                                             │
│  • Vendor X Due Diligence — In Progress ◐  │
│    23 evidence items so far • 4 lanes       │
│                                             │
│  • Treatment Y Safety — Completed ✓        │
│    82 evidence items • 44 sources • 0.83    │
│                                             │
└─────────────────────────────────────────────┘
```

#### Investigation Progress (live)

```
┌─────────────────────────────────────────────┐
│  INVESTIGATION: AWS vs GCP Migration        │
│  Status: Evidence Gathering (Phase 3)       │
│  Elapsed: 12 min                            │
│                                             │
│  Research Lanes                             │
│  ├─ Cost Comparison ████████░░ 80%          │
│  │  12 sources found, 8 evidence items      │
│  ├─ Reliability     ██████░░░░ 60%          │
│  │  9 sources found, 6 evidence items       │
│  ├─ Migration Risk  ████░░░░░░ 40%          │
│  │  5 sources found, 3 evidence items       │
│  └─ Vendor Lock-in  ███░░░░░░░ 30%          │
│     4 sources found, 2 evidence items       │
│                                             │
│  Total: 30 sources • 19 evidence items      │
│  Gaps found so far: 2                       │
│                                             │
│  [View evidence so far] [Pause] [Cancel]    │
│                                             │
└─────────────────────────────────────────────┘
```

#### Dossier (final output)

```
┌─────────────────────────────────────────────┐
│  DOSSIER: AWS vs GCP Migration Assessment   │
│  Published: 2026-03-10 • 47 evidence items  │
│  Sources: 31 (26 independent)               │
│                                             │
│  TABS: [Summary] [Findings] [Deductions]    │
│         [Counter-Evidence] [Gaps]            │
│         [Evidence Board] [Sources] [Trace]  │
│                                             │
│  ─── SUMMARY ───                            │
│                                             │
│  Based on 47 evidence items from 26         │
│  independent sources, we find:              │
│                                             │
│  1. GCP offers 15-25% cost reduction for    │
│     always-on compute workloads.            │
│     Support: Strong (0.82) │ Challenge:     │
│     Weak (0.15) │ SETTLED                   │
│     [4 supporting sources] [0 contradictions]│
│     [Challenge this claim]                  │
│                                             │
│  2. GCP reliability is comparable to AWS    │
│     for SaaS workloads, with fewer but      │
│     longer outages in the past 2 years.     │
│     Support: Moderate (0.68) │ Challenge:   │
│     Moderate (0.45) │ CONTESTED             │
│     [3 supporting] [2 contradictions]       │
│     [Challenge this claim]                  │
│                                             │
│  3. Migration risk is moderate. Typical     │
│     timeline is 4-8 months for comparable   │
│     workloads. [...]                        │
│                                             │
│  ─── COUNTER-EVIDENCE ───                   │
│                                             │
│  • Claim #2 contested: Two incident reports │
│    show GCP had a 4-hour regional outage in │
│    Nov 2025 affecting Compute Engine. AWS   │
│    had no equivalent-severity event in the  │
│    same period.                             │
│    Source: [GCP Status Dashboard]           │
│    Source: [Downdetector Analysis 2025]     │
│                                             │
│  ─── WHAT WE COULD NOT DETERMINE ───       │
│                                             │
│  • Exact cost comparison for your specific  │
│    workload mix (requires detailed usage    │
│    export from AWS Cost Explorer).          │
│  • GCP networking costs for your traffic    │
│    patterns (egress pricing varies by       │
│    destination).                            │
│  • We searched for migration case studies   │
│    from companies with similar stack (React │
│    + Node.js + PostgreSQL on ECS) and found │
│    only 2. Evidence is limited.             │
│                                             │
│  [Share dossier ↗] [Export PDF] [Export MD] │
│  [Continue investigation] [Request refresh] │
│                                             │
└─────────────────────────────────────────────┘
```

#### Evidence Board

```
┌─────────────────────────────────────────────┐
│  EVIDENCE BOARD                             │
│                                             │
│  Filter: [All lanes ▾] [All sources ▾]     │
│          [Supports ▾]  [All freshness ▾]   │
│                                             │
│  ─── EVIDENCE ITEM #14 ───                  │
│  Source: Google Cloud Pricing Docs          │
│  Class: Primary (vendor documentation)      │
│  Retrieved: 2026-03-10T14:23:00Z           │
│  Freshness: Current                         │
│  Independence: PRIMARY SOURCE               │
│                                             │
│  "Compute Engine automatically gives you    │
│   a discount for every incremental hour...  │
│   up to a 30% net discount for instances    │
│   that run the entire month."               │
│                                             │
│  Used in: Claim #1 (supports)              │
│  [View full source] [View in context]       │
│                                             │
│  ─── EVIDENCE ITEM #22 ───                  │
│  Source: CloudOptimize Benchmark (2025)     │
│  Class: Third-party analysis                │
│  Retrieved: 2026-03-10T14:25:00Z           │
│  Freshness: Recent                          │
│  Independence: INDEPENDENT ✓                │
│                                             │
│  "In our testing, sustained-use discounts   │
│   applied automatically, resulting in a     │
│   22-28% reduction for always-on workloads."│
│                                             │
│  Used in: Claim #1 (supports)              │
│  [View full source] [View in context]       │
│                                             │
│  ─── [47 more items...] ───                 │
│                                             │
│  SOURCE INDEPENDENCE GRAPH                  │
│  [View which sources cite each other →]     │
│                                             │
└─────────────────────────────────────────────┘
```

### 10.3 What the user never sees

- Agent names or roles. The user does not know about "Planner," "Adversary," or "Analyst." They see investigation phases. The derived conclusions appear as "Evidence-Backed Deductions" — the user never sees the word "Analyst agent."
- Agent prompts or internal communications. The trace view shows what actions were taken, not the LLM conversations.
- Token counts or model names. These are internal performance metrics.
- The word "agent" anywhere in the UI. The vocabulary is: investigation, lane, evidence, source, claim, deduction, challenge, gap, dossier.

---

## 11. Output Design

### 11.1 The dossier structure

Every dossier, regardless of format, contains these sections in this order:

1. **Header:** Investigation title, objective, date, depth tier, evidence summary (count, source count, independent source count, deduction count).

2. **Key Findings:** 3-8 top-level claims, each with:
   - Clear statement
   - Support strength + challenge strength + confidence label
   - Number of supporting independent sources
   - Number of contradictions found
   - Link to drill into evidence

3. **Evidence-Backed Deductions:** Conclusions that the Analyst agent derived from cross-evidence reasoning. Each deduction includes:
   - Clear statement of the derived conclusion
   - Full derivation chain (which evidence items, combined with what reasoning, led to this)
   - Deduction type label (temporal pattern, cross-lane connection, absence-as-evidence, etc.)
   - Confidence assessment and falsification condition
   - Adversary review verdict (confirmed, weakened, or rejected)
   - **Clearly labeled as "DEDUCTION — not directly sourced"** so the user always knows they are reading a derived conclusion, not a fact

4. **Counter-Evidence:** All high-severity findings from the Adversary Agent, presented as challenges to specific claims AND to deductions. Each with its own evidence chain.

5. **What We Could Not Determine:** All gaps, categorized by type (no results, paywalled, unanswerable from public sources, time-sensitive).

6. **Detailed Findings:** Expanded discussion of each research lane, with inline evidence references. Every paragraph maps to at least one evidence item.

7. **Source List:** All sources used, with metadata: URL, publisher, date, source class, freshness, independence status.

8. **Evidence Appendix:** Full set of extracted text items, organized by claim.

9. **Investigation Trace:** Timeline of what was done: when each lane started and completed, when review happened, when the deduction phase ran, what gaps were found and addressed.

### 11.2 Output formats

**V1 (launch):**
- Interactive web dossier (the full experience, with drill-down and filtering)
- Markdown export (for use in other tools)
- PDF export (for sharing with non-technical stakeholders)

**V2 (after product-market fit):**
- Executive brief (1-page summary with confidence scores and top 3 findings)
- Evidence pack (structured JSON export of all evidence items and claims — for API consumers)
- Shareable public page (read-only web view with its own URL)

### 11.3 Language and tone constraints for the Writer Agent

The Writer's system prompt includes these rules:
- Never use "It is clear that..." unless support > 0.85 and challenge < 0.20.
- Never use "undoubtedly," "certainly," "obviously," or similar certainty signals.
- Always use hedging language proportional to confidence: "Evidence suggests..." (moderate), "Limited evidence indicates..." (weak), "Multiple independent sources confirm..." (strong).
- Every factual sentence must end with an evidence reference in brackets.
- The counter-evidence section must not be framed as a minor caveat. It must be presented with equal weight to the supporting evidence.
- If the honest answer is "the evidence is inconclusive," the dossier must say that. A non-answer is better than a false answer.

---

## 12. Technical Stack

### 12.1 Stack overview

| Layer | Technology | Why |
|-------|-----------|-----|
| **API framework** | FastAPI (Python) | Async-native, excellent typing, fast development. Ecosystem of AI/ML libraries in Python is unmatched. Easy for contributors to understand and extend. |
| **Database (default)** | SQLite + FTS5 | Zero-config, single-file database. Perfect for self-hosted single-user deployments. No separate database server needed. Ships with full-text search via FTS5. |
| **Database (scale)** | PostgreSQL 16+ | Optional upgrade for multi-user or high-volume deployments. JSONB for flexible fields, full-text search, rock-solid reliability. Switch by changing `DATABASE_URL` in `.env`. |
| **Orchestration** | Custom Python state machine, backed by database state + in-process async task queue | Simple, no external dependencies, sufficient for self-hosted deployments. Uses `asyncio` task groups for parallel researcher execution. |
| **Task queue (optional)** | Redis + arq (lightweight) or Celery | Only needed for heavy parallel workloads or multi-worker deployments. Not required for default single-machine setup. |
| **LLM provider abstraction** | LiteLLM | Unified interface for 100+ LLM providers. Handles retries, rate limiting, streaming, and cost tracking. Users configure one env var to switch providers. Supports: OpenAI, Anthropic, Google, Groq, Mistral, Together, Fireworks, Ollama, vLLM, LM Studio, any OpenAI-compatible endpoint. |
| **Web search** | Pluggable search adapter | Tavily (best quality, requires key), Serper (good, requires key), Brave Search (good, requires key), SearXNG (free, self-hosted), DuckDuckGo (free, no key, rate-limited). User picks in `.env`. |
| **Web fetching** | httpx + BeautifulSoup4 + readability-lxml | Fast, reliable HTML fetching and content extraction. Handles 90% of web pages. |
| **Browser automation** | Playwright (optional, off by default) | For JS-heavy pages that cannot be fetched with httpx. Enabled via `PLAYWRIGHT_ENABLED=true`. Runs in a separate Docker container. |
| **PDF extraction** | pdfplumber + PyMuPDF (fitz) | pdfplumber for text extraction, PyMuPDF for layout-aware extraction. Both handle most PDFs well. |
| **Screenshot capture** | Playwright (when enabled) | Evidence preservation. Screenshot the page as it appeared at retrieval time. |
| **Deduplication** | Content hashing (SHA-256 for exact) + RapidFuzz (for fuzzy text matching) | Prevent the same source appearing multiple times. Detect near-duplicate content across different URLs. |
| **Object storage** | Local filesystem (default) or S3/MinIO (optional) | Raw HTML, PDFs, screenshots, cached source content. Default stores in `./data/storage/`. Configure S3 via env vars for cloud deployments. |
| **Frontend** | Next.js + React (static export mode) | Statically exported for simple serving. React for interactive evidence board. No Node.js server needed in production — served as static files by FastAPI. |
| **Auth (optional)** | None (default) / Basic Auth / Reverse proxy auth / OIDC | Default: no auth (single-user local deployment). Enable basic auth via env var. For teams: integrate with any reverse proxy (Nginx, Traefik, Cloudflare Tunnel) or OIDC provider. |
| **Observability (optional)** | Built-in cost tracker + optional OpenTelemetry | Every investigation logs LLM calls, token counts, search calls, and estimated cost. Optional OpenTelemetry export for Prometheus/Grafana setups. |
| **CLI** | Python CLI (`dossier investigate "question"`) | Run investigations from the command line. Useful for scripting, automation, and when you do not need the web UI. |

### 12.2 Model compatibility matrix

| Provider | Model | Quality | Cost per Standard Investigation | Notes |
|----------|-------|---------|-------------------------------|-------|
| OpenAI | GPT-4o | Excellent | ~$3-$6 | Best overall price/performance |
| OpenAI | GPT-4o-mini | Good | ~$0.50-$1.50 | Great for quick scans |
| Anthropic | Claude Sonnet 4 | Excellent | ~$4-$8 | Best at following adversarial prompts |
| Anthropic | Claude Haiku | Good | ~$0.30-$1.00 | Fast, affordable for quick scans |
| Google | Gemini 2.0 Flash | Good | ~$1-$3 | Good balance, generous free tier |
| Google | Gemini 2.5 Pro | Excellent | ~$5-$12 | Top-tier quality |
| Groq | Llama 3.1 70B | Good | ~$0.50-$2 | Extremely fast inference |
| Mistral | Mistral Large | Good | ~$3-$7 | Strong European option |
| Ollama (local) | Llama 3.1 70B | Good | $0 (your hardware) | Fully offline, requires 40GB+ VRAM |
| Ollama (local) | Llama 3.1 8B | Usable | $0 (your hardware) | Lower quality but runs on consumer GPUs |
| Ollama (local) | Qwen 2.5 72B | Good | $0 (your hardware) | Strong alternative to Llama |

**Cost note:** These are the raw API costs the user pays directly to the LLM provider. Dossier adds zero markup. Users control costs via the `INVESTIGATION_BUDGET_CAP` setting.

### 12.3 What NOT to over-invest in for V1

- **Do not build a custom LLM.** Use existing providers via LiteLLM. Fine-tuning is a contributor-led V3+ experiment.
- **Do not build a knowledge graph database.** SQLite/PostgreSQL with foreign keys handles the evidence graph fine until you have 100K+ cases.
- **Do not build a custom search engine.** Tavily, Serper, and SearXNG are good enough. Build on top of them.
- **Do not build a custom NER/NLP pipeline.** Let the LLM extract entities and dates. Dedicated NLP is a V2 optimization.
- **Do not add Redis as a default dependency.** The default deployment should require only Docker. Async task queues in-process are sufficient for single-machine use.

---

## 13. Sustainability Model

### 13.1 Core principle: the full product is free, forever

Dossier is MIT-licensed open-source software. There is no "open core" bait-and-switch. Every feature — all agent types, all domain templates, all output formats, the full evidence engine — is available to anyone who runs it themselves. Users pay only for their own LLM and search API usage, directly to the providers.

### 13.2 Per-investigation cost to the user

Users pay LLM and search API providers directly. Dossier adds zero markup:

| Depth | LLM cost (varies by provider) | Search API cost | Your infrastructure | Total cost to you |
|-------|------------------------------|-----------------|--------------------|--------------------|
| Quick scan | $0.30-$1.50 | $0.05-$0.20 | ~$0 | **~$0.50-$2.00** |
| Standard | $1.50-$6.00 | $0.30-$1.00 | ~$0 | **~$2.00-$7.00** |
| Deep | $5.00-$20.00 | $1.00-$3.00 | ~$0 | **~$6.00-$23.00** |
| Fully local (Ollama + SearXNG) | $0 (your hardware) | $0 | Electricity | **~$0** |

**Key point:** A user doing 10 standard investigations per month pays ~$20-$70 directly to OpenAI/Anthropic/Google. Compare this to $49/month for a SaaS subscription that forces you to use their infrastructure and gives them your data. With Dossier, you get the same (or better) product for less money, with full data ownership.

### 13.3 Revenue streams (for sustaining development)

| Stream | Model | Expected revenue | Timeline |
|--------|-------|-----------------|----------|
| **GitHub Sponsors / Open Collective** | Individuals and companies sponsor ongoing development. Sponsors get a badge, early access to roadmap discussions, and voting on feature priority. | $500-$5,000/month | From launch |
| **Dossier Cloud (optional managed hosting)** | Hosted version for users who do not want to self-host. Same open-source code, we manage the infrastructure. User still brings their own API key but does not need Docker. | $9/month (personal) to $49/month (team) | 3-6 months post-launch |
| **Enterprise support contracts** | Priority support, SLA guarantees, custom deployment assistance, private template development, security audits. For companies running Dossier on their own infrastructure at scale. | $500-$5,000/month per contract | 6-12 months post-launch |
| **Domain template packs (community marketplace)** | Community-built, peer-reviewed investigation templates for specific industries (legal, medical, financial, compliance). Free to create and share. Optional paid premium templates from domain experts. | Revenue share with template authors | 12+ months post-launch |
| **Grants and fellowships** | Apply for open-source sustainability grants (NLnet, Sovereign Tech Fund, Mozilla, Ford Foundation) focused on open-source, information integrity, and public interest technology. | $25K-$200K per grant | From launch |

### 13.4 Why this model works

1. **Users save money vs. SaaS.** At scale, raw API costs are 30-70% cheaper than SaaS subscription pricing that includes cloud infrastructure, margin, and overhead. Users keep the savings.
2. **Trust through transparency.** Open-source means users can audit every prompt, every scoring algorithm, every data flow. For an investigation tool built on trust, this is a feature that no closed-source competitor can match.
3. **Community accelerates development.** Domain templates, search provider adapters, output format plugins, and frontend improvements all benefit from community contribution. One maintainer team cannot build templates for every industry; a community can.
4. **Managed hosting captures convenience buyers.** Many users would rather pay $9/month than manage Docker. Dossier Cloud serves them without compromising the open-source core.
5. **Enterprise pays for support, not features.** Large companies need SLAs, compliance documentation, and deployment assistance. They gladly pay for these services even when the software itself is free.

### 13.5 What this model does NOT do

- **No vendor lock-in.** If Dossier Cloud shuts down, users export their data and self-host. The code is the same.
- **No telemetry or data monetization.** User investigation data is never collected, aggregated, or sold. 
- **No "premium" features in the open-source version.** If a feature exists, it ships to everyone. Dossier Cloud may offer convenience features (automated backups, one-click updates, team management UI) but the investigation engine is identical.

---

## 14. Go-to-Market

### 14.1 Distribution strategy: GitHub-first, README-driven

Dossier is an open-source project. The distribution strategy is fundamentally different from SaaS:

**The GitHub repository IS the product page.** The README is the landing page. The star count is social proof. Issues and discussions are the community. Every design decision should make the README compellingly simple.

**The "5-minute hook":**
```
1. Clone → 2. Add API key → 3. docker compose up → 4. Ask a question → 5. Read a dossier
```
If this does not work in 5 minutes, the project fails. Nothing else matters until this works flawlessly.

### 14.2 Launch wedge: Company and vendor due diligence

**Why this wedge:**
- Structured enough to template (company name → standardized investigation)
- Evidence traceability is a requirement, not a nice-to-have (procurement decisions, investment decisions)
- Output is naturally shareable — "look what I found with this open-source tool"
- "Takes 30 minutes instead of 30 hours" is a compelling pitch
- The same user who uses it once will use it again (recurring use case)
- High overlap with the developer/open-source audience (founders, VCs, analysts who use GitHub)

**V1 launch template: Company Due Diligence**

When a user mentions a company name, the system activates the due diligence template:

Pre-configured research lanes:
1. Company overview (founding, leadership, funding, headcount, growth)
2. Financial health (revenue, margins, funding rounds, burn rate, profitability signals)
3. Legal and regulatory exposure (lawsuits, regulatory actions, compliance history)
4. Product and technology (product lines, tech stack, patents, competitive position)
5. Reputation (employee reviews, customer reviews, media coverage, social sentiment)
6. Risk factors (leadership changes, market risks, dependency risks, negative press)

Pre-configured source classes per lane:
- SEC filings, Crunchbase, LinkedIn, Glassdoor, G2, news archives, court records, patent databases, company website, social media

This template dramatically improves first-investigation quality because the Planner does not need to figure out what to look for from scratch.

### 14.3 Growth strategy

**Phase 1: Open-source launch (months 1-3)**
- Release on GitHub with MIT license, comprehensive README, and 5-minute quickstart.
- Launch on Hacker News, Reddit (r/selfhosted, r/artificial, r/LocalLLaMA), Product Hunt, and Twitter/X.
- Run 10-20 high-profile public investigations (trending startups, controversial companies) and publish the dossiers as proof-of-quality examples in the repo's `/examples` folder.
- Create a demo video (3 minutes): clone → API key → docker compose up → submit question → dossier appears.
- Write a detailed blog post: "Why we open-sourced our investigation engine" explaining the philosophy.

**Phase 2: Community building (months 2-6)**
- Establish a Discord or GitHub Discussions community for users and contributors.
- Create a `CONTRIBUTING.md` with clear contribution guidelines, coding standards, and a "good first issues" label.
- Accept community-contributed domain templates (market analysis, regulatory compliance, technology evaluation).
- Build a contributor recognition system (hall of fame in README, contributor badges).
- Regular releases (every 2-4 weeks) with changelogs that credit contributors.

**Phase 3: Ecosystem expansion (months 4-12)**
- Launch a template registry (community-built investigation templates, peer-reviewed, shareable).
- Build integrations with popular tools: Obsidian plugin (export dossiers to vault), Notion integration, Raycast extension, Alfred workflow.
- Create a plugin system for custom search providers, output formats, and evidence processors.
- Partner with privacy-focused and self-hosted communities (r/selfhosted, awesome-selfhosted, AlternativeTo listings).

**Phase 4: Managed cloud + enterprise (months 6-18)**
- Launch Dossier Cloud (optional hosted version for non-technical users who still bring their own API key).
- Announce enterprise support contracts for companies running Dossier in production.
- Create case studies from early enterprise adopters.
- Attend conferences (FOSDEM, All Things Open, PyCon) and give talks on adversarial evidence verification.

### 14.4 Distribution channels

| Channel | Tactic | Expected impact |
|---------|--------|----------------|
| GitHub | Excellent README, star growth, "good first issues," regular releases with changelogs. | Critical — the primary distribution channel. Target: 1K stars in month 1, 5K in 6 months. |
| Hacker News | Launch post: "Show HN: Open-source investigation engine — BYOK, self-hosted, adversarial evidence review." | High — single biggest day-one traffic source for developer tools. |
| Reddit | r/selfhosted, r/LocalLLaMA, r/artificial, r/opensource. Cross-post to relevant domain subreddits. | High — self-hosted audience is the exact target user. |
| Twitter/X | Build-in-public: share investigation output, architecture decisions, evidence visualizations. "What we couldn't find" screenshots are inherently shareable. | Medium-high — developers and researchers follow these conversations. |
| Product Hunt | Launch with a live example dossier and a "try it in 5 minutes" CTA. | Medium — one-time spike for wider audience. |
| SEO (blog) | Publish public dossier examples as blog posts. Each is a long-form, citation-rich page that ranks for "[Company name] analysis" queries. Host on the project's documentation site. | Medium — slow build but compounds over time. |
| YouTube/video | "Dossier in 5 minutes" demo, "Building an AI investigation engine" dev log series, livestream investigations. | Medium — video content has long shelf life for discovery. |
| Conference talks | "Adversarial AI: Building Investigation Tools You Can Trust" — submit to PyCon, FOSDEM, All Things Open, AI Engineer Summit. | Medium — credibility building, enterprise pipeline. |

---

## 15. Build Plan

### 15.1 V0 — Core engine proof (Weeks 1-4)

**Goal:** Prove that evidence-traced, adversarially-reviewed AI research is meaningfully better than ChatGPT Deep Research. Build it as a CLI tool first.

**Build:**
- Python package with CLI: `dossier investigate "Is Company X a good acquisition target?"`
- Planner: one LLM call that produces subquestions and research lanes (hardcoded to use the due diligence template).
- Researchers: 3-5 parallel async tasks, each running a search + fetch + extract loop.
- Adversary: one LLM call that receives all evidence and tries to find contradictions (using additional searches).
- Writer: one LLM call that produces a Markdown dossier from the evidence, with inline citations.
- Storage: SQLite for cases, claims, evidence. Local file system for raw content.
- LLM abstraction via LiteLLM from day one — test with at least 3 providers (OpenAI, Anthropic, Ollama).
- Search abstraction with at least 2 providers (Tavily + DuckDuckGo as free fallback).
- Configuration via `.env` file — one file, documented, with sensible defaults.

**Not built yet:**
- No web UI. CLI + Markdown output only.
- No Docker packaging.
- No evidence board.
- No challenge endpoint.
- No domain templates beyond company due diligence.

**Team:** 1 developer (solo founder OK).

**Success metric:** Run 30 investigations across 3 different LLM providers. Compare quality to ChatGPT Deep Research on the same questions. If at least 20/30 produce demonstrably better evidence tracing, and at least 10/30 surface meaningful counter-evidence that ChatGPT missed, proceed to V1.

**Cost estimate:** ~$300-$800 in LLM and search API costs for 30 test investigations. Infrastructure: zero (runs on your laptop).

### 15.2 V1 — Open-source launch (Weeks 5-12)

**Goal:** A self-hosted product that anyone can clone, configure, and run in 5 minutes. First public GitHub release.

**Build on top of V0:**
- Dockerized deployment: `docker compose up` starts everything.
- Web UI: Next.js frontend (static export) served by FastAPI.
  - Submit investigation page.
  - Investigation progress (real-time status updates).
  - Dossier viewer with all sections.
  - Evidence board (filterable, drillable).
- `.env.example` with every option documented and sensible defaults.
- SQLite as default database (zero config), PostgreSQL as optional upgrade.
- Local file storage by default, S3/MinIO optional.
- SearXNG Docker service as optional zero-cost search provider.
- Ollama profile for fully local/offline operation.
- PDF and Markdown export of dossiers.
- Source independence detection (basic: URL-based citation matching + timestamp analysis).
- Gap transparency section in every dossier.
- Human-in-the-loop checkpoint (optional plan review before evidence gathering).
- 3 depth tiers: quick scan (5 min), standard (20 min), deep (1-2 hr).
- Built-in cost tracker (logs token usage and estimated cost per investigation).
- Comprehensive README with: quickstart, configuration reference, model compatibility matrix, architecture overview.
- `CONTRIBUTING.md` with coding standards, PR process, and "good first issues."
- GitHub Actions CI: tests, linting, Docker build.

**Team:** 1-2 developers + community early adopters.

**Success metric:**
- 500+ GitHub stars within 4 weeks of launch.
- 50+ users running their own instance (tracked by opt-in anonymous launch ping, disabled by default).
- 10+ GitHub issues or feature requests from external users (shows real engagement).
- 3+ community PRs merged.
- Works across at least 5 LLM providers without code changes.

### 15.3 V2 — Community growth (Weeks 13-26)

**Goal:** An active open-source project with regular contributors and a growing ecosystem.

**Build on top of V1:**
- Challenge endpoint (user can dispute a specific claim → triggers targeted re-investigation).
- Full source independence graph (visual, interactive in the evidence board).
- Plugin system for search providers (community can add new providers without forking).
- Domain template registry (community-contributed investigation templates).
- 2-3 additional built-in domain templates (market analysis, competitive landscape, technology evaluation).
- Cross-case knowledge: if a company was investigated before, reference prior findings.
- REST API documentation (OpenAPI/Swagger) for programmatic access.
- Improved evidence extraction (better PDF parsing, table extraction, numeric extraction).
- Mobile-responsive dossier reading experience.
- Optional basic auth and reverse proxy auth integration.
- Helm chart for Kubernetes deployment.
- Investigation quality scoring (internal: measure evidence coverage, source diversity, gap count per investigation).
- Dossier Cloud beta (optional managed hosting for non-technical users, BYOK).

**Team:** 2-3 core maintainers + 10-20 community contributors.

**Success metric:**
- 5,000+ GitHub stars.
- 500+ active instances.
- 5+ community-contributed domain templates.
- 20+ unique contributors to the codebase.
- Dossier Cloud: 50+ beta users.

### 15.4 V3 — Ecosystem maturity (Months 7-18)

**Build on top of V2:**
- Enterprise features contributed upstream: SSO integration (OIDC/SAML), audit logs, team workspace with role-based access.
- Living dossiers (auto-refresh when sources update — monitor key sources for changes).
- Multi-language investigation support (search in multiple languages, translate evidence, dossier in user's language).
- Advanced source credibility scoring (community-trained from opt-in user feedback: "this source was actually wrong").
- Domain-specific evidence packs (pre-built source hierarchies maintained by domain expert community members).
- Output format plugins (Obsidian, Notion, Confluence, Slack integration).
- Embeddable investigation widget (iframe component for other apps).
- Desktop app (Electron wrapper for one-click local deployment without Docker).

**Team:** 3-5 core maintainers + 50+ community contributors.

**Success metric:**
- 15,000+ GitHub stars.
- 2,000+ active instances.
- 50+ community-contributed templates and plugins.
- 3+ enterprise support contracts.
- Dossier Cloud: 200+ paying users.
---

## 16. Team and Community Model

### 16.1 Core maintainer team (V0-V1)

| Role | Responsibility | Skills |
|------|---------------|--------|
| Lead maintainer / creator | Build the investigation engine, evidence graph, agent orchestration, API. Manage the open-source community. | Python, SQLite/PostgreSQL, async systems, LLM API integration, prompt engineering, open-source community management. |
| Product-focused co-maintainer (optional) | Design the UX, write the domain templates, write documentation, manage issues. | UX design, technical writing, user research. |

**One person can do this.** Many successful open-source projects start with a single maintainer. The advantage of open-source is that you do not need to hire — you need to attract contributors.

### 16.2 Community contribution model

| Contribution type | Who | Onboarding |
|--------------------|-----|-----------|
| Domain templates | Industry experts who code | Template spec + example template + "add a template" guide |
| Search provider adapters | Developers who use niche search APIs | Provider adapter interface + "add a search provider" guide |
| Output format plugins | Developers integrating Dossier into their tools | Output plugin interface + "add an output format" guide |
| Frontend improvements | Frontend developers (React/Next.js) | Standard React contribution workflow, Storybook components |
| Documentation | Technical writers, non-code contributors | Docs site + "improve docs" guide with clear contribution process |
| Bug reports + testing | All users | Issue templates, bug report form, "how to report a bug" guide |
| Translations | Multilingual community members | i18n framework + Crowdin or Weblate integration |

### 16.3 Scaling the team (V2-V3)

As sponsorships, Dossier Cloud revenue, and grants provide funding:

| Stage | Core team | Community |
|-------|-----------|-----------|
| V1 (launch) | 1-2 maintainers | 5-15 early contributors |
| V2 (growth) | 2-3 full-time maintainers (funded by grants + Dossier Cloud) | 20-50 contributors, 5-10 regular |
| V3 (maturity) | 3-5 full-time maintainers (funded by enterprise contracts + Dossier Cloud) | 50-200 contributors, 10-20 regular |

### 16.4 What NOT to do early

- **Do not hire before the community exists.** Let the project attract its first contributors organically. Hire from the contributor pool.
- **Do not set up a complex governance structure.** Benevolent dictator model works for V1-V2. Formalize governance only when there are 5+ regular contributors who want input on direction.
- **Do not create a foundation prematurely.** Foundation overhead is justified at 50+ contributors and significant funding. Until then, it is a project under a GitHub org.

---

## 17. Risks and Mitigations

### 17.1 Existential risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| OpenAI/Google ships "Deep Research v2" with evidence tracing and persistence | High (12-18 months) | Medium — covers some of the value prop, but is closed-source and cloud-only | Dossier's advantages become more visible: self-hosted, audit every prompt, no data leaves your machine, no subscription, works with any provider including local models. The open-source community can iterate faster on domain templates than a closed platform. |
| Investigation quality is inconsistent (great for some topics, terrible for others) | High (inherent in web-dependent research) | High — users lose trust after one bad experience | Launch narrow (company due diligence only). Pre-built source hierarchies reduce variance. Quality scoring on every investigation flags issues before the user sees them. Community templates encode domain expertise. |
| LLM providers change their APIs or pricing dramatically | Medium | Medium — breaks provider integration temporarily | LiteLLM abstracts providers and is actively maintained by a large community. Multiple provider support means no single provider is a dependency. Local models via Ollama provide a fallback that requires zero external APIs. |
| Web scraping fails on critical sources (paywalls, blocks, CAPTCHAs) | High | Medium — gaps in evidence, not total failure | Log gaps visibly (Gap Transparency). Do not pretend inaccessible sources don't exist. Community can contribute source-specific adapters. Long-term: integrate with data provider APIs (SEC EDGAR, Crunchbase, news APIs). |
| Project fails to attract contributors and community | Medium | High — solo maintainer burnout | Focus on developer experience: excellent documentation, "good first issues," fast PR review, clear architecture. Make contributing easy. Do not over-engineer governance. Build in public. |

### 17.2 Product risks

| Risk | Mitigation |
|------|-----------|
| Users don't care about evidence traceability (they just want the answer) | Test this in V0. If users never click on evidence links, the thesis is wrong. Pivot to a faster, shallower product. |
| "Hours-long research" scares away mainstream users | Offer quick scan (5 min) as the entry experience. Prove value fast. Deep investigations are for power users. |
| Agent complexity increases cost and latency without improving output quality | Start with 5 agent types (Planner, Researcher, Adversary, Analyst, Writer). Add complexity only when measurable quality improvement is demonstrated. Never add agents for architectural elegance — only for output quality. The Analyst agent is the exception: it exists because cross-evidence deduction is the core differentiator, not a nice-to-have. |
| The dossier is too long and verbose | Test output length with users. Some want the full dossier. Others want the 1-page executive brief. Offer both. But default to concise. |
| Investigation quality varies by domain (good for tech companies, bad for healthcare or legal) | Launch with ONE domain. Do not expand to a new domain until the current one is excellent. Each domain needs its own template and source hierarchy. Community-contributed templates accelerate domain expansion. |
| Setup is too hard for non-technical users | Docker Compose makes it one command, but Docker itself is a barrier. Address with: (1) excellent setup guide with screenshots, (2) one-click deploy buttons for Railway/Render, (3) Dossier Cloud for users who do not want to self-host. |

### 17.3 Technical risks

| Risk | Mitigation |
|------|-----------|
| Source independence detection is too hard to implement accurately | Start simple: URL-based citation matching + publication timestamp analysis. This catches the most obvious cases (articles citing the same press release). Improve iteratively. Do not claim perfect independence detection — show the graph and let users judge. |
| Contradiction detection produces false positives (different time periods or contexts flagged as contradictions) | The Adversary should include temporal and contextual information in its review notes. The Writer should present contradictions with their context, not as bare disagreements. Better prompting reduces (but does not eliminate) false positives. |
| PDF extraction quality is unreliable | Log extraction quality per source. When extraction quality is low, mark the evidence item as "low confidence extraction" in the UI. Do not hide extraction failures. |
| Different LLM providers produce inconsistent quality | Maintain a model compatibility matrix with quality ratings. Set minimum model recommendations per agent type (e.g., "Adversary requires GPT-4o class or better"). Allow users to assign different models to different agent roles. |
| SQLite has concurrency limitations for multi-user deployments | SQLite is the default for simplicity. Document when to switch to PostgreSQL (multiple concurrent users, team deployments). Make the migration a one-command operation. |

### 17.4 Open-source risks

| Risk | Mitigation |
|------|-----------|
| Someone forks and commercializes it without contributing back | MIT license allows this. This is a feature, not a bug. The original project retains community trust, momentum, and expertise. Forks that do not contribute back rarely succeed long-term. |
| Corporate contributions come with strings attached | Clear contribution guidelines: all PRs are reviewed by maintainers. Corporate sponsors do not get commit access or roadmap control. Feature requests from sponsors are weighed equally with community requests. |
| Maintainer burnout | Build a contributor pipeline. Identify and empower co-maintainers early. Set clear boundaries for response times and scope. Accept that not every feature request can be built. |
| Security vulnerabilities in prompts or agent behavior | Establish a security policy (SECURITY.md). Prompt injection defenses in all agent inputs. Community security audits. Responsible disclosure process. |

### 17.5 Assumptions that must be tested

These are the beliefs underlying this plan. If any of them is wrong, the plan needs to change:

1. **Users value evidence traceability.** Test: do users click on source links? Do they read the evidence board?
2. **Adversarial review improves perceived quality.** Test: do users rate dossiers with counter-evidence sections higher than dossiers without?
3. **Gap transparency builds trust.** Test: do users who see the "what we could not determine" section report higher trust scores?
4. **Cross-evidence deduction produces genuinely valuable conclusions.** Test: show users a dossier's "Evidence-Backed Deductions" section and ask — "Did you already know this, or is this new to you?" If >50% of deductions are genuinely new to the user (things they could not have found by searching), the deduction thesis is validated. This is the most critical assumption in the entire plan.
5. **Users value deductions AND trust them.** Test: do users rate dossiers with the deductions section higher than dossiers without? Do they cite deductions in their decisions? Or do they ignore/dismiss them because they are not directly sourced?
6. **Users will wait 20-50 minutes for a standard investigation.** Test: what is the abandonment rate at 5 min, 15 min, 30 min?
7. **Company due diligence is the right initial wedge.** Test: which investigation types have the highest completion rate and highest user satisfaction?
8. **Self-hosted BYOK is a meaningful differentiator.** Test: do users choose Dossier over SaaS alternatives specifically because of data ownership and provider choice?
9. **The developer/technical audience will adopt a docker-compose-based tool.** Test: what percentage of GitHub visitors successfully run the tool? Where do they get stuck?
10. **Community-contributed domain templates will reach quality parity with maintainer-built templates.** Test: compare investigation quality scores between built-in and community templates.

---

## 18. Success Metrics

### 18.1 North Star metric

**Number of investigations completed where Dossier derived evidence-backed deductions the user could not have found through conventional search — and the user trusted the output enough to act on it.**

For an open-source project, this is measured through: (1) opt-in feedback in the UI ("Was this dossier useful?" and "Did the deductions reveal something new?"), (2) GitHub discussions where users share how they used Dossier, and (3) qualitative community feedback.

### 18.2 Tracking metrics by stage

#### V0 stage (validation)

| Metric | Target |
|--------|--------|
| Investigations run (internal testing) | 30+ |
| Dossiers rated better than ChatGPT Deep Research (side-by-side) | >66% |
| Dossiers with meaningful counter-evidence found | >33% |
| Average evidence items per investigation | >15 |
| Average independent sources per investigation | >8 |
| Works across 3+ LLM providers without code changes | Yes |

#### V1 stage (open-source launch)

| Metric | Target |
|--------|--------|
| GitHub stars | 500+ within 4 weeks, 2,000+ within 3 months |
| Unique clones / Docker pulls | 200+ within 4 weeks |
| GitHub issues from external users | 10+ within 4 weeks (shows real engagement) |
| Community PRs merged | 3+ within 8 weeks |
| Investigation completion rate | >85% (started → finished) |
| Evidence link click-through rate | >20% of users click at least one source |
| Works across 5+ LLM providers | Yes |
| Successful 5-minute setup rate | >80% of users who attempt setup |

#### V2 stage (community growth)

| Metric | Target |
|--------|--------|
| GitHub stars | 5,000+ |
| Active instances (opt-in telemetry) | 500+ |
| Unique contributors to codebase | 20+ |
| Community-contributed domain templates | 5+ |
| Dossier Cloud beta users | 50+ |
| Investigation quality score (internal) | >0.75 average |

#### V3 stage (ecosystem maturity)

| Metric | Target |
|--------|--------|
| GitHub stars | 15,000+ |
| Active instances | 2,000+ |
| Unique contributors | 100+ |
| Community templates and plugins | 50+ |
| Enterprise support contracts | 3+ |
| Dossier Cloud paying users | 200+ |
| Monthly revenue (Cloud + Enterprise + Sponsors) | >$15K |

---

## 19. Long-Term Vision

### 19.1 The 3-year destination

Dossier becomes the open-source standard for evidence-grade research — the first tool that doesn't just find information, but **derives evidence-backed deductions, shows exactly how it derived them, and lets you challenge them**.

When someone says "I Googled it," they mean they found information. When someone says "I ran a Dossier on it," they mean they *investigated* it — the tool gathered evidence, challenged it, and then derived conclusions that no single source contained, with the full reasoning chain visible. The difference is not just trust. It is deduction. And they did it on their own machine, with their own API key, with zero data shared with any third party.

The long-term product is:
- **For individuals:** A self-hosted investigation engine that gives anyone access to investigation-grade research — not just evidence gathering, but cross-evidence reasoning that derives deductions, shows how they were derived, and lets you challenge them. Pay only for the API calls you make, not a SaaS subscription.
- **For developers:** An extensible open-source framework with a plugin system for custom search providers, domain templates, output formats, deduction strategies, and LLM configurations. Build your own investigation workflows on top of Dossier.
- **For teams:** A shared, self-hosted research workspace where investigations are reusable, updatable, and defensible. The Analyst agent's deduction capabilities improve with richer evidence graphs built over time.
- **For organizations:** An embedded investigation layer (via API) that integrates into decision workflows (procurement, investment, compliance, hiring). Deploy behind your firewall. Audit every prompt and every derivation chain.
- **For the open-source community:** A reference implementation of adversarial, evidence-traced, deduction-capable AI research that raises the standard for what AI research tools should do.

### 19.2 The moat at maturity

Open-source moats work differently from SaaS moats. The real competitive advantages are:

1. **Community-built domain expertise.** After hundreds of contributors build templates for finance, healthcare, legal, technology, and dozens of other domains, Dossier becomes the most comprehensive investigation framework available. No single company can match the combined domain expertise of an active community.

2. **Ecosystem lock-in (the good kind).** When teams build custom templates, integrate Dossier into their CI/CD pipelines, write output plugins for their internal tools, and accumulate investigation history — switching costs are high. Not because of vendor lock-in, but because of genuine integration depth.

3. **Trust through transparency.** For an investigation tool, being able to audit every line of code, every prompt, every scoring algorithm is a feature that no closed-source competitor can match. Enterprises in regulated industries (finance, healthcare, government) will choose auditable open-source over opaque SaaS.

4. **Brand recognition.** If "Dossier-verified" becomes a recognized marker of research quality — the way "Michelin-starred" signals restaurant quality — the brand itself is a moat. This requires consistent quality over time and high-profile public dossiers that prove the system's value.

5. **Contributor talent pipeline.** Active contributors to Dossier become the experts in adversarial AI research methodology. This expertise cannot be hired away — it grows within the community.

### 19.3 The open-source ecosystem vision

```
┌─────────────────────────────────────────────────────┐
│                    DOSSIER ECOSYSTEM                 │
│                                                     │
│  Core Engine (MIT)                                  │
│  ├─ Investigation orchestrator                     │
│  ├─ 5 agent types (Planner, Researcher, Adversary, │
│  │  Analyst, Writer)                               │
│  ├─ Evidence graph + deduction engine + scoring    │
│  ├─ Web UI + CLI + API                             │
│  └─ Provider abstraction (LLM, search, storage)    │
│                                                     │
│  Community Templates (MIT)                          │
│  ├─ Company due diligence                          │
│  ├─ Market analysis                                │
│  ├─ Technology evaluation                          │
│  ├─ Regulatory compliance                          │
│  ├─ Medical evidence review                        │
│  ├─ Academic literature review                     │
│  └─ 50+ domain-specific templates                  │
│                                                     │
│  Plugins & Integrations (MIT)                       │
│  ├─ Search: Tavily, Serper, SearXNG, Brave, custom │
│  ├─ Output: Obsidian, Notion, Confluence, Slack    │
│  ├─ Storage: S3, MinIO, R2, local                  │
│  ├─ Auth: OIDC, SAML, LDAP                        │
│  └─ Embeds: iframe widget, API client libraries    │
│                                                     │
│  Dossier Cloud (optional managed hosting)           │
│  └─ Same code, hosted for convenience, BYOK        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 19.4 What Dossier does NOT become

- **Not a general-purpose AI assistant.** It does not answer casual questions, write emails, or generate code. It investigates.
- **Not a surveillance tool.** Investigations are based on public sources. It does not hack, phish, or access private data.
- **Not a replacement for human judgment.** It provides evidence and analysis. The human makes the decision. The dossier is input, not output.
- **Not a news aggregator or content feed.** Each investigation is commissioned by a user for a specific purpose. There is no "browse" or "discover" mode.
- **Not a SaaS-first product.** Self-hosted is always the primary distribution. Dossier Cloud exists for convenience, never as a requirement.
- **Not a VC-backed growth machine.** The sustainability model is designed for long-term independence: community sponsorship, managed hosting revenue, and enterprise support contracts — not venture capital and growth-at-all-costs.

### 19.5 The future that makes this matter

In 3-5 years, most information people encounter will be AI-generated. Blog posts, product reviews, news summaries, social media content — the percentage that is AI-written will increase every year. In this environment, **the ability to trace a claim back to a primary, verified, independent source — and to derive what the available evidence implies but nobody has yet stated — becomes the most valuable capability in the information economy.**

Dossier is not just a research tool. It is an open-source deduction engine for the information age. It derives evidence-backed deductions, shows exactly how it derived them, and lets you challenge them. It is infrastructure for a world where "where did this claim come from?" and "what does the evidence actually imply?" are the most important questions anyone can ask. And because it is open-source, the methodology is public, auditable, and improvable by anyone.

---

## Appendix A: Naming Alternatives

The working name "Dossier" is strong but carries intelligence/espionage connotations. Alternatives to evaluate:

| Name | Signal | Concern |
|------|--------|---------|
| **Dossier** | Thoroughness, depth, seriousness | May sound too "spy" for mainstream |
| **Verdict** | Conclusion, decision-readiness | May sound too legal |
| **Inquire** | Investigation, curiosity | Too soft for high-stakes positioning |
| **Veriduct** | Verification + conduct, reliability | Novel, may need brand-building |
| **Clearance** | Clarity, authorization, trust | Works well for due diligence wedge |
| **Deep Case** | Depth + case-file metaphor | Descriptive but not distinctive |
| **Proven** | Trust, verified | Simple, strong, but may be taken |

Evaluate against criteria: (1) Is it memorable? (2) Does it signal the output, not the system? (3) Can you use it as a verb? ("I ran a Dossier" / "I got a Verdict" / "I Cleared it") (4) Is the GitHub org name available? (5) For open-source, does the name suggest a tool you own and run, not a service you subscribe to?

---

## Appendix B: What This Plan Intentionally Omits

This plan does not include:

1. **A generic multi-agent framework.** Dossier is not a platform for building arbitrary agent systems. It is a specific product with a specific investigation workflow.
2. **Named agent personalities.** Agents are worker types, not characters. No "Chief Scientist," no "Librarian," no "Governing Board." The intelligence is in the evidence graph constraints and the investigation lifecycle, not in role-play prompts.
3. **A watch/monitoring system in V1-V2.** Living dossiers that auto-refresh on source changes are a compelling feature but an infrastructure nightmare. Deferred to V3 when the community and contribution volume can support it.
4. **Multiple output formats in V1.** One format: the interactive web dossier with Markdown export. PDF comes in V1. Everything else is V2+.
5. **A mobile app.** The web app should be responsive. A dedicated mobile app is premature until there is clear mobile-specific demand.
6. **A SaaS-first business model.** Dossier is open-source first. Dossier Cloud (managed hosting) exists for convenience but is not the primary product and does not gate any features.
7. **Complex governance from day one.** Benevolent dictator for life (BDFL) model until there are 5+ regular contributors requesting a governance upgrade.
8. **Paid features or "open core" bait-and-switch.** Every feature ships to the open-source version. Dossier Cloud charges for hosting convenience, not for features.

---

## Appendix C: Decision Log

Key decisions made in this plan and the reasoning behind them:

| Decision | Alternatives considered | Why this choice |
|----------|----------------------|-----------------|
| Open-source, MIT licensed | Proprietary SaaS, AGPL, BSL (Business Source License) | MIT maximizes adoption and trust. AGPL scares enterprises. BSL is "open source theater." A research tool built on trust should be genuinely open. Revenue comes from managed hosting, support, and sponsorships — not from restricting the software. |
| BYOK (Bring Your Own Key), not managed API | Managed API where users pay us, who pay providers | BYOK eliminates margin pressure, removes the middleman cost, and gives users full control. Users pay providers directly at their own rates. Dossier adds zero markup. This is more honest and cheaper for the user. |
| SQLite default, PostgreSQL optional | PostgreSQL required | SQLite is zero-config and eliminates a Docker container dependency. Single-user self-hosted deployments do not need PostgreSQL. Offer PostgreSQL as an upgrade path for teams and high-volume users. |
| Local filesystem default, S3 optional | S3 required for raw content storage | Most self-hosted users do not have S3. Local disk is simpler and good enough until storage exceeds hundreds of GB. S3/MinIO is a config switch for users who need it. |
| No auth by default | Auth required (Clerk, Auth0) | Single-user self-hosted deployments do not need auth. Adding mandatory auth increases setup complexity for the 80% of users who run Dossier on localhost. Optional auth (env var) for multi-user or exposed deployments. |
| In-process async tasks, not Redis+Celery by default | Redis + Celery required for parallel researchers | Redis adds a Docker dependency. Python asyncio task groups handle parallel researcher execution fine for single-machine deployments. Redis+Celery is an optional profile for heavy workloads. |
| 5 agent types (adding Analyst), not 4 | Original plan had 4 (Planner, Researcher, Adversary, Writer) with no cross-evidence reasoning | The core vision is deduction, not aggregation. Without the Analyst, Dossier is just a better Perplexity. With the Analyst, it derives evidence-backed deductions. The Analyst reasons across the full evidence graph to derive conclusions that no single source contains — the feature that makes Dossier fundamentally different from every existing tool. One additional LLM call per investigation is a small cost for the defining capability. |
| Evidence board as primary interface, not dossier | Dossier-first (original blueprint) | The dossier is the deliverable. The evidence board is the product. Users who can explore, filter, and drill into evidence develop trust. Users who only read a polished report cannot verify anything. |
| Deductions labeled separately from sourced claims | Blend insights into findings without distinction | Trust requires transparency. A deduction presented as a sourced fact is indistinguishable from a hallucination. Mandatory labeling ("DEDUCTION — not directly sourced") with visible derivation chains means the user always knows what is a fact and what is a derived conclusion. They can inspect, challenge, or dismiss any deduction. |
| Company due diligence as the only V1 use case | Supporting all research types from day one (original blueprint) | Quality > breadth. One excellent template with pre-built source hierarchies produces dramatically better results than a generic system that figures everything out from scratch. Community-contributed templates expand domains in V2+. |
| Two-axis confidence (support + challenge) not single score | Single 0-1 confidence score (original blueprint) | A single number hides critical information. A claim with 0.70 support and 0.05 challenge is very different from 0.70 support and 0.60 challenge, but both would get the same single score. Two axes communicate this. |
| Human-in-the-loop plan review (optional) | Fully autonomous investigation | Prevents wasting API budget on a poorly scoped investigation. Builds user trust by giving them control. Optional means power users can skip it. |
| Custom state machine, not Temporal | Temporal from day one (original blueprint) | Temporal adds a heavy dependency (~500MB+ Docker image) that is inappropriate for self-hosted single-machine deployments. A Python state machine is simpler, has no dependencies, and sufficient for the investigation lifecycle. |
| GitHub-first distribution, not App Store / marketplace | Product Hunt first, marketplace listings | Dossier's target user (technical, privacy-conscious, values self-hosting) lives on GitHub. The README is the landing page. Stars are social proof. Issues are the community. |
| CLI-first development (V0), web UI second (V1) | Web UI from day one | CLI validates the core thesis (does the investigation engine produce good dossiers?) without the overhead of frontend development. Ship the engine first, the UI second. |

---

*This document is a living plan. It should be updated as assumptions are validated or invalidated through building and community feedback. The most important thing is to start building V0 and testing whether the deduction capability — deriving evidence-backed conclusions from cross-evidence reasoning — actually surfaces conclusions that users could not have found on their own. If it does, Dossier is a category-defining tool. If it does not, the plan needs fundamental revision before further investment.*

---

**End of plan.**
