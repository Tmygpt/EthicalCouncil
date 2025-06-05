from mcp.server.fastmcp import FastMCP
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_ENGINE = os.getenv("OPENAI_ENGINE")

mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def summarize_papers_science(papers: List[str], query: str) -> str:
    """Generate a summary of the provided papers for the user's query."""
    client = AsyncAzureOpenAI(
        api_key=OPENAI_API_KEY,
        azure_endpoint=OPENAI_API_BASE,
        api_version=OPENAI_API_VERSION,
        azure_deployment=OPENAI_ENGINE,
    )
    links = "\n".join(papers)
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant and a wise scholar seated in the Grand Council of Science. Every claim you make must be backed by a scientific paper provided by the user. You may interpret the findings but must always cite your source."
            },
            {
                "role": "user",
                "content": (
                    f"""Read the following papers:

                  {links}

                   The original user query is:  
                    {query}

                 Your task is to generate a clear, unbiased response that directly answers the user's query, focusing only on the **scientific findings, advantages, discoveries, and breakthroughs** discussed in the provided papers.

                  For every claim you make, you must provide a source from the papers using these strict rules:

                   - If the paper has two authors, reference as: [Surname of author & Surname of other author, Year]
                    - If the paper has three or more authors, reference as: [Surname of first author et al, Year]

                 Do not say 'as cited by' or use any indirect language like 'the author claims that...', or 'the paper states that...'.

                 Do not include the paper links inside the summary. Do not mention the paper links anywhere.

                  Write your response using simple, friendly language appropriate for a teenage audience.
                 """
                ),
            }
        ],
        model=OPENAI_ENGINE,
        temperature=0.5,
        max_tokens=1024,
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