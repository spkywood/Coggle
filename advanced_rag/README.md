# Advanced RAG 

## 检索前优化：句子窗口检索

您调整存储和后处理数据的方式。我们将使用 `SentenceWindowNodeParser` 来代替 `SimpleNodeParser。`

```Python
from llama_index.core.node_parser import SentenceWindowNodeParser

# create the sentence window node parser w/ default settings
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
```

`SentenceWindowNodeParser` 有两个功能：

- 将文档分离成单句，并嵌入其中。
- 为每个句子创建一个上下文窗口。如果指定 window_size = 3，则窗口长度为三个句子，从嵌入句子的前一个句子开始，横跨后一个句子。窗口将作为元数据存储。

在检索过程中，会返回与查询最匹配的句子。检索结束后，您需要定义一个 MetadataReplacementPostProcessor，并将其用于 node_postprocessors列表中，从而用元数据中的整个窗口替换该句子。

```Python
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

# The target key defaults to `window` to match the node_parser's default
postproc = MetadataReplacementPostProcessor(
    target_metadata_key="window"
)

...

query_engine = index.as_query_engine( 
    node_postprocessors = [postproc],
)
```


## 多路召回(混合搜索)

```Python
query_engine = index.as_query_engine(
    ...,
    vector_store_query_mode="hybrid", 
    alpha=0.5,
    ...
)
```

## 重排序


在高级 RAG 管道中添加重排器只需三个简单步骤：

1. 首先，定义 reranker 模型。在这里，我们使用的是 Hugging Face 中的 BAAI/bge-ranker-base 模型。
2. 在查询引擎中，将 reranker 模型添加到node_postprocessors列表中。
3. 增加查询引擎中的 similarity_top_k，以检索更多的上下文段落，重新排序后可将其减少到 top_n。

```Python
# !pip install torch sentence-transformers
from llama_index.core.postprocessor import SentenceTransformerRerank

# Define reranker model
rerank = SentenceTransformerRerank(
    top_n = 2, 
    model = "BAAI/bge-reranker-base"
)

...

# Add reranker to query engine
query_engine = index.as_query_engine(
  similarity_top_k = 6,
  ...,
                node_postprocessors = [rerank],
  ...,
)
```
