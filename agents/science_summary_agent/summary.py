from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from typing import List

mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def summarize_science_papers(papers: List[str], query: str) -> str:
    """Generate a scientific summary of the provided papers."""
    client = AsyncGroq()
    links = "\n".join(papers)
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Focus strictly on the scientific "
                    "aspect of the topic. Every claim must be backed by one of the "
                    "provided research papers. Do not discuss moral, ethical or "
                    "religious views. Cite sources inline using the format "
                    "[Author, Year]. Do not include a bibliography or the URLs."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Read through the following papers:\n\n{links}\n\n"
                    f"The original query was: {query}. "
                    f"Provide a concise scientific summary strictly based on these "
                    f"papers."
                ),
            },
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
    )

    summary = ""
    async for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        summary += delta
        print(delta, end="", flush=True)

    return summary
