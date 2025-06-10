from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from knowledge_flow_app.services.chat_profile_service import ChatProfileService
import tempfile
from pathlib import Path
import shutil

class ChatProfileController:
    def __init__(self, router: APIRouter):
        self.service = ChatProfileService()
        self._register_routes(router)

    def _register_routes(self, router: APIRouter):
        @router.get("/chatProfiles")
        async def list_profiles():
            return await self.service.list_profiles()

        @router.post("/chatProfiles")
        async def create_profile(
            title: str = Form(...),
            description: str = Form(...),
            files: list[UploadFile] = File(default=[])
        ):
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_path = Path(tmp_dir)
                    for f in files:
                        dest = tmp_path / f.filename
                        with open(dest, "wb") as out_file:
                            content = await f.read()
                            out_file.write(content)

                    profile = await self.service.create_profile(title, description, tmp_path)
                    return profile
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @router.put("/chatProfiles/{chatProfile_id}")
        async def update_profile(chatProfile_id: str, title: str, description: str):
            return await self.service.update_profile(chatProfile_id, title, description)

        @router.delete("/chatProfiles/{chatProfile_id}")
        async def delete_profile(chatProfile_id: str):
            return await self.service.delete_profile(chatProfile_id)

        @router.post("/chatProfiles/{chatProfile_id}/documents")
        async def upload_documents(chatProfile_id: str, files: list[UploadFile] = File(...)):
            # à implémenter plus tard
            return {"message": "not yet implemented"}

        @router.delete("/chatProfiles/{chatProfile_id}/documents/{document_id}")
        async def delete_document(chatProfile_id: str, document_id: str):
            return await self.service.delete_document(chatProfile_id, document_id)
