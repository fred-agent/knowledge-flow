import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import shortuuid
import pandas

logger = logging.getLogger(__name__)


class BaseInputProcessor(ABC):
    """
    Base class for all processors that handle file metadata extraction and processing.
    This class provides a common interface and utility methods for file processing.
    """
    def _generate_file_unique_id(self, metadata: dict) -> str:
        """
        Generate a unique identifier for the file based on its metadata.
        This identifier is used to track the file in the system.
        """
        return shortuuid.uuid()
        #identifier_str = f"{metadata.get('document_name', '')}"
        #return hashlib.sha256(identifier_str.encode('utf-8')).hexdigest()

    def _add_common_metadata(self, file_path: Path) -> dict:
        common_metadata = {
            "document_name": file_path.name,
            "date_added_to_kb": datetime.now().isoformat(),
            "retrievable": True,
        }
        common_metadata["document_uid"] = self._generate_file_unique_id(common_metadata)
        return common_metadata

    def _sanitize_front_metadata(self, front_metadata: dict) -> dict:
        sanitized = {
            key.replace(' ', '_'): (value if value else "unknown")
            for key, value in front_metadata.items()
            if value not in (None, '', [], {})
        }
        return sanitized

    def validate_metadata(self, metadata: dict) -> None:
        required_fields = ["document_uid"]
        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Missing required metadata field: {field}")

    def process_metadata(self, file_path: Path, front_metadata: dict = None) -> dict:
        if not self.check_file_validity(file_path):
            return {"document_name": file_path.name, "error": "Invalid file structure"}

        final_metadata = {}
        file_metadata = self.extract_file_metadata(file_path)
        common_metadata = self._add_common_metadata(file_path)

        if front_metadata:
            final_metadata["front_metadata"] = self._sanitize_front_metadata(front_metadata)

        final_metadata.update(file_metadata)
        final_metadata.update(common_metadata)

        self.validate_metadata(final_metadata)
        return final_metadata

    @abstractmethod
    def check_file_validity(self, file_path: Path) -> bool:
        pass

    @abstractmethod
    def extract_file_metadata(self, file_path: Path) -> dict:
        pass


class BaseMarkdownProcessor(BaseInputProcessor):
    """For processors that convert to Markdown."""

    @abstractmethod
    def convert_file_to_markdown(
        self, 
        file_path: Path, 
        output_dir: Path
    ) -> dict:
        pass


class BaseTabularProcessor(BaseInputProcessor):
    """For processors that convert to structured tabular format (e.g., SQL rows)."""

    @abstractmethod
    def convert_file_to_table(self, file_path: Path) -> pandas.DataFrame:
        pass
