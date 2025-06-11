import logging
import asyncio
from typing import List
import requests
import fitz
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from mcp.server.fastmcp import FastMCP
from openai import AsyncAzureOpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "research-paper-summary")

mcp = FastMCP("processor", transport="stdio")
logger = logging.getLogger(__name__)

client = AsyncAzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_API_BASE,
    api_version=OPENAI_API_VERSION,
)

pc = Pinecone(api_key=PINECONE_API_KEY)

async def _fetch_text(url: str) -> str:
    """Download and extract raw text from a URL or PDF."""
    try:
        response = await asyncio.to_thread(requests.get, url, timeout=30)
        response.raise_for_status()
        ctype = response.headers.get("Content-Type", "").lower()
        if "pdf" in ctype or url.lower().endswith(".pdf"):
            with fitz.open(stream=response.content, filetype="pdf") as doc:
                texts = [page.get_text() for page in doc]
            return "\n".join(texts)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n")
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""

async def _upload_chunks(url: str, splitter: RecursiveCharacterTextSplitter) -> int:
    index = pc.Index(host=PINECONE_HOST)
    text = await _fetch_text(url)
    if not text:
        return 0
    chunks = splitter.split_text(text)
    count = 0
    for i, chunk in enumerate(chunks):
        emb = await client.embeddings.create(input=[chunk], model="text-embedding-3-large")
        vec_id = f"{hash(url)}-{i}"
        metadata = {"source": url, "text": chunk}
        await asyncio.to_thread(index.upsert, vectors=[{"id": vec_id, "values": emb.data[0].embedding, "metadata": metadata}], namespace=PINECONE_INDEX_NAME)
        count += 1
    return count

@mcp.tool()
async def process_papers(urls: List[str]) -> str:
    """Fetch the provided URLs and upload their contents to Pinecone."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    total = 0
    for url in urls:
        total += await _upload_chunks(url, splitter)
    return f"Uploaded {total} chunks"
