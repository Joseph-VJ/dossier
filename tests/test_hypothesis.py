from __future__ import annotations

import json
from unittest.mock import patch

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.config import Settings
from dossier.hypothesis import (
    DemoHypothesisBeamGenerator,
    HypothesisBeamGenerator,
    build_hypothesis_generator,
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
            context="Acme Corp supply chain signal",
        ),
        EvidenceAtom(
            case_id="case_1",
            lane_id="lane_2",
            source_id="source_2",
            source_atom_id="atom_2",
            atom_type=EvidenceAtomType.CONTRADICTION,
            atom_value="however",
            confidence=0.7,
            context="However, risks are rising",
        ),
    ]


def test_demo_hypothesis_generator_returns_expected_count_with_cross_domain() -> None:
    generator = DemoHypothesisBeamGenerator(Settings(BEAM_SIZE=16, CROSS_DOMAIN_RATIO=0.2))

    hypotheses = generator.generate(
        question="Should Acme acquire Beta?",
        evidence_summary="Acme and Beta have mixed synergy and risk signals.",
        typed_atoms=_atoms(),
    )

    assert len(hypotheses) == 4
    assert sum(1 for item in hypotheses if item.is_cross_domain) >= 1


def test_hypothesis_generator_parses_llm_json_response() -> None:
    settings = Settings(
        LLM_PROVIDER="litellm",
        LLM_MODEL="main-model",
        LLM_API_KEY="test-key",
        BEAM_MODEL="beam-model",
        BEAM_SIZE=4,
    )
    generator = HypothesisBeamGenerator(settings)

    def fake_completion(**kwargs: object) -> dict[str, object]:
        assert kwargs["model"] == "beam-model"
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            [
                                {
                                    "title": "Hypothesis A",
                                    "summary": "A structured synthesis candidate.",
                                    "source_atom_ids": ["atom_1", "atom_2"],
                                    "is_cross_domain": False,
                                    "assumptions": ["Signals are representative."],
                                    "confidence": 0.66,
                                },
                                {
                                    "title": "Hypothesis B",
                                    "summary": "Cross-domain analogy from aerospace maintenance.",
                                    "source_atom_ids": ["atom_2", "atom_3"],
                                    "is_cross_domain": True,
                                    "assumptions": ["Analogical transfer is valid."],
                                    "confidence": 0.58,
                                },
                            ]
                        )
                    }
                }
            ]
        }

    with patch("dossier.hypothesis.completion", side_effect=fake_completion):
        hypotheses = generator.generate(
            question="Should Acme acquire Beta?",
            evidence_summary="Evidence summary text.",
            typed_atoms=_atoms(),
        )

    assert len(hypotheses) == 2
    assert hypotheses[0].title == "Hypothesis A"
    assert hypotheses[0].id.startswith("hyp_")


def test_hypothesis_generator_truncates_to_beam_size() -> None:
    settings = Settings(
        LLM_PROVIDER="litellm",
        LLM_MODEL="main-model",
        LLM_API_KEY="test-key",
        BEAM_SIZE=3,
    )
    generator = HypothesisBeamGenerator(settings)

    payload = [
        {
            "title": f"Hypothesis {idx}",
            "summary": "Candidate",
            "source_atom_ids": ["atom_1", "atom_2"],
            "is_cross_domain": idx == 0,
            "assumptions": ["A1"],
            "confidence": 0.5,
        }
        for idx in range(5)
    ]

    def fake_completion(**_: object) -> dict[str, object]:
        return {"choices": [{"message": {"content": json.dumps(payload)}}]}

    with patch("dossier.hypothesis.completion", side_effect=fake_completion):
        hypotheses = generator.generate(
            question="Question?",
            evidence_summary="Summary",
            typed_atoms=_atoms(),
        )

    assert len(hypotheses) == 3


def test_build_hypothesis_generator_uses_demo_when_llm_provider_is_demo() -> None:
    generator = build_hypothesis_generator(Settings(LLM_PROVIDER="demo"))
    assert isinstance(generator, DemoHypothesisBeamGenerator)


def test_hypothesis_generator_skips_invalid_keeps_valid() -> None:
    """Fix #1: partial validation failure must not discard valid candidates."""
    settings = Settings(
        LLM_PROVIDER="litellm",
        LLM_MODEL="m",
        LLM_API_KEY="k",
        BEAM_SIZE=4,
    )
    generator = HypothesisBeamGenerator(settings)

    payload = [
        {
            "title": "Valid",
            "summary": "Good candidate.",
            "source_atom_ids": ["atom_1", "atom_2"],
            "is_cross_domain": False,
            "assumptions": ["A"],
            "confidence": 0.7,
        },
        {
            "title": "Invalid – only one source atom",
            "summary": "Bad candidate.",
            "source_atom_ids": ["atom_1"],  # min_length=2 violated
            "is_cross_domain": False,
            "assumptions": ["A"],
            "confidence": 0.5,
        },
        {
            "title": "Also valid",
            "summary": "Another good candidate.",
            "source_atom_ids": ["atom_2", "atom_3"],
            "is_cross_domain": True,
            "assumptions": ["B"],
            "confidence": 0.6,
        },
    ]

    def fake_completion(**_: object) -> dict[str, object]:
        return {"choices": [{"message": {"content": json.dumps(payload)}}]}

    with patch("dossier.hypothesis.completion", side_effect=fake_completion):
        hypotheses = generator.generate(
            question="Q?",
            evidence_summary="S",
            typed_atoms=_atoms(),
        )

    assert len(hypotheses) == 2
    assert hypotheses[0].title == "Valid"
    assert hypotheses[1].title == "Also valid"


def test_hypothesis_generator_falls_back_on_empty_llm_response() -> None:
    """Fix #2: empty LLM array must trigger demo fallback."""
    settings = Settings(
        LLM_PROVIDER="litellm",
        LLM_MODEL="m",
        LLM_API_KEY="k",
        BEAM_SIZE=4,
    )
    generator = HypothesisBeamGenerator(settings)

    def fake_completion(**_: object) -> dict[str, object]:
        return {"choices": [{"message": {"content": "[]"}}]}

    with patch("dossier.hypothesis.completion", side_effect=fake_completion):
        hypotheses = generator.generate(
            question="Q?",
            evidence_summary="S",
            typed_atoms=_atoms(),
        )

    # Should get demo fallback results, not empty list
    assert len(hypotheses) > 0
    assert hypotheses[0].title == "Constraint-driven integration risk"


def test_hypothesis_generator_falls_back_when_all_invalid() -> None:
    """Fix #2 extended: all invalid candidates must trigger demo fallback."""
    settings = Settings(
        LLM_PROVIDER="litellm",
        LLM_MODEL="m",
        LLM_API_KEY="k",
        BEAM_SIZE=4,
    )
    generator = HypothesisBeamGenerator(settings)

    payload = [
        {
            "title": "Bad",
            "summary": "Only one atom.",
            "source_atom_ids": ["atom_1"],
            "is_cross_domain": False,
            "assumptions": [],
            "confidence": 0.5,
        },
    ]

    def fake_completion(**_: object) -> dict[str, object]:
        return {"choices": [{"message": {"content": json.dumps(payload)}}]}

    with patch("dossier.hypothesis.completion", side_effect=fake_completion):
        hypotheses = generator.generate(
            question="Q?",
            evidence_summary="S",
            typed_atoms=_atoms(),
        )

    assert len(hypotheses) > 0
    assert hypotheses[0].title == "Constraint-driven integration risk"
