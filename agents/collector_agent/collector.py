from typing import List, Dict
import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import time
import random
import asyncio

mcp = FastMCP("collector", transport="stdio")

ARXIV_API_URL = "http://export.arxiv.org/api/query"

GSCHOLAR_BASE_URL = "https://scholar.google.com/scholar"

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

def scrape_scholar_articles(query: str, num_pages: int = 2) -> List[Dict]:
    """Scrape Google Scholar for the given query."""
    articles = []
    page = 0

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        )
    }

    while page < num_pages:
        url = f"{GSCHOLAR_BASE_URL}?start={page*10}&q={query}&hl=en&as_sdt=0,5"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page+1}: Status {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="gs_ri")

        for result in results:
            title_tag = result.find("h3", class_="gs_rt")
            title = title_tag.text if title_tag else "No Title"

            authors_tag = result.find("div", class_="gs_a")
            authors = authors_tag.text if authors_tag else "No Authors"

            link_tag = title_tag.find("a") if title_tag else None
            link = link_tag["href"] if link_tag else "No Link"

            if link:
                papers_list.append(link)

            articles.append(
                {
                    "title": title,
                    "authors": authors,
                    "link": link,
                    "topics": [],
                }
            )

        page += 1
        time.sleep(random.uniform(1, 3))

    return articles


async def get_scholar_articles(topic: str, limit: int = 7) -> List[Dict]:
    """Retrieve papers from arXiv and Google Scholar."""
    arxiv_results = await get_arxiv_articles(topic, max_results=limit)
    scholar_results = await asyncio.to_thread(scrape_scholar_articles, topic, 2)
    return (arxiv_results + scholar_results)[:limit]
        
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
    results = await get_scholar_articles(topic)

    if not results:
        return "No relevant research papers found."

    formatted = []
    for paper in results:
        formatted.append(f"""Title: {paper['title']}
Link: {paper['link']}
Topics: {', '.join(paper.get('topics', []))}
""")

    return "\n---\n".join(formatted)