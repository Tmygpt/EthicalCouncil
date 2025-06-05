from typing import List, Dict
import os
import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("collector", transport="stdio")

ARXIV_API_URL = "http://export.arxiv.org/api/query"
CROSSREF_API_URL = "https://api.crossref.org/works"
CROSSREF_MAILTO = os.environ.get("CROSSREF_MAILTO", "openaccess@ethicalcouncil.org")

papers_list: List[str] = []

# SCIENCE:
def show_science_response(xml_text: str) -> List[Dict]:
    url = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)
    results = []

    for paper in root.findall("atom:entry", url):
        title = paper.find("atom:title", url).text.strip()
        authors = [author.find("atom:name", url).text for author in paper.findall("atom:author", url)]
        link = next((l.attrib["href"] for l in paper.findall("atom:link", url) if l.attrib.get("type") == "application/pdf"),"No PDF link",)
        papers_list.append(link)
        results.append({
            "title": title,
            "authors": ", ".join(authors),
            "link": link,
            "topics": []
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

def show_crossref_response(data: Dict, limit: int) -> List[Dict]:
    """Parse Crossref API response data."""
    results = []

    items = data.get("message", {}).get("items", [])
    for item in items[:limit]:
        titles = item.get("title", [])
        title = titles[0] if titles else "No Title"

        pdf_link = None
        for link in item.get("link", []):
            if link.get("content-type") == "application/pdf" and link.get("URL"):
                pdf_link = link["URL"]
                break
        if not pdf_link:
            url = item.get("URL")
            if isinstance(url, str) and url.endswith(".pdf"):
                pdf_link = url
            else:
                pdf_link = url

        if pdf_link:
            papers_list.append(pdf_link)

        results.append({
            "title": title,
            "link": pdf_link or "No Link",
            "topics": []
        })

    return results

async def get_crossref_articles(topic: str, limit: int = 7) -> List[Dict]:
    """Retrieve papers from arXiv and the Crossref API."""
    arxiv_results = await get_arxiv_articles(topic, max_results=limit)

    params = {
        "query": topic,
        "rows": limit,
    }
    if CROSSREF_MAILTO:
        params["mailto"] = CROSSREF_MAILTO

    headers = {"User-Agent": f"ethicalcouncil/1.0 (mailto:{CROSSREF_MAILTO})"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(CROSSREF_API_URL, params=params, headers=headers, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            cr_results = show_crossref_response(data, limit)
        except Exception as e:
            print(f"[Crossref API ERROR] {e}")
            cr_results = []

    return (arxiv_results + cr_results)[:limit]
        
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
    results = await get_crossref_articles(topic)

    if not results:
        return "No relevant research papers found."

    formatted = []
    for paper in results:
        formatted.append(f"""Title: {paper['title']}
Link: {paper['link']}
Topics: {', '.join(paper.get('topics', []))}
""")

    return "\n---\n".join(formatted)