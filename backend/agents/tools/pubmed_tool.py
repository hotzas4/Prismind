from __future__ import annotations

import httpx


async def search_pubmed(query: str, max_results: int = 10, api_key: str | None = None) -> list[dict]:
    """Search PubMed for papers matching the query using the NCBI E-utilities API.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.
        api_key: Optional NCBI API key for higher rate limits.

    Returns:
        List of paper metadata dictionaries.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    params: dict[str, str | int] = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "usehistory": "y",
    }
    if api_key:
        params["api_key"] = api_key

    async with httpx.AsyncClient() as client:
        # Step 1: Search for IDs
        search_response = await client.get(f"{base_url}/esearch.fcgi", params=params)
        search_response.raise_for_status()
        search_data = search_response.json()

        ids = search_data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        # Step 2: Fetch summaries for the IDs
        summary_params: dict[str, str] = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
        }
        if api_key:
            summary_params["api_key"] = api_key

        summary_response = await client.get(f"{base_url}/esummary.fcgi", params=summary_params)
        summary_response.raise_for_status()
        summary_data = summary_response.json()

    papers = []
    for uid, doc in summary_data.get("result", {}).items():
        if uid == "uids":
            continue
        papers.append(
            {
                "pubmed_id": uid,
                "title": doc.get("title", ""),
                "authors": [a.get("name", "") for a in doc.get("authors", [])],
                "journal": doc.get("fulljournalname", ""),
                "published": doc.get("pubdate", ""),
                "doi": doc.get("elocationid", ""),
            }
        )

    return papers
