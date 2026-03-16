from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Protocol

from litellm import completion

from dossier.config import Settings
from dossier.contracts import HypothesisCandidate, Mechanism
from dossier.llm_utils import extract_content_text

logger = logging.getLogger(__name__)


class MechanismSynthesizerProtocol(Protocol):
    def synthesize(self, hypothesis: HypothesisCandidate, evidence_context: str) -> Mechanism:
        ...

    def synthesize_batch(
        self,
        hypotheses: list[HypothesisCandidate],
        evidence_context: str,
    ) -> list[Mechanism]:
        ...


def _parse_mechanism_payload(content: Any) -> dict[str, Any]:
    text = extract_content_text(content)
    if not text:
        msg = "Mechanism response was empty."
        raise ValueError(msg)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        msg = "Mechanism response did not contain a JSON object."
        raise ValueError(msg)

    parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        msg = "Mechanism response payload is not a JSON object."
        raise ValueError(msg)
    return parsed


def _unknown_mechanism() -> Mechanism:
    return Mechanism(
        name="Unknown",
        description="Mechanism synthesis failed; placeholder mechanism applied.",
        steps=[
            "Collect additional disconfirming evidence for this hypothesis.",
            "Retry mechanism synthesis with expanded context.",
        ],
    )


class MechanismSynthesizer:
    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model
        self.api_key = settings.llm_api_key
        self.fallback = DemoMechanismSynthesizer(settings)

    def synthesize(self, hypothesis: HypothesisCandidate, evidence_context: str) -> Mechanism:
        payload = {
            "hypothesis": hypothesis.model_dump(mode="json"),
            "evidence_context": evidence_context,
            "instructions": (
                "Construct an explicit mechanism for this hypothesis, including causal chain, "
                "required assumptions, failure points, and rival explanations. "
                "Return JSON with: name, description, steps."
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
                            "For this hypothesis, construct an explicit mechanism: causal chain, "
                            "required assumptions, failure points, rival explanations. "
                            "Return JSON only."
                        ),
                    },
                    {"role": "user", "content": json.dumps(payload)},
                ],
                temperature=0.2,
            )
            message_content = raw_response["choices"][0]["message"]["content"]
            mechanism_payload = _parse_mechanism_payload(message_content)
            return Mechanism.model_validate(mechanism_payload)
        except Exception:
            logger.warning(
                "Mechanism synthesis failed for hypothesis %s; returning placeholder mechanism.",
                hypothesis.id,
                exc_info=True,
            )
            return _unknown_mechanism()

    def synthesize_batch(
        self,
        hypotheses: list[HypothesisCandidate],
        evidence_context: str,
    ) -> list[Mechanism]:
        if not hypotheses:
            return []

        mechanisms: list[Mechanism | None] = [None] * len(hypotheses)
        max_workers = min(len(hypotheses), 8)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {
                executor.submit(self.synthesize, hypothesis, evidence_context): index
                for index, hypothesis in enumerate(hypotheses)
            }
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    mechanisms[index] = future.result()
                except Exception:
                    logger.warning(
                        "Mechanism batch execution failed at index %s; using placeholder mechanism.",
                        index,
                        exc_info=True,
                    )
                    mechanisms[index] = _unknown_mechanism()

        result = [item if item is not None else _unknown_mechanism() for item in mechanisms]
        if all(item.name == "Unknown" for item in result):
            logger.warning(
                "All %s mechanism syntheses failed; falling back to demo.",
                len(result),
            )
            return self.fallback.synthesize_batch(hypotheses, evidence_context)
        return result


class DemoMechanismSynthesizer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def synthesize(self, hypothesis: HypothesisCandidate, evidence_context: str) -> Mechanism:
        del evidence_context
        return Mechanism(
            name=f"Demo mechanism for {hypothesis.title}",
            description=(
                "Signals from supporting and disconfirming atoms are mapped into a simple "
                "causal chain with explicit failure points."
            ),
            steps=[
                "Map hypothesis assumptions to source atoms.",
                "Construct causal links between supporting and contradictory signals.",
                "Define the highest-leverage failure point.",
            ],
        )

    def synthesize_batch(
        self,
        hypotheses: list[HypothesisCandidate],
        evidence_context: str,
    ) -> list[Mechanism]:
        return [self.synthesize(hypothesis, evidence_context) for hypothesis in hypotheses]


def build_mechanism_synthesizer(settings: Settings) -> MechanismSynthesizerProtocol:
    provider = settings.llm_provider.lower()
    if provider == "demo":
        return DemoMechanismSynthesizer(settings)
    if provider == "litellm":
        return MechanismSynthesizer(settings)
    msg = f"Unsupported LLM_PROVIDER '{settings.llm_provider}'."
    raise ValueError(msg)

