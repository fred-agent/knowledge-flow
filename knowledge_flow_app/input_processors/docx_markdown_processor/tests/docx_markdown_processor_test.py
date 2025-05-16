import tempfile
from pathlib import Path

import pytest

from knowledge_flow_app.input_processors.docx_markdown_processor.docx_markdown_processor import DocxMarkdownProcessor
from knowledge_flow_app.services.input_processor_service import InputProcessorService

@pytest.fixture
def processor():
    return DocxMarkdownProcessor()

@pytest.mark.asyncio
async def test_process_docx_file(processor):

    test_docx_path = Path("knowledge_flow_app/input_processors/docx_markdown_processor/tests/assets/sample.docx")

    assert processor.check_file_validity(test_docx_path)
    metadata = processor.process_metadata(test_docx_path)
    assert "document_uid" in metadata

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        result = processor.convert_file_to_markdown(test_docx_path, output_dir)
        print(result)

