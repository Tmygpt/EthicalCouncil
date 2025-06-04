from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def mediate_summaries(science_summary: str, ethics_summary: str, query: str) -> str:
    """Combine scientific and ethical summaries into a balanced response."""
    client = AsyncGroq()
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a mediator who combines scientific and ethical perspectives "
                    "into one concise answer. Do not include references or a bibliography."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"User query: {query}\n\n"
                    f"Scientific summary:\n{science_summary}\n\n"
                    f"Ethical summary:\n{ethics_summary}\n\n"
                    "Provide a short balanced overview addressing the question."
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
