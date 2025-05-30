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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Convert this question into 3-6 keywords that can be used to search for research papers relevant to this. The keywords should focus on the scientific aspect and be enough to be displayed in relevant titles of scientific research papers"},
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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Convert this question into 3-6 keywords that can be used to search for research papers relevant to this. The keywords should focus on the ethical and moral aspect and be enough to be displayed in relevant titles of philosophical/ethical/moral/religious research papers"},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content.strip()
