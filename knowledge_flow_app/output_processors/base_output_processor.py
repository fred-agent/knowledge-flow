from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseOutputProcessor(ABC):
    """
    Base output Processor
    -------------------
    Interface for post-processing files after they have been processed by the extraction processors.
    This interface is designed to be implemented by various concrete classes that handle
    different post-processing tasks (e.g., vectorization, database insertion).
    Design Motivation:
    - Separation of concerns: isolates the post-processing step from the extraction step.
    - Flexibility: allows for different post-processing strategies to be implemented.
    - Testability: enables unit testing of post-processing logic without involving actual file I/O.
    - Uniformity: keeps the processing pipeline modular and easy to extend.
    """
    @abstractmethod
    def process(self, file_path: str, metadata: dict):
        """
        Process the file after it has been extracted.
        Args:
            file_path (str): The path to the extracted file. This is typically a temporary file, markdown or tabular.
            metadata (dict): Metadata associated with the input file.
        """
        logger.error(f"No implementation found for ouput processor: {file_path} with metadata {metadata}")
        raise NotImplementedError("Output processor not implemented for this file type.")
