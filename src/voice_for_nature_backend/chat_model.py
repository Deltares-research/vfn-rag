from typing import List
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.schema import Document
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
