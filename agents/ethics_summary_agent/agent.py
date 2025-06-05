import logging
from typing import List
from agents.ethics_summary_agent.ethics_summary import summarize_papers_ethics

logger = logging.getLogger(__name__)

class SummaryAgent:
    """Agent that summarizes ethical content from papers."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, papers: List[str], query: str) -> str:
        """Summarize the provided papers focusing on ethical discussion."""
        print("What the Ethics Sage thinks:\n")
        await summarize_papers_ethics(papers, query)
        return ""