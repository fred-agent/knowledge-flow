# tests/test_pdf_processor.py

import pytest
from pathlib import Path
from knowledge_flow_app.input_processors.pdf_markdown_processor.pdf_markdown_processor import PdfMarkdownProcessor


@pytest.fixture
def processor():
    return PdfMarkdownProcessor()


@pytest.fixture
def sample_pdf_file():
    return Path(__file__).parent / "assets" / "sample.pdf"


def test_pdf_processor_end_to_end(processor, sample_pdf_file):
    output_dir = Path("/tmp/knowledge_flow/test/output")
    output_dir.mkdir(exist_ok=True, parents=True)

    assert processor.check_file_validity(sample_pdf_file)

    metadata = processor.process_metadata(sample_pdf_file)
    
    assert metadata["document_name"] == "sample.pdf"
    # assert metadata["title"] == "Test Title"
    # assert metadata["author"] == "Test Author"
    # assert metadata["subject"] == "Test Subject"
    assert metadata["num_pages"] == 2
    assert "document_uid" in metadata

    result = processor.convert_file_to_markdown(sample_pdf_file, output_dir)
    
    assert result["status"] == "fallback_to_text"
    assert Path(result["md_file"]).exists()
    assert Path(result["md_file"]).read_text(encoding="utf-8").strip() != ""
