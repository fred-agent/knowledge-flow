import logging
from pathlib import Path

from google.cloud import storage
from knowledge_flow_app.config.content_store_gcs_settings import ContentStoreGcsSettings
from knowledge_flow_app.stores.content.base_content_store import BaseContentStore
logger = logging.getLogger(__name__)

class GCSUploader(BaseContentStore):
    def __init__(self):
        """
        Initializes a Google Cloud Storage uploader.

        :param settings: Optional GcsSettings object. If not provided, defaults will be used.
        """
        # Load settings from env if none provided
        self.settings = ContentStoreGcsSettings()

        # Use the JSON key path if provided, otherwise fall back to default creds
        creds = self.settings.gcs_credentials_path
        if creds:
            self.client = storage.Client.from_service_account_json(creds)
        else:
            self.client = storage.Client()

        self.bucket_name = self.settings.gcs_bucket_name
        self.bucket = self.client.bucket(self.bucket_name)

        if not self.bucket.exists():
            raise RuntimeError(f"GCS bucket '{self.bucket_name}' does not exist.")

    async def upload_dir(self, doc_dir: Path):
        """
        Uploads all files in the given directory to GCS,
        preserving the document UID as the root prefix.
        """
        document_uid = doc_dir.stem

        for file_path in doc_dir.rglob("*"):
            if file_path.is_file():
                blob_name = f"{document_uid}/{file_path.name}"
                try:
                    blob = self.bucket.blob(blob_name)
                    blob.upload_from_filename(str(file_path))
                    logger.info(f"Uploaded '{blob_name}' to GCS bucket '{self.bucket_name}'.")
                except Exception as e:
                    logger.error(f"Failed to upload '{file_path}' to GCS: {e}")
