from __future__ import annotations

import arxiv


async def search_arxiv(query: str, max_results: int = 10) -> list[dict]:
    """Search arXiv for papers matching the query.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        List of paper metadata dictionaries.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in client.results(search):
        papers.append(
            {
                "arxiv_id": result.entry_id,
                "title": result.title,
                "abstract": result.summary,
                "authors": [str(a) for a in result.authors],
                "published": result.published.isoformat() if result.published else None,
                "categories": result.categories,
                "pdf_url": result.pdf_url,
            }
        )

    return papers
