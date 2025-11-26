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
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from dotenv import load_dotenv
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.upload.postgres_manager import PostgresManager

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
table_name = "vector_store"
schema_name = "raw_schema"

#%% Setup Azure OpenAI
llm = azure_open_ai()
embed_model = get_azure_open_ai_embedding(dimensions=1024)  # Set embedding dimension to 1024
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
pm = PostgresManager.from_params(host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD)

pm.create_table(
    table_name=table_name,
    schema_name=schema_name,
    embed_dim=1024,  # Dimension for text-embedding-3-large
)


#%% Create nodes
# Create the nodes (embedding documents) and store in PostgreSQL
pipeline = IngestionPipeline(
    documents=documents,
    transformations=[embed_model])

nodes = pipeline.run()
print(f"Created {len(nodes)} nodes.")

pm.insert_nodes(nodes, table_name=table_name, schema_name=schema_name)

# Verify insertion
count = pm.get_table_count(table_name=table_name, schema_name=schema_name)
print(f"\nTable now contains {count} rows.")