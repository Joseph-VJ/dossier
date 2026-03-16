import pytest

from dossier.config import Settings
from dossier.contracts import ResearchLane
from dossier.search import (
    DemoSearchProvider,
    DuckDuckGoSearchProvider,
    TavilySearchProvider,
    build_search_provider,
)


def _lane() -> ResearchLane:
    return ResearchLane(name="Test Lane", query="test query", goal="test goal")


# --- DemoSearchProvider ---


def test_demo_returns_correct_count() -> None:
    provider = DemoSearchProvider()
    hits = provider.search("query", _lane(), 5)
    assert len(hits) == 5


def test_demo_returns_zero_when_limit_zero() -> None:
    provider = DemoSearchProvider()
    hits = provider.search("query", _lane(), 0)
    assert len(hits) == 0


def test_demo_hits_have_content() -> None:
    provider = DemoSearchProvider()
    hits = provider.search("query", _lane(), 2)
    for hit in hits:
        assert hit.title
        assert hit.url
        assert hit.snippet
        assert hit.content is not None
        assert hit.metadata["provider"] == "demo"


def test_demo_hit_url_contains_lane_id() -> None:
    lane = _lane()
    provider = DemoSearchProvider()
    hits = provider.search("query", lane, 1)
    assert lane.id in hits[0].url


# --- build_search_provider factory ---


def test_build_demo_provider() -> None:
    settings = Settings(SEARCH_PROVIDER="demo")
    provider = build_search_provider(settings)
    assert isinstance(provider, DemoSearchProvider)


def test_build_tavily_requires_key() -> None:
    settings = Settings(SEARCH_PROVIDER="tavily", SEARCH_API_KEY=None)
    with pytest.raises(ValueError, match="SEARCH_API_KEY"):
        build_search_provider(settings)


def test_build_tavily_with_key() -> None:
    settings = Settings(SEARCH_PROVIDER="tavily", SEARCH_API_KEY="test-key")
    provider = build_search_provider(settings)
    assert isinstance(provider, TavilySearchProvider)


def test_build_duckduckgo_provider() -> None:
    settings = Settings(SEARCH_PROVIDER="duckduckgo")
    provider = build_search_provider(settings)
    assert isinstance(provider, DuckDuckGoSearchProvider)


def test_build_unsupported_provider_raises() -> None:
    settings = Settings(SEARCH_PROVIDER="unknown")
    with pytest.raises(ValueError, match="Unsupported SEARCH_PROVIDER"):
        build_search_provider(settings)
