from pathlib import Path

from dossier.atomizer import EvidenceAtom, EvidenceAtomType
from dossier.contracts import (
    CounterfactualTest,
    EvidencePacket,
    InsightClass,
    InvestigationMetrics,
    InvestigationPlan,
    Mechanism,
    NoveltyScore,
    Prediction,
    ProofTree,
    RankedInsight,
    ResearchLane,
    SourceAtom,
)
from dossier.db import SqliteRepository


def _repo(tmp_path: Path) -> SqliteRepository:
    repo = SqliteRepository(tmp_path / "test.db")
    repo.initialize()
    return repo


def _plan() -> InvestigationPlan:
    return InvestigationPlan(
        objective="obj",
        novelty_target="target",
        lanes=[ResearchLane(id="lane_1", name="L", query="q", goal="g")],
    )


def _insight() -> RankedInsight:
    return RankedInsight(
        insight_class=InsightClass.NOVEL_DEDUCTION,
        title="Test Insight",
        summary="s",
        source_atoms=["a1"],
        assumptions=["a"],
        mechanism=Mechanism(name="m", description="d", steps=["s"]),
        proof_tree=ProofTree(conclusion="c", premises=["p"], reasoning_notes=["n"]),
        predicted_observables=[
            Prediction(observable="o", expected_signal="e", time_horizon="t", confidence=0.5)
        ],
        disconfirming_signals=["d"],
        counterfactual_tests=[
            CounterfactualTest(assumption="a", challenge_prompt="cp", expected_failure_mode="efm")
        ],
        score=NoveltyScore(
            novelty_distance=0.5, synthesis_depth=0.5, mechanism_quality=0.5,
            predictive_power=0.5, cross_domain_transfer=0.5, token_efficiency=0.5,
            coherence_penalty=0.1,
        ),
    )


def _packet(case_id: str = "case_1") -> EvidencePacket:
    return EvidencePacket(
        case_id=case_id,
        lane_id="lane_1",
        source_atom=SourceAtom(
            source_id="s1", lane_id="lane_1", title="Title",
            url="https://example.com", quote="q", summary="s",
        ),
        summary="ps",
        quote="pq",
        relevance=0.6,
    )


def _atoms(case_id: str = "case_1") -> list[EvidenceAtom]:
    return [
        EvidenceAtom(
            case_id=case_id,
            lane_id="lane_1",
            source_id="source_a",
            source_atom_id="atom_a",
            atom_type=EvidenceAtomType.ENTITY,
            atom_value="Acme Corp",
            confidence=0.61,
            context="Acme Corp reported delays.",
        ),
        EvidenceAtom(
            case_id=case_id,
            lane_id="lane_1",
            source_id="source_a",
            source_atom_id="atom_a",
            atom_type=EvidenceAtomType.WEAK_SIGNAL,
            atom_value="might",
            confidence=0.51,
            context="This might indicate a deeper issue.",
        ),
    ]


# --- initialize ---


