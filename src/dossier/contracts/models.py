from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


def utc_now() -> datetime:
    return datetime.now(UTC)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class InsightClass(StrEnum):
    NOVEL_DEDUCTION = "Novel Deduction"
    SPECULATIVE_MECHANISM = "Speculative Mechanism"
    EXPLORATORY_PREDICTION = "Exploratory Prediction"


class ResearchLane(BaseModel):
    id: str = Field(default_factory=lambda: new_id("lane"))
    name: str
    query: str
    goal: str


class InvestigationPlan(BaseModel):
    objective: str
    novelty_target: str
    lanes: list[ResearchLane]
    case_memory_notes: list[str] = Field(default_factory=list)


class SourceAtom(BaseModel):
    id: str = Field(default_factory=lambda: new_id("atom"))
    source_id: str
    lane_id: str
    title: str
    url: str
    quote: str
    summary: str


class SearchHit(BaseModel):
    title: str
    url: str
    snippet: str
    content: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvidencePacket(BaseModel):
    id: str = Field(default_factory=lambda: new_id("evidence"))
    case_id: str
    lane_id: str
    source_atom: SourceAtom
    summary: str
    quote: str
    relevance: float = Field(ge=0.0, le=1.0)
    extracted_at: datetime = Field(default_factory=utc_now)


class SourceOriginCluster(BaseModel):
    id: str = Field(default_factory=lambda: new_id("origin"))
    label: str
    member_source_ids: list[str]
    independence_note: str


class Contradiction(BaseModel):
    id: str = Field(default_factory=lambda: new_id("contradiction"))
    left_source_id: str
    right_source_id: str
    description: str
    severity: float = Field(ge=0.0, le=1.0)


class Hypothesis(BaseModel):
    id: str = Field(default_factory=lambda: new_id("hypothesis"))
    title: str
    summary: str
    source_atom_ids: list[str]
    assumptions: list[str]


class Mechanism(BaseModel):
    id: str = Field(default_factory=lambda: new_id("mechanism"))
    name: str
    description: str
    steps: list[str]


class ProofTree(BaseModel):
    id: str = Field(default_factory=lambda: new_id("proof"))
    conclusion: str
    premises: list[str]
    reasoning_notes: list[str]


class Prediction(BaseModel):
    id: str = Field(default_factory=lambda: new_id("prediction"))
    observable: str
    expected_signal: str
    time_horizon: str
    confidence: float = Field(ge=0.0, le=1.0)


class CounterfactualTest(BaseModel):
    id: str = Field(default_factory=lambda: new_id("counterfactual"))
    assumption: str
    challenge_prompt: str
    expected_failure_mode: str


class TriggerType(StrEnum):
    CROSS_LANE_CONVERGENCE = "Cross-lane convergence"
    CONTRADICTION_DENSITY = "Contradiction density"
    UNEXPLAINED_EVENT = "Unexplained event"
    MEANINGFUL_ABSENCE = "Meaningful absence"
    WEAK_SIGNAL_ALIGNMENT = "Weak-signal alignment"
    SPARSE_RETRIEVAL = "Sparse retrieval"
    UNCERTAINTY_SPIKE = "Uncertainty spike"
    ANALOGICAL_MATCH = "Analogical match"


class TriggerResult(BaseModel):
    trigger_type: TriggerType
    description: str
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_evidence: list[str]


class NoveltyScore(BaseModel):
    novelty_distance: float = Field(ge=0.0, le=1.0)
    synthesis_depth: float = Field(ge=0.0, le=1.0)
    mechanism_quality: float = Field(ge=0.0, le=1.0)
    predictive_power: float = Field(ge=0.0, le=1.0)
    cross_domain_transfer: float = Field(ge=0.0, le=1.0)
    token_efficiency: float = Field(ge=0.0, le=1.0)
    coherence_penalty: float = Field(ge=0.0, le=1.0)
    total: float | None = Field(default=None, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def apply_formula(self) -> NoveltyScore:
        computed = (
            0.30 * self.novelty_distance
            + 0.20 * self.synthesis_depth
            + 0.20 * self.mechanism_quality
            + 0.15 * self.predictive_power
            + 0.10 * self.cross_domain_transfer
            + 0.05 * self.token_efficiency
            - 0.10 * self.coherence_penalty
        )
        bounded = round(max(0.0, min(1.0, computed)), 4)
        if self.total is None:
            self.total = bounded
            return self
        if abs(self.total - bounded) > 0.15:
            msg = "NoveltyScore.total deviates too far from the weighted formula."
            raise ValueError(msg)
        self.total = round(self.total, 4)
        return self


class RankedInsight(BaseModel):
    id: str = Field(default_factory=lambda: new_id("insight"))
    insight_class: InsightClass
    title: str
    summary: str
    source_atoms: list[str]
    assumptions: list[str]
    mechanism: Mechanism
    proof_tree: ProofTree
    predicted_observables: list[Prediction]
    disconfirming_signals: list[str]
    counterfactual_tests: list[CounterfactualTest]
    score: NoveltyScore


class SynthesisResult(BaseModel):
    insights: list[RankedInsight]
    tokens_in: int = 0
    tokens_out: int = 0
    estimated_cost_usd: float = 0.0


class InvestigationMetrics(BaseModel):
    search_queries: int = 0
    sources_considered: int = 0
    evidence_packets: int = 0
    packets_after_compression: int = 0
    evidence_atoms_extracted: int = 0
    graph_nodes_created: int = 0
    graph_edges_created: int = 0
    triggers_fired: int = 0
    trigger_types: list[str] = Field(default_factory=list)
    synthesis_mode: str = "deep"
    tokens_in: int = 0
    tokens_out: int = 0
    estimated_cost_usd: float = 0.0
    latency_seconds: float = 0.0
    grounded_novelty_ratio: float = 0.0
    coherence_failures: int = 0


class InvestigationResult(BaseModel):
    case_id: str
    question: str
    plan: InvestigationPlan
    evidence_packets: list[EvidencePacket]
    triggers: list[TriggerResult] = Field(default_factory=list)
    insights: list[RankedInsight]
    metrics: InvestigationMetrics
    dossier_path: str
