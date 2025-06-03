import logging
from agents.input_agent.input import prompt_science, prompt_religion

logger = logging.getLogger(__name__)

class InputAgent:
    """Agent that extracts scientific and ethical keywords from a prompt."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    async def invoke(self, query: str, session_id: str) -> str:
        science = await prompt_science(query)
        ethics = await prompt_religion(query)
        return f"SCIENCE: {science}\nETHICS: {ethics}"
