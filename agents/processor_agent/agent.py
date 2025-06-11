import logging
from typing import List
from agents.processor_agent.processor import process_papers

logger = logging.getLogger(__name__)

class ProcessorAgent:
    """Agent that uploads PDF contents to Pinecone."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, urls: List[str]) -> str:
        logger.info("Processing %d urls", len(urls))
        result = await process_papers(urls)
        return result
