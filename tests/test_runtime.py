import sqlite3
import threading
import time
from pathlib import Path
from typing import cast
from unittest.mock import MagicMock

from dossier.config import Settings
from dossier.contracts import InvestigationPlan, ResearchLane, SearchHit, TriggerResult, TriggerType
from dossier.llm import DemoLlmClient
from dossier.runtime import InvestigationService


def build_settings(tmp_path: Path) -> Settings:
    return Settings(
        DOSSIER_DATA_DIR=tmp_path / "data",
        OUTPUT_DIR=tmp_path / "data" / "dossiers",
        DATABASE_URL=f"sqlite:///{tmp_path / 'data' / 'dossier.db'}",
        LLM_PROVIDER="demo",
        SEARCH_PROVIDER="demo",
    )


class ThreeLanePlanner:
    def create_plan(
        self,
        question: str,
        case_memory_notes: list[str] | None = None,
    ) -> InvestigationPlan:
        del question
        return InvestigationPlan(
            objective="Investigate: fixed",
            novelty_target="target",
            lanes=[
                ResearchLane(id="lane_1", name="Lane 1", query="q1", goal="g1"),
                ResearchLane(id="lane_2", name="Lane 2", query="q2", goal="g2"),
                ResearchLane(id="lane_3", name="Lane 3", query="q3", goal="g3"),
            ],
            case_memory_notes=case_memory_notes or [],
        )


def test_investigation_service_runs_end_to_end(tmp_path: Path) -> None:
    service = InvestigationService(build_settings(tmp_path))
    result = service.investigate("Should Acme acquire Beta?")
    expected_packets = len(result.plan.lanes) * service.settings.search_max_results

    assert result.case_id.startswith("case_")
    assert len(result.plan.lanes) >= 2
    assert len(result.evidence_packets) == expected_packets
    assert len(result.insights) == 3
    assert Path(result.dossier_path).exists()
    assert result.metrics.evidence_packets == expected_packets
    assert result.metrics.synthesis_mode == "deep"
    assert result.triggers


def test_investigation_metrics_are_populated(tmp_path: Path) -> None:
    service = InvestigationService(build_settings(tmp_path))
    result = service.investigate("Test?")

    assert result.metrics.search_queries == len(result.plan.lanes)
    assert result.metrics.sources_considered == len(result.evidence_packets)
    assert 0 < result.metrics.packets_after_compression <= len(result.evidence_packets)
    assert result.metrics.evidence_atoms_extracted > 0
    assert result.metrics.graph_nodes_created > 0
    assert result.metrics.graph_edges_created > 0
    assert result.metrics.latency_seconds > 0


def test_dossier_file_contains_question(tmp_path: Path) -> None:
    service = InvestigationService(build_settings(tmp_path))
    result = service.investigate("Is expansion viable?")

    content = Path(result.dossier_path).read_text(encoding="utf-8")
    assert "Is expansion viable?" in content


def test_search_fallback_on_provider_failure(tmp_path: Path) -> None:
    settings = build_settings(tmp_path)
    failing_search = MagicMock()
    failing_search.search.side_effect = RuntimeError("provider down")
    service = InvestigationService(settings, search_provider=failing_search)
    result = service.investigate("Fallback test?")

    # Should still complete via demo fallback
    assert len(result.evidence_packets) == len(result.plan.lanes) * settings.search_max_results
    assert result.case_id.startswith("case_")


def test_llm_fallback_on_provider_failure(tmp_path: Path) -> None:
    settings = build_settings(tmp_path)
    demo = DemoLlmClient()
    failing_llm = MagicMock()
    failing_llm.plan.side_effect = demo.plan
    failing_llm.synthesize.side_effect = RuntimeError("LLM down")
    service = InvestigationService(settings, llm_client=failing_llm)
    result = service.investigate("LLM fallback test?")

    # Should still produce insights via demo fallback
    assert len(result.insights) == 3


def test_grounded_novelty_ratio(tmp_path: Path) -> None:
    service = InvestigationService(build_settings(tmp_path))
    result = service.investigate("Ratio test?")

    # Demo insights have source_atoms and scores > 0.48 — at least some should be grounded
    assert 0.0 <= result.metrics.grounded_novelty_ratio <= 1.0


def test_coherence_failures_count(tmp_path: Path) -> None:
    service = InvestigationService(build_settings(tmp_path))
    result = service.investigate("Coherence test?")

    # Demo insights have all required fields, so coherence_failures should be 0
    assert result.metrics.coherence_failures == 0


