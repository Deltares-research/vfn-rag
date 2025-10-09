"""A module for managing vector Storage and retrieval."""

import os
from pathlib import Path
from typing import Sequence, Union, List
from openai import RateLimitError
import pandas as pd
from retry import retry
from llama_index.core.storage.docstore import SimpleDocumentStore, BaseDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.index_store.types import BaseIndexStore
from llama_index.core import StorageContext
from llama_index.core.schema import Document, TextNode, BaseNode
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.node_parser.interface import NodeParser
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    KeywordExtractor,
    SummaryExtractor,
)
from llama_index.readers.file import PDFReader
from vfn_rag.utils.helper_functions import generate_content_hash
from vfn_rag.utils.errors import StorageNotFoundError
from vfn_rag.retrieval.cosmos_storage import CosmosStorageContextFactory


EXTRACTORS = dict(
    text_splitter=TokenTextSplitter,
    title=TitleExtractor,
    question_answer=QuestionsAnsweredExtractor,
    summary=SummaryExtractor,
    keyword=KeywordExtractor,
)
ID_MAPPING_FILE = "metadata_index.csv"

from enum import Enum
class Database(Enum):
    COSMOS = "cosmos"
    POSTGRES = "postgres"
    LOCAL = "local"


class Storage:
    """A class to manage vector Storage and retrieval."""

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

    @classmethod
    def create(cls, database: Database=Database.LOCAL) -> "Storage":
        """Create a new instance of the Storage class."""
        if (database == Database.COSMOS):
            storage = CosmosStorageContextFactory(create_container=True).create_storage_context()
            return cls(storage)
        elif (database == Database.POSTGRES):
            raise NotImplementedError("Postgress storage is implemented yet.")
        storage = cls._create_simple_storage_context()
        return cls(storage)

    @staticmethod
    def _create_simple_storage_context() -> StorageContext:
        """Create a simple Storage context."""
        return StorageContext.from_defaults(
            docstore=SimpleDocumentStore(),
            vector_store=SimpleVectorStore(),
            index_store=SimpleIndexStore(),
        )

    @staticmethod
    def _create_metadata_index():
        """Create a metadata-based index."""
        """Create a metadata-based index."""
        return pd.DataFrame(columns=["file_name", "doc_id"])

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

    def save(self, store_dir: str):
        """Save the store to a directory.

        Parameters
        ----------
        store_dir: str
            The directory to save the store.

        Returns
        -------
        None
        """
        self.store.persist(persist_dir=store_dir)

    @classmethod
    def load(cls, store_dir: str="", database: Database=Database.LOCAL) -> "Storage":
        """Load the store from a directory.

        Parameters
        ----------
        store_dir: str
            The directory containing the store.

        Returns
        -------
        None
        """
        if (database == Database.POSTGRES):
            raise NotImplementedError("Postgress storage is implemented yet.")
        elif (database == Database.COSMOS):
            storage = CosmosStorageContextFactory().create_storage_context()
        elif (database == Database.LOCAL):
            if not Path(store_dir).exists():
                raise StorageNotFoundError(f"Storage not found at {store_dir}")
            storage = StorageContext.from_defaults(persist_dir=store_dir)
        return cls(storage)

    def add_documents(
        self,
        docs: Sequence[Union[Document, TextNode]],
        generate_id: bool = True,
        update: bool = False,
    ):
        """Add node/documents to the store.

            The `add_documents` method adds a node to the store. The node's id is a sha256 hash generated based on the
            node's text content. if the `update` parameter is True and the nodes already exist the existing node will
            be updated.

        Parameters
        ----------
        docs: Sequence[TextNode/Document]
            The node/documents to add to the store.
        generate_id: bool, optional, default is False.
            True if you want to generate a sha256 hash number as a doc_id based on the content of the nodes
        update: bool, optional, default is True.
            True to update the document in the docstore if it already exist.

        Returns
        -------
        None
        """
        new_entries = []
        file_names = []
        # Create a metadata-based index
        for doc in docs:
            # change the id to a sha256 hash if it is not already
            if generate_id:
                doc.node_id = generate_content_hash(doc.text)

            if not self.docstore.document_exists(doc.node_id) or update:
                self.docstore.add_documents([doc], allow_update=update)
                # Update the metadata index with file name as key and doc_id as value
                file_name = os.path.basename(doc.metadata["file_path"])
                if file_name in file_names:
                    file_name = f"{file_name}_{len(file_names)}"
                new_entries.append({"file_name": file_name, "doc_id": doc.node_id})
                file_names.append(file_name)
            else:
                print(f"Document with ID {doc.node_id} already exists. Skipping.")

        # Convert new entries to a DataFrame and append to the existing metadata DataFrame
        # if new_entries:
        #     new_entries_df = pd.DataFrame(new_entries)
        #     # self._metadata_index = pd.concat(
        #     #     [self._metadata_index, new_entries_df], ignore_index=True
        #     # )

    @retry(RateLimitError, tries=2, delay=60)
    @staticmethod
    def apply_extractor(nodes: List[BaseNode]) -> List[BaseNode]:
        """Apply the summary extractor to a list of nodes.

        Parameters
        ----------
        nodes: List[Node]
            The list of nodes to process.

        Returns
        -------
        List[Node]
            The list of processed nodes.
        """
        all_summaries = SummaryExtractor().extract(nodes)
        for node, summary in zip(nodes, all_summaries):
            node.metadata["summary"] = summary.get("section_summary", "")
        return nodes

    @staticmethod
    def read_documents(
        path: str,
        show_progres: bool = False,
        num_workers: int = None,
        recursive: bool = False,
        node_parser: NodeParser = Settings.node_parser,
        **kwargs,
    ) -> List[Union[Document, TextNode]]:
        """Read documents from a directory.

        the `read_documents` method reads documents from a directory and returns a list of documents.
        the `doc_id` is sha256 hash number generated based on the document's text content.

        Parameters
        ----------
        path: str
            path to the directory containing the documents.
        show_progres: bool, optional, default is False.
            True to show progress bar.
        num_workers: int, optional, default is None.
            The number of workers to use for loading the data.
        recursive: bool, optional, default is False.
            True to read from subdirectories.

        Returns
        -------
        Sequence[Union[Document, TextNode]]
            The documents/nodes read from the store.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")

        pdf_reader = PDFReader(return_full_document=True)
        reader = SimpleDirectoryReader(path, 
                                       recursive=recursive, 
                                       file_extractor={".pdf": pdf_reader}, 
                                       **kwargs)
        documents = reader.load_data(
            show_progress=show_progres, num_workers=num_workers, **kwargs
        )

        nodes = node_parser.get_nodes_from_documents(documents, show_progress=show_progres)
        # nodes = Storage.apply_extractor(nodes)

        for node in nodes:
            # exclude the file name from the llm metadata in order to avoid affecting the llm by weird file names
            node.excluded_llm_metadata_keys = ["file_name"]
            # exclude the file name from the embeddings metadata in order to avoid affecting the llm by weird file names
            node.excluded_embed_metadata_keys = ["file_name"]
            # Generate a hash based on the document's text content
            if (node is TextNode):
                content_hash = generate_content_hash(node.text)
                # Assign the hash as the doc_id
                node.doc_id = content_hash

        return nodes
