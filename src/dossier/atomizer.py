from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, Field

from dossier.contracts.models import new_id


class EvidenceAtomType(StrEnum):
    ENTITY = "entity"
    EVENT = "event"
    NUMERIC = "numeric"
    TEMPORAL_RELATION = "temporal_relation"
    CONTRADICTION = "contradiction"
    ABSENCE = "absence"
    WEAK_SIGNAL = "weak_signal"


class EvidenceAtom(BaseModel):
    id: str = Field(default_factory=lambda: new_id("eatom"))
    case_id: str
    lane_id: str
    source_id: str
    source_atom_id: str
    atom_type: EvidenceAtomType
    atom_value: str
    confidence: float = Field(ge=0.0, le=1.0)
    context: str = ""


class EvidenceAtomizer:
    _entity_pattern = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b")
    _numeric_pattern = re.compile(
        r"\b(?:\d{4}|\d+(?:\.\d+)?%|\$?\d+(?:,\d{3})*(?:\.\d+)?)\b"
    )
    _temporal_pattern = re.compile(
        r"\b(?:Q[1-4]|quarter|year|month|week|day|today|tomorrow|yesterday|"
        r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b",
        flags=re.IGNORECASE,
    )
    _event_verbs = (
        "acquired",
        "acquire",
        "launched",
        "launch",
        "filed",
        "announced",
        "reported",
        "signed",
        "raised",
        "declined",
        "grew",
        "merged",
    )
    _contradiction_markers = (
        "however",
        "but",
        "despite",
        "contradict",
        "conflict",
        "whereas",
    )
    _absence_markers = (
        "no evidence",
        "lack of",
        "without",
        "absent",
        "missing",
    )
    _weak_signal_markers = (
        "may",
        "might",
        "could",
        "suggests",
        "unclear",
        "rumor",
        "possible",
    )

    def extract_atoms(
        self,
        case_id: str,
        lane_id: str,
        source_id: str,
        source_atom_id: str,
        title: str,
        summary: str,
        quote: str,
        content: str | None,
    ) -> list[EvidenceAtom]:
        text = self._compose_text(title=title, summary=summary, quote=quote, content=content)
        sentences = self._sentences(text)

        atoms: list[EvidenceAtom] = []
        atoms.extend(
            self._regex_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.ENTITY,
                pattern=self._entity_pattern,
                text=text,
                confidence=0.58,
            )
        )
        atoms.extend(
            self._regex_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.NUMERIC,
                pattern=self._numeric_pattern,
                text=text,
                confidence=0.66,
            )
        )
        atoms.extend(
            self._regex_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.TEMPORAL_RELATION,
                pattern=self._temporal_pattern,
                text=text,
                confidence=0.54,
            )
        )

        atoms.extend(
            self._keyword_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.EVENT,
                keywords=self._event_verbs,
                sentences=sentences,
                confidence=0.62,
            )
        )
        atoms.extend(
            self._keyword_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.CONTRADICTION,
                keywords=self._contradiction_markers,
                sentences=sentences,
                confidence=0.60,
            )
        )
        atoms.extend(
            self._keyword_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.ABSENCE,
                keywords=self._absence_markers,
                sentences=sentences,
                confidence=0.59,
            )
        )
        atoms.extend(
            self._keyword_atoms(
                case_id=case_id,
                lane_id=lane_id,
                source_id=source_id,
                source_atom_id=source_atom_id,
                atom_type=EvidenceAtomType.WEAK_SIGNAL,
                keywords=self._weak_signal_markers,
                sentences=sentences,
                confidence=0.51,
            )
        )

        deduped: list[EvidenceAtom] = []
        seen: set[tuple[EvidenceAtomType, str]] = set()
        for atom in atoms:
            key = (atom.atom_type, atom.atom_value.lower())
            if key in seen:
                continue
            seen.add(key)
            deduped.append(atom)
            if len(deduped) >= 24:
                break

        if not deduped and text:
            deduped.append(
                EvidenceAtom(
                    case_id=case_id,
                    lane_id=lane_id,
                    source_id=source_id,
                    source_atom_id=source_atom_id,
                    atom_type=EvidenceAtomType.WEAK_SIGNAL,
                    atom_value="Limited structured signal extracted",
                    confidence=0.35,
                    context=text[:180],
                )
            )

        return deduped

    def _compose_text(self, title: str, summary: str, quote: str, content: str | None) -> str:
        parts = [title, summary, quote, content or ""]
        return " ".join(part.strip() for part in parts if part.strip())

    def _sentences(self, text: str) -> list[str]:
        return [segment.strip() for segment in re.split(r"[.!?]+", text) if segment.strip()]

    def _regex_atoms(
        self,
        case_id: str,
        lane_id: str,
        source_id: str,
        source_atom_id: str,
        atom_type: EvidenceAtomType,
        pattern: re.Pattern[str],
        text: str,
        confidence: float,
    ) -> list[EvidenceAtom]:
        atoms: list[EvidenceAtom] = []
        for match in pattern.finditer(text):
            value = match.group(0).strip()
            if len(value) < 2:
                continue
            atoms.append(
                EvidenceAtom(
                    case_id=case_id,
                    lane_id=lane_id,
                    source_id=source_id,
                    source_atom_id=source_atom_id,
                    atom_type=atom_type,
                    atom_value=value[:120],
                    confidence=confidence,
                    context=text[max(0, match.start() - 60) : match.end() + 60][:200],
                )
            )
        return atoms

    def _keyword_atoms(
        self,
        case_id: str,
        lane_id: str,
        source_id: str,
        source_atom_id: str,
        atom_type: EvidenceAtomType,
        keywords: tuple[str, ...],
        sentences: list[str],
        confidence: float,
    ) -> list[EvidenceAtom]:
        atoms: list[EvidenceAtom] = []
        for sentence in sentences:
            lowered = sentence.lower()
            for keyword in keywords:
                if keyword in lowered:
                    atoms.append(
                        EvidenceAtom(
                            case_id=case_id,
                            lane_id=lane_id,
                            source_id=source_id,
                            source_atom_id=source_atom_id,
                            atom_type=atom_type,
                            atom_value=keyword,
                            confidence=confidence,
                            context=sentence[:200],
                        )
                    )
                    break
        return atoms
