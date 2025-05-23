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




