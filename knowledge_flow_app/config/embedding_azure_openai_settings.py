import logging
from pydantic import Field, ValidationError
import os

from pydantic_settings import BaseSettings
logger = logging.getLogger(__name__)

class EmbeddingAzureOpenAISettings(BaseSettings):
    azure_openai_base_url: str = Field(..., validation_alias="AZURE_OPENAI_BASE_URL")
    azure_openai_api_key: str = Field(..., validation_alias="AZURE_OPENAI_API_KEY")
    azure_api_version: str = Field(..., validation_alias="AZURE_API_VERSION")
    azure_deployment_llm: str = Field(..., validation_alias="AZURE_DEPLOYMENT_LLM")
    azure_deployment_embedding: str = Field(..., validation_alias="AZURE_DEPLOYMENT_EMBEDDING")

    model_config = {
        "extra": "ignore" # allows unrelated variables in .env or os.environ
    }

