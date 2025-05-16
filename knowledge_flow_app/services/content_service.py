import logging
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import HTTPException

from knowledge_flow_app.stores.content.content_storage_factory import get_content_store

logger = logging.getLogger(__name__)

class ContentService:
    """
    Service for retrieving document content and converting it to markdown.
    Focuses solely on content retrieval and conversion.
    """
    
    def __init__(self):
        """Initialize content service with necessary stores."""
        from knowledge_flow_app.stores.metadata.metadata_storage_factory import get_metadata_store
        from knowledge_flow_app.application_context import ApplicationContext
        
        self.metadata_store = get_metadata_store()
        self.content_store = get_content_store()
        self.config = ApplicationContext.get_instance().get_config()
    
    async def get_document_content(self, document_uid: str) -> Dict[str, Any]:
        """
        Get document and convert its content to markdown.
        
        Args:
            document_uid: Document unique identifier
            
        Returns:
            API response with document metadata and markdown content
        """
        if not document_uid:
            raise ValueError("Document UID cannot be empty")
        
        try:
            # Find original file name first - we'll use this regardless of which file we end up serving
            original_file_path, original_file_name = self._find_original_file(document_uid)
            
            # Create basic response structure
            response_document = {
                "uid": document_uid,
                "document_uid": document_uid,
                "file_name": original_file_name or "document.md",  # Use original name or fallback
                "content": "",
                "content_type": "text/markdown"
            }
            
            # First priority: Check if output.md exists
            markdown = self._get_output_markdown(document_uid)
            if markdown:
                response_document["content"] = markdown
                # Keep the original filename but change extension to .md if needed
                if original_file_name and not original_file_name.lower().endswith('.md'):
                    base_name = Path(original_file_name).stem
                    response_document["file_name"] = f"{base_name}.md"
                return {"status": "success", "documents": [response_document]}
            
            # Second priority: Get original file and convert to markdown
            if original_file_path and original_file_path.exists():
                response_document["content"] = self._convert_to_markdown(original_file_path)
                # Keep the original filename but change extension to .md if needed
                if not original_file_name.lower().endswith('.md'):
                    base_name = Path(original_file_name).stem
                    response_document["file_name"] = f"{base_name}.md"
                return {"status": "success", "documents": [response_document]}
            
            # If document not found, return 404
            raise HTTPException(status_code=404, detail="Document not found")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve document: {str(e)}")
    
    def _get_output_markdown(self, document_uid: str) -> Optional[str]:
        """
        Get markdown content from output.md if it exists.
        
        Args:
            document_uid: Document unique identifier
            
        Returns:
            Markdown content or None if not found
        """
        # Only check for local storage
        if self.config.content_storage.type != "local":
            return None
        
        try:
            from knowledge_flow_app.config.content_store_local_settings import ContentStoreLocalSettings
            
            # Get path to output.md
            settings = ContentStoreLocalSettings()
            output_path = Path(settings.root_path).expanduser() / document_uid / "output" / "output.md"
            
            # Check if file exists
            if output_path.exists() and output_path.is_file():
                # Read content
                try:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    logger.error(f"Error reading output.md: {str(e)}")
            
            return None
        except Exception as e:
            logger.error(f"Error accessing output.md: {str(e)}")
            return None
    
    def _find_original_file(self, document_uid: str) -> tuple:
        """
        Find the original input file (not the converted output).
        
        Args:
            document_uid: Document unique identifier
            
        Returns:
            Tuple of (file_path, file_name) or (None, None) if not found
        """
        # Only works for local storage
        if self.config.content_storage.type != "local":
            return None, None
        
        try:
            from knowledge_flow_app.config.content_store_local_settings import ContentStoreLocalSettings
            
            # Get document directory
            settings = ContentStoreLocalSettings()
            doc_dir = Path(settings.root_path).expanduser() / document_uid
            
            if not doc_dir.exists():
                return None, None
            
            # Check input directory for original file
            input_dir = doc_dir / "input"
            if input_dir.exists():
                files = list(input_dir.iterdir())
                if files:
                    return files[0], files[0].name
            
            return None, None
        except Exception as e:
            logger.error(f"Error finding original file: {str(e)}")
            return None, None
    
    def _find_document_file(self, document_uid: str) -> tuple:
        """
        Find document file in the file system.
        
        Args:
            document_uid: Document unique identifier
            
        Returns:
            Tuple of (file_path, file_name) or (None, None) if not found
        """
        # Only works for local storage
        if self.config.content_storage.type != "local":
            return None, None
        
        try:
            from knowledge_flow_app.config.content_store_local_settings import ContentStoreLocalSettings
            
            # Get document directory
            settings = ContentStoreLocalSettings()
            doc_dir = Path(settings.root_path).expanduser() / document_uid
            
            if not doc_dir.exists():
                return None, None
            
            # First check input directory
            input_dir = doc_dir / "input"
            if input_dir.exists():
                files = list(input_dir.iterdir())
                if files:
                    return files[0], files[0].name
            
            # If no files in input, check output directory
            output_dir = doc_dir / "output"
            if output_dir.exists():
                files = list(output_dir.iterdir())
                if files:
                    return files[0], files[0].name
            
            return None, None
        except Exception as e:
            logger.error(f"Error finding document file: {str(e)}")
            return None, None
    
    def _convert_to_markdown(self, file_path: Path) -> str:
        """
        Convert document to markdown based on file type.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Markdown content
        """
        try:
            # Handle different file types
            file_ext = file_path.suffix.lower()
            
            # Plain text or markdown
            if file_ext in ['.txt', '.md']:
                return self._read_text_file(file_path)
            
            # Word documents
            elif file_ext in ['.docx', '.doc']:
                return self._convert_word_to_markdown(file_path)
            
            # PDF files
            elif file_ext == '.pdf':
                return f"# {file_path.name}\n\nThis PDF document cannot be displayed as text."
            
            # Other file types
            else:
                return f"# {file_path.name}\n\nThis document type cannot be displayed as text."
                
        except Exception as e:
            logger.error(f"Error converting to markdown: {str(e)}")
            return f"# Error\n\nFailed to convert document to markdown: {str(e)}"
    
    def _read_text_file(self, file_path: Path) -> str:
        """
        Read content from a text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception:
                return f"# {file_path.name}\n\nUnable to read file content."
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            return f"# {file_path.name}\n\nError reading file: {str(e)}"
    
    def _convert_word_to_markdown(self, file_path: Path) -> str:
        """
        Convert Word document to markdown.
        
        Args:
            file_path: Path to Word document
            
        Returns:
            Markdown representation of the document
        """
        try:
            # Try docx2txt first (simpler)
            try:
                import docx2txt
                return docx2txt.process(file_path)
            except ImportError:
                # Fall back to python-docx if available
                try:
                    from docx import Document
                    doc = Document(file_path)
                    
                    # Extract text from paragraphs
                    lines = [f"# {file_path.name}", ""]
                    for para in doc.paragraphs:
                        if para.text.strip():
                            lines.append(para.text)
                            lines.append("")
                    
                    return "\n".join(lines)
                except ImportError:
                    return f"# {file_path.name}\n\nUnable to convert Word document. Required libraries not installed."
        except Exception as e:
            logger.error(f"Error converting Word document: {str(e)}")
            return f"# {file_path.name}\n\nError converting document: {str(e)}"