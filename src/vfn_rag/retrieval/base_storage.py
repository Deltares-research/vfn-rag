import os
from typing import Sequence, Union
from abc import ABC, abstractmethod
from llama_index.core import StorageContext
from llama_index.core.storage.index_store.types import BaseIndexStore
from llama_index.core.storage.docstore import BaseDocumentStore
from llama_index.core import StorageContext, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.schema import BaseNode
from llama_index.readers.file import PDFReader

from vfn_rag.utils.config_loader import ConfigLoader
from llama_index.core.extractors import (
    KeywordExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    TitleExtractor,
)


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
                f"Storage class should be instantiated using StorageContext object, given: {storage_backend}"
            )

        self._store = storage_backend

    @abstractmethod
    def create(self, *args, **kwargs) -> StorageContext:
        """Create the storage."""
        pass

    def save(self, *args, **kwargs):
        """Save the storage."""
        pass

    def load(self, *args, **kwargs):
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

    def setup_chunking_pipeline(
            self,
            path: str,
            config: ConfigLoader,
            show_progress: bool = False,
            summary_extractor: bool = False,
            title_extractor: bool = False,
            keyword_extractor: bool = False,
            questions_answered_extractor: bool = False,
            **kwargs
    ) -> None:
        """
        Sets up the chunking and ingestion pipeline for processing documents in a specified directory.
        This method initializes a document reader for the given path, loads documents (including PDFs),
        and constructs an ingestion pipeline with specified transformations and embedding models.
        The pipeline is stored in the instance for later use.
        Args:
            path (str): Path to the directory containing documents to process.
            config (ConfigLoader): Configuration object containing settings for node parsing and embedding.
            show_progress (bool, optional): Whether to display progress during document loading. Defaults to False.
            summary_extractor (bool, optional): Whether to include a summary extractor in the pipeline. Defaults to False.
            title_extractor (bool, optional): Whether to include a title extractor in the pipeline.
            keyword_extractor (bool, optional): Whether to include a keyword extractor in the pipeline. Defaults to False.
            questions_answered_extractor (bool, optional): Whether to include a questions answered extractor in the pipeline. Defaults to False.
            **kwargs: Additional keyword arguments passed to the document reader and loader.
        Raises:
            FileNotFoundError: If the specified directory does not exist.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")

        pdf_reader = PDFReader(return_full_document=True)
        reader = SimpleDirectoryReader(path, 
                                       file_extractor={".pdf": pdf_reader}, 
                                       filename_as_id=True,
                                       **kwargs)
        documents = reader.load_data(
            show_progress=show_progress, **kwargs
        )

        transformations = []
        transformations.append(config.settings.node_parser)
        if summary_extractor:
            transformations.append(SummaryExtractor())
        if title_extractor:
            transformations.append(TitleExtractor())
        if keyword_extractor:
            transformations.append(KeywordExtractor())
        if questions_answered_extractor:
            transformations.append(QuestionsAnsweredExtractor())
        transformations.append(config.settings.embed_model)

        pipeline = IngestionPipeline(
            transformations=transformations,
            vector_store=self.store.vector_store,
            documents=documents,
        )
        self.pipeline = pipeline

    def run_pipeline(self, show_progress: bool = False) -> Sequence[BaseNode]:
        """
        Executes the ingestion pipeline if it has been set up.
        Args:
            show_progress (bool, optional): If True, displays a progress indicator during pipeline execution. Defaults to False.
        Returns:
            Sequence[BaseNode]: A sequence of processed nodes resulting from the pipeline execution. Not needed when the vector store is directly available, for example in Cosmos storage.
        Raises:
            ValueError: If the ingestion pipeline has not been set up prior to calling this method.
        """
        if self.pipeline is None:
            raise ValueError("Ingestion pipeline not set up. Call setup_chunking_pipeline first.")
        
        return self.pipeline.run(show_progress=show_progress)

