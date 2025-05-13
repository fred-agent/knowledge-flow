from pathlib import Path
import os

class MetadataStoreLocalSettings:
    def __init__(self):
        env_value = os.getenv("LOCAL_METADATA_STORAGE_PATH")
        if env_value:
            self.root_path = Path(env_value)
        else:
            self.root_path = Path.home() / ".fred" / "knowledge" / "metadata-store.json"

        # Ensure parent folder exists
        self.root_path.parent.mkdir(parents=True, exist_ok=True)