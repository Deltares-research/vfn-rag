import os
from warnings import warn
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.ollama import Ollama
from dllm_rag import __path__


def azure_open_ai(model_id: str = "gpt-4o", engine: str = "4o"):
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

    if endpoint is None or api_key is None or api_version is None:
        warn("Azure OpenAI environment variables are not set.")

    llm = AzureOpenAI(
        engine="4o" if engine is None else engine,
        model="gpt-4o" if model_id is None else model_id,  # o1-preview
        temperature=0.0,
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    return llm


def get_ollama_llm(model_id: str = "llama3"):
    """Get the Ollama LLM.

    Parameters
    ----------
    model_id: str, optional, default is "llama3"
        The model ID.

    Returns
    -------
    Ollama
        The Ollama LLM.
    """
    llm = Ollama(model=model_id, request_timeout=360.0)
    return llm


def get_hugging_face_embedding(
    model_name: str = "BAAI/bge-small-en-v1.5", cache_folder: str = None
) -> HuggingFaceEmbedding:
    """

    Parameters
    ----------
    model_name: str, optional, default is "BAAI/bge-base-en-v1.5"
        Name of the hugging face embedding model.
    cache_folder: str, optional, default is None
        Folder to cache the model. If not provided the function will search for
        - `LLAMA_INDEX_CACHE_DIR` in your environment variables.
        - `~/tmp/llama_index` if your OS is Linux.
        - `~/Library/Caches/llama_index` if your OS is MacOS.
        - `~/AppData/Local/llama_index` if your OS is Windows.

    Returns
    -------
    HuggingFaceEmbedding
        The hugging face embedding model.
    """
    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    except ImportError:
        raise ImportError(
            "Please install the `llama-index-embeddings-huggingface` package to use the Hugging Face embedding model."
        )

    embedding = HuggingFaceEmbedding(model_name=model_name, cache_folder=cache_folder)
    return embedding


def get_azure_open_ai_embedding(model_id: str = "text-embedding-3-large"):
    endpoint = os.environ["AZURE_EMBEDDING_API_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.environ["AZURE_OPENAI_API_VERSION"]

    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-3-large" if model_id is None else model_id,
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )
    return embed_model