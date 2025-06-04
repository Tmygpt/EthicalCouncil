# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import json
from uuid import uuid4                                 # Used to encode/decode JSON data
import httpx                                # Async HTTP client for making web requests
from httpx_sse import connect_sse           # SSE client extension for httpx (not used currently)
from typing import Any                      # Type hints for flexible input/output

from agents.input_agent.input import prompt_science, prompt_religion
from agents.collector_agent.collector import (
    get_science_papers,
    get_religion_papers,
    papers_list as collector_papers_list,
)

# Import supported request types
from models.request import SendTaskRequest, GetTaskRequest  # Removed CancelTaskRequest

# Base request format for JSON-RPC 2.0
from models.json_rpc import JSONRPCRequest

# Models for task results and agent identity
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


# -----------------------------------------------------------------------------
# A2AClient: Main interface for talking to an A2A agent
# -----------------------------------------------------------------------------

class A2AClient:
    def __init__(self, agent_card: AgentCard = None, url: str = None):
        if agent_card:
            self.url = agent_card.url
        elif url:
            self.url = url
        else:
            raise ValueError("Must provide either agent_card or url")


    # -------------------------------------------------------------------------
    # send_task: Send a new task to the agent
    # -------------------------------------------------------------------------
    async def send_task(self, payload: dict[str, Any]) -> Task:

        request = SendTaskRequest(
            id=uuid4().hex,
            params=TaskSendParams(**payload)  # ✅ Proper model wrapping
        )

        print("\n📤 Sending JSON-RPC request:")
        print(json.dumps(request.model_dump(), indent=2))

        response = await self._send_request(request)
        return Task(**response["result"])  # ✅ Extract just the 'result' field



    # -------------------------------------------------------------------------
    # get_task: Retrieve the status or history of a previously sent task
    # -------------------------------------------------------------------------
    async def get_task(self, payload: dict[str, Any]) -> Task:
        request = GetTaskRequest(params=payload)
        response = await self._send_request(request)
        return Task(**response["result"])



    # -------------------------------------------------------------------------
    # _send_request: Internal helper to send a JSON-RPC request
    # -------------------------------------------------------------------------
    async def _send_request(self, request: JSONRPCRequest) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.url,
                    json=request.model_dump(),  # Convert Pydantic model to JSON
                    timeout=60,
                )
                response.raise_for_status()  # Raise error if status code is 4xx/5xx
                return response.json()  # Return parsed response as a dict

            except httpx.HTTPStatusError as e:
                # Try to include any server-provided error details
                try:
                    error_body = e.response.json()
                except Exception:
                    error_body = e.response.text
                raise A2AClientHTTPError(e.response.status_code, str(error_body)) from e

            except httpx.RequestError as e:
                raise A2AClientHTTPError(None, str(e)) from e

            except json.JSONDecodeError as e:
                raise A2AClientJSONError(str(e)) from e


async def process_prompt(prompt: str) -> str:
    """Process a user prompt by collecting papers and invoking the mediator."""
    from agents.mediator_agent.agent import MediatorAgent

    # Extract keywords using the input agent helpers
    science = await prompt_science(prompt)
    ethics = await prompt_religion(prompt)

    # Clear any previous collector results and fetch papers for both sets
    collector_papers_list.clear()
    science_papers = await get_science_papers(science)
    ethics_papers = await get_religion_papers(ethics)

    # Copy the collected links before the global list is mutated again
    papers = collector_papers_list.copy()

    """summary_text = await MediatorAgent().invoke(papers, prompt)"""

    # Combine keywords, paper listings, and the summary for display
    links_text = "\n".join(papers)
    """return (
        f"Science keywords: {science}\n"
        f"Ethical keywords: {ethics}\n\n"
        f"Collected Links:\n{links_text}\n\n"
        f"Science Papers:\n{science_papers}\n\n"
        f"Religious Papers:\n{ethics_papers}\n\n"
    )"""
    
    await MediatorAgent().invoke(papers, prompt)
    return ""
    