"""PostgreSQL database management for vector storage.

This module provides a PostgresManager class for managing PostgreSQL databases
independently of LlamaIndex. It handles table creation, data insertion, and
direct database operations.
"""

from typing import Optional, Sequence
import os
import json
from llama_index.core.schema import BaseNode, MetadataMode
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_batch


__all__ = ["PostgresManager"]


class PostgresManager:
    """Manages PostgreSQL database operations for vector storage.
    
    This class handles direct database operations including table creation
    and data insertion, separate from LlamaIndex retrieval functionalities.
    
    Example:
        # Create manager with connection string
        manager = PostgresManager(
            connection_string="postgresql://user:pass@localhost:5432/db"
        )
        
        # Or with individual parameters
        manager = PostgresManager.from_params(
            host="localhost",
            database="vectordb",
            user="user",
            password="password"
        )
        
        # Create a table
        manager.create_table(
            table_name="my_vectors",
            schema_name="public",
            embed_dim=3072
        )
        
        # Insert nodes
        manager.insert_nodes(nodes, table_name="my_vectors")
    """
    
    def __init__(self, connection_string: str):
        """Initialize PostgresManager with a connection string.
        
        Args:
            connection_string: PostgreSQL connection string
        """
        self.connection_string = connection_string
    
    @classmethod
    def from_params(
        cls,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> "PostgresManager":
        """Create PostgresManager from individual connection parameters.
        
        Args:
            host: PostgreSQL host
            port: PostgreSQL port (default: 5432)
            database: Database name
            user: Username
            password: Password
            
        Returns:
            PostgresManager instance
        """
        # Try to get from environment if not provided
        host = host or os.environ.get("POSTGRES_HOST")
        port = port or int(os.environ.get("POSTGRES_PORT", "5432"))
        database = database or os.environ.get("POSTGRES_DB")
        user = user or os.environ.get("POSTGRES_USER")
        password = password or os.environ.get("POSTGRES_PASSWORD")
        
        if not all([host, port, database, user, password]):
            raise ValueError(
                "All of (host, port, database, user, password) must be provided or set in environment"
            )
        
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return cls(connection_string)
    
    def create_table(
        self,
        table_name: str = "vector_store",
        schema_name: str = "public",
        embed_dim: int = 3072,
    ) -> None:
        """Create the vector store table in PostgreSQL.
        
        This method creates the table structure required for storing vectors,
        including the pgvector extension and the vector column.
        
        Args:
            table_name: Name of the table to create
            schema_name: PostgreSQL schema name (default: "public")
            embed_dim: Dimension of the embedding vectors (default: 3072)
            
        Raises:
            psycopg2.Error: If table creation fails
        """
        conn = None
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(self.connection_string)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Create pgvector extension if it doesn't exist
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Create schema if it doesn't exist
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
            
            # Create the table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                id BIGSERIAL NOT NULL,
                text VARCHAR NOT NULL,
                metadata_ JSON NULL,
                node_id VARCHAR NULL,
                embedding vector({embed_dim}) NULL,
                CONSTRAINT {table_name}_pkey PRIMARY KEY (id)
            );
            """
            cur.execute(create_table_sql)
            
            # Create index on node_id for faster lookups
            # cur.execute(f"""
            # CREATE INDEX IF NOT EXISTS {table_name}_node_id_idx 
            # ON {schema_name}.{table_name} (node_id);
            # """)
            
            # Create vector index for similarity search (HNSW)
            # cur.execute(f"""
            # CREATE INDEX IF NOT EXISTS {table_name}_embedding_idx 
            # ON {schema_name}.{table_name} 
            # USING hnsw (embedding vector_cosine_ops);
            # """)
            
            cur.close()
            print(f"Table {schema_name}.{table_name} created successfully.")
            
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def insert_nodes(
        self,
        nodes: Sequence[BaseNode],
        table_name: str = "vector_store",
        schema_name: str = "public",
    ) -> None:
        """Insert a list of BaseNode objects into the PostgreSQL table.
        
        This method directly inserts nodes into the database,
        extracting the text, metadata, node_id, and embedding from each node.
        
        Args:
            nodes: Sequence of BaseNode objects to insert
            table_name: Name of the table to insert into (default: "vector_store")
            schema_name: PostgreSQL schema name (default: "public")
            
        Raises:
            psycopg2.Error: If insertion fails
        """
        if not nodes:
            print("No nodes to insert.")
            return
        
        conn = None
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(self.connection_string)
            cur = conn.cursor()
            
            # Prepare insert statement
            insert_sql = f"""
            INSERT INTO {schema_name}.{table_name} 
            (text, metadata_, node_id, embedding)
            VALUES (%s, %s, %s, %s)
            """
            
            # Prepare data for batch insert
            data_to_insert = []
            for node in nodes:
                # Extract node properties
                text = node.get_content(metadata_mode=MetadataMode.NONE)
                
                # Prepare metadata with _node_content (required by LlamaIndex)
                metadata_dict = dict(node.metadata) if node.metadata else {}
                # Add _node_content which LlamaIndex uses for retrieval
                metadata_dict["_node_content"] = json.dumps(node.get_metadata_str())
                metadata = json.dumps(metadata_dict)
                
                node_id = node.node_id
                
                # Get embedding - handle both direct embedding and embedding property
                embedding = None
                if hasattr(node, 'embedding') and node.embedding is not None:
                    embedding = node.embedding
                elif hasattr(node, 'get_embedding') and callable(node.get_embedding):
                    try:
                        embedding = node.get_embedding()
                    except Exception:
                        pass
                
                data_to_insert.append((text, metadata, node_id, embedding))
            
            # Batch insert for better performance
            execute_batch(cur, insert_sql, data_to_insert, page_size=100)
            
            conn.commit()
            cur.close()
            
            print(f"Successfully inserted {len(nodes)} nodes into {schema_name}.{table_name}")
            
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Error inserting nodes: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def table_exists(
        self,
        table_name: str,
        schema_name: str = "public",
    ) -> bool:
        """Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check
            schema_name: PostgreSQL schema name (default: "public")
            
        Returns:
            True if table exists, False otherwise
        """
        conn = None
        try:
            conn = psycopg2.connect(self.connection_string)
            cur = conn.cursor()
            
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = %s 
                    AND table_name = %s
                );
            """, (schema_name, table_name))
            
            result = cur.fetchone()
            exists = result[0] if result else False
            cur.close()
            
            return exists
            
        except psycopg2.Error as e:
            print(f"Error checking table existence: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_table_count(
        self,
        table_name: str,
        schema_name: str = "public",
    ) -> int:
        """Get the number of rows in a table.
        
        Args:
            table_name: Name of the table
            schema_name: PostgreSQL schema name (default: "public")
            
        Returns:
            Number of rows in the table
        """
        conn = None
        try:
            conn = psycopg2.connect(self.connection_string)
            cur = conn.cursor()
            
            cur.execute(f"SELECT COUNT(*) FROM {schema_name}.{table_name};")
            result = cur.fetchone()
            count = result[0] if result else 0
            cur.close()
            
            return count
            
        except psycopg2.Error as e:
            print(f"Error getting table count: {e}")
            raise
        finally:
            if conn:
                conn.close()
