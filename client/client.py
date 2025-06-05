# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import json
from uuid import uuid4                               
import httpx                               
from httpx_sse import connect_sse          
from typing import Any                     

from agents.input_agent.input import prompt_science, prompt_religion
from agents.collector_agent.collector import (
    get_science_papers,
    get_religion_papers,
    papers_list as collector_papers_list,
)
from agents.summary_agent.agent import SummaryAgent

from models.request import SendTaskRequest, GetTaskRequest

from models.json_rpc import JSONRPCRequest

from models.task import Task, TaskSendParams
from models.agent import AgentCard


# -----------------------------------------------------------------------------
# Custom Error Classes
# -----------------------------------------------------------------------------

class A2AClientHTTPError(Exception):
    """Raised when an HTTP request fails (e.g., bad server response)"""
    pass

class A2AClientJSONError(Exception):
    """Raised when the response is not valid JSON"""
    pass



class A2AClient:
    def __init__(self, agent_card: AgentCard = None, url: str = None):
        if agent_card:
            self.url = agent_card.url
        elif url:
            self.url = url
        else:
            raise ValueError("Must provide either agent_card or url")


    async def send_task(self, payload: dict[str, Any]) -> Task:

        request = SendTaskRequest(
            id=uuid4().hex,
            params=TaskSendParams(**payload) 
        )

        print("\n📤 Sending JSON-RPC request:")
        print(json.dumps(request.model_dump(), indent=2))

        response = await self._send_request(request)
        return Task(**response["result"])  



    async def get_task(self, payload: dict[str, Any]) -> Task:
        request = GetTaskRequest(params=payload)
        response = await self._send_request(request)
        return Task(**response["result"])



    async def _send_request(self, request: JSONRPCRequest) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.url,
                    json=request.model_dump(), 
                    timeout=60
                )
                response.raise_for_status()    
                return response.json()        

            except httpx.HTTPStatusError as e:
                raise A2AClientHTTPError(e.response.status_code, str(e)) from e

            except json.JSONDecodeError as e:
                raise A2AClientJSONError(str(e)) from e


async def process_prompt(prompt: str) -> str:
    science = await prompt_science(prompt)
    ethics = await prompt_religion(prompt)

    collector_papers_list.clear()
    science_papers = await get_science_papers(science)
    ethics_papers = await get_religion_papers(ethics)

    papers = collector_papers_list.copy()

    """summary_text = await SummaryAgent().invoke(papers, prompt)"""

    links_text = "\n".join(papers)
    """return (
        f"Science keywords: {science}\n"
        f"Ethical keywords: {ethics}\n\n"
        f"Collected Links:\n{links_text}\n\n"
        f"Science Papers:\n{science_papers}\n\n"
        f"Religious Papers:\n{ethics_papers}\n\n"
    )"""
    
    await SummaryAgent().invoke(papers, prompt)
    return ""
    