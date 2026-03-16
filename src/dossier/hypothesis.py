from __future__ import annotations

import json
import logging
import re
from typing import Any, Protocol

from litellm import completion
from pydantic import ValidationError

from dossier.atomizer import EvidenceAtom
from dossier.config import Settings
from dossier.contracts import HypothesisCandidate

logger = logging.getLogger(__name__)


class HypothesisGenerator(Protocol):
    def generate(
        self,
        question: str,
        evidence_summary: str,
        typed_atoms: list[EvidenceAtom],
    ) -> list[HypothesisCandidate]:
        ...


def _extract_content_text(content: Any) -> str:
    if isinstance(content, list):
        text = "".join(
            str(item.get("text", ""))
            for item in content
            if isinstance(item, dict)
        )
    elif isinstance(content, str):
        text = content
    else:
        msg = f"Unsupported response content type: {type(content)!r}"
        raise ValueError(msg)

    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_hypothesis_payload(content: Any) -> list[dict[str, Any]]:
    text = _extract_content_text(content)
    if not text:
        msg = "Response did not contain JSON."
        raise ValueError(msg)

    candidates: Any | None = None
    for start_char, end_char in (("[", "]"), ("{", "}")):
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start == -1 or end == -1 or end <= start:
            continue
        try:
            parsed = json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            candidates = parsed
        elif isinstance(parsed, dict):
            for key in ("hypotheses", "items", "candidates"):
                value = parsed.get(key)
                if isinstance(value, list):
                    candidates = value
                    break
        if candidates is not None:
            break

    if not isinstance(candidates, list):
        msg = "Unable to parse hypothesis candidate list from response."
        raise ValueError(msg)
    return [item for item in candidates if isinstance(item, dict)]


class HypothesisBeamGenerator:
    def __init__(self, settings: Settings) -> None:
        self.model = settings.beam_model or settings.llm_model
        self.api_key = settings.llm_api_key
        self.beam_size = max(1, settings.beam_size)
        self.cross_domain_ratio = settings.cross_domain_ratio
        self.required_cross_domain = int(self.beam_size * self.cross_domain_ratio)
        self.max_atoms = max(1, settings.max_atoms_per_beam)
        self.fallback = DemoHypothesisBeamGenerator(settings)

    def generate(
        self,
        question: str,
        evidence_summary: str,
        typed_atoms: list[EvidenceAtom],
    ) -> list[HypothesisCandidate]:
        if len(typed_atoms) > self.max_atoms:
            logger.info(
                "Truncating %d atoms to %d for hypothesis beam generation.",
                len(typed_atoms),
                self.max_atoms,
            )
        atom_snapshot = [
            {
                "source_atom_id": atom.source_atom_id,
                "atom_type": atom.atom_type.value,
                "atom_value": atom.atom_value,
                "confidence": atom.confidence,
                "context": atom.context,
            }
            for atom in typed_atoms[: self.max_atoms]
        ]
        prompt = {
            "question": question,
            "evidence_summary": evidence_summary,
            "typed_atoms": atom_snapshot,
            "instructions": (
                "Generate a broad hypothesis beam grounded in the evidence. "
                "Each hypothesis must reference at least two source atom ids."
            ),
        }
        try:
            raw_response: Any = completion(
                model=self.model,
                api_key=self.api_key,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a hypothesis generation engine. "
                            f"Generate {self.beam_size} candidate hypotheses from the evidence. "
                            f"At least {self.required_cross_domain} hypotheses must be cross-domain analogies. "
                            "Each hypothesis must include: title, summary, source_atom_ids, "
                            "is_cross_domain, assumptions, confidence. "
                            "Return JSON only as an array."
                        ),
                    },
                    {"role": "user", "content": json.dumps(prompt)},
                ],
                temperature=0.4,
            )
            message_content = raw_response["choices"][0]["message"]["content"]
            parsed_items = _parse_hypothesis_payload(message_content)
            hypotheses: list[HypothesisCandidate] = []
            for item in parsed_items[: self.beam_size]:
                try:
                    hypotheses.append(HypothesisCandidate.model_validate(item))
                except ValidationError:
                    logger.warning(
                        "Skipping invalid hypothesis candidate: %s",
                        item.get("title", "unknown"),
                    )
            if not hypotheses:
                logger.warning(
                    "Hypothesis beam produced no valid candidates; falling back to demo.",
                )
                return self.fallback.generate(question, evidence_summary, typed_atoms)
            cross_domain_count = sum(1 for item in hypotheses if item.is_cross_domain)
            if cross_domain_count < self.required_cross_domain:
                logger.warning(
                    "Hypothesis beam produced %s cross-domain items (required: %s).",
                    cross_domain_count,
                    self.required_cross_domain,
                )
            return hypotheses
        except Exception:
            logger.exception("Hypothesis beam generation failed for model %r; falling back to demo", self.model)
            return self.fallback.generate(question, evidence_summary, typed_atoms)


class DemoHypothesisBeamGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _source_atom_pool(self, typed_atoms: list[EvidenceAtom]) -> list[str]:
        source_atom_ids = list(dict.fromkeys(atom.source_atom_id for atom in typed_atoms if atom.source_atom_id))
        if len(source_atom_ids) >= 3:
            return source_atom_ids
        if len(source_atom_ids) == 2:
            return [source_atom_ids[0], source_atom_ids[1], f"{source_atom_ids[1]}_alt"]
        if len(source_atom_ids) == 1:
            return [source_atom_ids[0], f"{source_atom_ids[0]}_alt", f"{source_atom_ids[0]}_alt_2"]
        return ["atom_demo_1", "atom_demo_2", "atom_demo_3"]

    def generate(
        self,
        question: str,
        evidence_summary: str,
        typed_atoms: list[EvidenceAtom],
    ) -> list[HypothesisCandidate]:
        del evidence_summary
        pool = self._source_atom_pool(typed_atoms)
        normalized_question = " ".join(question.split())
        return [
            HypothesisCandidate(
                title="Constraint-driven integration risk",
                summary=(
                    f"Integration outcomes for '{normalized_question}' depend on whether early execution "
                    "constraints amplify downstream risks faster than projected synergies."
                ),
                source_atom_ids=[pool[0], pool[1]],
                is_cross_domain=False,
                assumptions=[
                    "Retrieved atoms capture operational constraints, not only narrative claims.",
                    "Constraint effects scale non-linearly during integration phases.",
                ],
                confidence=0.64,
            ),
            HypothesisCandidate(
                title="Aerospace maintenance analogy for acquisition stability",
                summary=(
                    "The deal resembles safety-critical maintenance systems where small deferred fixes "
                    "cascade into reliability failures if monitoring loops are weak."
                ),
                source_atom_ids=[pool[1], pool[2]],
                is_cross_domain=True,
                assumptions=[
                    "Cross-domain transfer from reliability engineering is valid here.",
                    "Operational failure cascades map to post-acquisition integration debt.",
                ],
                confidence=0.58,
            ),
            HypothesisCandidate(
                title="Contradiction concentration predicts reversal risk",
                summary=(
                    "If contradiction-heavy atoms cluster around the same mechanism, final recommendations "
                    "should remain provisional pending one additional disconfirmation pass."
                ),
                source_atom_ids=[pool[0], pool[2]],
                is_cross_domain=False,
                assumptions=[
                    "Contradictions are independent signals rather than duplicate reporting.",
                ],
                confidence=0.61,
            ),
            HypothesisCandidate(
                title="Sparse evidence with high leverage",
                summary=(
                    "A small number of high-relevance atoms may dominate final ranking when they are "
                    "tied to falsifiable observables and explicit assumptions."
                ),
                source_atom_ids=[pool[2], pool[0]],
                is_cross_domain=False,
                assumptions=[
                    "High-relevance atoms can be distinguished from noisy weak signals.",
                ],
                confidence=0.55,
            ),
        ]


def build_hypothesis_generator(settings: Settings) -> HypothesisGenerator:
    provider = settings.llm_provider.lower()
    if provider == "demo":
        return DemoHypothesisBeamGenerator(settings)
    if provider == "litellm":
        return HypothesisBeamGenerator(settings)
    msg = f"Unsupported LLM_PROVIDER '{settings.llm_provider}'."
    raise ValueError(msg)
