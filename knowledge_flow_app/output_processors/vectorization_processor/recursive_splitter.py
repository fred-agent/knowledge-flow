from typing import List
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from knowledge_flow_app.output_processors.vectorization_processor.interfaces import BaseTextSplitter


class RecursiveSplitter(BaseTextSplitter):
    """
    Concrete implementation of TextSplitterInterface using LangChain's
    RecursiveCharacterTextSplitter.

    This splitter breaks long documents into smaller chunks based on character limits,
    attempting to preserve semantic boundaries (e.g., paragraph breaks).

    Chunk size and overlap are adjustable if needed later.
    """

    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(self, document: Document) -> List[Document]:
        """
        Split a document into smaller chunks using RecursiveCharacterTextSplitter.

        Args:
            document (Document): The original full document.

        Returns:
            List[Document]: A list of smaller chunked documents.
        """
        return self.splitter.split_documents([document])
