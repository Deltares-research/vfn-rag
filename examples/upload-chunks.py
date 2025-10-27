#%%
from dotenv import load_dotenv

from vfn_rag.retrieval.cosmos import Cosmos
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding

from llama_index.core import VectorStoreIndex

#%%
load_dotenv()
llm = azure_open_ai()
embedding = get_azure_open_ai_embedding()
config = ConfigLoader(llm=llm, embedding=embedding)
config.set_custom_node_parser(sentence_splitter=True, 
                              chunk_size=1024, 
                              chunk_overlap=10)
#%%
cosmos_storage = Cosmos.create(database_name="vectorSearchDB", container_name="vectorSearchContainer")
data_path = "./data/temp"
cosmos_storage.setup_chunking_pipeline(data_path, config, show_progress=True)
cosmos_storage.run_pipeline()

#%% create Index
index = VectorStoreIndex.from_vector_store(vector_store=cosmos_storage.store.vector_store, embed_model=embedding)


#%%
# cosmos_storage = Cosmos.load(database_name="vectorSearchDB", container_name="vectorSearchContainer")
# index = VectorStoreIndex.from_vector_store(vector_store=cosmos_storage.store.vector_store, embed_model=embedding)

#%% run queries
query_engine = index.as_query_engine()
# %%
response = query_engine.query("what is chemtrend?")

print(response.response)

# %%
