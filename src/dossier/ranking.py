from __future__ import annotations

import json
import logging
from typing import Any, Protocol, TypedDict

from litellm import completion

from dossier.config import Settings
from dossier.contracts import (
    CounterfactualTest,
    HypothesisCandidate,
    InsightClass,
    Mechanism,
    NoveltyScore,
    Prediction,
    ProofTree,
    RankedInsight,
)
from dossier.llm_utils import extract_content_text

logger = logging.getLogger(__name__)


class RankCandidate(TypedDict):
    hypothesis: HypothesisCandidate
    mechanism: Mechanism
    counterfactual_tests: list[CounterfactualTest]
    sanity_passed: bool
    sanity_reasons: list[str]


class CandidateScoreProvider(Protocol):
    def score(self, candidate: RankCandidate) -> NoveltyScore:
        ...


class InventionRankerProtocol(Protocol):
    def rank(self, candidates: list[RankCandidate]) -> list[RankedInsight]:
        ...


def _clamp_01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _parse_score_payload(content: Any) -> dict[str, Any]:
    text = extract_content_text(content)
    if not text:
        msg = "Scoring response was empty."
        raise ValueError(msg)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        msg = "Scoring response did not contain JSON."
        raise ValueError(msg)

    parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        msg = "Scoring payload must be a JSON object."
        raise ValueError(msg)

    score_payload: Any = parsed.get("score", parsed)
    if not isinstance(score_payload, dict):
        msg = "Scoring payload must contain a score object."
        raise ValueError(msg)
    return score_payload


class HeuristicScoreProvider:
    def score(self, candidate: RankCandidate) -> NoveltyScore:
        hypothesis = candidate["hypothesis"]
        mechanism = candidate["mechanism"]
        counterfactuals = candidate["counterfactual_tests"]
        sanity_reasons = candidate["sanity_reasons"]

        step_count = max(1, len([step for step in mechanism.steps if step.strip()]))
        source_count = max(1, len(set(hypothesis.source_atom_ids)))
        assumption_count = max(1, len([item for item in hypothesis.assumptions if item.strip()]))
        counterfactual_count = len(counterfactuals)

        cross_domain_bonus = 0.10 if hypothesis.is_cross_domain else 0.0
        novelty_distance = _clamp_01(0.40 + 0.45 * hypothesis.confidence + cross_domain_bonus)
        synthesis_depth = _clamp_01(0.35 + 0.12 * step_count + 0.06 * source_count)
        mechanism_quality = _clamp_01(0.38 + 0.14 * step_count + 0.04 * assumption_count)
        predictive_power = _clamp_01(0.34 + 0.15 * min(3, assumption_count))
        cross_domain_transfer = _clamp_01(0.25 + (0.35 if hypothesis.is_cross_domain else 0.10))
        token_efficiency = _clamp_01(0.50 + 0.08 * min(4, source_count) - 0.03 * max(0, step_count - 3))
        coherence_penalty = _clamp_01(0.08 + 0.03 * max(0, len(sanity_reasons)) - 0.02 * counterfactual_count)

        return NoveltyScore(
            novelty_distance=novelty_distance,
            synthesis_depth=synthesis_depth,
            mechanism_quality=mechanism_quality,
            predictive_power=predictive_power,
            cross_domain_transfer=cross_domain_transfer,
            token_efficiency=token_efficiency,
            coherence_penalty=coherence_penalty,
        )


class LiteLlmScoreProvider:
    def __init__(
        self,
        model: str,
        api_key: str | None,
        fallback: CandidateScoreProvider | None = None,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.fallback = fallback or HeuristicScoreProvider()

    def score(self, candidate: RankCandidate) -> NoveltyScore:
        hypothesis = candidate["hypothesis"]
        mechanism = candidate["mechanism"]
        payload = {
            "hypothesis": hypothesis.model_dump(mode="json"),
            "mechanism": mechanism.model_dump(mode="json"),
            "counterfactual_count": len(candidate["counterfactual_tests"]),
            "sanity_reasons": candidate["sanity_reasons"],
            "instructions": (
                "Rate this candidate on novelty_distance, synthesis_depth, mechanism_quality, "
                "predictive_power, cross_domain_transfer, token_efficiency, coherence_penalty. "
                "Return JSON only."
            ),
        }
        try:
            raw_response: Any = completion(
                model=self.model,
                api_key=self.api_key,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Score invention candidates using a 0-1 scale. Return JSON only. "
                            "Keys: novelty_distance, synthesis_depth, mechanism_quality, "
                            "predictive_power, cross_domain_transfer, token_efficiency, coherence_penalty."
                        ),
                    },
                    {"role": "user", "content": json.dumps(payload)},
                ],
                temperature=0.1,
            )
            message_content = raw_response["choices"][0]["message"]["content"]
            score_payload = _parse_score_payload(message_content)
            return NoveltyScore.model_validate(score_payload)
        except Exception:
            logger.warning(
                "LLM scoring failed for hypothesis %s; using heuristic scorer.",
                hypothesis.id,
                exc_info=True,
            )
            return self.fallback.score(candidate)


