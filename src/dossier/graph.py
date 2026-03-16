from __future__ import annotations

from typing import Any

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.contracts import EvidencePacket
from dossier.contracts.models import new_id
from dossier.db import SqliteRepository


class EvidenceGraphBuilder:
    def __init__(self, repository: SqliteRepository) -> None:
        self.repository = repository

    def materialize(
        self,
        case_id: str,
        packets: list[EvidencePacket],
        typed_atoms: list[EvidenceAtom],
    ) -> dict[str, int]:
        nodes_created = 0
        edges_created = 0
        source_node_ids: set[str] = set()

        for packet in packets:
            source_node_id = packet.source_atom.source_id
            source_payload = {
                "lane_id": packet.lane_id,
                "source_atom_id": packet.source_atom.id,
                "url": packet.source_atom.url,
                "summary": packet.source_atom.summary,
            }
            if source_node_id not in source_node_ids:
                self.repository.store_graph_node(
                    case_id=case_id,
                    node_id=source_node_id,
                    node_type="source",
                    label=packet.source_atom.title,
                    data=source_payload,
                )
                source_node_ids.add(source_node_id)
                nodes_created += 1

            evidence_node_id = packet.id
            self.repository.store_graph_node(
                case_id=case_id,
                node_id=evidence_node_id,
                node_type="evidence_item",
                label=packet.summary[:120] or packet.source_atom.title,
                data={
                    "lane_id": packet.lane_id,
                    "source_id": packet.source_atom.source_id,
                    "source_atom_id": packet.source_atom.id,
                    "quote": packet.quote,
                    "relevance": packet.relevance,
                },
            )
            self.repository.store_graph_edge(
                case_id=case_id,
                edge_id=new_id("gedge"),
                edge_type="cites",
                source_node_id=evidence_node_id,
                target_node_id=source_node_id,
                metadata={"lane_id": packet.lane_id},
            )
            nodes_created += 1
            edges_created += 1

        for atom in typed_atoms:
            typed_atom_payload: dict[str, Any] = {
                "lane_id": atom.lane_id,
                "source_id": atom.source_id,
                "source_atom_id": atom.source_atom_id,
                "atom_type": atom.atom_type.value,
                "confidence": atom.confidence,
                "context": atom.context,
            }
            self.repository.store_graph_node(
                case_id=case_id,
                node_id=atom.id,
                node_type="typed_atom",
                label=atom.atom_value,
                data=typed_atom_payload,
            )
            self.repository.store_graph_edge(
                case_id=case_id,
                edge_id=new_id("gedge"),
                edge_type="derived_from",
                source_node_id=atom.id,
                target_node_id=atom.source_id,
                metadata={"lane_id": atom.lane_id, "atom_type": atom.atom_type.value},
            )
            nodes_created += 1
            edges_created += 1

            if atom.atom_type is EvidenceAtomType.CONTRADICTION:
                contradiction_node_id = new_id("gcontr")
                self.repository.store_graph_node(
                    case_id=case_id,
                    node_id=contradiction_node_id,
                    node_type="contradiction",
                    label=f"Contradiction: {atom.atom_value}",
                    data={
                        "lane_id": atom.lane_id,
                        "source_id": atom.source_id,
                        "source_atom_id": atom.source_atom_id,
                        "confidence": atom.confidence,
                        "context": atom.context,
                    },
                )
                self.repository.store_graph_edge(
                    case_id=case_id,
                    edge_id=new_id("gedge"),
                    edge_type="contradicts",
                    source_node_id=contradiction_node_id,
                    target_node_id=atom.source_id,
                    metadata={"lane_id": atom.lane_id, "atom_id": atom.id},
                )
                nodes_created += 1
                edges_created += 1

        return {"nodes_created": nodes_created, "edges_created": edges_created}

    def get_subgraph_for_synthesis(
        self,
        case_id: str,
        lane_ids: list[str],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        lane_id_set = set(lane_ids)
        nodes = [
            node
            for node in self.repository.get_graph_nodes(case_id)
            if node["data"].get("lane_id") in lane_id_set
        ]
        node_ids = {str(node["id"]) for node in nodes}
        edges = [
            edge
            for edge in self.repository.get_graph_edges(case_id)
            if str(edge["source_node_id"]) in node_ids and str(edge["target_node_id"]) in node_ids
        ]
        return nodes, edges
