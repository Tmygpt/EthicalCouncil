from typing import List, Dict
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("collector")

OPENALEX_URL = "https://api.openalex.org/works"

async def search_openalex(topic: str, limit: int = 5) -> List[Dict]:
    params = {
        "search": topic,
        "per-page": limit
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENALEX_URL, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("results", []):
                title = item.get("title", "Untitled")
                # abstract = item.get("abstract", "No abstract available")
                doi = item.get("doi", "")
                authors = ", ".join(
                    a["author"]["display_name"]
                    for a in item.get("authorships", [])
                    if a.get("author", {}).get("display_name")
                )
                url = item.get("primary_location", {}).get("source", {}).get("url", "Unavailable")

                results.append({
                    "title": title,
                 #   "abstract": abstract,
                 #   "authors": authors,
                    "link": doi or url
                })

            return results
        except Exception as e:
            print(f"[OpenAlex API ERROR] {e}")
            return []

@mcp.tool()
async def get_research_papers(topic: str) -> str:
    results = await search_openalex(topic)
    return f"Got {len(results)} results\n" + "\n".join(p['title'] for p in results)
