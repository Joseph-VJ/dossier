from __future__ import annotations

import re

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.contracts import HypothesisCandidate, Mechanism


class SanityChecker:
    _GENERIC_TITLES = {"", "unknown", "tbd"}

    def check(
        self,
        hypothesis: HypothesisCandidate,
        mechanism: Mechanism,
        typed_atoms: list[EvidenceAtom],
    ) -> tuple[bool, list[str]]:
        reasons: list[str] = []

        hypothesis_atom_ids = [atom_id.strip() for atom_id in hypothesis.source_atom_ids if atom_id.strip()]
        if not hypothesis_atom_ids:
            reasons.append("Hypothesis must reference at least one source atom.")
        else:
            available_atom_ids = {atom.source_atom_id for atom in typed_atoms}
            if not any(atom_id in available_atom_ids for atom_id in hypothesis_atom_ids):
                reasons.append("Hypothesis source atom references are not present in typed atoms.")

        if not [step for step in mechanism.steps if step.strip()] or len(mechanism.steps) < 2:
            reasons.append("Mechanism must contain at least two steps.")

        if not [assumption for assumption in hypothesis.assumptions if assumption.strip()]:
            reasons.append("Hypothesis must include at least one assumption.")

        normalized_title = hypothesis.title.strip().lower()
        if normalized_title in self._GENERIC_TITLES:
            reasons.append("Hypothesis title must be specific and non-generic.")

        temporal_atoms = [
            atom
            for atom in typed_atoms
            if atom.atom_type == EvidenceAtomType.TEMPORAL_RELATION
            and atom.source_atom_id in hypothesis_atom_ids
        ]
        if temporal_atoms and self._has_temporal_inconsistency(temporal_atoms, mechanism.steps):
            reasons.append("Temporal ordering appears inconsistent with mechanism steps.")

        return (len(reasons) == 0, reasons)

    def _has_temporal_inconsistency(
        self,
        temporal_atoms: list[EvidenceAtom],
        mechanism_steps: list[str],
    ) -> bool:
        years = self._extract_years(temporal_atoms)
        if len(years) < 2:
            return False

        steps_text = " ".join(mechanism_steps).lower()
        positions: list[tuple[int, int]] = []
        for year in years:
            index = steps_text.find(str(year))
            if index == -1:
                continue
            positions.append((year, index))

        if len(positions) < 2:
            return False

        sorted_by_year = sorted(positions, key=lambda item: item[0])
        sorted_by_position = sorted(positions, key=lambda item: item[1])
        return [item[0] for item in sorted_by_year] != [item[0] for item in sorted_by_position]

    def _extract_years(self, temporal_atoms: list[EvidenceAtom]) -> list[int]:
        years: set[int] = set()
        for atom in temporal_atoms:
            text = f"{atom.atom_value} {atom.context}"
            for match in re.findall(r"\b(19\d{2}|20\d{2}|21\d{2})\b", text):
                years.add(int(match))
        return sorted(years)

