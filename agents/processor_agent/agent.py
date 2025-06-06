import logging
from typing import List
from agents.processor_agent.processor import process_papers

logger = logging.getLogger(__name__)

class ProcessorAgent:
    """Agent that downloads PDFs and returns text chunks."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain", "list"]

    async def invoke(self, urls: List[str]) -> List[str]:
        logger.info("Processing %d urls", len(urls))
        chunks = await process_papers(urls)
        return chunks