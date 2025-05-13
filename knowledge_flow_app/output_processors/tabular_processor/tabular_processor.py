import logging
from fastapi import HTTPException
from langchain.schema.document import Document

from knowledge_flow_app.output_processors.base_output_processor import BaseOutputProcessor

logger = logging.getLogger(__name__)

class TabularProcessor(BaseOutputProcessor):
    """
    A pipeline for processing tabular data.
    """
    def __init__(self):
        logger.info("Initializing TabularPipeline")
    
    def process(self, file_path: str, metadata: dict):
        logger.info(f"Processing file: {file_path} with metadata: {metadata}")

