from __future__ import annotations

import json
from unittest.mock import patch

from dossier.config import Settings
from dossier.contracts import HypothesisCandidate
from dossier.mechanism import DemoMechanismSynthesizer, MechanismSynthesizer


def _candidate(index: int = 1) -> HypothesisCandidate:
    return HypothesisCandidate(
        id=f"hyp_{index}",
        title=f"Hypothesis {index}",
        summary="Candidate summary",
        source_atom_ids=["atom_1", "atom_2"],
        is_cross_domain=False,
        assumptions=["Assumption A"],
        confidence=0.6,
    )


def test_mechanism_synthesizer_parses_llm_response() -> None:
    synthesizer = MechanismSynthesizer(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="mechanism-model", LLM_API_KEY="test-key")
    )

    def fake_completion(**kwargs: object) -> dict[str, object]:
        assert kwargs["model"] == "mechanism-model"
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "name": "Risk propagation chain",
                                "description": "Contradiction signals propagate into execution risk.",
                                "steps": [
                                    "Detect contradictory atoms.",
                                    "Map contradictions to process bottlenecks.",
                                ],
                            }
                        )
                    }
                }
            ]
        }

    with patch("dossier.mechanism.completion", side_effect=fake_completion):
        mechanism = synthesizer.synthesize(_candidate(), "Evidence context")

    assert mechanism.name == "Risk propagation chain"
    assert mechanism.description
    assert len(mechanism.steps) >= 2


def test_mechanism_synthesizer_falls_back_to_placeholder_on_failure() -> None:
    synthesizer = MechanismSynthesizer(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="mechanism-model", LLM_API_KEY="test-key")
    )

    with patch("dossier.mechanism.completion", side_effect=RuntimeError("upstream failure")):
        mechanism = synthesizer.synthesize(_candidate(), "Evidence context")

    assert mechanism.name == "Unknown"
    assert len(mechanism.steps) >= 2


def test_mechanism_synthesizer_batch_preserves_input_order() -> None:
    synthesizer = MechanismSynthesizer(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="mechanism-model", LLM_API_KEY="test-key")
    )

    def fake_completion(**kwargs: object) -> dict[str, object]:
        messages = kwargs["messages"]
        assert isinstance(messages, list)
        user_msg = messages[1]
        assert isinstance(user_msg, dict)
        content = user_msg["content"]
        assert isinstance(content, str)
        payload = json.loads(content)
        title = payload["hypothesis"]["title"]
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "name": f"Mechanism for {title}",
                                "description": "desc",
                                "steps": ["step 1", "step 2"],
                            }
                        )
                    }
                }
            ]
        }

    with patch("dossier.mechanism.completion", side_effect=fake_completion):
        mechanisms = synthesizer.synthesize_batch([_candidate(1), _candidate(2)], "Evidence context")

    assert mechanisms[0].name == "Mechanism for Hypothesis 1"
    assert mechanisms[1].name == "Mechanism for Hypothesis 2"


def test_demo_mechanism_synthesizer_returns_structured_mechanism() -> None:
    synthesizer = DemoMechanismSynthesizer(Settings())

    mechanism = synthesizer.synthesize(_candidate(), "Evidence context")

    assert mechanism.name
    assert mechanism.description
    assert len(mechanism.steps) >= 2


def test_mechanism_batch_falls_back_to_demo_when_all_fail() -> None:
    """Fix #3: batch-level fallback to demo when all LLM calls fail."""
    synthesizer = MechanismSynthesizer(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="mechanism-model", LLM_API_KEY="test-key")
    )

    with patch("dossier.mechanism.completion", side_effect=RuntimeError("all fail")):
        mechanisms = synthesizer.synthesize_batch(
            [_candidate(1), _candidate(2)], "Evidence context"
        )

    assert len(mechanisms) == 2
    assert all(m.name != "Unknown" for m in mechanisms)
    assert all("Demo mechanism" in m.name for m in mechanisms)
