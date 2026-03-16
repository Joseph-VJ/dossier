from __future__ import annotations

from dossier.config import Settings
from dossier.contracts import CounterfactualTest, HypothesisCandidate, Mechanism, NoveltyScore
from dossier.ranking import CandidateScoreProvider, InventionRanker


class FixedScoreProvider(CandidateScoreProvider):
    def __init__(self, totals: dict[str, float]) -> None:
        self.totals = totals

    def score(self, candidate: dict) -> NoveltyScore:
        hypothesis = candidate["hypothesis"]
        total = self.totals[hypothesis.id]
        return NoveltyScore(
            novelty_distance=total,
            synthesis_depth=total,
            mechanism_quality=total,
            predictive_power=total,
            cross_domain_transfer=total,
            token_efficiency=total,
            coherence_penalty=0.0,
            total=total,
        )


def _hypothesis(index: int, confidence: float = 0.6) -> HypothesisCandidate:
    return HypothesisCandidate(
        id=f"hyp_{index}",
        title=f"Hypothesis {index}",
        summary="Candidate summary",
        source_atom_ids=["atom_1", "atom_2"],
        is_cross_domain=False,
        assumptions=["Assumption A"],
        confidence=confidence,
    )


def _mechanism(index: int) -> Mechanism:
    return Mechanism(
        id=f"mechanism_{index}",
        name=f"Mechanism {index}",
        description="Mechanism description",
        steps=["Step 1", "Step 2"],
    )


def _candidate(index: int, sanity_passed: bool = True) -> dict:
    return {
        "hypothesis": _hypothesis(index),
        "mechanism": _mechanism(index),
        "counterfactual_tests": [
            CounterfactualTest(
                assumption="Assumption A",
                challenge_prompt="What if A is false?",
                expected_failure_mode="Mechanism confidence drops.",
            )
        ],
        "sanity_passed": sanity_passed,
        "sanity_reasons": [] if sanity_passed else ["Failed sanity."],
    }


def test_rank_discards_candidates_below_threshold() -> None:
    candidates = [_candidate(1), _candidate(2), _candidate(3)]
    ranker = InventionRanker(
        Settings(RANKING_TOP_K=5),
        scorer=FixedScoreProvider({"hyp_1": 0.80, "hyp_2": 0.47, "hyp_3": 0.62}),
    )

    insights = ranker.rank(candidates)

    titles = [insight.title for insight in insights]
    assert all("Hypothesis 2" not in title for title in titles)
    assert len(insights) == 2


def test_rank_classification_labels_match_thresholds() -> None:
    ranker = InventionRanker(Settings(), scorer=FixedScoreProvider({}))

    assert ranker.classify_label(0.78) == "Breakthrough"
    assert ranker.classify_label(0.62) == "Strong novel"
    assert ranker.classify_label(0.48) == "Exploratory"
    assert ranker.classify_label(0.47) is None


def test_rank_applies_top_k_sorting() -> None:
    candidates = [_candidate(1), _candidate(2), _candidate(3)]
    ranker = InventionRanker(
        Settings(RANKING_TOP_K=2),
        scorer=FixedScoreProvider({"hyp_1": 0.70, "hyp_2": 0.90, "hyp_3": 0.80}),
    )

    insights = ranker.rank(candidates)

    assert len(insights) == 2
    assert "Hypothesis 2" in insights[0].title
    assert "Hypothesis 3" in insights[1].title


def test_rank_filters_sanity_failed_candidates() -> None:
    candidates = [_candidate(1, sanity_passed=False), _candidate(2, sanity_passed=True)]
    ranker = InventionRanker(
        Settings(RANKING_TOP_K=5),
        scorer=FixedScoreProvider({"hyp_1": 0.95, "hyp_2": 0.70}),
    )

    insights = ranker.rank(candidates)

    assert len(insights) == 1
    assert "Hypothesis 2" in insights[0].title
