from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from typing import List

mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def summarize_papers_science(papers: List[str], query: str) -> str:
    """Generate a summary of the provided papers for the user's query."""
    client = AsyncGroq()
    links = "\n".join(papers)
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant and an old, wise wizard seated in a council. Every claim you make must be backed by a scientific paper or religious text. You can make your own interpretations, but you must always provide a source.", 
            },
            {
                "role": "user",
                "content": (
                   f"""Read the following papers:

                    {links}

                    The original user query is:  
                    {query}

                    Your task is to generate a clear, unbiased response that directly answers the user's query, focusing only on the scientific findings, methodologies, and conclusions discussed in the provided papers.

                    For every claim you make, you must provide a source from the papers using these strict rules:

                    - If the paper has two authors, reference as: (Surname of author & Surname of other author, Year)
                    - If the paper has three or more authors, reference as: (Surname of first author et al, Year)

                    Do not say 'as cited by' or use any indirect language like 'the author claims that...', or even 'the paper states that...'.

                    Do not include the paper links inside the summary.

                    Write your response using simple, friendly language appropriate for a teenage audience."""

                ),
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=True,
    )

    async for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)

    return ""

"""Incase i want to use the return value later:
summary = ""
    async for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
    # Print the incremental deltas returned by the LLM.
    return summary"""