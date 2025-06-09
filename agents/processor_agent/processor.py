import logging
import asyncio
from typing import List
import requests
import fitz
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("processor", transport="stdio")
logger = logging.getLogger(__name__)

async def _fetch_text(url: str) -> str:
    """Fetch and parse raw text from a URL.

    If the content is a PDF, use ``PyMuPDF`` to extract the text. Otherwise,
    parse the HTML with ``BeautifulSoup``.
    """

    try:
        response = await asyncio.to_thread(requests.get, url, timeout=30)
        response.raise_for_status()
        ctype = response.headers.get("Content-Type", "").lower()

        if "pdf" in ctype or url.lower().endswith(".pdf"):
            with fitz.open(stream=response.content, filetype="pdf") as doc:
                texts = [page.get_text() for page in doc]
            return "\n".join(texts)

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""

async def _process_url(url: str, splitter: RecursiveCharacterTextSplitter) -> List[str]:
    text = await _fetch_text(url)
    if not text:
        return []
    chunks = splitter.split_text(text)
    return chunks

@mcp.tool()
async def process_papers(urls: List[str]) -> List[str]:
    """Fetch URLs and return list of text chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=6000, chunk_overlap=500)
    tasks = [asyncio.create_task(_process_url(url, splitter)) for url in urls]
    results = await asyncio.gather(*tasks)
    # flatten
    chunks: List[str] = []
    for res in results:
        chunks.extend(res)
    return chunks