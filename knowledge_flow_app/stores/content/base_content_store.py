from pathlib import Path
from abc import ABC, abstractmethod
from typing import BinaryIO

class BaseContentStore(ABC):
    @abstractmethod
    def save_content(self, document_id: str, directory: Path) -> None:
        """
            Uploads the content of a directory (recursively) to storage.
            The directory should contain all files related to the document.
            The document_id is used to create a unique path in the storage.
            The directory structure will be preserved in the storage.
        """
        pass

    @abstractmethod
    def delete_content(self, document_uid: str) -> None:
        """
            Deletes the content of a document from storage.
            The document_uid is used to identify the document in storage.
        """
        pass

    @abstractmethod
    def get_content(self, document_uid: str) -> BinaryIO:
        """
        Retrieve a readable binary stream for the document's primary content.

        Returns:
            BinaryIO: A file-like object you can stream from.

        Raises:
            FileNotFoundError: If the document is not found.
        """
        pass

    @abstractmethod
    def get_markdown(self, document_uid: str) -> str:
        """
        Returns the markdown content (from output/output.md).
        """
        pass
