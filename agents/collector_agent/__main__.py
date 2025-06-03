import logging
import click

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.collector_agent.task_manager import CollectorTaskManager
from agents.collector_agent.agent import CollectorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10001, help="Port number for the server")
def main(host: str, port: int):
    """Start the CollectorAgent server."""
    capabilities = AgentCapabilities(streaming=False)
    skill = AgentSkill(
        id="collect_papers",
        name="Paper Collector",
        description="Fetches science and religious papers based on keywords",
        tags=["papers"],
        examples=["SCIENCE: quantum computing"],
    )
    agent_card = AgentCard(
        name="CollectorAgent",
        description="Retrieves papers for scientific and ethical topics",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=CollectorAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=CollectorAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=CollectorTaskManager(agent=CollectorAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()
