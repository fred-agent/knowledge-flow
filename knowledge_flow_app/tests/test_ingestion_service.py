from pathlib import Path

from knowledge_flow_app.services.ingestion_service import IngestionService

def test_ingestion_service():
    # Initialize service
    ingestion_service = IngestionService()
    # Load the sample file
    temp_file = ingestion_service.save_file_to_temp(Path("knowledge_flow_app/tests/assets/sample.docx"))
    assert temp_file.exists()
    assert temp_file.is_file()
    assert temp_file.name == "sample.docx"

    # 🧪 Step 2: Extract metadata
    metadata = ingestion_service.extract_metadata(temp_file, {"source": "test"})
    assert "document_uid" in metadata




