import logging
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os
logger = logging.getLogger(__name__)

class EmbeddingOpenAISettings(BaseSettings):
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    openai_api_base: str = Field(default="https://api.openai.com/v1", validation_alias="OPENAI_API_BASE")
    openai_model_name: str = Field(default="text-embedding-ada-002", validation_alias="OPENAI_MODEL_NAME")
    openai_api_version: Optional[str] = Field(default=None, validation_alias="OPENAI_API_VERSION")  # Azure needs version, OpenAI doesn't really

    model_config = {
        "extra": "ignore" # allows unrelated variables in .env or os.environ
    }

