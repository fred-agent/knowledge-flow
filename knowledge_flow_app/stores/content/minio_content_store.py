import logging
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from knowledge_flow_app.stores.content.base_content_store import BaseContentStore

logger = logging.getLogger(__name__)

class MinioContentStore(BaseContentStore):
    """
    MinIO content store for uploading files to a MinIO bucket.
    This class implements the BaseContentStore interface.
    """
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str, secure: bool):
        """
        Initializes the MinIO client and ensures the bucket exists.
        """
        self.bucket_name = bucket_name
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

        # Ensure bucket exists or create it
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully.")

    def save_content(self, document_uid: str, document_dir: Path):
        """
        Uploads all files in the given directory to MinIO,
        preserving the document UID as the root prefix.
        """
        for file_path in document_dir.rglob("*"):
            if file_path.is_file():
                object_name = f"{document_uid}/{file_path.name}"
                try:
                    self.client.fput_object(
                        self.bucket_name,
                        object_name,
                        str(file_path)
                    )
                    logger.info(f"Uploaded '{object_name}' to bucket '{self.bucket_name}'.")
                except S3Error as e:
                    logger.error(f"Failed to upload '{file_path}': {e}")
                    raise ValueError(f"Failed to upload '{file_path}': {e}")
                

    def delete_content(self, document_uid: str) -> None:
        """
        Deletes all objects in the bucket under the given document UID prefix.
        """
        try:
            objects_to_delete = self.client.list_objects(self.bucket_name, prefix=f"{document_uid}/", recursive=True)
            deleted_any = False

            for obj in objects_to_delete:
                self.client.remove_object(self.bucket_name, obj.object_name)
                logger.info(f"🗑️ Deleted '{obj.object_name}' from bucket '{self.bucket_name}'.")
                deleted_any = True

            if not deleted_any:
                logger.warning(f"⚠️ No objects found to delete for document {document_uid}.")

        except S3Error as e:
            logger.error(f"❌ Failed to delete objects for document {document_uid}: {e}")
            raise ValueError(f"Failed to delete document content from MinIO: {e}")

