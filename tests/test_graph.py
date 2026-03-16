from pathlib import Path

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.contracts import EvidencePacket, SourceAtom
from dossier.db import SqliteRepository
from dossier.graph import EvidenceGraphBuilder


def _repo(tmp_path: Path) -> SqliteRepository:
    repo = SqliteRepository(tmp_path / "graph.db")
    repo.initialize()
    return repo


def _packet(case_id: str, lane_id: str, source_id: str, source_atom_id: str, title: str) -> EvidencePacket:
    return EvidencePacket(
        case_id=case_id,
        lane_id=lane_id,
        source_atom=SourceAtom(
            id=source_atom_id,
            source_id=source_id,
            lane_id=lane_id,
            title=title,
            url="https://example.com",
            quote="quoted evidence",
            summary="source summary",
        ),
        summary="packet summary",
        quote="packet quote",
        relevance=0.7,
    )


def _atoms(case_id: str, lane_id: str, source_id: str, source_atom_id: str) -> list[EvidenceAtom]:
    return [
        EvidenceAtom(
            id=f"{source_atom_id}_entity",
            case_id=case_id,
            lane_id=lane_id,
            source_id=source_id,
            source_atom_id=source_atom_id,
            atom_type=EvidenceAtomType.ENTITY,
            atom_value="Acme Corp",
            confidence=0.7,
            context="Acme Corp signal",
        ),
        EvidenceAtom(
            id=f"{source_atom_id}_contradiction",
            case_id=case_id,
            lane_id=lane_id,
            source_id=source_id,
            source_atom_id=source_atom_id,
            atom_type=EvidenceAtomType.CONTRADICTION,
            atom_value="however",
            confidence=0.6,
            context="However, the risks remain.",
        ),
    ]


def test_materialize_creates_expected_nodes_and_edges(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    builder = EvidenceGraphBuilder(repo)
    packet = _packet("case_1", "lane_1", "source_1", "atom_1", "Source One")
    atoms = _atoms("case_1", "lane_1", "source_1", "atom_1")

    summary = builder.materialize("case_1", [packet], atoms)

    assert summary == {"nodes_created": 5, "edges_created": 4}
    assert len(repo.get_graph_nodes("case_1")) == 5
    assert len(repo.get_graph_edges("case_1")) == 4


def test_get_subgraph_for_synthesis_filters_by_lane(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    builder = EvidenceGraphBuilder(repo)
    packets = [
        _packet("case_1", "lane_1", "source_1", "atom_1", "Source One"),
        _packet("case_1", "lane_2", "source_2", "atom_2", "Source Two"),
    ]
    atoms = _atoms("case_1", "lane_1", "source_1", "atom_1") + _atoms(
        "case_1",
        "lane_2",
        "source_2",
        "atom_2",
    )

    builder.materialize("case_1", packets, atoms)
    nodes, edges = builder.get_subgraph_for_synthesis("case_1", ["lane_1"])

    assert nodes
    assert edges
    assert all(node["data"]["lane_id"] == "lane_1" for node in nodes)
    node_ids = {node["id"] for node in nodes}
    assert all(edge["source_node_id"] in node_ids for edge in edges)
    assert all(edge["target_node_id"] in node_ids for edge in edges)


def test_graph_db_roundtrip_preserves_payloads(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.store_graph_node("case_1", "node_1", "source", "Source", {"lane_id": "lane_1", "rank": 1})
    repo.store_graph_edge(
        "case_1",
        "edge_1",
        "supports",
        "node_1",
        "node_1",
        weight=0.9,
        metadata={"lane_id": "lane_1", "note": "self loop for roundtrip"},
    )

    nodes = repo.get_graph_nodes("case_1", node_type="source")
    edges = repo.get_graph_edges("case_1", edge_type="supports")

    assert nodes == [
        {
            "id": "node_1",
            "case_id": "case_1",
            "node_type": "source",
            "label": "Source",
            "data": {"lane_id": "lane_1", "rank": 1},
        }
    ]
    assert edges == [
        {
            "id": "edge_1",
            "case_id": "case_1",
            "edge_type": "supports",
            "source_node_id": "node_1",
            "target_node_id": "node_1",
            "weight": 0.9,
            "metadata": {"lane_id": "lane_1", "note": "self loop for roundtrip"},
        }
    ]
