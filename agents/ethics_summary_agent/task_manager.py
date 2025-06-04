import logging
from server.task_manager import InMemoryTaskManager
from agents.ethics_summary_agent.agent import EthicsSummaryAgent
from models.request import SendTaskRequest, SendTaskResponse
from models.task import Message, TaskStatus, TaskState, TextPart
from typing import List, Tuple

logger = logging.getLogger(__name__)

class EthicsSummaryTaskManager(InMemoryTaskManager):
    def __init__(self, agent: EthicsSummaryAgent):
        super().__init__()
        self.agent = agent

    def _parse_input(self, request: SendTaskRequest) -> Tuple[List[str], str]:
        text = request.params.message.parts[0].text
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not lines:
            return [], ""
        query = lines[0]
        papers = lines[1:]
        return papers, query

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        logger.info(f"Processing ethics summary task: {request.params.id}")
        task = await self.upsert_task(request.params)
        papers, query = self._parse_input(request)
        result_text = await self.agent.invoke(papers, query)
        agent_message = Message(role="agent", parts=[TextPart(text=result_text)])
        async with self.lock:
            task.status = TaskStatus(state=TaskState.COMPLETED)
            task.history.append(agent_message)
        return SendTaskResponse(id=request.id, result=task)
