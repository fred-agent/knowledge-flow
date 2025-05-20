#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entrypoint for the knowledge_flow_app microservice.
"""

import argparse
import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.logging import RichHandler

from knowledge_flow_app.application_context import ApplicationContext
from knowledge_flow_app.common.structures import Configuration
from knowledge_flow_app.common.utils import parse_server_configuration
from knowledge_flow_app.controllers.content_controller import ContentController
from knowledge_flow_app.controllers.ingestion_controller import \
    IngestionController
from knowledge_flow_app.controllers.metadata_controller import \
    MetadataController
from knowledge_flow_app.controllers.vector_search_controller import \
    VectorSearchController

load_dotenv()

logger = logging.getLogger(__name__)
app: FastAPI = None  # Global app instance for optional reuse


def configure_logging():
    """Configure logging dynamically based on LOG_LEVEL environment variable."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level not in valid_levels:
        log_level = "INFO"
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=False, show_time=False, show_path=False)],
    )
    logging.getLogger().info(f"Logging configured at {log_level} level.")
    
def create_app(config_path: str = "./config/configuration.yaml", base_url: str = "/knowledge/v1") -> FastAPI:
    """
    Creates the FastAPI application and registers routes and middleware.
    """
    global app
    configuration: Configuration = parse_server_configuration(config_path)
    ApplicationContext(configuration)

    app = FastAPI(
        docs_url=f"{base_url}/docs",
        redoc_url=f"{base_url}/redoc",
        openapi_url=f"{base_url}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router = APIRouter()
    IngestionController(router)
    VectorSearchController(router)
    MetadataController(router)
    ContentController(router)
    app.include_router(router, prefix=base_url)

    return app


def main():
    configure_logging()
    """
    Parses CLI arguments and starts the Uvicorn server.
    """
    parser = argparse.ArgumentParser(description="Start the knowledge_flow_app microservice")

    parser.add_argument("--config-path", dest="server_configuration_path", default="./config/configuration.yaml", help="Path to configuration YAML file")
    parser.add_argument("--base-url", dest="server_base_url_path", default="/knowledge/v1", help="Base path for all API endpoints")
    parser.add_argument("--server-address", dest="server_address", default="0.0.0.0", help="Server binding address")
    parser.add_argument("--server-port", dest="server_port", type=int, default=8111, help="Server port")
    parser.add_argument("--log-level", dest="server_log_level", default="info", help="Logging level")

    args = parser.parse_args()

    app = create_app(args.server_configuration_path, args.server_base_url_path)

    uvicorn.run(
        app,
        host=args.server_address,
        port=args.server_port,
        log_level=args.server_log_level,
    )


if __name__ == "__main__":
    main()
