# tests/test_sample_markdown_processor.py

import tempfile
from pathlib import Path

from knowledge_flow_app.input_processors.text_markdown_processor.text_markdown_processor import TextMarkdownProcessor

def test_sample_markdown_processor_end_to_end():
    processor = TextMarkdownProcessor()
    test_content = """# Sample Markdown Document

This is a **bold** statement, and _this_ is italic.

## List Example

- Item 1
- Item 2
  - Subitem

## Code Block

```python
def hello_world():
    print("Hello, Markdown!")
```
> This is a blockquote.

"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_file = temp_path / "sample.md"
        output_dir = temp_path / "output"

        input_file.write_text(test_content, encoding="utf-8")

        # Check file validity
        assert processor.check_file_validity(input_file)

        # Metadata
        metadata = processor.process_metadata(input_file)
        assert metadata["document_name"] == "sample.md"
        assert "document_uid" in metadata
        output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output_dir exists
        # Convert to markdown
        result = processor.convert_file_to_markdown(
            input_file, output_dir
        )
        output_file_path = Path(result["md_file"])
        assert output_file_path.exists()
        content_written = output_file_path.read_text(encoding="utf-8")
        assert "# Sample Markdown Document" in content_written
        assert "```python" in content_written
        assert "> This is a blockquote." in content_written
