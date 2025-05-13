from abc import ABC, abstractmethod

class BaseMetadataStore(ABC):
    @abstractmethod
    def get_all_metadata(self, filters: dict) -> list:
        pass

    @abstractmethod
    def get_metadata_by_uid(self, document_uid: str) -> dict:
        pass

    @abstractmethod
    def update_metadata_field(self, document_uid: str, field: str, value) -> dict:
        pass

    @abstractmethod
    def save_metadata(self, metadata: dict) -> None:
        """
        Add or replace a full metadata entry in the store.

        - If an entry with the same UID exists, it is overwritten.
        - If not, the metadata is added as a new entry.

        :param metadata: The full metadata dictionary.
        :raises ValueError: If 'document_uid' is missing.
        """
        pass

    @abstractmethod
    def delete_metadata(self, metadata: dict) -> None:
        pass
