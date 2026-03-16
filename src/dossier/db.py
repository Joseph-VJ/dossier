from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dossier.atomizer import EvidenceAtom
from dossier.contracts import EvidencePacket, InvestigationMetrics, InvestigationPlan, RankedInsight
from dossier.contracts.models import new_id


def utc_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def _json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    decoded = json.loads(value)
    if isinstance(decoded, dict):
        return decoded
    msg = "Expected JSON object payload."
    raise ValueError(msg)


class SqliteRepository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._connection: sqlite3.Connection | None = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.execute("PRAGMA foreign_keys=ON")
        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def initialize(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                plan_json TEXT NOT NULL,
                dossier_path TEXT,
                metrics_json TEXT
            );

            CREATE TABLE IF NOT EXISTS sources (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                lane_id TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                snippet TEXT NOT NULL,
                raw_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence_packets (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                lane_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                source_atom_id TEXT NOT NULL,
                packet_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence_atoms (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                lane_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                source_atom_id TEXT NOT NULL,
                atom_type TEXT NOT NULL,
                atom_value TEXT NOT NULL,
                confidence REAL NOT NULL,
                context TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS insights (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                insight_class TEXT NOT NULL,
                insight_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS graph_nodes (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                node_type TEXT NOT NULL,
                label TEXT NOT NULL,
                data_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS graph_edges (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                edge_type TEXT NOT NULL,
                source_node_id TEXT NOT NULL,
                target_node_id TEXT NOT NULL,
                weight REAL DEFAULT 1.0,
                metadata_json TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS case_memory (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                motif_type TEXT NOT NULL,
                content TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_sources_case_id ON sources(case_id);
            CREATE INDEX IF NOT EXISTS idx_evidence_case_id ON evidence_packets(case_id);
            CREATE INDEX IF NOT EXISTS idx_atoms_case_id ON evidence_atoms(case_id);
            CREATE INDEX IF NOT EXISTS idx_insights_case_id ON insights(case_id);
            CREATE INDEX IF NOT EXISTS idx_graph_nodes_case_id ON graph_nodes(case_id);
            CREATE INDEX IF NOT EXISTS idx_graph_nodes_type ON graph_nodes(node_type);
            CREATE INDEX IF NOT EXISTS idx_graph_edges_case_id ON graph_edges(case_id);
            CREATE INDEX IF NOT EXISTS idx_graph_edges_source ON graph_edges(source_node_id);
            CREATE INDEX IF NOT EXISTS idx_graph_edges_target ON graph_edges(target_node_id);
            CREATE INDEX IF NOT EXISTS idx_case_memory_motif ON case_memory(motif_type);
            """
        )
        self._migrate_schema()

    def _migrate_schema(self) -> None:
        """Add columns introduced after the initial schema (v0 -> v1)."""
        migrations: list[tuple[str, str, str]] = [
            ("evidence_packets", "source_id", "TEXT NOT NULL DEFAULT ''"),
            ("evidence_atoms", "source_id", "TEXT NOT NULL DEFAULT ''"),
        ]
        for table, column, col_def in migrations:
            existing = {
                row[1]
                for row in self.connection.execute(f"PRAGMA table_info({table})").fetchall()
            }
            if column not in existing:
                self.connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
        self.connection.commit()

    def create_case(self, case_id: str, question: str, plan: InvestigationPlan) -> None:
        timestamp = utc_timestamp()
        self.connection.execute(
            """
            INSERT INTO cases (id, question, status, created_at, updated_at, plan_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (case_id, question, "running", timestamp, timestamp, json.dumps(plan.model_dump(mode="json"))),
        )
        self.connection.commit()

    def store_source(
        self,
        source_id: str,
        case_id: str,
        lane_id: str,
        title: str,
        url: str,
        snippet: str,
        raw_json: str,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO sources (id, case_id, lane_id, title, url, snippet, raw_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (source_id, case_id, lane_id, title, url, snippet, raw_json, utc_timestamp()),
        )
        self.connection.commit()

    def store_evidence_packet(self, packet: EvidencePacket) -> None:
        self.connection.execute(
            """
            INSERT INTO evidence_packets (id, case_id, lane_id, source_id, source_atom_id, packet_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                packet.id,
                packet.case_id,
                packet.lane_id,
                packet.source_atom.source_id,
                packet.source_atom.id,
                json.dumps(packet.model_dump(mode="json")),
                utc_timestamp(),
            ),
        )
        self.connection.commit()

    def store_evidence_atoms(self, atoms: list[EvidenceAtom]) -> None:
        if not atoms:
            return
        self.connection.executemany(
            """
            INSERT INTO evidence_atoms
            (id, case_id, lane_id, source_id, source_atom_id, atom_type, atom_value, confidence, context, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    atom.id,
                    atom.case_id,
                    atom.lane_id,
                    atom.source_id,
                    atom.source_atom_id,
                    atom.atom_type.value,
                    atom.atom_value,
                    atom.confidence,
                    atom.context,
                    utc_timestamp(),
                )
                for atom in atoms
            ],
        )
        self.connection.commit()

    def store_insight(self, case_id: str, insight: RankedInsight) -> None:
        self.connection.execute(
            """
            INSERT INTO insights (id, case_id, insight_class, insight_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                insight.id,
                case_id,
                insight.insight_class.value,
                json.dumps(insight.model_dump(mode="json")),
                utc_timestamp(),
            ),
        )
        self.connection.commit()

    def store_graph_node(
        self,
        case_id: str,
        node_id: str,
        node_type: str,
        label: str,
        data: dict[str, Any],
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO graph_nodes (id, case_id, node_type, label, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (node_id, case_id, node_type, label, json.dumps(data), utc_timestamp()),
        )
        self.connection.commit()

    def store_graph_edge(
        self,
        case_id: str,
        edge_id: str,
        edge_type: str,
        source_node_id: str,
        target_node_id: str,
        weight: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO graph_edges
            (id, case_id, edge_type, source_node_id, target_node_id, weight, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                edge_id,
                case_id,
                edge_type,
                source_node_id,
                target_node_id,
                weight,
                json.dumps(metadata) if metadata is not None else None,
                utc_timestamp(),
            ),
        )
        self.connection.commit()

    def get_graph_nodes(
        self,
        case_id: str,
        node_type: str | None = None,
    ) -> list[dict[str, Any]]:
        query = (
            "SELECT id, case_id, node_type, label, data_json "
            "FROM graph_nodes WHERE case_id = ?"
        )
        params: tuple[str, ...] = (case_id,)
        if node_type is not None:
            query += " AND node_type = ?"
            params = (case_id, node_type)
        rows = self.connection.execute(query, params).fetchall()
        return [
            {
                "id": row[0],
                "case_id": row[1],
                "node_type": row[2],
                "label": row[3],
                "data": _json_object(row[4]),
            }
            for row in rows
        ]

    def get_graph_edges(
        self,
        case_id: str,
        edge_type: str | None = None,
    ) -> list[dict[str, Any]]:
        query = (
            "SELECT id, case_id, edge_type, source_node_id, target_node_id, weight, metadata_json "
            "FROM graph_edges WHERE case_id = ?"
        )
        params: tuple[str, ...] = (case_id,)
        if edge_type is not None:
            query += " AND edge_type = ?"
            params = (case_id, edge_type)
        rows = self.connection.execute(query, params).fetchall()
        return [
            {
                "id": row[0],
                "case_id": row[1],
                "edge_type": row[2],
                "source_node_id": row[3],
                "target_node_id": row[4],
                "weight": row[5],
                "metadata": _json_object(row[6]),
            }
            for row in rows
        ]

    def get_subgraph(
        self,
        case_id: str,
        center_node_id: str,
        depth: int = 2,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        all_nodes = {node["id"]: node for node in self.get_graph_nodes(case_id)}
        if center_node_id not in all_nodes:
            return [], []

        all_edges = self.get_graph_edges(case_id)
        if depth <= 0:
            return [all_nodes[center_node_id]], []

        visited_node_ids = {center_node_id}
        frontier = {center_node_id}
        visited_edge_ids: set[str] = set()

        for _ in range(depth):
            next_frontier: set[str] = set()
            for edge in all_edges:
                source_node_id = str(edge["source_node_id"])
                target_node_id = str(edge["target_node_id"])
                if source_node_id in frontier or target_node_id in frontier:
                    visited_edge_ids.add(str(edge["id"]))
                    if source_node_id in frontier and target_node_id not in visited_node_ids:
                        next_frontier.add(target_node_id)
                    if target_node_id in frontier and source_node_id not in visited_node_ids:
                        next_frontier.add(source_node_id)
            if not next_frontier:
                break
            visited_node_ids.update(next_frontier)
            frontier = next_frontier

        return (
            [all_nodes[node_id] for node_id in visited_node_ids],
            [edge for edge in all_edges if str(edge["id"]) in visited_edge_ids],
        )

    def store_case_memory(
        self,
        case_id: str,
        motif_type: str,
        content: str,
        score: float,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO case_memory (id, case_id, motif_type, content, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (new_id("memory"), case_id, motif_type, content, score, utc_timestamp()),
        )
        self.connection.commit()

    def search_case_memory(
        self,
        keywords: list[str],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        normalized_keywords = [keyword.lower() for keyword in keywords if keyword.strip()]
        if not normalized_keywords:
            return []

        rows = self.connection.execute(
            """
            SELECT id, case_id, motif_type, content, score
            FROM case_memory
            ORDER BY score DESC
            """
        ).fetchall()
        return [
            {
                "id": row[0],
                "case_id": row[1],
                "motif_type": row[2],
                "content": row[3],
                "score": row[4],
            }
            for row in rows
            if any(keyword in str(row[3]).lower() for keyword in normalized_keywords)
        ][:limit]

    def complete_case(self, case_id: str, dossier_path: str, metrics: InvestigationMetrics) -> None:
        timestamp = utc_timestamp()
        self.connection.execute(
            """
            UPDATE cases
            SET status = ?, updated_at = ?, dossier_path = ?, metrics_json = ?
            WHERE id = ?
            """,
            (
                "completed",
                timestamp,
                dossier_path,
                json.dumps(metrics.model_dump(mode="json")),
                case_id,
            ),
        )
        self.connection.commit()

    def fail_case(self, case_id: str, error_message: str) -> None:
        timestamp = utc_timestamp()
        payload = {"error": error_message[:500]}
        self.connection.execute(
            """
            UPDATE cases
            SET status = ?, updated_at = ?, metrics_json = ?
            WHERE id = ?
            """,
            ("failed", timestamp, json.dumps(payload), case_id),
        )
        self.connection.commit()
