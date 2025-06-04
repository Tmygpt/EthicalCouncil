import logging
import click

from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.science_summary_agent.task_manager import ScienceSummaryTaskManager
from agents.science_summary_agent.agent import ScienceSummaryAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10003, help="Port number for the server")
def main(host: str, port: int):
    """Start the ScienceSummaryAgent server."""
    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="summarize_science",
        name="Science Summarizer",
        description="Summarizes links to scientific papers",
        tags=["summary", "science"],
        examples=["<query>\n<url1>\n<url2>"]
    )
    agent_card = AgentCard(
        name="ScienceSummaryAgent",
        description="Generates a scientific summary from a list of papers",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=ScienceSummaryAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=ScienceSummaryAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=ScienceSummaryTaskManager(agent=ScienceSummaryAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()
