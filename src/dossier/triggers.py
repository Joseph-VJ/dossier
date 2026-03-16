from __future__ import annotations

import re
from collections import defaultdict
from typing import Protocol

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.config import Settings
from dossier.contracts import EvidencePacket, InvestigationPlan, TriggerResult, TriggerType

_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "was",
    "were",
    "with",
}


def _normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def _keywords(value: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", value.lower())
    return {
        token
        for token in tokens
        if len(token) >= 3 and token not in _STOP_WORDS
    }


def _bounded(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


class TriggerDetector:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def detect(
        self,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        typed_atoms: list[EvidenceAtom],
        graph_nodes: list[dict[str, object]],
        graph_edges: list[dict[str, object]],
        case_memory_notes: list[str],
    ) -> list[TriggerResult]:
        del graph_nodes, graph_edges
        triggers = [
            *self._detect_cross_lane_convergence(typed_atoms),
            *self._detect_contradiction_density(typed_atoms),
            *self._detect_unexplained_event(typed_atoms),
            *self._detect_meaningful_absence(plan, packets),
            *self._detect_weak_signal_alignment(typed_atoms),
            *self._detect_sparse_retrieval(packets),
            *self._detect_uncertainty_spike(typed_atoms),
            *self._detect_analogical_match(plan, typed_atoms, case_memory_notes),
        ]
        return [
            trigger
            for trigger in triggers
            if trigger.confidence >= self.settings.trigger_min_confidence
        ]

    def _detect_cross_lane_convergence(self, typed_atoms: list[EvidenceAtom]) -> list[TriggerResult]:
        entity_lanes: dict[str, set[str]] = defaultdict(set)
        entity_ids: dict[str, list[str]] = defaultdict(list)
        for atom in typed_atoms:
            if atom.atom_type is not EvidenceAtomType.ENTITY:
                continue
            normalized = _normalize_text(atom.atom_value)
            entity_lanes[normalized].add(atom.lane_id)
            entity_ids[normalized].append(atom.id)

        overlapping = [
            entity for entity, lanes in entity_lanes.items()
            if len(lanes) >= 2
        ]
        if len(overlapping) < 2:
            return []

        supporting_evidence = [
            atom_id
            for entity in overlapping[:4]
            for atom_id in entity_ids[entity][:2]
        ]
        lane_count = max(len(entity_lanes[entity]) for entity in overlapping)
        confidence = _bounded(0.45 + 0.15 * len(overlapping) + 0.05 * lane_count)
        return [
            TriggerResult(
                trigger_type=TriggerType.CROSS_LANE_CONVERGENCE,
                description=(
                    f"{len(overlapping)} shared entities recur across {lane_count} lanes, "
                    "suggesting a convergent cross-lane pattern."
                ),
                confidence=confidence,
                supporting_evidence=supporting_evidence,
            )
        ]

    def _detect_contradiction_density(self, typed_atoms: list[EvidenceAtom]) -> list[TriggerResult]:
        if not typed_atoms:
            return []
        contradictions = [atom for atom in typed_atoms if atom.atom_type is EvidenceAtomType.CONTRADICTION]
        contradiction_ratio = len(contradictions) / len(typed_atoms)
        if len(contradictions) < 3 and contradiction_ratio <= 0.2:
            return []
        confidence = _bounded(0.4 + contradiction_ratio + min(0.2, len(contradictions) * 0.05))
        return [
            TriggerResult(
                trigger_type=TriggerType.CONTRADICTION_DENSITY,
                description=(
                    f"{len(contradictions)} contradiction atoms account for {contradiction_ratio:.0%} "
                    "of extracted atoms."
                ),
                confidence=confidence,
                supporting_evidence=[atom.id for atom in contradictions[:6]],
            )
        ]

    def _detect_unexplained_event(self, typed_atoms: list[EvidenceAtom]) -> list[TriggerResult]:
        atoms_by_source_atom: dict[str, list[EvidenceAtom]] = defaultdict(list)
        for atom in typed_atoms:
            atoms_by_source_atom[atom.source_atom_id].append(atom)

        unsupported_event_ids: list[str] = []
        for atoms in atoms_by_source_atom.values():
            has_support = any(
                atom.atom_type in (EvidenceAtomType.NUMERIC, EvidenceAtomType.TEMPORAL_RELATION)
                for atom in atoms
            )
            if has_support:
                continue
            unsupported_event_ids.extend(
                atom.id for atom in atoms if atom.atom_type is EvidenceAtomType.EVENT
            )

        if not unsupported_event_ids:
            return []
        confidence = _bounded(0.45 + min(0.4, len(unsupported_event_ids) * 0.1))
        return [
            TriggerResult(
                trigger_type=TriggerType.UNEXPLAINED_EVENT,
                description=(
                    f"{len(unsupported_event_ids)} event atoms lack numeric or temporal context in their source packet."
                ),
                confidence=confidence,
                supporting_evidence=unsupported_event_ids[:6],
            )
        ]

    def _detect_meaningful_absence(
        self,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
    ) -> list[TriggerResult]:
        populated_lanes = {packet.lane_id for packet in packets}
        missing_lanes = [lane for lane in plan.lanes if lane.id not in populated_lanes]
        if not missing_lanes:
            return []
        confidence = _bounded(0.5 + min(0.3, len(missing_lanes) * 0.1))
        return [
            TriggerResult(
                trigger_type=TriggerType.MEANINGFUL_ABSENCE,
                description=f"{len(missing_lanes)} planned lanes returned no packets.",
                confidence=confidence,
                supporting_evidence=[lane.id for lane in missing_lanes],
            )
        ]

    def _detect_weak_signal_alignment(self, typed_atoms: list[EvidenceAtom]) -> list[TriggerResult]:
        weak_atoms = [atom for atom in typed_atoms if atom.atom_type is EvidenceAtomType.WEAK_SIGNAL]
        aligned_ids: set[str] = set()
        max_overlap = 0
        for index, left in enumerate(weak_atoms):
            left_words = _keywords(left.context)
            for right in weak_atoms[index + 1 :]:
                if left.source_atom_id == right.source_atom_id:
                    continue
                shared_words = left_words & _keywords(right.context)
                if len(shared_words) >= 2:
                    aligned_ids.update({left.id, right.id})
                    max_overlap = max(max_overlap, len(shared_words))
        if len(aligned_ids) < 2:
            return []
        confidence = _bounded(0.45 + min(0.3, len(aligned_ids) * 0.05) + min(0.2, max_overlap * 0.05))
        return [
            TriggerResult(
                trigger_type=TriggerType.WEAK_SIGNAL_ALIGNMENT,
                description=(
                    f"{len(aligned_ids)} weak-signal atoms share overlapping language across different sources."
                ),
                confidence=confidence,
                supporting_evidence=sorted(aligned_ids)[:6],
            )
        ]

    def _detect_sparse_retrieval(self, packets: list[EvidencePacket]) -> list[TriggerResult]:
        if len(packets) >= 4:
            return []
        confidence = _bounded(0.5 + ((4 - len(packets)) / 4) * 0.4)
        return [
            TriggerResult(
                trigger_type=TriggerType.SPARSE_RETRIEVAL,
                description=f"Only {len(packets)} packets were retrieved across all lanes.",
                confidence=confidence,
                supporting_evidence=[packet.id for packet in packets],
            )
        ]

    def _detect_uncertainty_spike(self, typed_atoms: list[EvidenceAtom]) -> list[TriggerResult]:
        if not typed_atoms:
            return []
        uncertainty_atoms = [
            atom
            for atom in typed_atoms
            if atom.atom_type in (
                EvidenceAtomType.WEAK_SIGNAL,
                EvidenceAtomType.CONTRADICTION,
                EvidenceAtomType.ABSENCE,
            )
        ]
        uncertainty_ratio = len(uncertainty_atoms) / len(typed_atoms)
        if len(uncertainty_atoms) < 4 or uncertainty_ratio < 0.35:
            return []
        confidence = _bounded(0.45 + min(0.35, uncertainty_ratio) + min(0.15, len(uncertainty_atoms) * 0.02))
        return [
            TriggerResult(
                trigger_type=TriggerType.UNCERTAINTY_SPIKE,
                description=(
                    f"Uncertainty atoms represent {uncertainty_ratio:.0%} of extracted atoms "
                    f"({len(uncertainty_atoms)} total)."
                ),
                confidence=confidence,
                supporting_evidence=[atom.id for atom in uncertainty_atoms[:6]],
            )
        ]

    def _detect_analogical_match(
        self,
        plan: InvestigationPlan,
        typed_atoms: list[EvidenceAtom],
        case_memory_notes: list[str],
    ) -> list[TriggerResult]:
        if not case_memory_notes or case_memory_notes == ["No prior case memory found."]:
            return []

        current_keywords = _keywords(plan.objective)
        entity_atoms = [atom for atom in typed_atoms if atom.atom_type is EvidenceAtomType.ENTITY]
        for atom in entity_atoms:
            current_keywords.update(_keywords(atom.atom_value))

        if not current_keywords:
            return []

        best_overlap: set[str] = set()
        best_note = ""
        for note in case_memory_notes:
            note_keywords = _keywords(note)
            overlap = current_keywords & note_keywords
            if len(overlap) > len(best_overlap):
                best_overlap = overlap
                best_note = note
        if len(best_overlap) < 2:
            return []

        supporting_atoms = [
            atom.id
            for atom in entity_atoms
            if _keywords(atom.atom_value) & best_overlap
        ]
        confidence = _bounded(0.45 + min(0.35, len(best_overlap) * 0.1))
        return [
            TriggerResult(
                trigger_type=TriggerType.ANALOGICAL_MATCH,
                description=(
                    f"Current case overlaps prior memory note '{best_note[:80]}' on "
                    f"{len(best_overlap)} keywords."
                ),
                confidence=confidence,
                supporting_evidence=supporting_atoms[:6] or sorted(best_overlap),
            )
        ]


class DemoTriggerDetector:
    def detect(
        self,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        typed_atoms: list[EvidenceAtom],
        graph_nodes: list[dict[str, object]],
        graph_edges: list[dict[str, object]],
        case_memory_notes: list[str],
    ) -> list[TriggerResult]:
        del plan, typed_atoms, graph_nodes, graph_edges, case_memory_notes
        supporting_evidence = [packet.id for packet in packets[:2]]
        return [
            TriggerResult(
                trigger_type=TriggerType.CROSS_LANE_CONVERGENCE,
                description="Demo trigger path assumes cross-lane convergence is worth deep synthesis.",
                confidence=0.7,
                supporting_evidence=supporting_evidence,
            )
        ]


class TriggerDetectorProtocol(Protocol):
    def detect(
        self,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        typed_atoms: list[EvidenceAtom],
        graph_nodes: list[dict[str, object]],
        graph_edges: list[dict[str, object]],
        case_memory_notes: list[str],
    ) -> list[TriggerResult]:
        ...


def build_trigger_detector(settings: Settings) -> TriggerDetectorProtocol:
    if settings.llm_provider.lower() == "demo":
        return DemoTriggerDetector()
    return TriggerDetector(settings)
