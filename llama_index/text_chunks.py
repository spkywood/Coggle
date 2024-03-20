"""
Text Chunk:
    - Embedding-based
    - Model-based
    - LLM-based
"""

from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)

data_path = './data'
documents = SimpleDirectoryReader(data_path).load_data()

# print(documents[0])

'''
    方法一：基于嵌入模型
'''
embed_model = HuggingFaceEmbedding(
    model_name= "/home/wangxh/workspace/model/paraphrase-multilingual-MiniLM-L12-v2"    # model path。
)

splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)

nodes = splitter.get_nodes_from_documents(documents)

# print(len(nodes))
# for node in nodes:
#     print('-' * 20)
#     print(node.get_content())

'''
     Naive BERT
      Cross Segment Attention
'''

from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline(
    task = Tasks.document_segmentation,
    model = 'damo/nlp_bert_document-segmentation_english-base',
    device='gpu',
)

print('-' * 10)

result = p([doc.get_content() for doc in documents])

# print(result[OutputKeys.TEXT])

"""
基于LLM的方法
"""

from llama_index.core import PromptTemplate

PROPOSITIONS_PROMPT = PromptTemplate(
    """Decompose the "Content" into clear and simple propositions, ensuring they are interpretable out of
context.
1. Split compound sentence into simple sentences. Maintain the original phrasing from the input
whenever possible.
2. For any named entity that is accompanied by additional descriptive information, separate this
information into its own distinct proposition.
3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences
and replacing pronouns (e.g., "it", "he", "she", "they", "this", "that") with the full name of the
entities they refer to.
4. Present the results as a list of strings, formatted in JSON.

Input: Title: ¯Eostre. Section: Theories and interpretations, Connection to Easter Hares. Content:
The earliest evidence for the Easter Hare (Osterhase) was recorded in south-west Germany in
1678 by the professor of medicine Georg Franck von Franckenau, but it remained unknown in
other parts of Germany until the 18th century. Scholar Richard Sermon writes that "hares were
frequently seen in gardens in spring, and thus may have served as a convenient explanation for the
origin of the colored eggs hidden there for children. Alternatively, there is a European tradition
that hares laid eggs, since a hare’s scratch or form and a lapwing’s nest look very similar, and
both occur on grassland and are first seen in the spring. In the nineteenth century the influence
of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular throughout Europe.
German immigrants then exported the custom to Britain and America where it evolved into the
Easter Bunny."
Output: [ "The earliest evidence for the Easter Hare was recorded in south-west Germany in
1678 by Georg Franck von Franckenau.", "Georg Franck von Franckenau was a professor of
medicine.", "The evidence for the Easter Hare remained unknown in other parts of Germany until
the 18th century.", "Richard Sermon was a scholar.", "Richard Sermon writes a hypothesis about
the possible explanation for the connection between hares and the tradition during Easter", "Hares
were frequently seen in gardens in spring.", "Hares may have served as a convenient explanation
for the origin of the colored eggs hidden in gardens for children.", "There is a European tradition
that hares laid eggs.", "A hare’s scratch or form and a lapwing’s nest look very similar.", "Both
hares and lapwing’s nests occur on grassland and are first seen in the spring.", "In the nineteenth
century the influence of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular
throughout Europe.", "German immigrants exported the custom of the Easter Hare/Rabbit to
Britain and America.", "The custom of the Easter Hare/Rabbit evolved into the Easter Bunny in
Britain and America." ]

Input: {node_text}
Output:"""
)

from llama_index.core.llama_pack import download_llama_pack, BaseLlamaPack
from typing import List, Optional
from llama_index.core.schema import Document
from llama_index.core.llms import LLM
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.node_parser import TextSplitter
from llama_index.core.service_context import ServiceContext
from llama_index.legacy.llms import OpenAI
from llama_index.legacy.embeddings import OpenAIEmbedding
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


"""
DenseXRetrievalPack = download_llama_pack(
    "DenseXRetrievalPack", "./dense_pack"
)

# If you have already downloaded DenseXRetrievalPack, you can import it directly.
from llama_index.packs.dense_x_retrieval import DenseXRetrievalPack

# Use LLM to extract propositions from every document/node
dense_pack = DenseXRetrievalPack(documents)

response = dense_pack.run("YOUR_QUERY")
#    通过上述测试代码，学会了初步使用类DenseXRetrievalPack，下面分析一下类DenseXRetrievalPack的源代码：

class DenseXRetrievalPack(BaseLlamaPack):
    def __init__(
        self,
        documents: List[Document],
        proposition_llm: Optional[LLM] = None,
        query_llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        text_splitter: TextSplitter = SentenceSplitter(),
        similarity_top_k: int = 4,
    ) -> None:

        self._proposition_llm = proposition_llm or OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=750,
        )

        embed_model = embed_model or OpenAIEmbedding(embed_batch_size=128)

        nodes = text_splitter.get_nodes_from_documents(documents)
        sub_nodes = self._gen_propositions(nodes)

        all_nodes = nodes + sub_nodes
        all_nodes_dict = {n.node_id: n for n in all_nodes}

        service_context = ServiceContext.from_defaults(
            llm=query_llm or OpenAI(),
            embed_model=embed_model,
            num_output=self._proposition_llm.metadata.num_output,
        )

        self.vector_index = VectorStoreIndex(
            all_nodes, service_context=service_context, show_progress=True
        )

        self.retriever = RecursiveRetriever(
            "vector",
            retriever_dict={
                "vector": self.vector_index.as_retriever(
                    similarity_top_k=similarity_top_k
                )
            },
            node_dict=all_nodes_dict,
        )

        self.query_engine = RetrieverQueryEngine.from_args(
            self.retriever, service_context=service_context
        )

"""