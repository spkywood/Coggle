'''
    Advanced RAG with LlamaIndex and Weaviate
'''

import llama_index
import weaviate
import torch
from importlib.metadata import version

print(f"LlamaIndex version: {version('llama_index')}")
print(f"Weaviate version: {version('weaviate-client')}")

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.settings import Settings
from transformers import AutoTokenizer, AutoModelForCausalLM

llm_model = "/home/wangxh/workspace/model/chatglm3-6b"
embedding_model = "/home/wangxh/workspace/model/paraphrase-multilingual-MiniLM-L12-v2"
model_kwargs = {'device' : 'cuda'}

tokenizer = AutoTokenizer.from_pretrained(llm_model, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(llm_model, trust_remote_code=True).to(torch.bfloat16).cuda()
model = model.eval()
model_kwargs = {'device' : 'cuda'}


Settings.llm = HuggingFaceLLM(
    tokenizer= tokenizer,
    model = model,
    model_kwargs = model_kwargs,
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name = embedding_model,
    cache_folder = embedding_model,
)

from llama_index.core import SimpleDirectoryReader

# Load data
documents = SimpleDirectoryReader(
        input_files=["./data/paul_graham_essay.txt"]
).load_data()

print(documents)

from llama_index.core.node_parser import SentenceWindowNodeParser

# create the sentence window node parser w/ default settings
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)

# Extract nodes from documents
nodes = node_parser.get_nodes_from_documents(documents)

# This block of code is for educational purposes 
# to showcase what the nodes looks like
i=10

print(f"Text: \n{nodes[i].text}")
print("------------------")
print(f"Window: \n{nodes[i].metadata['window']}")

# Connect to your Weaviate instance
client = weaviate.Client(
    embedded_options=weaviate.embedded.EmbeddedOptions(
        hostname='192.168.1.126',
        port=9091,
    ), 
)
print("------------------")

print(f"Client is ready: {client.is_ready()}")

# Print this line to get more information about the client
# client.get_meta()

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore

index_name = "MyExternalContext"

# Construct vector store
vector_store = WeaviateVectorStore(
    weaviate_client = client, 
    index_name = index_name
)

# Set up the storage for the embeddings
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# If an index with the same index name already exists within Weaviate, delete it
if client.schema.exists(index_name):
    client.schema.delete_class(index_name)

# Setup the index
# build VectorStoreIndex that takes care of chunking documents
# and encoding chunks to embeddings for future retrieval
index = VectorStoreIndex(
    nodes,
    storage_context = storage_context,
)

import json
response = client.schema.get(index_name)

print(json.dumps(response, indent=2))

from llama_index.core.postprocessor import MetadataReplacementPostProcessor

# The target key defaults to `window` to match the node_parser's default
postproc = MetadataReplacementPostProcessor(
    target_metadata_key="window"
)

# This block of code is for educational purposes 
# to showcase how the MetadataReplacementPostProcessor works
#from llama_index.core.schema import NodeWithScore
#from copy import deepcopy

#scored_nodes = [NodeWithScore(node=x, score=1.0) for x in nodes]
#nodes_old = [deepcopy(n) for n in nodes]
#replaced_nodes = postproc.postprocess_nodes(scored_nodes)

#print(f"Retrieved sentece: {nodes_old[i].text}")
#print("------------------")
#print(f"Replaced window: {replaced_nodes[i].text}")

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