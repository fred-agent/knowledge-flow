from pathlib import Path
from abc import ABC, abstractmethod

class BaseContentStore(ABC):
    @abstractmethod
    async def save_content(self, document_id: str, directory: Path) -> None:
        """
            Uploads the content of a directory (recursively) to storage.
            The directory should contain all files related to the document.
            The document_id is used to create a unique path in the storage.
            The directory structure will be preserved in the storage.
        """
        pass

