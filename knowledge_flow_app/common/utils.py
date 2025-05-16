import yaml
from typing import Dict

from knowledge_flow_app.common.structures import Configuration

def parse_server_configuration(configuration_path: str) -> Configuration:
    """
    Parses the server configuration from a YAML file.

    Args:
        configuration_path (str): The path to the configuration YAML file.

    Returns:
        Configuration: The parsed configuration object.
    """
    with open(configuration_path, "r") as f:
        try:
            config: Dict = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error while parsing configuration file {configuration_path}: {e}")
            exit(1)
    return Configuration(**config)


def get_embedding_model_name(embedding_model: object) -> str:
    """
    Returns a clean string name for the embedding model, even if wrapped inside a custom class.
    """
    if hasattr(embedding_model, "model"):
        inner = getattr(embedding_model, "model")
        return getattr(inner, "model", type(inner).__name__)
    return getattr(embedding_model, "model", type(embedding_model).__name__)
