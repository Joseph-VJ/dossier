from __future__ import annotations

import json
import logging
from typing import Any, Protocol

from litellm import completion
from pydantic import ValidationError

from dossier.config import Settings
from dossier.contracts import CounterfactualTest, HypothesisCandidate, Mechanism
from dossier.llm_utils import extract_content_text

logger = logging.getLogger(__name__)


class CounterfactualExpanderProtocol(Protocol):
    def expand(
        self,
        hypothesis: HypothesisCandidate,
        mechanism: Mechanism,
    ) -> list[CounterfactualTest]:
        ...

    def expand_top_k(
        self,
        hypotheses: list[HypothesisCandidate],
        mechanisms_by_id: dict[str, Mechanism],
    ) -> dict[str, list[CounterfactualTest]]:
        ...


def _parse_counterfactual_payload(content: Any) -> list[dict[str, Any]]:
    text = extract_content_text(content)
    if not text:
        msg = "Counterfactual response was empty."
        raise ValueError(msg)

    parsed: Any | None = None
    for start_char, end_char in (("[", "]"), ("{", "}")):
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start == -1 or end == -1 or end <= start:
            continue
        try:
            candidate = json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            continue
        parsed = candidate
        break

    if parsed is None:
        msg = "Unable to parse counterfactual JSON payload."
        raise ValueError(msg)

    if isinstance(parsed, list):
        items = parsed
    elif isinstance(parsed, dict):
        items = (
            parsed.get("counterfactual_tests")
            or parsed.get("tests")
            or parsed.get("items")
            or []
        )
    else:
        items = []

    if not isinstance(items, list):
        msg = "Counterfactual payload is not a list."
        raise ValueError(msg)

    return [item for item in items if isinstance(item, dict)]


class CounterfactualExpander:
    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model
        self.api_key = settings.llm_api_key
        self.top_k = settings.counterfactual_top_k

    def expand(
        self,
        hypothesis: HypothesisCandidate,
        mechanism: Mechanism,
    ) -> list[CounterfactualTest]:
        payload = {
            "hypothesis": hypothesis.model_dump(mode="json"),
            "mechanism": mechanism.model_dump(mode="json"),
            "instructions": (
                "Generate counterfactual tests using what-if variants, premise removals, "
                "and parameter perturbations. Return JSON array only."
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
                            "For this hypothesis and mechanism, generate counterfactual tests: "
                            "what-if variants, premise removals, parameter perturbations. "
                            "Return JSON only."
                        ),
                    },
                    {"role": "user", "content": json.dumps(payload)},
                ],
                temperature=0.3,
            )
            message_content = raw_response["choices"][0]["message"]["content"]
            parsed_items = _parse_counterfactual_payload(message_content)
            tests: list[CounterfactualTest] = []
            for item in parsed_items:
                try:
                    tests.append(CounterfactualTest.model_validate(item))
                except ValidationError:
                    logger.warning(
                        "Skipping invalid counterfactual test for hypothesis %s.",
                        hypothesis.id,
                    )
            return tests
        except Exception:
            logger.warning(
                "Counterfactual expansion failed for hypothesis %s; returning empty list.",
                hypothesis.id,
                exc_info=True,
            )
            return []

    def expand_top_k(
        self,
        hypotheses: list[HypothesisCandidate],
        mechanisms_by_id: dict[str, Mechanism],
    ) -> dict[str, list[CounterfactualTest]]:
        ranked = sorted(
            enumerate(hypotheses),
            key=lambda item: (-item[1].confidence, item[0]),
        )
        selected = ranked[: self.top_k]
        expanded: dict[str, list[CounterfactualTest]] = {}
        for _, hypothesis in selected:
            mechanism = mechanisms_by_id.get(hypothesis.id)
            expanded[hypothesis.id] = self.expand(hypothesis, mechanism) if mechanism else []
        return expanded


class DemoCounterfactualExpander:
    def __init__(self, settings: Settings) -> None:
        self.top_k = settings.counterfactual_top_k

    def expand(
        self,
        hypothesis: HypothesisCandidate,
        mechanism: Mechanism,
    ) -> list[CounterfactualTest]:
        del mechanism
        return [
            CounterfactualTest(
                assumption=f"{hypothesis.title} core assumption remains stable.",
                challenge_prompt="What if the primary assumption is removed?",
                expected_failure_mode="The mechanism loses predictive power and ranking confidence declines.",
            )
        ]

    def expand_top_k(
        self,
        hypotheses: list[HypothesisCandidate],
        mechanisms_by_id: dict[str, Mechanism],
    ) -> dict[str, list[CounterfactualTest]]:
        ranked = sorted(
            enumerate(hypotheses),
            key=lambda item: (-item[1].confidence, item[0]),
        )
        selected = ranked[: self.top_k]
        expanded: dict[str, list[CounterfactualTest]] = {}
        for _, hypothesis in selected:
            mechanism = mechanisms_by_id.get(hypothesis.id)
            expanded[hypothesis.id] = self.expand(hypothesis, mechanism) if mechanism else []
        return expanded


def build_counterfactual_expander(settings: Settings) -> CounterfactualExpanderProtocol:
    provider = settings.llm_provider.lower()
    if provider == "demo":
        return DemoCounterfactualExpander(settings)
    if provider == "litellm":
        return CounterfactualExpander(settings)
    msg = f"Unsupported LLM_PROVIDER '{settings.llm_provider}'."
    raise ValueError(msg)

