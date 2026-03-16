from pathlib import Path

import pytest

from dossier.config import Settings


def test_default_settings() -> None:
    s = Settings()
    assert s.llm_provider == "demo"
    assert s.search_provider == "demo"
    assert s.search_max_results == 3
    assert s.planner_min_lanes == 2
    assert s.planner_max_lanes == 4
    assert s.max_parallel_lanes == 4
    assert s.fetch_enabled is False
    assert s.compression_enabled is True
    assert s.compression_max_tokens_per_packet == 500
    assert s.compression_max_total_tokens == 4000
    assert s.trigger_enabled is True
    assert s.trigger_min_confidence == 0.5
    assert s.shallow_synthesis_model is None
    assert s.beam_size == 16
    assert s.cross_domain_ratio == 0.2
    assert s.beam_model is None
    assert s.max_atoms_per_beam == 32


def test_database_path_from_url() -> None:
    s = Settings(DATABASE_URL="sqlite:///./data/test.db")
    assert s.database_path == Path("./data/test.db")


def test_database_path_rejects_non_sqlite() -> None:
    s = Settings(DATABASE_URL="postgres://localhost/db")
    with pytest.raises(ValueError, match="Only sqlite"):
        _ = s.database_path


def test_prepare_paths_creates_dirs(tmp_path: Path) -> None:
    s = Settings(
        DOSSIER_DATA_DIR=tmp_path / "data",
        OUTPUT_DIR=tmp_path / "out",
        DATABASE_URL=f"sqlite:///{tmp_path / 'data' / 'test.db'}",
    )
    s.prepare_paths()
    assert (tmp_path / "data").is_dir()
    assert (tmp_path / "out").is_dir()


def test_model_copy_overrides() -> None:
    s = Settings()
    s2 = s.model_copy(update={"fetch_enabled": True})
    assert s2.fetch_enabled is True
    assert s.fetch_enabled is False
