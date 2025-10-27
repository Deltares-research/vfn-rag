# FastAPI Application

The FastAPI application provides a REST API for interacting with VFN-RAG.

## Overview

VFN-RAG includes a FastAPI-based web application that exposes REST endpoints for document storage, retrieval, and querying.

## Running the Application

### Using Poetry

```bash
poetry run python app.py
```

### Using uvicorn

```bash
poetry run uvicorn app:app --host 0.0.0.0 --port 80 --reload
```

### Using Docker

```bash
docker build -t vfn-rag .
docker run -p 80:80 vfn-rag
```

## Interactive API Documentation

When the application is running, access the interactive documentation at:

- **Swagger UI**: http://localhost:80/docs

This interface provides comprehensive API documentation and allows you to test endpoints interactively.

## Available Endpoints

The API currently provides:

- Health checks (`/health`)
- Hello world endpoint (`/hello`)
- RAG queries (`/query`)

For detailed endpoint documentation, see the interactive Swagger docs at `/docs` when the application is running.

## Installation

For detailed installation instructions, see the [Installation Guide](../guides/installation.md).

