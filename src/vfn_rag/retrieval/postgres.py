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


def create_connection_string(
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    connection_string: Optional[str] = None,
) -> str:
    """Create a PostgreSQL connection string.
    
    Args:
        host: PostgreSQL host
        port: PostgreSQL port (default: 5432)
        database: Database name
        user: Username
        password: Password
        connection_string: Direct connection string (overrides other parameters)
        
    Returns:
        PostgreSQL connection string
    """
    if connection_string:
        return connection_string
    
    # Try to get from environment if not provided
    host = host or os.environ.get("POSTGRES_HOST")
    port = port or int(os.environ.get("POSTGRES_PORT", "5432"))
    database = database or os.environ.get("POSTGRES_DB")
    user = user or os.environ.get("POSTGRES_USER")
    password = password or os.environ.get("POSTGRES_PASSWORD")
    
    if not all([host, port, database, user, password]):
        raise ValueError(
            "Either connection_string or all of (host, port, database, user, password) must be provided"
        )
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


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
        connection_string: str,
        port: int,
    ) -> None:
        self.connection_string = connection_string
        self.port = port
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
        connection_string: Optional[str] = None,
        embed_dim: int = 3072,
        **kwargs: Any,
    ) -> "Postgres":
        """Create and return a StorageContext configured with the PostgreSQL vector store.
        
        Args:
            table_name: Name of the table to store vectors (default: "vector_store")
            schema_name: PostgreSQL schema name (default: "public")
            host: PostgreSQL host
            port: PostgreSQL port (default: 5432)
            database: Database name
            user: Username
            password: Password
            connection_string: Direct connection string (overrides other parameters)
            embed_dim: Embedding dimension (default: 3072 for text-embedding-3-large)
            **kwargs: Additional arguments passed to PGVectorStore
            
        Returns:
            Postgres instance with configured storage context
        """
        # Get port with default
        port = port or int(os.environ.get("POSTGRES_PORT", "5432"))
        
        # Create connection string if not provided
        conn_str = create_connection_string(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connection_string=connection_string,
        )

        storage = cls._base_read_write(
            connection_string=conn_str,
            port=port,
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            **kwargs
        )

        return cls(storage, conn_str, port)

    @classmethod
    def load(
        cls,
        table_name: str = "vector_store",
        schema_name: str = "public",
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        connection_string: Optional[str] = None,
        embed_dim: int = 3072,
        **kwargs: Any,
    ) -> "Postgres":
        """Load an existing StorageContext from PostgreSQL.
        
        Args:
            table_name: Name of the table containing vectors (default: "vector_store")
            schema_name: PostgreSQL schema name (default: "public")
            host: PostgreSQL host
            port: PostgreSQL port (default: 5432)
            database: Database name
            user: Username
            password: Password
            connection_string: Direct connection string (overrides other parameters)
            embed_dim: Embedding dimension (default: 3072 for text-embedding-3-large)
            **kwargs: Additional arguments passed to PGVectorStore
            
        Returns:
            Postgres instance with loaded storage context
        """
        # Get port with default
        port = port or int(os.environ.get("POSTGRES_PORT", "5432"))
        
        # Create connection string if not provided
        conn_str = create_connection_string(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connection_string=connection_string,
        )

        storage = cls._base_read_write(
            connection_string=conn_str,
            port=port,
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            **kwargs
        )

        return cls(storage, conn_str, port)

    @staticmethod
    def _base_read_write(
        connection_string: str,
        port: int,
        table_name: str = "vector_store",
        schema_name: str = "public",
        embed_dim: int = 3072,
        **kwargs: Any,
    ) -> StorageContext:
        """Create the base storage context with PostgreSQL vector store.
        
        Args:
            connection_string: PostgreSQL connection string
            port: PostgreSQL port
            table_name: Name of the table to store vectors
            schema_name: PostgreSQL schema name
            embed_dim: Embedding dimension
            **kwargs: Additional arguments passed to PGVectorStore
            
        Returns:
            StorageContext configured with PGVectorStore
        """
        init_kwargs: dict[str, Any] = {
            "connection_string": connection_string,
            "port": port,
            "table_name": table_name,
            "schema_name": schema_name,
            "embed_dim": embed_dim,
            **kwargs
        }

        store = PGVectorStore.from_params(**init_kwargs)
        storage = StorageContext.from_defaults(vector_store=store)
        return storage
