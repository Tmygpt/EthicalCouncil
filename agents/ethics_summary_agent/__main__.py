import logging
import click

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.ethics_summary_agent.task_manager import EthicsSummaryTaskManager
from agents.ethics_summary_agent.agent import EthicsSummaryAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10004, help="Port number for the server")
def main(host: str, port: int):
    """Start the EthicsSummaryAgent server."""
    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="summarize_ethics",
        name="Ethics Summarizer",
        description="Summarizes links to ethical or religious papers",
        tags=["summary", "ethics"],
        examples=["<query>\n<url1>\n<url2>"]
    )
    agent_card = AgentCard(
        name="EthicsSummaryAgent",
        description="Generates an ethical summary from a list of papers",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=EthicsSummaryAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=EthicsSummaryAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=EthicsSummaryTaskManager(agent=EthicsSummaryAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()
