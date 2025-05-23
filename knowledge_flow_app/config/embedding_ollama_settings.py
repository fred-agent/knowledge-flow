import logging
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os
logger = logging.getLogger(__name__)

class EmbeddingOllamaSettings(BaseSettings):
    embedding_model_name: str = Field(..., validation_alias="OLLAMA_EMBEDDING_MODEL_NAME")
    api_url: Optional[str] = Field(default=None, validation_alias="OLLAMA_API_URL")

    model_config = {
        "extra": "ignore" # allow extra environment variable 
    }
