import logging
from pydantic_settings import BaseSettings
from pydantic import Field
import os

logger = logging.getLogger(__name__)
class EmbeddingAzureApimSettings(BaseSettings):
    azure_tenant_id: str = Field(..., validation_alias="AZURE_TENANT_ID")
    azure_client_id: str = Field(..., validation_alias="AZURE_CLIENT_ID")
    azure_client_secret: str = Field(..., validation_alias="AZURE_CLIENT_SECRET")
    azure_client_scope: str = Field(..., validation_alias="AZURE_CLIENT_SCOPE")

    azure_apim_base_url: str = Field(..., validation_alias="AZURE_APIM_BASE_URL")
    azure_resource_path_embeddings: str = Field(..., validation_alias="AZURE_RESOURCE_PATH_EMBEDDINGS")
    azure_resource_path_llm: str = Field(..., validation_alias="AZURE_RESOURCE_PATH_LLM")
    azure_api_version: str = Field(..., validation_alias="AZURE_API_VERSION")
    azure_apim_key: str = Field(..., validation_alias="AZURE_APIM_KEY")
    azure_deployment_llm: str = Field(..., validation_alias="AZURE_DEPLOYMENT_LLM")
    azure_deployment_embedding: str = Field(..., validation_alias="AZURE_DEPLOYMENT_EMBEDDING")

    model_config = {
        "env_file": os.getenv("ENV_FILE", None),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

    @classmethod
    def validate_or_exit(cls):
        try:
            return cls()
        except Exception as e:
            logger.critical("❌ Invalid Azure APIM embedding settings:\n%s", e)
