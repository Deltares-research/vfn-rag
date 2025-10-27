# Azure Cosmos DB No SQL Vector Store
# in this script we will create a vector store index and store it in cosmos db nosql.
#%%
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
from vfn_rag.utils.config_loader import ConfigLoader
from azure.cosmos import CosmosClient
from vfn_rag.retrieval.cosmos import Cosmos
#%%
load_dotenv()
COSMOS_URI = os.getenv("AZURE_COSMOSDB_URI")
COSMOS_KEY = os.getenv("AZURE_COSMOSDB_KEY")
#%% Setup Azure OpenAI

llm = azure_open_ai()
embed_model = get_azure_open_ai_embedding()
config = ConfigLoader(llm, embed_model)

#%% Loading Documents
# In this example we will be using the paul_graham essay which will be processed by the SimpleDirectoryReader.

documents = SimpleDirectoryReader(
    input_files=[r"examples/data/pond/deltares-pond-history.txt"]
).load_data()

print("Document ID:", documents[0].doc_id)
#%% connect to the cosmos db
# Here we establish the connection to cosmos db nosql and create a vector store index.
client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database_name = "vectorSearchDB"
container_name = "vectorSearchContainer"


storage_context = Cosmos.load(
    database_name, container_name, client
)
store = storage_context.store
#%% create index
index = VectorStoreIndex.from_documents(
    documents, storage_context=store
)
#%% Query the index
# We can now ask questions using our index.
# as a question answering engine
query_engine = index.as_query_engine()
response = query_engine.query("what is the history of the deltares pond?")
print(response.response)

# as a chat engine
query_engine = index.as_chat_engine()
response = query_engine.query("what is the history of the deltares pond?")
print(response.response)