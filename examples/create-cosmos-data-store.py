#%%
from dotenv import load_dotenv

from vfn_rag.retrieval.storage import Storage, Database
from vfn_rag.indexing.index_manager import IndexManager
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding

from llama_index.core import VectorStoreIndex

load_dotenv()

#%%
llm = azure_open_ai()
embedding = get_azure_open_ai_embedding()
config = ConfigLoader(llm=llm, embedding=embedding)
config.set_custom_node_parser(sentence_splitter=True, 
                              chunk_size=512, 
                              chunk_overlap=10)
#%%
storage = Storage.create(database=Database.COSMOS)
#%% all files
data_path = "./data/temp"
nodes = storage.read_documents(data_path, recursive = True, node_parser=config.settings.node_parser)

#%% create Index
index = VectorStoreIndex(nodes, storage_context=storage.store)


#%% run queries
query_engine = index.as_query_engine()
response = query_engine.query("what are the core quadrants? ")
import textwrap

print(textwrap.fill(str(response), 100))
# %%
