from mcp.server.fastmcp import FastMCP
from openai import AsyncAzureOpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import asyncio
import os
from typing import List

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_ENGINE = os.getenv("OPENAI_ENGINE")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "research-paper-summary")

mcp = FastMCP("input", transport="stdio")

client = AsyncAzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_API_BASE,
    api_version=OPENAI_API_VERSION,
    azure_deployment=OPENAI_ENGINE,
)

pc = Pinecone(api_key=PINECONE_API_KEY)

@mcp.tool()
async def summarize_papers_science(urls: List[str], query: str) -> str:
    """Answer the query using documents stored in Pinecone."""
    index = pc.Index(host=PINECONE_HOST)
    embed = await client.embeddings.create(input=[query], model="text-embedding-3-large")
    vector = embed.data[0].embedding
    res = await asyncio.to_thread(index.query, vector=vector, top_k=10, namespace=PINECONE_INDEX_NAME, include_metadata=True, filter={"source": {"$in": urls}})
    chunks = [m["metadata"].get("text", "") for m in res.get("matches", []) if m.get("metadata")]
    context = "\n\n".join(chunks)
    system_prompt = (
        "You are a helpful assistant and a wise scholar seated in the Grand Council of Science. "
        "Every claim you make must be backed by a scientific paper provided by the user. "
        "You may interpret the findings but must always cite your source."
    )
    final_prompt = (
        f"Use the following excerpts to answer the question.\n\n{context}\n\nQuestion: {query}\n\n"
        "Focus only on scientific findings. Cite your sources using the metadata provided."
    )
    response = await client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": final_prompt}],
        model=OPENAI_ENGINE,
        temperature=0.5,
        max_tokens=1024,
        stream=True,
    )
    async for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
    return ""
