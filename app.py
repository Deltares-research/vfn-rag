from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from vfn_rag.services.query import process_query
from vfn_rag.config.entities import ENTITY_MAPPING

# Initialize FastAPI app
app = FastAPI(
    title="VFN-RAG API",
    description="RAG (Retrieval-Augmented Generation) API for voice-for-nature project",
    version="1.0.0"
)

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    query: str
    entity: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    query: str
    entity: str

class HelloResponse(BaseModel):
    message: str
    service: str

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for container monitoring"""
    return {"status": "healthy", "service": "vfn-rag"}

# Hello world endpoint
@app.get("/hello", response_model=HelloResponse)
def hello_world():
    """Simple hello world endpoint"""
    return HelloResponse(
        message="Hello World from vfn-rag container!",
        service="vfn-rag"
    )

# RAG query endpoint
@app.post("/query", response_model=QueryResponse)
def rag_query(request: QueryRequest):
    """RAG query endpoint with entity selection"""
    try:
        # Validate entity
        if request.entity not in ENTITY_MAPPING:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown entity: '{request.entity}'. Available entities: {list(ENTITY_MAPPING.keys())}"
            )
        
        # Process query through service layer
        result = process_query(
            query=request.query,
            entity=request.entity
        )
        
        return QueryResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List available entities
@app.get("/entities")
def list_entities():
    """List all available entity knowledge bases"""
    return {
        "entities": {
            entity: {"description": config.description}
            for entity, config in ENTITY_MAPPING.items()
        }
    }

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "VFN-RAG API is running",
        "docs": "/docs",
        "health": "/health",
        "hello": "/hello",
        "query": "/query",
        "entities": "/entities"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
