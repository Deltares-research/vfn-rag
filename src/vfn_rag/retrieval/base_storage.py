from typing import Union
from abc import ABC, abstractmethod
from llama_index.core import StorageContext
from llama_index.core.storage.index_store.types import BaseIndexStore
from llama_index.core.storage.docstore import BaseDocumentStore


class BaseStorage(ABC):
    """Abstract base class for storage."""

    def __init__(
        self,
        storage_backend: Union[str, StorageContext] = None,
    ):
        """Initialize the Storage.

        Parameters
        ----------
        storage_backend: str, optional, default=None
            The desired vector Storage backend (e.g., Qdrant, FAISS). If none is provided, a simple Storage context
            will be created.
        """
        if not isinstance(storage_backend, StorageContext):
            raise ValueError(
                "Storage class should be instantiated using StorageContext object, given: {storage_backend}"
            )

        self._store = storage_backend

    @abstractmethod
    def create(self) -> StorageContext:
        """Create the storage."""
        pass

    def save(self, store_dir: str):
        """Save the storage."""
        pass

    def load(self, store_dir: str):
        """Load the storage."""
        pass

    @property
    def store(self) -> StorageContext:
        """Get the Storage context."""
        return self._store

    @property
    def docstore(self) -> BaseDocumentStore:
        """Get the document store."""
        return self.store.docstore

    @property
    def vector_store(self):
        return self.store.vector_store

    @property
    def index_store(self) -> BaseIndexStore:
        return self.store.index_store


