import logging
from typing import List
from agents.science_summary_agent.summary import summarize_science_papers

logger = logging.getLogger(__name__)

class ScienceSummaryAgent:
    """Agent that provides a scientific summary of papers."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, papers: List[str], query: str) -> str:
        print("Scientific perspective:\n")
        return await summarize_science_papers(papers, query)
