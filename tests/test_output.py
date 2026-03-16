from pathlib import Path

from dossier.contracts import (
    CounterfactualTest,
    EvidencePacket,
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
    TriggerResult,
    TriggerType,
)
from dossier.output import render_dossier_markdown, write_dossier


def _sample_data() -> (
    tuple[
        str,
        str,
        InvestigationPlan,
        list[EvidencePacket],
        list[TriggerResult],
        list[RankedInsight],
        InvestigationMetrics,
    ]
):
    question = "Test question?"
    case_id = "case_abc123"
    lane = ResearchLane(id="lane_1", name="Lane A", query="q", goal="g")
    plan = InvestigationPlan(
        objective="obj", novelty_target="target", lanes=[lane]
    )
    packet = EvidencePacket(
        case_id=case_id,
        lane_id="lane_1",
        source_atom=SourceAtom(
            source_id="s1", lane_id="lane_1", title="Source 1",
            url="https://example.com", quote="quote text", summary="summary text",
        ),
        summary="packet summary",
        quote="packet quote",
        relevance=0.6,
    )
    insight = RankedInsight(
        insight_class=InsightClass.NOVEL_DEDUCTION,
        title="Insight One",
        summary="insight summary",
        source_atoms=["a1"],
        assumptions=["assume"],
        mechanism=Mechanism(name="mech", description="desc", steps=["s1"]),
        proof_tree=ProofTree(conclusion="conc", premises=["p"], reasoning_notes=["n"]),
        predicted_observables=[
            Prediction(observable="obs", expected_signal="sig", time_horizon="now", confidence=0.5)
        ],
        disconfirming_signals=["dis"],
        counterfactual_tests=[
            CounterfactualTest(assumption="a", challenge_prompt="cp", expected_failure_mode="efm")
        ],
        score=NoveltyScore(
            novelty_distance=0.5, synthesis_depth=0.5, mechanism_quality=0.5,
            predictive_power=0.5, cross_domain_transfer=0.5, token_efficiency=0.5,
            coherence_penalty=0.1,
        ),
    )
    trigger = TriggerResult(
        trigger_type=TriggerType.CROSS_LANE_CONVERGENCE,
        description="Shared entities recur across lanes.",
        confidence=0.82,
        supporting_evidence=["a1", "a2"],
    )
    metrics = InvestigationMetrics(
        search_queries=1, sources_considered=1, evidence_packets=1, packets_after_compression=1,
        evidence_atoms_extracted=3, graph_nodes_created=5, graph_edges_created=4,
        triggers_fired=1, trigger_types=[TriggerType.CROSS_LANE_CONVERGENCE.value], synthesis_mode="deep",
        tokens_in=100, tokens_out=50, estimated_cost_usd=0.01,
        latency_seconds=1.5, grounded_novelty_ratio=0.5, coherence_failures=0,
    )
    return question, case_id, plan, [packet], [trigger], [insight], metrics


def test_render_contains_question() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert question in md


def test_render_contains_case_id() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert case_id in md


def test_render_contains_lane_name() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "Lane A" in md


def test_render_contains_insight_title() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "Insight One" in md


def test_render_contains_metrics() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "Latency seconds" in md
    assert "1.5" in md
    assert "Evidence atoms extracted" in md
    assert "3" in md
    assert "Packets after compression" in md
    assert "Graph nodes created" in md
    assert "5" in md
    assert "Graph edges created" in md
    assert "4" in md
    assert "Triggers fired" in md
    assert "Synthesis mode: deep" in md


def test_render_contains_prediction() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "obs" in md
    assert "sig" in md


def test_render_contains_score_breakdown() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "Score breakdown" in md
    assert "NoveltyDistance" in md
    assert "SynthesisDepth" in md


def test_render_contains_mechanism_steps_proof_tree_and_counterfactuals() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "Mechanism steps:" in md
    assert "s1" in md
    assert "Proof Tree:" in md
    assert "Conclusion: conc" in md
    assert "Premises:" in md
    assert "Reasoning notes:" in md
    assert "Counterfactual tests:" in md
    assert "Challenge prompt: cp" in md
    assert "Expected failure mode: efm" in md


def test_render_contains_trigger_detection_section() -> None:
    question, case_id, plan, packets, triggers, insights, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, packets, triggers, insights, metrics)
    assert "## Trigger Detection" in md
    assert "Cross-lane convergence" in md
    assert "Shared entities recur across lanes." in md


def test_render_empty_packets_and_insights() -> None:
    question, case_id, plan, _, _, _, metrics = _sample_data()
    md = render_dossier_markdown(question, case_id, plan, [], [], [], metrics)
    assert "## Evidence Packets" in md
    assert "## Trigger Detection" in md
    assert "## Ranked Insights" in md


def test_write_dossier_creates_file(tmp_path: Path) -> None:
    path = write_dossier(tmp_path, "case_test", "# Hello")
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "# Hello"
    assert path.name == "case_test.md"


def test_write_dossier_creates_dir(tmp_path: Path) -> None:
    nested = tmp_path / "sub" / "dir"
    path = write_dossier(nested, "case_x", "content")
    assert path.exists()
    assert nested.exists()
