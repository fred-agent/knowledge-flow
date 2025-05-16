import logging
from pydantic_settings import BaseSettings
from pydantic import Field
import os
logger = logging.getLogger(__name__)
class ContentStoreGcsSettings(BaseSettings):
    gcs_bucket_name: str = Field(..., validation_alias="GCS_BUCKET_NAME")
    gcs_credentials_path: str = Field(..., validation_alias="GCS_CREDENTIALS_PATH")
    gcs_project_id: str = Field(..., validation_alias="GCS_PROJECT_ID")

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
            logger.critical("❌ Invalid GCS settings:\n%s", e)