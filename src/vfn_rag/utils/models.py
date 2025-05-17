import os
from warnings import warn
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding


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


def get_azure_open_ai_embedding(model_id: str = "text-embedding-3-large"):
    endpoint = os.environ.get("AZURE_EMBEDDING_API_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-3-large" if model_id is None else model_id,
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )
    return embed_model