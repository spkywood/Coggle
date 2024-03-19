"""
    Parent Child Chunks Retrieval
    自动合并检索器（父文档检索器）
"""

import warnings
warnings.filterwarnings("ignore")

from llama_index.readers.web import TrafilaturaWebReader

from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import IndexNode

docs = TrafilaturaWebReader().load_data(
    [
        "https://baike.baidu.com/item/ChatGPT/62446358",
        "https://baike.baidu.com/item/%E6%81%90%E9%BE%99/139019"
    ]
)

# print(docs)

# 创建文档切分器
node_parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
doc_node = node_parser.get_nodes_from_documents(documents=docs)

# print(len(doc_node))

# 设置Embedding和LLM模型
import torch
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.settings import Settings
from transformers import AutoTokenizer, AutoModelForCausalLM

llm_model_path = "/home/wangxh/workspace/model/chatglm3-6b"
embedding_model_path = "/home/wangxh/workspace/model/paraphrase-multilingual-MiniLM-L12-v2"

model_kwargs = {'device' : 'cuda'}

tokenizer = AutoTokenizer.from_pretrained(llm_model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(llm_model_path, trust_remote_code=True).to(torch.bfloat16).cuda()
model = model.eval()
model_kwargs = {'device' : 'cuda'}

llm_model = HuggingFaceLLM(
    model= model,
    tokenizer= tokenizer,
)

embed_model = HuggingFaceEmbedding(
    model_name= embedding_model_path
)

embeddings = embed_model.get_text_embedding("Hello World!")

print(len(embeddings))
print(embeddings[:5])

"""
Instructor Embedding 带指令的Embedding:
    TypeError: INSTRUCTOR._load_sbert_model() got an unexpected keyword argument 'token'
    pip install sentence_transformers==2.2.2
"""

print("------------------\n")
from llama_index.embeddings.instructor import InstructorEmbedding

in_embed_model = InstructorEmbedding(
    model_name = "/home/wangxh/workspace/model/instructor-base"
)

embeddings = in_embed_model.get_text_embedding("Hello World!")
print(len(embeddings))
print(embeddings[:5])

"""
Optimum Embedding

Optimum in a HuggingFace library for exporting and running HuggingFace models in the ONNX format.

You can install the dependencies with pip install transformers optimum[exporters].

First, we need to create the ONNX model. ONNX models provide improved inference speeds, and can be used across platforms (i.e. in TransformersJS)
"""

# from llama_index.embeddings.huggingface_optimum import OptimumEmbedding

# OptimumEmbedding.create_and_save_optimum_model(
#     "BAAI/bge-small-en-v1.5", "./bge_onnx"
# )

# op_embed_model = OptimumEmbedding(folder_name="./bge_onnx")
# embeddings = op_embed_model.get_text_embedding("Hello World!")

# print(len(embeddings))
# print(embeddings[:5])
