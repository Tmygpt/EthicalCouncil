from typing import List, Dict
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("collectorReligion", transport="stdio")

OPENALEX_API_URL = "https://api.openalex.org/works"

def get_response(data: Dict) -> List[Dict]:
    results = []

    for paper in data.get("results", []):
        title = paper.get("title", "No Title")
        link = paper.get("primary_location", {}).get("landing_page_url", "No Link")
        topics = [concept.get("display_name", "") for concept in paper.get("concepts", [])]

        results.append({
            "title": title,
            "link": link,
            "topics": topics
        })

    return results

# Call OpenAlex API
async def show_response(topic: str, limit: int = 7) -> List[Dict]:
    params = {
        "search": topic,
        "per_page": limit
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENALEX_API_URL, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            return get_response(data)
        except Exception as e:
            print(f"[OpenAlex API ERROR] {e}")
            return []

# MCP Tool
@mcp.tool()
async def get_research_papers(topic: str) -> str:
    """
    Get openalex results
    """
    results = await show_response(topic)

    if not results:
        return "No relevant research papers were found."

    formatted = []
    for paper in results:
        formatted.append(f"""Title: {paper['title']}
Link: {paper['link']}
Topics: {', '.join(paper['topics'])}
""")

    return "\n---\n".join(formatted)