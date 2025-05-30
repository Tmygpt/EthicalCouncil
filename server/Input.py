import httpx
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

mcp = FastMCP("input-agent")

async def get_keywords_from_openai(prompt: str) -> str:
    """Use OpenAI to convert a natural question into keywords."""
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Convert the question into 3–6 academic search keywords."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

async def call_collector_agent(keywords: str) -> str:
    """Make an A2A request to the collector agent."""
    url = f"http://localhost:3100/a2a/collector/get_research_papers"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"topic": keywords}, timeout=15.0)
        response.raise_for_status()
        return response.json().get("result", "[No response from collector]")

@mcp.tool()
async def route_query(question: str) -> str:
    """Reformat the query using OpenAI and send to the collector agent via A2A."""
    keywords = await get_keywords_from_openai(question)
    result = await call_collector_agent(keywords)

    return f"""🔎 Reformatted Query: {keywords}

📚 Collector Agent Response:
{result}
"""
