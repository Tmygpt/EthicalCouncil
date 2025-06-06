import logging
from typing import List
from server.task_manager import InMemoryTaskManager
from agents.processor_agent.agent import ProcessorAgent
from models.request import SendTaskRequest, SendTaskResponse
from models.task import Message, TaskStatus, TaskState, TextPart

logger = logging.getLogger(__name__)

class ProcessorTaskManager(InMemoryTaskManager):
    def __init__(self, agent: ProcessorAgent):
        super().__init__()
        self.agent = agent

    def _get_urls(self, request: SendTaskRequest) -> List[str]:
        text = request.params.message.parts[0].text
        return [l.strip() for l in text.splitlines() if l.strip()]

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        logger.info(f"Processing processor task: {request.params.id}")
        task = await self.upsert_task(request.params)
        urls = self._get_urls(request)
        chunks = await self.agent.invoke(urls)
        result_text = "\n".join(chunks)
        agent_message = Message(role="agent", parts=[TextPart(text=result_text)])
        async with self.lock:
            task.status = TaskStatus(state=TaskState.COMPLETED)
            task.history.append(agent_message)
        return SendTaskResponse(id=request.id, result=task)