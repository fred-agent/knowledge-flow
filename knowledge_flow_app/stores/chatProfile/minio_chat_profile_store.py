import json
import logging
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from .base_chat_profile_store import BaseChatProfileStore

logger = logging.getLogger(__name__)

class MinioChatProfileStore(BaseChatProfileStore):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str, secure: bool):
        self.bucket_name = bucket_name
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created.")

    def save_profile(self, profile_id: str, directory: Path) -> None:
        """
        Uploads the entire chat profile folder (including profile.json and files/) to MinIO.
        """
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                object_name = f"{profile_id}/{file_path.relative_to(directory)}"
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

    def delete_profile(self, profile_id: str) -> None:
        """
        Deletes all files under a chat profile ID from the bucket.
        """
        try:
            objects_to_delete = self.client.list_objects(self.bucket_name, prefix=f"{profile_id}/", recursive=True)
            for obj in objects_to_delete:
                self.client.remove_object(self.bucket_name, obj.object_name)
                logger.info(f"Deleted '{obj.object_name}' from bucket '{self.bucket_name}'.")
        except S3Error as e:
            logger.error(f"Failed to delete profile {profile_id}: {e}")
            raise ValueError(f"Failed to delete chat profile from MinIO: {e}")

    def get_profile_description(self, profile_id: str) -> dict:
        """
        Retrieves the profile.json metadata from MinIO.
        """
        object_name = f"{profile_id}/profile.json"
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return json.loads(response.read().decode("utf-8"))
        except S3Error as e:
            logger.error(f"Failed to fetch profile.json for {profile_id}: {e}")
            raise FileNotFoundError(f"Metadata not found for chat profile: {profile_id}")

    def get_document(self, profile_id: str, document_name: str) -> BinaryIO:
        """
        Fetches a single markdown document from the files/ folder inside a profile.
        """
        object_name = f"{profile_id}/files/{document_name}"
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return BytesIO(response.read())
        except S3Error as e:
            logger.error(f"Failed to fetch document '{document_name}' for {profile_id}: {e}")
            raise FileNotFoundError(f"Document '{document_name}' not found in chat profile: {profile_id}")
