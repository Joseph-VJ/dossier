from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dossier.contracts import (  # noqa: E402
    Contradiction,
    CounterfactualTest,
    Hypothesis,
    Mechanism,
    NoveltyScore,
    Prediction,
    ProofTree,
    SourceOriginCluster,
)


def main() -> int:
    out_dir = ROOT / "contracts"
    out_dir.mkdir(parents=True, exist_ok=True)

    registry = {
        "SOURCE_ORIGIN_CLUSTER": SourceOriginCluster,
        "CONTRADICTION": Contradiction,
        "HYPOTHESIS": Hypothesis,
        "MECHANISM": Mechanism,
        "PROOF_TREE": ProofTree,
        "PREDICTION": Prediction,
        "NOVELTY_SCORE": NoveltyScore,
        "COUNTERFACTUAL_TEST": CounterfactualTest,
    }

    for name, model in registry.items():
        schema_path = out_dir / f"{name.lower()}.schema.json"
        schema_path.write_text(
            json.dumps(model.model_json_schema(), indent=2, sort_keys=True),
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
