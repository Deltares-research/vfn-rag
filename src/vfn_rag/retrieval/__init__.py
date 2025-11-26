"""Retrieval module for VFN RAG.

This module provides storage backends for vector stores and document retrieval.
"""

from vfn_rag.retrieval.base_storage import BaseStorage
from vfn_rag.retrieval.storage import Storage
from vfn_rag.retrieval.cosmos import Cosmos
from vfn_rag.retrieval.postgres import Postgres

__all__ = ["BaseStorage", "Storage", "Cosmos", "Postgres"]
