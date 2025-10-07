import os
from warnings import warn
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding


def azure_open_ai():
    endpoint = os.environ.get("AZURE_OPENAI_BASE")
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    api_version = os.environ.get("AZURE_OPENAI_VERSION")
    engine = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    model = os.environ.get("AZURE_OPENAI_MODEL")

    if endpoint is None or api_key is None or api_version is None or engine is None or model is None:
        warn("Azure OpenAI environment variables are not set.")

    llm = AzureOpenAI(
        engine=engine,
        model=model,
        temperature=0.0,
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    return llm


def get_azure_open_ai_embedding():
    endpoint = os.environ.get("AZURE_OPENAI_BASE")
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    api_version = os.environ.get("AZURE_OPENAI_VERSION")
    model = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL")
    deployment_name = os.environ.get("AZURE_EMBED_DEPLOYMENT_NAME")

    if endpoint is None or api_key is None or api_version is None or model is None or deployment_name is None:
        warn("Azure OpenAI Embedding environment variables are not set.")

    embed_model = AzureOpenAIEmbedding(
        model=model,
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
        deployment_name=deployment_name,
    )
    return embed_model