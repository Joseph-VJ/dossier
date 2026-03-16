from dossier.llm import DemoLlmClient
from dossier.planner import DefaultPlanner


def test_planner_creates_dynamic_lanes() -> None:
    planner = DefaultPlanner(llm_client=DemoLlmClient(), min_lanes=2, max_lanes=4, search_limit=3)
    plan = planner.create_plan("Why did delivery reliability fall in Q3?")
    assert 2 <= len(plan.lanes) <= 4


def test_planner_objective_includes_question() -> None:
    planner = DefaultPlanner(llm_client=DemoLlmClient(), min_lanes=2, max_lanes=3, search_limit=3)
    plan = planner.create_plan("Is this viable?")
    assert "Is this viable?" in plan.objective


def test_planner_sets_strategy_and_budget_notes() -> None:
    planner = DefaultPlanner(llm_client=DemoLlmClient(), min_lanes=2, max_lanes=3, search_limit=3)
    plan = planner.create_plan("Test question")
    assert any(note.startswith("Planner strategy:") for note in plan.case_memory_notes)
    assert any(note.startswith("Lane budget [") for note in plan.case_memory_notes)


def test_planner_normalizes_whitespace_in_query() -> None:
    planner = DefaultPlanner(llm_client=DemoLlmClient(), min_lanes=2, max_lanes=3, search_limit=3)
    plan = planner.create_plan("  lots   of   spaces  ")
    assert "lots of spaces" in plan.objective
    assert "  " not in plan.lanes[0].query


def test_planner_respects_max_lane_limit() -> None:
    planner = DefaultPlanner(llm_client=DemoLlmClient(), min_lanes=2, max_lanes=2, search_limit=3)
    plan = planner.create_plan("Why did revenue fall and what happens next quarter?")
    assert len(plan.lanes) == 2


def test_planner_preserves_warm_start_case_memory_notes() -> None:
    planner = DefaultPlanner(llm_client=DemoLlmClient(), min_lanes=2, max_lanes=3, search_limit=3)
    plan = planner.create_plan(
        "Why did delivery reliability fall?",
        case_memory_notes=["[mechanism_pattern] Supplier pressure motif (score: 0.82)"],
    )

    assert plan.case_memory_notes[0].startswith("[mechanism_pattern]")
