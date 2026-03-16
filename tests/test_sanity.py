from __future__ import annotations

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.contracts import HypothesisCandidate, Mechanism
from dossier.sanity import SanityChecker


def _valid_hypothesis() -> HypothesisCandidate:
    return HypothesisCandidate(
        id="hyp_valid",
        title="Supply chain pressure hypothesis",
        summary="Summary",
        source_atom_ids=["atom_1", "atom_2"],
        is_cross_domain=False,
        assumptions=["Signals are representative."],
        confidence=0.6,
    )


def _valid_mechanism() -> Mechanism:
    return Mechanism(
        name="Pressure escalation",
        description="Contradictions escalate into delivery risk.",
        steps=[
            "Collect contradiction evidence from multiple lanes.",
            "Map contradiction clusters to failure pathways.",
        ],
    )


def _atoms() -> list[EvidenceAtom]:
    return [
        EvidenceAtom(
            case_id="case_1",
            lane_id="lane_1",
            source_id="source_1",
            source_atom_id="atom_1",
            atom_type=EvidenceAtomType.ENTITY,
            atom_value="Acme Corp",
            confidence=0.8,
            context="Acme Corp signal",
        ),
        EvidenceAtom(
            case_id="case_1",
            lane_id="lane_2",
            source_id="source_2",
            source_atom_id="atom_2",
            atom_type=EvidenceAtomType.EVENT,
            atom_value="launched",
            confidence=0.7,
            context="New process launched",
        ),
    ]


def test_sanity_checker_passes_valid_hypothesis() -> None:
    checker = SanityChecker()

    passed, reasons = checker.check(_valid_hypothesis(), _valid_mechanism(), _atoms())

    assert passed is True
    assert reasons == []


def test_sanity_checker_fails_when_assumptions_are_empty() -> None:
    checker = SanityChecker()
    hypothesis = _valid_hypothesis().model_copy(update={"assumptions": []})

    passed, reasons = checker.check(hypothesis, _valid_mechanism(), _atoms())

    assert passed is False
    assert any("assumption" in reason.lower() for reason in reasons)


def test_sanity_checker_fails_when_mechanism_has_too_few_steps() -> None:
    checker = SanityChecker()
    mechanism = _valid_mechanism().model_copy(update={"steps": []})

    passed, reasons = checker.check(_valid_hypothesis(), mechanism, _atoms())

    assert passed is False
    assert any("step" in reason.lower() for reason in reasons)


def test_sanity_checker_fails_when_hypothesis_has_no_source_atoms() -> None:
    checker = SanityChecker()
    hypothesis = _valid_hypothesis().model_copy(update={"source_atom_ids": []})

    passed, reasons = checker.check(hypothesis, _valid_mechanism(), _atoms())

    assert passed is False
    assert any("source atom" in reason.lower() for reason in reasons)


def test_sanity_checker_fails_on_generic_title() -> None:
    checker = SanityChecker()
    hypothesis = _valid_hypothesis().model_copy(update={"title": "unknown"})

    passed, reasons = checker.check(hypothesis, _valid_mechanism(), _atoms())

    assert passed is False
    assert any("generic" in reason.lower() or "title" in reason.lower() for reason in reasons)


def test_sanity_checker_fails_on_whitespace_only_assumptions() -> None:
    checker = SanityChecker()
    hypothesis = _valid_hypothesis().model_copy(update={"assumptions": ["  ", ""]})

    passed, reasons = checker.check(hypothesis, _valid_mechanism(), _atoms())

    assert passed is False
    assert any("assumption" in reason.lower() for reason in reasons)


def test_sanity_checker_fails_on_whitespace_only_mechanism_steps() -> None:
    checker = SanityChecker()
    mechanism = _valid_mechanism().model_copy(update={"steps": ["  ", ""]})

    passed, reasons = checker.check(_valid_hypothesis(), mechanism, _atoms())

    assert passed is False
    assert any("step" in reason.lower() for reason in reasons)


def test_sanity_checker_fails_when_source_atoms_not_in_typed_atoms() -> None:
    checker = SanityChecker()
    hypothesis = _valid_hypothesis().model_copy(
        update={"source_atom_ids": ["nonexistent_1", "nonexistent_2"]},
    )

    passed, reasons = checker.check(hypothesis, _valid_mechanism(), _atoms())

    assert passed is False
    assert any("not present" in reason.lower() for reason in reasons)


def test_sanity_checker_detects_temporal_inconsistency() -> None:
    checker = SanityChecker()
    atoms = [
        EvidenceAtom(
            case_id="case_1",
            lane_id="lane_1",
            source_id="source_1",
            source_atom_id="atom_1",
            atom_type=EvidenceAtomType.TEMPORAL_RELATION,
            atom_value="2020",
            confidence=0.8,
            context="In 2020 the project started",
        ),
        EvidenceAtom(
            case_id="case_1",
            lane_id="lane_2",
            source_id="source_2",
            source_atom_id="atom_2",
            atom_type=EvidenceAtomType.TEMPORAL_RELATION,
            atom_value="2023",
            confidence=0.7,
            context="By 2023 the project completed",
        ),
    ]
    # Mechanism steps mention years in reverse order (2023 before 2020)
    mechanism = _valid_mechanism().model_copy(
        update={"steps": ["In 2023 the first phase ran.", "In 2020 the second phase completed."]},
    )

    passed, reasons = checker.check(_valid_hypothesis(), mechanism, atoms)

    assert passed is False
    assert any("temporal" in reason.lower() for reason in reasons)
