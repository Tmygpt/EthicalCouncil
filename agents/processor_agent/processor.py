import logging
import asyncio
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("processor", transport="stdio")
logger = logging.getLogger(__name__)

async def _fetch_text(url: str) -> str:
    """Fetch and parse raw text from a URL using UnstructuredURLLoader."""
    try:
        loader = UnstructuredURLLoader(urls=[url])
        docs = await asyncio.to_thread(loader.load)
        return "\n".join(d.page_content for d in docs)
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