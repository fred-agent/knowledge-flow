import logging
import shutil
from pathlib import Path

from knowledge_flow_app.stores.content.base_content_store import BaseContentStore
logger = logging.getLogger(__name__)

class LocalStorageBackend(BaseContentStore):
    def __init__(self, destination_root: Path):
        self.destination_root = destination_root

    def save_content(self, document_uid: str, document_dir: Path) -> None:
        destination = self.destination_root / document_uid

        # 🧹 1. Clean old destination if it exists
        if destination.exists():
            shutil.rmtree(destination)

        # 🏗️ 2. Create destination
        destination.mkdir(parents=True, exist_ok=True)

        logger.info(f"📂 Created destination folder: {destination}")

        # 📦 3. Copy all contents
        for item in document_dir.iterdir():
            target = destination / item.name
            if item.is_dir():
                shutil.copytree(item, target)
                logger.info(f"📁 Copied directory: {item} -> {target}")
            else:
                shutil.copy2(item, target)
                logger.info(f"📄 Copied file: {item} -> {target}")

        logger.info(f"✅ Successfully saved document {document_uid} to {destination}")

