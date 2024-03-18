import os

from tqdm import tqdm
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

MODEL_PATH="model/paraphrase-multilingual-MiniLM-L12-v2"

def get_files(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            # 通过后缀名判断文件类型是否满足要求
            if filename.endswith(".md"):
                # 如果满足要求，将其绝对路径加入到结果列表
                file_list.append(os.path.join(filepath, filename))
            elif filename.endswith(".txt"):
                file_list.append(os.path.join(filepath, filename))
            elif filename.endswith(".pdf"):
                file_list.append(os.path.join(filepath, filename))
    return file_list

def get_text(file_list):
    docs = []
    # 遍历所有目标文件
    for file in tqdm(file_list):
        file_type = file.split('.')[-1]
        if file_type == 'md':
            loader = UnstructuredMarkdownLoader(file)
        elif file_type == 'txt':
            loader = UnstructuredFileLoader(file)
        elif file_type == 'pdf':
            loader = PDFMinerLoader(file)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue

        # print(file)
        # docs.extend(loader.load())
        try:
            docs.extend(loader.load())
        except:
            print(file)
    return docs


if __name__ == "__main__":
    file_list = get_files("/home/wangxh/dataDownload")
    docs = get_text(file_list)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    model_name = MODEL_PATH
    model_kwargs = {'device' : 'cuda'}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        cache_folder=MODEL_PATH,
        multi_process=False
    )

    # 定义持久化路径
    persist_directory = 'data_base/vector_db/chroma'
    # 加载数据库
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )
    # 将加载的向量数据库持久化到磁盘上
    vectordb.persist()
