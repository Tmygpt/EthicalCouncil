import logging
from agents.collector_agent.collector import (
    get_science_papers,
    get_religion_papers,
)

logger = logging.getLogger(__name__)

class CollectorAgent:
    """Agent that fetches science and religious papers given keywords."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    async def invoke(self, science: str, ethics: str) -> str:
        science_res = await get_science_papers(science) if science else ""
        ethics_res = await get_religion_papers(ethics) if ethics else ""
        return f"Science Papers:\n{science_res}\n---\nReligious Papers:\n{ethics_res}"
