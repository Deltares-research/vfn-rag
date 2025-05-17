from dotenv import load_dotenv
from vfn_rag.retrieval.storage import Storage
from vfn_rag.indexing.index_manager import IndexManager
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
load_dotenv()
storage_dir = "examples/pond/storage"
#%%
llm = azure_open_ai()
embedding = get_azure_open_ai_embedding()
config = ConfigLoader(llm=llm, embedding=embedding)
#%%
storage = Storage.create()
storage.save(storage_dir)
# storage = Storage.load(storage_dir)
#%% all files
data_path = "examples/data/pond"
docs = storage.read_documents(data_path, recursive = True)
#%%
storage.add_documents(docs, generate_id=False)
#%% create Index
index_manager = IndexManager.create_from_storage(storage)
#%% save the storage and index
storage.save(storage_dir)


#

