# processors/sample_markdown_processor.py

from pathlib import Path

from knowledge_flow_app.input_processors.base_input_processor import BaseMarkdownProcessor

class MarkdownMarkdownProcessor(BaseMarkdownProcessor):
    def check_file_validity(self, file_path: Path) -> bool:
        return file_path.exists() and file_path.suffix in [".md"]

    def extract_file_metadata(self, file_path: Path) -> dict:
        return {
            "document_name": file_path.name,
            "size_bytes": file_path.stat().st_size,
            "suffix": file_path.suffix,
        }

    def convert_file_to_markdown(self, file_path: Path, output_dir: Path) -> dict:
        md_path = output_dir / "output.md"
        with open(file_path, "r", encoding="utf-8") as f_in, open(md_path, "w", encoding="utf-8") as f_out:
            f_out.write(f_in.read())
        return {
            "doc_dir": str(output_dir),
            "md_file": str(md_path)
        }
