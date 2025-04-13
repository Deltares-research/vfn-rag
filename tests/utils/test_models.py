import pytest
from unittest.mock import MagicMock, patch
from llama_index.llms.ollama import Ollama
from dllm_rag.utils.models import (
    get_ollama_llm,
    azure_open_ai,
    get_hugging_face_embedding,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def test_get_ollama_llm():
    llm = get_ollama_llm()
    assert isinstance(llm, Ollama)
    assert llm.context_window == 3900
    assert llm.model == "llama3"
    assert llm.request_timeout == pytest.approx(360.0)
    assert llm.temperature == pytest.approx(0.75)
    assert llm is not None


def test_azure_open_ai():
    with pytest.warns(
        UserWarning, match="Azure OpenAI environment variables are not set."
    ):
        llm = azure_open_ai()
        assert llm.temperature == 0
        assert llm.model == "gpt-4o"
        assert llm.engine == "4o"


def test_embedding():
    model = get_hugging_face_embedding()
    assert isinstance(model, HuggingFaceEmbedding)
    assert model.model_name == "BAAI/bge-small-en-v1.5"
    assert model.cache_folder is None
    assert model.max_length == 512
