
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

from azure.cosmos import CosmosClient, PartitionKey
from llama_index.vector_stores.azurecosmosnosql import AzureCosmosDBNoSqlVectorSearch
from llama_index.core import StorageContext


class CosmosStorageContextFactory:
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
		cosmos_client: Optional[CosmosClient] = None,
		uri: Optional[str] = None,
		key: Optional[str] = None,
		indexing_policy: Optional[Dict[str, Any]] = None,
		vector_embedding_policy: Optional[Dict[str, Any]] = None,
		cosmos_container_properties: Optional[Dict[str, Any]] = None,
		cosmos_database_properties: Optional[Dict[str, Any]] = None,
		database_name: Optional[str] = None,
		container_name: Optional[str] = None,
		create_container: bool = False,
	) -> None:
		if cosmos_client is None:
			if uri is None:
				uri = os.environ.get("AZURE_COSMOSDB_URI")
			if key is None:
				key = os.environ.get("AZURE_COSMOSDB_KEY")
			if uri is None or key is None:
				raise ValueError("Either cosmos_client or both uri and key must be provided")
			cosmos_client = CosmosClient(uri, credential=key)

		self.cosmos_client = cosmos_client
		self.indexing_policy = indexing_policy or {
			"indexingMode": "consistent",
			"includedPaths": [{"path": "/*"}],
			"excludedPaths": [{"path": '/"_etag"/?'}],
			"vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
		}

		self.vector_embedding_policy = vector_embedding_policy or {
			"vectorEmbeddings": [
				{
					"path": "/embedding",
					"dataType": "float32",
					"distanceFunction": "cosine",
					"dimensions": 3072,
				}
			]
		}

		if cosmos_container_properties is not None:
			self.cosmos_container_properties = cosmos_container_properties
		else:
			self.cosmos_container_properties = {"partition_key": PartitionKey(path="/id")}
		self.cosmos_database_properties = cosmos_database_properties or {}
		# when connecting to an existing deployment we usually don't want to create
		self.database_name = database_name
		self.container_name = container_name
		self.create_container = create_container

	def create_storage_context(self) -> StorageContext:
		"""Create and return a StorageContext configured with the Cosmos vector store."""
		init_kwargs: Dict[str, Any] = {
			"cosmos_client": self.cosmos_client,
			"vector_embedding_policy": self.vector_embedding_policy,
			"indexing_policy": self.indexing_policy,
			"cosmos_container_properties": self.cosmos_container_properties,
			"cosmos_database_properties": self.cosmos_database_properties,
			"create_container": self.create_container,
		}
		if self.database_name is not None:
			init_kwargs["database_name"] = self.database_name
		if self.container_name is not None:
			init_kwargs["container_name"] = self.container_name

		store = AzureCosmosDBNoSqlVectorSearch(**init_kwargs)

		return StorageContext.from_defaults(vector_store=store)

