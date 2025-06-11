import logging
import click
from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.processor_agent.task_manager import ProcessorTaskManager
from agents.processor_agent.agent import ProcessorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10006, help="Port number for the server")
def main(host: str, port: int):
    """Start the ProcessorAgent server."""
    capabilities = AgentCapabilities(streaming=False)
    skill = AgentSkill(
        id="process_papers",
        name="URL Processor",
        description="Uploads document text to Pinecone",
        tags=["url", "process"],
        examples=["<url1>\n<url2>"]
    )
    agent_card = AgentCard(
        name="ProcessorAgent",
        description="Uploads the provided links to a Pinecone index",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=ProcessorAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=ProcessorAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=ProcessorTaskManager(agent=ProcessorAgent()),
    )
    server.start()

if __name__ == "__main__":
    main()