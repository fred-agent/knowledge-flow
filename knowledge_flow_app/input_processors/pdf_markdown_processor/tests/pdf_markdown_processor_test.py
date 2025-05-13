# tests/test_pdf_processor.py

import tempfile
from pathlib import Path
from knowledge_flow_app.input_processors.pdf_markdown_processor.pdf_markdown_processor import PdfMarkdownProcessor
import pytest

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@pytest.fixture
def sample_pdf_file():
    """Creates a simple valid PDF file with known metadata."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "test.pdf"

        # Generate a sample PDF using reportlab
        c = canvas.Canvas(str(file_path), pagesize=letter)
        c.setAuthor("Test Author")
        c.setTitle("Test Title")
        c.setSubject("Test Subject")
        c.drawString(100, 750, "Hello, this is a test PDF file.")
        c.showPage()
        c.save()

        yield file_path


@pytest.fixture
def processor():
    return PdfMarkdownProcessor()


def test_pdf_processor_end_to_end(processor, sample_pdf_file):
    output_dir = sample_pdf_file.parent / "output"
    output_dir.mkdir(exist_ok=True)

    assert processor.check_file_validity(sample_pdf_file)

    metadata = processor.process_metadata(sample_pdf_file)
    assert metadata["title"] == "Test Title"
    assert metadata["author"] == "Test Author"
    assert metadata["subject"] == "Test Subject"
    assert metadata["num_pages"] == 1
    assert "document_uid" in metadata

    result = processor.convert_file_to_markdown(sample_pdf_file, output_dir)
    assert result["status"] in ("success", "fallback_to_text")
    assert Path(result["md_file"]).exists()
    assert Path(result["md_file"]).read_text(encoding="utf-8").strip() != ""
