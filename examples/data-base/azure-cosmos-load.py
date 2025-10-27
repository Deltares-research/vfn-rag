# Azure Cosmos DB No SQL Vector Store
# in this script we will load an existing vector store index from a data stored in cosmos db.
#%%
import os
from llama_index.core import VectorStoreIndex
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
#%% connect to the cosmos db
# Here we establish the connection to cosmos db nosql and create a vector store index.
client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database_name = "vectorSearchDB"
container_name = "vectorSearchContainer"


storage_context = Cosmos.load(
    database_name, container_name, client
)
store = storage_context.store
#%% load index
index = VectorStoreIndex.from_vector_store(vector_store=store.vector_store, embed_model=embed_model)

#%% Query the index
# We can now ask questions using our index.
#%%
query_engine = index.as_query_engine()
response = query_engine.query("what is the history of the deltares pond?")
print(response)