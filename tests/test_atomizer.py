from dossier.atomizer import EvidenceAtomizer, EvidenceAtomType


def test_atomizer_extracts_multiple_atom_types() -> None:
    atomizer = EvidenceAtomizer()
    atoms = atomizer.extract_atoms(
        case_id="case_1",
        lane_id="lane_1",
        source_id="source_1",
        source_atom_id="atom_1",
        title="Acme Corp Q3 update",
        summary="Revenue declined 12% in Q3 2025, but management announced a turnaround plan.",
        quote="The board might revisit strategy next quarter due to missing enterprise deals.",
        content="Acme Corp announced layoffs despite prior growth guidance.",
    )
    atom_types = {atom.atom_type for atom in atoms}
    assert EvidenceAtomType.ENTITY in atom_types
    assert EvidenceAtomType.NUMERIC in atom_types
    assert EvidenceAtomType.TEMPORAL_RELATION in atom_types
    assert EvidenceAtomType.CONTRADICTION in atom_types
    assert EvidenceAtomType.WEAK_SIGNAL in atom_types
    for atom in atoms:
        assert atom.source_id == "source_1"


def test_atomizer_fallback_atom_when_signal_is_sparse() -> None:
    atomizer = EvidenceAtomizer()
    atoms = atomizer.extract_atoms(
        case_id="case_2",
        lane_id="lane_1",
        source_id="source_2",
        source_atom_id="atom_2",
        title="",
        summary="",
        quote="",
        content=None,
    )
    # Empty text yields no atoms. Ensure non-empty content path emits at least one.
    atoms_with_text = atomizer.extract_atoms(
        case_id="case_2",
        lane_id="lane_1",
        source_id="source_3",
        source_atom_id="atom_3",
        title="x",
        summary="",
        quote="",
        content=None,
    )
    assert atoms == []
    assert len(atoms_with_text) >= 1
