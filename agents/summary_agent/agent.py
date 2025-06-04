import logging
from typing import List
from agents.summary_agent.summary import summarize_papers

logger = logging.getLogger(__name__)

class SummaryAgent:
    """Agent that summarizes scientific and religious papers."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, papers: List[str], query: str) -> str:
        """
        Summarize the provided papers based on the given query.
        
        Args:
            papers (List[str]): Links to the papers to summarize.
            query (str): The original query for context.
        
        Returns:
            str: A summary of the papers.
        """
        response = await summarize_papers(papers, query)
        return f"What the public thought:\n{response}"
