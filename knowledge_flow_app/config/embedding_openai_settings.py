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
        "env_file": os.getenv("ENV_FILE", None),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

    @classmethod
    def validate_or_exit(cls):
        try:
            return cls()
        except Exception as e:
            logger.critical("❌ Invalid OpenAI embedding settings:\n%s", e)

