from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.config import Settings
from dossier.contracts import (
    EvidencePacket,
    InvestigationPlan,
    ResearchLane,
    SourceAtom,
    TriggerType,
)
from dossier.triggers import DemoTriggerDetector, TriggerDetector


def _packet(case_id: str, lane_id: str, source_id: str, atom_id: str, title: str) -> EvidencePacket:
    return EvidencePacket(
        case_id=case_id,
        lane_id=lane_id,
        source_atom=SourceAtom(
            id=atom_id,
            source_id=source_id,
            lane_id=lane_id,
            title=title,
            url=f"https://example.com/{atom_id}",
            quote="quote",
            summary="summary",
        ),
        summary="summary",
        quote="quote",
        relevance=0.7,
    )


def _atom(
    atom_id: str,
    lane_id: str,
    source_id: str,
    source_atom_id: str,
    atom_type: EvidenceAtomType,
    atom_value: str,
    context: str,
) -> EvidenceAtom:
    return EvidenceAtom(
        id=atom_id,
        case_id="case_1",
        lane_id=lane_id,
        source_id=source_id,
        source_atom_id=source_atom_id,
        atom_type=atom_type,
        atom_value=atom_value,
        confidence=0.7,
        context=context,
    )


def _plan() -> InvestigationPlan:
    return InvestigationPlan(
        objective="Investigate: supplier concentration and delivery reliability",
        novelty_target="target",
        lanes=[
            ResearchLane(id="lane_1", name="Lane 1", query="q1", goal="g1"),
            ResearchLane(id="lane_2", name="Lane 2", query="q2", goal="g2"),
        ],
    )


def _detector() -> TriggerDetector:
    return TriggerDetector(Settings(LLM_PROVIDER="litellm", TRIGGER_MIN_CONFIDENCE=0.5))


def test_cross_lane_convergence_trigger_fires() -> None:
    packets = [
        _packet("case_1", "lane_1", "source_1", "atom_a", "A"),
        _packet("case_1", "lane_2", "source_2", "atom_b", "B"),
    ]
    atoms = [
        _atom("e1", "lane_1", "source_1", "atom_a", EvidenceAtomType.ENTITY, "Acme Corp", "Acme Corp"),
        _atom("e2", "lane_2", "source_2", "atom_b", EvidenceAtomType.ENTITY, "Acme Corp", "Acme Corp"),
        _atom("e3", "lane_1", "source_1", "atom_a", EvidenceAtomType.ENTITY, "Delivery Risk", "Delivery Risk"),
        _atom("e4", "lane_2", "source_2", "atom_b", EvidenceAtomType.ENTITY, "Delivery Risk", "Delivery Risk"),
    ]

    triggers = _detector().detect(_plan(), packets, atoms, [], [], [])

    assert TriggerType.CROSS_LANE_CONVERGENCE in {trigger.trigger_type for trigger in triggers}


def test_contradiction_density_trigger_fires() -> None:
    packets = [_packet("case_1", "lane_1", "source_1", "atom_a", "A")] * 4
    atoms = [
        _atom(f"c{i}", "lane_1", "source_1", "atom_a", EvidenceAtomType.CONTRADICTION, "however", "however")
        for i in range(3)
    ] + [
        _atom("n1", "lane_1", "source_1", "atom_a", EvidenceAtomType.NUMERIC, "12%", "12%"),
    ]

    triggers = _detector().detect(_plan(), packets, atoms, [], [], [])

    assert TriggerType.CONTRADICTION_DENSITY in {trigger.trigger_type for trigger in triggers}


def test_unexplained_event_trigger_fires() -> None:
    packets = [_packet("case_1", "lane_1", "source_1", "atom_a", "A")] * 4
    atoms = [
        _atom("ev1", "lane_1", "source_1", "atom_a", EvidenceAtomType.EVENT, "launched", "Product launched"),
    ]

    triggers = _detector().detect(_plan(), packets, atoms, [], [], [])

    assert TriggerType.UNEXPLAINED_EVENT in {trigger.trigger_type for trigger in triggers}


def test_meaningful_absence_trigger_fires() -> None:
    packets = [_packet("case_1", "lane_1", "source_1", "atom_a", "A")]

    triggers = _detector().detect(_plan(), packets, [], [], [], [])

    assert TriggerType.MEANINGFUL_ABSENCE in {trigger.trigger_type for trigger in triggers}


