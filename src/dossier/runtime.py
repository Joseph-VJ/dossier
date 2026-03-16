from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from time import perf_counter

from dossier.atomizer import EvidenceAtom, EvidenceAtomizer
from dossier.compression import Compressor, build_compressor
from dossier.config import Settings
from dossier.contracts import (
    EvidencePacket,
    InvestigationMetrics,
    InvestigationPlan,
    InvestigationResult,
    RankedInsight,
    ResearchLane,
    SearchHit,
    SourceAtom,
    SynthesisResult,
)
from dossier.contracts.models import new_id
from dossier.db import SqliteRepository
from dossier.fetching import HttpFetcher
from dossier.graph import EvidenceGraphBuilder
from dossier.llm import DemoLlmClient, LlmClient, build_llm_client
from dossier.memory import CaseMemoryManager
from dossier.output import render_dossier_markdown, write_dossier
from dossier.planner import DefaultPlanner, Planner
from dossier.search import DemoSearchProvider, SearchProvider, build_search_provider
from dossier.triggers import TriggerDetectorProtocol, build_trigger_detector

logger = logging.getLogger(__name__)


@dataclass
class SourceRecord:
    source_id: str
    case_id: str
    lane_id: str
    title: str
    url: str
    snippet: str
    raw_json: str


@dataclass
class LaneExecutionResult:
    lane_id: str
    lane_name: str
    source_count: int
    sources_to_store: list[SourceRecord]
    packets: list[EvidencePacket]
    atoms: list[EvidenceAtom]
    failed: bool = False
    error_message: str | None = None


