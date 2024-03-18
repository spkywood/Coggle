'''
    Advanced RAG with LlamaIndex and Weaviate
'''

import llama_index
import weaviate
from importlib.metadata import version

print(f"LlamaIndex version: {version('llama_index')}")
print(f"Weaviate version: {version('weaviate-client')}")

# define Embedding Model and LLM

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
Settings.embed_model = OpenAIEmbedding()

# Load data

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(
        input_files=["./data/paul_graham_essay.txt"]
).load_data()

from llama_index.core.postprocessor import SentenceTransformerRerank

# BAAI/bge-reranker-base
# link: https://huggingface.co/BAAI/bge-reranker-base
rerank = SentenceTransformerRerank(
    top_n = 2,
    model = "BAAI/bge-reranker-base"
)

# The QueryEngine class is equipped with the generator
# and facilitates the retrieval and generation steps
query_engine = index.as_query_engine(
    similarity_top_k = 6,
    vector_store_query_mode="hybrid",
    alpha=0.5,
    node_postprocessors = [postproc, rerank],
)

# Use your Default RAG
response = query_engine.query(
    "What happened at Interleaf?"
)
print(str(response))

window = response.source_nodes[0].node.metadata["window"]
sentence = response.source_nodes[0].node.metadata["original_text"]

print(f"Window: {window}")
print("------------------")
print(f"Original Sentence: {sentence}")

##  References
# * [Llamaindex docs: Weaviate Vector Store](https://docs.llamaindex.ai/en/stable/examples/vector_stores/WeaviateIndexDemo.html)
# * [LlamaIndex docs: Metadata Replacement + Node Sentence Window](https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/MetadataReplacementDemo.html)
