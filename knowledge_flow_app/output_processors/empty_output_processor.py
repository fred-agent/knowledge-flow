# knowledge_flow_app/output_processors/empty_output_processor.py

import logging
from knowledge_flow_app.output_processors.base_output_processor import BaseOutputProcessor

logger = logging.getLogger(__name__)

class EmptyOutputProcessor(BaseOutputProcessor):
    """
    A no-op output processor that does nothing.

    Used to intentionally skip output processing for specific file types.
    """

    def __init__(self):
        super().__init__()

    def process(self, document_uid: str, document_content: str, metadata: dict) -> None:
        logger.info(f"Skipping output processing for document UID: {document_uid}")
        return  # Do nothing
