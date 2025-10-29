"""Cosmos DB client management with singleton pattern."""

from typing import Optional
from azure.cosmos import CosmosClient
import os


_client: Optional[CosmosClient] = None


def get_cosmos_client() -> CosmosClient:
    """Get or create a Cosmos client instance (singleton pattern).
    
    The client is created lazily on first access and cached for subsequent calls.
    This ensures a single shared client across the application with connection pooling.
    
    Returns
    -------
    CosmosClient
        The Azure Cosmos client instance
    
    Raises
    ------
    ValueError
        If Azure Cosmos DB credentials are not configured
    """
    global _client
    if _client is None:
        uri = os.getenv("AZURE_COSMOSDB_URI")
        key = os.getenv("AZURE_COSMOSDB_KEY")
        
        if not uri or not key:
            raise ValueError("Azure Cosmos DB credentials not configured. Set AZURE_COSMOSDB_URI and AZURE_COSMOSDB_KEY environment variables.")
        
        _client = CosmosClient(uri, credential=key)
    
    return _client


def reset_client():
    """Reset the cached client (useful for testing or reconnection).
    
    The next call to get_cosmos_client() will create a new client instance.
    """
    global _client
    _client = None

