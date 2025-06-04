import logging
import click

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.input_agent.task_manager import AgentTaskManager
from agents.input_agent.agent import InputAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10002, help="Port number for the server")
def main(host: str, port: int):
    """Start the InputAgent server."""
    capabilities = AgentCapabilities(streaming=False)
    skill = AgentSkill(
        id="split_prompt",
        name="Prompt Splitter",
        description="Splits a prompt into scientific and ethical keywords",
        tags=["keywords", "split"],
        examples=["Explain the big bang"],
    )
    agent_card = AgentCard(
        name="InputAgent",
        description="Extracts scientific and ethical keywords from prompts",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=InputAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=InputAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=AgentTaskManager(agent=InputAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()
