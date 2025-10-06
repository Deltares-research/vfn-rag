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
docker build -t vfn-rag . && docker run -p 5000:5000 vfn-rag
```

### Alternative: Build and Run Separately
```bash
# Build the Docker image
docker build -t vfn-rag .

# Run the container
docker run -p 5000:5000 vfn-rag
```

### Test the Container
Once the container is running, test the endpoints:
- **API Documentation:** http://localhost:5000/docs
- **Health Check:** http://localhost:5000/health
- **Hello World:** http://localhost:5000/hello

### Stop the Container
```bash
# Stop the running container
docker stop $(docker ps -q --filter ancestor=vfn-rag)
```

## Run the Web application
```bash
poetry run streamlit run src\voice_for_nature_backend\app.py
```

# eBird API

## Get API Key
https://ebird.org/api/keygen

## eBird API UI
https://ebird-api-ui.com/


## Help
https://support.ebird.org/en/support/solutions/48000450743?__hstc=75100365.0adbf9eb515854b31ac354f97e0e20b9.1726650992004.1726650992004.1726659709561.2&__hssc=75100365.59.1726659342230&__hsfp=526774486&_gl=1*215rzm*_gcl_au*MTA1MTY0OTY0Ny4xNzI2NjUwOTkx*_ga*MTU5NjA5NTgzMy4xNzI2NjUwOTkx*_ga_QR4NVXZ8BM*MTcyNjY2NDE2Mi4zLjEuMTcyNjY2NDgxOS42MC4wLjA.&_ga=2.32463165.2010216176.1726650991-1596095833.1726650991
