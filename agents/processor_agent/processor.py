import logging
import asyncio
from typing import List
import requests
import fitz 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("processor", transport="stdio")
logger = logging.getLogger(__name__)

async def _download_pdf(url: str) -> bytes:
    logger.info(f"Downloading {url}")
    try:
        response = await asyncio.to_thread(requests.get, url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.warning(f"Failed to download {url}: {e}")
        return b""

async def _extract_text(pdf_bytes: bytes) -> str:
    if not pdf_bytes:
        return ""
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            texts = [page.get_text() for page in doc]
        text = "\n".join(texts)
        # basic cleanup
        text = " ".join(text.split())
        return text
    except Exception as e:
        logger.warning(f"Failed to parse PDF: {e}")
        return ""

async def _process_url(url: str, splitter: RecursiveCharacterTextSplitter) -> List[str]:
    pdf_bytes = await _download_pdf(url)
    text = await _extract_text(pdf_bytes)
    if not text:
        return []
    chunks = splitter.split_text(text)
    return chunks

@mcp.tool()
async def process_papers(urls: List[str]) -> List[str]:
    """Download PDFs and return list of text chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=6000, chunk_overlap=500)
    tasks = [asyncio.create_task(_process_url(url, splitter)) for url in urls]
    results = await asyncio.gather(*tasks)
    # flatten
    chunks: List[str] = []
    for res in results:
        chunks.extend(res)
    return chunks