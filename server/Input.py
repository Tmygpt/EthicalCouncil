from mcp.server.fastmcp import FastMCP
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def prompt_science(question: str) -> str:
    """
    Science prompt
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract 3-6 keywords for scientific paper search. Focus strictly on technical and empirical concepts. Example: 'Formation of universe' → 'big bang, cosmic inflation, nucleosynthesis, dark matter, general relativity, astrophysics'."},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content.strip()

@mcp.tool()
async def prompt_religion(question: str) -> str:
    """
    Religion prompt
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract 3-6 keywords for philosophy, ethics, or religion papers. Focus on metaphysical, existential, or moral aspects of the topic. Example: 'Formation of universe' → 'creationism, divine origin, cosmology, first cause, theology of creation, metaphysics'."},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content.strip()
