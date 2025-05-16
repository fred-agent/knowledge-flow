import logging
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# --- Response Models ---
class DocumentContent(BaseModel):
    """
    Model representing a document's content and metadata.
    """
    uid: str
    file_name: str
    title: str = ""
    agent_name: str = ""
    content: Any = None
    has_binary_content: bool = False
    content_type: str = "application/octet-stream"
    file_url: str = None
    modified: str = ""
    metadata: Dict[str, Any] = {}


class GetDocumentContentResponse(BaseModel):
    """
    Response model for retrieving content for a single document.
    """
    status: str
    documents: List[Dict[str, Any]]


class ContentController:
    """
    FastAPI controller for managing document content operations.
    """
    
    def __init__(self, router: APIRouter):
        """
        Initialize the controller with a FastAPI router and content service.
        """
        from knowledge_flow_app.services.content_service import ContentService
        self.service = ContentService()
        self._register_routes(router)
    
    def _register_routes(self, router: APIRouter):
        """
        Register all content-related routes with the provided router.
        """
        @router.get(
            "/document/{document_uid}",
            tags=["Content"],
            summary="Get content for a specific document",
            description="Fetch content for a single document using its unique UID.",
            response_model=GetDocumentContentResponse
        )
        async def get_document_content(document_uid: str):
            """
            Endpoint to retrieve content for a single document.
            """
            try:
                logger.info(f"Retrieving document: {document_uid}")
                result = await self.service.get_document_content(document_uid)
                return result
            except HTTPException as e:
                raise e
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.error(f"Error retrieving document {document_uid}: {str(e)}")
                raise HTTPException(status_code=500, detail="An unexpected error occurred")
                
        @router.get(
            "/fullDocument/{document_uid}",
            tags=["Content"],
            summary="Get complete document with content",
            description="Fetch complete document including content using its unique UID.",
            response_model=GetDocumentContentResponse
        )
        async def get_full_document(document_uid: str):
            """
            Endpoint to retrieve a complete document including its content.
            """
            try:
                logger.info(f"Retrieving full document: {document_uid}")
                result = await self.service.get_document_content(document_uid)
                return result
            except HTTPException as e:
                raise e
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.error(f"Error retrieving full document {document_uid}: {str(e)}")
                raise HTTPException(status_code=500, detail="An unexpected error occurred")