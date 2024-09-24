from typing import List
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document
from . import __path__


def get_data(rdir: str = None) -> List[Document]:
    if rdir is None:
        rdir = f"{__path__[0]}/data"
    documents = SimpleDirectoryReader(rdir).load_data()
    return documents
