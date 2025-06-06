import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from server.task_manager import InMemoryTaskManager
from models.request import GetTaskRequest
from models.task import (
    TaskSendParams, TaskQueryParams, Message, TextPart, TaskState
)

@pytest.mark.asyncio
async def test_upsert_new_task():
    manager = InMemoryTaskManager()
    params = TaskSendParams(
        id="t1",
        sessionId="s",
        message=Message(role="user", parts=[TextPart(text="hello")])
    )
    task = await manager.upsert_task(params)
    assert task.id == "t1"
    assert task.status.state == TaskState.SUBMITTED
    assert task.history[0].parts[0].text == "hello"


@pytest.mark.asyncio
async def test_upsert_existing_task_appends_history():
    manager = InMemoryTaskManager()
    params1 = TaskSendParams(id="t1", sessionId="s", message=Message(role="user", parts=[TextPart(text="a")]))
    await manager.upsert_task(params1)
    params2 = TaskSendParams(id="t1", sessionId="s", message=Message(role="user", parts=[TextPart(text="b")]))
    task = await manager.upsert_task(params2)
    assert len(task.history) == 2
    assert task.history[1].parts[0].text == "b"


@pytest.mark.asyncio
async def test_on_get_task_truncates_history():
    manager = InMemoryTaskManager()
    await manager.upsert_task(TaskSendParams(id="t1", sessionId="s", message=Message(role="user", parts=[TextPart(text="1")])))
    await manager.upsert_task(TaskSendParams(id="t1", sessionId="s", message=Message(role="user", parts=[TextPart(text="2")])))

    request = GetTaskRequest(id="req", params=TaskQueryParams(id="t1", historyLength=1))
    response = await manager.on_get_task(request)
    assert response.result.history[0].parts[0].text == "2"