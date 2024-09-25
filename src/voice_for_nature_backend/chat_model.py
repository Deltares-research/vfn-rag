from typing import List
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from . import __path__


def get_data(rdir: str = None) -> List[Document]:
    """Load documents from a directory.

    Parameters
    ----------
    rdir : str, optional, default is None.
        Directory path

    Returns
    -------
    List[Document]
        List of documents
    """

    if rdir is None:
        rdir = f"{__path__[0]}/data"
    documents = SimpleDirectoryReader(rdir).load_data()
    return documents


def create_index(documents: List[Document]) -> VectorStoreIndex:
    """Create an index from a list of documents.

    Parameters
    ----------
    documents : List[Document]
        List of documents

    Returns
    -------
    VectorStoreIndex
        VectorStoreIndex object
    """

    index = VectorStoreIndex.from_documents(
        documents,
    )
    return index


def setup_llm(
    llm_model_id: str = "llama3",
    embedding_model_id: str = "BAAI/bge-base-en-v1.5",
    cache_dir: str = None,
):
    """Setup the LLM and embedding model.

    Parameters
    ----------
    llm_model_id : str, optional, default is "llama3".
        LLM model id
    embedding_model_id : str, optional, default is "BAAI/bge-base-en-v1.5".
        Embedding model id
    cache_dir : str, optional, default is None.
        Cache directory for the embedding model

    Returns
    -------
    None
    """
    # bge-base embedding model
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embedding_model_id, cache_folder=cache_dir
    )

    # ollama
    Settings.llm = Ollama(model=llm_model_id, request_timeout=360.0)