def test_weak_signal_alignment_trigger_fires() -> None:
    packets = [_packet("case_1", "lane_1", "source_1", "atom_a", "A")] * 4
    atoms = [
        _atom(
            "w1",
            "lane_1",
            "source_1",
            "atom_a",
            EvidenceAtomType.WEAK_SIGNAL,
            "might",
            "Supplier delay escalation risk remains unclear",
        ),
        _atom(
            "w2",
            "lane_2",
            "source_2",
            "atom_b",
            EvidenceAtomType.WEAK_SIGNAL,
            "could",
            "Supplier delay escalation risk is still possible",
        ),
    ]

    triggers = _detector().detect(_plan(), packets, atoms, [], [], [])

    assert TriggerType.WEAK_SIGNAL_ALIGNMENT in {trigger.trigger_type for trigger in triggers}


def test_sparse_retrieval_trigger_fires() -> None:
    packets = [
        _packet("case_1", "lane_1", "source_1", "atom_a", "A"),
        _packet("case_1", "lane_2", "source_2", "atom_b", "B"),
        _packet("case_1", "lane_2", "source_3", "atom_c", "C"),
    ]

    triggers = _detector().detect(_plan(), packets, [], [], [], [])

    assert TriggerType.SPARSE_RETRIEVAL in {trigger.trigger_type for trigger in triggers}


def test_uncertainty_spike_trigger_fires() -> None:
    packets = [_packet("case_1", "lane_1", "source_1", "atom_a", "A")] * 5
    atoms = [
        _atom("u1", "lane_1", "source_1", "atom_a", EvidenceAtomType.WEAK_SIGNAL, "might", "might"),
        _atom("u2", "lane_1", "source_1", "atom_a", EvidenceAtomType.WEAK_SIGNAL, "could", "could"),
        _atom("u3", "lane_1", "source_1", "atom_a", EvidenceAtomType.CONTRADICTION, "however", "however"),
        _atom("u4", "lane_2", "source_2", "atom_b", EvidenceAtomType.ABSENCE, "missing", "missing"),
        _atom("n1", "lane_1", "source_1", "atom_a", EvidenceAtomType.NUMERIC, "12%", "12%"),
        _atom("n2", "lane_2", "source_2", "atom_b", EvidenceAtomType.ENTITY, "Acme", "Acme"),
    ]

    triggers = _detector().detect(_plan(), packets, atoms, [], [], [])

    assert TriggerType.UNCERTAINTY_SPIKE in {trigger.trigger_type for trigger in triggers}


def test_analogical_match_trigger_fires_from_case_memory() -> None:
    packets = [_packet("case_1", "lane_1", "source_1", "atom_a", "A")] * 4
    atoms = [
        _atom("e1", "lane_1", "source_1", "atom_a", EvidenceAtomType.ENTITY, "Supplier Concentration", "entity")
    ]
    notes = ["[mechanism_pattern] Supplier concentration risk can amplify delivery delays (score: 0.82)"]

    triggers = _detector().detect(_plan(), packets, atoms, [], [], notes)

    assert TriggerType.ANALOGICAL_MATCH in {trigger.trigger_type for trigger in triggers}


def test_clean_evidence_yields_no_triggers() -> None:
    plan = InvestigationPlan(
        objective="Investigate: independent signals remain healthy",
        novelty_target="target",
        lanes=[
            ResearchLane(id="lane_1", name="Lane 1", query="q1", goal="g1"),
            ResearchLane(id="lane_2", name="Lane 2", query="q2", goal="g2"),
        ],
    )
    packets = [
        _packet("case_1", "lane_1", "source_1", "atom_a", "A"),
        _packet("case_1", "lane_1", "source_2", "atom_b", "B"),
        _packet("case_1", "lane_2", "source_3", "atom_c", "C"),
        _packet("case_1", "lane_2", "source_4", "atom_d", "D"),
    ]
    atoms = [
        _atom("n1", "lane_1", "source_1", "atom_a", EvidenceAtomType.NUMERIC, "12%", "12%"),
        _atom("t1", "lane_1", "source_2", "atom_b", EvidenceAtomType.TEMPORAL_RELATION, "Q3", "Q3"),
        _atom("n2", "lane_2", "source_3", "atom_c", EvidenceAtomType.NUMERIC, "18%", "18%"),
        _atom("t2", "lane_2", "source_4", "atom_d", EvidenceAtomType.TEMPORAL_RELATION, "Q4", "Q4"),
    ]

    triggers = _detector().detect(plan, packets, atoms, [], [], [])

    assert triggers == []


def test_demo_trigger_detector_always_returns_one_trigger() -> None:
    triggers = DemoTriggerDetector().detect(_plan(), [], [], [], [], [])

    assert len(triggers) == 1
    assert triggers[0].trigger_type is TriggerType.CROSS_LANE_CONVERGENCE
