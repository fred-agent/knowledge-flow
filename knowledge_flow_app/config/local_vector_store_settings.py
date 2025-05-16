# settings_minio.py

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
import os

class LocalVectorStoreSettings:
    """
    Local vector store settings class.
    This class is responsible for managing the local vector store settings.
    The defauls is "~/.fred/knowledge/vectore-store".
    The path can be overridden by setting the "LOCAL_VECTOR_STORAGE_PATH" environment variable.
    """
    def __init__(self):
        env_value = os.getenv("LOCAL_VECTOR_STORAGE_PATH")
        if env_value:
            self.root_path = Path(env_value)
        else:
            self.root_path = Path.home() / ".fred" / "knowledge" / "vectore-store"

        # Ensure parent folder exists
        self.root_path.parent.mkdir(parents=True, exist_ok=True)