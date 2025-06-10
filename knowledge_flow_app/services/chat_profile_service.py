from datetime import datetime
import shutil
from uuid import uuid4
from pathlib import Path
import tempfile
import json

from knowledge_flow_app.common.structures import ChatProfile, ChatProfileDocument
from knowledge_flow_app.services.input_processor_service import InputProcessorService
from knowledge_flow_app.stores.chatProfile.chat_profile_storage_factory import get_chat_profile_store


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

                        # Backfill required fields if missing
                        profile_data["created_at"] = profile_data.get("created_at", datetime.now().isoformat())
                        profile_data["updated_at"] = profile_data.get("updated_at", datetime.now().isoformat())
                        profile_data["user_id"] = profile_data.get("user_id", "local")
                        profile_data["tokens"] = profile_data.get("tokens", 0)
                        profile_data["creator"] = profile_data.get("creator", "system")

                        # Load documents from metadata or reconstruct
                        if "documents" in profile_data:
                            documents = [ChatProfileDocument(**doc) for doc in profile_data["documents"]]
                        else:
                            documents = []
                            files_dir = dir_path / "files"
                            if files_dir.exists():
                                for file_path in files_dir.iterdir():
                                    documents.append(ChatProfileDocument(
                                        id=file_path.stem,
                                        document_name=file_path.name,
                                        document_type=file_path.suffix[1:],
                                        size=file_path.stat().st_size
                                    ))
                        profile_data["documents"] = documents

                        profile = ChatProfile(**profile_data)
                        all_profiles.append(profile)

                    except Exception as e:
                        print(f"⚠️ Failed to parse {profile_path}: {e}")

        return all_profiles

    async def create_profile(self, title: str, description: str, files_dir: Path) -> ChatProfile:
        profile_id = str(uuid4())

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            profile_dir = tmp_path / profile_id
            files_subdir = profile_dir / "files"
            files_subdir.mkdir(parents=True, exist_ok=True)

            documents = []

            for file in files_dir.iterdir():
                if file.is_file():
                    try:
                        processing_dir = tmp_path / f"{file.stem}_processing"
                        processing_dir.mkdir(parents=True, exist_ok=True)

                        input_metadata = {
                            "source_file": file.name,
                            "document_uid": file.stem
                        }

                        # Copy file to processing input
                        temp_input_file = processing_dir / file.name
                        shutil.copy(file, temp_input_file)

                        # Run processor
                        self.processor.process(
                            output_dir=processing_dir,
                            input_file=file.name,
                            input_file_metadata=input_metadata
                        )

                        # Find and rename the output .md file
                        output_md = next((processing_dir / "output").glob("*.md"), None)
                        if output_md:
                            new_md_name = f"{file.stem}.md"
                            dest_path = files_subdir / new_md_name
                            shutil.move(str(output_md), dest_path)

                            documents.append(ChatProfileDocument(
                                id=file.stem,
                                document_name=file.name,  # original file name for display
                                document_type=file.suffix[1:],  # e.g. "pdf"
                                size=file.stat().st_size
                            ))

                    except Exception as e:
                        print(f"⚠️ Failed to process file {file.name}: {e}")

            # Build metadata dict
            now = datetime.utcnow().isoformat()
            metadata = {
                "id": profile_id,
                "title": title,
                "description": description,
                "created_at": now,
                "updated_at": now,
                "creator": "system",
                "documents": [doc.model_dump() for doc in documents]
            }

            # Write metadata to profile.json
            (profile_dir / "profile.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            # Save profile directory
            self.store.save_profile(profile_id, profile_dir)

        # Remove 'documents' from metadata to avoid double passing
        metadata.pop("documents", None)

        return ChatProfile(
            **metadata,
            documents=documents,
            tokens=0,
            user_id="local"
        )

    async def delete_profile(self, profile_id: str):
        self.store.delete_profile(profile_id)
        return {"success": True}
