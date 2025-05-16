from pathlib import Path
from abc import ABC, abstractmethod

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
