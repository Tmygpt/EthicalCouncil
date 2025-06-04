import logging
import uuid
from typing import List
from utilities.a2a.agent_connect import AgentConnector
from agents.mediator_agent.summary import mediate_summaries

logger = logging.getLogger(__name__)

class MediatorAgent:
    """Agent that mediates between science and ethics summaries."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    def __init__(self,
                 science_url: str = "http://localhost:10003/",
                 ethics_url: str = "http://localhost:10004/") -> None:
        self.science = AgentConnector("ScienceSummaryAgent", science_url)
        self.ethics = AgentConnector("EthicsSummaryAgent", ethics_url)

    async def _get_summary(self, connector: AgentConnector, papers: List[str], query: str) -> str:
        message = "\n".join([query, *papers])
        task = await connector.send_task(message, uuid.uuid4().hex)
        if task.history and len(task.history) > 1:
            return task.history[-1].parts[0].text
        return ""

    async def invoke(self, papers: List[str], query: str) -> str:
        science_summary = await self._get_summary(self.science, papers, query)
        ethics_summary = await self._get_summary(self.ethics, papers, query)
        print("Mediator's perspective:\n")
        return await mediate_summaries(science_summary, ethics_summary, query)
