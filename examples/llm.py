from llm_rag.chat_model import get_data, create_index, setup_llm
CACHE_DIR = r"C:\MyComputer\llm\models"

documents = get_data() # rdir="examples/data/knowledge-base"
setup_llm(cache_dir=CACHE_DIR)
index = create_index(documents)
# %%
query_engine = index.as_query_engine()
"""
You have to start the server before running the query
ollama server --model llama3
"""
response = query_engine.query("What bird species exist in the netherlands?")
print(response)
response = query_engine.query("What are the bird species that exist in the netherlands?")
print(response)
response = query_engine.query("What are the bird species names that exist in the netherlands?")
print(response.response)

response = query_engine.query("are there any ducks in the netherlands?")
print(response)
print([response.metadata[key]["file_name"] for key in response.metadata.keys()])
# %%
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.4)],
)
