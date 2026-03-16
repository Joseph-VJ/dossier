from __future__ import annotations

import json
from unittest.mock import patch

from dossier.config import Settings
from dossier.contracts import CounterfactualTest, HypothesisCandidate, Mechanism
from dossier.counterfactual import CounterfactualExpander, DemoCounterfactualExpander


def _hypothesis(index: int, confidence: float) -> HypothesisCandidate:
    return HypothesisCandidate(
        id=f"hyp_{index}",
        title=f"Hypothesis {index}",
        summary="Summary",
        source_atom_ids=["atom_1", "atom_2"],
        is_cross_domain=False,
        assumptions=["A1"],
        confidence=confidence,
    )


def _mechanism(index: int) -> Mechanism:
    return Mechanism(
        id=f"mechanism_{index}",
        name=f"Mechanism {index}",
        description="Description",
        steps=["Step 1", "Step 2"],
    )


def test_counterfactual_expander_parses_llm_response() -> None:
    expander = CounterfactualExpander(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="cf-model", LLM_API_KEY="test-key")
    )

    def fake_completion(**kwargs: object) -> dict[str, object]:
        assert kwargs["model"] == "cf-model"
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            [
                                {
                                    "assumption": "Assumption A",
                                    "challenge_prompt": "What if Assumption A is false?",
                                    "expected_failure_mode": "Mechanism confidence drops.",
                                }
                            ]
                        )
                    }
                }
            ]
        }

    with patch("dossier.counterfactual.completion", side_effect=fake_completion):
        tests = expander.expand(_hypothesis(1, 0.8), _mechanism(1))

    assert len(tests) == 1
    assert isinstance(tests[0], CounterfactualTest)


def test_counterfactual_expander_returns_empty_list_on_failure() -> None:
    expander = CounterfactualExpander(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="cf-model", LLM_API_KEY="test-key")
    )

    with patch("dossier.counterfactual.completion", side_effect=RuntimeError("LLM unavailable")):
        tests = expander.expand(_hypothesis(1, 0.8), _mechanism(1))

    assert tests == []


def test_demo_counterfactual_expander_returns_single_test() -> None:
    expander = DemoCounterfactualExpander(Settings())

    tests = expander.expand(_hypothesis(1, 0.8), _mechanism(1))

    assert len(tests) == 1
    assert isinstance(tests[0], CounterfactualTest)


def test_expand_top_k_respects_counterfactual_top_k() -> None:
    expander = CounterfactualExpander(
        Settings(
            LLM_PROVIDER="litellm",
            LLM_MODEL="cf-model",
            LLM_API_KEY="test-key",
            COUNTERFACTUAL_TOP_K=2,
        )
    )
    hypotheses = [_hypothesis(1, 0.9), _hypothesis(2, 0.7), _hypothesis(3, 0.2)]
    mechanisms = {hyp.id: _mechanism(idx + 1) for idx, hyp in enumerate(hypotheses)}

    def fake_completion(**kwargs: object) -> dict[str, object]:
        messages = kwargs["messages"]
        assert isinstance(messages, list)
        user_message = messages[1]
        assert isinstance(user_message, dict)
        payload = json.loads(str(user_message["content"]))
        hypothesis_title = payload["hypothesis"]["title"]
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            [
                                {
                                    "assumption": f"{hypothesis_title} assumption",
                                    "challenge_prompt": "What breaks first?",
                                    "expected_failure_mode": "Primary mechanism collapses.",
                                }
                            ]
                        )
                    }
                }
            ]
        }

    with patch("dossier.counterfactual.completion", side_effect=fake_completion):
        expanded = expander.expand_top_k(hypotheses, mechanisms)

    assert set(expanded.keys()) == {"hyp_1", "hyp_2"}
    assert "hyp_3" not in expanded


def test_counterfactual_expander_skips_invalid_keeps_valid() -> None:
    """Fix #1: partial validation failure must not discard valid items."""
    expander = CounterfactualExpander(
        Settings(LLM_PROVIDER="litellm", LLM_MODEL="cf-model", LLM_API_KEY="test-key")
    )

    payload = [
        {
            "assumption": "Valid assumption",
            "challenge_prompt": "What if valid?",
            "expected_failure_mode": "Mechanism degrades.",
        },
        {
            # Missing required field "assumption"
            "challenge_prompt": "Invalid item",
        },
        {
            "assumption": "Another valid",
            "challenge_prompt": "What if also valid?",
            "expected_failure_mode": "Score drops.",
        },
    ]

    def fake_completion(**_: object) -> dict[str, object]:
        return {"choices": [{"message": {"content": json.dumps(payload)}}]}

    with patch("dossier.counterfactual.completion", side_effect=fake_completion):
        tests = expander.expand(_hypothesis(1, 0.8), _mechanism(1))

    assert len(tests) == 2
    assert tests[0].assumption == "Valid assumption"
    assert tests[1].assumption == "Another valid"
