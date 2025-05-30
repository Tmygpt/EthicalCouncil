from typing import List, Dict
import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("collector", transport="stdio")

ARXIV_API_URL = "http://export.arxiv.org/api/query"
OPENALEX_API_URL = "https://api.openalex.org/works"

# SCIENCE:
def show_science_response(xml_text: str) -> List[Dict]:
    url = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)
    results = []

    for paper in root.findall("atom:entry", url):
        title = paper.find("atom:title", url).text.strip()
        authors = [author.find("atom:name", url).text for author in paper.findall("atom:author", url)]
        link = next((l.attrib["href"] for l in paper.findall("atom:link", url) if l.attrib.get("type") == "application/pdf"), "No PDF link")

        results.append({
            "title": title,
            "authors": ", ".join(authors),
            "link": link
        })
    return results

async def get_arxiv_articles(topic: str, max_results: int = 7) -> List[Dict]:
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": max_results
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ARXIV_API_URL, params=params, timeout=15.0)
            response.raise_for_status()
            return show_science_response(response.text)
        except Exception as e:
            print(f"[arXiv API ERROR] {e}")
            return []
        
# RELIGION:

def show_religion_response(data: Dict) -> List[Dict]:
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

async def get_openalex_articles(topic: str, limit: int = 7) -> List[Dict]:
    params = {
        "search": topic,
        "per_page": limit
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENALEX_API_URL, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            return show_religion_response(data)
        except Exception as e:
            print(f"[OpenAlex API ERROR] {e}")
            return []
        
@mcp.tool()
async def get_science_papers(topic: str) -> str:
    """
    Get Scientific Papers
    """
    results = await get_arxiv_articles(topic)

    if not results:
        return "No relevant research papers found"

    formatted = []
    for paper in results:
        formatted.append(f""" Title: {paper['title']}
        Authors: {paper['authors']}
        Link: {paper['link']}
        """)

    return "\n---\n".join(formatted)

@mcp.tool()
async def get_religion_papers(topic: str) -> str:
    """
    Get Religious Papers
    """
    results = await get_openalex_articles(topic)

    if not results:
        return "No relevant research papers found."

    formatted = []
    for paper in results:
        formatted.append(f"""Title: {paper['title']}
Link: {paper['link']}
Topics: {', '.join(paper['topics'])}
""")

    return "\n---\n".join(formatted)