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
async def summarize_papers_ethics(papers: List[str], query: str) -> str:
    """Generate a summary using a MapReduce-style approach."""
    client = AsyncAzureOpenAI(
        api_key=OPENAI_API_KEY,
        azure_endpoint=OPENAI_API_BASE,
        api_version=OPENAI_API_VERSION,
        azure_deployment=OPENAI_ENGINE,
    )

    system_prompt = (
        "You are a helpful assistant and a wise elder seated in the Council of Ethics. "
        "Every claim you make must be backed by a scientific paper or religious text provided by the user. "
        "You may interpret the findings but must always cite your source."
    )

    chunk_summaries: List[str] = []
    for chunk in papers:
        resp = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk},
            ],
            model=OPENAI_ENGINE,
            temperature=0.5,
            max_tokens=256,
            top_p=1,
        )
        chunk_summaries.append(resp.choices[0].message.content.strip())

    combined = "\n".join(chunk_summaries)

    final_prompt = (
        f"Read the following summaries of the paper excerpts:\n\n{combined}\n\n"
        f"The original user query is:\n{query}\n\n"
        "Your task is to generate a clear, unbiased response that directly answers the user's query, "
        "focusing only on the **ethical dilemmas, moral conflicts, value-based implications, or philosophical concerns** discussed in the provided papers.\n\n"
        "For every claim you make, you must provide a source from the papers using these strict rules:\n"
        "- If the paper has two authors, reference as: [Surname of author & Surname of other author, Year]\n"
        "- If the paper has three or more authors, reference as: [Surname of first author et al, Year]\n\n"
        "Do not say 'as cited by' or use any indirect language like 'the author claims that...', or 'the paper states that...'.\n"
        "Do not include the paper links inside the summary. Do not mention the paper links anywhere.\n"
        "Write your response using simple, friendly language appropriate for a teenage audience."
    )

    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt},
        ],
        model=OPENAI_ENGINE,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=True,
    )

    async for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)

    return ""