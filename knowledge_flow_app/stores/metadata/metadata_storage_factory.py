from knowledge_flow_app.application_context import ApplicationContext
from knowledge_flow_app.config.metadata_store_local_settings import MetadataStoreLocalSettings
from knowledge_flow_app.config.opensearch_settings import OpenSearchSettings
from pathlib import Path

from knowledge_flow_app.stores.metadata.base_metadata_store import BaseMetadataStore
from knowledge_flow_app.stores.metadata.local_metadata_store import LocalMetadataStore
from knowledge_flow_app.stores.metadata.opensearch_metadata_store import OpenSearchMetadataStore

def get_metadata_store() -> BaseMetadataStore:
    """
    Factory function to create a metadata store instance based on the configuration.
    As of now, it supports local and OpenSearch metadata storage.
    Returns:
        BaseMetadataStore: An instance of the metadata store.
    """
    # Get the metadata storage configuration from the application context
    config = ApplicationContext.get_instance().get_config().metadata_storage

    if config.type == "local":
        settings = MetadataStoreLocalSettings()
        return LocalMetadataStore(Path(settings.root_path).expanduser())
    elif config.type == "opensearch":
        settings = OpenSearchSettings().validate_or_exit()
        return OpenSearchMetadataStore(
            host=settings.opensearch_host,
            username=settings.opensearch_user,
            password=settings.opensearch_password,
            secure=settings.opensearch_secure,
            verify_certs=settings.opensearch_verify_certs,
            vector_index_name=settings.opensearch_vector_index,
            metadata_index_name=settings.opensearch_metadata_index
        )
    else:   
        raise ValueError(f"Unsupported metadata storage backend: {config.type}")
