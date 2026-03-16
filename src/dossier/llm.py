from __future__ import annotations

import json
import logging
import re
from typing import Any, Protocol

from litellm import completion
from pydantic import BaseModel, Field

from dossier.config import Settings
from dossier.contracts import (
    CounterfactualTest,
    EvidencePacket,
    InsightClass,
    InvestigationPlan,
    Mechanism,
    NoveltyScore,
    Prediction,
    ProofTree,
    RankedInsight,
    SynthesisResult,
)

logger = logging.getLogger(__name__)


def _normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def _extract_json_payload(content: Any) -> Any:
    if isinstance(content, list):
        text = "".join(
            str(item.get("text", ""))
            for item in content
            if isinstance(item, dict)
        )
    elif isinstance(content, str):
        text = content
    else:
        msg = f"Unsupported response content type: {type(content)!r}"
        raise ValueError(msg)

    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        msg = "Response did not contain a JSON object."
        raise ValueError(msg)
    return json.loads(text[start : end + 1])


class PlannerLane(BaseModel):
    name: str
    query: str
    goal: str
    budget: int = Field(ge=1, le=20)


class PlannerResult(BaseModel):
    objective: str
    novelty_target: str
    strategy: str
    lanes: list[PlannerLane]


class LlmClient(Protocol):
    def plan(
        self,
        question: str,
        min_lanes: int,
        max_lanes: int,
        search_limit: int,
        case_memory_notes: list[str] | None = None,
    ) -> PlannerResult:
        ...

    def synthesize(
        self,
        question: str,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        mode: str = "deep",
        model_override: str | None = None,
    ) -> SynthesisResult:
        ...


