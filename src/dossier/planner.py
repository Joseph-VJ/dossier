from __future__ import annotations

import logging
from typing import Protocol

from dossier.contracts import InvestigationPlan, ResearchLane
from dossier.llm import LlmClient

logger = logging.getLogger(__name__)


class Planner(Protocol):
    def create_plan(
        self,
        question: str,
        case_memory_notes: list[str] | None = None,
    ) -> InvestigationPlan:
        ...


def _normalize_question(question: str) -> str:
    return " ".join(question.split())


class DefaultPlanner:
    """LLM-driven planner with deterministic fallback behavior."""

    def __init__(
        self,
        llm_client: LlmClient,
        min_lanes: int = 2,
        max_lanes: int = 4,
        search_limit: int = 3,
    ) -> None:
        self.llm_client = llm_client
        self.min_lanes = max(1, min_lanes)
        self.max_lanes = max(self.min_lanes, max_lanes)
        self.search_limit = max(1, search_limit)

    def create_plan(
        self,
        question: str,
        case_memory_notes: list[str] | None = None,
    ) -> InvestigationPlan:
        normalized_question = _normalize_question(question)
        planned = self.llm_client.plan(
            question=normalized_question,
            min_lanes=self.min_lanes,
            max_lanes=self.max_lanes,
            search_limit=self.search_limit,
            case_memory_notes=case_memory_notes,
        )

        lanes: list[ResearchLane] = []
        lane_budget_notes: list[str] = []
        for lane in planned.lanes[: self.max_lanes]:
            lane_name = " ".join(lane.name.split()) or "Research Lane"
            lane_query = " ".join(lane.query.split()) or normalized_question
            lane_goal = " ".join(lane.goal.split()) or "Collect relevant evidence for synthesis."
            lanes.append(
                ResearchLane(
                    name=lane_name,
                    query=lane_query,
                    goal=lane_goal,
                )
            )
            lane_budget_notes.append(
                f"Lane budget [{lane_name}]: {lane.budget} retrieval units."
            )

        if not lanes:
            logger.warning("Planner returned no lanes; falling back to single default lane.")
            lanes = [
                ResearchLane(
                    name="Direct Evidence",
                    query=normalized_question,
                    goal="Collect direct evidence and primary supporting signals.",
                )
            ]

        plan_notes = [
            *(case_memory_notes or []),
            f"Planner strategy: {planned.strategy}",
            *lane_budget_notes,
            "Prioritize source diversity and preserve disconfirming signals.",
        ]

        return InvestigationPlan(
            objective=planned.objective or f"Investigate: {normalized_question}",
            novelty_target=planned.novelty_target
            or "Produce top invention-grade insights with explicit assumptions.",
            lanes=lanes,
            case_memory_notes=plan_notes,
        )
