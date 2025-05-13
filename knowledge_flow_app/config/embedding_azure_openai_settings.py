import logging
from pydantic_settings import BaseSettings
from pydantic import Field
import os
logger = logging.getLogger(__name__)

class EmbeddingAzureOpenAISettings(BaseSettings):
    azure_openai_base_url: str = Field(..., validation_alias="AZURE_OPENAI_BASE_URL")
    azure_openai_api_key: str = Field(..., validation_alias="AZURE_OPENAI_API_KEY")
    azure_api_version: str = Field(..., validation_alias="AZURE_API_VERSION")
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
            logger.critical("❌ Invalid Azure OpenAI embedding settings:\n%s", e)

