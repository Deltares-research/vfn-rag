"""Helpers to create a StorageContext backed by PostgreSQL with pgvector.

This module provides a small convenience class, Postgres,
which mirrors the setup performed in the Cosmos class.

The class is deliberately simple: it accepts either an already-created
connection string or individual connection parameters (host, port, database, etc.).
The create method returns a `StorageContext` configured with a
PostgreSQL vector store using pgvector extension.
"""

from typing import Optional, Any
import os
from vfn_rag.retrieval.base_storage import BaseStorage
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext


__all__ = ["Postgres"]


class Postgres(BaseStorage):
    """Factory to create a StorageContext using PostgreSQL with pgvector.

    Example:
        factory = Postgres.create(
            host="localhost",
            database="vectordb",
            user="user",
            password="password"
        )
        storage_context = factory.store

    Inputs/outputs:
    - Inputs: either `connection_string` or individual connection parameters.
    - Output: an instance of `StorageContext` (from llama_index) using
      `PGVectorStore` as the vector store.

    Notes:
    - Requires PostgreSQL with pgvector extension installed.
    - If the llama_index postgres package is not installed, importing this
      module will still succeed but calling `create` will raise at runtime.
    """

    def __init__(
        self,
        storage: StorageContext,
    ) -> None:
        super().__init__(storage)

    @classmethod
    def create(
        cls,
        table_name: str = "vector_store",
        schema_name: str = "public",
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        embed_dim: int = 3072,
        **kwargs: Any,
    ) -> "Postgres":
        """Create and return a StorageContext configured with the PostgreSQL vector store.
        
        Args:
            table_name: Name of the table to store vectors (default: "vector_store")
            schema_name: PostgreSQL schema name (default: "public")
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            user: Username
            password: Password
            connection_string: Direct connection string (overrides other parameters)
            embed_dim: Embedding dimension (default: 3072 for text-embedding-3-large)
            **kwargs: Additional arguments passed to PGVectorStore
            
        Returns:
            Postgres instance with configured storage context
        """

        storage = cls._base_read_write(
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            **kwargs
        )

        return cls(storage)

    @classmethod
    def load(
        cls,
        table_name: str = "vector_store",
        schema_name: str = "public",
        connection_string: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        embed_dim: int = 3072,
        **kwargs: Any,
    ) -> "Postgres":
        """Load an existing StorageContext from PostgreSQL.
        
        Args:
            table_name: Name of the table containing vectors (default: "vector_store")
            schema_name: PostgreSQL schema name (default: "public")
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            user: Username
            password: Password
            embed_dim: Embedding dimension (default: 3072 for text-embedding-3-large)
            **kwargs: Additional arguments passed to PGVectorStore
            
        Returns:
            Postgres instance with loaded storage context
        """

        storage = cls._base_read_write(
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            connection_string=connection_string,
            # host=host,
            port=port,
            # database=database,
            # user=user,
            # password=password,
            **kwargs
        )

        return cls(storage)

    @staticmethod
    def _base_read_write(
        table_name: str = "vector_store",
        schema_name: str = "public",
        embed_dim: int = 3072,
        connection_string: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> StorageContext:
        """Create the base storage context with PostgreSQL vector store.
        
        Args:
            connection_string: PostgreSQL connection string
            table_name: Name of the table to store vectors
            schema_name: PostgreSQL schema name
            embed_dim: Embedding dimension
            **kwargs: Additional arguments passed to PGVectorStore
            
        Returns:
            StorageContext configured with PGVectorStore
        """
        init_kwargs: dict[str, Any] = {
            "table_name": table_name,
            "schema_name": schema_name,
            "embed_dim": embed_dim,
            "connection_string": connection_string,
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
            **kwargs
        }

        store = PGVectorStore.from_params(**init_kwargs)
        storage = StorageContext.from_defaults(vector_store=store)
        return storage
