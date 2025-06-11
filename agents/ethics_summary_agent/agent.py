import logging
from typing import List
from agents.ethics_summary_agent.ethics_summary import summarize_papers_ethics

logger = logging.getLogger(__name__)

class SummaryAgent:
    """Agent that answers ethical questions using RAG."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, urls: List[str], query: str) -> str:
        """Summarize ethical aspects of the papers referenced by the URLs."""
        print("What the Ethics Sage thinks:\n")
        await summarize_papers_ethics(urls, query)
        return ""
