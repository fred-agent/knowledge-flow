# settings_minio.py

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
import os

class ContentStoreLocalSettings:
    def __init__(self):
        env_value = os.getenv("LOCAL_CONTENT_STORAGE_PATH")
        if env_value:
            self.root_path = Path(env_value)
        else:
            self.root_path = Path.home() / ".fred" / "knowledge" / "content-store"

        # Ensure parent folder exists
        self.root_path.parent.mkdir(parents=True, exist_ok=True)