class DemoLlmClient:
    def plan(
        self,
        question: str,
        min_lanes: int,
        max_lanes: int,
        search_limit: int,
        case_memory_notes: list[str] | None = None,
    ) -> PlannerResult:
        del case_memory_notes
        normalized_question = _normalize_whitespace(question)
        lowered = normalized_question.lower()

        lanes: list[PlannerLane] = [
            PlannerLane(
                name="Direct Evidence",
                query=normalized_question,
                goal="Collect direct signals and high-confidence facts.",
                budget=max(1, min(20, search_limit + 1)),
            ),
            PlannerLane(
                name="Contradictions And Risks",
                query=f"{normalized_question} risks contradictions counterarguments",
                goal="Find disconfirming evidence, caveats, and downside scenarios.",
                budget=max(1, min(20, search_limit)),
            ),
        ]

        if any(token in lowered for token in ("why", "cause", "mechanism", "driver", "how")):
            lanes.append(
                PlannerLane(
                    name="Mechanism And Drivers",
                    query=f"{normalized_question} mechanism drivers historical pattern",
                    goal="Identify plausible mechanisms and causal drivers behind observed signals.",
                    budget=max(1, min(20, search_limit)),
                )
            )

        if any(token in lowered for token in ("forecast", "predict", "next", "12 months", "quarter")):
            lanes.append(
                PlannerLane(
                    name="Forward Indicators",
                    query=f"{normalized_question} leading indicators early warning signals",
                    goal="Look for signals that support or disconfirm short-term predictions.",
                    budget=max(1, min(20, search_limit)),
                )
            )

        lane_cap = max(min_lanes, min(max_lanes, len(lanes)))
        selected_lanes = lanes[:lane_cap]
        while len(selected_lanes) < min_lanes:
            ordinal = len(selected_lanes) + 1
            selected_lanes.append(
                PlannerLane(
                    name=f"Supplemental Lane {ordinal}",
                    query=f"{normalized_question} independent validation signal {ordinal}",
                    goal="Backfill missing evidence diversity with independent supporting or disconfirming sources.",
                    budget=max(1, min(20, search_limit)),
                )
            )

        return PlannerResult(
            objective=f"Investigate: {normalized_question}",
            novelty_target="Produce top invention-grade insights with explicit assumptions and disconfirming signals.",
            strategy=(
                "ReWOO-lite lane decomposition: start from direct evidence, then pressure-test with contradictions "
                "and mechanism-focused retrieval before synthesis."
            ),
            lanes=selected_lanes,
        )

    def synthesize(
        self,
        question: str,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        mode: str = "deep",
        model_override: str | None = None,
    ) -> SynthesisResult:
        del mode, model_override
        packet_summaries = packets[:4]
        source_ids = [packet.source_atom.id for packet in packet_summaries]
        summary_text = "; ".join(packet.summary for packet in packet_summaries) or "limited evidence"
        primary_phrase = question.rstrip("?")

        insights = [
            RankedInsight(
                insight_class=InsightClass.NOVEL_DEDUCTION,
                title="Cross-lane signal alignment",
                summary=(
                    f"Current evidence suggests the decision around '{primary_phrase}' depends on whether "
                    f"supporting signals and counterevidence remain balanced across lanes. "
                    f"Observed packets point to {summary_text}."
                ),
                source_atoms=source_ids[:2] or source_ids,
                assumptions=[
                    "The retrieved sources are directionally representative.",
                    "The strongest signals are not artifacts of duplicated reporting.",
                ],
                mechanism=Mechanism(
                    name="Alignment mechanism",
                    description="Decision quality improves when direct evidence and contradiction scans converge.",
                    steps=[
                        "Collect direct evidence in one lane.",
                        "Collect contradictions in the second lane.",
                        "Compare overlap, gaps, and pressure points before ranking a conclusion.",
                    ],
                ),
                proof_tree=ProofTree(
                    conclusion="Early confidence should stay provisional until both lanes agree on the dominant signal.",
                    premises=[
                        "The plan intentionally separates support from contradiction search.",
                        "Evidence packets already show multiple themes rather than one isolated signal.",
                    ],
                    reasoning_notes=[
                        "This is a thin-path deduction, not a high-confidence final recommendation.",
                    ],
                ),
                predicted_observables=[
                    Prediction(
                        observable="Source diversity",
                        expected_signal="At least two independent evidence atoms reinforce the same conclusion.",
                        time_horizon="current run",
                        confidence=0.64,
                    )
                ],
                disconfirming_signals=[
                    "New contradictory evidence outweighs the current supporting lane.",
                    "Most evidence resolves to one repeated origin cluster.",
                ],
                counterfactual_tests=[
                    CounterfactualTest(
                        assumption="Current evidence balance is meaningful.",
                        challenge_prompt="What if the contradiction lane has better source quality than the support lane?",
                        expected_failure_mode="The provisional deduction flips and the current top insight collapses.",
                    )
                ],
                score=NoveltyScore(
                    novelty_distance=0.63,
                    synthesis_depth=0.61,
                    mechanism_quality=0.67,
                    predictive_power=0.58,
                    cross_domain_transfer=0.42,
                    token_efficiency=0.85,
                    coherence_penalty=0.08,
                ),
            ),
            RankedInsight(
                insight_class=InsightClass.SPECULATIVE_MECHANISM,
                title="Failure-pressure mechanism",
                summary=(
                    "A plausible mechanism is that hidden execution risk sits between the obvious narrative "
                    "and the strongest contradiction signal. That makes missing evidence more important than the "
                    "raw count of sources."
                ),
                source_atoms=source_ids[1:3] or source_ids,
                assumptions=[
                    "Weak signals are not random noise.",
                    "Operational risk can surface before public consensus forms.",
                ],
                mechanism=Mechanism(
                    name="Pressure accumulation",
                    description="Weak contradictory signals accumulate until they change the decision boundary.",
                    steps=[
                        "Capture weak counter-signals.",
                        "Test whether they cluster around the same operational theme.",
                        "Promote them only if they survive disconfirmation checks.",
                    ],
                ),
                proof_tree=ProofTree(
                    conclusion="The strongest novelty may come from unexplained gaps rather than explicit claims.",
                    premises=[
                        "Contradiction lanes exist to surface non-obvious failure modes.",
                        "Sparse evidence can still be meaningful when it converges on the same mechanism.",
                    ],
                    reasoning_notes=["This mechanism should be challenged with additional retrieval before promotion."],
                ),
                predicted_observables=[
                    Prediction(
                        observable="Repeated weak-signal alignment",
                        expected_signal="Two or more contradictory packets point at the same failure mode.",
                        time_horizon="next investigation pass",
                        confidence=0.57,
                    )
                ],
                disconfirming_signals=[
                    "Contradiction packets remain isolated and unrelated.",
                    "New high-quality evidence explains away the current weak signals.",
                ],
                counterfactual_tests=[
                    CounterfactualTest(
                        assumption="Weak-signal convergence matters here.",
                        challenge_prompt="Assume the weak signals are sampling noise. What remains?",
                        expected_failure_mode="The mechanism loses explanatory value and should be discarded.",
                    )
                ],
                score=NoveltyScore(
                    novelty_distance=0.71,
                    synthesis_depth=0.68,
                    mechanism_quality=0.72,
                    predictive_power=0.62,
                    cross_domain_transfer=0.51,
                    token_efficiency=0.80,
                    coherence_penalty=0.09,
                ),
            ),
            RankedInsight(
                insight_class=InsightClass.EXPLORATORY_PREDICTION,
                title="Next-observable prediction",
                summary=(
                    "If the current hypothesis is valid, the next useful observable will be a concrete signal that "
                    "either narrows the main uncertainty or shows the contradiction lane is overstated."
                ),
                source_atoms=source_ids[-2:] or source_ids,
                assumptions=[
                    "The next retrieval pass can access more discriminating evidence than the current one.",
                ],
                mechanism=Mechanism(
                    name="Observable narrowing",
                    description="Predictions convert a speculative synthesis into a falsifiable next step.",
                    steps=[
                        "State the most decision-relevant uncertainty.",
                        "Predict a concrete observable tied to that uncertainty.",
                        "Treat the result as a gate for the next iteration.",
                    ],
                ),
                proof_tree=ProofTree(
                    conclusion="Prediction utility is the fastest way to improve the next run.",
                    premises=[
                        "Thin-path investigations need a disciplined next observable.",
                        "Disconfirming signals help bound speculative output.",
                    ],
                    reasoning_notes=["This prediction should drive the first benchmark prompt revisions."],
                ),
                predicted_observables=[
                    Prediction(
                        observable="Independent confirmation artifact",
                        expected_signal="A new source confirms or invalidates the main contradiction within one extra search pass.",
                        time_horizon="next iteration",
                        confidence=0.6,
                    )
                ],
                disconfirming_signals=[
                    "The next search pass adds no independent evidence.",
                    "The strongest packet cannot be tied to a falsifiable observable.",
                ],
                counterfactual_tests=[
                    CounterfactualTest(
                        assumption="There is a discriminating next observable available.",
                        challenge_prompt="What if every additional source only restates the current evidence?",
                        expected_failure_mode="The prediction has low utility and the case needs new lanes.",
                    )
                ],
                score=NoveltyScore(
                    novelty_distance=0.58,
                    synthesis_depth=0.55,
                    mechanism_quality=0.59,
                    predictive_power=0.76,
                    cross_domain_transfer=0.37,
                    token_efficiency=0.88,
                    coherence_penalty=0.07,
                ),
            ),
        ]

        return SynthesisResult(insights=insights, tokens_in=0, tokens_out=0, estimated_cost_usd=0.0)


