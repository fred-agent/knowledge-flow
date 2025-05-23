# Copyright Thales 2025
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import shutil
import logging
from pathlib import Path

import pypdf
from pypdf.errors import PdfReadError
from docling.document_converter import DocumentConverter

from knowledge_flow_app.input_processors.base_input_processor import BaseMarkdownProcessor

logger = logging.getLogger(__name__)

class PdfMarkdownProcessor(BaseMarkdownProcessor):
    def check_file_validity(self, file_path: Path) -> bool:
        """Checks if the PDF is readable and contains at least one page."""
        try:
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                if len(reader.pages) == 0:
                    logger.warning(f"The PDF file {file_path} is empty.")
                    return False
                return True
        except PdfReadError as e:
            logger.error(f"Corrupted PDF file: {file_path} - {e}")
        except Exception as e:
            logger.error(f"Unexpected error while validating {file_path}: {e}")
        return False

    def extract_file_metadata(self, file_path: Path) -> dict:
        """Extracts metadata from the PDF file."""
        metadata = {"document_name": file_path.name}
        try:
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                info = reader.metadata or {}

                metadata.update({
                    "title": info.title.strip() if info.title else "Unknown",
                    "author": info.author.strip() if info.author else "Unknown",
                    "subject": info.subject.strip() if info.subject else "Unknown",
                    "num_pages": len(reader.pages),
                })
        except Exception as e:
            logger.error(f"Error extracting metadata from PDF: {e}")
            metadata["error"] = str(e)
        return metadata

    def convert_file_to_markdown(self, file_path: Path, output_dir: Path) -> dict:

        md_path = output_dir / "output.md"

        converter = DocumentConverter()
        
        try:
            result = converter.convert(file_path)
            md_path.write_text(result.document.export_to_markdown())
        except Exception as fallback_error:
            logger.error(f"Fallback text extraction also failed: {fallback_error}")
            return {
                "doc_dir": str(output_dir),
                "md_file": None,
                "status": "error",
                "message": str(fallback_error),
            }

        return {
            "doc_dir": str(output_dir),
            "md_file": str(md_path),
            "status": "fallback_to_text",
            "message": "Conversion to plain text fallback succeeded.",
        }
