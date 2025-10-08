# voice-for-nature
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Installation
```bash
poetry install
```
### Install only dependencies
```bash
poetry install --no-dev
```
## install dev dependencies
```bash
poetry install --only=dev
```

## install the analysis dependencies
```bash
poetry install --only=analysis
```

to install both the dev and analysis dependencies
```bash
poetry install --only=dev,analysis
```

## Run the FastAPI Application

### Method 1: Using Poetry (Recommended)
```bash
# Install dependencies first
poetry install

# Run the FastAPI app
poetry run python app.py
```

### Method 2: Using Poetry with uvicorn directly
```bash
# Run with uvicorn for better performance
poetry run uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

### Method 3: Using CLI commands
```bash
# Test CLI commands
poetry run vfn-rag hello
poetry run vfn-rag version
poetry run vfn-rag query --query "test query"
```

## API Endpoints

Once the FastAPI app is running, you can access:

- **API Documentation:** http://localhost:5000/docs
- **Health Check:** http://localhost:5000/health
- **Hello World:** http://localhost:5000/hello
- **Root:** http://localhost:5000/


### Using browser:
- Open http://localhost:5000/docs for interactive API documentation
- Click "Try it out" on any endpoint to test it

## Run with Docker

### Build and Run Container
```bash
# Build the Docker image and run the container
docker build -t vfn-rag . && docker run -p 80:80 vfn-rag
```

### Alternative: Build and Run Separately
```bash
# Build the Docker image
docker build -t vfn-rag .

# Run the container
docker run -p 80:80 vfn-rag
```

### Test the Container
Once the container is running, test the endpoints:
- **API Documentation:** http://localhost:80/docs
- **Health Check:** http://localhost:80/health
- **Hello World:** http://localhost:80/hello

### Stop the Container
```bash
# Stop the running container
docker stop $(docker ps -q --filter ancestor=vfn-rag)
```