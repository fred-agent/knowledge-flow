# Knowledge Flow Backend

A modular **FastAPI microservice** for ingesting and structuring knowledge from documents.
This component is designed to be easily extended with various vector stores or completely different 
output processing once you have extracted information and knowledge from your input documents. 

## ✨ Features

- **Document ingestion** (DOCX, PDF, PPTX): conversion to Markdown or structured formats
- **Vectorization** of content for semantic search
- **Flexible storage backends** (MinIO, local filesystem)
- **Metadata indexing** using OpenSearch or in memory storage
- **Configurable processors** using a simple YAML file

---

## Table of Contents

- [Processor Variants](#processor-variants)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Environment Setup](#environment-setup)
- [Installation](#installation)
- [Development Mode](#development-mode)
- [Endpoints](#endpoints)
- [Makefile Commands](#makefile-commands)
- [Other Information](#other-information)

---

## Processor Variants

The backend distinguishes **two types of processors**:

### Input Processors

**Purpose**: Extract structured content and metadata from uploaded files.

- **Markdown Input Processors**  
  Handle unstructured textual documents like PDFs, DOCX, PPTX, and TXT.  
  Output: clean, unified Markdown for downstream processing.

  Example use cases:
  - Preparing content for LLM analysis
  - Enabling semantic search or RAG pipelines

- **Tabular Input Processors**  
  Handle structured tabular data such as CSV or Excel files.  
  Output: normalized rows and fields.

  Example use cases:
  - SQL-style querying
  - Dashboards and analytics

📌 *Each input processor should specialize in a single file type for clarity and maintainability.*

### Output Processors

**Purpose**: Post-process extracted knowledge (from Input Processors) and prepare it for storage, search, or advanced querying.

- **Vectorization Output Processors**  
  Transform text chunks into vector embeddings and store them into vector databases (e.g., OpenSearch, In Memory Langchain) Store.

- **Tabular Output Processors**  
  Process extracted tabular data for storage or analytics.

📌 *Output processors can be customized to plug into different backends (OpenSearch, Pinecone, SQL databases, etc.).*

### Default Vectorisation Processor

Many of you will want to reuse here the provided Vectorization output processor
that provides a ready-to-use, complete and fairly configurable vectorization pipeline. Here is its processing logic:

```txt
 [ FILE PATH + METADATA ]
             │
             ▼
┌───────────────────────────────┐
│    DocumentLoaderInterface    │  (ex: LocalFileLoader)
└───────────────────────────────┘
             │
             ▼
┌───────────────────────────────┐
│     TextSplitterInterface     │  (ex: RecursiveSplitter)
└───────────────────────────────┘
             │
             ▼
┌───────────────────────────────┐
│   EmbeddingModelInterface     │  (ex: AzureEmbedder)
└───────────────────────────────┘
             │
             ▼
┌───────────────────────────────┐
│   VectorStoreInterface        │  (ex: OpenSearch, In Memory) 
└───────────────────────────────┘
             │
             ▼
┌───────────────────────────-───┐
│   BaseMetadataStore           │  (ex: OpenSearch, Local)
└───────────────────────────────┘
```

Each step is handled by a modular, replaceable component.
This design allows easy switching of backends (e.g., OpenSearch ➔ ChromaDB, Azure ➔ HuggingFace).

---

## Project Structure

```text
## Project Structure

```text
knowledge_flow_app/
├── main.py                    # FastAPI app entrypoint
├── application_context.py      # Singleton managing configuration and processors

├── config/                     # Configuration for external services (Azure, OpenAI, etc.)
│   └── [service]_settings.py

├── controllers/                # API endpoints (FastAPI routers)
│   ├── ingestion_controller.py
│   └── metadata_controller.py

├── input_processors/           # Input processors: parse uploaded files
│   ├── base_input_processor.py
│   ├── [filetype]_markdown_processor/
│   └── csv_tabular_processor/

├── output_processors/          # Output processors: transform extracted knowledge
│   ├── base_output_processor.py
│   ├── tabular_processor/
│   └── vectorization_processor/

├── services/                   # Business logic services
│   ├── ingestion_service.py
│   ├── input_processor_service.py
│   └── output_processor_service.py

├── stores/                     # Storage backends for metadata and documents
│   ├── content/
│   └── metadata/

├── common/                     # Shared utilities and data structures
│   └── structures.py

└── tests/                      # Tests and sample assets
```

---

## Developer Guide

| What you would like to do | Where to do it |
|:-----|:-------------|
| ➡️ New **Input Processor** | Add in `input_processors/` |
| ➡️ New **Output Processor** | Add in `output_processors/` |
| ➡️ New **Service Logic** | Add in `services/` |
| ➡️ New **API Endpoint** | Add in `controllers/` |
| ➡️ New **Storage Backend** | Add in `stores/content/` or `stores/metadata/` |

---

## Configuration

All main settings are controlled by a `configuration.yaml` file.
Refer to the [config/configuration.yaml](config/configuration.yaml)  for a documented example.

---

## Environment Setup

Before starting the application, you must configure your environment variables.

### 1. `.env` file

Copy the provided template:

```bash
cp knowledge_flow_app/config/.env.template .env
```

Edit the `.env` file according to your setup.

This file controls:

| Category            | Purpose                                 |
| ------------------- | --------------------------------------- |
| Content Storage     | Local folder, MinIO, or GCS             |
| Metadata Storage    | Local JSON file or OpenSearch cluster   |
| Vector Storage      | OpenSearch or other future backends     |
| Embedding Backend   | OpenAI API, Azure OpenAI, or APIM setup |

---

### 2. Minimal `.env` example for **Local Storage + OpenAI Embeddings**

```env
# Content Storage
LOCAL_STORAGE_PATH=~/.knowledge-flow/content-store

# Metadata Storage
LOCAL_STORAGE_PATH=~/.knowledge-flow/metadata-store.json

# OpenAI Settings
OPENAI_API_KEY="your-openai-api-key"
OPENAI_MODEL_NAME="text-embedding-ada-002"
```

✅ With this, you can run everything locally without MinIO or OpenSearch.

---

### 3. Required `.env` Variables by Feature

| Feature         | Required Variables |
|:----------------|:--------------------|
| Local Storage   | `LOCAL_STORAGE_PATH` |
| MinIO Storage   | `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET_NAME`, `MINIO_SECURE` |
| GCS Storage     | `GCS_PROJECT_ID`, `GCS_BUCKET`, `GCS_KEY_FILE` |
| OpenSearch      | `OPENSEARCH_HOST`, `OPENSEARCH_USER`, `OPENSEARCH_PASSWORD`, `OPENSEARCH_VECTOR_INDEX`, `OPENSEARCH_METADATA_INDEX` |
| OpenAI Embedding| `OPENAI_API_KEY`, `OPENAI_MODEL_NAME` |
| Azure OpenAI (Direct) | `AZURE_OPENAI_BASE_URL`, `AZURE_OPENAI_API_KEY`, `AZURE_DEPLOYMENT_LLM`, `AZURE_DEPLOYMENT_EMBEDDING`, `AZURE_API_VERSION` |
| Azure OpenAI (via APIM) | `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_CLIENT_SCOPE`, `AZURE_APIM_BASE_URL`, `AZURE_RESOURCE_PATH_EMBEDDINGS`, `AZURE_RESOURCE_PATH_LLM`, `AZURE_APIM_KEY` |

---

### 4. Important Notes

- **If using OpenSearch**, you must launch OpenSearch before running the backend.
- **If using MinIO**, you must ensure your bucket exists.
- **Azure / APIM keys** must be valid if you select Azure as your embedding backend.

---

## Installation

Use Python 3.12+ and Poetry for dependency management.

### Setup Environment

```bash
make dev
```

Creates `.venv` and installs all dependencies.

### Optional: Build the project

```bash
make build
```

---

## Development Mode

To run the backend locally:

```bash
make run
```

Then open:

- Swagger: [http://localhost:8111/knowledge/v1/docs](http://localhost:8111/knowledge/v1/docs)
- ReDoc: [http://localhost:8111/knowledge/v1/redoc](http://localhost:8111/knowledge/v1/redoc)

### VsCode configuration

Here is a typical launch.json file you need in knowledge-flow/.vscode folder: 

```json
{
    "configurations": [

      {
        "type": "debugpy",
        "request": "launch",
        "name": "Launch FastAPI App",
        "program": "${workspaceFolder}/knowledge_flow_app/main.py",
        "args": [
          "--config-path",
          "${workspaceFolder}/config/configuration.yaml"
        ],
        "envFile": "${workspaceFolder}/config/.env"
      },
      {
        "name": "Debug Pytest Current File",
        "type": "debugpy",
        "request": "launch",
        "module": "pytest",
        "justMyCode": false,
        "args": [
          "${file}"
        ]
      }
      
    ]
  }
```

---

## Endpoints

### `/upload-documents`

- Upload DOCX, PDF, or PPTX files.
- Converts them to Markdown.
- Stores both metadata and content in the configured backend.

### `/documents/metadata`

- Retrieve a filtered list of documents (based on metadata).

### `/document/{uid}`

- Get metadata for a specific document.

### `/document/{uid}/retrievable`

- Mark a document as retrievable (or not).

---

## Makefile Commands

| Command             | Description                           |
| ------------------- | ------------------------------------- |
| `make dev`          | Create virtual env and install deps   |
| `make run`          | Start the FastAPI server              |
| `make build`        | Build Python package                  |
| `make docker-build` | Build Docker image                    |
| `make test`         | Run all tests                         |
| `make clean`        | Clean virtual env and build artifacts |

---

## Other Information

- Entry point: [`main.py`](./knowledge_flow_app/main.py)
- Custom configuration path: `--server.configurationPath`
- Logs: set `--server.logLevel=debug` to see full logs
- Compatible with Azure OpenAI, OpenAI API, and (future) other LLM backends.

---