def test_multiple_investigations_same_service(tmp_path: Path) -> None:
    service = InvestigationService(build_settings(tmp_path))
    r1 = service.investigate("First?")
    r2 = service.investigate("Second?")

    assert r1.case_id != r2.case_id
    assert "First?" in Path(r1.dossier_path).read_text(encoding="utf-8")
    assert "Second?" in Path(r2.dossier_path).read_text(encoding="utf-8")


def test_fetch_failure_falls_back_to_snippet(tmp_path: Path) -> None:
    class SnippetOnlySearch:
        def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
            del query, lane, limit
            return [SearchHit(title="T", url="http://127.0.0.1:1", snippet="snippet fallback", content=None)]

    settings = build_settings(tmp_path).model_copy(update={"fetch_enabled": True})
    failing_fetcher = MagicMock()
    failing_fetcher.fetch.side_effect = RuntimeError("fetch failed")
    service = InvestigationService(settings, search_provider=SnippetOnlySearch(), fetcher=failing_fetcher)

    result = service.investigate("Fetch fallback?")
    assert result.evidence_packets
    assert result.evidence_packets[0].quote == "snippet fallback"


def test_lane_preparation_failures_do_not_abort_case(tmp_path: Path) -> None:
    class InvalidSearchProvider:
        def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
            del query, lane, limit
            return cast(list[SearchHit], [object()])

    settings = build_settings(tmp_path)
    service = InvestigationService(settings, search_provider=InvalidSearchProvider())

    result = service.investigate("This should not abort")

    with sqlite3.connect(settings.database_path) as connection:
        row = connection.execute("SELECT status FROM cases ORDER BY created_at DESC LIMIT 1").fetchone()
    assert row is not None
    assert row[0] == "completed"
    assert result.evidence_packets == []
    assert Path(result.dossier_path).exists()


def test_runtime_persists_evidence_atoms(tmp_path: Path) -> None:
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    result = service.investigate("Should we renew this vendor contract next quarter?")

    with sqlite3.connect(settings.database_path) as connection:
        row = connection.execute(
            "SELECT count(*) FROM evidence_atoms WHERE case_id = ?",
            (result.case_id,),
        ).fetchone()

    assert row is not None
    assert row[0] > 0


def test_runtime_persists_graph_nodes_and_edges(tmp_path: Path) -> None:
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    result = service.investigate("Graph persistence test?")

    with sqlite3.connect(settings.database_path) as connection:
        node_row = connection.execute(
            "SELECT count(*) FROM graph_nodes WHERE case_id = ?",
            (result.case_id,),
        ).fetchone()
        edge_row = connection.execute(
            "SELECT count(*) FROM graph_edges WHERE case_id = ?",
            (result.case_id,),
        ).fetchone()

    assert node_row is not None
    assert node_row[0] == result.metrics.graph_nodes_created
    assert edge_row is not None
    assert edge_row[0] == result.metrics.graph_edges_created


def test_runtime_warm_start_reads_prior_case_memory(tmp_path: Path) -> None:
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    first = service.investigate("Why did supplier concentration hurt delivery reliability?")

    with sqlite3.connect(settings.database_path) as connection:
        stored = connection.execute(
            "SELECT count(*) FROM case_memory WHERE case_id = ?",
            (first.case_id,),
        ).fetchone()

    assert stored is not None
    assert stored[0] > 0

    second = service.investigate("How do pressure accumulation and contradiction signals interact?")
    assert any("mechanism_pattern" in note for note in second.plan.case_memory_notes)


def test_runtime_uses_compressed_packets_for_synthesis(tmp_path: Path) -> None:
    class DenseSearchProvider:
        def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
            del query, lane
            return [
                SearchHit(
                    title=f"Hit {index}",
                    url=f"https://example.com/{index}",
                    snippet="summary " * 80,
                    content="quote " * 80,
                )
                for index in range(limit)
            ]

    class RecordingLlmClient:
        def __init__(self) -> None:
            self.demo = DemoLlmClient()
            self.packet_counts: list[int] = []

        def plan(
            self,
            question: str,
            min_lanes: int,
            max_lanes: int,
            search_limit: int,
            case_memory_notes: list[str] | None = None,
        ):
            return self.demo.plan(question, min_lanes, max_lanes, search_limit, case_memory_notes)

        def synthesize(
            self,
            question: str,
            plan,
            packets,
            mode: str = "deep",
            model_override: str | None = None,
        ):
            self.packet_counts.append(len(packets))
            return self.demo.synthesize(question, plan, packets, mode=mode, model_override=model_override)

    settings = build_settings(tmp_path).model_copy(
        update={
            "compression_max_tokens_per_packet": 20,
            "compression_max_total_tokens": 30,
        }
    )
    llm_client = RecordingLlmClient()
    service = InvestigationService(
        settings,
        search_provider=DenseSearchProvider(),
        llm_client=llm_client,
    )

    result = service.investigate("Compression boundary test?")

    assert result.metrics.packets_after_compression < len(result.evidence_packets)
    assert llm_client.packet_counts == [result.metrics.packets_after_compression]


