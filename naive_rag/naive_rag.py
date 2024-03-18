from langchain.chains import RetrievalQA
from LLM import ChatGLM_LLM
from langchain_community.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import os
from langchain.prompts import PromptTemplate

# 我们所构造的 Prompt 模板
template = """    使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”
    {context}
    问题: {question}
    有用的回答:
"""

if __name__ == '__main__':
    # 定义 Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="/home/wangxh/workspace/model/paraphrase-multilingual-MiniLM-L12-v2")

    # 向量数据库持久化路径
    persist_directory = 'data_base/vector_db/chroma'

    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    llm = ChatGLM_LLM(model_path = "/home/wangxh/workspace/model/chatglm3-6b")
    res = llm.invoke("你是谁")
    print(res)

    print("\n\n")
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],template=template)
    # invoke
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt":QA_CHAIN_PROMPT}
    )

    # 检索问答链回答效果
    question = "2020年水利工程工作主要包括哪些"
    result = qa_chain.invoke({"query": question})
    print("检索问答链回答 question 的结果：")
    print(result["result"])

    print("\n\n")

    # 仅 LLM 回答效果
    result_2 = llm.invoke(question)
    print("大模型回答 question 的结果：")
    print(result_2)
