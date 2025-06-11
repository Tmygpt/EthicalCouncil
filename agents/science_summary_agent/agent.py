import logging
from typing import List
from agents.science_summary_agent.science_summary import summarize_papers_science

logger = logging.getLogger(__name__)

class SummaryAgent:
    """Agent that answers scientific questions using RAG."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, urls: List[str], query: str) -> str:
        """Summarize the papers referenced by the URLs for the given query."""
        print("What the Science Wizard thinks:\n")
        await summarize_papers_science(urls, query)
        return ""
