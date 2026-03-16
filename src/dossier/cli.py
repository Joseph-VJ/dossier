from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from dossier.config import Settings
from dossier.db import SqliteRepository
from dossier.runtime import InvestigationService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dossier", description="Dossier V0 investigation scaffold.")
    subparsers = parser.add_subparsers(dest="command")

    investigate_parser = subparsers.add_parser("investigate", help="Run an investigation.")
    investigate_parser.add_argument("question", help="Question to investigate.")
    investigate_parser.add_argument("--data-dir", type=Path, default=None, help="Override data dir.")
    investigate_parser.add_argument("--output-dir", type=Path, default=None, help="Override dossier output dir.")
    investigate_parser.add_argument("--fetch", action="store_true", help="Enable page fetching.")

    subparsers.add_parser("init-db", help="Initialize the SQLite database.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "init-db":
        settings = Settings()
        settings.prepare_paths()
        SqliteRepository(settings.database_path).initialize()
        print(f"Initialized database at {settings.database_path}")
        return 0

    if args.command == "investigate":
        settings = Settings()
        updates: dict[str, object] = {}
        if args.data_dir is not None:
            updates["data_dir"] = args.data_dir
            default_database_url = Settings.model_fields["database_url"].default
            if settings.database_url == default_database_url:
                updates["database_url"] = f"sqlite:///{args.data_dir / 'dossier.db'}"
        if args.output_dir is not None:
            updates["output_dir"] = args.output_dir
        if args.fetch:
            updates["fetch_enabled"] = True
        if updates:
            settings = settings.model_copy(update=updates)
        service = InvestigationService(settings)
        result = service.investigate(args.question)
        print(f"Case ID: {result.case_id}")
        print(f"Dossier: {result.dossier_path}")
        print(f"Insights: {len(result.insights)}")
        return 0

    parser.print_help()
    return 1
