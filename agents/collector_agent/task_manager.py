import logging
from server.task_manager import InMemoryTaskManager
from agents.collector_agent.agent import CollectorAgent
from models.request import SendTaskRequest, SendTaskResponse
from models.task import Message, TaskStatus, TaskState, TextPart

logger = logging.getLogger(__name__)

class CollectorTaskManager(InMemoryTaskManager):
    def __init__(self, agent: CollectorAgent):
        super().__init__()
        self.agent = agent

    def _get_keywords(self, request: SendTaskRequest):
        text = request.params.message.parts[0].text
        parts = text.split('\n')
        science = ""
        ethics = ""
        for p in parts:
            if p.lower().startswith('science:'):
                science = p.split(':',1)[1].strip()
            elif p.lower().startswith('ethics:'):
                ethics = p.split(':',1)[1].strip()
        return science, ethics

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        logger.info(f"Processing collector task: {request.params.id}")
        task = await self.upsert_task(request.params)
        science, ethics = self._get_keywords(request)
        result_text = await self.agent.invoke(science, ethics)
        agent_message = Message(role='agent', parts=[TextPart(text=result_text)])
        async with self.lock:
            task.status = TaskStatus(state=TaskState.COMPLETED)
            task.history.append(agent_message)
        return SendTaskResponse(id=request.id, result=task)
