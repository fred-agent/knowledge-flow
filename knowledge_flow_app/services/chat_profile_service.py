from datetime import datetime
import shutil
from uuid import uuid4
from pathlib import Path
import tempfile
import json
import tiktoken
import logging

from knowledge_flow_app.common.structures import ChatProfile, ChatProfileDocument
from knowledge_flow_app.services.input_processor_service import InputProcessorService
from knowledge_flow_app.stores.chatProfile.chat_profile_storage_factory import get_chat_profile_store
from knowledge_flow_app.application_context import ApplicationContext

logger = logging.getLogger(__name__)

MAX_TOKENS_PER_PROFILE = 40000

def count_tokens_from_markdown(md_path: Path) -> int:
    embedder = ApplicationContext.get_instance().get_embedder()

    try:
        model_name = embedder.embedding.model_name
        encoding = tiktoken.encoding_for_model(model_name)
    except (AttributeError, KeyError):
        encoding = tiktoken.get_encoding("cl100k_base")

    text = md_path.read_text(encoding="utf-8")
    return len(encoding.encode(text))

class ChatProfileService:
    def __init__(self):
        self.store = get_chat_profile_store()
        self.processor = InputProcessorService()

    async def list_profiles(self):
        all_profiles = []

        for dir_path in self.store.root_path.iterdir():
            if dir_path.is_dir():
                profile_path = dir_path / "profile.json"
                if profile_path.exists():
                    try:
                        profile_data = json.loads(profile_path.read_text(encoding="utf-8"))

                        profile_data["created_at"] = profile_data.get("created_at", datetime.now().isoformat())
                        profile_data["updated_at"] = profile_data.get("updated_at", datetime.now().isoformat())
                        profile_data["user_id"] = profile_data.get("user_id", "local")
                        profile_data["tokens"] = profile_data.get("tokens", 0)
                        profile_data["creator"] = profile_data.get("creator", "system")

                        documents = []
                        if "documents" in profile_data:
                            documents = [ChatProfileDocument(**doc) for doc in profile_data["documents"]]
                        else:
                            files_dir = dir_path / "files"
                            if files_dir.exists():
                                for file_path in files_dir.iterdir():
                                    documents.append(ChatProfileDocument(
                                        id=file_path.stem,
                                        document_name=file_path.name,
                                        document_type=file_path.suffix[1:],
                                        size=file_path.stat().st_size,
                                        tokens=0
                                    ))
                        profile_data["documents"] = documents

                        profile = ChatProfile(
                            id=profile_data["id"],
                            title=profile_data.get("title", ""),
                            description=profile_data.get("description", ""),
                            created_at=profile_data.get("created_at", datetime.utcnow().isoformat()),
                            updated_at=profile_data.get("updated_at", datetime.utcnow().isoformat()),
                            creator=profile_data.get("creator", "system"),
                            user_id=profile_data.get("user_id", "local"),
                            tokens=profile_data.get("tokens", 0),
                            documents=documents
                        )
                        all_profiles.append(profile)

                    except Exception as e:
                        logger.error(f"Failed to load profile from {profile_path}: {e}", exc_info=True)

        return all_profiles

    async def create_profile(self, title: str, description: str, files_dir: Path) -> ChatProfile:
        profile_id = str(uuid4())

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            profile_dir = tmp_path / profile_id
            files_subdir = profile_dir / "files"
            files_subdir.mkdir(parents=True, exist_ok=True)

            documents = []
            total_tokens = 0

            for file in files_dir.iterdir():
                if file.is_file():
                    try:
                        processing_dir = tmp_path / f"{file.stem}_processing"
                        processing_dir.mkdir(parents=True, exist_ok=True)

                        input_metadata = {
                            "source_file": file.name,
                            "document_uid": file.stem
                        }

                        temp_input_file = processing_dir / file.name
                        shutil.copy(file, temp_input_file)

                        self.processor.process(
                            output_dir=processing_dir,
                            input_file=file.name,
                            input_file_metadata=input_metadata
                        )

                        output_md = next((processing_dir / "output").glob("*.md"), None)
                        if not output_md:
                            raise FileNotFoundError(f"No .md output found for {file.name}")

                        new_md_name = f"{file.stem}.md"
                        dest_path = files_subdir / new_md_name
                        shutil.move(str(output_md), dest_path)

                        token_count = count_tokens_from_markdown(dest_path)
                        total_tokens += token_count

                        if total_tokens > MAX_TOKENS_PER_PROFILE:
                            raise ValueError(f"Profile exceeds the {MAX_TOKENS_PER_PROFILE} token limit.")

                        documents.append(ChatProfileDocument(
                            id=file.stem,
                            document_name=file.name,
                            document_type=file.suffix[1:],
                            size=file.stat().st_size,
                            tokens=token_count
                        ))

                    except Exception as e:
                        logger.error(f"Failed to process file '{file.name}': {e}", exc_info=True)

            now = datetime.utcnow().isoformat()
            metadata = {
                "id": profile_id,
                "title": title,
                "description": description,
                "created_at": now,
                "updated_at": now,
                "creator": "system",
                "documents": [doc.model_dump() for doc in documents],
                "tokens": total_tokens,
                "user_id": "local"
            }

            (profile_dir / "profile.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            self.store.save_profile(profile_id, profile_dir)

        return ChatProfile(**metadata)
