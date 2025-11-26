# PostgreSQL with pgvector Vector Store
# This script demonstrates how to create a vector store index and store it in PostgreSQL.
# Before running this script, start a PostgreSQL container with pgvector:
#
# docker run -d \
#   --name postgres-pgvector \
#   -e POSTGRES_PASSWORD=password \
#   -e POSTGRES_USER=postgres \
#   -e POSTGRES_DB=vector_db \
#   -p 5432:5432 \
#   pgvector/pgvector:pg16
#
#%%
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.retrieval.postgres import Postgres

#%%
load_dotenv()

# PostgreSQL connection settings (Docker defaults)
# You can also set these as environment variables:
# POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "vector_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

#%% Setup Azure OpenAI
llm = azure_open_ai()
embed_model = get_azure_open_ai_embedding()
config = ConfigLoader(llm, embed_model)

#%% Loading Documents
# In this example we will be using the deltares pond history document
# which will be processed by the SimpleDirectoryReader.

documents = SimpleDirectoryReader(
    input_dir=r"../data/knowledge-base/"
).load_data()

print("Document ID:", documents[0].doc_id)

#%% Connect to PostgreSQL
# Here we establish the connection to PostgreSQL and create a vector store.
# This will automatically:
# - Create the table if it doesn't exist
# - Set up the pgvector extension
# - Create appropriate indexes for vector similarity search

storage_context = Postgres.create(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    schema_name="kb",
    embed_dim=3072,  # Dimension for text-embedding-3-large
)

store = storage_context.store

#%% Create index
# Create the vector store index from documents and store in PostgreSQL
print("Creating vector store index...")
#%% Create nodes
VectorStoreIndex.from_documents(
    documents, storage_context=store, show_progress=True
)
print("Index created successfully!")

#%% Query the index
# We can now ask questions using our index.
print("\nQuerying the index...")

# As a question answering engine
query_engine = index.as_query_engine()
response = query_engine.query("tell me about birds")
print("\nResponse:")
print(response.response)

#%% Verify data in PostgreSQL (optional)
# You can verify the data was stored by connecting to PostgreSQL:
# docker exec -it postgres-pgvector psql -U postgres -d vector_db
# Then run: SELECT COUNT(*) FROM public.deltares_vectors;
