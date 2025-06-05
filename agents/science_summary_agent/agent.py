import logging
from typing import List
from agents.science_summary_agent.science_summary import summarize_papers_science

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
        print("What the Science Wizard thinks:\n")
        await summarize_papers_science(papers, query)
        return ""
