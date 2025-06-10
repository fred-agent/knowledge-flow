import json
import shutil
from pathlib import Path
from typing import BinaryIO
from .base_chat_profile_store import BaseChatProfileStore

class LocalChatProfileStore(BaseChatProfileStore):
    def __init__(self, root_path: Path):
        self.root_path = root_path

    def save_profile(self, profile_id: str, directory: Path) -> None:
        destination = self.root_path / profile_id
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(directory, destination)

    def delete_profile(self, profile_id: str) -> None:
        profile_dir = self.root_path / profile_id
        if profile_dir.exists():
            shutil.rmtree(profile_dir)

    def get_profile_description(self, profile_id: str) -> dict:
        desc_path = self.root_path / profile_id / "profile.json"
        if not desc_path.exists():
            raise FileNotFoundError("Chat profile description not found")
        return json.loads(desc_path.read_text(encoding="utf-8"))

    def get_document(self, profile_id: str, document_name: str) -> BinaryIO:
        doc_path = self.root_path / profile_id / "files" / document_name
        if not doc_path.exists():
            raise FileNotFoundError("Document not found in chat profile")
        return open(doc_path, "rb")