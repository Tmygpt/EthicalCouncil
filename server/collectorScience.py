from typing import List, Dict
import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("collectorScience", transport="stdio")

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def parse_arxiv_response(xml_text: str) -> List[Dict]:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)
    entries = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        authors = [author.find("atom:name", ns).text for author in entry.findall("atom:author", ns)]
        link = next((l.attrib["href"] for l in entry.findall("atom:link", ns) if l.attrib.get("type") == "application/pdf"), "No PDF link")

        entries.append({
            "title": title,
            "authors": ", ".join(authors),
            "link": link
        })
    return entries


# === ArXiv API Fetcher ===
async def fetch_arxiv_articles(topic: str, max_results: int = 7) -> List[Dict]:
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": max_results
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ARXIV_API_URL, params=params, timeout=15.0)
            response.raise_for_status()
            return parse_arxiv_response(response.text)
        except Exception as e:
            print(f"[arXiv API ERROR] {e}")
            return []


@mcp.tool()
async def get_research_papers(topic: str) -> str:
    """
    Get arxiv results
    """
    results = await fetch_arxiv_articles(topic)

    if not results:
        return "No relevant research papers found"

    formatted = []
    for paper in results:
        formatted.append(f""" Title: {paper['title']}
        Authors: {paper['authors']}
        Link: {paper['link']}
        """)

    return "\n---\n".join(formatted)