import pytest
from pydantic import ValidationError

from dossier.contracts.models import (
    Contradiction,
    CounterfactualTest,
    EvidencePacket,
    Hypothesis,
    HypothesisCandidate,
    InsightClass,
    InvestigationMetrics,
    InvestigationPlan,
    Mechanism,
    NoveltyScore,
    Prediction,
    ProofTree,
    RankedInsight,
    ResearchLane,
    SourceAtom,
    SourceOriginCluster,
    SynthesisResult,
    TriggerResult,
    TriggerType,
    new_id,
)

# --- new_id ---


def test_new_id_has_prefix() -> None:
    result = new_id("case")
    assert result.startswith("case_")


def test_new_id_unique() -> None:
    ids = {new_id("x") for _ in range(100)}
    assert len(ids) == 100


# --- NoveltyScore ---


def test_novelty_score_computes_total_when_missing() -> None:
    score = NoveltyScore(
        novelty_distance=0.7,
        synthesis_depth=0.6,
        mechanism_quality=0.8,
        predictive_power=0.5,
        cross_domain_transfer=0.4,
        token_efficiency=0.9,
        coherence_penalty=0.1,
    )

    assert score.total is not None
    assert 0.0 <= score.total <= 1.0


def test_novelty_score_accepts_close_total() -> None:
    # Pre-compute expected total manually so we can supply one within tolerance
    score_auto = NoveltyScore(
        novelty_distance=0.7,
        synthesis_depth=0.6,
        mechanism_quality=0.8,
        predictive_power=0.5,
        cross_domain_transfer=0.4,
        token_efficiency=0.9,
        coherence_penalty=0.1,
    )
    assert score_auto.total is not None
    # Supply a total within 0.15 of computed
    score_manual = NoveltyScore(
        novelty_distance=0.7,
        synthesis_depth=0.6,
        mechanism_quality=0.8,
        predictive_power=0.5,
        cross_domain_transfer=0.4,
        token_efficiency=0.9,
        coherence_penalty=0.1,
        total=score_auto.total,
    )
    assert score_manual.total == score_auto.total


def test_novelty_score_rejects_distant_total() -> None:
    with pytest.raises(ValidationError, match="deviates too far"):
        NoveltyScore(
            novelty_distance=0.7,
            synthesis_depth=0.6,
            mechanism_quality=0.8,
            predictive_power=0.5,
            cross_domain_transfer=0.4,
            token_efficiency=0.9,
            coherence_penalty=0.1,
            total=0.1,  # Far from the computed ~0.63
        )


def test_novelty_score_clamps_to_zero() -> None:
    score = NoveltyScore(
        novelty_distance=0.0,
        synthesis_depth=0.0,
        mechanism_quality=0.0,
        predictive_power=0.0,
        cross_domain_transfer=0.0,
        token_efficiency=0.0,
        coherence_penalty=1.0,
    )
    assert score.total == 0.0


def test_novelty_score_high_values() -> None:
    score = NoveltyScore(
        novelty_distance=1.0,
        synthesis_depth=1.0,
        mechanism_quality=1.0,
        predictive_power=1.0,
        cross_domain_transfer=1.0,
        token_efficiency=1.0,
        coherence_penalty=0.0,
    )
    assert score.total == 1.0


# --- Field validation ---


def test_relevance_out_of_range_rejected() -> None:
    with pytest.raises(ValidationError):
        EvidencePacket(
            case_id="c1",
            lane_id="l1",
            source_atom=SourceAtom(
                source_id="s1", lane_id="l1", title="t", url="u", quote="q", summary="s"
            ),
            summary="s",
            quote="q",
            relevance=1.5,
        )


def test_prediction_confidence_out_of_range_rejected() -> None:
    with pytest.raises(ValidationError):
        Prediction(
            observable="x",
            expected_signal="y",
            time_horizon="now",
            confidence=2.0,
        )


# --- Round-trip serialization ---


def test_research_lane_round_trip() -> None:
    lane = ResearchLane(name="Test", query="q", goal="g")
    data = lane.model_dump(mode="json")
    restored = ResearchLane.model_validate(data)
    assert restored.name == lane.name
    assert restored.id == lane.id


