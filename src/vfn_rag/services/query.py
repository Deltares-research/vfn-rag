"""Query service for processing RAG queries against entity knowledge bases."""

from typing import Dict

from llama_index.core import VectorStoreIndex, Settings

from vfn_rag.config.entities import get_entity_config, EntityConfig
from vfn_rag.retrieval.cosmos_client import get_cosmos_client
from vfn_rag.retrieval.cosmos import Cosmos
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding


# Lazily initialize models to ensure environment variables are loaded first
llm = None
embed_model = None


def _ensure_models_initialized():
    global llm, embed_model
    if llm is None:
        llm = azure_open_ai()
        Settings.llm = llm
    if embed_model is None:
        embed_model = get_azure_open_ai_embedding()
        Settings.embed_model = embed_model


def process_query(
    query: str,
    entity: str,
) -> Dict[str, any]:
    """Process a RAG query for a specific entity.
    
    Parameters
    ----------
    query: str
        The user's query string
    entity: str
        The entity to query (e.g., 'seal', 'seagrass')
    
    Returns
    -------
    Dict[str, any]
        Dictionary containing:
        - answer: The generated answer
        - sources: List of source file names 
        - query: The original query
        - entity: The queried entity
    
    Raises
    ------
    ValueError
        If entity is unknown or configuration is invalid
    """
    
    _ensure_models_initialized()


    config = get_entity_config(entity)
    original_query = query
    
    if config.grounded_prompt:
        query = f"{config.grounded_prompt} {query}"
    
 
    index = get_or_load_index(entity, config)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    
    sources = [
        node.metadata.get("file_name", "unknown")
        for node in response.source_nodes
    ]
    return {
        "answer": response.response,
        "sources": sources,
        "query": original_query,
        "entity": entity
    }


def get_or_load_index(entity: str, config: EntityConfig) -> VectorStoreIndex:
    """Load index for an entity from Cosmos DB.
    
    This function always loads fresh data from Cosmos DB on every call.
    
    Parameters
    ----------
    entity: str
        The entity name
    config: EntityConfig
        The entity configuration
    
    Returns
    -------
    VectorStoreIndex
        The loaded vector index
    
    Raises
    ------
    Exception
        If unable to load the index from Cosmos DB
    """
    storage_context = Cosmos.load(
        database_name=config.database_name,
        container_name=config.container_name,
        client=get_cosmos_client()
    )
    
    _ensure_models_initialized()

    index = VectorStoreIndex.from_vector_store(
        vector_store=storage_context.store.vector_store,
        embed_model=embed_model
    )
    
    return index