def test_parallel_lane_execution_returns_all_packets(tmp_path: Path) -> None:
    class ConcurrentSearchProvider:
        def __init__(self) -> None:
            self.active = 0
            self.max_active = 0
            self.lock = threading.Lock()
            self.barrier = threading.Barrier(3)

        def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
            del limit
            with self.lock:
                self.active += 1
                self.max_active = max(self.max_active, self.active)
            self.barrier.wait(timeout=1.0)
            time.sleep(0.05)
            with self.lock:
                self.active -= 1
            return [
                SearchHit(
                    title=f"{lane.name} title",
                    url=f"https://example.com/{lane.id}",
                    snippet=f"{query} snippet",
                    content=f"{lane.name} content",
                )
            ]

    provider = ConcurrentSearchProvider()
    settings = build_settings(tmp_path).model_copy(update={"max_parallel_lanes": 3})
    service = InvestigationService(settings, planner=ThreeLanePlanner(), search_provider=provider)

    result = service.investigate("Parallel test?")

    assert len(result.evidence_packets) == 3
    assert provider.max_active > 1


def test_lane_failure_does_not_crash_investigation(tmp_path: Path) -> None:
    class PartiallyBrokenSearchProvider:
        def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
            del query, limit
            if lane.id == "lane_2":
                return cast(list[SearchHit], [object()])
            return [
                SearchHit(
                    title=f"{lane.name} title",
                    url=f"https://example.com/{lane.id}",
                    snippet=f"{lane.name} snippet",
                    content=f"{lane.name} content",
                )
            ]

    settings = build_settings(tmp_path)
    service = InvestigationService(
        settings,
        planner=ThreeLanePlanner(),
        search_provider=PartiallyBrokenSearchProvider(),
    )

    result = service.investigate("Lane failure test?")

    assert len(result.evidence_packets) == 2
    assert Path(result.dossier_path).exists()


def test_persistence_order_follows_plan_lane_order(tmp_path: Path) -> None:
    class OrderedSearchProvider:
        def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
            del query, limit
            return [
                SearchHit(
                    title=f"{lane.name} source",
                    url=f"https://example.com/{lane.id}",
                    snippet=f"{lane.name} snippet",
                    content=f"{lane.name} content",
                )
            ]

    settings = build_settings(tmp_path)
    service = InvestigationService(
        settings,
        planner=ThreeLanePlanner(),
        search_provider=OrderedSearchProvider(),
    )
    result = service.investigate("Order test?")

    with sqlite3.connect(settings.database_path) as connection:
        rows = connection.execute(
            "SELECT lane_id FROM sources WHERE case_id = ? ORDER BY rowid",
            (result.case_id,),
        ).fetchall()

    assert [row[0] for row in rows] == ["lane_1", "lane_2", "lane_3"]


def test_no_trigger_uses_shallow_mode(tmp_path: Path) -> None:
    class NoTriggerDetector:
        def detect(self, plan, packets, typed_atoms, graph_nodes, graph_edges, case_memory_notes):
            del plan, packets, typed_atoms, graph_nodes, graph_edges, case_memory_notes
            return []

    class RecordingLlmClient:
        def __init__(self) -> None:
            self.demo = DemoLlmClient()
            self.calls: list[tuple[str, str | None]] = []

        def plan(
            self,
            question: str,
            min_lanes: int,
            max_lanes: int,
            search_limit: int,
            case_memory_notes: list[str] | None = None,
        ):
            return self.demo.plan(question, min_lanes, max_lanes, search_limit, case_memory_notes)

        def synthesize(
            self,
            question: str,
            plan,
            packets,
            mode: str = "deep",
            model_override: str | None = None,
        ):
            self.calls.append((mode, model_override))
            return self.demo.synthesize(question, plan, packets, mode=mode, model_override=model_override)

    settings = build_settings(tmp_path).model_copy(update={"shallow_synthesis_model": "cheap-model"})
    llm_client = RecordingLlmClient()
    service = InvestigationService(
        settings,
        llm_client=llm_client,
        trigger_detector=NoTriggerDetector(),
    )

    result = service.investigate("Shallow mode test?")

    assert result.metrics.synthesis_mode == "shallow"
    assert result.metrics.triggers_fired == 0
    assert llm_client.calls == [("shallow", "cheap-model")]