class InventionRanker:
    def __init__(self, settings: Settings, scorer: CandidateScoreProvider | None = None) -> None:
        self.settings = settings
        self.top_k = settings.ranking_top_k
        self.scorer = scorer or self._default_scorer(settings)

    def _default_scorer(self, settings: Settings) -> CandidateScoreProvider:
        if settings.llm_provider.lower() == "litellm":
            return LiteLlmScoreProvider(model=settings.llm_model, api_key=settings.llm_api_key)
        return HeuristicScoreProvider()

    def classify_label(self, total_score: float) -> str | None:
        if total_score >= 0.78:
            return "Breakthrough"
        if total_score >= 0.62:
            return "Strong novel"
        if total_score >= 0.48:
            return "Exploratory"
        return None

    def _insight_class_for_label(self, label: str) -> InsightClass:
        if label == "Breakthrough":
            return InsightClass.NOVEL_DEDUCTION
        if label == "Strong novel":
            return InsightClass.SPECULATIVE_MECHANISM
        return InsightClass.EXPLORATORY_PREDICTION

    def _build_proof_tree(
        self,
        candidate: RankCandidate,
        label: str,
    ) -> ProofTree:
        hypothesis = candidate["hypothesis"]
        mechanism = candidate["mechanism"]
        premises = [f"Source atom: {source_atom_id}" for source_atom_id in hypothesis.source_atom_ids[:3]]
        premises.extend([f"Assumption: {item}" for item in hypothesis.assumptions[:2]])
        premises.append(f"Mechanism anchor: {mechanism.name}")
        reasoning_notes = [f"Classification: {label}"]
        if candidate["sanity_reasons"]:
            reasoning_notes.extend(candidate["sanity_reasons"])
        return ProofTree(
            conclusion=hypothesis.summary,
            premises=premises,
            reasoning_notes=reasoning_notes,
        )

    def _build_predictions(self, hypothesis: HypothesisCandidate, score: NoveltyScore) -> list[Prediction]:
        assumptions = [item for item in hypothesis.assumptions if item.strip()]
        if not assumptions:
            assumptions = ["Core assumption should be validated with one new retrieval pass."]
        base_confidence = score.total if score.total is not None else hypothesis.confidence
        predictions: list[Prediction] = []
        for index, assumption in enumerate(assumptions[:2], start=1):
            confidence = _clamp_01(base_confidence - 0.05 + (0.03 * index))
            predictions.append(
                Prediction(
                    observable=f"Assumption {index} validation",
                    expected_signal=f"Evidence supports or falsifies: {assumption}",
                    time_horizon="next iteration",
                    confidence=confidence,
                )
            )
        return predictions

    def _build_disconfirming_signals(self, candidate: RankCandidate) -> list[str]:
        signals = [item.expected_failure_mode for item in candidate["counterfactual_tests"]]
        signals.extend(candidate["sanity_reasons"])
        unique_signals: list[str] = []
        for signal in signals:
            normalized = signal.strip()
            if not normalized or normalized in unique_signals:
                continue
            unique_signals.append(normalized)
        if not unique_signals:
            unique_signals.append("No disconfirming signal supplied; requires one explicit challenge test.")
        return unique_signals

    def _to_ranked_insight(self, candidate: RankCandidate, score: NoveltyScore, label: str) -> RankedInsight:
        hypothesis = candidate["hypothesis"]
        mechanism = candidate["mechanism"]
        return RankedInsight(
            insight_class=self._insight_class_for_label(label),
            title=f"[{label}] {hypothesis.title}",
            summary=f"{hypothesis.summary} Classification: {label}.",
            source_atoms=hypothesis.source_atom_ids,
            assumptions=hypothesis.assumptions,
            mechanism=mechanism,
            proof_tree=self._build_proof_tree(candidate, label),
            predicted_observables=self._build_predictions(hypothesis, score),
            disconfirming_signals=self._build_disconfirming_signals(candidate),
            counterfactual_tests=candidate["counterfactual_tests"],
            score=score,
        )

    def rank(self, candidates: list[RankCandidate]) -> list[RankedInsight]:
        surviving = [candidate for candidate in candidates if candidate["sanity_passed"]]
        insights: list[RankedInsight] = []
        for candidate in surviving:
            score = self.scorer.score(candidate)
            total = score.total if score.total is not None else 0.0
            label = self.classify_label(total)
            if label is None:
                continue
            insights.append(self._to_ranked_insight(candidate, score, label))

        insights.sort(key=lambda item: (-(item.score.total or 0.0), item.title.lower()))
        return insights[: self.top_k]


class DemoInventionRanker(InventionRanker):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, scorer=HeuristicScoreProvider())


def build_invention_ranker(settings: Settings) -> InventionRankerProtocol:
    provider = settings.llm_provider.lower()
    if provider == "demo":
        return DemoInventionRanker(settings)
    if provider == "litellm":
        return InventionRanker(settings)
    msg = f"Unsupported LLM_PROVIDER '{settings.llm_provider}'."
    raise ValueError(msg)
