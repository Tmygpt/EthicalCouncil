from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from typing import List

mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def summarize_ethics_papers(papers: List[str], query: str) -> str:
    """Generate an ethical or moral summary of the provided papers."""
    client = AsyncGroq()
    links = "\n".join(papers)
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Focus on the ethical, moral and "
                    "religious perspective of the user's question. Every claim "
                    "must reference one of the provided works. Use the citation "
                    "format [Author, Year]. Do not include a bibliography or URLs." 
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Read through the following papers:\n\n{links}\n\n"
                    f"The original query was: {query}. "
                    f"Provide a concise ethical/religious summary strictly based "
                    f"on these references."
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
