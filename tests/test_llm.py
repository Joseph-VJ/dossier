import json
from unittest.mock import patch

from dossier.contracts import EvidencePacket, InvestigationPlan, ResearchLane, SourceAtom
from dossier.llm import DemoLlmClient, LiteLlmClient, PlannerLane, PlannerResult


def _sample_plan_and_packets() -> tuple[InvestigationPlan, list[EvidencePacket]]:
    lane = ResearchLane(id="lane_1", name="Evidence", query="q", goal="g")
    plan = InvestigationPlan(objective="Investigate: q", novelty_target="target", lanes=[lane])
    packets = [
        EvidencePacket(
            case_id="case_1",
            lane_id="lane_1",
            source_atom=SourceAtom(
                id="atom_1",
                source_id="source_1",
                lane_id="lane_1",
                title="Title",
                url="https://example.com",
                quote="Quote",
                summary="Summary",
            ),
            summary="Summary",
            quote="Quote",
            relevance=0.7,
        )
    ]
    return plan, packets


def test_demo_llm_plan_respects_lane_bounds() -> None:
    client = DemoLlmClient()
    plan = client.plan(
        question="Why did churn increase and what happens next quarter?",
        min_lanes=2,
        max_lanes=3,
        search_limit=3,
    )
    assert 2 <= len(plan.lanes) <= 3
    assert all(1 <= lane.budget <= 20 for lane in plan.lanes)
    assert plan.strategy


def test_demo_llm_plan_has_disconfirmation_lane() -> None:
    client = DemoLlmClient()
    plan = client.plan(
        question="Should we acquire Beta?",
        min_lanes=2,
        max_lanes=4,
        search_limit=3,
    )
    lane_names = [lane.name.lower() for lane in plan.lanes]
    assert any("contradiction" in name or "risk" in name for name in lane_names)


def test_litellm_plan_includes_case_memory_notes_in_prompt() -> None:
    client = LiteLlmClient(model="test-model", api_key="test-key")

    def fake_completion(**kwargs: object) -> dict[str, object]:
        messages = kwargs["messages"]
        assert isinstance(messages, list)
        user_message = messages[1]
        assert isinstance(user_message, dict)
        content = user_message["content"]
        assert isinstance(content, str)
        assert "mechanism_pattern" in content
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"objective":"Investigate: x","novelty_target":"target",'
                            '"strategy":"strategy","lanes":[{"name":"Evidence","query":"x",'
                            '"goal":"collect evidence","budget":3},{"name":"Risks","query":"x risks",'
                            '"goal":"find contradicting evidence","budget":3}]}'
                        )
                    }
                }
            ]
        }

    with patch("dossier.llm.completion", side_effect=fake_completion):
        plan = client.plan(
            question="x",
            min_lanes=2,
            max_lanes=4,
            search_limit=3,
            case_memory_notes=["[mechanism_pattern] Supplier pressure motif (score: 0.82)"],
        )

    assert len(plan.lanes) == 2


def test_litellm_synthesize_uses_shallow_mode_and_model_override() -> None:
    client = LiteLlmClient(model="deep-model", api_key="test-key")
    plan, packets = _sample_plan_and_packets()
    demo_insights = DemoLlmClient().synthesize("Question?", plan, packets).insights

    def fake_completion(**kwargs: object) -> dict[str, object]:
        assert kwargs["model"] == "cheap-model"
        messages = kwargs["messages"]
        assert isinstance(messages, list)
        system_message = messages[0]
        user_message = messages[1]
        assert isinstance(system_message, dict)
        assert isinstance(user_message, dict)
        assert "low-cost" in str(system_message["content"]).lower()
        assert "synthesis_mode" in str(user_message["content"])
        assert "shallow" in str(user_message["content"])
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {"insights": [insight.model_dump(mode="json") for insight in demo_insights]}
                        )
                    }
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        }

    with patch("dossier.llm.completion", side_effect=fake_completion):
        result = client.synthesize(
            "Question?",
            plan,
            packets,
            mode="shallow",
            model_override="cheap-model",
        )

    assert len(result.insights) == 3
    assert result.tokens_in == 10
    assert result.tokens_out == 20


def test_demo_llm_synthesize_accepts_mode_and_override() -> None:
    client = DemoLlmClient()
    plan, packets = _sample_plan_and_packets()
    result = client.synthesize("Question?", plan, packets, mode="shallow", model_override="cheap-model")
    assert len(result.insights) == 3


def test_normalize_plan_injects_disconfirmation_lane_when_missing() -> None:
    """Fix 4: confirmation-only plans must get a contradiction lane appended."""
    client = LiteLlmClient(model="test", api_key="test")
    support_only = PlannerResult(
        objective="Investigate: test",
        novelty_target="target",
        strategy="strategy",
        lanes=[
            PlannerLane(name="Support 1", query="q1", goal="find supporting data", budget=3),
            PlannerLane(name="Support 2", query="q2", goal="find more supporting data", budget=3),
        ],
    )
    normalized = client._normalize_plan(support_only, "test?", 2, 4, 3)
    lane_text = " ".join(f"{ln.name} {ln.goal}" for ln in normalized.lanes).lower()
    assert any(
        kw in lane_text
        for kw in ("contradict", "risk", "disconfirm", "counter", "challenge", "downside", "caveat")
    ), f"No disconfirmation lane found in: {[ln.name for ln in normalized.lanes]}"


def test_normalize_plan_keeps_existing_disconfirmation_lane() -> None:
    """Fix 4: plans that already have a contradiction lane should not get a duplicate."""
    client = LiteLlmClient(model="test", api_key="test")
    plan_with_contra = PlannerResult(
        objective="Investigate: test",
        novelty_target="target",
        strategy="strategy",
        lanes=[
            PlannerLane(name="Evidence", query="q1", goal="find data", budget=3),
            PlannerLane(name="Risks and Contradictions", query="q2", goal="find contradicting data", budget=3),
        ],
    )
    normalized = client._normalize_plan(plan_with_contra, "test?", 2, 4, 3)
    assert len(normalized.lanes) == 2


def test_normalize_plan_respects_max_lanes_after_injection() -> None:
    """Injecting a contradiction lane must not exceed max_lanes."""
    client = LiteLlmClient(model="test", api_key="test")
    support_only = PlannerResult(
        objective="Investigate: test",
        novelty_target="target",
        strategy="strategy",
        lanes=[
            PlannerLane(name=f"Support {i}", query=f"q{i}", goal="find data", budget=3)
            for i in range(4)
        ],
    )
    normalized = client._normalize_plan(support_only, "test?", 2, 4, 3)
    assert len(normalized.lanes) <= 4, f"Expected <= 4 lanes, got {len(normalized.lanes)}"
    # The injected lane must still be present (replacing the last support lane).
    lane_text = " ".join(f"{ln.name} {ln.goal}" for ln in normalized.lanes).lower()
    assert any(
        kw in lane_text
        for kw in ("contradict", "risk", "disconfirm", "counter", "challenge", "downside", "caveat")
    ), f"No disconfirmation lane found in: {[ln.name for ln in normalized.lanes]}"
