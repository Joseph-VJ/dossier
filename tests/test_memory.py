from pathlib import Path

from dossier.contracts import (
    CounterfactualTest,
    InsightClass,
    Mechanism,
    NoveltyScore,
    Prediction,
    ProofTree,
    RankedInsight,
)
from dossier.db import SqliteRepository
from dossier.memory import CaseMemoryManager


def _repo(tmp_path: Path) -> SqliteRepository:
    repo = SqliteRepository(tmp_path / "memory.db")
    repo.initialize()
    return repo


def _insight(total: float) -> RankedInsight:
    return RankedInsight(
        insight_class=InsightClass.SPECULATIVE_MECHANISM,
        title="Vendor pressure pattern",
        summary="Supplier concentration can amplify delivery failures.",
        source_atoms=["atom_1", "atom_2"],
        assumptions=["Signals are representative."],
        mechanism=Mechanism(
            name="Concentration pressure",
            description="Single points of operational pressure compound downstream delays.",
            steps=["Identify concentration.", "Track failure propagation."],
        ),
        proof_tree=ProofTree(
            conclusion="Concentration creates a fragile operating mode.",
            premises=["Few suppliers dominate the chain."],
            reasoning_notes=["Needs stronger corroboration."],
        ),
        predicted_observables=[
            Prediction(
                observable="Supplier delay cluster",
                expected_signal="Repeated delays from the same upstream dependency.",
                time_horizon="next quarter",
                confidence=0.6,
            )
        ],
        disconfirming_signals=["Delay sources stay diversified."],
        counterfactual_tests=[
            CounterfactualTest(
                assumption="Concentration is the main driver.",
                challenge_prompt="What if delays are evenly spread across suppliers?",
                expected_failure_mode="The mechanism no longer explains the failures.",
            )
        ],
        score=NoveltyScore(
            novelty_distance=0.7,
            synthesis_depth=0.65,
            mechanism_quality=0.7,
            predictive_power=0.6,
            cross_domain_transfer=0.45,
            token_efficiency=0.8,
            coherence_penalty=0.08,
            total=total,
        ),
    )


def test_warm_start_returns_default_when_empty(tmp_path: Path) -> None:
    manager = CaseMemoryManager(_repo(tmp_path))
    assert manager.warm_start("Why did supplier concentration increase?") == [
        "No prior case memory found."
    ]


def test_warm_start_returns_relevant_motifs(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.store_case_memory(
        case_id="case_1",
        motif_type="mechanism_pattern",
        content="Supplier concentration pressure often predicts delivery volatility.",
        score=0.82,
    )
    repo.store_case_memory(
        case_id="case_2",
        motif_type="failed_approach",
        content="Marketing narrative rarely explains supply delays.",
        score=0.4,
    )
    manager = CaseMemoryManager(repo)

    notes = manager.warm_start("Why did supplier concentration hurt delivery reliability?")

    assert len(notes) == 1
    assert notes[0].startswith("[mechanism_pattern]")
    assert "0.82" in notes[0]


def test_writeback_stores_only_strong_insights(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    manager = CaseMemoryManager(repo)

    written = manager.writeback("case_1", [_insight(0.72), _insight(0.5)])
    matches = repo.search_case_memory(["pressure", "pattern"], limit=10)

    assert written == 2
    assert len(matches) == 2
    assert {match["motif_type"] for match in matches} == {
        "mechanism_pattern",
        "hypothesis_template",
    }


def test_writeback_skips_low_scoring_insights(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    manager = CaseMemoryManager(repo)

    written = manager.writeback("case_1", [_insight(0.5)])

    assert written == 0
    assert repo.search_case_memory(["vendor", "pressure"], limit=10) == []
