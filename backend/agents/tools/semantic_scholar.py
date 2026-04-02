from __future__ import annotations

import httpx

SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1"


async def search_semantic_scholar(
    query: str,
    max_results: int = 10,
    fields: list[str] | None = None,
) -> list[dict]:
    """Search Semantic Scholar for papers matching the query.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.
        fields: Paper fields to retrieve. Defaults to common fields.

    Returns:
        List of paper metadata dictionaries.
    """
    if fields is None:
        fields = ["title", "abstract", "authors", "year", "citationCount", "externalIds", "url"]

    params = {
        "query": query,
        "limit": min(max_results, 100),
        "fields": ",".join(fields),
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEMANTIC_SCHOLAR_BASE_URL}/paper/search",
            params=params,
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()

    papers = []
    for item in data.get("data", []):
        papers.append(
            {
                "semantic_scholar_id": item.get("paperId", ""),
                "title": item.get("title", ""),
                "abstract": item.get("abstract", ""),
                "authors": [a.get("name", "") for a in item.get("authors", [])],
                "year": item.get("year"),
                "citation_count": item.get("citationCount", 0),
                "doi": item.get("externalIds", {}).get("DOI", ""),
                "url": item.get("url", ""),
            }
        )

    return papers
