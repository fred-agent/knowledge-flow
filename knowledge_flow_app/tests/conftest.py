import pytest
from knowledge_flow_app.application_context import ApplicationContext
from knowledge_flow_app.common.structures import Configuration, ContentStorageConfig, EmbeddingConfig, MetadataStorageConfig, ProcessorConfig, VectorStorageConfig

@pytest.fixture(scope="function", autouse=True)
def app_context():
    """Fixture to initialize (and reset) the ApplicationContext for tests."""

    # 🧼 Force reset the singleton before initializing
    ApplicationContext._instance = None

    config = Configuration(
        security={
            "enabled": False,
            "keycloak_url": "http://fake",
            "client_id": "test-client"
        },
        content_storage=ContentStorageConfig(
            type="local"
        ),
        metadata_storage=MetadataStorageConfig(
            type="local"
        ),
        vector_storage=VectorStorageConfig(
            type="in_memory"
        ),
        embedding=EmbeddingConfig(
            type="openai"
        ),
        input_processors=[
            ProcessorConfig(
                prefix=".docx",
                class_path="knowledge_flow_app.input_processors.docx_markdown_processor.docx_markdown_processor.DocxMarkdownProcessor"
            ),
            ProcessorConfig(
                prefix=".pdf",
                class_path="knowledge_flow_app.input_processors.pdf_markdown_processor.pdf_markdown_processor.PdfMarkdownProcessor"
            ),
            ProcessorConfig(
                prefix=".pptx",
                class_path="knowledge_flow_app.input_processors.pptx_markdown_processor.pptx_markdown_processor.PptxMarkdownProcessor"
            ),
        ]
    )

    ApplicationContext(config)