class InvestigationService:
    def __init__(
        self,
        settings: Settings,
        repository: SqliteRepository | None = None,
        planner: Planner | None = None,
        search_provider: SearchProvider | None = None,
        llm_client: LlmClient | None = None,
        fetcher: HttpFetcher | None = None,
        atomizer: EvidenceAtomizer | None = None,
        graph_builder: EvidenceGraphBuilder | None = None,
        memory_manager: CaseMemoryManager | None = None,
        compressor: Compressor | None = None,
        trigger_detector: TriggerDetectorProtocol | None = None,
    ) -> None:
        self.settings = settings
        self.settings.prepare_paths()
        self.repository = repository or SqliteRepository(self.settings.database_path)
        self.search_provider = search_provider or build_search_provider(self.settings)
        self.demo_search_provider = DemoSearchProvider()
        self.llm_client = llm_client or build_llm_client(self.settings)
        self.planner = planner or DefaultPlanner(
            llm_client=self.llm_client,
            min_lanes=self.settings.planner_min_lanes,
            max_lanes=self.settings.planner_max_lanes,
            search_limit=self.settings.search_max_results,
        )
        self.demo_llm = DemoLlmClient()
        self.fetcher = fetcher or HttpFetcher()
        self.atomizer = atomizer or EvidenceAtomizer()
        self.graph_builder = graph_builder or EvidenceGraphBuilder(self.repository)
        self.memory_manager = memory_manager or CaseMemoryManager(self.repository)
        self.compressor = compressor or build_compressor(self.settings)
        self.trigger_detector = trigger_detector or build_trigger_detector(self.settings)
        self.repository.initialize()

    def investigate(self, question: str) -> InvestigationResult:
        started = perf_counter()
        case_id = new_id("case")
        case_created = False
        try:
            memory_notes = self.memory_manager.warm_start(question)
            plan = self.planner.create_plan(question, case_memory_notes=memory_notes)
            self.repository.create_case(case_id=case_id, question=question, plan=plan)
            case_created = True

            lane_results = self._execute_lanes(case_id, plan.lanes)
            packets: list[EvidencePacket] = []
            all_atoms: list[EvidenceAtom] = []
            source_count = 0
            atom_count = 0
            for lane in plan.lanes:
                result = lane_results.get(
                    lane.id,
                    LaneExecutionResult(
                        lane_id=lane.id,
                        lane_name=lane.name,
                        source_count=0,
                        sources_to_store=[],
                        packets=[],
                        atoms=[],
                        failed=True,
                        error_message="Lane result missing.",
                    ),
                )
                if result.failed:
                    logger.warning(
                        "Lane %s failed during preparation: %s",
                        result.lane_name,
                        result.error_message,
                    )
                    continue
                for source in result.sources_to_store:
                    self.repository.store_source(
                        source_id=source.source_id,
                        case_id=source.case_id,
                        lane_id=source.lane_id,
                        title=source.title,
                        url=source.url,
                        snippet=source.snippet,
                        raw_json=source.raw_json,
                    )
                for packet in result.packets:
                    self.repository.store_evidence_packet(packet)
                self.repository.store_evidence_atoms(result.atoms)
                packets.extend(result.packets)
                all_atoms.extend(result.atoms)
                source_count += result.source_count
                atom_count += len(result.atoms)

            graph_summary = self.graph_builder.materialize(case_id, packets, all_atoms)
            logger.info(
                "Graph materialized for case %s with %s nodes and %s edges",
                case_id,
                graph_summary["nodes_created"],
                graph_summary["edges_created"],
            )

            graph_nodes = self.repository.get_graph_nodes(case_id)
            graph_edges = self.repository.get_graph_edges(case_id)
            triggers = (
                self.trigger_detector.detect(
                    plan=plan,
                    packets=packets,
                    typed_atoms=all_atoms,
                    graph_nodes=graph_nodes,
                    graph_edges=graph_edges,
                    case_memory_notes=memory_notes,
                )
                if self.settings.trigger_enabled
                else []
            )
            synthesis_mode = "deep" if (not self.settings.trigger_enabled or triggers) else "shallow"
            logger.info(
                "Trigger detection for case %s produced %s trigger(s): %s",
                case_id,
                len(triggers),
                [trigger.trigger_type.value for trigger in triggers],
            )
            compressed_packets = self.compressor.compress(packets)
            synthesis = self._safe_synthesis(
                question=question,
                plan=plan,
                packets=compressed_packets,
                mode=synthesis_mode,
                model_override=(
                    self.settings.shallow_synthesis_model if synthesis_mode == "shallow" else None
                ),
            )
            valid_atom_ids = {packet.source_atom.id for packet in packets}
            for insight in synthesis.insights:
                insight.source_atoms = [
                    atom_id for atom_id in insight.source_atoms if atom_id in valid_atom_ids
                ]
            synthesis.insights.sort(
                key=lambda i: i.score.total if i.score.total is not None else 0.0,
                reverse=True,
            )
            for insight in synthesis.insights:
                self.repository.store_insight(case_id, insight)
            memory_motifs_written = self.memory_manager.writeback(case_id, synthesis.insights)
            logger.info("Case memory writeback stored %s motifs for case %s", memory_motifs_written, case_id)

            metrics = InvestigationMetrics(
                search_queries=len(plan.lanes),
                sources_considered=source_count,
                evidence_packets=len(packets),
                packets_after_compression=len(compressed_packets),
                evidence_atoms_extracted=atom_count,
                graph_nodes_created=graph_summary["nodes_created"],
                graph_edges_created=graph_summary["edges_created"],
                triggers_fired=len(triggers),
                trigger_types=[trigger.trigger_type.value for trigger in triggers],
                synthesis_mode=synthesis_mode,
                tokens_in=synthesis.tokens_in,
                tokens_out=synthesis.tokens_out,
                estimated_cost_usd=round(synthesis.estimated_cost_usd, 4),
                latency_seconds=round(perf_counter() - started, 3),
                grounded_novelty_ratio=self._grounded_novelty_ratio(synthesis.insights),
                coherence_failures=self._coherence_failures(synthesis.insights),
            )
            if atom_count == 0:
                logger.warning("No evidence atoms were extracted for case %s", case_id)
            markdown = render_dossier_markdown(
                question,
                case_id,
                plan,
                packets,
                triggers,
                synthesis.insights,
                metrics,
            )
            dossier_path = write_dossier(self.settings.output_dir, case_id, markdown)
            self.repository.complete_case(case_id, str(dossier_path), metrics)
            return InvestigationResult(
                case_id=case_id,
                question=question,
                plan=plan,
                evidence_packets=packets,
                triggers=triggers,
                insights=synthesis.insights,
                metrics=metrics,
                dossier_path=str(dossier_path),
            )
        except Exception as exc:
            logger.exception("Investigation failed for case %s", case_id)
            if case_created:
                self.repository.fail_case(case_id, str(exc))
            raise

    def _safe_search(self, query: str, lane: ResearchLane) -> list[SearchHit]:
        try:
            return self.search_provider.search(query, lane, self.settings.search_max_results)
        except Exception:
            logger.exception("Search provider failed for query %r, falling back to demo", query)
            return self.demo_search_provider.search(query, lane, self.settings.search_max_results)

    def _safe_synthesis(
        self,
        question: str,
        plan: InvestigationPlan,
        packets: list[EvidencePacket],
        mode: str = "deep",
        model_override: str | None = None,
    ) -> SynthesisResult:
        try:
            return self.llm_client.synthesize(
                question,
                plan,
                packets,
                mode=mode,
                model_override=model_override,
            )
        except Exception:
            logger.exception("LLM synthesis failed, falling back to demo")
            return self.demo_llm.synthesize(
                question,
                plan,
                packets,
                mode=mode,
                model_override=model_override,
            )

    def _execute_lanes(
        self,
        case_id: str,
        lanes: list[ResearchLane],
    ) -> dict[str, LaneExecutionResult]:
        if not lanes:
            return {}

        max_workers = max(1, min(self.settings.max_parallel_lanes, len(lanes)))
        results: dict[str, LaneExecutionResult] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._execute_lane, case_id, lane): lane
                for lane in lanes
            }
            for future in as_completed(futures):
                lane = futures[future]
                try:
                    result = future.result()
                except Exception as exc:
                    logger.exception("Lane %s failed unexpectedly", lane.name)
                    result = LaneExecutionResult(
                        lane_id=lane.id,
                        lane_name=lane.name,
                        source_count=0,
                        sources_to_store=[],
                        packets=[],
                        atoms=[],
                        failed=True,
                        error_message=str(exc),
                    )
                results[result.lane_id] = result
        return results

    def _execute_lane(self, case_id: str, lane: ResearchLane) -> LaneExecutionResult:
        try:
            hits = self._safe_search(lane.query, lane)
            sources_to_store: list[SourceRecord] = []
            packets: list[EvidencePacket] = []
            atoms: list[EvidenceAtom] = []
            for hit in hits:
                source_record, packet, hit_atoms = self._prepare_source_packet_and_atoms(case_id, lane, hit)
                sources_to_store.append(source_record)
                packets.append(packet)
                atoms.extend(hit_atoms)
            return LaneExecutionResult(
                lane_id=lane.id,
                lane_name=lane.name,
                source_count=len(hits),
                sources_to_store=sources_to_store,
                packets=packets,
                atoms=atoms,
            )
        except Exception as exc:
            logger.exception("Lane %s failed during preparation", lane.name)
            return LaneExecutionResult(
                lane_id=lane.id,
                lane_name=lane.name,
                source_count=0,
                sources_to_store=[],
                packets=[],
                atoms=[],
                failed=True,
                error_message=str(exc),
            )

    def _prepare_source_packet_and_atoms(
        self,
        case_id: str,
        lane: ResearchLane,
        hit: SearchHit,
    ) -> tuple[SourceRecord, EvidencePacket, list[EvidenceAtom]]:
        source_id = new_id("source")
        quote = self._quote_for_hit(hit)
        source_atom = SourceAtom(
            source_id=source_id,
            lane_id=lane.id,
            title=hit.title,
            url=hit.url,
            quote=quote,
            summary=hit.snippet or "No snippet returned.",
        )
        source_record = SourceRecord(
            source_id=source_atom.source_id,
            case_id=case_id,
            lane_id=lane.id,
            title=hit.title,
            url=hit.url,
            snippet=hit.snippet,
            raw_json=json.dumps(hit.model_dump(mode="json")),
        )
        packet = EvidencePacket(
            case_id=case_id,
            lane_id=lane.id,
            source_atom=source_atom,
            summary=hit.snippet or "No snippet returned.",
            quote=quote,
            relevance=0.62 if hit.content else 0.55,
        )
        atoms = self.atomizer.extract_atoms(
            case_id=case_id,
            lane_id=lane.id,
            source_id=packet.source_atom.source_id,
            source_atom_id=packet.source_atom.id,
            title=hit.title,
            summary=packet.summary,
            quote=packet.quote,
            content=hit.content,
        )
        return source_record, packet, atoms

    def _quote_for_hit(self, hit: SearchHit) -> str:
        if hit.content:
            return hit.content[:220]
        if self.settings.fetch_enabled and hit.url.startswith("http"):
            try:
                fetched_page = self.fetcher.fetch(hit.url)
                return fetched_page.excerpt
            except Exception:
                logger.exception("Fetch failed for %r, using snippet fallback", hit.url)
        return hit.snippet[:220]

    def _grounded_novelty_ratio(self, insights: list[RankedInsight]) -> float:
        if not insights:
            return 0.0
        grounded = [insight for insight in insights if len(insight.source_atoms) >= 2 and (insight.score.total or 0.0) >= 0.48]
        return round(len(grounded) / len(insights), 3)

    def _coherence_failures(self, insights: list[RankedInsight]) -> int:
        failures = 0
        for insight in insights:
            if not insight.assumptions or not insight.disconfirming_signals or not insight.source_atoms:
                failures += 1
        return failures
