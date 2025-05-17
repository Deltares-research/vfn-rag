from dotenv import load_dotenv

from vfn_rag.retrieval.storage import Storage
from vfn_rag.indexing.index_manager import IndexManager
from vfn_rag.utils.config_loader import ConfigLoader
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
load_dotenv()

#%%
llm = azure_open_ai()
embedding = get_azure_open_ai_embedding()
config_loader = ConfigLoader(llm=llm, embedding=embedding)
storage_path = r"examples/data/storage"
storage = Storage.load(storage_path)
index_manager = IndexManager.load_from_storage(storage)
#%%
index = index_manager.indexes[-1]
query_engine = index.as_query_engine()
user_prompt = "how is the deltares pond connected to the surrounding area?"
answer = query_engine.query(user_prompt)
print(answer.response)

reference_id = [
    answer.metadata[key]["file_name"] for key in answer.metadata.keys()
]
reference_text = [
    answer.source_nodes[i].text for i in range(len(answer.source_nodes))
]
score = [answer.source_nodes[i].score for i in range(len(answer.source_nodes))]

references = {
    f"{key}({round(score_i, 2)})": value
    for key, score_i, value in zip(reference_id, score, reference_text)
}
for key, value in references.items():
    print(f"{key}: {value}")