def test_initialize_creates_tables(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    cursor = repo.connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = {row[0] for row in cursor.fetchall()}
    assert {"cases", "sources", "evidence_packets", "evidence_atoms", "insights"}.issubset(tables)


def test_initialize_is_idempotent(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.initialize()  # second call should not raise
    cursor = repo.connection.execute("SELECT count(*) FROM cases")
    assert cursor.fetchone()[0] == 0


# --- create_case ---


def test_create_case(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.create_case("case_1", "Q?", _plan())
    cursor = repo.connection.execute("SELECT id, question, status FROM cases WHERE id = ?", ("case_1",))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "case_1"
    assert row[1] == "Q?"
    assert row[2] == "running"


# --- store_source ---


def test_store_source(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.store_source(
        source_id="s1", case_id="c1", lane_id="l1",
        title="T", url="https://example.com", snippet="snip",
        raw_json='{"k":"v"}',
    )
    cursor = repo.connection.execute("SELECT id, title FROM sources WHERE id = ?", ("s1",))
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == "T"


# --- store_evidence_packet ---


def test_store_evidence_packet(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    packet = _packet()
    repo.store_evidence_packet(packet)
    cursor = repo.connection.execute(
        "SELECT case_id FROM evidence_packets WHERE id = ?", (packet.id,)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "case_1"


# --- store_insight ---


def test_store_insight(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    insight = _insight()
    repo.store_insight("case_1", insight)
    cursor = repo.connection.execute(
        "SELECT insight_class FROM insights WHERE id = ?", (insight.id,)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "Novel Deduction"


# --- store_evidence_atoms ---


def test_store_evidence_atoms(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    atoms = _atoms()
    repo.store_evidence_atoms(atoms)
    cursor = repo.connection.execute(
        "SELECT count(*) FROM evidence_atoms WHERE case_id = ?",
        ("case_1",),
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == 2


# --- complete_case ---


def test_complete_case(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.create_case("case_1", "Q?", _plan())
    metrics = InvestigationMetrics(search_queries=1)
    repo.complete_case("case_1", "/path/to/dossier.md", metrics)
    cursor = repo.connection.execute(
        "SELECT status, dossier_path FROM cases WHERE id = ?", ("case_1",)
    )
    row = cursor.fetchone()
    assert row[0] == "completed"
    assert row[1] == "/path/to/dossier.md"


def test_store_and_get_graph_nodes_and_edges(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.store_graph_node(
        case_id="case_1",
        node_id="node_1",
        node_type="source",
        label="Source node",
        data={"lane_id": "lane_1"},
    )
    repo.store_graph_node(
        case_id="case_1",
        node_id="node_2",
        node_type="typed_atom",
        label="Atom node",
        data={"lane_id": "lane_1"},
    )
    repo.store_graph_edge(
        case_id="case_1",
        edge_id="edge_1",
        edge_type="derived_from",
        source_node_id="node_2",
        target_node_id="node_1",
        metadata={"lane_id": "lane_1"},
    )

    nodes = repo.get_graph_nodes("case_1")
    edges = repo.get_graph_edges("case_1")

    assert len(nodes) == 2
    assert nodes[0]["case_id"] == "case_1"
    assert len(edges) == 1
    assert edges[0]["metadata"]["lane_id"] == "lane_1"


def test_get_subgraph_returns_bfs_slice(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.store_graph_node("case_1", "node_1", "source", "Source", {"lane_id": "lane_1"})
    repo.store_graph_node("case_1", "node_2", "typed_atom", "Atom", {"lane_id": "lane_1"})
    repo.store_graph_node("case_1", "node_3", "contradiction", "Contradiction", {"lane_id": "lane_1"})
    repo.store_graph_edge("case_1", "edge_1", "derived_from", "node_2", "node_1")
    repo.store_graph_edge("case_1", "edge_2", "contradicts", "node_3", "node_1")

    nodes, edges = repo.get_subgraph("case_1", "node_1", depth=1)

    node_ids = {node["id"] for node in nodes}
    edge_ids = {edge["id"] for edge in edges}
    assert node_ids == {"node_1", "node_2", "node_3"}
    assert edge_ids == {"edge_1", "edge_2"}


# --- fail_case ---


def test_fail_case_updates_status_and_error(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.create_case("case_1", "Q?", _plan())
    repo.fail_case("case_1", "boom")

    cursor = repo.connection.execute(
        "SELECT status, metrics_json FROM cases WHERE id = ?", ("case_1",)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "failed"
    assert '"error": "boom"' in row[1]


# --- close ---


def test_close_and_reopen(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    repo.create_case("case_1", "Q?", _plan())
    repo.close()
    # Reopen
    repo2 = SqliteRepository(tmp_path / "test.db")
    repo2.initialize()
    cursor = repo2.connection.execute("SELECT id FROM cases")
    assert cursor.fetchone()[0] == "case_1"
    repo2.close()


def test_migrate_adds_source_id_to_legacy_schema(tmp_path: Path) -> None:
    """Pre-fix databases lacking source_id columns must be migrated on initialize()."""
    import sqlite3

    db_path = tmp_path / "legacy.db"
    con = sqlite3.connect(db_path)
    # Create the old schema WITHOUT source_id columns.
    con.executescript(
        """
        CREATE TABLE cases (
            id TEXT PRIMARY KEY, question TEXT, status TEXT,
            created_at TEXT, updated_at TEXT, plan_json TEXT,
            dossier_path TEXT, metrics_json TEXT
        );
        CREATE TABLE sources (
            id TEXT PRIMARY KEY, case_id TEXT, lane_id TEXT,
            title TEXT, url TEXT, snippet TEXT, raw_json TEXT, created_at TEXT
        );
        CREATE TABLE evidence_packets (
            id TEXT PRIMARY KEY, case_id TEXT, lane_id TEXT,
            source_atom_id TEXT, packet_json TEXT, created_at TEXT
        );
        CREATE TABLE evidence_atoms (
            id TEXT PRIMARY KEY, case_id TEXT, lane_id TEXT,
            source_atom_id TEXT, atom_type TEXT, atom_value TEXT,
            confidence REAL, context TEXT, created_at TEXT
        );
        CREATE TABLE insights (
            id TEXT PRIMARY KEY, case_id TEXT, insight_class TEXT,
            insight_json TEXT, created_at TEXT
        );
        """
    )
    con.close()

    repo = SqliteRepository(db_path)
    repo.initialize()  # must migrate without error

    cols_packets = {
        row[1] for row in repo.connection.execute("PRAGMA table_info(evidence_packets)").fetchall()
    }
    cols_atoms = {
        row[1] for row in repo.connection.execute("PRAGMA table_info(evidence_atoms)").fetchall()
    }
    assert "source_id" in cols_packets, f"evidence_packets missing source_id: {cols_packets}"
    assert "source_id" in cols_atoms, f"evidence_atoms missing source_id: {cols_atoms}"

    # New-schema inserts must also work after migration.
    repo.create_case("c1", "Q?", _plan())
    repo.store_evidence_packet(_packet(case_id="c1"))
    repo.store_evidence_atoms(_atoms())
    repo.close()
