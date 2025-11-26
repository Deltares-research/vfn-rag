"""Upload module for database management.

This module provides database management utilities separate from LlamaIndex
retrieval functionalities. It includes classes for managing PostgreSQL databases,
creating tables, and uploading data directly.
"""

from vfn_rag.upload.postgres_manager import PostgresManager

__all__ = ["PostgresManager"]
