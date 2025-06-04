import logging
import click

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.mediator_agent.task_manager import MediatorTaskManager
from agents.mediator_agent.agent import MediatorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10005, help="Port number for the server")
def main(host: str, port: int):
    """Start the MediatorAgent server."""
    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="mediate_summaries",
        name="Mediator",
        description="Combines science and ethics summaries",
        tags=["summary", "mediator"],
        examples=["<query>\n<url1>\n<url2>"]
    )
    agent_card = AgentCard(
        name="MediatorAgent",
        description="Produces a balanced summary from science and ethics views",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=MediatorAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=MediatorAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=MediatorTaskManager(agent=MediatorAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()