def test_investigation_plan_round_trip() -> None:
    plan = InvestigationPlan(
        objective="obj", novelty_target="target",
        lanes=[ResearchLane(name="A", query="q", goal="g")],
    )
    data = plan.model_dump(mode="json")
    restored = InvestigationPlan.model_validate(data)
    assert restored.objective == plan.objective
    assert len(restored.lanes) == 1


def test_ranked_insight_round_trip() -> None:
    insight = RankedInsight(
        insight_class=InsightClass.NOVEL_DEDUCTION,
        title="Test",
        summary="Summary",
        source_atoms=["a1"],
        assumptions=["a"],
        mechanism=Mechanism(name="m", description="d", steps=["s"]),
        proof_tree=ProofTree(conclusion="c", premises=["p"], reasoning_notes=["n"]),
        predicted_observables=[
            Prediction(observable="o", expected_signal="e", time_horizon="t", confidence=0.5)
        ],
        disconfirming_signals=["d"],
        counterfactual_tests=[
            CounterfactualTest(assumption="a", challenge_prompt="cp", expected_failure_mode="efm")
        ],
        score=NoveltyScore(
            novelty_distance=0.5, synthesis_depth=0.5, mechanism_quality=0.5,
            predictive_power=0.5, cross_domain_transfer=0.5, token_efficiency=0.5,
            coherence_penalty=0.1,
        ),
    )
    data = insight.model_dump(mode="json")
    restored = RankedInsight.model_validate(data)
    assert restored.title == "Test"
    assert restored.score.total is not None


# --- Enum ---


def test_insight_class_values() -> None:
    assert InsightClass.NOVEL_DEDUCTION.value == "Novel Deduction"
    assert InsightClass.SPECULATIVE_MECHANISM.value == "Speculative Mechanism"
    assert InsightClass.EXPLORATORY_PREDICTION.value == "Exploratory Prediction"


def test_trigger_type_values() -> None:
    assert TriggerType.CROSS_LANE_CONVERGENCE.value == "Cross-lane convergence"
    assert TriggerType.SPARSE_RETRIEVAL.value == "Sparse retrieval"


# --- Other models ---


def test_source_origin_cluster_creates() -> None:
    cluster = SourceOriginCluster(
        label="test", member_source_ids=["s1", "s2"], independence_note="note"
    )
    assert cluster.id.startswith("origin_")


def test_contradiction_creates() -> None:
    c = Contradiction(
        left_source_id="a", right_source_id="b", description="d", severity=0.5
    )
    assert c.id.startswith("contradiction_")


def test_hypothesis_creates() -> None:
    h = Hypothesis(title="t", summary="s", source_atom_ids=["a"], assumptions=["a"])
    assert h.id.startswith("hypothesis_")


def test_hypothesis_candidate_creates() -> None:
    candidate = HypothesisCandidate(
        title="candidate",
        summary="summary",
        source_atom_ids=["atom_1", "atom_2"],
        is_cross_domain=True,
        assumptions=["a1"],
        confidence=0.6,
    )
    assert candidate.id.startswith("hyp_")


def test_synthesis_result_defaults() -> None:
    sr = SynthesisResult(insights=[])
    assert sr.tokens_in == 0
    assert sr.tokens_out == 0
    assert sr.estimated_cost_usd == 0.0


def test_trigger_result_creates() -> None:
    trigger = TriggerResult(
        trigger_type=TriggerType.MEANINGFUL_ABSENCE,
        description="Lane returned no packets.",
        confidence=0.7,
        supporting_evidence=["lane_1"],
    )
    assert trigger.trigger_type is TriggerType.MEANINGFUL_ABSENCE


def test_investigation_metrics_defaults() -> None:
    m = InvestigationMetrics()
    assert m.search_queries == 0
    assert m.packets_after_compression == 0
    assert m.evidence_atoms_extracted == 0
    assert m.graph_nodes_created == 0
    assert m.graph_edges_created == 0
    assert m.triggers_fired == 0
    assert m.trigger_types == []
    assert m.synthesis_mode == "deep"
    assert m.latency_seconds == 0.0
