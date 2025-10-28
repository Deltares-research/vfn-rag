#%%
from dotenv import load_dotenv
from vfn_rag.retrieval.storage import Storage
from vfn_rag.indexing.index_manager import IndexManager
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
load_dotenv()
storage_dir = "./temp/storage"
#%%
llm = azure_open_ai()
embedding = get_azure_open_ai_embedding()
config = ConfigLoader(llm=llm, embedding=embedding)
config.set_custom_node_parser(sentence_splitter=True, 
                              chunk_size=512, 
                              chunk_overlap=10)
#%%
storage = Storage.create()
storage.save(storage_dir)
# storage = Storage.load(storage_dir)
#%% all files
data_path = "./data/temp"
# docs = storage.read_documents(data_path, recursive = True)
storage.setup_chunking_pipeline(data_path, config, show_progress=True)
nodes = storage.run_pipeline()
#%%
storage.docstore.add_documents(nodes)

storage.save(storage_dir)

#%% create Index
index_manager = IndexManager.create_from_storage(storage)

index = index_manager.indexes[-1]
query_engine = index.as_query_engine()

#%%
grounded_prompt = "Pretend that you are seagrass in the wadden sea and give truthful answers based on the report data. Do not hallucinate if no information is available."

# Combine the grounded prompt with the query
query = "Waardoor is klein zeegras verdwenen?"
query = f"{grounded_prompt} {query}"
response = query_engine.query(query)

print(response.response)