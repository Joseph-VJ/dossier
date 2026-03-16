from pathlib import Path

import pytest

from dossier.cli import main


def test_cli_investigate_creates_dossier(tmp_path: Path) -> None:
    exit_code = main(
        [
            "investigate",
            "Should Acme acquire Beta?",
            "--data-dir",
            str(tmp_path / "data"),
            "--output-dir",
            str(tmp_path / "data" / "dossiers"),
        ]
    )

    assert exit_code == 0
    dossier_files = list((tmp_path / "data" / "dossiers").glob("*.md"))
    assert len(dossier_files) == 1


def test_cli_init_db(tmp_path: Path, monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.setenv("DOSSIER_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'data' / 'test.db'}")
    exit_code = main(["init-db"])
    assert exit_code == 0
    assert (tmp_path / "data" / "test.db").exists()


def test_cli_no_command_returns_1() -> None:
    exit_code = main([])
    assert exit_code == 1


def test_cli_investigate_with_fetch_flag(tmp_path: Path) -> None:
    exit_code = main(
        [
            "investigate",
            "Test question",
            "--data-dir",
            str(tmp_path / "data"),
            "--output-dir",
            str(tmp_path / "out"),
            "--fetch",
        ]
    )
    assert exit_code == 0


def test_cli_data_dir_sets_default_database_path(
    tmp_path: Path,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DOSSIER_DATA_DIR", raising=False)
    monkeypatch.delenv("OUTPUT_DIR", raising=False)

    data_dir = tmp_path / "custom-data"
    exit_code = main(
        [
            "investigate",
            "Where should the DB go?",
            "--data-dir",
            str(data_dir),
            "--output-dir",
            str(tmp_path / "out"),
        ]
    )

    assert exit_code == 0
    assert (data_dir / "dossier.db").exists()
