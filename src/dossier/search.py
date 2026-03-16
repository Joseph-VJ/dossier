from __future__ import annotations

from typing import Protocol

import httpx

from dossier.config import Settings
from dossier.contracts import ResearchLane, SearchHit


class SearchProvider(Protocol):
    def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
        ...


class DemoSearchProvider:
    def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
        hits: list[SearchHit] = []
        lane_focus = lane.goal.lower()
        for index in range(limit):
            ordinal = index + 1
            snippet = (
                f"Demo finding {ordinal} for '{query}'. "
                f"This lane focuses on {lane_focus}"
            )
            content = (
                f"{snippet}. The source indicates that decision quality depends on "
                f"checking evidence diversity, operational constraints, and hidden failure modes."
            )
            hits.append(
                SearchHit(
                    title=f"{lane.name} source {ordinal}",
                    url=f"https://example.local/{lane.id}/{ordinal}",
                    snippet=snippet,
                    content=content,
                    metadata={"provider": "demo"},
                )
            )
        return hits


class TavilySearchProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
        response = httpx.post(
            "https://api.tavily.com/search",
            json={
                "api_key": self.api_key,
                "query": query,
                "max_results": limit,
                "search_depth": "advanced",
                "include_answer": False,
            },
            timeout=20.0,
        )
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results", [])
        hits: list[SearchHit] = []
        for item in results[:limit]:
            hits.append(
                SearchHit(
                    title=str(item.get("title", lane.name)),
                    url=str(item.get("url", "")),
                    snippet=str(item.get("content", "")),
                    metadata={"provider": "tavily"},
                )
            )
        return hits


class DuckDuckGoSearchProvider:
    def search(self, query: str, lane: ResearchLane, limit: int) -> list[SearchHit]:
        from duckduckgo_search import DDGS

        hits: list[SearchHit] = []
        with DDGS() as client:
            results = client.text(query, max_results=limit)
            for item in results:
                hits.append(
                    SearchHit(
                        title=str(item.get("title", lane.name)),
                        url=str(item.get("href", "")),
                        snippet=str(item.get("body", "")),
                        metadata={"provider": "duckduckgo"},
                    )
                )
        return hits


def build_search_provider(settings: Settings) -> SearchProvider:
    provider = settings.search_provider.lower()
    if provider == "demo":
        return DemoSearchProvider()
    if provider == "tavily":
        if not settings.search_api_key:
            msg = "SEARCH_API_KEY is required for Tavily."
            raise ValueError(msg)
        return TavilySearchProvider(settings.search_api_key)
    if provider == "duckduckgo":
        return DuckDuckGoSearchProvider()
    msg = f"Unsupported SEARCH_PROVIDER '{settings.search_provider}'."
    raise ValueError(msg)