class LiteLlmClient:
    def __init__(self, model: str, api_key: str | None, fallback: DemoLlmClient | None = None) -> None:
        self.model = model
        self.api_key = api_key
        self.fallback = fallback or DemoLlmClient()

    def _normalize_plan(
        self,
        plan: PlannerResult,
        question: str,
        min_lanes: int,
        max_lanes: int,
        search_limit: int,
    ) -> PlannerResult:
        lanes = plan.lanes[: max(1, max_lanes)]
        if len(lanes) < max(1, min_lanes):
            fallback_plan = self.fallback.plan(question, min_lanes, max_lanes, search_limit)
            missing = max(1, min_lanes) - len(lanes)
            lanes.extend(fallback_plan.lanes[:missing])

        budget_cap = max(1, min(20, search_limit * 2))
        normalized_lanes: list[PlannerLane] = []
        for lane in lanes:
            name = _normalize_whitespace(lane.name) or "Research Lane"
            query = _normalize_whitespace(lane.query) or _normalize_whitespace(question)
            goal = _normalize_whitespace(lane.goal) or "Collect evidence relevant to the objective."
            budget = max(1, min(budget_cap, lane.budget))
            normalized_lanes.append(PlannerLane(name=name, query=query, goal=goal, budget=budget))

        if not self._has_disconfirmation_lane(normalized_lanes):
            fallback_plan = self.fallback.plan(question, min_lanes, max_lanes, search_limit)
            for fb_lane in fallback_plan.lanes:
                if self._is_disconfirmation_lane(fb_lane):
                    if len(normalized_lanes) >= max(1, max_lanes):
                        normalized_lanes[-1] = fb_lane
                    else:
                        normalized_lanes.append(fb_lane)
                    break

        return PlannerResult(
            objective=_normalize_whitespace(plan.objective) or f"Investigate: {_normalize_whitespace(question)}",
            novelty_target=_normalize_whitespace(plan.novelty_target)
            or "Produce top invention-grade insights with explicit assumptions and disconfirming signals.",
            strategy=_normalize_whitespace(plan.strategy)
            or "Decompose the question into complementary evidence and contradiction lanes.",
            lanes=normalized_lanes,
        )

    _DISCONFIRMATION_KEYWORDS = (
        "contradict", "risk", "disconfirm", "counter", "challenge",
        "adversarial", "weakness", "failure", "downside", "caveat",
    )

    @classmethod
    def _is_disconfirmation_lane(cls, lane: PlannerLane) -> bool:
        text = f"{lane.name} {lane.goal}".lower()
        return any(kw in text for kw in cls._DISCONFIRMATION_KEYWORDS)

    @classmethod
    def _has_disconfirmation_lane(cls, lanes: list[PlannerLane]) -> bool:
        return any(cls._is_disconfirmation_lane(lane) for lane in lanes)

    def plan(
        self,
        question: str,
        min_lanes: int,
        max_lanes: int,
        search_limit: int,
        case_memory_notes: list[str] | None = None,
    ) -> PlannerResult:
        prompt = {
            "question": question,
            "case_memory_notes": case_memory_notes or [],
            "constraints": {
                "min_lanes": min_lanes,
                "max_lanes": max_lanes,
                "max_budget_per_lane": max(1, min(20, search_limit * 2)),
            },
            "instructions": (
                "Create a ReWOO-style investigation plan as JSON with keys: objective, novelty_target, strategy, lanes. "
                "Each lane must include name, query, goal, budget. Lanes should be complementary and include at least one "
                "disconfirmation-focused lane. Use case memory notes only when they are relevant to the question."
            ),
        }
        try:
            raw_response: Any = completion(
                model=self.model,
                api_key=self.api_key,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a structured investigation planner. Reply with JSON only.",
                    },
                    {"role": "user", "content": json.dumps(prompt)},
                ],
                temperature=0.2,
            )
            message_content = raw_response["choices"][0]["message"]["content"]
            parsed = _extract_json_payload(message_content)
            planned = PlannerResult.model_validate(parsed)
            return self._normalize_plan(planned, question, min_lanes, max_lanes, search_limit)
        except Exception:
            logger.exception("LiteLLM planning failed for model %r, falling back to demo", self.model)
            return self.fallback.plan(question, min_lanes, max_lanes, search_limit)

    def synthesize(
        self,
        question: str,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        mode: str = "deep",
        model_override: str | None = None,
    ) -> SynthesisResult:
        evidence_lines = [
            {
                "source_atom": packet.source_atom.id,
                "lane": packet.lane_id,
                "summary": packet.summary,
                "quote": packet.quote,
                "relevance": packet.relevance,
            }
            for packet in packets[:12]
        ]
        chosen_model = model_override or self.model
        prompt = self._build_synthesis_prompt(question, plan, evidence_lines, mode)
        try:
            raw_response: Any = completion(
                model=chosen_model,
                api_key=self.api_key,
                messages=[
                    {
                        "role": "system",
                        "content": self._build_synthesis_system_prompt(mode),
                    },
                    {"role": "user", "content": json.dumps(prompt)},
                ],
                temperature=0.2 if mode == "shallow" else 0.3,
            )
            message_content = raw_response["choices"][0]["message"]["content"]
            parsed = _extract_json_payload(message_content)
            raw_insights = parsed.get("insights", [])
            insights = [RankedInsight.model_validate(item) for item in raw_insights[:3]]
            if not insights:
                msg = "No insights returned from synthesis response."
                raise ValueError(msg)
            usage = raw_response.get("usage", {})
            return SynthesisResult(
                insights=insights,
                tokens_in=int(usage.get("prompt_tokens", 0)),
                tokens_out=int(usage.get("completion_tokens", 0)),
                estimated_cost_usd=0.0,
            )
        except Exception:
            logger.exception("LiteLLM synthesis failed for model %r, falling back to demo", chosen_model)
            return self.fallback.synthesize(question, plan, packets, mode=mode, model_override=model_override)

    def _build_synthesis_system_prompt(self, mode: str) -> str:
        if mode == "shallow":
            return (
                "You are a structured investigation summarizer. Reply with JSON only. "
                "Preserve the full schema but keep reasoning concise, conservative, and low-cost."
            )
        return "You are a structured invention synthesis engine. Reply with JSON only."

    def _build_synthesis_prompt(
        self,
        question: str,
        plan: InvestigationPlan,
        evidence_lines: list[dict[str, object]],
        mode: str,
    ) -> dict[str, object]:
        instructions = [
            "Return JSON only with key `insights` as an array of exactly 3 ranked insights.",
            "Each insight must include: insight_class, title, summary, source_atoms, assumptions, mechanism, proof_tree, predicted_observables, disconfirming_signals, counterfactual_tests, score.",
            "Mechanism must include name, description, steps.",
            "Proof tree must include conclusion, premises, reasoning_notes.",
            "Predicted observables must include observable, expected_signal, time_horizon, confidence.",
            "Counterfactual tests must include assumption, challenge_prompt, expected_failure_mode.",
            "Score must include novelty_distance, synthesis_depth, mechanism_quality, predictive_power, cross_domain_transfer, token_efficiency, coherence_penalty, total.",
            "Use only source atom IDs that exist in the evidence list.",
            "Summaries must include assumptions and disconfirmation-aware reasoning.",
        ]
        if mode == "shallow":
            instructions.extend(
                [
                    "Use concise summaries and shorter mechanism descriptions than deep mode.",
                    "Keep proof trees and predictions brief while still remaining schema-complete.",
                    "Prefer conservative synthesis over speculative expansion when evidence is weak.",
                ]
            )
        else:
            instructions.extend(
                [
                    "Maximize cross-source synthesis depth and mechanism quality when evidence supports it.",
                    "Use the full invention-oriented reasoning style with explicit disconfirming signals.",
                ]
            )

        return {
            "question": question,
            "objective": plan.objective,
            "novelty_target": plan.novelty_target,
            "synthesis_mode": mode,
            "lanes": [lane.model_dump() for lane in plan.lanes],
            "evidence": evidence_lines,
            "instructions": instructions,
            "scoring_formula_hint": {
                "total": "0.30*novelty_distance + 0.20*synthesis_depth + 0.20*mechanism_quality + 0.15*predictive_power + 0.10*cross_domain_transfer + 0.05*token_efficiency - 0.10*coherence_penalty"
            },
        }


def build_llm_client(settings: Settings) -> LlmClient:
    provider = settings.llm_provider.lower()
    if provider == "demo":
        return DemoLlmClient()
    if provider == "litellm":
        return LiteLlmClient(model=settings.llm_model, api_key=settings.llm_api_key)
    msg = f"Unsupported LLM_PROVIDER '{settings.llm_provider}'."
    raise ValueError(msg)
