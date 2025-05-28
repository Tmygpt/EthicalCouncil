from typing import List, Dict, Any
import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# === Load environment variables and init MCP ===
load_dotenv()
CORE_API_KEY = os.getenv("CORE_API_KEY")
CORE_API_URL = "https://api.core.ac.uk/v3/search/outputs"
mcp = FastMCP("collector")


# === CORE API Wrapper ===
async def search_outputs_by_keywords(keywords: str, limit: int = 5) -> List[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {CORE_API_KEY}"
    }
    params = {
        "q": f'fullText:"{keywords}" AND _exists_:fullText',
        "limit": limit
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(CORE_API_URL, headers=headers, params=params, timeout=20.0)
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            print(f"[CORE API ERROR] {e}")
            return []


# === MCP Tool ===
@mcp.tool()
async def get_research_papers(topic: str) -> str:
    """
    Retrieve scholarly articles from CORE based on a religious or ethical keyword/topic.
    Displays only title, abstract, and link.
    """
    results = await search_outputs_by_keywords(topic)

    if not results:
        return "No relevant research papers were found for this topic."

    formatted = []
    for paper in results:
        title = paper.get("title", "Untitled")
        abstract = paper.get("abstract", "No abstract available")
        url = paper.get("doi") or paper.get("url", "Unavailable")

        formatted.append(f"""📘 **Title**: {title}
📄 **Abstract**: {abstract}
🔗 **Link**: {url}
""")

    return "\n---\n".join(formatted)