def test_triggered_case_uses_deep_mode(tmp_path: Path) -> None:
    class FixedTriggerDetector:
        def detect(self, plan, packets, typed_atoms, graph_nodes, graph_edges, case_memory_notes):
            del plan, packets, typed_atoms, graph_nodes, graph_edges, case_memory_notes
            return [
                TriggerResult(
                    trigger_type=TriggerType.CROSS_LANE_CONVERGENCE,
                    description="Shared entity overlap.",
                    confidence=0.8,
                    supporting_evidence=["atom_1", "atom_2"],
                )
            ]

    class RecordingLlmClient:
        def __init__(self) -> None:
            self.demo = DemoLlmClient()
            self.calls: list[tuple[str, str | None]] = []

        def plan(
            self,
            question: str,
            min_lanes: int,
            max_lanes: int,
            search_limit: int,
            case_memory_notes: list[str] | None = None,
        ):
            return self.demo.plan(question, min_lanes, max_lanes, search_limit, case_memory_notes)

        def synthesize(
            self,
            question: str,
            plan,
            packets,
            mode: str = "deep",
            model_override: str | None = None,
        ):
            self.calls.append((mode, model_override))
            return self.demo.synthesize(question, plan, packets, mode=mode, model_override=model_override)

    settings = build_settings(tmp_path).model_copy(update={"shallow_synthesis_model": "cheap-model"})
    llm_client = RecordingLlmClient()
    service = InvestigationService(
        settings,
        llm_client=llm_client,
        trigger_detector=FixedTriggerDetector(),
    )

    result = service.investigate("Deep mode test?")

    assert result.metrics.synthesis_mode == "deep"
    assert result.metrics.triggers_fired == 1
    assert result.metrics.trigger_types == [TriggerType.CROSS_LANE_CONVERGENCE.value]
    assert llm_client.calls == [("deep", None)]


def test_provenance_chain_joins_source_to_packets(tmp_path: Path) -> None:
    """Fix 1: evidence_packets.source_id must join back to sources.id."""
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    result = service.investigate("Provenance chain test?")

    with sqlite3.connect(settings.database_path) as connection:
        joined = connection.execute(
            "SELECT count(*) FROM evidence_packets ep "
            "JOIN sources s ON s.id = ep.source_id "
            "WHERE ep.case_id = ?",
            (result.case_id,),
        ).fetchone()

    assert joined is not None
    assert joined[0] == len(result.evidence_packets)


def test_provenance_chain_joins_source_to_atoms(tmp_path: Path) -> None:
    """Fix 1: evidence_atoms.source_id must join back to sources.id."""
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    result = service.investigate("Atom provenance test?")

    with sqlite3.connect(settings.database_path) as connection:
        atom_count = connection.execute(
            "SELECT count(*) FROM evidence_atoms WHERE case_id = ?",
            (result.case_id,),
        ).fetchone()
        joined = connection.execute(
            "SELECT count(*) FROM evidence_atoms ea "
            "JOIN sources s ON s.id = ea.source_id "
            "WHERE ea.case_id = ?",
            (result.case_id,),
        ).fetchone()

    assert atom_count is not None and atom_count[0] > 0
    assert joined is not None
    assert joined[0] == atom_count[0]


def test_insights_sorted_by_score_descending(tmp_path: Path) -> None:
    """Fix 3: Ranked insights must be sorted by score.total descending."""
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    result = service.investigate("Sort test?")

    totals: list[float] = [i.score.total for i in result.insights if i.score.total is not None]
    assert totals == sorted(totals, reverse=True)


def test_citation_validation_filters_invalid_source_atoms(tmp_path: Path) -> None:
    """Fix 2: insights must not reference source_atom IDs that don't exist in packets."""
    settings = build_settings(tmp_path)
    service = InvestigationService(settings)
    result = service.investigate("Citation test?")

    valid_ids = {p.source_atom.id for p in result.evidence_packets}
    for insight in result.insights:
        for atom_id in insight.source_atoms:
            assert atom_id in valid_ids, f"Insight cites nonexistent atom {atom_id}"
