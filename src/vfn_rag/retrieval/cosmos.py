"""Helpers to create a StorageContext backed by Azure Cosmos DB (NoSQL).

This module provides a small convenience class, CosmosStorageContextFactory,
which mirrors the setup performed in the example AzureCosmosDBNoSqlDemo.py.

The class is deliberately simple: it accepts either an already-created
azure.cosmos.CosmosClient instance or the connection URI and key, plus
optional indexing/vector policies and container/database properties. The
create_storage_context method returns a `StorageContext` configured with an
`AzureCosmosDBNoSqlVectorSearch` vector store.
"""

from typing import Optional, Dict, Any
import os
from vfn_rag.retrieval.base_storage import BaseStorage
from azure.cosmos import CosmosClient, PartitionKey
from llama_index.vector_stores.azurecosmosnosql import AzureCosmosDBNoSqlVectorSearch
from llama_index.core import StorageContext

CONTAINER_PROPERTIES = {"partition_key": PartitionKey(path="/id")}
VectorEmbeddingPolicy = {
    "vectorEmbeddings": [
        {
            "path": "/embedding",
            "dataType": "float32",
            "distanceFunction": "cosine",
            "dimensions": 3072,
        }
    ]
}

INDEXING_POLICY = {
    "indexingMode": "consistent",
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{"path": '/"_etag"/?'}],
    "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
}


__all__ = ["Cosmos"]


def create_client(uri: str, key: str) -> CosmosClient:
    """Create a CosmosClient instance."""
    if uri is None:
        uri = os.environ.get("AZURE_COSMOSDB_URI")
    if key is None:
        key = os.environ.get("AZURE_COSMOSDB_KEY")
    if uri is None or key is None:
        raise ValueError("Either cosmos_client or both uri and key must be provided")

    return CosmosClient(uri, credential=key)


class Cosmos(BaseStorage):
    """Factory to create a StorageContext using Azure Cosmos DB NoSQL.

    Example:
        factory = CosmosStorageContextFactory(uri, key)
        storage_context = factory.create_storage_context()

    Inputs/outputs:
    - Inputs: either `cosmos_client` or (`uri` and `key`). Optional policies.
    - Output: an instance of `StorageContext` (from llama_index) using
      `AzureCosmosDBNoSqlVectorSearch` as the vector store.

    Notes:
    - If the llama_index/azure packages are not installed, importing this
      module will still succeed but calling `create_storage_context` will
      raise at runtime.
    """

    def __init__(
        self,
        storage: StorageContext,
        client: CosmosClient,
    ) -> None:
        self.client = client
        self.pipeline = None
        super().__init__(storage)

    @classmethod
    def create(
        cls,
        database_name: str,
        container_name: str,
        client: Optional[CosmosClient] = None,
        uri: Optional[str] = None,
        key: Optional[str] = None,
        **kwargs: Any,
    ) -> "Cosmos":
        """Create and return a StorageContext configured with the Cosmos vector store."""

        if client is None:
            client = create_client(uri, key)

        storage = cls._base_read_write(
            database_name, container_name, client, create_container=True, **kwargs
        )

        return cls(storage, client)

    @classmethod
    def load(
        cls,
        database_name: str,
        container_name: str,
        client: Optional[CosmosClient] = None,
        uri: Optional[str] = None,
        key: Optional[str] = None,
        **kwargs: Any,
    ):
        if client is None:
            client = create_client(uri, key)

        storage = cls._base_read_write(
            database_name, container_name, client, create_container=False, **kwargs
        )

        return cls(storage, client)

    @staticmethod
    def _base_read_write(
        database_name: str,
        container_name: str,
        client: Optional[CosmosClient],
        create_container: bool = False,
        indexing_policy: Optional[Dict[str, Any]] = None,
        vector_embedding_policy: Optional[Dict[str, Any]] = None,
        cosmos_container_properties: Optional[Dict[str, Any]] = None,
        cosmos_database_properties: Optional[Dict[str, Any]] = None,
    ) -> StorageContext:

        init_kwargs: Dict[str, Any] = {
            "cosmos_client": client,
            "database_name": database_name,
            "container_name": container_name,
            "vector_embedding_policy": vector_embedding_policy or VectorEmbeddingPolicy,
            "indexing_policy": indexing_policy or INDEXING_POLICY,
            "cosmos_container_properties": cosmos_container_properties or CONTAINER_PROPERTIES,
            "cosmos_database_properties": cosmos_database_properties or {},
            "create_container": create_container,
        }

        store = AzureCosmosDBNoSqlVectorSearch(**init_kwargs)
        storage = StorageContext.from_defaults(vector_store=store)
        return storage

    