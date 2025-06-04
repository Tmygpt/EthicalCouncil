import logging
from typing import List
from agents.ethics_summary_agent.summary import summarize_ethics_papers

logger = logging.getLogger(__name__)

class EthicsSummaryAgent:
    """Agent that provides an ethical/religious summary of papers."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, papers: List[str], query: str) -> str:
        print("Ethical perspective:\n")
        return await summarize_ethics_papers(papers, query)
