import logging
from agents.collector_agent.collector import (
    get_science_papers,
    get_religion_papers,
    papers_list as collector_papers_list,
)

logger = logging.getLogger(__name__)

class CollectorAgent:
    """Agent that fetches science and religious papers given keywords."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self) -> None:
        self.papers_list: list[str] = []

    async def invoke(self, science: str, ethics: str) -> str:
        collector_papers_list.clear()
        science_res = await get_science_papers(science) if science else ""
        ethics_res = await get_religion_papers(ethics) if ethics else ""
        self.papers_list = collector_papers_list.copy()
        return f"Science Papers:\n{science_res}\n---\nReligious Papers:\n{ethics_res}"
    
    def get_papers_list(self) -> list[str]:
        """Return the URLs collected during the last invocation."""
        return self.papers_list
