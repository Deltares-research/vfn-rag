from typing import Any
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter
from vfn_rag.utils.models import get_azure_open_ai_embedding, azure_open_ai


class ConfigLoader:
    """A class or function to load configuration files (e.g., YAML, JSON)."""

    def __init__(
        self,
        llm: Any = None,
        embedding: Any = None,
    ):
        """Initialize the ConfigLoader class.

        Parameters
        ----------
        llm: Any, optional, default is llama3
            llm model to use.
        embedding: Any, optional, default is BAAI/bge-base-en-v1.5
            Embedding model to use.
        """
        if llm is None:
            llm = azure_open_ai()
        if embedding is None:
            embedding = get_azure_open_ai_embedding()

        Settings.embed_model = embedding
        Settings.llm = llm
        self._settings = Settings
        self._embedding = embedding
        self._llm = llm

    @property
    def settings(self):
        return self._settings

    @property
    def llm(self):
        return self._llm

    @llm.setter
    def llm(self, value):
        self._llm = value
        Settings.llm = value

    @property
    def embedding(self):
        return self._embedding

    @embedding.setter
    def embedding(self, value):
        self._embedding = value
        Settings.embed_model = value

    def set_custom_node_parser(self, sentence_splitter: bool=True, chunk_size: int=512, chunk_overlap: int=20):
        """Set a custom node parser for document splitting. (Has to be explicitly called when using a SimpleDirectoryReader)
        Parameters
        ----------
        sentence_splitter: bool, optional, default=True
            Whether to use SentenceSplitter or TokenTextSplitter.
        chunk_size: int, optional, default=512
            The size of each chunk.
        chunk_overlap: int, optional, default=20
            The overlap between chunks.
        """
        if sentence_splitter:
            splitter = SentenceSplitter()
        else:
            splitter = TokenTextSplitter()
        splitter.chunk_size = chunk_size
        splitter.chunk_overlap = chunk_overlap
        self.settings.node_parser = splitter
