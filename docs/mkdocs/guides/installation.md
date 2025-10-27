# Installation

This guide will help you install and set up VFN-RAG.

## Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/) for dependency management
- Docker (optional, for containerized deployment)

## Installation Methods

### Method 1: Using Poetry (Recommended)

1. Clone the repository:

```bash
git clone https://github.com/Deltares-research/vfn-rag.git
cd vfn-rag
```

2. Install dependencies:

```bash
poetry install
```

To install only runtime dependencies (without development tools):

```bash
poetry install --no-dev
```

To install development dependencies:

```bash
poetry install --only=dev
```

To install analysis dependencies (Jupyter):

```bash
poetry install --only=analysis
```

To install both dev and analysis dependencies:

```bash
poetry install --only=dev,analysis
```

### Method 2: Using Docker

Build the Docker image:

```bash
docker build -t vfn- показа .
```

Run the container:

```bash
docker run -p 80:80 vfn-rag
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_API_VERSION=2024-03-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name_here

# Azure Embedding Configuration
AZURE_EMBEDDING_API_ENDPOINT=your_embedding_endpoint_here
```

## Running the Application

### Running the FastAPI Application

#### Using Poetry

```bash
poetry run python app.py
```

#### Using uvicorn

```bash
poetry run uvicorn app:app --host 0.0.0.0 --port 80 --reload
```

#### Using Docker

```bash
# Build and run in one command
docker build -t vfn-rag . && docker run -p 80:80 vfn-rag

# Or separately
docker build -t vfn-rag .
docker run -p 80:80 vfn-rag
```

Once running, access the application:
- API Documentation: http://localhost:80/docs
- Health Check: http://localhost:80/health
- Hello World: http://localhost:80/hello

### Running CLI Commands

Test the CLI:

```bash
poetry run vfn-rag hello
poetry run vfn-rag version
poetry run vfn-rag query --query "test query"
```

## Verification

1. **Test the API**:
   - Open http://localhost:80/docs in your browser
   - Click "Try it out" on any endpoint to test it

2. **Test the CLI**:
   ```bash
   poetry run vfn-rag version
   ```

3. **Check Health**:
   - Visit http://localhost:80/health

## Stopping the Application

### Docker

Stop the running container:

```bash
docker stop $(docker ps -q --filter ancestor=vfn-rag)
```

### Python

Press `Ctrl+C` in the terminal where the application is running.

## Next Steps

- [Getting Started Guide](getting-started.md) - Learn how to use VFN-RAG
- [Examples](examples.md) - Explore usage examples
- [API Reference](../api/cli.md) - Complete API documentation

