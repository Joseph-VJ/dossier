from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    dossier_env: str = Field(default="development", alias="DOSSIER_ENV")
    data_dir: Path = Field(default=Path("data"), alias="DOSSIER_DATA_DIR")
    output_dir: Path = Field(default=Path("data/dossiers"), alias="OUTPUT_DIR")
    database_url: str = Field(default="sqlite:///./data/dossier.db", alias="DATABASE_URL")

    llm_provider: str = Field(default="demo", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")
    llm_api_key: str | None = Field(default=None, alias="LLM_API_KEY")

    search_provider: str = Field(default="demo", alias="SEARCH_PROVIDER")
    search_api_key: str | None = Field(default=None, alias="SEARCH_API_KEY")
    search_max_results: int = Field(default=3, alias="SEARCH_MAX_RESULTS")

    planner_min_lanes: int = Field(default=2, alias="PLANNER_MIN_LANES")
    planner_max_lanes: int = Field(default=4, alias="PLANNER_MAX_LANES")
    max_parallel_lanes: int = Field(default=4, alias="MAX_PARALLEL_LANES")

    fetch_enabled: bool = Field(default=False, alias="FETCH_ENABLED")
    compression_enabled: bool = Field(default=True, alias="COMPRESSION_ENABLED")
    compression_max_tokens_per_packet: int = Field(
        default=500,
        alias="COMPRESSION_MAX_TOKENS_PER_PACKET",
    )
    compression_max_total_tokens: int = Field(default=4000, alias="COMPRESSION_MAX_TOTAL_TOKENS")
    trigger_enabled: bool = Field(default=True, alias="TRIGGER_ENABLED")
    trigger_min_confidence: float = Field(default=0.5, alias="TRIGGER_MIN_CONFIDENCE")
    shallow_synthesis_model: str | None = Field(default=None, alias="SHALLOW_SYNTHESIS_MODEL")
    beam_size: int = Field(default=16, ge=1, alias="BEAM_SIZE")
    cross_domain_ratio: float = Field(default=0.2, ge=0.0, le=1.0, alias="CROSS_DOMAIN_RATIO")
    beam_model: str | None = Field(default=None, alias="BEAM_MODEL")
    max_atoms_per_beam: int = Field(default=32, ge=1, alias="MAX_ATOMS_PER_BEAM")

    @property
    def database_path(self) -> Path:
        prefix = "sqlite:///"
        if not self.database_url.startswith(prefix):
            msg = "Only sqlite DATABASE_URL values are supported in V0."
            raise ValueError(msg)
        return Path(self.database_url.removeprefix(prefix))

    def prepare_paths(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
