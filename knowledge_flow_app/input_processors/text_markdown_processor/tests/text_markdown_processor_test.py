# tests/test_sample_markdown_processor.py

import tempfile
from pathlib import Path

from knowledge_flow_app.input_processors.text_markdown_processor.text_markdown_processor import TextMarkdownProcessor

def test_sample_markdown_processor_end_to_end():
    processor = TextMarkdownProcessor()
    test_content = "This is a test document.\nIt should become markdown."

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_file = temp_path / "sample.txt"
        output_dir = temp_path / "output"

        input_file.write_text(test_content, encoding="utf-8")

        # Check file validity
        assert processor.check_file_validity(input_file)

        # Metadata
        metadata = processor.process_metadata(input_file)
        assert metadata["document_name"] == "sample.txt"
        assert "document_uid" in metadata

        output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output_dir exists
        # Convert to markdown
        result = processor.convert_file_to_markdown(
            input_file, output_dir
        )
        assert Path(result["md_file"]).exists()
