import logging
import click

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.summary_agent.task_manager import SummaryTaskManager
from agents.summary_agent.agent import SummaryAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10003, help="Port number for the server")
def main(host: str, port: int):
    """Start the SummaryAgent server."""
    capabilities = AgentCapabilities(streaming=False)
    skill = AgentSkill(
        id="summarize_papers",
        name="Paper Summarizer",
        description="Summarizes links to scientific and religious papers",
        tags=["summary", "papers"],
        examples=["<query>\n<url1>\n<url2>"]
    )
    agent_card = AgentCard(
        name="SummaryAgent",
        description="Generates a summary from a list of papers",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=SummaryAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=SummaryAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=SummaryTaskManager(agent=SummaryAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()

