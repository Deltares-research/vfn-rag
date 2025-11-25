# PostgreSQL with pgvector Vector Store
# This script demonstrates how to load an existing vector store index from PostgreSQL.
# Make sure your PostgreSQL container is running before executing this script.
#%%
import os
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.retrieval.postgres import Postgres

#%%
load_dotenv()

# PostgreSQL connection settings (Docker defaults)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "vector_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

#%% Setup Azure OpenAI
llm = azure_open_ai()
embed_model = get_azure_open_ai_embedding()
config = ConfigLoader(llm, embed_model)

#%% Connect to PostgreSQL
# Load the existing vector store from PostgreSQL
print("Loading vector store from PostgreSQL...")

storage_context = Postgres.load(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    table_name="deltares_vectors",
    schema_name="kb",
    embed_dim=3072,  # Must match the dimension used when creating
)

store = storage_context.store

#%% Load index
# Load the index from the existing vector store
index = VectorStoreIndex.from_vector_store(
    vector_store=store.vector_store, 
    embed_model=embed_model
)
print("Index loaded successfully!")

#%% Query the index
# We can now ask questions using our index.

# As a question answering engine
print("\n--- Question Answering Mode ---")
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the available info")
print("Response:")
print(response.response)

# As a chat engine
# print("\n--- Chat Mode ---")
# chat_engine = index.as_chat_engine()
# response = chat_engine.chat("What is the history of the Deltares pond?")
# print("Response:")
# print(response.response)

# # Follow-up question in chat mode
# response = chat_engine.chat("Tell me more about its significance")
# print("\nFollow-up Response:")
# print(response.response)

#%% Advanced: Query with similarity score
# You can also retrieve nodes with similarity scores
retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve("Deltares pond history")

print("\n--- Top 3 Similar Nodes ---")
for i, node in enumerate(nodes, 1):
    print(f"\nNode {i} (Score: {node.score:.4f}):")
    print(node.text[:200] + "...")
